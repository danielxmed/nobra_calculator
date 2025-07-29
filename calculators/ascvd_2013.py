"""
ASCVD 2013 Risk Calculator

Calculates 10-year risk of atherosclerotic cardiovascular disease using
the Pooled Cohort Equations from the 2013 ACC/AHA guidelines.

Reference: Goff DC Jr, et al. Circulation. 2014;129(25 Suppl 2):S49-73.
"""

import math
from typing import Dict, Any


class Ascvd2013Calculator:
    """Calculator for ASCVD 10-year risk using 2013 Pooled Cohort Equations"""
    
    def __init__(self):
        # Coefficients from Table A of the 2013 ACC/AHA guidelines
        # Structure: [race][sex][parameter]
        self.coefficients = {
            "white": {
                "female": {
                    "ln_age": -29.799,
                    "ln_age_squared": 4.884,
                    "ln_total_chol": 13.540,
                    "ln_age_ln_total_chol": -3.114,
                    "ln_hdl": -13.578,
                    "ln_age_ln_hdl": 3.149,
                    "ln_treated_sbp": 2.019,
                    "ln_age_ln_treated_sbp": 0,  # N/A in table
                    "ln_untreated_sbp": 1.957,
                    "ln_age_ln_untreated_sbp": 0,  # N/A in table
                    "smoker": 7.574,
                    "ln_age_smoker": -1.665,
                    "diabetes": 0.661,
                    "mean_terms": -29.18,
                    "baseline_survival": 0.9665
                },
                "male": {
                    "ln_age": 12.344,
                    "ln_age_squared": 0,  # Not used for men
                    "ln_total_chol": 11.853,
                    "ln_age_ln_total_chol": -2.664,
                    "ln_hdl": -7.990,
                    "ln_age_ln_hdl": 1.769,
                    "ln_treated_sbp": 1.797,
                    "ln_age_ln_treated_sbp": 0,  # N/A in table
                    "ln_untreated_sbp": 1.764,
                    "ln_age_ln_untreated_sbp": 0,  # N/A in table
                    "smoker": 7.837,
                    "ln_age_smoker": -1.795,
                    "diabetes": 0.658,
                    "mean_terms": 61.18,
                    "baseline_survival": 0.9144
                }
            },
            "african_american": {
                "female": {
                    "ln_age": 17.114,
                    "ln_age_squared": 0,  # N/A for African American
                    "ln_total_chol": 0.940,
                    "ln_age_ln_total_chol": 0,  # N/A in table
                    "ln_hdl": -18.920,
                    "ln_age_ln_hdl": 4.475,
                    "ln_treated_sbp": 29.291,
                    "ln_age_ln_treated_sbp": -6.432,
                    "ln_untreated_sbp": 27.820,
                    "ln_age_ln_untreated_sbp": -6.087,
                    "smoker": 0.691,
                    "ln_age_smoker": 0,  # N/A in table
                    "diabetes": 0.874,
                    "mean_terms": 86.61,
                    "baseline_survival": 0.9533
                },
                "male": {
                    "ln_age": 2.469,
                    "ln_age_squared": 0,  # Not used
                    "ln_total_chol": 0.302,
                    "ln_age_ln_total_chol": 0,  # N/A in table
                    "ln_hdl": -0.307,
                    "ln_age_ln_hdl": 0,  # N/A in table
                    "ln_treated_sbp": 1.916,
                    "ln_age_ln_treated_sbp": 0,  # N/A in table
                    "ln_untreated_sbp": 1.809,
                    "ln_age_ln_untreated_sbp": 0,  # N/A in table
                    "smoker": 0.549,
                    "ln_age_smoker": 0,  # N/A in table
                    "diabetes": 0.645,
                    "mean_terms": 19.54,
                    "baseline_survival": 0.8954
                }
            }
        }
    
    def calculate(self, age: int, sex: str, race: str, 
                 total_cholesterol: float, hdl_cholesterol: float,
                 systolic_bp: int, bp_treatment: bool,
                 diabetes: bool, smoker: bool) -> Dict[str, Any]:
        """
        Calculates 10-year ASCVD risk using Pooled Cohort Equations
        
        Args:
            age: Age in years (40-79)
            sex: "male" or "female"
            race: "white", "african_american", or "other"
            total_cholesterol: Total cholesterol in mg/dL
            hdl_cholesterol: HDL cholesterol in mg/dL
            systolic_bp: Systolic blood pressure in mmHg
            bp_treatment: Currently on BP medication
            diabetes: History of diabetes
            smoker: Current smoker
            
        Returns:
            Dict with 10-year risk percentage and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(age, sex, race, total_cholesterol, 
                            hdl_cholesterol, systolic_bp)
        
        # For "other" race, use white coefficients as per guidelines
        if race == "other":
            race = "white"
        
        # Get coefficients for the specific race-sex group
        coeffs = self.coefficients[race][sex]
        
        # Calculate natural log transformations
        ln_age = math.log(age)
        ln_age_squared = ln_age * ln_age
        ln_total_chol = math.log(total_cholesterol)
        ln_hdl = math.log(hdl_cholesterol)
        ln_sbp = math.log(systolic_bp)
        
        # Calculate sum of coefficient × value
        sum_coeff_value = 0
        
        # Age terms
        sum_coeff_value += coeffs["ln_age"] * ln_age
        if coeffs["ln_age_squared"] != 0:
            sum_coeff_value += coeffs["ln_age_squared"] * ln_age_squared
        
        # Cholesterol terms
        sum_coeff_value += coeffs["ln_total_chol"] * ln_total_chol
        if coeffs["ln_age_ln_total_chol"] != 0:
            sum_coeff_value += coeffs["ln_age_ln_total_chol"] * ln_age * ln_total_chol
        
        # HDL terms
        sum_coeff_value += coeffs["ln_hdl"] * ln_hdl
        if coeffs["ln_age_ln_hdl"] != 0:
            sum_coeff_value += coeffs["ln_age_ln_hdl"] * ln_age * ln_hdl
        
        # Blood pressure terms
        if bp_treatment:
            sum_coeff_value += coeffs["ln_treated_sbp"] * ln_sbp
            if coeffs["ln_age_ln_treated_sbp"] != 0:
                sum_coeff_value += coeffs["ln_age_ln_treated_sbp"] * ln_age * ln_sbp
        else:
            sum_coeff_value += coeffs["ln_untreated_sbp"] * ln_sbp
            if coeffs["ln_age_ln_untreated_sbp"] != 0:
                sum_coeff_value += coeffs["ln_age_ln_untreated_sbp"] * ln_age * ln_sbp
        
        # Smoking
        if smoker:
            sum_coeff_value += coeffs["smoker"]
            if coeffs["ln_age_smoker"] != 0:
                sum_coeff_value += coeffs["ln_age_smoker"] * ln_age
        
        # Diabetes
        if diabetes:
            sum_coeff_value += coeffs["diabetes"]
        
        # Calculate 10-year risk using the formula:
        # Risk = 1 - S₀(t)^exp(Xβ - mean Xβ)
        exponent = sum_coeff_value - coeffs["mean_terms"]
        risk_decimal = 1 - math.pow(coeffs["baseline_survival"], math.exp(exponent))
        risk_percent = risk_decimal * 100
        
        # Round to 1 decimal place
        risk_percent = round(risk_percent, 1)
        
        # Get interpretation
        interpretation = self._get_interpretation(risk_percent)
        
        return {
            "result": risk_percent,
            "unit": "%",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"],
            "details": {
                "race_group": race,
                "sex": sex,
                "individual_sum": round(sum_coeff_value, 2),
                "mean_coefficient_sum": coeffs["mean_terms"],
                "baseline_survival": coeffs["baseline_survival"]
            }
        }
    
    def _validate_inputs(self, age: int, sex: str, race: str,
                        total_cholesterol: float, hdl_cholesterol: float,
                        systolic_bp: int):
        """Validates input parameters"""
        
        if not isinstance(age, int) or age < 40 or age > 79:
            raise ValueError("Age must be an integer between 40 and 79 years")
        
        if sex.lower() not in ["male", "female"]:
            raise ValueError("Sex must be 'male' or 'female'")
        
        if race.lower() not in ["white", "african_american", "other"]:
            raise ValueError("Race must be 'white', 'african_american', or 'other'")
        
        if not isinstance(total_cholesterol, (int, float)) or total_cholesterol < 130 or total_cholesterol > 320:
            raise ValueError("Total cholesterol must be between 130 and 320 mg/dL")
        
        if not isinstance(hdl_cholesterol, (int, float)) or hdl_cholesterol < 20 or hdl_cholesterol > 100:
            raise ValueError("HDL cholesterol must be between 20 and 100 mg/dL")
        
        if not isinstance(systolic_bp, (int, float)) or systolic_bp < 90 or systolic_bp > 200:
            raise ValueError("Systolic blood pressure must be between 90 and 200 mmHg")
    
    def _get_interpretation(self, risk_percent: float) -> Dict[str, str]:
        """
        Determines clinical interpretation based on risk percentage
        
        Args:
            risk_percent: Calculated 10-year ASCVD risk percentage
            
        Returns:
            Dict with stage, description, and interpretation
        """
        
        if risk_percent < 5:
            return {
                "stage": "Low Risk",
                "description": f"{risk_percent}% 10-year risk",
                "interpretation": "Low 10-year ASCVD risk. Focus on lifestyle modifications including heart-healthy diet, regular physical activity, and smoking cessation if applicable."
            }
        elif risk_percent < 7.5:
            return {
                "stage": "Borderline Risk",
                "description": f"{risk_percent}% 10-year risk",
                "interpretation": "Borderline 10-year ASCVD risk. Consider risk-enhancing factors. Emphasize lifestyle modifications. For selected patients, consider moderate-intensity statin therapy after risk discussion."
            }
        elif risk_percent < 20:
            return {
                "stage": "Intermediate Risk",
                "description": f"{risk_percent}% 10-year risk",
                "interpretation": "Intermediate 10-year ASCVD risk. Moderate- to high-intensity statin therapy recommended after clinician-patient risk discussion, especially if risk enhancers present."
            }
        else:
            return {
                "stage": "High Risk",
                "description": f"{risk_percent}% 10-year risk",
                "interpretation": "High 10-year ASCVD risk. High-intensity statin therapy recommended to reduce LDL-C by ≥50%. Consider adding ezetimibe if LDL-C remains ≥70 mg/dL on maximally tolerated statin."
            }


def calculate_ascvd_2013(age: int, sex: str, race: str,
                        total_cholesterol: float, hdl_cholesterol: float,
                        systolic_bp: int, bp_treatment: bool,
                        diabetes: bool, smoker: bool) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = Ascvd2013Calculator()
    return calculator.calculate(age, sex, race, total_cholesterol,
                              hdl_cholesterol, systolic_bp, bp_treatment,
                              diabetes, smoker)