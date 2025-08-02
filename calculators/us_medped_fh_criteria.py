"""
US (MEDPED) Diagnostic Criteria for Familial Hypercholesterolemia (FH) Calculator

Diagnoses familial hypercholesterolemia using age-specific total cholesterol cutoff values 
that vary based on family history of FH.

References:
1. Williams RR, Hunt SC, Schumacher MC, et al. Diagnosing heterozygous familial 
   hypercholesterolemia using new practical criteria focused on the family history. 
   Am J Cardiol. 1993;72(2):171-176.
2. Stone NJ, Levy RI, Fredrickson DS, Verter J. Coronary artery disease in 116 kindred 
   with familial type II hyperlipoproteinemia. Circulation. 1974;49(3):476-488.
"""

from typing import Dict, Any


class UsMedpedFhCriteriaCalculator:
    """Calculator for US (MEDPED) Diagnostic Criteria for Familial Hypercholesterolemia"""
    
    def __init__(self):
        # MEDPED cholesterol cutoff matrix: [age_group][family_history] = cutoff_mg_dl
        # Age groups: <20, 20-29, 30-39, ≥40
        # Family history: none (general population), 1st_degree, 2nd_degree, 3rd_degree
        self.CHOLESTEROL_CUTOFFS = {
            "under_20": {
                "none": 270,
                "1st_degree": 220,
                "2nd_degree": 230,
                "3rd_degree": 240
            },
            "20_to_29": {
                "none": 290,
                "1st_degree": 240,
                "2nd_degree": 250,
                "3rd_degree": 260
            },
            "30_to_39": {
                "none": 340,
                "1st_degree": 270,
                "2nd_degree": 280,
                "3rd_degree": 290
            },
            "40_and_over": {
                "none": 360,
                "1st_degree": 290,
                "2nd_degree": 300,
                "3rd_degree": 310
            }
        }
    
    def calculate(self, age: int, total_cholesterol_mg_dl: float, family_history: str) -> Dict[str, Any]:
        """
        Applies US MEDPED diagnostic criteria for familial hypercholesterolemia
        
        Args:
            age (int): Patient's age in years
            total_cholesterol_mg_dl (float): Total cholesterol level in mg/dL
            family_history (str): Family history of FH ("none", "1st_degree", "2nd_degree", "3rd_degree")
            
        Returns:
            Dict with diagnostic result and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(age, total_cholesterol_mg_dl, family_history)
        
        # Determine age group
        age_group = self._get_age_group(age)
        
        # Get appropriate cholesterol cutoff
        cutoff = self._get_cholesterol_cutoff(age_group, family_history)
        
        # Determine diagnosis
        diagnosis_result = self._determine_diagnosis(total_cholesterol_mg_dl, cutoff)
        
        # Get interpretation
        interpretation = self._get_interpretation(
            diagnosis_result, total_cholesterol_mg_dl, cutoff, age, family_history
        )
        
        return {
            "result": diagnosis_result,
            "interpretation": interpretation["interpretation"],
            "stage": diagnosis_result,
            "stage_description": interpretation["description"],
            "cholesterol_cutoff": cutoff,
            "age_group": age_group,
            "family_history_category": family_history
        }
    
    def _validate_inputs(self, age: int, total_cholesterol_mg_dl: float, family_history: str):
        """Validates input parameters"""
        
        if not isinstance(age, int) or age < 0 or age > 120:
            raise ValueError("Age must be an integer between 0 and 120 years")
        
        if not isinstance(total_cholesterol_mg_dl, (int, float)) or total_cholesterol_mg_dl < 50 or total_cholesterol_mg_dl > 1000:
            raise ValueError("Total cholesterol must be between 50 and 1000 mg/dL")
        
        valid_family_history = ["none", "1st_degree", "2nd_degree", "3rd_degree"]
        if family_history not in valid_family_history:
            raise ValueError(f"Family history must be one of: {valid_family_history}")
    
    def _get_age_group(self, age: int) -> str:
        """Determines age group category for MEDPED criteria"""
        
        if age < 20:
            return "under_20"
        elif 20 <= age <= 29:
            return "20_to_29"
        elif 30 <= age <= 39:
            return "30_to_39"
        else:  # age >= 40
            return "40_and_over"
    
    def _get_cholesterol_cutoff(self, age_group: str, family_history: str) -> int:
        """Gets the appropriate cholesterol cutoff for given age group and family history"""
        
        return self.CHOLESTEROL_CUTOFFS[age_group][family_history]
    
    def _determine_diagnosis(self, total_cholesterol: float, cutoff: int) -> str:
        """Determines diagnostic result based on cholesterol level vs cutoff"""
        
        if total_cholesterol >= cutoff:
            return "Positive"
        else:
            return "Negative"
    
    def _get_interpretation(self, diagnosis: str, cholesterol: float, cutoff: int, 
                          age: int, family_history: str) -> Dict[str, str]:
        """
        Generates clinical interpretation based on diagnostic result
        
        Args:
            diagnosis (str): "Positive" or "Negative"
            cholesterol (float): Total cholesterol level
            cutoff (int): Applied cutoff value
            age (int): Patient age
            family_history (str): Family history category
            
        Returns:
            Dict with interpretation details
        """
        
        # Format family history for display
        family_history_display = {
            "none": "no family history of FH",
            "1st_degree": "1st degree relative with FH",
            "2nd_degree": "2nd degree relative with FH", 
            "3rd_degree": "3rd degree relative with FH"
        }[family_history]
        
        if diagnosis == "Positive":
            return {
                "description": "Meets US MEDPED criteria for FH",
                "interpretation": f"Patient meets the US MEDPED diagnostic criteria for familial hypercholesterolemia. "
                               f"Total cholesterol of {cholesterol:.0f} mg/dL exceeds the cutoff of {cutoff} mg/dL "
                               f"for age {age} years with {family_history_display}. "
                               f"Recommendations: Consider genetic testing for FH mutations, cascade screening of "
                               f"family members, and initiation of high-intensity statin therapy. Target LDL-C "
                               f"<70 mg/dL (or <55 mg/dL if cardiovascular disease present). Refer to lipid specialist "
                               f"if LDL-C goals not achieved with standard therapy."
            }
        else:
            return {
                "description": "Does not meet US MEDPED criteria for FH",
                "interpretation": f"Patient does not meet the US MEDPED diagnostic criteria for familial hypercholesterolemia. "
                               f"Total cholesterol of {cholesterol:.0f} mg/dL is below the cutoff of {cutoff} mg/dL "
                               f"for age {age} years with {family_history_display}. "
                               f"If cholesterol is elevated, consider secondary causes of hypercholesterolemia "
                               f"(hypothyroidism, diabetes, nephrotic syndrome, medications) or polygenic hypercholesterolemia. "
                               f"Standard cardiovascular risk assessment and management guidelines apply."
            }


def calculate_us_medped_fh_criteria(age: int, total_cholesterol_mg_dl: float, family_history: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_us_medped_fh_criteria pattern
    """
    calculator = UsMedpedFhCriteriaCalculator()
    return calculator.calculate(age, total_cholesterol_mg_dl, family_history)