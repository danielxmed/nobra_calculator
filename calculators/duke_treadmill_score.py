"""
Duke Treadmill Score Calculator

Diagnoses and prognoses suspected coronary artery disease (CAD) based on treadmill 
exercise test. Uses exercise time, ST deviation, and angina to predict prognosis 
and guide further treatment decisions.

References:
1. Mark DB, Shaw L, Harrell FE Jr, Hlatky MA, Lee KL, Bengtson JR, et al. 
   Prognostic value of a treadmill exercise score in outpatients with suspected 
   coronary artery disease. N Engl J Med. 1991;325(12):849-53.
2. Mark DB, Hlatky MA, Harrell FE Jr, Lee KL, Califf RM, Pryor DB. Exercise 
   treadmill score for predicting prognosis in coronary artery disease. 
   Ann Intern Med. 1987;106(6):793-800.
"""

from typing import Dict, Any


class DukeTreadmillScoreCalculator:
    """Calculator for Duke Treadmill Score"""
    
    def __init__(self):
        # Formula coefficients for Duke Treadmill Score
        self.ST_COEFFICIENT = 5  # Coefficient for ST deviation
        self.ANGINA_COEFFICIENT = 4  # Coefficient for angina index
    
    def calculate(self, exercise_time: float, st_deviation: float, angina_index: int) -> Dict[str, Any]:
        """
        Calculates the Duke Treadmill Score
        
        Args:
            exercise_time (float): Exercise time in minutes using standard Bruce protocol
            st_deviation (float): Maximum ST change (elevation or depression) in mm in any lead except aVR
            angina_index (int): Angina during exercise (0=none, 1=non-limiting, 2=exercise-limiting)
            
        Returns:
            Dict with the result and interpretation
        """
        
        # Validations
        self._validate_inputs(exercise_time, st_deviation, angina_index)
        
        # Calculate Duke Treadmill Score
        # Formula: DTS = Exercise time - (5 × ST deviation) - (4 × angina index)
        dts = exercise_time - (self.ST_COEFFICIENT * st_deviation) - (self.ANGINA_COEFFICIENT * angina_index)
        
        # Get interpretation
        interpretation = self._get_interpretation(dts)
        
        return {
            "result": round(dts, 1),
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, exercise_time: float, st_deviation: float, angina_index: int):
        """Validates input parameters"""
        
        # Validate exercise time
        if not isinstance(exercise_time, (int, float)):
            raise ValueError("Exercise time must be a number")
        
        if exercise_time < 0 or exercise_time > 30:
            raise ValueError("Exercise time must be between 0 and 30 minutes")
        
        # Validate ST deviation
        if not isinstance(st_deviation, (int, float)):
            raise ValueError("ST deviation must be a number")
        
        if st_deviation < -10 or st_deviation > 10:
            raise ValueError("ST deviation must be between -10 and 10 mm")
        
        # Validate angina index
        if not isinstance(angina_index, int):
            raise ValueError("Angina index must be an integer")
        
        if angina_index not in [0, 1, 2]:
            raise ValueError("Angina index must be 0 (none), 1 (non-limiting), or 2 (exercise-limiting)")
    
    def _get_interpretation(self, dts: float) -> Dict[str, str]:
        """
        Determines the interpretation based on the Duke Treadmill Score
        
        Args:
            dts (float): Calculated Duke Treadmill Score
            
        Returns:
            Dict with interpretation
        """
        
        if dts < -11:
            return {
                "stage": "High Risk",
                "description": "High risk for coronary artery disease",
                "interpretation": f"High risk for coronary artery disease (DTS = {dts:.1f}) with 5-year survival of 65%. Strong indication for coronary angiography. 74% of patients have 3-vessel or left main coronary disease. Consider cardiology consultation and invasive evaluation."
            }
        elif dts <= 4:
            return {
                "stage": "Intermediate Risk",
                "description": "Intermediate risk for coronary artery disease",
                "interpretation": f"Intermediate risk for coronary artery disease (DTS = {dts:.1f}) with 5-year survival of 90%. Consider further non-invasive testing (stress imaging, coronary CT angiography) or cardiology consultation based on clinical context and risk factors."
            }
        else:  # dts >= 5
            return {
                "stage": "Low Risk",
                "description": "Low risk for coronary artery disease",
                "interpretation": f"Low risk for coronary artery disease (DTS = {dts:.1f}) with 5-year survival of 97%. Most patients have no coronary disease or single-vessel disease. Conservative management appropriate with medical therapy and risk factor modification."
            }


def calculate_duke_treadmill_score(exercise_time: float, st_deviation: float, angina_index: int) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_duke_treadmill_score pattern
    """
    calculator = DukeTreadmillScoreCalculator()
    return calculator.calculate(exercise_time, st_deviation, angina_index)