import json
from typing import Dict, List
from dataclasses import dataclass

@dataclass
class Solution:
    problem: str
    solution: str
    code_example: str
    references: List[str]

class SolanaProblemSolver:
    def __init__(self, agent_config: Dict):
        self.config = agent_config
        self.load_prompts()
        self.common_problems = self._initialize_common_problems()
    
    def load_prompts(self):
        with open('prompts.json', 'r') as f:
            self.prompts = json.load(f)
    
    def _initialize_common_problems(self) -> Dict[str, Solution]:
        return {
            "account_size_error": Solution(
                problem="Account size is too small for the data being stored",
                solution="Calculate correct account size including discriminator and all fields",
                code_example="""
                #[account]
                pub struct MyAccount {
                    pub data: Vec<u8>,
                }
                
                impl MyAccount {
                    pub fn get_space(data_size: usize) -> usize {
                        8 + // discriminator
                        4 + data_size // vec length + data
                    }
                }
                """,
                references=[
                    "https://docs.solana.com/developing/programming-model/accounts",
                    "https://docs.rs/anchor-lang/latest/anchor_lang/attr.account.html"
                ]
            ),
            "unauthorized_signer": Solution(
                problem="Transaction failed due to missing or invalid signer",
                solution="Ensure all required signers are included and properly validated",
                code_example="""
                #[derive(Accounts)]
                pub struct Initialize<'info> {
                    #[account(mut)]
                    pub authority: Signer<'info>,
                    // ... other accounts
                }
                
                // In your instruction
                require!(ctx.accounts.authority.key() == expected_authority, ErrorCode::Unauthorized);
                """,
                references=[
                    "https://docs.solana.com/developing/programming-model/accounts#signers",
                    "https://docs.rs/anchor-lang/latest/anchor_lang/derive.Accounts.html"
                ]
            ),
            "compute_budget": Solution(
                problem="Transaction exceeded compute budget",
                solution="Optimize compute-intensive operations and request additional compute units if needed",
                code_example="""
                use solana_program::compute_budget::ComputeBudgetInstruction;
                
                // Request additional compute units
                let compute_ix = ComputeBudgetInstruction::request_units(300_000);
                let message = Message::new(&[compute_ix, your_instruction], Some(&payer.pubkey()));
                """,
                references=[
                    "https://docs.solana.com/developing/programming-model/runtime",
                    "https://docs.rs/solana-program/latest/solana_program/compute_budget/index.html"
                ]
            )
        }
    
    async def find_solution(self, problem_description: str) -> Solution:
        # Use AGiXT's Smart Instruct to analyze problem and find solution
        for problem_type, solution in self.common_problems.items():
            if self._matches_problem(problem_description, problem_type):
                return solution
        
        # If no exact match found, generate custom solution
        return await self._generate_custom_solution(problem_description)
    
    def _matches_problem(self, description: str, problem_type: str) -> bool:
        # Implement problem matching logic
        keywords = {
            "account_size_error": ["account", "size", "too small", "space"],
            "unauthorized_signer": ["unauthorized", "signer", "permission"],
            "compute_budget": ["compute", "budget", "exceeded", "units"]
        }
        
        return any(keyword in description.lower() for keyword in keywords.get(problem_type, []))
    
    async def _generate_custom_solution(self, problem_description: str) -> Solution:
        # Use AGiXT's Smart Instruct to generate custom solution
        # This is a placeholder implementation
        return Solution(
            problem=problem_description,
            solution="Custom solution will be generated based on the specific problem",
            code_example="// Custom code example will be generated",
            references=["Relevant documentation links will be provided"]
        )
    
    def format_solution(self, solution: Solution) -> str:
        formatted_solution = f"""
# Problem
{solution.problem}

# Solution
{solution.solution}

# Code Example
```rust
{solution.code_example}
```

# References
"""
        for ref in solution.references:
            formatted_solution += f"- {ref}\n"
        
        return formatted_solution
