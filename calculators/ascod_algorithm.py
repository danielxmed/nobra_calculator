"""
ASCOD Algorithm for Ischemic Stroke Calculator

Assigns phenotype in patients with ischemic stroke of uncertain causes by evaluating
five main etiologic categories: Atherothrombosis, Small-vessel disease, Cardiac pathology,
Other causes, and Dissection.

References:
1. Amarenco P, Bogousslavsky J, Caplan LR, Donnan GA, Wolf ME, Hennerici MG. 
   The ASCOD phenotyping of ischemic stroke (Updated ASCO phenotyping). 
   Cerebrovasc Dis. 2013;36(1):1-5. doi: 10.1159/000352050.
2. Sirimarco G, Lavallée PC, Labreuche J, Meseguer E, Cabrejo L, Guidoux C, et al. 
   Overlap of diseases underlying ischemic stroke: the ASCOD phenotyping. 
   Stroke. 2013 Dec;44(12):3427-33. doi: 10.1161/STROKEAHA.113.001363.
"""

from typing import Dict, Any
import re


class AscodAlgorithmCalculator:
    """Calculator for ASCOD Algorithm for Ischemic Stroke"""
    
    def __init__(self):
        # Valid causality grades
        self.VALID_GRADES = [0, 1, 2, 3, 9]
        
        # Grade descriptions
        self.GRADE_DESCRIPTIONS = {
            0: "No disease detected",
            1: "Potentially causal",
            2: "Causal link uncertain", 
            3: "Causal link unlikely but disease present",
            9: "Incomplete workup"
        }
    
    def calculate(self, atherosclerosis: str, small_vessel_disease: str, 
                 cardiac_pathology: str, other_causes: str, dissection: str) -> Dict[str, Any]:
        """
        Calculates the ASCOD phenotype using the provided causality grades
        
        Args:
            atherosclerosis (str): Atherosclerosis grade (grade_0, grade_1, grade_2, grade_3, or grade_9)
            small_vessel_disease (str): Small-vessel disease grade (grade_0, grade_1, grade_2, grade_3, or grade_9)
            cardiac_pathology (str): Cardiac pathology grade (grade_0, grade_1, grade_2, grade_3, or grade_9)
            other_causes (str): Other causes grade (grade_0, grade_1, grade_2, grade_3, or grade_9)
            dissection (str): Dissection grade (grade_0, grade_1, grade_2, grade_3, or grade_9)
            
        Returns:
            Dict with the ASCOD phenotype and interpretation
        """
        
        # Convert string grades to integers
        grade_map = {'grade_0': 0, 'grade_1': 1, 'grade_2': 2, 'grade_3': 3, 'grade_9': 9}
        
        try:
            atherothrombosis_grade = grade_map[atherosclerosis]
            small_vessel_grade = grade_map[small_vessel_disease]
            cardiac_grade = grade_map[cardiac_pathology]
            other_causes_grade = grade_map[other_causes]
            dissection_grade = grade_map[dissection]
        except KeyError as e:
            raise ValueError(f"Invalid grade format: {e}. Expected format: grade_0, grade_1, grade_2, grade_3, or grade_9")
        
        # Validate inputs
        self._validate_inputs(atherothrombosis_grade, small_vessel_grade, cardiac_grade, 
                            other_causes_grade, dissection_grade)
        
        # Generate ASCOD phenotype
        phenotype = self._generate_phenotype(atherothrombosis_grade, small_vessel_grade, 
                                           cardiac_grade, other_causes_grade, dissection_grade)
        
        # Get interpretation
        interpretation = self._get_interpretation(phenotype, atherothrombosis_grade, 
                                                small_vessel_grade, cardiac_grade, 
                                                other_causes_grade, dissection_grade)
        
        return {
            "result": phenotype,
            "unit": "phenotype",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, atherothrombosis_grade: int, small_vessel_grade: int, 
                        cardiac_grade: int, other_causes_grade: int, dissection_grade: int):
        """Validates input parameters"""
        
        grades = [atherothrombosis_grade, small_vessel_grade, cardiac_grade, 
                 other_causes_grade, dissection_grade]
        grade_names = ["atherothrombosis_grade", "small_vessel_grade", "cardiac_grade", 
                      "other_causes_grade", "dissection_grade"]
        
        for grade, name in zip(grades, grade_names):
            if not isinstance(grade, int):
                raise ValueError(f"{name} must be an integer")
            
            if grade not in self.VALID_GRADES:
                raise ValueError(f"{name} must be one of {self.VALID_GRADES} (0=no disease, 1=potentially causal, 2=uncertain, 3=unlikely causal, 9=incomplete workup)")
    
    def _generate_phenotype(self, atherothrombosis_grade: int, small_vessel_grade: int, 
                           cardiac_grade: int, other_causes_grade: int, dissection_grade: int) -> str:
        """Generates the ASCOD phenotype string"""
        
        return f"A{atherothrombosis_grade}-S{small_vessel_grade}-C{cardiac_grade}-O{other_causes_grade}-D{dissection_grade}"
    
    def _get_interpretation(self, phenotype: str, atherothrombosis_grade: int, 
                          small_vessel_grade: int, cardiac_grade: int, 
                          other_causes_grade: int, dissection_grade: int) -> Dict[str, str]:
        """
        Determines the interpretation based on the ASCOD phenotype
        
        Args:
            phenotype (str): ASCOD phenotype string
            Individual grades for detailed interpretation
            
        Returns:
            Dict with interpretation details
        """
        
        grades = [atherothrombosis_grade, small_vessel_grade, cardiac_grade, 
                 other_causes_grade, dissection_grade]
        categories = ["Atherothrombosis", "Small-vessel disease", "Cardiac pathology", 
                     "Other causes", "Dissection"]
        
        # Check for specific patterns
        if phenotype == "A0-S0-C0-O0-D0":
            return {
                "stage": "No Disease Detected",
                "description": "No identifiable mechanisms detected",
                "interpretation": "Comprehensive workup negative for common stroke mechanisms. Consider rare causes or repeat evaluation if clinically indicated. Standard secondary prevention measures may still be appropriate based on overall cardiovascular risk."
            }
        
        # Check for incomplete workup
        if 9 in grades:
            incomplete_categories = [categories[i] for i, grade in enumerate(grades) if grade == 9]
            return {
                "stage": "Incomplete Workup",
                "description": "Incomplete diagnostic evaluation",
                "interpretation": f"Further diagnostic workup needed for: {', '.join(incomplete_categories)}. Complete evaluation recommended before finalizing stroke classification and secondary prevention strategy."
            }
        
        # Check for potentially causal mechanisms
        if 1 in grades:
            causal_categories = [categories[i] for i, grade in enumerate(grades) if grade == 1]
            interpretation_text = f"Potentially causal mechanism(s) identified: {', '.join(causal_categories)}. "
            
            if len(causal_categories) == 1:
                interpretation_text += "Consider targeted secondary prevention specific to this mechanism."
            else:
                interpretation_text += "Multiple potentially causal mechanisms present - consider comprehensive secondary prevention addressing all identified mechanisms."
            
            # Add specific recommendations based on mechanisms
            recommendations = []
            if atherothrombosis_grade == 1:
                recommendations.append("antiplatelet therapy and statin")
            if small_vessel_grade == 1:
                recommendations.append("blood pressure control")
            if cardiac_grade == 1:
                recommendations.append("anticoagulation evaluation")
            if other_causes_grade == 1:
                recommendations.append("mechanism-specific treatment")
            if dissection_grade == 1:
                recommendations.append("anticoagulation or antiplatelet therapy")
            
            if recommendations:
                interpretation_text += f" Consider: {', '.join(recommendations)}."
            
            return {
                "stage": "Potentially Causal",
                "description": "At least one potentially causal mechanism identified",
                "interpretation": interpretation_text
            }
        
        # Check for uncertain causality
        if 2 in grades:
            uncertain_categories = [categories[i] for i, grade in enumerate(grades) if grade == 2]
            return {
                "stage": "Uncertain Causality", 
                "description": "Causal link uncertain for identified mechanism(s)",
                "interpretation": f"Mechanism(s) present but relationship to stroke uncertain: {', '.join(uncertain_categories)}. Consider secondary prevention based on overall cardiovascular risk profile and clinical judgment. Additional evaluation may help clarify causality."
            }
        
        # Check for disease present but unlikely causal
        if 3 in grades:
            present_categories = [categories[i] for i, grade in enumerate(grades) if grade == 3]
            return {
                "stage": "Disease Present",
                "description": "Disease present but causal link unlikely", 
                "interpretation": f"Underlying condition(s) identified but not likely causative for this stroke: {', '.join(present_categories)}. May still require management for overall cardiovascular risk reduction. Consider evaluation for other stroke mechanisms."
            }
        
        # Fallback interpretation
        return {
            "stage": "Mixed Classification",
            "description": "Mixed causality grades assigned",
            "interpretation": f"ASCOD phenotype {phenotype} indicates a complex stroke classification. Review individual mechanism grades and consider appropriate secondary prevention strategies for all identified conditions."
        }


def calculate_ascod_algorithm(atherosclerosis: str, small_vessel_disease: str, 
                            cardiac_pathology: str, other_causes: str, 
                            dissection: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_ascod_algorithm pattern
    """
    calculator = AscodAlgorithmCalculator()
    return calculator.calculate(atherosclerosis, small_vessel_disease, cardiac_pathology, 
                              other_causes, dissection)