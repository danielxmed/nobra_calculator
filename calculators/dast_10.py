"""
Drug Abuse Screening Test-10 (DAST-10) Calculator

Brief 10-item assessment tool to measure, evaluate, and identify drug use problems,
excluding alcohol and tobacco. Assesses drug use in the past 12 months.

References:
1. Skinner HA. The drug abuse screening test. Addict Behav. 1982;7(4):363-71.
2. Yudko E, Lozhkina O, Fouts AA. A comprehensive review of the psychometric 
   properties of the Drug Abuse Screening Test. J Subst Abuse Treat. 2007;32(2):189-98.
"""

from typing import Dict, Any


class Dast10Calculator:
    """Calculator for Drug Abuse Screening Test-10 (DAST-10)"""
    
    def __init__(self):
        # DAST-10 question scoring weights (all questions worth 1 point except item 3 is reverse scored)  
        self.QUESTION_WEIGHTS = {
            1: 1,  # used_drugs_other_than_medical: Yes = 1 point
            2: 1,  # abuse_prescription_drugs: Yes = 1 point  
            3: 1,  # always_able_to_stop: No = 1 point (reverse scored)
            4: 1,  # blackouts_flashbacks: Yes = 1 point
            5: 1,  # feel_bad_guilty: Yes = 1 point
            6: 1,  # spouse_parents_complain: Yes = 1 point
            7: 1,  # neglected_family_work: Yes = 1 point
            8: 1,  # engaged_illegal_activities: Yes = 1 point
            9: 1,  # withdrawal_symptoms: Yes = 1 point
            10: 1  # medical_problems: Yes = 1 point
        }
    
    def calculate(self, used_drugs_other_than_medical: str, abuse_prescription_drugs: str,
                  always_able_to_stop: str, blackouts_flashbacks: str, feel_bad_guilty: str,
                  spouse_parents_complain: str, neglected_family_work: str, 
                  engaged_illegal_activities: str, withdrawal_symptoms: str,
                  medical_problems: str) -> Dict[str, Any]:
        """
        Calculates the DAST-10 score using the provided responses
        
        Args:
            used_drugs_other_than_medical (str): Have you used drugs other than those required for medical reasons?
            abuse_prescription_drugs (str): Do you abuse more than one drug at a time?
            always_able_to_stop (str): Are you always able to stop using drugs when you want to? (reverse scored)
            blackouts_flashbacks (str): Have you had 'blackouts' or 'flashbacks' as a result of drug use?
            feel_bad_guilty (str): Do you ever feel bad or guilty about your drug use?
            spouse_parents_complain (str): Does your spouse (or parents) ever complain about your involvement with drugs?
            neglected_family_work (str): Have you neglected your family because of your use of drugs?
            engaged_illegal_activities (str): Have you engaged in illegal activities in order to obtain drugs?
            withdrawal_symptoms (str): Have you ever experienced withdrawal symptoms when you stopped taking drugs?
            medical_problems (str): Have you had medical problems as a result of your drug use?
            
        Returns:
            Dict with the result and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(
            used_drugs_other_than_medical, abuse_prescription_drugs, always_able_to_stop,
            blackouts_flashbacks, feel_bad_guilty, spouse_parents_complain,
            neglected_family_work, engaged_illegal_activities, withdrawal_symptoms,
            medical_problems
        )
        
        # Calculate score
        result = self._calculate_score(
            used_drugs_other_than_medical, abuse_prescription_drugs, always_able_to_stop,
            blackouts_flashbacks, feel_bad_guilty, spouse_parents_complain,
            neglected_family_work, engaged_illegal_activities, withdrawal_symptoms,
            medical_problems
        )
        
        # Get interpretation
        interpretation = self._get_interpretation(result)
        
        return {
            "result": result,
            "unit": "points", 
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, *responses):
        """Validates input parameters"""
        
        valid_responses = ["yes", "no"]
        
        for i, response in enumerate(responses, 1):
            if not isinstance(response, str):
                raise ValueError(f"Response {i} must be a string")
            
            if response.lower() not in valid_responses:
                raise ValueError(f"Response {i} must be 'yes' or 'no', got '{response}'")
    
    def _calculate_score(self, used_drugs_other_than_medical: str, abuse_prescription_drugs: str,
                        always_able_to_stop: str, blackouts_flashbacks: str, feel_bad_guilty: str,
                        spouse_parents_complain: str, neglected_family_work: str,
                        engaged_illegal_activities: str, withdrawal_symptoms: str,
                        medical_problems: str) -> int:
        """Implements the DAST-10 scoring formula"""
        
        score = 0
        
        # Questions 1, 2, 4-10: 1 point for "yes" answers
        responses = [
            used_drugs_other_than_medical,  # Q1
            abuse_prescription_drugs,        # Q2  
            None,                           # Q3 handled separately (reverse scored)
            blackouts_flashbacks,           # Q4
            feel_bad_guilty,               # Q5
            spouse_parents_complain,        # Q6
            neglected_family_work,          # Q7
            engaged_illegal_activities,     # Q8
            withdrawal_symptoms,            # Q9
            medical_problems               # Q10
        ]
        
        # Score questions 1, 2, 4-10 (1 point for "yes")
        for i, response in enumerate(responses):
            if i == 2:  # Skip Q3, handled separately
                continue
            if response and response.lower() == "yes":
                score += 1
        
        # Question 3 is reverse scored: 1 point for "no" answer
        if always_able_to_stop.lower() == "no":
            score += 1
            
        return score
    
    def _get_interpretation(self, result: int) -> Dict[str, str]:
        """
        Determines the interpretation based on the DAST-10 score
        
        Args:
            result (int): Calculated DAST-10 score
            
        Returns:
            Dict with interpretation details
        """
        
        if result == 0:
            return {
                "stage": "No Problems",
                "description": "No drug problems reported",
                "interpretation": "No evidence of drug-related problems. Continue routine screening at appropriate intervals."
            }
        elif 1 <= result <= 2:
            return {
                "stage": "Low Level", 
                "description": "Low level problems",
                "interpretation": "Low level drug problems that may require monitoring and re-assessment of drug use at a later date."
            }
        elif 3 <= result <= 5:
            return {
                "stage": "Moderate Level",
                "description": "Moderate level problems", 
                "interpretation": "Moderate level drug problems that necessitate further investigation with additional tests or resources. Consider brief intervention."
            }
        elif 6 <= result <= 8:
            return {
                "stage": "Substantial Level",
                "description": "Substantial problems",
                "interpretation": "Substantial drug problems that require intensive assessment and treatment. Referral to specialized addiction services recommended."
            }
        else:  # 9-10
            return {
                "stage": "Severe Level",
                "description": "Severe problems", 
                "interpretation": "Severe drug problems that require intensive assessment and medical treatment. Immediate referral to specialized addiction treatment program is warranted."
            }


def calculate_dast_10(used_drugs_other_than_medical: str, abuse_prescription_drugs: str,
                     always_able_to_stop: str, blackouts_flashbacks: str, feel_bad_guilty: str,
                     spouse_parents_complain: str, neglected_family_work: str,
                     engaged_illegal_activities: str, withdrawal_symptoms: str,
                     medical_problems: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_dast_10 pattern
    """
    calculator = Dast10Calculator()
    return calculator.calculate(
        used_drugs_other_than_medical, abuse_prescription_drugs, always_able_to_stop,
        blackouts_flashbacks, feel_bad_guilty, spouse_parents_complain,
        neglected_family_work, engaged_illegal_activities, withdrawal_symptoms,
        medical_problems
    )