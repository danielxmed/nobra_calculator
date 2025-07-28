"""
ADAPT Protocol Calculator

Assesses chest pain patients at 2 hours for risk of cardiac event.
ADAPT stands for Accelerated Diagnostic Protocol to Assess Patients with 
Chest Pain Symptoms Using Contemporary Troponins as the Only Biomarker.

References:
- Than M, Flaws D, Sanders S, et al. Development and validation of the Emergency Department 
  Assessment of Chest pain Score and 2 h accelerated diagnostic protocol. Emerg Med Australas. 
  2014 Feb;26(1):34-44. doi: 10.1111/1742-6723.12164.
- Cullen L, Mueller C, Parsonage WA, et al. Validation of high-sensitivity troponin I in a 
  2-hour diagnostic strategy to assess 30-day outcomes in emergency department patients with 
  possible acute coronary syndrome. J Am Coll Cardiol. 2013 Oct 1;62(14):1242-9. 
  doi: 10.1016/j.jacc.2013.02.078.
"""

from typing import Dict, Any


class AdaptProtocolCalculator:
    """Calculator for ADAPT Protocol for Cardiac Event Risk"""
    
    def __init__(self):
        # ADAPT Protocol uses binary decision tree approach
        pass
    
    def calculate(self, abnormal_troponin: str, ischemic_changes_ecg: str,
                 age_65_or_older: str, three_or_more_cad_risk_factors: str,
                 known_cad: str, aspirin_use_past_7_days: str, 
                 severe_angina: str) -> Dict[str, Any]:
        """
        Calculates the ADAPT Protocol risk stratification
        
        Args:
            abnormal_troponin (str): Abnormal troponin at 0 or 2 hours ("no" or "yes")
            ischemic_changes_ecg (str): Ischemic changes on ECG ("no" or "yes")
            age_65_or_older (str): Age ≥65 years ("no" or "yes")
            three_or_more_cad_risk_factors (str): ≥3 CAD risk factors ("no" or "yes")
            known_cad (str): Known CAD (stenosis ≥50%) ("no" or "yes")
            aspirin_use_past_7_days (str): Aspirin use in past 7 days ("no" or "yes")
            severe_angina (str): Severe angina (≥2 episodes in 24 hrs or persisting discomfort) ("no" or "yes")
            
        Returns:
            Dict with the result and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(abnormal_troponin, ischemic_changes_ecg,
                            age_65_or_older, three_or_more_cad_risk_factors,
                            known_cad, aspirin_use_past_7_days, severe_angina)
        
        # Calculate risk level
        risk_level = self._calculate_risk_level(abnormal_troponin, ischemic_changes_ecg,
                                              age_65_or_older, three_or_more_cad_risk_factors,
                                              known_cad, aspirin_use_past_7_days, severe_angina)
        
        # Get interpretation
        interpretation = self._get_interpretation(risk_level)
        
        return {
            "result": risk_level,
            "unit": "",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, abnormal_troponin: str, ischemic_changes_ecg: str,
                        age_65_or_older: str, three_or_more_cad_risk_factors: str,
                        known_cad: str, aspirin_use_past_7_days: str, 
                        severe_angina: str):
        """Validates input parameters"""
        
        valid_options = ["no", "yes"]
        
        if abnormal_troponin not in valid_options:
            raise ValueError("Abnormal troponin must be 'no' or 'yes'")
        
        if ischemic_changes_ecg not in valid_options:
            raise ValueError("Ischemic changes on ECG must be 'no' or 'yes'")
        
        if age_65_or_older not in valid_options:
            raise ValueError("Age ≥65 years must be 'no' or 'yes'")
        
        if three_or_more_cad_risk_factors not in valid_options:
            raise ValueError("≥3 CAD risk factors must be 'no' or 'yes'")
        
        if known_cad not in valid_options:
            raise ValueError("Known CAD must be 'no' or 'yes'")
        
        if aspirin_use_past_7_days not in valid_options:
            raise ValueError("Aspirin use in past 7 days must be 'no' or 'yes'")
        
        if severe_angina not in valid_options:
            raise ValueError("Severe angina must be 'no' or 'yes'")
    
    def _calculate_risk_level(self, abnormal_troponin: str, ischemic_changes_ecg: str,
                             age_65_or_older: str, three_or_more_cad_risk_factors: str,
                             known_cad: str, aspirin_use_past_7_days: str, 
                             severe_angina: str) -> str:
        """Implements the ADAPT Protocol decision logic"""
        
        # High risk if any of the following are present:
        # 1. Abnormal troponin at 0 or 2 hours
        # 2. Ischemic changes on ECG
        # 3. Any TIMI risk factors (age ≥65, ≥3 CAD risk factors, known CAD, aspirin use, severe angina)
        
        high_risk_criteria = [
            abnormal_troponin == "yes",
            ischemic_changes_ecg == "yes",
            age_65_or_older == "yes",
            three_or_more_cad_risk_factors == "yes",
            known_cad == "yes",
            aspirin_use_past_7_days == "yes",
            severe_angina == "yes"
        ]
        
        # If any high-risk criteria are met, patient is high risk
        if any(high_risk_criteria):
            return "High Risk"
        else:
            return "Low Risk"
    
    def _get_interpretation(self, risk_level: str) -> Dict[str, str]:
        """
        Determines the interpretation based on the risk level
        
        Args:
            risk_level (str): Calculated risk level ("Low Risk" or "High Risk")
            
        Returns:
            Dict with interpretation
        """
        
        if risk_level == "Low Risk":
            return {
                "stage": "Low Risk",
                "description": "Low risk for major cardiac event",
                "interpretation": "0-0.3% risk of major cardiac event in 30 days. Patient can be safely discharged from the emergency department with appropriate outpatient follow-up."
            }
        else:  # High Risk
            return {
                "stage": "High Risk",
                "description": "High risk for major cardiac event",
                "interpretation": "Elevated risk of major cardiac event in 30 days. Further cardiac evaluation and monitoring recommended. Consider cardiology consultation and hospital admission or observation."
            }


def calculate_adapt_protocol(abnormal_troponin: str, ischemic_changes_ecg: str,
                           age_65_or_older: str, three_or_more_cad_risk_factors: str,
                           known_cad: str, aspirin_use_past_7_days: str, 
                           severe_angina: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_adapt_protocol pattern
    """
    calculator = AdaptProtocolCalculator()
    return calculator.calculate(abnormal_troponin, ischemic_changes_ecg,
                              age_65_or_older, three_or_more_cad_risk_factors,
                              known_cad, aspirin_use_past_7_days, severe_angina)