"""
Marburg Heart Score (MHS) Calculator

Rules out coronary artery disease in primary care patients aged 35 years and older 
presenting with chest pain using five equally weighted clinical criteria.

References:
1. Bösner S, Haasenritter J, Becker A, Karatolios K, Vaucher P, Gencer B, et al. 
   Ruling out coronary artery disease in primary care: development and validation of 
   a simple prediction rule. CMAJ. 2010 Sep 7;182(12):1295-300. doi: 10.1503/cmaj.100212.
2. Haasenritter J, Bösner S, Vaucher P, Herzig L, Heinzel-Gutenbrunner M, Baum E, et al. 
   Ruling out coronary heart disease in primary care: external validation of a clinical 
   prediction rule. Br J Gen Pract. 2012 Jun;62(599):e415-21. doi: 10.3399/bjgp12X649106.
"""

from typing import Dict, Any


class MarburgHeartScoreCalculator:
    """Calculator for Marburg Heart Score (MHS)"""
    
    def __init__(self):
        # Risk thresholds
        self.LOW_RISK_THRESHOLD = 3  # Score <3 is low risk
        
        # Valid options
        self.VALID_YES_NO_OPTIONS = ["yes", "no"]
    
    def calculate(self, age_sex_criteria: str, known_vascular_disease: str,
                  pain_worse_with_exercise: str, pain_not_reproducible_palpation: str,
                  patient_assumes_cardiac: str) -> Dict[str, Any]:
        """
        Calculates Marburg Heart Score for CAD risk assessment
        
        Args:
            age_sex_criteria (str): Female ≥65 years or male ≥55 years ("yes"/"no")
            known_vascular_disease (str): Known CAD, cerebrovascular, or PVD ("yes"/"no")
            pain_worse_with_exercise (str): Pain worsens with exercise ("yes"/"no")
            pain_not_reproducible_palpation (str): Pain NOT reproducible with palpation ("yes"/"no")
            patient_assumes_cardiac (str): Patient assumes pain is cardiac ("yes"/"no")
            
        Returns:
            Dict with the result and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(age_sex_criteria, known_vascular_disease, pain_worse_with_exercise,
                             pain_not_reproducible_palpation, patient_assumes_cardiac)
        
        # Calculate individual criteria scores
        criteria_scores = self._calculate_criteria_scores(
            age_sex_criteria, known_vascular_disease, pain_worse_with_exercise,
            pain_not_reproducible_palpation, patient_assumes_cardiac
        )
        
        # Calculate total score
        total_score = sum(criteria_scores.values())
        
        # Get interpretation
        interpretation = self._get_interpretation(total_score)
        
        # Get detailed assessment
        assessment_data = self._get_assessment_data(total_score, criteria_scores)
        
        return {
            "result": {
                "total_score": total_score,
                "criteria_scores": criteria_scores,
                "criteria_breakdown": {
                    "age_sex_criteria": f"Age/Sex criteria: {'Met' if criteria_scores['age_sex'] else 'Not met'}",
                    "known_vascular_disease": f"Known vascular disease: {'Present' if criteria_scores['vascular_disease'] else 'Absent'}",
                    "pain_worse_exercise": f"Pain worse with exercise: {'Yes' if criteria_scores['exercise_pain'] else 'No'}",
                    "pain_not_reproducible": f"Pain NOT reproducible: {'Yes' if criteria_scores['not_reproducible'] else 'No'}",
                    "patient_assumes_cardiac": f"Patient assumes cardiac: {'Yes' if criteria_scores['assumes_cardiac'] else 'No'}"
                },
                "assessment_data": assessment_data
            },
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, age_sex_criteria: str, known_vascular_disease: str,
                        pain_worse_with_exercise: str, pain_not_reproducible_palpation: str,
                        patient_assumes_cardiac: str):
        """Validates input parameters"""
        
        # Validate yes/no parameters
        yes_no_params = {
            "age_sex_criteria": age_sex_criteria,
            "known_vascular_disease": known_vascular_disease,
            "pain_worse_with_exercise": pain_worse_with_exercise,
            "pain_not_reproducible_palpation": pain_not_reproducible_palpation,
            "patient_assumes_cardiac": patient_assumes_cardiac
        }
        
        for param_name, param_value in yes_no_params.items():
            if not isinstance(param_value, str):
                raise ValueError(f"{param_name} must be a string")
            
            if param_value.lower() not in [option.lower() for option in self.VALID_YES_NO_OPTIONS]:
                raise ValueError(f"{param_name} must be 'yes' or 'no'")
    
    def _calculate_criteria_scores(self, age_sex_criteria: str, known_vascular_disease: str,
                                  pain_worse_with_exercise: str, pain_not_reproducible_palpation: str,
                                  patient_assumes_cardiac: str) -> Dict[str, int]:
        """Calculates individual MHS criteria scores"""
        
        return {
            "age_sex": 1 if age_sex_criteria.lower() == "yes" else 0,
            "vascular_disease": 1 if known_vascular_disease.lower() == "yes" else 0,
            "exercise_pain": 1 if pain_worse_with_exercise.lower() == "yes" else 0,
            "not_reproducible": 1 if pain_not_reproducible_palpation.lower() == "yes" else 0,
            "assumes_cardiac": 1 if patient_assumes_cardiac.lower() == "yes" else 0
        }
    
    def _get_assessment_data(self, total_score: int, criteria_scores: Dict[str, int]) -> Dict[str, str]:
        """
        Returns detailed assessment data based on MHS score
        
        Args:
            total_score (int): Total MHS score
            criteria_scores (Dict[str, int]): Individual criteria scores
            
        Returns:
            Dict with assessment information
        """
        
        # Determine risk category and CAD probability
        if total_score < self.LOW_RISK_THRESHOLD:  # 0-2 points
            risk_level = "Low Risk"
            cad_probability = "~3%"
            recommendation = "Outpatient evaluation as needed"
            urgency = "Non-urgent"
        else:  # 3-5 points
            risk_level = "Higher Risk"
            cad_probability = "~23%"
            recommendation = "Consider urgent evaluation or inpatient admission"
            urgency = "Urgent evaluation warranted"
        
        # Count positive criteria
        positive_criteria = sum(criteria_scores.values())
        
        return {
            "risk_level": risk_level,
            "cad_probability": cad_probability,
            "recommendation": recommendation,
            "urgency": urgency,
            "positive_criteria": f"{positive_criteria}/5 criteria positive",
            "score_threshold": f"Cut-off ≥{self.LOW_RISK_THRESHOLD} points for higher risk",
            "sensitivity": "87.1% (original validation)",
            "specificity": "80.8% (original validation)",
            "next_steps": "Clinical judgment should supplement score-based decisions"
        }
    
    def _get_interpretation(self, total_score: int) -> Dict[str, str]:
        """
        Determines the risk category and interpretation
        
        Args:
            total_score (int): Total MHS score
            
        Returns:
            Dict with risk category and clinical interpretation
        """
        
        if total_score < self.LOW_RISK_THRESHOLD:  # 0-2 points
            return {
                "stage": "Low Risk",
                "description": "Low risk for coronary artery disease",
                "interpretation": (
                    f"Marburg Heart Score of {total_score} indicates low risk for coronary artery disease "
                    f"with approximately 3% CAD probability. These patients are highly unlikely to have "
                    f"unstable CAD and can be managed with outpatient evaluation as needed. This low-risk "
                    f"stratification helps avoid unnecessary urgent referrals while maintaining patient safety. "
                    f"Consider routine follow-up with primary care provider, cardiovascular risk factor "
                    f"assessment and modification (blood pressure, cholesterol, diabetes, smoking cessation), "
                    f"symptom monitoring with clear return precautions, and lifestyle counseling for "
                    f"cardiovascular health promotion."
                )
            }
        else:  # 3-5 points
            return {
                "stage": "Higher Risk",
                "description": "Higher risk for coronary artery disease requiring urgent evaluation",
                "interpretation": (
                    f"Marburg Heart Score of {total_score} indicates higher risk for coronary artery disease "
                    f"with approximately 23% CAD probability. These patients warrant consideration for urgent "
                    f"evaluation or inpatient admission for comprehensive cardiac assessment. Recommended "
                    f"evaluation includes 12-lead ECG, cardiac biomarkers (troponin), chest X-ray, and "
                    f"consideration for stress testing or coronary imaging as clinically indicated. The modest "
                    f"positive predictive value (23%) emphasizes the need for thorough evaluation rather than "
                    f"assumption of CAD presence. Clinical judgment should guide the intensity and setting of "
                    f"further evaluation based on patient presentation, comorbidities, and clinical stability."
                )
            }


def calculate_marburg_heart_score(age_sex_criteria: str, known_vascular_disease: str,
                                 pain_worse_with_exercise: str, pain_not_reproducible_palpation: str,
                                 patient_assumes_cardiac: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = MarburgHeartScoreCalculator()
    return calculator.calculate(age_sex_criteria, known_vascular_disease, pain_worse_with_exercise,
                               pain_not_reproducible_palpation, patient_assumes_cardiac)