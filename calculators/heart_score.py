"""
HEART Score Calculator

Predicts 6-week risk of major adverse cardiac events in chest pain patients.

References:
- Six AJ, et al. Neth Heart J. 2008;16(6):191-6.
- Backus BE, et al. Int J Cardiol. 2013;168(3):2153-8.
"""

from typing import Dict, Any


class HeartScoreCalculator:
    """Calculator for HEART Score for Major Cardiac Events"""
    
    def calculate(self, history: int, ekg: int, age: int, 
                 risk_factors: int, troponin: int) -> Dict[str, Any]:
        """
        Calculates the HEART score using the provided parameters
        
        Args:
            history (int): Clinical history score (0-2)
            ekg (int): EKG findings score (0-2)
            age (int): Age score (0-2)
            risk_factors (int): Risk factors score (0-2)
            troponin (int): Troponin score (0-2)
            
        Returns:
            Dict with the result and interpretation
        """
        
        # Validations
        self._validate_inputs(history, ekg, age, risk_factors, troponin)
        
        # Calculate total score
        result = history + ekg + age + risk_factors + troponin
        
        # Get interpretation
        interpretation = self._get_interpretation(result)
        
        return {
            "result": result,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"],
            "mace_risk": interpretation["mace_risk"],
            "disposition": interpretation["disposition"]
        }
    
    def _validate_inputs(self, history: int, ekg: int, age: int,
                        risk_factors: int, troponin: int):
        """Validates input parameters"""
        
        parameters = {
            "history": history,
            "ekg": ekg,
            "age": age,
            "risk_factors": risk_factors,
            "troponin": troponin
        }
        
        for param_name, value in parameters.items():
            if not isinstance(value, int):
                raise ValueError(f"{param_name.replace('_', ' ').capitalize()} must be an integer")
            
            if value < 0 or value > 2:
                raise ValueError(f"{param_name.replace('_', ' ').capitalize()} must be between 0 and 2")
    
    def _get_interpretation(self, result: int) -> Dict[str, str]:
        """
        Determines the interpretation based on the result
        
        Args:
            result (int): Calculated HEART score
            
        Returns:
            Dict with interpretation
        """
        
        if result <= 3:
            return {
                "stage": "Low Risk",
                "description": "0.9-1.7% 6-week MACE risk",
                "mace_risk": "0.9-1.7%",
                "interpretation": "Low risk for major adverse cardiac events. Safe for discharge from the emergency department with outpatient follow-up. Consider stress testing within 72 hours if clinically indicated.",
                "disposition": "Discharge with outpatient follow-up"
            }
        elif result <= 6:
            return {
                "stage": "Moderate Risk",
                "description": "12-16.6% 6-week MACE risk",
                "mace_risk": "12-16.6%",
                "interpretation": "Moderate risk for major adverse cardiac events. Admission for clinical observation recommended with serial troponins and telemetry monitoring. Consider stress testing or advanced cardiac imaging.",
                "disposition": "Admit for observation"
            }
        else:  # result >= 7
            return {
                "stage": "High Risk",
                "description": "50-65% 6-week MACE risk",
                "mace_risk": "50-65%",
                "interpretation": "High risk for major adverse cardiac events. Consider early invasive strategies including coronary angiography. Cardiology consultation recommended for risk stratification and management.",
                "disposition": "Consider early invasive strategy"
            }


def calculate_heart_score(history: int, ekg: int, age: int,
                         risk_factors: int, troponin: int) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_heart_score pattern
    """
    calculator = HeartScoreCalculator()
    return calculator.calculate(history, ekg, age, risk_factors, troponin)