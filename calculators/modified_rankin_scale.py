"""
Modified Rankin Scale (mRS) Calculator

Measures the degree of disability or dependence in daily activities of people 
who have suffered a stroke or other causes of neurological disability. The most 
widely used outcome scale in acute stroke trials and clinical practice.

References:
1. Rankin J. Scott Med J. 1957;2(7):200-15.
2. Warlow C, et al. Stroke: A Practical Guide to Management. Oxford: Blackwell; 2001.
3. Bruno A, et al. Stroke. 2010;41(5):1048-50.
"""

from typing import Dict, Any


class ModifiedRankinScaleCalculator:
    """Calculator for Modified Rankin Scale (mRS)"""
    
    def __init__(self):
        # Scoring mappings for functional status levels
        self.FUNCTIONAL_STATUS_SCORES = {
            "no_symptoms": 0,
            "no_significant_disability": 1,
            "slight_disability": 2,
            "moderate_disability": 3,
            "moderately_severe_disability": 4,
            "severe_disability": 5,
            "dead": 6
        }
        
        # Detailed descriptions for each level
        self.STATUS_DESCRIPTIONS = {
            "no_symptoms": "No symptoms at all",
            "no_significant_disability": "No significant disability; able to carry out all usual duties and activities",
            "slight_disability": "Slight disability; unable to carry out all previous activities, but able to look after own affairs without assistance",
            "moderate_disability": "Moderate disability; requiring some help, but able to walk without assistance",
            "moderately_severe_disability": "Moderately severe disability; unable to walk and attend to bodily needs without assistance",
            "severe_disability": "Severe disability; bedridden, incontinent and requiring constant nursing care and attention",
            "dead": "Dead"
        }
    
    def calculate(self, functional_status: str) -> Dict[str, Any]:
        """
        Calculates the Modified Rankin Scale score
        
        Args:
            functional_status (str): Patient's current functional status level
            
        Returns:
            Dict with mRS score and clinical interpretation
        """
        
        # Validate inputs
        self._validate_inputs(functional_status)
        
        # Get score
        score = self.FUNCTIONAL_STATUS_SCORES[functional_status]
        
        # Get interpretation
        interpretation = self._get_interpretation(functional_status, score)
        
        return {
            "result": score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, functional_status: str):
        """Validates input parameters"""
        
        if functional_status not in self.FUNCTIONAL_STATUS_SCORES:
            valid_statuses = ", ".join(self.FUNCTIONAL_STATUS_SCORES.keys())
            raise ValueError(f"Functional status must be one of: {valid_statuses}")
    
    def _get_interpretation(self, functional_status: str, score: int) -> Dict[str, str]:
        """
        Provides clinical interpretation based on mRS score
        
        Args:
            functional_status (str): Functional status identifier
            score (int): mRS score
            
        Returns:
            Dict with interpretation details
        """
        
        interpretations = {
            "no_symptoms": {
                "stage": "No Symptoms",
                "description": "No symptoms at all",
                "interpretation": (f"Modified Rankin Scale {score}: No symptoms at all. The patient has "
                                f"achieved complete functional recovery with perfect health and no residual "
                                f"symptoms from their neurological event. Complete independence in all "
                                f"activities of daily living. This represents the best possible outcome "
                                f"following stroke or other neurological injury. No assistance or "
                                f"accommodations are needed for any activities.")
            },
            "no_significant_disability": {
                "stage": "No Significant Disability",
                "description": "Able to carry out all usual duties and activities",
                "interpretation": (f"Modified Rankin Scale {score}: No significant disability despite symptoms. "
                                f"The patient is able to carry out all usual duties and activities despite "
                                f"having some residual symptoms from their neurological event. This may "
                                f"include minor symptoms that do not interfere with daily function. "
                                f"Maintains independence in work, social activities, and self-care. "
                                f"Excellent functional outcome with minimal impact on quality of life.")
            },
            "slight_disability": {
                "stage": "Slight Disability",
                "description": "Unable to carry out all previous activities but can look after own affairs",
                "interpretation": (f"Modified Rankin Scale {score}: Slight disability. The patient is unable "
                                f"to carry out all previous activities but is able to look after their own "
                                f"affairs without assistance. This may include loss of some leisure activities "
                                f"or work modifications, but maintains independence in basic and instrumental "
                                f"activities of daily living. Good functional outcome with some lifestyle "
                                f"adjustments. May benefit from occupational therapy for activity modification.")
            },
            "moderate_disability": {
                "stage": "Moderate Disability",
                "description": "Requires some help but able to walk unassisted",
                "interpretation": (f"Modified Rankin Scale {score}: Moderate disability. The patient requires "
                                f"some help with activities but is able to walk unassisted. This typically "
                                f"includes need for assistance with complex tasks, shopping, or household "
                                f"management, but maintains mobility independence. May require help with "
                                f"medication management, finances, or transportation. Benefits from "
                                f"rehabilitation services and community support programs.")
            },
            "moderately_severe_disability": {
                "stage": "Moderately Severe Disability",
                "description": "Unable to attend to bodily needs without assistance and unable to walk unassisted",
                "interpretation": (f"Modified Rankin Scale {score}: Moderately severe disability. The patient "
                                f"is unable to attend to their own bodily needs without assistance and "
                                f"unable to walk unassisted. Requires help with bathing, dressing, toileting, "
                                f"and mobility. May use assistive devices for ambulation or require wheelchair. "
                                f"Needs regular caregiver support and may benefit from day programs or "
                                f"assisted living arrangements. Significant impact on independence and "
                                f"quality of life.")
            },
            "severe_disability": {
                "stage": "Severe Disability",
                "description": "Bedridden, incontinent and requiring constant nursing care",
                "interpretation": (f"Modified Rankin Scale {score}: Severe disability. The patient is "
                                f"bedridden, incontinent, and requires constant nursing care and attention. "
                                f"Complete dependence for all activities of daily living including feeding, "
                                f"positioning, and basic hygiene. Requires skilled nursing facility care "
                                f"or intensive home care with 24-hour supervision. Significant burden on "
                                f"family caregivers. Focus on comfort care, prevention of complications, "
                                f"and maintaining dignity.")
            },
            "dead": {
                "stage": "Dead",
                "description": "Death",
                "interpretation": (f"Modified Rankin Scale {score}: The patient has died. This represents "
                                f"the most severe outcome following neurological injury or stroke. Death "
                                f"may have occurred due to the primary neurological event, complications "
                                f"such as brain herniation, systemic complications, or withdrawal of "
                                f"life-sustaining treatments. This outcome emphasizes the serious nature "
                                f"of neurological injuries and the importance of prevention and acute "
                                f"intervention strategies.")
            }
        }
        
        return interpretations.get(functional_status, {
            "stage": f"mRS {score}",
            "description": "Unknown status",
            "interpretation": f"Modified Rankin Scale score {score}: Unknown functional status."
        })


def calculate_modified_rankin_scale(functional_status: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = ModifiedRankinScaleCalculator()
    return calculator.calculate(functional_status)