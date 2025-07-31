"""
Geriatric Depression Scale (GDS-15) Calculator

The Geriatric Depression Scale (GDS-15) is a validated screening tool for identifying 
possible depression in older adults aged 55 and older. The 15-item version, developed 
in 1986, provides a brief and reliable assessment using simple yes/no questions to 
evaluate depressive symptoms specific to the geriatric population over the past week.

References (Vancouver style):
1. Yesavage JA, Brink TL, Rose TL, et al. Development and validation of a geriatric depression 
   screening scale: a preliminary report. J Psychiatr Res. 1982-1983;17(1):37-49. 
   doi: 10.1016/0022-3956(82)90033-4.
2. Sheikh JI, Yesavage JA. Geriatric Depression Scale (GDS): recent evidence and development 
   of a shorter version. Clin Gerontol. 1986;5(1-2):165-173. doi: 10.1300/J018v05n01_09.
3. D'Ath P, Katona P, Mullan E, Evans S, Katona C. Screening, detection and management of 
   depression in elderly primary care attenders. I: The acceptability and performance of the 
   15 item Geriatric Depression Scale (GDS15) and the development of short versions. 
   Fam Pract. 1994;11(3):260-266. doi: 10.1093/fampra/11.3.260.
"""

from typing import Dict, Any


