#!/usr/bin/env python3
import logging
import yaml
from pathlib import Path
from data_handler import DataHandler
from optimizer import ShelterOptimizer
from output_generator import OutputGenerator

# Set up logging
logging.basicConfig(
    filename='logs/optimizer.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def main():
    try:
        # Load configuration
        with open('config.yaml', 'r') as f:
            config = yaml.safe_load(f)
        
        # Initialize components
        data_handler = DataHandler(config['input_file'])
        optimizer = ShelterOptimizer()
        output_gen = OutputGenerator(config['output_file'])
        
        # Load and validate data
        families, shelters = data_handler.load_data()
        logging.info(f'Loaded {len(families)} families and {len(shelters)} shelters')
        
        # Run optimization
        assignments = optimizer.optimize(families, shelters)
        
        # Generate output
        output_gen.generate_report(assignments, families, shelters)
        
        print('Optimization complete. Check assignments.xlsx for results.')
        
    except Exception as e:
        logging.error(f'Error in optimization process: {str(e)}')
        print(f'Error occurred. Please check logs/optimizer.log for details.')

if __name__ == '__main__':
    main()