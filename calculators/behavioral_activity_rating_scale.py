"""
Behavioral Activity Rating Scale (BARS) Calculator

Screens patients for agitation in emergency care and psychiatric settings using 
a 7-point observational scale.

References (Vancouver style):
1. Swift RH, Harrigan EP, Cappelleri JC, Kramer D, Chandler LP. Validation of the 
   behavioural activity rating scale (BARS): a novel measure of activity in agitated 
   patients. J Psychiatr Res. 2002 Mar-Apr;36(2):87-95.
2. Lindenmayer JP, Bossie CA, Kujawa M, Zhu Y, Canuso CM. Dimensions of agitation 
   in schizophrenia: results from the CATIE study. Schizophr Res. 2009 Feb;107(2-3):225-30.
3. Price LM, Forbat L, Chew-Graham C, Palen L, Robinson D, McGoldrick M, et al. 
   Learning and performance outcomes of mental health first aid training: a systematic 
   review of randomized controlled trials. Acad Med. 2018 Sep;93(9):1404-13.
"""

from typing import Dict, Any


class BehavioralActivityRatingScaleCalculator:
    """Calculator for Behavioral Activity Rating Scale (BARS)"""
    
    def __init__(self):
        # BARS scale descriptions
        self.scale_descriptions = {
            1: "Difficult or unable to arouse",
            2: "Asleep but responds normally to verbal or physical contact",
            3: "Drowsy, appears sedated", 
            4: "Quiet and awake (normal level of activity)",
            5: "Signs of over activity (physical or verbal); calms down with instructions",
            6: "Extremely or continuously active; does not require restraint",
            7: "Violent behavior requiring restraint"
        }
        
        # Clinical intervention threshold
        self.INTERVENTION_THRESHOLD = 4
    
    def calculate(self, activity_level: int) -> Dict[str, Any]:
        """
        Evaluates BARS score and provides clinical interpretation
        
        Args:
            activity_level (int): Observed activity level on 1-7 scale
            
        Returns:
            Dict with BARS score and clinical interpretation
        """
        
        # Validations
        self._validate_inputs(activity_level)
        
        # The score is the activity level itself
        bars_score = activity_level
        
        # Get interpretation
        interpretation = self._get_interpretation(bars_score)
        
        return {
            "result": bars_score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, activity_level: int):
        """Validates input parameters"""
        
        if not isinstance(activity_level, int):
            raise ValueError("Activity level must be an integer")
        
        if activity_level < 1 or activity_level > 7:
            raise ValueError("Activity level must be between 1 and 7")
    
    def _get_interpretation(self, score: int) -> Dict[str, str]:
        """
        Determines clinical interpretation based on BARS score
        
        Args:
            score (int): BARS score (1-7)
            
        Returns:
            Dict with clinical interpretation
        """
        
        # Get scale description
        scale_description = self.scale_descriptions[score]
        
        if score == 1:
            return {
                "stage": "Hypoactive",
                "description": "Difficult or unable to arouse",
                "interpretation": (
                    f"BARS score: {score}/7 - {scale_description}. "
                    "Patient is significantly under-responsive and difficult to arouse. "
                    "This may indicate oversedation, medical emergency, or severe psychiatric "
                    "withdrawal. Clinical action required: Immediate medical evaluation to "
                    "determine underlying cause. Check vital signs, assess airway, and consider "
                    "reversal agents if medication-induced. May require emergency interventions "
                    "such as naloxone for opioid overdose or flumazenil for benzodiazepine "
                    "overdose. Ensure adequate monitoring and supportive care."
                )
            }
        
        elif score in [2, 3]:
            stage = "Sedated"
            if score == 2:
                description = "Asleep but responds normally to verbal or physical contact"
            else:  # score == 3
                description = "Drowsy, appears sedated"
            
            return {
                "stage": stage,
                "description": description,
                "interpretation": (
                    f"BARS score: {score}/7 - {scale_description}. "
                    "Patient shows signs of sedation but remains responsive to stimulation. "
                    "This level may be appropriate for patients receiving sedating medications "
                    "or recovering from agitation episodes. Clinical considerations: Monitor "
                    "for respiratory depression and maintain airway protection. Assess medication "
                    "effects and timing. Consider dose adjustment if oversedation is present. "
                    "Continue monitoring for changes in mental status."
                )
            }
        
        elif score == 4:
            return {
                "stage": "Normal",
                "description": "Quiet and awake with normal activity level",
                "interpretation": (
                    f"BARS score: {score}/7 - {scale_description}. "
                    "Patient demonstrates normal, calm behavior with appropriate activity level. "
                    "This is the therapeutic target for most patients in emergency psychiatric "
                    "settings. Clinical management: Continue current management approach and "
                    "monitor for changes. Maintain therapeutic environment. This score indicates "
                    "successful de-escalation or appropriate medication response. No immediate "
                    "intervention required, but continue routine monitoring."
                )
            }
        
        elif score == 5:
            return {
                "stage": "Mild Agitation",
                "description": "Overactive but responds to verbal instructions",
                "interpretation": (
                    f"BARS score: {score}/7 - {scale_description}. "
                    "Patient shows signs of mild agitation with increased physical or verbal "
                    "activity but remains responsive to verbal redirection. Clinical action: "
                    "Implement de-escalation techniques including calm verbal communication, "
                    "limit setting, and environmental modifications. Assess for underlying causes "
                    "such as pain, fear, or confusion. Consider non-pharmacological interventions "
                    "first. May warrant clinical assessment for intervention if agitation persists "
                    "or escalates. Scores >4 typically indicate need for clinical evaluation."
                )
            }
        
        elif score == 6:
            return {
                "stage": "Moderate Agitation",
                "description": "Extremely or continuously active without restraint needs",
                "interpretation": (
                    f"BARS score: {score}/7 - {scale_description}. "
                    "Patient displays significant agitation with extreme or continuous activity "
                    "but does not require physical restraints. Clinical action required: "
                    "Implement immediate de-escalation techniques and ensure staff safety measures. "
                    "Consider pharmacological intervention with rapid-acting medications such as "
                    "haloperidol, olanzapine, or lorazepam. Evaluate for underlying medical causes. "
                    "Requires close monitoring and possible treatment escalation. Remove potential "
                    "environmental triggers and maintain therapeutic communication."
                )
            }
        
        else:  # score == 7
            return {
                "stage": "Severe Agitation",
                "description": "Violent behavior requiring restraint",
                "interpretation": (
                    f"BARS score: {score}/7 - {scale_description}. "
                    "Patient exhibits violent behavior that requires physical or chemical restraints "
                    "for safety. This represents the highest level of agitation requiring immediate "
                    "intervention. Emergency protocol activation: Ensure immediate staff and patient "
                    "safety. Implement emergency restraint procedures per institutional policy. "
                    "Administer rapid-acting medications (typically IM haloperidol + lorazepam or "
                    "olanzapine). Evaluate for underlying medical causes including delirium, "
                    "intoxication, or withdrawal. Consider security or code team activation. "
                    "Continuous monitoring required until stabilization achieved."
                )
            }


def calculate_behavioral_activity_rating_scale(activity_level: int) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = BehavioralActivityRatingScaleCalculator()
    return calculator.calculate(activity_level)