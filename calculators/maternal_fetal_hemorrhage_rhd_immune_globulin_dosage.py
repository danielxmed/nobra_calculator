"""
Maternal-Fetal Hemorrhage Rh(D) Immune Globulin Dosage Calculator

Calculates the amount of RhIG (RhoGAM) to be administered to Rh-negative mother
following maternal-fetal hemorrhage to prevent hemolytic disease of the fetus
and newborn (HDFN).

References:
1. AABB Technical Manual, 18th edition. American Association of Blood Banks; 2014.
2. American College of Obstetricians and Gynecologists. Prevention of Rh D alloimmunization. 
   ACOG Practice Bulletin No. 4. Washington, DC: American College of Obstetricians and 
   Gynecologists; 1999.
3. Bowman JM. The prevention of Rh immunization. Transfus Med Rev. 1988;2(3):129-50. 
   doi: 10.1016/s0887-7963(88)70067-9.
"""

import math
from typing import Dict, Any


class MaternalFetalHemorrhageRhdImmuneGlobulinDosageCalculator:
    """Calculator for Maternal-Fetal Hemorrhage Rh(D) Immune Globulin Dosage"""
    
    def __init__(self):
        # Standard RhIG vial parameters
        self.STANDARD_VIAL_DOSE_MCG = 300  # 300 μg per vial
        self.PROTECTION_VOLUME_ML = 30  # Each vial protects against 30 mL fetal whole blood
        self.FETAL_RBC_PROTECTION_ML = 15  # Or 15 mL of fetal red blood cells
        
        # Clinical thresholds
        self.NORMAL_BASELINE_PERCENTAGE = 0.1  # Normal baseline fetal cells <0.1%
        self.CLINICAL_SIGNIFICANCE_THRESHOLD = 0.3  # Clinical significance >0.3%
        
        # Dosing thresholds for interpretation
        self.MODERATE_HEMORRHAGE_THRESHOLD = 2
        self.LARGE_HEMORRHAGE_THRESHOLD = 4
        self.MASSIVE_HEMORRHAGE_THRESHOLD = 11
        
        # Safety margin
        self.SAFETY_MARGIN_VIALS = 1  # Add 1 additional vial for safety
    
    def calculate(self, maternal_blood_volume: float, fetal_cell_percentage: float) -> Dict[str, Any]:
        """
        Calculates RhIG dosage for maternal-fetal hemorrhage
        
        Args:
            maternal_blood_volume (float): Total maternal blood volume in mL
            fetal_cell_percentage (float): Percentage of fetal cells in maternal blood
            
        Returns:
            Dict with the result and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(maternal_blood_volume, fetal_cell_percentage)
        
        # Calculate fetal blood volume in maternal circulation
        fetal_blood_volume = self._calculate_fetal_blood_volume(
            maternal_blood_volume, fetal_cell_percentage
        )
        
        # Calculate required RhIG vials
        required_vials = self._calculate_rhig_vials(fetal_blood_volume)
        
        # Get clinical assessment
        clinical_assessment = self._get_clinical_assessment(
            fetal_cell_percentage, fetal_blood_volume, required_vials
        )
        
        # Get interpretation
        interpretation = self._get_interpretation(required_vials)
        
        return {
            "result": {
                "total_vials": required_vials,
                "fetal_blood_volume_ml": round(fetal_blood_volume, 2),
                "calculated_vials_raw": round(fetal_blood_volume / self.PROTECTION_VOLUME_ML, 2),
                "safety_margin_applied": self.SAFETY_MARGIN_VIALS,
                "vial_strength_mcg": self.STANDARD_VIAL_DOSE_MCG,
                "total_dose_mcg": required_vials * self.STANDARD_VIAL_DOSE_MCG,
                "protection_per_vial_ml": self.PROTECTION_VOLUME_ML,
                "clinical_assessment": clinical_assessment
            },
            "unit": "vials",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, maternal_blood_volume: float, fetal_cell_percentage: float):
        """Validates input parameters"""
        
        # Validate maternal blood volume
        if not isinstance(maternal_blood_volume, (int, float)):
            raise ValueError("Maternal blood volume must be a number")
        
        if maternal_blood_volume < 2000 or maternal_blood_volume > 6000:
            raise ValueError("Maternal blood volume must be between 2000 and 6000 mL")
        
        # Validate fetal cell percentage
        if not isinstance(fetal_cell_percentage, (int, float)):
            raise ValueError("Fetal cell percentage must be a number")
        
        if fetal_cell_percentage < 0 or fetal_cell_percentage > 10:
            raise ValueError("Fetal cell percentage must be between 0 and 10%")
    
    def _calculate_fetal_blood_volume(self, maternal_blood_volume: float, 
                                    fetal_cell_percentage: float) -> float:
        """
        Calculates volume of fetal blood in maternal circulation
        
        Args:
            maternal_blood_volume (float): Total maternal blood volume in mL
            fetal_cell_percentage (float): Percentage of fetal cells
            
        Returns:
            float: Volume of fetal blood in mL
        """
        
        # Convert percentage to decimal and calculate fetal blood volume
        fetal_blood_volume = maternal_blood_volume * (fetal_cell_percentage / 100)
        
        return fetal_blood_volume
    
    def _calculate_rhig_vials(self, fetal_blood_volume: float) -> int:
        """
        Calculates number of RhIG vials required using standard rounding rules
        
        Args:
            fetal_blood_volume (float): Volume of fetal blood in mL
            
        Returns:
            int: Number of 300 μg RhIG vials required
        """
        
        # Calculate raw number of vials needed
        raw_vials = fetal_blood_volume / self.PROTECTION_VOLUME_ML
        
        # Apply rounding rules
        # If decimal < 0.5, round up to next whole number
        # If decimal ≥ 0.5, round up and add 1 additional vial
        decimal_part = raw_vials - math.floor(raw_vials)
        
        if decimal_part == 0:
            # Exact whole number, add safety margin
            calculated_vials = int(raw_vials) + self.SAFETY_MARGIN_VIALS
        elif decimal_part < 0.5:
            # Round up to next whole number
            calculated_vials = math.ceil(raw_vials)
        else:
            # Round up and add 1 additional vial
            calculated_vials = math.ceil(raw_vials) + 1
        
        # Minimum of 1 vial
        return max(1, calculated_vials)
    
    def _get_clinical_assessment(self, fetal_cell_percentage: float, 
                               fetal_blood_volume: float, required_vials: int) -> Dict[str, Any]:
        """
        Provides clinical assessment of the hemorrhage severity
        
        Args:
            fetal_cell_percentage (float): Percentage of fetal cells
            fetal_blood_volume (float): Volume of fetal blood in mL
            required_vials (int): Number of RhIG vials required
            
        Returns:
            Dict with clinical assessment data
        """
        
        # Determine clinical significance
        if fetal_cell_percentage < self.NORMAL_BASELINE_PERCENTAGE:
            significance = "Normal baseline"
            risk_level = "Minimal"
        elif fetal_cell_percentage < self.CLINICAL_SIGNIFICANCE_THRESHOLD:
            significance = "Below clinical significance threshold"
            risk_level = "Low"
        else:
            significance = "Clinically significant"
            risk_level = "Significant"
        
        # Determine hemorrhage severity
        if required_vials == 1:
            severity = "Minimal hemorrhage"
        elif required_vials < self.MODERATE_HEMORRHAGE_THRESHOLD:
            severity = "Small hemorrhage"
        elif required_vials < self.LARGE_HEMORRHAGE_THRESHOLD:
            severity = "Moderate hemorrhage"
        elif required_vials < self.MASSIVE_HEMORRHAGE_THRESHOLD:
            severity = "Large hemorrhage"
        else:
            severity = "Massive hemorrhage"
        
        # Calculate protection coverage
        total_protection_ml = required_vials * self.PROTECTION_VOLUME_ML
        coverage_ratio = (total_protection_ml / fetal_blood_volume) if fetal_blood_volume > 0 else 0
        
        return {
            "fetal_cell_significance": significance,
            "alloimmunization_risk": risk_level,
            "hemorrhage_severity": severity,
            "total_protection_ml": total_protection_ml,
            "coverage_ratio": round(coverage_ratio, 2),
            "baseline_comparison": f"{fetal_cell_percentage / self.NORMAL_BASELINE_PERCENTAGE:.1f}x normal baseline" if fetal_cell_percentage > 0 else "At baseline",
            "time_sensitivity": "Administer within 72 hours for optimal efficacy",
            "follow_up_needed": required_vials > 3
        }
    
    def _get_interpretation(self, required_vials: int) -> Dict[str, str]:
        """
        Determines the clinical interpretation based on vial count
        
        Args:
            required_vials (int): Number of RhIG vials required
            
        Returns:
            Dict with interpretation details
        """
        
        if required_vials == 1:
            return {
                "stage": "Standard Dose",
                "description": "Minimal maternal-fetal hemorrhage",
                "interpretation": (
                    f"Standard single dose of {self.STANDARD_VIAL_DOSE_MCG} μg RhIG (1 vial) is "
                    f"sufficient to prevent alloimmunization. This covers fetal blood exposure "
                    f"up to {self.PROTECTION_VOLUME_ML} mL and represents the standard prophylactic "
                    f"dose for routine deliveries. Administer within 72 hours of delivery or "
                    f"hemorrhage event for optimal efficacy. Monitor for signs of maternal "
                    f"alloimmunization in subsequent pregnancies."
                )
            }
        elif required_vials <= 3:
            return {
                "stage": "Moderate Hemorrhage",
                "description": "Moderate maternal-fetal hemorrhage",
                "interpretation": (
                    f"Moderate hemorrhage requiring {required_vials} vials of {self.STANDARD_VIAL_DOSE_MCG} μg "
                    f"RhIG (total dose: {required_vials * self.STANDARD_VIAL_DOSE_MCG} μg). Each vial provides "
                    f"protection against {self.PROTECTION_VOLUME_ML} mL of fetal blood. Total protection "
                    f"coverage: {required_vials * self.PROTECTION_VOLUME_ML} mL. Administer within 72 hours "
                    f"for optimal efficacy. Consider follow-up Kleihauer-Betke testing to confirm "
                    f"adequate coverage and monitor for maternal alloimmunization."
                )
            }
        elif required_vials <= 10:
            return {
                "stage": "Large Hemorrhage",
                "description": "Large maternal-fetal hemorrhage",
                "interpretation": (
                    f"Significant hemorrhage requiring {required_vials} vials of {self.STANDARD_VIAL_DOSE_MCG} μg "
                    f"RhIG (total dose: {required_vials * self.STANDARD_VIAL_DOSE_MCG} μg). This represents a "
                    f"substantial fetal-maternal bleeding episode requiring aggressive prophylaxis. "
                    f"Total protection coverage: {required_vials * self.PROTECTION_VOLUME_ML} mL of fetal blood. "
                    f"Recommend obstetric consultation, follow-up Kleihauer-Betke testing to ensure "
                    f"adequate coverage, and intensive monitoring for maternal alloimmunization. "
                    f"Consider hematology consultation for complex cases."
                )
            }
        else:  # Massive hemorrhage
            return {
                "stage": "Massive Hemorrhage",
                "description": "Massive maternal-fetal hemorrhage",
                "interpretation": (
                    f"Massive hemorrhage requiring {required_vials} vials of {self.STANDARD_VIAL_DOSE_MCG} μg "
                    f"RhIG (total dose: {required_vials * self.STANDARD_VIAL_DOSE_MCG} μg). This is a rare "
                    f"but serious event requiring immediate obstetric and hematology consultation. "
                    f"Total protection coverage: {required_vials * self.PROTECTION_VOLUME_ML} mL of fetal blood. "
                    f"Consider intravenous RhIG administration if available, intensive monitoring, "
                    f"and potential need for exchange transfusion protocols. Urgent maternal-fetal "
                    f"medicine consultation recommended. Serial monitoring for adequate suppression "
                    f"of anti-D formation is essential."
                )
            }


def calculate_maternal_fetal_hemorrhage_rhd_immune_globulin_dosage(
    maternal_blood_volume: float, fetal_cell_percentage: float) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = MaternalFetalHemorrhageRhdImmuneGlobulinDosageCalculator()
    return calculator.calculate(maternal_blood_volume, fetal_cell_percentage)