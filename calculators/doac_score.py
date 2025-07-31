"""
Direct-Acting Oral Anticoagulants (DOAC) Score Calculator

Predicts bleeding risk in patients with atrial fibrillation on direct-acting oral anticoagulants.

References:
1. Aggarwal A, Wang TY, Rumsfeld JS, et al. Development and Validation of the DOAC Score: 
   A Novel Bleeding Risk Prediction Tool for Patients With Atrial Fibrillation on 
   Direct-Acting Oral Anticoagulants. Circulation. 2023 Nov 7;148(19):1482-1492.
2. Costa OS, Beyer-Westendorf J, Ashton V, et al. Performance of HAS-BLED and DOAC scores 
   to predict major bleeding events in atrial fibrillation patients treated with direct 
   oral anticoagulants. Thromb Res. 2024 Aug;240:109063.
"""

from typing import Dict, Any


class DoacScoreCalculator:
    """Calculator for Direct-Acting Oral Anticoagulants (DOAC) Score"""
    
    def __init__(self):
        # Age scoring points
        self.AGE_POINTS = {
            "under_65": 0,
            "65_to_69": 2,
            "70_to_74": 3,
            "75_to_79": 4,
            "80_or_over": 5
        }
        
        # Creatinine clearance scoring points
        self.CREATININE_POINTS = {
            "over_60": 0,
            "30_to_60": 1,
            "under_30": 2
        }
        
        # Risk factor points (each worth 1 point if present)
        self.RISK_FACTORS = [
            "underweight",
            "stroke_tia_embolism_history",
            "diabetes",
            "hypertension",
            "antiplatelet_use",
            "nsaid_use", 
            "bleeding_history",
            "liver_disease"
        ]
    
    def calculate(self, age_category: str, creatinine_clearance_category: str,
                  underweight: str, stroke_tia_embolism_history: str, diabetes: str,
                  hypertension: str, antiplatelet_use: str, nsaid_use: str,
                  bleeding_history: str, liver_disease: str) -> Dict[str, Any]:
        """
        Calculates the DOAC score
        
        Args:
            age_category (str): Age category (under_65, 65_to_69, 70_to_74, 75_to_79, 80_or_over)
            creatinine_clearance_category (str): Creatinine clearance (over_60, 30_to_60, under_30)
            underweight (str): BMI <18.5 kg/m² (yes/no)
            stroke_tia_embolism_history (str): History of stroke/TIA/embolism (yes/no)
            diabetes (str): Diabetes mellitus (yes/no)
            hypertension (str): Hypertension (yes/no)
            antiplatelet_use (str): Current antiplatelet use (yes/no)
            nsaid_use (str): Current NSAID use (yes/no)
            bleeding_history (str): History of major bleeding (yes/no)
            liver_disease (str): Liver disease (yes/no)
            
        Returns:
            Dict with the result and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(age_category, creatinine_clearance_category,
                             underweight, stroke_tia_embolism_history, diabetes,
                             hypertension, antiplatelet_use, nsaid_use,
                             bleeding_history, liver_disease)
        
        # Calculate age points
        age_points = self.AGE_POINTS[age_category]
        
        # Calculate creatinine clearance points
        creatinine_points = self.CREATININE_POINTS[creatinine_clearance_category]
        
        # Calculate risk factor points
        risk_factor_points = 0
        risk_factors = {
            "underweight": underweight,
            "stroke_tia_embolism_history": stroke_tia_embolism_history,
            "diabetes": diabetes,
            "hypertension": hypertension,
            "antiplatelet_use": antiplatelet_use,
            "nsaid_use": nsaid_use,
            "bleeding_history": bleeding_history,
            "liver_disease": liver_disease
        }
        
        for factor in self.RISK_FACTORS:
            if risk_factors[factor] == "yes":
                risk_factor_points += 1
        
        # Calculate total score (capped at 10)
        total_score = min(age_points + creatinine_points + risk_factor_points, 10)
        
        # Get interpretation
        interpretation = self._get_interpretation(total_score)
        
        return {
            "result": total_score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation.get("stage", ""),
            "stage_description": interpretation.get("description", "")
        }
    
    def _validate_inputs(self, age_category: str, creatinine_clearance_category: str,
                        underweight: str, stroke_tia_embolism_history: str, diabetes: str,
                        hypertension: str, antiplatelet_use: str, nsaid_use: str,
                        bleeding_history: str, liver_disease: str):
        """Validates input parameters"""
        
        # Validate age category
        if age_category not in self.AGE_POINTS:
            raise ValueError(f"Invalid age_category: {age_category}")
        
        # Validate creatinine clearance category
        if creatinine_clearance_category not in self.CREATININE_POINTS:
            raise ValueError(f"Invalid creatinine_clearance_category: {creatinine_clearance_category}")
        
        # Validate yes/no parameters
        yes_no_params = {
            "underweight": underweight,
            "stroke_tia_embolism_history": stroke_tia_embolism_history,
            "diabetes": diabetes,
            "hypertension": hypertension,
            "antiplatelet_use": antiplatelet_use,
            "nsaid_use": nsaid_use,
            "bleeding_history": bleeding_history,
            "liver_disease": liver_disease
        }
        
        for param_name, param_value in yes_no_params.items():
            if param_value not in ["yes", "no"]:
                raise ValueError(f"{param_name} must be 'yes' or 'no'")
    
    def _get_interpretation(self, score: int) -> Dict[str, str]:
        """
        Determines the interpretation based on the score
        
        Args:
            score (int): Total DOAC score (0-10)
            
        Returns:
            Dict with interpretation
        """
        
        if score <= 3:
            return {
                "stage": "Very Low",
                "description": "Very low bleeding risk",
                "interpretation": "Very low bleeding risk. Patient may continue DOAC therapy with standard monitoring. Annual bleeding rate approximately 0.3-0.8%."
            }
        elif score <= 5:
            return {
                "stage": "Low", 
                "description": "Low bleeding risk",
                "interpretation": "Low bleeding risk. Patient may continue DOAC therapy with standard monitoring. Annual bleeding rate approximately 1.1-1.9%."
            }
        elif score <= 7:
            return {
                "stage": "Moderate",
                "description": "Moderate bleeding risk",
                "interpretation": "Moderate bleeding risk. Consider more frequent monitoring and bleeding risk reduction strategies. Annual bleeding rate approximately 2.5-4.1%."
            }
        elif score <= 9:
            return {
                "stage": "High",
                "description": "High bleeding risk",
                "interpretation": "High bleeding risk. Consider bleeding risk reduction strategies, more frequent monitoring, and evaluate risk-benefit ratio. Annual bleeding rate approximately 5.2-8.1%."
            }
        else:  # score == 10
            return {
                "stage": "Very High",
                "description": "Very high bleeding risk",
                "interpretation": "Very high bleeding risk. Careful evaluation of risk-benefit ratio required. Consider bleeding risk reduction strategies and frequent monitoring. Annual bleeding rate approximately 10.8%."
            }


def calculate_doac_score(age_category: str, creatinine_clearance_category: str,
                        underweight: str, stroke_tia_embolism_history: str, diabetes: str,
                        hypertension: str, antiplatelet_use: str, nsaid_use: str,
                        bleeding_history: str, liver_disease: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = DoacScoreCalculator()
    return calculator.calculate(age_category, creatinine_clearance_category,
                               underweight, stroke_tia_embolism_history, diabetes,
                               hypertension, antiplatelet_use, nsaid_use,
                               bleeding_history, liver_disease)