"""
European System for Cardiac Operative Risk Evaluation (EuroSCORE) II Calculator

Predicts risk of in-hospital mortality after major cardiac surgery using a logistic regression model
with 18 validated variables from contemporary cardiac surgery data.

References:
1. Nashef SA, Roques F, Sharples LD, Nilsson J, Smith C, Goldstone AR, Lockowandt U. EuroSCORE II. 
   Eur J Cardiothorac Surg. 2012 Apr;41(4):734-44; discussion 744-5. doi: 10.1093/ejcts/ezs043.
2. Roques F, Michel P, Goldstone AR, Nashef SA. The logistic EuroSCORE. Eur Heart J. 2003 May;24(9):881-2. 
   doi: 10.1016/s0195-668x(02)00799-6.
3. Grant SW, Hickey GL, Dimarakis I, Trivedi U, Bryan A, Treasure T, Cooper G, Pagano D, McCollum C, 
   Bridgewater B. How does EuroSCORE II perform in UK cardiac surgery; an analysis of 23 740 patients 
   from the Society for Cardiothoracic Surgery in Great Britain and Ireland National Database. Heart. 
   2012 Dec;98(21):1568-72. doi: 10.1136/heartjnl-2012-302483.
"""

import math
from typing import Dict, Any


class EuroScoreIICalculator:
    """Calculator for European System for Cardiac Operative Risk Evaluation (EuroSCORE) II"""
    
    def __init__(self):
        """Initialize calculator with logistic regression coefficients"""
        # Logistic regression constant
        self.CONSTANT = -5.324537
        
        # Patient-related factors coefficients
        self.COEFFICIENTS = {
            # Age: increases by 1 point per year after 60
            "age": 0.0285181,
            
            # Sex
            "female": 0.2196434,
            
            # Insulin-dependent diabetes
            "insulin_dependent_diabetes": 0.3542749,
            
            # Chronic pulmonary dysfunction
            "chronic_pulmonary_dysfunction": 0.1886564,
            
            # Neurological/musculoskeletal mobility dysfunction
            "mobility_dysfunction": 0.2407181,
            
            # Renal dysfunction (creatinine clearance)
            "creatinine_clearance_51_to_85": 0.303553,
            "creatinine_clearance_50_or_less": 0.8592256,
            "on_dialysis": 0.6421508,
            
            # Critical preoperative state
            "critical_preoperative_state": 1.086517,
            
            # Cardiac-related factors
            # NYHA Class
            "nyha_class_2": 0.1070545,
            "nyha_class_3": 0.2958358,
            "nyha_class_4": 0.5597929,
            
            # CCS Class 4 angina
            "ccs_class_4": 0.2226147,
            
            # Extracardiac arteriopathy
            "extracardiac_arteriopathy": 0.5360268,
            
            # Previous cardiac surgery
            "previous_cardiac_surgery": 1.118599,
            
            # Active endocarditis
            "active_endocarditis": 0.6194522,
            
            # Left ventricular function
            "lv_function_moderate": 0.3150652,
            "lv_function_poor": 0.8084096,
            "lv_function_very_poor": 0.9346919,
            
            # Recent MI ≤90 days
            "recent_mi": 0.1528943,
            
            # Pulmonary hypertension
            "pulmonary_hypertension": 0.1788899,
            
            # Operation-related factors
            # Urgency
            "urgent": 0.3174673,
            "emergency": 0.7039121,
            "salvage": 1.362947,
            
            # Weight of intervention
            "two_procedures": 0.5521478,
            "three_or_more_procedures": 0.9724533,
            
            # Surgery on thoracic aorta
            "surgery_on_thoracic_aorta": 0.6527205
        }
    
    def calculate(self, age_years: int, sex: str, insulin_dependent_diabetes: str,
                 chronic_pulmonary_dysfunction: str, mobility_dysfunction: str,
                 creatinine_clearance: str, critical_preoperative_state: str,
                 nyha_class: str, ccs_class_4: str, extracardiac_arteriopathy: str,
                 previous_cardiac_surgery: str, active_endocarditis: str,
                 left_ventricular_function: str, recent_mi: str, pulmonary_hypertension: str,
                 urgency: str, weight_of_intervention: str, surgery_on_thoracic_aorta: str) -> Dict[str, Any]:
        """
        Calculates EuroSCORE II mortality risk prediction
        
        Args:
            age_years (int): Patient age in years
            sex (str): Patient biological sex (male/female)
            insulin_dependent_diabetes (str): Insulin-dependent diabetes (yes/no)
            chronic_pulmonary_dysfunction (str): Chronic pulmonary dysfunction (yes/no)
            mobility_dysfunction (str): Neurological/musculoskeletal dysfunction (yes/no)
            creatinine_clearance (str): Creatinine clearance category
            critical_preoperative_state (str): Critical preoperative state (yes/no)
            nyha_class (str): NYHA functional class
            ccs_class_4 (str): CCS Class 4 angina (yes/no)
            extracardiac_arteriopathy (str): Extracardiac arteriopathy (yes/no)
            previous_cardiac_surgery (str): Previous cardiac surgery (yes/no)
            active_endocarditis (str): Active endocarditis (yes/no)
            left_ventricular_function (str): LV function category
            recent_mi (str): Recent MI ≤90 days (yes/no)
            pulmonary_hypertension (str): Pulmonary hypertension (yes/no)
            urgency (str): Surgery urgency level
            weight_of_intervention (str): Intervention complexity
            surgery_on_thoracic_aorta (str): Surgery on thoracic aorta (yes/no)
            
        Returns:
            Dict with mortality risk percentage, risk category, and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(age_years, sex, insulin_dependent_diabetes, chronic_pulmonary_dysfunction,
                            mobility_dysfunction, creatinine_clearance, critical_preoperative_state,
                            nyha_class, ccs_class_4, extracardiac_arteriopathy, previous_cardiac_surgery,
                            active_endocarditis, left_ventricular_function, recent_mi,
                            pulmonary_hypertension, urgency, weight_of_intervention, surgery_on_thoracic_aorta)
        
        # Calculate logistic regression score
        y_value = self._calculate_logistic_score(age_years, sex, insulin_dependent_diabetes,
                                               chronic_pulmonary_dysfunction, mobility_dysfunction,
                                               creatinine_clearance, critical_preoperative_state,
                                               nyha_class, ccs_class_4, extracardiac_arteriopathy,
                                               previous_cardiac_surgery, active_endocarditis,
                                               left_ventricular_function, recent_mi, pulmonary_hypertension,
                                               urgency, weight_of_intervention, surgery_on_thoracic_aorta)
        
        # Calculate predicted mortality percentage
        mortality_percentage = self._calculate_mortality_percentage(y_value)
        
        # Get risk category and interpretation
        risk_category = self._get_risk_category(mortality_percentage)
        interpretation = self._get_interpretation(mortality_percentage, risk_category)
        
        return {
            "result": round(mortality_percentage, 2),
            "unit": "percentage",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"],
            "risk_category": risk_category,
            "logistic_score": round(y_value, 4)
        }
    
    def _validate_inputs(self, *args):
        """Validates input parameters"""
        # Basic validation - in a full implementation, would validate each parameter
        if not isinstance(args[0], int) or args[0] < 18 or args[0] > 110:
            raise ValueError("age_years must be an integer between 18 and 110")
        
        # Validate categorical inputs
        valid_binary = ["yes", "no"]
        valid_sex = ["male", "female"]
        valid_creatinine = ["greater_than_85", "51_to_85", "50_or_less", "on_dialysis"]
        valid_nyha = ["class_1", "class_2", "class_3", "class_4"]
        valid_lv_function = ["good_51_or_more", "moderate_31_to_50", "poor_21_to_30", "very_poor_20_or_less"]
        valid_urgency = ["elective", "urgent", "emergency", "salvage"]
        valid_weight = ["single_non_cabg", "two_procedures", "three_or_more_procedures"]
        
        if args[1] not in valid_sex:
            raise ValueError("sex must be 'male' or 'female'")
        if args[5] not in valid_creatinine:
            raise ValueError("creatinine_clearance must be a valid category")
        if args[7] not in valid_nyha:
            raise ValueError("nyha_class must be a valid class")
        if args[12] not in valid_lv_function:
            raise ValueError("left_ventricular_function must be a valid category")
        if args[15] not in valid_urgency:
            raise ValueError("urgency must be a valid level")
        if args[16] not in valid_weight:
            raise ValueError("weight_of_intervention must be a valid category")
    
    def _calculate_logistic_score(self, age_years, sex, insulin_dependent_diabetes,
                                chronic_pulmonary_dysfunction, mobility_dysfunction,
                                creatinine_clearance, critical_preoperative_state,
                                nyha_class, ccs_class_4, extracardiac_arteriopathy,
                                previous_cardiac_surgery, active_endocarditis,
                                left_ventricular_function, recent_mi, pulmonary_hypertension,
                                urgency, weight_of_intervention, surgery_on_thoracic_aorta) -> float:
        """
        Calculates the logistic regression score (y value)
        
        Returns:
            float: Logistic score for mortality calculation
        """
        
        y = self.CONSTANT
        
        # Age contribution (increases per year after 60)
        if age_years > 60:
            y += self.COEFFICIENTS["age"] * (age_years - 60)
        
        # Sex
        if sex == "female":
            y += self.COEFFICIENTS["female"]
        
        # Patient factors
        if insulin_dependent_diabetes == "yes":
            y += self.COEFFICIENTS["insulin_dependent_diabetes"]
        
        if chronic_pulmonary_dysfunction == "yes":
            y += self.COEFFICIENTS["chronic_pulmonary_dysfunction"]
        
        if mobility_dysfunction == "yes":
            y += self.COEFFICIENTS["mobility_dysfunction"]
        
        # Creatinine clearance
        if creatinine_clearance == "51_to_85":
            y += self.COEFFICIENTS["creatinine_clearance_51_to_85"]
        elif creatinine_clearance == "50_or_less":
            y += self.COEFFICIENTS["creatinine_clearance_50_or_less"]
        elif creatinine_clearance == "on_dialysis":
            y += self.COEFFICIENTS["on_dialysis"]
        
        if critical_preoperative_state == "yes":
            y += self.COEFFICIENTS["critical_preoperative_state"]
        
        # Cardiac factors
        if nyha_class == "class_2":
            y += self.COEFFICIENTS["nyha_class_2"]
        elif nyha_class == "class_3":
            y += self.COEFFICIENTS["nyha_class_3"]
        elif nyha_class == "class_4":
            y += self.COEFFICIENTS["nyha_class_4"]
        
        if ccs_class_4 == "yes":
            y += self.COEFFICIENTS["ccs_class_4"]
        
        if extracardiac_arteriopathy == "yes":
            y += self.COEFFICIENTS["extracardiac_arteriopathy"]
        
        if previous_cardiac_surgery == "yes":
            y += self.COEFFICIENTS["previous_cardiac_surgery"]
        
        if active_endocarditis == "yes":
            y += self.COEFFICIENTS["active_endocarditis"]
        
        # Left ventricular function
        if left_ventricular_function == "moderate_31_to_50":
            y += self.COEFFICIENTS["lv_function_moderate"]
        elif left_ventricular_function == "poor_21_to_30":
            y += self.COEFFICIENTS["lv_function_poor"]
        elif left_ventricular_function == "very_poor_20_or_less":
            y += self.COEFFICIENTS["lv_function_very_poor"]
        
        if recent_mi == "yes":
            y += self.COEFFICIENTS["recent_mi"]
        
        if pulmonary_hypertension == "yes":
            y += self.COEFFICIENTS["pulmonary_hypertension"]
        
        # Operation factors
        if urgency == "urgent":
            y += self.COEFFICIENTS["urgent"]
        elif urgency == "emergency":
            y += self.COEFFICIENTS["emergency"]
        elif urgency == "salvage":
            y += self.COEFFICIENTS["salvage"]
        
        if weight_of_intervention == "two_procedures":
            y += self.COEFFICIENTS["two_procedures"]
        elif weight_of_intervention == "three_or_more_procedures":
            y += self.COEFFICIENTS["three_or_more_procedures"]
        
        if surgery_on_thoracic_aorta == "yes":
            y += self.COEFFICIENTS["surgery_on_thoracic_aorta"]
        
        return y
    
    def _calculate_mortality_percentage(self, y_value: float) -> float:
        """
        Calculates mortality percentage from logistic score
        
        Args:
            y_value (float): Logistic regression score
            
        Returns:
            float: Predicted mortality percentage
        """
        
        # Logistic regression formula: P = e^y / (1 + e^y)
        try:
            exp_y = math.exp(y_value)
            probability = exp_y / (1 + exp_y)
            return probability * 100
        except OverflowError:
            # Handle extreme values
            if y_value > 0:
                return 99.99
            else:
                return 0.01
    
    def _get_risk_category(self, mortality_percentage: float) -> str:
        """
        Determines risk category based on mortality percentage
        
        Args:
            mortality_percentage (float): Predicted mortality percentage
            
        Returns:
            str: Risk category
        """
        
        if mortality_percentage < 2:
            return "Low Risk"
        elif mortality_percentage < 5:
            return "Medium Risk"
        elif mortality_percentage < 10:
            return "High Risk"
        else:
            return "Very High Risk"
    
    def _get_interpretation(self, mortality_percentage: float, risk_category: str) -> Dict[str, str]:
        """
        Determines clinical interpretation based on mortality risk
        
        Args:
            mortality_percentage (float): Predicted mortality percentage
            risk_category (str): Risk category
            
        Returns:
            Dict with interpretation details
        """
        
        if risk_category == "Low Risk":
            return {
                "stage": "Low Risk",
                "description": "Low operative risk",
                "interpretation": (
                    f"EuroSCORE II predicted in-hospital mortality: {mortality_percentage:.2f}%. "
                    f"LOW RISK for cardiac surgery. Standard perioperative care and monitoring "
                    f"recommended. Excellent expected outcomes with routine management protocols."
                )
            }
        elif risk_category == "Medium Risk":
            return {
                "stage": "Medium Risk",
                "description": "Medium operative risk",
                "interpretation": (
                    f"EuroSCORE II predicted in-hospital mortality: {mortality_percentage:.2f}%. "
                    f"MEDIUM RISK for cardiac surgery. Enhanced perioperative monitoring and care "
                    f"planning recommended. Consider optimization of modifiable risk factors."
                )
            }
        elif risk_category == "High Risk":
            return {
                "stage": "High Risk",
                "description": "High operative risk",
                "interpretation": (
                    f"EuroSCORE II predicted in-hospital mortality: {mortality_percentage:.2f}%. "
                    f"HIGH RISK for cardiac surgery. Intensive perioperative care, multidisciplinary "
                    f"team approach, and careful risk-benefit assessment recommended. Consider "
                    f"alternative treatments if appropriate."
                )
            }
        else:  # Very High Risk
            return {
                "stage": "Very High Risk",
                "description": "Very high operative risk",
                "interpretation": (
                    f"EuroSCORE II predicted in-hospital mortality: {mortality_percentage:.2f}%. "
                    f"VERY HIGH RISK for cardiac surgery. Requires detailed discussion with patient "
                    f"and family regarding risks and benefits. Consider alternative treatments, "
                    f"intensive perioperative support, and specialized cardiac surgery centers."
                )
            }


def calculate_euroscore_ii(age_years: int, sex: str, insulin_dependent_diabetes: str,
                          chronic_pulmonary_dysfunction: str, mobility_dysfunction: str,
                          creatinine_clearance: str, critical_preoperative_state: str,
                          nyha_class: str, ccs_class_4: str, extracardiac_arteriopathy: str,
                          previous_cardiac_surgery: str, active_endocarditis: str,
                          left_ventricular_function: str, recent_mi: str, pulmonary_hypertension: str,
                          urgency: str, weight_of_intervention: str, surgery_on_thoracic_aorta: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_euroscore_ii pattern
    """
    calculator = EuroScoreIICalculator()
    return calculator.calculate(age_years, sex, insulin_dependent_diabetes, chronic_pulmonary_dysfunction,
                               mobility_dysfunction, creatinine_clearance, critical_preoperative_state,
                               nyha_class, ccs_class_4, extracardiac_arteriopathy, previous_cardiac_surgery,
                               active_endocarditis, left_ventricular_function, recent_mi, pulmonary_hypertension,
                               urgency, weight_of_intervention, surgery_on_thoracic_aorta)