"""
ABCD² Score for TIA Calculator

Estimates stroke risk after a transient ischemic attack (TIA),
based on patient risk factors.
"""

from typing import Dict, Any


class Abcd2ScoreCalculator:
    """Calculator for ABCD² Score for TIA"""
    
    def calculate(self, age: int, blood_pressure: str, clinical_features: str, 
                 duration: str, diabetes: str) -> Dict[str, Any]:
        """
        Calculates the ABCD² Score
        
        Args:
            age (int): Patient's age in years
            blood_pressure (str): "normal" (<140/90) or "elevated" (≥140/90)
            clinical_features (str): "unilateral_weakness", "speech_disturbance", "other"
            duration (str): "less_10min", "10_59min", "60min_or_more"
            diabetes (str): "yes" or "no"
            
        Returns:
            Dict with the result and interpretation
        """
        
        # Validations
        self._validate_inputs(age, blood_pressure, clinical_features, duration, diabetes)
        
        # Calculate score
        score = 0
        
        # A - Age (≥60 years)
        if age >= 60:
            score += 1
        
        # B - Blood Pressure (≥140/90 mmHg)
        if blood_pressure == "elevated":
            score += 1
        
        # C - Clinical features
        if clinical_features == "unilateral_weakness":
            score += 2
        elif clinical_features == "speech_disturbance":
            score += 1
        # "other" = 0 points
        
        # D - Duration
        if duration == "60min_or_more":
            score += 2
        elif duration == "10_59min":
            score += 1
        # "less_10min" = 0 points
        
        # D - Diabetes
        if diabetes == "yes":
            score += 1
        
        # Get interpretation
        interpretation = self._get_interpretation(score)
        
        return {
            "result": score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"],
            "stroke_risk_2days": interpretation["stroke_risk_2days"],
            "stroke_risk_7days": interpretation["stroke_risk_7days"],
            "stroke_risk_90days": interpretation["stroke_risk_90days"]
        }
    
    def _validate_inputs(self, age, blood_pressure, clinical_features, duration, diabetes):
        """Validates input parameters"""
        
        if not isinstance(age, int) or age < 18 or age > 120:
            raise ValueError("Age must be an integer between 18 and 120 years")
        
        valid_bp = ["normal", "elevated"]
        if blood_pressure not in valid_bp:
            raise ValueError(f"Blood pressure must be: {', '.join(valid_bp)}")
        
        valid_features = ["unilateral_weakness", "speech_disturbance", "other"]
        if clinical_features not in valid_features:
            raise ValueError(f"Clinical features must be: {', '.join(valid_features)}")
        
        valid_duration = ["less_10min", "10_59min", "60min_or_more"]
        if duration not in valid_duration:
            raise ValueError(f"Duration must be: {', '.join(valid_duration)}")
        
        valid_diabetes = ["yes", "no"]
        if diabetes not in valid_diabetes:
            raise ValueError(f"Diabetes must be: {', '.join(valid_diabetes)}")
    
    def _get_interpretation(self, score: int) -> Dict[str, str]:
        """
        Determines the interpretation based on the score
        
        Args:
            score (int): Calculated value (0-7)
            
        Returns:
            Dict with interpretation
        """
        
        if score <= 3:
            return {
                "stage": "Low Risk",
                "description": "Low stroke risk",
                "interpretation": "Stroke risk in 2 days: 1.0%; in 7 days: 1.2%; in 90 days: 3.1%. Can be managed outpatient with scheduled diagnostic evaluation.",
                "stroke_risk_2days": "1.0%",
                "stroke_risk_7days": "1.2%",
                "stroke_risk_90days": "3.1%"
            }
        elif score <= 5:
            return {
                "stage": "Moderate Risk",
                "description": "Moderate stroke risk",
                "interpretation": "Stroke risk in 2 days: 4.1%; in 7 days: 5.9%; in 90 days: 9.8%. Consider hospitalization for urgent investigation and initiation of preventive measures.",
                "stroke_risk_2days": "4.1%",
                "stroke_risk_7days": "5.9%",
                "stroke_risk_90days": "9.8%"
            }
        else:  # score 6-7
            return {
                "stage": "High Risk",
                "description": "High stroke risk",
                "interpretation": "Stroke risk in 2 days: 8.1%; in 7 days: 11.7%; in 90 days: 17.8%. Urgent hospitalization recommended for investigation and immediate initiation of preventive measures.",
                "stroke_risk_2days": "8.1%",
                "stroke_risk_7days": "11.7%",
                "stroke_risk_90days": "17.8%"
            }


def calculate_abcd2_score(age: int, blood_pressure: str, clinical_features: str, 
                         duration: str, diabetes: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = Abcd2ScoreCalculator()
    return calculator.calculate(age, blood_pressure, clinical_features, duration, diabetes)
