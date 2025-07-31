"""
Fisher Grading Scale for Subarachnoid Hemorrhage (SAH) Calculator

Assesses risk of vasospasm in SAH based on amount and distribution of blood on CT.

References:
- Fisher CM, et al. Neurosurgery. 1980;6(1):1-9.
- Kistler JP, et al. Neurology. 1983;33(4):424-36.
"""

from typing import Dict, Any


class FisherGradingScaleCalculator:
    """Calculator for Fisher Grading Scale for SAH"""
    
    def __init__(self):
        # Define grade mapping based on CT findings
        self.GRADE_MAPPING = {
            "no_sah": 1,              # Grade I: No SAH detected
            "diffuse_thin": 2,        # Grade II: Diffuse or vertical layer <1mm
            "localized_thick": 3,     # Grade III: Localized clot or layer >1mm
            "ich_ivh": 4             # Grade IV: ICH or IVH with diffuse or no SAH
        }
        
        # Vasospasm risk ranges by grade
        self.VASOSPASM_RISK = {
            1: {"min": 0, "max": 21, "description": "Low risk"},
            2: {"min": 0, "max": 25, "description": "Low risk"},
            3: {"min": 23, "max": 96, "description": "Low to high risk"},
            4: {"min": 0, "max": 35, "description": "Low to moderate risk"}
        }
    
    def calculate(self, ct_findings: str) -> Dict[str, Any]:
        """
        Calculates the Fisher Grade based on CT findings
        
        Args:
            ct_findings: CT scan findings (no_sah, diffuse_thin, localized_thick, ich_ivh)
            
        Returns:
            Dict with the grade and interpretation
        """
        
        # Validate input
        self._validate_inputs(ct_findings)
        
        # Get Fisher grade
        grade = self.GRADE_MAPPING[ct_findings]
        
        # Get interpretation
        interpretation = self._get_interpretation(grade, ct_findings)
        
        return {
            "result": grade,
            "unit": "",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, ct_findings: str):
        """Validates input parameters"""
        
        if ct_findings not in self.GRADE_MAPPING:
            raise ValueError(f"Invalid CT findings. Must be one of: {list(self.GRADE_MAPPING.keys())}")
    
    def _get_interpretation(self, grade: int, ct_findings: str) -> Dict[str, str]:
        """
        Determines the interpretation based on the Fisher grade
        
        Args:
            grade: Calculated Fisher grade (1-4)
            ct_findings: Original CT findings for detailed description
            
        Returns:
            Dict with interpretation
        """
        
        risk = self.VASOSPASM_RISK[grade]
        risk_range = f"{risk['min']}-{risk['max']}%"
        
        if grade == 1:
            return {
                "stage": "Grade I",
                "description": "No SAH detected",
                "interpretation": f"Low risk of vasospasm ({risk_range}). No blood visualized on non-contrast head CT"
            }
        elif grade == 2:
            return {
                "stage": "Grade II",
                "description": "Diffuse or vertical layer <1mm thick",
                "interpretation": f"Low risk of vasospasm ({risk_range}). Diffuse deposition or thin layer with vertical layers of blood less than 1mm thick"
            }
        elif grade == 3:
            return {
                "stage": "Grade III",
                "description": "Localized clot or layer >1mm thick",
                "interpretation": f"Low to high risk of vasospasm ({risk_range}). Localized clots and/or vertical layers of blood 1mm or greater in thickness"
            }
        else:  # grade == 4
            return {
                "stage": "Grade IV",
                "description": "ICH or IVH with diffuse or no SAH",
                "interpretation": f"Low to moderate risk of vasospasm ({risk_range}). Intracerebral or intraventricular hemorrhage with diffuse or no subarachnoid blood"
            }


def calculate_fisher_grading_scale(ct_findings: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_fisher_grading_scale pattern
    """
    calculator = FisherGradingScaleCalculator()
    return calculator.calculate(ct_findings)