"""
Command Line Interface for Prompt Storm.

This module provides the CLI functionality for the prompt-storm package.
"""
import sys
from typing import Optional
import click
from rich.console import Console
from .optimizer import PromptOptimizer, OptimizationConfig
from .services.yaml_service import YAMLService
from .services.csv_service import CSVService
from .services.batch_optimizer_service import BatchOptimizerService
from .utils.logger import setup_logger, console

# Initialize with non-verbose logging by default
logger = setup_logger(__name__, verbose=False)

@click.group()
def cli():
    """Prompt Storm CLI - A tool for prompt engineering and optimization."""
    pass

@cli.command()
@click.argument('prompt', type=str)
@click.option('--model', '-m', 
              help='Model to use for optimization',
              default="gpt-4o-mini")
@click.option('--max-tokens', '-t',
              help='Maximum tokens in response',
              type=click.IntRange(min=1),
              default=2000)
@click.option('--temperature', '-temp',
              help='Temperature for generation',
              type=click.FloatRange(min=0.0, max=1.0),
              default=0.7)
@click.option('--input-file', '-i',
              help='Input file containing the prompt',
              type=click.Path(exists=True, dir_okay=False),
              default=None)
@click.option('--output-file', '-o',
              help='Output file to save the optimized prompt',
              type=click.Path(dir_okay=False),
              default=None)
@click.option('--yaml', '-y',
              help='Format the optimized prompt as YAML',
              is_flag=True,
              default=False)
@click.option('--verbose', '-v',
              help='Enable verbose logging',
              is_flag=True,
              default=False)
def optimize(prompt: str,
            model: str,
            max_tokens: int,
            temperature: float,
            input_file: Optional[str],
            output_file: Optional[str],
            yaml: bool,
            verbose: bool):
    """
    Optimize a prompt using LLM.
    
    If --input-file is provided, the prompt argument is ignored and the content
    of the file is used instead.

    If --yaml flag is set, the optimized prompt will be formatted as YAML.
    """
    try:
        # Set up logger with verbose setting
        global logger
        logger = setup_logger(__name__, verbose=verbose)
        
        if verbose:
            logger.debug("Verbose logging enabled")
            logger.info(f"Prompt: {prompt}")
            logger.info(f"Model: {model}")
        
        # Read from input file if provided
        if input_file:
            with open(input_file, 'r', encoding='utf-8') as f:
                prompt = f.read().strip()

        # Create configuration
        config = OptimizationConfig(
            model=model,
            max_tokens=max_tokens,
            temperature=temperature,
        )
        
        # Initialize optimizer and optimize prompt
        optimizer = PromptOptimizer(config)
        optimized_prompt = optimizer.optimize(prompt)
        
        # Format as YAML if requested
        if yaml:
            optimized_prompt = optimizer.format_to_yaml(optimized_prompt)
        
        # Handle output
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(optimized_prompt)
            logger.info(f"Optimized prompt saved to {output_file}")
        else:
            console.print(optimized_prompt)
            
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}", exc_info=verbose)
        sys.exit(1)

@cli.command()
@click.argument('input-csv', type=click.Path(exists=True, dir_okay=False))
@click.argument('output-dir', type=click.Path(file_okay=False))
@click.option('--prompt-column', '-c',
              help='Name of the column containing prompts',
              default='prompt')
@click.option('--model', '-m', 
              help='Model to use for optimization',
              default="gpt-4o-mini")
@click.option('--max-tokens', '-t',
              help='Maximum tokens in response',
              type=click.IntRange(min=1),
              default=2000)
@click.option('--temperature', '-temp',
              help='Temperature for generation',
              type=click.FloatRange(min=0.0, max=1.0),
              default=0.7)
@click.option('--language', '-l',
              help='Language for optimization',
              default="english")
@click.option('--verbose', '-v',
              help='Enable verbose logging',
              is_flag=True,
              default=False)
