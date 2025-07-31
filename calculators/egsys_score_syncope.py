"""
EGSYS (Evaluation of Guidelines in SYncope Study) Score for Syncope Calculator

Predicts likelihood that syncope is of cardiac cause to help emergency clinicians 
with screening and risk stratification in patients presenting with syncope.

References:
1. Del Rosso A, Ungar A, Maggi R, Giada F, Petix NR, De Santo T, et al. Clinical predictors 
   of cardiac syncope at initial evaluation in patients referred urgently to a general 
   hospital: the EGSYS score. Heart. 2008;94(12):1620-6. doi: 10.1136/hrt.2008.143123.
2. Kariman H, Harati S, Safari S, Baratloo A, Pishgahi M, Ardalani AR. Validation of EGSYS 
   Score in Prediction of Cardiogenic Syncope. Emerg Med Int. 2015;2015:515370. doi: 10.1155/2015/515370.
"""

from typing import Dict, Any


class EgsysScoreSyncopeCalculator:
    """Calculator for EGSYS (Evaluation of Guidelines in SYncope Study) Score for Syncope"""
    
    def __init__(self):
        # EGSYS scoring criteria and point values
        self.SCORING_CRITERIA = {
            'abnormal_ecg_heart_disease': {
                'description': 'Abnormal EKG and/or heart disease present',
                'points': {'yes': 3, 'no': 0}
            },
            'palpitations_before_syncope': {
                'description': 'Palpitations before syncope episode',
                'points': {'yes': 4, 'no': 0}
            },
            'syncope_during_effort': {
                'description': 'Syncope occurred during physical effort or exertion',
                'points': {'yes': 3, 'no': 0}
            },
            'syncope_supine_position': {
                'description': 'Syncope occurred while in supine (lying down) position',
                'points': {'yes': 2, 'no': 0}
            },
            'autonomic_prodromes': {
                'description': 'Autonomic prodromes present (nausea, vomiting, feeling warm/cold)',
                'points': {'yes': -1, 'no': 0}  # Negative points - reduces cardiac likelihood
            },
            'precipitating_factors': {
                'description': 'Predisposing or precipitating factors present (fear, pain, emotion, orthostasis)',
                'points': {'yes': -1, 'no': 0}  # Negative points - reduces cardiac likelihood
            }
        }
        
        # Risk thresholds and mortality data
        self.RISK_THRESHOLD = 3  # Score ≥3 indicates high risk for cardiac syncope
        self.MORTALITY_RATES = {
            'low_risk': 0.03,   # 3% 21-24 month mortality for score <3
            'high_risk': 0.17   # 17% 21-24 month mortality for score ≥3
        }
    
    def calculate(self, abnormal_ecg_heart_disease: str, palpitations_before_syncope: str,
                  syncope_during_effort: str, syncope_supine_position: str,
                  autonomic_prodromes: str, precipitating_factors: str) -> Dict[str, Any]:
        """
        Calculates the EGSYS score using the provided parameters
        
        Args:
            abnormal_ecg_heart_disease (str): Abnormal EKG and/or heart disease present ("yes" or "no")
            palpitations_before_syncope (str): Palpitations before syncope episode ("yes" or "no")
            syncope_during_effort (str): Syncope occurred during physical effort ("yes" or "no")
            syncope_supine_position (str): Syncope occurred while supine ("yes" or "no")
            autonomic_prodromes (str): Autonomic prodromes present ("yes" or "no")
            precipitating_factors (str): Precipitating factors present ("yes" or "no")
            
        Returns:
            Dict with the result and interpretation
        """
        
        # Map parameters for easier processing
        parameters = {
            'abnormal_ecg_heart_disease': abnormal_ecg_heart_disease,
            'palpitations_before_syncope': palpitations_before_syncope,
            'syncope_during_effort': syncope_during_effort,
            'syncope_supine_position': syncope_supine_position,
            'autonomic_prodromes': autonomic_prodromes,
            'precipitating_factors': precipitating_factors
        }
        
        # Validate inputs
        self._validate_inputs(parameters)
        
        # Calculate EGSYS score
        egsys_score, score_breakdown = self._calculate_egsys_score(parameters)
        
        # Get interpretation
        interpretation = self._get_interpretation(egsys_score, score_breakdown)
        
        return {
            "result": egsys_score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, parameters: Dict[str, Any]):
        """Validates input parameters"""
        
        for param_name, value in parameters.items():
            if not isinstance(value, str):
                raise ValueError(f"Parameter '{param_name}' must be a string")
            
            if value.lower() not in ['yes', 'no']:
                raise ValueError(f"Parameter '{param_name}' must be 'yes' or 'no', got '{value}'")
    
    def _calculate_egsys_score(self, parameters: Dict[str, Any]) -> tuple[int, Dict[str, int]]:
        """Calculates the EGSYS score with breakdown"""
        
        total_score = 0
        score_breakdown = {}
        
        for param_name, value in parameters.items():
            # Convert to lowercase for consistent processing
            value_lower = value.lower()
            
            # Get points for this parameter
            points = self.SCORING_CRITERIA[param_name]['points'][value_lower]
            total_score += points
            
            # Store breakdown for interpretation
            if points != 0:  # Only include parameters that contribute points
                score_breakdown[param_name] = points
        
        return total_score, score_breakdown
    
    def _get_interpretation(self, egsys_score: int, score_breakdown: Dict[str, int]) -> Dict[str, str]:
        """
        Determines the interpretation based on the EGSYS score
        
        Args:
            egsys_score (int): Calculated EGSYS score
            score_breakdown (Dict): Breakdown of contributing factors
            
        Returns:
            Dict with interpretation
        """
        
        # Determine risk category
        if egsys_score >= self.RISK_THRESHOLD:
            risk_category = {
                "stage": "High Risk",
                "description": "Cardiac syncope likely",
                "mortality_rate": self.MORTALITY_RATES['high_risk'],
                "base_text": ("Score ≥3 suggests cardiac syncope is likely with 95% sensitivity. "
                            "21-24 month mortality risk approximately 17%. Consider hospital admission "
                            "for diagnostic confirmation. Recommend cardiology consultation and further "
                            "cardiac evaluation including echocardiogram, telemetry monitoring, and "
                            "appropriate cardiac testing.")
            }
        else:
            risk_category = {
                "stage": "Low Risk", 
                "description": "Cardiac syncope less likely",
                "mortality_rate": self.MORTALITY_RATES['low_risk'],
                "base_text": ("Score <3 suggests cardiac syncope is less likely. 21-24 month mortality "
                            "risk approximately 3%. Continue standard syncope evaluation and consider "
                            "non-cardiac causes. Outpatient follow-up may be appropriate for stable "
                            "patients without high-risk features.")
            }
        
        # Add score breakdown context
        interpretation_text = risk_category["base_text"]
        
        if score_breakdown:
            contributing_factors = []
            for param_name, points in score_breakdown.items():
                factor_description = self.SCORING_CRITERIA[param_name]['description']
                sign = "+" if points > 0 else ""
                contributing_factors.append(f"{factor_description} ({sign}{points} points)")
            
            interpretation_text += (f" Contributing factors: {'; '.join(contributing_factors)}.")
        
        # Add clinical guidance
        if egsys_score >= self.RISK_THRESHOLD:
            interpretation_text += (" High-risk patients should receive priority cardiac evaluation, "
                                  "continuous cardiac monitoring, and consideration for inpatient management.")
        else:
            interpretation_text += (" Low-risk patients may be suitable for outpatient evaluation with "
                                  "appropriate follow-up and safety netting.")
        
        return {
            "stage": risk_category["stage"],
            "description": risk_category["description"],
            "interpretation": interpretation_text
        }


def calculate_egsys_score_syncope(abnormal_ecg_heart_disease: str, palpitations_before_syncope: str,
                                 syncope_during_effort: str, syncope_supine_position: str,
                                 autonomic_prodromes: str, precipitating_factors: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_egsys_score_syncope pattern
    """
    calculator = EgsysScoreSyncopeCalculator()
    return calculator.calculate(abnormal_ecg_heart_disease, palpitations_before_syncope,
                               syncope_during_effort, syncope_supine_position,
                               autonomic_prodromes, precipitating_factors)