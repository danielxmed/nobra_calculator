"""
Behavioral Observational Pain Scale (BOPS) Calculator

Quantifies post-operative pain for children aged 1-7 years using observational 
behavioral indicators.

References (Vancouver style):
1. Hesselgard K, Larsson S, Romner B, Strömblad LG, Reinstrup P. Validity and 
   reliability of the Behavioural Observational Pain Scale for postoperative pain 
   measurement in children 1-7 years of age. Pediatr Crit Care Med. 2007 Mar;8(2):102-8.
2. von Baeyer CL, Spagrud LJ. Systematic review of observational (behavioral) 
   measures of pain for children and adolescents aged 3 to 18 years. Pain. 2007 Jan;127(1-2):140-50.
3. Duhn LJ, Medves JM. A systematic integrative review of infant pain assessment 
   tools. Adv Neonatal Care. 2004 Jun;4(3):126-40.
"""

from typing import Dict, Any


class BehavioralObservationalPainScaleCalculator:
    """Calculator for Behavioral Observational Pain Scale (BOPS)"""
    
    def __init__(self):
        # Component descriptions
        self.facial_descriptions = {
            0: "Neutral/positive facial expression, composed, calm",
            1: "Negative facial expression, concerned",
            2: "Negative facial expression, grimace, distorted face"
        }
        
        self.verbalization_descriptions = {
            0: "Normal conversation, laugh, crow",
            1: "Completely quiet, sobbing and/or complaining but not because of pain",
            2: "Crying, screaming and/or complaining about pain"
        }
        
        self.position_descriptions = {
            0: "Inactive, laying, relaxed with all extremities or sitting, walking",
            1: "Restless movements, shifting fashion and/or touching wound or wound area",
            2: "Lying rigid and/or drawn up with arms and legs to the body"
        }
        
        # Pain threshold for analgesia consideration
        self.ANALGESIA_THRESHOLD = 3
    
    def calculate(self, facial_expression: int, verbalization: int, body_position: int) -> Dict[str, Any]:
        """
        Calculates the BOPS score
        
        Args:
            facial_expression (int): Facial expression score (0-2)
            verbalization (int): Verbalization score (0-2)
            body_position (int): Body position score (0-2)
            
        Returns:
            Dict with BOPS score and clinical interpretation
        """
        
        # Validations
        self._validate_inputs(facial_expression, verbalization, body_position)
        
        # Calculate total score
        bops_score = facial_expression + verbalization + body_position
        
        # Get interpretation
        interpretation = self._get_interpretation(
            bops_score, facial_expression, verbalization, body_position
        )
        
        return {
            "result": bops_score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, facial_expression: int, verbalization: int, body_position: int):
        """Validates input parameters"""
        
        if not isinstance(facial_expression, int):
            raise ValueError("Facial expression must be an integer")
        if not isinstance(verbalization, int):
            raise ValueError("Verbalization must be an integer")
        if not isinstance(body_position, int):
            raise ValueError("Body position must be an integer")
        
        if facial_expression < 0 or facial_expression > 2:
            raise ValueError("Facial expression must be between 0 and 2")
        if verbalization < 0 or verbalization > 2:
            raise ValueError("Verbalization must be between 0 and 2")
        if body_position < 0 or body_position > 2:
            raise ValueError("Body position must be between 0 and 2")
    
    def _get_interpretation(self, score: int, facial: int, verbal: int, position: int) -> Dict[str, str]:
        """
        Determines clinical interpretation based on BOPS score
        
        Args:
            score (int): Total BOPS score
            facial (int): Facial expression component score
            verbal (int): Verbalization component score  
            position (int): Body position component score
            
        Returns:
            Dict with clinical interpretation
        """
        
        # Generate component breakdown
        components = []
        if facial > 0:
            components.append(f"Facial expression: {self.facial_descriptions[facial]} ({facial} points)")
        if verbal > 0:
            components.append(f"Verbalization: {self.verbalization_descriptions[verbal]} ({verbal} points)")
        if position > 0:
            components.append(f"Body position: {self.position_descriptions[position]} ({position} points)")
        
        component_detail = ". ".join(components) if components else "All behavioral indicators within normal limits"
        
        if score < self.ANALGESIA_THRESHOLD:
            return {
                "stage": "Minimal Pain",
                "description": "Little to no pain behaviors observed",
                "interpretation": (
                    f"BOPS score: {score}/6 points. Minimal pain behaviors observed in this child aged 1-7 years. "
                    f"{component_detail}. Clinical management: Continue routine monitoring and comfort measures. "
                    "Consider non-pharmacological comfort interventions such as optimal positioning, "
                    "parental presence and comfort, distraction techniques, or environmental modifications. "
                    "Reassess pain regularly every 3 hours or as clinically indicated. "
                    "No immediate analgesic intervention required at this level, but maintain vigilance for changes."
                )
            }
        
        else:  # score >= 3
            return {
                "stage": "Significant Pain",
                "description": "Pain behaviors present, analgesia recommended",
                "interpretation": (
                    f"BOPS score: {score}/6 points. Significant pain behaviors observed requiring intervention. "
                    f"{component_detail}. Clinical action required: Consider analgesia administration according "
                    "to institutional protocols and physician orders. Appropriate analgesics may include "
                    "acetaminophen, ibuprofen, or opioids depending on pain severity and clinical context. "
                    "Reassess pain score 15-20 minutes after IV analgesics or 30-45 minutes after oral/rectal "
                    "analgesics to evaluate effectiveness. Implement comfort measures including positioning, "
                    "parental involvement, and environmental modifications. Document response to interventions "
                    "and continue regular pain assessments every 3 hours."
                )
            }


def calculate_behavioral_observational_pain_scale(facial_expression: int, verbalization: int, 
                                                body_position: int) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = BehavioralObservationalPainScaleCalculator()
    return calculator.calculate(facial_expression, verbalization, body_position)