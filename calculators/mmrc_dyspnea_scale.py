"""
mMRC (Modified Medical Research Council) Dyspnea Scale Calculator

Stratifies severity of dyspnea in respiratory diseases, particularly COPD,
based on functional disability due to breathlessness.

References:
1. Mahler DA, Wells CK. Chest. 1988;93(3):580-6.
2. Bestall JC, et al. Thorax. 1999;54(7):581-6.
3. Kocks JW, et al. Respir Res. 2006;7:62.
4. GOLD Guidelines 2023.
"""

from typing import Dict, Any


class MmrcDyspneaScaleCalculator:
    """Calculator for mMRC (Modified Medical Research Council) Dyspnea Scale"""
    
    def __init__(self):
        # Grade mapping
        self.GRADE_VALUES = {
            "grade_0": 0,
            "grade_1": 1,
            "grade_2": 2,
            "grade_3": 3,
            "grade_4": 4
        }
    
    def calculate(self, dyspnea_grade: str) -> Dict[str, Any]:
        """
        Determines mMRC dyspnea grade and functional limitation
        
        Args:
            dyspnea_grade: Patient's dyspnea grade ("grade_0" to "grade_4")
            
        Returns:
            Dict with grade and clinical interpretation
        """
        
        # Validate inputs
        self._validate_inputs(dyspnea_grade)
        
        # Get numeric grade
        grade_value = self.GRADE_VALUES[dyspnea_grade]
        
        # Get interpretation
        interpretation = self._get_interpretation(grade_value)
        
        return {
            "result": grade_value,
            "unit": "grade",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, dyspnea_grade: str):
        """Validates input parameters"""
        
        if dyspnea_grade not in self.GRADE_VALUES:
            raise ValueError(f"dyspnea_grade must be one of: {', '.join(self.GRADE_VALUES.keys())}")
    
    def _get_interpretation(self, grade: int) -> Dict[str, str]:
        """
        Provides clinical interpretation based on mMRC grade
        
        Args:
            grade: mMRC grade (0-4)
            
        Returns:
            Dict with interpretation details
        """
        
        if grade == 0:
            return {
                "stage": "No Dyspnea",
                "description": "Minimal functional limitation",
                "interpretation": ("Dyspnea only with strenuous exercise. Normal exercise tolerance "
                                 "with minimal functional impairment. Patient can perform most "
                                 "activities without significant breathlessness.")
            }
        elif grade == 1:
            return {
                "stage": "Mild Dyspnea",
                "description": "Mild functional limitation",
                "interpretation": ("Dyspnea when hurrying or walking up a slight hill. Slight "
                                 "limitation in activities involving exertion or walking uphill. "
                                 "Generally good functional capacity for daily activities.")
            }
        elif grade == 2:
            return {
                "stage": "Moderate Dyspnea",
                "description": "Moderate functional limitation",
                "interpretation": ("Walks slower than people of the same age because of dyspnea, or "
                                 "has to stop for breath when walking at own pace on level ground. "
                                 "Moderate limitation affecting walking speed and endurance.")
            }
        elif grade == 3:
            return {
                "stage": "Severe Dyspnea",
                "description": "Severe functional limitation",
                "interpretation": ("Stops for breath after walking 100 yards (91 m) or after a few "
                                 "minutes on level ground. Significant limitation in walking distance. "
                                 "Severely impaired exercise tolerance.")
            }
        else:  # grade == 4
            return {
                "stage": "Very Severe Dyspnea",
                "description": "Very severe functional limitation",
                "interpretation": ("Too dyspneic to leave house or breathless when dressing or "
                                 "undressing. Severe disability with breathlessness at rest or "
                                 "with minimal activity. Housebound due to dyspnea.")
            }


def calculate_mmrc_dyspnea_scale(dyspnea_grade: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = MmrcDyspneaScaleCalculator()
    return calculator.calculate(dyspnea_grade)