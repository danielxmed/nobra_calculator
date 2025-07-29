"""
BALL Score for Relapsed/Refractory CLL Calculator

Assesses prognosis of patients with relapsed/refractory chronic lymphocytic leukemia 
(R/R CLL) on targeted therapies. The BALL Score uses four parameters to predict 
24-month overall survival.

References:
1. Soumerai JD, Ni A, Darif M, Londhe A, Xing G, Mun Y, et al. Prognostic risk score 
   for patients with relapsed or refractory chronic lymphocytic leukaemia treated with 
   targeted therapies or chemoimmunotherapy: a retrospective, pooled cohort study with 
   external validations. Lancet Haematol. 2019 Jul;6(7):e366-e374. 
   doi: 10.1016/S2352-3026(19)30085-7.
2. Gentile M, Morabito F, Del Poeta G, Mauro FR, Reda G, Sportoletti P, et al. 
   Survival risk score for real-life relapsed/refractory chronic lymphocytic leukemia 
   patients receiving ibrutinib. A campus CLL study. Leukemia. 2021 Jan;35(1):235-238. 
   doi: 10.1038/s41375-020-0816-y.
"""

from typing import Dict, Any


class BallScoreRrCllCalculator:
    """Calculator for BALL Score for Relapsed/Refractory CLL"""
    
    def __init__(self):
        # BALL Score component thresholds
        self.BETA2_MICROGLOBULIN_THRESHOLD = 5.0  # mg/dL
        self.ANEMIA_THRESHOLD_MALE = 12.0  # g/dL
        self.ANEMIA_THRESHOLD_FEMALE = 11.0  # g/dL
        self.MONTHS_SINCE_THERAPY_THRESHOLD = 24  # months
    
    def calculate(self, beta2_microglobulin: float, hemoglobin: float, sex: str,
                  ldh: float, ldh_upper_limit: float, 
                  months_since_last_therapy: int) -> Dict[str, Any]:
        """
        Calculates the BALL Score using the provided parameters
        
        Args:
            beta2_microglobulin (float): Beta-2-microglobulin level in mg/dL
            hemoglobin (float): Hemoglobin level in g/dL
            sex (str): Patient's biological sex ('male' or 'female')
            ldh (float): Lactate dehydrogenase level in U/L
            ldh_upper_limit (float): Upper limit of normal for LDH in U/L
            months_since_last_therapy (int): Months since initiation of last therapy
            
        Returns:
            Dict with the result and interpretation
        """
        
        # Validations
        self._validate_inputs(beta2_microglobulin, hemoglobin, sex, ldh, 
                            ldh_upper_limit, months_since_last_therapy)
        
        # Calculate score
        score = self._calculate_score(beta2_microglobulin, hemoglobin, sex,
                                    ldh, ldh_upper_limit, months_since_last_therapy)
        
        # Get interpretation
        interpretation = self._get_interpretation(score)
        
        return {
            "result": score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, beta2_microglobulin: float, hemoglobin: float, 
                        sex: str, ldh: float, ldh_upper_limit: float,
                        months_since_last_therapy: int):
        """Validates input parameters"""
        
        # Validate beta-2-microglobulin
        if not isinstance(beta2_microglobulin, (int, float)) or beta2_microglobulin < 0.1:
            raise ValueError("Beta-2-microglobulin must be a positive number")
        if beta2_microglobulin > 50:
            raise ValueError("Beta-2-microglobulin value seems unusually high (>50 mg/dL)")
        
        # Validate hemoglobin
        if not isinstance(hemoglobin, (int, float)) or hemoglobin < 3:
            raise ValueError("Hemoglobin must be at least 3 g/dL")
        if hemoglobin > 20:
            raise ValueError("Hemoglobin value seems unusually high (>20 g/dL)")
        
        # Validate sex
        if sex not in ["male", "female"]:
            raise ValueError("Sex must be 'male' or 'female'")
        
        # Validate LDH
        if not isinstance(ldh, (int, float)) or ldh < 50:
            raise ValueError("LDH must be at least 50 U/L")
        if ldh > 5000:
            raise ValueError("LDH value seems unusually high (>5000 U/L)")
        
        # Validate LDH upper limit
        if not isinstance(ldh_upper_limit, (int, float)) or ldh_upper_limit < 100:
            raise ValueError("LDH upper limit must be at least 100 U/L")
        if ldh_upper_limit > 500:
            raise ValueError("LDH upper limit seems unusually high (>500 U/L)")
        
        # Validate months since last therapy
        if not isinstance(months_since_last_therapy, int) or months_since_last_therapy < 0:
            raise ValueError("Months since last therapy must be a non-negative integer")
        if months_since_last_therapy > 600:
            raise ValueError("Months since last therapy seems unusually high (>600 months)")
    
    def _calculate_score(self, beta2_microglobulin: float, hemoglobin: float, 
                        sex: str, ldh: float, ldh_upper_limit: float,
                        months_since_last_therapy: int) -> int:
        """Implements the BALL Score formula"""
        
        score = 0
        
        # B - Beta-2-microglobulin ≥5 mg/dL (1 point)
        if beta2_microglobulin >= self.BETA2_MICROGLOBULIN_THRESHOLD:
            score += 1
        
        # A - Anemia (1 point)
        # Men: Hgb <12 g/dL, Women: Hgb <11 g/dL
        if sex == "male" and hemoglobin < self.ANEMIA_THRESHOLD_MALE:
            score += 1
        elif sex == "female" and hemoglobin < self.ANEMIA_THRESHOLD_FEMALE:
            score += 1
        
        # L - LDH > upper limit of normal (1 point)
        if ldh > ldh_upper_limit:
            score += 1
        
        # L - Last therapy <24 months since initiation (1 point)
        if months_since_last_therapy < self.MONTHS_SINCE_THERAPY_THRESHOLD:
            score += 1
        
        return score
    
    def _get_interpretation(self, score: int) -> Dict[str, str]:
        """
        Determines the interpretation based on the BALL Score
        
        Args:
            score (int): Calculated BALL Score (0-4)
            
        Returns:
            Dict with interpretation details
        """
        
        if score <= 1:
            return {
                "stage": "Low Risk",
                "description": "Low risk group",
                "interpretation": (
                    "Low risk for mortality. Estimated 24-month overall survival: 89.7%. "
                    "Patients in this group have a favorable prognosis on targeted therapy."
                )
            }
        elif score <= 3:
            return {
                "stage": "Intermediate Risk",
                "description": "Intermediate risk group",
                "interpretation": (
                    "Intermediate risk for mortality. Estimated 24-month overall survival: 79.5%. "
                    "Patients require close monitoring and may benefit from more intensive surveillance."
                )
            }
        else:  # score = 4
            return {
                "stage": "High Risk",
                "description": "High risk group",
                "interpretation": (
                    "High risk for mortality. Estimated 24-month overall survival: 55.8%. "
                    "Consider more aggressive treatment strategies or clinical trial enrollment."
                )
            }


def calculate_ball_score_rr_cll(beta2_microglobulin: float, hemoglobin: float, 
                               sex: str, ldh: float, ldh_upper_limit: float,
                               months_since_last_therapy: int) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = BallScoreRrCllCalculator()
    return calculator.calculate(beta2_microglobulin, hemoglobin, sex, ldh, 
                              ldh_upper_limit, months_since_last_therapy)