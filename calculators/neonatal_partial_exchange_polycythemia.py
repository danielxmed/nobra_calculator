"""
Neonatal Partial Exchange for Polycythemia Calculator

Estimates total blood volume to remove and crystalloid volume to infuse in 
neonatal polycythemia.

References:
1. Black VD, et al. Pediatrics. 1985;76(2):225-31
2. Roback JD. Technical Manual. American Association of Blood Banks (AABB); 2014
"""

import math
from typing import Dict, Any


class NeonatalPartialExchangePolycythemiaCalculator:
    """Calculator for Neonatal Partial Exchange for Polycythemia"""
    
    def __init__(self):
        # Blood volume constants in mL/kg
        self.BLOOD_VOLUME_PRETERM = 100  # mL/kg for preterm infants
        self.BLOOD_VOLUME_TERM = 85  # mL/kg for term infants
    
    def calculate(self, weight: float, gestational_age: str, 
                  initial_hematocrit: float, goal_hematocrit: float) -> Dict[str, Any]:
        """
        Calculates the volume of blood to exchange for polycythemia
        
        Args:
            weight (float): Patient weight in kg
            gestational_age (str): "preterm" or "term"
            initial_hematocrit (float): Initial hematocrit percentage
            goal_hematocrit (float): Goal hematocrit percentage
            
        Returns:
            Dict with the exchange volume and interpretation
        """
        
        # Validations
        self._validate_inputs(weight, gestational_age, initial_hematocrit, goal_hematocrit)
        
        # Calculate blood volume based on gestational age
        if gestational_age == "preterm":
            blood_volume_per_kg = self.BLOOD_VOLUME_PRETERM
        else:  # term
            blood_volume_per_kg = self.BLOOD_VOLUME_TERM
        
        # Calculate total blood volume
        total_blood_volume = weight * blood_volume_per_kg
        
        # Calculate exchange volume using the formula
        # Volume = [blood volume × (initial Hct - goal Hct)] / initial Hct
        exchange_volume = (total_blood_volume * (initial_hematocrit - goal_hematocrit)) / initial_hematocrit
        
        # Round to 1 decimal place
        exchange_volume = round(exchange_volume, 1)
        
        # Get interpretation
        interpretation_text = self._get_interpretation(exchange_volume, initial_hematocrit, goal_hematocrit)
        
        return {
            "result": exchange_volume,
            "unit": "mL",
            "interpretation": interpretation_text,
            "stage": "Exchange Volume",
            "stage_description": f"Remove {exchange_volume} mL of blood and infuse {exchange_volume} mL of crystalloid"
        }
    
    def _validate_inputs(self, weight: float, gestational_age: str, 
                        initial_hematocrit: float, goal_hematocrit: float):
        """Validates input parameters"""
        
        # Weight validation
        if not isinstance(weight, (int, float)):
            raise ValueError("Weight must be a number")
        if weight < 0.5 or weight > 10:
            raise ValueError("Weight must be between 0.5 and 10 kg")
        
        # Gestational age validation
        if gestational_age not in ["preterm", "term"]:
            raise ValueError("Gestational age must be 'preterm' or 'term'")
        
        # Initial hematocrit validation
        if not isinstance(initial_hematocrit, (int, float)):
            raise ValueError("Initial hematocrit must be a number")
        if initial_hematocrit < 0 or initial_hematocrit > 100:
            raise ValueError("Initial hematocrit must be between 0 and 100%")
        
        # Goal hematocrit validation
        if not isinstance(goal_hematocrit, (int, float)):
            raise ValueError("Goal hematocrit must be a number")
        if goal_hematocrit < 40 or goal_hematocrit > 80:
            raise ValueError("Goal hematocrit must be between 40 and 80%")
        
        # Logical validation
        if goal_hematocrit >= initial_hematocrit:
            raise ValueError("Goal hematocrit must be less than initial hematocrit")
    
    def _get_interpretation(self, exchange_volume: float, initial_hct: float, 
                           goal_hct: float) -> str:
        """
        Generates clinical interpretation based on the calculated exchange volume
        
        Args:
            exchange_volume (float): Calculated exchange volume in mL
            initial_hct (float): Initial hematocrit percentage
            goal_hct (float): Goal hematocrit percentage
            
        Returns:
            str: Clinical interpretation
        """
        
        interpretation = f"Withdraw {exchange_volume} mL of whole blood while simultaneously infusing {exchange_volume} mL of normal saline. "
        
        # Add specific guidance based on initial hematocrit
        if initial_hct > 75:
            interpretation += "With initial Hct >75%, partial exchange is indicated even in asymptomatic infants. "
        elif initial_hct > 65:
            interpretation += "With initial Hct >65%, partial exchange is indicated if the infant is symptomatic. "
        
        interpretation += "The procedure should be performed by experienced clinical team members following institutional policies. "
        interpretation += "Monitor vital signs and hematocrit levels during and after the procedure."
        
        return interpretation


def calculate_neonatal_partial_exchange_polycythemia(weight: float, gestational_age: str,
                                                    initial_hematocrit: float, 
                                                    goal_hematocrit: float) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = NeonatalPartialExchangePolycythemiaCalculator()
    return calculator.calculate(weight, gestational_age, initial_hematocrit, goal_hematocrit)