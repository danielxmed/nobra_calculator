"""
Systematic Coronary Risk Evaluation 2-Older Persons (SCORE2-OP) Calculator

Predicts cardiovascular disease risk in older persons (≥70 years), accounting for competing risks.
Based on the European Heart Journal 2021 publication.

References:
1. SCORE2-OP working group. SCORE2-OP risk prediction algorithms: estimating 
   incident cardiovascular event risk in older persons. Eur Heart J. 2021;42(25):2455-2467.
"""

import math
from typing import Dict, Any


class Score2OpCalculator:
    """Calculator for SCORE2-OP"""
    
    def __init__(self):
        # Baseline survival probabilities (adjusted for competing risks)
        self.baseline_survival = {
            "5_year": {
                "male": {
                    "low": 0.9584,
                    "moderate": 0.9490,
                    "high": 0.9396,
                    "very_high": 0.9302
                },
                "female": {
                    "low": 0.9748,
                    "moderate": 0.9685,
                    "high": 0.9622,
                    "very_high": 0.9559
                }
            },
            "10_year": {
                "male": {
                    "low": 0.8928,
                    "moderate": 0.8744,
                    "high": 0.8560,
                    "very_high": 0.8376
                },
                "female": {
                    "low": 0.9365,
                    "moderate": 0.9238,
                    "high": 0.9111,
                    "very_high": 0.8984
                }
            }
        }
        
        # Coefficients (estimated based on competing risk models)
        self.coefficients = {
            "male": {
                "diabetes": 0.3684,
                "smoking": 0.3251,
                "sbp": 0.0139,
                "non_hdl_chol": 0.1385,
                # Age interactions (effects attenuate with age)
                "age_diabetes": -0.0038,
                "age_smoking": -0.0034,
                "age_sbp": -0.0001,
                "age_non_hdl_chol": -0.0015
            },
            "female": {
                "diabetes": 0.3378,
                "smoking": 0.2982,
                "sbp": 0.0128,
                "non_hdl_chol": 0.1271,
                # Age interactions
                "age_diabetes": -0.0035,
                "age_smoking": -0.0031,
                "age_sbp": -0.0001,
                "age_non_hdl_chol": -0.0014
            }
        }
    
    def calculate(self, sex: str, age: int, diabetes: str, smoking: str, 
                  systolic_bp: int, total_cholesterol: float, hdl_cholesterol: float,
                  risk_region: str, time_horizon: str) -> Dict[str, Any]:
        """
        Calculates SCORE2-OP cardiovascular risk
        
        Args:
            sex: "male" or "female"
            age: Age in years (70-89)
            diabetes: "yes" or "no"
            smoking: "current" or "other"
            systolic_bp: Systolic blood pressure in mmHg
            total_cholesterol: Total cholesterol in mmol/L
            hdl_cholesterol: HDL cholesterol in mmol/L
            risk_region: "low", "moderate", "high", or "very_high"
            time_horizon: "5_year" or "10_year"
            
        Returns:
            Dict with CVD risk and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(sex, age, diabetes, smoking, systolic_bp, 
                            total_cholesterol, hdl_cholesterol, risk_region, time_horizon)
        
        # Calculate non-HDL cholesterol
        non_hdl_cholesterol = total_cholesterol - hdl_cholesterol
        
        # Transform variables (centered at reference values)
        cage = age - 73  # Centered at 73 years
        csbp = (systolic_bp - 120) / 20
        cnon_hdl_chol = (non_hdl_cholesterol - 4) / 1
        
        # Get coefficients for sex
        coef = self.coefficients[sex]
        
        # Calculate linear predictor
        x = 0
        
        # Main effects
        if diabetes == "yes":
            x += coef["diabetes"]
        if smoking == "current":
            x += coef["smoking"]
        x += coef["sbp"] * csbp
        x += coef["non_hdl_chol"] * cnon_hdl_chol
        
        # Age interactions (effects attenuate with age)
        if diabetes == "yes":
            x += coef["age_diabetes"] * cage
        if smoking == "current":
            x += coef["age_smoking"] * cage
        x += coef["age_sbp"] * cage * csbp
        x += coef["age_non_hdl_chol"] * cage * cnon_hdl_chol
        
        # Calculate risk using competing risk-adjusted baseline survival
        s0 = self.baseline_survival[time_horizon][sex][risk_region]
        risk = (1 - math.pow(s0, math.exp(x))) * 100
        
        # Round to 1 decimal place
        risk = round(risk, 1)
        
        # Get interpretation
        interpretation = self._get_interpretation(risk)
        
        return {
            "result": risk,
            "unit": "%",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": f"{risk}% {time_horizon.replace('_', '-')} CVD risk"
        }
    
    def _validate_inputs(self, sex, age, diabetes, smoking, systolic_bp,
                        total_cholesterol, hdl_cholesterol, risk_region, time_horizon):
        """Validates input parameters"""
        
        if sex not in ["male", "female"]:
            raise ValueError("Sex must be 'male' or 'female'")
        
        if not 70 <= age <= 89:
            raise ValueError("Age must be between 70 and 89 years")
        
        if diabetes not in ["yes", "no"]:
            raise ValueError("Diabetes must be 'yes' or 'no'")
        
        if smoking not in ["current", "other"]:
            raise ValueError("Smoking must be 'current' or 'other'")
        
        if not 80 <= systolic_bp <= 250:
            raise ValueError("Systolic BP must be between 80 and 250 mmHg")
        
        if not 2.0 <= total_cholesterol <= 12.0:
            raise ValueError("Total cholesterol must be between 2.0 and 12.0 mmol/L")
        
        if not 0.5 <= hdl_cholesterol <= 3.5:
            raise ValueError("HDL cholesterol must be between 0.5 and 3.5 mmol/L")
        
        if hdl_cholesterol >= total_cholesterol:
            raise ValueError("HDL cholesterol cannot be greater than or equal to total cholesterol")
        
        if risk_region not in ["low", "moderate", "high", "very_high"]:
            raise ValueError("Risk region must be 'low', 'moderate', 'high', or 'very_high'")
        
        if time_horizon not in ["5_year", "10_year"]:
            raise ValueError("Time horizon must be '5_year' or '10_year'")
    
    def _get_interpretation(self, risk: float) -> Dict[str, str]:
        """
        Determines interpretation based on risk
        
        Thresholds:
        - Low-Moderate: <7.5%
        - High: 7.5-15%
        - Very High: ≥15%
        """
        
        if risk < 7.5:
            return {
                "stage": "Low to Moderate Risk",
                "interpretation": "Generally no treatment benefit. Focus on lifestyle interventions. Consider individual patient characteristics and preferences in shared decision-making."
            }
        elif risk < 15:
            return {
                "stage": "High Risk",
                "interpretation": "Treatment may be considered. Discuss benefits and risks with patient. Consider statin therapy and blood pressure management based on individual assessment and patient preferences."
            }
        else:
            return {
                "stage": "Very High Risk",
                "interpretation": "Treatment generally recommended. Consider statin therapy and blood pressure management. Individualize treatment intensity based on life expectancy, frailty, and patient preferences."
            }


def calculate_score2_op(sex, age, diabetes, smoking, systolic_bp, total_cholesterol,
                       hdl_cholesterol, risk_region, time_horizon) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    """
    calculator = Score2OpCalculator()
    return calculator.calculate(sex, age, diabetes, smoking, systolic_bp,
                              total_cholesterol, hdl_cholesterol, risk_region,
                              time_horizon)