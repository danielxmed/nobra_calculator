"""
Blood Volume Calculation Calculator

Calculates total blood volume, red blood cell volume, and plasma volume using 
Nadler equations and age-specific weight-based formulas. Based on the landmark 
1962 study by Nadler et al. using radioisotope labeling techniques.

References (Vancouver style):
1. Nadler SB, Hidalgo JH, Bloch T. Prediction of blood volume in normal human adults. 
   Surgery. 1962 Feb;51(2):224-32.
2. Gilcher RO, McCombs JS. Blood volume and red cell mass measurements. In: Hillman RS, 
   Ault KA, Rinder HM, editors. Hematology in Clinical Practice. 4th ed. New York: 
   McGraw-Hill; 2005. p. 595-605.
3. International Council for Standardization in Haematology. Recommended methods for 
   measurement of red-cell and plasma volume. J Nucl Med. 1980 Aug;21(8):793-800.
"""

from typing import Dict, Any, Optional


class BloodVolumeCalculationCalculator:
    """Calculator for Blood Volume Calculation using Nadler equations and age-specific formulas"""
    
    def __init__(self):
        # Weight-based blood volume multipliers (mL/kg) for pediatric patients
        self.pediatric_multipliers = {
            "preterm_neonate": 100,
            "term_neonate": 85,
            "infant_1_4_months": 75,
            "child_under_25kg": 70
        }
        
        # Nadler equation coefficients for adults/children ≥25 kg
        self.nadler_coefficients = {
            "male": {
                "height_coeff": 0.3669,
                "weight_coeff": 0.03219,
                "constant": 0.6041
            },
            "female": {
                "height_coeff": 0.3561,
                "weight_coeff": 0.03308,
                "constant": 0.1833
            }
        }
    
    def calculate(self, patient_category: str, weight: float, sex: Optional[str] = None, 
                 height: Optional[float] = None, hematocrit: Optional[float] = None) -> Dict[str, Any]:
        """
        Calculates blood volume components based on patient characteristics
        
        Args:
            patient_category (str): Patient age/weight category
            weight (float): Patient weight in kg
            sex (str, optional): Patient sex (required for Nadler equations)
            height (float, optional): Patient height in cm (required for Nadler equations)
            hematocrit (float, optional): Hematocrit percentage (for RBC/plasma volumes)
            
        Returns:
            Dict with total blood volume, RBC volume, and plasma volume
        """
        
        # Validate inputs
        self._validate_inputs(patient_category, weight, sex, height, hematocrit)
        
        # Calculate total blood volume
        total_blood_volume = self._calculate_total_blood_volume(
            patient_category, weight, sex, height
        )
        
        # Calculate RBC and plasma volumes if hematocrit provided
        rbc_volume = None
        plasma_volume = None
        
        if hematocrit is not None:
            rbc_volume = self._calculate_rbc_volume(total_blood_volume, hematocrit)
            plasma_volume = self._calculate_plasma_volume(total_blood_volume, hematocrit)
        
        # Prepare results
        results = {
            "total_blood_volume": round(total_blood_volume, 1),
            "rbc_volume": round(rbc_volume, 1) if rbc_volume is not None else None,
            "plasma_volume": round(plasma_volume, 1) if plasma_volume is not None else None
        }
        
        # Generate interpretation
        interpretation = self._get_interpretation(results, patient_category, weight)
        
        return {
            "result": results,
            "unit": "mL",
            "interpretation": interpretation,
            "stage": "Blood Volume Results",
            "stage_description": "Calculated blood volume components"
        }
    
    def _validate_inputs(self, patient_category, weight, sex, height, hematocrit):
        """Validates input parameters"""
        
        # Validate patient category
        valid_categories = list(self.pediatric_multipliers.keys()) + ["adult_or_child_25kg_plus"]
        if patient_category not in valid_categories:
            raise ValueError(f"patient_category must be one of: {valid_categories}")
        
        # Validate weight
        if not isinstance(weight, (int, float)) or weight <= 0:
            raise ValueError("weight must be a positive number")
        
        if weight < 0.5 or weight > 300:
            raise ValueError("weight must be between 0.5 and 300 kg")
        
        # Validate requirements for Nadler equations
        if patient_category == "adult_or_child_25kg_plus":
            if sex is None:
                raise ValueError("sex is required for adults/children ≥25 kg")
            if sex not in ["male", "female"]:
                raise ValueError("sex must be 'male' or 'female'")
            if height is None:
                raise ValueError("height is required for adults/children ≥25 kg")
            if not isinstance(height, (int, float)) or height <= 0:
                raise ValueError("height must be a positive number")
            if height < 30 or height > 250:
                raise ValueError("height must be between 30 and 250 cm")
        
        # Validate hematocrit if provided
        if hematocrit is not None:
            if not isinstance(hematocrit, (int, float)):
                raise ValueError("hematocrit must be a number")
            if hematocrit < 10 or hematocrit > 70:
                raise ValueError("hematocrit must be between 10 and 70%")
    
    def _calculate_total_blood_volume(self, patient_category: str, weight: float, 
                                    sex: Optional[str], height: Optional[float]) -> float:
        """
        Calculates total blood volume based on patient category
        
        Returns:
            float: Total blood volume in mL
        """
        
        if patient_category in self.pediatric_multipliers:
            # Weight-based calculation for pediatric patients
            multiplier = self.pediatric_multipliers[patient_category]
            return weight * multiplier
        
        else:  # adult_or_child_25kg_plus
            # Nadler equation calculation
            height_m = height / 100  # Convert cm to meters
            coeffs = self.nadler_coefficients[sex]
            
            total_volume = (
                coeffs["height_coeff"] * (height_m ** 3) +
                coeffs["weight_coeff"] * weight +
                coeffs["constant"]
            ) * 1000  # Convert L to mL
            
            return total_volume
    
    def _calculate_rbc_volume(self, total_blood_volume: float, hematocrit: float) -> float:
        """
        Calculates red blood cell volume
        
        Returns:
            float: RBC volume in mL
        """
        return total_blood_volume * (hematocrit / 100)
    
    def _calculate_plasma_volume(self, total_blood_volume: float, hematocrit: float) -> float:
        """
        Calculates plasma volume
        
        Returns:
            float: Plasma volume in mL
        """
        return total_blood_volume * (1 - hematocrit / 100)
    
    def _get_interpretation(self, results: Dict, patient_category: str, weight: float) -> str:
        """
        Provides clinical interpretation of blood volume results
        
        Returns:
            str: Clinical interpretation
        """
        
        total_volume = results["total_blood_volume"]
        volume_per_kg = total_volume / weight
        
        interpretation_parts = [
            f"Total blood volume: {total_volume} mL ({volume_per_kg:.1f} mL/kg)."
        ]
        
        if results["rbc_volume"] is not None and results["plasma_volume"] is not None:
            interpretation_parts.append(
                f"RBC volume: {results['rbc_volume']} mL. "
                f"Plasma volume: {results['plasma_volume']} mL."
            )
        else:
            interpretation_parts.append(
                "RBC and plasma volumes require hematocrit input for calculation."
            )
        
        # Add category-specific context
        if patient_category in self.pediatric_multipliers:
            multiplier = self.pediatric_multipliers[patient_category]
            interpretation_parts.append(
                f"Calculation based on {patient_category.replace('_', ' ')} standard of {multiplier} mL/kg."
            )
        else:
            interpretation_parts.append(
                "Calculation based on Nadler equations using height, weight, and sex."
            )
        
        interpretation_parts.append(
            "These estimates guide transfusion therapy, plasma exchange procedures, "
            "and coagulation factor dosing decisions."
        )
        
        return " ".join(interpretation_parts)


def calculate_blood_volume_calculation(patient_category: str, weight: float, 
                                     sex: Optional[str] = None, height: Optional[float] = None, 
                                     hematocrit: Optional[float] = None) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    Calculates total blood volume, RBC volume, and plasma volume using Nadler 
    equations for adults/children ≥25kg or weight-based formulas for pediatric 
    patients. Developed from Nadler's 1962 radioisotope labeling studies.
    """
    calculator = BloodVolumeCalculationCalculator()
    return calculator.calculate(patient_category, weight, sex, height, hematocrit)