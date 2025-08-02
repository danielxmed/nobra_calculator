"""
Modified Fisher Grading Scale for Subarachnoid Hemorrhage (SAH) Calculator

States severity of aneurysmal subarachnoid hemorrhage based on amount and type 
of blood on CT with associated risk of vasospasm. The modified Fisher scale 
provides better prediction of symptomatic vasospasm than the original Fisher scale.

References:
1. Frontera JA, et al. Neurosurgery. 2006;59(1):21-7.
2. Claassen J, et al. Stroke. 2001;32(9):2012-20.
3. Fisher CM, et al. Neurosurgery. 1980;6(1):1-9.
"""

from typing import Dict, Any


class ModifiedFisherGradingScaleCalculator:
    """Calculator for Modified Fisher Grading Scale for Subarachnoid Hemorrhage"""
    
    def __init__(self):
        # Vasospasm risk ranges by grade (percentages)
        self.VASOSPASM_RISK = {
            0: "0%",
            1: "6-24%",
            2: "15-33%",
            3: "33-35%",
            4: "34-40%"
        }
    
    def calculate(self, sah_thickness: str, ivh_present: str) -> Dict[str, Any]:
        """
        Calculates the Modified Fisher Grade for subarachnoid hemorrhage
        
        Args:
            sah_thickness (str): SAH thickness - "none", "thin" (<1mm), or "thick" (≥1mm)
            ivh_present (str): Presence of intraventricular hemorrhage - "yes" or "no"
            
        Returns:
            Dict with Modified Fisher grade and vasospasm risk interpretation
        """
        
        # Validate inputs
        self._validate_inputs(sah_thickness, ivh_present)
        
        # Calculate Modified Fisher grade
        grade = self._calculate_grade(sah_thickness, ivh_present)
        
        # Get interpretation
        interpretation = self._get_interpretation(grade)
        
        return {
            "result": grade,
            "unit": "grade",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, sah_thickness: str, ivh_present: str):
        """Validates input parameters"""
        
        valid_sah_thickness = ["none", "thin", "thick"]
        valid_ivh_present = ["yes", "no"]
        
        if sah_thickness not in valid_sah_thickness:
            raise ValueError(f"sah_thickness must be one of: {', '.join(valid_sah_thickness)}")
        
        if ivh_present not in valid_ivh_present:
            raise ValueError(f"ivh_present must be one of: {', '.join(valid_ivh_present)}")
    
    def _calculate_grade(self, sah_thickness: str, ivh_present: str) -> int:
        """
        Calculates Modified Fisher grade based on SAH thickness and IVH presence
        
        Grading Logic:
        - Grade 0: No SAH present
        - Grade 1: Thin SAH (<1mm), no IVH
        - Grade 2: Thin SAH (<1mm), with IVH
        - Grade 3: Thick SAH (≥1mm), no IVH
        - Grade 4: Thick SAH (≥1mm), with IVH
        """
        
        # Grade 0: No SAH
        if sah_thickness == "none":
            return 0
        
        # Grade 1: Thin SAH, no IVH
        if sah_thickness == "thin" and ivh_present == "no":
            return 1
        
        # Grade 2: Thin SAH, with IVH
        if sah_thickness == "thin" and ivh_present == "yes":
            return 2
        
        # Grade 3: Thick SAH, no IVH
        if sah_thickness == "thick" and ivh_present == "no":
            return 3
        
        # Grade 4: Thick SAH, with IVH
        if sah_thickness == "thick" and ivh_present == "yes":
            return 4
        
        # This should never be reached with proper validation
        raise ValueError("Invalid combination of parameters")
    
    def _get_interpretation(self, grade: int) -> Dict[str, str]:
        """
        Provides clinical interpretation based on Modified Fisher grade
        
        Args:
            grade: Modified Fisher grade (0-4)
            
        Returns:
            Dict with interpretation details including vasospasm risk
        """
        
        interpretations = {
            0: {
                "stage": "Grade 0",
                "description": "No SAH present",
                "interpretation": (f"Modified Fisher Grade {grade}: No subarachnoid hemorrhage detected on CT scan. "
                                f"Vasospasm risk: {self.VASOSPASM_RISK[grade]}. No specific SAH monitoring required, "
                                f"but continue evaluation for other causes of symptoms.")
            },
            1: {
                "stage": "Grade 1",
                "description": "Focal/thin SAH, no IVH",
                "interpretation": (f"Modified Fisher Grade {grade}: Focal or diffuse thin subarachnoid hemorrhage "
                                f"(<1mm thickness) without intraventricular hemorrhage. Vasospasm risk: "
                                f"{self.VASOSPASM_RISK[grade]}. Low risk for delayed cerebral ischemia. Standard "
                                f"monitoring protocols recommended.")
            },
            2: {
                "stage": "Grade 2",
                "description": "Focal/thin SAH with IVH",
                "interpretation": (f"Modified Fisher Grade {grade}: Focal or diffuse thin subarachnoid hemorrhage "
                                f"(<1mm thickness) with intraventricular hemorrhage. Vasospasm risk: "
                                f"{self.VASOSPASM_RISK[grade]}. Moderate risk for delayed cerebral ischemia. "
                                f"Consider enhanced monitoring and nimodipine prophylaxis.")
            },
            3: {
                "stage": "Grade 3",
                "description": "Focal/thick SAH, no IVH",
                "interpretation": (f"Modified Fisher Grade {grade}: Focal or diffuse thick subarachnoid hemorrhage "
                                f"(≥1mm thickness) without intraventricular hemorrhage. Vasospasm risk: "
                                f"{self.VASOSPASM_RISK[grade]}. High risk for delayed cerebral ischemia. "
                                f"Intensive monitoring, nimodipine prophylaxis, and consideration of angiographic "
                                f"surveillance recommended.")
            },
            4: {
                "stage": "Grade 4",
                "description": "Focal/thick SAH with IVH",
                "interpretation": (f"Modified Fisher Grade {grade}: Focal or diffuse thick subarachnoid hemorrhage "
                                f"(≥1mm thickness) with intraventricular hemorrhage. Vasospasm risk: "
                                f"{self.VASOSPASM_RISK[grade]}. Highest risk for delayed cerebral ischemia. "
                                f"Intensive monitoring, nimodipine prophylaxis, frequent neurological assessments, "
                                f"and consideration of angiographic surveillance strongly recommended.")
            }
        }
        
        return interpretations.get(grade, {
            "stage": f"Grade {grade}",
            "description": "Unknown grade",
            "interpretation": f"Unknown Modified Fisher grade: {grade}"
        })


def calculate_modified_fisher_grading_scale(sah_thickness: str, ivh_present: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = ModifiedFisherGradingScaleCalculator()
    return calculator.calculate(sah_thickness, ivh_present)