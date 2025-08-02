"""
Maintenance Fluids Calculations (Holliday-Segar Method)

Calculates maintenance fluid requirements by weight using the evidence-based
Holliday-Segar method developed in 1957.

References:
- Holliday MA, Segar WE. The maintenance need for water in parenteral fluid therapy. Pediatrics. 1957;19(5):823-32.
- Moritz ML, Ayus JC. Prevention of hospital-acquired hyponatremia: a case for using isotonic saline. Pediatrics. 2003;111(2):227-30.
"""

import math
from typing import Dict, Any


class MaintenanceFluidsCalculator:
    """Calculator for Maintenance Fluids using Holliday-Segar Method"""
    
    def __init__(self):
        # Holliday-Segar method constants
        self.FIRST_10KG_RATE = 100  # mL/kg/day for first 10 kg
        self.SECOND_10KG_RATE = 50  # mL/kg/day for next 10 kg (10-20 kg)
        self.ABOVE_20KG_RATE = 20   # mL/kg/day for each kg above 20 kg
        
        self.FIRST_10KG_BASE = 1000   # mL/day for first 10 kg
        self.SECOND_10KG_BASE = 1500  # mL/day for first 20 kg
    
    def calculate(self, weight: float) -> Dict[str, Any]:
        """
        Calculates maintenance fluid requirements using the Holliday-Segar method
        
        Args:
            weight (float): Patient weight in kilograms (0.5-200.0 kg)
            
        Returns:
            Dict with fluid requirements per day and per hour
        """
        
        # Validations
        self._validate_inputs(weight)
        
        # Calculate daily maintenance fluids
        daily_fluids = self._calculate_daily_maintenance(weight)
        
        # Calculate hourly rate
        hourly_rate = daily_fluids / 24
        
        # Get interpretation
        interpretation = self._get_interpretation(daily_fluids, hourly_rate, weight)
        
        return {
            "result": {
                "daily_maintenance": round(daily_fluids, 1),
                "hourly_rate": round(hourly_rate, 1),
                "weight_category": self._get_weight_category(weight)
            },
            "unit": "mL",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, weight):
        """Validates input parameters"""
        
        if not isinstance(weight, (int, float)) or weight <= 0:
            raise ValueError("Weight must be a positive number")
        
        if weight < 0.5:
            raise ValueError("Weight must be at least 0.5 kg")
        
        if weight > 200.0:
            raise ValueError("Weight must be no more than 200 kg")
    
    def _calculate_daily_maintenance(self, weight: float) -> float:
        """Implements the Holliday-Segar maintenance fluid calculation"""
        
        if weight <= 10:
            # First 10 kg: 100 mL/kg/day
            daily_fluids = weight * self.FIRST_10KG_RATE
        elif weight <= 20:
            # First 10 kg: 1000 mL + 50 mL/kg for each kg over 10
            excess_weight = weight - 10
            daily_fluids = self.FIRST_10KG_BASE + (excess_weight * self.SECOND_10KG_RATE)
        else:
            # Over 20 kg: 1500 mL + 20 mL/kg for each kg over 20
            excess_weight = weight - 20
            daily_fluids = self.SECOND_10KG_BASE + (excess_weight * self.ABOVE_20KG_RATE)
        
        return daily_fluids
    
    def _get_weight_category(self, weight: float) -> str:
        """Determines weight category for appropriate formula"""
        
        if weight <= 10:
            return "≤10 kg (100 mL/kg/day)"
        elif weight <= 20:
            return "10-20 kg (1000 mL + 50 mL/kg for each kg >10)"
        else:
            return ">20 kg (1500 mL + 20 mL/kg for each kg >20)"
    
    def _get_interpretation(self, daily_fluids: float, hourly_rate: float, weight: float) -> Dict[str, str]:
        """
        Provides clinical interpretation of the maintenance fluid calculation
        
        Args:
            daily_fluids (float): Daily maintenance fluid requirement in mL
            hourly_rate (float): Hourly maintenance fluid rate in mL/hr
            weight (float): Patient weight in kg
            
        Returns:
            Dict with interpretation
        """
        
        # Determine if pediatric or adult
        patient_type = "pediatric" if weight < 50 else "adult"
        
        # Base interpretation
        interpretation = (
            f"Maintenance fluid requirement: {daily_fluids:.1f} mL/day ({hourly_rate:.1f} mL/hr). "
            f"This calculation uses the Holliday-Segar method for {patient_type} patients. "
        )
        
        # Add clinical considerations
        interpretation += (
            "Consider using isotonic solutions (normal saline or lactated Ringer's) to prevent "
            "hyponatremia. Adjust for clinical condition, ongoing losses (fever, diarrhea, drainage), "
            "and fluid balance status. Monitor electrolytes and urine output regularly. "
        )
        
        # Weight-specific considerations
        if weight < 3:
            interpretation += (
                "Neonatal patient - consider specialist consultation for fluid management as "
                "standard formulas may not apply. Monitor closely for fluid overload."
            )
        elif weight < 10:
            interpretation += (
                "Pediatric patient - monitor for signs of dehydration or fluid overload. "
                "Adjust for fever (increase by 10-15% for each degree >37°C)."
            )
        elif weight > 100:
            interpretation += (
                "Large patient - consider clinical condition and comorbidities. May need "
                "fluid restriction in heart failure, renal disease, or liver disease."
            )
        
        return {
            "stage": "Maintenance Requirements",
            "description": "Standard maintenance fluid calculation",
            "interpretation": interpretation
        }


def calculate_maintenance_fluids_calculations(weight) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = MaintenanceFluidsCalculator()
    return calculator.calculate(weight)