"""
ABIC Score for Alcoholic Hepatitis Calculator

Predicts survival in patients with alcoholic hepatitis at 90 days and 1 year,
based on age, serum bilirubin, serum creatinine, and INR.
"""

import math
from typing import Dict, Any


class AbicScoreCalculator:
    """Calculator for ABIC Score for Alcoholic Hepatitis"""
    
    def __init__(self):
        # ABIC formula constants
        self.AGE_COEFFICIENT = 0.1
        self.BILIRUBIN_COEFFICIENT = 0.08
        self.CREATININE_COEFFICIENT = 0.3
        self.INR_COEFFICIENT = 0.8
        
        # Cutoff points for risk stratification
        self.LOW_RISK_CUTOFF = 6.71
        self.HIGH_RISK_CUTOFF = 9.0
    
    def calculate(self, age: int, serum_bilirubin: float, serum_creatinine: float, 
                 inr: float) -> Dict[str, Any]:
        """
        Calculates the ABIC Score
        
        Args:
            age (int): Patient's age in years
            serum_bilirubin (float): Total serum bilirubin in mg/dL
            serum_creatinine (float): Serum creatinine in mg/dL
            inr (float): International Normalized Ratio
            
        Returns:
            Dict with the result and interpretation
        """
        
        # Validations
        self._validate_inputs(age, serum_bilirubin, serum_creatinine, inr)
        
        # Calculate ABIC score using the formula:
        # (Age × 0.1) + (Bilirubin × 0.08) + (Creatinine × 0.3) + (INR × 0.8)
        abic_score = (
            (age * self.AGE_COEFFICIENT) +
            (serum_bilirubin * self.BILIRUBIN_COEFFICIENT) +
            (serum_creatinine * self.CREATININE_COEFFICIENT) +
            (inr * self.INR_COEFFICIENT)
        )
        
        # Round to 2 decimal places
        abic_score = round(abic_score, 2)
        
        # Get interpretation
        interpretation = self._get_interpretation(abic_score)
        
        return {
            "result": abic_score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"],
            "survival_90_days": interpretation["survival_90_days"],
            "survival_1_year": interpretation["survival_1_year"]
        }
    
    def _validate_inputs(self, age, serum_bilirubin, serum_creatinine, inr):
        """Validates input parameters"""
        
        if not isinstance(age, int) or age < 18 or age > 100:
            raise ValueError("Age must be an integer between 18 and 100 years")
        
        if not isinstance(serum_bilirubin, (int, float)) or serum_bilirubin < 0.1 or serum_bilirubin > 50.0:
            raise ValueError("Serum bilirubin must be between 0.1 and 50.0 mg/dL")
        
        if not isinstance(serum_creatinine, (int, float)) or serum_creatinine < 0.1 or serum_creatinine > 20.0:
            raise ValueError("Serum creatinine must be between 0.1 and 20.0 mg/dL")
        
        if not isinstance(inr, (int, float)) or inr < 0.5 or inr > 10.0:
            raise ValueError("INR must be between 0.5 and 10.0")
    
    def _get_interpretation(self, abic_score: float) -> Dict[str, str]:
        """
        Determines the interpretation based on the ABIC score
        
        Args:
            abic_score (float): Calculated ABIC score value
            
        Returns:
            Dict with clinical interpretation
        """
        
        if abic_score < self.LOW_RISK_CUTOFF:
            return {
                "stage": "Low Risk",
                "description": "Excellent survival",
                "interpretation": "90-day survival: 100%. 1-year survival: 97.1%. Excellent prognosis with appropriate conservative treatment.",
                "survival_90_days": "100%",
                "survival_1_year": "97.1%"
            }
        elif abic_score <= self.HIGH_RISK_CUTOFF:
            return {
                "stage": "Intermediate Risk",
                "description": "Moderate survival",
                "interpretation": "90-day survival: 70%. 1-year survival: 64.3%. Consider more aggressive treatment and intensive monitoring.",
                "survival_90_days": "70%",
                "survival_1_year": "64.3%"
            }
        else:
            return {
                "stage": "High Risk",
                "description": "Low survival",
                "interpretation": "90-day survival: 25%. 1-year survival: 33.6%. Reserved prognosis. Consider corticosteroid therapy, intensive care, and evaluation for liver transplant.",
                "survival_90_days": "25%",
                "survival_1_year": "33.6%"
            }


def calculate_abic_score(age: int, serum_bilirubin: float, serum_creatinine: float, 
                        inr: float) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = AbicScoreCalculator()
    return calculator.calculate(age, serum_bilirubin, serum_creatinine, inr)
