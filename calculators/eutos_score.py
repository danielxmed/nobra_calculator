"""
EUTOS Score for Chronic Myelogenous Leukemia (CML) Calculator

Predicts outcomes after CML treatments, specifically adjusted for tyrosine kinase inhibitor 
treatments. Predicts probability of complete cytogenetic response at 18 months and 
progression-free survival in newly-diagnosed CML patients.

References:
- Hasford J, Baccarani M, Hoffmann V, et al. Predicting complete cytogenetic response 
  and subsequent progression-free survival in 2060 patients with CML on imatinib treatment: 
  the EUTOS score. Blood. 2011;118(3):686-92.
- Baccarani M, Deininger MW, Rosti G, et al. European LeukemiaNet recommendations 
  for the management of chronic myeloid leukemia: 2013 update. Blood. 2013;122(6):872-84.
"""

import math
from typing import Dict, Any


class EutosScoreCalculator:
    """Calculator for EUTOS Score for Chronic Myelogenous Leukemia (CML)"""
    
    def __init__(self):
        # Formula coefficients from original EUTOS Score development
        self.BASOPHIL_COEFFICIENT = 7
        self.SPLEEN_COEFFICIENT = 4
        self.RISK_THRESHOLD = 87
    
    def calculate(self, basophil_percentage: float, spleen_size_cm: float) -> Dict[str, Any]:
        """
        Calculates the EUTOS Score using basophil percentage and spleen size
        
        Args:
            basophil_percentage (float): Basophils as percentage of peripheral blood leukocytes (0-100%)
            spleen_size_cm (float): Spleen size palpable below left costal margin in cm (0-30 cm)
            
        Returns:
            Dict with the EUTOS Score result and clinical interpretation
        """
        
        # Validate inputs
        self._validate_inputs(basophil_percentage, spleen_size_cm)
        
        # Calculate EUTOS Score
        eutos_score = self._calculate_score(basophil_percentage, spleen_size_cm)
        
        # Get risk classification and interpretation
        interpretation = self._get_interpretation(eutos_score)
        
        # Calculate probability of not achieving complete cytogenetic response
        probability_no_ccyr = self._calculate_probability_no_ccyr(basophil_percentage, spleen_size_cm)
        
        return {
            "result": eutos_score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"],
            "probability_no_ccyr": round(probability_no_ccyr * 100, 1),
            "five_year_pfs": interpretation["five_year_pfs"],
            "ccyr_18_months": interpretation["ccyr_18_months"]
        }
    
    def _validate_inputs(self, basophil_percentage: float, spleen_size_cm: float):
        """Validates input parameters"""
        
        if not isinstance(basophil_percentage, (int, float)):
            raise ValueError("Basophil percentage must be a number")
        
        if not isinstance(spleen_size_cm, (int, float)):
            raise ValueError("Spleen size must be a number")
        
        if basophil_percentage < 0 or basophil_percentage > 100:
            raise ValueError("Basophil percentage must be between 0 and 100%")
        
        if spleen_size_cm < 0 or spleen_size_cm > 30:
            raise ValueError("Spleen size must be between 0 and 30 cm")
    
    def _calculate_score(self, basophil_percentage: float, spleen_size_cm: float) -> float:
        """
        Calculates the EUTOS Score using the formula:
        EUTOS Score = (7 × basophil percentage) + (4 × spleen size in cm)
        """
        
        score = (self.BASOPHIL_COEFFICIENT * basophil_percentage) + (self.SPLEEN_COEFFICIENT * spleen_size_cm)
        
        return round(score, 1)
    
    def _calculate_probability_no_ccyr(self, basophil_percentage: float, spleen_size_cm: float) -> float:
        """
        Calculates probability of not achieving complete cytogenetic response (CCyR) at 18 months
        using the formula: Probability = x / (1 + x), where x = exp(−2.1007 + 0.0700 × basophils + 0.0402 × spleen size)
        """
        
        # Calculate the exponential term
        exponent = -2.1007 + (0.0700 * basophil_percentage) + (0.0402 * spleen_size_cm)
        x = math.exp(exponent)
        
        # Calculate probability
        probability = x / (1 + x)
        
        return probability
    
    def _get_interpretation(self, score: float) -> Dict[str, Any]:
        """
        Determines the risk classification and clinical interpretation based on EUTOS Score
        
        Args:
            score (float): Calculated EUTOS Score
            
        Returns:
            Dict with risk classification and clinical interpretation
        """
        
        if score <= self.RISK_THRESHOLD:
            return {
                "stage": "Low Risk",
                "description": "Low risk for CML progression",
                "interpretation": f"EUTOS Score: {score} points (≤87 = Low Risk). 5-year progression-free survival: 90%, complete cytogenetic response at 18 months: 86%. Standard imatinib therapy recommended with routine monitoring. Excellent prognosis expected with first-line tyrosine kinase inhibitor treatment.",
                "five_year_pfs": "90%",
                "ccyr_18_months": "86%"
            }
        else:
            return {
                "stage": "High Risk",
                "description": "High risk for CML progression",
                "interpretation": f"EUTOS Score: {score} points (>87 = High Risk). 5-year progression-free survival: 82%, complete cytogenetic response at 18 months: 66%. Consider more intensive monitoring, earlier assessment of treatment response, or alternative treatment strategies. Enhanced clinical surveillance recommended.",
                "five_year_pfs": "82%",
                "ccyr_18_months": "66%"
            }


def calculate_eutos_score(basophil_percentage: float, spleen_size_cm: float) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_eutos_score pattern
    """
    calculator = EutosScoreCalculator()
    return calculator.calculate(basophil_percentage, spleen_size_cm)