"""
GCS-Pupils Score Calculator

The GCS-Pupils Score (GCS-P) combines the Glasgow Coma Scale with pupillary reactivity 
assessment to provide enhanced prognostic accuracy in traumatic brain injury patients.

This extended index offers improved prediction of 6-month mortality and unfavorable outcomes, 
particularly in patients with severe brain injury where standard GCS may be limited.

References (Vancouver style):
1. Brennan PM, Murray GD, Teasdale GM. Simplifying the use of prognostic information in traumatic 
   brain injury. Part 1: The GCS-Pupils score: an extended index of clinical severity. 
   J Neurosurg. 2018;128(6):1612-1620. doi: 10.3171/2017.12.JNS172780.
2. Teasdale G, Maas A, Lecky F, et al. The Glasgow Coma Scale at 40 years: standing the test of time. 
   Lancet Neurol. 2014;13(8):844-54. doi: 10.1016/S1474-4422(14)70120-6.
3. Steyerberg EW, Mushkudiani N, Perel P, et al. Predicting outcome after traumatic brain injury: 
   development and international validation of prognostic scores based on admission characteristics. 
   PLoS Med. 2008;5(8):e165. doi: 10.1371/journal.pmed.0050165.
"""

from typing import Dict, Any


class GcsPupilsScoreCalculator:
    """Calculator for GCS-Pupils Score"""
    
    def __init__(self):
        # Mortality rates by GCS-P score (6-month post-injury)
        self.MORTALITY_RATES = {
            1: 74.45,
            2: 64.62,
            3: 40.92,
            4: 39.47,
            5: 32.57,
            6: 24.97,
            7: 19.17,
            8: 20.04,
            9: 18.75,
            10: 17.35,
            11: 11.60,
            12: 9.43,
            13: 7.07,
            14: 5.64,
            15: 2.54,
            16: 2.54,  # Extended for GCS 15 + pupils
            17: 2.54
        }
        
        # Unfavorable outcome rates by GCS-P score (6-month post-injury)
        self.UNFAVORABLE_OUTCOME_RATES = {
            1: 89.59,
            2: 85.22,
            3: 65.53,
            4: 68.90,
            5: 57.75,
            6: 46.26,
            7: 37.20,
            8: 33.55,
            9: 30.32,
            10: 28.88,
            11: 21.81,
            12: 19.92,
            13: 15.85,
            14: 14.39,
            15: 11.75,
            16: 11.75,  # Extended for GCS 15 + pupils
            17: 11.75
        }
        
        # Pupil reactivity scoring
        self.PUPIL_SCORES = {
            'both_reactive': 0,
            'one_unreactive': 1,
            'both_unreactive': 2
        }
    
    def calculate(self, eye_response: int, verbal_response: int, motor_response: int, 
                 pupil_reactivity: str) -> Dict[str, Any]:
        """
        Calculates GCS-Pupils score using provided parameters
        
        Args:
            eye_response (int): Eye opening response (1-4)
            verbal_response (int): Verbal response (1-5)
            motor_response (int): Motor response (1-6)
            pupil_reactivity (str): Pupillary light reflex assessment
            
        Returns:
            Dict with the result and clinical interpretation
        """
        
        # Validate inputs
        self._validate_inputs(eye_response, verbal_response, motor_response, pupil_reactivity)
        
        # Calculate GCS total score
        gcs_total = eye_response + verbal_response + motor_response
        
        # Get pupil reactivity score
        pupil_score = self.PUPIL_SCORES[pupil_reactivity]
        
        # Calculate GCS-Pupils score
        gcs_pupils_score = gcs_total + pupil_score
        
        # Get mortality and outcome predictions
        mortality_rate = self.MORTALITY_RATES.get(gcs_pupils_score, 2.54)  # Default to lowest rate
        unfavorable_outcome_rate = self.UNFAVORABLE_OUTCOME_RATES.get(gcs_pupils_score, 11.75)
        
        # Get clinical interpretation
        interpretation = self._get_interpretation(gcs_pupils_score, gcs_total, pupil_reactivity, 
                                                mortality_rate, unfavorable_outcome_rate)
        
        return {
            "result": gcs_pupils_score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"],
            "gcs_total": gcs_total,
            "pupil_score": pupil_score,
            "mortality_6_month": round(mortality_rate, 1),
            "unfavorable_outcome_6_month": round(unfavorable_outcome_rate, 1)
        }
    
    def _validate_inputs(self, eye_response, verbal_response, motor_response, pupil_reactivity):
        """Validates input parameters"""
        
        if not isinstance(eye_response, int) or eye_response < 1 or eye_response > 4:
            raise ValueError("Eye response must be an integer between 1 and 4")
        
        if not isinstance(verbal_response, int) or verbal_response < 1 or verbal_response > 5:
            raise ValueError("Verbal response must be an integer between 1 and 5")
        
        if not isinstance(motor_response, int) or motor_response < 1 or motor_response > 6:
            raise ValueError("Motor response must be an integer between 1 and 6")
        
        if pupil_reactivity not in self.PUPIL_SCORES:
            raise ValueError("Pupil reactivity must be 'both_reactive', 'one_unreactive', or 'both_unreactive'")
    
    def _get_interpretation(self, gcs_pupils_score: int, gcs_total: int, pupil_reactivity: str,
                           mortality_rate: float, unfavorable_outcome_rate: float) -> Dict[str, str]:
        """
        Determines clinical interpretation based on GCS-Pupils score
        
        Args:
            gcs_pupils_score (int): Calculated GCS-P score
            gcs_total (int): Standard GCS total score
            pupil_reactivity (str): Pupil reactivity status
            mortality_rate (float): 6-month mortality rate
            unfavorable_outcome_rate (float): 6-month unfavorable outcome rate
            
        Returns:
            Dict with interpretation
        """
        
        # Convert pupil status to readable format
        pupil_status_map = {
            'both_reactive': 'both pupils reactive to light',
            'one_unreactive': 'one pupil unreactive to light',
            'both_unreactive': 'both pupils unreactive to light'
        }
        pupil_status = pupil_status_map[pupil_reactivity]
        
        # Base interpretation with components and predictions
        base_interpretation = (
            f"GCS-Pupils score of {gcs_pupils_score} (GCS {gcs_total} + pupil score {self.PUPIL_SCORES[pupil_reactivity]}) "
            f"with {pupil_status}. Predicted 6-month mortality: {mortality_rate:.1f}%. "
            f"Predicted unfavorable outcome: {unfavorable_outcome_rate:.1f}%. "
        )
        
        # Determine severity category and specific recommendations
        if gcs_pupils_score <= 3:
            return {
                "stage": "Extremely Severe",
                "description": "Very poor prognosis",
                "interpretation": base_interpretation + 
                    "Extremely severe brain injury with very high mortality risk. Requires intensive neurological monitoring, "
                    "aggressive supportive care, and immediate neurosurgical consultation if indicated. Consider goals of care "
                    "discussions with family regarding prognosis and treatment intensity. Implement measures to prevent "
                    "secondary brain injury including ICP monitoring, optimal CPP maintenance, and temperature management."
            }
        elif gcs_pupils_score <= 6:
            return {
                "stage": "Severe", 
                "description": "Poor prognosis",
                "interpretation": base_interpretation +
                    "Severe brain injury with high mortality risk. Requires intensive neurological monitoring with frequent "
                    "neurological assessments, ICP monitoring if indicated, and comprehensive supportive care. Early involvement "
                    "of neurosurgical team for management decisions. Initiate rehabilitation planning and family education "
                    "regarding expected recovery trajectory and potential outcomes."
            }
        elif gcs_pupils_score <= 9:
            return {
                "stage": "Moderate",
                "description": "Guarded prognosis", 
                "interpretation": base_interpretation +
                    "Moderate brain injury with intermediate mortality risk. Close neurological monitoring with serial assessments "
                    "to detect deterioration. Early rehabilitation intervention recommended to optimize functional outcomes. "
                    "Monitor for complications including post-traumatic seizures, cognitive impairment, and behavioral changes. "
                    "Provide family education and support throughout recovery process."
            }
        elif gcs_pupils_score <= 12:
            return {
                "stage": "Mild-Moderate",
                "description": "Fair prognosis",
                "interpretation": base_interpretation +
                    "Mild to moderate brain injury with lower mortality risk. Regular neurological monitoring to detect any "
                    "complications or deterioration. Initiate appropriate rehabilitation services including physical, occupational, "
                    "and speech therapy as indicated. Screen for post-concussive symptoms, cognitive impairment, and mood changes. "
                    "Educate patient and family about recovery expectations and available support resources."
            }
        else:  # 13-17
            return {
                "stage": "Mild",
                "description": "Good prognosis",
                "interpretation": base_interpretation +
                    "Mild brain injury with low mortality risk and generally favorable prognosis. Monitor for post-concussive "
                    "symptoms including headache, dizziness, cognitive difficulties, and mood changes. Provide patient education "
                    "about expected recovery timeline and when to seek medical attention. Ensure appropriate follow-up with "
                    "primary care or neurology for symptom monitoring and gradual return to activities."
            }


def calculate_gcs_pupils_score(eye_response: int, verbal_response: int, motor_response: int,
                              pupil_reactivity: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_gcs_pupils_score pattern
    """
    calculator = GcsPupilsScoreCalculator()
    return calculator.calculate(eye_response, verbal_response, motor_response, pupil_reactivity)