import json
from typing import Dict, List, Optional
from dataclasses import dataclass
import aiohttp
import asyncio
from datetime import datetime, timedelta

@dataclass
class DocumentReference:
    title: str
    content: str
    url: str
    last_updated: datetime
    category: str

@dataclass
class SearchResult:
    references: List[DocumentReference]
    relevance_score: float
    timestamp: datetime

class SolanaDocumentRetriever:
    def __init__(self, agent_config: Dict):
        self.config = agent_config
        self.cache = {}
        self.cache_ttl = timedelta(hours=24)
        self.doc_sources = {
            "solana": "https://docs.solana.com",
            "anchor": "https://docs.rs/anchor-lang",
            "spl": "https://spl.solana.com",
        }
    
    async def query_documentation(self, query: str, category: Optional[str] = None) -> SearchResult:
        # Check cache first
        cache_key = f"{category}:{query}" if category else query
        if cache_key in self.cache:
            cached_result = self.cache[cache_key]
            if datetime.now() - cached_result.timestamp < self.cache_ttl:
                return cached_result
        
        # Perform documentation search based on category
        if category == "solana":
            results = await self._search_solana_docs(query)
        elif category == "anchor":
            results = await self._search_anchor_docs(query)
        elif category == "spl":
            results = await self._search_spl_docs(query)
        else:
            # Search all documentation sources
            results = await self._search_all_docs(query)
        
        search_result = SearchResult(
            references=results,
            relevance_score=self._calculate_relevance(query, results),
            timestamp=datetime.now()
        )
        
        # Cache the result
        self.cache[cache_key] = search_result
        return search_result

    async def _search_solana_docs(self, query: str) -> List[DocumentReference]:
        # Implement Solana documentation search
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.doc_sources['solana']}/api/search", 
                               params={"q": query}) as response:
                if response.status == 200:
                    data = await response.json()
                    return self._parse_solana_results(data)
        return []
    
    async def _search_anchor_docs(self, query: str) -> List[DocumentReference]:
        # Implement Anchor documentation search
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.doc_sources['anchor']}/search", 
                               params={"q": query}) as response:
                if response.status == 200:
                    data = await response.json()
                    return self._parse_anchor_results(data)
        return []
    
    async def _search_spl_docs(self, query: str) -> List[DocumentReference]:
        # Implement SPL documentation search
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.doc_sources['spl']}/search", 
                               params={"q": query}) as response:
                if response.status == 200:
                    data = await response.json()
                    return self._parse_spl_results(data)
        return []
    
    async def _search_all_docs(self, query: str) -> List[DocumentReference]:
        # Search all documentation sources concurrently
        tasks = [
            self._search_solana_docs(query),
            self._search_anchor_docs(query),
            self._search_spl_docs(query)
        ]
        results = await asyncio.gather(*tasks)
        # Combine and sort results by relevance
        combined_results = []
        for result_list in results:
            combined_results.extend(result_list)
        return sorted(combined_results, 
                     key=lambda x: self._calculate_doc_relevance(query, x),
                     reverse=True)
    
    def _calculate_relevance(self, query: str, references: List[DocumentReference]) -> float:
        # Calculate overall relevance score for search results
        if not references:
            return 0.0
        
        total_score = sum(self._calculate_doc_relevance(query, ref) 
                         for ref in references)
        return total_score / len(references)
    
    def _calculate_doc_relevance(self, query: str, doc: DocumentReference) -> float:
        # Calculate relevance score for individual document
        query_terms = set(query.lower().split())
        content_terms = set(doc.content.lower().split())
        title_terms = set(doc.title.lower().split())
        
        content_match = len(query_terms & content_terms) / len(query_terms)
        title_match = len(query_terms & title_terms) / len(query_terms)
        
        # Weight title matches more heavily
        return (0.7 * title_match) + (0.3 * content_match)
    
    def _parse_solana_results(self, data: Dict) -> List[DocumentReference]:
        # Parse Solana documentation search results
        references = []
        for item in data.get("items", []):
            references.append(DocumentReference(
                title=item.get("title", ""),
                content=item.get("content", ""),
                url=item.get("url", ""),
                last_updated=datetime.fromisoformat(item.get("last_updated", "")),
                category="solana"
            ))
        return references
    
    def _parse_anchor_results(self, data: Dict) -> List[DocumentReference]:
        # Parse Anchor documentation search results
        references = []
        for item in data.get("items", []):
            references.append(DocumentReference(
                title=item.get("title", ""),
                content=item.get("content", ""),
                url=item.get("url", ""),
                last_updated=datetime.fromisoformat(item.get("last_updated", "")),
                category="anchor"
            ))
        return references
    
    def _parse_spl_results(self, data: Dict) -> List[DocumentReference]:
        # Parse SPL documentation search results
        references = []
        for item in data.get("items", []):
            references.append(DocumentReference(
                title=item.get("title", ""),
                content=item.get("content", ""),
                url=item.get("url", ""),
                last_updated=datetime.fromisoformat(item.get("last_updated", "")),
                category="spl"
            ))
        return references
