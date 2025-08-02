"""
MAGGIC Risk Calculator for Heart Failure

Estimates 1- and 3-year mortality in heart failure patients based on 13 clinical variables.
Developed from meta-analysis of 39,372 patients from 30 studies.

References:
- Pocock SJ, et al. Predicting survival in heart failure: a risk score based on 39 372 patients from 30 studies. Eur Heart J. 2013;34(19):1404-13.
- Sartipy U, et al. Predicting survival in heart failure: validation of the MAGGIC heart failure risk score in 51,043 patients from the Swedish heart failure registry. Eur J Heart Fail. 2014;16(2):173-9.
"""

import math
from typing import Dict, Any


class MaggicRiskCalculator:
    """Calculator for MAGGIC Risk Score for Heart Failure"""
    
    def __init__(self):
        # Age scoring varies by ejection fraction category
        self.AGE_SCORING_HFREF = {  # EF <= 40%
            (18, 55): 0,
            (56, 60): 1,
            (61, 65): 2,
            (66, 70): 3,
            (71, 75): 5,
            (76, 80): 6,
            (81, 120): 8
        }
        
        self.AGE_SCORING_HFPEF = {  # EF > 40%
            (18, 55): 0,
            (56, 60): 2,
            (61, 65): 4,
            (66, 70): 6,
            (71, 75): 8,
            (76, 80): 10,
            (81, 120): 13
        }
        
        # Ejection fraction scoring
        self.EF_SCORING = {
            (40, 80): 0,  # Normal/preserved
            (35, 39): 1,  # Mildly reduced
            (30, 34): 2,  # Moderately reduced
            (25, 29): 3,  # Severely reduced
            (20, 24): 5,  # Very severely reduced
            (10, 19): 6   # Extremely reduced
        }
        
        # NYHA class scoring
        self.NYHA_SCORING = {
            "I": 0,
            "II": 2,
            "III": 6,
            "IV": 8
        }
        
        # Creatinine scoring (mg/dL)
        self.CREATININE_SCORING = {
            (0.3, 1.2): 0,   # Normal
            (1.21, 1.4): 1,  # Mild elevation
            (1.41, 1.8): 2,  # Moderate elevation
            (1.81, 2.3): 3,  # Significant elevation
            (2.31, 2.8): 4,  # Severe elevation
            (2.81, 15.0): 5  # Very severe elevation
        }
        
        # Systolic BP scoring (mmHg)
        self.SBP_SCORING = {
            (140, 250): 0,   # Normal/high
            (120, 139): 1,   # Prehypertension
            (110, 119): 2,   # Mild hypotension
            (100, 109): 3,   # Moderate hypotension
            (60, 99): 5      # Severe hypotension
        }
        
        # BMI scoring (kg/m²)
        self.BMI_SCORING = {
            (30, 60): 0,     # Obese (protective)
            (25, 29.9): 1,   # Overweight
            (22, 24.9): 2,   # Normal high
            (18, 21.9): 3,   # Normal low
            (10, 17.9): 5    # Underweight (high risk)
        }
    
    def calculate(self, age: int, gender: str, ejection_fraction: int, nyha_class: str,
                 creatinine: float, systolic_bp: int, bmi: float, diabetes: str,
                 copd: str, current_smoker: str, hf_duration_over_18_months: str,
                 beta_blocker: str, ace_arb: str) -> Dict[str, Any]:
        """
        Calculates the MAGGIC risk score using the provided parameters
        
        Args:
            age (int): Patient age in years (18-120)
            gender (str): Patient gender ('male' or 'female')
            ejection_fraction (int): Left ventricular ejection fraction (10-80%)
            nyha_class (str): NYHA functional class ('I', 'II', 'III', 'IV')
            creatinine (float): Serum creatinine level in mg/dL (0.3-15.0)
            systolic_bp (int): Systolic blood pressure in mmHg (60-250)
            bmi (float): Body mass index in kg/m² (10.0-60.0)
            diabetes (str): Diabetes mellitus present ('yes' or 'no')
            copd (str): Chronic obstructive pulmonary disease present ('yes' or 'no')
            current_smoker (str): Current smoking status ('yes' or 'no')
            hf_duration_over_18_months (str): Heart failure diagnosed >18 months ago ('yes' or 'no')
            beta_blocker (str): Currently prescribed beta-blocker ('yes' or 'no')
            ace_arb (str): Currently prescribed ACE inhibitor or ARB ('yes' or 'no')
            
        Returns:
            Dict with the result and interpretation
        """
        
        # Validations
        self._validate_inputs(age, gender, ejection_fraction, nyha_class, creatinine,
                            systolic_bp, bmi, diabetes, copd, current_smoker,
                            hf_duration_over_18_months, beta_blocker, ace_arb)
        
        # Calculate score
        maggic_score = self._calculate_maggic_score(
            age, gender, ejection_fraction, nyha_class, creatinine,
            systolic_bp, bmi, diabetes, copd, current_smoker,
            hf_duration_over_18_months, beta_blocker, ace_arb
        )
        
        # Get interpretation
        interpretation = self._get_interpretation(maggic_score)
        
        return {
            "result": maggic_score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, age, gender, ejection_fraction, nyha_class, creatinine,
                        systolic_bp, bmi, diabetes, copd, current_smoker,
                        hf_duration_over_18_months, beta_blocker, ace_arb):
        """Validates input parameters"""
        
        # Age validation
        if not isinstance(age, int) or age < 18 or age > 120:
            raise ValueError("Age must be an integer between 18 and 120 years")
        
        # Gender validation
        if gender not in ["male", "female"]:
            raise ValueError("Gender must be 'male' or 'female'")
        
        # Ejection fraction validation
        if not isinstance(ejection_fraction, int) or ejection_fraction < 10 or ejection_fraction > 80:
            raise ValueError("Ejection fraction must be an integer between 10 and 80%")
        
        # NYHA class validation
        if nyha_class not in ["I", "II", "III", "IV"]:
            raise ValueError("NYHA class must be 'I', 'II', 'III', or 'IV'")
        
        # Creatinine validation
        if not isinstance(creatinine, (int, float)) or creatinine < 0.3 or creatinine > 15.0:
            raise ValueError("Creatinine must be a number between 0.3 and 15.0 mg/dL")
        
        # Systolic BP validation
        if not isinstance(systolic_bp, int) or systolic_bp < 60 or systolic_bp > 250:
            raise ValueError("Systolic blood pressure must be an integer between 60 and 250 mmHg")
        
        # BMI validation
        if not isinstance(bmi, (int, float)) or bmi < 10.0 or bmi > 60.0:
            raise ValueError("BMI must be a number between 10.0 and 60.0 kg/m²")
        
        # Binary parameter validation
        binary_params = {
            "diabetes": diabetes,
            "copd": copd,
            "current_smoker": current_smoker,
            "hf_duration_over_18_months": hf_duration_over_18_months,
            "beta_blocker": beta_blocker,
            "ace_arb": ace_arb
        }
        
        for param_name, param_value in binary_params.items():
            if param_value not in ["yes", "no"]:
                raise ValueError(f"{param_name} must be 'yes' or 'no'")
    
    def _calculate_maggic_score(self, age, gender, ejection_fraction, nyha_class, creatinine,
                               systolic_bp, bmi, diabetes, copd, current_smoker,
                               hf_duration_over_18_months, beta_blocker, ace_arb) -> int:
        """Implements the MAGGIC risk score calculation"""
        
        score = 0
        
        # Age scoring (varies by EF category)
        if ejection_fraction <= 40:
            age_points = self._get_range_score(age, self.AGE_SCORING_HFREF)
        else:
            age_points = self._get_range_score(age, self.AGE_SCORING_HFPEF)
        score += age_points
        
        # Gender scoring (male = +1)
        if gender == "male":
            score += 1
        
        # Ejection fraction scoring
        ef_points = self._get_range_score(ejection_fraction, self.EF_SCORING)
        score += ef_points
        
        # NYHA class scoring
        score += self.NYHA_SCORING[nyha_class]
        
        # Creatinine scoring
        creatinine_points = self._get_range_score(creatinine, self.CREATININE_SCORING)
        score += creatinine_points
        
        # Systolic BP scoring
        sbp_points = self._get_range_score(systolic_bp, self.SBP_SCORING)
        score += sbp_points
        
        # BMI scoring
        bmi_points = self._get_range_score(bmi, self.BMI_SCORING)
        score += bmi_points
        
        # Diabetes (+3 points)
        if diabetes == "yes":
            score += 3
        
        # COPD (+2 points)
        if copd == "yes":
            score += 2
        
        # Current smoker (+1 point)
        if current_smoker == "yes":
            score += 1
        
        # Heart failure duration >18 months (+2 points)
        if hf_duration_over_18_months == "yes":
            score += 2
        
        # Not on beta-blocker (+3 points)
        if beta_blocker == "no":
            score += 3
        
        # Not on ACE-I/ARB (+1 point)
        if ace_arb == "no":
            score += 1
        
        return score
    
    def _get_range_score(self, value, scoring_dict):
        """Gets score for a value based on range dictionary"""
        for (min_val, max_val), points in scoring_dict.items():
            if min_val <= value <= max_val:
                return points
        return 0  # Default if no range matches
    
    def _get_interpretation(self, score: int) -> Dict[str, str]:
        """
        Determines the interpretation based on the MAGGIC score
        
        Args:
            score (int): Calculated MAGGIC score
            
        Returns:
            Dict with interpretation
        """
        
        if score <= 15:
            return {
                "stage": "Low Risk",
                "description": "Low mortality risk",
                "interpretation": "Low risk for 1-year (<5%) and 3-year (<15%) mortality. Standard heart failure management appropriate. Continue evidence-based medical therapy including ACE-I/ARB, beta-blockers, and lifestyle modifications. Regular monitoring and optimization of medical therapy recommended."
            }
        elif score <= 25:
            return {
                "stage": "Intermediate Risk",
                "description": "Intermediate mortality risk",
                "interpretation": "Intermediate risk for 1-year (5-15%) and 3-year (15-40%) mortality. Consider optimized medical therapy and closer monitoring. Ensure maximal tolerated evidence-based therapy. Consider device therapy evaluation if indicated. Regular cardiology follow-up recommended."
            }
        elif score <= 35:
            return {
                "stage": "High Risk",
                "description": "High mortality risk",
                "interpretation": "High risk for 1-year (15-40%) and 3-year (40-70%) mortality. Aggressive management and advanced therapies may be indicated. Consider referral to advanced heart failure specialist. Evaluate for device therapy (ICD/CRT). Consider advanced therapies including transplant evaluation if appropriate."
            }
        else:
            return {
                "stage": "Very High Risk",
                "description": "Very high mortality risk",
                "interpretation": "Very high risk for 1-year (>40%) and 3-year (>70%) mortality. Urgent referral to advanced heart failure center recommended. Consider advanced heart failure therapies including mechanical circulatory support, heart transplant evaluation, or palliative care discussions. Intensive monitoring and maximal medical therapy essential."
            }


def calculate_maggic_risk_calculator(age, gender, ejection_fraction, nyha_class,
                                   creatinine, systolic_bp, bmi, diabetes, copd,
                                   current_smoker, hf_duration_over_18_months,
                                   beta_blocker, ace_arb) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = MaggicRiskCalculator()
    return calculator.calculate(age, gender, ejection_fraction, nyha_class,
                              creatinine, systolic_bp, bmi, diabetes, copd,
                              current_smoker, hf_duration_over_18_months,
                              beta_blocker, ace_arb)