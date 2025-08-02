"""
MELD Na (UNOS/OPTN) Calculator

Quantifies end-stage liver disease for transplant planning with sodium.
Used by UNOS for liver allocation since January 2016.

References:
1. Kim WR, et al. N Engl J Med. 2008;359(10):1018-26.
2. Kamath PS, Kim WR. Hepatology. 2007;45(3):797-805.
3. OPTN Policy 9: Allocation of Livers and Liver-Intestines. 2016.
"""

import math
from typing import Dict, Any


class MeldNaUnosOptnCalculator:
    """Calculator for MELD Na (UNOS/OPTN) Score"""
    
    def __init__(self):
        # Constants for MELD calculation
        self.CR_COEFFICIENT = 0.957
        self.BILI_COEFFICIENT = 0.378
        self.INR_COEFFICIENT = 1.120
        self.CONSTANT = 0.643
        self.MULTIPLIER = 10
        
        # Constants for sodium adjustment
        self.SODIUM_COEFFICIENT = 1.32
        self.INTERACTION_COEFFICIENT = 0.033
        self.SODIUM_REFERENCE = 137
        
        # Bounds
        self.MIN_VALUE = 1.0  # Minimum value for lab parameters
        self.DIALYSIS_CREATININE = 4.0
        self.MIN_SODIUM = 125
        self.MAX_SODIUM = 137
        self.MIN_MELD = 6
        self.MAX_MELD = 40
        self.SODIUM_ADJUSTMENT_THRESHOLD = 11
    
    def calculate(self, creatinine: float, bilirubin: float, inr: float, 
                  sodium: float, dialysis_twice_past_week: str) -> Dict[str, Any]:
        """
        Calculates the MELD Na score for liver disease severity
        
        Args:
            creatinine (float): Serum creatinine in mg/dL
            bilirubin (float): Total bilirubin in mg/dL
            inr (float): International Normalized Ratio
            sodium (float): Serum sodium in mEq/L
            dialysis_twice_past_week (str): Dialysis ≥2 times in past week ("yes"/"no")
            
        Returns:
            Dict with the MELD Na score and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(creatinine, bilirubin, inr, sodium, dialysis_twice_past_week)
        
        # Adjust values according to MELD rules
        cr_adjusted = self._adjust_creatinine(creatinine, dialysis_twice_past_week)
        bili_adjusted = max(bilirubin, self.MIN_VALUE)
        inr_adjusted = max(inr, self.MIN_VALUE)
        na_adjusted = self._adjust_sodium(sodium)
        
        # Calculate initial MELD score
        meld_initial = self._calculate_initial_meld(cr_adjusted, bili_adjusted, inr_adjusted)
        
        # Apply sodium adjustment if MELD > 11
        if meld_initial > self.SODIUM_ADJUSTMENT_THRESHOLD:
            meld_na = self._apply_sodium_adjustment(meld_initial, na_adjusted)
        else:
            meld_na = meld_initial
        
        # Bound final score
        meld_na_final = max(self.MIN_MELD, min(self.MAX_MELD, meld_na))
        
        # Get interpretation
        interpretation = self._get_interpretation(meld_na_final)
        
        return {
            "result": meld_na_final,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, creatinine: float, bilirubin: float, inr: float,
                        sodium: float, dialysis_twice_past_week: str):
        """Validates input parameters"""
        
        if creatinine <= 0 or creatinine > 40:
            raise ValueError(f"Creatinine must be between 0.01 and 40 mg/dL, got {creatinine}")
        
        if bilirubin <= 0 or bilirubin > 100:
            raise ValueError(f"Bilirubin must be between 0.01 and 100 mg/dL, got {bilirubin}")
        
        if inr <= 0 or inr > 100:
            raise ValueError(f"INR must be between 0.01 and 100, got {inr}")
        
        if sodium < 100 or sodium > 150:
            raise ValueError(f"Sodium must be between 100 and 150 mEq/L, got {sodium}")
        
        if dialysis_twice_past_week not in ["yes", "no"]:
            raise ValueError(f"dialysis_twice_past_week must be 'yes' or 'no', got '{dialysis_twice_past_week}'")
    
    def _adjust_creatinine(self, creatinine: float, dialysis: str) -> float:
        """Adjusts creatinine based on dialysis status"""
        if dialysis == "yes":
            return self.DIALYSIS_CREATININE
        return max(creatinine, self.MIN_VALUE)
    
    def _adjust_sodium(self, sodium: float) -> float:
        """Bounds sodium between 125-137 mEq/L"""
        return max(self.MIN_SODIUM, min(self.MAX_SODIUM, sodium))
    
    def _calculate_initial_meld(self, cr: float, bili: float, inr: float) -> int:
        """Calculates initial MELD score before sodium adjustment"""
        
        # MELD = 0.957 × ln(Cr) + 0.378 × ln(bili) + 1.120 × ln(INR) + 0.643
        meld_raw = (
            self.CR_COEFFICIENT * math.log(cr) +
            self.BILI_COEFFICIENT * math.log(bili) +
            self.INR_COEFFICIENT * math.log(inr) +
            self.CONSTANT
        )
        
        # Multiply by 10 and round
        meld_score = round(self.MULTIPLIER * meld_raw)
        
        return meld_score
    
    def _apply_sodium_adjustment(self, meld: int, sodium: float) -> int:
        """Applies sodium adjustment to MELD score"""
        
        # MELD Na = MELD + 1.32 × (137 - Na) - [0.033 × MELD × (137 - Na)]
        sodium_diff = self.SODIUM_REFERENCE - sodium
        
        meld_na = meld + (
            self.SODIUM_COEFFICIENT * sodium_diff -
            (self.INTERACTION_COEFFICIENT * meld * sodium_diff)
        )
        
        return round(meld_na)
    
    def _get_interpretation(self, score: int) -> Dict[str, str]:
        """
        Determines the interpretation based on the MELD Na score
        
        Args:
            score (int): Calculated MELD Na score
            
        Returns:
            Dict with risk category and interpretation
        """
        
        if score <= 9:
            return {
                "stage": "Low Risk",
                "description": "MELD Na ≤9",
                "interpretation": (
                    "3-month mortality approximately 1.9%. Lower priority for liver "
                    "transplant. Continue routine monitoring and management."
                )
            }
        elif score <= 19:
            return {
                "stage": "Moderate Risk",
                "description": "MELD Na 10-19",
                "interpretation": (
                    "3-month mortality approximately 6.0%. Moderate priority for liver "
                    "transplant. Consider hepatology referral if not already established. "
                    "Monitor labs regularly."
                )
            }
        elif score <= 29:
            return {
                "stage": "High Risk",
                "description": "MELD Na 20-29",
                "interpretation": (
                    "3-month mortality approximately 19.6%. High priority for liver "
                    "transplant. Requires close monitoring and aggressive management "
                    "of complications."
                )
            }
        elif score <= 39:
            return {
                "stage": "Very High Risk",
                "description": "MELD Na 30-39",
                "interpretation": (
                    "3-month mortality approximately 52.6%. Very high priority for liver "
                    "transplant. Consider ICU-level care for complications."
                )
            }
        else:  # score >= 40
            return {
                "stage": "Extremely High Risk",
                "description": "MELD Na ≥40",
                "interpretation": (
                    "3-month mortality approximately 71.3%. Highest priority for liver "
                    "transplant. Requires intensive care management."
                )
            }


def calculate_meld_na_unos_optn(creatinine: float, bilirubin: float, inr: float,
                                sodium: float, dialysis_twice_past_week: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = MeldNaUnosOptnCalculator()
    return calculator.calculate(creatinine, bilirubin, inr, sodium, dialysis_twice_past_week)