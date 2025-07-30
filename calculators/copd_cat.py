"""
COPD Assessment Test (CAT) Calculator

Quantifies the impact of COPD symptoms on patients' overall health and quality of life
using an 8-item questionnaire.

References:
1. Jones PW, et al. Eur Respir J. 2009;34(3):648-54.
2. GOLD 2023 Guidelines
3. Gupta N, et al. Eur Respir J. 2014;44(4):873-84.
"""

from typing import Dict, Any


class CopdCatCalculator:
    """Calculator for COPD Assessment Test (CAT)"""
    
    def __init__(self):
        # Score ranges for interpretation
        self.IMPACT_LOW = (0, 10)
        self.IMPACT_MEDIUM = (11, 20)
        self.IMPACT_HIGH = (21, 30)
        self.IMPACT_VERY_HIGH = (31, 40)
    
    def calculate(self, cough: int, phlegm: int, chest_tightness: int,
                 breathlessness: int, activities: int, confidence: int,
                 sleep: int, energy: int) -> Dict[str, Any]:
        """
        Calculates the CAT score using the 8 questionnaire items
        
        Args:
            cough (int): Cough frequency (0-5)
            phlegm (int): Phlegm amount (0-5)
            chest_tightness (int): Chest tightness (0-5)
            breathlessness (int): Breathlessness on exertion (0-5)
            activities (int): Activity limitation (0-5)
            confidence (int): Confidence leaving home (0-5)
            sleep (int): Sleep quality (0-5)
            energy (int): Energy level (0-5)
            
        Returns:
            Dict with the CAT score and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(cough, phlegm, chest_tightness, breathlessness,
                            activities, confidence, sleep, energy)
        
        # Calculate total CAT score
        total_score = (cough + phlegm + chest_tightness + breathlessness +
                      activities + confidence + sleep + energy)
        
        # Get interpretation
        interpretation = self._get_interpretation(total_score)
        
        # Create detailed item scores
        item_scores = {
            "cough": cough,
            "phlegm": phlegm,
            "chest_tightness": chest_tightness,
            "breathlessness": breathlessness,
            "activities": activities,
            "confidence": confidence,
            "sleep": sleep,
            "energy": energy
        }
        
        # Identify highly symptomatic items (≥3 points)
        highly_symptomatic = [item for item, score in item_scores.items() if score >= 3]
        
        return {
            "result": total_score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"],
            "item_scores": item_scores,
            "highly_symptomatic_items": highly_symptomatic
        }
    
    def _validate_inputs(self, cough: int, phlegm: int, chest_tightness: int,
                        breathlessness: int, activities: int, confidence: int,
                        sleep: int, energy: int):
        """Validates that all inputs are integers between 0 and 5"""
        
        parameters = {
            "cough": cough,
            "phlegm": phlegm,
            "chest_tightness": chest_tightness,
            "breathlessness": breathlessness,
            "activities": activities,
            "confidence": confidence,
            "sleep": sleep,
            "energy": energy
        }
        
        for param_name, value in parameters.items():
            if not isinstance(value, int):
                raise ValueError(f"{param_name} must be an integer")
            
            if value < 0 or value > 5:
                raise ValueError(f"{param_name} must be between 0 and 5 (got {value})")
    
    def _get_interpretation(self, score: int) -> Dict[str, str]:
        """
        Determines the interpretation based on the CAT score
        
        Args:
            score (int): Total CAT score (0-40)
            
        Returns:
            Dict with interpretation details
        """
        
        if score <= self.IMPACT_LOW[1]:
            return {
                "stage": "Low impact",
                "description": "Low COPD impact on health",
                "interpretation": "COPD has low impact on patient's life. Continue current management with focus on smoking cessation, preventive care, and reduced exposure to exacerbation risk factors. Consider LAMA, LABA, or rescue inhalers as needed."
            }
        elif score <= self.IMPACT_MEDIUM[1]:
            return {
                "stage": "Medium impact",
                "description": "Medium COPD impact on health",
                "interpretation": "COPD has medium impact on patient's life. Optimize bronchodilator therapy with LAMA, LABA, or combination. Ensure smoking cessation, preventive care, and reduced exposure to exacerbation risk factors."
            }
        elif score <= self.IMPACT_HIGH[1]:
            return {
                "stage": "High impact",
                "description": "High COPD impact on health",
                "interpretation": "COPD has high impact on patient's life. Consider adding ICS to bronchodilator therapy, evaluate for oxygen supplementation, and refer for pulmonary rehabilitation. Ensure comprehensive management including smoking cessation."
            }
        else:  # score > 30
            return {
                "stage": "Very high impact",
                "description": "Very high COPD impact on health",
                "interpretation": "COPD has very high impact on patient's life. Requires intensive management including triple therapy (LAMA/LABA/ICS), oxygen supplementation evaluation, pulmonary rehabilitation, and consideration for lung transplant evaluation in appropriate candidates."
            }


def calculate_copd_cat(cough: int, phlegm: int, chest_tightness: int,
                      breathlessness: int, activities: int, confidence: int,
                      sleep: int, energy: int) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = CopdCatCalculator()
    return calculator.calculate(cough, phlegm, chest_tightness, breathlessness,
                              activities, confidence, sleep, energy)