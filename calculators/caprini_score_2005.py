"""
Caprini Score for Venous Thromboembolism (2005) Calculator

Stratifies risk of venous thromboembolism (VTE) in surgical patients,
guiding prophylaxis decisions.

References:
1. Caprini JA. Thrombosis risk assessment as a guide to quality patient care. 
   Dis Mon. 2005;51(2-3):70-8.
2. Pannucci CJ, Laird S, Dimick JB, et al. A validated risk model to predict 
   90-day VTE events in postsurgical patients. Chest. 2014;145(3):567-73.
"""

from typing import Dict, Any


class CapriniScore2005Calculator:
    """Calculator for Caprini Score (2005)"""
    
    def __init__(self):
        pass
    
    def calculate(
        self,
        age_category: str,
        minor_surgery: str,
        major_surgery: str,
        hip_knee_arthroplasty: str,
        hip_pelvis_leg_fracture: str,
        acute_spinal_cord_injury: str,
        varicose_veins: str,
        current_swollen_legs: str,
        central_venous_access: str,
        inflammatory_bowel_disease: str,
        bmi_over_25: str,
        acute_myocardial_infarction: str,
        congestive_heart_failure: str,
        sepsis: str,
        serious_lung_disease: str,
        abnormal_pulmonary_function: str,
        medical_patient_bed_rest: str,
        cast_or_brace: str,
        history_of_vte: str,
        family_history_thrombosis: str,
        factor_v_leiden: str,
        prothrombin_20210a: str,
        lupus_anticoagulant: str,
        anticardiolipin_antibodies: str,
        heparin_induced_thrombocytopenia: str,
        other_congenital_thrombophilia: str,
        malignancy: str
    ) -> Dict[str, Any]:
        """
        Calculates the Caprini Score for VTE risk
        
        Args:
            age_category: Patient age category
            minor_surgery: Minor surgery <45 minutes (yes/no)
            major_surgery: Major surgery >45 minutes (yes/no)
            hip_knee_arthroplasty: Hip or knee replacement (yes/no)
            hip_pelvis_leg_fracture: Hip, pelvis, or leg fracture (yes/no)
            acute_spinal_cord_injury: Acute spinal cord injury (yes/no)
            varicose_veins: Varicose veins (yes/no)
            current_swollen_legs: Current swollen legs (yes/no)
            central_venous_access: Central venous access (yes/no)
            inflammatory_bowel_disease: Inflammatory bowel disease (yes/no)
            bmi_over_25: BMI >25 kg/m² (yes/no)
            acute_myocardial_infarction: Acute MI (yes/no)
            congestive_heart_failure: CHF <1 month (yes/no)
            sepsis: Sepsis <1 month (yes/no)
            serious_lung_disease: Serious lung disease <1 month (yes/no)
            abnormal_pulmonary_function: COPD (yes/no)
            medical_patient_bed_rest: Medical patient at bed rest (yes/no)
            cast_or_brace: Plaster cast or brace (yes/no)
            history_of_vte: History of DVT/PE (yes/no)
            family_history_thrombosis: Family history of thrombosis (yes/no)
            factor_v_leiden: Factor V Leiden (yes/no)
            prothrombin_20210a: Prothrombin 20210A (yes/no)
            lupus_anticoagulant: Lupus anticoagulant (yes/no)
            anticardiolipin_antibodies: Anticardiolipin antibodies (yes/no)
            heparin_induced_thrombocytopenia: HIT (yes/no)
            other_congenital_thrombophilia: Other thrombophilia (yes/no)
            malignancy: Malignancy present or previous (yes/no)
            
        Returns:
            Dict with Caprini score and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(
            age_category, minor_surgery, major_surgery, hip_knee_arthroplasty,
            hip_pelvis_leg_fracture, acute_spinal_cord_injury, varicose_veins,
            current_swollen_legs, central_venous_access, inflammatory_bowel_disease,
            bmi_over_25, acute_myocardial_infarction, congestive_heart_failure,
            sepsis, serious_lung_disease, abnormal_pulmonary_function,
            medical_patient_bed_rest, cast_or_brace, history_of_vte,
            family_history_thrombosis, factor_v_leiden, prothrombin_20210a,
            lupus_anticoagulant, anticardiolipin_antibodies,
            heparin_induced_thrombocytopenia, other_congenital_thrombophilia,
            malignancy
        )
        
        # Calculate total score
        score = 0
        
        # Age points
        age_points = {
            "under_41": 0,
            "41_to_60": 1,
            "61_to_74": 2,
            "75_or_older": 3
        }
        score += age_points[age_category]
        
        # 1-point risk factors
        one_point_factors = [
            minor_surgery, varicose_veins, inflammatory_bowel_disease,
            bmi_over_25, current_swollen_legs, central_venous_access
        ]
        for factor in one_point_factors:
            if factor == "yes":
                score += 1
        
        # 2-point risk factors
        two_point_factors = [
            major_surgery, acute_myocardial_infarction, congestive_heart_failure,
            sepsis, serious_lung_disease, abnormal_pulmonary_function,
            medical_patient_bed_rest, cast_or_brace
        ]
        for factor in two_point_factors:
            if factor == "yes":
                score += 2
        
        # 3-point risk factors
        three_point_factors = [
            history_of_vte, family_history_thrombosis, factor_v_leiden,
            prothrombin_20210a, lupus_anticoagulant, anticardiolipin_antibodies,
            heparin_induced_thrombocytopenia, other_congenital_thrombophilia
        ]
        for factor in three_point_factors:
            if factor == "yes":
                score += 3
        
        # 5-point risk factors
        five_point_factors = [
            hip_knee_arthroplasty, hip_pelvis_leg_fracture,
            acute_spinal_cord_injury, malignancy
        ]
        for factor in five_point_factors:
            if factor == "yes":
                score += 5
        
        # Get interpretation
        interpretation = self._get_interpretation(score)
        
        return {
            "result": score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, age_category, *yes_no_params):
        """Validates input parameters"""
        
        # Validate age category
        valid_ages = ["under_41", "41_to_60", "61_to_74", "75_or_older"]
        if age_category not in valid_ages:
            raise ValueError(f"age_category must be one of: {valid_ages}")
        
        # Validate yes/no parameters
        param_names = [
            "minor_surgery", "major_surgery", "hip_knee_arthroplasty",
            "hip_pelvis_leg_fracture", "acute_spinal_cord_injury", "varicose_veins",
            "current_swollen_legs", "central_venous_access", "inflammatory_bowel_disease",
            "bmi_over_25", "acute_myocardial_infarction", "congestive_heart_failure",
            "sepsis", "serious_lung_disease", "abnormal_pulmonary_function",
            "medical_patient_bed_rest", "cast_or_brace", "history_of_vte",
            "family_history_thrombosis", "factor_v_leiden", "prothrombin_20210a",
            "lupus_anticoagulant", "anticardiolipin_antibodies",
            "heparin_induced_thrombocytopenia", "other_congenital_thrombophilia",
            "malignancy"
        ]
        
        for i, param in enumerate(yes_no_params):
            if param not in ["yes", "no"]:
                raise ValueError(f"{param_names[i]} must be 'yes' or 'no'")
    
    def _get_interpretation(self, score: int) -> Dict[str, str]:
        """
        Determines the interpretation based on the Caprini score
        
        Args:
            score (int): Total Caprini score
            
        Returns:
            Dict with interpretation details
        """
        
        if score == 0:
            return {
                "stage": "Lowest Risk",
                "description": "Minimal risk",
                "interpretation": "Lowest risk of VTE. No specific anticoagulation prophylaxis required. Early ambulation and compression stockings recommended."
            }
        elif score <= 2:
            return {
                "stage": "Low Risk",
                "description": "Minimal risk",
                "interpretation": "Low risk of VTE. No specific anticoagulation prophylaxis required. Early ambulation, compression stockings, and intermittent pneumatic compression recommended."
            }
        elif score <= 4:
            return {
                "stage": "Moderate Risk",
                "description": "0.7% VTE risk",
                "interpretation": "Moderate risk of VTE. Consider intermittent pneumatic compression or low molecular weight heparin. Risk-benefit assessment for chemoprophylaxis recommended."
            }
        elif score <= 6:
            return {
                "stage": "High Risk",
                "description": "1.8% VTE risk",
                "interpretation": "High risk of VTE. Intermittent pneumatic compression AND low molecular weight heparin recommended. Consider extended prophylaxis based on individual risk factors."
            }
        elif score <= 8:
            return {
                "stage": "High Risk",
                "description": "4.0% VTE risk",
                "interpretation": "High risk of VTE. Intermittent pneumatic compression AND low molecular weight heparin strongly recommended. Consider extended prophylaxis for 30 days post-operatively."
            }
        else:  # score >= 9
            return {
                "stage": "Highest Risk",
                "description": "10.7% VTE risk",
                "interpretation": "Highest risk of VTE. Aggressive prophylaxis with intermittent pneumatic compression AND low molecular weight heparin mandatory. Extended prophylaxis for 30 days post-operatively strongly recommended. Consider inferior vena cava filter if anticoagulation contraindicated."
            }


def calculate_caprini_score_2005(
    age_category: str,
    minor_surgery: str,
    major_surgery: str,
    hip_knee_arthroplasty: str,
    hip_pelvis_leg_fracture: str,
    acute_spinal_cord_injury: str,
    varicose_veins: str,
    current_swollen_legs: str,
    central_venous_access: str,
    inflammatory_bowel_disease: str,
    bmi_over_25: str,
    acute_myocardial_infarction: str,
    congestive_heart_failure: str,
    sepsis: str,
    serious_lung_disease: str,
    abnormal_pulmonary_function: str,
    medical_patient_bed_rest: str,
    cast_or_brace: str,
    history_of_vte: str,
    family_history_thrombosis: str,
    factor_v_leiden: str,
    prothrombin_20210a: str,
    lupus_anticoagulant: str,
    anticardiolipin_antibodies: str,
    heparin_induced_thrombocytopenia: str,
    other_congenital_thrombophilia: str,
    malignancy: str
) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = CapriniScore2005Calculator()
    return calculator.calculate(
        age_category=age_category,
        minor_surgery=minor_surgery,
        major_surgery=major_surgery,
        hip_knee_arthroplasty=hip_knee_arthroplasty,
        hip_pelvis_leg_fracture=hip_pelvis_leg_fracture,
        acute_spinal_cord_injury=acute_spinal_cord_injury,
        varicose_veins=varicose_veins,
        current_swollen_legs=current_swollen_legs,
        central_venous_access=central_venous_access,
        inflammatory_bowel_disease=inflammatory_bowel_disease,
        bmi_over_25=bmi_over_25,
        acute_myocardial_infarction=acute_myocardial_infarction,
        congestive_heart_failure=congestive_heart_failure,
        sepsis=sepsis,
        serious_lung_disease=serious_lung_disease,
        abnormal_pulmonary_function=abnormal_pulmonary_function,
        medical_patient_bed_rest=medical_patient_bed_rest,
        cast_or_brace=cast_or_brace,
        history_of_vte=history_of_vte,
        family_history_thrombosis=family_history_thrombosis,
        factor_v_leiden=factor_v_leiden,
        prothrombin_20210a=prothrombin_20210a,
        lupus_anticoagulant=lupus_anticoagulant,
        anticardiolipin_antibodies=anticardiolipin_antibodies,
        heparin_induced_thrombocytopenia=heparin_induced_thrombocytopenia,
        other_congenital_thrombophilia=other_congenital_thrombophilia,
        malignancy=malignancy
    )