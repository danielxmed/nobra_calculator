"""
Veterans Aging Cohort Study-Charlson Comorbidity Index (VACS-CCI) Calculator

Combines the Veterans Aging Cohort Study (VACS) Index with the Charlson 
Comorbidity Index to provide enhanced mortality risk prediction for patients 
with HIV. This integrated score incorporates HIV-specific biomarkers, general 
health indicators, and comprehensive comorbidity assessment.

References (Vancouver style):
1. Justice AC, Lasky E, McGinnis KA, Skanderson M, Conigliaro J, Fultz SL, et al. 
   Medical disease and alcohol use among veterans with human immunodeficiency infection: 
   A comparison of disease measurement strategies. Med Care. 2006 Apr;44(4):S52-60. 
   doi: 10.1097/01.mlr.0000208140.93199.44.
2. Tate JP, Justice AC, Hughes MD, Bonnet F, Reiss P, Mocroft A, et al. An internationally 
   generalizable risk index for mortality after one year of antiretroviral therapy. 
   AIDS. 2013 Feb 20;27(4):563-72. doi: 10.1097/QAD.0b013e32835c5b67.
3. Charlson ME, Pompei P, Ales KL, MacKenzie CR. A new method of classifying prognostic 
   comorbidity in longitudinal studies: development and validation. J Chronic Dis. 1987;40(5):373-83. 
   doi: 10.1016/0021-9681(87)90171-8.
"""

import math
from typing import Dict, Any


