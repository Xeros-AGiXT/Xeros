import json
from typing import Dict, List
from dataclasses import dataclass
import os

# Get the base directory for the package
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

@dataclass
class TestCase:
    name: str
    description: str
    test_code: str
    expected_result: str

class SolanaTestGenerator:
    def __init__(self, agent_config: Dict):
        self.config = agent_config
        self.load_prompts()
    
    def load_prompts(self):
        prompts_path = os.path.join(BASE_DIR, 'code_assistance_module/prompts/prompts.json')
        with open(prompts_path, 'r') as f:
            self.prompts = json.load(f)
    
    async def generate_tests(self, contract_code: str) -> List[TestCase]:
        # Use AGiXT's Smart Instruct to generate tests
        test_prompt = self.prompts['test_generation']['prompt'].format(
            contract_code=contract_code
        )
        
        test_cases = []
        
        # Generate unit tests
        unit_tests = await self._generate_unit_tests(contract_code)
        test_cases.extend(unit_tests)
        
        # Generate integration tests
        integration_tests = await self._generate_integration_tests(contract_code)
        test_cases.extend(integration_tests)
        
        # Generate security tests
        security_tests = await self._generate_security_tests(contract_code)
        test_cases.extend(security_tests)
        
        return test_cases
    
    async def _generate_unit_tests(self, contract_code: str) -> List[TestCase]:
        # Generate unit tests for each public function
        unit_tests = []
        
        # Basic functionality tests
        unit_tests.append(TestCase(
            name="test_initialization",
            description="Test contract initialization with valid parameters",
            test_code=self._generate_init_test(),
            expected_result="Contract initializes successfully"
        ))
        
        # Error case tests
        unit_tests.append(TestCase(
            name="test_invalid_parameters",
            description="Test contract initialization with invalid parameters",
            test_code=self._generate_invalid_params_test(),
            expected_result="Contract initialization fails with appropriate error"
        ))
        
        return unit_tests
    
    async def _generate_integration_tests(self, contract_code: str) -> List[TestCase]:
        # Generate integration tests
        integration_tests = []
        
        # Interaction with other programs
        integration_tests.append(TestCase(
            name="test_token_interaction",
            description="Test interaction with SPL Token program",
            test_code=self._generate_token_interaction_test(),
            expected_result="Token operations execute successfully"
        ))
        
        return integration_tests
    
    async def _generate_security_tests(self, contract_code: str) -> List[TestCase]:
        # Generate security-focused tests
        security_tests = []
        
        # Authority checks
        security_tests.append(TestCase(
            name="test_unauthorized_access",
            description="Test unauthorized access attempts",
            test_code=self._generate_unauthorized_access_test(),
            expected_result="Unauthorized access attempts are rejected"
        ))
        
        return security_tests
    
    def _generate_init_test(self) -> str:
        return """
        #[test]
        fn test_initialize() {
            let program = ProgramTest::new(
                "token_contract",
                program_id,
                processor!(process_instruction),
            );
            
            let (mut banks_client, payer, recent_blockhash) = program.start().unwrap();
            
            // Test initialization
            let decimals = 9;
            let mint = Keypair::new();
            let authority = Keypair::new();
            
            let accounts = Initialize {
                authority: authority.pubkey(),
                payer: payer.pubkey(),
                mint: mint.pubkey(),
                token_program: token::ID,
                system_program: system_program::ID,
                rent: rent::ID,
            };
            
            let instruction = initialize(accounts, decimals);
            let transaction = Transaction::new_signed_with_payer(
                &[instruction],
                Some(&payer.pubkey()),
                &[&payer, &authority],
                recent_blockhash,
            );
            
            banks_client.process_transaction(transaction).unwrap();
        }
        """
    
    def _generate_invalid_params_test(self) -> str:
        return """
        #[test]
        #[should_panic(expected = "Invalid parameters")]
        fn test_initialize_invalid_params() {
            // Similar to test_initialize but with invalid parameters
        }
        """
    
    def _generate_token_interaction_test(self) -> str:
        return """
        #[test]
        fn test_token_operations() {
            // Test token mint, transfer, burn operations
        }
        """
    
    def _generate_unauthorized_access_test(self) -> str:
        return """
        #[test]
        #[should_panic(expected = "Unauthorized")]
        fn test_unauthorized_access() {
            // Test unauthorized access attempts
        }
        """
