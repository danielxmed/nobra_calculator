"""
High-dose Insulin Euglycemia Therapy (HIET) Calculator

Calculates insulin dosing for calcium channel blocker or beta blocker overdose.

References:
- Holger JS, et al. Clin Toxicol. 2011;49(7):653-8.
- Greene SL, et al. Intensive Care Med. 2007;33(11):2019-24.
- Engebretsen KM, et al. Clin Toxicol. 2011;49(4):277-83.
"""

from typing import Dict, Any


class HietCalculator:
    """Calculator for High-dose Insulin Euglycemia Therapy"""
    
    def __init__(self):
        # Insulin dosing constants
        self.INSULIN_BOLUS_UNITS_PER_KG = 1.0
        self.DEXTROSE_INFUSION_G_PER_KG_HR = 0.5
        
        # Dextrose concentration options
        self.D10_CONCENTRATION = 0.1  # 10% dextrose = 0.1 g/mL
        self.D25_CONCENTRATION = 0.25  # 25% dextrose = 0.25 g/mL
        self.D50_CONCENTRATION = 0.5  # 50% dextrose = 0.5 g/mL
    
    def calculate(self, weight: float, infusion_rate: str) -> Dict[str, Any]:
        """
        Calculates the HIET protocol doses
        
        Args:
            weight (float): Patient weight in kg
            infusion_rate (str): Initial infusion rate ("0.5" or "1.0" units/kg/hr)
            
        Returns:
            Dict with complete dosing protocol
        """
        
        # Validate inputs
        self._validate_inputs(weight, infusion_rate)
        
        # Convert infusion rate to float
        infusion_rate_value = float(infusion_rate)
        
        # Calculate insulin bolus
        insulin_bolus = weight * self.INSULIN_BOLUS_UNITS_PER_KG
        
        # Calculate insulin infusion rate
        insulin_infusion = weight * infusion_rate_value
        
        # Calculate dextrose requirements
        dextrose_g_per_hr = weight * self.DEXTROSE_INFUSION_G_PER_KG_HR
        
        # Calculate dextrose infusion rates for different concentrations
        d10_rate = (dextrose_g_per_hr / self.D10_CONCENTRATION) * 1  # mL/hr
        d25_rate = (dextrose_g_per_hr / self.D25_CONCENTRATION) * 1  # mL/hr
        d50_rate = (dextrose_g_per_hr / self.D50_CONCENTRATION) * 1  # mL/hr
        
        # Build result object
        result = {
            "insulin_bolus": round(insulin_bolus, 1),
            "insulin_infusion": round(insulin_infusion, 1),
            "dextrose_g_per_hr": round(dextrose_g_per_hr, 1),
            "d10_rate_ml_hr": round(d10_rate, 0),
            "d25_rate_ml_hr": round(d25_rate, 0),
            "d50_rate_ml_hr": round(d50_rate, 0)
        }
        
        # Get interpretation
        interpretation = self._get_interpretation()
        
        return {
            "result": result,
            "unit": "protocol",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, weight: float, infusion_rate: str):
        """Validates input parameters"""
        
        if not isinstance(weight, (int, float)) or weight <= 0:
            raise ValueError("Weight must be a positive number")
        
        if weight < 1 or weight > 500:
            raise ValueError("Weight must be between 1 and 500 kg")
        
        valid_rates = ["0.5", "1.0"]
        if infusion_rate not in valid_rates:
            raise ValueError(f"Infusion rate must be one of {valid_rates}")
    
    def _get_interpretation(self) -> Dict[str, str]:
        """
        Returns the standard interpretation for HIET protocol
        
        Returns:
            Dict with interpretation
        """
        
        return {
            "stage": "HIET Protocol",
            "description": "Dosing calculated",
            "interpretation": "Follow the calculated protocol with close monitoring. "
                            "Check glucose every 30 minutes for 1-2 hours until stable. "
                            "Monitor potassium hourly. Continue until hemodynamic "
                            "improvement achieved. May increase insulin infusion up to "
                            "10 units/kg/hr if needed. Maintain glucose 110-250 mg/dL. "
                            "Give dextrose 25-50g bolus if glucose <250 mg/dL."
        }


def calculate_hiet(weight: float, infusion_rate: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = HietCalculator()
    return calculator.calculate(weight, infusion_rate)