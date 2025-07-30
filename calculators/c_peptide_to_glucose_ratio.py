"""
C-Peptide to Glucose Ratio Calculator

Assesses beta cell secretory function in patients with diabetes/pre-diabetes.

References:
1. Saisho Y. Postprandial C-Peptide to Glucose Ratio as a Marker of β Cell Function: 
   Implication for the Management of Type 2 Diabetes. Int J Mol Sci. 2016 May 6;17(5):744. 
   doi: 10.3390/ijms17050744.
"""

from typing import Dict, Any


class CPeptideToGlucoseRatioCalculator:
    """Calculator for C-Peptide to Glucose Ratio"""
    
    def __init__(self):
        # Interpretation thresholds
        self.SEVERE_DEFICIT_THRESHOLD = 2.0
        self.IMPAIRED_THRESHOLD = 5.0
    
    def calculate(self, c_peptide: float, glucose: float) -> Dict[str, Any]:
        """
        Calculates the C-peptide to glucose ratio
        
        Args:
            c_peptide (float): Serum C-peptide level in ng/mL
            glucose (float): Plasma glucose level in mg/dL
            
        Returns:
            Dict with the ratio and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(c_peptide, glucose)
        
        # Calculate the ratio
        # Formula: CGR = C-peptide (ng/mL) / Glucose (mg/dL) × 100
        ratio = (c_peptide / glucose) * 100
        
        # Get interpretation
        interpretation = self._get_interpretation(ratio)
        
        return {
            "result": round(ratio, 2),
            "unit": "ratio",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"],
            "details": {
                "c_peptide": c_peptide,
                "glucose": glucose,
                "c_peptide_unit": "ng/mL",
                "glucose_unit": "mg/dL"
            }
        }
    
    def _validate_inputs(self, c_peptide: float, glucose: float):
        """Validates input parameters"""
        
        if not isinstance(c_peptide, (int, float)):
            raise ValueError("C-peptide must be a number")
        
        if c_peptide < 0.01 or c_peptide > 50.0:
            raise ValueError("C-peptide must be between 0.01 and 50.0 ng/mL")
        
        if not isinstance(glucose, (int, float)):
            raise ValueError("Glucose must be a number")
        
        if glucose < 10 or glucose > 1000:
            raise ValueError("Glucose must be between 10 and 1000 mg/dL")
    
    def _get_interpretation(self, ratio: float) -> Dict[str, str]:
        """
        Determines the interpretation based on the ratio
        
        Args:
            ratio (float): C-peptide to glucose ratio
            
        Returns:
            Dict with stage, description, and interpretation
        """
        
        if ratio < self.SEVERE_DEFICIT_THRESHOLD:
            return {
                "stage": "Insulin Secretion Deficit",
                "description": "Severe beta cell dysfunction",
                "interpretation": (
                    f"With a C-peptide to glucose ratio of {ratio:.2f}, there is evidence of severe insulin "
                    f"secretion deficit indicating significant beta cell dysfunction. Insulin therapy is "
                    f"necessary for adequate glycemic control. This pattern is commonly seen in Type 1 diabetes, "
                    f"longstanding Type 2 diabetes with beta cell exhaustion, or other forms of diabetes with "
                    f"severe beta cell impairment. Regular monitoring and adjustment of insulin therapy is essential."
                )
            }
        elif ratio < self.IMPAIRED_THRESHOLD:
            return {
                "stage": "Impaired Insulin Secretion",
                "description": "Moderate beta cell dysfunction",
                "interpretation": (
                    f"With a C-peptide to glucose ratio of {ratio:.2f}, there is evidence of impaired endogenous "
                    f"insulin secretion indicating moderate beta cell dysfunction. Management typically requires "
                    f"basal insulin plus other antidiabetic agents. This pattern suggests partial preservation of "
                    f"beta cell function. Consider optimizing non-insulin therapies and lifestyle modifications while "
                    f"monitoring for further deterioration in beta cell function."
                )
            }
        else:
            return {
                "stage": "Preserved Insulin Secretion",
                "description": "Adequate beta cell function",
                "interpretation": (
                    f"With a C-peptide to glucose ratio of {ratio:.2f}, there is evidence of preserved endogenous "
                    f"insulin secretion indicating adequate beta cell function. Insulin therapy is usually unnecessary "
                    f"at this time. Management can typically be achieved with lifestyle modifications and non-insulin "
                    f"antidiabetic agents. This favorable ratio suggests that the pancreatic beta cells retain "
                    f"significant secretory capacity. Continue monitoring to detect any future decline in function."
                )
            }


def calculate_c_peptide_to_glucose_ratio(c_peptide: float, glucose: float) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = CPeptideToGlucoseRatioCalculator()
    return calculator.calculate(c_peptide, glucose)