def optimize_batch(input_csv: str,
                  output_dir: str,
                  prompt_column: str,
                  model: str,
                  max_tokens: int,
                  temperature: float,
                  language: str,
                  verbose: bool):
    """
    Optimize a batch of prompts from a CSV file.
    
    The optimized prompts will be saved as YAML files in categorized subdirectories.
    Each prompt will be analyzed to determine its category and an appropriate name.
    """
    try:
        # Set up logger with verbose setting
        global logger
        logger = setup_logger(__name__, verbose=verbose)
        
        if verbose:
            logger.debug("Verbose logging enabled")
            logger.info(f"Input CSV: {input_csv}")
            logger.info(f"Output directory: {output_dir}")
            logger.info(f"Model: {model}")
            logger.info(f"Language: {language}")

        # Create configuration
        config = OptimizationConfig(
            model=model,
            max_tokens=max_tokens,
            temperature=temperature,
            language=language
        )

        # Initialize services
        optimizer_service = PromptOptimizer(config)
        yaml_service = YAMLService(config)
        csv_service = CSVService()
        
        # Initialize batch optimizer with services
        batch_optimizer = BatchOptimizerService(
            optimizer_service=optimizer_service,
            yaml_service=yaml_service,
            csv_service=csv_service,
            verbose=verbose
        )
        
        # Run batch optimization
        results = batch_optimizer.optimize_batch(
            input_csv=input_csv,
            output_dir=output_dir,
            prompt_column=prompt_column,
            model=model,
            max_tokens=max_tokens,
            temperature=temperature,
            language=language
        )
        
        # Print final summary
        success_count = sum(1 for r in results.values() if not r.startswith("ERROR:"))
        console.print("\n[bold green]Batch Processing Complete[/bold green]")
        console.print(f"Successfully processed: [green]{success_count}[/green] out of [blue]{len(results)}[/blue] prompts")
        
        if success_count < len(results):
            console.print("\n[yellow]Errors encountered:[/yellow]")
            for prompt, result in results.items():
                if result.startswith("ERROR:"):
                    console.print(f"[red]{result}[/red]")
                    
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}", exc_info=verbose)
        sys.exit(1)

@cli.command()
@click.argument('prompt', type=str)
@click.option('--input-file', '-i', help='Input file containing the prompt', type=click.Path(exists=True, dir_okay=False), default=None)
@click.option('--output-file', '-o', help='Output file to save the formatted YAML', type=click.Path(dir_okay=False), default=None)
@click.option('--verbose', '-v', help='Enable verbose logging', is_flag=True, default=False)
@click.option('--language', '-l', help='Language for optimization', default="english")
@click.option('--model', '-m', help='Model to use for optimization', default="gpt-4o-mini")
@click.option('--max-tokens', '-t', help='Maximum tokens in response', type=click.IntRange(min=1), default=2000)
@click.option('--temperature', '-temp', help='Temperature for generation', type=click.FloatRange(min=0.0, max=1.0), default=0.7)
def format_prompt(prompt: str, input_file: Optional[str], output_file: Optional[str], verbose: bool, language: str, model: str, max_tokens: int, temperature: float):
    """Format a provided prompt into YAML. If --input-file is specified, the content of the file is used instead."""
    try:
        # Set up logger with verbose setting
        global logger
        logger = setup_logger(__name__, verbose=verbose)
        if verbose:
            logger.debug("Verbose logging enabled")
            # display parameters
            logger.info(f"Prompt: {prompt}")
            logger.info(f"Language: {language}")
            logger.info(f"Model: {model}")
            logger.info(f"Max Tokens: {max_tokens}")
            logger.info(f"Temperature: {temperature}")

        # Create configuration
        config = OptimizationConfig(
            model=model,
            max_tokens=max_tokens,
            temperature=temperature,
            language=language
        )

        
        # Load prompt from file if specified
        if input_file:
            with open(input_file, 'r', encoding='utf-8') as f:
                prompt = f.read().strip()
        
        # Initialize YAML service and format
        yaml_service = YAMLService(config)
        formatted_yaml = yaml_service.format_to_yaml(prompt)

        # Handle output
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(formatted_yaml)
            console.print(f"Formatted prompt saved to {output_file}")
        else:
            console.print(formatted_yaml)

    except Exception as e:
        logger.error(f"Fatal error: {str(e)}", exc_info=verbose)
        sys.exit(1)

if __name__ == '__main__':
    cli()
