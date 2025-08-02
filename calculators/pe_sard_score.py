"""
Pulmonary Embolism Syncope-Anemia-Renal Dysfunction (PE-SARD) Score Calculator

Estimates risk of early major bleeding in patients with acute pulmonary embolism (PE).
This validated risk assessment tool helps identify PE patients at higher risk for 
bleeding complications within 30 days of diagnosis.

References:
1. Barrios D, Rosa-Salazar V, Morillo R, Nieto R, Fernández-Golfín C, Zamorano JL, et al. 
   An Original Risk Score to Predict Early Major Bleeding in Acute Pulmonary Embolism: 
   The Syncope, Anemia, Renal Dysfunction (PE-SARD) Bleeding Score. Chest. 2021 Sep;160(3):992-1000. 
   doi: 10.1016/j.chest.2021.04.063.
2. Lobo JL, Zorrilla V, Aizpuru F, Grau E, Jiménez D, Prandoni P, et al. 
   External validation of the PE-SARD risk score for predicting early bleeding in acute 
   pulmonary embolism in the RIETE Registry. Thromb Res. 2024 Mar;235:176-181. 
   doi: 10.1016/j.thromres.2024.01.016.
"""

from typing import Dict, Any


class PeSardScoreCalculator:
    """Calculator for Pulmonary Embolism Syncope-Anemia-Renal Dysfunction (PE-SARD) Score"""
    
    def __init__(self):
        # PE-SARD scoring points
        self.SYNCOPE_POINTS = 1.5
        self.ANEMIA_POINTS = 2.5
        self.RENAL_DYSFUNCTION_POINTS = 1.0
        
        # Risk thresholds
        self.LOW_RISK_MAX = 0
        self.INTERMEDIATE_RISK_MAX = 2.5
    
    def calculate(self, syncope: str, anemia: str, renal_dysfunction: str) -> Dict[str, Any]:
        """
        Calculates PE-SARD score for bleeding risk assessment in acute PE
        
        Args:
            syncope (str): History of syncope ('yes' or 'no')
            anemia (str): Anemia with Hgb <12 g/dL ('yes' or 'no')
            renal_dysfunction (str): Renal dysfunction with GFR <60 mL/min ('yes' or 'no')
            
        Returns:
            Dict with PE-SARD score and clinical interpretation
        """
        
        # Validate inputs
        self._validate_inputs(syncope, anemia, renal_dysfunction)
        
        # Calculate total PE-SARD score
        total_score = self._calculate_total_score(syncope, anemia, renal_dysfunction)
        
        # Get interpretation
        interpretation = self._get_interpretation(total_score)
        
        return {
            "result": total_score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, syncope: str, anemia: str, renal_dysfunction: str):
        """Validates input parameters"""
        
        # Validate yes/no parameters
        yes_no_params = [
            (syncope, "syncope"),
            (anemia, "anemia"),
            (renal_dysfunction, "renal_dysfunction")
        ]
        
        for param, name in yes_no_params:
            if param not in ["yes", "no"]:
                raise ValueError(f"{name} must be 'yes' or 'no'")
    
    def _calculate_total_score(self, syncope: str, anemia: str, renal_dysfunction: str) -> float:
        """Calculates the total PE-SARD score"""
        
        score = 0.0
        
        # Add points for each present risk factor
        if syncope == "yes":
            score += self.SYNCOPE_POINTS
            
        if anemia == "yes":
            score += self.ANEMIA_POINTS
            
        if renal_dysfunction == "yes":
            score += self.RENAL_DYSFUNCTION_POINTS
            
        return score
    
    def _get_interpretation(self, score: float) -> Dict[str, str]:
        """
        Determines clinical interpretation based on PE-SARD score
        
        Args:
            score (float): Calculated PE-SARD score
            
        Returns:
            Dict with clinical interpretation
        """
        
        if score <= self.LOW_RISK_MAX:  # 0 points
            return {
                "stage": "Low Risk",
                "description": "Low bleeding risk",
                "interpretation": "Low risk for early major bleeding (0.6% incidence within 30 days). Standard anticoagulation therapy is appropriate with routine monitoring. Consider outpatient management if other clinical factors permit. Regular follow-up and patient education about bleeding signs remain important."
            }
        elif score <= self.INTERMEDIATE_RISK_MAX:  # 1-2.5 points
            return {
                "stage": "Intermediate Risk",
                "description": "Intermediate bleeding risk",
                "interpretation": "Intermediate risk for early major bleeding (1.5% incidence within 30 days). Consider more frequent monitoring and careful assessment of bleeding vs. thrombotic risk. May require modified anticoagulation approach, closer surveillance, or enhanced patient education about bleeding precautions."
            }
        else:  # >2.5 points
            return {
                "stage": "High Risk",
                "description": "High bleeding risk",
                "interpretation": "High risk for early major bleeding (2.5% incidence within 30 days). Requires careful consideration of bleeding vs. thrombotic risk in shared decision-making. Consider reduced-intensity anticoagulation, closer monitoring, alternative treatment strategies, or specialist consultation for complex management decisions."
            }


def calculate_pe_sard_score(syncope: str, anemia: str, renal_dysfunction: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = PeSardScoreCalculator()
    return calculator.calculate(syncope, anemia, renal_dysfunction)