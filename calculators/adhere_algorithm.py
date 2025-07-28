"""
ADHERE Algorithm Calculator

The Acute Decompensated Heart Failure National Registry (ADHERE) Algorithm 
is a decision tree-based risk stratification tool that predicts in-hospital 
mortality in patients hospitalized with acute decompensated heart failure.

The algorithm uses three readily available clinical parameters:
- Blood urea nitrogen (BUN)
- Systolic blood pressure (SBP) 
- Serum creatinine

This simple decision tree was derived from analysis of over 65,000 
hospitalizations in the ADHERE registry and provides an effective way 
to risk-stratify heart failure patients at admission.

References:
- Fonarow GC, et al. JAMA. 2005;293(5):572-80.
- Abraham WT, et al. J Am Coll Cardiol. 2008;52(5):347-56.
"""

from typing import Dict, Any


class AdhereAlgorithmCalculator:
    """Calculator for ADHERE Algorithm"""
    
    def __init__(self):
        # Mortality risk ranges based on original ADHERE registry data
        self.MORTALITY_RANGES = {
            0: {
                "stage": "Low Risk",
                "description": "BUN <43 mg/dL",
                "mortality_rate": "2.1-2.3%",
                "interpretation": "Low risk of in-hospital mortality (2.1-2.3%). Standard heart failure management on general medical ward is appropriate. Monitor response to therapy and optimize guideline-directed medical therapy."
            },
            1: {
                "stage": "Intermediate Risk", 
                "description": "BUN ≥43 mg/dL and SBP ≥115 mmHg",
                "mortality_rate": "5.5-6.4%",
                "interpretation": "Intermediate risk of in-hospital mortality (5.5-6.4%). Consider enhanced monitoring on telemetry unit. May benefit from more intensive diuretic therapy and closer hemodynamic monitoring."
            },
            2: {
                "stage": "Intermediate-High Risk",
                "description": "BUN ≥43 mg/dL, SBP <115 mmHg, and creatinine <2.75 mg/dL", 
                "mortality_rate": "12.4-12.8%",
                "interpretation": "Intermediate-high risk of in-hospital mortality (12.4-12.8%). Consider intensive care unit monitoring or step-down unit care. May require inotropic support and aggressive hemodynamic optimization."
            },
            3: {
                "stage": "High Risk",
                "description": "BUN ≥43 mg/dL, SBP <115 mmHg, and creatinine ≥2.75 mg/dL",
                "mortality_rate": "19.8-21.9%", 
                "interpretation": "High risk of in-hospital mortality (19.8-21.9%). Strong consideration for intensive care unit admission. Likely requires inotropic support, aggressive diuresis, and consideration of advanced heart failure therapies or mechanical circulatory support."
            }
        }
    
    def calculate(self, bun: str, systolic_bp: str, creatinine: str) -> Dict[str, Any]:
        """
        Calculates the ADHERE Algorithm risk category using the provided parameters
        
        Args:
            bun (str): Blood urea nitrogen level ("under_43" or "43_or_over")
            systolic_bp (str): Systolic blood pressure ("115_or_over" or "under_115")
            creatinine (str): Serum creatinine level ("under_2_75" or "2_75_or_over")
            
        Returns:
            Dict with the risk category and clinical interpretation
        """
        
        # Validate inputs
        self._validate_inputs(bun, systolic_bp, creatinine)
        
        # Apply decision tree logic
        risk_level = self._apply_decision_tree(bun, systolic_bp, creatinine)
        
        # Get interpretation
        interpretation_data = self._get_interpretation(risk_level)
        
        return {
            "result": risk_level,
            "unit": "risk_level",
            "interpretation": interpretation_data["interpretation"],
            "stage": interpretation_data["stage"],
            "stage_description": interpretation_data["description"]
        }
    
    def _validate_inputs(self, bun: str, systolic_bp: str, creatinine: str):
        """Validates input parameters"""
        
        # Validate BUN
        if not isinstance(bun, str) or bun not in ["under_43", "43_or_over"]:
            raise ValueError("BUN must be 'under_43' or '43_or_over'")
        
        # Validate systolic BP
        if not isinstance(systolic_bp, str) or systolic_bp not in ["115_or_over", "under_115"]:
            raise ValueError("Systolic BP must be '115_or_over' or 'under_115'")
        
        # Validate creatinine
        if not isinstance(creatinine, str) or creatinine not in ["under_2_75", "2_75_or_over"]:
            raise ValueError("Creatinine must be 'under_2_75' or '2_75_or_over'")
    
    def _apply_decision_tree(self, bun: str, systolic_bp: str, creatinine: str) -> int:
        """
        Applies the ADHERE decision tree algorithm
        
        Decision tree logic:
        1. If BUN <43 mg/dL → Low Risk (0)
        2. If BUN ≥43 mg/dL and SBP ≥115 mmHg → Intermediate Risk (1)
        3. If BUN ≥43 mg/dL, SBP <115 mmHg, and creatinine <2.75 mg/dL → Intermediate-High Risk (2)
        4. If BUN ≥43 mg/dL, SBP <115 mmHg, and creatinine ≥2.75 mg/dL → High Risk (3)
        
        Args:
            bun (str): Blood urea nitrogen level
            systolic_bp (str): Systolic blood pressure
            creatinine (str): Serum creatinine level
            
        Returns:
            int: Risk level (0-3)
        """
        
        # Step 1: Check BUN
        if bun == "under_43":
            return 0  # Low Risk
        
        # BUN ≥43 mg/dL, continue to Step 2
        # Step 2: Check systolic BP
        if systolic_bp == "115_or_over":
            return 1  # Intermediate Risk
        
        # BUN ≥43 mg/dL and SBP <115 mmHg, continue to Step 3
        # Step 3: Check creatinine
        if creatinine == "under_2_75":
            return 2  # Intermediate-High Risk
        else:
            return 3  # High Risk
    
    def _get_interpretation(self, risk_level: int) -> Dict[str, str]:
        """
        Determines the clinical interpretation based on the risk level
        
        Args:
            risk_level (int): Calculated risk level (0-3)
            
        Returns:
            Dict with interpretation details
        """
        
        if risk_level not in self.MORTALITY_RANGES:
            raise ValueError(f"Invalid risk level: {risk_level}")
        
        return self.MORTALITY_RANGES[risk_level]


def calculate_adhere_algorithm(bun: str, systolic_bp: str, creatinine: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_adhere_algorithm pattern
    """
    calculator = AdhereAlgorithmCalculator()
    return calculator.calculate(bun, systolic_bp, creatinine)