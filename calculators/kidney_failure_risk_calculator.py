"""
Kidney Failure Risk Calculator (4-Variable) Calculator

Predicts progression to kidney failure (dialysis or transplantation) in patients 
with CKD stages 3-5 using age, sex, eGFR, and urine albumin/creatinine ratio.

References:
1. Tangri N, Stevens LA, Griffith J, Tighiouart H, Djurdjev O, Naimark D, et al. 
   A predictive model for progression of chronic kidney disease to kidney failure. 
   JAMA. 2011;305(15):1553-9.
2. Tangri N, Grams ME, Levey AS, Coresh J, Appel LJ, Astor BC, et al. 
   Multinational Assessment of Accuracy of Equations for Predicting Risk of 
   Kidney Failure: A Meta-analysis. JAMA. 2016;315(2):164-74.
3. Ramspek CL, de Jong Y, Dekker FW, van Diepen M. Towards the best kidney 
   failure prediction tool: a systematic review and selection aid. 
   Nephrol Dial Transplant. 2020;35(9):1527-1538.
4. Major RW, Shepherd D, Medcalf JF, Xu G, Gray LJ, Brunskill NJ. The Kidney 
   Failure Risk Equation for prediction of end stage renal disease in UK 
   primary care: An external validation and clinical impact projection cohort 
   study. PLoS Med. 2019;16(11):e1002955.
"""

import math
from typing import Dict, Any


