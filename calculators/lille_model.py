"""
Lille Model for Alcoholic Hepatitis Calculator

Predicts mortality in alcoholic hepatitis patients not responding to steroid therapy.
Helps identify patients who should be considered for alternative therapies or early 
referral for liver transplantation.

References:
1. Louvet A, Naveau S, Abdelnour M, Ramond MJ, Diaz E, Fartoux L, et al. The Lille 
   model: a new tool for therapeutic strategy in patients with severe alcoholic 
   hepatitis treated with steroids. Hepatology. 2007 Jun;45(6):1348-54.
2. Mathurin P, O'Grady J, Carithers RL, Phillips M, Louvet A, Mendenhall CL, et al. 
   Corticosteroids improve short-term survival in patients with severe alcoholic 
   hepatitis: a meta-analysis of individual patient data. Gut. 2011 Feb;60(2):255-60.
"""

import math
from typing import Dict, Any


class LilleModelCalculator:
    """Calculator for Lille Model for Alcoholic Hepatitis"""
    
    def __init__(self):
        # Model coefficients from the original study
        self.CONSTANT = 3.19
        self.AGE_COEFFICIENT = -0.101
        self.ALBUMIN_COEFFICIENT = 0.147
        self.BILIRUBIN_EVOLUTION_COEFFICIENT = 0.0165
        self.RENAL_INSUFFICIENCY_COEFFICIENT = -0.206
        self.BILIRUBIN_DAY0_COEFFICIENT = -0.0065
        self.PROTHROMBIN_TIME_COEFFICIENT = -0.0096
        
        # Renal insufficiency threshold
        self.CREATININE_THRESHOLD = 1.3  # mg/dL
        
        # Prognostic threshold
        self.RESPONSE_THRESHOLD = 0.45
    
    def calculate(
        self,
        age_years: int,
        albumin_day0: float,
        bilirubin_day0: float,
        bilirubin_day7: float,
        creatinine: float,
        prothrombin_time: float
    ) -> Dict[str, Any]:
        """
        Calculates the Lille Model score for alcoholic hepatitis prognosis
        
        Args:
            age_years (int): Patient age in years
            albumin_day0 (float): Serum albumin at day 0 in g/L
            bilirubin_day0 (float): Total bilirubin at day 0 in µmol/L
            bilirubin_day7 (float): Total bilirubin at day 7 in µmol/L
            creatinine (float): Serum creatinine in mg/dL
            prothrombin_time (float): Prothrombin time in seconds
            
        Returns:
            Dict with the result and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(
            age_years, albumin_day0, bilirubin_day0, bilirubin_day7,
            creatinine, prothrombin_time
        )
        
        # Calculate the Lille score
        lille_score = self._calculate_score(
            age_years, albumin_day0, bilirubin_day0, bilirubin_day7,
            creatinine, prothrombin_time
        )
        
        # Get interpretation
        interpretation = self._get_interpretation(
            lille_score, age_years, albumin_day0, bilirubin_day0, 
            bilirubin_day7, creatinine, prothrombin_time
        )
        
        return {
            "result": round(lille_score, 4),
            "unit": "score",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["stage_description"]
        }
    
    def _validate_inputs(
        self, age_years, albumin_day0, bilirubin_day0, bilirubin_day7,
        creatinine, prothrombin_time
    ):
        """Validates input parameters"""
        
        if not isinstance(age_years, int) or age_years < 18 or age_years > 100:
            raise ValueError("Age must be an integer between 18 and 100 years")
        
        if not isinstance(albumin_day0, (int, float)) or albumin_day0 < 10.0 or albumin_day0 > 60.0:
            raise ValueError("Albumin day 0 must be between 10.0 and 60.0 g/L")
        
        if not isinstance(bilirubin_day0, (int, float)) or bilirubin_day0 < 50.0 or bilirubin_day0 > 1000.0:
            raise ValueError("Bilirubin day 0 must be between 50.0 and 1000.0 µmol/L")
        
        if not isinstance(bilirubin_day7, (int, float)) or bilirubin_day7 < 20.0 or bilirubin_day7 > 1000.0:
            raise ValueError("Bilirubin day 7 must be between 20.0 and 1000.0 µmol/L")
        
        if not isinstance(creatinine, (int, float)) or creatinine < 0.3 or creatinine > 15.0:
            raise ValueError("Creatinine must be between 0.3 and 15.0 mg/dL")
        
        if not isinstance(prothrombin_time, (int, float)) or prothrombin_time < 10.0 or prothrombin_time > 120.0:
            raise ValueError("Prothrombin time must be between 10.0 and 120.0 seconds")
    
    def _calculate_score(
        self, age_years, albumin_day0, bilirubin_day0, bilirubin_day7,
        creatinine, prothrombin_time
    ) -> float:
        """
        Calculates the Lille Model score using the original formula
        
        Formula: Lille Score = exp(-R)/(1 + exp(-R))
        where R = 3.19 - 0.101×age + 0.147×albumin + 0.0165×(bilirubin_day7 - bilirubin_day0) 
                  - 0.206×renal_insufficiency - 0.0065×bilirubin_day0 - 0.0096×prothrombin_time
        """
        
        # Determine renal insufficiency (1 if creatinine > 1.3 mg/dL, 0 otherwise)
        renal_insufficiency = 1 if creatinine > self.CREATININE_THRESHOLD else 0
        
        # Calculate bilirubin evolution (day 7 - day 0)
        bilirubin_evolution = bilirubin_day7 - bilirubin_day0
        
        # Calculate R value
        R = (self.CONSTANT + 
             self.AGE_COEFFICIENT * age_years +
             self.ALBUMIN_COEFFICIENT * albumin_day0 +
             self.BILIRUBIN_EVOLUTION_COEFFICIENT * bilirubin_evolution +
             self.RENAL_INSUFFICIENCY_COEFFICIENT * renal_insufficiency +
             self.BILIRUBIN_DAY0_COEFFICIENT * bilirubin_day0 +
             self.PROTHROMBIN_TIME_COEFFICIENT * prothrombin_time)
        
        # Calculate Lille score using logistic function
        try:
            exp_neg_r = math.exp(-R)
            lille_score = exp_neg_r / (1 + exp_neg_r)
        except OverflowError:
            # Handle extreme values
            if R > 50:
                lille_score = 0.0
            elif R < -50:
                lille_score = 1.0
            else:
                raise
        
        return lille_score
    
    def _get_interpretation(
        self, lille_score, age_years, albumin_day0, bilirubin_day0, 
        bilirubin_day7, creatinine, prothrombin_time
    ) -> Dict[str, str]:
        """
        Determines the interpretation based on the Lille score
        
        Args:
            lille_score (float): Calculated Lille score
            
        Returns:
            Dict with interpretation details
        """
        
        # Calculate additional metrics for interpretation
        bilirubin_change = bilirubin_day7 - bilirubin_day0
        bilirubin_percent_change = (bilirubin_change / bilirubin_day0) * 100
        renal_insufficiency = creatinine > self.CREATININE_THRESHOLD
        
        if lille_score < self.RESPONSE_THRESHOLD:
            return {
                "stage": "Responder",
                "stage_description": "Good response to steroid therapy",
                "interpretation": f"Lille Model Score: {lille_score:.4f}. Classification: Steroid Responder. "
                                f"The score is below the threshold of 0.45, indicating a good response to "
                                f"corticosteroid therapy with an expected 6-month survival of 85%. "
                                f"Clinical parameters: bilirubin change from {bilirubin_day0:.0f} to "
                                f"{bilirubin_day7:.0f} µmol/L ({bilirubin_percent_change:+.1f}%), "
                                f"albumin {albumin_day0:.1f} g/L, age {age_years} years, "
                                f"{'renal insufficiency present' if renal_insufficiency else 'normal renal function'}, "
                                f"PT {prothrombin_time:.1f} seconds. "
                                f"Recommendation: Continue corticosteroid treatment (typically prednisolone "
                                f"40 mg daily) for the full 4-week course with gradual tapering. Monitor for "
                                f"improvement in liver function tests, nutritional status, and clinical symptoms. "
                                f"Provide supportive care including nutritional support, thiamine, folate, and "
                                f"alcohol cessation counseling. Regular monitoring for steroid-related complications "
                                f"and infection surveillance is essential."
            }
        else:
            return {
                "stage": "Non-responder",
                "stage_description": "Poor response to steroid therapy",
                "interpretation": f"Lille Model Score: {lille_score:.4f}. Classification: Steroid Non-responder. "
                                f"The score is at or above the threshold of 0.45, indicating poor response to "
                                f"corticosteroid therapy with an expected 6-month survival of only 25%. "
                                f"Clinical parameters: bilirubin change from {bilirubin_day0:.0f} to "
                                f"{bilirubin_day7:.0f} µmol/L ({bilirubin_percent_change:+.1f}%), "
                                f"albumin {albumin_day0:.1f} g/L, age {age_years} years, "
                                f"{'renal insufficiency present' if renal_insufficiency else 'normal renal function'}, "
                                f"PT {prothrombin_time:.1f} seconds. "
                                f"Recommendations: Strongly consider discontinuing corticosteroids to avoid "
                                f"further immunosuppression and infection risk. Evaluate for alternative "
                                f"therapies and urgent liver transplant assessment. Non-responders have "
                                f"significantly increased mortality and should be managed with palliative "
                                f"care principles while pursuing definitive treatment options. Early "
                                f"transplant evaluation is critical as this represents the only proven "
                                f"life-saving intervention for steroid non-responders."
            }


def calculate_lille_model(
    age_years: int,
    albumin_day0: float,
    bilirubin_day0: float,
    bilirubin_day7: float,
    creatinine: float,
    prothrombin_time: float
) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_lille_model pattern
    """
    calculator = LilleModelCalculator()
    return calculator.calculate(
        age_years, albumin_day0, bilirubin_day0, bilirubin_day7,
        creatinine, prothrombin_time
    )