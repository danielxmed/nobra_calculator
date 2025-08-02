"""
Modified Glasgow Prognostic Score (mGPS) for Cancer Outcomes Calculator

Provides improved cancer prognosis assessment based on serum biomarkers (CRP and albumin)
that reflect systemic inflammation and nutritional status. The modified version weighs 
the inflammatory component more heavily than the original Glasgow Prognostic Score.

References:
1. Proctor MJ, et al. Br J Cancer. 2011;105(5):726-34.
2. McMillan DC. Cancer Treat Rev. 2013;39(5):534-40.
3. Forrest LM, et al. Br J Cancer. 2003;89(3):477-81.
"""

from typing import Dict, Any


class ModifiedGlasgowPrognosticScoreCalculator:
    """Calculator for Modified Glasgow Prognostic Score (mGPS)"""
    
    def __init__(self):
        # CRP and albumin thresholds
        self.CRP_THRESHOLD = 10.0  # mg/L
        self.ALBUMIN_THRESHOLD = 35.0  # g/L
    
    def calculate(self, crp_level: float, albumin_level: float) -> Dict[str, Any]:
        """
        Calculates the Modified Glasgow Prognostic Score (mGPS)
        
        Args:
            crp_level (float): C-Reactive Protein level in mg/L
            albumin_level (float): Serum albumin level in g/L
            
        Returns:
            Dict with mGPS score and prognostic interpretation
        """
        
        # Validate inputs
        self._validate_inputs(crp_level, albumin_level)
        
        # Calculate mGPS score
        score = self._calculate_mgps(crp_level, albumin_level)
        
        # Get interpretation
        interpretation = self._get_interpretation(score, crp_level, albumin_level)
        
        return {
            "result": score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, crp_level: float, albumin_level: float):
        """Validates input parameters"""
        
        if not isinstance(crp_level, (int, float)):
            raise ValueError("CRP level must be a number")
        
        if not isinstance(albumin_level, (int, float)):
            raise ValueError("Albumin level must be a number")
        
        if crp_level < 0:
            raise ValueError("CRP level cannot be negative")
        
        if crp_level > 500:
            raise ValueError("CRP level seems unreasonably high (>500 mg/L)")
        
        if albumin_level < 10:
            raise ValueError("Albumin level seems unreasonably low (<10 g/L)")
        
        if albumin_level > 60:
            raise ValueError("Albumin level seems unreasonably high (>60 g/L)")
    
    def _calculate_mgps(self, crp_level: float, albumin_level: float) -> int:
        """
        Calculates Modified Glasgow Prognostic Score based on CRP and albumin levels
        
        mGPS Scoring Logic (modified from original GPS):
        - Score 0: CRP ≤10 mg/L (regardless of albumin level)
        - Score 1: CRP >10 mg/L and albumin ≥35 g/L
        - Score 2: CRP >10 mg/L and albumin <35 g/L
        
        Key difference from original GPS: Low albumin alone (without elevated CRP) 
        scores 0 points in mGPS vs 1 point in original GPS
        """
        
        # Score 0: Normal CRP (regardless of albumin)
        if crp_level <= self.CRP_THRESHOLD:
            return 0
        
        # CRP is elevated (>10 mg/L)
        # Score 1: Elevated CRP with normal albumin
        if albumin_level >= self.ALBUMIN_THRESHOLD:
            return 1
        
        # Score 2: Elevated CRP with low albumin
        else:
            return 2
    
    def _get_interpretation(self, score: int, crp_level: float, albumin_level: float) -> Dict[str, str]:
        """
        Provides clinical interpretation based on mGPS score
        
        Args:
            score: mGPS score (0-2)
            crp_level: CRP level for detailed interpretation
            albumin_level: Albumin level for detailed interpretation
            
        Returns:
            Dict with interpretation details
        """
        
        interpretations = {
            0: {
                "stage": "Score 0",
                "description": "Good prognosis",
                "interpretation": (f"Modified Glasgow Prognostic Score 0: Good prognosis. "
                                f"CRP {crp_level:.1f} mg/L (≤10 mg/L, normal inflammatory markers). "
                                f"Albumin {albumin_level:.1f} g/L. This score is associated with better "
                                f"overall survival across multiple cancer types. The absence of systemic "
                                f"inflammation (normal CRP) indicates a more favorable prognosis regardless "
                                f"of albumin level.")
            },
            1: {
                "stage": "Score 1",
                "description": "Intermediate prognosis",
                "interpretation": (f"Modified Glasgow Prognostic Score 1: Intermediate prognosis. "
                                f"CRP {crp_level:.1f} mg/L (>10 mg/L, elevated) with albumin "
                                f"{albumin_level:.1f} g/L (≥35 g/L, adequate). This reflects systemic "
                                f"inflammation but preserved nutritional status. Associated with intermediate "
                                f"survival outcomes compared to score 0 and 2. Monitor for disease progression "
                                f"and consider anti-inflammatory supportive care measures.")
            },
            2: {
                "stage": "Score 2", 
                "description": "Poor prognosis",
                "interpretation": (f"Modified Glasgow Prognostic Score 2: Poor prognosis. "
                                f"CRP {crp_level:.1f} mg/L (>10 mg/L, elevated) with albumin "
                                f"{albumin_level:.1f} g/L (<35 g/L, low). This combination reflects both "
                                f"systemic inflammation and compromised nutritional status, associated with "
                                f"worse overall survival, disease-specific survival, and disease-free survival. "
                                f"Consider aggressive supportive care including nutritional support and "
                                f"anti-inflammatory measures where appropriate.")
            }
        }
        
        return interpretations.get(score, {
            "stage": f"Score {score}",
            "description": "Unknown score",
            "interpretation": f"Unknown mGPS score: {score}"
        })


def calculate_modified_glasgow_prognostic_score(crp_level: float, albumin_level: float) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = ModifiedGlasgowPrognosticScoreCalculator()
    return calculator.calculate(crp_level, albumin_level)