"""
Modified Rankin Score 9Q (mRS-9Q) Calculator

9-question yes/no survey that provides simple and reliable determination of the 
modified Rankin Scale score in neurosurgical and neurological patients. Reduces 
subjectivity and can be administered by medical or non-medical personnel.

References:
1. Bruno A, et al. Stroke. 2010;41(5):1048-50.
2. Bruno A, et al. Stroke. 2012;43(8):2086-90.  
3. Bruno A, et al. Stroke. 2011;42(8):2276-9.
"""

from typing import Dict, Any


class ModifiedRankinScore9QCalculator:
    """Calculator for Modified Rankin Score 9Q (mRS-9Q)"""
    
    def __init__(self):
        # Question mappings for yes/no responses
        self.YES_NO_MAPPING = {
            "yes": True,
            "no": False
        }
    
    def calculate(self, symptoms_bothering: str, same_work: str, keep_hobbies: str,
                  maintain_social_ties: str, need_help_basic_tasks: str,
                  need_help_shopping_travel: str, need_help_walking: str,
                  need_help_personal_care: str, bedridden_nursing_care: str) -> Dict[str, Any]:
        """
        Calculates the Modified Rankin Score 9Q using the algorithm-based approach
        
        Args:
            symptoms_bothering (str): Do you have any symptoms that are bothering you?
            same_work (str): Are you able to do the same work as before?
            keep_hobbies (str): Are you able to keep up with your hobbies?
            maintain_social_ties (str): Have you maintained your ties to friends and family?
            need_help_basic_tasks (str): Need help making meals, chores, or balancing checkbook?
            need_help_shopping_travel (str): Need help with shopping or traveling close to home?
            need_help_walking (str): Do you need another person to help you walk?
            need_help_personal_care (str): Need help with eating, toilet, or bathing?
            bedridden_nursing_care (str): Stay in bed most of day and need constant nursing care?
            
        Returns:
            Dict with mRS-9Q score and clinical interpretation
        """
        
        # Validate inputs
        self._validate_inputs(symptoms_bothering, same_work, keep_hobbies,
                             maintain_social_ties, need_help_basic_tasks,
                             need_help_shopping_travel, need_help_walking,
                             need_help_personal_care, bedridden_nursing_care)
        
        # Convert string responses to boolean
        q1 = self.YES_NO_MAPPING[symptoms_bothering]  # Symptoms bothering
        q2 = self.YES_NO_MAPPING[same_work]           # Same work
        q3 = self.YES_NO_MAPPING[keep_hobbies]        # Keep hobbies  
        q4 = self.YES_NO_MAPPING[maintain_social_ties] # Maintain social ties
        q5 = self.YES_NO_MAPPING[need_help_basic_tasks] # Help with basic tasks
        q6 = self.YES_NO_MAPPING[need_help_shopping_travel] # Help shopping/travel
        q7 = self.YES_NO_MAPPING[need_help_walking]   # Help walking
        q8 = self.YES_NO_MAPPING[need_help_personal_care] # Help personal care
        q9 = self.YES_NO_MAPPING[bedridden_nursing_care] # Bedridden/nursing care
        
        # Apply mRS-9Q algorithm
        score = self._calculate_mrs_algorithm(q1, q2, q3, q4, q5, q6, q7, q8, q9)
        
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
        """Validates all input parameters are valid yes/no responses"""
        
        for i, arg in enumerate(args, 1):
            if arg not in self.YES_NO_MAPPING:
                raise ValueError(f"Question {i} response must be 'yes' or 'no', got: {arg}")
    
    def _calculate_mrs_algorithm(self, q1: bool, q2: bool, q3: bool, q4: bool,
                                q5: bool, q6: bool, q7: bool, q8: bool, q9: bool) -> int:
        """
        Implements the mRS-9Q algorithm to determine final mRS score
        
        Algorithm logic based on Bruno et al. validation studies:
        - Q1 (symptoms) determines mRS 0 vs ≥1
        - Higher disability levels take precedence
        - Sequential logic determines final score
        """
        
        # mRS 5: Bedridden and requiring constant nursing care
        if q9:  # Stay in bed most of day and need constant nursing care
            return 5
        
        # mRS 4: Unable to attend to bodily needs without assistance
        if q8:  # Need help with eating, toilet, or bathing
            return 4
        
        # mRS 4: Unable to walk without assistance  
        if q7:  # Need another person to help walk
            return 4
            
        # mRS 3: Requires some help but able to walk unassisted
        if q5 or q6:  # Need help with basic tasks OR shopping/travel
            return 3
        
        # mRS 2: Unable to carry out all previous activities but independent
        if not q2 or not q3 or not q4:  # Can't do same work OR keep hobbies OR maintain social ties
            return 2
        
        # mRS 1: No significant disability despite symptoms
        if q1:  # Have symptoms that are bothering you
            return 1
        
        # mRS 0: No symptoms at all
        return 0
    
    def _get_interpretation(self, score: int) -> Dict[str, str]:
        """
        Provides clinical interpretation based on mRS-9Q score
        
        Args:
            score (int): mRS-9Q score
            
        Returns:
            Dict with interpretation details
        """
        
        interpretations = {
            0: {
                "stage": "No Symptoms",
                "description": "No symptoms at all",
                "interpretation": (f"mRS-9Q Score {score}: No symptoms at all. The patient has achieved "
                                f"complete functional recovery with no residual symptoms from their "
                                f"neurological condition. Perfect health with complete independence in "
                                f"all activities of daily living. This represents the best possible "
                                f"outcome following stroke or other neurological injury. No assistance "
                                f"or accommodations are needed for any activities.")
            },
            1: {
                "stage": "No Significant Disability", 
                "description": "Symptoms present but able to carry out all usual duties",
                "interpretation": (f"mRS-9Q Score {score}: No significant disability despite symptoms. "
                                f"The patient has some symptoms that are bothering them but is able "
                                f"to carry out all usual duties and activities. This includes maintaining "
                                f"work, hobbies, and social relationships. Minor symptoms do not interfere "
                                f"with daily function. Excellent functional outcome with minimal impact "
                                f"on quality of life and independence.")
            },
            2: {
                "stage": "Slight Disability",
                "description": "Unable to carry out all previous activities but independent", 
                "interpretation": (f"mRS-9Q Score {score}: Slight disability. The patient is unable "
                                f"to carry out all previous activities but remains able to look after "
                                f"their own affairs without assistance. This may include inability to "
                                f"perform the same work as before, difficulty keeping up with hobbies, "
                                f"or challenges maintaining all social connections. However, basic and "
                                f"instrumental activities of daily living remain independent. Good "
                                f"functional outcome with lifestyle adjustments.")
            },
            3: {
                "stage": "Moderate Disability",
                "description": "Requires some help but able to walk unassisted",
                "interpretation": (f"mRS-9Q Score {score}: Moderate disability. The patient requires "
                                f"some help with daily activities but is able to walk unassisted. "
                                f"This includes needing assistance with making meals, household chores, "
                                f"balancing finances, shopping, or traveling close to home. While "
                                f"mobility remains independent, complex instrumental activities require "
                                f"support. Benefits from community services and occupational therapy.")
            },
            4: {
                "stage": "Moderately Severe Disability", 
                "description": "Unable to attend to bodily needs without assistance",
                "interpretation": (f"mRS-9Q Score {score}: Moderately severe disability. The patient "
                                f"is unable to attend to their own bodily needs without assistance "
                                f"and/or unable to walk without help from another person. Requires "
                                f"assistance with eating, toileting, bathing, and/or mobility. "
                                f"Significant functional impairment affecting independence in basic "
                                f"activities of daily living. Needs regular caregiver support and "
                                f"may benefit from assisted living or skilled care.")
            },
            5: {
                "stage": "Severe Disability",
                "description": "Bedridden and requiring constant nursing care",
                "interpretation": (f"mRS-9Q Score {score}: Severe disability. The patient stays in "
                                f"bed most of the day and requires constant nursing care and attention. "
                                f"Complete dependence for all activities of daily living including "
                                f"feeding, positioning, hygiene, and basic medical care. Requires "
                                f"skilled nursing facility care or intensive home care with 24-hour "
                                f"supervision. Significant burden on family caregivers and healthcare "
                                f"system. Focus on comfort care and maintaining dignity.")
            }
        }
        
        return interpretations.get(score, {
            "stage": f"mRS {score}",
            "description": "Unknown status",
            "interpretation": f"mRS-9Q Score {score}: Unknown functional status."
        })


def calculate_modified_rankin_score_9q(symptoms_bothering: str, same_work: str,
                                      keep_hobbies: str, maintain_social_ties: str,
                                      need_help_basic_tasks: str, need_help_shopping_travel: str,
                                      need_help_walking: str, need_help_personal_care: str,
                                      bedridden_nursing_care: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = ModifiedRankinScore9QCalculator()
    return calculator.calculate(symptoms_bothering, same_work, keep_hobbies,
                               maintain_social_ties, need_help_basic_tasks,
                               need_help_shopping_travel, need_help_walking,
                               need_help_personal_care, bedridden_nursing_care)