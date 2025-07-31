"""
Framingham Risk Score for Hard Coronary Heart Disease Calculator

Estimates 10-year risk of myocardial infarction in patients aged 30-79 with no 
history of coronary heart disease or diabetes.

References:
1. Wilson PW, D'Agostino RB, Levy D, Belanger AM, Silbershatz H, Kannel WB. 
   Prediction of coronary heart disease using risk factor categories. Circulation. 
   1998;97(18):1837-47. doi: 10.1161/01.cir.97.18.1837.
2. D'Agostino RB Sr, Vasan RS, Pencina MJ, Wolf PA, Cobain M, Massaro JM, Kannel WB. 
   General cardiovascular risk profile for use in primary care: the Framingham Heart Study. 
   Circulation. 2008;117(6):743-53. doi: 10.1161/CIRCULATIONAHA.107.699579.
3. Expert Panel on Detection, Evaluation, and Treatment of High Blood Cholesterol in Adults. 
   Executive Summary of The Third Report of The National Cholesterol Education Program (NCEP) 
   Expert Panel on Detection, Evaluation, And Treatment of High Blood Cholesterol In Adults 
   (Adult Treatment Panel III). JAMA. 2001;285(19):2486-97. doi: 10.1001/jama.285.19.2486.
"""

from typing import Dict, Any


