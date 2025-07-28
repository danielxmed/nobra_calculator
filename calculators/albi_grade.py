"""
ALBI (Albumin-Bilirubin) Grade for Hepatocellular Carcinoma (HCC) Calculator

Predicts survival in hepatocellular carcinoma patients based on objective measures 
of liver function using serum albumin and bilirubin levels. The ALBI grade is an 
alternative to the Child-Pugh grade that relies solely on objective laboratory values.

The ALBI grade was developed to provide a more objective assessment of liver function 
in HCC patients, eliminating the subjective variables (ascites and encephalopathy) 
used in the Child-Pugh classification.

References:
- Johnson PJ, Berhane S, Kagebayashi C, et al. Assessment of liver function in 
  patients with hepatocellular carcinoma: a new evidence-based approach-the ALBI 
  grade. J Clin Oncol. 2015;33(6):550-8.
- Hiraoka A, Michitaka K, Kumada T, et al. Validation and Potential of Albumin-
  Bilirubin Grade and Prognostication in a Nationwide Survey of 46,681 Hepatocellular 
  Carcinoma Patients in Japan. Liver Cancer. 2017;6(4):325-336.
"""

import math
from typing import Dict, Any


class AlbiGradeCalculator:
    """Calculator for ALBI (Albumin-Bilirubin) Grade for Hepatocellular Carcinoma"""
    
    def __init__(self):
        # ALBI grade definitions with survival data
        self.GRADE_DEFINITIONS = {
            1: {
                "name": "Grade 1",
                "description": "Best liver function",
                "cutoff": "≤-2.60",
                "median_survival": "18.5-85.6 months",
                "prognosis": "Best",
                "treatment_options": "Surgery, transplantation, systemic therapy"
            },
            2: {
                "name": "Grade 2", 
                "description": "Intermediate liver function",
                "cutoff": ">-2.60 to ≤-1.39",
                "median_survival": "5.3-46.5 months",
                "prognosis": "Intermediate",
                "treatment_options": "Selected treatments based on condition"
            },
            3: {
                "name": "Grade 3",
                "description": "Poor liver function",
                "cutoff": ">-1.39",
                "median_survival": "2.3-15.5 months",
                "prognosis": "Poor",
                "treatment_options": "Supportive care, palliative measures"
            }
        }
    
    def calculate(self, albumin: float, bilirubin: float) -> Dict[str, Any]:
        """
        Calculates ALBI grade using the provided parameters
        
        Args:
            albumin (float): Serum albumin level in g/L
            bilirubin (float): Serum bilirubin level in μmol/L
            
        Returns:
            Dict with the result and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(albumin, bilirubin)
        
        # Calculate ALBI score
        # Formula: ALBI = (log10 bilirubin × 0.66) + (albumin × -0.085)
        albi_score = (math.log10(bilirubin) * 0.66) + (albumin * -0.085)
        
        # Determine grade
        grade = self._determine_grade(albi_score)
        
        # Get interpretation
        interpretation = self._get_interpretation(albi_score, grade, albumin, bilirubin)
        
        return {
            "result": round(albi_score, 3),
            "unit": "score",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"],
            "grade": grade,
            "median_survival": interpretation["median_survival"],
            "prognosis": interpretation["prognosis"],
            "treatment_options": interpretation["treatment_options"]
        }
    
    def _validate_inputs(self, albumin: float, bilirubin: float):
        """Validates input parameters"""
        
        # Validate albumin
        if not isinstance(albumin, (int, float)):
            raise ValueError("Albumin must be a number")
        
        if albumin < 10.0 or albumin > 60.0:
            raise ValueError("Albumin must be between 10.0 and 60.0 g/L")
        
        # Validate bilirubin
        if not isinstance(bilirubin, (int, float)):
            raise ValueError("Bilirubin must be a number")
        
        if bilirubin < 1.0 or bilirubin > 1000.0:
            raise ValueError("Bilirubin must be between 1.0 and 1000.0 μmol/L")
        
        if bilirubin <= 0:
            raise ValueError("Bilirubin must be positive for logarithm calculation")
    
    def _determine_grade(self, albi_score: float) -> int:
        """Determines ALBI grade based on score"""
        
        if albi_score <= -2.60:
            return 1
        elif albi_score <= -1.39:
            return 2
        else:
            return 3
    
    def _get_interpretation(self, albi_score: float, grade: int, albumin: float, 
                          bilirubin: float) -> Dict[str, str]:
        """
        Determines the interpretation based on the ALBI grade
        
        Args:
            albi_score (float): Calculated ALBI score
            grade (int): ALBI grade (1-3)
            albumin (float): Albumin level
            bilirubin (float): Bilirubin level
            
        Returns:
            Dict with interpretation details
        """
        
        grade_info = self.GRADE_DEFINITIONS[grade]
        
        interpretation_parts = []
        
        # Score and grade
        interpretation_parts.append(
            f"ALBI score: {albi_score:.3f} (Grade {grade}: {grade_info['description']})."
        )
        
        # Laboratory values
        interpretation_parts.append(f"Albumin: {albumin} g/L, Bilirubin: {bilirubin} μmol/L.")
        
        # Prognosis and survival
        interpretation_parts.append(
            f"Prognosis: {grade_info['prognosis']}. "
            f"Median survival: {grade_info['median_survival']}."
        )
        
        # Treatment recommendations based on grade
        if grade == 1:
            interpretation_parts.append(
                "TREATMENT: Best liver function. Good candidate for aggressive treatments "
                "including surgical resection, liver transplantation, and systemic therapy. "
                "Excellent treatment tolerance expected."
            )
        elif grade == 2:
            interpretation_parts.append(
                "TREATMENT: Intermediate liver function. Consider treatment options based "
                "on overall condition, tumor characteristics, and performance status. "
                "Moderate treatment tolerance expected."
            )
        else:  # grade == 3
            interpretation_parts.append(
                "TREATMENT: Poor liver function. Limited treatment options available. "
                "Focus on supportive care and palliative measures. Consider best supportive "
                "care and symptom management."
            )
        
        # Clinical context
        interpretation_parts.append(
            "CLINICAL CONTEXT: ALBI grade provides objective assessment of liver function "
            "using only laboratory values (albumin and bilirubin). More objective than "
            "Child-Pugh grade as it eliminates subjective variables like ascites and encephalopathy."
        )
        
        # Additional notes
        interpretation_parts.append(
            "IMPORTANT: ALBI grade is validated for HCC patients and correlates with "
            "treatment tolerance and response. Use with tumor staging, performance status, "
            "and overall clinical assessment for comprehensive treatment planning."
        )
        
        return {
            "stage": grade_info["name"],
            "description": grade_info["description"],
            "interpretation": " ".join(interpretation_parts),
            "median_survival": grade_info["median_survival"],
            "prognosis": grade_info["prognosis"],
            "treatment_options": grade_info["treatment_options"]
        }


def calculate_albi_grade(albumin: float, bilirubin: float) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_albi_grade pattern
    """
    calculator = AlbiGradeCalculator()
    return calculator.calculate(
        albumin=albumin,
        bilirubin=bilirubin
    )