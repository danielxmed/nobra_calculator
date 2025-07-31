"""
HEART Pathway Calculator

Identifies emergency department patients with acute chest pain for early discharge.
Combines HEART score with serial troponin measurements.

References:
- Mahler SA, et al. Circ Cardiovasc Qual Outcomes. 2015;8(2):195-203.
- Backus BE, et al. Int J Cardiol. 2013;168(3):2153-8.
"""

from typing import Dict, Any, Optional


class HeartPathwayCalculator:
    """Calculator for HEART Pathway for Early Discharge in Acute Chest Pain"""
    
    def calculate(self, history: int, ecg: int, age: int, 
                 risk_factors: int, initial_troponin: int, 
                 repeat_troponin_negative: Optional[str] = "not_done") -> Dict[str, Any]:
        """
        Calculates the HEART score and provides pathway recommendations
        
        Args:
            history (int): Clinical history score (0-2)
            ecg (int): ECG findings score (0-2)
            age (int): Age score (0-2)
            risk_factors (int): Risk factors score (0-2)
            initial_troponin (int): Initial troponin score (0-2)
            repeat_troponin_negative (str): 3-hour troponin result ("yes", "no", "not_done")
            
        Returns:
            Dict with the result and interpretation
        """
        
        # Validations
        self._validate_inputs(history, ecg, age, risk_factors, 
                            initial_troponin, repeat_troponin_negative)
        
        # Calculate HEART score
        heart_score = history + ecg + age + risk_factors + initial_troponin
        
        # Get interpretation based on score and troponin status
        interpretation = self._get_interpretation(heart_score, initial_troponin, 
                                                repeat_troponin_negative)
        
        return {
            "result": heart_score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"],
            "risk_category": interpretation["risk_category"],
            "mace_risk": interpretation["mace_risk"],
            "recommendation": interpretation["recommendation"],
            "initial_troponin_elevated": initial_troponin > 0,
            "pathway_complete": interpretation["pathway_complete"]
        }
    
    def _validate_inputs(self, history: int, ecg: int, age: int,
                        risk_factors: int, initial_troponin: int,
                        repeat_troponin_negative: Optional[str]):
        """Validates input parameters"""
        
        parameters = {
            "history": history,
            "ecg": ecg,
            "age": age,
            "risk_factors": risk_factors,
            "initial_troponin": initial_troponin
        }
        
        for param_name, value in parameters.items():
            if not isinstance(value, int):
                raise ValueError(f"{param_name.replace('_', ' ').capitalize()} must be an integer")
            
            if value < 0 or value > 2:
                raise ValueError(f"{param_name.replace('_', ' ').capitalize()} must be between 0 and 2")
        
        if repeat_troponin_negative is not None:
            if repeat_troponin_negative not in ["yes", "no", "not_done"]:
                raise ValueError("Repeat troponin result must be 'yes', 'no', or 'not_done'")
    
    def _get_interpretation(self, heart_score: int, initial_troponin: int, 
                          repeat_troponin_negative: Optional[str]) -> Dict[str, Any]:
        """
        Determines the interpretation based on HEART score and troponin status
        
        Args:
            heart_score (int): Total HEART score
            initial_troponin (int): Initial troponin score (0-2)
            repeat_troponin_negative (str): 3-hour troponin result
            
        Returns:
            Dict with interpretation
        """
        
        # Check if initial troponin is elevated (score 1-2)
        if initial_troponin >= 1:
            return {
                "stage": "High Risk",
                "risk_category": "High",
                "description": "Elevated initial troponin",
                "mace_risk": "12-65% 30-day MACE risk",
                "interpretation": "High risk for major adverse cardiac events due to elevated initial troponin. Immediate admission recommended for cardiology consultation, serial troponins, and objective cardiac testing.",
                "recommendation": "Admit to hospital/observation unit for cardiac evaluation",
                "pathway_complete": True
            }
        
        # HEART score ≤3 (low risk) with normal initial troponin
        if heart_score <= 3:
            if repeat_troponin_negative == "not_done":
                return {
                    "stage": "Low Risk (Pending)",
                    "risk_category": "Low",
                    "description": "0.9-1.7% 30-day MACE risk",
                    "mace_risk": "0.9-1.7% 30-day MACE risk",
                    "interpretation": "Low risk HEART score with negative initial troponin. Repeat troponin at 3 hours required to complete HEART Pathway. If 3-hour troponin is also negative, safe for early discharge.",
                    "recommendation": "Obtain 3-hour troponin to complete pathway",
                    "pathway_complete": False
                }
            elif repeat_troponin_negative == "yes":
                return {
                    "stage": "Low Risk",
                    "risk_category": "Low",
                    "description": "0.9-1.7% 30-day MACE risk",
                    "mace_risk": "0.9-1.7% 30-day MACE risk",
                    "interpretation": "Low risk for major adverse cardiac events with HEART score ≤3 and negative serial troponins at 0 and 3 hours. Safe for early discharge from the emergency department with outpatient follow-up.",
                    "recommendation": "Discharge home with primary care follow-up",
                    "pathway_complete": True
                }
            else:  # repeat_troponin_negative == "no"
                return {
                    "stage": "High Risk",
                    "risk_category": "High",
                    "description": "Positive 3-hour troponin",
                    "mace_risk": "12-65% 30-day MACE risk",
                    "interpretation": "Initially low risk HEART score but 3-hour troponin is positive. Now classified as high risk requiring admission for further cardiac evaluation and management.",
                    "recommendation": "Admit to hospital/observation unit for cardiac evaluation",
                    "pathway_complete": True
                }
        
        # HEART score ≥4 (high risk)
        else:
            return {
                "stage": "High Risk",
                "risk_category": "High",
                "description": "12-65% 30-day MACE risk",
                "mace_risk": "12-65% 30-day MACE risk",
                "interpretation": "High risk for major adverse cardiac events with HEART score ≥4. Admission recommended for further cardiac evaluation including serial troponins, objective cardiac testing, and possible cardiology consultation.",
                "recommendation": "Admit to hospital/observation unit for cardiac evaluation",
                "pathway_complete": True
            }


def calculate_heart_pathway(history: int, ecg: int, age: int,
                          risk_factors: int, initial_troponin: int,
                          repeat_troponin_negative: Optional[str] = "not_done") -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_heart_pathway pattern
    """
    calculator = HeartPathwayCalculator()
    return calculator.calculate(history, ecg, age, risk_factors,
                              initial_troponin, repeat_troponin_negative)