class FraminghamRiskScoreCalculator:
    """Calculator for Framingham Risk Score for Hard Coronary Heart Disease"""
    
    def __init__(self):
        # Point-based scoring system from Framingham Risk Score
        
        # Age points for men
        self.MALE_AGE_POINTS = [
            (20, 34, -9), (35, 39, -4), (40, 44, 0), (45, 49, 3),
            (50, 54, 6), (55, 59, 8), (60, 64, 10), (65, 69, 11),
            (70, 74, 12), (75, 79, 13)
        ]
        
        # Age points for women  
        self.FEMALE_AGE_POINTS = [
            (20, 34, -7), (35, 39, -3), (40, 44, 0), (45, 49, 3),
            (50, 54, 6), (55, 59, 8), (60, 64, 10), (65, 69, 12),
            (70, 74, 14), (75, 79, 16)
        ]
        
        # Total cholesterol points for men
        self.MALE_CHOL_POINTS = [
            (0, 159, 0), (160, 199, 4), (200, 239, 7), (240, 279, 9), (280, 999, 11)
        ]
        
        # Total cholesterol points for women
        self.FEMALE_CHOL_POINTS = [
            (0, 159, 0), (160, 199, 4), (200, 239, 8), (240, 279, 11), (280, 999, 13)
        ]
        
        # HDL points (same for both sexes)
        self.HDL_POINTS = [
            (60, 999, -1), (50, 59, 0), (40, 49, 1), (0, 39, 2)
        ]
        
        # Systolic BP points for men - untreated
        self.MALE_SBP_UNTREATED_POINTS = [
            (0, 119, 0), (120, 129, 0), (130, 139, 1), (140, 159, 1), (160, 999, 2)
        ]
        
        # Systolic BP points for men - treated
        self.MALE_SBP_TREATED_POINTS = [
            (0, 119, 0), (120, 129, 1), (130, 139, 2), (140, 159, 2), (160, 999, 3)
        ]
        
        # Systolic BP points for women - untreated
        self.FEMALE_SBP_UNTREATED_POINTS = [
            (0, 119, 0), (120, 129, 1), (130, 139, 2), (140, 159, 3), (160, 999, 4)
        ]
        
        # Systolic BP points for women - treated
        self.FEMALE_SBP_TREATED_POINTS = [
            (0, 119, 0), (120, 129, 3), (130, 139, 4), (140, 159, 5), (160, 999, 6)
        ]
        
        # Smoking points
        self.MALE_SMOKING_POINTS = 8
        self.FEMALE_SMOKING_POINTS = 9
        
        # Risk percentage lookup tables based on total points
        self.MALE_RISK_TABLE = {
            -2: 1, -1: 1, 0: 1, 1: 1, 2: 1, 3: 1, 4: 1, 5: 2, 6: 2, 7: 3,
            8: 4, 9: 5, 10: 6, 11: 8, 12: 10, 13: 12, 14: 16, 15: 20, 16: 25, 17: 30
        }
        
        self.FEMALE_RISK_TABLE = {
            -2: 1, -1: 1, 0: 1, 1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 2,
            8: 2, 9: 3, 10: 4, 11: 5, 12: 6, 13: 8, 14: 11, 15: 14, 16: 17, 17: 22,
            18: 27, 19: 30, 20: 30
        }
    
    def calculate(self, age: int, sex: str, total_cholesterol: float, hdl_cholesterol: float,
                  systolic_bp: int, bp_treatment: str, smoking: str) -> Dict[str, Any]:
        """
        Calculates 10-year CHD risk using Framingham Risk Score
        
        Args:
            age (int): Patient age in years (30-79)
            sex (str): Patient sex ("male" or "female")
            total_cholesterol (float): Total cholesterol in mg/dL
            hdl_cholesterol (float): HDL cholesterol in mg/dL
            systolic_bp (int): Systolic blood pressure in mmHg
            bp_treatment (str): Taking BP medication ("yes" or "no")
            smoking (str): Current smoker ("yes" or "no")
            
        Returns:
            Dict with risk percentage and interpretation
        """
        
        # Validations
        self._validate_inputs(age, sex, total_cholesterol, hdl_cholesterol, 
                            systolic_bp, bp_treatment, smoking)
        
        # Calculate risk using point-based system
        risk_percentage = self._calculate_points_risk(age, sex, total_cholesterol, hdl_cholesterol,
                                                     systolic_bp, bp_treatment, smoking)
        
        # Get interpretation
        interpretation = self._get_interpretation(risk_percentage)
        
        return {
            "result": round(risk_percentage, 1),
            "unit": "%",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, age, sex, total_cholesterol, hdl_cholesterol, 
                        systolic_bp, bp_treatment, smoking):
        """Validates input parameters"""
        
        if not isinstance(age, int):
            raise ValueError("Age must be an integer")
        if age < 30 or age > 79:
            raise ValueError("Age must be between 30 and 79 years")
        
        if not isinstance(sex, str) or sex.lower() not in ["male", "female"]:
            raise ValueError("Sex must be 'male' or 'female'")
        
        if not isinstance(total_cholesterol, (int, float)):
            raise ValueError("Total cholesterol must be a number")
        if total_cholesterol < 100 or total_cholesterol > 400:
            raise ValueError("Total cholesterol must be between 100 and 400 mg/dL")
        
        if not isinstance(hdl_cholesterol, (int, float)):
            raise ValueError("HDL cholesterol must be a number")
        if hdl_cholesterol < 20 or hdl_cholesterol > 100:
            raise ValueError("HDL cholesterol must be between 20 and 100 mg/dL")
        
        if not isinstance(systolic_bp, int):
            raise ValueError("Systolic BP must be an integer")
        if systolic_bp < 90 or systolic_bp > 200:
            raise ValueError("Systolic BP must be between 90 and 200 mmHg")
        
        if not isinstance(bp_treatment, str) or bp_treatment.lower() not in ["yes", "no"]:
            raise ValueError("BP treatment must be 'yes' or 'no'")
        
        if not isinstance(smoking, str) or smoking.lower() not in ["yes", "no"]:
            raise ValueError("Smoking must be 'yes' or 'no'")
    
    def _calculate_points_risk(self, age, sex, total_cholesterol, hdl_cholesterol,
                              systolic_bp, bp_treatment, smoking):
        """Implements the Framingham Risk Score point-based calculation"""
        
        # Normalize inputs
        sex = sex.lower()
        bp_treatment = bp_treatment.lower() == "yes"
        smoking = smoking.lower() == "yes"
        
        total_points = 0
        
        # Age points
        if sex == "male":
            total_points += self._get_points_from_range(age, self.MALE_AGE_POINTS)
            chol_points = self._get_points_from_range(total_cholesterol, self.MALE_CHOL_POINTS)
            if bp_treatment:
                bp_points = self._get_points_from_range(systolic_bp, self.MALE_SBP_TREATED_POINTS)
            else:
                bp_points = self._get_points_from_range(systolic_bp, self.MALE_SBP_UNTREATED_POINTS)
            smoking_points = self.MALE_SMOKING_POINTS if smoking else 0
        else:
            total_points += self._get_points_from_range(age, self.FEMALE_AGE_POINTS)
            chol_points = self._get_points_from_range(total_cholesterol, self.FEMALE_CHOL_POINTS)
            if bp_treatment:
                bp_points = self._get_points_from_range(systolic_bp, self.FEMALE_SBP_TREATED_POINTS)
            else:
                bp_points = self._get_points_from_range(systolic_bp, self.FEMALE_SBP_UNTREATED_POINTS)
            smoking_points = self.FEMALE_SMOKING_POINTS if smoking else 0
        
        # Add all point components
        total_points += chol_points
        total_points += self._get_points_from_range(hdl_cholesterol, self.HDL_POINTS)
        total_points += bp_points
        total_points += smoking_points
        
        # Look up risk percentage from points
        if sex == "male":
            risk_percentage = self._get_risk_from_points(total_points, self.MALE_RISK_TABLE)
        else:
            risk_percentage = self._get_risk_from_points(total_points, self.FEMALE_RISK_TABLE)
        
        return risk_percentage
    
    def _get_points_from_range(self, value, range_table):
        """Gets points for a value from a range table"""
        for min_val, max_val, points in range_table:
            if min_val <= value <= max_val:
                return points
        # Default case - return 0 if no range matches
        return 0
    
    def _get_risk_from_points(self, points, risk_table):
        """Gets risk percentage from total points"""
        # Clamp points to table range
        min_points = min(risk_table.keys())
        max_points = max(risk_table.keys())
        
        if points < min_points:
            return risk_table[min_points]
        elif points > max_points:
            return risk_table[max_points] 
        else:
            return risk_table.get(points, risk_table[max_points])
    
    def _get_interpretation(self, risk_percentage: float) -> Dict[str, str]:
        """
        Determines clinical interpretation based on risk percentage
        
        Args:
            risk_percentage (float): Calculated 10-year CHD risk
            
        Returns:
            Dict with interpretation
        """
        
        if risk_percentage < 5:
            return {
                "stage": "Low Risk",
                "description": "Low 10-year CHD risk",
                "interpretation": (f"Low risk with {risk_percentage:.1f}% 10-year risk of hard coronary heart "
                                f"disease events (MI, coronary death). Continue standard preventive measures "
                                f"including healthy lifestyle modifications (diet, exercise, smoking cessation if applicable). "
                                f"Regular monitoring of cardiovascular risk factors recommended.")
            }
        elif risk_percentage < 10:
            return {
                "stage": "Borderline Risk",
                "description": "Borderline 10-year CHD risk", 
                "interpretation": (f"Borderline risk with {risk_percentage:.1f}% 10-year risk of hard coronary heart "
                                f"disease events. Consider additional risk factors and intensive lifestyle modifications "
                                f"(diet, exercise, weight management). May benefit from statin therapy in some cases based "
                                f"on clinical judgment and patient preferences. Consider coronary artery calcium scoring for "
                                f"further risk stratification.")
            }
        elif risk_percentage < 20:
            return {
                "stage": "Intermediate Risk",
                "description": "Intermediate 10-year CHD risk",
                "interpretation": (f"Intermediate risk with {risk_percentage:.1f}% 10-year risk of hard coronary heart "
                                f"disease events. Strong consideration for pharmacotherapy (statins) in addition to "
                                f"intensive lifestyle modifications. Consider additional risk stratification tools if "
                                f"treatment decision uncertain. Target LDL-C <100 mg/dL, consider <70 mg/dL.")
            }
        else:
            return {
                "stage": "High Risk",
                "description": "High 10-year CHD risk",
                "interpretation": (f"High risk with {risk_percentage:.1f}% 10-year risk of hard coronary heart "
                                f"disease events. Definite indication for pharmacotherapy (high-intensity statin) "
                                f"and aggressive risk factor modification. Target LDL-C <70 mg/dL. Consider additional "
                                f"antiplatelet therapy, ACE inhibitors, and other cardioprotective medications as clinically "
                                f"appropriate. Intensive lifestyle counseling and close follow-up recommended.")
            }


def calculate_framingham_risk_score(age: int, sex: str, total_cholesterol: float, 
                                   hdl_cholesterol: float, systolic_bp: int, 
                                   bp_treatment: str, smoking: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_framingham_risk_score pattern
    """
    calculator = FraminghamRiskScoreCalculator()
    return calculator.calculate(age, sex, total_cholesterol, hdl_cholesterol,
                              systolic_bp, bp_treatment, smoking)