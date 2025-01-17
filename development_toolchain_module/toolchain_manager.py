import json
from typing import Dict, List, Optional
from dataclasses import dataclass
import asyncio
import logging
from datetime import datetime

@dataclass
class ToolchainCommand:
    command: str
    description: str
    usage_example: str
    context: str

@dataclass
class EnvironmentConfig:
    component: str
    version: str
    configuration: Dict
    dependencies: List[str]

@dataclass
class DeploymentStep:
    step_name: str
    commands: List[str]
    validation_checks: List[str]
    rollback_steps: List[str]

class ToolchainManager:
    def __init__(self, config_path: str):
        self.config = self._load_config(config_path)
        self.cli_commands = self._initialize_cli_commands()
        self.env_configs = self._initialize_env_configs()
        self.deployment_workflows = self._initialize_deployment_workflows()
        
    def _load_config(self, config_path: str) -> Dict:
        with open(config_path, 'r') as f:
            return json.load(f)
    
    def _initialize_cli_commands(self) -> Dict[str, ToolchainCommand]:
        return {
            "init": ToolchainCommand(
                command="solana-keygen new",
                description="Generate a new Solana keypair",
                usage_example="solana-keygen new -o keypair.json",
                context="Key Management"
            ),
            "build": ToolchainCommand(
                command="anchor build",
                description="Build Anchor program",
                usage_example="anchor build",
                context="Development"
            ),
            "deploy": ToolchainCommand(
                command="anchor deploy",
                description="Deploy Anchor program",
                usage_example="anchor deploy --provider.cluster devnet",
                context="Deployment"
            ),
            "test": ToolchainCommand(
                command="anchor test",
                description="Run Anchor tests",
                usage_example="anchor test",
                context="Testing"
            )
        }
    
    def _initialize_env_configs(self) -> Dict[str, EnvironmentConfig]:
        return {
            "solana": EnvironmentConfig(
                component="Solana CLI",
                version="1.14.x",
                configuration={
                    "network": "devnet",
                    "keypair_path": "~/.config/solana/id.json"
                },
                dependencies=["rust", "node"]
            ),
            "anchor": EnvironmentConfig(
                component="Anchor Framework",
                version="0.27.x",
                configuration={
                    "provider": {
                        "cluster": "localnet"
                    }
                },
                dependencies=["solana"]
            ),
            "rust": EnvironmentConfig(
                component="Rust",
                version="1.69.x",
                configuration={
                    "toolchain": "stable"
                },
                dependencies=[]
            )
        }
    
    def _initialize_deployment_workflows(self) -> Dict[str, List[DeploymentStep]]:
        return {
            "standard_deployment": [
                DeploymentStep(
                    step_name="Build",
                    commands=["anchor build"],
                    validation_checks=["check_build_artifacts"],
                    rollback_steps=["clean_artifacts"]
                ),
                DeploymentStep(
                    step_name="Test",
                    commands=["anchor test"],
                    validation_checks=["check_test_results"],
                    rollback_steps=[]
                ),
                DeploymentStep(
                    step_name="Deploy",
                    commands=["anchor deploy"],
                    validation_checks=["verify_deployment"],
                    rollback_steps=["revert_deployment"]
                )
            ]
        }
    
    async def get_cli_assistance(self, context: str, action: str) -> Optional[ToolchainCommand]:
        # Find relevant CLI command based on context and action
        for cmd in self.cli_commands.values():
            if context.lower() in cmd.context.lower() and action.lower() in cmd.description.lower():
                return cmd
        return None
    
    async def validate_environment(self) -> List[Dict[str, str]]:
        issues = []
        
        # Check each component
        for name, config in self.env_configs.items():
            # Verify version
            if not await self._check_component_version(name, config.version):
                issues.append({
                    "component": name,
                    "issue": f"Version mismatch. Expected {config.version}",
                    "solution": f"Install correct version using package manager"
                })
            
            # Check dependencies
            for dep in config.dependencies:
                if not await self._check_dependency(dep):
                    issues.append({
                        "component": name,
                        "issue": f"Missing dependency: {dep}",
                        "solution": f"Install {dep} using package manager"
                    })
        
        return issues
    
    async def get_deployment_guidance(self, deployment_type: str = "standard") -> List[Dict]:
        workflow = self.deployment_workflows.get(f"{deployment_type}_deployment")
        if not workflow:
            return []
        
        guidance = []
        for step in workflow:
            guidance.append({
                "step": step.step_name,
                "commands": step.commands,
                "validation": step.validation_checks,
                "rollback": step.rollback_steps
            })
        
        return guidance
    
    async def get_testnet_guide(self) -> Dict[str, str]:
        return {
            "setup": "solana config set --url https://api.devnet.solana.com",
            "airdrop": "solana airdrop 2",
            "deploy": "anchor deploy --provider.cluster devnet",
            "verify": "solana confirm -v <SIGNATURE>",
            "monitor": "solana logs <PROGRAM_ID>"
        }
    
    async def get_debug_recommendations(self, error_context: str) -> List[Dict[str, str]]:
        recommendations = []
        
        if "Build" in error_context:
            recommendations.append({
                "tool": "cargo-expand",
                "description": "Expand Rust macros for debugging",
                "installation": "cargo install cargo-expand",
                "usage": "cargo expand"
            })
        
        if "Runtime" in error_context:
            recommendations.append({
                "tool": "solana-program-test",
                "description": "Local testing environment",
                "installation": "Built into Solana",
                "usage": "Use in integration tests"
            })
        
        if "Transaction" in error_context:
            recommendations.append({
                "tool": "solana logs",
                "description": "Monitor program logs",
                "installation": "Part of Solana CLI",
                "usage": "solana logs <PROGRAM_ID>"
            })
        
        return recommendations
    
    async def _check_component_version(self, component: str, expected_version: str) -> bool:
        # Implement version checking logic
        return True  # Placeholder
    
    async def _check_dependency(self, dependency: str) -> bool:
        # Implement dependency checking logic
        return True  # Placeholder
    
    async def validate_deployment(self, signature: str) -> bool:
        # Implement deployment validation logic
        return True  # Placeholder
