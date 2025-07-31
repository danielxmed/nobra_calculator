"""
Glasgow Coma Scale (GCS) Calculator

The Glasgow Coma Scale is a clinical scale used to reliably measure a person's level 
of consciousness after a brain injury. It was developed by Graham Teasdale and Bryan 
Jennett in 1974 and has become the most widely used neurological assessment tool 
internationally. The scale assesses three aspects of responsiveness: eye opening, 
verbal response, and motor response.

References (Vancouver style):
1. Teasdale G, Jennett B. Assessment of coma and impaired consciousness. A practical scale. 
   Lancet. 1974;2(7872):81-84. doi: 10.1016/s0140-6736(74)91639-0.
2. Teasdale G, Maas A, Lecky F, Manley G, Stocchetti N, Murray G. The Glasgow Coma Scale 
   at 40 years: standing the test of time. Lancet Neurol. 2014;13(8):844-854. 
   doi: 10.1016/S1474-4422(14)70120-6.
3. Brennan PM, Murray GD, Teasdale GM. Simplifying the use of prognostic information in 
   traumatic brain injury. Part 1: The GCS-Pupils score: an extended index of clinical 
   severity. J Neurosurg. 2018;128(6):1612-1620. doi: 10.3171/2017.12.JNS172780.
"""

from typing import Dict, Any


class GlasgowComaScaleCalculator:
    """Calculator for Glasgow Coma Scale (GCS)"""
    
    def __init__(self):
        # Component descriptions for interpretation
        self.EYE_OPENING_DESCRIPTIONS = {
            4: "Spontaneous eye opening",
            3: "Eye opening to verbal command", 
            2: "Eye opening to pain",
            1: "No eye opening"
        }
        
        self.VERBAL_RESPONSE_DESCRIPTIONS = {
            5: "Oriented and conversing",
            4: "Confused conversation",
            3: "Inappropriate words", 
            2: "Incomprehensible sounds",
            1: "No verbal response"
        }
        
        self.MOTOR_RESPONSE_DESCRIPTIONS = {
            6: "Obeys commands",
            5: "Localizes to pain",
            4: "Normal flexion (withdrawal)",
            3: "Abnormal flexion (decorticate)",
            2: "Extension (decerebrate)",
            1: "No motor response"
        }
        
        # Severity thresholds
        self.SEVERE_THRESHOLD = 8  # GCS 3-8
        self.MODERATE_THRESHOLD = 12  # GCS 9-12
        # Mild is 13-15
    
    def calculate(self, eye_opening: int, verbal_response: int, motor_response: int) -> Dict[str, Any]:
        """
        Calculates Glasgow Coma Scale score using the three components
        
        Args:
            eye_opening (int): Eye opening response (1-4)
            verbal_response (int): Verbal response (1-5)  
            motor_response (int): Motor response (1-6)
            
        Returns:
            Dict with the total score and clinical interpretation
        """
        
        # Validate inputs
        self._validate_inputs(eye_opening, verbal_response, motor_response)
        
        # Calculate total score
        total_score = eye_opening + verbal_response + motor_response
        
        # Get interpretation
        interpretation = self._get_interpretation(total_score, eye_opening, verbal_response, motor_response)
        
        return {
            "result": total_score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, eye_opening: int, verbal_response: int, motor_response: int):
        """Validates input parameters"""
        
        if not isinstance(eye_opening, int) or eye_opening < 1 or eye_opening > 4:
            raise ValueError("Eye opening must be an integer between 1 and 4")
        
        if not isinstance(verbal_response, int) or verbal_response < 1 or verbal_response > 5:
            raise ValueError("Verbal response must be an integer between 1 and 5")
        
        if not isinstance(motor_response, int) or motor_response < 1 or motor_response > 6:
            raise ValueError("Motor response must be an integer between 1 and 6")
    
    def _get_interpretation(self, total_score: int, eye_opening: int, 
                          verbal_response: int, motor_response: int) -> Dict[str, str]:
        """
        Provides clinical interpretation based on the GCS score
        
        Args:
            total_score (int): Total GCS score
            eye_opening, verbal_response, motor_response (int): Individual component scores
            
        Returns:
            Dict with interpretation details
        """
        
        # Build component summary
        eye_desc = self.EYE_OPENING_DESCRIPTIONS[eye_opening]
        verbal_desc = self.VERBAL_RESPONSE_DESCRIPTIONS[verbal_response]
        motor_desc = self.MOTOR_RESPONSE_DESCRIPTIONS[motor_response]
        
        component_summary = (f"E{eye_opening} ({eye_desc}), "
                           f"V{verbal_response} ({verbal_desc}), "
                           f"M{motor_response} ({motor_desc})")
        
        # Determine severity level and recommendations
        if total_score <= self.SEVERE_THRESHOLD:
            return {
                "stage": "Severe Brain Injury",
                "description": "Comatose state",
                "interpretation": (
                    f"Glasgow Coma Scale: {total_score}/15 [{component_summary}]. "
                    f"Severe brain injury with significant impairment of consciousness. "
                    f"Patient is comatose and unable to follow commands. Requires immediate "
                    f"neurological assessment and intensive monitoring. Consider intubation "
                    f"for airway protection if GCS ≤8. Urgent neurosurgical consultation may "
                    f"be indicated. Monitor for signs of increased intracranial pressure. "
                    f"Serial GCS assessments essential to track neurological status."
                )
            }
        elif total_score <= self.MODERATE_THRESHOLD:
            return {
                "stage": "Moderate Brain Injury", 
                "description": "Stuporous to obtunded",
                "interpretation": (
                    f"Glasgow Coma Scale: {total_score}/15 [{component_summary}]. "
                    f"Moderate brain injury with altered level of consciousness. Patient "
                    f"may be drowsy or obtunded but can open eyes and localize painful stimuli. "
                    f"Close neurological monitoring required with frequent GCS assessments. "
                    f"Consider CT scan if not already performed. Monitor for neurological "
                    f"deterioration. May require admission to monitored setting. Assess need "
                    f"for neurosurgical consultation based on clinical context."
                )
            }
        else:  # GCS 13-15
            return {
                "stage": "Mild Brain Injury",
                "description": "Alert to mildly confused", 
                "interpretation": (
                    f"Glasgow Coma Scale: {total_score}/15 [{component_summary}]. "
                    f"Mild brain injury or normal consciousness. Patient is awake and can "
                    f"follow directions and communicate appropriately. May have mild confusion "
                    f"but maintains cognitive function. Continue routine neurological monitoring. "
                    f"Consider discharge planning if clinically stable and no other concerning "
                    f"features. Provide head injury precautions and return instructions. "
                    f"Follow-up as clinically indicated."
                )
            }


def calculate_glasgow_coma_scale(eye_opening: int, verbal_response: int, motor_response: int) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_glasgow_coma_scale pattern
    """
    calculator = GlasgowComaScaleCalculator()
    return calculator.calculate(eye_opening, verbal_response, motor_response)