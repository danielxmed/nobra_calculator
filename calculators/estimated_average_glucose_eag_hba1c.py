"""
Estimated Average Glucose (eAG) From HbA1C Calculator

Estimates average glucose level from Hemoglobin A1C value using the linear 
relationship established by the A1c-Derived Average Glucose (ADAG) Study Group.

The formula eAG (mg/dL) = (28.7 × HbA1c %) - 46.7 provides a way to translate
HbA1c values into estimated average glucose levels that correspond to everyday
glucose meter readings.

References:
1. Nathan DM, Kuenen J, Borg R, Zheng H, Schoenfeld D, Heine RJ. Translating 
   the A1C assay into estimated average glucose values. Diabetes Care. 
   2008;31(8):1473-8.
2. American Diabetes Association. 6. Glycemic Targets: Standards of Medical 
   Care in Diabetes-2021. Diabetes Care. 2021;44(Suppl 1):S73-S84.
"""

from typing import Dict, Any


class EstimatedAverageGlucoseEagHba1cCalculator:
    """Calculator for Estimated Average Glucose (eAG) From HbA1C"""
    
    def __init__(self):
        # Formula constants from ADAG Study Group
        self.MULTIPLIER = 28.7
        self.CONSTANT = 46.7
        
        # Glucose range thresholds (mg/dL)
        self.NORMAL_THRESHOLD = 125
        self.PREDIABETES_THRESHOLD = 153
        self.GOOD_CONTROL_THRESHOLD = 182
        self.MODERATE_CONTROL_THRESHOLD = 239
    
    def calculate(self, hba1c_percent: float) -> Dict[str, Any]:
        """
        Calculates estimated average glucose from HbA1c percentage
        
        Args:
            hba1c_percent (float): HbA1c value as percentage (3.0-20.0)
            
        Returns:
            Dict with the result and interpretation
        """
        
        # Validations
        self._validate_inputs(hba1c_percent)
        
        # Calculate eAG using the ADAG formula
        eag_mg_dl = self._calculate_eag(hba1c_percent)
        
        # Get clinical interpretation
        interpretation = self._get_interpretation(eag_mg_dl, hba1c_percent)
        
        return {
            "result": round(eag_mg_dl, 1),
            "unit": "mg/dL",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, hba1c_percent):
        """Validates input parameters"""
        
        if not isinstance(hba1c_percent, (int, float)):
            raise ValueError("HbA1c must be a number")
        
        if hba1c_percent < 3.0 or hba1c_percent > 20.0:
            raise ValueError("HbA1c must be between 3.0% and 20.0%")
    
    def _calculate_eag(self, hba1c_percent: float) -> float:
        """
        Calculates estimated average glucose using the ADAG formula
        
        Formula: eAG (mg/dL) = (28.7 × HbA1c %) - 46.7
        """
        
        eag = (self.MULTIPLIER * hba1c_percent) - self.CONSTANT
        return eag
    
    def _get_interpretation(self, eag_mg_dl: float, hba1c_percent: float) -> Dict[str, str]:
        """
        Determines the clinical interpretation based on eAG and HbA1c values
        
        Args:
            eag_mg_dl (float): Estimated average glucose in mg/dL
            hba1c_percent (float): HbA1c percentage
            
        Returns:
            Dict with interpretation details
        """
        
        if eag_mg_dl <= self.NORMAL_THRESHOLD:
            return {
                "stage": "Normal",
                "description": "Normal glucose levels",
                "interpretation": f"Estimated average glucose is within normal range. HbA1c {hba1c_percent:.1f}% indicates normal glucose metabolism. Continue healthy lifestyle habits including regular physical activity, balanced diet, and weight management. Regular monitoring may be appropriate based on individual risk factors."
            }
        elif eag_mg_dl <= self.PREDIABETES_THRESHOLD:
            return {
                "stage": "Prediabetes",
                "description": "Prediabetic range",
                "interpretation": f"Estimated average glucose suggests prediabetes (HbA1c {hba1c_percent:.1f}%). This indicates increased risk of developing type 2 diabetes. Lifestyle interventions including weight loss, increased physical activity, and dietary modifications are recommended. Regular monitoring and diabetes prevention programs may be beneficial."
            }
        elif eag_mg_dl <= self.GOOD_CONTROL_THRESHOLD:
            return {
                "stage": "Diabetes - Good Control",
                "description": "Diabetic range with good control",
                "interpretation": f"Estimated average glucose indicates diabetes (HbA1c {hba1c_percent:.1f}%) with relatively good glycemic control. The American Diabetes Association suggests target HbA1c <7% (eAG <154 mg/dL) for most nonpregnant adults with diabetes. Continue current diabetes management plan with regular monitoring and healthcare provider follow-up."
            }
        elif eag_mg_dl <= self.MODERATE_CONTROL_THRESHOLD:
            return {
                "stage": "Diabetes - Moderate Control",
                "description": "Diabetic range with moderate control",
                "interpretation": f"Estimated average glucose indicates diabetes with moderate glycemic control (HbA1c {hba1c_percent:.1f}%). Consider intensification of diabetes management including medication adjustment, lifestyle modification, diabetes education, and more frequent monitoring. Work with healthcare provider to optimize treatment plan."
            }
        else:
            return {
                "stage": "Diabetes - Poor Control",
                "description": "Diabetic range with poor control",
                "interpretation": f"Estimated average glucose indicates diabetes with poor glycemic control (HbA1c {hba1c_percent:.1f}%). Immediate intensification of diabetes management is recommended. This may include insulin therapy, comprehensive medication review, diabetes education, and frequent monitoring. Risk of diabetic complications is significantly increased. Urgent consultation with endocrinologist or diabetes specialist may be appropriate."
            }


def calculate_estimated_average_glucose_eag_hba1c(hba1c_percent: float) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_estimated_average_glucose_eag_hba1c pattern
    """
    calculator = EstimatedAverageGlucoseEagHba1cCalculator()
    return calculator.calculate(hba1c_percent)