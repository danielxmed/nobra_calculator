"""
COVID-GRAM Critical Illness Risk Score Calculator

Predicts risk of critical illness (ICU admission, mechanical ventilation, or death) 
in hospitalized COVID-19 patients using 10 clinical variables available at admission.

References:
1. Liang W, Liang H, Ou L, Chen B, Chen A, Li C, et al. Development and Validation 
   of a Clinical Risk Score to Predict the Occurrence of Critical Illness in 
   Hospitalized Patients With COVID-19. JAMA Intern Med. 2020;180(8):1081-1089. 
   doi:10.1001/jamainternmed.2020.2033
"""

import math
from typing import Dict, Any


class CovidGramCriticalIllnessCalculator:
    """Calculator for COVID-GRAM Critical Illness Risk Score"""
    
    def __init__(self):
        # Coefficients from the original COVID-GRAM model
        self.COEFFICIENTS = {
            "chest_xray_abnormality": 27.1464,
            "age": 0.6139,
            "hemoptysis": 33.6210,
            "dyspnea": 14.0569,
            "unconsciousness": 34.4617,
            "number_of_comorbidities": 10.3826,
            "cancer_history": 31.2211,
            "neutrophil_lymphocyte_ratio": 1.25,
            "lactate_dehydrogenase": 0.0534,
            "direct_bilirubin": 3.0605
        }
        
        # Intercept for logistic regression
        self.INTERCEPT = -146.5
        
        # Risk thresholds
        self.LOW_RISK_THRESHOLD = 1.7
        self.HIGH_RISK_THRESHOLD = 40.4
    
    def calculate(
        self,
        chest_xray_abnormality: str,
        age: int,
        hemoptysis: str,
        dyspnea: str,
        unconsciousness: str,
        number_of_comorbidities: int,
        cancer_history: str,
        neutrophil_lymphocyte_ratio: float,
        lactate_dehydrogenase: float,
        direct_bilirubin: float
    ) -> Dict[str, Any]:
        """
        Calculates the COVID-GRAM Critical Illness Risk Score
        
        Args:
            chest_xray_abnormality: Chest X-ray abnormality present (yes/no)
            age: Patient age in years
            hemoptysis: Presence of hemoptysis (yes/no)
            dyspnea: Presence of dyspnea (yes/no)
            unconsciousness: Presence of unconsciousness (yes/no)
            number_of_comorbidities: Number of comorbidities (0-10)
            cancer_history: History of cancer (yes/no)
            neutrophil_lymphocyte_ratio: Neutrophil to lymphocyte ratio
            lactate_dehydrogenase: LDH level in U/L
            direct_bilirubin: Direct bilirubin level in mg/dL
            
        Returns:
            Dict with risk probability and clinical interpretation
        """
        
        # Validate inputs
        self._validate_inputs(
            chest_xray_abnormality, age, hemoptysis, dyspnea, unconsciousness,
            number_of_comorbidities, cancer_history, neutrophil_lymphocyte_ratio,
            lactate_dehydrogenase, direct_bilirubin
        )
        
        # Calculate the linear predictor (logit)
        linear_predictor = self._calculate_linear_predictor(
            chest_xray_abnormality, age, hemoptysis, dyspnea, unconsciousness,
            number_of_comorbidities, cancer_history, neutrophil_lymphocyte_ratio,
            lactate_dehydrogenase, direct_bilirubin
        )
        
        # Convert to probability using logistic function
        risk_probability = self._calculate_probability(linear_predictor)
        
        # Get clinical interpretation
        interpretation = self._get_interpretation(risk_probability)
        
        return {
            "result": round(risk_probability, 1),
            "unit": "%",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"],
            "calculation_details": {
                "linear_predictor": round(linear_predictor, 2),
                "risk_factors_present": interpretation["risk_factors"],
                "clinical_recommendations": interpretation["recommendations"],
                "monitoring_level": interpretation["monitoring"],
                "critical_illness_components": [
                    "ICU admission requirement",
                    "Invasive mechanical ventilation",
                    "Death"
                ]
            }
        }
    
    def _validate_inputs(
        self, chest_xray_abnormality, age, hemoptysis, dyspnea, unconsciousness,
        number_of_comorbidities, cancer_history, neutrophil_lymphocyte_ratio,
        lactate_dehydrogenase, direct_bilirubin
    ):
        """Validates input parameters"""
        
        # Validate age
        if not isinstance(age, int) or age < 18 or age > 120:
            raise ValueError("Age must be between 18 and 120 years")
        
        # Validate yes/no parameters
        valid_yes_no = ["yes", "no"]
        yes_no_params = {
            "chest_xray_abnormality": chest_xray_abnormality,
            "hemoptysis": hemoptysis,
            "dyspnea": dyspnea,
            "unconsciousness": unconsciousness,
            "cancer_history": cancer_history
        }
        
        for param_name, param_value in yes_no_params.items():
            if param_value not in valid_yes_no:
                raise ValueError(f"{param_name} must be 'yes' or 'no'")
        
        # Validate number of comorbidities
        if not isinstance(number_of_comorbidities, int) or number_of_comorbidities < 0 or number_of_comorbidities > 10:
            raise ValueError("Number of comorbidities must be between 0 and 10")
        
        # Validate continuous parameters
        if not isinstance(neutrophil_lymphocyte_ratio, (int, float)) or neutrophil_lymphocyte_ratio < 0.5 or neutrophil_lymphocyte_ratio > 50.0:
            raise ValueError("Neutrophil-lymphocyte ratio must be between 0.5 and 50.0")
        
        if not isinstance(lactate_dehydrogenase, (int, float)) or lactate_dehydrogenase < 100.0 or lactate_dehydrogenase > 2000.0:
            raise ValueError("Lactate dehydrogenase must be between 100.0 and 2000.0 U/L")
        
        if not isinstance(direct_bilirubin, (int, float)) or direct_bilirubin < 0.1 or direct_bilirubin > 20.0:
            raise ValueError("Direct bilirubin must be between 0.1 and 20.0 mg/dL")
    
    def _calculate_linear_predictor(
        self, chest_xray_abnormality, age, hemoptysis, dyspnea, unconsciousness,
        number_of_comorbidities, cancer_history, neutrophil_lymphocyte_ratio,
        lactate_dehydrogenase, direct_bilirubin
    ) -> float:
        """Calculate the linear predictor for the logistic regression model"""
        
        # Convert binary variables to numeric
        xray_score = 1 if chest_xray_abnormality == "yes" else 0
        hemoptysis_score = 1 if hemoptysis == "yes" else 0
        dyspnea_score = 1 if dyspnea == "yes" else 0
        unconsciousness_score = 1 if unconsciousness == "yes" else 0
        cancer_score = 1 if cancer_history == "yes" else 0
        
        # Calculate weighted sum
        linear_predictor = (
            self.INTERCEPT +
            (xray_score * self.COEFFICIENTS["chest_xray_abnormality"]) +
            (age * self.COEFFICIENTS["age"]) +
            (hemoptysis_score * self.COEFFICIENTS["hemoptysis"]) +
            (dyspnea_score * self.COEFFICIENTS["dyspnea"]) +
            (unconsciousness_score * self.COEFFICIENTS["unconsciousness"]) +
            (number_of_comorbidities * self.COEFFICIENTS["number_of_comorbidities"]) +
            (cancer_score * self.COEFFICIENTS["cancer_history"]) +
            (neutrophil_lymphocyte_ratio * self.COEFFICIENTS["neutrophil_lymphocyte_ratio"]) +
            (lactate_dehydrogenase * self.COEFFICIENTS["lactate_dehydrogenase"]) +
            (direct_bilirubin * self.COEFFICIENTS["direct_bilirubin"])
        )
        
        return linear_predictor
    
    def _calculate_probability(self, linear_predictor: float) -> float:
        """Convert linear predictor to probability using logistic function"""
        try:
            # Logistic function: p = e^x / (1 + e^x) = 1 / (1 + e^(-x))
            probability = 1 / (1 + math.exp(-linear_predictor))
            
            # Convert to percentage and ensure reasonable bounds
            probability_percent = probability * 100
            return max(0.1, min(99.9, probability_percent))
            
        except OverflowError:
            # Handle extreme values
            if linear_predictor > 0:
                return 99.9
            else:
                return 0.1
    
    def _get_interpretation(self, risk_probability: float) -> Dict[str, Any]:
        """
        Determines the interpretation based on COVID-GRAM risk probability
        
        Args:
            risk_probability: Calculated risk probability percentage
            
        Returns:
            Dict with interpretation details
        """
        
        if risk_probability < self.LOW_RISK_THRESHOLD:
            stage = "Low Risk"
            description = "Low risk of critical illness"
            recommendations = "Standard monitoring and care"
            monitoring = "Standard ward-level monitoring"
            risk_factors = "Few high-risk factors for critical illness"
            
            interpretation = (
                f"COVID-GRAM risk probability of {risk_probability:.1f}% indicates low risk "
                f"for critical illness. Standard monitoring and care protocols are appropriate. "
                f"Low probability of requiring ICU admission, mechanical ventilation, or death."
            )
            
        elif risk_probability < self.HIGH_RISK_THRESHOLD:
            stage = "Medium Risk"
            description = "Medium risk of critical illness"
            recommendations = "Enhanced monitoring with close observation"
            monitoring = "Enhanced monitoring with frequent assessments"
            risk_factors = "Moderate risk factors for critical illness"
            
            interpretation = (
                f"COVID-GRAM risk probability of {risk_probability:.1f}% indicates medium risk "
                f"for critical illness. Enhanced monitoring and close observation are recommended. "
                f"Intermediate probability of requiring ICU admission, mechanical ventilation, or death."
            )
            
        else:
            stage = "High Risk"
            description = "High risk of critical illness"
            recommendations = "Intensive monitoring and ICU consideration"
            monitoring = "Intensive monitoring with ICU readiness"
            risk_factors = "Multiple high-risk factors for critical illness"
            
            interpretation = (
                f"COVID-GRAM risk probability of {risk_probability:.1f}% indicates high risk "
                f"for critical illness. Intensive monitoring and ICU consideration are recommended. "
                f"High probability of requiring ICU admission, mechanical ventilation, or death."
            )
        
        return {
            "stage": stage,
            "description": description,
            "interpretation": interpretation,
            "risk_factors": risk_factors,
            "recommendations": recommendations,
            "monitoring": monitoring
        }


def calculate_covid_gram_critical_illness(
    chest_xray_abnormality: str,
    age: int,
    hemoptysis: str,
    dyspnea: str,
    unconsciousness: str,
    number_of_comorbidities: int,
    cancer_history: str,
    neutrophil_lymphocyte_ratio: float,
    lactate_dehydrogenase: float,
    direct_bilirubin: float
) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = CovidGramCriticalIllnessCalculator()
    return calculator.calculate(
        chest_xray_abnormality=chest_xray_abnormality,
        age=age,
        hemoptysis=hemoptysis,
        dyspnea=dyspnea,
        unconsciousness=unconsciousness,
        number_of_comorbidities=number_of_comorbidities,
        cancer_history=cancer_history,
        neutrophil_lymphocyte_ratio=neutrophil_lymphocyte_ratio,
        lactate_dehydrogenase=lactate_dehydrogenase,
        direct_bilirubin=direct_bilirubin
    )