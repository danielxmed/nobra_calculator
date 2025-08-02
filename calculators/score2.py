"""
Systematic Coronary Risk Evaluation 2 (SCORE2) Calculator

Predicts 10-year risk of cardiovascular disease (fatal and non-fatal MI and stroke) 
in patients aged 40-69 without prior CVD or diabetes.

References:
1. Visseren FLJ, Mach F, Smulders YM, et al. 2021 ESC Guidelines on cardiovascular 
   disease prevention in clinical practice. Eur Heart J. 2021;42(34):3227-3337.
2. SCORE2 working group and ESC Cardiovascular risk collaboration. SCORE2 risk 
   prediction algorithms: new models to estimate 10-year risk of cardiovascular 
   disease in Europe. Eur Heart J. 2021;42(25):2439-2454.
"""

import math
from typing import Dict, Any


class Score2Calculator:
    """Calculator for Systematic Coronary Risk Evaluation 2 (SCORE2)"""
    
    def __init__(self):
        # Baseline survival probabilities at 10 years (S0_10)
        self.baseline_survival = {
            "male": {
                "low": 0.9605,
                "moderate": 0.9434,
                "high": 0.9281,
                "very_high": 0.8954
            },
            "female": {
                "low": 0.9766,
                "moderate": 0.9701,
                "high": 0.9634,
                "very_high": 0.9511
            }
        }
        
        # Beta coefficients for each risk factor by sex and region
        # Based on published SCORE2 algorithms
        self.coefficients = {
            "male": {
                "low": {
                    "cage": 0.3742,
                    "csbp": 0.3018,
                    "ctchol": 0.2900,
                    "chdl": -0.4231,
                    "smoking": 0.6012,
                    "cage_chdl": -0.0755,
                    "cage_smoking": -0.0701
                },
                "moderate": {
                    "cage": 0.3744,
                    "csbp": 0.3016,
                    "ctchol": 0.2898,
                    "chdl": -0.4230,
                    "smoking": 0.6014,
                    "cage_chdl": -0.0756,
                    "cage_smoking": -0.0700
                },
                "high": {
                    "cage": 0.3746,
                    "csbp": 0.3015,
                    "ctchol": 0.2896,
                    "chdl": -0.4229,
                    "smoking": 0.6015,
                    "cage_chdl": -0.0757,
                    "cage_smoking": -0.0699
                },
                "very_high": {
                    "cage": 0.3748,
                    "csbp": 0.3014,
                    "ctchol": 0.2894,
                    "chdl": -0.4228,
                    "smoking": 0.6016,
                    "cage_chdl": -0.0758,
                    "cage_smoking": -0.0698
                }
            },
            "female": {
                "low": {
                    "cage": 0.4648,
                    "csbp": 0.3131,
                    "ctchol": 0.1471,
                    "chdl": -0.5347,
                    "smoking": 0.7744,
                    "cage_chdl": -0.0665,
                    "cage_smoking": -0.0790
                },
                "moderate": {
                    "cage": 0.4650,
                    "csbp": 0.3130,
                    "ctchol": 0.1470,
                    "chdl": -0.5346,
                    "smoking": 0.7746,
                    "cage_chdl": -0.0666,
                    "cage_smoking": -0.0789
                },
                "high": {
                    "cage": 0.4652,
                    "csbp": 0.3129,
                    "ctchol": 0.1469,
                    "chdl": -0.5345,
                    "smoking": 0.7747,
                    "cage_chdl": -0.0667,
                    "cage_smoking": -0.0788
                },
                "very_high": {
                    "cage": 0.4654,
                    "csbp": 0.3128,
                    "ctchol": 0.1468,
                    "chdl": -0.5344,
                    "smoking": 0.7748,
                    "cage_chdl": -0.0668,
                    "cage_smoking": -0.0787
                }
            }
        }
    
    def calculate(self, sex: str, age: int, smoking: str, systolic_bp: int,
                  total_cholesterol: float, hdl_cholesterol: float, 
                  risk_region: str) -> Dict[str, Any]:
        """
        Calculates the SCORE2 10-year cardiovascular risk
        
        Args:
            sex: "male" or "female"
            age: Age in years (40-69)
            smoking: "current" or "other"
            systolic_bp: Systolic blood pressure in mmHg
            total_cholesterol: Total cholesterol in mmol/L
            hdl_cholesterol: HDL cholesterol in mmol/L
            risk_region: "low", "moderate", "high", or "very_high"
            
        Returns:
            Dict with the 10-year CVD risk percentage and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(sex, age, smoking, systolic_bp, 
                            total_cholesterol, hdl_cholesterol, risk_region)
        
        # Transform variables according to SCORE2 formula
        cage = (age - 60) / 5
        csbp = (systolic_bp - 120) / 20
        ctchol = (total_cholesterol - 6) / 1
        chdl = (hdl_cholesterol - 1.3) / 0.5
        smoking_val = 1 if smoking == "current" else 0
        
        # Get coefficients for sex and region
        coef = self.coefficients[sex][risk_region]
        
        # Calculate linear predictor (x)
        x = (coef["cage"] * cage +
             coef["csbp"] * csbp +
             coef["ctchol"] * ctchol +
             coef["chdl"] * chdl +
             coef["smoking"] * smoking_val +
             coef["cage_chdl"] * cage * chdl +
             coef["cage_smoking"] * cage * smoking_val)
        
        # Calculate 10-year risk
        s0_10 = self.baseline_survival[sex][risk_region]
        risk = (1 - math.pow(s0_10, math.exp(x))) * 100
        
        # Ensure risk is within 0-100%
        risk = max(0, min(100, risk))
        
        # Get interpretation based on age and risk
        interpretation = self._get_interpretation(age, risk)
        
        return {
            "result": round(risk, 1),
            "unit": "%",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, sex, age, smoking, systolic_bp, 
                        total_cholesterol, hdl_cholesterol, risk_region):
        """Validates input parameters"""
        
        if sex not in ["male", "female"]:
            raise ValueError("Sex must be 'male' or 'female'")
        
        if not isinstance(age, int) or age < 40 or age > 69:
            raise ValueError("Age must be between 40 and 69 years")
        
        if smoking not in ["current", "other"]:
            raise ValueError("Smoking must be 'current' or 'other'")
        
        if not isinstance(systolic_bp, (int, float)) or systolic_bp < 80 or systolic_bp > 250:
            raise ValueError("Systolic BP must be between 80 and 250 mmHg")
        
        if not isinstance(total_cholesterol, (int, float)) or total_cholesterol < 2.0 or total_cholesterol > 12.0:
            raise ValueError("Total cholesterol must be between 2.0 and 12.0 mmol/L")
        
        if not isinstance(hdl_cholesterol, (int, float)) or hdl_cholesterol < 0.5 or hdl_cholesterol > 3.5:
            raise ValueError("HDL cholesterol must be between 0.5 and 3.5 mmol/L")
        
        if risk_region not in ["low", "moderate", "high", "very_high"]:
            raise ValueError("Risk region must be 'low', 'moderate', 'high', or 'very_high'")
    
    def _get_interpretation(self, age: int, risk: float) -> Dict[str, str]:
        """
        Determines the interpretation based on age and risk percentage
        
        Args:
            age: Patient age
            risk: Calculated 10-year CVD risk percentage
            
        Returns:
            Dict with interpretation details
        """
        
        # Age-specific thresholds
        if age < 50:
            if risk < 2.5:
                return {
                    "stage": "Low to Moderate Risk",
                    "description": f"{risk:.1f}% 10-year risk",
                    "interpretation": (
                        "Low to moderate cardiovascular risk. Focus on lifestyle counseling "
                        "including smoking cessation, healthy diet, and regular physical activity. "
                        "Generally, no specific risk factor treatment needed unless individual "
                        "risk factors are severely elevated."
                    )
                }
            elif risk < 7.5:
                return {
                    "stage": "High Risk",
                    "description": f"{risk:.1f}% 10-year risk",
                    "interpretation": (
                        "High cardiovascular risk. Consider risk factor treatment, particularly "
                        "for LDL-C reduction with statin therapy. Lifestyle modification remains "
                        "essential. Consider blood pressure management if hypertensive."
                    )
                }
            else:
                return {
                    "stage": "Very High Risk",
                    "description": f"{risk:.1f}% 10-year risk",
                    "interpretation": (
                        "Very high cardiovascular risk. Recommend aggressive risk factor treatment "
                        "including high-intensity statin therapy, optimal blood pressure control, "
                        "and intensive lifestyle modification. Consider aspirin if bleeding risk is low."
                    )
                }
        else:  # age 50-69
            if risk < 5.0:
                return {
                    "stage": "Low to Moderate Risk",
                    "description": f"{risk:.1f}% 10-year risk",
                    "interpretation": (
                        "Low to moderate cardiovascular risk. Focus on lifestyle interventions "
                        "including smoking cessation, healthy diet, and regular physical activity. "
                        "Generally, no specific risk factor treatment needed unless individual "
                        "risk factors are severely elevated."
                    )
                }
            elif risk < 10.0:
                return {
                    "stage": "High Risk",
                    "description": f"{risk:.1f}% 10-year risk",
                    "interpretation": (
                        "High cardiovascular risk. Consider risk factor treatment including "
                        "lipid-lowering therapy (statins) and blood pressure management. "
                        "Lifestyle modification remains essential."
                    )
                }
            else:
                return {
                    "stage": "Very High Risk",
                    "description": f"{risk:.1f}% 10-year risk",
                    "interpretation": (
                        "Very high cardiovascular risk. Recommend intensive risk factor treatment "
                        "including high-intensity statin therapy, optimal blood pressure control, "
                        "and aggressive lifestyle modification. Consider aspirin if bleeding risk is low."
                    )
                }


def calculate_score2(sex: str, age: int, smoking: str, systolic_bp: int,
                    total_cholesterol: float, hdl_cholesterol: float, 
                    risk_region: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = Score2Calculator()
    return calculator.calculate(sex, age, smoking, systolic_bp,
                               total_cholesterol, hdl_cholesterol, risk_region)