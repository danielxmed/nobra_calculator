"""
Fuhrman Nuclear Grade Calculator

Provides prognostic grading system for clear cell renal cell carcinoma based on 
nuclear morphology and cellular appearance.

References:
- Fuhrman SA, et al. Am J Surg Pathol. 1982;6(7):655-63.
- Rioux-Leclercq N, et al. Cancer. 2007;109(5):868-74.
"""

from typing import Dict, Any


class FuhrmanNuclearGradeCalculator:
    """Calculator for Fuhrman Nuclear Grade for Clear Cell Renal Carcinoma"""
    
    def __init__(self):
        # Grade criteria mapping
        self.GRADE_CRITERIA = {
            "nuclear_diameter": {
                "small_10um": 1,
                "larger_15um": 2,
                "even_larger_20um": 3
            },
            "nuclear_shape": {
                "round_uniform": 1,
                "irregularities": 2,
                "obvious_irregular": 3
            },
            "nucleoli": {
                "absent_inconspicuous": 1,
                "visible_400x": 2,
                "prominent_100x": 3
            }
        }
    
    def calculate(self, nuclear_diameter: str, nuclear_shape: str, 
                  nucleoli: str, bizarre_multilobed_spindle: str) -> Dict[str, Any]:
        """
        Calculates the Fuhrman nuclear grade
        
        Args:
            nuclear_diameter: Size of tumor cell nuclei (small_10um, larger_15um, even_larger_20um)
            nuclear_shape: Shape and regularity (round_uniform, irregularities, obvious_irregular)
            nucleoli: Visibility of nucleoli (absent_inconspicuous, visible_400x, prominent_100x)
            bizarre_multilobed_spindle: Presence of bizarre features (yes/no)
            
        Returns:
            Dict with the grade and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(nuclear_diameter, nuclear_shape, nucleoli, bizarre_multilobed_spindle)
        
        # Calculate grade
        result = self._calculate_grade(nuclear_diameter, nuclear_shape, nucleoli, bizarre_multilobed_spindle)
        
        # Get interpretation
        interpretation = self._get_interpretation(result)
        
        return {
            "result": result,
            "unit": "grade",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, nuclear_diameter: str, nuclear_shape: str, 
                        nucleoli: str, bizarre_multilobed_spindle: str):
        """Validates input parameters"""
        
        valid_diameters = ["small_10um", "larger_15um", "even_larger_20um"]
        if nuclear_diameter not in valid_diameters:
            raise ValueError(f"Nuclear diameter must be one of: {', '.join(valid_diameters)}")
        
        valid_shapes = ["round_uniform", "irregularities", "obvious_irregular"]
        if nuclear_shape not in valid_shapes:
            raise ValueError(f"Nuclear shape must be one of: {', '.join(valid_shapes)}")
        
        valid_nucleoli = ["absent_inconspicuous", "visible_400x", "prominent_100x"]
        if nucleoli not in valid_nucleoli:
            raise ValueError(f"Nucleoli must be one of: {', '.join(valid_nucleoli)}")
        
        if bizarre_multilobed_spindle not in ["yes", "no"]:
            raise ValueError("Bizarre/multilobed/spindle must be 'yes' or 'no'")
    
    def _calculate_grade(self, nuclear_diameter: str, nuclear_shape: str, 
                        nucleoli: str, bizarre_multilobed_spindle: str) -> int:
        """Calculates the Fuhrman grade based on nuclear features"""
        
        # Grade 4 if bizarre features present
        if bizarre_multilobed_spindle == "yes":
            return 4
        
        # Otherwise, grade is the highest among the three main criteria
        diameter_grade = self.GRADE_CRITERIA["nuclear_diameter"][nuclear_diameter]
        shape_grade = self.GRADE_CRITERIA["nuclear_shape"][nuclear_shape]
        nucleoli_grade = self.GRADE_CRITERIA["nucleoli"][nucleoli]
        
        # Return the highest grade among the three features
        return max(diameter_grade, shape_grade, nucleoli_grade)
    
    def _get_interpretation(self, grade: int) -> Dict[str, str]:
        """
        Determines the interpretation based on the grade
        
        Args:
            grade (int): Fuhrman grade (1-4)
            
        Returns:
            Dict with interpretation
        """
        
        if grade == 1:
            return {
                "stage": "Grade 1",
                "description": "Small nuclei, round and uniform",
                "interpretation": "Small nuclei (<10 µm), hyperchromatic, round (resembling mature lymphocytes), with no visible nucleoli and little detail in the chromatin. Best prognosis among all grades."
            }
        elif grade == 2:
            return {
                "stage": "Grade 2",
                "description": "Slightly irregular nuclei with visible nucleoli",
                "interpretation": "Larger nuclei (15 µm), may be oval with finely granular chromatin. Nucleoli visible at 400x magnification. Intermediate prognosis."
            }
        elif grade == 3:
            return {
                "stage": "Grade 3",
                "description": "Obviously irregular nuclei with prominent nucleoli",
                "interpretation": "Even larger nuclei (20 µm), coarsely granular chromatin, easily recognizable nucleoli at 100x magnification. Worse prognosis than grades 1-2."
            }
        else:  # grade == 4
            return {
                "stage": "Grade 4",
                "description": "Pleomorphic nuclei with extreme features",
                "interpretation": "Extreme nuclear pleomorphism, bizarre multilobed nuclei, spindle cells, rhabdoid morphology or sarcomatoid differentiation. Poorest prognosis."
            }


def calculate_fuhrman_nuclear_grade(nuclear_diameter, nuclear_shape, 
                                   nucleoli, bizarre_multilobed_spindle) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = FuhrmanNuclearGradeCalculator()
    return calculator.calculate(nuclear_diameter, nuclear_shape, 
                               nucleoli, bizarre_multilobed_spindle)