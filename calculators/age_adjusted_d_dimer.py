"""
Age-Adjusted D-dimer for Venous Thromboembolism (VTE) Calculator

Adjusts D-dimer cutoffs to help rule out VTE in patients ≥50 years old, improving 
specificity while maintaining sensitivity.

Based on the ADJUST-PE study and systematic reviews showing that age-adjusted 
D-dimer cutoffs are more specific as patient age increases, with minimal reduction 
in sensitivity. This helps prevent unnecessary imaging in elderly patients.

References:
- Schouten HJ, Geersing GJ, Koek HL, et al. Diagnostic accuracy of conventional 
  or age adjusted D-dimer cut-off values in older patients with suspected venous 
  thromboembolism: systematic review and meta-analysis. BMJ. 2013;346:f2492.
- Righini M, Van Es J, Den Exter PL, et al. Age-adjusted D-dimer cutoff levels 
  to rule out pulmonary embolism: the ADJUST-PE study. JAMA. 2014;311(11):1117-1124.
"""

from typing import Dict, Any, Optional


class AgeAdjustedDDimerCalculator:
    """Calculator for Age-Adjusted D-dimer for VTE"""
    
    def __init__(self):
        # Multipliers for different D-dimer unit types
        self.MULTIPLIERS = {
            'FEU': 10,  # Fibrinogen Equivalent Units
            'DDU': 5    # D-dimer Units
        }
        
        # Conventional cutoffs for reference
        self.CONVENTIONAL_CUTOFFS = {
            'FEU': 500,  # µg/L
            'DDU': 250   # µg/L
        }
    
    def calculate(self, age: int, d_dimer_unit_type: str, 
                 d_dimer_level: Optional[float] = None) -> Dict[str, Any]:
        """
        Calculates the age-adjusted D-dimer cutoff using the provided parameters
        
        Args:
            age (int): Patient age in years (must be ≥50)
            d_dimer_unit_type (str): Type of D-dimer units ("FEU" or "DDU")
            d_dimer_level (float, optional): Measured D-dimer level for comparison
            
        Returns:
            Dict with the result and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(age, d_dimer_unit_type, d_dimer_level)
        
        # Calculate age-adjusted cutoff
        cutoff = self._calculate_cutoff(age, d_dimer_unit_type)
        
        # Get interpretation
        interpretation = self._get_interpretation(cutoff, d_dimer_level, d_dimer_unit_type)
        
        return {
            "result": cutoff,
            "unit": "µg/L",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"],
            "conventional_cutoff": self.CONVENTIONAL_CUTOFFS[d_dimer_unit_type],
            "measured_d_dimer": d_dimer_level,
            "vte_ruled_out": d_dimer_level is not None and d_dimer_level <= cutoff
        }
    
    def _validate_inputs(self, age: int, d_dimer_unit_type: str, 
                        d_dimer_level: Optional[float]):
        """Validates input parameters"""
        
        # Validate age
        if not isinstance(age, int):
            raise ValueError("Age must be an integer")
        
        if age < 50:
            raise ValueError("Age-adjusted D-dimer is only applicable to patients ≥50 years old")
        
        if age > 120:
            raise ValueError("Age must be ≤120 years")
        
        # Validate D-dimer unit type
        if not isinstance(d_dimer_unit_type, str):
            raise ValueError("D-dimer unit type must be a string")
        
        if d_dimer_unit_type not in self.MULTIPLIERS:
            raise ValueError("D-dimer unit type must be 'FEU' or 'DDU'")
        
        # Validate D-dimer level if provided
        if d_dimer_level is not None:
            if not isinstance(d_dimer_level, (int, float)):
                raise ValueError("D-dimer level must be a number")
            
            if d_dimer_level < 0:
                raise ValueError("D-dimer level cannot be negative")
            
            if d_dimer_level > 10000:
                raise ValueError("D-dimer level seems unusually high (>10,000 µg/L)")
    
    def _calculate_cutoff(self, age: int, d_dimer_unit_type: str) -> float:
        """Calculates the age-adjusted D-dimer cutoff"""
        
        multiplier = self.MULTIPLIERS[d_dimer_unit_type]
        cutoff = age * multiplier
        
        return float(cutoff)
    
    def _get_interpretation(self, cutoff: float, d_dimer_level: Optional[float], 
                          unit_type: str) -> Dict[str, str]:
        """
        Determines the interpretation based on the cutoff and measured level
        
        Args:
            cutoff (float): Calculated age-adjusted cutoff
            d_dimer_level (float, optional): Measured D-dimer level
            unit_type (str): D-dimer unit type
            
        Returns:
            Dict with interpretation details
        """
        
        conventional_cutoff = self.CONVENTIONAL_CUTOFFS[unit_type]
        
        if d_dimer_level is not None:
            if d_dimer_level <= cutoff:
                interpretation = (
                    f"VTE diagnosis UNLIKELY. Measured D-dimer ({d_dimer_level} µg/L) is "
                    f"≤ age-adjusted cutoff ({cutoff} µg/L). No further testing needed. "
                    f"Note: Age-adjusted cutoff ({cutoff} µg/L) is higher than conventional "
                    f"cutoff ({conventional_cutoff} µg/L), allowing safe rule-out in elderly patients."
                )
                stage = "VTE Ruled Out"
                description = "D-dimer below age-adjusted cutoff"
            else:
                interpretation = (
                    f"VTE cannot be ruled out. Measured D-dimer ({d_dimer_level} µg/L) is "
                    f"> age-adjusted cutoff ({cutoff} µg/L). Proceed with imaging (CTA or V/Q scan). "
                    f"Remember that elevated D-dimer can have many causes besides VTE."
                )
                stage = "Further Testing Required"
                description = "D-dimer above age-adjusted cutoff"
        else:
            interpretation = (
                f"Age-adjusted D-dimer cutoff is {cutoff} µg/L ({unit_type} units). "
                f"This is higher than the conventional cutoff of {conventional_cutoff} µg/L, "
                f"providing better specificity in elderly patients. If measured D-dimer "
                f"≤ {cutoff} µg/L: VTE unlikely, no imaging needed. If > {cutoff} µg/L: "
                f"proceed with imaging."
            )
            stage = "Age-Adjusted Cutoff"
            description = "Calculated age-adjusted D-dimer cutoff"
        
        return {
            "stage": stage,
            "description": description,
            "interpretation": interpretation
        }


def calculate_age_adjusted_d_dimer(age: int, d_dimer_unit_type: str, 
                                  d_dimer_level: Optional[float] = None) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_age_adjusted_d_dimer pattern
    """
    calculator = AgeAdjustedDDimerCalculator()
    return calculator.calculate(
        age=age,
        d_dimer_unit_type=d_dimer_unit_type,
        d_dimer_level=d_dimer_level
    )