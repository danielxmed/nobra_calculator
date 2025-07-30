"""
Brief Addiction Monitor (BAM) Calculator

Assesses substance use-related behaviors over the past 30 days.

References:
- Cacciola JS, et al. J Subst Abuse Treat. 2013;44(3):256-63.
- Nelson KG, et al. J Subst Abuse Treat. 2014;46(4):472-81.
- McDonell MG, et al. Addict Behav. 2016;63:118-24.
"""

from typing import Dict, Any


class BamCalculator:
    """Calculator for Brief Addiction Monitor (BAM)"""
    
    def __init__(self):
        # Question response scores (inverted for some protective factors)
        self.RESPONSE_SCORES = {
            'standard': {0: 0, 1: 1, 2: 2, 3: 3, 4: 4},
            'inverted': {0: 4, 1: 3, 2: 2, 3: 1, 4: 0},
            'binary': {0: 0, 4: 4}
        }
    
    def calculate(self, physical_health: int, sleep_troubles: int, emotional_distress: int,
                  alcohol_use: int, alcohol_intoxication: int, illegal_drug_use: int,
                  marijuana_use: int, cravings: int, abstinence_confidence: int,
                  self_help_attendance: int, risky_situations: int, spiritual_support: int,
                  work_participation: int, income_adequate: int, family_conflicts: int,
                  social_support: int, recovery_satisfaction: int) -> Dict[str, Any]:
        """
        Calculates the BAM score using provided parameters
        
        Args:
            All parameters are integers representing responses (0-4 scale)
            
        Returns:
            Dict with total score and subscale scores
        """
        
        # Validate inputs
        self._validate_inputs(physical_health, sleep_troubles, emotional_distress,
                            alcohol_use, alcohol_intoxication, illegal_drug_use,
                            marijuana_use, cravings, abstinence_confidence,
                            self_help_attendance, risky_situations, spiritual_support,
                            work_participation, income_adequate, family_conflicts,
                            social_support, recovery_satisfaction)
        
        # Apply scoring (some items need to be inverted for protective factors)
        scores = {
            'physical_health': self.RESPONSE_SCORES['inverted'][physical_health],
            'sleep_troubles': sleep_troubles,
            'emotional_distress': emotional_distress,
            'alcohol_use': alcohol_use,
            'alcohol_intoxication': alcohol_intoxication,
            'illegal_drug_use': illegal_drug_use,
            'marijuana_use': marijuana_use,
            'cravings': cravings,
            'abstinence_confidence': self.RESPONSE_SCORES['inverted'][abstinence_confidence],
            'self_help_attendance': self.RESPONSE_SCORES['inverted'][self_help_attendance],
            'risky_situations': risky_situations,
            'spiritual_support': self.RESPONSE_SCORES['inverted'][spiritual_support],
            'work_participation': self.RESPONSE_SCORES['inverted'][work_participation],
            'income_adequate': self.RESPONSE_SCORES['inverted'][income_adequate] if income_adequate in [0, 4] else income_adequate,
            'family_conflicts': family_conflicts,
            'social_support': self.RESPONSE_SCORES['inverted'][social_support],
            'recovery_satisfaction': self.RESPONSE_SCORES['inverted'][recovery_satisfaction]
        }
        
        # Calculate subscales
        use_factors = (scores['alcohol_use'] + scores['alcohol_intoxication'] + 
                      scores['illegal_drug_use'] + scores['marijuana_use'])
        
        risk_factors = (scores['physical_health'] + scores['sleep_troubles'] + 
                       scores['emotional_distress'] + scores['cravings'] + 
                       scores['risky_situations'] + scores['family_conflicts'])
        
        protective_factors = (scores['abstinence_confidence'] + scores['self_help_attendance'] + 
                            scores['spiritual_support'] + scores['work_participation'] + 
                            scores['income_adequate'] + scores['social_support'] + 
                            scores['recovery_satisfaction'])
        
        # Calculate total score
        total_score = sum(scores.values())
        
        # Determine interpretation
        interpretation = self._get_interpretation(total_score, use_factors, risk_factors, protective_factors)
        
        return {
            "result": total_score,
            "unit": "points",
            "interpretation": interpretation,
            "stage": "Assessment Complete",
            "stage_description": f"Total: {total_score}, Use: {use_factors}, Risk: {risk_factors}, Protective: {protective_factors}",
            "subscales": {
                "use_factors": use_factors,
                "risk_factors": risk_factors,
                "protective_factors": protective_factors
            }
        }
    
    def _validate_inputs(self, *args):
        """Validates input parameters"""
        
        # All parameters except income_adequate should be 0-4
        for i, value in enumerate(args):
            if i == 13:  # income_adequate is binary (0 or 4)
                if value not in [0, 4]:
                    raise ValueError(f"Income adequate must be 0 or 4, got {value}")
            else:
                if not isinstance(value, int) or value < 0 or value > 4:
                    raise ValueError(f"All parameters must be integers between 0 and 4")
    
    def _get_interpretation(self, total_score: int, use_factors: int, 
                           risk_factors: int, protective_factors: int) -> str:
        """
        Determines interpretation based on scores
        
        Args:
            total_score: Total BAM score
            use_factors: Use subscale score
            risk_factors: Risk subscale score  
            protective_factors: Protective subscale score
            
        Returns:
            Clinical interpretation
        """
        
        interpretation_parts = []
        
        # Interpret use factors (0-16 scale)
        if use_factors == 0:
            interpretation_parts.append("No substance use reported in past 30 days.")
        elif use_factors <= 4:
            interpretation_parts.append("Minimal substance use reported.")
        elif use_factors <= 8:
            interpretation_parts.append("Moderate substance use reported.")
        else:
            interpretation_parts.append("Significant substance use reported.")
        
        # Interpret risk factors (0-24 scale)
        if risk_factors <= 6:
            interpretation_parts.append("Low risk factors present.")
        elif risk_factors <= 12:
            interpretation_parts.append("Moderate risk factors present.")
        else:
            interpretation_parts.append("High risk factors present.")
        
        # Interpret protective factors (0-28 scale)
        if protective_factors <= 7:
            interpretation_parts.append("Strong protective factors present.")
        elif protective_factors <= 14:
            interpretation_parts.append("Moderate protective factors present.")
        else:
            interpretation_parts.append("Weak protective factors present.")
        
        # Overall assessment
        if total_score <= 20:
            interpretation_parts.append("Overall low severity profile suggesting good recovery status.")
        elif total_score <= 40:
            interpretation_parts.append("Overall moderate severity profile suggesting ongoing recovery challenges.")
        else:
            interpretation_parts.append("Overall high severity profile suggesting significant recovery difficulties.")
        
        return " ".join(interpretation_parts)


def calculate_bam(physical_health: int, sleep_troubles: int, emotional_distress: int,
                  alcohol_use: int, alcohol_intoxication: int, illegal_drug_use: int,
                  marijuana_use: int, cravings: int, abstinence_confidence: int,
                  self_help_attendance: int, risky_situations: int, spiritual_support: int,
                  work_participation: int, income_adequate: int, family_conflicts: int,
                  social_support: int, recovery_satisfaction: int) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = BamCalculator()
    return calculator.calculate(physical_health, sleep_troubles, emotional_distress,
                               alcohol_use, alcohol_intoxication, illegal_drug_use,
                               marijuana_use, cravings, abstinence_confidence,
                               self_help_attendance, risky_situations, spiritual_support,
                               work_participation, income_adequate, family_conflicts,
                               social_support, recovery_satisfaction)