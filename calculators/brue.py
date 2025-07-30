"""
Brief Resolved Unexplained Events (BRUE) Criteria Calculator

Classifies unexplained events in infants <1 year old and replaces the Apparent 
Life-Threatening Events (ALTE) classification. Determines risk stratification 
and management recommendations for infants who have experienced brief, resolved 
episodes of concerning symptoms.

References:
- Tieder JS, et al. Brief resolved unexplained events (formerly apparent 
  life-threatening events) and evaluation of lower-risk infants. Pediatrics. 
  2016;137(5):e20160590.
- American Academy of Pediatrics Subcommittee on Apparent Life-Threatening Events. 
  Apparent life-threatening events in infants: an evidence-based review. 
  Pediatrics. 2003;111(2):361-7.
"""

from typing import Dict, Any


class BrueCalculator:
    """Calculator for Brief Resolved Unexplained Events (BRUE) Criteria"""
    
    def __init__(self):
        # Classification stages
        self.NOT_BRUE = 0
        self.BRUE_HIGHER_RISK = 1
        self.BRUE_LOWER_RISK = 2
    
    def calculate(self, age_under_1_year: str, asymptomatic_on_presentation: str,
                 no_explanation_after_exam: str, sudden_brief_resolved_episode: str,
                 cyanosis_or_pallor: str, breathing_changes: str, tone_changes: str,
                 altered_responsiveness: str, episode_duration_under_1_min: str,
                 age_over_2_months: str, no_history_prematurity: str,
                 no_prior_brue: str, no_cpr_by_provider: str) -> Dict[str, Any]:
        """
        Calculates the BRUE classification using the provided parameters
        
        Args:
            age_under_1_year (str): Is infant <1 year old? (yes/no)
            asymptomatic_on_presentation (str): Asymptomatic on presentation? (yes/no)
            no_explanation_after_exam (str): No explanation after H&P? (yes/no)
            sudden_brief_resolved_episode (str): History of sudden, brief, resolved episode? (yes/no)
            cyanosis_or_pallor (str): Episode included cyanosis or pallor? (yes/no)
            breathing_changes (str): Episode included breathing changes? (yes/no)
            tone_changes (str): Episode included tone changes? (yes/no)
            altered_responsiveness (str): Episode included altered responsiveness? (yes/no)
            episode_duration_under_1_min (str): Episode duration <1 minute? (yes/no)
            age_over_2_months (str): Is infant >2 months old? (yes/no)
            no_history_prematurity (str): No history of prematurity? (yes/no)
            no_prior_brue (str): No prior BRUE events? (yes/no)
            no_cpr_by_provider (str): No need for CPR by provider? (yes/no)
            
        Returns:
            Dict with the result and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(
            age_under_1_year, asymptomatic_on_presentation, no_explanation_after_exam,
            sudden_brief_resolved_episode, cyanosis_or_pallor, breathing_changes,
            tone_changes, altered_responsiveness, episode_duration_under_1_min,
            age_over_2_months, no_history_prematurity, no_prior_brue, no_cpr_by_provider
        )
        
        # Calculate classification
        classification = self._calculate_classification(
            age_under_1_year, asymptomatic_on_presentation, no_explanation_after_exam,
            sudden_brief_resolved_episode, cyanosis_or_pallor, breathing_changes,
            tone_changes, altered_responsiveness, episode_duration_under_1_min,
            age_over_2_months, no_history_prematurity, no_prior_brue, no_cpr_by_provider
        )
        
        # Get interpretation
        interpretation = self._get_interpretation(classification)
        
        return {
            "result": classification,
            "unit": "",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"],
            "criteria_summary": self._get_criteria_summary(
                age_under_1_year, asymptomatic_on_presentation, no_explanation_after_exam,
                sudden_brief_resolved_episode, cyanosis_or_pallor, breathing_changes,
                tone_changes, altered_responsiveness, episode_duration_under_1_min,
                age_over_2_months, no_history_prematurity, no_prior_brue, no_cpr_by_provider
            )
        }
    
    def _validate_inputs(self, *args):
        """Validates all input parameters"""
        
        parameter_names = [
            'age_under_1_year', 'asymptomatic_on_presentation', 'no_explanation_after_exam',
            'sudden_brief_resolved_episode', 'cyanosis_or_pallor', 'breathing_changes',
            'tone_changes', 'altered_responsiveness', 'episode_duration_under_1_min',
            'age_over_2_months', 'no_history_prematurity', 'no_prior_brue', 'no_cpr_by_provider'
        ]
        
        for i, value in enumerate(args):
            if not isinstance(value, str):
                raise ValueError(f"{parameter_names[i]} must be a string")
            
            if value.lower() not in ['yes', 'no']:
                raise ValueError(f"{parameter_names[i]} must be 'yes' or 'no'")
    
    def _calculate_classification(self, age_under_1_year: str, asymptomatic_on_presentation: str,
                                no_explanation_after_exam: str, sudden_brief_resolved_episode: str,
                                cyanosis_or_pallor: str, breathing_changes: str, tone_changes: str,
                                altered_responsiveness: str, episode_duration_under_1_min: str,
                                age_over_2_months: str, no_history_prematurity: str,
                                no_prior_brue: str, no_cpr_by_provider: str) -> int:
        """Calculates the BRUE classification"""
        
        # Check entry criteria (ALL must be met)
        entry_criteria = [
            age_under_1_year.lower() == 'yes',
            asymptomatic_on_presentation.lower() == 'yes',
            no_explanation_after_exam.lower() == 'yes',
            sudden_brief_resolved_episode.lower() == 'yes'
        ]
        
        # Check qualifying event characteristics (at least ONE must be present)
        event_characteristics = [
            cyanosis_or_pallor.lower() == 'yes',
            breathing_changes.lower() == 'yes',
            tone_changes.lower() == 'yes',
            altered_responsiveness.lower() == 'yes'
        ]
        
        # Must meet all entry criteria AND at least one event characteristic
        if not all(entry_criteria) or not any(event_characteristics):
            return self.NOT_BRUE
        
        # Check lower-risk criteria (ALL must be met for lower risk)
        lower_risk_criteria = [
            episode_duration_under_1_min.lower() == 'yes',
            age_over_2_months.lower() == 'yes',
            no_history_prematurity.lower() == 'yes',
            no_prior_brue.lower() == 'yes',
            no_cpr_by_provider.lower() == 'yes'
        ]
        
        if all(lower_risk_criteria):
            return self.BRUE_LOWER_RISK
        else:
            return self.BRUE_HIGHER_RISK
    
    def _get_interpretation(self, classification: int) -> Dict[str, str]:
        """
        Determines the interpretation based on the classification
        
        Args:
            classification (int): BRUE classification result
            
        Returns:
            Dict with interpretation details
        """
        
        if classification == self.NOT_BRUE:
            return {
                "stage": "Not BRUE",
                "description": "Does not meet BRUE criteria",
                "interpretation": "The event does not meet the criteria for Brief Resolved Unexplained Event (BRUE). Consider alternative diagnoses and appropriate evaluation based on clinical presentation. Review entry criteria and event characteristics."
            }
        elif classification == self.BRUE_HIGHER_RISK:
            return {
                "stage": "BRUE - Higher Risk",
                "description": "Meets BRUE criteria but classified as higher risk",
                "interpretation": "Meets BRUE criteria but does not meet all lower-risk criteria. Consider further evaluation, monitoring, and potential hospitalization based on clinical judgment and shared decision-making with family. May require diagnostic testing and close observation."
            }
        else:  # BRUE_LOWER_RISK
            return {
                "stage": "BRUE - Lower Risk",
                "description": "Meets BRUE criteria and classified as lower risk",
                "interpretation": "Meets criteria for lower-risk BRUE. May be managed with observation, parental education, CPR training resources, and shared decision-making. Routine diagnostic testing (chest x-rays, blood gas, sleep studies, ECG, etc.) is NOT recommended. Assess social risk factors and provide family support."
            }
    
    def _get_criteria_summary(self, age_under_1_year: str, asymptomatic_on_presentation: str,
                            no_explanation_after_exam: str, sudden_brief_resolved_episode: str,
                            cyanosis_or_pallor: str, breathing_changes: str, tone_changes: str,
                            altered_responsiveness: str, episode_duration_under_1_min: str,
                            age_over_2_months: str, no_history_prematurity: str,
                            no_prior_brue: str, no_cpr_by_provider: str) -> Dict[str, Any]:
        """Provides a summary of which criteria were met"""
        
        return {
            "entry_criteria": {
                "age_under_1_year": age_under_1_year.lower() == 'yes',
                "asymptomatic_on_presentation": asymptomatic_on_presentation.lower() == 'yes',
                "no_explanation_after_exam": no_explanation_after_exam.lower() == 'yes',
                "sudden_brief_resolved_episode": sudden_brief_resolved_episode.lower() == 'yes'
            },
            "event_characteristics": {
                "cyanosis_or_pallor": cyanosis_or_pallor.lower() == 'yes',
                "breathing_changes": breathing_changes.lower() == 'yes',
                "tone_changes": tone_changes.lower() == 'yes',
                "altered_responsiveness": altered_responsiveness.lower() == 'yes'
            },
            "lower_risk_criteria": {
                "episode_duration_under_1_min": episode_duration_under_1_min.lower() == 'yes',
                "age_over_2_months": age_over_2_months.lower() == 'yes',
                "no_history_prematurity": no_history_prematurity.lower() == 'yes',
                "no_prior_brue": no_prior_brue.lower() == 'yes',
                "no_cpr_by_provider": no_cpr_by_provider.lower() == 'yes'
            }
        }


def calculate_brue(age_under_1_year: str, asymptomatic_on_presentation: str,
                  no_explanation_after_exam: str, sudden_brief_resolved_episode: str,
                  cyanosis_or_pallor: str, breathing_changes: str, tone_changes: str,
                  altered_responsiveness: str, episode_duration_under_1_min: str,
                  age_over_2_months: str, no_history_prematurity: str,
                  no_prior_brue: str, no_cpr_by_provider: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_brue pattern
    """
    calculator = BrueCalculator()
    return calculator.calculate(
        age_under_1_year, asymptomatic_on_presentation, no_explanation_after_exam,
        sudden_brief_resolved_episode, cyanosis_or_pallor, breathing_changes,
        tone_changes, altered_responsiveness, episode_duration_under_1_min,
        age_over_2_months, no_history_prematurity, no_prior_brue, no_cpr_by_provider
    )