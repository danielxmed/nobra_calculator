"""
INTERCHEST Clinical Prediction Rule for Chest Pain in Primary Care Calculator

Rules out coronary artery disease (CAD) in primary care patients 30 years and older 
presenting with chest pain. This clinical prediction rule identifies patients with 
very low likelihood of chest pain due to unstable CAD.

References (Vancouver style):
1. Aerts M, Minalu G, Bösner S, et al. Pooled individual patient data from five countries 
   were used to derive a multi-variable clinical prediction rule for the diagnosis of 
   coronary artery disease in primary care. J Clin Epidemiol. 2017 Jan;81:120-129. 
   doi: 10.1016/j.jclinepi.2016.09.011.
2. Bösner S, Haasenritter J, Becker A, et al. Ruling out coronary artery disease in 
   primary care: development and validation of a simple prediction rule. CMAJ. 2010 
   Sep 7;182(12):1295-300. doi: 10.1503/cmaj.100212.
3. Cayley WE Jr. Chest pain--tools to improve your in-office evaluation. J Fam Pract. 
   2014 May;63(5):246-51.
"""

from typing import Dict, Any


class InterchestRuleCalculator:
    """Calculator for INTERCHEST Clinical Prediction Rule"""
    
    def __init__(self):
        # INTERCHEST scoring weights
        self.scoring_weights = {
            "history_of_cad": {
                "no": 0,
                "yes": 1
            },
            "age_gender_risk": {
                "no": 0,
                "yes": 1
            },
            "effort_related_pain": {
                "no": 0,
                "yes": 1
            },
            "pain_reproducible_palpation": {
                "no": 0,
                "yes": -1  # Only negative predictor
            },
            "physician_suspected_serious": {
                "no": 0,
                "yes": 1
            },
            "pressure_sensation": {
                "no": 0,
                "yes": 1
            }
        }
    
    def calculate(self, history_of_cad: str, age_gender_risk: str, effort_related_pain: str,
                 pain_reproducible_palpation: str, physician_suspected_serious: str, 
                 pressure_sensation: str) -> Dict[str, Any]:
        """
        Calculates the INTERCHEST Clinical Prediction Rule score
        
        Args:
            history_of_cad (str): Previous history of CAD
            age_gender_risk (str): Female ≥65 years or male ≥55 years
            effort_related_pain (str): Chest pain related to physical effort
            pain_reproducible_palpation (str): Pain reproducible by palpation
            physician_suspected_serious (str): Physician initially suspected serious condition
            pressure_sensation (str): Chest discomfort feels like pressure
            
        Returns:
            Dict with the INTERCHEST score and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(
            history_of_cad, age_gender_risk, effort_related_pain,
            pain_reproducible_palpation, physician_suspected_serious, pressure_sensation
        )
        
        # Calculate total score
        score = self._calculate_total_score(
            history_of_cad, age_gender_risk, effort_related_pain,
            pain_reproducible_palpation, physician_suspected_serious, pressure_sensation
        )
        
        # Get interpretation
        interpretation = self._get_interpretation(score)
        
        return {
            "result": score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, history_of_cad: str, age_gender_risk: str, effort_related_pain: str,
                        pain_reproducible_palpation: str, physician_suspected_serious: str, 
                        pressure_sensation: str):
        """Validates input parameters"""
        
        # Define valid options for each parameter
        valid_options = ["no", "yes"]
        
        # Validate all parameters
        parameters = {
            "history_of_cad": history_of_cad,
            "age_gender_risk": age_gender_risk,
            "effort_related_pain": effort_related_pain,
            "pain_reproducible_palpation": pain_reproducible_palpation,
            "physician_suspected_serious": physician_suspected_serious,
            "pressure_sensation": pressure_sensation
        }
        
        for param_name, param_value in parameters.items():
            if param_value not in valid_options:
                raise ValueError(f"{param_name} must be 'no' or 'yes'")
    
    def _calculate_total_score(self, history_of_cad: str, age_gender_risk: str, effort_related_pain: str,
                              pain_reproducible_palpation: str, physician_suspected_serious: str, 
                              pressure_sensation: str) -> int:
        """
        Calculates the total INTERCHEST score
        
        INTERCHEST Scoring System:
        - History of CAD: +1 point if yes
        - Age/Gender risk (Female ≥65 or Male ≥55): +1 point if yes
        - Effort-related pain: +1 point if yes
        - Pain reproducible by palpation: -1 point if yes (only negative predictor)
        - Physician suspected serious condition: +1 point if yes
        - Pressure sensation: +1 point if yes
        
        Total score range: -1 to +5 points
        """
        
        total_score = 0
        
        # Add points for each parameter
        total_score += self.scoring_weights["history_of_cad"][history_of_cad]
        total_score += self.scoring_weights["age_gender_risk"][age_gender_risk]
        total_score += self.scoring_weights["effort_related_pain"][effort_related_pain]
        total_score += self.scoring_weights["pain_reproducible_palpation"][pain_reproducible_palpation]
        total_score += self.scoring_weights["physician_suspected_serious"][physician_suspected_serious]
        total_score += self.scoring_weights["pressure_sensation"][pressure_sensation]
        
        return total_score
    
    def _get_interpretation(self, score: int) -> Dict[str, str]:
        """
        Provides clinical interpretation based on INTERCHEST score
        
        Args:
            score (int): INTERCHEST score (-1 to +5)
            
        Returns:
            Dict with interpretation details
        """
        
        if score <= 1:
            return {
                "stage": "Low Risk",
                "description": f"Score {score} points (≤1 points)",
                "interpretation": "Very low likelihood of chest pain due to unstable CAD (2.1% probability, 98% NPV). Safe for discharge without urgent further evaluation. Consider routine outpatient follow-up if symptoms persist."
            }
        else:  # score >= 2
            return {
                "stage": "Higher Risk",
                "description": f"Score {score} points (2-5 points)",
                "interpretation": "Cannot rule out unstable CAD (43% probability). Requires further urgent evaluation with ECG, cardiac biomarkers, and consideration for stress testing or cardiology consultation."
            }


def calculate_interchest_rule(history_of_cad: str, age_gender_risk: str, effort_related_pain: str,
                             pain_reproducible_palpation: str, physician_suspected_serious: str, 
                             pressure_sensation: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = InterchestRuleCalculator()
    return calculator.calculate(
        history_of_cad, age_gender_risk, effort_related_pain,
        pain_reproducible_palpation, physician_suspected_serious, pressure_sensation
    )