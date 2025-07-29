"""
ALT-70 Score for Cellulitis Calculator

Predicts likelihood of lower extremity cellulitis over other diagnoses.

References:
1. Raff AB, et al. J Am Acad Dermatol. 2017;76(4):618-625.e2.
2. Li DG, et al. J Am Acad Dermatol. 2018;79(6):1076-1080.e1.
"""

from typing import Dict, Any


class Alt70CellulitisCalculator:
    """Calculator for ALT-70 Score for Cellulitis"""
    
    def __init__(self):
        # Score points for each criterion
        self.ASYMMETRIC_POINTS = 3
        self.LEUKOCYTOSIS_POINTS = 1
        self.TACHYCARDIA_POINTS = 1
        self.AGE_70_POINTS = 2
    
    def calculate(self, asymmetric: str, leukocytosis: str, 
                  tachycardia: str, age_70_or_older: str) -> Dict[str, Any]:
        """
        Calculates the ALT-70 score for cellulitis prediction
        
        Args:
            asymmetric (str): "yes" if asymmetric/unilateral leg involvement, "no" otherwise
            leukocytosis (str): "yes" if WBC ≥10,000/µL, "no" otherwise
            tachycardia (str): "yes" if HR ≥90 bpm, "no" otherwise
            age_70_or_older (str): "yes" if age ≥70 years, "no" otherwise
            
        Returns:
            Dict with the score and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(asymmetric, leukocytosis, tachycardia, age_70_or_older)
        
        # Calculate score
        score = self._calculate_score(asymmetric, leukocytosis, tachycardia, age_70_or_older)
        
        # Get interpretation
        interpretation = self._get_interpretation(score)
        
        return {
            "result": score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"],
            "likelihood_percent": interpretation["likelihood"]
        }
    
    def _validate_inputs(self, asymmetric: str, leukocytosis: str, 
                        tachycardia: str, age_70_or_older: str):
        """Validates input parameters"""
        
        valid_options = ["yes", "no"]
        
        if asymmetric not in valid_options:
            raise ValueError("Asymmetric must be 'yes' or 'no'")
        
        if leukocytosis not in valid_options:
            raise ValueError("Leukocytosis must be 'yes' or 'no'")
        
        if tachycardia not in valid_options:
            raise ValueError("Tachycardia must be 'yes' or 'no'")
        
        if age_70_or_older not in valid_options:
            raise ValueError("Age 70 or older must be 'yes' or 'no'")
    
    def _calculate_score(self, asymmetric: str, leukocytosis: str, 
                        tachycardia: str, age_70_or_older: str) -> int:
        """Calculates the ALT-70 score"""
        
        score = 0
        
        # Add points for each positive criterion
        if asymmetric == "yes":
            score += self.ASYMMETRIC_POINTS
        
        if leukocytosis == "yes":
            score += self.LEUKOCYTOSIS_POINTS
        
        if tachycardia == "yes":
            score += self.TACHYCARDIA_POINTS
        
        if age_70_or_older == "yes":
            score += self.AGE_70_POINTS
        
        return score
    
    def _get_interpretation(self, score: int) -> Dict[str, str]:
        """
        Determines the interpretation based on the ALT-70 score
        
        Args:
            score (int): Calculated ALT-70 score (0-7)
            
        Returns:
            Dict with interpretation details
        """
        
        if score <= 2:
            return {
                "stage": "Cellulitis Unlikely",
                "description": "Low probability of cellulitis",
                "likelihood": "9%",
                "interpretation": "Cellulitis unlikely (9% likelihood). Reassess diagnosis and consider pseudocellulitis diagnoses such as venous stasis dermatitis, contact dermatitis, superficial thrombophlebitis, gout, or lymphedema. More than 83.3% likelihood of pseudocellulitis."
            }
        elif score <= 4:
            return {
                "stage": "Indeterminate",
                "description": "Moderate probability of cellulitis",
                "likelihood": "72%",
                "interpretation": "Indeterminate (72% likelihood of cellulitis). Consider dermatology or infectious disease consultation to improve diagnostic accuracy, as clinical features alone are insufficient to rule in or rule out cellulitis."
            }
        else:  # score >= 5
            return {
                "stage": "Cellulitis Likely",
                "description": "High probability of cellulitis",
                "likelihood": "95%",
                "interpretation": "Cellulitis likely (95% likelihood). Treat empirically with appropriate antibiotic therapy for cellulitis. Consider typical cellulitis pathogens (Streptococcus species and Staphylococcus aureus)."
            }


def calculate_alt_70_cellulitis(asymmetric: str, leukocytosis: str,
                              tachycardia: str, age_70_or_older: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = Alt70CellulitisCalculator()
    return calculator.calculate(asymmetric, leukocytosis, tachycardia, age_70_or_older)