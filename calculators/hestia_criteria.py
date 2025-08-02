"""
Hestia Criteria for Outpatient Pulmonary Embolism Treatment Calculator

Identifies low-risk PE patients who may be safe for outpatient management.

References:
- Zondag W, et al. J Thromb Haemost. 2011;9(8):1500-7.
- Zondag W, et al. Thromb Haemost. 2013;109(1):47-52.
"""

from typing import Dict, Any


class HestiaCriteriaCalculator:
    """Calculator for Hestia Criteria"""
    
    def __init__(self):
        # Each criterion is worth 1 point if present
        self.CRITERION_POINTS = 1
        
        # Threshold for low risk
        self.LOW_RISK_THRESHOLD = 0
    
    def calculate(self, hemodynamically_unstable: str, thrombolysis_embolectomy: str,
                  active_bleeding: str, oxygen_24hr: str, pe_on_anticoagulation: str,
                  severe_pain_iv_meds: str, medical_social_reason: str,
                  creatinine_clearance_low: str, severe_liver_impairment: str,
                  pregnant: str, history_of_hit: str) -> Dict[str, Any]:
        """
        Calculates the Hestia Criteria score
        
        Args:
            hemodynamically_unstable (str): "yes" or "no"
            thrombolysis_embolectomy (str): "yes" or "no"
            active_bleeding (str): "yes" or "no"
            oxygen_24hr (str): "yes" or "no"
            pe_on_anticoagulation (str): "yes" or "no"
            severe_pain_iv_meds (str): "yes" or "no"
            medical_social_reason (str): "yes" or "no"
            creatinine_clearance_low (str): "yes" or "no"
            severe_liver_impairment (str): "yes" or "no"
            pregnant (str): "yes" or "no"
            history_of_hit (str): "yes" or "no"
            
        Returns:
            Dict with the result and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(
            hemodynamically_unstable, thrombolysis_embolectomy, active_bleeding,
            oxygen_24hr, pe_on_anticoagulation, severe_pain_iv_meds,
            medical_social_reason, creatinine_clearance_low, severe_liver_impairment,
            pregnant, history_of_hit
        )
        
        # Calculate score (count of 'yes' responses)
        score = 0
        
        criteria = [
            hemodynamically_unstable,
            thrombolysis_embolectomy,
            active_bleeding,
            oxygen_24hr,
            pe_on_anticoagulation,
            severe_pain_iv_meds,
            medical_social_reason,
            creatinine_clearance_low,
            severe_liver_impairment,
            pregnant,
            history_of_hit
        ]
        
        for criterion in criteria:
            if criterion == "yes":
                score += self.CRITERION_POINTS
        
        # Get interpretation
        interpretation = self._get_interpretation(score)
        
        return {
            "result": score,
            "unit": "criteria met",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, *args):
        """Validates that all inputs are either 'yes' or 'no'"""
        
        valid_responses = ["yes", "no"]
        
        for i, arg in enumerate(args):
            if arg not in valid_responses:
                raise ValueError(f"Parameter {i+1} must be one of {valid_responses}")
    
    def _get_interpretation(self, score: int) -> Dict[str, str]:
        """
        Determines the interpretation based on the score
        
        Args:
            score (int): Number of criteria met
            
        Returns:
            Dict with interpretation
        """
        
        if score == self.LOW_RISK_THRESHOLD:
            return {
                "stage": "Low Risk",
                "description": "Suitable for outpatient treatment",
                "interpretation": "Patient meets criteria for outpatient management. "
                                "Associated with 0% mortality and 2% VTE recurrence rate. "
                                "Consider for home treatment with appropriate anticoagulation "
                                "and close follow-up."
            }
        else:
            return {
                "stage": "Not Low Risk",
                "description": "Not suitable for outpatient treatment",
                "interpretation": f"Patient has {score} exclusion criteria and should be "
                                "considered for inpatient management. Hospitalization "
                                "recommended for closer monitoring and treatment."
            }


def calculate_hestia_criteria(hemodynamically_unstable: str, thrombolysis_embolectomy: str,
                              active_bleeding: str, oxygen_24hr: str, pe_on_anticoagulation: str,
                              severe_pain_iv_meds: str, medical_social_reason: str,
                              creatinine_clearance_low: str, severe_liver_impairment: str,
                              pregnant: str, history_of_hit: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = HestiaCriteriaCalculator()
    return calculator.calculate(
        hemodynamically_unstable, thrombolysis_embolectomy, active_bleeding,
        oxygen_24hr, pe_on_anticoagulation, severe_pain_iv_meds,
        medical_social_reason, creatinine_clearance_low, severe_liver_impairment,
        pregnant, history_of_hit
    )