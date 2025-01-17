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
    
    async def get_best_practices(self, topic: str) -> List[DocumentReference]:
        # Query best practices documentation
        query = f"best practices {topic}"
        results = await self.query_documentation(query)
        return [ref for ref in results.references if self._is_best_practice(ref)]
    
    async def get_error_solution(self, error_message: str) -> Optional[DocumentReference]:
        # Search for error solutions
        query = f"error {error_message}"
        results = await self.query_documentation(query)
        if results.references:
            return results.references[0]  # Return most relevant solution
        return None
    
    async def get_spl_token_standard(self, standard_name: Optional[str] = None) -> List[DocumentReference]:
        # Query SPL token standards
        query = f"SPL token standard {standard_name}" if standard_name else "SPL token standards"
        results = await self.query_documentation(query, category="spl")
        return results.references
    
    async def _search_solana_docs(self, query: str) -> List[DocumentReference]:
        # Mock implementation for testing
        return [
            DocumentReference(
                title="Token Program Guide",
                content="Comprehensive guide to the Solana Token Program",
                url="https://docs.solana.com/developing/programming-model/token",
                last_updated=datetime.now(),
                category="solana"
            ),
            DocumentReference(
                title="Best Practices",
                content="Security best practices for Solana development",
                url="https://docs.solana.com/developing/best-practices",
                last_updated=datetime.now(),
                category="solana"
            )
        ]
    
    async def _search_anchor_docs(self, query: str) -> List[DocumentReference]:
        # Mock implementation for testing
        return [
            DocumentReference(
                title="Anchor Framework Guide",
                content="Complete guide to Anchor development",
                url="https://docs.rs/anchor-lang/latest/anchor_lang",
                last_updated=datetime.now(),
                category="anchor"
            ),
            DocumentReference(
                title="Account Validation",
                content="Guide to account validation in Anchor",
                url="https://docs.rs/anchor-lang/latest/anchor_lang/accounts",
                last_updated=datetime.now(),
                category="anchor"
            )
        ]
    
    async def _search_spl_docs(self, query: str) -> List[DocumentReference]:
        # Mock implementation for testing
        return [
            DocumentReference(
                title="SPL Token Standard",
                content="Standard for SPL token implementation",
                url="https://spl.solana.com/token",
                last_updated=datetime.now(),
                category="spl"
            ),
            DocumentReference(
                title="Token Program Interface",
                content="Interface documentation for Token program",
                url="https://spl.solana.com/token/interface",
                last_updated=datetime.now(),
                category="spl"
            )
        ]
    
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
    
    def _is_best_practice(self, doc: DocumentReference) -> bool:
        # Determine if document is a best practice guide
        best_practice_keywords = {"best practice", "recommended", "guideline", 
                                "standard", "convention"}
        doc_text = f"{doc.title} {doc.content}".lower()
        return any(keyword in doc_text for keyword in best_practice_keywords)
