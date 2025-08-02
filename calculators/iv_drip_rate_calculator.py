"""
IV Drip Rate Calculator

Calculates IV infusion rate using drip count when IV pumps are unavailable. This tool determines 
the correct drops per minute needed to deliver a specified volume of intravenous fluid over a 
given time period using gravity-fed IV administration sets.

References:
1. Phillips LD, Gorski LA. Manual of I.V. therapeutics: evidence-based practice for infusion therapy. 6th ed. Philadelphia, PA: F.A. Davis Company; 2014.
2. Weinstein SM, Hagle ME. Plumer's principles and practice of infusion therapy. 9th ed. Philadelphia, PA: Wolters Kluwer/Lippincott Williams & Wilkins; 2014.
3. Alexander M, Corrigan A, Gorski L, Hankins J, Perucca R. Infusion nursing: an evidence-based approach. 3rd ed. St. Louis, MO: Saunders Elsevier; 2010.
"""

from typing import Dict, Any


class IvDripRateCalculator:
    """Calculator for IV Drip Rate"""
    
    def __init__(self):
        # Standard drop factors for different IV tubing types
        self.DROP_FACTORS = {
            "10": 10,    # Macrodrip tubing
            "15": 15,    # Macrodrip tubing  
            "20": 20,    # Macrodrip tubing
            "60": 60     # Microdrip/minidrip tubing
        }
    
    def calculate(self, volume_ml: float, time_minutes: float, drop_factor: str) -> Dict[str, Any]:
        """
        Calculates the IV drip rate in drops per minute
        
        Args:
            volume_ml (float): Total volume to be administered in mL
            time_minutes (float): Total infusion time in minutes
            drop_factor (str): Drop factor of IV tubing (gtts/mL)
            
        Returns:
            Dict with the drip rate and interpretation
        """
        
        # Validations
        self._validate_inputs(volume_ml, time_minutes, drop_factor)
        
        # Calculate drip rate
        drip_rate = self._calculate_drip_rate(volume_ml, time_minutes, drop_factor)
        
        # Get interpretation
        interpretation = self._get_interpretation(drip_rate, volume_ml, time_minutes, drop_factor)
        
        return {
            "result": round(drip_rate, 1),
            "unit": "gtts/min",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, volume_ml: float, time_minutes: float, drop_factor: str):
        """Validates input parameters"""
        
        if not isinstance(volume_ml, (int, float)) or volume_ml < 1 or volume_ml > 10000:
            raise ValueError("volume_ml must be a number between 1 and 10000 mL")
        
        if not isinstance(time_minutes, (int, float)) or time_minutes < 1 or time_minutes > 14400:
            raise ValueError("time_minutes must be a number between 1 and 14400 minutes")
        
        if drop_factor not in self.DROP_FACTORS:
            raise ValueError(f"drop_factor must be one of: {list(self.DROP_FACTORS.keys())}")
    
    def _calculate_drip_rate(self, volume_ml: float, time_minutes: float, drop_factor: str) -> float:
        """
        Calculates the IV drip rate using the standard formula
        
        Formula: IV Drip Rate (gtts/min) = (Volume in mL × Drop factor in gtts/mL) / Time in minutes
        
        Args:
            volume_ml (float): Volume to be administered
            time_minutes (float): Infusion time in minutes
            drop_factor (str): Drop factor string key
            
        Returns:
            float: Drip rate in drops per minute
        """
        
        drop_factor_value = self.DROP_FACTORS[drop_factor]
        drip_rate = (volume_ml * drop_factor_value) / time_minutes
        
        return drip_rate
    
    def _get_interpretation(self, drip_rate: float, volume_ml: float, 
                          time_minutes: float, drop_factor: str) -> Dict[str, str]:
        """
        Gets clinical interpretation based on drip rate
        
        Args:
            drip_rate (float): Calculated drip rate
            volume_ml (float): Volume being administered
            time_minutes (float): Infusion time
            drop_factor (str): Drop factor used
            
        Returns:
            Dict with interpretation details
        """
        
        hours = time_minutes / 60
        ml_per_hour = volume_ml / hours
        drop_factor_value = self.DROP_FACTORS[drop_factor]
        
        # Determine tubing type for context
        tubing_type = "microdrip (60 gtts/mL)" if drop_factor == "60" else f"macrodrip ({drop_factor} gtts/mL)"
        
        if drip_rate < 30:
            return {
                "stage": "Slow Infusion",
                "description": "Low drip rate infusion",
                "interpretation": f"Slow infusion rate of {drip_rate:.1f} gtts/min using {tubing_type} tubing. Delivering {volume_ml:.0f} mL over {hours:.1f} hours at {ml_per_hour:.1f} mL/hr. This slow rate is suitable for maintenance fluids, medications requiring careful titration, or patients at risk of fluid overload. Easy to count and monitor manually. Count drops for 15 seconds and multiply by 4 to verify rate."
            }
        elif drip_rate < 100:
            return {
                "stage": "Moderate Infusion",
                "description": "Moderate drip rate infusion",
                "interpretation": f"Moderate infusion rate of {drip_rate:.1f} gtts/min using {tubing_type} tubing. Delivering {volume_ml:.0f} mL over {hours:.1f} hours at {ml_per_hour:.1f} mL/hr. This rate is appropriate for standard fluid resuscitation, blood products, or routine medication administration. Requires careful counting and frequent monitoring. Adjust roller clamp as needed to maintain consistent rate."
            }
        elif drip_rate < 200:
            return {
                "stage": "Fast Infusion",
                "description": "High drip rate infusion",
                "interpretation": f"Fast infusion rate of {drip_rate:.1f} gtts/min using {tubing_type} tubing. Delivering {volume_ml:.0f} mL over {hours:.1f} hours at {ml_per_hour:.1f} mL/hr. This fast rate is for rapid fluid resuscitation or urgent medication delivery. Difficult to count accurately - consider using larger bore tubing or multiple IV lines if available. Monitor patient closely for signs of fluid overload."
            }
        else:
            return {
                "stage": "Very Fast Infusion",
                "description": "Very high drip rate infusion",
                "interpretation": f"Very fast infusion rate of {drip_rate:.1f} gtts/min using {tubing_type} tubing. Delivering {volume_ml:.0f} mL over {hours:.1f} hours at {ml_per_hour:.1f} mL/hr. This extremely fast rate is for emergency situations requiring rapid volume expansion. Extremely difficult to count manually - strongly consider alternative delivery methods if available, such as pressure bags, multiple IV lines, or electronic pumps. Monitor patient continuously for complications."
            }


def calculate_iv_drip_rate_calculator(volume_ml: float, time_minutes: float, drop_factor: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_iv_drip_rate_calculator pattern
    """
    calculator = IvDripRateCalculator()
    return calculator.calculate(volume_ml, time_minutes, drop_factor)