"""
El-Ganzouri Risk Index (EGRI) for Difficult Airway Calculator

Predicts risk of difficult airway using seven clinical parameters to guide 
anesthesia management and intubation strategy planning.

References:
1. El-Ganzouri AR, McCarthy RJ, Tuman KJ, Tanck EN, Ivankovich AD. Preoperative airway 
   assessment: predictive value of a multivariate risk index. Anesth Analg. 1996;82(6):1197-204. 
   doi: 10.1097/00000539-199606000-00017.
2. Cortellazzi P, Caldiroli D, Byrne A, Sommariva A, Orena EF, Tramacere I. Defining and 
   developing expertise in tracheal intubation using a GlideScope for anaesthetists with 
   expertise in Macintosh direct laryngoscopy: an in-vivo longitudinal study. Anaesthesia. 
   2015;70(3):290-5. doi: 10.1111/anae.12878.
"""

from typing import Dict, Any


class ElGanzouriRiskIndexDifficultAirwayCalculator:
    """Calculator for El-Ganzouri Risk Index (EGRI) for Difficult Airway"""
    
    def __init__(self):
        # EGRI scoring criteria and point values
        self.SCORING_CRITERIA = {
            'mouth_opening': {
                'description': 'Inter-incisor mouth opening distance',
                'points': {'≥4 cm': 0, '<4 cm': 1}
            },
            'thyromental_distance': {
                'description': 'Thyromental distance (thyroid notch to tip of mandible)',
                'points': {'>6.5 cm': 0, '6.0-6.5 cm': 1, '<6.0 cm': 2}
            },
            'mallampati_class': {
                'description': 'Modified Mallampati Classification',
                'points': {'Class I': 0, 'Class II': 1, 'Class III': 2, 'Class IV': 2}
            },
            'neck_movement': {
                'description': 'Neck extension/flexion movement range',
                'points': {'>90°': 0, '80-90°': 1, '<80°': 2}
            },
            'ability_to_prognath': {
                'description': 'Ability to advance lower jaw beyond upper teeth',
                'points': {'Yes': 0, 'No': 1}
            },
            'weight': {
                'description': 'Patient body weight category',
                'points': {'<90 kg': 0, '90-110 kg': 1, '>110 kg': 2}
            },
            'history_difficult_intubation': {
                'description': 'Previous history of difficult intubation',
                'points': {'None': 0, 'Questionable': 1, 'Definite': 2}
            }
        }
        
        # Risk threshold for difficult airway
        self.DIFFICULT_AIRWAY_THRESHOLD = 4  # Score ≥4 indicates high risk
    
    def calculate(self, mouth_opening: str, thyromental_distance: str, mallampati_class: str,
                  neck_movement: str, ability_to_prognath: str, weight: str,
                  history_difficult_intubation: str) -> Dict[str, Any]:
        """
        Calculates the EGRI score using the provided parameters
        
        Args:
            mouth_opening (str): Inter-incisor mouth opening distance ("≥4 cm" or "<4 cm")
            thyromental_distance (str): Thyromental distance (">6.5 cm", "6.0-6.5 cm", or "<6.0 cm")
            mallampati_class (str): Modified Mallampati Classification ("Class I", "Class II", "Class III", or "Class IV")
            neck_movement (str): Neck extension/flexion range (">90°", "80-90°", or "<80°")
            ability_to_prognath (str): Ability to advance lower jaw ("Yes" or "No")
            weight (str): Patient body weight category ("<90 kg", "90-110 kg", or ">110 kg")
            history_difficult_intubation (str): Previous difficult intubation history ("None", "Questionable", or "Definite")
            
        Returns:
            Dict with the result and interpretation
        """
        
        # Map parameters for easier processing
        parameters = {
            'mouth_opening': mouth_opening,
            'thyromental_distance': thyromental_distance,
            'mallampati_class': mallampati_class,
            'neck_movement': neck_movement,
            'ability_to_prognath': ability_to_prognath,
            'weight': weight,
            'history_difficult_intubation': history_difficult_intubation
        }
        
        # Validate inputs
        self._validate_inputs(parameters)
        
        # Calculate EGRI score
        egri_score, score_breakdown = self._calculate_egri_score(parameters)
        
        # Get interpretation
        interpretation = self._get_interpretation(egri_score, score_breakdown)
        
        return {
            "result": egri_score,
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
            
            # Check if value is in valid options for this parameter
            valid_options = list(self.SCORING_CRITERIA[param_name]['points'].keys())
            if value not in valid_options:
                raise ValueError(f"Parameter '{param_name}' must be one of {valid_options}, got '{value}'")
    
    def _calculate_egri_score(self, parameters: Dict[str, Any]) -> tuple[int, Dict[str, int]]:
        """Calculates the EGRI score with breakdown"""
        
        total_score = 0
        score_breakdown = {}
        
        for param_name, value in parameters.items():
            # Get points for this parameter
            points = self.SCORING_CRITERIA[param_name]['points'][value]
            total_score += points
            
            # Store breakdown for interpretation
            if points > 0:  # Only include parameters that contribute points
                score_breakdown[param_name] = points
        
        return total_score, score_breakdown
    
    def _get_interpretation(self, egri_score: int, score_breakdown: Dict[str, int]) -> Dict[str, str]:
        """
        Determines the interpretation based on the EGRI score
        
        Args:
            egri_score (int): Calculated EGRI score
            score_breakdown (Dict): Breakdown of contributing factors
            
        Returns:
            Dict with interpretation
        """
        
        # Determine risk category
        if egri_score >= self.DIFFICULT_AIRWAY_THRESHOLD:
            risk_category = {
                "stage": "High Risk",
                "description": "High risk of difficult airway",
                "base_text": ("High risk of difficult airway (93.8% specificity). Consider precautions such as "
                            "video-assisted laryngoscopy, awake intubation, or fiberoptic intubation. Ensure "
                            "experienced anesthesiologist, difficult airway equipment available, and backup "
                            "plans prepared. Consider regional anesthesia if appropriate for the procedure.")
            }
        else:
            risk_category = {
                "stage": "Low Risk",
                "description": "Low risk of difficult airway",
                "base_text": ("Low risk of difficult airway. Conventional laryngoscopy and standard intubation "
                            "techniques are likely to be successful. Routine airway management protocol can "
                            "be followed with standard preparation and equipment readily available.")
            }
        
        # Add score breakdown context
        interpretation_text = risk_category["base_text"]
        
        if score_breakdown:
            contributing_factors = []
            for param_name, points in score_breakdown.items():
                factor_description = self.SCORING_CRITERIA[param_name]['description']
                contributing_factors.append(f"{factor_description} (+{points} points)")
            
            interpretation_text += (f" Contributing risk factors: {'; '.join(contributing_factors)}.")
        
        # Add specific management recommendations based on score
        if egri_score >= 7:
            interpretation_text += (" Very high risk (score ≥7): Strong consideration for awake "
                                  "fiberoptic intubation or alternative airway management techniques.")
        elif egri_score >= 4:
            interpretation_text += (" Moderate-high risk: Video laryngoscopy recommended as first-line "
                                  "approach with fiberoptic backup readily available.")
        
        # Add general safety recommendations
        interpretation_text += (" Always have backup airway plan and appropriate equipment available. "
                              "Consider consultation with senior anesthesiologist for high-risk cases.")
        
        return {
            "stage": risk_category["stage"],
            "description": risk_category["description"],
            "interpretation": interpretation_text
        }


def calculate_el_ganzouri_risk_index_difficult_airway(mouth_opening: str, thyromental_distance: str,
                                                     mallampati_class: str, neck_movement: str,
                                                     ability_to_prognath: str, weight: str,
                                                     history_difficult_intubation: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_el_ganzouri_risk_index_difficult_airway pattern
    """
    calculator = ElGanzouriRiskIndexDifficultAirwayCalculator()
    return calculator.calculate(mouth_opening, thyromental_distance, mallampati_class,
                               neck_movement, ability_to_prognath, weight, history_difficult_intubation)