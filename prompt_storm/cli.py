"""
Command Line Interface for Prompt Storm.

This module provides the CLI functionality for the prompt-storm package.
"""
import sys
from typing import Optional
import click
from .optimizer import PromptOptimizer, OptimizationConfig

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
def optimize(prompt: str,
            model: str,
            max_tokens: int,
            temperature: float,
            input_file: Optional[str],
            output_file: Optional[str],
            yaml: bool):
    """
    Optimize a prompt using LLM.
    
    If --input-file is provided, the prompt argument is ignored and the content
    of the file is used instead.

    If --yaml flag is set, the optimized prompt will be formatted as YAML.
    """
    try:
        # Read from input file if provided
        if input_file:
            with open(input_file, 'r', encoding='utf-8') as f:
                prompt = f.read().strip()

        # Create configuration
        config = OptimizationConfig(
            model=model,
            max_tokens=max_tokens,
            temperature=temperature
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
            click.echo(f"Optimized prompt saved to {output_file}")
        else:
            click.echo(optimized_prompt)
            
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        sys.exit(1)

if __name__ == '__main__':
    cli()
