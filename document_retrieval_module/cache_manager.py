import json
import os
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
import aiofiles
import asyncio
import logging

class DocumentCache:
    def __init__(self, config_path: str):
        self.config = self._load_config(config_path)
        self.cache_dir = os.path.join(os.path.dirname(__file__), "cache")
        self.ensure_cache_directory()
        self.cleanup_task = None
        
    def _load_config(self, config_path: str) -> Dict:
        with open(config_path, 'r') as f:
            return json.load(f)
    
    def ensure_cache_directory(self):
        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir)
    
    async def start_cleanup_task(self):
        if self.cleanup_task is None:
            self.cleanup_task = asyncio.create_task(self._periodic_cleanup())
    
    async def stop_cleanup_task(self):
        if self.cleanup_task:
            self.cleanup_task.cancel()
            try:
                await self.cleanup_task
            except asyncio.CancelledError:
                pass
            self.cleanup_task = None
    
    async def get(self, key: str) -> Optional[Dict]:
        cache_file = os.path.join(self.cache_dir, f"{key}.json")
        try:
            async with aiofiles.open(cache_file, 'r') as f:
                content = await f.read()
                data = json.loads(content)
                
                # Check if cache entry is still valid
                if self._is_cache_valid(data):
                    return data['content']
                else:
                    await self.delete(key)
                    return None
        except (FileNotFoundError, json.JSONDecodeError):
            return None
    
    async def set(self, key: str, value: Any):
        cache_file = os.path.join(self.cache_dir, f"{key}.json")
        cache_data = {
            'content': value,
            'timestamp': datetime.now().isoformat(),
            'ttl': self.config['cache_settings']['ttl_hours']
        }
        
        try:
            async with aiofiles.open(cache_file, 'w') as f:
                await f.write(json.dumps(cache_data))
        except Exception as e:
            logging.error(f"Failed to write cache file {cache_file}: {str(e)}")
    
    async def delete(self, key: str):
        cache_file = os.path.join(self.cache_dir, f"{key}.json")
        try:
            os.remove(cache_file)
        except FileNotFoundError:
            pass
    
    async def clear(self):
        for filename in os.listdir(self.cache_dir):
            if filename.endswith('.json'):
                await self.delete(filename[:-5])
    
    def _is_cache_valid(self, cache_data: Dict) -> bool:
        timestamp = datetime.fromisoformat(cache_data['timestamp'])
        ttl_hours = cache_data['ttl']
        return datetime.now() - timestamp < timedelta(hours=ttl_hours)
    
    async def _periodic_cleanup(self):
        while True:
            try:
                await self._cleanup_expired_entries()
                await asyncio.sleep(self.config['cache_settings']['cleanup_interval'])
            except asyncio.CancelledError:
                break
            except Exception as e:
                logging.error(f"Error during cache cleanup: {str(e)}")
                await asyncio.sleep(60)  # Wait before retrying
    
    async def _cleanup_expired_entries(self):
        for filename in os.listdir(self.cache_dir):
            if not filename.endswith('.json'):
                continue
                
            cache_file = os.path.join(self.cache_dir, filename)
            try:
                async with aiofiles.open(cache_file, 'r') as f:
                    content = await f.read()
                    data = json.loads(content)
                    
                    if not self._is_cache_valid(data):
                        await self.delete(filename[:-5])
            except Exception as e:
                logging.error(f"Error processing cache file {filename}: {str(e)}")
    
    async def get_cache_size(self) -> int:
        total_size = 0
        for filename in os.listdir(self.cache_dir):
            if filename.endswith('.json'):
                file_path = os.path.join(self.cache_dir, filename)
                total_size += os.path.getsize(file_path)
        return total_size
    
    async def ensure_cache_size_limit(self):
        max_size = self.config['cache_settings']['max_size_mb'] * 1024 * 1024
        current_size = await self.get_cache_size()
        
        if current_size > max_size:
            # Remove oldest entries until under limit
            cache_files = []
            for filename in os.listdir(self.cache_dir):
                if filename.endswith('.json'):
                    file_path = os.path.join(self.cache_dir, filename)
                    cache_files.append((
                        filename,
                        os.path.getmtime(file_path)
                    ))
            
            # Sort by modification time (oldest first)
            cache_files.sort(key=lambda x: x[1])
            
            # Remove files until under limit
            for filename, _ in cache_files:
                if current_size <= max_size:
                    break
                    
                file_path = os.path.join(self.cache_dir, filename)
                file_size = os.path.getsize(file_path)
                await self.delete(filename[:-5])
                current_size -= file_size
