import pandas as pd
import logging
from typing import Tuple, Dict, List

class DataHandler:
    def __init__(self, input_file: str):
        self.input_file = input_file
        
    def load_data(self) -> Tuple[Dict, Dict]:
        """Load and validate input data."""
        try:
            df = pd.read_csv(self.input_file)
            
            # Validate required columns
            required_cols = ['family_id', 'family_size', 'shelter_id', 'shelter_capacity', 'special_needs']
            if not all(col in df.columns for col in required_cols):
                raise ValueError('Missing required columns in input file')
            
            # Process families data - anonymize sensitive information
            families = {}
            for _, row in df[['family_id', 'family_size', 'special_needs']].drop_duplicates().iterrows():
                families[row['family_id']] = {
                    'size': row['family_size'],
                    'special_needs': row['special_needs']
                }
            
            # Process shelters data
            shelters = {}
            for _, row in df[['shelter_id', 'shelter_capacity']].drop_duplicates().iterrows():
                shelters[row['shelter_id']] = {
                    'capacity': row['shelter_capacity'],
                    'current_occupancy': 0
                }
            
            return families, shelters
            
        except Exception as e:
            logging.error(f'Error loading data: {str(e)}')
            raise
