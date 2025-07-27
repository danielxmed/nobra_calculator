"""
4-Level Pulmonary Embolism Clinical Probability Score (4PEPS) Calculator

Clinical probability score for suspected pulmonary embolism using 13 clinical variables 
to safely decrease imaging testing needs.

Reference: Roy PM, et al. JAMA Cardiol. 2021;6(6):669-677.
"""

from typing import Dict, Any


class FourPepsCalculator:
    """Calculator for 4-Level Pulmonary Embolism Clinical Probability Score (4PEPS)"""
    
    def __init__(self):
        # Scoring weights for each criterion
        self.AGE_WEIGHTS = {
            "under_50": -2,
            "50_to_64": -1,
            "65_or_over": 0
        }
        
        self.CRITERION_WEIGHTS = {
            "chronic_respiratory_disease": -1,
            "heart_rate_under_80": -1,
            "chest_pain_dyspnea": 1,
            "male_gender": 2,
            "hormonal_treatment": 2,
            "personal_history_vte": 2,
            "syncope": 2,
            "immobility_4_weeks": 2,
            "oxygen_saturation_under_95": 3,
            "calf_pain_edema": 3,
            "pe_most_likely": 5
        }
    
    def calculate(self, age_category: str, chronic_respiratory_disease: str, 
                 heart_rate_under_80: str, chest_pain_dyspnea: str, male_gender: str,
                 hormonal_treatment: str, personal_history_vte: str, syncope: str,
                 immobility_4_weeks: str, oxygen_saturation_under_95: str,
                 calf_pain_edema: str, pe_most_likely: str) -> Dict[str, Any]:
        """
        Calculates the 4PEPS score using the provided clinical parameters
        
        Args:
            age_category (str): Age category (under_50, 50_to_64, 65_or_over)
            chronic_respiratory_disease (str): Chronic respiratory disease (yes/no)
            heart_rate_under_80 (str): Heart rate <80 bpm (yes/no)
            chest_pain_dyspnea (str): Chest pain and acute dyspnea (yes/no)
            male_gender (str): Male gender (yes/no)
            hormonal_treatment (str): Hormonal estrogenic treatment (yes/no)
            personal_history_vte (str): Personal history of VTE (yes/no)
            syncope (str): Syncope (yes/no)
            immobility_4_weeks (str): Immobility within 4 weeks (yes/no)
            oxygen_saturation_under_95 (str): O2 saturation <95% (yes/no)
            calf_pain_edema (str): Calf pain/unilateral edema (yes/no)
            pe_most_likely (str): PE is most likely diagnosis (yes/no)
            
        Returns:
            Dict with the result and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(
            age_category, chronic_respiratory_disease, heart_rate_under_80,
            chest_pain_dyspnea, male_gender, hormonal_treatment, personal_history_vte,
            syncope, immobility_4_weeks, oxygen_saturation_under_95,
            calf_pain_edema, pe_most_likely
        )
        
        # Calculate score
        score = self._calculate_score(
            age_category, chronic_respiratory_disease, heart_rate_under_80,
            chest_pain_dyspnea, male_gender, hormonal_treatment, personal_history_vte,
            syncope, immobility_4_weeks, oxygen_saturation_under_95,
            calf_pain_edema, pe_most_likely
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
    
    def _validate_inputs(self, age_category: str, chronic_respiratory_disease: str,
                        heart_rate_under_80: str, chest_pain_dyspnea: str, male_gender: str,
                        hormonal_treatment: str, personal_history_vte: str, syncope: str,
                        immobility_4_weeks: str, oxygen_saturation_under_95: str,
                        calf_pain_edema: str, pe_most_likely: str):
        """Validates input parameters"""
        
        # Validate age category
        if age_category not in self.AGE_WEIGHTS:
            raise ValueError(f"Age category must be one of: {list(self.AGE_WEIGHTS.keys())}")
        
        # Validate yes/no parameters
        yes_no_params = [
            ("chronic_respiratory_disease", chronic_respiratory_disease),
            ("heart_rate_under_80", heart_rate_under_80),
            ("chest_pain_dyspnea", chest_pain_dyspnea),
            ("male_gender", male_gender),
            ("hormonal_treatment", hormonal_treatment),
            ("personal_history_vte", personal_history_vte),
            ("syncope", syncope),
            ("immobility_4_weeks", immobility_4_weeks),
            ("oxygen_saturation_under_95", oxygen_saturation_under_95),
            ("calf_pain_edema", calf_pain_edema),
            ("pe_most_likely", pe_most_likely)
        ]
        
        for param_name, param_value in yes_no_params:
            if param_value not in ["yes", "no"]:
                raise ValueError(f"{param_name} must be 'yes' or 'no'")
    
    def _calculate_score(self, age_category: str, chronic_respiratory_disease: str,
                        heart_rate_under_80: str, chest_pain_dyspnea: str, male_gender: str,
                        hormonal_treatment: str, personal_history_vte: str, syncope: str,
                        immobility_4_weeks: str, oxygen_saturation_under_95: str,
                        calf_pain_edema: str, pe_most_likely: str) -> int:
        """Calculates the 4PEPS score"""
        
        score = 0
        
        # Add age category score
        score += self.AGE_WEIGHTS[age_category]
        
        # Add scores for yes/no criteria
        criteria = {
            "chronic_respiratory_disease": chronic_respiratory_disease,
            "heart_rate_under_80": heart_rate_under_80,
            "chest_pain_dyspnea": chest_pain_dyspnea,
            "male_gender": male_gender,
            "hormonal_treatment": hormonal_treatment,
            "personal_history_vte": personal_history_vte,
            "syncope": syncope,
            "immobility_4_weeks": immobility_4_weeks,
            "oxygen_saturation_under_95": oxygen_saturation_under_95,
            "calf_pain_edema": calf_pain_edema,
            "pe_most_likely": pe_most_likely
        }
        
        for criterion, value in criteria.items():
            if value == "yes":
                score += self.CRITERION_WEIGHTS[criterion]
        
        return score
    
    def _get_interpretation(self, score: int) -> Dict[str, str]:
        """
        Determines the interpretation based on the 4PEPS score
        
        Args:
            score (int): Calculated 4PEPS score
            
        Returns:
            Dict with interpretation details
        """
        
        if score < 0:
            return {
                "stage": "Very Low",
                "description": "Very low clinical probability",
                "interpretation": "PE ruled out - no testing needed. Risk of PE <1%. No D-dimer or imaging required."
            }
        elif score <= 5:
            return {
                "stage": "Low",
                "description": "Low clinical probability",
                "interpretation": "Low probability of PE. Use D-dimer with 1000 μg/L cut-off. If D-dimer <1000 μg/L, PE is ruled out."
            }
        elif score <= 12:
            return {
                "stage": "Moderate",
                "description": "Moderate clinical probability",
                "interpretation": "Moderate probability of PE. Use age-adjusted D-dimer cut-off (age × 10 μg/L for patients >50 years). If below threshold, PE is ruled out."
            }
        else:  # score >= 13
            return {
                "stage": "High",
                "description": "High clinical probability",
                "interpretation": "High probability of PE. Proceed directly to imaging (CTPA or V/Q scan). D-dimer not recommended."
            }


def calculate_four_peps(age_category: str, chronic_respiratory_disease: str,
                       heart_rate_under_80: str, chest_pain_dyspnea: str, male_gender: str,
                       hormonal_treatment: str, personal_history_vte: str, syncope: str,
                       immobility_4_weeks: str, oxygen_saturation_under_95: str,
                       calf_pain_edema: str, pe_most_likely: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = FourPepsCalculator()
    return calculator.calculate(
        age_category, chronic_respiratory_disease, heart_rate_under_80,
        chest_pain_dyspnea, male_gender, hormonal_treatment, personal_history_vte,
        syncope, immobility_4_weeks, oxygen_saturation_under_95,
        calf_pain_edema, pe_most_likely
    )