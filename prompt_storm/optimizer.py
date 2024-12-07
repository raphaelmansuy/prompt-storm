"""
Prompt Optimization Module.

This module provides functionality to optimize prompts using LiteLLM.
"""
from typing import Optional
from prompt_storm.models.config import OptimizationConfig
from prompt_storm.services.optimizer_service import OptimizerService
from prompt_storm.services.yaml_service import YAMLService

class PromptOptimizer:
    """Class for optimizing prompts using LiteLLM."""
    
    def __init__(self, config: Optional[OptimizationConfig] = None):
        """Initialize the prompt optimizer with optional configuration."""
        self.config = config or OptimizationConfig()
        self._optimizer_service = OptimizerService(self.config)
        self._yaml_service = YAMLService(self.config)

    def optimize(self, prompt: str, **kwargs) -> str:
        """
        Optimize the given prompt using LiteLLM.
        
        Args:
            prompt: The prompt to optimize
            **kwargs: Additional arguments to pass to the LiteLLM completion
        
        Returns:
            str: The optimized prompt
        """
        return self._optimizer_service.optimize(prompt, **kwargs)

    def format_to_yaml(self, prompt: str, **kwargs) -> str:
        """
        Format the given prompt to YAML.
        
        Args:
            prompt: The prompt to format
            **kwargs: Additional arguments to pass to the LiteLLM completion
            
        Returns:
            str: The formatted YAML string
        """
        return self._yaml_service.format_to_yaml(prompt, **kwargs)