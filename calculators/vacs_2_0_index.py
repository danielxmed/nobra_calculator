"""
Veterans Aging Cohort Study (VACS) 2.0 Index Calculator

Estimates 5-year all-cause mortality risk in patients with HIV using age, HIV-specific 
biomarkers, and general health indicators.

References:
1. Justice AC, McGinnis KA, Skanderson M, et al. Towards a combined prognostic index 
   for survival in HIV infection: the role of 'non-HIV' biomarkers. HIV Med. 2010;11(2):143-51.
2. Tate JP, Justice AC, Hughes MD, et al. An internationally generalizable risk index 
   for mortality after one year of antiretroviral therapy. AIDS. 2013;27(4):563-72.
3. Rodriguez-Barradas MC, Tate JP, Justice AC, et al. Albumin, white blood cell count, 
   and body mass index improve discrimination of mortality in HIV-positive individuals. 
   AIDS. 2019;33(6):903-912.
"""

import math
from typing import Dict, Any


class Vacs20IndexCalculator:
    """Calculator for Veterans Aging Cohort Study (VACS) 2.0 Index"""
    
    def __init__(self):
        # Based on research findings about parameter influences and score ranges
        # These coefficients are approximated from the published literature
        # and should be validated against the official VACS calculator
        
        # Age scoring: 30 years = 32 points, 75 years = 59 points (range 27 points)
        self.AGE_COEFFICIENT = 0.6  # Approximate coefficient for age scoring
        self.AGE_BASE = 14  # Base adjustment for age calculation
        
        # Albumin scoring: 2.0 g/dL = 65 points, 5.0 g/dL = 39 points (range 26 points)
        self.ALBUMIN_COEFFICIENT = -8.67  # Coefficient for albumin (inverted relationship)
        self.ALBUMIN_BASE = 82.34  # Base adjustment for albumin calculation
        
        # Other parameter coefficients based on their relative influence
        # CD4 count: 10-900 cells/ul (23 points range)
        self.CD4_COEFFICIENT = -0.026  # Inverted relationship
        self.CD4_BASE = 23
        
        # HIV RNA: 1.3-5.0 log10 copies/mL (18 points range)
        self.HIV_RNA_COEFFICIENT = 4.86  # Positive relationship
        self.HIV_RNA_BASE = -6.32
        
        # FIB-4: 0.5-7.5 (20 points range)
        self.FIB4_COEFFICIENT = 2.86  # Positive relationship
        self.FIB4_BASE = -1.43
        
        # BMI: 15-35 kg/m2 (20 points range)
        self.BMI_COEFFICIENT = -0.5  # Inverted relationship (higher BMI = lower risk to a point)
        self.BMI_BASE = 12.5
        
        # Hemoglobin: 9-16 g/dl (16 points range)
        self.HEMOGLOBIN_COEFFICIENT = -2.29  # Inverted relationship
        self.HEMOGLOBIN_BASE = 32.64
        
        # eGFR: 0-180 ml/min (16 points range)
        self.EGFR_COEFFICIENT = -0.089  # Inverted relationship
        self.EGFR_BASE = 16
        
        # WBC count coefficient (approximate)
        self.WBC_COEFFICIENT = 0.5  # Positive relationship
        self.WBC_BASE = 0
        
        # HCV status: 6 points if positive
        self.HCV_POINTS = 6
    
    def calculate(self, age: int, sex: str, race: str, cd4_count: int, hiv_rna_log: float,
                 hemoglobin: float, platelets: int, ast: int, alt: int, creatinine: float,
                 albumin: float, wbc_count: float, bmi: float, hepatitis_c: str) -> Dict[str, Any]:
        """
        Calculates the VACS 2.0 Index score
        
        Args:
            age (int): Patient age in years
            sex (str): Patient sex ('male' or 'female')
            race (str): Patient race ('black' or 'non_black')
            cd4_count (int): CD4 T-cell count (cells/μL)
            hiv_rna_log (float): HIV-1 RNA viral load (log10 copies/mL)
            hemoglobin (float): Hemoglobin level (g/dL)
            platelets (int): Platelet count (×10³/μL)
            ast (int): Aspartate aminotransferase (U/L)
            alt (int): Alanine aminotransferase (U/L)
            creatinine (float): Serum creatinine (mg/dL)
            albumin (float): Serum albumin (g/dL)
            wbc_count (float): White blood cell count (×10³/μL)
            bmi (float): Body mass index (kg/m²)
            hepatitis_c (str): Hepatitis C virus co-infection ('yes' or 'no')
            
        Returns:
            Dict with VACS 2.0 Index score and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(age, sex, race, cd4_count, hiv_rna_log, hemoglobin, platelets,
                            ast, alt, creatinine, albumin, wbc_count, bmi, hepatitis_c)
        
        # Calculate composite biomarkers
        fib4_score = self._calculate_fib4(age, ast, alt, platelets)
        egfr = self._calculate_egfr(creatinine, age, sex, race)
        
        # Calculate individual component scores
        age_score = self._calculate_age_score(age)
        cd4_score = self._calculate_cd4_score(cd4_count)
        hiv_rna_score = self._calculate_hiv_rna_score(hiv_rna_log)
        hemoglobin_score = self._calculate_hemoglobin_score(hemoglobin)
        fib4_component_score = self._calculate_fib4_score(fib4_score)
        egfr_score = self._calculate_egfr_score(egfr)
        albumin_score = self._calculate_albumin_score(albumin)
        wbc_score = self._calculate_wbc_score(wbc_count)
        bmi_score = self._calculate_bmi_score(bmi)
        hcv_score = self._calculate_hcv_score(hepatitis_c)
        
        # Calculate total VACS 2.0 score
        total_score = (age_score + cd4_score + hiv_rna_score + hemoglobin_score + 
                      fib4_component_score + egfr_score + albumin_score + wbc_score + 
                      bmi_score + hcv_score)
        
        # Ensure score is within reasonable bounds (0-164)
        total_score = max(0, min(164, total_score))
        
        # Get interpretation
        interpretation = self._get_interpretation(total_score)
        
        return {
            "result": round(total_score, 1),
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"],
            "component_scores": {
                "age_score": round(age_score, 1),
                "cd4_score": round(cd4_score, 1),
                "hiv_rna_score": round(hiv_rna_score, 1),
                "hemoglobin_score": round(hemoglobin_score, 1),
                "fib4_score": round(fib4_component_score, 1),
                "egfr_score": round(egfr_score, 1),
                "albumin_score": round(albumin_score, 1),
                "wbc_score": round(wbc_score, 1),
                "bmi_score": round(bmi_score, 1),
                "hcv_score": round(hcv_score, 1)
            },
            "composite_biomarkers": {
                "fib4": round(fib4_score, 2),
                "egfr": round(egfr, 1)
            },
            "mortality_risk_5year": self._estimate_mortality_risk(total_score)
        }
    
    def _validate_inputs(self, age, sex, race, cd4_count, hiv_rna_log, hemoglobin, platelets,
                        ast, alt, creatinine, albumin, wbc_count, bmi, hepatitis_c):
        """Validates input parameters"""
        
        if not isinstance(age, int) or age < 18 or age > 100:
            raise ValueError("Age must be an integer between 18 and 100 years")
        
        if sex not in ["male", "female"]:
            raise ValueError("Sex must be 'male' or 'female'")
        
        if race not in ["black", "non_black"]:
            raise ValueError("Race must be 'black' or 'non_black'")
        
        if not isinstance(cd4_count, int) or cd4_count < 0 or cd4_count > 2000:
            raise ValueError("CD4 count must be an integer between 0 and 2000 cells/μL")
        
        if hiv_rna_log < 0.0 or hiv_rna_log > 7.0:
            raise ValueError("HIV RNA log must be between 0.0 and 7.0 log10 copies/mL")
        
        if hemoglobin < 5.0 or hemoglobin > 20.0:
            raise ValueError("Hemoglobin must be between 5.0 and 20.0 g/dL")
        
        if not isinstance(platelets, int) or platelets < 10 or platelets > 1000:
            raise ValueError("Platelets must be an integer between 10 and 1000 ×10³/μL")
        
        if not isinstance(ast, int) or ast < 10 or ast > 500:
            raise ValueError("AST must be an integer between 10 and 500 U/L")
        
        if not isinstance(alt, int) or alt < 10 or alt > 500:
            raise ValueError("ALT must be an integer between 10 and 500 U/L")
        
        if creatinine < 0.5 or creatinine > 10.0:
            raise ValueError("Creatinine must be between 0.5 and 10.0 mg/dL")
        
        if albumin < 1.0 or albumin > 6.0:
            raise ValueError("Albumin must be between 1.0 and 6.0 g/dL")
        
        if wbc_count < 1.0 or wbc_count > 50.0:
            raise ValueError("WBC count must be between 1.0 and 50.0 ×10³/μL")
        
        if bmi < 10.0 or bmi > 50.0:
            raise ValueError("BMI must be between 10.0 and 50.0 kg/m²")
        
        if hepatitis_c not in ["yes", "no"]:
            raise ValueError("Hepatitis C status must be 'yes' or 'no'")
    
    def _calculate_fib4(self, age: int, ast: int, alt: int, platelets: int) -> float:
        """Calculates FIB-4 score: (Age × AST) / (Platelets × √ALT)"""
        return (age * ast) / (platelets * math.sqrt(alt))
    
    def _calculate_egfr(self, creatinine: float, age: int, sex: str, race: str) -> float:
        """Calculates eGFR using CKD-EPI equation"""
        # CKD-EPI equation
        if sex == "female":
            if creatinine <= 0.7:
                egfr = 144 * (creatinine / 0.7) ** (-0.329) * (0.993 ** age)
            else:
                egfr = 144 * (creatinine / 0.7) ** (-1.209) * (0.993 ** age)
        else:  # male
            if creatinine <= 0.9:
                egfr = 141 * (creatinine / 0.9) ** (-0.411) * (0.993 ** age)
            else:
                egfr = 141 * (creatinine / 0.9) ** (-1.209) * (0.993 ** age)
        
        # Adjust for race
        if race == "black":
            egfr *= 1.159
        
        return egfr
    
    def _calculate_age_score(self, age: int) -> float:
        """Calculates age component score"""
        return max(0, (age * self.AGE_COEFFICIENT) + self.AGE_BASE)
    
    def _calculate_cd4_score(self, cd4_count: int) -> float:
        """Calculates CD4 component score"""
        return max(0, (cd4_count * self.CD4_COEFFICIENT) + self.CD4_BASE)
    
    def _calculate_hiv_rna_score(self, hiv_rna_log: float) -> float:
        """Calculates HIV RNA component score"""
        return max(0, (hiv_rna_log * self.HIV_RNA_COEFFICIENT) + self.HIV_RNA_BASE)
    
    def _calculate_hemoglobin_score(self, hemoglobin: float) -> float:
        """Calculates hemoglobin component score"""
        return max(0, (hemoglobin * self.HEMOGLOBIN_COEFFICIENT) + self.HEMOGLOBIN_BASE)
    
    def _calculate_fib4_score(self, fib4: float) -> float:
        """Calculates FIB-4 component score"""
        return max(0, (fib4 * self.FIB4_COEFFICIENT) + self.FIB4_BASE)
    
    def _calculate_egfr_score(self, egfr: float) -> float:
        """Calculates eGFR component score"""
        return max(0, (egfr * self.EGFR_COEFFICIENT) + self.EGFR_BASE)
    
    def _calculate_albumin_score(self, albumin: float) -> float:
        """Calculates albumin component score"""
        return max(0, (albumin * self.ALBUMIN_COEFFICIENT) + self.ALBUMIN_BASE)
    
    def _calculate_wbc_score(self, wbc_count: float) -> float:
        """Calculates WBC component score"""
        return max(0, (wbc_count * self.WBC_COEFFICIENT) + self.WBC_BASE)
    
    def _calculate_bmi_score(self, bmi: float) -> float:
        """Calculates BMI component score"""
        return max(0, (bmi * self.BMI_COEFFICIENT) + self.BMI_BASE)
    
    def _calculate_hcv_score(self, hepatitis_c: str) -> float:
        """Calculates HCV component score"""
        return self.HCV_POINTS if hepatitis_c == "yes" else 0
    
    def _estimate_mortality_risk(self, vacs_score: float) -> str:
        """Estimates 5-year mortality risk based on VACS score"""
        # Based on research: mortality approximately doubles for every 10-unit increase
        # Mean score of 38 = 1% mortality risk
        base_score = 38
        base_risk = 1.0
        
        if vacs_score <= base_score:
            # Linear interpolation below base score
            risk = base_risk * (vacs_score / base_score)
        else:
            # Exponential increase above base score
            score_difference = vacs_score - base_score
            risk_multiplier = 2 ** (score_difference / 10)
            risk = base_risk * risk_multiplier
        
        # Cap at 95% maximum risk
        risk = min(95.0, risk)
        
        return f"Approximately {risk:.1f}% 5-year mortality risk"
    
    def _get_interpretation(self, score: float) -> Dict[str, str]:
        """
        Determines the interpretation based on the VACS 2.0 score
        
        Args:
            score (float): Calculated VACS 2.0 score
            
        Returns:
            Dict with interpretation details
        """
        
        if score <= 25:
            return {
                "stage": "Low Risk",
                "description": "Low 5-year mortality risk",
                "interpretation": (f"VACS 2.0 Index score: {score:.1f} points. Low disease burden "
                                f"and mortality risk. Continue routine HIV care and monitoring. "
                                f"Excellent prognosis with current management.")
            }
        elif score <= 50:
            return {
                "stage": "Moderate Risk",
                "description": "Moderate 5-year mortality risk",
                "interpretation": (f"VACS 2.0 Index score: {score:.1f} points. Moderate disease burden. "
                                f"Consider enhanced monitoring and preventive interventions. "
                                f"Optimize HIV therapy and address modifiable risk factors.")
            }
        elif score <= 75:
            return {
                "stage": "High Risk",
                "description": "High 5-year mortality risk",
                "interpretation": (f"VACS 2.0 Index score: {score:.1f} points. High disease burden. "
                                f"Intensify monitoring, optimize HIV therapy, and address comorbidities. "
                                f"Consider multidisciplinary care approach.")
            }
        else:
            return {
                "stage": "Very High Risk",
                "description": "Very high 5-year mortality risk",
                "interpretation": (f"VACS 2.0 Index score: {score:.1f} points. Very high disease burden. "
                                f"Consider aggressive intervention strategies and end-of-life planning "
                                f"discussions. Urgent optimization of all modifiable factors.")
            }


def calculate_vacs_2_0_index(age, sex, race, cd4_count, hiv_rna_log, hemoglobin, platelets,
                           ast, alt, creatinine, albumin, wbc_count, bmi, hepatitis_c) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_vacs_2_0_index pattern
    """
    calculator = Vacs20IndexCalculator()
    return calculator.calculate(age, sex, race, cd4_count, hiv_rna_log, hemoglobin, platelets,
                              ast, alt, creatinine, albumin, wbc_count, bmi, hepatitis_c)