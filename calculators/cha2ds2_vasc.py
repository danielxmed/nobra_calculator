"""
CHA₂DS₂-VASc Score Calculator

Calculates stroke risk in patients with non-valvular atrial fibrillation.
Reference: Lip GY et al. Chest. 2010;137(2):263-72.
"""

from typing import Dict, Any


class Cha2ds2VascCalculator:
    """Calculator for CHA₂DS₂-VASc Score"""
    
    def __init__(self):
        # Annual stroke risks by score
        self.stroke_risk = {
            0: 0.3,
            1: 0.9,
            2: 2.9,
            3: 4.6,
            4: 6.7,
            5: 10.0,
            6: 13.6,
            7: 15.7,
            8: 15.2,
            9: 17.4
        }
    
    def calculate(self, age: int, sex: str, congestive_heart_failure: bool,
                 hypertension: bool, stroke_tia_thromboembolism: bool,
                 vascular_disease: bool, diabetes: bool) -> Dict[str, Any]:
        """
        Calculates the CHA₂DS₂-VASc score
        
        Args:
            age: Age in years
            sex: "male" or "female"
            congestive_heart_failure: History of CHF or LV dysfunction
            hypertension: History of hypertension
            stroke_tia_thromboembolism: History of Stroke/TIA/TE
            vascular_disease: Previous vascular disease
            diabetes: History of diabetes
            
        Returns:
            Dict with result, interpretation, and annual risk
        """
        
        # Validations
        self._validate_inputs(age, sex)
        
        # Calculate score
        score = 0
        
        # C - Congestive heart failure (1 point)
        if congestive_heart_failure:
            score += 1
        
        # H - Hypertension (1 point)
        if hypertension:
            score += 1
        
        # A₂ - Age (0-2 points)
        if age >= 75:
            score += 2
        elif age >= 65:
            score += 1
        
        # D - Diabetes (1 point)
        if diabetes:
            score += 1
        
        # S₂ - Stroke/TIA/TE (2 points)
        if stroke_tia_thromboembolism:
            score += 2
        
        # V - Vascular disease (1 point)
        if vascular_disease:
            score += 1
        
        # Sc - Sex category (1 point if female)
        if sex.lower() == "female":
            score += 1
        
        # Get interpretation
        interpretation = self._get_interpretation(score, sex)
        annual_risk = self.stroke_risk.get(score, 17.4)
        
        return {
            "result": score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"],
            "annual_stroke_risk": f"{annual_risk}%",
            "components": {
                "congestive_heart_failure": 1 if congestive_heart_failure else 0,
                "hypertension": 1 if hypertension else 0,
                "age_points": 2 if age >= 75 else (1 if age >= 65 else 0),
                "diabetes": 1 if diabetes else 0,
                "stroke_tia": 2 if stroke_tia_thromboembolism else 0,
                "vascular_disease": 1 if vascular_disease else 0,
                "sex_category": 1 if sex.lower() == "female" else 0
            }
        }
    
    def _validate_inputs(self, age: int, sex: str):
        """Validates input parameters"""
        
        if not isinstance(age, int) or age < 18 or age > 120:
            raise ValueError("Age must be an integer between 18 and 120 years")
        
        if sex.lower() not in ["male", "female"]:
            raise ValueError("Sex must be 'male' or 'female'")
    
    def _get_interpretation(self, score: int, sex: str) -> Dict[str, str]:
        """
        Determines the interpretation based on the score and sex
        
        Args:
            score: Calculated CHA₂DS₂-VASc score
            sex: Patient's sex
            
        Returns:
            Dict with clinical interpretation
        """
        
        is_male = sex.lower() == "male"
        annual_risk = self.stroke_risk.get(score, 17.4)
        
        if score == 0:
            return {
                "stage": "Very Low Risk",
                "description": f"Annual stroke risk: {annual_risk}%",
                "interpretation": "Male patients with 0 points: anticoagulation not recommended. Consider aspirin or no antithrombotic therapy."
            }
        
        elif score == 1:
            if is_male:
                return {
                    "stage": "Low Risk",
                    "description": f"Annual stroke risk: {annual_risk}%",
                    "interpretation": "Men with 1 point: anticoagulation may be considered after risk-benefit discussion with the patient."
                }
            else:
                return {
                    "stage": "Low Risk",
                    "description": f"Annual stroke risk: {annual_risk}%",
                    "interpretation": "Women with 1 point (due to sex only): anticoagulation not recommended."
                }
        
        elif score == 2:
            return {
                "stage": "Moderate Risk",
                "description": f"Annual stroke risk: {annual_risk}%",
                "interpretation": "Oral anticoagulation recommended (warfarin with INR 2-3 or DOAC). Benefit outweighs bleeding risk in most patients."
            }
        
        elif score == 3:
            return {
                "stage": "Moderate-High Risk",
                "description": f"Annual stroke risk: {annual_risk}%",
                "interpretation": "Oral anticoagulation strongly recommended. Consider DOACs as first choice due to better safety profile."
            }
        
        elif score == 4:
            return {
                "stage": "High Risk",
                "description": f"Annual stroke risk: {annual_risk}%",
                "interpretation": "Oral anticoagulation essential. Monitor adherence and adjust dose according to renal function if using DOACs."
            }
        
        elif score == 5:
            return {
                "stage": "High Risk",
                "description": f"Annual stroke risk: {annual_risk}%",
                "interpretation": "Oral anticoagulation mandatory. Consider strategies to improve adherence and minimize bleeding risk."
            }
        
        elif score == 6:
            return {
                "stage": "Very High Risk",
                "description": f"Annual stroke risk: {annual_risk}%",
                "interpretation": "Oral anticoagulation imperative. Evaluate and optimize modifiable risk factors. Frequent monitoring."
            }
        
        else:  # score >= 7
            return {
                "stage": "Extreme Risk",
                "description": f"Annual stroke risk: {annual_risk}%",
                "interpretation": "Critical oral anticoagulation. Consider left atrial appendage occlusion if absolute contraindication to anticoagulation."
            }


def calculate_cha2ds2_vasc(age: int, sex: str, congestive_heart_failure: bool,
                          hypertension: bool, stroke_tia_thromboembolism: bool,
                          vascular_disease: bool, diabetes: bool) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_cha2ds2_vasc pattern
    """
    calculator = Cha2ds2VascCalculator()
    return calculator.calculate(age, sex, congestive_heart_failure,
                               hypertension, stroke_tia_thromboembolism,
                               vascular_disease, diabetes)
