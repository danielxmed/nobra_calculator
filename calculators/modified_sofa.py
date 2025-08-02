"""
Modified Sequential Organ Failure Assessment (mSOFA) Score Calculator

Predicts ICU mortality using mostly clinical variables and fewer labs compared 
to the original SOFA Score. Designed for resource-constrained critical care 
environments during disasters or pandemics.

References:
1. Grissom CK, et al. Disaster Med Public Health Prep. 2010;4(4):277-84.
2. Vahedian-Azimi A, et al. Turk J Anaesthesiol Reanim. 2017;45(1):16-22.
3. Rahmatinejad Z, et al. Am J Emerg Med. 2018;36(5):775-781.
"""

from typing import Dict, Any


class ModifiedSofaCalculator:
    """Calculator for Modified Sequential Organ Failure Assessment (mSOFA) Score"""
    
    def __init__(self):
        # Vasopressor use mappings
        self.VASOPRESSOR_MAPPING = {
            "none": "none",
            "low_dose": "low_dose",
            "moderate_dose": "moderate_dose", 
            "high_dose": "high_dose"
        }
        
        # Scleral icterus mappings
        self.ICTERUS_MAPPING = {
            "absent": False,
            "present": True
        }
    
    def calculate(self, spo2_fio2_ratio: int, scleral_icterus: str, mean_arterial_pressure: int,
                  vasopressor_use: str, glasgow_coma_scale: int, creatinine: float) -> Dict[str, Any]:
        """
        Calculates the mSOFA score based on organ system dysfunction
        
        Args:
            spo2_fio2_ratio (int): SpO₂/FiO₂ ratio for respiratory assessment
            scleral_icterus (str): Presence of scleral icterus or jaundice
            mean_arterial_pressure (int): Mean arterial pressure in mmHg
            vasopressor_use (str): Use of vasopressor medications
            glasgow_coma_scale (int): Glasgow Coma Scale score
            creatinine (float): Serum creatinine level in mg/dL
            
        Returns:
            Dict with mSOFA score and clinical interpretation
        """
        
        # Validate inputs
        self._validate_inputs(spo2_fio2_ratio, scleral_icterus, mean_arterial_pressure,
                             vasopressor_use, glasgow_coma_scale, creatinine)
        
        # Calculate component scores
        respiratory_score = self._calculate_respiratory_score(spo2_fio2_ratio)
        liver_score = self._calculate_liver_score(scleral_icterus)
        cardiovascular_score = self._calculate_cardiovascular_score(mean_arterial_pressure, vasopressor_use)
        cns_score = self._calculate_cns_score(glasgow_coma_scale)
        renal_score = self._calculate_renal_score(creatinine)
        
        # Total mSOFA score
        total_score = respiratory_score + liver_score + cardiovascular_score + cns_score + renal_score
        
        # Get interpretation
        interpretation = self._get_interpretation(total_score)
        
        return {
            "result": total_score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, spo2_fio2_ratio: int, scleral_icterus: str, mean_arterial_pressure: int,
                        vasopressor_use: str, glasgow_coma_scale: int, creatinine: float):
        """Validates input parameters"""
        
        if not isinstance(spo2_fio2_ratio, int) or spo2_fio2_ratio < 50 or spo2_fio2_ratio > 500:
            raise ValueError("SpO₂/FiO₂ ratio must be an integer between 50 and 500")
        
        if scleral_icterus not in self.ICTERUS_MAPPING:
            raise ValueError(f"Scleral icterus must be one of: {list(self.ICTERUS_MAPPING.keys())}")
        
        if not isinstance(mean_arterial_pressure, int) or mean_arterial_pressure < 30 or mean_arterial_pressure > 200:
            raise ValueError("Mean arterial pressure must be an integer between 30 and 200 mmHg")
        
        if vasopressor_use not in self.VASOPRESSOR_MAPPING:
            raise ValueError(f"Vasopressor use must be one of: {list(self.VASOPRESSOR_MAPPING.keys())}")
        
        if not isinstance(glasgow_coma_scale, int) or glasgow_coma_scale < 3 or glasgow_coma_scale > 15:
            raise ValueError("Glasgow Coma Scale must be an integer between 3 and 15")
        
        if not isinstance(creatinine, (int, float)) or creatinine < 0.1 or creatinine > 10.0:
            raise ValueError("Creatinine must be a number between 0.1 and 10.0 mg/dL")
    
    def _calculate_respiratory_score(self, spo2_fio2_ratio: int) -> int:
        """
        Calculates respiratory system score based on SpO₂/FiO₂ ratio
        
        SpO₂/FiO₂ scoring:
        - >400: 0 points
        - 315-400: 1 point  
        - 235-314: 2 points
        - 150-234: 3 points
        - ≤150: 4 points
        """
        
        if spo2_fio2_ratio > 400:
            return 0
        elif spo2_fio2_ratio >= 315:
            return 1
        elif spo2_fio2_ratio >= 235:
            return 2
        elif spo2_fio2_ratio >= 150:
            return 3
        else:  # ≤150
            return 4
    
    def _calculate_liver_score(self, scleral_icterus: str) -> int:
        """
        Calculates liver system score based on scleral icterus
        
        Liver scoring:
        - Absent: 0 points
        - Present: 3 points
        """
        
        icterus_present = self.ICTERUS_MAPPING[scleral_icterus]
        return 3 if icterus_present else 0
    
    def _calculate_cardiovascular_score(self, mean_arterial_pressure: int, vasopressor_use: str) -> int:
        """
        Calculates cardiovascular system score based on MAP and vasopressor use
        
        Cardiovascular scoring:
        - MAP ≥70 mmHg: 0 points
        - MAP <70 mmHg: 1 point
        - Low-dose vasopressors: 2 points
        - Moderate-dose vasopressors: 3 points
        - High-dose vasopressors: 4 points
        """
        
        # If on vasopressors, use vasopressor-based scoring
        if vasopressor_use == "low_dose":
            return 2
        elif vasopressor_use == "moderate_dose":
            return 3
        elif vasopressor_use == "high_dose":
            return 4
        
        # If no vasopressors, use MAP-based scoring
        if mean_arterial_pressure >= 70:
            return 0
        else:  # MAP <70 mmHg
            return 1
    
    def _calculate_cns_score(self, glasgow_coma_scale: int) -> int:
        """
        Calculates central nervous system score based on Glasgow Coma Scale
        
        CNS scoring:
        - GCS 15: 0 points
        - GCS 13-14: 1 point
        - GCS 10-12: 2 points
        - GCS 6-9: 3 points
        - GCS <6: 4 points
        """
        
        if glasgow_coma_scale == 15:
            return 0
        elif glasgow_coma_scale >= 13:
            return 1
        elif glasgow_coma_scale >= 10:
            return 2
        elif glasgow_coma_scale >= 6:
            return 3
        else:  # GCS <6
            return 4
    
    def _calculate_renal_score(self, creatinine: float) -> int:
        """
        Calculates renal system score based on serum creatinine
        
        Renal scoring:
        - <1.2 mg/dL: 0 points
        - 1.2-1.9 mg/dL: 1 point
        - 2.0-3.4 mg/dL: 2 points
        - 3.5-4.9 mg/dL: 3 points
        - ≥5.0 mg/dL: 4 points
        """
        
        if creatinine < 1.2:
            return 0
        elif creatinine < 2.0:
            return 1
        elif creatinine < 3.5:
            return 2
        elif creatinine < 5.0:
            return 3
        else:  # ≥5.0 mg/dL
            return 4
    
    def _get_interpretation(self, score: int) -> Dict[str, str]:
        """
        Provides clinical interpretation based on mSOFA score
        
        Args:
            score (int): Total mSOFA score
            
        Returns:
            Dict with interpretation details
        """
        
        if score <= 7:
            return {
                "stage": "Low Risk",
                "description": "4% 30-day mortality",
                "interpretation": (f"mSOFA Score {score}: Low mortality risk. The patient has a 4% risk of "
                                f"30-day mortality in the ICU setting. This represents good prognosis with "
                                f"relatively mild organ dysfunction. Continue standard ICU care with routine "
                                f"monitoring. The simplified mSOFA assessment suggests the patient is likely "
                                f"to recover well with appropriate supportive care. Regular reassessment "
                                f"recommended to monitor for any changes in clinical status.")
            }
        elif score <= 11:
            return {
                "stage": "Moderate Risk", 
                "description": "31% 30-day mortality",
                "interpretation": (f"mSOFA Score {score}: Moderate mortality risk. The patient has a 31% risk "
                                f"of 30-day mortality, indicating moderate organ dysfunction requiring intensive "
                                f"monitoring and aggressive treatment. This score suggests the need for close "
                                f"observation and potentially more intensive interventions. Consider escalation "
                                f"of care, optimization of organ support measures, and frequent reassessment "
                                f"of clinical status. The patient may benefit from multidisciplinary team "
                                f"involvement and early goals of care discussions.")
            }
        else:  # score > 11
            return {
                "stage": "High Risk",
                "description": "58% 30-day mortality", 
                "interpretation": (f"mSOFA Score {score}: High mortality risk. The patient has a 58% risk of "
                                f"30-day mortality, indicating severe multi-organ dysfunction requiring maximum "
                                f"intensive care support. This high score warrants immediate consideration of "
                                f"goals of care discussions, potential limitations of care, and prognosis "
                                f"communication with family. Evaluate for appropriateness of aggressive "
                                f"interventions, consider palliative care consultation, and ensure comprehensive "
                                f"family communication regarding the patient's critical condition and prognosis.")
            }


def calculate_modified_sofa(spo2_fio2_ratio: int, scleral_icterus: str, mean_arterial_pressure: int,
                           vasopressor_use: str, glasgow_coma_scale: int, creatinine: float) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = ModifiedSofaCalculator()
    return calculator.calculate(spo2_fio2_ratio, scleral_icterus, mean_arterial_pressure,
                               vasopressor_use, glasgow_coma_scale, creatinine)