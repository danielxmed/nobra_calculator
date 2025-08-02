"""
Modified Fatigue Impact Scale (MFIS) Calculator

Measures the impact that fatigue has on patient's daily life across physical, 
cognitive, and psychosocial domains. Originally developed for multiple sclerosis 
patients but applicable to various conditions.

References:
1. Fisk JD, et al. Clin Infect Dis. 1994;18 Suppl 1:S79-83.
2. Learmonth YC, et al. J Neurol Sci. 2013;331(1-2):102-7.
"""

from typing import Dict, Any


class ModifiedFatigueImpactScaleCalculator:
    """Calculator for Modified Fatigue Impact Scale (MFIS)"""
    
    def __init__(self):
        # MFIS subscale item mappings (1-indexed to match questionnaire)
        # Physical subscale items (maximum 36 points)
        self.PHYSICAL_ITEMS = [4, 6, 7, 10, 13, 14, 17, 20, 21]
        
        # Cognitive subscale items (maximum 40 points)
        self.COGNITIVE_ITEMS = [1, 2, 3, 5, 11, 12, 15, 16, 18, 19]
        
        # Psychosocial subscale items (maximum 8 points)
        self.PSYCHOSOCIAL_ITEMS = [8, 9]
        
        # Item names mapping to their numbers for subscale calculations
        self.ITEM_MAPPING = {
            1: 'less_alert',
            2: 'difficulty_paying_attention',
            3: 'unable_think_clearly',
            4: 'clumsy_uncoordinated',
            5: 'forgetful',
            6: 'pace_physical_activities',
            7: 'less_motivated_physical',
            8: 'less_motivated_social',
            9: 'limited_away_from_home',
            10: 'trouble_maintaining_effort',
            11: 'difficulty_making_decisions',
            12: 'less_motivated_thinking',
            13: 'muscles_weak',
            14: 'physically_uncomfortable',
            15: 'trouble_finishing_thinking_tasks',
            16: 'difficulty_organizing',
            17: 'less_able_physical_tasks',
            18: 'thinking_slowed',
            19: 'trouble_concentrating',
            20: 'limited_physical_activities',
            21: 'need_more_rest'
        }
    
    def calculate(self, less_alert: int, difficulty_paying_attention: int,
                  unable_think_clearly: int, clumsy_uncoordinated: int,
                  forgetful: int, pace_physical_activities: int,
                  less_motivated_physical: int, less_motivated_social: int,
                  limited_away_from_home: int, trouble_maintaining_effort: int,
                  difficulty_making_decisions: int, less_motivated_thinking: int,
                  muscles_weak: int, physically_uncomfortable: int,
                  trouble_finishing_thinking_tasks: int, difficulty_organizing: int,
                  less_able_physical_tasks: int, thinking_slowed: int,
                  trouble_concentrating: int, limited_physical_activities: int,
                  need_more_rest: int) -> Dict[str, Any]:
        """
        Calculates the Modified Fatigue Impact Scale (MFIS) score
        
        Args:
            All 21 MFIS items scored 0-4 (Never=0, Rarely=1, Sometimes=2, Often=3, Almost Always=4)
            
        Returns:
            Dict with total score, subscale scores, and interpretation
        """
        
        # Create values dictionary for easier processing
        values = {
            'less_alert': less_alert,
            'difficulty_paying_attention': difficulty_paying_attention,
            'unable_think_clearly': unable_think_clearly,
            'clumsy_uncoordinated': clumsy_uncoordinated,
            'forgetful': forgetful,
            'pace_physical_activities': pace_physical_activities,
            'less_motivated_physical': less_motivated_physical,
            'less_motivated_social': less_motivated_social,
            'limited_away_from_home': limited_away_from_home,
            'trouble_maintaining_effort': trouble_maintaining_effort,
            'difficulty_making_decisions': difficulty_making_decisions,
            'less_motivated_thinking': less_motivated_thinking,
            'muscles_weak': muscles_weak,
            'physically_uncomfortable': physically_uncomfortable,
            'trouble_finishing_thinking_tasks': trouble_finishing_thinking_tasks,
            'difficulty_organizing': difficulty_organizing,
            'less_able_physical_tasks': less_able_physical_tasks,
            'thinking_slowed': thinking_slowed,
            'trouble_concentrating': trouble_concentrating,
            'limited_physical_activities': limited_physical_activities,
            'need_more_rest': need_more_rest
        }
        
        # Validate inputs
        self._validate_inputs(values)
        
        # Calculate subscale scores
        physical_score = self._calculate_subscale_score(values, self.PHYSICAL_ITEMS)
        cognitive_score = self._calculate_subscale_score(values, self.COGNITIVE_ITEMS)
        psychosocial_score = self._calculate_subscale_score(values, self.PSYCHOSOCIAL_ITEMS)
        
        # Calculate total score
        total_score = physical_score + cognitive_score + psychosocial_score
        
        # Get interpretation
        interpretation = self._get_interpretation(total_score, physical_score, 
                                                cognitive_score, psychosocial_score)
        
        return {
            "result": total_score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"],
            "physical_score": physical_score,
            "cognitive_score": cognitive_score,
            "psychosocial_score": psychosocial_score
        }
    
    def _validate_inputs(self, values: Dict[str, int]):
        """Validates input parameters"""
        
        for item_name, value in values.items():
            # Check data type
            if not isinstance(value, int):
                raise ValueError(f"{item_name} must be an integer")
            
            # Check range (0-4 scale)
            if value < 0 or value > 4:
                raise ValueError(f"{item_name} must be between 0 and 4 (inclusive)")
    
    def _calculate_subscale_score(self, values: Dict[str, int], item_numbers: list) -> int:
        """Calculate subscale score for given items"""
        
        subscale_score = 0
        for item_number in item_numbers:
            item_name = self.ITEM_MAPPING[item_number]
            subscale_score += values[item_name]
        
        return subscale_score
    
    def _get_interpretation(self, total_score: int, physical_score: int,
                          cognitive_score: int, psychosocial_score: int) -> Dict[str, str]:
        """
        Provides clinical interpretation based on MFIS total and subscale scores
        
        Args:
            total_score: Total MFIS score (0-84)
            physical_score: Physical subscale score (0-36)
            cognitive_score: Cognitive subscale score (0-40)
            psychosocial_score: Psychosocial subscale score (0-8)
            
        Returns:
            Dict with interpretation details
        """
        
        # Determine overall interpretation based on cutoff of 38
        if total_score < 38:
            base_interpretation = {
                "stage": "Below Cutoff",
                "description": "Fatigue impact below clinical cutoff",
                "interpretation": (f"MFIS total score of {total_score} is below the clinical cutoff of 38, "
                                "suggesting fatigue impact that may not significantly affect quality of life. "
                                "Continue routine monitoring and consider lifestyle interventions for fatigue management.")
            }
        else:
            base_interpretation = {
                "stage": "Above Cutoff", 
                "description": "Clinically significant fatigue impact",
                "interpretation": (f"MFIS total score of {total_score} indicates clinically significant fatigue impact "
                                "on daily functioning. Consider comprehensive fatigue management strategies including "
                                "energy conservation techniques, exercise programs, and regular monitoring.")
            }
        
        # Add subscale information to interpretation
        subscale_details = (f" Subscale scores: Physical={physical_score}/36, "
                          f"Cognitive={cognitive_score}/40, Psychosocial={psychosocial_score}/8.")
        
        # Identify predominant domains affected
        physical_pct = (physical_score / 36) * 100
        cognitive_pct = (cognitive_score / 40) * 100
        psychosocial_pct = (psychosocial_score / 8) * 100
        
        dominant_domains = []
        if physical_pct >= 50:
            dominant_domains.append("physical")
        if cognitive_pct >= 50:
            dominant_domains.append("cognitive")
        if psychosocial_pct >= 50:
            dominant_domains.append("psychosocial")
        
        if dominant_domains:
            domain_details = f" Primary impact areas: {', '.join(dominant_domains)} functioning."
        else:
            domain_details = " Fatigue impact is distributed across multiple domains."
        
        base_interpretation["interpretation"] += subscale_details + domain_details
        
        return base_interpretation


