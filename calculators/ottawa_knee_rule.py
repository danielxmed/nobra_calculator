"""
Ottawa Knee Rule Calculator

Clinical decision rule for determining when knee radiography is required
in patients with acute knee trauma. High sensitivity (98-100%) for 
clinically significant fractures.

References:
1. Stiell IG, Greenberg GH, Wells GA, McDowell I, Cwinn AA, Smith NA, et al. 
   Prospective validation of a decision rule for the use of radiography in 
   acute knee injuries. JAMA. 1996 Feb 28;275(8):611-5.
2. Stiell IG, Wells GA, Hoag RH, Sivilotti ML, Cacciotti TF, Verbeek PR, et al. 
   Implementation of the Ottawa Knee Rule for the use of radiography in 
   acute knee injuries. JAMA. 1997 Dec 17;278(23):2075-9.
"""

from typing import Dict, Any


class OttawaKneeRuleCalculator:
    """Calculator for Ottawa Knee Rule"""
    
    def __init__(self):
        """Initialize calculator"""
        pass
    
    def calculate(self, age_55_or_older: str, isolated_patellar_tenderness: str, 
                 fibular_head_tenderness: str, unable_to_flex_90_degrees: str,
                 unable_to_bear_weight: str) -> Dict[str, Any]:
        """
        Applies the Ottawa Knee Rule to determine need for knee x-ray
        
        Args:
            age_55_or_older (str): Is patient age 55 years or older? (yes/no)
            isolated_patellar_tenderness (str): Isolated patella tenderness? (yes/no)
            fibular_head_tenderness (str): Tenderness at fibular head? (yes/no)
            unable_to_flex_90_degrees (str): Unable to flex knee to 90°? (yes/no)
            unable_to_bear_weight (str): Unable to bear weight? (yes/no)
            
        Returns:
            Dict with result and clinical interpretation
        """
        
        # Validate inputs
        self._validate_inputs(age_55_or_older, isolated_patellar_tenderness, 
                            fibular_head_tenderness, unable_to_flex_90_degrees,
                            unable_to_bear_weight)
        
        # Apply Ottawa Knee Rule logic
        result = self._apply_rule(age_55_or_older, isolated_patellar_tenderness,
                                fibular_head_tenderness, unable_to_flex_90_degrees,
                                unable_to_bear_weight)
        
        # Get interpretation
        interpretation = self._get_interpretation(result)
        
        return {
            "result": result,
            "unit": "recommendation",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, age_55_or_older: str, isolated_patellar_tenderness: str,
                        fibular_head_tenderness: str, unable_to_flex_90_degrees: str,
                        unable_to_bear_weight: str):
        """Validates input parameters"""
        
        valid_options = ["yes", "no"]
        
        if age_55_or_older not in valid_options:
            raise ValueError("age_55_or_older must be 'yes' or 'no'")
        
        if isolated_patellar_tenderness not in valid_options:
            raise ValueError("isolated_patellar_tenderness must be 'yes' or 'no'")
        
        if fibular_head_tenderness not in valid_options:
            raise ValueError("fibular_head_tenderness must be 'yes' or 'no'")
        
        if unable_to_flex_90_degrees not in valid_options:
            raise ValueError("unable_to_flex_90_degrees must be 'yes' or 'no'")
        
        if unable_to_bear_weight not in valid_options:
            raise ValueError("unable_to_bear_weight must be 'yes' or 'no'")
    
    def _apply_rule(self, age_55_or_older: str, isolated_patellar_tenderness: str,
                   fibular_head_tenderness: str, unable_to_flex_90_degrees: str,
                   unable_to_bear_weight: str) -> str:
        """
        Applies the Ottawa Knee Rule logic
        
        X-ray is indicated if ANY of the following criteria are present:
        - Age 55 years or older
        - Isolated patellar tenderness
        - Fibular head tenderness  
        - Unable to flex knee to 90 degrees
        - Unable to bear weight both immediately and in ED
        
        Args:
            All five clinical criteria as strings
            
        Returns:
            str: "xray_indicated" or "no_xray_needed"
        """
        
        # Check if any criterion is positive
        criteria = [
            age_55_or_older == "yes",
            isolated_patellar_tenderness == "yes", 
            fibular_head_tenderness == "yes",
            unable_to_flex_90_degrees == "yes",
            unable_to_bear_weight == "yes"
        ]
        
        # If ANY criterion is positive, x-ray is indicated
        if any(criteria):
            return "xray_indicated"
        else:
            return "no_xray_needed"
    
    def _get_interpretation(self, result: str) -> Dict[str, str]:
        """
        Determines clinical interpretation based on result
        
        Args:
            result (str): Rule result
            
        Returns:
            Dict with interpretation details
        """
        
        if result == "no_xray_needed":
            return {
                "stage": "No imaging required",
                "description": "No x-ray needed",
                "interpretation": (
                    "Based on the Ottawa Knee Rule, no knee x-ray is required. "
                    "The absence of all clinical criteria suggests a very low probability "
                    "of clinically significant fracture. The rule has 98-100% sensitivity "
                    "for detecting fractures. Provide written instructions and encourage "
                    "follow-up in 5-7 days if pain or walking does not improve."
                )
            }
        else:  # xray_indicated
            return {
                "stage": "X-ray indicated", 
                "description": "Knee x-ray series required",
                "interpretation": (
                    "Based on the Ottawa Knee Rule, a knee x-ray series is indicated. "
                    "The presence of one or more clinical criteria suggests possible "
                    "knee fracture requiring radiographic evaluation. The rule has "
                    "high sensitivity for detecting clinically significant fractures."
                )
            }


def calculate_ottawa_knee_rule(age_55_or_older: str, isolated_patellar_tenderness: str,
                              fibular_head_tenderness: str, unable_to_flex_90_degrees: str,
                              unable_to_bear_weight: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_ottawa_knee_rule pattern
    """
    calculator = OttawaKneeRuleCalculator()
    return calculator.calculate(age_55_or_older, isolated_patellar_tenderness,
                               fibular_head_tenderness, unable_to_flex_90_degrees,
                               unable_to_bear_weight)