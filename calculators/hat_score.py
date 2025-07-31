"""
HAT (Hemorrhage After Thrombolysis) Score for Predicting Post-tPA Hemorrhage Calculator

Predicts hemorrhage risk after tPA administration in acute ischemic stroke patients.
Helps determine risk/benefit of tPA in borderline cases and identify patients
needing closest monitoring.

References:
1. Lou M, et al. Neurology. 2008;71(18):1417-23.
2. Tsivgoulis G, et al. Stroke. 2009;40(11):3631-4.
"""

from typing import Dict, Any


class HatScoreCalculator:
    """Calculator for HAT (Hemorrhage After Thrombolysis) Score"""
    
    def __init__(self):
        # Hemorrhage risk percentages based on score
        self.HEMORRHAGE_RISKS = {
            0: {"any": 6, "symptomatic": 2, "fatal": 0},
            1: {"any": 16, "symptomatic": 5, "fatal": 3},
            2: {"any": 23, "symptomatic": 10, "fatal": 7},
            3: {"any": 36, "symptomatic": 15, "fatal": 6},
            4: {"any": 78, "symptomatic": 44, "fatal": 33},
            5: {"any": 78, "symptomatic": 44, "fatal": 33}  # Same as score 4
        }
    
    def calculate(self, diabetes_or_glucose: str, nihss_score: str,
                  hypodensity_on_ct: str) -> Dict[str, Any]:
        """
        Calculates the HAT score using the provided parameters
        
        Args:
            diabetes_or_glucose (str): "no" or "yes" - diabetes history or glucose >200
            nihss_score (str): "less_than_15", "15_to_20", or "greater_than_20"
            hypodensity_on_ct (str): "no", "yes_less_than_one_third", or "yes_one_third_or_more"
            
        Returns:
            Dict with the result and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(diabetes_or_glucose, nihss_score, hypodensity_on_ct)
        
        # Calculate HAT score
        score = 0
        
        # History of diabetes or glucose >200 mg/dL (1 point)
        if diabetes_or_glucose == "yes":
            score += 1
        
        # Pre-tPA NIH Stroke Scale score
        if nihss_score == "15_to_20":
            score += 1
        elif nihss_score == "greater_than_20":
            score += 2
        
        # Hypodensity on initial head CT
        if hypodensity_on_ct == "yes_less_than_one_third":
            score += 1
        elif hypodensity_on_ct == "yes_one_third_or_more":
            score += 2
        
        # Get interpretation and hemorrhage risks
        interpretation = self._get_interpretation(score)
        risks = self.HEMORRHAGE_RISKS[score]
        
        # Add specific risk percentages to interpretation
        enhanced_interpretation = interpretation["interpretation"].replace(
            "after tPA.",
            f"after tPA. Any hemorrhage: {risks['any']}%, "
            f"Symptomatic ICH: {risks['symptomatic']}%, "
            f"Fatal hemorrhage: {risks['fatal']}%."
        )
        
        return {
            "result": score,
            "unit": "points",
            "interpretation": enhanced_interpretation,
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, diabetes_or_glucose: str, nihss_score: str,
                        hypodensity_on_ct: str):
        """Validates input parameters"""
        
        valid_yes_no = ["yes", "no"]
        valid_nihss = ["less_than_15", "15_to_20", "greater_than_20"]
        valid_ct = ["no", "yes_less_than_one_third", "yes_one_third_or_more"]
        
        if diabetes_or_glucose not in valid_yes_no:
            raise ValueError(f"Diabetes/glucose must be one of: {', '.join(valid_yes_no)}")
        
        if nihss_score not in valid_nihss:
            raise ValueError(f"NIHSS score must be one of: {', '.join(valid_nihss)}")
        
        if hypodensity_on_ct not in valid_ct:
            raise ValueError(f"CT hypodensity must be one of: {', '.join(valid_ct)}")
    
    def _get_interpretation(self, score: int) -> Dict[str, str]:
        """
        Determines the interpretation based on the HAT score
        
        Args:
            score (int): Calculated HAT score (0-5)
            
        Returns:
            Dict with interpretation
        """
        
        if score == 0:
            return {
                "stage": "Low Risk",
                "description": "Low hemorrhage risk",
                "interpretation": (
                    "Low risk of hemorrhage after tPA. Benefits of tPA likely outweigh risks "
                    "in eligible patients."
                )
            }
        elif score == 1:
            return {
                "stage": "Low-Moderate Risk",
                "description": "Low-moderate hemorrhage risk",
                "interpretation": (
                    "Low-moderate risk of hemorrhage after tPA. Consider benefits vs risks "
                    "carefully, ensure close monitoring if tPA given."
                )
            }
        elif score == 2:
            return {
                "stage": "Moderate Risk",
                "description": "Moderate hemorrhage risk",
                "interpretation": (
                    "Moderate risk of hemorrhage after tPA. Carefully weigh risks and benefits. "
                    "Ensure intensive monitoring if tPA given."
                )
            }
        elif score == 3:
            return {
                "stage": "High Risk",
                "description": "High hemorrhage risk",
                "interpretation": (
                    "High risk of hemorrhage after tPA. Consider alternative treatments. "
                    "If tPA given, requires intensive monitoring."
                )
            }
        else:  # score >= 4
            return {
                "stage": "Very High Risk",
                "description": "Very high hemorrhage risk",
                "interpretation": (
                    "Very high risk of hemorrhage after tPA. tPA generally not recommended "
                    "unless exceptional circumstances. Consider alternative treatments."
                )
            }


def calculate_hat_score(diabetes_or_glucose: str, nihss_score: str,
                       hypodensity_on_ct: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = HatScoreCalculator()
    return calculator.calculate(diabetes_or_glucose, nihss_score, hypodensity_on_ct)