"""
Absolute Lymphocyte Count (ALC) Calculator

Assesses lymphocyte count and predicts CD4 count in HIV patients,
based on white blood cell count and lymphocyte percentage.
"""

from typing import Dict, Any


class AlcCalculator:
    """Calculator for Absolute Lymphocyte Count (ALC)"""
    
    def __init__(self):
        # Cutoff points for CD4 prediction
        self.LOW_CD4_CUTOFF = 1000
        self.HIGH_CD4_CUTOFF = 2000
        
        # Normal ALC range
        self.NORMAL_ALC_MIN = 1300
        self.NORMAL_ALC_MAX = 3500
    
    def calculate(self, wbc_count: float, lymphocyte_percent: float) -> Dict[str, Any]:
        """
        Calculates the Absolute Lymphocyte Count (ALC)
        
        Args:
            wbc_count (float): White blood cell count in x 10³/mm³
            lymphocyte_percent (float): Lymphocyte percentage (1-100%)
            
        Returns:
            Dict with the result and interpretation
        """
        
        # Validations
        self._validate_inputs(wbc_count, lymphocyte_percent)
        
        # Calculate ALC using the formula:
        # ALC = WBC count × 1000 × (% Lymphocytes / 100)
        alc_count = wbc_count * 1000 * (lymphocyte_percent / 100)
        
        # Round to 1 decimal place
        alc_count = round(alc_count, 1)
        
        # Determine if it's in the normal range
        is_normal = self.NORMAL_ALC_MIN <= alc_count <= self.NORMAL_ALC_MAX
        
        # Get interpretation
        interpretation = self._get_interpretation(alc_count)
        
        # CD4 prediction
        cd4_prediction = self._predict_cd4_status(alc_count)
        
        return {
            "result": alc_count,
            "unit": "cells/mm³",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"],
            "is_normal_range": is_normal,
            "cd4_prediction": cd4_prediction
        }
    
    def _validate_inputs(self, wbc_count, lymphocyte_percent):
        """Validates input parameters"""
        
        if not isinstance(wbc_count, (int, float)) or wbc_count < 0.5 or wbc_count > 50.0:
            raise ValueError("WBC count must be between 0.5 and 50.0 x 10³/mm³")
        
        if not isinstance(lymphocyte_percent, (int, float)) or lymphocyte_percent < 1.0 or lymphocyte_percent > 100.0:
            raise ValueError("Lymphocyte percentage must be between 1.0 and 100.0%")
    
    def _predict_cd4_status(self, alc_count: float) -> Dict[str, Any]:
        """
        Predicts CD4 status based on ALC
        
        Args:
            alc_count (float): Absolute lymphocyte count
            
        Returns:
            Dict with CD4 prediction
        """
        
        if alc_count < self.LOW_CD4_CUTOFF:
            return {
                "cd4_likely_below_200": True,
                "cd4_likely_above_200": False,
                "prediction_confidence": "high",
                "risk_level": "high"
            }
        elif alc_count >= self.HIGH_CD4_CUTOFF:
            return {
                "cd4_likely_below_200": False,
                "cd4_likely_above_200": True,
                "prediction_confidence": "high",
                "risk_level": "low"
            }
        else:
            return {
                "cd4_likely_below_200": None,
                "cd4_likely_above_200": None,
                "prediction_confidence": "low",
                "risk_level": "indeterminate"
            }
    
    def _get_interpretation(self, alc_count: float) -> Dict[str, str]:
        """
        Determines the interpretation based on ALC
        
        Args:
            alc_count (float): Absolute lymphocyte count
            
        Returns:
            Dict with clinical interpretation
        """
        
        if alc_count < self.LOW_CD4_CUTOFF:
            return {
                "stage": "Low CD4",
                "description": "CD4 likely <200 cells/mm³",
                "interpretation": "High risk of opportunistic infections. CD4 very likely <200 cells/mm³. Requires specific CD4 count and consideration for opportunistic infection prophylaxis."
            }
        elif alc_count < self.HIGH_CD4_CUTOFF:
            return {
                "stage": "Indeterminate Zone",
                "description": "CD4 indeterminate",
                "interpretation": "Indeterminate range for CD4 prediction. Specific CD4 count is necessary for accurate immunological status assessment."
            }
        else:
            return {
                "stage": "Adequate CD4",
                "description": "CD4 likely ≥200 cells/mm³",
                "interpretation": "CD4 very likely ≥200 cells/mm³. Lower risk of opportunistic infections. Continue regular monitoring."
            }


def calculate_alc(wbc_count: float, lymphocyte_percent: float) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = AlcCalculator()
    return calculator.calculate(wbc_count, lymphocyte_percent)
