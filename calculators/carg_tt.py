"""
Cancer and Aging Research Group Chemotherapy Toxicity Tool (CARG-TT) Calculator

Estimates the risk of severe chemotherapy-related side effects (Grade 3 or greater
toxicity) in older cancer patients (age >65).

References:
1. Hurria A, Togawa K, Mohile SG, et al. Predicting chemotherapy toxicity in older 
   adults with cancer: a prospective multicenter study. J Clin Oncol. 2011;29(25):3457-65.
2. Magnuson A, Sattar S, Nightingale G, et al. A practical guide to geriatric 
   syndromes in older adults with cancer. Am Soc Clin Oncol Educ Book. 2019;39:e96-e109.
"""

from typing import Dict, Any


class CargTtCalculator:
    """Calculator for CARG-TT Score"""
    
    def __init__(self):
        pass
    
    def calculate(
        self,
        sex: str,
        age_72_or_older: str,
        gi_gu_cancer: str,
        standard_dose_chemo: str,
        polychemotherapy: str,
        hemoglobin_low: str,
        creatinine_clearance_low: str,
        hearing_impaired: str,
        falls_past_6_months: str,
        medication_assistance: str,
        walking_limited: str,
        social_activity_decreased: str
    ) -> Dict[str, Any]:
        """
        Calculates the CARG-TT Score
        
        Args:
            sex: Patient sex (male/female)
            age_72_or_older: Age ≥72 years (yes/no)
            gi_gu_cancer: GI or GU cancer type (yes/no)
            standard_dose_chemo: Standard-dose chemotherapy (yes/no)
            polychemotherapy: >1 chemotherapy drug (yes/no)
            hemoglobin_low: Low hemoglobin (males <11, females <10 g/dL) (yes/no)
            creatinine_clearance_low: CrCl <34 mL/min (yes/no)
            hearing_impaired: Hearing fair/poor/deaf (yes/no)
            falls_past_6_months: Falls in past 6 months (yes/no)
            medication_assistance: Needs medication assistance (yes/no)
            walking_limited: Limited walking ≥1 block (yes/no)
            social_activity_decreased: Decreased social activity due to health (yes/no)
            
        Returns:
            Dict with CARG-TT score and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(
            sex, age_72_or_older, gi_gu_cancer, standard_dose_chemo,
            polychemotherapy, hemoglobin_low, creatinine_clearance_low,
            hearing_impaired, falls_past_6_months, medication_assistance,
            walking_limited, social_activity_decreased
        )
        
        # Calculate total score
        score = 0
        
        # Age (2 points if ≥72 years)
        if age_72_or_older == "yes":
            score += 2
        
        # Cancer type (2 points if GI/GU)
        if gi_gu_cancer == "yes":
            score += 2
        
        # Dosage (2 points if standard dose)
        if standard_dose_chemo == "yes":
            score += 2
        
        # Number of drugs (2 points if polychemotherapy)
        if polychemotherapy == "yes":
            score += 2
        
        # Hemoglobin (3 points if low)
        if hemoglobin_low == "yes":
            score += 3
        
        # Creatinine clearance (3 points if <34 mL/min)
        if creatinine_clearance_low == "yes":
            score += 3
        
        # Hearing (2 points if impaired)
        if hearing_impaired == "yes":
            score += 2
        
        # Falls (3 points if history of falls)
        if falls_past_6_months == "yes":
            score += 3
        
        # Medication assistance (1 point if needs help)
        if medication_assistance == "yes":
            score += 1
        
        # Walking limitation (2 points if limited)
        if walking_limited == "yes":
            score += 2
        
        # Social activity (1 point if decreased)
        if social_activity_decreased == "yes":
            score += 1
        
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
        
        # First parameter (sex) should be male/female
        if args[0] not in ["male", "female"]:
            raise ValueError("sex must be 'male' or 'female'")
        
        # All other parameters should be yes/no
        yes_no_params = args[1:]
        param_names = [
            "age_72_or_older", "gi_gu_cancer", "standard_dose_chemo",
            "polychemotherapy", "hemoglobin_low", "creatinine_clearance_low",
            "hearing_impaired", "falls_past_6_months", "medication_assistance",
            "walking_limited", "social_activity_decreased"
        ]
        
        for i, param in enumerate(yes_no_params):
            if param not in ["yes", "no"]:
                raise ValueError(f"{param_names[i]} must be 'yes' or 'no'")
    
    def _get_interpretation(self, score: int) -> Dict[str, str]:
        """
        Determines the interpretation based on the CARG-TT score
        
        Args:
            score (int): Total CARG-TT score
            
        Returns:
            Dict with interpretation details
        """
        
        if score <= 5:
            return {
                "stage": "Low Risk",
                "description": "30% risk of grade ≥3 toxicity",
                "interpretation": "Low risk of severe chemotherapy toxicity. Standard chemotherapy regimens can generally be considered. Monitor closely for side effects and provide supportive care as needed."
            }
        elif score <= 9:
            return {
                "stage": "Intermediate Risk",
                "description": "52% risk of grade ≥3 toxicity",
                "interpretation": "Intermediate risk of severe chemotherapy toxicity. Consider dose reduction, alternative regimens, or enhanced supportive care measures. Close monitoring and frequent follow-up recommended."
            }
        else:  # score >= 10
            return {
                "stage": "High Risk",
                "description": "83% risk of grade ≥3 toxicity",
                "interpretation": "High risk of severe chemotherapy toxicity. Strongly consider dose reduction, single-agent therapy, or alternative treatment approaches. Intensive supportive care and very frequent monitoring essential."
            }


def calculate_carg_tt(
    sex: str,
    age_72_or_older: str,
    gi_gu_cancer: str,
    standard_dose_chemo: str,
    polychemotherapy: str,
    hemoglobin_low: str,
    creatinine_clearance_low: str,
    hearing_impaired: str,
    falls_past_6_months: str,
    medication_assistance: str,
    walking_limited: str,
    social_activity_decreased: str
) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = CargTtCalculator()
    return calculator.calculate(
        sex=sex,
        age_72_or_older=age_72_or_older,
        gi_gu_cancer=gi_gu_cancer,
        standard_dose_chemo=standard_dose_chemo,
        polychemotherapy=polychemotherapy,
        hemoglobin_low=hemoglobin_low,
        creatinine_clearance_low=creatinine_clearance_low,
        hearing_impaired=hearing_impaired,
        falls_past_6_months=falls_past_6_months,
        medication_assistance=medication_assistance,
        walking_limited=walking_limited,
        social_activity_decreased=social_activity_decreased
    )