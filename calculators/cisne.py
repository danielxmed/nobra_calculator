"""
Clinical Index of Stable Febrile Neutropenia (CISNE) Calculator

Identifies febrile neutropenia patients at low risk for serious complications.

References:
1. Carmona-Bayonas A, et al. Br J Cancer. 2011;105(5):612-7.
2. Carmona-Bayonas A, et al. J Clin Oncol. 2015;33(5):465-71.
"""

from typing import Dict, Any


class CisneCalculator:
    """Calculator for Clinical Index of Stable Febrile Neutropenia (CISNE)"""
    
    def calculate(
        self,
        ecog_performance_status: str,
        stress_induced_hyperglycemia: str,
        copd: str,
        cardiovascular_disease: str,
        nci_mucositis_grade: str,
        monocytes: str
    ) -> Dict[str, Any]:
        """
        Calculates the CISNE score for febrile neutropenia risk assessment
        
        Args:
            ecog_performance_status: "<2" or "≥2"
            stress_induced_hyperglycemia: "yes" or "no"
            copd: "yes" or "no"
            cardiovascular_disease: "yes" or "no"
            nci_mucositis_grade: "yes" (≥2) or "no" (<2)
            monocytes: "≥200/µL" or "<200/µL"
            
        Returns:
            Dict with the CISNE score and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(
            ecog_performance_status, stress_induced_hyperglycemia,
            copd, cardiovascular_disease, nci_mucositis_grade, monocytes
        )
        
        # Calculate CISNE score
        score = 0
        
        # ECOG Performance Status (0 or 2 points)
        if ecog_performance_status == "≥2":
            score += 2
        
        # Stress-induced hyperglycemia (0 or 2 points)
        if stress_induced_hyperglycemia == "yes":
            score += 2
        
        # COPD (0 or 1 point)
        if copd == "yes":
            score += 1
        
        # Cardiovascular disease (0 or 1 point)
        if cardiovascular_disease == "yes":
            score += 1
        
        # NCI mucositis grade ≥2 (0 or 1 point)
        if nci_mucositis_grade == "yes":
            score += 1
        
        # Monocytes (0 or 1 point)
        if monocytes == "<200/µL":
            score += 1
        
        # Get interpretation
        interpretation = self._get_interpretation(score)
        
        return {
            "result": score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["risk_category"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(
        self, ecog_performance_status, stress_induced_hyperglycemia,
        copd, cardiovascular_disease, nci_mucositis_grade, monocytes
    ):
        """Validates input parameters"""
        
        # Validate ECOG Performance Status
        if ecog_performance_status not in ["<2", "≥2"]:
            raise ValueError("ECOG Performance Status must be '<2' or '≥2'")
        
        # Validate yes/no parameters
        yes_no_params = [
            ("Stress-induced hyperglycemia", stress_induced_hyperglycemia),
            ("COPD", copd),
            ("Cardiovascular disease", cardiovascular_disease),
            ("NCI mucositis grade", nci_mucositis_grade)
        ]
        
        for param_name, param_value in yes_no_params:
            if param_value not in ["yes", "no"]:
                raise ValueError(f"{param_name} must be 'yes' or 'no'")
        
        # Validate monocytes
        if monocytes not in ["≥200/µL", "<200/µL"]:
            raise ValueError("Monocytes must be '≥200/µL' or '<200/µL'")
    
    def _get_interpretation(self, score: int) -> Dict[str, str]:
        """
        Determines the interpretation based on the CISNE score
        
        Args:
            score: CISNE score (0-8)
            
        Returns:
            Dict with interpretation details
        """
        
        if score == 0:
            return {
                "risk_category": "Low",
                "description": "Low risk",
                "interpretation": "Low risk of complications (1.1%). May be appropriate for outpatient management with close monitoring."
            }
        elif score <= 2:
            return {
                "risk_category": "Intermediate", 
                "description": "Intermediate risk",
                "interpretation": "Intermediate risk of complications (6.2%). Consider admission or very close outpatient monitoring."
            }
        else:  # score >= 3
            return {
                "risk_category": "High",
                "description": "High risk",
                "interpretation": "High risk of complications (36%). Hospital admission strongly recommended."
            }


def calculate_cisne(
    ecog_performance_status, stress_induced_hyperglycemia,
    copd, cardiovascular_disease, nci_mucositis_grade, monocytes
) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = CisneCalculator()
    return calculator.calculate(
        ecog_performance_status, stress_induced_hyperglycemia,
        copd, cardiovascular_disease, nci_mucositis_grade, monocytes
    )