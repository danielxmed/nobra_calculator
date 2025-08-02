"""
Prognostic Index for Cancer Outcomes Calculator

Predicts cancer mortality from serum biomarkers using C-reactive protein (CRP) 
and white blood cell (WBC) count. This simple scoring system helps stratify 
cancer patients based on inflammatory markers.

References:
1. Proctor MJ, McMillan DC, Morrison DS, Fletcher CD, Horgan PG, Clarke SJ. 
   A derived neutrophil to lymphocyte ratio predicts survival in patients with cancer. 
   Br J Cancer. 2012;107(4):695-9. doi: 10.1038/bjc.2012.292.
2. Proctor MJ, Morrison DS, Talwar D, Balmer SM, Fletcher CD, O'Reilly DS, et al. 
   A comparison of inflammation-based prognostic scores in patients with cancer. 
   A Glasgow Inflammation Outcome Study. Eur J Cancer. 2011;47(17):2633-41. 
   doi: 10.1016/j.ejca.2011.03.028.
"""

from typing import Dict, Any


class PrognosticIndexCancerOutcomesCalculator:
    """Calculator for Prognostic Index for Cancer Outcomes"""
    
    def __init__(self):
        # Scoring thresholds
        self.CRP_THRESHOLD = 10  # mg/L
        self.WBC_THRESHOLD = 11  # x10⁹/L
        
        # Valid options
        self.VALID_CRP_OPTIONS = ["≤10", ">10"]
        self.VALID_WBC_OPTIONS = ["≤11", ">11"]
    
    def calculate(self, crp: str, wbc_count: str) -> Dict[str, Any]:
        """
        Calculates the Prognostic Index for Cancer Outcomes
        
        Args:
            crp (str): C-reactive protein level category ("≤10" or ">10")
            wbc_count (str): White blood cell count category ("≤11" or ">11")
            
        Returns:
            Dict with the prognostic index score and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(crp, wbc_count)
        
        # Calculate score
        crp_points = self._get_crp_points(crp)
        wbc_points = self._get_wbc_points(wbc_count)
        
        total_score = crp_points + wbc_points
        
        # Get interpretation
        interpretation = self._get_interpretation(total_score)
        
        return {
            "result": total_score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, crp: str, wbc_count: str):
        """Validates input parameters"""
        
        if not isinstance(crp, str):
            raise ValueError("CRP must be a string")
        
        if not isinstance(wbc_count, str):
            raise ValueError("WBC count must be a string")
        
        if crp not in self.VALID_CRP_OPTIONS:
            raise ValueError(f"CRP must be one of: {', '.join(self.VALID_CRP_OPTIONS)}")
        
        if wbc_count not in self.VALID_WBC_OPTIONS:
            raise ValueError(f"WBC count must be one of: {', '.join(self.VALID_WBC_OPTIONS)}")
    
    def _get_crp_points(self, crp: str) -> int:
        """
        Calculates points for CRP level
        
        Args:
            crp (str): CRP category
            
        Returns:
            int: Points for CRP (0 or 1)
        """
        if crp == "≤10":
            return 0
        else:  # ">10"
            return 1
    
    def _get_wbc_points(self, wbc_count: str) -> int:
        """
        Calculates points for WBC count
        
        Args:
            wbc_count (str): WBC count category
            
        Returns:
            int: Points for WBC count (0 or 1)
        """
        if wbc_count == "≤11":
            return 0
        else:  # ">11"
            return 1
    
    def _get_interpretation(self, score: int) -> Dict[str, str]:
        """
        Determines the interpretation based on the total score
        
        Args:
            score (int): Total prognostic index score
            
        Returns:
            Dict with interpretation details
        """
        
        if score == 0:
            return {
                "stage": "Low Risk",
                "description": "Minimal inflammatory response",
                "interpretation": "GOOD PROGNOSIS (Score: 0): Minimal systemic inflammatory response with both "
                                "CRP ≤10 mg/L and WBC ≤11 × 10⁹/L. This suggests less aggressive disease and "
                                "better potential outcomes. CLINICAL SIGNIFICANCE: Lower inflammatory burden "
                                "is associated with improved survival across multiple cancer types. "
                                "MANAGEMENT: Continue standard oncologic care with regular monitoring. "
                                "FOLLOW-UP: Monitor inflammatory markers during treatment to track response."
            }
        elif score == 1:
            return {
                "stage": "Intermediate Risk",
                "description": "Moderate inflammatory response",
                "interpretation": "INTERMEDIATE PROGNOSIS (Score: 1): Moderate systemic inflammatory response "
                                "with either elevated CRP (>10 mg/L) OR elevated WBC (>11 × 10⁹/L). "
                                "This indicates some degree of inflammation associated with cancer progression. "
                                "CLINICAL SIGNIFICANCE: Intermediate inflammatory burden suggests moderate "
                                "disease activity and prognosis between low and high-risk groups. "
                                "MANAGEMENT: Optimize supportive care and consider anti-inflammatory strategies "
                                "if appropriate. MONITORING: Track inflammatory markers regularly."
            }
        else:  # score == 2
            return {
                "stage": "High Risk",
                "description": "Significant inflammatory response",
                "interpretation": "POOR PROGNOSIS (Score: 2): Significant systemic inflammatory response "
                                "with both elevated CRP (>10 mg/L) AND elevated WBC (>11 × 10⁹/L). "
                                "This indicates substantial inflammation and potentially more aggressive "
                                "disease with worse outcomes. CLINICAL SIGNIFICANCE: High inflammatory "
                                "burden is associated with reduced survival and treatment resistance. "
                                "MANAGEMENT: Consider aggressive supportive care, nutritional support, "
                                "and evaluation for infection. MONITORING: Close surveillance and "
                                "frequent reassessment of treatment response."
            }


def calculate_prognostic_index_cancer_outcomes(crp: str, wbc_count: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = PrognosticIndexCancerOutcomesCalculator()
    return calculator.calculate(crp, wbc_count)