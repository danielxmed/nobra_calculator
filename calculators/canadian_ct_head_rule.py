"""
Canadian CT Head Injury/Trauma Rule Calculator

Determines which patients with minor head injury require CT head imaging based on
high-risk and medium-risk criteria.

References:
1. Stiell IG, Wells GA, Vandemheen K, et al. The Canadian CT Head Rule for patients 
   with minor head injury. Lancet. 2001;357(9266):1391-6.
2. Stiell IG, Clement CM, Rowe BH, et al. Comparison of the Canadian CT Head Rule 
   and the New Orleans Criteria in patients with minor head injury. JAMA. 
   2005;294(12):1511-8.
"""

from typing import Dict, Any


class CanadianCtHeadRuleCalculator:
    """Calculator for Canadian CT Head Injury/Trauma Rule"""
    
    def __init__(self):
        pass
    
    def calculate(
        self,
        gcs_less_than_15_at_2hrs: str,
        suspected_skull_fracture: str,
        basilar_skull_fracture_signs: str,
        vomiting_2_or_more: str,
        age_65_or_over: str,
        amnesia_30_min_or_more: str,
        dangerous_mechanism: str
    ) -> Dict[str, Any]:
        """
        Calculates the Canadian CT Head Rule recommendation
        
        Args:
            gcs_less_than_15_at_2hrs: GCS <15 at 2 hours post-injury? (yes/no)
            suspected_skull_fracture: Suspected open/depressed skull fracture? (yes/no)
            basilar_skull_fracture_signs: Any basilar skull fracture signs? (yes/no)
            vomiting_2_or_more: Vomited 2 or more times? (yes/no)
            age_65_or_over: Age ≥65 years? (yes/no)
            amnesia_30_min_or_more: Retrograde amnesia ≥30 minutes? (yes/no)
            dangerous_mechanism: Dangerous mechanism of injury? (yes/no)
            
        Returns:
            Dict with CT imaging recommendation and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(
            gcs_less_than_15_at_2hrs, suspected_skull_fracture,
            basilar_skull_fracture_signs, vomiting_2_or_more,
            age_65_or_over, amnesia_30_min_or_more, dangerous_mechanism
        )
        
        # Check for high-risk criteria
        has_high_risk = self._check_high_risk_criteria(
            gcs_less_than_15_at_2hrs, suspected_skull_fracture,
            basilar_skull_fracture_signs, vomiting_2_or_more, age_65_or_over
        )
        
        if has_high_risk:
            return {
                "result": "CT Required - High Risk",
                "unit": "recommendation",
                "interpretation": "The patient has high-risk criteria present. CT head imaging is recommended. High-risk criteria are 100% sensitive for predicting need for neurosurgical intervention.",
                "stage": "High Risk",
                "stage_description": "CT head recommended"
            }
        
        # Check for medium-risk criteria
        has_medium_risk = self._check_medium_risk_criteria(
            amnesia_30_min_or_more, dangerous_mechanism
        )
        
        if has_medium_risk:
            return {
                "result": "CT Required - Medium Risk",
                "unit": "recommendation",
                "interpretation": "The patient has medium-risk criteria present (but no high-risk criteria). CT head imaging is recommended. Medium-risk criteria identify patients with clinically important brain injury that may require admission.",
                "stage": "Medium Risk",
                "stage_description": "CT head recommended"
            }
        
        # No risk criteria present
        return {
            "result": "CT Not Required",
            "unit": "recommendation",
            "interpretation": "The patient has no high-risk or medium-risk criteria. CT head imaging is not required based on the Canadian CT Head Rule. The patient can be safely discharged without imaging.",
            "stage": "Low Risk",
            "stage_description": "No CT head required"
        }
    
    def _validate_inputs(self, *args):
        """Validates input parameters"""
        
        for i, param in enumerate(args):
            if param not in ["yes", "no"]:
                param_names = [
                    "gcs_less_than_15_at_2hrs", "suspected_skull_fracture",
                    "basilar_skull_fracture_signs", "vomiting_2_or_more",
                    "age_65_or_over", "amnesia_30_min_or_more", "dangerous_mechanism"
                ]
                raise ValueError(f"{param_names[i]} must be 'yes' or 'no'")
    
    def _check_high_risk_criteria(
        self,
        gcs_less_than_15_at_2hrs: str,
        suspected_skull_fracture: str,
        basilar_skull_fracture_signs: str,
        vomiting_2_or_more: str,
        age_65_or_over: str
    ) -> bool:
        """Checks for presence of any high-risk criteria"""
        
        return (
            gcs_less_than_15_at_2hrs == "yes" or
            suspected_skull_fracture == "yes" or
            basilar_skull_fracture_signs == "yes" or
            vomiting_2_or_more == "yes" or
            age_65_or_over == "yes"
        )
    
    def _check_medium_risk_criteria(
        self,
        amnesia_30_min_or_more: str,
        dangerous_mechanism: str
    ) -> bool:
        """Checks for presence of any medium-risk criteria"""
        
        return (
            amnesia_30_min_or_more == "yes" or
            dangerous_mechanism == "yes"
        )


def calculate_canadian_ct_head_rule(
    gcs_less_than_15_at_2hrs: str,
    suspected_skull_fracture: str,
    basilar_skull_fracture_signs: str,
    vomiting_2_or_more: str,
    age_65_or_over: str,
    amnesia_30_min_or_more: str,
    dangerous_mechanism: str
) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = CanadianCtHeadRuleCalculator()
    return calculator.calculate(
        gcs_less_than_15_at_2hrs=gcs_less_than_15_at_2hrs,
        suspected_skull_fracture=suspected_skull_fracture,
        basilar_skull_fracture_signs=basilar_skull_fracture_signs,
        vomiting_2_or_more=vomiting_2_or_more,
        age_65_or_over=age_65_or_over,
        amnesia_30_min_or_more=amnesia_30_min_or_more,
        dangerous_mechanism=dangerous_mechanism
    )