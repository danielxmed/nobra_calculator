"""
Follicular Lymphoma International Prognostic Index (FLIPI) Calculator

Estimates overall survival in patients with follicular lymphoma based on 
5 adverse prognostic factors.

References:
1. Solal-Céligny P, Roy P, Colombat P, White J, Armitage JO, Arranz-Saez R, 
   et al. Follicular lymphoma international prognostic index. Blood. 
   2004 Sep 1;104(5):1258-65.
2. van de Schans SA, Steyerberg EW, Nijziel MR, Creemers GJ, Janssen-Heijnen ML, 
   van Spronsen DJ. Validation, revision and extension of the Follicular 
   Lymphoma International Prognostic Index (FLIPI) in a population-based 
   setting. Ann Oncol. 2009 Oct;20(10):1697-702.
"""

from typing import Dict, Any


class FlipiCalculator:
    """Calculator for Follicular Lymphoma International Prognostic Index (FLIPI)"""
    
    def __init__(self):
        # No specific constants needed for FLIPI
        pass
    
    def calculate(self, age_over_60: str, nodal_sites_over_4: str,
                  ldh_elevated: str, hemoglobin_below_120: str,
                  stage_3_or_4: str) -> Dict[str, Any]:
        """
        Calculates the FLIPI score using 5 adverse prognostic factors
        
        Args:
            age_over_60 (str): Age >60 years (yes/no)
            nodal_sites_over_4 (str): >4 nodal sites involved (yes/no)
            ldh_elevated (str): LDH above normal (yes/no)
            hemoglobin_below_120 (str): Hemoglobin <120 g/L (yes/no)
            stage_3_or_4 (str): Ann Arbor stage III or IV (yes/no)
            
        Returns:
            Dict with FLIPI score and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(age_over_60, nodal_sites_over_4,
                            ldh_elevated, hemoglobin_below_120,
                            stage_3_or_4)
        
        # Calculate FLIPI score
        score = self._calculate_score(age_over_60, nodal_sites_over_4,
                                    ldh_elevated, hemoglobin_below_120,
                                    stage_3_or_4)
        
        # Get interpretation
        interpretation = self._get_interpretation(score)
        
        return {
            "result": score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, age_over_60: str, nodal_sites_over_4: str,
                        ldh_elevated: str, hemoglobin_below_120: str,
                        stage_3_or_4: str):
        """Validates input parameters"""
        
        valid_options = ["yes", "no"]
        
        # Validate each parameter
        for param, name in [
            (age_over_60, "Age >60"),
            (nodal_sites_over_4, ">4 nodal sites"),
            (ldh_elevated, "LDH elevated"),
            (hemoglobin_below_120, "Hemoglobin <120 g/L"),
            (stage_3_or_4, "Stage III-IV")
        ]:
            if param not in valid_options:
                raise ValueError(f"{name} must be 'yes' or 'no'")
    
    def _calculate_score(self, age_over_60: str, nodal_sites_over_4: str,
                        ldh_elevated: str, hemoglobin_below_120: str,
                        stage_3_or_4: str) -> int:
        """
        Calculates FLIPI score (sum of adverse factors)
        
        Returns:
            int: FLIPI score (0-5)
        """
        
        score = 0
        
        # Each adverse factor adds 1 point
        if age_over_60 == "yes":
            score += 1
        
        if nodal_sites_over_4 == "yes":
            score += 1
        
        if ldh_elevated == "yes":
            score += 1
        
        if hemoglobin_below_120 == "yes":
            score += 1
        
        if stage_3_or_4 == "yes":
            score += 1
        
        return score
    
    def _get_interpretation(self, score: int) -> Dict[str, str]:
        """
        Determines risk group and prognosis based on FLIPI score
        
        Args:
            score (int): FLIPI score (0-5)
            
        Returns:
            Dict with interpretation details
        """
        
        if score <= 1:
            return {
                "stage": "Low Risk",
                "description": f"{score} adverse {'factor' if score == 1 else 'factors'}",
                "interpretation": ("Low risk group with favorable prognosis. 10-year overall "
                                 "survival approximately 70%. 5-year overall survival approximately "
                                 "85%. These patients may be candidates for watchful waiting or less "
                                 "intensive therapy depending on symptoms, tumor burden, and patient "
                                 "preferences. Regular monitoring is essential.")
            }
        elif score == 2:
            return {
                "stage": "Intermediate Risk",
                "description": "2 adverse factors",
                "interpretation": ("Intermediate risk group with moderate prognosis. 10-year overall "
                                 "survival approximately 50%. 5-year overall survival approximately "
                                 "70%. These patients often benefit from systemic therapy, particularly "
                                 "when symptomatic or with high tumor burden. Treatment options include "
                                 "rituximab monotherapy or chemoimmunotherapy depending on clinical context.")
            }
        else:  # score >= 3
            return {
                "stage": "High Risk",
                "description": f"{score} adverse factors",
                "interpretation": ("High risk group with less favorable prognosis. 10-year overall "
                                 "survival approximately 35%. 5-year overall survival approximately "
                                 "50%. These patients typically require prompt treatment with combination "
                                 "chemotherapy or immunotherapy (e.g., R-CHOP, R-bendamustine). Consider "
                                 "clinical trial enrollment, maintenance therapy, and more intensive "
                                 "monitoring. Transformation risk may be higher in this group.")
            }


def calculate_flipi(age_over_60: str, nodal_sites_over_4: str,
                   ldh_elevated: str, hemoglobin_below_120: str,
                   stage_3_or_4: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = FlipiCalculator()
    return calculator.calculate(age_over_60, nodal_sites_over_4,
                              ldh_elevated, hemoglobin_below_120,
                              stage_3_or_4)