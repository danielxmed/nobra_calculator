"""
Cryoprecipitate Dosing for Fibrinogen Replacement Calculator

Calculates the required dose of cryoprecipitate units needed to achieve 
target fibrinogen levels in patients with hypofibrinogenemia.

References:
- American Association of Blood Banks (AABB). Technical Manual, 20th Edition. 2020.
- British Committee for Standards in Haematology. Br J Haematol. 2004;126(1):11-28.
- American Red Cross. Circular of Information for the Use of Human Blood and Blood Components. 2017.
"""

import math
from typing import Dict, Any, Optional


class CryoprecipitateDosing Calculator:
    """Calculator for Cryoprecipitate Dosing for Fibrinogen Replacement"""
    
    def __init__(self):
        # Plasma volume factors
        self.MALE_PLASMA_FACTOR = 0.07
        self.FEMALE_PLASMA_FACTOR = 0.065
        
        # Default fibrinogen content per unit
        self.DEFAULT_FIBRINOGEN_PER_UNIT = 200.0  # mg
        
        # Clinical thresholds
        self.CRITICAL_FIBRINOGEN = 50.0  # mg/dL
        self.NORMAL_FIBRINOGEN_MIN = 150.0  # mg/dL
        self.MAJOR_BLEEDING_TARGET = 200.0  # mg/dL
    
    def calculate(self, patient_weight: float, patient_sex: str, hematocrit: float,
                  current_fibrinogen: float, target_fibrinogen: float,
                  fibrinogen_per_unit: Optional[float] = None) -> Dict[str, Any]:
        """
        Calculates the required cryoprecipitate dose for fibrinogen replacement
        
        Args:
            patient_weight (float): Patient weight in kg
            patient_sex (str): Patient biological sex ("male" or "female")
            hematocrit (float): Current hematocrit as decimal (0.40 for 40%)
            current_fibrinogen (float): Current fibrinogen level in mg/dL
            target_fibrinogen (float): Target fibrinogen level in mg/dL
            fibrinogen_per_unit (float, optional): Fibrinogen content per unit in mg
            
        Returns:
            Dict with the result and interpretation
        """
        
        # Use default fibrinogen content if not provided
        if fibrinogen_per_unit is None:
            fibrinogen_per_unit = self.DEFAULT_FIBRINOGEN_PER_UNIT
        
        # Validations
        self._validate_inputs(patient_weight, patient_sex, hematocrit,
                            current_fibrinogen, target_fibrinogen, fibrinogen_per_unit)
        
        # Calculate plasma volume
        plasma_volume_dL = self._calculate_plasma_volume(patient_weight, patient_sex, hematocrit)
        
        # Calculate required fibrinogen increase
        fibrinogen_increase = target_fibrinogen - current_fibrinogen
        
        # Calculate total fibrinogen needed (mg)
        total_fibrinogen_needed = fibrinogen_increase * plasma_volume_dL
        
        # Calculate units required
        units_required = total_fibrinogen_needed / fibrinogen_per_unit
        
        # Round up to whole units
        units_required_rounded = math.ceil(max(0, units_required))
        
        # Get interpretation
        interpretation = self._get_interpretation(units_required_rounded, current_fibrinogen,
                                                target_fibrinogen, patient_weight)
        
        return {
            "result": units_required_rounded,
            "unit": "units",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"],
            "calculation_details": {
                "plasma_volume_dL": round(plasma_volume_dL, 1),
                "fibrinogen_increase_needed": round(fibrinogen_increase, 1),
                "total_fibrinogen_needed_mg": round(total_fibrinogen_needed, 0),
                "fibrinogen_per_unit_mg": fibrinogen_per_unit,
                "exact_units_calculated": round(units_required, 2)
            },
            "clinical_considerations": self._get_clinical_considerations(units_required_rounded,
                                                                      current_fibrinogen,
                                                                      target_fibrinogen),
            "alternative_dosing": self._get_alternative_dosing(patient_weight, fibrinogen_increase)
        }
    
    def _validate_inputs(self, patient_weight: float, patient_sex: str, hematocrit: float,
                        current_fibrinogen: float, target_fibrinogen: float,
                        fibrinogen_per_unit: float):
        """Validates input parameters"""
        
        if not 1.0 <= patient_weight <= 300.0:
            raise ValueError("Patient weight must be between 1.0 and 300.0 kg")
        
        if patient_sex not in ["male", "female"]:
            raise ValueError("Patient sex must be 'male' or 'female'")
        
        if not 0.15 <= hematocrit <= 0.65:
            raise ValueError("Hematocrit must be between 0.15 and 0.65 (15-65%)")
        
        if not 0.0 <= current_fibrinogen <= 1000.0:
            raise ValueError("Current fibrinogen must be between 0.0 and 1000.0 mg/dL")
        
        if not 50.0 <= target_fibrinogen <= 500.0:
            raise ValueError("Target fibrinogen must be between 50.0 and 500.0 mg/dL")
        
        if current_fibrinogen >= target_fibrinogen:
            raise ValueError("Target fibrinogen must be higher than current fibrinogen")
        
        if not 150.0 <= fibrinogen_per_unit <= 300.0:
            raise ValueError("Fibrinogen per unit must be between 150.0 and 300.0 mg")
    
    def _calculate_plasma_volume(self, weight: float, sex: str, hematocrit: float) -> float:
        """
        Calculate plasma volume in deciliters
        
        Formula: Plasma Volume (dL) = Weight (kg) × Factor × (1 - Hematocrit)
        Factor: 0.07 for males, 0.065 for females
        """
        
        factor = self.MALE_PLASMA_FACTOR if sex == "male" else self.FEMALE_PLASMA_FACTOR
        plasma_volume = weight * factor * (1 - hematocrit)
        
        return plasma_volume
    
    def _get_interpretation(self, units_required: int, current_fibrinogen: float,
                          target_fibrinogen: float, patient_weight: float) -> Dict[str, str]:
        """
        Determines the interpretation based on the units required
        
        Args:
            units_required (int): Number of cryoprecipitate units required
            current_fibrinogen (float): Current fibrinogen level
            target_fibrinogen (float): Target fibrinogen level
            patient_weight (float): Patient weight in kg
            
        Returns:
            Dict with interpretation
        """
        
        if units_required <= 5:
            return {
                "stage": "Low Dose",
                "description": "Small fibrinogen replacement",
                "interpretation": (f"Calculated dose of {units_required} cryoprecipitate units "
                                 f"represents a small fibrinogen replacement to increase levels from "
                                 f"{current_fibrinogen} to {target_fibrinogen} mg/dL. Monitor response "
                                 f"with repeat fibrinogen levels 1-2 hours post-transfusion.")
            }
        elif units_required <= 15:
            return {
                "stage": "Standard Dose",
                "description": "Typical therapeutic replacement",
                "interpretation": (f"Calculated dose of {units_required} cryoprecipitate units "
                                 f"represents standard therapeutic replacement. Consider using pooled "
                                 f"units (typically 10 units per pool) for efficient administration. "
                                 f"This dose should increase fibrinogen from {current_fibrinogen} to "
                                 f"approximately {target_fibrinogen} mg/dL.")
            }
        elif units_required <= 30:
            return {
                "stage": "High Dose",
                "description": "Large fibrinogen replacement",
                "interpretation": (f"Calculated dose of {units_required} cryoprecipitate units "
                                 f"represents a high dose replacement. Consider alternative therapies "
                                 f"like fibrinogen concentrate for more efficient administration. "
                                 f"Monitor for volume overload in patients with cardiac or renal compromise.")
            }
        else:
            return {
                "stage": "Very High Dose",
                "description": "Massive fibrinogen replacement",
                "interpretation": (f"Calculated dose of {units_required} cryoprecipitate units "
                                 f"represents a very high dose requirement. Strongly consider "
                                 f"fibrinogen concentrate instead of cryoprecipitate for this patient. "
                                 f"Ensure adequate vascular access and monitor closely for complications "
                                 f"including volume overload and transfusion reactions.")
            }
    
    def _get_clinical_considerations(self, units_required: int, current_fibrinogen: float,
                                   target_fibrinogen: float) -> Dict[str, Any]:
        """Get clinical considerations based on the dose and fibrinogen levels"""
        
        considerations = []
        
        # Critical fibrinogen level
        if current_fibrinogen < self.CRITICAL_FIBRINOGEN:
            considerations.append("CRITICAL: Current fibrinogen <50 mg/dL requires urgent replacement")
        
        # High target for bleeding
        if target_fibrinogen >= self.MAJOR_BLEEDING_TARGET:
            considerations.append("Target appropriate for major bleeding or surgery")
        
        # Large dose considerations
        if units_required > 20:
            considerations.append("Consider fibrinogen concentrate for large dose requirements")
            considerations.append("Monitor for volume overload")
            considerations.append("Ensure adequate vascular access")
        
        # Standard monitoring
        considerations.append("Monitor response with repeat fibrinogen levels 1-2 hours post-transfusion")
        considerations.append("Each unit is approximately 15-20 mL volume")
        
        # Pooled units
        if 8 <= units_required <= 12:
            considerations.append("Consider requesting 1 pooled unit (10 units) for convenience")
        elif 18 <= units_required <= 22:
            considerations.append("Consider requesting 2 pooled units (20 units) for convenience")
        
        return {
            "monitoring": "Repeat fibrinogen levels 1-2 hours post-transfusion",
            "administration": "Cryoprecipitate should be ABO compatible when possible",
            "special_considerations": considerations,
            "volume_consideration": f"Total volume approximately {units_required * 17.5:.0f} mL"
        }
    
    def _get_alternative_dosing(self, weight: float, fibrinogen_increase: float) -> Dict[str, Any]:
        """Provide alternative dosing methods for comparison"""
        
        # Weight-based dosing: 1 unit per 5-10 kg increases fibrinogen by ~60-100 mg/dL
        units_per_5kg = weight / 5
        units_per_10kg = weight / 10
        
        # Simple rule: 0.2 × weight (kg) for ~100 mg/dL increase
        simple_rule_units = 0.2 * weight * (fibrinogen_increase / 100)
        
        return {
            "weight_based_5kg": {
                "units": math.ceil(units_per_5kg),
                "description": "1 unit per 5 kg (increases fibrinogen ~100 mg/dL)",
                "note": "Simple weight-based dosing method"
            },
            "weight_based_10kg": {
                "units": math.ceil(units_per_10kg),
                "description": "1 unit per 10 kg (increases fibrinogen ~60-100 mg/dL)",
                "note": "Conservative weight-based dosing method"
            },
            "simple_rule": {
                "units": math.ceil(simple_rule_units),
                "description": f"0.2 × weight × (target increase/100)",
                "note": "Simple calculation rule for comparison"
            },
            "standard_adult_dose": {
                "units": 10,
                "description": "Standard adult dose (1 pooled unit)",
                "note": "Typical starting dose for adults, increases fibrinogen ~50-100 mg/dL"
            }
        }


def calculate_cryoprecipitate_dosing(patient_weight: float, patient_sex: str, hematocrit: float,
                                   current_fibrinogen: float, target_fibrinogen: float,
                                   fibrinogen_per_unit: Optional[float] = None) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = CryoprecipitateDosing Calculator()
    return calculator.calculate(patient_weight, patient_sex, hematocrit,
                              current_fibrinogen, target_fibrinogen, fibrinogen_per_unit)