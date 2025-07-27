"""
2023 Duke-ISCVID Criteria Calculator

Diagnostic criteria for infective endocarditis based on the 2023 Duke-International
Society for Cardiovascular Infectious Diseases updated criteria.
"""

from typing import Dict, Any


class DukeIscvid2023Calculator:
    """Calculator for 2023 Duke-ISCVID Criteria for Infective Endocarditis"""
    
    def __init__(self):
        self.major_microbiologic_criteria = [
            "microbiologic_major_typical",
            "microbiologic_major_nontypical", 
            "pcr_positive_coxiella_bartonella_tropheryma",
            "coxiella_antibody_titer",
            "bartonella_antibody_titer"
        ]
        
        self.major_imaging_criteria = [
            "imaging_major_echo_ct",
            "new_valvular_regurgitation",
            "prosthetic_valve_dehiscence",
            "pet_ct_abnormal_activity"
        ]
        
        self.major_surgical_criteria = [
            "surgical_evidence"
        ]
        
        self.minor_criteria = [
            "previous_ie",
            "prosthetic_valve",
            "previous_valve_repair",
            "congenital_heart_disease",
            "significant_regurgitation_stenosis",
            "endovascular_cied",
            "hypertrophic_cardiomyopathy",
            "injection_drug_use",
            "fever",
            "vascular_phenomena",
            "immunologic_phenomena",
            "positive_blood_cultures_minor",
            "positive_sterile_site_culture",
            "pet_ct_within_3_months",
            "new_regurgitation_auscultation"
        ]
        
        self.pathologic_criteria = [
            "pathologic_microorganisms",
            "pathologic_active_endocarditis"
        ]
    
    def calculate(self, **kwargs) -> Dict[str, Any]:
        """
        Calculates the Duke-ISCVID diagnosis for infective endocarditis
        
        Args:
            **kwargs: All the Duke-ISCVID criteria parameters
            
        Returns:
            Dict with the diagnosis and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(**kwargs)
        
        # Count criteria
        pathologic_count = self._count_pathologic_criteria(**kwargs)
        major_count = self._count_major_criteria(**kwargs)
        minor_count = self._count_minor_criteria(**kwargs)
        
        # Determine diagnosis
        diagnosis = self._get_diagnosis(pathologic_count, major_count, minor_count)
        
        # Get interpretation
        interpretation = self._get_interpretation(diagnosis)
        
        return {
            "result": diagnosis,
            "pathologic_criteria_count": pathologic_count,
            "major_criteria_count": major_count,
            "minor_criteria_count": minor_count,
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, **kwargs):
        """Validates input parameters"""
        
        # Check that all parameters are either 'none' or 'present'
        valid_values = {"none", "present"}
        
        for key, value in kwargs.items():
            if value not in valid_values:
                raise ValueError(f"Parameter {key} must be either 'none' or 'present', got '{value}'")
    
    def _count_pathologic_criteria(self, **kwargs) -> int:
        """Counts positive pathologic criteria"""
        count = 0
        for criterion in self.pathologic_criteria:
            if kwargs.get(criterion, "none") == "present":
                count += 1
        return count
    
    def _count_major_criteria(self, **kwargs) -> int:
        """Counts positive major criteria"""
        count = 0
        
        # Check microbiologic major criteria (any one counts as 1 major)
        microbiologic_present = any(
            kwargs.get(criterion, "none") == "present" 
            for criterion in self.major_microbiologic_criteria
        )
        if microbiologic_present:
            count += 1
        
        # Check imaging major criteria (any one counts as 1 major)
        imaging_present = any(
            kwargs.get(criterion, "none") == "present" 
            for criterion in self.major_imaging_criteria
        )
        if imaging_present:
            count += 1
        
        # Check surgical major criteria
        surgical_present = any(
            kwargs.get(criterion, "none") == "present" 
            for criterion in self.major_surgical_criteria
        )
        if surgical_present:
            count += 1
        
        return count
    
    def _count_minor_criteria(self, **kwargs) -> int:
        """Counts positive minor criteria"""
        count = 0
        for criterion in self.minor_criteria:
            if kwargs.get(criterion, "none") == "present":
                count += 1
        return count
    
    def _get_diagnosis(self, pathologic_count: int, major_count: int, minor_count: int) -> str:
        """
        Determines the diagnosis based on criteria counts
        
        Args:
            pathologic_count: Number of positive pathologic criteria
            major_count: Number of positive major criteria
            minor_count: Number of positive minor criteria
            
        Returns:
            Diagnosis string
        """
        
        # Definite IE if any pathologic criteria present
        if pathologic_count > 0:
            return "Definite IE"
        
        # Definite IE if:
        # - 2 major criteria OR
        # - 1 major + 3 minor criteria OR  
        # - 5 minor criteria
        if (major_count >= 2 or 
            (major_count >= 1 and minor_count >= 3) or 
            minor_count >= 5):
            return "Definite IE"
        
        # Possible IE if:
        # - 1 major + 1 minor criteria OR
        # - 3 minor criteria
        if (major_count >= 1 and minor_count >= 1) or minor_count >= 3:
            return "Possible IE"
        
        # Otherwise rejected
        return "Rejected"
    
    def _get_interpretation(self, diagnosis: str) -> Dict[str, str]:
        """
        Gets the clinical interpretation based on diagnosis
        
        Args:
            diagnosis: The calculated diagnosis
            
        Returns:
            Dict with interpretation details
        """
        
        if diagnosis == "Definite IE":
            return {
                "stage": "Definite IE",
                "description": "Meets criteria for definite infective endocarditis",
                "interpretation": "Patient meets Duke-ISCVID criteria for definite infective endocarditis. Appropriate antimicrobial therapy and cardiology/infectious disease consultation recommended."
            }
        elif diagnosis == "Possible IE":
            return {
                "stage": "Possible IE", 
                "description": "Meets criteria for possible infective endocarditis",
                "interpretation": "Patient meets Duke-ISCVID criteria for possible infective endocarditis. Further diagnostic workup including repeat echocardiography, blood cultures, and specialist consultation recommended."
            }
        else:
            return {
                "stage": "Rejected",
                "description": "Does not meet criteria for infective endocarditis",
                "interpretation": "Patient does not meet Duke-ISCVID criteria for infective endocarditis. Consider alternative diagnoses. Clinical correlation and specialist consultation if high clinical suspicion persists."
            }


def calculate_duke_iscvid_2023(**kwargs) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = DukeIscvid2023Calculator()
    return calculator.calculate(**kwargs)