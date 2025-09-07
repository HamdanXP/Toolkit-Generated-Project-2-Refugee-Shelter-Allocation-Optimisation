import pandas as pd
import logging
from typing import Dict
from datetime import datetime

class OutputGenerator:
    def __init__(self, output_file: str):
        self.output_file = output_file
    
    def generate_report(self, assignments: Dict, families: Dict, shelters: Dict):
        """Generate assignment report with privacy protection."""
        try:
            # Create assignments dataframe
            rows = []
            for family_id, shelter_id in assignments.items():
                rows.append({
                    'Family ID': self._anonymize_id(family_id),
                    'Family Size': families[family_id]['size'],
                    'Assigned Shelter': shelter_id,
                    'Special Needs': 'Yes' if families[family_id]['special_needs'] != 'none' else 'No'
                })
            
            df = pd.DataFrame(rows)
            
            # Create summary sheet
            summary = self._generate_summary(assignments, families, shelters)
            
            # Save to Excel with multiple sheets
            with pd.ExcelWriter(self.output_file) as writer:
                df.to_excel(writer, sheet_name='Assignments', index=False)
                summary.to_excel(writer, sheet_name='Summary', index=False)
                
        except Exception as e:
            logging.error(f'Error generating report: {str(e)}')
            raise
    
    def _anonymize_id(self, id_str: str) -> str:
        """Anonymize family IDs for privacy protection."""
        return f'F{hash(id_str) % 10000:04d}'
    
    def _generate_summary(self, assignments, families, shelters) -> pd.DataFrame:
        """Generate summary statistics."""
        shelter_stats = []
        for shelter_id in shelters:
            assigned_families = [f for f, s in assignments.items() if s == shelter_id]
            current_occupancy = sum(families[f]['size'] for f in assigned_families)
            shelter_stats.append({
                'Shelter ID': shelter_id,
                'Capacity': shelters[shelter_id]['capacity'],
                'Current Occupancy': current_occupancy,
                'Utilization %': round(current_occupancy / shelters[shelter_id]['capacity'] * 100, 1)
            })
        
        return pd.DataFrame(shelter_stats)