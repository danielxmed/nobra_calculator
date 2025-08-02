"""
International Prognostic Score for Asymptomatic Early-stage CLL (IPS-E) Calculator

Assesses prognosis of asymptomatic early-stage chronic lymphocytic leukemia (CLL) 
to predict time to first treatment (TTFT) using three independent prognostic factors.

References (Vancouver style):
1. Condoluci A, Terzi di Bergamo L, Langerbeins P, Hoechstetter MA, Herling CD, De Paoli L, 
   et al. International prognostic score for asymptomatic early-stage chronic lymphocytic 
   leukemia. Blood. 2020 May 21;135(21):1859-1869. doi: 10.1182/blood.2019003453.
2. Hallek M, Cheson BD, Catovsky D, Caligaris-Cappio F, Dighiero G, Döhner H, et al. 
   iwCLL guidelines for diagnosis, indications for treatment, response assessment, and 
   supportive management of CLL. Blood. 2018 Jun 21;131(25):2745-2760. 
   doi: 10.1182/blood-2017-09-806398.
3. Rai KR, Sawitsky A, Cronkite EP, Chanana AD, Levy RN, Pasternack BS. Clinical staging 
   of chronic lymphocytic leukemia. Blood. 1975 Aug;46(2):219-34. 
   doi: 10.1182/blood.V46.2.219.219.
"""

from typing import Dict, Any


class IpsECllCalculator:
    """Calculator for International Prognostic Score for Asymptomatic Early-stage CLL (IPS-E)"""
    
    def __init__(self):
        # Risk factor scoring weights - each factor contributes 1 point
        self.scoring_weights = {
            "ighv_status": {
                "mutated": 0,
                "unmutated": 1
            },
            "lymphocyte_count": {
                "15_or_less": 0,
                "greater_than_15": 1
            },
            "palpable_lymph_nodes": {
                "absent": 0,
                "present": 1
            }
        }
    
    def calculate(self, ighv_status: str, lymphocyte_count: str, palpable_lymph_nodes: str) -> Dict[str, Any]:
        """
        Calculates the IPS-E score using the provided parameters
        
        Args:
            ighv_status (str): IGHV mutational status ("mutated", "unmutated")
            lymphocyte_count (str): Absolute lymphocyte count ("15_or_less", "greater_than_15")
            palpable_lymph_nodes (str): Presence of palpable lymph nodes ("absent", "present")
            
        Returns:
            Dict with the IPS-E score and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(ighv_status, lymphocyte_count, palpable_lymph_nodes)
        
        # Calculate total score
        total_score = self._calculate_total_score(ighv_status, lymphocyte_count, palpable_lymph_nodes)
        
        # Get interpretation based on score
        interpretation = self._get_interpretation(total_score)
        
        return {
            "result": total_score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, ighv_status: str, lymphocyte_count: str, palpable_lymph_nodes: str):
        """Validates input parameters"""
        
        # Validate IGHV status
        if ighv_status not in self.scoring_weights["ighv_status"]:
            raise ValueError(f"IGHV status must be one of: {list(self.scoring_weights['ighv_status'].keys())}")
        
        # Validate lymphocyte count
        if lymphocyte_count not in self.scoring_weights["lymphocyte_count"]:
            raise ValueError(f"Lymphocyte count must be one of: {list(self.scoring_weights['lymphocyte_count'].keys())}")
        
        # Validate palpable lymph nodes
        if palpable_lymph_nodes not in self.scoring_weights["palpable_lymph_nodes"]:
            raise ValueError(f"Palpable lymph nodes must be one of: {list(self.scoring_weights['palpable_lymph_nodes'].keys())}")
    
    def _calculate_total_score(self, ighv_status: str, lymphocyte_count: str, palpable_lymph_nodes: str) -> int:
        """Calculates the total IPS-E score"""
        
        total_score = 0
        total_score += self.scoring_weights["ighv_status"][ighv_status]
        total_score += self.scoring_weights["lymphocyte_count"][lymphocyte_count]
        total_score += self.scoring_weights["palpable_lymph_nodes"][palpable_lymph_nodes]
        
        return total_score
    
    def _get_interpretation(self, score: int) -> Dict[str, str]:
        """
        Determines the interpretation based on the IPS-E score
        
        Args:
            score (int): Calculated IPS-E score (0-3 points)
            
        Returns:
            Dict with risk stratification and clinical interpretation
        """
        
        if score == 0:
            return {
                "stage": "Low Risk",
                "description": "Score 0 points",
                "interpretation": "Excellent prognosis. 5-year cumulative risk for treatment need: 8.4%. 1-year risk <0.1%. These patients have very low likelihood of requiring treatment in the near future. Standard surveillance every 3-6 months is appropriate. Ideal candidates for observation without intervention. Clinical trials for early intervention are generally not indicated."
            }
        elif score == 1:
            return {
                "stage": "Intermediate Risk",
                "description": "Score 1 point",
                "interpretation": "Intermediate prognosis. 5-year cumulative risk for treatment need: 28.4%. 1-year risk: 3.1%. Closer monitoring recommended every 3 months. Consider for early intervention clinical trials. Patients may benefit from more frequent assessment of disease progression markers."
            }
        else:  # score >= 2
            return {
                "stage": "High Risk",
                "description": "Score 2-3 points",
                "interpretation": "Higher risk of disease progression. 5-year cumulative risk for treatment need: 61.2%. Close monitoring every 2-3 months recommended. Strong candidates for early intervention clinical trials. Consider evaluation for novel therapeutic approaches or investigational agents. Regular assessment for iwCLL treatment criteria development."
            }


def calculate_ips_e_cll(ighv_status: str, lymphocyte_count: str, palpable_lymph_nodes: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    Calculates the International Prognostic Score for Asymptomatic Early-stage CLL (IPS-E)
    using three independent prognostic factors to predict time to first treatment.
    
    Args:
        ighv_status (str): IGHV mutational status
        lymphocyte_count (str): Absolute lymphocyte count category
        palpable_lymph_nodes (str): Presence of palpable lymph nodes
        
    Returns:
        Dict with IPS-E score and risk stratification
    """
    calculator = IpsECllCalculator()
    return calculator.calculate(ighv_status, lymphocyte_count, palpable_lymph_nodes)