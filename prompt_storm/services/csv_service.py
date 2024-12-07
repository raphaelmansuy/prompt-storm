"""
Service for CSV processing.
"""
import pandas as pd
from typing import List
from prompt_storm.interfaces.service_interfaces import CSVServiceInterface

class CSVService(CSVServiceInterface):
    """Service for reading prompts from CSV files."""
    
    def read_prompts(self, csv_path: str, prompt_column: str) -> List[str]:
        """
        Read prompts from a CSV file.
        
        Args:
            csv_path: Path to the CSV file
            prompt_column: Name of the column containing prompts
            
        Returns:
            List of prompts
            
        Raises:
            FileNotFoundError: If CSV file doesn't exist
            KeyError: If prompt column doesn't exist
        """
        try:
            df = pd.read_csv(csv_path)
            if prompt_column not in df.columns:
                raise KeyError(f"Column '{prompt_column}' not found in CSV file")
            return df[prompt_column].tolist()
        except FileNotFoundError:
            raise FileNotFoundError(f"CSV file not found at: {csv_path}")
        except Exception as e:
            raise Exception(f"Error reading CSV file: {str(e)}")
