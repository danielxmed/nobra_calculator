"""
Menza Score Calculator

Predicts 4-year HIV risk for men who have sex with men (MSM) based on 
sexual behavior and substance use factors.

References:
1. Menza TW, et al. Sex Transm Dis. 2009;36(9):547-55.
2. Jones J, et al. Sex Transm Dis. 2017;44(5):297-302.
3. Luo Q, et al. Arch Sex Behav. 2023;52(5):2293-2322.
"""

from typing import Dict, Any


class MenzaScoreCalculator:
    """Calculator for Menza Score HIV risk prediction for MSM"""
    
    def __init__(self):
        # Point values for each risk factor
        self.POINTS = {
            "sti_history": {"no": 0, "yes": 4},
            "meth_nitrite_use": {"no": 0, "yes": 11},
            "unprotected_anal_intercourse": {"no": 0, "yes": 1},
            "ten_plus_partners": {"no": 0, "yes": 3}
        }
        
        # Maximum possible score
        self.MAX_SCORE = 19
    
    def calculate(self, sti_history: str, meth_nitrite_use: str,
                  unprotected_anal_intercourse: str, ten_plus_partners: str) -> Dict[str, Any]:
        """
        Calculates the Menza Score for HIV risk prediction in MSM
        
        Args:
            sti_history (str): History of gonorrhea, chlamydia, or syphilis ("yes"/"no")
            meth_nitrite_use (str): Methamphetamine or nitrite use in prior 6 months ("yes"/"no")
            unprotected_anal_intercourse (str): Unprotected anal intercourse with HIV+/unknown partner ("yes"/"no")
            ten_plus_partners (str): 10+ male sexual partners in prior year ("yes"/"no")
            
        Returns:
            Dict with the score and risk interpretation
        """
        
        # Validate inputs
        self._validate_inputs(sti_history, meth_nitrite_use, 
                             unprotected_anal_intercourse, ten_plus_partners)
        
        # Calculate total score
        score = 0
        score += self.POINTS["sti_history"][sti_history]
        score += self.POINTS["meth_nitrite_use"][meth_nitrite_use]
        score += self.POINTS["unprotected_anal_intercourse"][unprotected_anal_intercourse]
        score += self.POINTS["ten_plus_partners"][ten_plus_partners]
        
        # Get interpretation based on score
        interpretation = self._get_interpretation(score)
        
        return {
            "result": score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, sti_history: str, meth_nitrite_use: str,
                        unprotected_anal_intercourse: str, ten_plus_partners: str):
        """Validates input parameters"""
        
        valid_options = ["yes", "no"]
        
        parameters = {
            "sti_history": sti_history,
            "meth_nitrite_use": meth_nitrite_use,
            "unprotected_anal_intercourse": unprotected_anal_intercourse,
            "ten_plus_partners": ten_plus_partners
        }
        
        for param_name, param_value in parameters.items():
            if param_value not in valid_options:
                raise ValueError(f"{param_name} must be 'yes' or 'no', got '{param_value}'")
    
    def _get_interpretation(self, score: int) -> Dict[str, str]:
        """
        Determines the risk category and interpretation based on the score
        
        Args:
            score (int): Calculated Menza Score (0-19)
            
        Returns:
            Dict with risk category, description, and clinical interpretation
        """
        
        if score == 0:
            return {
                "stage": "Low Risk",
                "description": "<5% 4-year HIV risk",
                "interpretation": (
                    "Low risk for HIV acquisition over the next 4 years. Continue routine HIV "
                    "screening and preventive counseling. Discuss general HIV prevention strategies."
                )
            }
        elif score <= 3:
            return {
                "stage": "Moderate Risk",
                "description": "5-9% 4-year HIV risk",
                "interpretation": (
                    "Moderate risk for HIV acquisition. Consider discussing pre-exposure prophylaxis "
                    "(PrEP) and intensified HIV prevention counseling. Regular HIV testing recommended."
                )
            }
        elif score <= 11:
            return {
                "stage": "High Risk",
                "description": "10-14% 4-year HIV risk",
                "interpretation": (
                    "High risk for HIV acquisition. Strongly consider pre-exposure prophylaxis (PrEP) "
                    "initiation. Provide comprehensive HIV prevention counseling and frequent HIV testing."
                )
            }
        else:  # score >= 12
            return {
                "stage": "Very High Risk",
                "description": ">14% 4-year HIV risk",
                "interpretation": (
                    "Very high risk for HIV acquisition. Pre-exposure prophylaxis (PrEP) strongly "
                    "recommended. Implement intensive HIV prevention interventions and very frequent "
                    "HIV testing."
                )
            }


def calculate_menza_score(sti_history: str, meth_nitrite_use: str,
                         unprotected_anal_intercourse: str, ten_plus_partners: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = MenzaScoreCalculator()
    return calculator.calculate(sti_history, meth_nitrite_use,
                               unprotected_anal_intercourse, ten_plus_partners)