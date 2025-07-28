"""
Thakar Score Calculator

Predicts risk of acute kidney injury (AKI) requiring dialysis after cardiac surgery.
Originally developed and validated in 33,217 patients at Cleveland Clinic Foundation.

References:
- Thakar CV, Arrigain S, Worley S, et al. A clinical score to predict acute renal failure after cardiac surgery. 
  J Am Soc Nephrol. 2005 Jan;16(1):162-8. doi: 10.1681/ASN.2004040331.
"""

from typing import Dict, Any


class ThakarScoreCalculator:
    """Calculator for Thakar Score (Acute Renal Failure after Cardiac Surgery)"""
    
    def __init__(self):
        # Point assignments based on original study
        self.GENDER_POINTS = {"male": 0, "female": 1}
        self.CHF_POINTS = {"no": 0, "yes": 1}
        self.LVEF_POINTS = {"no": 0, "yes": 1}
        self.IABP_POINTS = {"no": 0, "yes": 2}
        self.COPD_POINTS = {"no": 0, "yes": 1}
        self.DIABETES_POINTS = {"no": 0, "yes": 1}
        self.PREVIOUS_SURGERY_POINTS = {"no": 0, "yes": 1}
        self.EMERGENCY_POINTS = {"no": 0, "yes": 2}
        self.SURGERY_TYPE_POINTS = {
            "none": 0,
            "valve_only": 1,
            "cabg_and_valve": 2,
            "other": 2
        }
    
    def calculate(self, gender: str, congestive_heart_failure: str, 
                 left_ventricular_ejection_fraction_under_35: str, preoperative_iabp: str,
                 copd: str, insulin_requiring_diabetes: str, previous_cardiac_surgery: str,
                 emergency_surgery: str, surgery_type: str, preoperative_creatinine: float) -> Dict[str, Any]:
        """
        Calculates the Thakar Score using the provided parameters
        
        Args:
            gender (str): Patient gender ("male" or "female")
            congestive_heart_failure (str): Presence of CHF ("no" or "yes")
            left_ventricular_ejection_fraction_under_35 (str): LVEF <35% ("no" or "yes")
            preoperative_iabp (str): Preop IABP use ("no" or "yes")
            copd (str): COPD presence ("no" or "yes")
            insulin_requiring_diabetes (str): Insulin-requiring DM ("no" or "yes")
            previous_cardiac_surgery (str): Previous cardiac surgery ("no" or "yes")
            emergency_surgery (str): Emergency surgery ("no" or "yes")
            surgery_type (str): Surgery type ("none", "valve_only", "cabg_and_valve", "other")
            preoperative_creatinine (float): Preop creatinine in mg/dL
            
        Returns:
            Dict with the result and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(gender, congestive_heart_failure, 
                            left_ventricular_ejection_fraction_under_35, preoperative_iabp,
                            copd, insulin_requiring_diabetes, previous_cardiac_surgery,
                            emergency_surgery, surgery_type, preoperative_creatinine)
        
        # Calculate score
        score = self._calculate_score(gender, congestive_heart_failure, 
                                    left_ventricular_ejection_fraction_under_35, preoperative_iabp,
                                    copd, insulin_requiring_diabetes, previous_cardiac_surgery,
                                    emergency_surgery, surgery_type, preoperative_creatinine)
        
        # Get interpretation
        interpretation = self._get_interpretation(score)
        
        return {
            "result": score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, gender: str, congestive_heart_failure: str, 
                        left_ventricular_ejection_fraction_under_35: str, preoperative_iabp: str,
                        copd: str, insulin_requiring_diabetes: str, previous_cardiac_surgery: str,
                        emergency_surgery: str, surgery_type: str, preoperative_creatinine: float):
        """Validates input parameters"""
        
        # Validate string parameters
        valid_yes_no = ["no", "yes"]
        
        if gender not in ["male", "female"]:
            raise ValueError("Gender must be 'male' or 'female'")
        
        if congestive_heart_failure not in valid_yes_no:
            raise ValueError("Congestive heart failure must be 'no' or 'yes'")
        
        if left_ventricular_ejection_fraction_under_35 not in valid_yes_no:
            raise ValueError("Left ventricular ejection fraction <35% must be 'no' or 'yes'")
        
        if preoperative_iabp not in valid_yes_no:
            raise ValueError("Preoperative IABP must be 'no' or 'yes'")
        
        if copd not in valid_yes_no:
            raise ValueError("COPD must be 'no' or 'yes'")
        
        if insulin_requiring_diabetes not in valid_yes_no:
            raise ValueError("Insulin-requiring diabetes must be 'no' or 'yes'")
        
        if previous_cardiac_surgery not in valid_yes_no:
            raise ValueError("Previous cardiac surgery must be 'no' or 'yes'")
        
        if emergency_surgery not in valid_yes_no:
            raise ValueError("Emergency surgery must be 'no' or 'yes'")
        
        if surgery_type not in ["none", "valve_only", "cabg_and_valve", "other"]:
            raise ValueError("Surgery type must be 'none', 'valve_only', 'cabg_and_valve', or 'other'")
        
        # Validate creatinine
        if not isinstance(preoperative_creatinine, (int, float)):
            raise ValueError("Preoperative creatinine must be a number")
        
        if preoperative_creatinine < 0.1 or preoperative_creatinine > 20.0:
            raise ValueError("Preoperative creatinine must be between 0.1 and 20.0 mg/dL")
    
    def _calculate_score(self, gender: str, congestive_heart_failure: str, 
                        left_ventricular_ejection_fraction_under_35: str, preoperative_iabp: str,
                        copd: str, insulin_requiring_diabetes: str, previous_cardiac_surgery: str,
                        emergency_surgery: str, surgery_type: str, preoperative_creatinine: float) -> int:
        """Implements the Thakar Score calculation"""
        
        score = 0
        
        # Add points for each parameter
        score += self.GENDER_POINTS[gender]
        score += self.CHF_POINTS[congestive_heart_failure]
        score += self.LVEF_POINTS[left_ventricular_ejection_fraction_under_35]
        score += self.IABP_POINTS[preoperative_iabp]
        score += self.COPD_POINTS[copd]
        score += self.DIABETES_POINTS[insulin_requiring_diabetes]
        score += self.PREVIOUS_SURGERY_POINTS[previous_cardiac_surgery]
        score += self.EMERGENCY_POINTS[emergency_surgery]
        score += self.SURGERY_TYPE_POINTS[surgery_type]
        
        # Add points for creatinine ranges
        if preoperative_creatinine < 1.2:
            score += 0
        elif 1.2 <= preoperative_creatinine <= 2.0:
            score += 2
        else:  # > 2.0
            score += 5
        
        return score
    
    def _get_interpretation(self, score: int) -> Dict[str, str]:
        """
        Determines the interpretation based on the score
        
        Args:
            score (int): Calculated Thakar score
            
        Returns:
            Dict with interpretation
        """
        
        if score <= 2:
            return {
                "stage": "Very Low Risk",
                "description": "Very low risk for AKI requiring dialysis",
                "interpretation": "Score 0-2 points: Very low risk (0.3-0.5% risk of AKI requiring dialysis). These patients have excellent renal prognosis after cardiac surgery."
            }
        elif score <= 5:
            return {
                "stage": "Low Risk",
                "description": "Low risk for AKI requiring dialysis",
                "interpretation": "Score 3-5 points: Low risk (1.8-3.3% risk of AKI requiring dialysis). Standard perioperative renal monitoring is appropriate."
            }
        elif score <= 8:
            return {
                "stage": "Moderate Risk",
                "description": "Moderate risk for AKI requiring dialysis",
                "interpretation": "Score 6-8 points: Moderate risk (7.8-11.4% risk of AKI requiring dialysis). Consider enhanced renal monitoring and nephrotoxin avoidance."
            }
        elif score <= 13:
            return {
                "stage": "High Risk",
                "description": "High risk for AKI requiring dialysis",
                "interpretation": "Score 9-13 points: High risk (18.6-22.1% risk of AKI requiring dialysis). Aggressive renal protection strategies warranted, nephrology consultation may be beneficial."
            }
        else:  # score > 13
            return {
                "stage": "Very High Risk",
                "description": "Very high risk for AKI requiring dialysis",
                "interpretation": "Score >13 points: Very high risk (>22% risk of AKI requiring dialysis). Consider postponing surgery if possible to optimize patient, nephrology consultation recommended."
            }


def calculate_thakar_score(gender: str, congestive_heart_failure: str, 
                          left_ventricular_ejection_fraction_under_35: str, preoperative_iabp: str,
                          copd: str, insulin_requiring_diabetes: str, previous_cardiac_surgery: str,
                          emergency_surgery: str, surgery_type: str, preoperative_creatinine: float) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_thakar_score pattern
    """
    calculator = ThakarScoreCalculator()
    return calculator.calculate(gender, congestive_heart_failure, 
                              left_ventricular_ejection_fraction_under_35, preoperative_iabp,
                              copd, insulin_requiring_diabetes, previous_cardiac_surgery,
                              emergency_surgery, surgery_type, preoperative_creatinine)