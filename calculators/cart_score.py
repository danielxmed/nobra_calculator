"""
CART (Cardiac Arrest Risk Triage) Score Calculator

Predicts risk of in-hospital cardiac arrest within 48 hours using vital signs and age.
Developed to identify hospitalized patients at high risk for cardiac arrest.

References:
1. Churpek MM, Yuen TC, Park SY, Meltzer DO, Hall JB, Edelson DP. Derivation of a 
   cardiac arrest prediction model using ward vital signs. Crit Care Med. 2012 
   Jul;40(7):2102-8. doi: 10.1097/CCM.0b013e318250aa5a.
2. Churpek MM, Yuen TC, Winslow C, Hall J, Edelson DP. Multicenter development and 
   validation of a risk stratification tool for ward patients. Am J Respir Crit Care Med. 
   2014 Sep 15;190(6):649-55. doi: 10.1164/rccm.201406-1022OC.
3. Churpek MM, Yuen TC, Winslow C, Meltzer DO, Kattan MW, Edelson DP. Multicenter 
   comparison of machine learning methods and conventional regression for predicting 
   clinical deterioration on the wards. Crit Care Med. 2016 Feb;44(2):368-74.
"""

from typing import Dict, Any


class CartScoreCalculator:
    """Calculator for CART (Cardiac Arrest Risk Triage) Score"""
    
    def __init__(self):
        # Scoring tables for each parameter
        self.respiratory_rate_scores = {
            (0, 20): 0,      # <21
            (21, 23): 8,     # 21-23
            (24, 25): 12,    # 24-25
            (26, 29): 15,    # 26-29
            (30, 999): 22    # >29
        }
        
        self.heart_rate_scores = {
            (0, 109): 0,     # <110
            (110, 139): 4,   # 110-139
            (140, 999): 13   # >139
        }
        
        self.diastolic_bp_scores = {
            (50, 999): 0,    # >49
            (40, 49): 4,     # 40-49
            (35, 39): 6,     # 35-39
            (0, 34): 13      # <35
        }
        
        self.age_scores = {
            (0, 54): 0,      # <55
            (55, 69): 4,     # 55-69
            (70, 999): 9     # >69
        }
        
        # Risk threshold
        self.HIGH_RISK_THRESHOLD = 20
    
    def calculate(
        self,
        respiratory_rate: int,
        heart_rate: int,
        diastolic_bp: int,
        age: int
    ) -> Dict[str, Any]:
        """
        Calculates CART Score for predicting cardiac arrest risk
        
        Args:
            respiratory_rate: Respiratory rate in breaths/min
            heart_rate: Heart rate in beats/min
            diastolic_bp: Diastolic blood pressure in mmHg
            age: Patient age in years
            
        Returns:
            Dict with CART score and clinical interpretation
        """
        
        # Validate inputs
        self._validate_inputs(respiratory_rate, heart_rate, diastolic_bp, age)
        
        # Calculate component scores
        rr_score = self._get_respiratory_rate_score(respiratory_rate)
        hr_score = self._get_heart_rate_score(heart_rate)
        dbp_score = self._get_diastolic_bp_score(diastolic_bp)
        age_score = self._get_age_score(age)
        
        # Calculate total CART score
        total_score = rr_score + hr_score + dbp_score + age_score
        
        # Get interpretation
        interpretation = self._get_interpretation(total_score)
        
        return {
            "result": total_score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"],
            "component_scores": {
                "respiratory_rate_score": rr_score,
                "heart_rate_score": hr_score,
                "diastolic_bp_score": dbp_score,
                "age_score": age_score
            }
        }
    
    def _validate_inputs(self, rr: int, hr: int, dbp: int, age: int):
        """Validates input parameters"""
        
        if not isinstance(rr, int) or not (5 <= rr <= 60):
            raise ValueError("Respiratory rate must be an integer between 5-60 breaths/min")
        
        if not isinstance(hr, int) or not (30 <= hr <= 250):
            raise ValueError("Heart rate must be an integer between 30-250 beats/min")
        
        if not isinstance(dbp, int) or not (20 <= dbp <= 150):
            raise ValueError("Diastolic blood pressure must be an integer between 20-150 mmHg")
        
        if not isinstance(age, int) or not (18 <= age <= 120):
            raise ValueError("Age must be an integer between 18-120 years")
    
    def _get_respiratory_rate_score(self, rr: int) -> int:
        """Gets points for respiratory rate"""
        for (min_val, max_val), score in self.respiratory_rate_scores.items():
            if min_val <= rr <= max_val:
                return score
        return 0
    
    def _get_heart_rate_score(self, hr: int) -> int:
        """Gets points for heart rate"""
        for (min_val, max_val), score in self.heart_rate_scores.items():
            if min_val <= hr <= max_val:
                return score
        return 0
    
    def _get_diastolic_bp_score(self, dbp: int) -> int:
        """Gets points for diastolic blood pressure"""
        for (min_val, max_val), score in self.diastolic_bp_scores.items():
            if min_val <= dbp <= max_val:
                return score
        return 0
    
    def _get_age_score(self, age: int) -> int:
        """Gets points for age"""
        for (min_val, max_val), score in self.age_scores.items():
            if min_val <= age <= max_val:
                return score
        return 0
    
    def _get_interpretation(self, score: int) -> Dict[str, str]:
        """
        Determines clinical interpretation based on CART score
        
        Args:
            score: CART score (0-59 points)
            
        Returns:
            Dict with clinical interpretation
        """
        
        if score <= self.HIGH_RISK_THRESHOLD:
            return {
                "stage": "Low Risk",
                "description": "Low risk of cardiac arrest",
                "interpretation": f"CART Score {score} indicates low risk of cardiac arrest within 48 hours. Standard monitoring and care appropriate. Continue routine assessments and interventions. The patient's vital signs suggest stable cardiac status."
            }
        else:
            return {
                "stage": "High Risk",
                "description": "High risk of cardiac arrest",
                "interpretation": f"CART Score {score} indicates high risk of cardiac arrest within 48 hours. Consider intensive monitoring, rapid response team activation, or transfer to higher level of care. Implement aggressive interventions to address abnormal vital signs and consider ICU consultation."
            }


def calculate_cart_score(
    respiratory_rate: int,
    heart_rate: int,
    diastolic_bp: int,
    age: int
) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = CartScoreCalculator()
    return calculator.calculate(
        respiratory_rate=respiratory_rate,
        heart_rate=heart_rate,
        diastolic_bp=diastolic_bp,
        age=age
    )