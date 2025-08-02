"""
Intraoperative Fluid Dosing in Adult Patients Calculator

Calculates intraoperative IV fluid requirements for adult patients during surgery, providing hourly fluid 
requirement, fluid deficit, and hour-by-hour fluid requirement based on surgical needs. Uses patient weight, 
NPO time, and surgical trauma severity to guide perioperative fluid management.

References:
1. Miller RD, et al. Miller's Anesthesia. 8th ed. Philadelphia: Elsevier Saunders; 2015.
2. Holte K, Sharrock NE, Kehlet H. Pathophysiology and clinical implications of perioperative fluid excess. Br J Anaesth. 2002;89(4):622-32.
3. Brandstrup B, et al. Effects of intravenous fluid restriction on postoperative complications. Ann Surg. 2003;238(5):641-8.
4. Gan TJ, et al. Goal-directed intraoperative fluid administration reduces length of hospital stay after major surgery. Anesthesiology. 2002;97(4):820-6.
"""

import math
from typing import Dict, Any


class IntraoperativeFluidDosingCalculator:
    """Calculator for Intraoperative Fluid Dosing in Adult Patients"""
    
    def __init__(self):
        # Surgical trauma fluid loss rates (mL/kg/hr)
        self.TRAUMA_RATES = {
            "minimal": 3,    # Laparoscopic procedures
            "moderate": 5,   # Open cholecystectomy
            "severe": 7      # Bowel resection, major abdominal surgery
        }
    
    def calculate(self, weight_kg: float, hours_npo: float, surgical_trauma: str) -> Dict[str, Any]:
        """
        Calculates intraoperative fluid dosing plan
        
        Args:
            weight_kg (float): Patient body weight in kilograms (≥20 kg)
            hours_npo (float): Time spent NPO before surgery in hours
            surgical_trauma (str): Surgical trauma severity ("minimal", "moderate", "severe")
            
        Returns:
            Dict with fluid dosing plan and interpretation
        """
        
        # Validations
        self._validate_inputs(weight_kg, hours_npo, surgical_trauma)
        
        # Calculate fluid requirements
        fluid_plan = self._calculate_fluid_plan(weight_kg, hours_npo, surgical_trauma)
        
        # Get interpretation
        interpretation = self._get_interpretation(surgical_trauma, weight_kg)
        
        return {
            "result": fluid_plan,
            "unit": "mL",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, weight_kg: float, hours_npo: float, surgical_trauma: str):
        """Validates input parameters"""
        
        if not isinstance(weight_kg, (int, float)) or weight_kg < 20 or weight_kg > 300:
            raise ValueError("weight_kg must be a number between 20 and 300 kg")
        
        if not isinstance(hours_npo, (int, float)) or hours_npo < 0 or hours_npo > 48:
            raise ValueError("hours_npo must be a number between 0 and 48 hours")
        
        if surgical_trauma not in self.TRAUMA_RATES:
            raise ValueError("surgical_trauma must be 'minimal', 'moderate', or 'severe'")
    
    def _calculate_fluid_plan(self, weight_kg: float, hours_npo: float, surgical_trauma: str) -> str:
        """
        Calculates the structured fluid dosing plan
        
        Args:
            weight_kg (float): Patient weight in kg
            hours_npo (float): Hours NPO
            surgical_trauma (str): Trauma severity
            
        Returns:
            String describing the fluid plan
        """
        
        # Calculate hourly maintenance fluid (weight + 40 mL)
        hourly_maintenance = weight_kg + 40
        
        # Calculate NPO fluid deficit
        npo_deficit = hourly_maintenance * hours_npo
        
        # Get surgical trauma fluid loss rate
        trauma_rate = self.TRAUMA_RATES[surgical_trauma]
        surgical_loss_per_hour = trauma_rate * weight_kg
        
        # Calculate hourly requirements
        hour_1 = (npo_deficit / 2) + hourly_maintenance
        hour_2_3 = (npo_deficit / 4) + hourly_maintenance + surgical_loss_per_hour
        hour_4_plus = hourly_maintenance + surgical_loss_per_hour
        
        # Format the fluid plan
        plan_components = [
            f"Hourly maintenance fluid: {hourly_maintenance:.0f} mL/hr",
            f"NPO deficit (total): {npo_deficit:.0f} mL ({hours_npo:.1f} hrs NPO)",
            f"Surgical trauma loss: {surgical_loss_per_hour:.0f} mL/hr ({surgical_trauma} trauma)",
            "",
            "Hour-by-hour fluid requirements:",
            f"Hour 1: {hour_1:.0f} mL (½ NPO deficit + maintenance)",
            f"Hours 2-3: {hour_2_3:.0f} mL/hr (¼ NPO deficit + maintenance + surgical loss)",
            f"Hour 4+: {hour_4_plus:.0f} mL/hr (maintenance + surgical loss)",
            "",
            f"Total first 4 hours: {hour_1 + (2 * hour_2_3) + hour_4_plus:.0f} mL"
        ]
        
        return "; ".join(plan_components)
    
    def _get_interpretation(self, surgical_trauma: str, weight_kg: float) -> Dict[str, str]:
        """
        Gets clinical interpretation based on surgical trauma severity
        
        Args:
            surgical_trauma (str): Trauma severity
            weight_kg (float): Patient weight
            
        Returns:
            Dict with interpretation details
        """
        
        trauma_rate = self.TRAUMA_RATES[surgical_trauma]
        surgical_loss = trauma_rate * weight_kg
        
        interpretations = {
            "minimal": {
                "stage": "Minimal Trauma",
                "description": "Low fluid loss procedures",
                "interpretation": f"Minimal tissue trauma and fluid loss procedures such as laparoscopic surgery. Requires {trauma_rate} mL/kg/hr ({surgical_loss:.0f} mL/hr for this patient) additional fluid replacement for surgical losses. Monitor for adequate urine output (>0.5 mL/kg/hr) and stable hemodynamics. Avoid fluid overload in susceptible patients."
            },
            "moderate": {
                "stage": "Moderate Trauma",
                "description": "Moderate fluid loss procedures", 
                "interpretation": f"Moderate tissue trauma and fluid loss procedures such as open cholecystectomy or appendectomy. Requires {trauma_rate} mL/kg/hr ({surgical_loss:.0f} mL/hr for this patient) additional fluid replacement for surgical losses. Close monitoring of hemodynamics, urine output, and fluid balance is essential. Consider goal-directed fluid therapy."
            },
            "severe": {
                "stage": "Severe Trauma",
                "description": "High fluid loss procedures",
                "interpretation": f"Significant tissue trauma and fluid loss procedures such as bowel resection, major abdominal surgery, or extensive orthopedic procedures. Requires {trauma_rate} mL/kg/hr ({surgical_loss:.0f} mL/hr for this patient) additional fluid replacement for surgical losses. Intensive monitoring including arterial line, central venous pressure, and possible cardiac output monitoring may be indicated. Consider blood product availability and coagulation status."
            }
        }
        
        return interpretations[surgical_trauma]


def calculate_intraoperative_fluid_dosing(weight_kg: float, hours_npo: float, surgical_trauma: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_intraoperative_fluid_dosing pattern
    """
    calculator = IntraoperativeFluidDosingCalculator()
    return calculator.calculate(weight_kg, hours_npo, surgical_trauma)