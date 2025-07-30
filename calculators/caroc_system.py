"""
CAROC System Calculator

Canadian Association of Radiologists and Osteoporosis Canada (CAROC) System
for assessing 10-year absolute fracture risk.

References:
1. Leslie WD, Berger C, Langsetmo L, et al. Construction and validation of a 
   simplified fracture risk assessment tool for Canadian women and men: results 
   from the CaMos and Manitoba cohorts. Osteoporos Int. 2011;22(6):1873-83.
2. Papaioannou A, Morin S, Cheung AM, et al. 2010 clinical practice guidelines 
   for the diagnosis and management of osteoporosis in Canada. CMAJ. 2010;182(17):1864-73.
"""

from typing import Dict, Any


class CAROCSystemCalculator:
    """Calculator for CAROC System"""
    
    def __init__(self):
        # T-score thresholds for risk categories by age and sex
        # Based on 2010 CAROC guidelines and literature
        # Structure: {sex: {age_range: (moderate_threshold, high_threshold)}}
        self.T_SCORE_THRESHOLDS = {
            'female': {
                (50, 54): (-1.5, -3.2),
                (55, 59): (-1.7, -3.3),
                (60, 64): (-1.8, -3.4),
                (65, 69): (-1.9, -3.5),
                (70, 74): (-2.1, -3.6),
                (75, 79): (-2.3, -3.7),
                (80, 85): (-2.5, -3.8)
            },
            'male': {
                (50, 54): (-1.3, -3.0),
                (55, 59): (-1.4, -3.1),
                (60, 64): (-1.6, -3.2),
                (65, 69): (-1.8, -3.3),
                (70, 74): (-2.0, -3.4),
                (75, 79): (-2.2, -3.5),
                (80, 85): (-2.4, -3.6)
            }
        }
        
        # Automatic classification thresholds
        self.OSTEOPOROSIS_THRESHOLD = -2.5
    
    def calculate(self, sex: str, age: int, femoral_neck_t_score: float,
                  fragility_fracture: str, glucocorticoid_use: str) -> Dict[str, Any]:
        """
        Calculates CAROC fracture risk category
        
        Args:
            sex (str): 'male' or 'female'
            age (int): Age in years (50-85)
            femoral_neck_t_score (float): Femoral neck T-score
            fragility_fracture (str): 'yes' or 'no'
            glucocorticoid_use (str): 'yes' or 'no'
            
        Returns:
            Dict with risk category and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(sex, age, femoral_neck_t_score, 
                            fragility_fracture, glucocorticoid_use)
        
        # Determine base risk category from T-score
        base_risk = self._determine_base_risk(sex, age, femoral_neck_t_score)
        
        # Apply clinical risk factor modifiers
        final_risk = self._apply_risk_modifiers(base_risk, fragility_fracture, 
                                               glucocorticoid_use, femoral_neck_t_score)
        
        # Get interpretation
        interpretation = self._get_interpretation(final_risk)
        
        # Calculate risk percentage estimate
        risk_percentage = self._estimate_risk_percentage(final_risk)
        
        return {
            "result": final_risk,
            "unit": "category",
            "interpretation": interpretation["interpretation"],
            "stage": final_risk,
            "stage_description": interpretation["description"],
            "details": {
                "base_risk_category": base_risk,
                "fragility_fracture": fragility_fracture,
                "glucocorticoid_use": glucocorticoid_use,
                "femoral_neck_t_score": femoral_neck_t_score,
                "estimated_10_year_risk": risk_percentage,
                "automatic_moderate_risk": femoral_neck_t_score <= self.OSTEOPOROSIS_THRESHOLD
            }
        }
    
    def _validate_inputs(self, sex: str, age: int, femoral_neck_t_score: float,
                        fragility_fracture: str, glucocorticoid_use: str):
        """Validates input parameters"""
        
        if sex not in ['male', 'female']:
            raise ValueError("Sex must be 'male' or 'female'")
        
        if not isinstance(age, (int, float)) or age < 50 or age > 85:
            raise ValueError("Age must be between 50 and 85 years")
        
        if not isinstance(femoral_neck_t_score, (int, float)) or \
           femoral_neck_t_score < -5 or femoral_neck_t_score > 2:
            raise ValueError("Femoral neck T-score must be between -5 and 2")
        
        if fragility_fracture not in ['yes', 'no']:
            raise ValueError("Fragility fracture must be 'yes' or 'no'")
        
        if glucocorticoid_use not in ['yes', 'no']:
            raise ValueError("Glucocorticoid use must be 'yes' or 'no'")
    
    def _determine_base_risk(self, sex: str, age: int, t_score: float) -> str:
        """Determines base risk category from T-score thresholds"""
        
        # Find appropriate age range
        age_range = None
        for age_range_key in self.T_SCORE_THRESHOLDS[sex]:
            if age_range_key[0] <= age <= age_range_key[1]:
                age_range = age_range_key
                break
        
        if age_range is None:
            # Default to closest age range
            if age < 50:
                age_range = (50, 54)
            else:
                age_range = (80, 85)
        
        moderate_threshold, high_threshold = self.T_SCORE_THRESHOLDS[sex][age_range]
        
        # Determine risk category
        if t_score < high_threshold:
            return "High Risk"
        elif t_score < moderate_threshold:
            return "Moderate Risk"
        else:
            return "Low Risk"
    
    def _apply_risk_modifiers(self, base_risk: str, fragility_fracture: str,
                             glucocorticoid_use: str, t_score: float) -> str:
        """Applies clinical risk factor modifiers to base risk"""
        
        # Rule 1: Any T-score ≤ -2.5 indicates at least moderate risk
        if t_score <= self.OSTEOPOROSIS_THRESHOLD and base_risk == "Low Risk":
            base_risk = "Moderate Risk"
        
        # Rule 2: Both fragility fracture AND glucocorticoid use = High Risk
        if fragility_fracture == "yes" and glucocorticoid_use == "yes":
            return "High Risk"
        
        # Rule 3: Either risk factor elevates by one category
        if fragility_fracture == "yes" or glucocorticoid_use == "yes":
            if base_risk == "Low Risk":
                return "Moderate Risk"
            elif base_risk == "Moderate Risk":
                return "High Risk"
        
        return base_risk
    
    def _estimate_risk_percentage(self, risk_category: str) -> str:
        """Estimates the 10-year fracture risk percentage range"""
        
        if risk_category == "Low Risk":
            return "<10%"
        elif risk_category == "Moderate Risk":
            return "10-20%"
        else:  # High Risk
            return ">20%"
    
    def _get_interpretation(self, risk_category: str) -> Dict[str, str]:
        """
        Provides interpretation based on risk category
        
        Args:
            risk_category (str): Risk category
            
        Returns:
            Dict with interpretation details
        """
        
        if risk_category == "Low Risk":
            return {
                "description": "<10% 10-year fracture risk",
                "interpretation": (
                    "Low risk of major osteoporotic fracture over the next 10 years. "
                    "General lifestyle recommendations including adequate calcium "
                    "(1200 mg/day), vitamin D (800-2000 IU/day), regular weight-bearing "
                    "exercise, fall prevention, and avoidance of smoking and excessive "
                    "alcohol. Repeat BMD in 3-5 years or as clinically indicated."
                )
            }
        elif risk_category == "Moderate Risk":
            return {
                "description": "10-20% 10-year fracture risk",
                "interpretation": (
                    "Moderate risk of major osteoporotic fracture over the next 10 years. "
                    "Consider pharmacologic therapy based on patient preferences, "
                    "additional risk factors, and BMD trends. Ensure adequate calcium "
                    "and vitamin D supplementation. Implement fall prevention strategies. "
                    "Consider vertebral imaging if height loss or back pain present."
                )
            }
        else:  # High Risk
            return {
                "description": ">20% 10-year fracture risk",
                "interpretation": (
                    "High risk of major osteoporotic fracture over the next 10 years. "
                    "Pharmacologic therapy strongly recommended unless contraindicated. "
                    "First-line options include bisphosphonates, denosumab, or other "
                    "approved therapies. Ensure adequate calcium and vitamin D. "
                    "Implement comprehensive fracture prevention strategies including "
                    "fall prevention and exercise programs."
                )
            }


def calculate_caroc_system(sex: str, age: int, femoral_neck_t_score: float,
                          fragility_fracture: str, glucocorticoid_use: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = CAROCSystemCalculator()
    return calculator.calculate(sex, age, femoral_neck_t_score,
                              fragility_fracture, glucocorticoid_use)