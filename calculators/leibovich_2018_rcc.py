"""
2018 Leibovich Model for Renal Cell Carcinoma (RCC) Calculator

Predicts progression-free and cancer-specific survival in patients with renal cell carcinoma.
Reference: Thompson RH et al. Am J Surg Pathol. 2018;42(4):474-481.
"""

from typing import Dict, Any


class Leibovich2018RccCalculator:
    """Calculator for 2018 Leibovich Model for RCC"""
    
    def __init__(self):
        # Scoring coefficients for Clear Cell RCC
        # Based on research data for progression-free survival (PFS) and cancer-specific survival (CSS)
        pass
    
    def calculate(self, age: int, ecog_status: str, constitutional_symptoms: bool,
                 adrenalectomy: bool, surgical_margins: str, tumor_grade: str,
                 coagulative_necrosis: bool, sarcomatoid_differentiation: bool,
                 tumor_size: float, perinephric_invasion: bool, tumor_thrombus: str,
                 extension_beyond_kidney: bool) -> Dict[str, Any]:
        """
        Calculates the Leibovich 2018 score for RCC
        
        Args:
            age: Patient's age in years
            ecog_status: ECOG Performance Status ("0" or "≥1")
            constitutional_symptoms: Presence of constitutional symptoms
            adrenalectomy: Adrenalectomy performed
            surgical_margins: Surgical margin status ("negative" or "positive")
            tumor_grade: Tumor grade ("1", "2", "3", "4")
            coagulative_necrosis: Presence of coagulative necrosis
            sarcomatoid_differentiation: Presence of sarcomatoid differentiation
            tumor_size: Tumor size in cm
            perinephric_invasion: Perinephric/renal sinus fat invasion
            tumor_thrombus: Tumor thrombus level ("none", "level_0", "level_1_4")
            extension_beyond_kidney: Extension beyond kidney
            
        Returns:
            Dict with progression-free survival and cancer-specific survival scores
        """
        
        # Validations
        self._validate_inputs(age, ecog_status, surgical_margins, tumor_grade, 
                             tumor_size, tumor_thrombus)
        
        # Calculate both PFS and CSS scores
        pfs_score = self._calculate_pfs_score(
            age, ecog_status, constitutional_symptoms, adrenalectomy,
            surgical_margins, tumor_grade, coagulative_necrosis,
            sarcomatoid_differentiation, tumor_size, perinephric_invasion,
            tumor_thrombus, extension_beyond_kidney
        )
        
        css_score = self._calculate_css_score(
            age, ecog_status, constitutional_symptoms, adrenalectomy,
            surgical_margins, tumor_grade, coagulative_necrosis,
            sarcomatoid_differentiation, tumor_size, perinephric_invasion,
            tumor_thrombus, extension_beyond_kidney
        )
        
        # Get interpretations
        pfs_interpretation = self._get_interpretation(pfs_score, "PFS")
        css_interpretation = self._get_interpretation(css_score, "CSS")
        
        return {
            "result": {
                "pfs_score": pfs_score,
                "css_score": css_score,
                "overall_risk_category": self._get_overall_risk_category(pfs_score, css_score)
            },
            "unit": "points",
            "interpretation": f"PFS: {pfs_interpretation['interpretation']} CSS: {css_interpretation['interpretation']}",
            "stage": self._get_overall_risk_category(pfs_score, css_score),
            "stage_description": f"PFS Score: {pfs_score}, CSS Score: {css_score}",
            "details": {
                "progression_free_survival": {
                    "score": pfs_score,
                    "stage": pfs_interpretation["stage"],
                    "interpretation": pfs_interpretation["interpretation"]
                },
                "cancer_specific_survival": {
                    "score": css_score,
                    "stage": css_interpretation["stage"],
                    "interpretation": css_interpretation["interpretation"]
                }
            },
            "components": self._get_components(
                age, ecog_status, constitutional_symptoms, adrenalectomy,
                surgical_margins, tumor_grade, coagulative_necrosis,
                sarcomatoid_differentiation, tumor_size, perinephric_invasion,
                tumor_thrombus, extension_beyond_kidney
            )
        }
    
    def _validate_inputs(self, age: int, ecog_status: str, surgical_margins: str,
                        tumor_grade: str, tumor_size: float, tumor_thrombus: str):
        """Validates input parameters"""
        
        if not isinstance(age, int) or age < 18 or age > 100:
            raise ValueError("Age must be an integer between 18 and 100 years")
        
        if ecog_status not in ["0", "≥1"]:
            raise ValueError("ECOG status must be '0' or '≥1'")
        
        if surgical_margins not in ["negative", "positive"]:
            raise ValueError("Surgical margins must be 'negative' or 'positive'")
        
        if tumor_grade not in ["1", "2", "3", "4"]:
            raise ValueError("Tumor grade must be '1', '2', '3', or '4'")
        
        if not isinstance(tumor_size, (int, float)) or tumor_size < 0.5 or tumor_size > 25.0:
            raise ValueError("Tumor size must be between 0.5 and 25.0 cm")
        
        if tumor_thrombus not in ["none", "level_0", "level_1_4"]:
            raise ValueError("Tumor thrombus must be 'none', 'level_0', or 'level_1_4'")
    
    def _calculate_pfs_score(self, age: int, ecog_status: str, constitutional_symptoms: bool,
                            adrenalectomy: bool, surgical_margins: str, tumor_grade: str,
                            coagulative_necrosis: bool, sarcomatoid_differentiation: bool,
                            tumor_size: float, perinephric_invasion: bool, tumor_thrombus: str,
                            extension_beyond_kidney: bool) -> int:
        """Calculate progression-free survival score"""
        
        score = 0
        
        # Constitutional symptoms (1 point)
        if constitutional_symptoms:
            score += 1
        
        # Tumor grade
        grade_points = {"1": 0, "2": 2, "3": 3, "4": 4}
        score += grade_points[tumor_grade]
        
        # Coagulative necrosis (2 points)
        if coagulative_necrosis:
            score += 2
        
        # Tumor size points
        if tumor_size <= 4:
            size_points = 0
        elif tumor_size <= 7:
            size_points = 3
        elif tumor_size <= 10:
            size_points = 4
        else:
            size_points = 5
        score += size_points
        
        # Perinephric invasion (1 point)
        if perinephric_invasion:
            score += 1
        
        # Tumor thrombus
        if tumor_thrombus == "level_0":
            score += 1
        elif tumor_thrombus == "level_1_4":
            score += 2
        
        # Extension beyond kidney (2 points)
        if extension_beyond_kidney:
            score += 2
        
        return score
    
    def _calculate_css_score(self, age: int, ecog_status: str, constitutional_symptoms: bool,
                            adrenalectomy: bool, surgical_margins: str, tumor_grade: str,
                            coagulative_necrosis: bool, sarcomatoid_differentiation: bool,
                            tumor_size: float, perinephric_invasion: bool, tumor_thrombus: str,
                            extension_beyond_kidney: bool) -> int:
        """Calculate cancer-specific survival score"""
        
        score = 0
        
        # Age ≥60 years (1 point)
        if age >= 60:
            score += 1
        
        # ECOG ≥1 (2 points)
        if ecog_status == "≥1":
            score += 2
        
        # Constitutional symptoms (1 point)
        if constitutional_symptoms:
            score += 1
        
        # Adrenalectomy (1 point)
        if adrenalectomy:
            score += 1
        
        # Positive surgical margins (1 point)
        if surgical_margins == "positive":
            score += 1
        
        # Tumor grade
        grade_points = {"1": 0, "2": 2, "3": 3, "4": 4}
        score += grade_points[tumor_grade]
        
        # Coagulative necrosis (2 points)
        if coagulative_necrosis:
            score += 2
        
        # Sarcomatoid differentiation (1 point)
        if sarcomatoid_differentiation:
            score += 1
        
        # Tumor size points (slightly different from PFS)
        if tumor_size <= 4:
            size_points = 0
        elif tumor_size <= 7:
            size_points = 3
        elif tumor_size <= 10:
            size_points = 4
        else:
            size_points = 4
        score += size_points
        
        # Perinephric invasion (2 points for CSS)
        if perinephric_invasion:
            score += 2
        
        # Tumor thrombus
        if tumor_thrombus == "level_0":
            score += 1
        elif tumor_thrombus == "level_1_4":
            score += 2
        
        return score
    
    def _get_interpretation(self, score: int, score_type: str) -> Dict[str, str]:
        """
        Determines the interpretation based on the score and type
        
        Args:
            score: Calculated score
            score_type: "PFS" or "CSS"
            
        Returns:
            Dict with clinical interpretation
        """
        
        if score <= 4:
            return {
                "stage": "Low Risk",
                "description": "Excellent prognosis",
                "interpretation": f"Low risk of {'progression' if score_type == 'PFS' else 'cancer-specific death'}. Standard surveillance recommended."
            }
        elif score <= 9:
            return {
                "stage": "Intermediate Risk",
                "description": "Good prognosis",
                "interpretation": f"Intermediate risk of {'progression' if score_type == 'PFS' else 'cancer-specific death'}. Enhanced surveillance may be considered."
            }
        elif score <= 14:
            return {
                "stage": "High Risk",
                "description": "Poor prognosis",
                "interpretation": f"High risk of {'progression' if score_type == 'PFS' else 'cancer-specific death'}. Intensive surveillance and adjuvant therapy consideration recommended."
            }
        else:
            return {
                "stage": "Very High Risk",
                "description": "Very poor prognosis",
                "interpretation": f"Very high risk of {'progression' if score_type == 'PFS' else 'cancer-specific death'}. Aggressive management warranted."
            }
    
    def _get_overall_risk_category(self, pfs_score: int, css_score: int) -> str:
        """Determine overall risk category based on both scores"""
        
        max_score = max(pfs_score, css_score)
        
        if max_score <= 4:
            return "Low Risk"
        elif max_score <= 9:
            return "Intermediate Risk"
        elif max_score <= 14:
            return "High Risk"
        else:
            return "Very High Risk"
    
    def _get_components(self, age: int, ecog_status: str, constitutional_symptoms: bool,
                       adrenalectomy: bool, surgical_margins: str, tumor_grade: str,
                       coagulative_necrosis: bool, sarcomatoid_differentiation: bool,
                       tumor_size: float, perinephric_invasion: bool, tumor_thrombus: str,
                       extension_beyond_kidney: bool) -> Dict[str, Any]:
        """Return component breakdown for transparency"""
        
        return {
            "age_≥60": 1 if age >= 60 else 0,
            "ecog_≥1": 2 if ecog_status == "≥1" else 0,
            "constitutional_symptoms": 1 if constitutional_symptoms else 0,
            "adrenalectomy": 1 if adrenalectomy else 0,
            "positive_margins": 1 if surgical_margins == "positive" else 0,
            "tumor_grade": tumor_grade,
            "coagulative_necrosis": 2 if coagulative_necrosis else 0,
            "sarcomatoid_differentiation": 1 if sarcomatoid_differentiation else 0,
            "tumor_size_cm": tumor_size,
            "perinephric_invasion": 1 if perinephric_invasion else 0,
            "tumor_thrombus": tumor_thrombus,
            "extension_beyond_kidney": 2 if extension_beyond_kidney else 0
        }


def calculate_leibovich_2018_rcc(age: int, ecog_status: str, constitutional_symptoms: bool,
                                adrenalectomy: bool, surgical_margins: str, tumor_grade: str,
                                coagulative_necrosis: bool, sarcomatoid_differentiation: bool,
                                tumor_size: float, perinephric_invasion: bool, tumor_thrombus: str,
                                extension_beyond_kidney: bool) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_leibovich_2018_rcc pattern
    """
    calculator = Leibovich2018RccCalculator()
    return calculator.calculate(age, ecog_status, constitutional_symptoms,
                               adrenalectomy, surgical_margins, tumor_grade,
                               coagulative_necrosis, sarcomatoid_differentiation,
                               tumor_size, perinephric_invasion, tumor_thrombus,
                               extension_beyond_kidney)