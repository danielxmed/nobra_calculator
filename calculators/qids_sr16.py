"""
Quick Inventory of Depressive Symptomatology (QIDS-SR-16) Calculator

Assesses depressive symptoms by self-report using 16 items covering the 9 DSM-IV 
depression criterion symptom domains. This validated instrument evaluates depression 
severity over the prior 7 days and is used for screening, monitoring treatment 
response, and research applications.

References:
1. Rush AJ, Trivedi MH, Ibrahim HM, Carmody TJ, Arnow B, Klein DN, et al. 
   The 16-Item Quick Inventory of Depressive Symptomatology (QIDS), clinician rating 
   (QIDS-C), and self-report (QIDS-SR): a psychometric evaluation in patients with 
   chronic major depression. Biol Psychiatry. 2003 Sep 1;54(5):573-83. 
   doi: 10.1016/s0006-3223(02)01866-8.
2. Trivedi MH, Rush AJ, Ibrahim HM, Carmody TJ, Biggs MM, Suppes T, et al. 
   The Inventory of Depressive Symptomatology, Clinician Rating (IDS-C) and Self-Report 
   (IDS-SR), and the Quick Inventory of Depressive Symptomatology, Clinician Rating 
   (QIDS-C) and Self-Report (QIDS-SR) in public sector patients with mood disorders: 
   a psychometric evaluation. Psychol Med. 2004 Jan;34(1):73-82. doi: 10.1017/s0033291703001107.
"""

from typing import Dict, Any


