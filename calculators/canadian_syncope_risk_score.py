"""
Canadian Syncope Risk Score Calculator

Predicts 30-day serious adverse events in patients presenting with syncope to the
emergency department.

References:
1. Thiruganasambandamoorthy V, Kwong K, Wells GA, et al. Development of the 
   Canadian Syncope Risk Score to predict serious adverse events after emergency 
   department assessment of syncope. CMAJ. 2016;188(12):E289-98.
2. Thiruganasambandamoorthy V, Sivilotti MLA, Le Sage N, et al. Multicenter 
   Emergency Department Validation of the Canadian Syncope Risk Score. JAMA 
   Intern Med. 2020;180(5):737-44.
"""

from typing import Dict, Any


class CanadianSyncopeRiskScoreCalculator:
    """Calculator for Canadian Syncope Risk Score"""
    
    def __init__(self):
        pass
    
    def calculate(
        self,
        vasovagal_predisposition: str,
        heart_disease_history: str,
        systolic_bp_abnormal: str,
        troponin_elevated: str,
        abnormal_qrs_axis: str,
        qrs_duration_prolonged: str,
        qtc_interval_prolonged: str,
        ed_diagnosis: str
    ) -> Dict[str, Any]:
        """
        Calculates the Canadian Syncope Risk Score
        
        Args:
            vasovagal_predisposition: Predisposition to vasovagal symptoms (yes/no)
            heart_disease_history: History of heart disease (yes/no)
            systolic_bp_abnormal: Any SBP <90 or >180 mmHg in ED (yes/no)
            troponin_elevated: Troponin above 99th percentile (yes/no)
            abnormal_qrs_axis: QRS axis <-30° or >100° (yes/no)
            qrs_duration_prolonged: QRS duration >130 ms (yes/no)
            qtc_interval_prolonged: QTc interval >480 ms (yes/no)
            ed_diagnosis: ED diagnosis (vasovagal_syncope/cardiac_syncope/neither)
            
        Returns:
            Dict with CSRS score and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(
            vasovagal_predisposition, heart_disease_history,
            systolic_bp_abnormal, troponin_elevated,
            abnormal_qrs_axis, qrs_duration_prolonged,
            qtc_interval_prolonged, ed_diagnosis
        )
        
        # Calculate total score
        score = 0
        
        # Clinical evaluation
        if vasovagal_predisposition == "yes":
            score -= 1
        
        if heart_disease_history == "yes":
            score += 1
        
        if systolic_bp_abnormal == "yes":
            score += 2
        
        # Investigations
        if troponin_elevated == "yes":
            score += 2
        
        if abnormal_qrs_axis == "yes":
            score += 1
        
        if qrs_duration_prolonged == "yes":
            score += 1
        
        if qtc_interval_prolonged == "yes":
            score += 2
        
        # ED diagnosis
        if ed_diagnosis == "vasovagal_syncope":
            score -= 2
        elif ed_diagnosis == "cardiac_syncope":
            score += 2
        # neither = 0 points (no change)
        
        # Get interpretation
        interpretation = self._get_interpretation(score)
        
        return {
            "result": score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, *args):
        """Validates input parameters"""
        
        # First 7 parameters should be yes/no
        yes_no_params = args[:7]
        for i, param in enumerate(yes_no_params):
            if param not in ["yes", "no"]:
                param_names = [
                    "vasovagal_predisposition", "heart_disease_history",
                    "systolic_bp_abnormal", "troponin_elevated",
                    "abnormal_qrs_axis", "qrs_duration_prolonged",
                    "qtc_interval_prolonged"
                ]
                raise ValueError(f"{param_names[i]} must be 'yes' or 'no'")
        
        # ED diagnosis validation
        if args[7] not in ["vasovagal_syncope", "cardiac_syncope", "neither"]:
            raise ValueError(
                "ed_diagnosis must be 'vasovagal_syncope', 'cardiac_syncope', or 'neither'"
            )
    
    def _get_interpretation(self, score: int) -> Dict[str, str]:
        """
        Determines the interpretation based on the CSRS score
        
        Args:
            score (int): Total CSRS score
            
        Returns:
            Dict with interpretation details
        """
        
        if score <= -2:
            return {
                "stage": "Very Low Risk",
                "description": "0.4-0.7% risk of serious adverse event",
                "interpretation": "Very low risk of serious adverse event within 30 days. Consider discharge home with appropriate follow-up as needed. No specific syncope workup typically required."
            }
        elif score <= 0:
            return {
                "stage": "Low Risk",
                "description": "1.2-1.9% risk of serious adverse event",
                "interpretation": "Low risk of serious adverse event within 30 days. Consider discharge home with close follow-up. Outpatient evaluation may be appropriate based on clinical judgment."
            }
        elif score <= 3:
            return {
                "stage": "Medium Risk",
                "description": "3.1-8.1% risk of serious adverse event",
                "interpretation": "Medium risk of serious adverse event within 30 days. Consider further ED evaluation and monitoring. Cardiac monitoring and additional testing may be warranted. Disposition based on findings and clinical judgment."
            }
        elif score <= 5:
            return {
                "stage": "High Risk",
                "description": "12.9-19.7% risk of serious adverse event",
                "interpretation": "High risk of serious adverse event within 30 days. Recommend admission for cardiac monitoring and expedited evaluation for underlying causes. Consider cardiology consultation."
            }
        else:  # score >= 6
            return {
                "stage": "Very High Risk",
                "description": "28.9-83.6% risk of serious adverse event",
                "interpretation": "Very high risk of serious adverse event within 30 days. Strongly recommend admission to monitored setting. Urgent cardiology consultation and comprehensive evaluation for life-threatening causes of syncope."
            }


def calculate_canadian_syncope_risk_score(
    vasovagal_predisposition: str,
    heart_disease_history: str,
    systolic_bp_abnormal: str,
    troponin_elevated: str,
    abnormal_qrs_axis: str,
    qrs_duration_prolonged: str,
    qtc_interval_prolonged: str,
    ed_diagnosis: str
) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = CanadianSyncopeRiskScoreCalculator()
    return calculator.calculate(
        vasovagal_predisposition=vasovagal_predisposition,
        heart_disease_history=heart_disease_history,
        systolic_bp_abnormal=systolic_bp_abnormal,
        troponin_elevated=troponin_elevated,
        abnormal_qrs_axis=abnormal_qrs_axis,
        qrs_duration_prolonged=qrs_duration_prolonged,
        qtc_interval_prolonged=qtc_interval_prolonged,
        ed_diagnosis=ed_diagnosis
    )