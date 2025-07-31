"""
Duke Criteria for Infective Endocarditis Calculator

Provides standardized diagnostic criteria for infective endocarditis based on clinical, 
microbiological, and echocardiographic findings. Classifies patients as having definite, 
possible, or rejected endocarditis based on major and minor criteria.

References:
1. Durack DT, Lukes AS, Bright DK. New criteria for diagnosis of infective endocarditis: 
   utilization of specific echocardiographic findings. Duke Endocarditis Service. 
   Am J Med. 1994;96(3):200-9.
2. Li JS, Sexton DJ, Mick N, Nettles R, Fowler VG Jr, Ryan T, et al. Proposed modifications 
   to the Duke criteria for the diagnosis of infective endocarditis. Clin Infect Dis. 
   2000;30(4):633-8.
"""

from typing import Dict, Any


class DukeCriteriaInfectiveEndocarditisCalculator:
    """Calculator for Duke Criteria for Infective Endocarditis"""
    
    def __init__(self):
        # Major criteria parameters
        self.MAJOR_CRITERIA = ['blood_culture_major', 'endocardial_involvement']
        
        # Minor criteria parameters
        self.MINOR_CRITERIA = [
            'predisposition', 
            'fever', 
            'vascular_phenomena', 
            'immunologic_phenomena', 
            'microbiological_evidence'
        ]
    
    def calculate(self, blood_culture_major: str, endocardial_involvement: str, 
                  predisposition: str, fever: str, vascular_phenomena: str,
                  immunologic_phenomena: str, microbiological_evidence: str) -> Dict[str, Any]:
        """
        Calculates the Duke Criteria for Infective Endocarditis
        
        Args:
            blood_culture_major (str): Blood culture positive for IE with typical organisms
            endocardial_involvement (str): Evidence of endocardial involvement
            predisposition (str): Predisposing heart condition or injection drug use
            fever (str): Fever > 38°C (100.4°F)
            vascular_phenomena (str): Vascular phenomena present
            immunologic_phenomena (str): Immunologic phenomena present
            microbiological_evidence (str): Microbiological evidence not meeting major criteria
            
        Returns:
            Dict with the result and interpretation
        """
        
        # Map parameters for easier processing
        parameters = {
            'blood_culture_major': blood_culture_major,
            'endocardial_involvement': endocardial_involvement,
            'predisposition': predisposition,
            'fever': fever,
            'vascular_phenomena': vascular_phenomena,
            'immunologic_phenomena': immunologic_phenomena,
            'microbiological_evidence': microbiological_evidence
        }
        
        # Validate inputs
        self._validate_inputs(parameters)
        
        # Count major and minor criteria
        major_count = self._count_major_criteria(parameters)
        minor_count = self._count_minor_criteria(parameters)
        
        # Determine diagnosis
        diagnosis = self._determine_diagnosis(major_count, minor_count)
        
        # Get interpretation
        interpretation = self._get_interpretation(diagnosis, major_count, minor_count)
        
        return {
            "result": diagnosis,
            "unit": "category",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"],
            "major_criteria_count": major_count,
            "minor_criteria_count": minor_count
        }
    
    def _validate_inputs(self, parameters: Dict[str, str]):
        """Validates input parameters"""
        
        valid_responses = ["yes", "no"]
        
        for param_name, response in parameters.items():
            if not isinstance(response, str):
                raise ValueError(f"Parameter '{param_name}' must be a string")
            
            if response.lower() not in valid_responses:
                raise ValueError(f"Parameter '{param_name}' must be 'yes' or 'no', got '{response}'")
    
    def _count_major_criteria(self, parameters: Dict[str, str]) -> int:
        """Counts the number of positive major criteria"""
        
        count = 0
        for criterion in self.MAJOR_CRITERIA:
            if parameters[criterion].lower() == 'yes':
                count += 1
        
        return count
    
    def _count_minor_criteria(self, parameters: Dict[str, str]) -> int:
        """Counts the number of positive minor criteria"""
        
        count = 0
        for criterion in self.MINOR_CRITERIA:
            if parameters[criterion].lower() == 'yes':
                count += 1
        
        return count
    
    def _determine_diagnosis(self, major_count: int, minor_count: int) -> str:
        """
        Determines the diagnostic classification based on major and minor criteria counts
        
        Args:
            major_count (int): Number of positive major criteria
            minor_count (int): Number of positive minor criteria
            
        Returns:
            str: Diagnostic classification (Definite, Possible, or Rejected)
        """
        
        # Definite IE criteria:
        # - 2 major criteria OR
        # - 1 major + 3 minor criteria OR  
        # - 5 minor criteria
        if (major_count >= 2 or 
            (major_count >= 1 and minor_count >= 3) or 
            minor_count >= 5):
            return "Definite"
        
        # Possible IE criteria:
        # - 1 major + 1 minor criterion OR
        # - 3 minor criteria
        elif (major_count >= 1 and minor_count >= 1) or minor_count >= 3:
            return "Possible"
        
        # Rejected IE
        else:
            return "Rejected"
    
    def _get_interpretation(self, diagnosis: str, major_count: int, minor_count: int) -> Dict[str, str]:
        """
        Determines the interpretation based on the diagnosis
        
        Args:
            diagnosis (str): Diagnostic classification
            major_count (int): Number of positive major criteria  
            minor_count (int): Number of positive minor criteria
            
        Returns:
            Dict with interpretation
        """
        
        if diagnosis == "Definite":
            return {
                "stage": "Definite",
                "description": "Definite infective endocarditis",
                "interpretation": f"Definite infective endocarditis based on {major_count} major and {minor_count} minor criteria. Immediate antimicrobial therapy indicated. Cardiology and infectious disease consultation recommended. Consider surgical evaluation if complicated IE."
            }
        elif diagnosis == "Possible":
            return {
                "stage": "Possible",
                "description": "Possible infective endocarditis",
                "interpretation": f"Possible infective endocarditis based on {major_count} major and {minor_count} minor criteria. Findings are consistent with IE but do not meet criteria for definite IE. Consider further diagnostic workup including repeat echocardiography, additional blood cultures, and specialist consultation."
            }
        else:  # Rejected
            return {
                "stage": "Rejected",
                "description": "Infective endocarditis rejected",
                "interpretation": f"Infective endocarditis is rejected based on {major_count} major and {minor_count} minor criteria. Criteria not met for possible or definite IE. Consider alternative diagnoses including non-infectious causes of valve disease, systemic infection, or other cardiac conditions."
            }


def calculate_duke_criteria_infective_endocarditis(blood_culture_major: str, endocardial_involvement: str,
                                                  predisposition: str, fever: str, vascular_phenomena: str,
                                                  immunologic_phenomena: str, microbiological_evidence: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_duke_criteria_infective_endocarditis pattern
    """
    calculator = DukeCriteriaInfectiveEndocarditisCalculator()
    return calculator.calculate(
        blood_culture_major, endocardial_involvement, predisposition, fever,
        vascular_phenomena, immunologic_phenomena, microbiological_evidence
    )