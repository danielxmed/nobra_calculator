"""
Behavioral Pain Scale (BPS) Calculator

Quantifies pain in critically ill intubated patients who cannot self-report 
using three behavioral indicators.

References (Vancouver style):
1. Payen JF, Bru O, Bosson JL, Lagrasta A, Novel E, Deschaux I, et al. Assessing 
   pain in critically ill sedated patients by using a behavioral pain scale. 
   Crit Care Med. 2001 Dec;29(12):2258-63.
2. Ahlers SJ, van Gulik L, van der Veen AM, van Dongen HP, de Boer A, Tibboel D, et al. 
   Comparison of different pain scoring systems in critically ill patients in a general ICU. 
   Crit Care. 2008;12(1):R15.
3. Chanques G, Sebbane M, Barbotte E, Viel E, Eledjam JJ, Jaber S. A prospective 
   study of pain at rest: incidence and characteristics of an unrecognized symptom 
   in surgical and trauma versus medical intensive care unit patients. Anesthesiology. 
   2007 Nov;107(5):858-60.
"""

from typing import Dict, Any


class BehavioralPainScaleCalculator:
    """Calculator for Behavioral Pain Scale (BPS)"""
    
    def __init__(self):
        # Component descriptions
        self.facial_descriptions = {
            1: "Relaxed",
            2: "Partially tightened (e.g., brow lowering)",
            3: "Fully tightened (e.g., eyelid closing)",
            4: "Grimacing"
        }
        
        self.limb_descriptions = {
            1: "No movement",
            2: "Partially bent",
            3: "Fully bent with finger flexion",
            4: "Permanently retracted"
        }
        
        self.ventilation_descriptions = {
            1: "Tolerating movement",
            2: "Coughing but tolerating ventilation for most of the time",
            3: "Fighting ventilator",
            4: "Unable to control ventilation"
        }
        
        # Pain thresholds
        self.MILD_PAIN_THRESHOLD = 4
        self.UNACCEPTABLE_PAIN_THRESHOLD = 6
        self.MAXIMUM_PAIN_THRESHOLD = 12
    
    def calculate(self, facial_expression: int, upper_limb_movements: int, 
                  compliance_with_ventilation: int) -> Dict[str, Any]:
        """
        Calculates the BPS score
        
        Args:
            facial_expression (int): Facial expression score (1-4)
            upper_limb_movements (int): Upper limb movement score (1-4)
            compliance_with_ventilation (int): Ventilation compliance score (1-4)
            
        Returns:
            Dict with BPS score and clinical interpretation
        """
        
        # Validations
        self._validate_inputs(facial_expression, upper_limb_movements, compliance_with_ventilation)
        
        # Calculate total score
        bps_score = facial_expression + upper_limb_movements + compliance_with_ventilation
        
        # Get interpretation
        interpretation = self._get_interpretation(
            bps_score, facial_expression, upper_limb_movements, compliance_with_ventilation
        )
        
        return {
            "result": bps_score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, facial: int, limb: int, ventilation: int):
        """Validates input parameters"""
        
        if not isinstance(facial, int):
            raise ValueError("Facial expression must be an integer")
        if not isinstance(limb, int):
            raise ValueError("Upper limb movements must be an integer")
        if not isinstance(ventilation, int):
            raise ValueError("Compliance with ventilation must be an integer")
        
        if facial < 1 or facial > 4:
            raise ValueError("Facial expression must be between 1 and 4")
        if limb < 1 or limb > 4:
            raise ValueError("Upper limb movements must be between 1 and 4")
        if ventilation < 1 or ventilation > 4:
            raise ValueError("Compliance with ventilation must be between 1 and 4")
    
    def _get_interpretation(self, score: int, facial: int, limb: int, ventilation: int) -> Dict[str, str]:
        """
        Determines clinical interpretation based on BPS score
        
        Args:
            score (int): Total BPS score
            facial (int): Facial expression component score
            limb (int): Upper limb movement component score
            ventilation (int): Ventilation compliance component score
            
        Returns:
            Dict with clinical interpretation
        """
        
        # Generate component breakdown
        components = [
            f"Facial expression: {self.facial_descriptions[facial]} ({facial} points)",
            f"Upper limb movements: {self.limb_descriptions[limb]} ({limb} points)",
            f"Compliance with ventilation: {self.ventilation_descriptions[ventilation]} ({ventilation} points)"
        ]
        
        component_detail = ". ".join(components)
        
        if score == 3:
            return {
                "stage": "No Pain",
                "description": "No pain behaviors observed",
                "interpretation": (
                    f"BPS score: {score}/12 points. No pain behaviors observed in this critically ill "
                    f"intubated patient. {component_detail}. Clinical management: Continue current "
                    "management with routine monitoring. Patient appears comfortable with minimal "
                    "signs of distress. No analgesic intervention required at this time. Continue "
                    "to monitor for changes and reassess according to institutional protocol. "
                    "Maintain current sedation and ventilator settings as appropriate."
                )
            }
        
        elif score <= self.MILD_PAIN_THRESHOLD:  # score 4-5
            return {
                "stage": "Mild Pain",
                "description": "Mild pain behaviors present",
                "interpretation": (
                    f"BPS score: {score}/12 points. Mild pain behaviors present in this critically ill "
                    f"intubated patient. {component_detail}. Clinical management: Consider comfort "
                    "measures including repositioning, environmental modifications, and reassessment "
                    "in 15-30 minutes. May consider low-dose analgesics based on clinical context "
                    "and individual patient factors. Monitor for progression of pain behaviors. "
                    "Document interventions and response to treatment."
                )
            }
        
        elif score < self.MAXIMUM_PAIN_THRESHOLD:  # score 6-11
            return {
                "stage": "Unacceptable Pain",
                "description": "Unacceptable amount of pain requiring intervention",
                "interpretation": (
                    f"BPS score: {score}/12 points. Unacceptable amount of pain requiring intervention. "
                    f"{component_detail}. Clinical action required: Consider sedation and/or analgesia "
                    "according to institutional protocols. Appropriate interventions may include "
                    "opioid analgesics (morphine, fentanyl), sedatives (propofol, dexmedetomidine), "
                    "or combination therapy. Reassess BPS score 15-30 minutes after intervention. "
                    "Evaluate for underlying causes of pain such as positioning, invasive procedures, "
                    "or medical conditions. Consider multimodal pain management approach."
                )
            }
        
        else:  # score == 12
            return {
                "stage": "Maximum Pain",
                "description": "Maximum pain requiring immediate intervention",
                "interpretation": (
                    f"BPS score: {score}/12 points. Maximum pain behaviors requiring immediate intervention. "
                    f"{component_detail}. Emergency pain management required: Administer appropriate "
                    "analgesia and sedation immediately according to institutional protocols. Consider "
                    "bolus doses of opioid analgesics and sedatives. Implement multimodal pain management "
                    "approach including non-pharmacological interventions. Reassess frequently and "
                    "titrate medications to effect. Investigate underlying causes of severe pain "
                    "such as surgical complications, device malposition, or inadequate sedation. "
                    "Consider consultation with pain management or critical care specialists."
                )
            }


def calculate_behavioral_pain_scale(facial_expression: int, upper_limb_movements: int,
                                  compliance_with_ventilation: int) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = BehavioralPainScaleCalculator()
    return calculator.calculate(facial_expression, upper_limb_movements, compliance_with_ventilation)