class VacsCciCalculator:
    """Calculator for Veterans Aging Cohort Study-Charlson Comorbidity Index (VACS-CCI)"""
    
    def __init__(self):
        # Formula constants from research
        self.INTERCEPT = 2.5390222
        self.SCALE_FACTOR = 10.6663937
        
        # VACS Index coefficients (simplified for this implementation)
        self.VACS_COEFFICIENTS = {
            'age': 0.054,
            'cd4_count': -0.0035,
            'hiv_rna_log': 0.31,
            'hemoglobin': -0.19,
            'fib4': 0.24,
            'egfr': -0.0086,
            'hepatitis_c': 0.62
        }
        
        # Charlson Comorbidity Index weights
        self.CHARLSON_WEIGHTS = {
            'myocardial_infarction': 1,
            'congestive_heart_failure': 1,
            'peripheral_vascular_disease': 1,
            'cerebrovascular_disease': 1,
            'dementia': 1,
            'chronic_pulmonary_disease': 1,
            'rheumatic_disease': 1,
            'peptic_ulcer_disease': 1,
            'mild_liver_disease': 1,
            'diabetes': 1,
            'diabetes_complications': 2,
            'hemiplegia': 2,
            'renal_disease': 2,
            'any_malignancy': 2,
            'moderate_severe_liver_disease': 3,
            'metastatic_solid_tumor': 6,
            'aids': 6
        }
    
    def calculate(self, age: int, sex: str, race: str, cd4_count: int, hiv_rna_log: float,
                 hemoglobin: float, platelets: int, ast: int, alt: int, creatinine: float,
                 hepatitis_c: str, myocardial_infarction: str, congestive_heart_failure: str,
                 peripheral_vascular_disease: str, cerebrovascular_disease: str, dementia: str,
                 chronic_pulmonary_disease: str, rheumatic_disease: str, peptic_ulcer_disease: str,
                 mild_liver_disease: str, diabetes: str, diabetes_complications: str,
                 hemiplegia: str, renal_disease: str, any_malignancy: str,
                 moderate_severe_liver_disease: str, metastatic_solid_tumor: str,
                 aids: str) -> Dict[str, Any]:
        """
        Calculates the VACS-CCI score using the provided parameters
        
        Args:
            age (int): Patient age in years
            sex (str): Patient sex ('male' or 'female')
            race (str): Patient race ('black' or 'non_black')
            cd4_count (int): CD4 T-cell count in cells/μL
            hiv_rna_log (float): HIV-1 RNA viral load in log10 copies/mL
            hemoglobin (float): Hemoglobin level in g/dL
            platelets (int): Platelet count in ×10³/μL
            ast (int): Aspartate aminotransferase in U/L
            alt (int): Alanine aminotransferase in U/L
            creatinine (float): Serum creatinine in mg/dL
            hepatitis_c (str): Hepatitis C status ('yes' or 'no')
            myocardial_infarction (str): History of MI ('yes' or 'no')
            congestive_heart_failure (str): History of CHF ('yes' or 'no')
            peripheral_vascular_disease (str): History of PVD ('yes' or 'no')
            cerebrovascular_disease (str): History of stroke ('yes' or 'no')
            dementia (str): History of dementia ('yes' or 'no')
            chronic_pulmonary_disease (str): History of COPD ('yes' or 'no')
            rheumatic_disease (str): History of rheumatic disease ('yes' or 'no')
            peptic_ulcer_disease (str): History of PUD ('yes' or 'no')
            mild_liver_disease (str): History of mild liver disease ('yes' or 'no')
            diabetes (str): History of diabetes ('yes' or 'no')
            diabetes_complications (str): Diabetes with complications ('yes' or 'no')
            hemiplegia (str): History of hemiplegia ('yes' or 'no')
            renal_disease (str): History of renal disease ('yes' or 'no')
            any_malignancy (str): History of malignancy ('yes' or 'no')
            moderate_severe_liver_disease (str): Moderate/severe liver disease ('yes' or 'no')
            metastatic_solid_tumor (str): Metastatic solid tumor ('yes' or 'no')
            aids (str): AIDS diagnosis ('yes' or 'no')
            
        Returns:
            Dict with the result and interpretation
        """
        
        # Validations
        self._validate_inputs(age, sex, race, cd4_count, hiv_rna_log, hemoglobin, 
                            platelets, ast, alt, creatinine, hepatitis_c)
        
        # Calculate composite biomarkers
        fib4 = self._calculate_fib4(age, ast, alt, platelets)
        egfr = self._calculate_egfr(creatinine, age, sex, race)
        
        # Calculate VACS components
        vacs_score = self._calculate_vacs_components(age, cd4_count, hiv_rna_log, 
                                                   hemoglobin, fib4, egfr, hepatitis_c)
        
        # Calculate Charlson components
        charlson_score = self._calculate_charlson_components(
            myocardial_infarction, congestive_heart_failure, peripheral_vascular_disease,
            cerebrovascular_disease, dementia, chronic_pulmonary_disease, rheumatic_disease,
            peptic_ulcer_disease, mild_liver_disease, diabetes, diabetes_complications,
            hemiplegia, renal_disease, any_malignancy, moderate_severe_liver_disease,
            metastatic_solid_tumor, aids
        )
        
        # Calculate linear predictor
        linear_predictor = vacs_score + charlson_score
        
        # Apply final formula
        result = ((linear_predictor + self.INTERCEPT) / self.SCALE_FACTOR) * 100
        
        # Ensure result is within valid range
        result = max(0, min(100, result))
        
        # Get interpretation
        interpretation = self._get_interpretation(result)
        
        return {
            "result": round(result, 1),
            "unit": "percentage",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"],
            "component_scores": {
                "vacs_score": round(vacs_score, 2),
                "charlson_score": round(charlson_score, 2),
                "linear_predictor": round(linear_predictor, 2)
            },
            "composite_biomarkers": {
                "fib4": round(fib4, 2),
                "egfr": round(egfr, 1)
            }
        }
    
    def _validate_inputs(self, age, sex, race, cd4_count, hiv_rna_log, hemoglobin,
                        platelets, ast, alt, creatinine, hepatitis_c):
        """Validates input parameters"""
        
        if not isinstance(age, int) or age < 18 or age > 100:
            raise ValueError("Age must be an integer between 18 and 100 years")
        
        if sex not in ["male", "female"]:
            raise ValueError("Sex must be 'male' or 'female'")
        
        if race not in ["black", "non_black"]:
            raise ValueError("Race must be 'black' or 'non_black'")
        
        if not isinstance(cd4_count, int) or cd4_count < 0 or cd4_count > 2000:
            raise ValueError("CD4 count must be an integer between 0 and 2000 cells/μL")
        
        if not isinstance(hiv_rna_log, (int, float)) or hiv_rna_log < 0 or hiv_rna_log > 7:
            raise ValueError("HIV RNA log must be between 0 and 7 log10 copies/mL")
        
        if not isinstance(hemoglobin, (int, float)) or hemoglobin < 5 or hemoglobin > 20:
            raise ValueError("Hemoglobin must be between 5 and 20 g/dL")
        
        if not isinstance(platelets, int) or platelets < 10 or platelets > 1000:
            raise ValueError("Platelets must be an integer between 10 and 1000 ×10³/μL")
        
        if not isinstance(ast, int) or ast < 10 or ast > 500:
            raise ValueError("AST must be an integer between 10 and 500 U/L")
        
        if not isinstance(alt, int) or alt < 10 or alt > 500:
            raise ValueError("ALT must be an integer between 10 and 500 U/L")
        
        if not isinstance(creatinine, (int, float)) or creatinine < 0.5 or creatinine > 10:
            raise ValueError("Creatinine must be between 0.5 and 10 mg/dL")
        
        if hepatitis_c not in ["yes", "no"]:
            raise ValueError("Hepatitis C status must be 'yes' or 'no'")
    
    def _calculate_fib4(self, age: int, ast: int, alt: int, platelets: int) -> float:
        """Calculates FIB-4 score: (Age × AST) / (Platelets × √ALT)"""
        
        if alt <= 0 or platelets <= 0:
            raise ValueError("ALT and platelets must be positive for FIB-4 calculation")
        
        fib4 = (age * ast) / (platelets * math.sqrt(alt))
        return fib4
    
    def _calculate_egfr(self, creatinine: float, age: int, sex: str, race: str) -> float:
        """Calculates eGFR using CKD-EPI equation"""
        
        # CKD-EPI equation constants
        if sex == "female":
            if creatinine <= 0.7:
                egfr = 144 * ((creatinine / 0.7) ** -0.329) * (0.993 ** age)
            else:
                egfr = 144 * ((creatinine / 0.7) ** -1.209) * (0.993 ** age)
        else:  # male
            if creatinine <= 0.9:
                egfr = 141 * ((creatinine / 0.9) ** -0.411) * (0.993 ** age)
            else:
                egfr = 141 * ((creatinine / 0.9) ** -1.209) * (0.993 ** age)
        
        # Apply race factor
        if race == "black":
            egfr *= 1.159
        
        return egfr
    
    def _calculate_vacs_components(self, age: int, cd4_count: int, hiv_rna_log: float,
                                 hemoglobin: float, fib4: float, egfr: float,
                                 hepatitis_c: str) -> float:
        """Calculates VACS Index components"""
        
        vacs_score = 0
        
        # Age component
        vacs_score += age * self.VACS_COEFFICIENTS['age']
        
        # CD4 count component
        vacs_score += cd4_count * self.VACS_COEFFICIENTS['cd4_count']
        
        # HIV RNA component
        vacs_score += hiv_rna_log * self.VACS_COEFFICIENTS['hiv_rna_log']
        
        # Hemoglobin component
        vacs_score += hemoglobin * self.VACS_COEFFICIENTS['hemoglobin']
        
        # FIB-4 component
        vacs_score += fib4 * self.VACS_COEFFICIENTS['fib4']
        
        # eGFR component
        vacs_score += egfr * self.VACS_COEFFICIENTS['egfr']
        
        # Hepatitis C component
        if hepatitis_c == "yes":
            vacs_score += self.VACS_COEFFICIENTS['hepatitis_c']
        
        return vacs_score
    
    def _calculate_charlson_components(self, myocardial_infarction: str, congestive_heart_failure: str,
                                     peripheral_vascular_disease: str, cerebrovascular_disease: str,
                                     dementia: str, chronic_pulmonary_disease: str, rheumatic_disease: str,
                                     peptic_ulcer_disease: str, mild_liver_disease: str, diabetes: str,
                                     diabetes_complications: str, hemiplegia: str, renal_disease: str,
                                     any_malignancy: str, moderate_severe_liver_disease: str,
                                     metastatic_solid_tumor: str, aids: str) -> float:
        """Calculates Charlson Comorbidity Index components"""
        
        charlson_score = 0
        
        # Define comorbidity variables
        comorbidities = {
            'myocardial_infarction': myocardial_infarction,
            'congestive_heart_failure': congestive_heart_failure,
            'peripheral_vascular_disease': peripheral_vascular_disease,
            'cerebrovascular_disease': cerebrovascular_disease,
            'dementia': dementia,
            'chronic_pulmonary_disease': chronic_pulmonary_disease,
            'rheumatic_disease': rheumatic_disease,
            'peptic_ulcer_disease': peptic_ulcer_disease,
            'mild_liver_disease': mild_liver_disease,
            'diabetes': diabetes,
            'diabetes_complications': diabetes_complications,
            'hemiplegia': hemiplegia,
            'renal_disease': renal_disease,
            'any_malignancy': any_malignancy,
            'moderate_severe_liver_disease': moderate_severe_liver_disease,
            'metastatic_solid_tumor': metastatic_solid_tumor,
            'aids': aids
        }
        
        # Calculate Charlson score
        for comorbidity, status in comorbidities.items():
            if status == "yes":
                charlson_score += self.CHARLSON_WEIGHTS[comorbidity]
        
        return charlson_score
    
    def _get_interpretation(self, result: float) -> Dict[str, str]:
        """
        Determines the interpretation based on the result
        
        Args:
            result (float): Calculated VACS-CCI percentage
            
        Returns:
            Dict with interpretation
        """
        
        if result <= 25:
            return {
                "stage": "Low Risk",
                "description": "Low mortality risk",
                "interpretation": f"VACS-CCI score: {result:.1f}%. Low 5-year mortality risk. "
                                f"Routine HIV care and standard preventive measures appropriate. "
                                f"Regular monitoring and optimization of antiretroviral therapy recommended."
            }
        elif result <= 50:
            return {
                "stage": "Moderate Risk",
                "description": "Moderate mortality risk",
                "interpretation": f"VACS-CCI score: {result:.1f}%. Moderate 5-year mortality risk. "
                                f"Enhanced monitoring and proactive management of comorbidities recommended. "
                                f"Consider intensified preventive interventions and specialist consultations."
            }
        elif result <= 75:
            return {
                "stage": "High Risk",
                "description": "High mortality risk",
                "interpretation": f"VACS-CCI score: {result:.1f}%. High 5-year mortality risk. "
                                f"Intensive management required with multidisciplinary care approach. "
                                f"Aggressive treatment of all modifiable risk factors and frequent monitoring indicated."
            }
        else:
            return {
                "stage": "Very High Risk",
                "description": "Very high mortality risk",
                "interpretation": f"VACS-CCI score: {result:.1f}%. Very high 5-year mortality risk. "
                                f"Maximum therapeutic interventions and comprehensive care coordination essential. "
                                f"Consider palliative care consultation and advance care planning discussions."
            }


def calculate_vacs_cci(age, sex, race, cd4_count, hiv_rna_log, hemoglobin, platelets,
                      ast, alt, creatinine, hepatitis_c, myocardial_infarction,
                      congestive_heart_failure, peripheral_vascular_disease,
                      cerebrovascular_disease, dementia, chronic_pulmonary_disease,
                      rheumatic_disease, peptic_ulcer_disease, mild_liver_disease,
                      diabetes, diabetes_complications, hemiplegia, renal_disease,
                      any_malignancy, moderate_severe_liver_disease,
                      metastatic_solid_tumor, aids) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_vacs_cci pattern
    """
    calculator = VacsCciCalculator()
    return calculator.calculate(
        age, sex, race, cd4_count, hiv_rna_log, hemoglobin, platelets,
        ast, alt, creatinine, hepatitis_c, myocardial_infarction,
        congestive_heart_failure, peripheral_vascular_disease,
        cerebrovascular_disease, dementia, chronic_pulmonary_disease,
        rheumatic_disease, peptic_ulcer_disease, mild_liver_disease,
        diabetes, diabetes_complications, hemiplegia, renal_disease,
        any_malignancy, moderate_severe_liver_disease,
        metastatic_solid_tumor, aids
    )