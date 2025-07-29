"""
Bicarbonate Deficit Calculator

Calculates total body bicarbonate deficit for assessment of metabolic acidosis severity.

References (Vancouver style):
1. Kurtz I. Acid-Base Case Studies. 2nd Ed. Trafford Publishing (2004); 68:150.
2. Forsythe SM, Schmidt GA. Sodium bicarbonate for the treatment of lactic acidosis. 
   Chest. 2000;117(1):260.
3. Kollef MH, et al. The Washington Manual of Critical Care. Lippincott Williams & Wilkins, 
   2007; p185:583.
4. Sabatini S, Kurtzman NA. Bicarbonate Therapy in Severe Metabolic Acidosis. 
   JASN. 2009;20(4):692-695.
"""

from typing import Dict, Any, Optional


class BicarbonateDeficitCalculator:
    """Calculator for Bicarbonate Deficit"""
    
    def __init__(self):
        # Constants
        self.DISTRIBUTION_COEFFICIENT = 0.4  # Distribution volume coefficient for bicarbonate
        self.DEFAULT_TARGET_BICARBONATE = 24.0  # mEq/L
        self.NORMAL_BICARBONATE_MIN = 23.0  # mEq/L
        self.NORMAL_BICARBONATE_MAX = 28.0  # mEq/L
    
    def calculate(self, weight: float, bicarbonate_level: float, 
                  target_bicarbonate: Optional[float] = None) -> Dict[str, Any]:
        """
        Calculates the bicarbonate deficit
        
        Args:
            weight: Patient weight in kilograms
            bicarbonate_level: Current serum bicarbonate level in mEq/L
            target_bicarbonate: Target bicarbonate level in mEq/L (default: 24)
            
        Returns:
            Dict with the bicarbonate deficit and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(weight, bicarbonate_level, target_bicarbonate)
        
        # Use default target if not provided
        if target_bicarbonate is None:
            target_bicarbonate = self.DEFAULT_TARGET_BICARBONATE
        
        # Calculate bicarbonate deficit using the formula
        deficit = self._calculate_deficit(weight, bicarbonate_level, target_bicarbonate)
        
        # Generate interpretation
        interpretation = self._generate_interpretation(
            bicarbonate_level, target_bicarbonate, deficit, weight
        )
        
        return {
            "result": round(deficit, 1),
            "unit": "mEq",
            "interpretation": interpretation,
            "stage": self._get_severity_stage(bicarbonate_level),
            "stage_description": self._get_stage_description(bicarbonate_level)
        }
    
    def _validate_inputs(self, weight: float, bicarbonate_level: float, 
                        target_bicarbonate: Optional[float]) -> None:
        """Validates input parameters"""
        
        if weight < 0.5 or weight > 500:
            raise ValueError("Weight must be between 0.5 and 500 kg")
        
        if bicarbonate_level < 4 or bicarbonate_level > 60:
            raise ValueError("Bicarbonate level must be between 4 and 60 mEq/L")
        
        if target_bicarbonate is not None and (target_bicarbonate < 15 or target_bicarbonate > 30):
            raise ValueError("Target bicarbonate must be between 15 and 30 mEq/L")
    
    def _calculate_deficit(self, weight: float, current_hco3: float, 
                          target_hco3: float) -> float:
        """Calculates the bicarbonate deficit using the standard formula"""
        
        # Bicarbonate Deficit = 0.4 × Weight (kg) × (Target HCO3 - Current HCO3)
        deficit = self.DISTRIBUTION_COEFFICIENT * weight * (target_hco3 - current_hco3)
        
        # If current level is higher than target, deficit is negative (no replacement needed)
        return max(0, deficit)
    
    def _get_severity_stage(self, bicarbonate_level: float) -> str:
        """Determines the severity stage based on bicarbonate level"""
        
        if bicarbonate_level >= self.NORMAL_BICARBONATE_MIN:
            return "Normal"
        elif bicarbonate_level >= 18:
            return "Mild Acidosis"
        elif bicarbonate_level >= 15:
            return "Moderate Acidosis"
        else:
            return "Severe Acidosis"
    
    def _get_stage_description(self, bicarbonate_level: float) -> str:
        """Provides description for the severity stage"""
        
        if bicarbonate_level >= self.NORMAL_BICARBONATE_MIN:
            return "Normal bicarbonate levels"
        elif bicarbonate_level >= 18:
            return "Mild metabolic acidosis"
        elif bicarbonate_level >= 15:
            return "Moderate metabolic acidosis"
        else:
            return "Severe metabolic acidosis"
    
    def _generate_interpretation(self, current_hco3: float, target_hco3: float, 
                               deficit: float, weight: float) -> str:
        """Generates detailed interpretation of the calculation"""
        
        interpretation_parts = []
        
        # Current bicarbonate status
        if current_hco3 >= self.NORMAL_BICARBONATE_MIN:
            interpretation_parts.append(
                f"Current bicarbonate level ({current_hco3} mEq/L) is within normal range "
                f"({self.NORMAL_BICARBONATE_MIN}-{self.NORMAL_BICARBONATE_MAX} mEq/L). "
                "No bicarbonate replacement needed."
            )
        elif current_hco3 >= 18:
            interpretation_parts.append(
                f"Mild metabolic acidosis (HCO3 = {current_hco3} mEq/L). "
                "Monitor patient and treat underlying cause."
            )
        elif current_hco3 >= 15:
            interpretation_parts.append(
                f"Moderate metabolic acidosis (HCO3 = {current_hco3} mEq/L). "
                "Consider bicarbonate replacement depending on clinical context."
            )
        else:
            interpretation_parts.append(
                f"Severe metabolic acidosis (HCO3 = {current_hco3} mEq/L). "
                "Bicarbonate replacement may be indicated."
            )
        
        # Deficit calculation result
        if deficit > 0:
            interpretation_parts.append(
                f"Estimated bicarbonate deficit: {deficit:.1f} mEq. "
                f"This represents the total body bicarbonate needed to reach {target_hco3} mEq/L."
            )
            
            # Dosing recommendations
            if deficit > 0:
                initial_dose = deficit * 0.5  # Give half the calculated deficit initially
                interpretation_parts.append(
                    f"Consider initial replacement of {initial_dose:.0f} mEq (50% of calculated deficit), "
                    "then reassess with repeat arterial blood gas."
                )
        else:
            interpretation_parts.append("No bicarbonate deficit calculated.")
        
        # Clinical pearls
        interpretation_parts.append(
            "Remember: treat underlying cause of acidosis, avoid overly rapid correction, "
            "and monitor for complications of bicarbonate therapy."
        )
        
        return " ".join(interpretation_parts)


def calculate_bicarbonate_deficit(weight: float, bicarbonate_level: float, 
                                target_bicarbonate: Optional[float] = None) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = BicarbonateDeficitCalculator()
    return calculator.calculate(weight, bicarbonate_level, target_bicarbonate)