def calculate_modified_fatigue_impact_scale(less_alert: int, difficulty_paying_attention: int,
                                          unable_think_clearly: int, clumsy_uncoordinated: int,
                                          forgetful: int, pace_physical_activities: int,
                                          less_motivated_physical: int, less_motivated_social: int,
                                          limited_away_from_home: int, trouble_maintaining_effort: int,
                                          difficulty_making_decisions: int, less_motivated_thinking: int,
                                          muscles_weak: int, physically_uncomfortable: int,
                                          trouble_finishing_thinking_tasks: int, difficulty_organizing: int,
                                          less_able_physical_tasks: int, thinking_slowed: int,
                                          trouble_concentrating: int, limited_physical_activities: int,
                                          need_more_rest: int) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = ModifiedFatigueImpactScaleCalculator()
    return calculator.calculate(less_alert, difficulty_paying_attention,
                              unable_think_clearly, clumsy_uncoordinated,
                              forgetful, pace_physical_activities,
                              less_motivated_physical, less_motivated_social,
                              limited_away_from_home, trouble_maintaining_effort,
                              difficulty_making_decisions, less_motivated_thinking,
                              muscles_weak, physically_uncomfortable,
                              trouble_finishing_thinking_tasks, difficulty_organizing,
                              less_able_physical_tasks, thinking_slowed,
                              trouble_concentrating, limited_physical_activities,
                              need_more_rest)