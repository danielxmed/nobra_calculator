"""
Canadian Transient Ischemic Attack (TIA) Score Calculator

Identifies risk of stroke, carotid endarterectomy, or carotid artery stenting
within 7 days in patients who experienced TIA symptoms.

References:
1. Perry JJ, Sharma M, Sivilotti ML, et al. A prospective cohort study of patients 
   with transient ischemic attack to identify high-risk clinical characteristics. 
   Stroke. 2014;45(1):92-100.
2. Perry JJ, Sharma M, Sivilotti ML, et al. Prospective validation of the ABCD2 
   score for patients in the emergency department with transient ischemic attack. 
   CMAJ. 2011;183(10):1137-45.
"""

from typing import Dict, Any


class CanadianTiaScoreCalculator:
    """Calculator for Canadian TIA Score"""
    
    def __init__(self):
        pass
    
    def calculate(
        self,
        first_tia_lifetime: str,
        symptoms_ten_minutes: str,
        history_carotid_stenosis: str,
        on_antiplatelet_therapy: str,
        history_gait_disturbance: str,
        history_unilateral_weakness: str,
        history_vertigo: str,
        diastolic_bp_110: str,
        dysarthria_aphasia: str,
        atrial_fibrillation_ecg: str,
        infarction_on_ct: str,
        platelet_count_400: str,
        glucose_15_mmol: str
    ) -> Dict[str, Any]:
        """
        Calculates the Canadian TIA Score
        
        Args:
            first_tia_lifetime: First TIA episode in lifetime (yes/no)
            symptoms_ten_minutes: Symptoms lasted ≥10 minutes (yes/no)
            history_carotid_stenosis: Known carotid stenosis (yes/no)
            on_antiplatelet_therapy: Already on antiplatelet therapy (yes/no)
            history_gait_disturbance: Gait disturbance during TIA (yes/no)
            history_unilateral_weakness: Unilateral weakness during TIA (yes/no)
            history_vertigo: Vertigo during TIA (yes/no)
            diastolic_bp_110: Initial diastolic BP ≥110 mmHg (yes/no)
            dysarthria_aphasia: Dysarthria or aphasia (yes/no)
            atrial_fibrillation_ecg: Atrial fibrillation on ECG (yes/no)
            infarction_on_ct: Infarction on CT scan (yes/no)
            platelet_count_400: Platelet count ≥400×10⁹/L (yes/no)
            glucose_15_mmol: Glucose ≥15 mmol/L (yes/no)
            
        Returns:
            Dict with Canadian TIA score and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(
            first_tia_lifetime, symptoms_ten_minutes, history_carotid_stenosis,
            on_antiplatelet_therapy, history_gait_disturbance, history_unilateral_weakness,
            history_vertigo, diastolic_bp_110, dysarthria_aphasia,
            atrial_fibrillation_ecg, infarction_on_ct, platelet_count_400,
            glucose_15_mmol
        )
        
        # Calculate total score
        score = 0
        
        # Clinical history variables
        if first_tia_lifetime == "yes":
            score += 2
        
        if symptoms_ten_minutes == "yes":
            score += 2
        
        if history_carotid_stenosis == "yes":
            score += 2
        
        if on_antiplatelet_therapy == "yes":
            score += 3
        
        if history_gait_disturbance == "yes":
            score += 1
        
        if history_unilateral_weakness == "yes":
            score += 1
        
        if history_vertigo == "yes":
            score -= 3  # Only negative score
        
        # Physical examination variables
        if diastolic_bp_110 == "yes":
            score += 3
        
        if dysarthria_aphasia == "yes":
            score += 1
        
        # Investigation variables
        if atrial_fibrillation_ecg == "yes":
            score += 2
        
        if infarction_on_ct == "yes":
            score += 1
        
        if platelet_count_400 == "yes":
            score += 2
        
        if glucose_15_mmol == "yes":
            score += 3
        
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
        
        # All 13 parameters should be yes/no
        param_names = [
            "first_tia_lifetime", "symptoms_ten_minutes", "history_carotid_stenosis",
            "on_antiplatelet_therapy", "history_gait_disturbance", "history_unilateral_weakness",
            "history_vertigo", "diastolic_bp_110", "dysarthria_aphasia",
            "atrial_fibrillation_ecg", "infarction_on_ct", "platelet_count_400",
            "glucose_15_mmol"
        ]
        
        for i, param in enumerate(args):
            if param not in ["yes", "no"]:
                raise ValueError(f"{param_names[i]} must be 'yes' or 'no'")
    
    def _get_interpretation(self, score: int) -> Dict[str, str]:
        """
        Determines the interpretation based on the Canadian TIA score
        
        Args:
            score (int): Total Canadian TIA score
            
        Returns:
            Dict with interpretation details
        """
        
        if score <= 3:
            return {
                "stage": "Low Risk",
                "description": "0.01-0.5% risk of stroke/intervention within 7 days",
                "interpretation": "Low risk of stroke, carotid endarterectomy, or carotid artery stenting within 7 days. Consider discharge home with outpatient follow-up. Routine investigations and specialist referral can be arranged non-urgently."
            }
        elif score <= 8:
            return {
                "stage": "Medium Risk",
                "description": "1-5% risk of stroke/intervention within 7 days",
                "interpretation": "Medium risk of stroke, carotid endarterectomy, or carotid artery stenting within 7 days. Consider admission or urgent outpatient workup within 24-48 hours. Expedited imaging and specialist consultation recommended."
            }
        else:  # score >= 9
            return {
                "stage": "High Risk",
                "description": "5.9-27.6% risk of stroke/intervention within 7 days",
                "interpretation": "High risk of stroke, carotid endarterectomy, or carotid artery stenting within 7 days. Recommend admission for monitoring and urgent evaluation. Immediate imaging, specialist consultation, and consideration of antithrombotic therapy indicated."
            }


def calculate_canadian_tia_score(
    first_tia_lifetime: str,
    symptoms_ten_minutes: str,
    history_carotid_stenosis: str,
    on_antiplatelet_therapy: str,
    history_gait_disturbance: str,
    history_unilateral_weakness: str,
    history_vertigo: str,
    diastolic_bp_110: str,
    dysarthria_aphasia: str,
    atrial_fibrillation_ecg: str,
    infarction_on_ct: str,
    platelet_count_400: str,
    glucose_15_mmol: str
) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = CanadianTiaScoreCalculator()
    return calculator.calculate(
        first_tia_lifetime=first_tia_lifetime,
        symptoms_ten_minutes=symptoms_ten_minutes,
        history_carotid_stenosis=history_carotid_stenosis,
        on_antiplatelet_therapy=on_antiplatelet_therapy,
        history_gait_disturbance=history_gait_disturbance,
        history_unilateral_weakness=history_unilateral_weakness,
        history_vertigo=history_vertigo,
        diastolic_bp_110=diastolic_bp_110,
        dysarthria_aphasia=dysarthria_aphasia,
        atrial_fibrillation_ecg=atrial_fibrillation_ecg,
        infarction_on_ct=infarction_on_ct,
        platelet_count_400=platelet_count_400,
        glucose_15_mmol=glucose_15_mmol
    )