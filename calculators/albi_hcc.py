"""
ALBI (Albumin-Bilirubin) Grade for Hepatocellular Carcinoma (HCC) Calculator

Predicts survival in hepatocellular carcinoma patients based on serum albumin 
and bilirubin concentrations as an alternative to Child-Pugh grade.

References:
- Johnson PJ, Berhane S, Kagebayashi C, et al. Assessment of liver function in 
  patients with hepatocellular carcinoma: a new evidence-based approach-the ALBI grade. 
  J Clin Oncol. 2015;33(6):550-8.
- Hiraoka A, Michitaka K, Kumada T, et al. Validation and Potential of Albumin-Bilirubin 
  Grade and Prognostication in a Nationwide Survey of 46,681 Hepatocellular Carcinoma 
  Patients in Japan. Liver Cancer. 2017;6(4):325-336.
"""

import math
from typing import Dict, Any


class AlbiHccCalculator:
    """Calculator for ALBI (Albumin-Bilirubin) Grade for HCC"""
    
    def __init__(self):
        # ALBI grade thresholds and survival data
        self.GRADE_THRESHOLDS = {
            1: {"max": -2.60, "survival_range": "18.5 - 85.6 months"},
            2: {"min": -2.60, "max": -1.39, "survival_range": "5.3 - 46.5 months"},
            3: {"min": -1.39, "survival_range": "2.3 - 15.5 months"}
        }
        
        # Formula coefficients
        self.BILIRUBIN_COEFF = 0.66
        self.ALBUMIN_COEFF = -0.085
    
    def calculate(self, albumin: float, bilirubin: float) -> Dict[str, Any]:
        """
        Calculates the ALBI score and grade using the provided parameters
        
        Args:
            albumin (float): Serum albumin concentration in g/L
            bilirubin (float): Serum bilirubin concentration in μmol/L
            
        Returns:
            Dict with the ALBI score, grade, and survival interpretation
        """
        
        # Validations
        self._validate_inputs(albumin, bilirubin)
        
        # Calculate ALBI score
        albi_score = self._calculate_albi_score(albumin, bilirubin)
        
        # Determine grade and interpretation
        grade_info = self._get_grade_interpretation(albi_score)
        
        return {
            "result": round(albi_score, 3),
            "unit": "score",
            "interpretation": grade_info["interpretation"],
            "stage": grade_info["stage"],
            "stage_description": grade_info["description"],
            "grade": grade_info["grade"],
            "survival_range": grade_info["survival_range"]
        }
    
    def _validate_inputs(self, albumin: float, bilirubin: float):
        """Validates input parameters"""
        
        if not isinstance(albumin, (int, float)):
            raise ValueError("Albumin must be a number")
        
        if not isinstance(bilirubin, (int, float)):
            raise ValueError("Bilirubin must be a number")
        
        if albumin < 1.0 or albumin > 6.0:
            raise ValueError("Albumin must be between 1.0 and 6.0 g/L")
        
        if bilirubin < 3.0 or bilirubin > 500.0:
            raise ValueError("Bilirubin must be between 3.0 and 500.0 μmol/L")
    
    def _calculate_albi_score(self, albumin: float, bilirubin: float) -> float:
        """
        Implements the ALBI score formula
        
        ALBI = (log10 bilirubin × 0.66) + (albumin × -0.085)
        where bilirubin is in μmol/L and albumin is in g/L
        """
        
        # Calculate log10 of bilirubin
        log_bilirubin = math.log10(bilirubin)
        
        # Apply ALBI formula
        albi_score = (log_bilirubin * self.BILIRUBIN_COEFF) + (albumin * self.ALBUMIN_COEFF)
        
        return albi_score
    
    def _get_grade_interpretation(self, albi_score: float) -> Dict[str, str]:
        """
        Determines the ALBI grade and interpretation based on the score
        
        Args:
            albi_score (float): Calculated ALBI score
            
        Returns:
            Dict with grade information and interpretation
        """
        
        if albi_score <= -2.60:
            return {
                "grade": 1,
                "stage": "Grade 1",
                "description": "Best prognosis",
                "survival_range": self.GRADE_THRESHOLDS[1]["survival_range"],
                "interpretation": f"ALBI Grade 1 (score ≤-2.60). Median survival: {self.GRADE_THRESHOLDS[1]['survival_range']}. Best liver function and prognosis in HCC patients. This grade indicates relatively preserved liver function with the longest expected survival among HCC patients."
            }
        elif albi_score <= -1.39:
            return {
                "grade": 2,
                "stage": "Grade 2", 
                "description": "Intermediate prognosis",
                "survival_range": self.GRADE_THRESHOLDS[2]["survival_range"],
                "interpretation": f"ALBI Grade 2 (score >-2.60 to ≤-1.39). Median survival: {self.GRADE_THRESHOLDS[2]['survival_range']}. Intermediate liver function and prognosis in HCC patients. This grade indicates moderately impaired liver function with intermediate survival expectations."
            }
        else:
            return {
                "grade": 3,
                "stage": "Grade 3",
                "description": "Poorest prognosis", 
                "survival_range": self.GRADE_THRESHOLDS[3]["survival_range"],
                "interpretation": f"ALBI Grade 3 (score >-1.39). Median survival: {self.GRADE_THRESHOLDS[3]['survival_range']}. Poorest liver function and prognosis in HCC patients. This grade indicates severely impaired liver function with the shortest expected survival and may require more aggressive supportive care."
            }


def calculate_albi_hcc(albumin: float, bilirubin: float) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = AlbiHccCalculator()
    return calculator.calculate(albumin, bilirubin)