"""
Berg Balance Scale (BBS) Calculator

Assesses balance and fall risk in community-dwelling older adults through 
14 functional tasks.

References (Vancouver style):
1. Berg KO, Wood-Dauphinee SL, Williams JI, Maki B. Measuring balance in the elderly: 
   validation of an instrument. Can J Public Health. 1992 Jul-Aug;83 Suppl 2:S7-11.
2. Berg K, Wood-Dauphinee S, Williams JI, Gayton D. Measuring balance in the elderly: 
   preliminary development of an instrument. Physiother Can. 1989;41:304-311.
3. Bogle Thorbahn LD, Newton RA. Use of the Berg Balance Scale to predict falls in 
   elderly persons. Phys Ther. 1996 Jun;76(6):576-83; discussion 584-5.
"""

from typing import Dict, Any


class BergBalanceScaleCalculator:
    """Calculator for Berg Balance Scale (BBS)"""
    
    def __init__(self):
        # Task descriptions for scoring reference
        self.task_descriptions = {
            "sitting_to_standing": "Sitting to standing",
            "standing_unsupported": "Standing unsupported",  
            "sitting_unsupported": "Sitting with back unsupported",
            "standing_to_sitting": "Standing to sitting",
            "transfers": "Transfers",
            "standing_eyes_closed": "Standing with eyes closed",
            "standing_feet_together": "Standing with feet together",
            "reaching_forward": "Reaching forward while standing",
            "picking_up_object": "Picking up object from floor",
            "turning_to_look_behind": "Turning to look behind",
            "turning_360_degrees": "Turning 360 degrees",
            "placing_alternate_foot_on_step": "Placing alternate foot on step",
            "standing_one_foot_in_front": "Standing one foot in front",
            "standing_on_one_leg": "Standing on one leg"
        }
        
        # Fall risk thresholds
        self.INDEPENDENT_THRESHOLD = 45
        self.HIGH_RISK_THRESHOLD = 40
        self.SEVERE_IMPAIRMENT_THRESHOLD = 20
    
    def calculate(self, **kwargs) -> Dict[str, Any]:
        """
        Calculates the Berg Balance Scale score
        
        Args:
            **kwargs: Individual task scores (0-4 each)
            
        Returns:
            Dict with BBS score and clinical interpretation
        """
        
        # Extract and validate all task scores
        task_scores = self._extract_and_validate_scores(kwargs)
        
        # Calculate total score
        total_score = sum(task_scores.values())
        
        # Get interpretation
        interpretation = self._get_interpretation(total_score, task_scores)
        
        return {
            "result": total_score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _extract_and_validate_scores(self, kwargs: Dict[str, Any]) -> Dict[str, int]:
        """Extracts and validates individual task scores"""
        
        task_scores = {}
        
        for task_name in self.task_descriptions.keys():
            if task_name not in kwargs:
                raise ValueError(f"Missing required task: {task_name}")
            
            score = kwargs[task_name]
            
            if not isinstance(score, int):
                raise ValueError(f"{task_name} must be an integer")
            
            if score < 0 or score > 4:
                raise ValueError(f"{task_name} must be between 0 and 4")
            
            task_scores[task_name] = score
        
        return task_scores
    
    def _get_interpretation(self, total_score: int, task_scores: Dict[str, int]) -> Dict[str, str]:
        """
        Determines clinical interpretation based on BBS score
        
        Args:
            total_score (int): Total BBS score
            task_scores (Dict[str, int]): Individual task scores
            
        Returns:
            Dict with clinical interpretation
        """
        
        # Generate summary of performance
        perfect_tasks = sum(1 for score in task_scores.values() if score == 4)
        impaired_tasks = sum(1 for score in task_scores.values() if score <= 2)
        
        # Identify specific areas of concern
        concerning_tasks = [
            self.task_descriptions[task] for task, score in task_scores.items() 
            if score <= 2
        ]
        
        base_interpretation = (
            f"Berg Balance Scale score: {total_score}/56 points. "
            f"Performance summary: {perfect_tasks}/14 tasks completed with maximum score, "
            f"{impaired_tasks}/14 tasks showing significant impairment (≤2 points). "
        )
        
        if concerning_tasks:
            base_interpretation += f"Areas of concern: {', '.join(concerning_tasks)}. "
        
        if total_score >= self.INDEPENDENT_THRESHOLD:
            return {
                "stage": "Independent",
                "description": "Good balance with low fall risk",
                "interpretation": (
                    base_interpretation +
                    "FUNCTIONAL BALANCE: Score indicates good functional balance with low fall risk. "
                    "Patient is generally safe for independent mobility and activities of daily living. "
                    "Clinical recommendations: Continue current activity level and balance maintenance "
                    "exercises. Periodic reassessment (annually or with health changes) is recommended. "
                    "Focus on maintaining strength, flexibility, and balance through regular exercise. "
                    "Consider environmental safety assessment to optimize home safety. "
                    "Educate on fall prevention strategies and importance of regular vision and "
                    "medication reviews."
                )
            }
        
        elif total_score >= 41:
            return {
                "stage": "Increased Fall Risk",
                "description": "Moderate balance impairment with increased fall risk",
                "interpretation": (
                    base_interpretation +
                    "MODERATE IMPAIRMENT: Score indicates moderate balance impairment with increased "
                    "fall risk. Patient may benefit from balance training and fall prevention "
                    "interventions. Clinical recommendations: Implement structured balance training "
                    "program (e.g., Tai Chi, balance exercises). Consider physical therapy evaluation "
                    "for individualized intervention plan. Assess need for assistive devices and "
                    "home safety modifications. Regular monitoring and reassessment every 3-6 months. "
                    "Review medications for fall risk factors. Educate patient and family on fall "
                    "prevention strategies and warning signs."
                )
            }
        
        elif total_score >= 21:
            return {
                "stage": "Walking with Assistance",
                "description": "Significant balance impairment requiring walking aid",
                "interpretation": (
                    base_interpretation +
                    "SIGNIFICANT IMPAIRMENT: Score indicates significant balance impairment requiring "
                    "walking aids and supervision. High fall risk present. Clinical recommendations: "
                    "Immediate physical therapy referral for comprehensive assessment and treatment. "
                    "Prescribe appropriate assistive device (walker, cane) with proper training. "
                    "Implement comprehensive fall prevention program including home safety assessment, "
                    "medication review, and vision check. Close supervision needed for mobility "
                    "activities. Consider occupational therapy for ADL modifications. Regular "
                    "reassessment every 1-3 months to monitor progress."
                )
            }
        
        else:  # score <= 20
            return {
                "stage": "Wheelchair Bound",
                "description": "Severe balance impairment requiring wheelchair",
                "interpretation": (
                    base_interpretation +
                    "SEVERE IMPAIRMENT: Score indicates severe balance impairment typically requiring "
                    "wheelchair use. Extremely high fall risk present. Clinical recommendations: "
                    "Immediate comprehensive rehabilitation assessment including physical and "
                    "occupational therapy. Focus on wheelchair mobility training and transfer safety. "
                    "Implement maximum fall prevention strategies including environmental modifications "
                    "and 24-hour supervision when out of wheelchair. Address underlying medical "
                    "conditions contributing to balance impairment. Consider power wheelchair if "
                    "manual propulsion is unsafe. Regular reassessment to monitor for any improvement "
                    "potential with intensive rehabilitation."
                )
            }


def calculate_berg_balance_scale(**kwargs) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = BergBalanceScaleCalculator()
    return calculator.calculate(**kwargs)