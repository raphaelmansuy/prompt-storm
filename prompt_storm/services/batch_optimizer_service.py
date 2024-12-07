"""
Service for batch optimization of prompts.
"""
import os
import asyncio
from pathlib import Path
from typing import Dict, List, Optional
import litellm
from prompt_storm.interfaces.service_interfaces import (
    BatchOptimizerServiceInterface,
    OptimizerServiceInterface,
    YAMLServiceInterface,
    CSVServiceInterface
)
from prompt_storm.models.config import OptimizationConfig
from prompt_storm.utils.logger import BatchProgressTracker, setup_logger

logger = setup_logger(__name__, verbose=False)

class BatchOptimizerService(BatchOptimizerServiceInterface):
    """Service for batch optimization of prompts."""
    
    def __init__(
        self,
        optimizer_service: OptimizerServiceInterface,
        yaml_service: YAMLServiceInterface,
        csv_service: CSVServiceInterface,
        config: Optional[OptimizationConfig] = None,
        verbose: bool = False
    ):
        """Initialize the batch optimizer service."""
        self.optimizer_service = optimizer_service
        self.yaml_service = yaml_service
        self.csv_service = csv_service
        self.config = config or OptimizationConfig()
        self.verbose = verbose
        global logger
        logger = setup_logger(__name__, verbose=verbose)
        
    async def _infer_category_and_name(self, prompt: str) -> tuple[str, str]:
        """
        Infer category and name for a prompt using LLM.
        
        Args:
            prompt: The prompt to categorize
            
        Returns:
            Tuple of (category, name)
        """
        messages = [
            {"role": "system", "content": "You are an expert at categorizing prompts. Respond with exactly two lines: first line is a single word category, second line is a short kebab-case name."},
            {"role": "user", "content": f"Categorize this prompt:\n{prompt}"}
        ]
        
        completion = await litellm.acompletion(
            model=self.config.model,
            messages=messages,
            temperature=0.3,
            max_tokens=50
        )
        
        response = completion.choices[0].message.content.strip().split('\n')
        if len(response) != 2:
            logger.warning(f"Invalid categorization response format: {response}")
            return "general", "unnamed-prompt"
            
        category, name = response
        if self.verbose:
            logger.debug(f"Inferred category: {category}, name: {name}")
        return category.lower(), name.lower()
        
    def _get_unique_filepath(self, directory: Path, filename: str) -> Path:
        """Get a unique filepath by appending numbers if necessary."""
        base = directory / filename
        if not base.exists():
            return base
            
        counter = 1
        while True:
            new_path = directory / f"{filename.rsplit('.', 1)[0]}_{counter}.yaml"
            if not new_path.exists():
                if self.verbose:
                    logger.debug(f"Generated unique filepath: {new_path}")
                return new_path
            counter += 1
            
    async def optimize_batch(
        self,
        input_csv: str,
        output_dir: str,
        prompt_column: str
    ) -> Dict[str, str]:
        """
        Optimize a batch of prompts from CSV and save to YAML files.
        
        Args:
            input_csv: Path to input CSV file
            output_dir: Directory to save optimized prompts
            prompt_column: Name of the column containing prompts
            
        Returns:
            Dictionary mapping original prompts to output file paths
        """
        # Create output directory
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        if self.verbose:
            logger.info(f"Created output directory: {output_dir}")
        
        # Read prompts
        if self.verbose:
            logger.info(f"Reading prompts from {input_csv}")
        prompts = await self.csv_service.read_prompts(input_csv, prompt_column)
        if self.verbose:
            logger.info(f"Found {len(prompts)} prompts to process")
        
        # Process each prompt
        results = {}
        with BatchProgressTracker(len(prompts), "Optimizing prompts") as progress:
            for i, prompt in enumerate(prompts, 1):
                try:
                    # Update progress with current prompt number
                    progress.update(status=f"Prompt {i}/{len(prompts)}")
                    
                    # Optimize prompt
                    if self.verbose:
                        logger.debug(f"Optimizing prompt {i}")
                    optimized = await self.optimizer_service.optimize(prompt)
                    
                    # Infer category and name
                    if self.verbose:
                        logger.debug(f"Categorizing prompt {i}")
                    category, name = await self._infer_category_and_name(prompt)
                    
                    # Create category directory
                    category_dir = output_path / category
                    category_dir.mkdir(exist_ok=True)
                    
                    # Get unique filepath
                    filepath = self._get_unique_filepath(category_dir, f"{name}.yaml")
                    
                    # Format and save as YAML
                    if self.verbose:
                        logger.debug(f"Saving prompt {i} to {filepath}")
                    yaml_content = await self.yaml_service.format_to_yaml(optimized)
                    filepath.write_text(yaml_content)
                    
                    progress.log_success(f"Successfully processed prompt {i} → {filepath}")
                    results[prompt] = str(filepath)
                    
                except Exception as e:
                    error_msg = f"Error processing prompt {i}: {str(e)}"
                    progress.log_error(error_msg)
                    logger.error(error_msg, exc_info=self.verbose)
                    results[prompt] = f"ERROR: {str(e)}"
        
        # Log final summary
        success_count = sum(1 for r in results.values() if not r.startswith("ERROR:"))
        if self.verbose:
            logger.info(f"Batch processing complete: {success_count}/{len(prompts)} prompts successful")
        
        return results
