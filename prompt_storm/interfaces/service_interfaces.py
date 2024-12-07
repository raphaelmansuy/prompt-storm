"""
Service interfaces for the prompt_storm package.
"""
from abc import ABC, abstractmethod

class OptimizerServiceInterface(ABC):
    """Interface for prompt optimization services."""
    
    @abstractmethod
    async def optimize(self, prompt: str, **kwargs) -> str:
        """Optimize the given prompt."""
        pass
    
    @abstractmethod
    def optimize_sync(self, prompt: str, **kwargs) -> str:
        """Synchronously optimize the given prompt."""
        pass

class YAMLServiceInterface(ABC):
    """Interface for YAML formatting services."""
    
    @abstractmethod
    async def format_to_yaml(self, prompt: str, **kwargs) -> str:
        """Format the given prompt to YAML."""
        pass
    
    @abstractmethod
    def format_to_yaml_sync(self, prompt: str, **kwargs) -> str:
        """Synchronously format the given prompt to YAML."""
        pass

class CSVServiceInterface(ABC):
    """Interface for CSV processing services."""
    
    @abstractmethod
    async def read_prompts(self, csv_path: str, prompt_column: str) -> list[str]:
        """Read prompts from CSV file."""
        pass

class BatchOptimizerServiceInterface(ABC):
    """Interface for batch optimization services."""
    
    @abstractmethod
    async def optimize_batch(
        self, 
        input_csv: str, 
        output_dir: str, 
        prompt_column: str
    ) -> dict[str, str]:
        """Optimize a batch of prompts from CSV and save to YAML files."""
        pass
