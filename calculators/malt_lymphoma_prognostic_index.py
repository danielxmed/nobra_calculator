"""
MALT Lymphoma Prognostic Index (MALT-IPI) Calculator

Calculates the MALT-IPI score to identify MALT lymphoma patients at risk for poor outcomes.
Based on three clinical parameters: age ≥70 years, Ann Arbor stage III/IV, and elevated LDH.

References:
1. Thieblemont C, Cascione L, Conconi A, Kiesewetter B, Raderer M, Gaidano G, et al. 
   A MALT lymphoma prognostic index. Blood. 2017 Sep 21;130(12):1409-1417. 
   doi: 10.1182/blood-2017-03-771915.
2. Hong J, Lee Y, Park J, Kim SJ, Lim ST, Kim JS, et al. Validation of the MALT-lymphoma 
   international prognostic index (MALT-IPI) and extension of the prognostic model with 
   the addition of β2-microglobulin. Ann Hematol. 2019 Nov;98(11):2499-2507. 
   doi: 10.1007/s00277-019-03808-x.
"""

from typing import Dict, Any


class MaltLymphomaPrognosticIndexCalculator:
    """Calculator for MALT Lymphoma Prognostic Index (MALT-IPI)"""
    
    def __init__(self):
        # Age threshold for scoring
        self.AGE_THRESHOLD = 70
        
        # Valid Ann Arbor stages
        self.VALID_STAGES = ["I", "II", "III", "IV"]
        self.ADVANCED_STAGES = ["III", "IV"]
        
        # Valid LDH levels
        self.VALID_LDH_LEVELS = ["normal", "elevated"]
    
    def calculate(self, age: int, ldh_level: str, ann_arbor_stage: str) -> Dict[str, Any]:
        """
        Calculates the MALT-IPI score using the provided clinical parameters
        
        Args:
            age (int): Patient age in years
            ldh_level (str): LDH level relative to upper limit of normal ("normal" or "elevated")
            ann_arbor_stage (str): Ann Arbor stage ("I", "II", "III", or "IV")
            
        Returns:
            Dict with the result, survival data, and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(age, ldh_level, ann_arbor_stage)
        
        # Calculate individual component scores
        age_score = self._calculate_age_score(age)
        ldh_score = self._calculate_ldh_score(ldh_level)
        stage_score = self._calculate_stage_score(ann_arbor_stage)
        
        # Calculate total MALT-IPI score
        total_score = age_score + ldh_score + stage_score
        
        # Get risk stratification and interpretation
        interpretation_data = self._get_interpretation(total_score)
        
        # Get detailed survival outcomes
        survival_outcomes = self._get_survival_outcomes(total_score)
        
        return {
            "result": {
                "total_score": total_score,
                "age_score": age_score,
                "ldh_score": ldh_score,
                "stage_score": stage_score,
                "age_category": f"Age {'≥70' if age >= self.AGE_THRESHOLD else '<70'} years: {age}",
                "ldh_category": f"LDH {ldh_level}",
                "stage_category": f"Ann Arbor stage {ann_arbor_stage}",
                "survival_outcomes": survival_outcomes
            },
            "unit": "points",
            "interpretation": interpretation_data["interpretation"],
            "stage": interpretation_data["stage"],
            "stage_description": interpretation_data["description"]
        }
    
    def _validate_inputs(self, age: int, ldh_level: str, ann_arbor_stage: str):
        """Validates input parameters"""
        
        # Validate age
        if not isinstance(age, int):
            raise ValueError("Age must be an integer")
        
        if age < 18 or age > 120:
            raise ValueError("Age must be between 18 and 120 years")
        
        # Validate LDH level
        if not isinstance(ldh_level, str):
            raise ValueError("LDH level must be a string")
        
        if ldh_level.lower() not in [level.lower() for level in self.VALID_LDH_LEVELS]:
            raise ValueError(f"LDH level must be one of: {', '.join(self.VALID_LDH_LEVELS)}")
        
        # Validate Ann Arbor stage
        if not isinstance(ann_arbor_stage, str):
            raise ValueError("Ann Arbor stage must be a string")
        
        if ann_arbor_stage.upper() not in self.VALID_STAGES:
            raise ValueError(f"Ann Arbor stage must be one of: {', '.join(self.VALID_STAGES)}")
    
    def _calculate_age_score(self, age: int) -> int:
        """Calculates score based on age"""
        return 1 if age >= self.AGE_THRESHOLD else 0
    
    def _calculate_ldh_score(self, ldh_level: str) -> int:
        """Calculates score based on LDH level"""
        return 1 if ldh_level.lower() == "elevated" else 0
    
    def _calculate_stage_score(self, ann_arbor_stage: str) -> int:
        """Calculates score based on Ann Arbor stage"""
        return 1 if ann_arbor_stage.upper() in self.ADVANCED_STAGES else 0
    
    def _get_survival_outcomes(self, total_score: int) -> Dict[str, str]:
        """
        Returns detailed survival outcomes based on risk group
        
        Args:
            total_score (int): Total MALT-IPI score
            
        Returns:
            Dict with 5-year survival percentages
        """
        
        if total_score == 0:  # Low risk
            return {
                "event_free_survival_5yr": "76.0%",
                "progression_free_survival_5yr": "56.8%",
                "cause_specific_survival_5yr": "98.2%",
                "overall_survival_5yr": "96.7%"
            }
        elif total_score == 1:  # Intermediate risk
            return {
                "event_free_survival_5yr": "48.4%",
                "progression_free_survival_5yr": "48.0%",
                "cause_specific_survival_5yr": "94.7%",
                "overall_survival_5yr": "81.7%"
            }
        else:  # High risk (≥2 points)
            return {
                "event_free_survival_5yr": "15.7%",
                "progression_free_survival_5yr": "22.7%",
                "cause_specific_survival_5yr": "74.3%",
                "overall_survival_5yr": "64.9%"
            }
    
    def _get_interpretation(self, total_score: int) -> Dict[str, str]:
        """
        Determines the risk stratification and interpretation based on the total score
        
        Args:
            total_score (int): Total MALT-IPI score
            
        Returns:
            Dict with risk stratification and clinical interpretation
        """
        
        if total_score == 0:  # Low risk
            return {
                "stage": "Low Risk",
                "description": "Low risk of poor outcomes",
                "interpretation": (
                    "Low risk MALT lymphoma with excellent prognosis. 5-year survival outcomes: "
                    "overall survival 96.7%, event-free survival 76.0%, cause-specific survival 98.2%, "
                    "and progression-free survival 56.8%. Conservative management approaches may be "
                    "considered including watchful waiting or minimal intervention. Regular monitoring "
                    "with clinical assessment and imaging is recommended. Treatment decisions should "
                    "consider patient preferences, comorbidities, and symptoms."
                )
            }
        elif total_score == 1:  # Intermediate risk
            return {
                "stage": "Intermediate Risk",
                "description": "Intermediate risk of poor outcomes",
                "interpretation": (
                    "Intermediate risk MALT lymphoma with moderate prognosis. 5-year survival outcomes: "
                    "overall survival 81.7%, event-free survival 48.4%, cause-specific survival 94.7%, "
                    "and progression-free survival 48.0%. Consider more intensive monitoring and "
                    "treatment planning. May benefit from early intervention depending on clinical "
                    "presentation, symptoms, and disease location. Regular follow-up with oncology "
                    "is recommended for treatment optimization."
                )
            }
        else:  # High risk (≥2 points)
            return {
                "stage": "High Risk",
                "description": "High risk of poor outcomes",
                "interpretation": (
                    "High risk MALT lymphoma with poor prognosis. 5-year survival outcomes: "
                    "overall survival 64.9%, event-free survival 15.7%, cause-specific survival 74.3%, "
                    "and progression-free survival 22.7%. Aggressive treatment approaches should be "
                    "strongly considered including combination chemotherapy, rituximab-based regimens, "
                    "or clinical trial enrollment. Prompt oncology referral and multidisciplinary "
                    "care planning are essential for optimal outcomes."
                )
            }


def calculate_malt_lymphoma_prognostic_index(age: int, ldh_level: str, ann_arbor_stage: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = MaltLymphomaPrognosticIndexCalculator()
    return calculator.calculate(age, ldh_level, ann_arbor_stage)