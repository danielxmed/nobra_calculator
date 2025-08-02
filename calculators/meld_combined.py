"""
Model for End-Stage Liver Disease (Combined MELD) Calculator

Offers multiple versions of MELD for liver transplant planning and 
end-stage liver disease severity assessment.

References:
1. Kamath PS, et al. Hepatology. 2001;33(2):464-70.
2. Wiesner R, et al. Gastroenterology. 2003;124(1):91-6.
3. Kim WR, et al. N Engl J Med. 2008;359(10):1018-26.
4. Kim WR, et al. Gastroenterology. 2021;161(6):1887-1895.
"""

import math
from typing import Dict, Any, Optional


class MeldCombinedCalculator:
    """Calculator for Model for End-Stage Liver Disease (Combined MELD)"""
    
    def __init__(self):
        # Constants for MELD calculations
        self.MIN_BILIRUBIN = 1.0
        self.MIN_CREATININE = 1.0
        self.MIN_INR = 1.0
        self.MAX_CREATININE = 4.0
        self.MIN_SODIUM = 125
        self.MAX_SODIUM = 137
        self.MAX_SCORE = 40
        self.MIN_SCORE = 6
    
    def calculate(self, meld_version: str, bilirubin: float, creatinine: float, 
                  inr: float, sodium: Optional[float] = None, 
                  albumin: Optional[float] = None, age: Optional[int] = None,
                  sex: Optional[str] = None, 
                  dialysis_twice_in_week: Optional[str] = None) -> Dict[str, Any]:
        """
        Calculates MELD score using specified version
        
        Args:
            meld_version: MELD version ("original", "meld_na", "meld_3_0")
            bilirubin: Serum bilirubin in mg/dL
            creatinine: Serum creatinine in mg/dL
            inr: International Normalized Ratio
            sodium: Serum sodium in mEq/L (for MELD-Na and MELD 3.0)
            albumin: Serum albumin in g/dL (for MELD 3.0)
            age: Patient age in years (for MELD 3.0)
            sex: Patient sex ("male", "female") (for MELD 3.0)
            dialysis_twice_in_week: Dialysis status ("yes", "no")
            
        Returns:
            Dict with MELD score and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(meld_version, bilirubin, creatinine, inr, 
                            sodium, albumin, age, sex, dialysis_twice_in_week)
        
        # Calculate score based on version
        if meld_version == "original":
            score = self._calculate_original_meld(bilirubin, creatinine, inr, dialysis_twice_in_week)
        elif meld_version == "meld_na":
            score = self._calculate_meld_na(bilirubin, creatinine, inr, sodium, dialysis_twice_in_week)
        elif meld_version == "meld_3_0":
            score = self._calculate_meld_3_0(bilirubin, creatinine, inr, sodium, 
                                           albumin, age, sex, dialysis_twice_in_week)
        else:
            raise ValueError(f"Unknown MELD version: {meld_version}")
        
        # Get interpretation
        interpretation = self._get_interpretation(score)
        
        return {
            "result": score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, meld_version: str, bilirubin: float, creatinine: float, 
                        inr: float, sodium: Optional[float], albumin: Optional[float], 
                        age: Optional[int], sex: Optional[str], 
                        dialysis_twice_in_week: Optional[str]):
        """Validates input parameters based on MELD version"""
        
        valid_versions = ["original", "meld_na", "meld_3_0"]
        if meld_version not in valid_versions:
            raise ValueError(f"meld_version must be one of: {', '.join(valid_versions)}")
        
        # Basic parameter validation
        if bilirubin < 0.1 or bilirubin > 50.0:
            raise ValueError("bilirubin must be between 0.1 and 50.0 mg/dL")
        if creatinine < 0.1 or creatinine > 15.0:
            raise ValueError("creatinine must be between 0.1 and 15.0 mg/dL")
        if inr < 0.8 or inr > 10.0:
            raise ValueError("inr must be between 0.8 and 10.0")
        
        # Version-specific validation
        if meld_version in ["meld_na", "meld_3_0"]:
            if sodium is None:
                raise ValueError(f"sodium is required for {meld_version}")
            if sodium < 120 or sodium > 160:
                raise ValueError("sodium must be between 120 and 160 mEq/L")
        
        if meld_version == "meld_3_0":
            if albumin is None:
                raise ValueError("albumin is required for MELD 3.0")
            if age is None:
                raise ValueError("age is required for MELD 3.0")
            if sex is None:
                raise ValueError("sex is required for MELD 3.0")
            
            if albumin < 1.0 or albumin > 6.0:
                raise ValueError("albumin must be between 1.0 and 6.0 g/dL")
            if age < 12 or age > 120:
                raise ValueError("age must be between 12 and 120 years")
            if sex not in ["male", "female"]:
                raise ValueError("sex must be 'male' or 'female'")
        
        if dialysis_twice_in_week and dialysis_twice_in_week not in ["yes", "no"]:
            raise ValueError("dialysis_twice_in_week must be 'yes' or 'no'")
    
    def _calculate_original_meld(self, bilirubin: float, creatinine: float, 
                               inr: float, dialysis_twice_in_week: Optional[str]) -> int:
        """Calculates original MELD score"""
        
        # Apply minimum values
        bili = max(bilirubin, self.MIN_BILIRUBIN)
        creat = max(creatinine, self.MIN_CREATININE)
        inr_val = max(inr, self.MIN_INR)
        
        # Apply maximum creatinine and dialysis adjustment
        if dialysis_twice_in_week == "yes":
            creat = self.MAX_CREATININE
        else:
            creat = min(creat, self.MAX_CREATININE)
        
        # Original MELD formula (9.57 × ln(creatinine) + 3.78 × ln(bilirubin) + 11.2 × ln(INR) + 6.43)
        score = (9.57 * math.log(creat) + 
                3.78 * math.log(bili) + 
                11.2 * math.log(inr_val) + 
                6.43)
        
        # Round and clamp
        score = round(score)
        return max(self.MIN_SCORE, min(score, self.MAX_SCORE))
    
    def _calculate_meld_na(self, bilirubin: float, creatinine: float, inr: float,
                          sodium: float, dialysis_twice_in_week: Optional[str]) -> int:
        """Calculates MELD-Na score"""
        
        # Calculate original MELD first
        meld_score = self._calculate_original_meld(bilirubin, creatinine, inr, dialysis_twice_in_week)
        
        # Apply sodium adjustment
        na = max(self.MIN_SODIUM, min(sodium, self.MAX_SODIUM))
        
        # MELD-Na formula
        if meld_score > 11:
            meld_na = meld_score + 1.32 * (137 - na) - (0.033 * meld_score * (137 - na))
        else:
            meld_na = meld_score
        
        # Round and clamp
        meld_na = round(meld_na)
        return max(self.MIN_SCORE, min(meld_na, self.MAX_SCORE))
    
    def _calculate_meld_3_0(self, bilirubin: float, creatinine: float, inr: float,
                           sodium: float, albumin: float, age: int, sex: str,
                           dialysis_twice_in_week: Optional[str]) -> int:
        """Calculates MELD 3.0 score"""
        
        # Apply minimum values and adjustments
        bili = max(bilirubin, self.MIN_BILIRUBIN)
        creat = max(creatinine, self.MIN_CREATININE)
        inr_val = max(inr, self.MIN_INR)
        
        # Apply maximum creatinine and dialysis adjustment
        if dialysis_twice_in_week == "yes":
            creat = self.MAX_CREATININE
        else:
            creat = min(creat, self.MAX_CREATININE)
        
        # Clamp sodium and albumin
        na = max(self.MIN_SODIUM, min(sodium, self.MAX_SODIUM))
        alb = max(1.5, min(albumin, 3.5))  # MELD 3.0 specific albumin range
        
        # Sex coefficient
        sex_coeff = 1.33 if sex == "female" else 1.0
        
        # Age-specific formulas
        if age >= 18:
            # Adult formula
            score = (1.33 * sex_coeff * 
                    (4.56 * math.log(bili) + 
                     0.82 * (137 - na) - 
                     0.24 * (137 - na) * math.log(bili) + 
                     9.09 * math.log(inr_val) + 
                     11.14 * math.log(creat) + 
                     1.85 * (3.5 - alb) - 
                     1.83 * (3.5 - alb) * math.log(creat) + 
                     6.0))
        else:
            # Pediatric formula (12-18 years)
            score = (1.33 * sex_coeff * 
                    (4.56 * math.log(bili) + 
                     0.82 * (137 - na) - 
                     0.24 * (137 - na) * math.log(bili) + 
                     9.09 * math.log(inr_val) + 
                     11.14 * math.log(creat) + 
                     1.85 * (3.5 - alb) - 
                     1.83 * (3.5 - alb) * math.log(creat) + 
                     6.0))
        
        # Round and clamp
        score = round(score)
        return max(self.MIN_SCORE, min(score, self.MAX_SCORE))
    
    def _get_interpretation(self, score: int) -> Dict[str, str]:
        """
        Provides clinical interpretation based on MELD score
        
        Args:
            score: MELD score (6-40)
            
        Returns:
            Dict with interpretation details
        """
        
        if 6 <= score <= 9:
            return {
                "stage": "Mild Disease",
                "description": "Lower mortality risk",
                "interpretation": ("Mild liver disease with low 90-day mortality risk (<2%). "
                                 "Generally not considered for liver transplantation unless "
                                 "specific indications present.")
            }
        elif 10 <= score <= 14:
            return {
                "stage": "Moderate Disease", 
                "description": "Moderate mortality risk",
                "interpretation": ("Moderate liver disease with intermediate mortality risk (6-20%). "
                                 "May be considered for liver transplantation evaluation depending "
                                 "on clinical circumstances.")
            }
        elif 15 <= score <= 19:
            return {
                "stage": "Severe Disease",
                "description": "High mortality risk",
                "interpretation": ("Severe liver disease with high mortality risk (>20%). Strong "
                                 "indication for liver transplantation evaluation. MELD ≥15 is "
                                 "generally the threshold for transplant consideration.")
            }
        elif 20 <= score <= 29:
            return {
                "stage": "Very Severe Disease",
                "description": "Very high mortality risk",
                "interpretation": ("Very severe liver disease with very high mortality risk (>50%). "
                                 "High priority for liver transplantation. Close monitoring and "
                                 "intensive management required.")
            }
        else:  # 30-40
            return {
                "stage": "Critical Disease",
                "description": "Extremely high mortality risk",
                "interpretation": ("Critical liver disease with extremely high mortality risk (>80%). "
                                 "Highest priority for liver transplantation. Consider intensive "
                                 "care management and urgent transplant evaluation.")
            }


def calculate_meld_combined(meld_version: str, bilirubin: float, creatinine: float,
                          inr: float, sodium: Optional[float] = None,
                          albumin: Optional[float] = None, age: Optional[int] = None,
                          sex: Optional[str] = None, 
                          dialysis_twice_in_week: Optional[str] = None) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = MeldCombinedCalculator()
    return calculator.calculate(meld_version, bilirubin, creatinine, inr, 
                              sodium, albumin, age, sex, dialysis_twice_in_week)