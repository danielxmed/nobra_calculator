"""
Major Depression Inventory (MDI)

WHO-developed depression screening tool that provides both diagnosis and severity assessment
using ICD-10 and DSM-IV criteria for major depression.

References:
- Bech P, et al. The sensitivity and specificity of the Major Depression Inventory, using the Present State Examination as the index of diagnostic validity. J Affect Disord. 2001;66(2-3):159-64.
- Olsen LR, et al. The internal and external validity of the Major Depression Inventory in measuring severity of depressive states. Psychol Med. 2003;33(2):351-6.
"""

import math
from typing import Dict, Any


class MajorDepressionIndexCalculator:
    """Calculator for Major Depression Inventory (MDI)"""
    
    def __init__(self):
        # Scoring values for each response option
        self.SCORING = {
            "not_at_all": 0,
            "some_of_time": 1, 
            "most_of_time": 2,
            "all_the_time": 3
        }
        
        # Core symptoms for diagnostic criteria (items 1-2)
        self.CORE_SYMPTOMS = ["depressed_mood", "lack_of_interest"]
        
        # Additional symptoms for diagnostic criteria (items 3-10)
        self.ADDITIONAL_SYMPTOMS = [
            "lack_of_energy", "low_self_confidence", "bad_conscience",
            "life_not_worth_living", "concentration_problems",
            "agitation_restlessness", "psychomotor_retardation", "sleep_problems"
        ]
    
    def calculate(self, depressed_mood: str, lack_of_interest: str, lack_of_energy: str,
                 low_self_confidence: str, bad_conscience: str, life_not_worth_living: str,
                 concentration_problems: str, agitation_restlessness: str,
                 psychomotor_retardation: str, sleep_problems: str) -> Dict[str, Any]:
        """
        Calculates the MDI score and determines depression severity
        
        Args:
            depressed_mood (str): Feeling sad or depressed
            lack_of_interest (str): Lost interest in daily activities
            lack_of_energy (str): Lacking in energy and strength
            low_self_confidence (str): Feeling less self-confident
            bad_conscience (str): Bad conscience or feelings of guilt
            life_not_worth_living (str): Feeling that life wasn't worth living
            concentration_problems (str): Difficulty concentrating
            agitation_restlessness (str): Feeling very restless
            psychomotor_retardation (str): Movements have been slower
            sleep_problems (str): Trouble sleeping at night
            
        Returns:
            Dict with the result and interpretation
        """
        
        # Create parameters list for validation
        parameters = [
            depressed_mood, lack_of_interest, lack_of_energy, low_self_confidence,
            bad_conscience, life_not_worth_living, concentration_problems,
            agitation_restlessness, psychomotor_retardation, sleep_problems
        ]
        
        # Validations
        self._validate_inputs(parameters)
        
        # Calculate total score
        total_score = self._calculate_total_score(parameters)
        
        # Assess diagnostic criteria
        diagnostic_assessment = self._assess_diagnostic_criteria(
            depressed_mood, lack_of_interest, lack_of_energy, low_self_confidence,
            bad_conscience, life_not_worth_living, concentration_problems,
            agitation_restlessness, psychomotor_retardation, sleep_problems
        )
        
        # Get interpretation
        interpretation = self._get_interpretation(total_score, diagnostic_assessment)
        
        # Check for suicide risk
        suicide_risk = self._assess_suicide_risk(life_not_worth_living)
        
        return {
            "result": {
                "total_score": total_score,
                "diagnostic_criteria_met": diagnostic_assessment["criteria_met"],
                "core_symptoms": diagnostic_assessment["core_symptoms"],
                "additional_symptoms": diagnostic_assessment["additional_symptoms"],
                "suicide_risk_flag": suicide_risk
            },
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, parameters):
        """Validates input parameters"""
        
        valid_options = ["not_at_all", "some_of_time", "most_of_time", "all_the_time"]
        
        for i, param in enumerate(parameters):
            if param not in valid_options:
                param_names = [
                    "depressed_mood", "lack_of_interest", "lack_of_energy",
                    "low_self_confidence", "bad_conscience", "life_not_worth_living",
                    "concentration_problems", "agitation_restlessness",
                    "psychomotor_retardation", "sleep_problems"
                ]
                raise ValueError(f"{param_names[i]} must be one of: {', '.join(valid_options)}")
    
    def _calculate_total_score(self, parameters) -> int:
        """Calculates the total MDI score"""
        
        total_score = 0
        for param in parameters:
            total_score += self.SCORING[param]
        
        return total_score
    
    def _assess_diagnostic_criteria(self, depressed_mood, lack_of_interest, lack_of_energy,
                                  low_self_confidence, bad_conscience, life_not_worth_living,
                                  concentration_problems, agitation_restlessness,
                                  psychomotor_retardation, sleep_problems) -> Dict[str, Any]:
        """Assesses whether diagnostic criteria for major depression are met"""
        
        # Core symptoms assessment (at least one must be present most/all of the time)
        core_symptoms_count = 0
        if depressed_mood in ["most_of_time", "all_the_time"]:
            core_symptoms_count += 1
        if lack_of_interest in ["most_of_time", "all_the_time"]:
            core_symptoms_count += 1
        
        core_criteria_met = core_symptoms_count >= 1
        
        # Additional symptoms assessment (present some/most/all of the time)
        additional_symptoms = [
            lack_of_energy, low_self_confidence, bad_conscience, life_not_worth_living,
            concentration_problems, agitation_restlessness, psychomotor_retardation, sleep_problems
        ]
        
        additional_symptoms_count = 0
        for symptom in additional_symptoms:
            if symptom in ["some_of_time", "most_of_time", "all_the_time"]:
                additional_symptoms_count += 1
        
        # Total symptoms for diagnostic criteria (need at least 5 total)
        total_symptoms = core_symptoms_count + additional_symptoms_count
        
        # Diagnostic criteria: at least 1 core symptom + total of 5 symptoms
        criteria_met = core_criteria_met and total_symptoms >= 5
        
        return {
            "criteria_met": criteria_met,
            "core_symptoms": core_symptoms_count,
            "additional_symptoms": additional_symptoms_count,
            "total_symptoms": total_symptoms
        }
    
    def _assess_suicide_risk(self, life_not_worth_living: str) -> bool:
        """Assesses suicide risk based on life not worth living item"""
        
        return life_not_worth_living in ["most_of_time", "all_the_time"]
    
    def _get_interpretation(self, score: int, diagnostic_assessment: Dict[str, Any]) -> Dict[str, str]:
        """
        Determines the interpretation based on the MDI score and diagnostic criteria
        
        Args:
            score (int): Total MDI score
            diagnostic_assessment (dict): Diagnostic criteria assessment
            
        Returns:
            Dict with interpretation
        """
        
        # Base interpretation on score ranges
        if score <= 13:
            stage = "No Depression"
            description = "Minimal or no depressive symptoms"
            base_interpretation = (
                "No evidence of clinically significant depression. Continue routine monitoring "
                "and preventive care. Consider lifestyle factors and general mental health promotion."
            )
        elif score <= 20:
            stage = "Mild Depression"
            description = "Mild depressive symptoms"
            base_interpretation = (
                "Mild depression present. Consider watchful waiting, psychosocial interventions, "
                "counseling, or brief therapy. Monitor closely for symptom progression. "
                "Lifestyle modifications and social support may be beneficial."
            )
        elif score <= 25:
            stage = "Moderate Depression"
            description = "Moderate depressive symptoms"
            base_interpretation = (
                "Moderate depression requiring treatment. Consider psychotherapy and/or "
                "antidepressant medication. Regular follow-up essential. Assess for "
                "functional impairment and safety concerns."
            )
        else:  # score >= 26
            stage = "Severe Depression"
            description = "Severe depressive symptoms"
            base_interpretation = (
                "Severe depression requiring immediate treatment. Strong indication for "
                "combined therapy (psychotherapy + medication). Assess suicide risk. "
                "Consider psychiatric referral and intensive monitoring."
            )
        
        # Add diagnostic criteria information
        if diagnostic_assessment["criteria_met"]:
            diagnostic_note = (
                f" Diagnostic criteria for major depression are met "
                f"({diagnostic_assessment['core_symptoms']} core symptoms, "
                f"{diagnostic_assessment['additional_symptoms']} additional symptoms)."
            )
        else:
            diagnostic_note = (
                f" Diagnostic criteria for major depression are not fully met "
                f"({diagnostic_assessment['core_symptoms']} core symptoms, "
                f"{diagnostic_assessment['additional_symptoms']} additional symptoms). "
                f"Clinical interview recommended for comprehensive assessment."
            )
        
        # Add suicide risk warning if applicable
        suicide_warning = ""
        if diagnostic_assessment.get("suicide_risk_flag", False):
            suicide_warning = (
                " WARNING: Patient endorsed feeling that life is not worth living. "
                "Immediate suicide risk assessment and safety planning required."
            )
        
        final_interpretation = base_interpretation + diagnostic_note + suicide_warning
        
        return {
            "stage": stage,
            "description": description,
            "interpretation": final_interpretation
        }


def calculate_major_depression_index(depressed_mood, lack_of_interest, lack_of_energy,
                                   low_self_confidence, bad_conscience, life_not_worth_living,
                                   concentration_problems, agitation_restlessness,
                                   psychomotor_retardation, sleep_problems) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = MajorDepressionIndexCalculator()
    return calculator.calculate(depressed_mood, lack_of_interest, lack_of_energy,
                              low_self_confidence, bad_conscience, life_not_worth_living,
                              concentration_problems, agitation_restlessness,
                              psychomotor_retardation, sleep_problems)