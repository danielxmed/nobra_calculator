"""
Hunt & Hess Classification of Subarachnoid Hemorrhage Calculator

Classifies severity of aneurysmal subarachnoid hemorrhage based on clinical presentation 
to predict mortality and guide surgical risk assessment.

References:
- Hunt WE, Hess RM. Surgical risk as related to time of intervention in the repair of 
  intracranial aneurysms. J Neurosurg. 1968 Jan;28(1):14-20.
- Hunt WE, Kosnik EJ. Timing and perioperative care in intracranial aneurysm surgery. 
  Clin Neurosurg. 1974;21:79-89.
"""

from typing import Dict, Any


class HuntHessClassificationCalculator:
    """Calculator for Hunt & Hess Classification of Subarachnoid Hemorrhage"""
    
    def __init__(self):
        # Define base grades based on clinical presentation
        self.clinical_grades = {
            "asymptomatic_minimal_headache": 1,
            "moderate_severe_headache_nuchal_rigidity": 2,
            "drowsiness_confusion_mild_focal_deficit": 3,
            "stupor_moderate_severe_hemiparesis": 4,
            "deep_coma_decerebrate_rigidity_moribund": 5
        }
        
        # Survival rates by grade (approximate historical data)
        self.survival_rates = {
            1: 70,
            2: 60,
            3: 50,
            4: 40,
            5: 10
        }
        
        # Mortality rates (inverse of survival)
        self.mortality_rates = {
            1: 30,
            2: 40,
            3: 50,
            4: 60,
            5: 90
        }
    
    def calculate(self, clinical_presentation: str, serious_systemic_disease: str) -> Dict[str, Any]:
        """
        Calculates Hunt-Hess grade for subarachnoid hemorrhage
        
        Args:
            clinical_presentation (str): Clinical presentation category
            serious_systemic_disease (str): Presence of serious systemic disease ("yes" or "no")
            
        Returns:
            Dict with Hunt-Hess grade and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(clinical_presentation, serious_systemic_disease)
        
        # Get base grade from clinical presentation
        base_grade = self.clinical_grades[clinical_presentation]
        
        # Adjust for serious systemic disease (add 1 grade if present)
        if serious_systemic_disease == "yes":
            final_grade = min(base_grade + 1, 5)  # Cap at grade 5
            grade_adjusted = True
        else:
            final_grade = base_grade
            grade_adjusted = False
        
        # Get interpretation
        interpretation = self._get_interpretation(final_grade)
        
        # Get mortality and survival data
        survival_rate = self.survival_rates[final_grade]
        mortality_rate = self.mortality_rates[final_grade]
        
        return {
            "result": f"Grade {self._grade_to_roman(final_grade)}",
            "unit": "grade",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"],
            "numeric_grade": final_grade,
            "survival_rate_percent": survival_rate,
            "mortality_rate_percent": mortality_rate,
            "grade_adjusted_for_systemic_disease": grade_adjusted,
            "surgical_risk": self._get_surgical_risk(final_grade)
        }
    
    def _validate_inputs(self, clinical_presentation: str, serious_systemic_disease: str):
        """Validates input parameters"""
        
        valid_presentations = list(self.clinical_grades.keys())
        if clinical_presentation not in valid_presentations:
            raise ValueError(f"Clinical presentation must be one of: {valid_presentations}")
        
        valid_systemic_disease = ["yes", "no"]
        if serious_systemic_disease not in valid_systemic_disease:
            raise ValueError(f"Serious systemic disease must be one of: {valid_systemic_disease}")
    
    def _grade_to_roman(self, grade: int) -> str:
        """Converts numeric grade to Roman numeral"""
        roman_numerals = {1: "I", 2: "II", 3: "III", 4: "IV", 5: "V"}
        return roman_numerals[grade]
    
    def _get_surgical_risk(self, grade: int) -> str:
        """Determines surgical risk level based on grade"""
        if grade == 1:
            return "Low"
        elif grade == 2:
            return "Low-Moderate" 
        elif grade == 3:
            return "Moderate"
        elif grade == 4:
            return "High"
        else:  # grade == 5
            return "Very High"
    
    def _get_interpretation(self, grade: int) -> Dict[str, str]:
        """
        Determines the interpretation based on Hunt-Hess grade
        
        Args:
            grade (int): Hunt-Hess grade (1-5)
            
        Returns:
            Dict with interpretation details
        """
        
        if grade == 1:
            return {
                "stage": "Grade I",
                "description": "Asymptomatic or minimal headache",
                "interpretation": "Asymptomatic or minimal headache and slight nuchal rigidity. Excellent prognosis with ~70% survival rate. Low surgical risk. Early intervention generally recommended."
            }
        elif grade == 2:
            return {
                "stage": "Grade II",
                "description": "Moderate to severe headache",
                "interpretation": "Moderate to severe headache, nuchal rigidity, no neurologic deficit other than cranial nerve palsy. Good prognosis with ~60% survival rate. Reasonable surgical candidate."
            }
        elif grade == 3:
            return {
                "stage": "Grade III",
                "description": "Drowsiness, confusion, mild focal deficit",
                "interpretation": "Drowsiness, confusion, or mild focal deficit. Fair prognosis with ~50% survival rate. Higher surgical risk, careful evaluation needed."
            }
        elif grade == 4:
            return {
                "stage": "Grade IV",
                "description": "Stupor, moderate to severe hemiparesis",
                "interpretation": "Stupor, moderate to severe hemiparesis, possibly early decerebrate rigidity and vegetative disturbances. Poor prognosis with ~40% survival rate. High surgical risk."
            }
        else:  # grade == 5
            return {
                "stage": "Grade V",
                "description": "Deep coma, decerebrate rigidity, moribund",
                "interpretation": "Deep coma, decerebrate rigidity, moribund appearance. Very poor prognosis with ~10% survival rate. Extremely high surgical risk, intervention often futile."
            }


def calculate_hunt_hess_classification(clinical_presentation: str, 
                                     serious_systemic_disease: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = HuntHessClassificationCalculator()
    return calculator.calculate(clinical_presentation, serious_systemic_disease)