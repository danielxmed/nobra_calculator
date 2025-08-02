"""
McDonald Criteria for Multiple Sclerosis (2017 Revision) Calculator

Diagnoses multiple sclerosis using clinical attacks, lesion characteristics, and MRI findings.
The 2017 revision introduced key changes including CSF oligoclonal bands substitution for 
dissemination in time and inclusion of cortical lesions for dissemination in space.

References (Vancouver style):
1. Thompson AJ, Banwell BL, Barkhof F, Carroll WM, Coetzee T, Comi G, et al. Diagnosis of 
   multiple sclerosis: 2017 revisions of the McDonald criteria. Lancet Neurol. 2018 Feb;17(2):162-173. 
   doi: 10.1016/S1474-4422(17)30470-2.
2. Polman CH, Reingold SC, Banwell B, Clanet M, Cohen JA, Filippi M, et al. Diagnostic criteria 
   for multiple sclerosis: 2010 revisions to the McDonald criteria. Ann Neurol. 2011 Feb;69(2):292-302. 
   doi: 10.1002/ana.22366.
"""

from typing import Dict, Any


class McdonaldCriteriaMultipleSclerosis2017RevisionCalculator:
    """Calculator for McDonald Criteria for Multiple Sclerosis (2017 Revision)"""
    
    def __init__(self):
        # Valid options for each parameter
        self.CLINICAL_ATTACKS_OPTIONS = ["0", "1", "2_or_more"]
        self.OBJECTIVE_EVIDENCE_OPTIONS = ["0", "1", "2_or_more"]
        self.DISSEMINATION_OPTIONS = ["not_demonstrated", "demonstrated"]
        self.CSF_OPTIONS = ["absent", "present", "not_tested"]
        self.ALTERNATIVE_DIAGNOSIS_OPTIONS = ["excluded", "possible"]
    
    def calculate(self, clinical_attacks: str, objective_clinical_evidence: str,
                 dissemination_in_space: str, dissemination_in_time: str,
                 csf_oligoclonal_bands: str, alternative_diagnosis: str) -> Dict[str, Any]:
        """
        Evaluates McDonald Criteria for MS diagnosis using the 2017 revision
        
        Args:
            clinical_attacks (str): Number of clinical attacks (0, 1, 2_or_more)
            objective_clinical_evidence (str): Number of lesions with objective evidence (0, 1, 2_or_more)
            dissemination_in_space (str): DIS demonstrated (not_demonstrated, demonstrated)
            dissemination_in_time (str): DIT demonstrated (not_demonstrated, demonstrated)
            csf_oligoclonal_bands (str): CSF oligoclonal bands present (absent, present, not_tested)
            alternative_diagnosis (str): Alternative diagnosis excluded (excluded, possible)
            
        Returns:
            Dict with the diagnosis and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(clinical_attacks, objective_clinical_evidence, dissemination_in_space,
                             dissemination_in_time, csf_oligoclonal_bands, alternative_diagnosis)
        
        # Evaluate McDonald Criteria
        diagnosis_result = self._evaluate_mcdonald_criteria(
            clinical_attacks, objective_clinical_evidence, dissemination_in_space,
            dissemination_in_time, csf_oligoclonal_bands, alternative_diagnosis
        )
        
        # Get interpretation
        interpretation = self._get_interpretation(diagnosis_result)
        
        return {
            "result": interpretation["stage"],
            "unit": "diagnosis",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"],
            "criteria_details": diagnosis_result["details"]
        }
    
    def _validate_inputs(self, clinical_attacks: str, objective_clinical_evidence: str,
                        dissemination_in_space: str, dissemination_in_time: str,
                        csf_oligoclonal_bands: str, alternative_diagnosis: str):
        """Validates input parameters"""
        
        if clinical_attacks not in self.CLINICAL_ATTACKS_OPTIONS:
            raise ValueError(f"Invalid clinical_attacks. Must be one of: {self.CLINICAL_ATTACKS_OPTIONS}")
        
        if objective_clinical_evidence not in self.OBJECTIVE_EVIDENCE_OPTIONS:
            raise ValueError(f"Invalid objective_clinical_evidence. Must be one of: {self.OBJECTIVE_EVIDENCE_OPTIONS}")
        
        if dissemination_in_space not in self.DISSEMINATION_OPTIONS:
            raise ValueError(f"Invalid dissemination_in_space. Must be one of: {self.DISSEMINATION_OPTIONS}")
        
        if dissemination_in_time not in self.DISSEMINATION_OPTIONS:
            raise ValueError(f"Invalid dissemination_in_time. Must be one of: {self.DISSEMINATION_OPTIONS}")
        
        if csf_oligoclonal_bands not in self.CSF_OPTIONS:
            raise ValueError(f"Invalid csf_oligoclonal_bands. Must be one of: {self.CSF_OPTIONS}")
        
        if alternative_diagnosis not in self.ALTERNATIVE_DIAGNOSIS_OPTIONS:
            raise ValueError(f"Invalid alternative_diagnosis. Must be one of: {self.ALTERNATIVE_DIAGNOSIS_OPTIONS}")
    
    def _evaluate_mcdonald_criteria(self, clinical_attacks: str, objective_clinical_evidence: str,
                                  dissemination_in_space: str, dissemination_in_time: str,
                                  csf_oligoclonal_bands: str, alternative_diagnosis: str) -> Dict[str, Any]:
        """Evaluates McDonald Criteria logic for MS diagnosis"""
        
        # Essential requirement: Alternative diagnosis must be excluded
        if alternative_diagnosis == "possible":
            return {
                "diagnosis": "not_diagnosed",
                "reason": "Alternative diagnosis not adequately excluded",
                "details": {
                    "alternative_diagnosis": "Possible alternative diagnosis present",
                    "recommendation": "Further investigation needed to exclude other conditions"
                }
            }
        
        # 2017 revision: CSF oligoclonal bands can substitute for DIT when DIS is present
        effective_dit = dissemination_in_time == "demonstrated" or (
            dissemination_in_space == "demonstrated" and csf_oligoclonal_bands == "present"
        )
        
        # McDonald Criteria evaluation based on clinical presentation
        if clinical_attacks == "2_or_more" and objective_clinical_evidence == "2_or_more":
            # ≥2 attacks, ≥2 objective clinical evidence: No additional requirements
            return {
                "diagnosis": "diagnosed",
                "reason": "≥2 clinical attacks with ≥2 objective clinical evidence",
                "details": {
                    "clinical_attacks": "≥2 attacks present",
                    "objective_evidence": "≥2 lesions with objective evidence",
                    "additional_requirements": "None needed"
                }
            }
        
        elif clinical_attacks == "2_or_more" and objective_clinical_evidence == "1":
            # ≥2 attacks, 1 objective clinical evidence: Need DIS
            if dissemination_in_space == "demonstrated":
                return {
                    "diagnosis": "diagnosed",
                    "reason": "≥2 attacks, 1 objective evidence, DIS demonstrated",
                    "details": {
                        "clinical_attacks": "≥2 attacks present",
                        "objective_evidence": "1 lesion with objective evidence",
                        "dissemination_in_space": "Demonstrated"
                    }
                }
            else:
                return {
                    "diagnosis": "insufficient",
                    "reason": "DIS not demonstrated",
                    "details": {
                        "clinical_attacks": "≥2 attacks present",
                        "objective_evidence": "1 lesion with objective evidence",
                        "dissemination_in_space": "Not demonstrated - required for diagnosis"
                    }
                }
        
        elif clinical_attacks == "1" and objective_clinical_evidence == "2_or_more":
            # 1 attack, ≥2 objective clinical evidence: Need DIT or CSF oligoclonal bands
            if effective_dit:
                return {
                    "diagnosis": "diagnosed",
                    "reason": "1 attack, ≥2 objective evidence, DIT/CSF-OCB demonstrated",
                    "details": {
                        "clinical_attacks": "1 attack present",
                        "objective_evidence": "≥2 lesions with objective evidence",
                        "dissemination_in_time": "Demonstrated" if dissemination_in_time == "demonstrated" else "Substituted by CSF oligoclonal bands"
                    }
                }
            else:
                return {
                    "diagnosis": "insufficient",
                    "reason": "DIT not demonstrated and CSF oligoclonal bands not present",
                    "details": {
                        "clinical_attacks": "1 attack present",
                        "objective_evidence": "≥2 lesions with objective evidence",
                        "dissemination_in_time": "Not demonstrated",
                        "csf_oligoclonal_bands": "Not present/tested - could substitute for DIT"
                    }
                }
        
        elif clinical_attacks == "1" and objective_clinical_evidence == "1":
            # 1 attack, 1 objective clinical evidence: Need both DIS and DIT
            if dissemination_in_space == "demonstrated" and effective_dit:
                return {
                    "diagnosis": "diagnosed",
                    "reason": "1 attack, 1 objective evidence, both DIS and DIT demonstrated",
                    "details": {
                        "clinical_attacks": "1 attack present",
                        "objective_evidence": "1 lesion with objective evidence",
                        "dissemination_in_space": "Demonstrated",
                        "dissemination_in_time": "Demonstrated" if dissemination_in_time == "demonstrated" else "Substituted by CSF oligoclonal bands"
                    }
                }
            else:
                missing_criteria = []
                if dissemination_in_space != "demonstrated":
                    missing_criteria.append("DIS")
                if not effective_dit:
                    missing_criteria.append("DIT")
                
                return {
                    "diagnosis": "insufficient",
                    "reason": f"Missing {', '.join(missing_criteria)}",
                    "details": {
                        "clinical_attacks": "1 attack present",
                        "objective_evidence": "1 lesion with objective evidence",
                        "dissemination_in_space": "Demonstrated" if dissemination_in_space == "demonstrated" else "Not demonstrated",
                        "dissemination_in_time": "Demonstrated" if effective_dit else "Not demonstrated",
                        "missing_criteria": missing_criteria
                    }
                }
        
        else:
            # Insufficient clinical presentation
            return {
                "diagnosis": "insufficient",
                "reason": "Insufficient clinical attacks or objective evidence",
                "details": {
                    "clinical_attacks": f"{clinical_attacks} attacks",
                    "objective_evidence": f"{objective_clinical_evidence} lesions with objective evidence",
                    "recommendation": "At least 1 clinical attack with objective evidence required"
                }
            }
    
    def _get_interpretation(self, diagnosis_result: Dict[str, Any]) -> Dict[str, str]:
        """
        Returns interpretation based on diagnosis result
        
        Args:
            diagnosis_result (Dict): Result from McDonald Criteria evaluation
            
        Returns:
            Dict with interpretation details
        """
        
        if diagnosis_result["diagnosis"] == "diagnosed":
            return {
                "stage": "MS Diagnosed",
                "description": "Criteria fulfilled",
                "interpretation": "The 2017 McDonald Criteria for multiple sclerosis are fulfilled. "
                               "The patient meets the diagnostic requirements for MS with evidence of "
                               "dissemination in space and time, appropriate clinical presentation, and "
                               "exclusion of alternative diagnoses. Initiate appropriate disease-modifying "
                               "therapy, provide patient education, and establish multidisciplinary care. "
                               "Monitor for disease progression and treatment response. Consider referral "
                               "to MS specialist if not already involved in care."
            }
        elif diagnosis_result["diagnosis"] == "insufficient":
            return {
                "stage": "Possible MS",
                "description": "Insufficient criteria",
                "interpretation": "The clinical and radiological findings are suggestive of multiple "
                               "sclerosis but do not fully meet the 2017 McDonald Criteria. This may "
                               "represent early disease, clinically isolated syndrome (CIS), or an "
                               "alternative diagnosis. Continue clinical monitoring with serial neurological "
                               "examinations and follow-up MRI in 3-6 months. Consider CSF analysis if not "
                               "already performed. Discuss risk of conversion to MS and potential early "
                               "treatment options if high-risk features are present."
            }
        else:  # not_diagnosed
            return {
                "stage": "MS Not Diagnosed",
                "description": "Criteria not met",
                "interpretation": "The 2017 McDonald Criteria for multiple sclerosis are not fulfilled. "
                               "The clinical presentation and findings do not meet the diagnostic requirements "
                               "for MS. Consider alternative diagnoses, continue clinical monitoring, or repeat "
                               "MRI evaluation in 3-6 months if clinical suspicion remains high. Additional "
                               "testing such as CSF analysis, visual evoked potentials, or other investigations "
                               "may be warranted based on clinical judgment."
            }


def calculate_mcdonald_criteria_multiple_sclerosis_2017_revision(
    clinical_attacks: str, objective_clinical_evidence: str, dissemination_in_space: str,
    dissemination_in_time: str, csf_oligoclonal_bands: str, alternative_diagnosis: str
) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = McdonaldCriteriaMultipleSclerosis2017RevisionCalculator()
    return calculator.calculate(clinical_attacks, objective_clinical_evidence, dissemination_in_space,
                               dissemination_in_time, csf_oligoclonal_bands, alternative_diagnosis)