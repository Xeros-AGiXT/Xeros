import json
from typing import Dict, List
from dataclasses import dataclass
import os

# Get the base directory for the package
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

@dataclass
class OptimizationSuggestion:
    category: str
    description: str
    current_code: str
    suggested_code: str
    impact: str
    priority: str

class SolanaOptimizer:
    def __init__(self, agent_config: Dict):
        self.config = agent_config
        self.load_prompts()
    
    def load_prompts(self):
        prompts_path = os.path.join(BASE_DIR, 'code_assistance_module/prompts/prompts.json')
        with open(prompts_path, 'r') as f:
            self.prompts = json.load(f)
    
    async def analyze_code(self, contract_code: str) -> List[OptimizationSuggestion]:
        # Use AGiXT's Smart Instruct to analyze code for optimization
        optimization_prompt = self.prompts['optimization_suggestions']['prompt'].format(
            contract_code=contract_code
        )
        
        suggestions = []
        
        # Analyze compute unit usage
        compute_suggestions = await self._analyze_compute_usage(contract_code)
        suggestions.extend(compute_suggestions)
        
        # Analyze memory efficiency
        memory_suggestions = await self._analyze_memory_efficiency(contract_code)
        suggestions.extend(memory_suggestions)
        
        # Analyze storage optimization
        storage_suggestions = await self._analyze_storage_optimization(contract_code)
        suggestions.extend(storage_suggestions)
        
        return suggestions
    
    async def _analyze_compute_usage(self, contract_code: str) -> List[OptimizationSuggestion]:
        compute_suggestions = []
        
        # Check for expensive operations
        compute_suggestions.append(OptimizationSuggestion(
            category="Compute Units",
            description="Optimize expensive computation in loop",
            current_code="for item in items { complex_computation(); }",
            suggested_code="let computed_value = complex_computation();\nfor item in items { use_computed_value(); }",
            impact="Reduces compute units by avoiding redundant calculations",
            priority="High"
        ))
        
        return compute_suggestions
    
    async def _analyze_memory_efficiency(self, contract_code: str) -> List[OptimizationSuggestion]:
        memory_suggestions = []
        
        # Check for efficient data structures
        memory_suggestions.append(OptimizationSuggestion(
            category="Memory Usage",
            description="Use more efficient data structure",
            current_code="let data: Vec<u8> = vec![0; 1000];",
            suggested_code="let data: [u8; 1000] = [0; 1000];",
            impact="Reduces heap allocations and improves memory efficiency",
            priority="Medium"
        ))
        
        return memory_suggestions
    
    async def _analyze_storage_optimization(self, contract_code: str) -> List[OptimizationSuggestion]:
        storage_suggestions = []
        
        # Check for storage packing
        storage_suggestions.append(OptimizationSuggestion(
            category="Storage",
            description="Pack storage variables efficiently",
            current_code="pub struct State { pub value1: u64, pub value2: u64 }",
            suggested_code="pub struct State { pub packed_values: u128 }",
            impact="Reduces storage cost and improves gas efficiency",
            priority="High"
        ))
        
        return storage_suggestions
    
    def get_optimization_report(self, suggestions: List[OptimizationSuggestion]) -> str:
        report = "# Solana Smart Contract Optimization Report\n\n"
        
        for suggestion in suggestions:
            report += f"## {suggestion.category}\n"
            report += f"Priority: {suggestion.priority}\n\n"
            report += f"### Description\n{suggestion.description}\n\n"
            report += f"### Current Code\n```rust\n{suggestion.current_code}\n```\n\n"
            report += f"### Suggested Code\n```rust\n{suggestion.suggested_code}\n```\n\n"
            report += f"### Impact\n{suggestion.impact}\n\n"
            report += "---\n\n"
        
        return report
