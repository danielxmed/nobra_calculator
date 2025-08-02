"""
International Prognostic Index for Chronic Lymphocytic Leukemia (CLL-IPI) Calculator

Stratifies chronic lymphocytic leukemia patients into four risk categories based on 
five independent prognostic factors. Predicts overall survival and guides treatment 
decisions in CLL patients.

References (Vancouver style):
1. An international prognostic index for patients with chronic lymphocytic leukaemia 
   (CLL-IPI): a meta-analysis of individual patient data. Lancet Oncol. 2016 Jul;17(7):779-90. 
   doi: 10.1016/S1470-2045(16)30029-8.
2. Condoluci A, Terzi di Bergamo L, Langerbeins P, et al. International prognostic score 
   for asymptomatic early-stage chronic lymphocytic leukemia. Blood. 2020 May 28;135(22):1859-1869. 
   doi: 10.1182/blood.2019003453.
3. Gentile M, Shanafelt TD, Rossi D, et al. Validation of the CLL-IPI and comparison with 
   the MDACC prognostic index in newly diagnosed patients. Blood. 2016 Oct 13;128(15):2093-2095. 
   doi: 10.1182/blood-2016-07-728261.
"""

from typing import Dict, Any


class CllIpiCalculator:
    """Calculator for CLL-IPI (International Prognostic Index for Chronic Lymphocytic Leukemia)"""
    
    def __init__(self):
        # CLL-IPI scoring weights based on meta-analysis
        self.scoring_weights = {
            "tp53_status": {
                "normal": 0,
                "abnormal": 4  # del(17p) and/or TP53 mutation
            },
            "ighv_status": {
                "mutated": 0,      # <98% homology (favorable)
                "unmutated": 2     # ≥98% homology (unfavorable)
            },
            "beta2_microglobulin": {
                "normal": 0,      # ≤3.5 mg/L
                "elevated": 2     # >3.5 mg/L
            },
            "clinical_stage": {
                "early": 0,       # Binet A or Rai 0
                "advanced": 1     # Binet B-C or Rai I-IV
            },
            "age": {
                "65_or_younger": 0,  # ≤65 years
                "older_than_65": 1   # >65 years
            }
        }
    
    def calculate(self, tp53_status: str, ighv_status: str, beta2_microglobulin: str,
                 clinical_stage: str, age: str) -> Dict[str, Any]:
        """
        Calculates the CLL-IPI score and risk stratification
        
        Args:
            tp53_status (str): TP53 gene status (normal/abnormal)
            ighv_status (str): IGHV mutational status (mutated/unmutated)
            beta2_microglobulin (str): β2-microglobulin level (normal/elevated)
            clinical_stage (str): Clinical stage (early/advanced)
            age (str): Age category (65_or_younger/older_than_65)
            
        Returns:
            Dict with the CLL-IPI score and risk stratification
        """
        
        # Validate inputs
        self._validate_inputs(tp53_status, ighv_status, beta2_microglobulin, clinical_stage, age)
        
        # Calculate total score
        score = self._calculate_total_score(tp53_status, ighv_status, beta2_microglobulin, 
                                          clinical_stage, age)
        
        # Get risk stratification
        risk_stratification = self._get_risk_stratification(score)
        
        return {
            "result": score,
            "unit": "points",
            "interpretation": risk_stratification["interpretation"],
            "stage": risk_stratification["stage"],
            "stage_description": risk_stratification["description"]
        }
    
    def _validate_inputs(self, tp53_status: str, ighv_status: str, beta2_microglobulin: str,
                        clinical_stage: str, age: str):
        """Validates input parameters"""
        
        # Define valid options for each parameter
        valid_tp53 = ["normal", "abnormal"]
        valid_ighv = ["mutated", "unmutated"]
        valid_beta2 = ["normal", "elevated"]
        valid_stage = ["early", "advanced"]
        valid_age = ["65_or_younger", "older_than_65"]
        
        # Validate all parameters
        if tp53_status not in valid_tp53:
            raise ValueError("tp53_status must be 'normal' or 'abnormal'")
        if ighv_status not in valid_ighv:
            raise ValueError("ighv_status must be 'mutated' or 'unmutated'")
        if beta2_microglobulin not in valid_beta2:
            raise ValueError("beta2_microglobulin must be 'normal' or 'elevated'")
        if clinical_stage not in valid_stage:
            raise ValueError("clinical_stage must be 'early' or 'advanced'")
        if age not in valid_age:
            raise ValueError("age must be '65_or_younger' or 'older_than_65'")
    
    def _calculate_total_score(self, tp53_status: str, ighv_status: str, beta2_microglobulin: str,
                              clinical_stage: str, age: str) -> int:
        """
        Calculates the total CLL-IPI score
        
        CLL-IPI Scoring:
        - TP53 abnormal (del(17p) and/or TP53 mutation): 4 points
        - IGHV unmutated (≥98% homology): 2 points
        - β2-microglobulin >3.5 mg/L: 2 points
        - Advanced clinical stage (Binet B-C or Rai I-IV): 1 point
        - Age >65 years: 1 point
        
        Total score range: 0-10 points
        """
        
        total_score = 0
        
        # Add points for each risk factor
        total_score += self.scoring_weights["tp53_status"][tp53_status]
        total_score += self.scoring_weights["ighv_status"][ighv_status]
        total_score += self.scoring_weights["beta2_microglobulin"][beta2_microglobulin]
        total_score += self.scoring_weights["clinical_stage"][clinical_stage]
        total_score += self.scoring_weights["age"][age]
        
        return total_score
    
    def _get_risk_stratification(self, score: int) -> Dict[str, str]:
        """
        Provides risk stratification based on CLL-IPI score
        
        Args:
            score (int): CLL-IPI score (0-10)
            
        Returns:
            Dict with risk stratification details
        """
        
        if score <= 1:
            return {
                "stage": "Low Risk",
                "description": f"Score {score} points (0-1 points)",
                "interpretation": "Excellent prognosis with 5-year overall survival of 93.2% (95% CI 90.5-96.0%). These patients have favorable genetic and clinical characteristics with prolonged survival expected. Consider watchful waiting approach for asymptomatic patients. Lower intensity treatments may be appropriate when therapy is indicated."
            }
        elif score <= 3:
            return {
                "stage": "Intermediate Risk",
                "description": f"Score {score} points (2-3 points)",
                "interpretation": "Good prognosis with 5-year overall survival of 79.3% (95% CI 75.5-83.2%). These patients have mixed prognostic factors and moderate survival expectations. Standard treatment approaches are appropriate. Consider patient preferences and comorbidities when selecting therapy."
            }
        elif score <= 6:
            return {
                "stage": "High Risk",
                "description": f"Score {score} points (4-6 points)",
                "interpretation": "Unfavorable prognosis with 5-year overall survival of 63.3% (95% CI 57.9-68.8%). These patients have several adverse prognostic factors requiring closer monitoring. Consider more intensive treatment approaches and clinical trial enrollment. Earlier intervention may be beneficial."
            }
        else:  # score 7-10
            return {
                "stage": "Very High Risk",
                "description": f"Score {score} points (7-10 points)",
                "interpretation": "Poor prognosis with 5-year overall survival of 23.3% (95% CI 12.5-34.1%). These patients have multiple high-risk features requiring aggressive management. Strong consideration for clinical trials, novel targeted therapies, and intensive treatment regimens. Close monitoring and supportive care essential."
            }


def calculate_cll_ipi(tp53_status: str, ighv_status: str, beta2_microglobulin: str,
                     clinical_stage: str, age: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = CllIpiCalculator()
    return calculator.calculate(tp53_status, ighv_status, beta2_microglobulin, clinical_stage, age)