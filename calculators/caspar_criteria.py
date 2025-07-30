"""
CASPAR Criteria for Psoriatic Arthritis Calculator

Provides standardized classification criteria for identifying psoriatic arthritis (PsA) 
in patients with inflammatory arthritis.

References:
1. Taylor W, Gladman D, Helliwell P, Marchesoni A, Mease P, Mielants H; CASPAR Study Group. 
   Classification criteria for psoriatic arthritis: development of new criteria from a large 
   international study. Arthritis Rheum. 2006 Aug;54(8):2665-73. doi: 10.1002/art.21972.
2. Chandran V, Schentag CT, Gladman DD. Sensitivity and specificity of the CASPAR criteria 
   for psoriatic arthritis in a family medicine clinic setting. J Rheumatol. 2008 
   Oct;35(10):2069-70.
3. Helliwell PS, Taylor WJ. Classification and diagnostic criteria for psoriatic arthritis. 
   Ann Rheum Dis. 2005 Mar;64 Suppl 2(Suppl 2):ii3-8. doi: 10.1136/ard.2004.032318.
"""

from typing import Dict, Any


class CasparCriteriaCalculator:
    """Calculator for CASPAR Criteria for Psoriatic Arthritis"""
    
    def __init__(self):
        # Classification threshold
        self.CLASSIFICATION_THRESHOLD = 3
        
        # Scoring weights
        self.CURRENT_PSORIASIS_POINTS = 2
        self.HISTORY_PSORIASIS_POINTS = 1
        self.OTHER_CRITERIA_POINTS = 1
    
    def calculate(
        self,
        inflammatory_articular_disease: str,
        psoriasis_status: str,
        nail_dystrophy: str,
        rheumatoid_factor: str,
        dactylitis: str,
        juxta_articular_new_bone: str
    ) -> Dict[str, Any]:
        """
        Calculates CASPAR classification for psoriatic arthritis
        
        Args:
            inflammatory_articular_disease: Presence of inflammatory articular disease
            psoriasis_status: Current psoriasis status or history
            nail_dystrophy: Presence of nail dystrophy
            rheumatoid_factor: Rheumatoid factor status
            dactylitis: Presence of dactylitis
            juxta_articular_new_bone: Presence of juxtaarticular new bone formation
            
        Returns:
            Dict with CASPAR classification result and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(
            inflammatory_articular_disease, psoriasis_status, nail_dystrophy,
            rheumatoid_factor, dactylitis, juxta_articular_new_bone
        )
        
        # Check mandatory criterion
        if inflammatory_articular_disease == "no":
            return self._create_negative_result("Missing mandatory criterion: inflammatory articular disease")
        
        # Calculate points from additional criteria
        points = self._calculate_points(
            psoriasis_status, nail_dystrophy, rheumatoid_factor,
            dactylitis, juxta_articular_new_bone
        )
        
        # Get detailed scoring breakdown
        scoring_breakdown = self._get_scoring_breakdown(
            psoriasis_status, nail_dystrophy, rheumatoid_factor,
            dactylitis, juxta_articular_new_bone
        )
        
        # Determine classification
        meets_criteria = points >= self.CLASSIFICATION_THRESHOLD
        interpretation = self._get_interpretation(points, meets_criteria)
        
        return {
            "result": {
                "total_points": points,
                "meets_criteria": meets_criteria,
                "mandatory_criterion_met": True,
                "scoring_breakdown": scoring_breakdown
            },
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, inflammatory_articular, psoriasis, nail, rf, dactylitis, bone):
        """Validates input parameters"""
        
        valid_yes_no = ["yes", "no"]
        valid_psoriasis = ["current", "history", "none"]
        valid_rf = ["negative", "positive"]
        
        if inflammatory_articular not in valid_yes_no:
            raise ValueError("Inflammatory articular disease must be 'yes' or 'no'")
        
        if psoriasis not in valid_psoriasis:
            raise ValueError("Psoriasis status must be 'current', 'history', or 'none'")
        
        if nail not in valid_yes_no:
            raise ValueError("Nail dystrophy must be 'yes' or 'no'")
        
        if rf not in valid_rf:
            raise ValueError("Rheumatoid factor must be 'negative' or 'positive'")
        
        if dactylitis not in valid_yes_no:
            raise ValueError("Dactylitis must be 'yes' or 'no'")
        
        if bone not in valid_yes_no:
            raise ValueError("Juxtaarticular new bone formation must be 'yes' or 'no'")
    
    def _calculate_points(self, psoriasis, nail, rf, dactylitis, bone):
        """Calculates total points from additional criteria"""
        
        points = 0
        
        # Psoriasis scoring
        if psoriasis == "current":
            points += self.CURRENT_PSORIASIS_POINTS
        elif psoriasis == "history":
            points += self.HISTORY_PSORIASIS_POINTS
        
        # Other criteria (1 point each)
        if nail == "yes":
            points += self.OTHER_CRITERIA_POINTS
        
        if rf == "negative":
            points += self.OTHER_CRITERIA_POINTS
        
        if dactylitis == "yes":
            points += self.OTHER_CRITERIA_POINTS
        
        if bone == "yes":
            points += self.OTHER_CRITERIA_POINTS
        
        return points
    
    def _get_scoring_breakdown(self, psoriasis, nail, rf, dactylitis, bone):
        """Provides detailed scoring breakdown"""
        
        breakdown = {}
        
        # Psoriasis
        if psoriasis == "current":
            breakdown["psoriasis"] = {"status": "Current psoriasis", "points": 2}
        elif psoriasis == "history":
            breakdown["psoriasis"] = {"status": "History of psoriasis", "points": 1}
        else:
            breakdown["psoriasis"] = {"status": "No psoriasis", "points": 0}
        
        # Nail dystrophy
        breakdown["nail_dystrophy"] = {
            "status": "Present" if nail == "yes" else "Absent",
            "points": 1 if nail == "yes" else 0
        }
        
        # Rheumatoid factor
        breakdown["rheumatoid_factor"] = {
            "status": "Negative" if rf == "negative" else "Positive",
            "points": 1 if rf == "negative" else 0
        }
        
        # Dactylitis
        breakdown["dactylitis"] = {
            "status": "Present" if dactylitis == "yes" else "Absent",
            "points": 1 if dactylitis == "yes" else 0
        }
        
        # Juxtaarticular new bone formation
        breakdown["juxta_articular_new_bone"] = {
            "status": "Present" if bone == "yes" else "Absent",
            "points": 1 if bone == "yes" else 0
        }
        
        return breakdown
    
    def _create_negative_result(self, reason):
        """Creates result for cases that don't meet mandatory criterion"""
        
        return {
            "result": {
                "total_points": 0,
                "meets_criteria": False,
                "mandatory_criterion_met": False,
                "scoring_breakdown": {}
            },
            "unit": "points",
            "interpretation": f"Patient does not meet CASPAR criteria for psoriatic arthritis classification. {reason}. The mandatory criterion of inflammatory articular disease must be present to proceed with classification.",
            "stage": "Does Not Meet CASPAR Criteria",
            "stage_description": "Insufficient criteria for psoriatic arthritis classification"
        }
    
    def _get_interpretation(self, points: int, meets_criteria: bool) -> Dict[str, str]:
        """
        Determines clinical interpretation based on CASPAR criteria
        
        Args:
            points: Total points from additional criteria
            meets_criteria: Whether patient meets classification criteria
            
        Returns:
            Dict with clinical interpretation
        """
        
        if meets_criteria:
            return {
                "stage": "Meets CASPAR Criteria",
                "description": "Meets criteria for psoriatic arthritis classification",
                "interpretation": f"Patient meets CASPAR criteria for psoriatic arthritis classification with {points}/6 possible points. The presence of inflammatory articular disease plus ≥3 points from additional criteria supports PsA classification for research purposes. Note: CASPAR criteria are classification criteria designed for research, not diagnostic criteria for clinical practice."
            }
        else:
            return {
                "stage": "Does Not Meet CASPAR Criteria",
                "description": "Insufficient criteria for psoriatic arthritis classification",
                "interpretation": f"Patient does not meet CASPAR criteria for psoriatic arthritis classification with {points}/6 possible points. Requires ≥3 points from additional criteria. Consider alternative diagnoses, further evaluation, or clinical judgment may still support PsA diagnosis outside of formal classification criteria."
            }


def calculate_caspar_criteria(
    inflammatory_articular_disease: str,
    psoriasis_status: str,
    nail_dystrophy: str,
    rheumatoid_factor: str,
    dactylitis: str,
    juxta_articular_new_bone: str
) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = CasparCriteriaCalculator()
    return calculator.calculate(
        inflammatory_articular_disease=inflammatory_articular_disease,
        psoriasis_status=psoriasis_status,
        nail_dystrophy=nail_dystrophy,
        rheumatoid_factor=rheumatoid_factor,
        dactylitis=dactylitis,
        juxta_articular_new_bone=juxta_articular_new_bone
    )