"""Example script to test the prompt optimizer."""
import asyncio
from prompt_storm.optimizer import PromptOptimizer

async def main():
    # Create optimizer with default config (using gpt-4o-mini)
    optimizer = PromptOptimizer()
    
    # Test prompt to optimize
    test_prompt = "Write a function that calculates fibonacci numbers"
    
    try:
        # Optimize the prompt
        print("Original prompt:", test_prompt)
        print("\nOptimizing prompt...")
        
        optimized = await optimizer.optimize(test_prompt)
        print("\nOptimized prompt:", optimized)
        
    except Exception as e:
        print(f"Error occurred: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())
