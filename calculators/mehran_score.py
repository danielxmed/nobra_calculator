"""
Mehran Score for Post-PCI Contrast Nephropathy Calculator

Predicts risk of contrast-induced nephropathy (CIN) after percutaneous coronary 
intervention (PCI) using 8 clinical variables.

References:
1. Mehran R, et al. A simple risk score for prediction of contrast-induced nephropathy 
   after percutaneous coronary intervention. J Am Coll Cardiol. 2004.
2. Wi J, et al. Impact of contrast-induced acute kidney injury with transient or 
   persistent renal dysfunction on long-term outcomes. Heart. 2011.
3. Narula A, et al. Contrast-induced acute kidney injury after primary percutaneous 
   coronary intervention: results from the HORIZONS-AMI substudy. Eur Heart J. 2014.
"""

import math
from typing import Dict, Any


class MehranScoreCalculator:
    """Calculator for Mehran Score for Post-PCI Contrast Nephropathy"""
    
    def __init__(self):
        # Point values for each risk factor
        self.HYPOTENSION_POINTS = 5
        self.IABP_POINTS = 5
        self.CHF_POINTS = 5
        self.AGE_OVER_75_POINTS = 4
        self.ANEMIA_POINTS = 3
        self.DIABETES_POINTS = 3
        self.CONTRAST_PER_100ML_POINTS = 1
        
        # eGFR thresholds and points
        self.EGFR_SEVERE_THRESHOLD = 20
        self.EGFR_MODERATE_THRESHOLD = 40
        self.EGFR_MILD_THRESHOLD = 60
        self.EGFR_SEVERE_POINTS = 6
        self.EGFR_MODERATE_POINTS = 4
        self.EGFR_MILD_POINTS = 2
        
    def calculate(self, hypotension: str, intra_aortic_balloon_pump: str, 
                  congestive_heart_failure: str, age_over_75: str, anemia: str,
                  diabetes: str, contrast_volume_ml: float, egfr: float) -> Dict[str, Any]:
        """
        Calculates the Mehran Score for post-PCI contrast nephropathy risk
        
        Args:
            hypotension: SBP <80 mmHg for ≥1 hr requiring inotropic support ('yes' or 'no')
            intra_aortic_balloon_pump: Use of IABP ('yes' or 'no')
            congestive_heart_failure: CHF class III/IV or history of pulmonary edema ('yes' or 'no')
            age_over_75: Age >75 years ('yes' or 'no')
            anemia: Hematocrit <39% (men) or <36% (women) ('yes' or 'no')
            diabetes: History of diabetes mellitus ('yes' or 'no')
            contrast_volume_ml: Total volume of contrast media used in mL
            egfr: Estimated glomerular filtration rate in mL/min/1.73 m²
            
        Returns:
            Dict with Mehran score and risk interpretation
        """
        
        # Validate inputs
        self._validate_inputs(hypotension, intra_aortic_balloon_pump, 
                            congestive_heart_failure, age_over_75, anemia,
                            diabetes, contrast_volume_ml, egfr)
        
        # Calculate total score
        total_score = 0
        
        # Add points for yes/no risk factors
        if hypotension == "yes":
            total_score += self.HYPOTENSION_POINTS
        
        if intra_aortic_balloon_pump == "yes":
            total_score += self.IABP_POINTS
            
        if congestive_heart_failure == "yes":
            total_score += self.CHF_POINTS
            
        if age_over_75 == "yes":
            total_score += self.AGE_OVER_75_POINTS
            
        if anemia == "yes":
            total_score += self.ANEMIA_POINTS
            
        if diabetes == "yes":
            total_score += self.DIABETES_POINTS
        
        # Add points for contrast volume (1 point per 100 mL)
        contrast_points = int(contrast_volume_ml / 100)
        total_score += contrast_points
        
        # Add points based on eGFR
        egfr_points = self._calculate_egfr_points(egfr)
        total_score += egfr_points
        
        # Get interpretation
        interpretation = self._get_interpretation(total_score)
        
        return {
            "result": total_score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, hypotension: str, intra_aortic_balloon_pump: str,
                        congestive_heart_failure: str, age_over_75: str, anemia: str,
                        diabetes: str, contrast_volume_ml: float, egfr: float):
        """Validates all input parameters"""
        
        # Validate yes/no parameters
        yes_no_params = {
            "hypotension": hypotension,
            "intra_aortic_balloon_pump": intra_aortic_balloon_pump,
            "congestive_heart_failure": congestive_heart_failure,
            "age_over_75": age_over_75,
            "anemia": anemia,
            "diabetes": diabetes
        }
        
        for param_name, value in yes_no_params.items():
            if value not in ["yes", "no"]:
                raise ValueError(f"{param_name} must be 'yes' or 'no'")
        
        # Validate contrast volume
        if not isinstance(contrast_volume_ml, (int, float)):
            raise ValueError("Contrast volume must be a number")
        
        if contrast_volume_ml < 0 or contrast_volume_ml > 1000:
            raise ValueError("Contrast volume must be between 0 and 1000 mL")
        
        # Validate eGFR
        if not isinstance(egfr, (int, float)):
            raise ValueError("eGFR must be a number")
        
        if egfr < 0 or egfr > 200:
            raise ValueError("eGFR must be between 0 and 200 mL/min/1.73 m²")
    
    def _calculate_egfr_points(self, egfr: float) -> int:
        """
        Calculates points based on eGFR value
        
        Args:
            egfr: Estimated glomerular filtration rate
            
        Returns:
            Points based on eGFR category
        """
        
        if egfr < self.EGFR_SEVERE_THRESHOLD:
            return self.EGFR_SEVERE_POINTS
        elif egfr < self.EGFR_MODERATE_THRESHOLD:
            return self.EGFR_MODERATE_POINTS
        elif egfr < self.EGFR_MILD_THRESHOLD:
            return self.EGFR_MILD_POINTS
        else:
            return 0
    
    def _get_interpretation(self, score: int) -> Dict[str, str]:
        """
        Determines the risk category and interpretation based on Mehran score
        
        Args:
            score: Calculated Mehran score
            
        Returns:
            Dict with stage, description, and interpretation
        """
        
        if score <= 5:
            return {
                "stage": "Low Risk",
                "description": "Low risk of CIN",
                "interpretation": "7.5% risk of contrast-induced nephropathy. 0.04% risk of CIN "
                                "requiring dialysis. Standard preventive measures recommended "
                                "including adequate hydration."
            }
        elif score <= 10:
            return {
                "stage": "Moderate Risk",
                "description": "Moderate risk of CIN",
                "interpretation": "14.0% risk of contrast-induced nephropathy. 0.12% risk of CIN "
                                "requiring dialysis. Consider enhanced preventive measures including "
                                "N-acetylcysteine, sodium bicarbonate, and minimizing contrast volume."
            }
        elif score <= 15:
            return {
                "stage": "High Risk",
                "description": "High risk of CIN",
                "interpretation": "26.1% risk of contrast-induced nephropathy. 1.09% risk of CIN "
                                "requiring dialysis. Aggressive preventive measures recommended. "
                                "Consider alternative imaging if possible or minimize contrast volume "
                                "with careful monitoring."
            }
        else:
            return {
                "stage": "Very High Risk",
                "description": "Very high risk of CIN",
                "interpretation": "57.4% risk of contrast-induced nephropathy. 12.6% risk of CIN "
                                "requiring dialysis. Maximum preventive measures required. Strongly "
                                "consider alternative imaging modalities if clinically appropriate. "
                                "If PCI necessary, use minimal contrast with aggressive hydration "
                                "and renal protection."
            }


def calculate_mehran_score(hypotension: str, intra_aortic_balloon_pump: str,
                          congestive_heart_failure: str, age_over_75: str, anemia: str,
                          diabetes: str, contrast_volume_ml: float, egfr: float) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = MehranScoreCalculator()
    return calculator.calculate(hypotension, intra_aortic_balloon_pump,
                               congestive_heart_failure, age_over_75, anemia,
                               diabetes, contrast_volume_ml, egfr)