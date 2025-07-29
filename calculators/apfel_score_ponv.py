"""
Apfel Score for Postoperative Nausea and Vomiting Calculator

Predicts risk of postoperative nausea and vomiting (PONV) using four simple 
clinical factors to guide prophylactic antiemetic therapy decisions.

References (Vancouver style):
1. Apfel CC, Läärä E, Koivuranta M, Greim CA, Roewer N. A simplified risk score 
   for predicting postoperative nausea and vomiting: conclusions from cross-validations 
   between two centers. Anesthesiology. 1999;91(3):693-700.
2. Gan TJ, Belani KG, Bergese S, et al. Fourth Consensus Guidelines for the Management 
   of Postoperative Nausea and Vomiting. Anesth Analg. 2020;131(2):411-448.
3. Apfel CC, Heidrich FM, Jukar-Rao S, et al. Evidence-based analysis of risk factors 
   for postoperative nausea and vomiting. Br J Anaesth. 2012;109(5):742-753.
"""

from typing import Dict, Any


class ApfelScorePonvCalculator:
    """Calculator for Apfel Score for Postoperative Nausea and Vomiting"""
    
    def __init__(self):
        # Risk factors scoring (each factor contributes 1 point if present)
        self.FEMALE_GENDER_POINTS = 1
        self.NONSMOKER_POINTS = 1
        self.HISTORY_MOTION_SICKNESS_PONV_POINTS = 1
        self.POSTOP_OPIOIDS_POINTS = 1
    
    def calculate(self, gender: str, smoking_status: str, history_motion_sickness_ponv: str, 
                 postoperative_opioids: str) -> Dict[str, Any]:
        """
        Calculates the Apfel Score for PONV risk
        
        Args:
            gender (str): Patient gender ("male" or "female")
            smoking_status (str): Smoking status ("smoker" or "nonsmoker")
            history_motion_sickness_ponv (str): History of motion sickness or PONV ("no" or "yes")
            postoperative_opioids (str): Use of postoperative opioids ("no" or "yes")
            
        Returns:
            Dict with the result and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(gender, smoking_status, history_motion_sickness_ponv, postoperative_opioids)
        
        # Calculate score
        score = self._calculate_score(gender, smoking_status, history_motion_sickness_ponv, postoperative_opioids)
        
        # Get interpretation
        interpretation = self._get_interpretation(score)
        
        return {
            "result": score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, gender: str, smoking_status: str, history_motion_sickness_ponv: str, 
                        postoperative_opioids: str):
        """Validates input parameters"""
        
        if gender not in ["male", "female"]:
            raise ValueError("Gender must be 'male' or 'female'")
        
        if smoking_status not in ["smoker", "nonsmoker"]:
            raise ValueError("Smoking status must be 'smoker' or 'nonsmoker'")
        
        if history_motion_sickness_ponv not in ["no", "yes"]:
            raise ValueError("History of motion sickness or PONV must be 'no' or 'yes'")
        
        if postoperative_opioids not in ["no", "yes"]:
            raise ValueError("Postoperative opioids must be 'no' or 'yes'")
    
    def _calculate_score(self, gender: str, smoking_status: str, history_motion_sickness_ponv: str,
                        postoperative_opioids: str) -> int:
        """Calculates the Apfel Score"""
        
        score = 0
        
        # Female gender: +1 point
        if gender == "female":
            score += self.FEMALE_GENDER_POINTS
        
        # Non-smoker: +1 point
        if smoking_status == "nonsmoker":
            score += self.NONSMOKER_POINTS
        
        # History of motion sickness or PONV: +1 point
        if history_motion_sickness_ponv == "yes":
            score += self.HISTORY_MOTION_SICKNESS_PONV_POINTS
        
        # Use of postoperative opioids: +1 point
        if postoperative_opioids == "yes":
            score += self.POSTOP_OPIOIDS_POINTS
        
        return score
    
    def _get_interpretation(self, score: int) -> Dict[str, str]:
        """
        Determines the interpretation based on the Apfel Score
        
        Args:
            score (int): Calculated Apfel Score (0-4)
            
        Returns:
            Dict with interpretation details
        """
        
        interpretations = {
            0: {
                "stage": "Very Low Risk",
                "description": "0 risk factors",
                "interpretation": "Approximately 10% risk of PONV within 24 hours. Prophylactic antiemetics generally not recommended."
            },
            1: {
                "stage": "Low Risk",
                "description": "1 risk factor", 
                "interpretation": "Approximately 20% risk of PONV within 24 hours. Consider single prophylactic antiemetic agent."
            },
            2: {
                "stage": "Moderate Risk",
                "description": "2 risk factors",
                "interpretation": "Approximately 40% risk of PONV within 24 hours. Recommend combination of 2 prophylactic antiemetic agents."
            },
            3: {
                "stage": "High Risk",
                "description": "3 risk factors",
                "interpretation": "Approximately 60% risk of PONV within 24 hours. Recommend combination of 2-3 prophylactic antiemetic agents."
            },
            4: {
                "stage": "Very High Risk",
                "description": "4 risk factors",
                "interpretation": "Approximately 80% risk of PONV within 24 hours. Recommend combination of multiple prophylactic antiemetic agents and consider total intravenous anesthesia (TIVA)."
            }
        }
        
        return interpretations.get(score, interpretations[4])


def calculate_apfel_score_ponv(gender: str, smoking_status: str, history_motion_sickness_ponv: str,
                              postoperative_opioids: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_apfel_score_ponv pattern
    """
    calculator = ApfelScorePonvCalculator()
    return calculator.calculate(gender, smoking_status, history_motion_sickness_ponv, postoperative_opioids)
