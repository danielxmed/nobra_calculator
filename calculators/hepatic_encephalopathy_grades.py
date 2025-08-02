"""
Hepatic Encephalopathy Grades/Stages (West Haven Criteria) Calculator

Classifies hepatic encephalopathy severity based on clinical features.

References:
- Vilstrup H, et al. J Hepatol. 2014;61(3):642-59.
- European Association for the Study of the Liver. J Hepatol. 2022;77(3):807-824.
"""

from typing import Dict, Any


class HepaticEncephalopathyGradesCalculator:
    """Calculator for Hepatic Encephalopathy Grades/Stages using West Haven Criteria"""
    
    def __init__(self):
        # Grade definitions with detailed clinical features
        self.GRADE_DEFINITIONS = {
            "grade_0": {
                "grade": "Grade 0",
                "stage": "Grade 0 (Minimal HE)",
                "description": "Minimal hepatic encephalopathy",
                "interpretation": "No clinically evident changes in personality or behavior. Impaired psychometric or neuropsychological tests. No asterixis. Previously known as subclinical hepatic encephalopathy. Patients appear normal but have subtle cognitive deficits detectable only by specialized testing."
            },
            "grade_1": {
                "grade": "Grade 1",
                "stage": "Grade 1 (Covert HE)",
                "description": "Changes in behavior with minimal change in level of consciousness",
                "interpretation": "Trivial lack of awareness, euphoria or anxiety, shortened attention span, impaired performance of addition or subtraction. Mild asterixis or tremor may be present. Sleep-wake cycle may be reversed. This stage is often only noticed by family members."
            },
            "grade_2": {
                "grade": "Grade 2",
                "stage": "Grade 2 (Overt HE)",
                "description": "Gross disorientation, drowsiness, possibly asterixis, inappropriate behavior",
                "interpretation": "Lethargy or apathy, minimal disorientation for time or place, subtle personality change, inappropriate behavior, impaired performance of subtraction. Obvious asterixis. Patient is drowsy but arousable. This is the first stage clearly identifiable on clinical examination."
            },
            "grade_3": {
                "grade": "Grade 3",
                "stage": "Grade 3 (Overt HE)",
                "description": "Marked confusion, incoherent speech, sleeping most of the time but arousable to vocal stimuli",
                "interpretation": "Somnolence to semi-stupor but responsive to verbal stimuli, confusion, gross disorientation. Patient cannot perform mental tasks, disorientation to time and place, marked confusion, amnesia, occasional fits of rage, speech is incomprehensible. Muscular rigidity and clonus may be present."
            },
            "grade_4": {
                "grade": "Grade 4",
                "stage": "Grade 4 (Overt HE)",
                "description": "Comatose, unresponsive to pain; decorticate or decerebrate posturing",
                "interpretation": "Coma with or without response to painful stimuli. No personality or behavioral changes can be assessed. Decerebrate or decorticate posturing may be present. Pupils may be dilated. This represents complete loss of consciousness."
            }
        }
    
    def calculate(self, clinical_features: str) -> Dict[str, Any]:
        """
        Determines the hepatic encephalopathy grade based on clinical features
        
        Args:
            clinical_features: Clinical presentation grade (grade_0 to grade_4)
            
        Returns:
            Dict with the grade and detailed interpretation
        """
        
        # Validate input
        self._validate_input(clinical_features)
        
        # Get grade information
        grade_info = self._get_grade_information(clinical_features)
        
        return {
            "result": grade_info["grade"],
            "unit": "grade",
            "interpretation": grade_info["interpretation"],
            "stage": grade_info["stage"],
            "stage_description": grade_info["description"]
        }
    
    def _validate_input(self, clinical_features: str):
        """Validates input parameter"""
        
        valid_grades = list(self.GRADE_DEFINITIONS.keys())
        
        if clinical_features not in valid_grades:
            raise ValueError(f"clinical_features must be one of {valid_grades}")
    
    def _get_grade_information(self, clinical_features: str) -> Dict[str, str]:
        """
        Returns detailed information for the specified grade
        
        Args:
            clinical_features (str): The clinical grade selection
            
        Returns:
            Dict with grade, stage, description, and interpretation
        """
        
        return self.GRADE_DEFINITIONS[clinical_features]


def calculate_hepatic_encephalopathy_grades(clinical_features: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_hepatic_encephalopathy_grades pattern
    """
    calculator = HepaticEncephalopathyGradesCalculator()
    return calculator.calculate(clinical_features)