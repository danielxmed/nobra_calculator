"""
Canadian C-Spine Rule Calculator

The Canadian C-Spine Rule is a clinical decision tool that helps determine whether 
cervical spine imaging can be safely avoided in alert and stable trauma patients.

References:
1. Stiell IG, Wells GA, Vandemheen KL, et al. The Canadian C-spine rule for radiography 
   in alert and stable trauma patients. JAMA. 2001;286(15):1841-8.
2. Stiell IG, Clement CM, McKnight RD, et al. The Canadian C-spine rule versus the 
   NEXUS low-risk criteria in patients with trauma. N Engl J Med. 2003;349(26):2510-8.
"""

from typing import Dict, Any


class CanadianCSpineRuleCalculator:
    """Calculator for Canadian C-Spine Rule"""
    
    def __init__(self):
        pass
    
    def calculate(
        self, 
        age_65_or_over: str,
        dangerous_mechanism: str,
        paresthesias_in_extremities: str,
        simple_rear_end_mvc: str,
        sitting_position_in_ed: str,
        ambulatory_at_any_time: str,
        delayed_onset_neck_pain: str,
        absence_midline_tenderness: str,
        able_to_rotate_neck: str = "not_assessed"
    ) -> Dict[str, Any]:
        """
        Calculates the Canadian C-Spine Rule recommendation
        
        Args:
            age_65_or_over: Is patient aged ≥65 years? (yes/no)
            dangerous_mechanism: Was there a dangerous mechanism? (yes/no)
            paresthesias_in_extremities: Are there paresthesias? (yes/no)
            simple_rear_end_mvc: Simple rear-end MVC? (yes/no/not_applicable)
            sitting_position_in_ed: Sitting upright in ED? (yes/no)
            ambulatory_at_any_time: Ambulatory at any time? (yes/no)
            delayed_onset_neck_pain: Delayed onset of neck pain? (yes/no)
            absence_midline_tenderness: Absence of midline tenderness? (yes/no)
            able_to_rotate_neck: Can rotate neck 45° both ways? (yes/no/not_assessed)
            
        Returns:
            Dict with imaging recommendation and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(
            age_65_or_over, dangerous_mechanism, paresthesias_in_extremities,
            simple_rear_end_mvc, sitting_position_in_ed, ambulatory_at_any_time,
            delayed_onset_neck_pain, absence_midline_tenderness, able_to_rotate_neck
        )
        
        # Step 1: Check for high-risk factors
        has_high_risk = self._check_high_risk_factors(
            age_65_or_over, dangerous_mechanism, paresthesias_in_extremities
        )
        
        if has_high_risk:
            return {
                "result": "Imaging Required",
                "unit": "recommendation",
                "interpretation": "The patient has high-risk factors that mandate radiography (age ≥65 years, dangerous mechanism, or paresthesias in extremities). Proceed with cervical spine imaging as clinically indicated.",
                "stage": "High Risk",
                "stage_description": "Cervical spine imaging is indicated"
            }
        
        # Step 2: Check for low-risk factors
        has_low_risk = self._check_low_risk_factors(
            simple_rear_end_mvc, sitting_position_in_ed, ambulatory_at_any_time,
            delayed_onset_neck_pain, absence_midline_tenderness
        )
        
        if not has_low_risk:
            return {
                "result": "Imaging Required - No Low Risk Factors",
                "unit": "recommendation",
                "interpretation": "The patient has no high-risk factors but also lacks any low-risk factors that would allow safe assessment of range of motion. Cervical spine imaging is required.",
                "stage": "No Low Risk Factors",
                "stage_description": "Cervical spine imaging is indicated"
            }
        
        # Step 3: Assess range of motion (only if low-risk factors present)
        if able_to_rotate_neck == "yes":
            return {
                "result": "Safe to Clear Clinically",
                "unit": "recommendation",
                "interpretation": "The patient has low-risk factors allowing safe assessment of range of motion AND can actively rotate neck 45° left and right. The cervical spine can be cleared clinically without imaging.",
                "stage": "Clinically Clear",
                "stage_description": "No cervical spine imaging required"
            }
        else:
            return {
                "result": "Imaging Required - Unable to Rotate",
                "unit": "recommendation",
                "interpretation": "Although the patient has low-risk factors, they are unable to actively rotate their neck 45° left and right. Cervical spine imaging is required.",
                "stage": "Unable to Rotate",
                "stage_description": "Cervical spine imaging is indicated"
            }
    
    def _validate_inputs(self, *args):
        """Validates input parameters"""
        
        yes_no_params = args[:8]  # First 8 parameters
        for i, param in enumerate(yes_no_params):
            if param not in ["yes", "no"]:
                # Special case for simple_rear_end_mvc
                if i == 3 and param == "not_applicable":
                    continue
                param_names = [
                    "age_65_or_over", "dangerous_mechanism", "paresthesias_in_extremities",
                    "simple_rear_end_mvc", "sitting_position_in_ed", "ambulatory_at_any_time",
                    "delayed_onset_neck_pain", "absence_midline_tenderness"
                ]
                raise ValueError(f"{param_names[i]} must be 'yes' or 'no' (or 'not_applicable' for simple_rear_end_mvc)")
        
        # Validate able_to_rotate_neck
        if args[8] not in ["yes", "no", "not_assessed"]:
            raise ValueError("able_to_rotate_neck must be 'yes', 'no', or 'not_assessed'")
    
    def _check_high_risk_factors(
        self, 
        age_65_or_over: str,
        dangerous_mechanism: str,
        paresthesias_in_extremities: str
    ) -> bool:
        """Checks for presence of any high-risk factors"""
        
        return (
            age_65_or_over == "yes" or
            dangerous_mechanism == "yes" or
            paresthesias_in_extremities == "yes"
        )
    
    def _check_low_risk_factors(
        self,
        simple_rear_end_mvc: str,
        sitting_position_in_ed: str,
        ambulatory_at_any_time: str,
        delayed_onset_neck_pain: str,
        absence_midline_tenderness: str
    ) -> bool:
        """Checks for presence of any low-risk factors"""
        
        return (
            simple_rear_end_mvc == "yes" or
            sitting_position_in_ed == "yes" or
            ambulatory_at_any_time == "yes" or
            delayed_onset_neck_pain == "yes" or
            absence_midline_tenderness == "yes"
        )


def calculate_canadian_c_spine_rule(
    age_65_or_over: str,
    dangerous_mechanism: str,
    paresthesias_in_extremities: str,
    simple_rear_end_mvc: str,
    sitting_position_in_ed: str,
    ambulatory_at_any_time: str,
    delayed_onset_neck_pain: str,
    absence_midline_tenderness: str,
    able_to_rotate_neck: str = "not_assessed"
) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = CanadianCSpineRuleCalculator()
    return calculator.calculate(
        age_65_or_over=age_65_or_over,
        dangerous_mechanism=dangerous_mechanism,
        paresthesias_in_extremities=paresthesias_in_extremities,
        simple_rear_end_mvc=simple_rear_end_mvc,
        sitting_position_in_ed=sitting_position_in_ed,
        ambulatory_at_any_time=ambulatory_at_any_time,
        delayed_onset_neck_pain=delayed_onset_neck_pain,
        absence_midline_tenderness=absence_midline_tenderness,
        able_to_rotate_neck=able_to_rotate_neck
    )