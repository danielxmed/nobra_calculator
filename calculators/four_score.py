"""
FOUR (Full Outline of UnResponsiveness) Score Calculator

Grades severity of coma; may be more accurate than Glasgow Coma Scale. Evaluates 
consciousness level through four components: eye response, motor response, brainstem 
reflexes, and respiration pattern.

References:
1. Wijdicks EF, Bamlet WR, Maramattom BV, Manno EM, McClelland RL. Validation of a new 
   coma scale: The FOUR score. Ann Neurol. 2005;58(4):585-93.
2. Wolf CA, Wijdicks EF, Bamlet WR, McClelland RL. Further validation of the FOUR score 
   coma scale by intensive care unit nurses. Mayo Clin Proc. 2007;82(4):435-8.
3. Stead LG, Wijdicks EF, Bhagra A, et al. Validation of a new coma scale, the FOUR score, 
   in the emergency department. Neurocrit Care. 2009;10(1):50-4.
4. Kramer AA, Wijdicks EF, Snavely VL, et al. A multicenter prospective study of 
   interobserver agreement using the Full Outline of UnResponsiveness score coma scale 
   in the intensive care unit. Crit Care Med. 2012;40(9):2671-6.
"""

from typing import Dict, Any


class FourScoreCalculator:
    """Calculator for FOUR (Full Outline of UnResponsiveness) Score"""
    
    def __init__(self):
        # Component descriptions for interpretation
        self.EYE_RESPONSE_DESCRIPTIONS = {
            4: "Eyelids open, tracking, or blinking to command",
            3: "Eyelids open but not tracking",
            2: "Eyelids closed but open to loud voice",
            1: "Eyelids closed but open to pain",
            0: "Eyelids remain closed with pain"
        }
        
        self.MOTOR_RESPONSE_DESCRIPTIONS = {
            4: "Thumbs-up, fist, or peace sign",
            3: "Localizing to pain",
            2: "Flexion response to pain",
            1: "Extension response to pain",
            0: "No response to pain or generalized myoclonus"
        }
        
        self.BRAINSTEM_REFLEXES_DESCRIPTIONS = {
            4: "Pupil and corneal reflexes present",
            3: "One pupil wide and fixed",
            2: "Pupil OR corneal reflex absent",
            1: "Pupil AND corneal reflexes absent",
            0: "Absent pupil, corneal, and cough reflexes"
        }
        
        self.RESPIRATION_PATTERN_DESCRIPTIONS = {
            4: "Not intubated, regular breathing",
            3: "Not intubated, Cheyne-Stokes breathing",
            2: "Not intubated, irregular breathing",
            1: "Breathes above ventilatory rate",
            0: "Breathes at ventilator rate or apnea"
        }
    
    def calculate(self, eye_response: int, motor_response: int, 
                  brainstem_reflexes: int, respiration_pattern: int) -> Dict[str, Any]:
        """
        Calculates the FOUR Score
        
        Args:
            eye_response (int): Eye response component (0-4 points)
            motor_response (int): Motor response of upper extremities (0-4 points)
            brainstem_reflexes (int): Brainstem reflexes assessment (0-4 points)
            respiration_pattern (int): Respiration pattern assessment (0-4 points)
            
        Returns:
            Dict with the total FOUR score and clinical interpretation
        """
        
        # Validations
        self._validate_inputs(eye_response, motor_response, brainstem_reflexes, respiration_pattern)
        
        # Calculate total score
        total_score = self._calculate_total_score(eye_response, motor_response, 
                                                brainstem_reflexes, respiration_pattern)
        
        # Get interpretation
        interpretation_data = self._get_interpretation(total_score)
        
        return {
            "result": total_score,
            "unit": "points",
            "interpretation": interpretation_data["interpretation"],
            "stage": interpretation_data["stage"],
            "stage_description": interpretation_data["description"]
        }
    
    def _validate_inputs(self, eye_response: int, motor_response: int, 
                        brainstem_reflexes: int, respiration_pattern: int):
        """Validates input parameters"""
        
        # Validate each component is integer and within valid range (0-4)
        components = {
            "Eye response": eye_response,
            "Motor response": motor_response,
            "Brainstem reflexes": brainstem_reflexes,
            "Respiration pattern": respiration_pattern
        }
        
        for component_name, value in components.items():
            if not isinstance(value, int):
                raise ValueError(f"{component_name} must be an integer")
            
            if value < 0 or value > 4:
                raise ValueError(f"{component_name} must be between 0 and 4 points")
    
    def _calculate_total_score(self, eye_response: int, motor_response: int, 
                              brainstem_reflexes: int, respiration_pattern: int) -> int:
        """Calculates the total FOUR score by summing all components"""
        
        return eye_response + motor_response + brainstem_reflexes + respiration_pattern
    
    def _get_interpretation(self, total_score: int) -> Dict[str, str]:
        """
        Determines the interpretation based on the total score
        
        Args:
            total_score (int): Total FOUR score (0-16)
            
        Returns:
            Dict with interpretation details
        """
        
        if total_score <= 4:
            return {
                "stage": "Very Severe Coma",
                "description": "Very severe impairment of consciousness",
                "interpretation": (f"FOUR Score: {total_score}/16. Very severe coma with profound impairment of consciousness. "
                                f"Extensive brainstem dysfunction. Poor prognosis with high mortality risk. "
                                f"Requires intensive neurological monitoring and management.")
            }
        elif total_score <= 8:
            return {
                "stage": "Severe Coma",
                "description": "Severe impairment of consciousness",
                "interpretation": (f"FOUR Score: {total_score}/16. Severe coma with significant neurological impairment. "
                                f"Substantial brainstem dysfunction present. Guarded prognosis requiring intensive care "
                                f"and frequent neurological assessment.")
            }
        elif total_score <= 12:
            return {
                "stage": "Moderate Coma",
                "description": "Moderate impairment of consciousness",
                "interpretation": (f"FOUR Score: {total_score}/16. Moderate coma with variable neurological function. "
                                f"Some brainstem reflexes may be preserved. Prognosis depends on underlying etiology "
                                f"and response to treatment.")
            }
        else:  # total_score >= 13
            return {
                "stage": "Mild Impairment",
                "description": "Mild to minimal impairment of consciousness",
                "interpretation": (f"FOUR Score: {total_score}/16. Mild impairment of consciousness with relatively "
                                f"preserved neurological function. Better prognosis with potential for recovery. "
                                f"Continue supportive care and monitor for improvement.")
            }


def calculate_four_score(eye_response: int, motor_response: int, 
                        brainstem_reflexes: int, respiration_pattern: int) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_four_score pattern
    """
    calculator = FourScoreCalculator()
    return calculator.calculate(eye_response, motor_response, brainstem_reflexes, respiration_pattern)