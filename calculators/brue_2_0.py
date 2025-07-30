"""
Brief Resolved Unexplained Events 2.0 (BRUE 2.0) Criteria Calculator

Classifies unexplained events and improves on the original BRUE criteria by 
providing sophisticated risk prediction models for serious underlying conditions 
and event recurrence in infants <1 year old. Uses derived models to predict 
risk of serious diagnosis and recurrent events.

References:
- Tieder JS, et al. Brief resolved unexplained events (formerly apparent 
  life-threatening events) and evaluation of lower-risk infants. Pediatrics. 
  2016;137(5):e20160590.
- Merritt JL, et al. A framework for evaluation of the higher-risk infant 
  after a brief resolved unexplained event. Pediatrics. 2021;148(1):e2021050798.
"""

import math
from typing import Dict, Any


class Brue20Calculator:
    """Calculator for Brief Resolved Unexplained Events 2.0 (BRUE 2.0) Criteria"""
    
    def __init__(self):
        # Risk thresholds for classification
        self.VERY_LOW_RISK_THRESHOLD = 2
        self.LOW_RISK_THRESHOLD = 10
        self.MODERATE_RISK_THRESHOLD = 20
        
        # Model coefficients for serious condition risk
        self.SERIOUS_CONDITION_INTERCEPT = -2.9
        self.AGE_COEFFICIENT = -0.0046
        self.HISTORY_COEFFICIENT = 1.22
        self.ABNORMAL_HISTORY_COEFFICIENT = 0.35
        
        # Base recurrence risk factors (weights)
        self.RECURRENCE_BASE_RISK = 15.0  # Base percentage
        self.HISTORY_SIMILAR_WEIGHT = 25.0
        self.MULTIPLE_CLUSTERS_WEIGHT = 15.0
        self.PREMATURITY_WEIGHT = 10.0
        self.CYANOSIS_PALLOR_WEIGHT = 8.0
        self.BREATHING_CHANGES_WEIGHT = 6.0
        self.TONE_CHANGES_WEIGHT = 5.0
    
    def calculate(self, age_under_1_year: str, asymptomatic_on_presentation: str,
                 no_explanation_after_exam: str, sudden_brief_resolved_episode: str,
                 cyanosis_or_pallor: str, breathing_changes: str, tone_changes: str,
                 altered_responsiveness: str, age_in_days: int, history_similar_event: str,
                 abnormal_medical_history: str, multiple_event_clusters: str,
                 prematurity: str) -> Dict[str, Any]:
        """
        Calculates the BRUE 2.0 assessment using the provided parameters
        
        Args:
            age_under_1_year (str): Is infant <1 year old? (yes/no)
            asymptomatic_on_presentation (str): Asymptomatic on presentation? (yes/no)
            no_explanation_after_exam (str): No explanation after H&P? (yes/no)
            sudden_brief_resolved_episode (str): History of sudden, brief, resolved episode? (yes/no)
            cyanosis_or_pallor (str): Episode included cyanosis or pallor? (yes/no)
            breathing_changes (str): Episode included breathing changes? (yes/no)
            tone_changes (str): Episode included tone changes? (yes/no)
            altered_responsiveness (str): Episode included altered responsiveness? (yes/no)
            age_in_days (int): Age of infant in days
            history_similar_event (str): History of similar events? (yes/no)
            abnormal_medical_history (str): Abnormal medical history? (yes/no)
            multiple_event_clusters (str): Multiple event clusters? (yes/no)
            prematurity (str): History of prematurity? (yes/no)
            
        Returns:
            Dict with the result and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(
            age_under_1_year, asymptomatic_on_presentation, no_explanation_after_exam,
            sudden_brief_resolved_episode, cyanosis_or_pallor, breathing_changes,
            tone_changes, altered_responsiveness, history_similar_event,
            abnormal_medical_history, multiple_event_clusters, prematurity,
            age_in_days=age_in_days
        )
        
        # Check if meets BRUE criteria
        meets_brue = self._meets_brue_criteria(
            age_under_1_year, asymptomatic_on_presentation, no_explanation_after_exam,
            sudden_brief_resolved_episode, cyanosis_or_pallor, breathing_changes,
            tone_changes, altered_responsiveness
        )
        
        if not meets_brue:
            return self._not_brue_result()
        
        # Calculate risk predictions
        serious_condition_risk = self._calculate_serious_condition_risk(
            age_in_days, history_similar_event, abnormal_medical_history
        )
        
        recurrence_risk = self._calculate_recurrence_risk(
            history_similar_event, multiple_event_clusters, prematurity,
            cyanosis_or_pallor, breathing_changes, tone_changes
        )
        
        # Determine overall risk category
        overall_risk = max(serious_condition_risk, recurrence_risk)
        classification = self._get_risk_classification(overall_risk)
        
        # Get interpretation
        interpretation = self._get_interpretation(classification, serious_condition_risk, recurrence_risk)
        
        return {
            "result": classification,
            "unit": "",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"],
            "risk_predictions": {
                "serious_condition_risk": round(serious_condition_risk, 1),
                "recurrence_risk": round(recurrence_risk, 1),
                "overall_risk": round(overall_risk, 1)
            },
            "risk_factors": self._get_risk_factors_summary(
                age_in_days, history_similar_event, abnormal_medical_history,
                multiple_event_clusters, prematurity, cyanosis_or_pallor,
                breathing_changes, tone_changes
            )
        }
    
    def _validate_inputs(self, *string_args, age_in_days: int):
        """Validates all input parameters"""
        
        # Validate string parameters
        string_parameter_names = [
            'age_under_1_year', 'asymptomatic_on_presentation', 'no_explanation_after_exam',
            'sudden_brief_resolved_episode', 'cyanosis_or_pallor', 'breathing_changes',
            'tone_changes', 'altered_responsiveness', 'history_similar_event',
            'abnormal_medical_history', 'multiple_event_clusters', 'prematurity'
        ]
        
        for i, value in enumerate(string_args[:-1]):  # Exclude age_in_days
            if not isinstance(value, str):
                raise ValueError(f"{string_parameter_names[i]} must be a string")
            
            if value.lower() not in ['yes', 'no']:
                raise ValueError(f"{string_parameter_names[i]} must be 'yes' or 'no'")
        
        # Validate age_in_days
        if not isinstance(age_in_days, int):
            raise ValueError("age_in_days must be an integer")
        
        if age_in_days < 0 or age_in_days > 365:
            raise ValueError("age_in_days must be between 0 and 365")
    
    def _meets_brue_criteria(self, age_under_1_year: str, asymptomatic_on_presentation: str,
                           no_explanation_after_exam: str, sudden_brief_resolved_episode: str,
                           cyanosis_or_pallor: str, breathing_changes: str, tone_changes: str,
                           altered_responsiveness: str) -> bool:
        """Checks if the infant meets basic BRUE criteria"""
        
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
        
        return all(entry_criteria) and any(event_characteristics)
    
    def _calculate_serious_condition_risk(self, age_in_days: int, history_similar_event: str,
                                        abnormal_medical_history: str) -> float:
        """Calculates risk of serious underlying condition using the derived model"""
        
        # Convert yes/no to binary
        history_binary = 1 if history_similar_event.lower() == 'yes' else 0
        abnormal_history_binary = 1 if abnormal_medical_history.lower() == 'yes' else 0
        
        # Calculate x value for logistic regression
        x = (self.SERIOUS_CONDITION_INTERCEPT + 
             self.AGE_COEFFICIENT * age_in_days + 
             self.HISTORY_COEFFICIENT * history_binary + 
             self.ABNORMAL_HISTORY_COEFFICIENT * abnormal_history_binary)
        
        # Apply logistic function and convert to percentage
        risk_probability = math.exp(x) / (1 + math.exp(x))
        return risk_probability * 100
    
    def _calculate_recurrence_risk(self, history_similar_event: str, multiple_event_clusters: str,
                                 prematurity: str, cyanosis_or_pallor: str, breathing_changes: str,
                                 tone_changes: str) -> float:
        """Calculates risk of event recurrence using weighted factors"""
        
        risk_score = self.RECURRENCE_BASE_RISK
        
        if history_similar_event.lower() == 'yes':
            risk_score += self.HISTORY_SIMILAR_WEIGHT
        
        if multiple_event_clusters.lower() == 'yes':
            risk_score += self.MULTIPLE_CLUSTERS_WEIGHT
        
        if prematurity.lower() == 'yes':
            risk_score += self.PREMATURITY_WEIGHT
        
        if cyanosis_or_pallor.lower() == 'yes':
            risk_score += self.CYANOSIS_PALLOR_WEIGHT
        
        if breathing_changes.lower() == 'yes':
            risk_score += self.BREATHING_CHANGES_WEIGHT
        
        if tone_changes.lower() == 'yes':
            risk_score += self.TONE_CHANGES_WEIGHT
        
        # Cap at 100%
        return min(risk_score, 100.0)
    
    def _get_risk_classification(self, overall_risk: float) -> int:
        """Determines risk classification based on overall risk percentage"""
        
        if overall_risk < self.VERY_LOW_RISK_THRESHOLD:
            return 1  # Very Low Risk
        elif overall_risk < self.LOW_RISK_THRESHOLD:
            return 6  # Low Risk
        elif overall_risk < self.MODERATE_RISK_THRESHOLD:
            return 16  # Moderate Risk
        else:
            return 31  # High Risk
    
    def _get_interpretation(self, classification: int, serious_condition_risk: float,
                          recurrence_risk: float) -> Dict[str, str]:
        """Determines the interpretation based on the risk classification"""
        
        if classification == 1:  # Very Low Risk
            return {
                "stage": "Very Low Risk",
                "description": "BRUE with very low risk for serious condition or recurrence",
                "interpretation": f"Meets BRUE criteria with very low risk ({serious_condition_risk:.1f}% for serious condition, {recurrence_risk:.1f}% recurrence). Appropriate for home management with family education, CPR training, and routine follow-up. Routine diagnostic testing not recommended."
            }
        elif classification == 6:  # Low Risk
            return {
                "stage": "Low Risk",
                "description": "BRUE with low risk for serious condition or recurrence",
                "interpretation": f"Meets BRUE criteria with low risk ({serious_condition_risk:.1f}% for serious condition, {recurrence_risk:.1f}% recurrence). Consider brief observation, family education, and shared decision-making about diagnostic testing. Close follow-up recommended."
            }
        elif classification == 16:  # Moderate Risk
            return {
                "stage": "Moderate Risk",
                "description": "BRUE with moderate risk for serious condition or recurrence",
                "interpretation": f"Meets BRUE criteria with moderate risk ({serious_condition_risk:.1f}% for serious condition, {recurrence_risk:.1f}% recurrence). Consider extended monitoring, selective diagnostic testing based on clinical judgment, and close follow-up. Hospitalization may be indicated."
            }
        else:  # High Risk
            return {
                "stage": "High Risk",
                "description": "BRUE with high risk for serious condition or recurrence",
                "interpretation": f"Meets BRUE criteria with high risk ({serious_condition_risk:.1f}% for serious condition, {recurrence_risk:.1f}% recurrence). Requires comprehensive evaluation, strong consideration for hospitalization, and extensive diagnostic workup. Close monitoring essential."
            }
    
    def _not_brue_result(self) -> Dict[str, Any]:
        """Returns result for cases that don't meet BRUE criteria"""
        
        return {
            "result": 0,
            "unit": "",
            "interpretation": "The event does not meet the criteria for Brief Resolved Unexplained Event (BRUE). Consider alternative diagnoses and appropriate evaluation based on clinical presentation. Review entry criteria and event characteristics.",
            "stage": "Not BRUE",
            "stage_description": "Does not meet BRUE criteria",
            "risk_predictions": {
                "serious_condition_risk": 0.0,
                "recurrence_risk": 0.0,
                "overall_risk": 0.0
            },
            "risk_factors": {}
        }
    
    def _get_risk_factors_summary(self, age_in_days: int, history_similar_event: str,
                                abnormal_medical_history: str, multiple_event_clusters: str,
                                prematurity: str, cyanosis_or_pallor: str, breathing_changes: str,
                                tone_changes: str) -> Dict[str, Any]:
        """Provides summary of risk factors present"""
        
        return {
            "age_in_days": age_in_days,
            "risk_factors_present": {
                "history_similar_event": history_similar_event.lower() == 'yes',
                "abnormal_medical_history": abnormal_medical_history.lower() == 'yes',
                "multiple_event_clusters": multiple_event_clusters.lower() == 'yes',
                "prematurity": prematurity.lower() == 'yes',
                "cyanosis_or_pallor": cyanosis_or_pallor.lower() == 'yes',
                "breathing_changes": breathing_changes.lower() == 'yes',
                "tone_changes": tone_changes.lower() == 'yes'
            }
        }


def calculate_brue_2_0(age_under_1_year: str, asymptomatic_on_presentation: str,
                      no_explanation_after_exam: str, sudden_brief_resolved_episode: str,
                      cyanosis_or_pallor: str, breathing_changes: str, tone_changes: str,
                      altered_responsiveness: str, age_in_days: int, history_similar_event: str,
                      abnormal_medical_history: str, multiple_event_clusters: str,
                      prematurity: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_brue_2_0 pattern
    """
    calculator = Brue20Calculator()
    return calculator.calculate(
        age_under_1_year, asymptomatic_on_presentation, no_explanation_after_exam,
        sudden_brief_resolved_episode, cyanosis_or_pallor, breathing_changes,
        tone_changes, altered_responsiveness, age_in_days, history_similar_event,
        abnormal_medical_history, multiple_event_clusters, prematurity
    )