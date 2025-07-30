"""
Clinical Pulmonary Infection Score (CPIS) Calculator

Evaluates objective data in mechanically ventilated patients suspected of 
ventilator-associated pneumonia (VAP) and stratifies risk of positive diagnosis.

References:
1. Pugin J, et al. Am Rev Respir Dis. 1991;143(5 Pt 1):1121-9.
2. Singh N, et al. Am J Respir Crit Care Med. 2000;162(2 Pt 1):505-11.
3. Schurink CA, et al. Intensive Care Med. 2004;30(2):217-24.
"""

from typing import Dict, Any


class CpisCalculator:
    """Calculator for Clinical Pulmonary Infection Score (CPIS)"""
    
    def __init__(self):
        # Score mappings for each parameter
        self.temperature_scores = {
            "36.5-38.4": 0,
            "38.5-38.9": 1,
            "≥39.0 or ≤36.0": 2
        }
        
        self.wbc_scores = {
            "4-11": 0,
            "<4 or >11": 1,
            "<4 or >11 plus band forms ≥500": 2
        }
        
        self.secretions_scores = {
            "<14+": 0,
            "≥14+": 1,
            "≥14+ plus purulent": 2
        }
        
        self.oxygenation_scores = {
            ">240 or ARDS": 0,
            "≤240 and no ARDS": 2
        }
        
        self.radiograph_scores = {
            "No infiltrate": 0,
            "Diffuse or patchy infiltrate": 1,
            "Localized infiltrate": 2
        }
        
        self.culture_scores = {
            "Pathogenic bacteria ≤1+ or no growth": 0,
            "Pathogenic bacteria >1+": 1,
            "Pathogenic bacteria >1+ plus same on gram stain >1+": 2
        }
    
    def calculate(self, temperature: str, white_blood_cells: str, 
                 tracheal_secretions: str, oxygenation: str,
                 chest_radiograph: str, tracheal_aspirate_culture: str) -> Dict[str, Any]:
        """
        Calculates the CPIS score using the provided parameters
        
        Args:
            temperature (str): Core body temperature category
            white_blood_cells (str): WBC count category
            tracheal_secretions (str): Secretions volume and character
            oxygenation (str): PaO2/FiO2 ratio category
            chest_radiograph (str): Chest X-ray findings
            tracheal_aspirate_culture (str): Culture and gram stain results
            
        Returns:
            Dict with the CPIS score and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(temperature, white_blood_cells, tracheal_secretions,
                            oxygenation, chest_radiograph, tracheal_aspirate_culture)
        
        # Calculate individual component scores
        temp_score = self.temperature_scores[temperature]
        wbc_score = self.wbc_scores[white_blood_cells]
        secretions_score = self.secretions_scores[tracheal_secretions]
        oxygenation_score = self.oxygenation_scores[oxygenation]
        radiograph_score = self.radiograph_scores[chest_radiograph]
        culture_score = self.culture_scores[tracheal_aspirate_culture]
        
        # Calculate total CPIS score
        total_score = (temp_score + wbc_score + secretions_score + 
                      oxygenation_score + radiograph_score + culture_score)
        
        # Get interpretation
        interpretation = self._get_interpretation(total_score)
        
        return {
            "result": total_score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"],
            "component_scores": {
                "temperature": temp_score,
                "white_blood_cells": wbc_score,
                "tracheal_secretions": secretions_score,
                "oxygenation": oxygenation_score,
                "chest_radiograph": radiograph_score,
                "tracheal_aspirate_culture": culture_score
            }
        }
    
    def _validate_inputs(self, temperature: str, white_blood_cells: str,
                        tracheal_secretions: str, oxygenation: str,
                        chest_radiograph: str, tracheal_aspirate_culture: str):
        """Validates input parameters"""
        
        if temperature not in self.temperature_scores:
            raise ValueError(f"Invalid temperature category: {temperature}")
        
        if white_blood_cells not in self.wbc_scores:
            raise ValueError(f"Invalid white blood cells category: {white_blood_cells}")
        
        if tracheal_secretions not in self.secretions_scores:
            raise ValueError(f"Invalid tracheal secretions category: {tracheal_secretions}")
        
        if oxygenation not in self.oxygenation_scores:
            raise ValueError(f"Invalid oxygenation category: {oxygenation}")
        
        if chest_radiograph not in self.radiograph_scores:
            raise ValueError(f"Invalid chest radiograph category: {chest_radiograph}")
        
        if tracheal_aspirate_culture not in self.culture_scores:
            raise ValueError(f"Invalid tracheal aspirate culture category: {tracheal_aspirate_culture}")
    
    def _get_interpretation(self, score: int) -> Dict[str, str]:
        """
        Determines the interpretation based on the CPIS score
        
        Args:
            score (int): Calculated CPIS score (0-12)
            
        Returns:
            Dict with interpretation details
        """
        
        if score <= 6:
            return {
                "stage": "Low likelihood",
                "description": "Low likelihood of VAP",
                "interpretation": "Score ≤6 suggests low probability of ventilator-associated pneumonia. Consider early discontinuation of empirical antimicrobial therapy if initiated. Continue monitoring clinical status."
            }
        else:  # score >= 7
            return {
                "stage": "High likelihood",
                "description": "High likelihood of VAP",
                "interpretation": "Score ≥7 may indicate higher likelihood of ventilator-associated pneumonia. Consider obtaining pulmonary cultures (quantitative BAL or PSB) and continuing empirical antimicrobial therapy pending culture results."
            }


def calculate_cpis(temperature: str, white_blood_cells: str,
                  tracheal_secretions: str, oxygenation: str,
                  chest_radiograph: str, tracheal_aspirate_culture: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = CpisCalculator()
    return calculator.calculate(temperature, white_blood_cells, tracheal_secretions,
                              oxygenation, chest_radiograph, tracheal_aspirate_culture)