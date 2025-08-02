"""
History and Electrocardiogram-only Manchester Acute Coronary Syndromes (HE-MACS) Calculator

Rules out acute coronary syndrome using history and ECG only.

References:
- Alghamdi A, et al. Eur J Emerg Med. 2019;26(5):356-361.
- Body R, et al. Resuscitation. 2010;81(3):281-6.
"""

import math
from typing import Dict, Any


class HeMacsCalculator:
    """Calculator for HE-MACS score"""
    
    def __init__(self):
        # Coefficients for the logistic regression model
        self.SWEATING_COEF = 1.426
        self.ECG_ISCHEMIA_COEF = 1.838
        self.PAIN_RIGHT_ARM_COEF = 0.734
        self.VOMITING_COEF = 0.996
        self.SYSTOLIC_BP_LOW_COEF = 1.353
        self.CURRENT_SMOKER_COEF = 0.675
        self.AGE_COEF = 0.024
        self.SEX_MALE_COEF = 0.462
        self.INTERCEPT = -4.416
        
        # Risk thresholds
        self.VERY_LOW_RISK_MAX = 3.99
        self.LOW_RISK_MAX = 6.99
        self.MODERATE_RISK_MAX = 49.99
    
    def calculate(self, age: int, sex: str, sweating: str, acute_ecg_ischemia: str,
                  pain_radiating_right_arm: str, vomiting: str, systolic_bp_low: str,
                  current_smoker: str) -> Dict[str, Any]:
        """
        Calculates the HE-MACS probability of ACS
        
        Args:
            age (int): Patient age in years
            sex (str): "male" or "female"
            sweating (str): "yes" or "no"
            acute_ecg_ischemia (str): "yes" or "no"
            pain_radiating_right_arm (str): "yes" or "no"
            vomiting (str): "yes" or "no"
            systolic_bp_low (str): "yes" or "no" (SBP <100 mmHg)
            current_smoker (str): "yes" or "no"
            
        Returns:
            Dict with the result and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(age, sex, sweating, acute_ecg_ischemia,
                            pain_radiating_right_arm, vomiting, systolic_bp_low,
                            current_smoker)
        
        # Calculate linear predictor
        x = 0
        
        # Binary variables (1 if yes, 0 if no)
        if sweating == "yes":
            x += self.SWEATING_COEF
        
        if acute_ecg_ischemia == "yes":
            x += self.ECG_ISCHEMIA_COEF
        
        if pain_radiating_right_arm == "yes":
            x += self.PAIN_RIGHT_ARM_COEF
        
        if vomiting == "yes":
            x += self.VOMITING_COEF
        
        if systolic_bp_low == "yes":
            x += self.SYSTOLIC_BP_LOW_COEF
        
        if current_smoker == "yes":
            x += self.CURRENT_SMOKER_COEF
        
        # Sex (1 if male, 0 if female)
        if sex == "male":
            x += self.SEX_MALE_COEF
        
        # Continuous variable
        x += self.AGE_COEF * age
        
        # Add intercept
        x += self.INTERCEPT
        
        # Calculate probability using logistic function
        # Note: we need to negate x for the formula as given
        probability = 1 / (1 + math.exp(x))
        
        # Convert to percentage
        probability_percent = probability * 100
        
        # Get interpretation
        interpretation = self._get_interpretation(probability_percent)
        
        return {
            "result": round(probability_percent, 1),
            "unit": "percent",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, age: int, sex: str, sweating: str, acute_ecg_ischemia: str,
                        pain_radiating_right_arm: str, vomiting: str, systolic_bp_low: str,
                        current_smoker: str):
        """Validates input parameters"""
        
        if not isinstance(age, int) or age < 18 or age > 120:
            raise ValueError("Age must be an integer between 18 and 120")
        
        valid_sex = ["male", "female"]
        if sex not in valid_sex:
            raise ValueError(f"Sex must be one of {valid_sex}")
        
        valid_yes_no = ["yes", "no"]
        
        if sweating not in valid_yes_no:
            raise ValueError(f"Sweating must be one of {valid_yes_no}")
        
        if acute_ecg_ischemia not in valid_yes_no:
            raise ValueError(f"Acute ECG ischemia must be one of {valid_yes_no}")
        
        if pain_radiating_right_arm not in valid_yes_no:
            raise ValueError(f"Pain radiating to right arm must be one of {valid_yes_no}")
        
        if vomiting not in valid_yes_no:
            raise ValueError(f"Vomiting must be one of {valid_yes_no}")
        
        if systolic_bp_low not in valid_yes_no:
            raise ValueError(f"Systolic BP low must be one of {valid_yes_no}")
        
        if current_smoker not in valid_yes_no:
            raise ValueError(f"Current smoker must be one of {valid_yes_no}")
    
    def _get_interpretation(self, probability: float) -> Dict[str, str]:
        """
        Determines the interpretation based on the probability
        
        Args:
            probability (float): Calculated probability in percent
            
        Returns:
            Dict with interpretation
        """
        
        if probability < self.VERY_LOW_RISK_MAX:
            return {
                "stage": "Very Low Risk",
                "description": "<4% risk",
                "interpretation": "Very low risk of ACS or major adverse cardiac events "
                                "within 30 days. Consider discharge with appropriate follow-up."
            }
        elif probability <= self.LOW_RISK_MAX:
            return {
                "stage": "Low Risk",
                "description": "4-6.9% risk",
                "interpretation": "Low risk of ACS or major adverse cardiac events within "
                                "30 days. Consider serial troponins and further observation."
            }
        elif probability <= self.MODERATE_RISK_MAX:
            return {
                "stage": "Moderate Risk",
                "description": "7-49.9% risk",
                "interpretation": "Moderate risk of ACS or major adverse cardiac events "
                                "within 30 days. Requires further investigation with "
                                "troponins and possible admission."
            }
        else:
            return {
                "stage": "High Risk",
                "description": "≥50% risk",
                "interpretation": "High risk of ACS or major adverse cardiac events within "
                                "30 days. Requires urgent cardiology consultation and admission."
            }


def calculate_he_macs(age: int, sex: str, sweating: str, acute_ecg_ischemia: str,
                      pain_radiating_right_arm: str, vomiting: str, systolic_bp_low: str,
                      current_smoker: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = HeMacsCalculator()
    return calculator.calculate(age, sex, sweating, acute_ecg_ischemia,
                              pain_radiating_right_arm, vomiting, systolic_bp_low,
                              current_smoker)