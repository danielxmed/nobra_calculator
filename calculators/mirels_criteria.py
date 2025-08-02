"""
Mirels' Criteria for Prophylactic Fixation Calculator

Predicts risk of pathologic fracture in patients with long bone metastasis
to guide prophylactic fixation decisions.

References:
1. Mirels H. Clin Orthop Relat Res. 1989;(249):256-64.
2. Van der Linden YM, et al. J Bone Joint Surg Br. 2004;86(4):566-73.
3. Nazarian A, et al. Clin Cancer Res. 2014;20(9):2465-73.
4. Evans AR, et al. Clin Orthop Relat Res. 2008;466(6):1279-84.
"""

from typing import Dict, Any


class MirelsCriteriaCalculator:
    """Calculator for Mirels' Criteria for Prophylactic Fixation"""
    
    def __init__(self):
        # Scoring system points
        self.SITE_POINTS = {
            "upper_limb": 1,
            "lower_limb": 2,
            "trochanteric_region": 3
        }
        
        self.SIZE_POINTS = {
            "less_than_one_third": 1,
            "one_third_to_two_thirds": 2,
            "more_than_two_thirds": 3
        }
        
        self.NATURE_POINTS = {
            "blastic": 1,
            "mixed": 2,
            "lytic": 3
        }
        
        self.PAIN_POINTS = {
            "mild": 1,
            "moderate": 2,
            "functional": 3
        }
    
    def calculate(self, site_of_lesion: str, size_of_lesion: str, 
                  nature_of_lesion: str, pain: str) -> Dict[str, Any]:
        """
        Calculates Mirels' Criteria score for pathologic fracture risk
        
        Args:
            site_of_lesion: Location of lesion ("upper_limb", "lower_limb", "trochanteric_region")
            size_of_lesion: Size relative to bone diameter ("less_than_one_third", "one_third_to_two_thirds", "more_than_two_thirds")
            nature_of_lesion: Radiographic appearance ("blastic", "mixed", "lytic")
            pain: Pain level ("mild", "moderate", "functional")
            
        Returns:
            Dict with total score and clinical interpretation
        """
        
        # Validate inputs
        self._validate_inputs(site_of_lesion, size_of_lesion, nature_of_lesion, pain)
        
        # Calculate total score
        total_score = (
            self.SITE_POINTS[site_of_lesion] +
            self.SIZE_POINTS[size_of_lesion] +
            self.NATURE_POINTS[nature_of_lesion] +
            self.PAIN_POINTS[pain]
        )
        
        # Get interpretation
        interpretation = self._get_interpretation(total_score)
        
        return {
            "result": total_score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, site_of_lesion: str, size_of_lesion: str,
                        nature_of_lesion: str, pain: str):
        """Validates input parameters"""
        
        if site_of_lesion not in self.SITE_POINTS:
            raise ValueError(f"site_of_lesion must be one of: {', '.join(self.SITE_POINTS.keys())}")
        
        if size_of_lesion not in self.SIZE_POINTS:
            raise ValueError(f"size_of_lesion must be one of: {', '.join(self.SIZE_POINTS.keys())}")
        
        if nature_of_lesion not in self.NATURE_POINTS:
            raise ValueError(f"nature_of_lesion must be one of: {', '.join(self.NATURE_POINTS.keys())}")
        
        if pain not in self.PAIN_POINTS:
            raise ValueError(f"pain must be one of: {', '.join(self.PAIN_POINTS.keys())}")
    
    def _get_interpretation(self, score: int) -> Dict[str, str]:
        """
        Provides clinical interpretation based on Mirels score
        
        Args:
            score: Total Mirels score (4-12)
            
        Returns:
            Dict with interpretation details
        """
        
        if score <= 7:
            return {
                "stage": "Low Risk",
                "description": "0-4% fracture risk at 6 months",
                "interpretation": ("Safe to irradiate with minimal risk of fracture. Clinical "
                                 "management and radiotherapy appropriate. Prophylactic fixation "
                                 "not indicated.")
            }
        elif score == 8:
            return {
                "stage": "Intermediate Risk",
                "description": "15% fracture risk at 6 months",
                "interpretation": ("Consider prophylactic fixation based on clinical judgment. "
                                 "Treatment decision should incorporate patient-specific factors "
                                 "including functional status, life expectancy, and treatment goals.")
            }
        else:  # score >= 9
            return {
                "stage": "High Risk",
                "description": ">33% fracture risk at 6 months",
                "interpretation": ("Prophylactic fixation indicated prior to irradiation. High risk "
                                 "of pathologic fracture warrants surgical intervention to prevent "
                                 "fracture and maintain function.")
            }


def calculate_mirels_criteria(site_of_lesion: str, size_of_lesion: str,
                            nature_of_lesion: str, pain: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = MirelsCriteriaCalculator()
    return calculator.calculate(site_of_lesion, size_of_lesion, nature_of_lesion, pain)