class KidneyFailureRiskCalculator:
    """Calculator for Kidney Failure Risk (4-Variable KFRE)"""
    
    def __init__(self):
        # Baseline survival probabilities
        self.baseline_survival = {
            "north_america": {
                "2_year": 0.9832,
                "5_year": 0.9365
            },
            "non_north_america": {
                "2_year": 0.9870,
                "5_year": 0.9520
            }
        }
        
        # Mean values for centering (from original cohort)
        self.means = {
            "age_decades": 7.036,
            "male_proportion": 0.5642,
            "egfr_5units": 7.222,
            "log_acr": 5.137
        }
        
        # Beta coefficients for 4-variable model
        self.coefficients = {
            "age": -0.2201,
            "male": 0.2467,
            "egfr": -0.5567,
            "log_acr": 0.4510
        }
    
    def calculate(self, age: int, sex: str, egfr: float, urine_acr: float, 
                 region: str) -> Dict[str, Any]:
        """
        Calculates kidney failure risk using 4-variable KFRE
        
        Args:
            age (int): Patient age in years
            sex (str): Biological sex (male/female)
            egfr (float): eGFR in mL/min/1.73 m²
            urine_acr (float): Urine albumin-to-creatinine ratio in mg/g
            region (str): Geographic region (north_america/non_north_america)
            
        Returns:
            Dict with 2-year and 5-year kidney failure risk
        """
        
        # Validate inputs
        self._validate_inputs(age, sex, egfr, urine_acr, region)
        
        # Calculate linear predictor
        linear_predictor = self._calculate_linear_predictor(age, sex, egfr, urine_acr)
        
        # Calculate risks
        risk_2_year = self._calculate_risk(linear_predictor, region, "2_year")
        risk_5_year = self._calculate_risk(linear_predictor, region, "5_year")
        
        # Get clinical interpretation
        interpretation = self._get_interpretation(risk_2_year, risk_5_year, egfr)
        
        return {
            "result": {
                "risk_2_year": round(risk_2_year, 1),
                "risk_5_year": round(risk_5_year, 1)
            },
            "unit": "percentage",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["stage_description"]
        }
    
    def _validate_inputs(self, age: int, sex: str, egfr: float, 
                        urine_acr: float, region: str):
        """Validates input parameters"""
        
        if not isinstance(age, int):
            raise ValueError("Age must be an integer")
        
        if age < 18 or age > 110:
            raise ValueError("Age must be between 18 and 110 years")
        
        if sex not in ["male", "female"]:
            raise ValueError("Sex must be 'male' or 'female'")
        
        if not isinstance(egfr, (int, float)):
            raise ValueError("eGFR must be a number")
        
        if egfr < 1 or egfr > 60:
            raise ValueError("eGFR must be between 1 and 60 mL/min/1.73 m² (CKD stages 3-5)")
        
        if not isinstance(urine_acr, (int, float)):
            raise ValueError("Urine ACR must be a number")
        
        if urine_acr < 0.1 or urine_acr > 25000:
            raise ValueError("Urine ACR must be between 0.1 and 25000 mg/g")
        
        if region not in ["north_america", "non_north_america"]:
            raise ValueError("Region must be 'north_america' or 'non_north_america'")
    
    def _calculate_linear_predictor(self, age: int, sex: str, egfr: float, 
                                   urine_acr: float) -> float:
        """Calculates the linear predictor (Xβ) for the Cox model"""
        
        # Convert variables to appropriate scales and center
        age_decades = age / 10.0
        male = 1 if sex == "male" else 0
        egfr_5units = egfr / 5.0
        log_acr = math.log(urine_acr)
        
        # Calculate linear predictor
        linear_predictor = (
            self.coefficients["age"] * (age_decades - self.means["age_decades"]) +
            self.coefficients["male"] * (male - self.means["male_proportion"]) +
            self.coefficients["egfr"] * (egfr_5units - self.means["egfr_5units"]) +
            self.coefficients["log_acr"] * (log_acr - self.means["log_acr"])
        )
        
        return linear_predictor
    
    def _calculate_risk(self, linear_predictor: float, region: str, 
                       time_period: str) -> float:
        """
        Calculates the absolute risk of kidney failure
        
        Args:
            linear_predictor (float): Xβ from Cox model
            region (str): Geographic region
            time_period (str): "2_year" or "5_year"
            
        Returns:
            float: Risk percentage
        """
        
        # Get baseline survival for region and time
        baseline_survival = self.baseline_survival[region][time_period]
        
        # Calculate risk: 1 - S0(t)^exp(Xβ)
        risk = 1 - math.pow(baseline_survival, math.exp(linear_predictor))
        
        # Convert to percentage
        risk_percentage = risk * 100
        
        return risk_percentage
    
    def _get_interpretation(self, risk_2_year: float, risk_5_year: float, 
                           egfr: float) -> Dict[str, str]:
        """
        Provides clinical interpretation based on kidney failure risk
        
        Args:
            risk_2_year (float): 2-year risk percentage
            risk_5_year (float): 5-year risk percentage
            egfr (float): Current eGFR
            
        Returns:
            Dict with interpretation details
        """
        
        # Determine risk category based on common clinical thresholds
        if risk_5_year < 5:
            risk_category = "Low"
            stage_description = "Low risk of kidney failure"
        elif risk_5_year < 15:
            risk_category = "Intermediate"
            stage_description = "Intermediate risk of kidney failure"
        elif risk_5_year < 30:
            risk_category = "High"
            stage_description = "High risk of kidney failure"
        else:
            risk_category = "Very High"
            stage_description = "Very high risk of kidney failure"
        
        # Generate detailed interpretation
        interpretation = (
            f"Based on the 4-variable Kidney Failure Risk Equation, this patient with "
            f"CKD (eGFR {egfr:.1f} mL/min/1.73 m²) has a {risk_2_year:.1f}% risk of "
            f"kidney failure at 2 years and {risk_5_year:.1f}% risk at 5 years. "
        )
        
        # Add management recommendations based on risk level
        if risk_category == "Low":
            interpretation += (
                "Low-risk patients can often be managed in primary care with annual "
                "monitoring of kidney function and albuminuria. Focus on cardiovascular "
                "risk reduction, blood pressure control, and lifestyle modifications."
            )
        elif risk_category == "Intermediate":
            interpretation += (
                "Consider nephrology referral, especially if 2-year risk >5% or "
                "5-year risk >15%. Optimize CKD management including blood pressure "
                "control, RAAS blockade if appropriate, and cardiovascular risk reduction. "
                "Monitor kidney function every 3-6 months."
            )
        elif risk_category == "High":
            interpretation += (
                "Nephrology referral is strongly recommended. Begin preparation for "
                "renal replacement therapy including patient education, vascular access "
                "planning, and transplant evaluation if appropriate. Aggressive management "
                "of CKD complications and cardiovascular risk factors is essential."
            )
        else:  # Very High
            interpretation += (
                "Urgent nephrology referral required. Immediate planning for renal "
                "replacement therapy is necessary, including dialysis access creation "
                "and expedited transplant evaluation. Consider preemptive transplantation "
                "if feasible. Close monitoring for uremic complications."
            )
        
        return {
            "stage": risk_category,
            "stage_description": stage_description,
            "interpretation": interpretation
        }


def calculate_kidney_failure_risk_calculator(age: int, sex: str, egfr: float, 
                                           urine_acr: float, region: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_kidney_failure_risk_calculator pattern
    """
    calculator = KidneyFailureRiskCalculator()
    return calculator.calculate(age, sex, egfr, urine_acr, region)