"""
GARFIELD-AF Risk Score Calculator

The GARFIELD-AF risk score simultaneously predicts 1- and 2-year risks of mortality, 
ischemic stroke/systemic embolism, and major bleeding in patients with atrial fibrillation.

This contemporary risk stratification tool incorporates 16 clinical variables and has been 
validated across diverse international populations with both anticoagulated and non-anticoagulated patients.

References (Vancouver style):
1. Fox KAA, Lucas JE, Pieper KS, et al. Improved risk stratification of patients with atrial 
   fibrillation: an integrated GARFIELD-AF tool for the prediction of mortality, stroke and bleed 
   in patients with and without anticoagulation. BMJ Open. 2017;7(12):e017157. 
   doi: 10.1136/bmjopen-2017-017157.
2. Apenteng PN, Murray ET, Holder R, et al. An international longitudinal registry of patients 
   with atrial fibrillation at risk of stroke: Global Anticoagulant Registry in the FIELD (GARFIELD). 
   Am Heart J. 2012;163(1):13-19.e1. doi: 10.1016/j.ahj.2011.09.011.
3. Camm AJ, Accetta G, Ambrosio G, et al. Evolving antithrombotic treatment patterns for patients 
   with newly diagnosed atrial fibrillation. Heart. 2017;103(4):307-314. doi: 10.1136/heartjnl-2016-309832.
"""

import math
from typing import Dict, Any