class QidsSr16Calculator:
    """Calculator for Quick Inventory of Depressive Symptomatology (QIDS-SR-16)"""
    
    def __init__(self):
        # Severity thresholds
        self.NO_DEPRESSION_MAX = 5
        self.MILD_DEPRESSION_MAX = 10
        self.MODERATE_DEPRESSION_MAX = 15
        self.SEVERE_DEPRESSION_MAX = 20
    
    def calculate(self, sleep_onset: int, sleep_maintenance: int, early_awakening: int,
                 hypersomnia: int, sad_mood: int, appetite_decrease: int, appetite_increase: int,
                 weight_decrease: int, weight_increase: int, concentration: int, self_view: int,
                 suicidal_ideation: int, general_interest: int, energy_level: int,
                 psychomotor_slowing: int, psychomotor_agitation: int) -> Dict[str, Any]:
        """
        Calculates QIDS-SR-16 score for depression severity assessment
        
        Args:
            sleep_onset (int): Falling asleep difficulty (0-3)
            sleep_maintenance (int): Sleep during the night issues (0-3)
            early_awakening (int): Waking up too early (0-3)
            hypersomnia (int): Sleeping too much (0-3)
            sad_mood (int): Feeling sad (0-3)
            appetite_decrease (int): Decreased appetite (0-3)
            appetite_increase (int): Increased appetite (0-3)
            weight_decrease (int): Decreased weight (0-3)
            weight_increase (int): Increased weight (0-3)
            concentration (int): Concentration/decision making (0-3)
            self_view (int): View of myself (0-3)
            suicidal_ideation (int): Thoughts of death or suicide (0-3)
            general_interest (int): General interest (0-3)
            energy_level (int): Energy level (0-3)
            psychomotor_slowing (int): Feeling slowed down (0-3)
            psychomotor_agitation (int): Feeling restless (0-3)
            
        Returns:
            Dict with QIDS-SR-16 score and clinical interpretation
        """
        
        # Validate inputs
        self._validate_inputs(sleep_onset, sleep_maintenance, early_awakening, hypersomnia,
                             sad_mood, appetite_decrease, appetite_increase, weight_decrease,
                             weight_increase, concentration, self_view, suicidal_ideation,
                             general_interest, energy_level, psychomotor_slowing, psychomotor_agitation)
        
        # Calculate total QIDS-SR-16 score using special scoring rules
        total_score = self._calculate_total_score(sleep_onset, sleep_maintenance, early_awakening,
                                                 hypersomnia, sad_mood, appetite_decrease, appetite_increase,
                                                 weight_decrease, weight_increase, concentration, self_view,
                                                 suicidal_ideation, general_interest, energy_level,
                                                 psychomotor_slowing, psychomotor_agitation)
        
        # Get interpretation
        interpretation = self._get_interpretation(total_score)
        
        return {
            "result": total_score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, sleep_onset: int, sleep_maintenance: int, early_awakening: int,
                        hypersomnia: int, sad_mood: int, appetite_decrease: int, appetite_increase: int,
                        weight_decrease: int, weight_increase: int, concentration: int, self_view: int,
                        suicidal_ideation: int, general_interest: int, energy_level: int,
                        psychomotor_slowing: int, psychomotor_agitation: int):
        """Validates input parameters"""
        
        # List of all parameters with their names for validation
        parameters = [
            (sleep_onset, "sleep_onset"),
            (sleep_maintenance, "sleep_maintenance"),
            (early_awakening, "early_awakening"),
            (hypersomnia, "hypersomnia"),
            (sad_mood, "sad_mood"),
            (appetite_decrease, "appetite_decrease"),
            (appetite_increase, "appetite_increase"),
            (weight_decrease, "weight_decrease"),
            (weight_increase, "weight_increase"),
            (concentration, "concentration"),
            (self_view, "self_view"),
            (suicidal_ideation, "suicidal_ideation"),
            (general_interest, "general_interest"),
            (energy_level, "energy_level"),
            (psychomotor_slowing, "psychomotor_slowing"),
            (psychomotor_agitation, "psychomotor_agitation")
        ]
        
        for param, name in parameters:
            if not isinstance(param, int) or param < 0 or param > 3:
                raise ValueError(f"{name} must be an integer between 0 and 3")
    
    def _calculate_total_score(self, sleep_onset: int, sleep_maintenance: int, early_awakening: int,
                              hypersomnia: int, sad_mood: int, appetite_decrease: int, appetite_increase: int,
                              weight_decrease: int, weight_increase: int, concentration: int, self_view: int,
                              suicidal_ideation: int, general_interest: int, energy_level: int,
                              psychomotor_slowing: int, psychomotor_agitation: int) -> int:
        """Calculates the total QIDS-SR-16 score using special scoring rules"""
        
        # Sleep domain: use the highest score among the 4 sleep items
        sleep_score = max(sleep_onset, sleep_maintenance, early_awakening, hypersomnia)
        
        # Appetite/weight domain: use the highest score among the 4 appetite/weight items
        appetite_weight_score = max(appetite_decrease, appetite_increase, weight_decrease, weight_increase)
        
        # Psychomotor domain: use the highest score among agitation and retardation
        psychomotor_score = max(psychomotor_slowing, psychomotor_agitation)
        
        # Calculate total score: sleep + mood + appetite/weight + other core symptoms + psychomotor
        total_score = (
            sleep_score +  # Items 1-4 (highest score)
            sad_mood +  # Item 5
            appetite_weight_score +  # Items 6-9 (highest score)
            concentration +  # Item 10
            self_view +  # Item 11
            suicidal_ideation +  # Item 12
            general_interest +  # Item 13
            energy_level +  # Item 14
            psychomotor_score  # Items 15-16 (highest score)
        )
        
        return total_score
    
    def _get_interpretation(self, score: int) -> Dict[str, str]:
        """
        Determines clinical interpretation based on QIDS-SR-16 score
        
        Args:
            score (int): Calculated QIDS-SR-16 score
            
        Returns:
            Dict with clinical interpretation
        """
        
        if score <= self.NO_DEPRESSION_MAX:  # 0-5
            return {
                "stage": "No Depression",
                "description": "No depression",
                "interpretation": "No depression present. Score indicates absence of clinically significant depressive symptoms. Continue routine monitoring and maintain current well-being strategies. Consider preventive mental health measures and lifestyle factors that support emotional wellness including regular exercise, adequate sleep, social connections, and stress management."
            }
        elif score <= self.MILD_DEPRESSION_MAX:  # 6-10
            return {
                "stage": "Mild Depression",
                "description": "Mild depression",
                "interpretation": "Mild depression. Some depressive symptoms present that may warrant attention and monitoring. Consider lifestyle interventions including exercise, sleep hygiene, stress reduction techniques, and psychoeducation. Supportive counseling or brief therapy may be beneficial. Reassess in 2-4 weeks and monitor for progression of symptoms."
            }
        elif score <= self.MODERATE_DEPRESSION_MAX:  # 11-15
            return {
                "stage": "Moderate Depression",
                "description": "Moderate depression",
                "interpretation": "Moderate depression. Clinically significant depressive symptoms requiring active treatment. Consider evidence-based psychotherapy (CBT, IPT, behavioral activation), medication evaluation with antidepressants, or combination treatment. Monitor for functional impairment, safety concerns, and treatment response. Reassess every 2-4 weeks initially."
            }
        elif score <= self.SEVERE_DEPRESSION_MAX:  # 16-20
            return {
                "stage": "Severe Depression",
                "description": "Severe depression",
                "interpretation": "Severe depression. Significant depressive symptoms requiring immediate attention and intensive treatment. Strongly recommend combination of psychotherapy and antidepressant medication. Monitor closely for safety concerns including suicidal ideation (item 12 score ≥2 requires immediate risk assessment). Consider psychiatric consultation and comprehensive treatment planning with close follow-up."
            }
        else:  # 21-27
            return {
                "stage": "Very Severe Depression",
                "description": "Very severe depression",
                "interpretation": "Very severe depression. Requires immediate psychiatric evaluation and intensive treatment intervention. High risk for significant functional impairment and safety concerns. Immediate suicide risk assessment essential. Consider hospitalization if suicidal risk present. Implement comprehensive treatment plan with frequent monitoring, family involvement, and coordinated care team approach."
            }


def calculate_qids_sr16(sleep_onset: int, sleep_maintenance: int, early_awakening: int,
                       hypersomnia: int, sad_mood: int, appetite_decrease: int, appetite_increase: int,
                       weight_decrease: int, weight_increase: int, concentration: int, self_view: int,
                       suicidal_ideation: int, general_interest: int, energy_level: int,
                       psychomotor_slowing: int, psychomotor_agitation: int) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = QidsSr16Calculator()
    return calculator.calculate(sleep_onset, sleep_maintenance, early_awakening, hypersomnia,
                               sad_mood, appetite_decrease, appetite_increase, weight_decrease,
                               weight_increase, concentration, self_view, suicidal_ideation,
                               general_interest, energy_level, psychomotor_slowing, psychomotor_agitation)