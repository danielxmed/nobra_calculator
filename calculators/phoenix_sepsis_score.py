"""
Phoenix Sepsis Score Calculator

International consensus criteria for pediatric sepsis and septic shock diagnosis 
based on organ dysfunction assessment. Developed by the SCCM Pediatric Sepsis 
Definition Task Force and published in JAMA 2024.

References (Vancouver style):
1. Schlapbach LJ, Watson RS, Sorce LR, Argent AC, Menon K, Hartman ME, et al. 
   International Consensus Criteria for Pediatric Sepsis and Septic Shock. 
   JAMA. 2024 Feb 27;331(8):665-674. doi: 10.1001/jama.2024.0179.
2. Watson RS, Schlapbach LJ, Sorce LR, Argent AC, Menon K, Hartman ME, et al. 
   Development and Validation of the Phoenix Criteria for Pediatric Sepsis and 
   Septic Shock. JAMA. 2024 Feb 27;331(8):675-686. doi: 10.1001/jama.2024.0196.
"""

from typing import Dict, Any, Optional


class PhoenixSepsisScoreCalculator:
    """Calculator for Phoenix Sepsis Score"""
    
    def __init__(self):
        # Age-based MAP thresholds (5th percentile)
        self.MAP_THRESHOLDS = {
            0: 31,   # 1 month to 1 year
            1: 32,   # 1-2 years
            2: 32,   # 2-5 years
            5: 36,   # 5-12 years
            12: 44,  # 12-18 years
        }
    
    def calculate(self, age: int, suspected_infection: str, respiratory_support: str,
                 pao2_fio2_ratio: Optional[float], spo2_fio2_ratio: Optional[float],
                 vasoactive_medications: int, lactate: Optional[float],
                 mean_arterial_pressure: Optional[int], platelets: Optional[int],
                 inr: Optional[float], d_dimer: Optional[float], 
                 fibrinogen: Optional[float], glasgow_coma_scale: int,
                 pupil_reactivity: str) -> Dict[str, Any]:
        """
        Calculates the Phoenix Sepsis Score using the provided parameters
        
        Args:
            age (int): Patient age in years (<18)
            suspected_infection (str): Presence of suspected/confirmed infection
            respiratory_support (str): Type of respiratory support
            pao2_fio2_ratio (Optional[float]): PaO2/FiO2 ratio
            spo2_fio2_ratio (Optional[float]): SpO2/FiO2 ratio
            vasoactive_medications (int): Number of vasoactive medications
            lactate (Optional[float]): Serum lactate in mmol/L
            mean_arterial_pressure (Optional[int]): MAP in mmHg
            platelets (Optional[int]): Platelet count in ×10³/μL
            inr (Optional[float]): International normalized ratio
            d_dimer (Optional[float]): D-dimer in mg/L FEU
            fibrinogen (Optional[float]): Fibrinogen in g/L
            glasgow_coma_scale (int): GCS score (3-15)
            pupil_reactivity (str): Pupil reactivity status
            
        Returns:
            Dict with the result and interpretation
        """
        
        # Validations
        self._validate_inputs(age, suspected_infection, respiratory_support,
                            vasoactive_medications, glasgow_coma_scale, pupil_reactivity)
        
        if suspected_infection == "no":
            return {
                "result": 0,
                "unit": "points",
                "interpretation": "Phoenix Sepsis Score cannot be calculated without suspected infection. Sepsis criteria require suspected or confirmed infection.",
                "stage": "Not Applicable",
                "stage_description": "No suspected infection",
                "component_scores": {
                    "respiratory_score": 0,
                    "cardiovascular_score": 0,
                    "coagulation_score": 0,
                    "neurologic_score": 0
                }
            }
        
        # Calculate component scores
        respiratory_score = self._calculate_respiratory_score(respiratory_support, pao2_fio2_ratio, spo2_fio2_ratio)
        cardiovascular_score = self._calculate_cardiovascular_score(vasoactive_medications, lactate, mean_arterial_pressure, age)
        coagulation_score = self._calculate_coagulation_score(platelets, inr, d_dimer, fibrinogen)
        neurologic_score = self._calculate_neurologic_score(glasgow_coma_scale, pupil_reactivity)
        
        # Calculate total score
        total_score = respiratory_score + cardiovascular_score + coagulation_score + neurologic_score
        
        # Determine sepsis and septic shock status
        sepsis_status = total_score >= 2
        septic_shock_status = sepsis_status and cardiovascular_score >= 1
        
        # Get interpretation
        interpretation = self._get_interpretation(total_score, sepsis_status, septic_shock_status)
        
        return {
            "result": total_score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"],
            "component_scores": {
                "respiratory_score": respiratory_score,
                "cardiovascular_score": cardiovascular_score,
                "coagulation_score": coagulation_score,
                "neurologic_score": neurologic_score
            },
            "clinical_status": {
                "sepsis": sepsis_status,
                "septic_shock": septic_shock_status
            }
        }
    
    def _validate_inputs(self, age, suspected_infection, respiratory_support,
                        vasoactive_medications, glasgow_coma_scale, pupil_reactivity):
        """Validates input parameters"""
        
        if not isinstance(age, int) or age < 0 or age >= 18:
            raise ValueError("Age must be an integer between 0 and 17 years")
        
        if suspected_infection not in ["yes", "no"]:
            raise ValueError("Suspected infection must be 'yes' or 'no'")
        
        valid_respiratory = ["none", "supplemental_oxygen", "high_flow_nasal_cannula", 
                           "non_invasive_ventilation", "invasive_mechanical_ventilation"]
        if respiratory_support not in valid_respiratory:
            raise ValueError(f"Respiratory support must be one of: {valid_respiratory}")
        
        if not isinstance(vasoactive_medications, int) or vasoactive_medications < 0:
            raise ValueError("Vasoactive medications must be a non-negative integer")
        
        if not isinstance(glasgow_coma_scale, int) or glasgow_coma_scale < 3 or glasgow_coma_scale > 15:
            raise ValueError("Glasgow Coma Scale must be an integer between 3 and 15")
        
        if pupil_reactivity not in ["both_reactive", "one_fixed", "both_fixed"]:
            raise ValueError("Pupil reactivity must be 'both_reactive', 'one_fixed', or 'both_fixed'")
    
    def _calculate_respiratory_score(self, respiratory_support: str, 
                                   pao2_fio2_ratio: Optional[float],
                                   spo2_fio2_ratio: Optional[float]) -> int:
        """Calculates respiratory subscore (0-3 points)"""
        
        score = 0
        
        # Base score for respiratory support
        if respiratory_support == "none":
            score = 0
        elif respiratory_support == "supplemental_oxygen":
            score = 1
        elif respiratory_support == "high_flow_nasal_cannula":
            score = 2
        elif respiratory_support == "non_invasive_ventilation":
            score = 3
        elif respiratory_support == "invasive_mechanical_ventilation":
            score = 3
        
        # Adjust based on oxygenation ratios if available
        if pao2_fio2_ratio is not None:
            if pao2_fio2_ratio < 100:
                score = max(score, 3)
            elif pao2_fio2_ratio < 200:
                score = max(score, 2)
            elif pao2_fio2_ratio < 300:
                score = max(score, 1)
        elif spo2_fio2_ratio is not None:
            if spo2_fio2_ratio < 150:
                score = max(score, 3)
            elif spo2_fio2_ratio < 220:
                score = max(score, 2)
            elif spo2_fio2_ratio < 300:
                score = max(score, 1)
        
        return min(score, 3)  # Maximum 3 points
    
    def _calculate_cardiovascular_score(self, vasoactive_medications: int,
                                      lactate: Optional[float],
                                      mean_arterial_pressure: Optional[int],
                                      age: int) -> int:
        """Calculates cardiovascular subscore (0-6 points)"""
        
        score = 0
        
        # Vasoactive medications (0-2 points)
        if vasoactive_medications == 0:
            vaso_score = 0
        elif vasoactive_medications == 1:
            vaso_score = 1
        else:  # 2 or more medications
            vaso_score = 2
        
        score += vaso_score
        
        # Lactate (0-2 points)
        if lactate is not None:
            if lactate >= 11.0:
                lactate_score = 2
            elif lactate >= 5.0:
                lactate_score = 1
            else:
                lactate_score = 0
            
            score += lactate_score
        
        # Mean arterial pressure (0-2 points)
        if mean_arterial_pressure is not None:
            map_threshold = self._get_map_threshold(age)
            if mean_arterial_pressure < map_threshold:
                score += 2
        
        return min(score, 6)  # Maximum 6 points
    
    def _get_map_threshold(self, age: int) -> int:
        """Gets age-appropriate MAP threshold (5th percentile)"""
        
        if age < 1:
            return self.MAP_THRESHOLDS[0]
        elif age < 2:
            return self.MAP_THRESHOLDS[1]
        elif age < 5:
            return self.MAP_THRESHOLDS[2]
        elif age < 12:
            return self.MAP_THRESHOLDS[5]
        else:
            return self.MAP_THRESHOLDS[12]
    
    def _calculate_coagulation_score(self, platelets: Optional[int], inr: Optional[float],
                                   d_dimer: Optional[float], fibrinogen: Optional[float]) -> int:
        """Calculates coagulation subscore (0-2 points)"""
        
        score = 0
        
        # Platelets (0-1 point)
        if platelets is not None and platelets < 100:
            score += 1
        
        # INR (0-1 point)
        if inr is not None and inr > 1.3:
            score += 1
        
        # D-dimer (0-1 point) - using elevated threshold
        if d_dimer is not None and d_dimer > 2.0:
            score += 1
        
        # Fibrinogen (0-1 point)
        if fibrinogen is not None and fibrinogen < 1.0:
            score += 1
        
        return min(score, 2)  # Maximum 2 points
    
    def _calculate_neurologic_score(self, glasgow_coma_scale: int, pupil_reactivity: str) -> int:
        """Calculates neurologic subscore (0-2 points)"""
        
        score = 0
        
        # Glasgow Coma Scale
        if glasgow_coma_scale < 11:
            score += 1
        
        # Pupil reactivity
        if pupil_reactivity == "one_fixed":
            score += 1
        elif pupil_reactivity == "both_fixed":
            score += 2
        
        return min(score, 2)  # Maximum 2 points
    
    def _get_interpretation(self, total_score: int, sepsis_status: bool, 
                          septic_shock_status: bool) -> Dict[str, str]:
        """
        Determines the interpretation based on the result
        
        Args:
            total_score (int): Calculated Phoenix Sepsis Score
            sepsis_status (bool): Whether patient meets sepsis criteria
            septic_shock_status (bool): Whether patient meets septic shock criteria
            
        Returns:
            Dict with interpretation
        """
        
        if not sepsis_status:
            return {
                "stage": "No Sepsis",
                "description": "Score does not meet sepsis criteria",
                "interpretation": f"Phoenix Sepsis Score: {total_score} points. Does not meet criteria for sepsis (requires ≥2 points with suspected infection). Continue monitoring for clinical deterioration and reassess if condition changes."
            }
        else:
            if septic_shock_status:
                return {
                    "stage": "Septic Shock",
                    "description": "Meets criteria for septic shock",
                    "interpretation": f"Phoenix Sepsis Score: {total_score} points. Meets criteria for SEPTIC SHOCK (sepsis with cardiovascular dysfunction). This indicates potentially life-threatening organ dysfunction requiring immediate intensive care management, aggressive fluid resuscitation, and vasoactive support."
                }
            else:
                return {
                    "stage": "Sepsis",
                    "description": "Meets criteria for sepsis",
                    "interpretation": f"Phoenix Sepsis Score: {total_score} points. Meets criteria for SEPSIS indicating potentially life-threatening organ dysfunction. Requires urgent medical evaluation, immediate antibiotic therapy, fluid resuscitation, and close monitoring for progression to septic shock."
                }


def calculate_phoenix_sepsis_score(age, suspected_infection, respiratory_support,
                                 pao2_fio2_ratio, spo2_fio2_ratio, vasoactive_medications,
                                 lactate, mean_arterial_pressure, platelets, inr,
                                 d_dimer, fibrinogen, glasgow_coma_scale,
                                 pupil_reactivity) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_phoenix_sepsis_score pattern
    """
    calculator = PhoenixSepsisScoreCalculator()
    return calculator.calculate(
        age, suspected_infection, respiratory_support, pao2_fio2_ratio,
        spo2_fio2_ratio, vasoactive_medications, lactate, mean_arterial_pressure,
        platelets, inr, d_dimer, fibrinogen, glasgow_coma_scale, pupil_reactivity
    )