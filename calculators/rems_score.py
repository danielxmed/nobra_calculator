"""
REMS Score (Rapid Emergency Medicine Score) Calculator

Emergency department mortality risk prediction using six physiological and 
demographic variables. Developed as an attenuated version of APACHE II for 
rapid calculation in emergency settings.

References (Vancouver style):
1. Olsson T, Terent A, Lind L. Rapid Emergency Medicine score: a new prognostic 
   tool for in-hospital mortality in nonsurgical emergency department patients. 
   J Intern Med. 2004;255(5):579-587. doi: 10.1111/j.1365-2796.2004.01321.x.
2. Goodacre S, Turner J, Nicholl J. Prediction of mortality among emergency medical 
   admissions. Emerg Med J. 2006;23(5):372-375. doi: 10.1136/emj.2005.028522.
3. Imhoff BF, Thompson NJ, Hastings MA, et al. Rapid Emergency Medicine Score (REMS) 
   in the trauma population: a retrospective study. BMJ Open. 2014;4(5):e004738. 
   doi: 10.1136/bmjopen-2013-004738.
"""

from typing import Dict, Any


class RemsScoreCalculator:
    """Calculator for REMS (Rapid Emergency Medicine Score)"""
    
    def __init__(self):
        # Age scoring thresholds
        self.AGE_THRESHOLDS = [
            (45, 0),    # <45 years
            (55, 2),    # 45-54 years  
            (65, 3),    # 55-64 years
            (75, 5),    # 65-74 years
            (999, 6)    # >74 years
        ]
        
        # Body temperature scoring thresholds (°C)
        self.TEMP_THRESHOLDS = [
            (30.0, 4),      # <30°C
            (32.0, 3),      # 30-31.9°C
            (34.0, 2),      # 32-33.9°C
            (36.0, 1),      # 34-35.9°C
            (38.5, 0),      # 36-38.4°C
            (39.0, 1),      # 38.5-38.9°C
            (41.0, 3),      # 39-40.9°C
            (999.0, 4)      # >40.9°C
        ]
        
        # Mean arterial pressure scoring thresholds (mmHg)
        self.MAP_THRESHOLDS = [
            (49, 2),        # <49 mmHg
            (70, 1),        # 50-69 mmHg
            (110, 0),       # 70-109 mmHg
            (130, 2),       # 110-129 mmHg
            (160, 3),       # 130-159 mmHg
            (999, 4)        # >159 mmHg
        ]
        
        # Heart rate scoring thresholds (bpm)
        self.HR_THRESHOLDS = [
            (39, 3),        # <39 bpm
            (55, 2),        # 40-54 bpm
            (70, 1),        # 55-69 bpm
            (110, 0),       # 70-109 bpm
            (140, 2),       # 110-139 bpm
            (180, 3),       # 140-179 bpm
            (999, 4)        # >179 bpm
        ]
        
        # Respiratory rate scoring thresholds (breaths/min)
        self.RR_THRESHOLDS = [
            (5, 3),         # <5 breaths/min
            (10, 2),        # 6-9 breaths/min
            (12, 1),        # 10-11 breaths/min
            (25, 0),        # 12-24 breaths/min
            (35, 2),        # 25-34 breaths/min
            (50, 3),        # 35-49 breaths/min
            (999, 4)        # >49 breaths/min
        ]
        
        # Oxygen saturation scoring thresholds (%)
        self.SAT_THRESHOLDS = [
            (75, 4),        # <75%
            (86, 3),        # 75-85%
            (90, 2),        # 86-89%
            (100, 0)        # >89%
        ]
        
        # Glasgow Coma Scale scoring thresholds
        self.GCS_THRESHOLDS = [
            (5, 4),         # <5
            (8, 3),         # 5-7
            (11, 2),        # 8-10
            (14, 1),        # 11-13
            (15, 0)         # >13
        ]
    
    def calculate(self, age: int, body_temperature: float, mean_arterial_pressure: int,
                 heart_rate: int, respiratory_rate: int, oxygen_saturation: int,
                 glasgow_coma_scale: int) -> Dict[str, Any]:
        """
        Calculates the REMS score using the provided parameters
        
        Args:
            age (int): Patient age in years
            body_temperature (float): Body temperature in °C
            mean_arterial_pressure (int): MAP in mmHg
            heart_rate (int): Heart rate in bpm
            respiratory_rate (int): Respiratory rate in breaths/min
            oxygen_saturation (int): SpO2 percentage
            glasgow_coma_scale (int): GCS score (3-15)
            
        Returns:
            Dict with the result and interpretation
        """
        
        # Validations
        self._validate_inputs(age, body_temperature, mean_arterial_pressure,
                            heart_rate, respiratory_rate, oxygen_saturation,
                            glasgow_coma_scale)
        
        # Calculate component scores
        age_score = self._calculate_age_score(age)
        temp_score = self._calculate_temperature_score(body_temperature)
        map_score = self._calculate_map_score(mean_arterial_pressure)
        hr_score = self._calculate_heart_rate_score(heart_rate)
        rr_score = self._calculate_respiratory_rate_score(respiratory_rate)
        sat_score = self._calculate_oxygen_saturation_score(oxygen_saturation)
        gcs_score = self._calculate_gcs_score(glasgow_coma_scale)
        
        # Calculate total score
        total_score = age_score + temp_score + map_score + hr_score + rr_score + sat_score + gcs_score
        
        # Get interpretation
        interpretation = self._get_interpretation(total_score)
        
        return {
            "result": total_score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"],
            "component_scores": {
                "age_score": age_score,
                "temperature_score": temp_score,
                "map_score": map_score,
                "heart_rate_score": hr_score,
                "respiratory_rate_score": rr_score,
                "oxygen_saturation_score": sat_score,
                "glasgow_coma_scale_score": gcs_score
            }
        }
    
    def _validate_inputs(self, age, body_temperature, mean_arterial_pressure,
                        heart_rate, respiratory_rate, oxygen_saturation,
                        glasgow_coma_scale):
        """Validates input parameters"""
        
        if not isinstance(age, int) or age < 0 or age > 120:
            raise ValueError("Age must be an integer between 0 and 120 years")
        
        if not isinstance(body_temperature, (int, float)) or body_temperature < 25.0 or body_temperature > 45.0:
            raise ValueError("Body temperature must be between 25.0 and 45.0°C")
        
        if not isinstance(mean_arterial_pressure, int) or mean_arterial_pressure < 20 or mean_arterial_pressure > 250:
            raise ValueError("Mean arterial pressure must be an integer between 20 and 250 mmHg")
        
        if not isinstance(heart_rate, int) or heart_rate < 20 or heart_rate > 250:
            raise ValueError("Heart rate must be an integer between 20 and 250 bpm")
        
        if not isinstance(respiratory_rate, int) or respiratory_rate < 1 or respiratory_rate > 80:
            raise ValueError("Respiratory rate must be an integer between 1 and 80 breaths/min")
        
        if not isinstance(oxygen_saturation, int) or oxygen_saturation < 50 or oxygen_saturation > 100:
            raise ValueError("Oxygen saturation must be an integer between 50 and 100%")
        
        if not isinstance(glasgow_coma_scale, int) or glasgow_coma_scale < 3 or glasgow_coma_scale > 15:
            raise ValueError("Glasgow Coma Scale must be an integer between 3 and 15")
    
    def _calculate_age_score(self, age: int) -> int:
        """Calculates age component score"""
        for threshold, score in self.AGE_THRESHOLDS:
            if age < threshold:
                return score
        return self.AGE_THRESHOLDS[-1][1]  # Default to highest score
    
    def _calculate_temperature_score(self, temperature: float) -> int:
        """Calculates body temperature component score"""
        if temperature < 30.0:
            return 4
        elif temperature < 32.0:
            return 3
        elif temperature < 34.0:
            return 2
        elif temperature < 36.0:
            return 1
        elif temperature <= 38.4:
            return 0
        elif temperature < 38.9:
            return 1
        elif temperature <= 40.9:
            return 3
        else:  # >40.9
            return 4
    
    def _calculate_map_score(self, map_pressure: int) -> int:
        """Calculates mean arterial pressure component score"""
        if map_pressure < 50:
            return 2
        elif map_pressure < 70:
            return 1
        elif map_pressure <= 109:
            return 0
        elif map_pressure < 130:
            return 2
        elif map_pressure < 160:
            return 3
        else:  # >=160
            return 4
    
    def _calculate_heart_rate_score(self, heart_rate: int) -> int:
        """Calculates heart rate component score"""
        if heart_rate < 40:
            return 3
        elif heart_rate < 55:
            return 2
        elif heart_rate < 70:
            return 1
        elif heart_rate <= 109:
            return 0
        elif heart_rate < 140:
            return 2
        elif heart_rate < 180:
            return 3
        else:  # >=180
            return 4
    
    def _calculate_respiratory_rate_score(self, respiratory_rate: int) -> int:
        """Calculates respiratory rate component score"""
        if respiratory_rate < 6:
            return 3
        elif respiratory_rate < 10:
            return 2
        elif respiratory_rate < 12:
            return 1
        elif respiratory_rate <= 24:
            return 0
        elif respiratory_rate < 35:
            return 2
        elif respiratory_rate <= 49:
            return 3
        else:  # >49
            return 4
    
    def _calculate_oxygen_saturation_score(self, oxygen_saturation: int) -> int:
        """Calculates oxygen saturation component score"""
        if oxygen_saturation < 75:
            return 4
        elif oxygen_saturation <= 85:
            return 3
        elif oxygen_saturation <= 89:
            return 2
        else:  # >89
            return 0
    
    def _calculate_gcs_score(self, glasgow_coma_scale: int) -> int:
        """Calculates Glasgow Coma Scale component score"""
        if glasgow_coma_scale < 5:
            return 4
        elif glasgow_coma_scale <= 7:
            return 3
        elif glasgow_coma_scale <= 10:
            return 2
        elif glasgow_coma_scale <= 13:
            return 1
        else:  # >13
            return 0
    
    def _get_interpretation(self, total_score: int) -> Dict[str, str]:
        """
        Determines the interpretation based on the result
        
        Args:
            total_score (int): Calculated REMS score
            
        Returns:
            Dict with interpretation
        """
        
        if total_score <= 2:
            return {
                "stage": "Very Low Risk",
                "description": "Very low mortality risk",
                "interpretation": f"REMS Score: {total_score} points. Very low risk of in-hospital mortality (0.3%). Standard care and monitoring appropriate."
            }
        elif total_score <= 5:
            return {
                "stage": "Low Risk",
                "description": "Low mortality risk",
                "interpretation": f"REMS Score: {total_score} points. Low risk of in-hospital mortality (2%). Close monitoring recommended."
            }
        elif total_score <= 9:
            return {
                "stage": "Moderate Risk",
                "description": "Moderate mortality risk",
                "interpretation": f"REMS Score: {total_score} points. Moderate risk of in-hospital mortality (6.7%). Enhanced monitoring and prompt intervention indicated."
            }
        elif total_score <= 11:
            return {
                "stage": "High Risk",
                "description": "High mortality risk",
                "interpretation": f"REMS Score: {total_score} points. High risk of in-hospital mortality (20.3%). Intensive monitoring and aggressive intervention required."
            }
        elif total_score <= 21:
            return {
                "stage": "Very High Risk",
                "description": "Very high mortality risk",
                "interpretation": f"REMS Score: {total_score} points. Very high risk of in-hospital mortality (>20%). Critical care management and intensive intervention required."
            }
        else:  # 22-26
            return {
                "stage": "Extremely High Risk",
                "description": "Extremely high mortality risk",
                "interpretation": f"REMS Score: {total_score} points. Extremely high risk of in-hospital mortality (approaching 100%). Palliative care considerations may be appropriate."
            }


def calculate_rems_score(age, body_temperature, mean_arterial_pressure,
                        heart_rate, respiratory_rate, oxygen_saturation,
                        glasgow_coma_scale) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_rems_score pattern
    """
    calculator = RemsScoreCalculator()
    return calculator.calculate(
        age, body_temperature, mean_arterial_pressure, heart_rate,
        respiratory_rate, oxygen_saturation, glasgow_coma_scale
    )