"""
International Diabetes Federation-Diabetes and Ramadan Alliance (IDF-DAR) Fasting Risk Assessment Calculator

Stratifies risk of fasting during Ramadan in diabetic patients using validated clinical parameters.

References (Vancouver style):
1. Hassanein M, Sahay BK, Hafidh K, Djaballah K, Li H, Rahim MA, et al. Diabetes and Ramadan: 
   Practical guidelines 2021. Diabetes Res Clin Pract. 2022 Mar;185:109185. doi: 10.1016/j.diabres.2021.109185.
2. Ibrahim M, Al Magd MA, Annabi FA, Assaad-Khalil S, Ba-Essa EM, Fahdil I, et al. Recommendations 
   for management of diabetes during Ramadan: update 2020, applying evidence from a decade of research. 
   BMJ Open Diabetes Res Care. 2020 May;8(1):e001248. doi: 10.1136/bmjdrc-2020-001248.
3. Alam F, Oubari S, Ahmad J, Eba-Alkhayri A, Almadani A, Babineaux S, et al. Validity of the 
   International Diabetes Federation risk stratification score of Ramadan fasting in individuals 
   with diabetes mellitus. Saudi Med J. 2024 Jan;45(1):86-92. doi: 10.15537/smj.2024.45.1.20230497.
"""

from typing import Dict, Any


