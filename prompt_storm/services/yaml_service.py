"""
Service for YAML formatting using LiteLLM.
"""
import litellm
from typing import Optional, Dict, Any
from prompt_storm.interfaces.service_interfaces import YAMLServiceInterface
from prompt_storm.models.config import YAMLConfig, OptimizationConfig
from prompt_storm.utils.response_processor import extract_content_from_completion, strip_markdown
from prompt_storm.utils.error_handler import handle_completion_error

class YAMLService(YAMLServiceInterface):
    """Service for YAML formatting."""
    
    def __init__(self, config: Optional[OptimizationConfig] = None):
        """Initialize the YAML service."""
        self.optimization_config = config or OptimizationConfig()
        self.yaml_config = YAMLConfig()
    
    def _prepare_completion_kwargs(self, **kwargs) -> Dict[str, Any]:
        """Prepare kwargs for completion API call."""
        return {
            "model": self.optimization_config.model,
            "temperature": self.optimization_config.temperature,
            "max_tokens": self.optimization_config.max_tokens,
            **kwargs
        }
    
    def _prepare_messages(self, prompt: str) -> list:
        """Prepare messages for completion API call."""
        yaml_prompt = self.yaml_config.template.format(prompt=prompt)
        return [
            {"role": "system", "content": "You are an expert at converting prompts into well-structured YAML format."},
            {"role": "user", "content": yaml_prompt}
        ]
    
    async def format_to_yaml(self, prompt: str, **kwargs) -> str:
        """
        Asynchronously format the given prompt to YAML.
        
        Args:
            prompt: The prompt to format
            **kwargs: Additional arguments to pass to the LiteLLM completion
        
        Returns:
            str: The formatted YAML string
        """
        try:
            completion_kwargs = self._prepare_completion_kwargs(**kwargs)
            messages = self._prepare_messages(prompt)
            
            response = await litellm.acompletion(
                messages=messages,
                **completion_kwargs
            )
            
            content = extract_content_from_completion(response)
            return strip_markdown(content)
        except Exception as e:
            raise handle_completion_error(e)
    
    def format_to_yaml_sync(self, prompt: str, **kwargs) -> str:
        """
        Synchronously format the given prompt to YAML.
        
        Args:
            prompt: The prompt to format
            **kwargs: Additional arguments to pass to the LiteLLM completion
        
        Returns:
            str: The formatted YAML string
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
