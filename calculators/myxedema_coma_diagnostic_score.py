"""
Myxedema Coma Diagnostic Score Calculator

Diagnostic scoring system for myxedema coma (MC), a rare but life-threatening 
decompensated state of extreme hypothyroidism with high mortality if untreated.

References:
1. Popoveniuc G, Chandra T, Sud A, Sharma M, Blackman MR, Burman KD, et al. 
   A diagnostic scoring system for myxedema coma. Endocr Pract. 2014;20(8):808-17. 
   doi: 10.4158/EP13460.OR.
2. Mathew V, Misgar RA, Ghosh S, Mukhopadhyay P, Roychowdhury P, Pandit K, et al. 
   Myxedema coma: a new look into an old crisis. J Thyroid Res. 2011;2011:493462. 
   doi: 10.4061/2011/493462.
"""

from typing import Dict, Any


class MyxedemaComatDiagnosticScoreCalculator:
    """Calculator for Myxedema Coma Diagnostic Score"""
    
    def __init__(self):
        # Scoring criteria based on Popoveniuc et al. system
        self.TEMPERATURE_SCORES = {
            "normal_37": 0,
            "mild_hypothermia_35_37": 10,
            "moderate_hypothermia_32_35": 15,
            "severe_hypothermia_below_32": 20
        }
        
        self.CNS_SCORES = {
            "normal": 0,
            "mild_lethargy": 10,
            "moderate_somnolence": 20,
            "stupor_semicoma": 25,
            "coma": 30
        }
        
        self.CARDIOVASCULAR_SCORES = {
            "normal": 0,
            "mild_bradycardia": 5,
            "moderate_bradycardia_hypotension": 10,
            "severe_shock": 15
        }
        
        self.GI_SCORES = {
            "normal": 0,
            "mild_constipation": 5,
            "moderate_distension": 10,
            "severe_ileus": 15
        }
        
        self.METABOLIC_SCORES = {
            "normal": 0,
            "mild_hyponatremia": 5,
            "moderate_hyponatremia": 10,
            "severe_hyponatremia_hypoglycemia": 15
        }
        
        self.PRECIPITATING_SCORES = {
            "none": 0,
            "minor_stress": 5,
            "moderate_stress": 10,
            "major_stress": 15
        }
        
        # Diagnostic thresholds
        self.UNLIKELY_THRESHOLD = 25
        self.AT_RISK_THRESHOLD = 45
        self.DIAGNOSTIC_THRESHOLD = 60
    
    def calculate(self, body_temperature: str, central_nervous_system: str,
                 cardiovascular_dysfunction: str, gastrointestinal_dysfunction: str,
                 metabolic_dysfunction: str, precipitating_event: str) -> Dict[str, Any]:
        """
        Calculates the Myxedema Coma Diagnostic Score
        
        Args:
            body_temperature (str): Core body temperature category
            central_nervous_system (str): CNS manifestation severity
            cardiovascular_dysfunction (str): Cardiovascular dysfunction severity
            gastrointestinal_dysfunction (str): GI dysfunction severity
            metabolic_dysfunction (str): Metabolic dysfunction severity
            precipitating_event (str): Presence and severity of precipitating events
            
        Returns:
            Dict with the diagnostic score and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(body_temperature, central_nervous_system, cardiovascular_dysfunction,
                            gastrointestinal_dysfunction, metabolic_dysfunction, precipitating_event)
        
        # Calculate component scores
        score_components = self._calculate_component_scores(
            body_temperature, central_nervous_system, cardiovascular_dysfunction,
            gastrointestinal_dysfunction, metabolic_dysfunction, precipitating_event
        )
        
        # Calculate total score
        total_score = sum(score_components.values())
        
        # Get interpretation
        interpretation = self._get_interpretation(total_score)
        
        return {
            "result": total_score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, body_temperature: str, central_nervous_system: str,
                        cardiovascular_dysfunction: str, gastrointestinal_dysfunction: str,
                        metabolic_dysfunction: str, precipitating_event: str):
        """Validates input parameters"""
        
        valid_temperature_values = list(self.TEMPERATURE_SCORES.keys())
        if body_temperature not in valid_temperature_values:
            raise ValueError(f"Body temperature must be one of: {valid_temperature_values}")
        
        valid_cns_values = list(self.CNS_SCORES.keys())
        if central_nervous_system not in valid_cns_values:
            raise ValueError(f"Central nervous system must be one of: {valid_cns_values}")
        
        valid_cv_values = list(self.CARDIOVASCULAR_SCORES.keys())
        if cardiovascular_dysfunction not in valid_cv_values:
            raise ValueError(f"Cardiovascular dysfunction must be one of: {valid_cv_values}")
        
        valid_gi_values = list(self.GI_SCORES.keys())
        if gastrointestinal_dysfunction not in valid_gi_values:
            raise ValueError(f"Gastrointestinal dysfunction must be one of: {valid_gi_values}")
        
        valid_metabolic_values = list(self.METABOLIC_SCORES.keys())
        if metabolic_dysfunction not in valid_metabolic_values:
            raise ValueError(f"Metabolic dysfunction must be one of: {valid_metabolic_values}")
        
        valid_precipitating_values = list(self.PRECIPITATING_SCORES.keys())
        if precipitating_event not in valid_precipitating_values:
            raise ValueError(f"Precipitating event must be one of: {valid_precipitating_values}")
    
    def _calculate_component_scores(self, body_temperature: str, central_nervous_system: str,
                                  cardiovascular_dysfunction: str, gastrointestinal_dysfunction: str,
                                  metabolic_dysfunction: str, precipitating_event: str) -> Dict[str, int]:
        """Calculates individual component scores"""
        
        scores = {}
        
        scores["temperature"] = self.TEMPERATURE_SCORES[body_temperature]
        scores["cns"] = self.CNS_SCORES[central_nervous_system]
        scores["cardiovascular"] = self.CARDIOVASCULAR_SCORES[cardiovascular_dysfunction]
        scores["gastrointestinal"] = self.GI_SCORES[gastrointestinal_dysfunction]
        scores["metabolic"] = self.METABOLIC_SCORES[metabolic_dysfunction]
        scores["precipitating"] = self.PRECIPITATING_SCORES[precipitating_event]
        
        return scores
    
    def _get_interpretation(self, score: int) -> Dict[str, str]:
        """
        Determines the interpretation based on diagnostic score
        
        Args:
            score (int): Total diagnostic score
            
        Returns:
            Dict with interpretation details
        """
        
        if score < self.UNLIKELY_THRESHOLD:
            return {
                "stage": "Unlikely",
                "description": "Myxedema coma unlikely",
                "interpretation": f"MYXEDEMA COMA UNLIKELY (Score: {score}): Score <25 makes the diagnosis of "
                                "myxedema coma unlikely. EVALUATION: Consider alternative diagnoses for altered "
                                "mental status, hypothermia, or cardiovascular dysfunction. MONITORING: If clinical "
                                "suspicion remains, obtain thyroid function tests (TSH, free T4) and continue "
                                "supportive care. DIFFERENTIAL: Evaluate for sepsis, drug intoxication, metabolic "
                                "disorders, or other causes of altered consciousness. FOLLOW-UP: Reassess if "
                                "clinical condition changes or if thyroid dysfunction is confirmed."
            }
        elif score < self.AT_RISK_THRESHOLD:
            return {
                "stage": "Possible",
                "description": "Myxedema coma possible but unlikely",
                "interpretation": f"MYXEDEMA COMA POSSIBLE BUT UNLIKELY (Score: {score}): Low probability of "
                                "myxedema coma but cannot be excluded. EVALUATION: Continue evaluation for other "
                                "causes while considering thyroid function assessment. MONITORING: Obtain urgent "
                                "thyroid function tests (TSH, free T4) and monitor closely. MANAGEMENT: Provide "
                                "supportive care and address any precipitating factors. REASSESSMENT: Consider "
                                "repeat scoring if clinical condition deteriorates or new symptoms develop."
            }
        elif score < self.DIAGNOSTIC_THRESHOLD:
            return {
                "stage": "At Risk",
                "description": "Patient at risk for myxedema coma",
                "interpretation": f"PATIENT AT RISK FOR MYXEDEMA COMA (Score: {score}): Intermediate probability - "
                                "patient at significant risk for myxedema coma. EVALUATION: Urgent thyroid function "
                                "testing (TSH, free T4, free T3) and close monitoring required. MANAGEMENT: Consider "
                                "empirical thyroid hormone therapy if severe hypothyroidism suspected and clinical "
                                "deterioration evident. MONITORING: Intensive care monitoring recommended. Address "
                                "precipitating factors and provide aggressive supportive care. ESCALATION: Prepare "
                                "for potential progression to full myxedema coma."
            }
        else:  # score >= 60
            return {
                "stage": "Diagnostic",
                "description": "Highly suggestive of myxedema coma",
                "interpretation": f"HIGHLY SUGGESTIVE OF MYXEDEMA COMA (Score: {score}): High probability - "
                                "potentially diagnostic for myxedema coma. IMMEDIATE TREATMENT: Emergency "
                                "intervention required. Administer IV levothyroxine (200-400 mcg bolus, then "
                                "50-100 mcg daily) and IV liothyronine (T3) if available. SUPPORTIVE CARE: "
                                "Intensive care monitoring, mechanical ventilation if needed, vasopressor support "
                                "for shock, passive rewarming for hypothermia. MANAGEMENT: Treat precipitating "
                                "factors, provide stress-dose corticosteroids (hydrocortisone 100-300 mg every "
                                "8 hours), correct electrolyte abnormalities. PROGNOSIS: High mortality risk "
                                "requiring immediate aggressive treatment."
            }


def calculate_myxedema_coma_diagnostic_score(body_temperature: str, central_nervous_system: str,
                                           cardiovascular_dysfunction: str, gastrointestinal_dysfunction: str,
                                           metabolic_dysfunction: str, precipitating_event: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = MyxedemaComatDiagnosticScoreCalculator()
    return calculator.calculate(body_temperature, central_nervous_system, cardiovascular_dysfunction,
                               gastrointestinal_dysfunction, metabolic_dysfunction, precipitating_event)