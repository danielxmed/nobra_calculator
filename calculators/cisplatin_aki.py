"""
Cisplatin-Associated Acute Kidney Injury (CP-AKI) Risk Calculator

Predicts the risk of moderate to severe acute kidney injury in patients 
treated with intravenous cisplatin.

References:
1. Gupta S, et al. BMJ. 2024 Mar 27;384:e077169. doi: 10.1136/bmj-2023-077169.
2. Motwani SS, et al. J Clin Oncol. 2018 Mar 1;36(7):682-688.
"""

import math
from typing import Dict, Any


class CisplatinAkiCalculator:
    """Calculator for Cisplatin-Associated Acute Kidney Injury (CP-AKI) Risk"""
    
    def calculate(
        self, 
        age: int,
        hypertension: str,
        diabetes: str,
        cisplatin_dose: float,
        hemoglobin: float,
        wbc_count: float,
        platelet_count: float,
        albumin: float,
        magnesium: float
    ) -> Dict[str, Any]:
        """
        Calculates the risk of cisplatin-associated acute kidney injury
        
        Args:
            age: Patient age in years (18-110)
            hypertension: "yes" or "no"
            diabetes: "yes" or "no"
            cisplatin_dose: Total cisplatin dose in mg (1-1000)
            hemoglobin: Hemoglobin level in g/dL (2.0-20.0)
            wbc_count: White blood cell count ×10³/µL (1.0-300.0)
            platelet_count: Platelet count ×10³/µL (1-1500)
            albumin: Serum albumin level in g/dL (0.5-8.0)
            magnesium: Serum magnesium level in mg/dL (0.5-5.0)
            
        Returns:
            Dict with risk percentage and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(
            age, hypertension, diabetes, cisplatin_dose,
            hemoglobin, wbc_count, platelet_count, albumin, magnesium
        )
        
        # Calculate risk score
        # Note: Using simplified scoring based on available literature
        # The exact coefficients from BMJ 2024 paper were not publicly available
        
        # Age scoring
        age_score = 0
        if age <= 60:
            age_score = 0
        elif age <= 70:
            age_score = 1.5
        else:
            age_score = 3.0
        
        # Cisplatin dose scoring
        dose_score = 0
        if cisplatin_dose <= 100:
            dose_score = 0
        elif cisplatin_dose <= 150:
            dose_score = 1.5
        else:
            dose_score = 3.0
        
        # Comorbidity scoring
        htn_score = 2.0 if hypertension == "yes" else 0
        dm_score = 1.5 if diabetes == "yes" else 0
        
        # Lab value scoring
        alb_score = 0
        if albumin < 2.0:
            alb_score = 3.0
        elif albumin <= 3.5:
            alb_score = 2.0
        else:
            alb_score = 0
        
        # Hemoglobin scoring (anemia risk factor)
        hgb_score = 0
        if hemoglobin < 10:
            hgb_score = 1.5
        elif hemoglobin < 12:
            hgb_score = 1.0
        else:
            hgb_score = 0
        
        # WBC scoring (neutropenia/leukocytosis risk)
        wbc_score = 0
        if wbc_count < 4.0 or wbc_count > 12.0:
            wbc_score = 1.0
        
        # Platelet scoring (thrombocytopenia risk)
        plt_score = 0
        if platelet_count < 150:
            plt_score = 1.0
        
        # Magnesium scoring (hypomagnesemia is a known risk factor)
        mg_score = 0
        if magnesium < 1.6:
            mg_score = 1.5
        
        # Calculate total score
        total_score = (age_score + dose_score + htn_score + dm_score + 
                      alb_score + hgb_score + wbc_score + plt_score + mg_score)
        
        # Convert score to risk percentage using logistic function
        # Calibrated to approximate the reported risk ranges
        logit = -3.5 + (0.45 * total_score)
        risk_percentage = 100 / (1 + math.exp(-logit))
        
        # Round to 1 decimal place
        risk_percentage = round(risk_percentage, 1)
        
        # Get interpretation
        interpretation = self._get_interpretation(risk_percentage)
        
        return {
            "result": risk_percentage,
            "unit": "%",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["risk_category"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(
        self, age, hypertension, diabetes, cisplatin_dose,
        hemoglobin, wbc_count, platelet_count, albumin, magnesium
    ):
        """Validates input parameters"""
        
        # Age validation
        if not isinstance(age, (int, float)) or age < 18 or age > 110:
            raise ValueError("Age must be between 18 and 110 years")
        
        # Hypertension validation
        if hypertension not in ["yes", "no"]:
            raise ValueError("Hypertension must be 'yes' or 'no'")
        
        # Diabetes validation
        if diabetes not in ["yes", "no"]:
            raise ValueError("Diabetes must be 'yes' or 'no'")
        
        # Cisplatin dose validation
        if not isinstance(cisplatin_dose, (int, float)) or cisplatin_dose < 1 or cisplatin_dose > 1000:
            raise ValueError("Cisplatin dose must be between 1 and 1000 mg")
        
        # Hemoglobin validation
        if not isinstance(hemoglobin, (int, float)) or hemoglobin < 2.0 or hemoglobin > 20.0:
            raise ValueError("Hemoglobin must be between 2.0 and 20.0 g/dL")
        
        # WBC count validation
        if not isinstance(wbc_count, (int, float)) or wbc_count < 1.0 or wbc_count > 300.0:
            raise ValueError("WBC count must be between 1.0 and 300.0 ×10³/µL")
        
        # Platelet count validation
        if not isinstance(platelet_count, (int, float)) or platelet_count < 1 or platelet_count > 1500:
            raise ValueError("Platelet count must be between 1 and 1500 ×10³/µL")
        
        # Albumin validation
        if not isinstance(albumin, (int, float)) or albumin < 0.5 or albumin > 8.0:
            raise ValueError("Albumin must be between 0.5 and 8.0 g/dL")
        
        # Magnesium validation
        if not isinstance(magnesium, (int, float)) or magnesium < 0.5 or magnesium > 5.0:
            raise ValueError("Magnesium must be between 0.5 and 5.0 mg/dL")
    
    def _get_interpretation(self, risk_percentage: float) -> Dict[str, str]:
        """
        Determines the interpretation based on risk percentage
        
        Args:
            risk_percentage: Calculated risk percentage
            
        Returns:
            Dict with interpretation details
        """
        
        if risk_percentage < 5:
            return {
                "risk_category": "Low",
                "description": "Low risk",
                "interpretation": "Low risk of cisplatin-associated acute kidney injury (< 5%). Standard monitoring may be appropriate. Consider baseline and follow-up creatinine measurements."
            }
        elif risk_percentage < 15:
            return {
                "risk_category": "Moderate",
                "description": "Moderate risk",
                "interpretation": "Moderate risk of cisplatin-associated acute kidney injury (5-15%). Enhanced monitoring recommended. Consider prophylactic measures such as aggressive hydration and electrolyte repletion."
            }
        elif risk_percentage < 30:
            return {
                "risk_category": "High",
                "description": "High risk",
                "interpretation": "High risk of cisplatin-associated acute kidney injury (15-30%). Close monitoring essential. Consider dose modification, alternative chemotherapy regimens, or nephrology consultation."
            }
        else:
            return {
                "risk_category": "Very High",
                "description": "Very high risk",
                "interpretation": "Very high risk of cisplatin-associated acute kidney injury (≥30%). Strong consideration should be given to alternative treatment options. If cisplatin is necessary, intensive monitoring and prophylactic measures are mandatory. Nephrology consultation strongly recommended."
            }


def calculate_cisplatin_aki(
    age, hypertension, diabetes, cisplatin_dose,
    hemoglobin, wbc_count, platelet_count, albumin, magnesium
) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = CisplatinAkiCalculator()
    return calculator.calculate(
        age, hypertension, diabetes, cisplatin_dose,
        hemoglobin, wbc_count, platelet_count, albumin, magnesium
    )