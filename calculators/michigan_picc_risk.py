"""
Michigan Risk Score for PICC-Related Thrombosis Calculator

Predicts risk of DVT in patients with peripherally inserted central catheter (PICC).

References:
1. Chopra V, et al. J Thromb Haemost. 2017;15(10):1951-1962.
2. Chopra V, et al. Lancet. 2013;382(9889):311-25.
"""

from typing import Dict, Any


class MichiganPiccRiskCalculator:
    """Calculator for Michigan Risk Score for PICC-Related Thrombosis"""
    
    def __init__(self):
        # Point values for each risk factor
        self.POINTS = {
            "another_cvc": {"no": 0, "yes": 1},
            "wbc_over_12": {"no": 0, "yes": 1},
            "picc_lumens": {"1": 0, "2": 1, "3_or_4": 2},
            "history_of_vte": {
                "never": 0,
                "yes_over_30_days": 2,
                "yes_within_30_days": 3
            },
            "active_cancer": {"no": 0, "yes": 3}
        }
    
    def calculate(self, another_cvc_present: str, wbc_over_12: str,
                  picc_lumens: str, history_of_vte: str,
                  active_cancer: str) -> Dict[str, Any]:
        """
        Calculates the Michigan Risk Score for PICC-Related Thrombosis
        
        Args:
            another_cvc_present (str): "no" or "yes"
            wbc_over_12 (str): "no" or "yes"
            picc_lumens (str): "1", "2", or "3_or_4"
            history_of_vte (str): "never", "yes_over_30_days", or "yes_within_30_days"
            active_cancer (str): "no" or "yes"
            
        Returns:
            Dict with risk score and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(another_cvc_present, wbc_over_12, picc_lumens,
                            history_of_vte, active_cancer)
        
        # Calculate total score
        score = 0
        score += self.POINTS["another_cvc"][another_cvc_present]
        score += self.POINTS["wbc_over_12"][wbc_over_12]
        score += self.POINTS["picc_lumens"][picc_lumens]
        score += self.POINTS["history_of_vte"][history_of_vte]
        score += self.POINTS["active_cancer"][active_cancer]
        
        # Get interpretation
        interpretation = self._get_interpretation(score)
        
        return {
            "result": score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, another_cvc_present: str, wbc_over_12: str,
                        picc_lumens: str, history_of_vte: str,
                        active_cancer: str):
        """Validates input parameters"""
        
        # Validate another CVC present
        valid_cvc = ["no", "yes"]
        if another_cvc_present not in valid_cvc:
            raise ValueError(f"Another CVC present must be one of {valid_cvc}, got '{another_cvc_present}'")
        
        # Validate WBC > 12
        valid_wbc = ["no", "yes"]
        if wbc_over_12 not in valid_wbc:
            raise ValueError(f"WBC > 12 must be one of {valid_wbc}, got '{wbc_over_12}'")
        
        # Validate PICC lumens
        valid_lumens = ["1", "2", "3_or_4"]
        if picc_lumens not in valid_lumens:
            raise ValueError(f"PICC lumens must be one of {valid_lumens}, got '{picc_lumens}'")
        
        # Validate history of VTE
        valid_vte = ["never", "yes_over_30_days", "yes_within_30_days"]
        if history_of_vte not in valid_vte:
            raise ValueError(f"History of VTE must be one of {valid_vte}, got '{history_of_vte}'")
        
        # Validate active cancer
        valid_cancer = ["no", "yes"]
        if active_cancer not in valid_cancer:
            raise ValueError(f"Active cancer must be one of {valid_cancer}, got '{active_cancer}'")
    
    def _get_interpretation(self, score: int) -> Dict[str, str]:
        """
        Determines the risk class and interpretation based on score
        
        Args:
            score (int): Calculated Michigan Risk Score
            
        Returns:
            Dict with stage, description, and interpretation
        """
        
        if score == 0:
            return {
                "stage": "Class I",
                "description": "0.9% VTE probability",
                "interpretation": "Low risk of PICC-related thrombosis. Standard monitoring and VTE prophylaxis as per institutional protocol."
            }
        elif score <= 2:
            return {
                "stage": "Class II",
                "description": "1.6% VTE probability",
                "interpretation": "Low-moderate risk of PICC-related thrombosis. Consider enhanced monitoring for VTE symptoms."
            }
        elif score <= 4:
            return {
                "stage": "Class III",
                "description": "2.7% VTE probability",
                "interpretation": "Moderate-high risk of PICC-related thrombosis. Consider alternative vascular access if feasible, or implement enhanced VTE prophylaxis and monitoring."
            }
        else:  # score >= 5
            return {
                "stage": "Class IV",
                "description": "4.7% VTE probability",
                "interpretation": "High risk of PICC-related thrombosis. Strongly consider alternative vascular access options. If PICC necessary, implement aggressive VTE prophylaxis and frequent monitoring."
            }


def calculate_michigan_picc_risk(another_cvc_present: str, wbc_over_12: str,
                                picc_lumens: str, history_of_vte: str,
                                active_cancer: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = MichiganPiccRiskCalculator()
    return calculator.calculate(another_cvc_present, wbc_over_12, picc_lumens,
                              history_of_vte, active_cancer)