"""
DIPSS/DIPSS Plus (Dynamic International Prognostic Scoring System) for Myelofibrosis Calculator

Estimates survival in patients with primary myelofibrosis.

References:
1. Passamonti F, Cervantes F, Vannucchi AM, et al. A dynamic prognostic model to predict 
   survival in primary myelofibrosis: a study by the IWG-MRT (International Working Group 
   for Myeloproliferative Neoplasms Research and Treatment). Blood. 2010;115(9):1703-8.
2. Gangat N, Caramazza D, Vaidya R, et al. DIPSS plus: a refined Dynamic International 
   Prognostic Scoring System for primary myelofibrosis that incorporates prognostic 
   information from karyotype, platelet count, and transfusion status. J Clin Oncol. 
   2011;29(4):392-7.
"""

from typing import Dict, Any


class DipssCalculator:
    """Calculator for DIPSS/DIPSS Plus scoring in myelofibrosis"""
    
    def __init__(self):
        # Define point values for each parameter
        self.POINTS = {
            "age_over_65": 1,
            "wbc_over_25": 1,
            "hemoglobin_under_10": 2,  # Note: This is 2 points
            "peripheral_blast_1_or_more": 1,
            "constitutional_symptoms": 1,
            "unfavorable_karyotype": 1,  # DIPSS Plus only
            "platelets_under_100": 1,     # DIPSS Plus only
            "transfusion_dependent": 1    # DIPSS Plus only
        }
    
    def calculate(self, scoring_system: str, age_over_65: str, wbc_over_25: str,
                  hemoglobin_under_10: str, peripheral_blast_1_or_more: str,
                  constitutional_symptoms: str, unfavorable_karyotype: str = None,
                  platelets_under_100: str = None, transfusion_dependent: str = None) -> Dict[str, Any]:
        """
        Calculates DIPSS or DIPSS Plus score
        
        Args:
            scoring_system (str): "DIPSS" or "DIPSS_Plus"
            age_over_65 (str): "yes" or "no"
            wbc_over_25 (str): "yes" or "no"
            hemoglobin_under_10 (str): "yes" or "no"
            peripheral_blast_1_or_more (str): "yes" or "no"
            constitutional_symptoms (str): "yes" or "no"
            unfavorable_karyotype (str, optional): "yes" or "no" - required for DIPSS Plus
            platelets_under_100 (str, optional): "yes" or "no" - required for DIPSS Plus
            transfusion_dependent (str, optional): "yes" or "no" - required for DIPSS Plus
            
        Returns:
            Dict with the result and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(scoring_system, age_over_65, wbc_over_25, hemoglobin_under_10,
                             peripheral_blast_1_or_more, constitutional_symptoms,
                             unfavorable_karyotype, platelets_under_100, transfusion_dependent)
        
        # Calculate base DIPSS score
        score = 0
        
        if age_over_65 == "yes":
            score += self.POINTS["age_over_65"]
        
        if wbc_over_25 == "yes":
            score += self.POINTS["wbc_over_25"]
        
        if hemoglobin_under_10 == "yes":
            score += self.POINTS["hemoglobin_under_10"]
        
        if peripheral_blast_1_or_more == "yes":
            score += self.POINTS["peripheral_blast_1_or_more"]
        
        if constitutional_symptoms == "yes":
            score += self.POINTS["constitutional_symptoms"]
        
        # Add DIPSS Plus parameters if applicable
        if scoring_system == "DIPSS_Plus":
            if unfavorable_karyotype == "yes":
                score += self.POINTS["unfavorable_karyotype"]
            
            if platelets_under_100 == "yes":
                score += self.POINTS["platelets_under_100"]
            
            if transfusion_dependent == "yes":
                score += self.POINTS["transfusion_dependent"]
        
        # Get interpretation based on score and scoring system
        interpretation = self._get_interpretation(score, scoring_system)
        
        return {
            "result": score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation.get("stage", ""),
            "stage_description": interpretation.get("description", "")
        }
    
    def _validate_inputs(self, scoring_system: str, age_over_65: str, wbc_over_25: str,
                        hemoglobin_under_10: str, peripheral_blast_1_or_more: str,
                        constitutional_symptoms: str, unfavorable_karyotype: str = None,
                        platelets_under_100: str = None, transfusion_dependent: str = None):
        """Validates input parameters"""
        
        # Validate scoring system
        if scoring_system not in ["DIPSS", "DIPSS_Plus"]:
            raise ValueError("Scoring system must be 'DIPSS' or 'DIPSS_Plus'")
        
        # Validate yes/no parameters
        yes_no_params = {
            "age_over_65": age_over_65,
            "wbc_over_25": wbc_over_25,
            "hemoglobin_under_10": hemoglobin_under_10,
            "peripheral_blast_1_or_more": peripheral_blast_1_or_more,
            "constitutional_symptoms": constitutional_symptoms
        }
        
        for param_name, param_value in yes_no_params.items():
            if param_value not in ["yes", "no"]:
                raise ValueError(f"{param_name} must be 'yes' or 'no'")
        
        # Validate DIPSS Plus specific parameters if applicable
        if scoring_system == "DIPSS_Plus":
            if unfavorable_karyotype is None:
                raise ValueError("Unfavorable karyotype is required for DIPSS Plus")
            if platelets_under_100 is None:
                raise ValueError("Platelets under 100 is required for DIPSS Plus")
            if transfusion_dependent is None:
                raise ValueError("Transfusion dependency status is required for DIPSS Plus")
            
            if unfavorable_karyotype not in ["yes", "no"]:
                raise ValueError("Unfavorable karyotype must be 'yes' or 'no'")
            if platelets_under_100 not in ["yes", "no"]:
                raise ValueError("Platelets under 100 must be 'yes' or 'no'")
            if transfusion_dependent not in ["yes", "no"]:
                raise ValueError("Transfusion dependent must be 'yes' or 'no'")
    
    def _get_interpretation(self, score: int, scoring_system: str) -> Dict[str, str]:
        """
        Determines the interpretation based on the score and scoring system
        
        Args:
            score (int): Calculated DIPSS or DIPSS Plus score
            scoring_system (str): "DIPSS" or "DIPSS_Plus"
            
        Returns:
            Dict with interpretation
        """
        
        if scoring_system == "DIPSS":
            if score == 0:
                return {
                    "stage": "Low risk",
                    "description": "Low risk category",
                    "interpretation": "DIPSS Low risk: Median survival not reached. Consider observation with regular monitoring."
                }
            elif score <= 2:
                return {
                    "stage": "Intermediate-1 risk",
                    "description": "Intermediate-1 risk category",
                    "interpretation": "DIPSS Intermediate-1 risk: Median survival 14.2 years. Consider risk-adapted therapy and clinical trial enrollment."
                }
            elif score <= 4:
                return {
                    "stage": "Intermediate-2 risk",
                    "description": "Intermediate-2 risk category",
                    "interpretation": "DIPSS Intermediate-2 risk: Median survival 4 years. Consider allogeneic stem cell transplantation evaluation in eligible patients."
                }
            else:  # score >= 5
                return {
                    "stage": "High risk",
                    "description": "High risk category",
                    "interpretation": "DIPSS High risk: Median survival 1.5 years. Strong consideration for allogeneic stem cell transplantation in eligible patients or clinical trials."
                }
        
        else:  # DIPSS_Plus
            if score == 0:
                return {
                    "stage": "Low risk",
                    "description": "Low risk category",
                    "interpretation": "DIPSS Plus Low risk: Median survival 185 months (15.4 years). Consider observation with regular monitoring."
                }
            elif score == 1:
                return {
                    "stage": "Intermediate-1 risk",
                    "description": "Intermediate-1 risk category",
                    "interpretation": "DIPSS Plus Intermediate-1 risk: Median survival 78 months (6.5 years). Consider risk-adapted therapy and clinical trial enrollment."
                }
            elif score <= 3:
                return {
                    "stage": "Intermediate-2 risk",
                    "description": "Intermediate-2 risk category",
                    "interpretation": "DIPSS Plus Intermediate-2 risk: Median survival 35 months (2.9 years). Consider allogeneic stem cell transplantation evaluation in eligible patients."
                }
            else:  # score >= 4
                return {
                    "stage": "High risk",
                    "description": "High risk category",
                    "interpretation": "DIPSS Plus High risk: Median survival 16 months (1.3 years). Strong consideration for allogeneic stem cell transplantation in eligible patients or clinical trials."
                }


def calculate_dipss_plus(scoring_system: str, age_over_65: str, wbc_over_25: str,
                        hemoglobin_under_10: str, peripheral_blast_1_or_more: str,
                        constitutional_symptoms: str, unfavorable_karyotype: str = None,
                        platelets_under_100: str = None, transfusion_dependent: str = None) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = DipssCalculator()
    return calculator.calculate(scoring_system, age_over_65, wbc_over_25,
                               hemoglobin_under_10, peripheral_blast_1_or_more,
                               constitutional_symptoms, unfavorable_karyotype,
                               platelets_under_100, transfusion_dependent)