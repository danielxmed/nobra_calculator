"""
MELD Score (Original, Pre-2016) Calculator

Quantifies end-stage liver disease for transplant planning using the original formula.
This is the pre-2016 version without sodium adjustment.

References:
1. Kamath PS, et al. Hepatology. 2001;33(2):464-70.
2. Wiesner R, et al. Gastroenterology. 2003;124(1):91-6.
3. Malinchoc M, et al. Hepatology. 2000;31(4):864-71.
"""

import math
from typing import Dict, Any


class MeldScoreOriginalCalculator:
    """Calculator for MELD Score (Original, Pre-2016)"""
    
    def __init__(self):
        # Constants for MELD calculation
        self.CR_COEFFICIENT = 0.957
        self.BILI_COEFFICIENT = 0.378
        self.INR_COEFFICIENT = 1.120
        self.CONSTANT = 0.643
        self.MULTIPLIER = 10
        
        # Bounds
        self.MIN_VALUE = 1.0  # Minimum value for lab parameters
        self.DIALYSIS_CREATININE = 4.0
        self.MIN_MELD = 6
        self.MAX_MELD = 40
    
    def calculate(self, creatinine: float, bilirubin: float, inr: float, 
                  dialysis: str) -> Dict[str, Any]:
        """
        Calculates the original MELD score for liver disease severity
        
        Args:
            creatinine (float): Serum creatinine in mg/dL
            bilirubin (float): Total bilirubin in mg/dL
            inr (float): International Normalized Ratio
            dialysis (str): Hemodialysis ≥2 times in past week ("yes"/"no")
            
        Returns:
            Dict with the MELD score and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(creatinine, bilirubin, inr, dialysis)
        
        # Adjust values according to MELD rules
        cr_adjusted = self._adjust_creatinine(creatinine, dialysis)
        bili_adjusted = max(bilirubin, self.MIN_VALUE)
        inr_adjusted = max(inr, self.MIN_VALUE)
        
        # Calculate MELD score
        meld_score = self._calculate_meld(cr_adjusted, bili_adjusted, inr_adjusted)
        
        # Bound final score
        meld_final = max(self.MIN_MELD, min(self.MAX_MELD, meld_score))
        
        # Get interpretation
        interpretation = self._get_interpretation(meld_final)
        
        return {
            "result": meld_final,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, creatinine: float, bilirubin: float, inr: float,
                        dialysis: str):
        """Validates input parameters"""
        
        if creatinine <= 0 or creatinine > 40:
            raise ValueError(f"Creatinine must be between 0.01 and 40 mg/dL, got {creatinine}")
        
        if bilirubin <= 0 or bilirubin > 50:
            raise ValueError(f"Bilirubin must be between 0.00000001 and 50 mg/dL, got {bilirubin}")
        
        if inr <= 0 or inr > 20:
            raise ValueError(f"INR must be between 0.1 and 20, got {inr}")
        
        if dialysis not in ["yes", "no"]:
            raise ValueError(f"dialysis must be 'yes' or 'no', got '{dialysis}'")
    
    def _adjust_creatinine(self, creatinine: float, dialysis: str) -> float:
        """Adjusts creatinine based on dialysis status"""
        if dialysis == "yes":
            return self.DIALYSIS_CREATININE
        return max(creatinine, self.MIN_VALUE)
    
    def _calculate_meld(self, cr: float, bili: float, inr: float) -> int:
        """Calculates MELD score using the original formula"""
        
        # MELD = (0.957 × ln(Cr) + 0.378 × ln(bili) + 1.120 × ln(INR) + 0.643) × 10
        meld_raw = (
            self.CR_COEFFICIENT * math.log(cr) +
            self.BILI_COEFFICIENT * math.log(bili) +
            self.INR_COEFFICIENT * math.log(inr) +
            self.CONSTANT
        )
        
        # Multiply by 10 and round
        meld_score = round(self.MULTIPLIER * meld_raw)
        
        return meld_score
    
    def _get_interpretation(self, score: int) -> Dict[str, str]:
        """
        Determines the interpretation based on the MELD score
        
        Args:
            score (int): Calculated MELD score
            
        Returns:
            Dict with risk category and interpretation
        """
        
        if score <= 9:
            return {
                "stage": "Low Risk",
                "description": "MELD ≤9",
                "interpretation": (
                    "3-month mortality approximately 1.9%. Lower priority for liver "
                    "transplant. Continue routine monitoring."
                )
            }
        elif score <= 19:
            return {
                "stage": "Moderate Risk",
                "description": "MELD 10-19",
                "interpretation": (
                    "3-month mortality approximately 6.0%. Moderate priority for liver "
                    "transplant. Consider hepatology referral if not established."
                )
            }
        elif score <= 29:
            return {
                "stage": "High Risk",
                "description": "MELD 20-29",
                "interpretation": (
                    "3-month mortality approximately 19.6%. High priority for liver "
                    "transplant. Requires close monitoring."
                )
            }
        elif score <= 39:
            return {
                "stage": "Very High Risk",
                "description": "MELD 30-39",
                "interpretation": (
                    "3-month mortality approximately 52.6%. Very high priority for liver "
                    "transplant. Consider ICU-level care."
                )
            }
        else:  # score >= 40
            return {
                "stage": "Extremely High Risk",
                "description": "MELD ≥40",
                "interpretation": (
                    "3-month mortality approximately 71.3%. Highest priority for liver "
                    "transplant. Requires intensive care."
                )
            }


def calculate_meld_score_original(creatinine: float, bilirubin: float, inr: float,
                                 dialysis: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = MeldScoreOriginalCalculator()
    return calculator.calculate(creatinine, bilirubin, inr, dialysis)