class Gds15Calculator:
    """Calculator for Geriatric Depression Scale (GDS-15)"""
    
    def __init__(self):
        # Questions that indicate depression when answered "YES"
        self.DEPRESSION_YES_QUESTIONS = {
            'q2_dropped_activities',
            'q3_life_empty',
            'q4_often_bored',
            'q6_afraid_bad_happen',
            'q8_feel_helpless',
            'q9_prefer_stay_home',
            'q10_memory_problems',
            'q12_feel_worthless',
            'q14_situation_hopeless',
            'q15_others_better_off'
        }
        
        # Questions that indicate depression when answered "NO"
        self.DEPRESSION_NO_QUESTIONS = {
            'q1_satisfied_with_life',
            'q5_good_spirits',
            'q7_happy_most_time',
            'q11_wonderful_to_be_alive',
            'q13_full_of_energy'
        }
        
        # All question parameters
        self.ALL_QUESTIONS = self.DEPRESSION_YES_QUESTIONS | self.DEPRESSION_NO_QUESTIONS
    
    def calculate(self, q1_satisfied_with_life: str, q2_dropped_activities: str, 
                 q3_life_empty: str, q4_often_bored: str, q5_good_spirits: str,
                 q6_afraid_bad_happen: str, q7_happy_most_time: str, q8_feel_helpless: str,
                 q9_prefer_stay_home: str, q10_memory_problems: str, 
                 q11_wonderful_to_be_alive: str, q12_feel_worthless: str,
                 q13_full_of_energy: str, q14_situation_hopeless: str,
                 q15_others_better_off: str) -> Dict[str, Any]:
        """
        Calculates GDS-15 score using provided responses to 15 questions
        
        Args:
            q1_satisfied_with_life (str): Are you basically satisfied with your life?
            q2_dropped_activities (str): Have you dropped many of your activities and interests?
            q3_life_empty (str): Do you feel that your life is empty?
            q4_often_bored (str): Do you often get bored?
            q5_good_spirits (str): Are you in good spirits most of the time?
            q6_afraid_bad_happen (str): Are you afraid that something bad is going to happen to you?
            q7_happy_most_time (str): Do you feel happy most of the time?
            q8_feel_helpless (str): Do you often feel helpless?
            q9_prefer_stay_home (str): Do you prefer to stay at home, rather than going out and doing new things?
            q10_memory_problems (str): Do you feel you have more problems with memory than most?
            q11_wonderful_to_be_alive (str): Do you think it is wonderful to be alive now?
            q12_feel_worthless (str): Do you feel pretty worthless the way you are now?
            q13_full_of_energy (str): Do you feel full of energy?
            q14_situation_hopeless (str): Do you feel that your situation is hopeless?
            q15_others_better_off (str): Do you think that most people are better off than you are?
            
        Returns:
            Dict with the result and clinical interpretation
        """
        
        # Collect all parameters for validation and calculation
        parameters = {
            'q1_satisfied_with_life': q1_satisfied_with_life,
            'q2_dropped_activities': q2_dropped_activities,
            'q3_life_empty': q3_life_empty,
            'q4_often_bored': q4_often_bored,
            'q5_good_spirits': q5_good_spirits,
            'q6_afraid_bad_happen': q6_afraid_bad_happen,
            'q7_happy_most_time': q7_happy_most_time,
            'q8_feel_helpless': q8_feel_helpless,
            'q9_prefer_stay_home': q9_prefer_stay_home,
            'q10_memory_problems': q10_memory_problems,
            'q11_wonderful_to_be_alive': q11_wonderful_to_be_alive,
            'q12_feel_worthless': q12_feel_worthless,
            'q13_full_of_energy': q13_full_of_energy,
            'q14_situation_hopeless': q14_situation_hopeless,
            'q15_others_better_off': q15_others_better_off
        }
        
        # Validate inputs
        self._validate_inputs(parameters)
        
        # Calculate GDS-15 score
        gds_score = self._calculate_gds_score(parameters)
        
        # Get clinical interpretation
        interpretation = self._get_interpretation(gds_score, parameters)
        
        return {
            "result": gds_score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, parameters: Dict[str, str]):
        """Validates input parameters"""
        
        for param_name, param_value in parameters.items():
            if param_value not in ["yes", "no"]:
                raise ValueError(f"{param_name} must be 'yes' or 'no'")
    
    def _calculate_gds_score(self, parameters: Dict[str, str]) -> int:
        """Calculates the GDS-15 total score"""
        
        total_score = 0
        
        # Score questions that indicate depression when answered "YES"
        for question in self.DEPRESSION_YES_QUESTIONS:
            if parameters[question] == "yes":
                total_score += 1
        
        # Score questions that indicate depression when answered "NO"
        for question in self.DEPRESSION_NO_QUESTIONS:
            if parameters[question] == "no":
                total_score += 1
        
        return total_score
    
    def _get_interpretation(self, score: int, parameters: Dict[str, str]) -> Dict[str, str]:
        """
        Determines clinical interpretation based on GDS-15 score
        
        Args:
            score (int): Calculated GDS-15 score
            parameters (Dict): Question responses for context
            
        Returns:
            Dict with interpretation
        """
        
        # Build summary of concerning responses
        concerning_responses = []
        
        # Check depression-indicating "YES" responses
        concerning_yes_descriptions = {
            'q2_dropped_activities': 'dropped activities/interests',
            'q3_life_empty': 'life feels empty',
            'q4_often_bored': 'often bored',
            'q6_afraid_bad_happen': 'afraid something bad will happen',
            'q8_feel_helpless': 'often feels helpless',
            'q9_prefer_stay_home': 'prefers staying home',
            'q10_memory_problems': 'memory problems',
            'q12_feel_worthless': 'feels worthless',
            'q14_situation_hopeless': 'situation feels hopeless',
            'q15_others_better_off': 'others are better off'
        }
        
        for question, response in parameters.items():
            if question in self.DEPRESSION_YES_QUESTIONS and response == "yes":
                concerning_responses.append(concerning_yes_descriptions[question])
        
        # Check depression-indicating "NO" responses
        concerning_no_descriptions = {
            'q1_satisfied_with_life': 'not satisfied with life',
            'q5_good_spirits': 'not in good spirits',
            'q7_happy_most_time': 'not happy most of the time',
            'q11_wonderful_to_be_alive': 'does not think it is wonderful to be alive',
            'q13_full_of_energy': 'not full of energy'
        }
        
        for question, response in parameters.items():
            if question in self.DEPRESSION_NO_QUESTIONS and response == "no":
                concerning_responses.append(concerning_no_descriptions[question])
        
        # Build concerning responses summary
        if concerning_responses:
            if len(concerning_responses) <= 3:
                concern_summary = f"Concerning responses: {', '.join(concerning_responses)}. "
            else:
                concern_summary = f"Multiple concerning responses identified ({len(concerning_responses)} items). "
        else:
            concern_summary = "No concerning responses identified. "
        
        # Determine severity level and recommendations
        if score <= 4:
            return {
                "stage": "Normal",
                "description": "Absence of clinically significant depressive symptoms",
                "interpretation": (
                    f"GDS-15 Score: {score}/15 points. {concern_summary}"
                    f"Normal range - absence of clinically significant depressive symptoms. "
                    f"These are normal scores, depending on age, education, and complaints. "
                    f"Continue routine screening at regular intervals. Monitor for changes "
                    f"in mood, function, or social engagement. Promote healthy aging activities "
                    f"and social connections."
                )
            }
        elif score <= 7:
            return {
                "stage": "Mild Depression",
                "description": "Suggests mild depression",
                "interpretation": (
                    f"GDS-15 Score: {score}/15 points. {concern_summary}"
                    f"Mild depression indicated. Consider formal diagnostic evaluation by "
                    f"qualified mental health professional. Monitor symptoms closely and "
                    f"consider counseling, supportive interventions, or community resources. "
                    f"Assess functional impact and provide patient education about depression "
                    f"in older adults. Follow up in 2-4 weeks."
                )
            }
        elif score <= 9:
            return {
                "stage": "Moderate Depression",
                "description": "Suggests moderate depression",
                "interpretation": (
                    f"GDS-15 Score: {score}/15 points. {concern_summary}"
                    f"Moderate depression indicated. Formal psychiatric evaluation "
                    f"recommended. Consider pharmacological and/or psychotherapeutic "
                    f"interventions. Assess suicide risk and functional impairment. "
                    f"Coordinate care with mental health specialists. Monitor treatment "
                    f"response and adjust interventions as needed. Provide family education "
                    f"and support resources."
                )
            }
        else:  # Score 10-15
            return {
                "stage": "Severe Depression",
                "description": "Suggests severe depression",
                "interpretation": (
                    f"GDS-15 Score: {score}/15 points. {concern_summary}"
                    f"Severe depression indicated. Urgent psychiatric evaluation required. "
                    f"Assess suicide risk IMMEDIATELY using standardized tools and safety "
                    f"planning. Consider intensive treatment including medication and "
                    f"psychotherapy. May require close monitoring, intensive outpatient "
                    f"programs, or hospitalization if safety concerns. Coordinate care with "
                    f"psychiatry, involve family/caregivers, and ensure appropriate follow-up."
                )
            }


def calculate_gds_15(q1_satisfied_with_life: str, q2_dropped_activities: str, 
                    q3_life_empty: str, q4_often_bored: str, q5_good_spirits: str,
                    q6_afraid_bad_happen: str, q7_happy_most_time: str, q8_feel_helpless: str,
                    q9_prefer_stay_home: str, q10_memory_problems: str, 
                    q11_wonderful_to_be_alive: str, q12_feel_worthless: str,
                    q13_full_of_energy: str, q14_situation_hopeless: str,
                    q15_others_better_off: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_gds_15 pattern
    """
    calculator = Gds15Calculator()
    return calculator.calculate(
        q1_satisfied_with_life, q2_dropped_activities, q3_life_empty, q4_often_bored,
        q5_good_spirits, q6_afraid_bad_happen, q7_happy_most_time, q8_feel_helpless,
        q9_prefer_stay_home, q10_memory_problems, q11_wonderful_to_be_alive,
        q12_feel_worthless, q13_full_of_energy, q14_situation_hopeless, q15_others_better_off
    )