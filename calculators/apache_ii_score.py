"""
APACHE II Score Calculator

Acute Physiology and Chronic Health Evaluation II score for estimating ICU mortality.
Based on physiological parameters, age, and chronic health status within 24 hours of ICU admission.

References:
- Knaus WA, Draper EA, Wagner DP, Zimmerman JE. APACHE II: a severity of disease classification system. 
  Crit Care Med. 1985;13(10):818-29. doi: 10.1097/00003246-198510000-00009. PMID: 3928249.
"""

import math
from typing import Dict, Any


class ApacheIiScoreCalculator:
    """Calculator for APACHE II Score"""
    
    def __init__(self):
        # Temperature scoring ranges (Celsius)
        self.TEMP_RANGES = {
            (41.0, float('inf')): 4,
            (39.0, 40.9): 3,
            (38.5, 38.9): 1,
            (36.0, 38.4): 0,
            (34.0, 35.9): 1,
            (32.0, 33.9): 2,
            (30.0, 31.9): 3,
            (float('-inf'), 29.9): 4
        }
        
        # Mean arterial pressure scoring ranges (mmHg)
        self.MAP_RANGES = {
            (160, float('inf')): 4,
            (130, 159): 3,
            (110, 129): 2,
            (70, 109): 0,
            (50, 69): 2,
            (float('-inf'), 49): 4
        }
        
        # Heart rate scoring ranges (bpm)
        self.HR_RANGES = {
            (180, float('inf')): 4,
            (140, 179): 3,
            (110, 139): 2,
            (70, 109): 0,
            (55, 69): 2,
            (40, 54): 3,
            (float('-inf'), 39): 4
        }
        
        # Respiratory rate scoring ranges (breaths/min)
        self.RR_RANGES = {
            (50, float('inf')): 4,
            (35, 49): 3,
            (25, 34): 1,
            (12, 24): 0,
            (10, 11): 1,
            (6, 9): 2,
            (float('-inf'), 5): 4
        }
        
        # pH scoring ranges
        self.PH_RANGES = {
            (7.7, float('inf')): 4,
            (7.6, 7.69): 3,
            (7.5, 7.59): 1,
            (7.33, 7.49): 0,
            (7.25, 7.32): 2,
            (7.15, 7.24): 3,
            (float('-inf'), 7.14): 4
        }
        
        # Sodium scoring ranges (mEq/L)
        self.SODIUM_RANGES = {
            (180, float('inf')): 4,
            (160, 179): 3,
            (155, 159): 2,
            (150, 154): 1,
            (130, 149): 0,
            (120, 129): 2,
            (111, 119): 3,
            (float('-inf'), 110): 4
        }
        
        # Potassium scoring ranges (mEq/L)
        self.POTASSIUM_RANGES = {
            (7.0, float('inf')): 4,
            (6.0, 6.9): 3,
            (5.5, 5.9): 1,
            (3.5, 5.4): 0,
            (3.0, 3.4): 1,
            (2.5, 2.9): 2,
            (float('-inf'), 2.4): 4
        }
        
        # Creatinine scoring ranges (mg/dL)
        self.CREATININE_RANGES = {
            (3.5, float('inf')): 4,
            (2.0, 3.4): 3,
            (1.5, 1.9): 2,
            (0.6, 1.4): 0,
            (float('-inf'), 0.5): 2
        }
        
        # Hematocrit scoring ranges (%)
        self.HEMATOCRIT_RANGES = {
            (60, float('inf')): 4,
            (50, 59.9): 2,
            (46, 49.9): 1,
            (30, 45.9): 0,
            (20, 29.9): 2,
            (float('-inf'), 19.9): 4
        }
        
        # WBC scoring ranges (×10³/mm³)
        self.WBC_RANGES = {
            (40, float('inf')): 4,
            (20, 39.9): 2,
            (15, 19.9): 1,
            (3, 14.9): 0,
            (1, 2.9): 2,
            (float('-inf'), 0.9): 4
        }
        
        # PaO2 scoring ranges for FiO2 < 0.5 (mmHg)
        self.PAO2_RANGES = {
            (500, float('inf')): 4,
            (350, 499): 3,
            (200, 349): 1,
            (70, 199): 0,
            (61, 69): 1,
            (55, 60): 3,
            (float('-inf'), 54): 4
        }
        
        # A-aDO2 scoring ranges for FiO2 ≥ 0.5 (mmHg)
        self.AADO2_RANGES = {
            (500, float('inf')): 4,
            (350, 499): 3,
            (200, 349): 2,
            (float('-inf'), 199): 0
        }
    
    def calculate(self, age: int, temperature: float, mean_arterial_pressure: int, 
                 ph: float, heart_rate: int, respiratory_rate: int, sodium: int,
                 potassium: float, creatinine: float, acute_renal_failure: str,
                 hematocrit: float, white_blood_cell_count: float, glasgow_coma_scale: int,
                 fio2: float, pao2: float = None, aado2: float = None,
                 chronic_health_status: str = "none", admission_type: str = "nonoperative") -> Dict[str, Any]:
        """
        Calculates APACHE II Score
        
        Args:
            age (int): Patient's age in years
            temperature (float): Worst body temperature in °C
            mean_arterial_pressure (int): Worst MAP in mmHg
            ph (float): Worst arterial pH
            heart_rate (int): Worst heart rate in bpm
            respiratory_rate (int): Worst respiratory rate in breaths/min
            sodium (int): Worst serum sodium in mEq/L
            potassium (float): Worst serum potassium in mEq/L
            creatinine (float): Worst serum creatinine in mg/dL
            acute_renal_failure (str): "yes" or "no"
            hematocrit (float): Worst hematocrit in %
            white_blood_cell_count (float): Worst WBC in ×10³/mm³
            glasgow_coma_scale (int): GCS score (3-15)
            fio2 (float): Fraction of inspired oxygen (0.21-1.0)
            pao2 (float): Arterial oxygen pressure in mmHg (required if FiO2 < 0.5)
            aado2 (float): A-aDO2 in mmHg (required if FiO2 ≥ 0.5)
            chronic_health_status (str): "none" or "present"
            admission_type (str): "elective_postoperative", "nonoperative", or "emergency_postoperative"
            
        Returns:
            Dict with the result and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(age, temperature, mean_arterial_pressure, ph, heart_rate,
                            respiratory_rate, sodium, potassium, creatinine, acute_renal_failure,
                            hematocrit, white_blood_cell_count, glasgow_coma_scale, fio2,
                            pao2, aado2, chronic_health_status, admission_type)
        
        # Calculate Acute Physiology Score
        aps = self._calculate_acute_physiology_score(
            temperature, mean_arterial_pressure, ph, heart_rate, respiratory_rate,
            sodium, potassium, creatinine, acute_renal_failure, hematocrit,
            white_blood_cell_count, glasgow_coma_scale, fio2, pao2, aado2
        )
        
        # Calculate age points
        age_points = self._calculate_age_points(age)
        
        # Calculate chronic health points
        chronic_health_points = self._calculate_chronic_health_points(chronic_health_status, admission_type)
        
        # Calculate total APACHE II score
        apache_ii_score = aps + age_points + chronic_health_points
        
        # Get interpretation
        interpretation = self._get_interpretation(apache_ii_score)
        
        return {
            "result": apache_ii_score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, age, temperature, mean_arterial_pressure, ph, heart_rate,
                        respiratory_rate, sodium, potassium, creatinine, acute_renal_failure,
                        hematocrit, white_blood_cell_count, glasgow_coma_scale, fio2,
                        pao2, aado2, chronic_health_status, admission_type):
        """Validates input parameters"""
        
        if not isinstance(age, int) or age < 0 or age > 120:
            raise ValueError("Age must be an integer between 0 and 120 years")
        
        if not isinstance(temperature, (int, float)) or temperature < 25.0 or temperature > 46.0:
            raise ValueError("Temperature must be between 25.0 and 46.0°C")
        
        if not isinstance(mean_arterial_pressure, int) or mean_arterial_pressure < 30 or mean_arterial_pressure > 250:
            raise ValueError("Mean arterial pressure must be between 30 and 250 mmHg")
        
        if not isinstance(ph, (int, float)) or ph < 6.5 or ph > 8.0:
            raise ValueError("pH must be between 6.5 and 8.0")
        
        if not isinstance(heart_rate, int) or heart_rate < 20 or heart_rate > 250:
            raise ValueError("Heart rate must be between 20 and 250 bpm")
        
        if not isinstance(respiratory_rate, int) or respiratory_rate < 5 or respiratory_rate > 80:
            raise ValueError("Respiratory rate must be between 5 and 80 breaths/min")
        
        if not isinstance(sodium, int) or sodium < 100 or sodium > 200:
            raise ValueError("Sodium must be between 100 and 200 mEq/L")
        
        if not isinstance(potassium, (int, float)) or potassium < 1.0 or potassium > 10.0:
            raise ValueError("Potassium must be between 1.0 and 10.0 mEq/L")
        
        if not isinstance(creatinine, (int, float)) or creatinine < 0.1 or creatinine > 20.0:
            raise ValueError("Creatinine must be between 0.1 and 20.0 mg/dL")
        
        if acute_renal_failure not in ["yes", "no"]:
            raise ValueError("Acute renal failure must be 'yes' or 'no'")
        
        if not isinstance(hematocrit, (int, float)) or hematocrit < 10.0 or hematocrit > 70.0:
            raise ValueError("Hematocrit must be between 10.0 and 70.0%")
        
        if not isinstance(white_blood_cell_count, (int, float)) or white_blood_cell_count < 0.1 or white_blood_cell_count > 100.0:
            raise ValueError("White blood cell count must be between 0.1 and 100.0 ×10³/mm³")
        
        if not isinstance(glasgow_coma_scale, int) or glasgow_coma_scale < 3 or glasgow_coma_scale > 15:
            raise ValueError("Glasgow Coma Scale must be between 3 and 15")
        
        if not isinstance(fio2, (int, float)) or fio2 < 0.21 or fio2 > 1.0:
            raise ValueError("FiO2 must be between 0.21 and 1.0")
        
        if fio2 < 0.5:
            if pao2 is None:
                raise ValueError("PaO2 is required when FiO2 < 0.5")
            if not isinstance(pao2, (int, float)) or pao2 < 30.0 or pao2 > 700.0:
                raise ValueError("PaO2 must be between 30.0 and 700.0 mmHg")
        
        if fio2 >= 0.5:
            if aado2 is None:
                raise ValueError("A-aDO2 is required when FiO2 ≥ 0.5")
            if not isinstance(aado2, (int, float)) or aado2 < 0.0 or aado2 > 800.0:
                raise ValueError("A-aDO2 must be between 0.0 and 800.0 mmHg")
        
        if chronic_health_status not in ["none", "present"]:
            raise ValueError("Chronic health status must be 'none' or 'present'")
        
        if admission_type not in ["elective_postoperative", "nonoperative", "emergency_postoperative"]:
            raise ValueError("Admission type must be 'elective_postoperative', 'nonoperative', or 'emergency_postoperative'")
    
    def _get_points_from_ranges(self, value: float, ranges: dict) -> int:
        """Helper function to get points from value ranges"""
        for (min_val, max_val), points in ranges.items():
            if min_val <= value <= max_val:
                return points
        return 0
    
    def _calculate_acute_physiology_score(self, temperature, mean_arterial_pressure, ph,
                                        heart_rate, respiratory_rate, sodium, potassium,
                                        creatinine, acute_renal_failure, hematocrit,
                                        white_blood_cell_count, glasgow_coma_scale,
                                        fio2, pao2, aado2):
        """Calculates the Acute Physiology Score component (0-60 points)"""
        
        aps = 0
        
        # Temperature points
        aps += self._get_points_from_ranges(temperature, self.TEMP_RANGES)
        
        # MAP points
        aps += self._get_points_from_ranges(mean_arterial_pressure, self.MAP_RANGES)
        
        # Heart rate points
        aps += self._get_points_from_ranges(heart_rate, self.HR_RANGES)
        
        # Respiratory rate points
        aps += self._get_points_from_ranges(respiratory_rate, self.RR_RANGES)
        
        # pH points
        aps += self._get_points_from_ranges(ph, self.PH_RANGES)
        
        # Sodium points
        aps += self._get_points_from_ranges(sodium, self.SODIUM_RANGES)
        
        # Potassium points
        aps += self._get_points_from_ranges(potassium, self.POTASSIUM_RANGES)
        
        # Creatinine points (doubled if acute renal failure)
        creatinine_points = self._get_points_from_ranges(creatinine, self.CREATININE_RANGES)
        if acute_renal_failure == "yes":
            creatinine_points *= 2
        aps += creatinine_points
        
        # Hematocrit points
        aps += self._get_points_from_ranges(hematocrit, self.HEMATOCRIT_RANGES)
        
        # WBC points
        aps += self._get_points_from_ranges(white_blood_cell_count, self.WBC_RANGES)
        
        # Glasgow Coma Scale points (15 - actual GCS)
        aps += 15 - glasgow_coma_scale
        
        # Oxygenation points
        if fio2 < 0.5:
            aps += self._get_points_from_ranges(pao2, self.PAO2_RANGES)
        else:
            aps += self._get_points_from_ranges(aado2, self.AADO2_RANGES)
        
        return aps
    
    def _calculate_age_points(self, age: int) -> int:
        """Calculates age points (0-6 points)"""
        if age <= 44:
            return 0
        elif 45 <= age <= 54:
            return 2
        elif 55 <= age <= 64:
            return 3
        elif 65 <= age <= 74:
            return 5
        else:  # age >= 75
            return 6
    
    def _calculate_chronic_health_points(self, chronic_health_status: str, admission_type: str) -> int:
        """Calculates chronic health points (0-5 points)"""
        if chronic_health_status == "none":
            return 0
        
        if admission_type == "elective_postoperative":
            return 2
        else:  # nonoperative or emergency_postoperative
            return 5
    
    def _get_interpretation(self, score: int) -> Dict[str, str]:
        """
        Determines the interpretation based on the APACHE II score
        
        Args:
            score (int): APACHE II score
            
        Returns:
            Dict with interpretation
        """
        
        if score <= 9:
            return {
                "stage": "Low Risk",
                "description": "Low mortality risk",
                "interpretation": "APACHE II score 0-9 points indicates low severity of illness with predicted mortality typically <10%. Patients in this range generally have a good prognosis for ICU survival."
            }
        elif score <= 19:
            return {
                "stage": "Moderate Risk",
                "description": "Moderate mortality risk",
                "interpretation": "APACHE II score 10-19 points indicates moderate severity of illness with predicted mortality typically 10-25%. Close monitoring and standard ICU care are appropriate."
            }
        elif score <= 29:
            return {
                "stage": "High Risk",
                "description": "High mortality risk",
                "interpretation": "APACHE II score 20-29 points indicates high severity of illness with predicted mortality typically 25-50%. Aggressive intensive care management is warranted."
            }
        elif score <= 39:
            return {
                "stage": "Very High Risk",
                "description": "Very high mortality risk",
                "interpretation": "APACHE II score 30-39 points indicates very high severity of illness with predicted mortality typically 50-75%. Maximum intensive care support and consideration of goals of care discussions may be appropriate."
            }
        else:  # score >= 40
            return {
                "stage": "Extremely High Risk",
                "description": "Extremely high mortality risk",
                "interpretation": "APACHE II score ≥40 points indicates extremely high severity of illness with predicted mortality typically >75%. Consider palliative care consultation and careful evaluation of treatment goals."
            }


def calculate_apache_ii_score(age, temperature, mean_arterial_pressure, ph, heart_rate,
                            respiratory_rate, sodium, potassium, creatinine, acute_renal_failure,
                            hematocrit, white_blood_cell_count, glasgow_coma_scale, fio2,
                            pao2=None, aado2=None, chronic_health_status="none", 
                            admission_type="nonoperative") -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_apache_ii_score pattern
    """
    calculator = ApacheIiScoreCalculator()
    return calculator.calculate(
        age, temperature, mean_arterial_pressure, ph, heart_rate,
        respiratory_rate, sodium, potassium, creatinine, acute_renal_failure,
        hematocrit, white_blood_cell_count, glasgow_coma_scale, fio2,
        pao2, aado2, chronic_health_status, admission_type
    )