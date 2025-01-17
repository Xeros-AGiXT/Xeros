import json
from typing import Dict, List, Optional
from dataclasses import dataclass
import os

# Get the base directory for the package
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

@dataclass
class CodeReviewResult:
    security_issues: List[Dict[str, str]]
    performance_suggestions: List[Dict[str, str]]
    best_practices: List[Dict[str, str]]
    potential_warnings: List[Dict[str, str]]

class SolanaCodeReviewer:
    def __init__(self, agent_config: Dict):
        self.config = agent_config
        self.load_prompts()
    
    def load_prompts(self):
        prompts_path = os.path.join(BASE_DIR, 'code_assistance_module/prompts/prompts.json')
        with open(prompts_path, 'r') as f:
            self.prompts = json.load(f)
    
    async def review_code(self, code: str) -> CodeReviewResult:
        # Use AGiXT's Smart Instruct to analyze code
        review_prompt = self.prompts['code_review']['prompt'].format(code=code)
        
        # Security checks
        security_issues = await self._check_security(code)
        
        # Performance analysis
        performance_suggestions = await self._analyze_performance(code)
        
        # Best practices validation
        best_practices = await self._validate_best_practices(code)
        
        # Warning detection
        potential_warnings = await self._detect_warnings(code)
        
        return CodeReviewResult(
            security_issues=security_issues,
            performance_suggestions=performance_suggestions,
            best_practices=best_practices,
            potential_warnings=potential_warnings
        )
    
    async def _check_security(self, code: str) -> List[Dict[str, str]]:
        # Implement security checks
        security_issues = []
        
        # Check access control
        if "require!" in code:
            security_issues.append({
                "type": "access_control",
                "severity": "info",
                "description": "Access control check found using require! macro",
                "suggestion": "Ensure all sensitive operations are protected by appropriate checks"
            })
        
        # Check input validation
        if "pub fn" in code and "assert!" not in code:
            security_issues.append({
                "type": "input_validation",
                "severity": "medium",
                "description": "Function lacks input validation",
                "suggestion": "Add input validation using assert! or require!"
            })
        
        # Check arithmetic operations
        if "+" in code or "-" in code or "*" in code:
            security_issues.append({
                "type": "arithmetic",
                "severity": "medium",
                "description": "Potential integer overflow/underflow",
                "suggestion": "Use checked arithmetic operations"
            })
        
        # Check reentrancy
        if "invoke" in code and "mut" in code:
            security_issues.append({
                "type": "reentrancy",
                "severity": "high",
                "description": "Potential reentrancy vulnerability",
                "suggestion": "Implement checks-effects-interactions pattern"
            })
        
        return security_issues
    
    async def _analyze_performance(self, code: str) -> List[Dict[str, str]]:
        # Implement performance analysis
        performance_checks = [
            self._check_compute_units(code),
            self._check_memory_usage(code),
            self._check_storage_optimization(code)
        ]
        return [suggestion for check in performance_checks if (suggestion := check) is not None]
    
    async def _validate_best_practices(self, code: str) -> List[Dict[str, str]]:
        # Implement best practices validation
        practice_checks = [
            self._check_naming_conventions(code),
            self._check_error_handling(code),
            self._check_documentation(code)
        ]
        return [practice for check in practice_checks if (practice := check) is not None]
    
    async def _detect_warnings(self, code: str) -> List[Dict[str, str]]:
        # Implement warning detection
        warning_checks = [
            self._check_deprecated_features(code),
            self._check_potential_bugs(code),
            self._check_gas_inefficiencies(code)
        ]
        return [warning for check in warning_checks if (warning := check) is not None]
    
    # Individual check implementations
    def _check_access_control(self, code: str) -> Optional[Dict[str, str]]:
        # Implement access control checks
        pass
    
    def _check_input_validation(self, code: str) -> Optional[Dict[str, str]]:
        # Implement input validation checks
        pass
    
    def _check_arithmetic_operations(self, code: str) -> Optional[Dict[str, str]]:
        # Implement arithmetic operation checks
        pass
    
    def _check_reentrancy(self, code: str) -> Optional[Dict[str, str]]:
        # Implement reentrancy checks
        pass
    
    def _check_compute_units(self, code: str) -> Optional[Dict[str, str]]:
        # Implement compute units analysis
        pass
    
    def _check_memory_usage(self, code: str) -> Optional[Dict[str, str]]:
        # Implement memory usage analysis
        pass
    
    def _check_storage_optimization(self, code: str) -> Optional[Dict[str, str]]:
        # Implement storage optimization analysis
        pass
    
    def _check_naming_conventions(self, code: str) -> Optional[Dict[str, str]]:
        # Implement naming convention checks
        pass
    
    def _check_error_handling(self, code: str) -> Optional[Dict[str, str]]:
        # Implement error handling checks
        pass
    
    def _check_documentation(self, code: str) -> Optional[Dict[str, str]]:
        # Implement documentation checks
        pass
    
    def _check_deprecated_features(self, code: str) -> Optional[Dict[str, str]]:
        # Implement deprecated feature checks
        pass
    
    def _check_potential_bugs(self, code: str) -> Optional[Dict[str, str]]:
        # Implement potential bug detection
        pass
    
    def _check_gas_inefficiencies(self, code: str) -> Optional[Dict[str, str]]:
        # Implement gas inefficiency checks
        pass
