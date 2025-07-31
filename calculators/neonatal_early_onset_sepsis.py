"""
Neonatal Early-Onset Sepsis Calculator

Estimates the probability of early-onset sepsis in newborns ≥34 weeks gestation
based on maternal intrapartum risk factors.

References:
- Puopolo KM, et al. Pediatrics. 2011;128(5):e1155-1163.
- Kuzniewicz MW, et al. Jt Comm J Qual Patient Saf. 2016;42(5):232-239.
"""

import math
from typing import Dict, Any


class NeonatalEarlyOnsetSepsisCalculator:
    """Calculator for Neonatal Early-Onset Sepsis risk"""
    
    def __init__(self):
        # Model coefficients
        self.CONSTANT = 40.5656
        self.GA_COEF = -6.9325
        self.GA2_COEF = 0.0877
        self.TEMP_COEF = 0.8680
        self.ROM_COEF = 1.2256
        self.GBS_POSITIVE_COEF = 0.5771
        self.GBS_UNKNOWN_COEF = 0.0427
        self.BROAD_SPECTRUM_GT_4HRS_COEF = -1.1861
        self.BROAD_SPECTRUM_2_TO_4HRS_COEF = -1.0488
        self.GBS_SPECIFIC_GT_2HRS_COEF = -1.0488
    
    def calculate(self, gestational_age_weeks: float, maternal_temp_celsius: float,
                  rom_hours: float, gbs_status: str, antibiotics_type: str) -> Dict[str, Any]:
        """
        Calculates the early-onset sepsis risk per 1000 births
        
        Args:
            gestational_age_weeks (float): Gestational age in weeks (34-43)
            maternal_temp_celsius (float): Highest maternal antepartum temperature in Celsius
            rom_hours (float): Duration of rupture of membranes in hours
            gbs_status (str): Maternal GBS status (negative, positive, unknown)
            antibiotics_type (str): Type of intrapartum antibiotics
            
        Returns:
            Dict with the result and interpretation
        """
        
        # Validations
        self._validate_inputs(gestational_age_weeks, maternal_temp_celsius,
                            rom_hours, gbs_status, antibiotics_type)
        
        # Convert temperature from Celsius to Fahrenheit for the formula
        maternal_temp_fahrenheit = (maternal_temp_celsius * 9/5) + 32
        
        # Calculate linear predictor (x)
        x = self._calculate_linear_predictor(
            gestational_age_weeks,
            maternal_temp_fahrenheit,
            rom_hours,
            gbs_status,
            antibiotics_type
        )
        
        # Calculate EOS risk at birth
        eos_risk_at_birth = 1 / (1 + math.exp(-x))
        
        # Convert to risk per 1000 births
        eos_risk_per_1000 = eos_risk_at_birth * 1000
        
        # Get interpretation
        interpretation = self._get_interpretation(eos_risk_per_1000)
        
        return {
            "result": round(eos_risk_per_1000, 2),
            "unit": "per 1000 births",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, gestational_age_weeks: float, maternal_temp_celsius: float,
                        rom_hours: float, gbs_status: str, antibiotics_type: str):
        """Validates input parameters"""
        
        # Validate gestational age
        if not isinstance(gestational_age_weeks, (int, float)) or gestational_age_weeks < 34 or gestational_age_weeks > 43:
            raise ValueError("Gestational age must be between 34 and 43 weeks")
        
        # Validate maternal temperature
        if not isinstance(maternal_temp_celsius, (int, float)) or maternal_temp_celsius < 35 or maternal_temp_celsius > 42:
            raise ValueError("Maternal temperature must be between 35 and 42°C")
        
        # Validate ROM hours
        if not isinstance(rom_hours, (int, float)) or rom_hours < 0 or rom_hours > 240:
            raise ValueError("Duration of rupture of membranes must be between 0 and 240 hours")
        
        # Validate GBS status
        valid_gbs_status = ["negative", "positive", "unknown"]
        if gbs_status not in valid_gbs_status:
            raise ValueError(f"GBS status must be one of: {', '.join(valid_gbs_status)}")
        
        # Validate antibiotics type
        valid_antibiotics = [
            "broad_spectrum_gt_4hrs",
            "broad_spectrum_2_to_4hrs",
            "gbs_specific_gt_2hrs",
            "no_antibiotics_or_lt_2hrs"
        ]
        if antibiotics_type not in valid_antibiotics:
            raise ValueError(f"Antibiotics type must be one of: {', '.join(valid_antibiotics)}")
    
    def _calculate_linear_predictor(self, ga: float, temp_f: float, rom: float,
                                   gbs_status: str, antibiotics_type: str) -> float:
        """
        Calculates the linear predictor (x) for the logistic regression model
        
        Formula: x = β0 + β1×GA + β2×GA² + β3×Temp + β4×tROM + β5×GBS + β6×Antibiotics
        """
        
        # Start with constant
        x = self.CONSTANT
        
        # Add gestational age terms
        x += self.GA_COEF * ga
        x += self.GA2_COEF * (ga ** 2)
        
        # Add temperature term
        x += self.TEMP_COEF * temp_f
        
        # Add transformed ROM term: (ROM + 0.05)^0.2
        trom = (rom + 0.05) ** 0.2
        x += self.ROM_COEF * trom
        
        # Add GBS status coefficients
        if gbs_status == "positive":
            x += self.GBS_POSITIVE_COEF
        elif gbs_status == "unknown":
            x += self.GBS_UNKNOWN_COEF
        # Note: negative is the reference category (coefficient = 0)
        
        # Add antibiotics coefficients
        if antibiotics_type == "broad_spectrum_gt_4hrs":
            x += self.BROAD_SPECTRUM_GT_4HRS_COEF
        elif antibiotics_type == "broad_spectrum_2_to_4hrs":
            x += self.BROAD_SPECTRUM_2_TO_4HRS_COEF
        elif antibiotics_type == "gbs_specific_gt_2hrs":
            x += self.GBS_SPECIFIC_GT_2HRS_COEF
        # Note: no_antibiotics_or_lt_2hrs is the reference category (coefficient = 0)
        
        return x
    
    def _get_interpretation(self, risk_per_1000: float) -> Dict[str, str]:
        """
        Determines the interpretation based on the EOS risk
        
        Args:
            risk_per_1000 (float): Calculated EOS risk per 1000 births
            
        Returns:
            Dict with interpretation details
        """
        
        if risk_per_1000 < 0.5:
            return {
                "stage": "Very Low Risk",
                "description": "Risk <0.5 per 1000",
                "interpretation": "Very low risk of early-onset sepsis. Routine care appropriate with continued observation for clinical signs."
            }
        elif risk_per_1000 < 1.0:
            return {
                "stage": "Low Risk",
                "description": "Risk 0.5-1.0 per 1000",
                "interpretation": "Low risk of early-onset sepsis. Enhanced observation may be considered based on clinical judgment."
            }
        elif risk_per_1000 < 3.0:
            return {
                "stage": "Intermediate Risk",
                "description": "Risk 1.0-3.0 per 1000",
                "interpretation": "Intermediate risk of early-onset sepsis. Enhanced observation recommended. Consider blood culture and empiric antibiotics based on clinical examination."
            }
        elif risk_per_1000 < 10.0:
            return {
                "stage": "High Risk",
                "description": "Risk 3.0-10.0 per 1000",
                "interpretation": "High risk of early-onset sepsis. Blood culture and empiric antibiotics strongly recommended unless infant is well-appearing with normal vital signs."
            }
        else:
            return {
                "stage": "Very High Risk",
                "description": "Risk ≥10.0 per 1000",
                "interpretation": "Very high risk of early-onset sepsis. Blood culture and empiric antibiotics recommended. Close monitoring in NICU setting may be warranted."
            }


def calculate_neonatal_early_onset_sepsis(gestational_age_weeks: float, maternal_temp_celsius: float,
                                         rom_hours: float, gbs_status: str, 
                                         antibiotics_type: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_neonatal_early_onset_sepsis pattern
    """
    calculator = NeonatalEarlyOnsetSepsisCalculator()
    return calculator.calculate(gestational_age_weeks, maternal_temp_celsius,
                              rom_hours, gbs_status, antibiotics_type)