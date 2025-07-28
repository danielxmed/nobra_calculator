"""
Acute Gout Diagnosis Rule Calculator

A diagnostic rule for acute gouty arthritis in primary care without joint fluid analysis.
Helps clinicians risk stratify patients for gout vs non-gout arthritis and determine
which patients benefit most from joint aspiration.

References:
- Janssens HJ, et al. Arch Intern Med. 2010;170(13):1120-6.
- Kienhorst LB, et al. Rheumatology. 2015;54(4):609-14.
"""

from typing import Dict, Any


class AcuteGoutDiagnosisRuleCalculator:
    """Calculator for Acute Gout Diagnosis Rule"""
    
    def __init__(self):
        # Scoring weights for each parameter
        self.MALE_SEX_SCORES = {
            "no": 0,
            "yes": 2
        }
        
        self.PREVIOUS_ARTHRITIS_SCORES = {
            "no": 0,
            "yes": 2
        }
        
        self.ONSET_ONE_DAY_SCORES = {
            "no": 0,
            "yes": 0.5
        }
        
        self.JOINT_REDNESS_SCORES = {
            "no": 0,
            "yes": 1
        }
        
        self.FIRST_MTP_SCORES = {
            "no": 0,
            "yes": 2.5
        }
        
        self.HYPERTENSION_CVD_SCORES = {
            "no": 0,
            "yes": 1.5
        }
        
        self.ELEVATED_URIC_ACID_SCORES = {
            "no": 0,
            "yes": 3.5
        }
    
    def calculate(self, male_sex: str, previous_arthritis_attack: str, onset_within_one_day: str,
                 joint_redness: str, first_mtp_involvement: str, hypertension_or_cardiovascular: str,
                 elevated_uric_acid: str) -> Dict[str, Any]:
        """
        Calculates the Acute Gout Diagnosis Rule score
        
        Args:
            male_sex (str): "yes" or "no" for male sex
            previous_arthritis_attack (str): "yes" or "no" for previous patient-reported arthritis attack
            onset_within_one_day (str): "yes" or "no" for onset within 1 day
            joint_redness (str): "yes" or "no" for joint redness
            first_mtp_involvement (str): "yes" or "no" for first MTP joint involvement
            hypertension_or_cardiovascular (str): "yes" or "no" for hypertension or cardiovascular disease
            elevated_uric_acid (str): "yes" or "no" for serum uric acid > 5.88 mg/dL
            
        Returns:
            Dict with the calculated score and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(
            male_sex, previous_arthritis_attack, onset_within_one_day,
            joint_redness, first_mtp_involvement, hypertension_or_cardiovascular,
            elevated_uric_acid
        )
        
        # Calculate score
        score = self._calculate_score(
            male_sex, previous_arthritis_attack, onset_within_one_day,
            joint_redness, first_mtp_involvement, hypertension_or_cardiovascular,
            elevated_uric_acid
        )
        
        # Get interpretation
        interpretation = self._get_interpretation(score)
        
        return {
            "result": score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, male_sex, previous_arthritis_attack, onset_within_one_day,
                        joint_redness, first_mtp_involvement, hypertension_or_cardiovascular,
                        elevated_uric_acid):
        """Validates input parameters"""
        
        valid_options = ["yes", "no"]
        
        parameters = [
            (male_sex, "male_sex"),
            (previous_arthritis_attack, "previous_arthritis_attack"),
            (onset_within_one_day, "onset_within_one_day"),
            (joint_redness, "joint_redness"),
            (first_mtp_involvement, "first_mtp_involvement"),
            (hypertension_or_cardiovascular, "hypertension_or_cardiovascular"),
            (elevated_uric_acid, "elevated_uric_acid")
        ]
        
        for value, param_name in parameters:
            if not isinstance(value, str):
                raise ValueError(f"{param_name} must be a string")
            
            if value not in valid_options:
                raise ValueError(f"{param_name} must be either 'yes' or 'no'")
    
    def _calculate_score(self, male_sex, previous_arthritis_attack, onset_within_one_day,
                        joint_redness, first_mtp_involvement, hypertension_or_cardiovascular,
                        elevated_uric_acid):
        """Calculates the total score based on all parameters"""
        
        score = 0
        score += self.MALE_SEX_SCORES[male_sex]
        score += self.PREVIOUS_ARTHRITIS_SCORES[previous_arthritis_attack]
        score += self.ONSET_ONE_DAY_SCORES[onset_within_one_day]
        score += self.JOINT_REDNESS_SCORES[joint_redness]
        score += self.FIRST_MTP_SCORES[first_mtp_involvement]
        score += self.HYPERTENSION_CVD_SCORES[hypertension_or_cardiovascular]
        score += self.ELEVATED_URIC_ACID_SCORES[elevated_uric_acid]
        
        return score
    
    def _get_interpretation(self, score: float) -> Dict[str, str]:
        """
        Determines the interpretation based on the score
        
        Args:
            score (float): Calculated score
            
        Returns:
            Dict with interpretation details
        """
        
        if score <= 4:
            return {
                "stage": "Low Risk",
                "description": "Score ≤4",
                "interpretation": "Low likelihood of acute gout (2.2% prevalence). Gout is unlikely, consider alternative diagnoses. Joint aspiration is not typically needed. NPV 97.8%."
            }
        elif 4 < score < 8:
            return {
                "stage": "Intermediate Risk", 
                "description": "Score 4.5-7.5",
                "interpretation": "Intermediate likelihood of acute gout (31.2% prevalence). Diagnosis remains uncertain. Consider joint aspiration for synovial fluid analysis to confirm diagnosis and rule out other crystal arthropathies."
            }
        else:  # score >= 8
            return {
                "stage": "High Risk",
                "description": "Score ≥8", 
                "interpretation": "High likelihood of acute gout (80.4-82.5% prevalence). Gout is highly likely. Consider empirical treatment with anti-inflammatory therapy while awaiting confirmatory testing if needed. PPV 87%."
            }


def calculate_acute_gout_diagnosis_rule(male_sex, previous_arthritis_attack, onset_within_one_day,
                                      joint_redness, first_mtp_involvement, hypertension_or_cardiovascular,
                                      elevated_uric_acid) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = AcuteGoutDiagnosisRuleCalculator()
    return calculator.calculate(
        male_sex, previous_arthritis_attack, onset_within_one_day,
        joint_redness, first_mtp_involvement, hypertension_or_cardiovascular,
        elevated_uric_acid
    )