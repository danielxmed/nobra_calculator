"""
Modified SOAR Score for Stroke Calculator

Predicts short-term mortality in acute stroke by adding NIHSS score to the original 
SOAR criteria, improving prognostic accuracy while maintaining clinical practicality.

References:
1. Myint PK, et al. Int J Stroke. 2014;9(3):278-83.
2. Abdul-Rahim AH, et al. Eur J Neurol. 2015;22(8):1048-55.
3. Myint PK, et al. J Am Heart Assoc. 2015;4(12):e002652.
"""

from typing import Dict, Any


class ModifiedSoarScoreCalculator:
    """Calculator for Modified SOAR Score for Stroke"""
    
    def __init__(self):
        # Age category mappings
        self.AGE_MAPPING = {
            "65_or_less": 0,
            "66_to_85": 1,
            "85_or_more": 2
        }
        
        # Stroke subtype mappings
        self.SUBTYPE_MAPPING = {
            "ischemic": 0,
            "hemorrhagic": 1
        }
        
        # Oxfordshire classification mappings
        self.OXFORDSHIRE_MAPPING = {
            "partial_anterior_lacunar": 0,
            "posterior_circulation": 1,
            "total_anterior_circulation": 2
        }
        
        # Pre-stroke mRS mappings
        self.MRS_MAPPING = {
            "0_to_2": 0,
            "3_to_4": 1,
            "5": 2
        }
    
    def calculate(self, age_category: str, stroke_subtype: str, oxfordshire_classification: str,
                  prestroke_mrs: str, nihss_score: int) -> Dict[str, Any]:
        """
        Calculates the Modified SOAR score for stroke mortality prediction
        
        Args:
            age_category (str): Patient age category
            stroke_subtype (str): Type of stroke (ischemic or hemorrhagic)
            oxfordshire_classification (str): Oxfordshire Community Stroke Project classification
            prestroke_mrs (str): Pre-stroke modified Rankin Scale category
            nihss_score (int): National Institutes of Health Stroke Scale score
            
        Returns:
            Dict with Modified SOAR score and clinical interpretation
        """
        
        # Validate inputs
        self._validate_inputs(age_category, stroke_subtype, oxfordshire_classification,
                             prestroke_mrs, nihss_score)
        
        # Calculate component scores
        age_points = self.AGE_MAPPING[age_category]
        subtype_points = self.SUBTYPE_MAPPING[stroke_subtype]
        oxfordshire_points = self.OXFORDSHIRE_MAPPING[oxfordshire_classification]
        mrs_points = self.MRS_MAPPING[prestroke_mrs]
        nihss_points = self._calculate_nihss_score(nihss_score)
        
        # Total Modified SOAR score
        total_score = age_points + subtype_points + oxfordshire_points + mrs_points + nihss_points
        
        # Get interpretation
        interpretation = self._get_interpretation(total_score)
        
        return {
            "result": total_score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, age_category: str, stroke_subtype: str, oxfordshire_classification: str,
                        prestroke_mrs: str, nihss_score: int):
        """Validates input parameters"""
        
        if age_category not in self.AGE_MAPPING:
            raise ValueError(f"Age category must be one of: {list(self.AGE_MAPPING.keys())}")
        
        if stroke_subtype not in self.SUBTYPE_MAPPING:
            raise ValueError(f"Stroke subtype must be one of: {list(self.SUBTYPE_MAPPING.keys())}")
        
        if oxfordshire_classification not in self.OXFORDSHIRE_MAPPING:
            raise ValueError(f"Oxfordshire classification must be one of: {list(self.OXFORDSHIRE_MAPPING.keys())}")
        
        if prestroke_mrs not in self.MRS_MAPPING:
            raise ValueError(f"Pre-stroke mRS must be one of: {list(self.MRS_MAPPING.keys())}")
        
        if not isinstance(nihss_score, int) or nihss_score < 0 or nihss_score > 42:
            raise ValueError("NIHSS score must be an integer between 0 and 42")
    
    def _calculate_nihss_score(self, nihss_score: int) -> int:
        """
        Calculates NIHSS component score
        
        NIHSS scoring:
        - 1-4: 0 points
        - 5-10: 1 point
        - 11-20: 2 points
        - ≥21: 2 points
        """
        
        if nihss_score <= 4:
            return 0
        elif nihss_score <= 10:
            return 1
        else:  # nihss_score >= 11
            return 2
    
    def _get_interpretation(self, score: int) -> Dict[str, str]:
        """
        Provides clinical interpretation based on Modified SOAR score
        
        Args:
            score (int): Total Modified SOAR score
            
        Returns:
            Dict with interpretation details
        """
        
        if score <= 2:
            return {
                "stage": "Low Risk",
                "description": "3-7% early mortality risk",
                "interpretation": (f"Modified SOAR Score {score}: Low risk of early mortality. "
                                f"The patient has a 3-7% risk of early mortality following acute stroke. "
                                f"This represents a good prognosis with favorable functional outcomes expected. "
                                f"Standard stroke care protocols should be followed with routine monitoring. "
                                f"The mSOAR score demonstrates excellent prognostic utility with an area under "
                                f"the ROC curve of 0.83, significantly improved from the original SOAR score. "
                                f"Continue with evidence-based acute stroke management including appropriate "
                                f"reperfusion therapy if indicated, antiplatelet therapy, and stroke prevention "
                                f"measures. Early mobilization and rehabilitation planning are appropriate.")
            }
        elif score <= 4:
            return {
                "stage": "Moderate Risk",
                "description": "8-20% early mortality risk",
                "interpretation": (f"Modified SOAR Score {score}: Moderate risk of early mortality. "
                                f"The patient has an 8-20% risk of early mortality following acute stroke. "
                                f"This indicates moderate stroke severity requiring close monitoring and "
                                f"intensive nursing care. Consider more frequent neurological assessments and "
                                f"monitoring for complications such as brain edema, hemorrhagic transformation, "
                                f"or cardiac events. Ensure appropriate stroke unit care with multidisciplinary "
                                f"team involvement. Discuss prognosis with family members while maintaining "
                                f"realistic hope for recovery. The patient may benefit from more intensive "
                                f"rehabilitation planning and consideration of potential complications that "
                                f"could affect recovery trajectory.")
            }
        elif score <= 6:
            return {
                "stage": "High Risk",
                "description": "21-35% early mortality risk",
                "interpretation": (f"Modified SOAR Score {score}: High risk of early mortality. "
                                f"The patient has a 21-35% risk of early mortality following acute stroke. "
                                f"This indicates severe stroke with significant risk of poor outcomes. "
                                f"Aggressive monitoring and management are warranted, including frequent "
                                f"neurological assessments, intracranial pressure monitoring if indicated, "
                                f"and proactive management of complications. Early and comprehensive "
                                f"discussions with family regarding prognosis, treatment goals, and "
                                f"potential outcomes are essential. Consider palliative care consultation "
                                f"to assist with symptom management and family support. Despite the high "
                                f"mortality risk, aggressive treatment may still be appropriate depending "
                                f"on patient/family preferences and overall clinical context.")
            }
        else:  # score >= 7
            return {
                "stage": "Very High Risk",
                "description": ">35% early mortality risk",
                "interpretation": (f"Modified SOAR Score {score}: Very high risk of early mortality. "
                                f"The patient has greater than 35% risk of early mortality following "
                                f"acute stroke. This represents very severe stroke with poor prognosis. "
                                f"Immediate and comprehensive discussions with patient/family regarding "
                                f"goals of care, prognosis, and treatment preferences are critical. "
                                f"Palliative care consultation should be strongly considered to help "
                                f"with symptom management, family support, and care planning decisions. "
                                f"While aggressive treatment may still be pursued based on patient/family "
                                f"wishes, realistic expectations about outcomes should be communicated. "
                                f"Focus on comfort measures, dignity, and quality of life becomes "
                                f"increasingly important in addition to medical management.")
            }


def calculate_modified_soar_score(age_category: str, stroke_subtype: str, oxfordshire_classification: str,
                                prestroke_mrs: str, nihss_score: int) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = ModifiedSoarScoreCalculator()
    return calculator.calculate(age_category, stroke_subtype, oxfordshire_classification,
                               prestroke_mrs, nihss_score)