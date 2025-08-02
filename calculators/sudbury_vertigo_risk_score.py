"""
Sudbury Vertigo Risk Score Calculator

The Sudbury Vertigo Risk Score is a clinical risk stratification tool to identify patients 
at risk for serious causes of vertigo (stroke, TIA, vertebral artery dissection, or brain tumor) 
in the emergency department.

References:
1. Lelli D, Dinh J, Ahuja N, et al. Development of a Clinical Risk Score to Risk Stratify 
   for a Serious Cause of Vertigo in Patients Presenting to the Emergency Department. 
   Ann Emerg Med. 2024 Nov;84(5):500-511. doi: 10.1016/j.annemergmed.2024.06.003.
2. de Guise C, Chagnon M, Boudier-Revéret M, et al. Validation of the Sudbury Vertigo 
   Risk Score to risk stratify for a serious cause of vertigo. Acad Emerg Med. 2024 
   Dec;31(12):1218-1227. doi: 10.1111/acem.14950.
"""

from typing import Dict, Any


class SudburyVertigoRiskScoreCalculator:
    """Calculator for Sudbury Vertigo Risk Score"""
    
    def __init__(self):
        # Note: Exact point values not publicly available yet
        # Using placeholder values based on score range (-4 to 17) and components
        # These will need to be updated when official values are published
        self.MALE_SEX_POINTS = 3
        self.AGE_OVER_65_POINTS = 3
        self.HYPERTENSION_POINTS = 3
        self.DIABETES_POINTS = 2
        self.MOTOR_SENSORY_DEFICITS_POINTS = 3
        self.CEREBELLAR_SIGNS_POINTS = 3
        self.BPPV_DIAGNOSIS_POINTS = -4  # Negative points as BPPV is protective
    
    def calculate(self, male_sex: str, age_over_65: str, hypertension: str, 
                  diabetes: str, motor_sensory_deficits: str, cerebellar_signs: str,
                  bppv_diagnosis: str) -> Dict[str, Any]:
        """
        Calculates the Sudbury Vertigo Risk Score
        
        Args:
            male_sex: "yes" or "no" - Patient is male
            age_over_65: "yes" or "no" - Patient age is over 65 years
            hypertension: "yes" or "no" - History of hypertension
            diabetes: "yes" or "no" - History of diabetes mellitus
            motor_sensory_deficits: "yes" or "no" - Motor or sensory deficits on examination
            cerebellar_signs: "yes" or "no" - Cerebellar signs/symptoms
            bppv_diagnosis: "yes" or "no" - Clinical diagnosis of BPPV
            
        Returns:
            Dict with the score and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(male_sex, age_over_65, hypertension, diabetes,
                            motor_sensory_deficits, cerebellar_signs, bppv_diagnosis)
        
        # Calculate score
        score = 0
        
        if male_sex == "yes":
            score += self.MALE_SEX_POINTS
            
        if age_over_65 == "yes":
            score += self.AGE_OVER_65_POINTS
            
        if hypertension == "yes":
            score += self.HYPERTENSION_POINTS
            
        if diabetes == "yes":
            score += self.DIABETES_POINTS
            
        if motor_sensory_deficits == "yes":
            score += self.MOTOR_SENSORY_DEFICITS_POINTS
            
        if cerebellar_signs == "yes":
            score += self.CEREBELLAR_SIGNS_POINTS
            
        if bppv_diagnosis == "yes":
            score += self.BPPV_DIAGNOSIS_POINTS
        
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
        """Validates all input parameters"""
        
        parameter_names = [
            "male_sex", "age_over_65", "hypertension", "diabetes",
            "motor_sensory_deficits", "cerebellar_signs", "bppv_diagnosis"
        ]
        
        for i, value in enumerate(args):
            if value not in ["yes", "no"]:
                raise ValueError(f"{parameter_names[i]} must be 'yes' or 'no'")
    
    def _get_interpretation(self, score: int) -> Dict[str, str]:
        """
        Determines the interpretation based on the score
        
        Args:
            score: Calculated Sudbury Vertigo Risk Score
            
        Returns:
            Dict with interpretation details
        """
        
        if score < 5:
            return {
                "stage": "Low Risk",
                "description": "0% risk of serious diagnosis",
                "interpretation": (
                    "Score <5 has 100% sensitivity for ruling out serious causes of vertigo. "
                    "Consider outpatient management without imaging if no other concerning features. "
                    "Consider BPPV or vestibular neuritis as likely diagnoses."
                )
            }
        elif score >= 5 and score <= 8:
            return {
                "stage": "Moderate Risk",
                "description": "2.1% risk of serious diagnosis",
                "interpretation": (
                    "Low but non-zero risk of serious cause. Consider further clinical assessment, "
                    "observation, or targeted imaging based on clinical judgment and specific symptoms."
                )
            }
        else:  # score > 8
            return {
                "stage": "High Risk",
                "description": "41% risk of serious diagnosis",
                "interpretation": (
                    "High risk for serious central cause including stroke, TIA, vertebral artery "
                    "dissection, or brain tumor. Strongly consider urgent neuroimaging (CT/MRI) "
                    "and neurological consultation."
                )
            }


def calculate_sudbury_vertigo_risk_score(male_sex: str, age_over_65: str, hypertension: str, 
                                        diabetes: str, motor_sensory_deficits: str, 
                                        cerebellar_signs: str, bppv_diagnosis: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = SudburyVertigoRiskScoreCalculator()
    return calculator.calculate(male_sex, age_over_65, hypertension, diabetes,
                               motor_sensory_deficits, cerebellar_signs, bppv_diagnosis)