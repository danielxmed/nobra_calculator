"""
ACTION ICU Score for Intensive Care in NSTEMI Calculator

Predicts risk of NSTEMI complications requiring ICU care.

References:
- Fanaroff AC, Chen AY, Roe MT, et al. A Simple Risk Score to Predict In-Hospital 
  Complications in Patients With Non-ST-Segment Elevation Myocardial Infarction. 
  J Am Heart Assoc. 2018;7(11):e008108.
"""

from typing import Dict, Any


class ActionIcuNstemiCalculator:
    """Calculator for ACTION ICU Score for Intensive Care in NSTEMI"""
    
    def __init__(self):
        # Scoring system constants
        self.AGE_SCORES = {
            "under_70": 0,
            "70_or_over": 1
        }
        
        self.CREATININE_SCORES = {
            "under_1_1": 0,
            "1_1_or_over": 1
        }
        
        self.HEART_RATE_SCORES = {
            "under_85": 0,
            "85_to_100": 1,
            "100_or_over": 3
        }
        
        self.SYSTOLIC_BP_SCORES = {
            "145_or_over": 0,
            "125_to_145": 1,
            "under_125": 3
        }
        
        self.TROPONIN_SCORES = {
            "under_12": 0,
            "12_or_over": 2
        }
        
        self.HEART_FAILURE_SCORES = {
            "no": 0,
            "yes": 5
        }
        
        self.ST_DEPRESSION_SCORES = {
            "no": 0,
            "yes": 1
        }
        
        self.REVASCULARIZATION_SCORES = {
            "yes": 0,
            "no": 1
        }
        
        self.LUNG_DISEASE_SCORES = {
            "no": 0,
            "yes": 2
        }
    
    def calculate(self, age: str, serum_creatinine: str, heart_rate: str, 
                 systolic_bp: str, troponin_ratio: str, heart_failure_signs: str,
                 st_depression: str, prior_revascularization: str, 
                 chronic_lung_disease: str) -> Dict[str, Any]:
        """
        Calculates the ACTION ICU score for NSTEMI complications
        
        Args:
            age (str): Age category ("under_70" or "70_or_over")
            serum_creatinine (str): Creatinine level ("under_1_1" or "1_1_or_over")
            heart_rate (str): Heart rate category ("under_85", "85_to_100", or "100_or_over")
            systolic_bp (str): Systolic BP category ("145_or_over", "125_to_145", or "under_125")
            troponin_ratio (str): Troponin ratio ("under_12" or "12_or_over")
            heart_failure_signs (str): Heart failure signs ("no" or "yes")
            st_depression (str): ST depression on EKG ("no" or "yes")
            prior_revascularization (str): Prior revascularization history ("yes" or "no")
            chronic_lung_disease (str): Chronic lung disease ("no" or "yes")
            
        Returns:
            Dict with the result and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(age, serum_creatinine, heart_rate, systolic_bp, 
                            troponin_ratio, heart_failure_signs, st_depression,
                            prior_revascularization, chronic_lung_disease)
        
        # Calculate total score
        score = self._calculate_score(age, serum_creatinine, heart_rate, systolic_bp,
                                    troponin_ratio, heart_failure_signs, st_depression,
                                    prior_revascularization, chronic_lung_disease)
        
        # Get interpretation
        interpretation = self._get_interpretation(score)
        
        return {
            "result": score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, age: str, serum_creatinine: str, heart_rate: str,
                        systolic_bp: str, troponin_ratio: str, heart_failure_signs: str,
                        st_depression: str, prior_revascularization: str,
                        chronic_lung_disease: str):
        """Validates input parameters"""
        
        if age not in self.AGE_SCORES:
            raise ValueError(f"Invalid age category: {age}")
            
        if serum_creatinine not in self.CREATININE_SCORES:
            raise ValueError(f"Invalid creatinine category: {serum_creatinine}")
            
        if heart_rate not in self.HEART_RATE_SCORES:
            raise ValueError(f"Invalid heart rate category: {heart_rate}")
            
        if systolic_bp not in self.SYSTOLIC_BP_SCORES:
            raise ValueError(f"Invalid systolic BP category: {systolic_bp}")
            
        if troponin_ratio not in self.TROPONIN_SCORES:
            raise ValueError(f"Invalid troponin ratio: {troponin_ratio}")
            
        if heart_failure_signs not in self.HEART_FAILURE_SCORES:
            raise ValueError(f"Invalid heart failure signs: {heart_failure_signs}")
            
        if st_depression not in self.ST_DEPRESSION_SCORES:
            raise ValueError(f"Invalid ST depression: {st_depression}")
            
        if prior_revascularization not in self.REVASCULARIZATION_SCORES:
            raise ValueError(f"Invalid prior revascularization: {prior_revascularization}")
            
        if chronic_lung_disease not in self.LUNG_DISEASE_SCORES:
            raise ValueError(f"Invalid chronic lung disease: {chronic_lung_disease}")
    
    def _calculate_score(self, age: str, serum_creatinine: str, heart_rate: str,
                        systolic_bp: str, troponin_ratio: str, heart_failure_signs: str,
                        st_depression: str, prior_revascularization: str,
                        chronic_lung_disease: str) -> int:
        """Calculates the total ACTION ICU score"""
        
        total_score = 0
        
        # Add points for each parameter
        total_score += self.AGE_SCORES[age]
        total_score += self.CREATININE_SCORES[serum_creatinine]
        total_score += self.HEART_RATE_SCORES[heart_rate]
        total_score += self.SYSTOLIC_BP_SCORES[systolic_bp]
        total_score += self.TROPONIN_SCORES[troponin_ratio]
        total_score += self.HEART_FAILURE_SCORES[heart_failure_signs]
        total_score += self.ST_DEPRESSION_SCORES[st_depression]
        total_score += self.REVASCULARIZATION_SCORES[prior_revascularization]
        total_score += self.LUNG_DISEASE_SCORES[chronic_lung_disease]
        
        return total_score
    
    def _get_interpretation(self, score: int) -> Dict[str, str]:
        """
        Determines the interpretation based on the score
        
        Args:
            score (int): Calculated ACTION ICU score
            
        Returns:
            Dict with interpretation
        """
        
        if score <= 3:
            return {
                "stage": "Low risk",
                "description": "Low risk of ICU complications",
                "interpretation": "Low risk of complications requiring ICU care. Consider standard cardiac monitoring and care on telemetry unit."
            }
        elif score <= 7:
            return {
                "stage": "Intermediate risk",
                "description": "Intermediate risk of ICU complications",
                "interpretation": "Intermediate risk of complications requiring ICU care. Consider enhanced monitoring and possible step-down unit care."
            }
        else:  # score >= 8
            return {
                "stage": "High risk",
                "description": "High risk of ICU complications",
                "interpretation": "High risk of complications requiring ICU care. Consider direct ICU admission for intensive monitoring and management."
            }


def calculate_action_icu_nstemi(age: str, serum_creatinine: str, heart_rate: str,
                               systolic_bp: str, troponin_ratio: str, heart_failure_signs: str,
                               st_depression: str, prior_revascularization: str,
                               chronic_lung_disease: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = ActionIcuNstemiCalculator()
    return calculator.calculate(age, serum_creatinine, heart_rate, systolic_bp,
                               troponin_ratio, heart_failure_signs, st_depression,
                               prior_revascularization, chronic_lung_disease)