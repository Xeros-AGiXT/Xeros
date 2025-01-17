import json
from typing import Dict, List, Set, Optional
from dataclasses import dataclass
import aiofiles
import asyncio
import logging
from datetime import datetime

@dataclass
class DocumentIndex:
    keywords: Set[str]
    category: str
    last_updated: datetime
    relevance: float
    document_id: str

class IndexManager:
    def __init__(self, config_path: str):
        self.config = self._load_config(config_path)
        self.indices: Dict[str, DocumentIndex] = {}
        self.update_task = None
    
    def _load_config(self, config_path: str) -> Dict:
        with open(config_path, 'r') as f:
            return json.load(f)
    
    async def start_update_task(self):
        if self.update_task is None:
            self.update_task = asyncio.create_task(self._periodic_update())
    
    async def stop_update_task(self):
        if self.update_task:
            self.update_task.cancel()
            try:
                await self.update_task
            except asyncio.CancelledError:
                pass
            self.update_task = None
    
    async def index_document(self, doc_id: str, content: str, category: str):
        # Extract keywords and create index
        keywords = self._extract_keywords(content)
        self.indices[doc_id] = DocumentIndex(
            keywords=keywords,
            category=category,
            last_updated=datetime.now(),
            relevance=1.0,
            document_id=doc_id
        )
    
    async def search(self, query: str, category: Optional[str] = None) -> List[str]:
        query_keywords = self._extract_keywords(query)
        results = []
        
        for doc_id, index in self.indices.items():
            if category and index.category != category:
                continue
            
            # Calculate relevance score
            relevance = self._calculate_relevance(query_keywords, index.keywords)
            if relevance >= self.config['search_settings']['min_relevance_score']:
                results.append((doc_id, relevance))
        
        # Sort by relevance and return document IDs
        results.sort(key=lambda x: x[1], reverse=True)
        return [doc_id for doc_id, _ in results[:self.config['search_settings']['max_results']]]
    
    def _extract_keywords(self, text: str) -> Set[str]:
        # Simple keyword extraction (can be enhanced with NLP)
        words = text.lower().split()
        # Remove common words and punctuation
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for'}
        return {word.strip('.,!?()[]{}') for word in words if word not in stop_words}
    
    def _calculate_relevance(self, query_keywords: Set[str], doc_keywords: Set[str]) -> float:
        if not query_keywords:
            return 0.0
        
        intersection = len(query_keywords & doc_keywords)
        return intersection / len(query_keywords)
    
    async def _periodic_update(self):
        while True:
            try:
                await self._update_indices()
                await asyncio.sleep(self.config['update_settings']['check_interval'])
            except asyncio.CancelledError:
                break
            except Exception as e:
                logging.error(f"Error during index update: {str(e)}")
                await asyncio.sleep(60)  # Wait before retrying
    
    async def _update_indices(self):
        # Update document indices
        for doc_id, index in self.indices.items():
            try:
                # Check if document needs updating
                if await self._should_update_index(index):
                    await self._update_document_index(doc_id)
            except Exception as e:
                logging.error(f"Error updating index for {doc_id}: {str(e)}")
    
    async def _should_update_index(self, index: DocumentIndex) -> bool:
        # Check if index is older than update interval
        age = datetime.now() - index.last_updated
        return age.total_seconds() >= self.config['update_settings']['check_interval']
    
    async def _update_document_index(self, doc_id: str):
        # Implement document update logic
        pass  # Placeholder for actual implementation
