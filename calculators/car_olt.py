"""
Cardiovascular Risk in Orthotopic Liver Transplantation (CAR-OLT) Calculator

Predicts cardiovascular risk in orthotopic liver transplantation patients.
The CAR-OLT score predicts the 1-year risk for death or hospitalization related 
to a major CVD event after liver transplantation.

References:
1. VanWagner LB, et al. A point-based prediction model for cardiovascular risk 
   in orthotopic liver transplantation: The CAR-OLT score. Hepatology. 2017;66(6):1968-1979.
2. VanWagner LB, et al. Factors Associated With Major Adverse Cardiovascular Events 
   After Liver Transplantation Among a National Sample. Am J Transplant. 2016;16(9):2684-94.
"""

from typing import Dict, Any


class CarOltCalculator:
    """Calculator for Cardiovascular Risk in Orthotopic Liver Transplantation (CAR-OLT)"""
    
    def __init__(self):
        # Define point values for each parameter
        self.age_points = {
            "under_45": 0,
            "45_to_49": -6,
            "50_to_54": -4,
            "55_to_59": 2,
            "60_to_64": 5,
            "65_or_over": 8
        }
        
        self.sex_points = {
            "male": 0,
            "female": 1
        }
        
        self.race_points = {
            "other": 0,
            "white": 7,
            "black": 10
        }
        
        self.working_points = {
            "yes": 0,  # Working for income
            "no": 10   # Not working for income
        }
        
        self.education_points = {
            "college_or_higher": 0,
            "high_school_or_less_unknown": 5
        }
        
        self.binary_conditions = {
            "atrial_fibrillation": {"yes": 25, "no": 0},
            "respiratory_failure_ventilator": {"yes": 13, "no": 0},
            "pulmonary_hypertension": {"yes": 9, "no": 0},
            "hepatocellular_carcinoma": {"yes": 0, "no": 6},  # Note: HCC presence gives 0 points, absence gives 6
            "hypertension": {"yes": 4, "no": 0},
            "diabetes": {"yes": 4, "no": 0},
            "heart_failure": {"yes": 7, "no": 0}
        }
    
    def calculate(self, age_category: str, sex: str, race: str, working_status: str,
                  education: str, atrial_fibrillation: str, respiratory_failure_ventilator: str,
                  pulmonary_hypertension: str, hepatocellular_carcinoma: str,
                  hypertension: str, diabetes: str, heart_failure: str) -> Dict[str, Any]:
        """
        Calculates the CAR-OLT score
        
        Args:
            age_category: Age category at transplant
            sex: Patient sex
            race: Patient race
            working_status: Employment status
            education: Education level
            atrial_fibrillation: History of atrial fibrillation
            respiratory_failure_ventilator: Respiratory failure on ventilator
            pulmonary_hypertension: Presence of pulmonary hypertension
            hepatocellular_carcinoma: Presence of HCC
            hypertension: History of hypertension
            diabetes: History of diabetes
            heart_failure: History of heart failure
            
        Returns:
            Dict with the result and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(age_category, sex, race, working_status, education,
                            atrial_fibrillation, respiratory_failure_ventilator,
                            pulmonary_hypertension, hepatocellular_carcinoma,
                            hypertension, diabetes, heart_failure)
        
        # Calculate total score
        total_score = 0
        
        # Add age points
        total_score += self.age_points[age_category]
        
        # Add sex points
        total_score += self.sex_points[sex]
        
        # Add race points
        total_score += self.race_points[race]
        
        # Add working status points
        total_score += self.working_points[working_status]
        
        # Add education points
        total_score += self.education_points[education]
        
        # Add points for binary conditions
        total_score += self.binary_conditions["atrial_fibrillation"][atrial_fibrillation]
        total_score += self.binary_conditions["respiratory_failure_ventilator"][respiratory_failure_ventilator]
        total_score += self.binary_conditions["pulmonary_hypertension"][pulmonary_hypertension]
        total_score += self.binary_conditions["hepatocellular_carcinoma"][hepatocellular_carcinoma]
        total_score += self.binary_conditions["hypertension"][hypertension]
        total_score += self.binary_conditions["diabetes"][diabetes]
        total_score += self.binary_conditions["heart_failure"][heart_failure]
        
        # Get interpretation
        interpretation = self._get_interpretation(total_score)
        
        return {
            "result": total_score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["risk_category"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, age_category: str, sex: str, race: str, working_status: str,
                        education: str, atrial_fibrillation: str, respiratory_failure_ventilator: str,
                        pulmonary_hypertension: str, hepatocellular_carcinoma: str,
                        hypertension: str, diabetes: str, heart_failure: str):
        """Validates input parameters"""
        
        if age_category not in self.age_points:
            raise ValueError(f"Invalid age category: {age_category}")
        
        if sex not in self.sex_points:
            raise ValueError(f"Invalid sex: {sex}")
        
        if race not in self.race_points:
            raise ValueError(f"Invalid race: {race}")
        
        if working_status not in self.working_points:
            raise ValueError(f"Invalid working status: {working_status}")
        
        if education not in self.education_points:
            raise ValueError(f"Invalid education level: {education}")
        
        # Validate binary conditions
        binary_params = {
            "atrial_fibrillation": atrial_fibrillation,
            "respiratory_failure_ventilator": respiratory_failure_ventilator,
            "pulmonary_hypertension": pulmonary_hypertension,
            "hepatocellular_carcinoma": hepatocellular_carcinoma,
            "hypertension": hypertension,
            "diabetes": diabetes,
            "heart_failure": heart_failure
        }
        
        for param_name, param_value in binary_params.items():
            if param_value not in ["yes", "no"]:
                raise ValueError(f"{param_name} must be 'yes' or 'no', got: {param_value}")
    
    def _get_interpretation(self, score: int) -> Dict[str, str]:
        """
        Determines the interpretation based on the CAR-OLT score
        
        Args:
            score (int): Calculated CAR-OLT score
            
        Returns:
            Dict with interpretation
        """
        
        if score < 10:
            return {
                "risk_category": "Very Low",
                "description": "Very low cardiovascular risk",
                "interpretation": "Less than 5% 1-year risk of death or hospitalization related to a major cardiovascular event (MI, cardiac revascularization, heart failure, atrial fibrillation, cardiac arrest, pulmonary embolism, or stroke) after liver transplantation"
            }
        elif score <= 12:
            return {
                "risk_category": "Low",
                "description": "Low cardiovascular risk",
                "interpretation": "6-8% 1-year risk of death or hospitalization related to a major cardiovascular event (MI, cardiac revascularization, heart failure, atrial fibrillation, cardiac arrest, pulmonary embolism, or stroke) after liver transplantation"
            }
        elif score <= 15:
            return {
                "risk_category": "Low",
                "description": "Low cardiovascular risk",
                "interpretation": "8% 1-year risk of death or hospitalization related to a major cardiovascular event (MI, cardiac revascularization, heart failure, atrial fibrillation, cardiac arrest, pulmonary embolism, or stroke) after liver transplantation"
            }
        elif score <= 30:
            return {
                "risk_category": "Moderate",
                "description": "Moderate cardiovascular risk",
                "interpretation": "10-26% 1-year risk of death or hospitalization related to a major cardiovascular event (MI, cardiac revascularization, heart failure, atrial fibrillation, cardiac arrest, pulmonary embolism, or stroke) after liver transplantation"
            }
        elif score <= 36:
            return {
                "risk_category": "High",
                "description": "High cardiovascular risk",
                "interpretation": "30-38% 1-year risk of death or hospitalization related to a major cardiovascular event (MI, cardiac revascularization, heart failure, atrial fibrillation, cardiac arrest, pulmonary embolism, or stroke) after liver transplantation"
            }
        else:
            return {
                "risk_category": "Very High",
                "description": "Very high cardiovascular risk",
                "interpretation": "≥40% 1-year risk of death or hospitalization related to a major cardiovascular event (MI, cardiac revascularization, heart failure, atrial fibrillation, cardiac arrest, pulmonary embolism, or stroke) after liver transplantation"
            }


def calculate_car_olt(age_category: str, sex: str, race: str, working_status: str,
                     education: str, atrial_fibrillation: str, respiratory_failure_ventilator: str,
                     pulmonary_hypertension: str, hepatocellular_carcinoma: str,
                     hypertension: str, diabetes: str, heart_failure: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = CarOltCalculator()
    return calculator.calculate(age_category, sex, race, working_status, education,
                               atrial_fibrillation, respiratory_failure_ventilator,
                               pulmonary_hypertension, hepatocellular_carcinoma,
                               hypertension, diabetes, heart_failure)