class IdfDarFastingRiskAssessmentCalculator:
    """Calculator for IDF-DAR Fasting Risk Assessment"""
    
    def __init__(self):
        # Scoring weights for different risk factors
        self.DIABETES_TYPE_SCORES = {
            "type_2": 0,
            "type_1": 1
        }
        
        self.YEARS_DIAGNOSIS_SCORES = {
            "less_than_10": 0,
            "10_or_more": 1
        }
        
        self.HYPOGLYCEMIA_SCORES = {
            "none": 0,
            "less_than_weekly": 1,
            "multiple_weekly": 3.5,
            "recent_severe": 5.5,
            "unawareness": 6.5
        }
        
        self.HBA1C_SCORES = {
            "less_than_7_5": 0,
            "7_5_to_9": 1,
            "greater_than_9": 2
        }
        
        self.TREATMENT_SCORES = {
            "other_therapy": 0,
            "short_acting_sulfonylurea": 0.5,
            "long_acting_sulfonylurea": 1,
            "basal_insulin": 1.5,
            "mixed_insulin": 2.5,
            "intensive_insulin": 3
        }
        
        self.MONITORING_SCORES = {
            "regular": 0,
            "irregular": 0.5,
            "none": 1
        }
        
        self.COMPLICATIONS_SCORES = {
            "yes": 1,
            "no": 0
        }
        
        self.PREGNANCY_SCORES = {
            "pregnant_breastfeeding": 2,
            "not_applicable": 0
        }
        
        self.FRAILTY_SCORES = {
            "impaired": 1,
            "normal": 0
        }
        
        self.PHYSICAL_LABOR_SCORES = {
            "intense": 1,
            "moderate": 0.5,
            "light": 0
        }
        
        self.RAMADAN_EXPERIENCE_SCORES = {
            "successful": 0,
            "unsuccessful": 0.5,
            "never_fasted": 1
        }
        
        self.FASTING_HOURS_SCORES = {
            "less_than_15": 0,
            "15_or_more": 0.5
        }
    
    def calculate(self, diabetes_type: str, years_since_diagnosis: str, hypoglycemia_frequency: str,
                  hba1c_level: str, treatment_type: str, self_monitoring_frequency: str,
                  acute_complications: str, macrovascular_disease: str, renal_complications: str,
                  pregnancy_status: str, frailty_cognitive_function: str, physical_labor: str,
                  previous_ramadan_experience: str, fasting_hours: str) -> Dict[str, Any]:
        """
        Calculates IDF-DAR fasting risk score
        
        Args:
            diabetes_type (str): Type of diabetes ("type_1" or "type_2")
            years_since_diagnosis (str): Duration of diabetes ("less_than_10" or "10_or_more")
            hypoglycemia_frequency (str): Frequency of hypoglycemia
            hba1c_level (str): Glycemic control level
            treatment_type (str): Current diabetes treatment
            self_monitoring_frequency (str): Blood glucose monitoring frequency
            acute_complications (str): Recent acute complications ("yes" or "no")
            macrovascular_disease (str): Macrovascular complications ("yes" or "no")
            renal_complications (str): Renal complications ("yes" or "no")
            pregnancy_status (str): Pregnancy/breastfeeding status
            frailty_cognitive_function (str): Frailty or cognitive impairment
            physical_labor (str): Physical activity level
            previous_ramadan_experience (str): Previous Ramadan fasting experience
            fasting_hours (str): Daily fasting duration
            
        Returns:
            Dict with risk score and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(diabetes_type, years_since_diagnosis, hypoglycemia_frequency,
                            hba1c_level, treatment_type, self_monitoring_frequency,
                            acute_complications, macrovascular_disease, renal_complications,
                            pregnancy_status, frailty_cognitive_function, physical_labor,
                            previous_ramadan_experience, fasting_hours)
        
        # Calculate risk score
        risk_score = self._calculate_risk_score(
            diabetes_type, years_since_diagnosis, hypoglycemia_frequency,
            hba1c_level, treatment_type, self_monitoring_frequency,
            acute_complications, macrovascular_disease, renal_complications,
            pregnancy_status, frailty_cognitive_function, physical_labor,
            previous_ramadan_experience, fasting_hours
        )
        
        # Get interpretation
        interpretation = self._get_interpretation(risk_score)
        
        return {
            "result": risk_score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, diabetes_type: str, years_since_diagnosis: str, hypoglycemia_frequency: str,
                        hba1c_level: str, treatment_type: str, self_monitoring_frequency: str,
                        acute_complications: str, macrovascular_disease: str, renal_complications: str,
                        pregnancy_status: str, frailty_cognitive_function: str, physical_labor: str,
                        previous_ramadan_experience: str, fasting_hours: str):
        """Validates input parameters"""
        
        # Validate diabetes type
        if diabetes_type not in self.DIABETES_TYPE_SCORES:
            raise ValueError("Diabetes type must be 'type_1' or 'type_2'")
        
        # Validate years since diagnosis
        if years_since_diagnosis not in self.YEARS_DIAGNOSIS_SCORES:
            raise ValueError("Years since diagnosis must be 'less_than_10' or '10_or_more'")
        
        # Validate hypoglycemia frequency
        if hypoglycemia_frequency not in self.HYPOGLYCEMIA_SCORES:
            raise ValueError("Hypoglycemia frequency must be one of: 'none', 'less_than_weekly', 'multiple_weekly', 'recent_severe', 'unawareness'")
        
        # Validate HbA1c level
        if hba1c_level not in self.HBA1C_SCORES:
            raise ValueError("HbA1c level must be one of: 'less_than_7_5', '7_5_to_9', 'greater_than_9'")
        
        # Validate treatment type
        if treatment_type not in self.TREATMENT_SCORES:
            raise ValueError("Treatment type must be one of: 'other_therapy', 'short_acting_sulfonylurea', 'long_acting_sulfonylurea', 'basal_insulin', 'mixed_insulin', 'intensive_insulin'")
        
        # Validate monitoring frequency
        if self_monitoring_frequency not in self.MONITORING_SCORES:
            raise ValueError("Self monitoring frequency must be one of: 'regular', 'irregular', 'none'")
        
        # Validate yes/no parameters
        yes_no_params = [acute_complications, macrovascular_disease, renal_complications]
        yes_no_names = ["acute_complications", "macrovascular_disease", "renal_complications"]
        
        for param, name in zip(yes_no_params, yes_no_names):
            if param not in ["yes", "no"]:
                raise ValueError(f"{name} must be 'yes' or 'no'")
        
        # Validate pregnancy status
        if pregnancy_status not in self.PREGNANCY_SCORES:
            raise ValueError("Pregnancy status must be 'pregnant_breastfeeding' or 'not_applicable'")
        
        # Validate frailty
        if frailty_cognitive_function not in self.FRAILTY_SCORES:
            raise ValueError("Frailty cognitive function must be 'impaired' or 'normal'")
        
        # Validate physical labor
        if physical_labor not in self.PHYSICAL_LABOR_SCORES:
            raise ValueError("Physical labor must be one of: 'intense', 'moderate', 'light'")
        
        # Validate Ramadan experience
        if previous_ramadan_experience not in self.RAMADAN_EXPERIENCE_SCORES:
            raise ValueError("Previous Ramadan experience must be one of: 'successful', 'unsuccessful', 'never_fasted'")
        
        # Validate fasting hours
        if fasting_hours not in self.FASTING_HOURS_SCORES:
            raise ValueError("Fasting hours must be 'less_than_15' or '15_or_more'")
    
    def _calculate_risk_score(self, diabetes_type: str, years_since_diagnosis: str, hypoglycemia_frequency: str,
                            hba1c_level: str, treatment_type: str, self_monitoring_frequency: str,
                            acute_complications: str, macrovascular_disease: str, renal_complications: str,
                            pregnancy_status: str, frailty_cognitive_function: str, physical_labor: str,
                            previous_ramadan_experience: str, fasting_hours: str) -> float:
        """Calculates the total risk score"""
        
        total_score = 0.0
        
        # Add scores for each factor
        total_score += self.DIABETES_TYPE_SCORES[diabetes_type]
        total_score += self.YEARS_DIAGNOSIS_SCORES[years_since_diagnosis]
        total_score += self.HYPOGLYCEMIA_SCORES[hypoglycemia_frequency]
        total_score += self.HBA1C_SCORES[hba1c_level]
        total_score += self.TREATMENT_SCORES[treatment_type]
        total_score += self.MONITORING_SCORES[self_monitoring_frequency]
        total_score += self.COMPLICATIONS_SCORES[acute_complications]
        total_score += self.COMPLICATIONS_SCORES[macrovascular_disease]
        total_score += self.COMPLICATIONS_SCORES[renal_complications]
        total_score += self.PREGNANCY_SCORES[pregnancy_status]
        total_score += self.FRAILTY_SCORES[frailty_cognitive_function]
        total_score += self.PHYSICAL_LABOR_SCORES[physical_labor]
        total_score += self.RAMADAN_EXPERIENCE_SCORES[previous_ramadan_experience]
        total_score += self.FASTING_HOURS_SCORES[fasting_hours]
        
        return round(total_score, 1)
    
    def _get_interpretation(self, risk_score: float) -> Dict[str, str]:
        """
        Determines the interpretation based on the risk score
        
        Args:
            risk_score (float): Calculated risk score
            
        Returns:
            Dict with risk interpretation and recommendations
        """
        
        if risk_score <= 3.0:
            return {
                "stage": "Low Risk",
                "description": "Fasting probably safe",
                "interpretation": "Low risk for complications during Ramadan fasting. Patient can likely fast safely with appropriate education and monitoring. Recommend pre-Ramadan counseling on meal timing, glucose monitoring, and recognition of hypoglycemia symptoms. Consider adjusting medication timing but major therapy changes usually not required. Monitor for breakthrough hypoglycemia and maintain regular follow-up."
            }
        elif risk_score <= 6.0:
            return {
                "stage": "Moderate Risk",
                "description": "Fasting safety uncertain",
                "interpretation": "Moderate risk for complications during Ramadan fasting. Requires careful evaluation and enhanced monitoring. Consider medication adjustments, intensified glucose monitoring, and structured diabetes education. Patients should have clear action plans for hypoglycemia and hyperglycemia. Close supervision by healthcare team recommended. May fast with medical supervision if patient strongly desires."
            }
        else:  # risk_score > 6.0
            return {
                "stage": "High Risk",
                "description": "Fasting probably unsafe",
                "interpretation": "High risk for serious complications during Ramadan fasting. Generally advised against fasting due to significant risk of hypoglycemia, hyperglycemia, diabetic ketoacidosis, or other acute complications. If patient insists on fasting despite medical advice, requires intensive monitoring, immediate access to medical care, and detailed emergency action plans. Consider alternative spiritual practices and emphasize that health preservation is a religious priority."
            }


def calculate_idf_dar_fasting_risk_assessment(diabetes_type: str, years_since_diagnosis: str, hypoglycemia_frequency: str,
                                            hba1c_level: str, treatment_type: str, self_monitoring_frequency: str,
                                            acute_complications: str, macrovascular_disease: str, renal_complications: str,
                                            pregnancy_status: str, frailty_cognitive_function: str, physical_labor: str,
                                            previous_ramadan_experience: str, fasting_hours: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    Calculates IDF-DAR fasting risk score for Ramadan fasting in diabetic patients.
    
    Args:
        diabetes_type (str): Type of diabetes
        years_since_diagnosis (str): Duration of diabetes
        hypoglycemia_frequency (str): Frequency of hypoglycemia
        hba1c_level (str): Glycemic control level
        treatment_type (str): Current diabetes treatment
        self_monitoring_frequency (str): Blood glucose monitoring frequency
        acute_complications (str): Recent acute complications
        macrovascular_disease (str): Macrovascular complications
        renal_complications (str): Renal complications
        pregnancy_status (str): Pregnancy/breastfeeding status
        frailty_cognitive_function (str): Frailty or cognitive impairment
        physical_labor (str): Physical activity level
        previous_ramadan_experience (str): Previous Ramadan fasting experience
        fasting_hours (str): Daily fasting duration
        
    Returns:
        Dict with risk score and clinical interpretation
    """
    calculator = IdfDarFastingRiskAssessmentCalculator()
    return calculator.calculate(diabetes_type, years_since_diagnosis, hypoglycemia_frequency,
                              hba1c_level, treatment_type, self_monitoring_frequency,
                              acute_complications, macrovascular_disease, renal_complications,
                              pregnancy_status, frailty_cognitive_function, physical_labor,
                              previous_ramadan_experience, fasting_hours)