"""
LDL Calculated Calculator

Calculates LDL cholesterol using the Friedewald formula based on total cholesterol, 
HDL cholesterol, and triglycerides. This widely-used formula provides an estimated 
LDL cholesterol level when direct measurement is not available, helping healthcare 
providers assess cardiovascular risk and guide lipid management.

References:
1. Friedewald WT, Levy RI, Fredrickson DS. Estimation of the concentration of low-density 
   lipoprotein cholesterol in plasma, without use of the preparative ultracentrifuge. 
   Clin Chem. 1972 Jun;18(6):499-502.
2. National Cholesterol Education Program (NCEP) Expert Panel on Detection, Evaluation, 
   and Treatment of High Blood Cholesterol in Adults (Adult Treatment Panel III). 
   Third Report of the National Cholesterol Education Program (NCEP) Expert Panel on 
   Detection, Evaluation, and Treatment of High Blood Cholesterol in Adults (Adult 
   Treatment Panel III) final report. Circulation. 2002 Dec 17;106(25):3143-421.
"""

from typing import Dict, Any


class LdlCalculatedCalculator:
    """Calculator for LDL Cholesterol using Friedewald Formula"""
    
    def __init__(self):
        """Initialize LDL interpretation thresholds and parameters"""
        
        # LDL cholesterol interpretation thresholds (mg/dL)
        self.optimal_threshold = 100
        self.near_optimal_threshold = 130
        self.borderline_high_threshold = 160
        self.high_threshold = 190
        
        # Risk-based LDL targets (mg/dL)
        self.very_high_risk_target = 70
        self.high_risk_target = 100
        self.moderate_risk_target = 130
        self.lower_risk_target = 160
        
        # Formula validation limits
        self.triglyceride_accuracy_limit = 400  # mg/dL - above this, formula is inaccurate
        self.triglyceride_low_limit = 100  # mg/dL - below this, may underestimate LDL
    
    def calculate(self, total_cholesterol: float, hdl_cholesterol: float, 
                 triglycerides: float) -> Dict[str, Any]:
        """
        Calculates LDL cholesterol using the Friedewald formula
        
        Args:
            total_cholesterol (float): Total cholesterol in mg/dL
            hdl_cholesterol (float): HDL cholesterol in mg/dL
            triglycerides (float): Triglycerides in mg/dL (fasting required)
            
        Returns:
            Dict with LDL cholesterol calculation and clinical interpretation
        """
        
        # Validate inputs
        self._validate_inputs(total_cholesterol, hdl_cholesterol, triglycerides)
        
        # Calculate LDL using Friedewald formula
        ldl_cholesterol = self._calculate_friedewald_ldl(
            total_cholesterol, hdl_cholesterol, triglycerides
        )
        
        # Assess accuracy limitations
        accuracy_assessment = self._assess_accuracy(triglycerides, ldl_cholesterol)
        
        # Get LDL interpretation
        ldl_interpretation = self._interpret_ldl_level(ldl_cholesterol)
        
        # Generate comprehensive interpretation
        interpretation = self._generate_interpretation(
            ldl_cholesterol, ldl_interpretation, accuracy_assessment, 
            total_cholesterol, hdl_cholesterol, triglycerides
        )
        
        return {
            "result": ldl_cholesterol,
            "unit": "mg/dL",
            "interpretation": interpretation,
            "stage": ldl_interpretation["stage"],
            "stage_description": ldl_interpretation["description"]
        }
    
    def _validate_inputs(self, total_cholesterol: float, hdl_cholesterol: float, 
                        triglycerides: float):
        """Validates input parameters"""
        
        if not isinstance(total_cholesterol, (int, float)) or total_cholesterol <= 0:
            raise ValueError("Total cholesterol must be a positive number")
        
        if not isinstance(hdl_cholesterol, (int, float)) or hdl_cholesterol <= 0:
            raise ValueError("HDL cholesterol must be a positive number")
        
        if not isinstance(triglycerides, (int, float)) or triglycerides <= 0:
            raise ValueError("Triglycerides must be a positive number")
        
        # Clinical validation ranges
        if total_cholesterol < 50 or total_cholesterol > 1000:
            raise ValueError("Total cholesterol should be between 50-1000 mg/dL")
        
        if hdl_cholesterol < 10 or hdl_cholesterol > 200:
            raise ValueError("HDL cholesterol should be between 10-200 mg/dL")
        
        if triglycerides < 30 or triglycerides > 5000:
            raise ValueError("Triglycerides should be between 30-5000 mg/dL")
        
        # Logical validation
        if hdl_cholesterol >= total_cholesterol:
            raise ValueError("HDL cholesterol cannot be greater than or equal to total cholesterol")
    
    def _calculate_friedewald_ldl(self, total_cholesterol: float, hdl_cholesterol: float, 
                                 triglycerides: float) -> float:
        """
        Calculates LDL cholesterol using Friedewald formula
        
        Formula: LDL = Total Cholesterol - HDL Cholesterol - (Triglycerides/5)
        
        Args:
            total_cholesterol (float): Total cholesterol in mg/dL
            hdl_cholesterol (float): HDL cholesterol in mg/dL
            triglycerides (float): Triglycerides in mg/dL
            
        Returns:
            float: Calculated LDL cholesterol in mg/dL
        """
        
        # Friedewald formula
        ldl_cholesterol = total_cholesterol - hdl_cholesterol - (triglycerides / 5.0)
        
        # Round to one decimal place
        return round(ldl_cholesterol, 1)
    
    def _assess_accuracy(self, triglycerides: float, ldl_cholesterol: float) -> Dict[str, Any]:
        """
        Assesses accuracy limitations of the Friedewald formula
        
        Args:
            triglycerides (float): Triglyceride level
            ldl_cholesterol (float): Calculated LDL cholesterol
            
        Returns:
            Dict with accuracy assessment
        """
        
        accuracy_issues = []
        accuracy_level = "High"
        
        # Check triglyceride limitations
        if triglycerides > self.triglyceride_accuracy_limit:
            accuracy_issues.append("Triglycerides >400 mg/dL - formula inaccurate")
            accuracy_level = "Poor"
        elif triglycerides > 200:
            if ldl_cholesterol < 70:
                accuracy_issues.append("May underestimate LDL at triglycerides >200 mg/dL and LDL <70 mg/dL")
                accuracy_level = "Moderate"
            elif ldl_cholesterol > 130:
                accuracy_issues.append("May overestimate LDL at triglycerides >200 mg/dL and LDL >130 mg/dL")
                accuracy_level = "Moderate"
        
        if triglycerides < self.triglyceride_low_limit:
            accuracy_issues.append("May underestimate LDL when triglycerides <100 mg/dL")
            accuracy_level = "Moderate" if accuracy_level == "High" else accuracy_level
        
        return {
            "accuracy_level": accuracy_level,
            "issues": accuracy_issues,
            "recommend_direct_measurement": triglycerides > self.triglyceride_accuracy_limit
        }
    
    def _interpret_ldl_level(self, ldl_cholesterol: float) -> Dict[str, str]:
        """
        Interprets LDL cholesterol level according to clinical guidelines
        
        Args:
            ldl_cholesterol (float): LDL cholesterol level
            
        Returns:
            Dict with LDL interpretation
        """
        
        if ldl_cholesterol < self.optimal_threshold:
            return {
                "stage": "Optimal",
                "description": "Optimal LDL cholesterol",
                "risk_category": "Low"
            }
        elif ldl_cholesterol < self.near_optimal_threshold:
            return {
                "stage": "Near Optimal",
                "description": "Near optimal/above optimal LDL cholesterol",
                "risk_category": "Low-Moderate"
            }
        elif ldl_cholesterol < self.borderline_high_threshold:
            return {
                "stage": "Borderline High",
                "description": "Borderline high LDL cholesterol",
                "risk_category": "Moderate"
            }
        elif ldl_cholesterol < self.high_threshold:
            return {
                "stage": "High",
                "description": "High LDL cholesterol",
                "risk_category": "High"
            }
        else:
            return {
                "stage": "Very High",
                "description": "Very high LDL cholesterol",
                "risk_category": "Very High"
            }
    
    def _generate_interpretation(self, ldl_cholesterol: float, ldl_interpretation: Dict,
                               accuracy_assessment: Dict, total_cholesterol: float,
                               hdl_cholesterol: float, triglycerides: float) -> str:
        """
        Generates comprehensive clinical interpretation
        
        Args:
            ldl_cholesterol (float): Calculated LDL cholesterol
            ldl_interpretation (Dict): LDL level interpretation
            accuracy_assessment (Dict): Formula accuracy assessment
            total_cholesterol, hdl_cholesterol, triglycerides (float): Input values
            
        Returns:
            str: Detailed clinical interpretation
        """
        
        # Base interpretation
        interpretation = (
            f"Calculated LDL cholesterol: {ldl_cholesterol} mg/dL using Friedewald formula "
            f"(Total cholesterol {total_cholesterol} - HDL {hdl_cholesterol} - Triglycerides/5 [{triglycerides}/5]). "
        )
        
        # Add LDL level interpretation
        interpretation += f"LDL level is {ldl_interpretation['stage'].lower()}. "
        
        # Clinical recommendations based on LDL level
        if ldl_cholesterol < 100:
            interpretation += (
                "Excellent LDL level. Continue heart-healthy lifestyle practices including "
                "diet, regular physical activity, and weight management. "
            )
        elif ldl_cholesterol < 130:
            interpretation += (
                "Consider lifestyle modifications including heart-healthy diet, regular exercise, "
                "and weight management. Assess overall cardiovascular risk factors. "
            )
        elif ldl_cholesterol < 160:
            interpretation += (
                "Lifestyle modifications strongly recommended. Consider medication therapy "
                "based on overall cardiovascular risk assessment and patient factors. "
            )
        elif ldl_cholesterol < 190:
            interpretation += (
                "High LDL level requiring intervention. Intensive lifestyle modifications "
                "and likely medication therapy indicated. Comprehensive cardiovascular risk assessment recommended. "
            )
        else:
            interpretation += (
                "Very high LDL level requiring immediate attention. Medication therapy strongly "
                "recommended along with intensive lifestyle modifications. Consider evaluation "
                "for familial hypercholesterolemia. "
            )
        
        # Add accuracy considerations
        if accuracy_assessment["accuracy_level"] != "High":
            interpretation += f"Formula accuracy: {accuracy_assessment['accuracy_level']}. "
            for issue in accuracy_assessment["issues"]:
                interpretation += f"{issue}. "
        
        if accuracy_assessment["recommend_direct_measurement"]:
            interpretation += "Direct LDL measurement recommended for accurate assessment. "
        
        # Add risk-based targets
        interpretation += (
            "LDL targets vary by cardiovascular risk: <70 mg/dL (very high risk), "
            "<100 mg/dL (high risk), <130 mg/dL (moderate risk), <160 mg/dL (lower risk). "
        )
        
        # Additional clinical notes
        interpretation += (
            "This calculation requires fasting triglycerides for accuracy. "
            "Results should be interpreted in context of overall cardiovascular risk assessment "
            "including other lipid parameters, blood pressure, diabetes, smoking status, and family history."
        )
        
        return interpretation


def calculate_ldl_calculated(total_cholesterol, hdl_cholesterol, triglycerides) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = LdlCalculatedCalculator()
    return calculator.calculate(total_cholesterol, hdl_cholesterol, triglycerides)