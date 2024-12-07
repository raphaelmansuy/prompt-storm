"""
Service for optimizing prompts using LiteLLM.
"""
import litellm
from typing import Optional, Dict, Any
from prompt_storm.interfaces.service_interfaces import OptimizerServiceInterface
from prompt_storm.models.config import OptimizationConfig
from prompt_storm.utils.response_processor import extract_content_from_completion, strip_markdown
from prompt_storm.utils.error_handler import handle_completion_error

class OptimizerService(OptimizerServiceInterface):
    """Service for optimizing prompts."""
    
    def __init__(self, config: Optional[OptimizationConfig] = None):
        """Initialize the optimizer service."""
        self.config = config or OptimizationConfig()
    
    def _prepare_completion_kwargs(self, **kwargs) -> Dict[str, Any]:
        """Prepare kwargs for completion API call."""
        return {
            "model": self.config.model,
            "temperature": self.config.temperature,
            "max_tokens": self.config.max_tokens,
            **kwargs
        }
    
    def _prepare_messages(self, prompt: str) -> list:
        """Prepare messages for completion API call."""
        optimization_prompt = self.config.template.format(prompt=prompt)
        return [{"role": "user", "content": optimization_prompt}]
    
    def optimize(self, prompt: str, **kwargs) -> str:
        """
        Optimize the given prompt.
        
        Args:
            prompt: The prompt to optimize
            **kwargs: Additional arguments to pass to the LiteLLM completion
        
        Returns:
            str: The optimized prompt
        """
        try:
            completion_kwargs = self._prepare_completion_kwargs(**kwargs)
            messages = self._prepare_messages(prompt)
            
            response = litellm.completion(
                messages=messages,
                **completion_kwargs
            )
            
            content = extract_content_from_completion(response)
            return strip_markdown(content)
        except Exception as e:
            raise handle_completion_error(e)