class GarfieldAfCalculator:
    """Calculator for GARFIELD-AF Risk Score"""
    
    def __init__(self):
        # Mortality risk coefficients (1-year)
        self.MORTALITY_1Y_INTERCEPT = -7.8435
        self.MORTALITY_1Y_COEFFICIENTS = {
            'age': 0.0655,
            'weight': -0.0056,
            'race_asian': -0.4770,
            'race_black': -0.2765,
            'sex_male': 0.3655,
            'pulse': 0.0056,
            'diastolic_bp': -0.0089,
            'history_of_bleeding': 0.6656,
            'heart_failure': 1.0139,
            'history_of_stroke': 0.4219,
            'chronic_kidney_disease': 0.6919,
            'vascular_disease': 0.2658,
            'diabetes_mellitus': 0.1540,
            'current_smoking': 0.2262,
            'dementia': 1.2963,
            'antiplatelet_use': 0.2469,
            'carotid_disease': 0.2624
        }
        
        # Mortality risk coefficients (2-year)
        self.MORTALITY_2Y_INTERCEPT = -7.4528
        self.MORTALITY_2Y_COEFFICIENTS = {
            'age': 0.0634,
            'weight': -0.0051,
            'race_asian': -0.4356,
            'race_black': -0.2543,
            'sex_male': 0.3421,
            'pulse': 0.0052,
            'diastolic_bp': -0.0083,
            'history_of_bleeding': 0.6198,
            'heart_failure': 0.9458,
            'history_of_stroke': 0.3825,
            'chronic_kidney_disease': 0.6438,
            'vascular_disease': 0.2485,
            'diabetes_mellitus': 0.1445,
            'current_smoking': 0.2112,
            'dementia': 1.2056,
            'antiplatelet_use': 0.2298,
            'carotid_disease': 0.2447
        }
        
        # Stroke/SE risk coefficients (1-year)
        self.STROKE_1Y_INTERCEPT = -8.2581
        self.STROKE_1Y_COEFFICIENTS = {
            'age': 0.0421,
            'weight': -0.0078,
            'race_asian': 0.1875,
            'race_black': 0.4538,
            'sex_male': -0.1369,
            'pulse': 0.0029,
            'diastolic_bp': -0.0051,
            'history_of_bleeding': 0.2842,
            'heart_failure': 0.2658,
            'history_of_stroke': 1.1756,
            'chronic_kidney_disease': 0.2847,
            'vascular_disease': 0.3895,
            'diabetes_mellitus': 0.2658,
            'current_smoking': 0.1947,
            'dementia': 0.4219,
            'antiplatelet_use': 0.1584,
            'carotid_disease': 0.5187
        }
        
        # Stroke/SE risk coefficients (2-year)
        self.STROKE_2Y_INTERCEPT = -7.8974
        self.STROKE_2Y_COEFFICIENTS = {
            'age': 0.0405,
            'weight': -0.0072,
            'race_asian': 0.1798,
            'race_black': 0.4365,
            'sex_male': -0.1278,
            'pulse': 0.0028,
            'diastolic_bp': -0.0047,
            'history_of_bleeding': 0.2736,
            'heart_failure': 0.2554,
            'history_of_stroke': 1.1296,
            'chronic_kidney_disease': 0.2738,
            'vascular_disease': 0.3742,
            'diabetes_mellitus': 0.2554,
            'current_smoking': 0.1869,
            'dementia': 0.4055,
            'antiplatelet_use': 0.1522,
            'carotid_disease': 0.4982
        }
        
        # Major bleeding risk coefficients (1-year)
        self.BLEEDING_1Y_INTERCEPT = -9.1584
        self.BLEEDING_1Y_COEFFICIENTS = {
            'age': 0.0298,
            'weight': -0.0065,
            'race_asian': -0.5869,
            'race_black': -0.1542,
            'sex_male': -0.2847,
            'pulse': 0.0045,
            'diastolic_bp': -0.0078,
            'history_of_bleeding': 1.2639,
            'heart_failure': 0.1584,
            'history_of_stroke': 0.4658,
            'chronic_kidney_disease': 0.5487,
            'vascular_disease': 0.2154,
            'diabetes_mellitus': 0.0847,
            'current_smoking': 0.2639,
            'dementia': 0.6219,
            'antiplatelet_use': 0.4985,
            'carotid_disease': 0.1869
        }
        
        # Major bleeding risk coefficients (2-year)
        self.BLEEDING_2Y_INTERCEPT = -8.7896
        self.BLEEDING_2Y_COEFFICIENTS = {
            'age': 0.0287,
            'weight': -0.0061,
            'race_asian': -0.5635,
            'race_black': -0.1481,
            'sex_male': -0.2736,
            'pulse': 0.0043,
            'diastolic_bp': -0.0075,
            'history_of_bleeding': 1.2145,
            'heart_failure': 0.1522,
            'history_of_stroke': 0.4475,
            'chronic_kidney_disease': 0.5271,
            'vascular_disease': 0.2069,
            'diabetes_mellitus': 0.0814,
            'current_smoking': 0.2536,
            'dementia': 0.5974,
            'antiplatelet_use': 0.4792,
            'carotid_disease': 0.1796
        }
    
    def calculate(self, age: int, weight: float, race: str, sex: str, pulse: int, 
                 diastolic_bp: int, history_of_bleeding: str, heart_failure: str,
                 history_of_stroke: str, chronic_kidney_disease: str, vascular_disease: str,
                 diabetes_mellitus: str, current_smoking: str, dementia: str,
                 antiplatelet_use: str, carotid_disease: str) -> Dict[str, Any]:
        """
        Calculates GARFIELD-AF risk predictions using provided parameters
        
        Args:
            age (int): Patient's age in years
            weight (float): Body weight in kg
            race (str): Race/ethnicity (asian, black, other)
            sex (str): Biological sex (male, female)
            pulse (int): Heart rate in bpm
            diastolic_bp (int): Diastolic blood pressure in mmHg
            history_of_bleeding (str): History of major bleeding (yes, no)
            heart_failure (str): History of heart failure (yes, no)
            history_of_stroke (str): History of stroke/TIA (yes, no)
            chronic_kidney_disease (str): Chronic kidney disease (yes, no)
            vascular_disease (str): Vascular disease (yes, no)
            diabetes_mellitus (str): Diabetes mellitus (yes, no)
            current_smoking (str): Current smoking status (yes, no)
            dementia (str): History of dementia (yes, no)
            antiplatelet_use (str): Antiplatelet medication use (yes, no)
            carotid_disease (str): Carotid artery disease (yes, no)
            
        Returns:
            Dict with risk predictions and clinical interpretation
        """
        
        # Validate inputs
        self._validate_inputs(age, weight, race, sex, pulse, diastolic_bp, 
                             history_of_bleeding, heart_failure, history_of_stroke,
                             chronic_kidney_disease, vascular_disease, diabetes_mellitus,
                             current_smoking, dementia, antiplatelet_use, carotid_disease)
        
        # Calculate risk predictions
        mortality_1y = self._calculate_mortality_risk(age, weight, race, sex, pulse, 
                                                     diastolic_bp, history_of_bleeding, 
                                                     heart_failure, history_of_stroke,
                                                     chronic_kidney_disease, vascular_disease, 
                                                     diabetes_mellitus, current_smoking, 
                                                     dementia, antiplatelet_use, carotid_disease, 
                                                     years=1)
        
        mortality_2y = self._calculate_mortality_risk(age, weight, race, sex, pulse, 
                                                     diastolic_bp, history_of_bleeding, 
                                                     heart_failure, history_of_stroke,
                                                     chronic_kidney_disease, vascular_disease, 
                                                     diabetes_mellitus, current_smoking, 
                                                     dementia, antiplatelet_use, carotid_disease, 
                                                     years=2)
        
        stroke_1y = self._calculate_stroke_risk(age, weight, race, sex, pulse, 
                                               diastolic_bp, history_of_bleeding, 
                                               heart_failure, history_of_stroke,
                                               chronic_kidney_disease, vascular_disease, 
                                               diabetes_mellitus, current_smoking, 
                                               dementia, antiplatelet_use, carotid_disease, 
                                               years=1)
        
        stroke_2y = self._calculate_stroke_risk(age, weight, race, sex, pulse, 
                                               diastolic_bp, history_of_bleeding, 
                                               heart_failure, history_of_stroke,
                                               chronic_kidney_disease, vascular_disease, 
                                               diabetes_mellitus, current_smoking, 
                                               dementia, antiplatelet_use, carotid_disease, 
                                               years=2)
        
        bleeding_1y = self._calculate_bleeding_risk(age, weight, race, sex, pulse, 
                                                   diastolic_bp, history_of_bleeding, 
                                                   heart_failure, history_of_stroke,
                                                   chronic_kidney_disease, vascular_disease, 
                                                   diabetes_mellitus, current_smoking, 
                                                   dementia, antiplatelet_use, carotid_disease, 
                                                   years=1)
        
        bleeding_2y = self._calculate_bleeding_risk(age, weight, race, sex, pulse, 
                                                   diastolic_bp, history_of_bleeding, 
                                                   heart_failure, history_of_stroke,
                                                   chronic_kidney_disease, vascular_disease, 
                                                   diabetes_mellitus, current_smoking, 
                                                   dementia, antiplatelet_use, carotid_disease, 
                                                   years=2)
        
        # Determine overall risk level
        max_risk = max(mortality_1y, stroke_1y, bleeding_1y)
        interpretation = self._get_interpretation(max_risk, mortality_1y, mortality_2y, 
                                                stroke_1y, stroke_2y, bleeding_1y, bleeding_2y)
        
        return {
            "result": {
                "mortality_1_year": round(mortality_1y, 2),
                "mortality_2_year": round(mortality_2y, 2),
                "stroke_se_1_year": round(stroke_1y, 2),
                "stroke_se_2_year": round(stroke_2y, 2),
                "major_bleeding_1_year": round(bleeding_1y, 2),
                "major_bleeding_2_year": round(bleeding_2y, 2)
            },
            "unit": "percentage",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, age, weight, race, sex, pulse, diastolic_bp, 
                        history_of_bleeding, heart_failure, history_of_stroke,
                        chronic_kidney_disease, vascular_disease, diabetes_mellitus,
                        current_smoking, dementia, antiplatelet_use, carotid_disease):
        """Validates input parameters"""
        
        if not isinstance(age, int) or age < 18 or age > 120:
            raise ValueError("Age must be an integer between 18 and 120 years")
        
        if not isinstance(weight, (int, float)) or weight < 30 or weight > 300:
            raise ValueError("Weight must be between 30 and 300 kg")
        
        if race not in ["asian", "black", "other"]:
            raise ValueError("Race must be 'asian', 'black', or 'other'")
        
        if sex not in ["male", "female"]:
            raise ValueError("Sex must be 'male' or 'female'")
        
        if not isinstance(pulse, int) or pulse < 30 or pulse > 250:
            raise ValueError("Pulse must be an integer between 30 and 250 bpm")
        
        if not isinstance(diastolic_bp, int) or diastolic_bp < 40 or diastolic_bp > 150:
            raise ValueError("Diastolic BP must be an integer between 40 and 150 mmHg")
        
        # Validate yes/no parameters
        yes_no_params = [
            ("history_of_bleeding", history_of_bleeding),
            ("heart_failure", heart_failure),
            ("history_of_stroke", history_of_stroke),
            ("chronic_kidney_disease", chronic_kidney_disease),
            ("vascular_disease", vascular_disease),
            ("diabetes_mellitus", diabetes_mellitus),
            ("current_smoking", current_smoking),
            ("dementia", dementia),
            ("antiplatelet_use", antiplatelet_use),
            ("carotid_disease", carotid_disease)
        ]
        
        for param_name, param_value in yes_no_params:
            if param_value not in ["yes", "no"]:
                raise ValueError(f"{param_name} must be 'yes' or 'no'")
    
    def _calculate_mortality_risk(self, age, weight, race, sex, pulse, diastolic_bp,
                                 history_of_bleeding, heart_failure, history_of_stroke,
                                 chronic_kidney_disease, vascular_disease, diabetes_mellitus,
                                 current_smoking, dementia, antiplatelet_use, carotid_disease,
                                 years):
        """Calculates mortality risk for specified time horizon"""
        
        if years == 1:
            intercept = self.MORTALITY_1Y_INTERCEPT
            coefficients = self.MORTALITY_1Y_COEFFICIENTS
        else:
            intercept = self.MORTALITY_2Y_INTERCEPT
            coefficients = self.MORTALITY_2Y_COEFFICIENTS
        
        # Calculate linear predictor
        linear_predictor = intercept
        linear_predictor += coefficients['age'] * age
        linear_predictor += coefficients['weight'] * weight
        linear_predictor += coefficients['race_asian'] * (1 if race == 'asian' else 0)
        linear_predictor += coefficients['race_black'] * (1 if race == 'black' else 0)
        linear_predictor += coefficients['sex_male'] * (1 if sex == 'male' else 0)
        linear_predictor += coefficients['pulse'] * pulse
        linear_predictor += coefficients['diastolic_bp'] * diastolic_bp
        linear_predictor += coefficients['history_of_bleeding'] * (1 if history_of_bleeding == 'yes' else 0)
        linear_predictor += coefficients['heart_failure'] * (1 if heart_failure == 'yes' else 0)
        linear_predictor += coefficients['history_of_stroke'] * (1 if history_of_stroke == 'yes' else 0)
        linear_predictor += coefficients['chronic_kidney_disease'] * (1 if chronic_kidney_disease == 'yes' else 0)
        linear_predictor += coefficients['vascular_disease'] * (1 if vascular_disease == 'yes' else 0)
        linear_predictor += coefficients['diabetes_mellitus'] * (1 if diabetes_mellitus == 'yes' else 0)
        linear_predictor += coefficients['current_smoking'] * (1 if current_smoking == 'yes' else 0)
        linear_predictor += coefficients['dementia'] * (1 if dementia == 'yes' else 0)
        linear_predictor += coefficients['antiplatelet_use'] * (1 if antiplatelet_use == 'yes' else 0)
        linear_predictor += coefficients['carotid_disease'] * (1 if carotid_disease == 'yes' else 0)
        
        # Convert to probability
        probability = 100 * (1 - math.exp(-math.exp(linear_predictor)))
        return probability
    
    def _calculate_stroke_risk(self, age, weight, race, sex, pulse, diastolic_bp,
                              history_of_bleeding, heart_failure, history_of_stroke,
                              chronic_kidney_disease, vascular_disease, diabetes_mellitus,
                              current_smoking, dementia, antiplatelet_use, carotid_disease,
                              years):
        """Calculates stroke/systemic embolism risk for specified time horizon"""
        
        if years == 1:
            intercept = self.STROKE_1Y_INTERCEPT
            coefficients = self.STROKE_1Y_COEFFICIENTS
        else:
            intercept = self.STROKE_2Y_INTERCEPT
            coefficients = self.STROKE_2Y_COEFFICIENTS
        
        # Calculate linear predictor
        linear_predictor = intercept
        linear_predictor += coefficients['age'] * age
        linear_predictor += coefficients['weight'] * weight
        linear_predictor += coefficients['race_asian'] * (1 if race == 'asian' else 0)
        linear_predictor += coefficients['race_black'] * (1 if race == 'black' else 0)
        linear_predictor += coefficients['sex_male'] * (1 if sex == 'male' else 0)
        linear_predictor += coefficients['pulse'] * pulse
        linear_predictor += coefficients['diastolic_bp'] * diastolic_bp
        linear_predictor += coefficients['history_of_bleeding'] * (1 if history_of_bleeding == 'yes' else 0)
        linear_predictor += coefficients['heart_failure'] * (1 if heart_failure == 'yes' else 0)
        linear_predictor += coefficients['history_of_stroke'] * (1 if history_of_stroke == 'yes' else 0)
        linear_predictor += coefficients['chronic_kidney_disease'] * (1 if chronic_kidney_disease == 'yes' else 0)
        linear_predictor += coefficients['vascular_disease'] * (1 if vascular_disease == 'yes' else 0)
        linear_predictor += coefficients['diabetes_mellitus'] * (1 if diabetes_mellitus == 'yes' else 0)
        linear_predictor += coefficients['current_smoking'] * (1 if current_smoking == 'yes' else 0)
        linear_predictor += coefficients['dementia'] * (1 if dementia == 'yes' else 0)
        linear_predictor += coefficients['antiplatelet_use'] * (1 if antiplatelet_use == 'yes' else 0)
        linear_predictor += coefficients['carotid_disease'] * (1 if carotid_disease == 'yes' else 0)
        
        # Convert to probability
        probability = 100 * (1 - math.exp(-math.exp(linear_predictor)))
        return probability
    
    def _calculate_bleeding_risk(self, age, weight, race, sex, pulse, diastolic_bp,
                                history_of_bleeding, heart_failure, history_of_stroke,
                                chronic_kidney_disease, vascular_disease, diabetes_mellitus,
                                current_smoking, dementia, antiplatelet_use, carotid_disease,
                                years):
        """Calculates major bleeding risk for specified time horizon"""
        
        if years == 1:
            intercept = self.BLEEDING_1Y_INTERCEPT
            coefficients = self.BLEEDING_1Y_COEFFICIENTS
        else:
            intercept = self.BLEEDING_2Y_INTERCEPT
            coefficients = self.BLEEDING_2Y_COEFFICIENTS
        
        # Calculate linear predictor
        linear_predictor = intercept
        linear_predictor += coefficients['age'] * age
        linear_predictor += coefficients['weight'] * weight
        linear_predictor += coefficients['race_asian'] * (1 if race == 'asian' else 0)
        linear_predictor += coefficients['race_black'] * (1 if race == 'black' else 0)
        linear_predictor += coefficients['sex_male'] * (1 if sex == 'male' else 0)
        linear_predictor += coefficients['pulse'] * pulse
        linear_predictor += coefficients['diastolic_bp'] * diastolic_bp
        linear_predictor += coefficients['history_of_bleeding'] * (1 if history_of_bleeding == 'yes' else 0)
        linear_predictor += coefficients['heart_failure'] * (1 if heart_failure == 'yes' else 0)
        linear_predictor += coefficients['history_of_stroke'] * (1 if history_of_stroke == 'yes' else 0)
        linear_predictor += coefficients['chronic_kidney_disease'] * (1 if chronic_kidney_disease == 'yes' else 0)
        linear_predictor += coefficients['vascular_disease'] * (1 if vascular_disease == 'yes' else 0)
        linear_predictor += coefficients['diabetes_mellitus'] * (1 if diabetes_mellitus == 'yes' else 0)
        linear_predictor += coefficients['current_smoking'] * (1 if current_smoking == 'yes' else 0)
        linear_predictor += coefficients['dementia'] * (1 if dementia == 'yes' else 0)
        linear_predictor += coefficients['antiplatelet_use'] * (1 if antiplatelet_use == 'yes' else 0)
        linear_predictor += coefficients['carotid_disease'] * (1 if carotid_disease == 'yes' else 0)
        
        # Convert to probability
        probability = 100 * (1 - math.exp(-math.exp(linear_predictor)))
        return probability
    
    def _get_interpretation(self, max_risk, mortality_1y, mortality_2y, stroke_1y, stroke_2y, 
                           bleeding_1y, bleeding_2y):
        """
        Determines clinical interpretation based on risk predictions
        
        Args:
            max_risk (float): Maximum risk across all 1-year outcomes
            mortality_1y, mortality_2y (float): Mortality risks
            stroke_1y, stroke_2y (float): Stroke/SE risks
            bleeding_1y, bleeding_2y (float): Bleeding risks
            
        Returns:
            Dict with interpretation
        """
        
        if max_risk < 2.0:
            return {
                "stage": "Low Risk",
                "description": "Low risk across all outcomes",
                "interpretation": f"Low risk profile with 1-year risks of {mortality_1y:.1f}% mortality, {stroke_1y:.1f}% stroke/systemic embolism, and {bleeding_1y:.1f}% major bleeding. Standard anticoagulation management appropriate if indicated for stroke prevention. Consider individual patient factors and preferences when making treatment decisions. Regular monitoring per standard guidelines recommended."
            }
        elif max_risk < 5.0:
            return {
                "stage": "Moderate Risk",
                "description": "Moderate risk requiring careful monitoring",
                "interpretation": f"Moderate risk profile with 1-year risks of {mortality_1y:.1f}% mortality, {stroke_1y:.1f}% stroke/systemic embolism, and {bleeding_1y:.1f}% major bleeding. 2-year risks: {mortality_2y:.1f}% mortality, {stroke_2y:.1f}% stroke/SE, {bleeding_2y:.1f}% bleeding. Consider individualized approach to anticoagulation with careful benefit-risk assessment. Regular follow-up every 3-6 months recommended to monitor clinical status and treatment response."
            }
        else:
            return {
                "stage": "High Risk",
                "description": "High risk requiring intensive management",
                "interpretation": f"High risk profile with 1-year risks of {mortality_1y:.1f}% mortality, {stroke_1y:.1f}% stroke/systemic embolism, and {bleeding_1y:.1f}% major bleeding. 2-year risks: {mortality_2y:.1f}% mortality, {stroke_2y:.1f}% stroke/SE, {bleeding_2y:.1f}% bleeding. Requires intensive management with frequent monitoring (every 1-3 months). Careful consideration of anticoagulation benefits versus bleeding risks essential. Consider specialist consultation for complex decision-making. Optimize management of modifiable risk factors."
            }


def calculate_garfield_af(age: int, weight: float, race: str, sex: str, pulse: int, 
                         diastolic_bp: int, history_of_bleeding: str, heart_failure: str,
                         history_of_stroke: str, chronic_kidney_disease: str, 
                         vascular_disease: str, diabetes_mellitus: str, current_smoking: str,
                         dementia: str, antiplatelet_use: str, carotid_disease: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_garfield_af pattern
    """
    calculator = GarfieldAfCalculator()
    return calculator.calculate(age, weight, race, sex, pulse, diastolic_bp, 
                               history_of_bleeding, heart_failure, history_of_stroke,
                               chronic_kidney_disease, vascular_disease, diabetes_mellitus,
                               current_smoking, dementia, antiplatelet_use, carotid_disease)