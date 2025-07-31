"""
VACO Index COVID-19 Mortality Risk Calculator

Estimates 30-day mortality risk after COVID-19 infection using pre-existing health conditions 
and demographics. Developed by researchers from Yale University and VA Connecticut Healthcare 
System in collaboration with the US Department of Health and Human Services.

References:
1. Justice AC, Freiburg MS, Lopez-Class M, et al. Patient-facing COVID-19 risk tool. 
   Developed in collaboration with US Department of Health and Human Services. 
   Yale University and VA Connecticut Healthcare System; 2020.
2. King JT Jr, Yoon JS, Rentsch CT, et al. Development and validation of a 30-day mortality 
   index based on pre-existing medical administrative data from 13,323 COVID-19 patients: 
   The Veterans Health Administration COVID-19 (VACO) Index. PLoS One. 2020;15(11):e0241825.
3. Rentsch CT, Kidwai-Khan F, Tate JP, et al. Patterns of COVID-19 testing and mortality 
   by race and ethnicity among United States veterans: A nationwide cohort study. 
   PLoS Med. 2020;17(9):e1003379.
"""

import math
from typing import Dict, Any


class VacoIndexCovid19Calculator:
    """Calculator for VACO Index COVID-19 Mortality Risk"""
    
    def __init__(self):
        # Age coefficients from the VACO Index model
        self.AGE_COEFFICIENTS = {
            (20, 49): -2.228678713,
            (50, 54): 0.0,
            (55, 59): 0.400599289,
            (60, 64): 0.941322019,
            (65, 69): 1.295007128,
            (70, 74): 1.629533438,
            (75, 79): 1.763345763,
            (80, 89): 1.927443543,
            (90, 115): 2.018752269
        }
        
        # Sex coefficient
        self.SEX_COEFFICIENTS = {
            "female": 0.0,
            "male": 0.322291449
        }
        
        # Charlson Comorbidity Index points for each condition
        self.COMORBIDITY_POINTS = {
            "diabetes": {"none": 0, "uncomplicated": 1, "complicated": 2},
            "chronic_pulmonary_disease": {"no": 0, "yes": 1},
            "renal_disease": {"none": 0, "mild_moderate": 1, "severe": 2},
            "peripheral_vascular_disease": {"no": 0, "yes": 1},
            "congestive_heart_failure": {"no": 0, "yes": 1},
            "dementia": {"no": 0, "yes": 1},
            "cancer": {"none": 0, "localized_solid": 2, "metastatic_solid": 6, "leukemia": 2, "lymphoma": 2},
            "cerebrovascular_accident": {"no": 0, "yes": 1},
            "liver_disease": {"none": 0, "mild": 1, "moderate_severe": 3},
            "myocardial_infarction": {"no": 0, "yes": 1},
            "peptic_ulcer_disease": {"no": 0, "yes": 1},
            "paralysis": {"no": 0, "yes": 2},
            "aids": {"no": 0, "yes": 6},
            "rheumatologic_disease": {"no": 0, "yes": 1}
        }
        
        # Base coefficient for the model
        self.BASE_COEFFICIENT = -5.645
        
        # CCI coefficient
        self.CCI_COEFFICIENT = 0.254
    
    def calculate(self, age: int, sex: str, diabetes: str, chronic_pulmonary_disease: str,
                  renal_disease: str, peripheral_vascular_disease: str, congestive_heart_failure: str,
                  dementia: str, cancer: str, cerebrovascular_accident: str, liver_disease: str,
                  myocardial_infarction: str, peptic_ulcer_disease: str, paralysis: str,
                  aids: str, rheumatologic_disease: str) -> Dict[str, Any]:
        """
        Calculates the VACO Index COVID-19 mortality risk
        
        Args:
            age (int): Patient age in years (20-115)
            sex (str): Patient biological sex ("female" or "male")
            diabetes (str): Diabetes status ("none", "uncomplicated", "complicated")
            chronic_pulmonary_disease (str): Chronic pulmonary disease ("no", "yes")
            renal_disease (str): Renal disease status ("none", "mild_moderate", "severe")
            peripheral_vascular_disease (str): Peripheral vascular disease ("no", "yes")
            congestive_heart_failure (str): Congestive heart failure ("no", "yes")
            dementia (str): Dementia status ("no", "yes")
            cancer (str): Cancer status ("none", "localized_solid", "metastatic_solid", "leukemia", "lymphoma")
            cerebrovascular_accident (str): Stroke history ("no", "yes")
            liver_disease (str): Liver disease status ("none", "mild", "moderate_severe")
            myocardial_infarction (str): MI history ("no", "yes")
            peptic_ulcer_disease (str): Peptic ulcer disease ("no", "yes")
            paralysis (str): Paralysis status ("no", "yes")
            aids (str): AIDS/HIV status ("no", "yes")
            rheumatologic_disease (str): Rheumatologic disease ("no", "yes")
            
        Returns:
            Dict with the mortality risk percentage and interpretation
        """
        
        # Validations
        self._validate_inputs(age, sex, diabetes, chronic_pulmonary_disease, renal_disease,
                            peripheral_vascular_disease, congestive_heart_failure, dementia,
                            cancer, cerebrovascular_accident, liver_disease, myocardial_infarction,
                            peptic_ulcer_disease, paralysis, aids, rheumatologic_disease)
        
        # Calculate risk
        risk_percentage = self._calculate_risk(age, sex, diabetes, chronic_pulmonary_disease,
                                             renal_disease, peripheral_vascular_disease,
                                             congestive_heart_failure, dementia, cancer,
                                             cerebrovascular_accident, liver_disease,
                                             myocardial_infarction, peptic_ulcer_disease,
                                             paralysis, aids, rheumatologic_disease)
        
        # Get interpretation
        interpretation_data = self._get_interpretation(risk_percentage)
        
        return {
            "result": risk_percentage,
            "unit": "percentage",
            "interpretation": interpretation_data["interpretation"],
            "stage": interpretation_data["stage"],
            "stage_description": interpretation_data["description"]
        }
    
    def _validate_inputs(self, age: int, sex: str, diabetes: str, chronic_pulmonary_disease: str,
                        renal_disease: str, peripheral_vascular_disease: str, congestive_heart_failure: str,
                        dementia: str, cancer: str, cerebrovascular_accident: str, liver_disease: str,
                        myocardial_infarction: str, peptic_ulcer_disease: str, paralysis: str,
                        aids: str, rheumatologic_disease: str):
        """Validates input parameters"""
        
        # Validate age
        if not isinstance(age, int) or age < 20 or age > 115:
            raise ValueError("Age must be an integer between 20 and 115 years")
        
        # Validate sex
        if sex not in ["female", "male"]:
            raise ValueError("Sex must be 'female' or 'male'")
        
        # Validate comorbidity parameters
        comorbidity_params = {
            "diabetes": diabetes,
            "chronic_pulmonary_disease": chronic_pulmonary_disease,
            "renal_disease": renal_disease,
            "peripheral_vascular_disease": peripheral_vascular_disease,
            "congestive_heart_failure": congestive_heart_failure,
            "dementia": dementia,
            "cancer": cancer,
            "cerebrovascular_accident": cerebrovascular_accident,
            "liver_disease": liver_disease,
            "myocardial_infarction": myocardial_infarction,
            "peptic_ulcer_disease": peptic_ulcer_disease,
            "paralysis": paralysis,
            "aids": aids,
            "rheumatologic_disease": rheumatologic_disease
        }
        
        for param_name, param_value in comorbidity_params.items():
            valid_options = list(self.COMORBIDITY_POINTS[param_name].keys())
            if param_value not in valid_options:
                raise ValueError(f"{param_name} must be one of: {valid_options}")
    
    def _get_age_coefficient(self, age: int) -> float:
        """Gets the age coefficient based on age range"""
        for (min_age, max_age), coefficient in self.AGE_COEFFICIENTS.items():
            if min_age <= age <= max_age:
                return coefficient
        
        # Fallback for ages not in ranges (shouldn't happen with validation)
        return 0.0
    
    def _calculate_cci_score(self, diabetes: str, chronic_pulmonary_disease: str, renal_disease: str,
                            peripheral_vascular_disease: str, congestive_heart_failure: str, dementia: str,
                            cancer: str, cerebrovascular_accident: str, liver_disease: str,
                            myocardial_infarction: str, peptic_ulcer_disease: str, paralysis: str,
                            aids: str, rheumatologic_disease: str) -> int:
        """Calculates the Charlson Comorbidity Index score"""
        
        cci_score = 0
        
        # Sum up all comorbidity points
        cci_score += self.COMORBIDITY_POINTS["diabetes"][diabetes]
        cci_score += self.COMORBIDITY_POINTS["chronic_pulmonary_disease"][chronic_pulmonary_disease]
        cci_score += self.COMORBIDITY_POINTS["renal_disease"][renal_disease]
        cci_score += self.COMORBIDITY_POINTS["peripheral_vascular_disease"][peripheral_vascular_disease]
        cci_score += self.COMORBIDITY_POINTS["congestive_heart_failure"][congestive_heart_failure]
        cci_score += self.COMORBIDITY_POINTS["dementia"][dementia]
        cci_score += self.COMORBIDITY_POINTS["cancer"][cancer]
        cci_score += self.COMORBIDITY_POINTS["cerebrovascular_accident"][cerebrovascular_accident]
        cci_score += self.COMORBIDITY_POINTS["liver_disease"][liver_disease]
        cci_score += self.COMORBIDITY_POINTS["myocardial_infarction"][myocardial_infarction]
        cci_score += self.COMORBIDITY_POINTS["peptic_ulcer_disease"][peptic_ulcer_disease]
        cci_score += self.COMORBIDITY_POINTS["paralysis"][paralysis]
        cci_score += self.COMORBIDITY_POINTS["aids"][aids]
        cci_score += self.COMORBIDITY_POINTS["rheumatologic_disease"][rheumatologic_disease]
        
        return cci_score
    
    def _calculate_risk(self, age: int, sex: str, diabetes: str, chronic_pulmonary_disease: str,
                       renal_disease: str, peripheral_vascular_disease: str, congestive_heart_failure: str,
                       dementia: str, cancer: str, cerebrovascular_accident: str, liver_disease: str,
                       myocardial_infarction: str, peptic_ulcer_disease: str, paralysis: str,
                       aids: str, rheumatologic_disease: str) -> float:
        """Calculates the mortality risk percentage using the VACO Index model"""
        
        # Get age coefficient
        age_coeff = self._get_age_coefficient(age)
        
        # Get sex coefficient
        sex_coeff = self.SEX_COEFFICIENTS[sex]
        
        # Calculate CCI score
        cci_score = self._calculate_cci_score(diabetes, chronic_pulmonary_disease, renal_disease,
                                            peripheral_vascular_disease, congestive_heart_failure,
                                            dementia, cancer, cerebrovascular_accident, liver_disease,
                                            myocardial_infarction, peptic_ulcer_disease, paralysis,
                                            aids, rheumatologic_disease)
        
        # Calculate coefficient sum
        coefficient_sum = (self.BASE_COEFFICIENT + age_coeff + sex_coeff + 
                          (self.CCI_COEFFICIENT * cci_score))
        
        # Calculate odds ratio and risk
        odds_ratio = math.exp(coefficient_sum)
        risk = odds_ratio / (1 + odds_ratio)
        
        # Convert to percentage and round to 1 decimal place
        risk_percentage = round(risk * 100, 1)
        
        return risk_percentage
    
    def _get_interpretation(self, risk_percentage: float) -> Dict[str, str]:
        """
        Determines the interpretation based on the risk percentage
        
        Args:
            risk_percentage (float): Calculated mortality risk percentage
            
        Returns:
            Dict with interpretation details
        """
        
        if risk_percentage <= 8.7:
            return {
                "stage": "Lower Risk",
                "description": "Lower risk of 30-day mortality",
                "interpretation": (f"Lower risk ({risk_percentage}%) of death within 30 days of COVID-19 infection. "
                                f"Continue standard preventive measures and consult healthcare provider if symptoms develop.")
            }
        elif risk_percentage <= 16.0:
            return {
                "stage": "Moderate Risk",
                "description": "Moderate risk of 30-day mortality",
                "interpretation": (f"Moderate risk ({risk_percentage}%) of death within 30 days of COVID-19 infection. "
                                f"Enhanced preventive measures recommended. Seek medical attention promptly if COVID-19 symptoms develop.")
            }
        elif risk_percentage <= 21.2:
            return {
                "stage": "High Risk",
                "description": "High risk of 30-day mortality",
                "interpretation": (f"High risk ({risk_percentage}%) of death within 30 days of COVID-19 infection. "
                                f"Strict preventive measures strongly recommended. Consider discussing additional protective strategies with healthcare provider.")
            }
        else:
            return {
                "stage": "Extreme Risk",
                "description": "Extreme risk of 30-day mortality",
                "interpretation": (f"Extreme risk ({risk_percentage}%) of death within 30 days of COVID-19 infection. "
                                f"Maximum preventive measures essential. Immediate medical consultation recommended for risk mitigation strategies.")
            }


def calculate_vaco_index_covid19(age: int, sex: str, diabetes: str, chronic_pulmonary_disease: str,
                                renal_disease: str, peripheral_vascular_disease: str, 
                                congestive_heart_failure: str, dementia: str, cancer: str,
                                cerebrovascular_accident: str, liver_disease: str,
                                myocardial_infarction: str, peptic_ulcer_disease: str,
                                paralysis: str, aids: str, rheumatologic_disease: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_vaco_index_covid19 pattern
    """
    calculator = VacoIndexCovid19Calculator()
    return calculator.calculate(age, sex, diabetes, chronic_pulmonary_disease, renal_disease,
                               peripheral_vascular_disease, congestive_heart_failure, dementia,
                               cancer, cerebrovascular_accident, liver_disease, myocardial_infarction,
                               peptic_ulcer_disease, paralysis, aids, rheumatologic_disease)