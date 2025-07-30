"""
Bova Score for Pulmonary Embolism Complications Calculator

Predicts 30-day risk of PE-related complications in hemodynamically stable patients 
with confirmed pulmonary embolism.

References:
1. Bova C, Sanchez O, Prandoni P, et al. Identification of intermediate-risk patients 
   with acute symptomatic pulmonary embolism. Eur Respir J. 2014;44(3):694-703.
2. Fernández C, Bova C, Sanchez O, et al. Validation of a Model for Identification 
   of Patients at Intermediate to High Risk for Complications Associated With Acute 
   Symptomatic Pulmonary Embolism. Chest. 2015;148(1):211-218.
"""

from typing import Dict, Any


class BovaScoreCalculator:
    """Calculator for Bova Score for Pulmonary Embolism Complications"""
    
    def __init__(self):
        # Score thresholds for risk stratification
        self.STAGE_I_MAX = 2
        self.STAGE_II_MAX = 4
        
    def calculate(self, systolic_bp: int, elevated_troponin: str, 
                  rv_dysfunction: str, heart_rate: int) -> Dict[str, Any]:
        """
        Calculates the Bova score for PE complications
        
        Args:
            systolic_bp (int): Systolic blood pressure in mmHg (must be ≥90)
            elevated_troponin (str): "yes" if troponin elevated, "no" otherwise
            rv_dysfunction (str): "yes" if RV dysfunction present, "no" otherwise
            heart_rate (int): Heart rate in beats per minute
            
        Returns:
            Dict with score, unit, stage, and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(systolic_bp, elevated_troponin, rv_dysfunction, heart_rate)
        
        # Calculate score
        score = self._calculate_score(systolic_bp, elevated_troponin, rv_dysfunction, heart_rate)
        
        # Get interpretation
        interpretation = self._get_interpretation(score)
        
        return {
            "result": score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, systolic_bp: int, elevated_troponin: str, 
                        rv_dysfunction: str, heart_rate: int):
        """Validates input parameters"""
        
        # Validate systolic BP
        if not isinstance(systolic_bp, int):
            raise ValueError("Systolic blood pressure must be an integer")
        if systolic_bp < 90:
            raise ValueError("Bova score is only applicable for hemodynamically stable patients (systolic BP ≥90 mmHg)")
        if systolic_bp > 300:
            raise ValueError("Systolic blood pressure must be ≤300 mmHg")
        
        # Validate elevated troponin
        if elevated_troponin not in ["yes", "no"]:
            raise ValueError("Elevated troponin must be 'yes' or 'no'")
        
        # Validate RV dysfunction
        if rv_dysfunction not in ["yes", "no"]:
            raise ValueError("RV dysfunction must be 'yes' or 'no'")
        
        # Validate heart rate
        if not isinstance(heart_rate, int):
            raise ValueError("Heart rate must be an integer")
        if heart_rate < 30 or heart_rate > 250:
            raise ValueError("Heart rate must be between 30 and 250 beats/min")
    
    def _calculate_score(self, systolic_bp: int, elevated_troponin: str, 
                        rv_dysfunction: str, heart_rate: int) -> int:
        """Calculates the Bova score"""
        
        score = 0
        
        # Systolic BP: 2 points if 90-100 mmHg
        if 90 <= systolic_bp <= 100:
            score += 2
        
        # Elevated troponin: 2 points if yes
        if elevated_troponin == "yes":
            score += 2
        
        # RV dysfunction: 2 points if yes
        if rv_dysfunction == "yes":
            score += 2
        
        # Heart rate: 1 point if ≥110
        if heart_rate >= 110:
            score += 1
        
        return score
    
    def _get_interpretation(self, score: int) -> Dict[str, str]:
        """
        Determines stage and interpretation based on score
        
        Args:
            score (int): Calculated Bova score
            
        Returns:
            Dict with stage, description, and interpretation
        """
        
        if score <= self.STAGE_I_MAX:
            return {
                "stage": "Stage I",
                "description": "Low risk",
                "interpretation": "4.4% risk of PE-related complications and 3.1% PE-related mortality at 30 days. Consider outpatient management if clinically appropriate and no other contraindications."
            }
        elif score <= self.STAGE_II_MAX:
            return {
                "stage": "Stage II",
                "description": "Intermediate risk",
                "interpretation": "18% risk of PE-related complications and 6.8% PE-related mortality at 30 days. Consider hospital admission for monitoring. May benefit from closer observation or advanced therapies."
            }
        else:
            return {
                "stage": "Stage III",
                "description": "High risk",
                "interpretation": "42% risk of PE-related complications and 10% PE-related mortality at 30 days. Requires hospital admission and close monitoring. Consider ICU admission and advanced therapies such as thrombolysis or embolectomy."
            }


def calculate_bova_score(systolic_bp: int, elevated_troponin: str, 
                        rv_dysfunction: str, heart_rate: int) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = BovaScoreCalculator()
    return calculator.calculate(systolic_bp, elevated_troponin, rv_dysfunction, heart_rate)