import unittest
import asyncio
import json
import os
from datetime import datetime
from typing import Dict, List

# Import modules
from xeros.code_assistance_module.code_review import SolanaCodeReviewer
from xeros.code_assistance_module.test_generator import SolanaTestGenerator
from xeros.code_assistance_module.optimizer import SolanaOptimizer
from xeros.code_assistance_module.problem_solver import SolanaProblemSolver
from xeros.document_retrieval_module.document_retriever import SolanaDocumentRetriever
from xeros.development_toolchain_module.toolchain_manager import ToolchainManager
from xeros.development_toolchain_module.workflow_chains import WorkflowChainManager

class TestXerosAssistant(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Load configurations
        with open('/home/ubuntu/program1/xeros/agent_config/config.json', 'r') as f:
            cls.agent_config = json.load(f)
        
        # Initialize components
        cls.code_reviewer = SolanaCodeReviewer(cls.agent_config)
        cls.test_generator = SolanaTestGenerator(cls.agent_config)
        cls.optimizer = SolanaOptimizer(cls.agent_config)
        cls.problem_solver = SolanaProblemSolver(cls.agent_config)
        cls.doc_retriever = SolanaDocumentRetriever(cls.agent_config)
        cls.toolchain_manager = ToolchainManager('/home/ubuntu/program1/xeros/development_toolchain_module/config.json')
        cls.workflow_manager = WorkflowChainManager('/home/ubuntu/program1/xeros/development_toolchain_module/config.json')
    
    def setUp(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
    
    def tearDown(self):
        self.loop.close()
    
    def test_code_assistance_module(self):
        """Test code assistance functionality"""
        # Test code review
        with open('/home/ubuntu/program1/xeros/code_assistance_module/code_templates/token_contract.rs', 'r') as f:
            test_code = f.read()
        
        review_result = self.loop.run_until_complete(
            self.code_reviewer.review_code(test_code)
        )
        self.assertIsNotNone(review_result)
        self.assertTrue(len(review_result.security_issues) > 0)
        
        # Test test generation
        test_cases = self.loop.run_until_complete(
            self.test_generator.generate_tests(test_code)
        )
        self.assertIsNotNone(test_cases)
        self.assertTrue(len(test_cases) > 0)
        
        # Test optimization suggestions
        suggestions = self.loop.run_until_complete(
            self.optimizer.analyze_code(test_code)
        )
        self.assertIsNotNone(suggestions)
        self.assertTrue(len(suggestions) > 0)
    
    def test_document_retrieval_module(self):
        """Test document retrieval functionality"""
        # Test Solana documentation query
        query_result = self.loop.run_until_complete(
            self.doc_retriever.query_documentation("token program")
        )
        self.assertIsNotNone(query_result)
        self.assertTrue(len(query_result.references) > 0)
        
        # Test best practices retrieval
        practices = self.loop.run_until_complete(
            self.doc_retriever.get_best_practices("token contract")
        )
        self.assertIsNotNone(practices)
        self.assertTrue(len(practices) > 0)
        
        # Test error solution retrieval
        solution = self.loop.run_until_complete(
            self.doc_retriever.get_error_solution("Account size too small")
        )
        self.assertIsNotNone(solution)
    
    def test_toolchain_support_module(self):
        """Test development toolchain functionality"""
        # Test CLI assistance
        cli_help = self.loop.run_until_complete(
            self.toolchain_manager.get_cli_assistance("deployment", "deploy")
        )
        self.assertIsNotNone(cli_help)
        
        # Test environment validation
        env_issues = self.loop.run_until_complete(
            self.toolchain_manager.validate_environment()
        )
        self.assertIsNotNone(env_issues)
        
        # Test deployment guidance
        guidance = self.loop.run_until_complete(
            self.toolchain_manager.get_deployment_guidance()
        )
        self.assertIsNotNone(guidance)
        self.assertTrue(len(guidance) > 0)
    
    def test_workflow_chains(self):
        """Test workflow chain functionality"""
        # Test project initialization chain
        init_chain_id = self.loop.run_until_complete(
            self.workflow_manager.create_initialization_chain()
        )
        self.assertIsNotNone(init_chain_id)
        init_success = self.loop.run_until_complete(
            self.workflow_manager.execute_chain(init_chain_id)
        )
        self.assertTrue(init_success)
        init_status = self.workflow_manager.get_chain_status(init_chain_id)
        self.assertEqual(init_status['status'], 'completed')
        
        # Test deployment chain
        deploy_chain_id = self.loop.run_until_complete(
            self.workflow_manager.create_deployment_chain()
        )
        self.assertIsNotNone(deploy_chain_id)
        deploy_success = self.loop.run_until_complete(
            self.workflow_manager.execute_chain(deploy_chain_id)
        )
        self.assertTrue(deploy_success)
        deploy_status = self.workflow_manager.get_chain_status(deploy_chain_id)
        self.assertEqual(deploy_status['status'], 'completed')
        
        # Test diagnostic chain
        diag_chain_id = self.loop.run_until_complete(
            self.workflow_manager.create_diagnostic_chain()
        )
        self.assertIsNotNone(diag_chain_id)
        diag_success = self.loop.run_until_complete(
            self.workflow_manager.execute_chain(diag_chain_id)
        )
        self.assertTrue(diag_success)
        diag_status = self.workflow_manager.get_chain_status(diag_chain_id)
        self.assertEqual(diag_status['status'], 'completed')
        
        # Verify chain steps
        init_steps = init_status['steps']
        self.assertTrue(any(step['name'] == 'environment_check' for step in init_steps))
        self.assertTrue(any(step['name'] == 'template_generation' for step in init_steps))
        self.assertTrue(any(step['name'] == 'dependency_setup' for step in init_steps))
        
        deploy_steps = deploy_status['steps']
        self.assertTrue(any(step['name'] == 'code_review' for step in deploy_steps))
        self.assertTrue(any(step['name'] == 'test_validation' for step in deploy_steps))
        self.assertTrue(any(step['name'] == 'deployment_verification' for step in deploy_steps))
        
        diag_steps = diag_status['steps']
        self.assertTrue(any(step['name'] == 'error_collection' for step in diag_steps))
        self.assertTrue(any(step['name'] == 'log_analysis' for step in diag_steps))
        self.assertTrue(any(step['name'] == 'solution_recommendation' for step in diag_steps))
    
    def test_security_requirements(self):
        """Test security implementation"""
        # Test code review security checks
        with open('/home/ubuntu/program1/xeros/code_assistance_module/code_templates/token_contract.rs', 'r') as f:
            test_code = f.read()
        
        review_result = self.loop.run_until_complete(
            self.code_reviewer.review_code(test_code)
        )
        
        # Verify security checks are comprehensive
        security_issues = review_result.security_issues
        self.assertTrue(any(issue['type'] == 'access_control' for issue in security_issues))
        self.assertTrue(any(issue['type'] == 'input_validation' for issue in security_issues))
        self.assertTrue(any(issue['type'] == 'arithmetic' for issue in security_issues))
        
        # Test configuration security settings
        self.assertTrue(self.agent_config['security']['code_review_required'])
        self.assertTrue(self.agent_config['security']['keypair_encryption'])
        self.assertTrue(self.agent_config['security']['deployment_approval'])
        
        # Test sensitive data handling
        self.assertTrue(self.agent_config['security']['sensitive_data_handling']['encryption'])
        self.assertTrue(self.agent_config['security']['sensitive_data_handling']['secure_storage'])
        self.assertTrue(self.agent_config['security']['sensitive_data_handling']['access_control'])
        
        # Test deployment security
        deployment_config = self.toolchain_manager.config['deployment']['security']
        self.assertTrue(deployment_config['keypair_encryption'])
        self.assertTrue(deployment_config['deployment_approval_required'])
        
        # Test workflow chain security
        chain_id = self.loop.run_until_complete(
            self.workflow_manager.create_deployment_chain()
        )
        chain_status = self.workflow_manager.get_chain_status(chain_id)
        self.assertTrue(any(
            step['name'] == 'code_review' and step['required'] == True
            for step in chain_status['steps']
        ))
    
    def test_performance_requirements(self):
        """Test performance implementation"""
        # Test response optimization
        start_time = datetime.now()
        
        # Test parallel execution of multiple operations
        tasks = [
            self.doc_retriever.query_documentation("token program"),
            self.doc_retriever.get_best_practices("smart contract"),
            self.doc_retriever.get_error_solution("Account size too small"),
            self.test_generator.generate_tests("pub fn initialize() {}"),
            self.optimizer.analyze_code("pub fn transfer() {}")
        ]
        results = self.loop.run_until_complete(asyncio.gather(*tasks))
        
        # Verify all operations completed successfully
        self.assertTrue(all(result is not None for result in results))
        
        # Check response time
        execution_time = (datetime.now() - start_time).total_seconds()
        self.assertLess(execution_time, 5.0)  # Should complete within 5 seconds
        
        # Test resource management
        self.assertTrue(self.agent_config['performance']['response_optimization']['cache_enabled'])
        self.assertTrue(self.agent_config['performance']['response_optimization']['parallel_execution'])
        
        # Verify concurrent operations
        self.assertGreaterEqual(
            self.agent_config['performance']['resource_management']['max_concurrent_tasks'],
            len(tasks)
        )
        
        # Test memory management
        memory_limit = self.agent_config['performance']['resource_management']['max_memory']
        self.assertEqual(memory_limit, "1GB")  # Verify memory limit is set
        
        # Test cache efficiency
        cache_ttl = self.agent_config['performance']['response_optimization']['cache_ttl']
        self.assertGreater(cache_ttl, 0)  # Cache TTL should be positive
    
    def test_accuracy_requirements(self):
        """Test accuracy implementation"""
        # Test problem solving accuracy
        problem_desc = "Account size too small for data"
        solution = self.loop.run_until_complete(
            self.problem_solver.find_solution(problem_desc)
        )
        self.assertIsNotNone(solution)
        self.assertTrue(len(solution.code_example) > 0)
        self.assertTrue(len(solution.references) > 0)

        # Test code generation accuracy
        test_code = self.loop.run_until_complete(
            self.test_generator.generate_tests("pub fn initialize() {}")
        )
        self.assertTrue(any(t.name == "test_initialization" for t in test_code))
        self.assertTrue(all(len(t.test_code) > 0 for t in test_code))

        # Test documentation accuracy
        docs = self.loop.run_until_complete(
            self.doc_retriever.query_documentation("token program")
        )
        self.assertTrue(any(ref.title == "Token Program Guide" for ref in docs.references))
        self.assertTrue(all(ref.url.startswith("https://") for ref in docs.references))

        # Test workflow chain accuracy
        init_chain_id = self.loop.run_until_complete(
            self.workflow_manager.create_initialization_chain()
        )
        success = self.loop.run_until_complete(
            self.workflow_manager.execute_chain(init_chain_id)
        )
        self.assertTrue(success)
        status = self.workflow_manager.get_chain_status(init_chain_id)
        self.assertEqual(status['status'], 'completed')
        steps = status['steps']
        self.assertTrue(all(step['status'] == 'completed' for step in steps))

if __name__ == '__main__':
    unittest.main()
