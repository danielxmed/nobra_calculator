"""
Body Roundness Index (BRI) Calculator

Estimates % body fat and % visceral adipose tissue (VAT) based on waist 
circumference and height using a geometric model of body shape.

References:
1. Thomas DM, et al. Obesity (Silver Spring). 2013;21(11):2264-71.
2. Zhang X, et al. JAMA Netw Open. 2024;7(6):e2415051.
"""

import math
from typing import Dict, Any


class BodyRoundnessIndexCalculator:
    """Calculator for Body Roundness Index (BRI)"""
    
    def __init__(self):
        # Formula constants
        self.A_CONSTANT = 364.2
        self.B_CONSTANT = 365.5
        self.PI = math.pi
    
    def calculate(self, waist_circumference: float, height: float) -> Dict[str, Any]:
        """
        Calculates the Body Roundness Index using waist circumference and height
        
        Args:
            waist_circumference (float): Waist circumference in cm
            height (float): Height in cm
            
        Returns:
            Dict with the BRI result and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(waist_circumference, height)
        
        # Convert cm to meters for calculation
        waist_m = waist_circumference / 100
        height_m = height / 100
        
        # Calculate BRI using the formula:
        # BRI = 364.2 - 365.5 × √(1 - [(WC/2π) / (0.5 × H)]²)
        
        # Step 1: Calculate the ratio
        # (WC/2π) / (0.5 × H) = WC / (π × H)
        ratio = waist_m / (self.PI * height_m)
        
        # Step 2: Check if ratio is valid (must be < 1 for square root)
        if ratio >= 1:
            # This would happen if waist circumference ≥ π × height
            # which is geometrically impossible for a human body
            raise ValueError(
                f"Invalid measurements: waist circumference ({waist_circumference} cm) "
                f"is too large relative to height ({height} cm)"
            )
        
        # Step 3: Calculate the eccentricity term
        eccentricity_squared = 1 - (ratio ** 2)
        eccentricity = math.sqrt(eccentricity_squared)
        
        # Step 4: Calculate BRI
        bri = self.A_CONSTANT - self.B_CONSTANT * eccentricity
        
        # Round to 2 decimal places
        bri = round(bri, 2)
        
        # Get interpretation
        interpretation = self._get_interpretation(bri)
        
        # Calculate additional metrics
        waist_to_height_ratio = round(waist_circumference / height, 3)
        
        return {
            "result": bri,
            "unit": "index",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"],
            "additional_metrics": {
                "waist_to_height_ratio": waist_to_height_ratio,
                "eccentricity": round(eccentricity, 4)
            }
        }
    
    def _validate_inputs(self, waist_circumference: float, height: float):
        """Validates input parameters"""
        
        # Check types
        if not isinstance(waist_circumference, (int, float)):
            raise ValueError("Waist circumference must be a number")
        
        if not isinstance(height, (int, float)):
            raise ValueError("Height must be a number")
        
        # Check ranges
        if waist_circumference < 40 or waist_circumference > 200:
            raise ValueError(
                f"Waist circumference must be between 40 and 200 cm (got {waist_circumference} cm)"
            )
        
        if height < 100 or height > 250:
            raise ValueError(
                f"Height must be between 100 and 250 cm (got {height} cm)"
            )
        
        # Additional validation: waist should not exceed height
        if waist_circumference >= height:
            raise ValueError(
                "Waist circumference cannot be greater than or equal to height"
            )
    
    def _get_interpretation(self, bri: float) -> Dict[str, str]:
        """
        Determines the interpretation based on the BRI value
        
        Args:
            bri (float): Calculated BRI value
            
        Returns:
            Dict with stage, description, and interpretation
        """
        
        if bri < 3.41:
            return {
                "stage": "Low BRI",
                "description": "Low body roundness",
                "interpretation": (
                    "BRI less than 3.41 may indicate lower body fat but could suggest "
                    "moderate increase in health risks in some populations. "
                    "Hazard ratio for mortality: 0.57 (95% CI 0.49-0.67) compared to reference group. "
                    "Consider comprehensive health assessment including muscle mass and nutritional status."
                )
            }
        elif bri < 4.45:
            return {
                "stage": "Below Average BRI",
                "description": "Below average body roundness",
                "interpretation": (
                    "BRI between 3.41-4.45 shows no statistically significant increase in health risks. "
                    "Hazard ratio for mortality: 0.81 (95% CI 0.69-0.95) compared to reference group. "
                    "This range generally indicates favorable body composition."
                )
            }
        elif bri < 5.46:
            return {
                "stage": "Average BRI",
                "description": "Average body roundness (reference)",
                "interpretation": (
                    "BRI between 4.45-5.46 represents the reference range for average body roundness. "
                    "This is used as the baseline for mortality risk comparisons (HR 1.0). "
                    "Generally indicates low risk for health problems related to visceral obesity."
                )
            }
        elif bri < 6.91:
            return {
                "stage": "Above Average BRI",
                "description": "Above average body roundness",
                "interpretation": (
                    "BRI between 5.46-6.91 indicates increased body roundness with elevated health risks. "
                    "Hazard ratio for mortality: 1.48 (95% CI 1.30-1.69) compared to reference group. "
                    "Consider lifestyle modifications including diet and exercise interventions."
                )
            }
        else:  # bri >= 6.91
            return {
                "stage": "High BRI",
                "description": "High body roundness",
                "interpretation": (
                    "BRI ≥6.91 indicates significantly increased body roundness with substantial health risks. "
                    "Hazard ratio for mortality: 1.62 (95% CI 1.42-1.85) compared to reference group. "
                    "Strongly recommend comprehensive metabolic assessment and aggressive risk factor modification."
                )
            }


def calculate_body_roundness_index(waist_circumference: float, height: float) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = BodyRoundnessIndexCalculator()
    return calculator.calculate(waist_circumference, height)