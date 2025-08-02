"""
Kinetic Estimated Glomerular Filtration Rate (keGFR) Calculator

Estimates GFR in patients with acutely changing creatinine levels to allow for 
earlier detection of acute kidney injury when creatinine is in a non-steady state.

References:
1. Chen S. Retooling the creatinine clearance equation to estimate kinetic GFR 
   when the plasma creatinine is changing acutely. J Am Soc Nephrol. 2013 
   May;24(6):877-88.
2. O'Sullivan ED, Doyle A. The clinical utility of kinetic glomerular filtration 
   rate. Clin Kidney J. 2017 Apr;10(2):202-208.
3. Pickering JW, Ralib AM, Endre ZH. Combining creatinine and volume kinetics 
   identifies missed cases of acute kidney injury following cardiac arrest. 
   Crit Care. 2013 Jan 14;17(1):R7.
"""

import math
from typing import Dict, Any


class KineticEgfrCalculator:
    """Calculator for Kinetic Estimated Glomerular Filtration Rate (keGFR)"""
    
    def __init__(self):
        # Constants for MDRD equation
        self.MDRD_CONSTANT = 175
        
        # Volume of distribution constants (mL/kg)
        self.VD_MALE = 600  # mL/kg
        self.VD_FEMALE = 500  # mL/kg
        
        # Creatinine production rate (mg/kg/day)
        self.CR_PRODUCTION_RATE = 20  # mg/kg/day
        
        # BSA calculation constants (DuBois formula)
        self.BSA_CONSTANT = 0.007184
        self.BSA_HEIGHT_EXP = 0.725
        self.BSA_WEIGHT_EXP = 0.425
    
    def calculate(self, age: int, sex: str, race: str, baseline_creatinine: float,
                 creatinine_1: float, creatinine_2: float, time_hours: float) -> Dict[str, Any]:
        """
        Calculates kinetic eGFR
        
        Args:
            age (int): Patient age in years
            sex (str): Biological sex (male/female)
            race (str): Race (black/non_black)
            baseline_creatinine (float): Baseline creatinine in mg/dL
            creatinine_1 (float): First creatinine measurement in mg/dL
            creatinine_2 (float): Second creatinine measurement in mg/dL
            time_hours (float): Time between measurements in hours
            
        Returns:
            Dict with keGFR result and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(age, sex, race, baseline_creatinine, 
                            creatinine_1, creatinine_2, time_hours)
        
        # Calculate baseline eGFR using MDRD equation
        baseline_egfr = self._calculate_mdrd_egfr(age, sex, race, baseline_creatinine)
        
        # Calculate kinetic eGFR
        kinetic_egfr = self._calculate_kinetic_egfr(
            baseline_egfr, creatinine_1, creatinine_2, time_hours, age, sex
        )
        
        # Get interpretation
        interpretation = self._get_interpretation(kinetic_egfr, baseline_egfr)
        
        return {
            "result": {
                "kinetic_egfr": round(kinetic_egfr, 1),
                "baseline_egfr": round(baseline_egfr, 1),
                "change_in_gfr": round(kinetic_egfr - baseline_egfr, 1)
            },
            "unit": "mL/min/1.73 m²",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["stage_description"]
        }
    
    def _validate_inputs(self, age: int, sex: str, race: str, baseline_creatinine: float,
                        creatinine_1: float, creatinine_2: float, time_hours: float):
        """Validates input parameters"""
        
        if not isinstance(age, int) or age < 18 or age > 120:
            raise ValueError("Age must be an integer between 18 and 120 years")
        
        if sex not in ["male", "female"]:
            raise ValueError("Sex must be 'male' or 'female'")
        
        if race not in ["black", "non_black"]:
            raise ValueError("Race must be 'black' or 'non_black'")
        
        if not isinstance(baseline_creatinine, (int, float)) or baseline_creatinine <= 0:
            raise ValueError("Baseline creatinine must be a positive number")
        
        if baseline_creatinine < 0.1 or baseline_creatinine > 15:
            raise ValueError("Baseline creatinine must be between 0.1 and 15 mg/dL")
        
        if not isinstance(creatinine_1, (int, float)) or creatinine_1 <= 0:
            raise ValueError("First creatinine must be a positive number")
        
        if creatinine_1 < 0.1 or creatinine_1 > 25:
            raise ValueError("First creatinine must be between 0.1 and 25 mg/dL")
        
        if not isinstance(creatinine_2, (int, float)) or creatinine_2 <= 0:
            raise ValueError("Second creatinine must be a positive number")
        
        if creatinine_2 < 0.1 or creatinine_2 > 25:
            raise ValueError("Second creatinine must be between 0.1 and 25 mg/dL")
        
        if not isinstance(time_hours, (int, float)) or time_hours <= 0:
            raise ValueError("Time must be a positive number")
        
        if time_hours < 1 or time_hours > 168:
            raise ValueError("Time must be between 1 and 168 hours")
    
    def _calculate_mdrd_egfr(self, age: int, sex: str, race: str, creatinine: float) -> float:
        """
        Calculates eGFR using MDRD equation
        
        Args:
            age (int): Patient age
            sex (str): Patient sex
            race (str): Patient race
            creatinine (float): Serum creatinine in mg/dL
            
        Returns:
            float: eGFR in mL/min/1.73 m²
        """
        
        # MDRD equation: 175 × (Scr)^-1.154 × (Age)^-0.203 × (0.742 if female) × (1.212 if black)
        egfr = self.MDRD_CONSTANT * (creatinine ** -1.154) * (age ** -0.203)
        
        # Apply sex factor
        if sex == "female":
            egfr *= 0.742
        
        # Apply race factor
        if race == "black":
            egfr *= 1.212
        
        return egfr
    
    def _calculate_kinetic_egfr(self, baseline_egfr: float, creatinine_1: float,
                               creatinine_2: float, time_hours: float, 
                               age: int, sex: str) -> float:
        """
        Calculates kinetic eGFR using Chen's formula
        
        Args:
            baseline_egfr (float): Baseline eGFR
            creatinine_1 (float): First creatinine
            creatinine_2 (float): Second creatinine  
            time_hours (float): Time between measurements
            age (int): Patient age
            sex (str): Patient sex
            
        Returns:
            float: Kinetic eGFR
        """
        
        # Estimate weight based on age and sex (for volume of distribution)
        # This is a rough approximation - ideally actual weight would be used
        if sex == "male":
            estimated_weight = 70  # kg - typical adult male
            vd_per_kg = self.VD_MALE
        else:
            estimated_weight = 60  # kg - typical adult female
            vd_per_kg = self.VD_FEMALE
        
        # Calculate volume of distribution
        vd = vd_per_kg * estimated_weight  # mL
        
        # Calculate BSA (assuming height of 170cm for males, 160cm for females)
        if sex == "male":
            estimated_height = 170  # cm
        else:
            estimated_height = 160  # cm
        
        bsa = self.BSA_CONSTANT * (estimated_weight ** self.BSA_WEIGHT_EXP) * (estimated_height ** self.BSA_HEIGHT_EXP)
        
        # Calculate change in creatinine
        delta_creatinine = creatinine_2 - creatinine_1
        
        # Convert time to days
        time_days = time_hours / 24.0
        
        # Calculate kinetic eGFR using Chen's formula
        # keGFR = baseline_eGFR - (ΔCr × Vd) / (time × BSA)
        # Adjustment factor to convert units properly
        kinetic_egfr = baseline_egfr - (delta_creatinine * vd) / (time_days * bsa * 1440)  # 1440 = minutes per day
        
        # Ensure keGFR doesn't go negative
        kinetic_egfr = max(0, kinetic_egfr)
        
        return kinetic_egfr
    
    def _get_interpretation(self, kinetic_egfr: float, baseline_egfr: float) -> Dict[str, str]:
        """
        Provides clinical interpretation based on keGFR value
        
        Args:
            kinetic_egfr (float): Calculated kinetic eGFR
            baseline_egfr (float): Baseline eGFR
            
        Returns:
            Dict with interpretation details
        """
        
        # Calculate percentage change
        gfr_change = kinetic_egfr - baseline_egfr
        percent_change = (gfr_change / baseline_egfr) * 100 if baseline_egfr > 0 else 0
        
        # Determine AKI risk based on keGFR thresholds
        if kinetic_egfr >= 60:
            stage = "Low AKI Risk"
            stage_description = "Normal/near-normal kidney function"
            aki_risk = "low"
        elif kinetic_egfr >= 30:
            stage = "Intermediate AKI Risk"
            stage_description = "Moderate kidney dysfunction"
            aki_risk = "intermediate"
        elif kinetic_egfr >= 15:
            stage = "High AKI Risk"
            stage_description = "Severe kidney dysfunction"
            aki_risk = "high"
        else:
            stage = "Very High AKI Risk"
            stage_description = "Kidney failure"
            aki_risk = "very high"
        
        # Generate interpretation
        interpretation = (
            f"Kinetic eGFR: {kinetic_egfr:.1f} mL/min/1.73 m² (baseline: {baseline_egfr:.1f}). "
            f"Change from baseline: {gfr_change:+.1f} mL/min/1.73 m² ({percent_change:+.1f}%). "
        )
        
        if kinetic_egfr < 30:
            interpretation += (
                f"keGFR <30 mL/min/1.73 m² is 90% specific for acute kidney injury. "
            )
        
        # Add clinical recommendations
        if aki_risk == "low":
            interpretation += (
                "Preserved kidney function with low AKI risk. Continue routine monitoring. "
                "Consider nephrotoxin avoidance and maintain adequate hydration."
            )
        elif aki_risk == "intermediate":
            interpretation += (
                "Moderate kidney impairment with intermediate AKI risk. Increase monitoring "
                "frequency, avoid nephrotoxins, ensure adequate perfusion, and consider "
                "nephrology consultation if deteriorating."
            )
        elif aki_risk == "high":
            interpretation += (
                "Severe kidney impairment with high AKI risk. Close monitoring required, "
                "strict nephrotoxin avoidance, optimize hemodynamics, and nephrology "
                "consultation recommended. Consider RRT preparation."
            )
        else:  # very high
            interpretation += (
                "Kidney failure with very high AKI risk. Urgent nephrology consultation "
                "required. Consider immediate RRT initiation, optimize fluid status, "
                "and manage uremic complications."
            )
        
        return {
            "stage": stage,
            "stage_description": stage_description,
            "interpretation": interpretation
        }


def calculate_kinetic_egfr(age: int, sex: str, race: str, baseline_creatinine: float,
                          creatinine_1: float, creatinine_2: float, time_hours: float) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_kinetic_egfr pattern
    """
    calculator = KineticEgfrCalculator()
    return calculator.calculate(age, sex, race, baseline_creatinine, 
                              creatinine_1, creatinine_2, time_hours)