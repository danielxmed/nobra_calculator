"""
International Working Group (IWG) 2 Criteria for Alzheimer's Disease Diagnosis Calculator

Diagnoses Alzheimer's disease using revised research diagnostic criteria that integrate 
clinical phenotypes with pathophysiological biomarkers.

References (Vancouver style):
1. Dubois B, Feldman HH, Jacova C, Hampel H, Molinuevo JL, Blennow K, et al. Advancing 
   research diagnostic criteria for Alzheimer's disease: the IWG-2 criteria. Lancet Neurol. 
   2014 Jun;13(6):614-29. doi: 10.1016/S1474-4422(14)70090-0.
2. Jack CR Jr, Bennett DA, Blennow K, Carrillo MC, Dunn B, Haeberlein SB, et al. NIA-AA 
   Research Framework: Toward a biological definition of Alzheimer's disease. Alzheimers 
   Dement. 2018 Apr;14(4):535-562. doi: 10.1016/j.jalz.2018.02.018.
3. Dubois B, Hampel H, Feldman HH, Scheltens P, Aisen P, Andrieu S, et al. Preclinical 
   Alzheimer's disease: Definition, natural history, and diagnostic criteria. Alzheimers 
   Dement. 2016 Mar;12(3):292-323. doi: 10.1016/j.jalz.2016.02.002.
"""

from typing import Dict, Any


class Iwg2AlzheimerCriteriaCalculator:
    """Calculator for International Working Group (IWG) 2 Criteria for Alzheimer's Disease Diagnosis"""
    
    def __init__(self):
        # Valid parameter values
        self.valid_values = {
            "clinical_phenotype": ["typical_ad", "atypical_ad", "mixed_ad", "asymptomatic"],
            "memory_impairment": ["present", "absent"],
            "cognitive_domains_affected": ["single_domain", "multiple_domains"],
            "csf_amyloid_beta": ["normal", "decreased", "not_available"],
            "csf_tau": ["normal", "elevated", "not_available"],
            "csf_ptau": ["normal", "elevated", "not_available"],
            "amyloid_pet": ["negative", "positive", "not_available"],
            "functional_decline": ["present", "absent", "mild"]
        }
    
    def calculate(self, clinical_phenotype: str, memory_impairment: str, cognitive_domains_affected: str,
                  csf_amyloid_beta: str, csf_tau: str, csf_ptau: str, amyloid_pet: str, 
                  functional_decline: str) -> Dict[str, Any]:
        """
        Evaluates IWG-2 criteria for Alzheimer's disease diagnosis
        
        Args:
            clinical_phenotype (str): Clinical presentation pattern
            memory_impairment (str): Presence of episodic memory impairment
            cognitive_domains_affected (str): Number of cognitive domains impaired
            csf_amyloid_beta (str): CSF Aβ1-42 levels
            csf_tau (str): CSF total tau levels
            csf_ptau (str): CSF phosphorylated tau levels
            amyloid_pet (str): Amyloid PET imaging results
            functional_decline (str): Progressive functional decline
            
        Returns:
            Dict with the diagnostic assessment and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(clinical_phenotype, memory_impairment, cognitive_domains_affected,
                            csf_amyloid_beta, csf_tau, csf_ptau, amyloid_pet, functional_decline)
        
        # Evaluate diagnostic criteria
        diagnosis = self._evaluate_criteria(clinical_phenotype, memory_impairment, cognitive_domains_affected,
                                          csf_amyloid_beta, csf_tau, csf_ptau, amyloid_pet, functional_decline)
        
        # Get interpretation based on diagnosis
        interpretation = self._get_interpretation(diagnosis)
        
        return {
            "result": diagnosis,
            "unit": "diagnosis",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, clinical_phenotype: str, memory_impairment: str, cognitive_domains_affected: str,
                        csf_amyloid_beta: str, csf_tau: str, csf_ptau: str, amyloid_pet: str, 
                        functional_decline: str):
        """Validates input parameters"""
        
        parameters = {
            "clinical_phenotype": clinical_phenotype,
            "memory_impairment": memory_impairment,
            "cognitive_domains_affected": cognitive_domains_affected,
            "csf_amyloid_beta": csf_amyloid_beta,
            "csf_tau": csf_tau,
            "csf_ptau": csf_ptau,
            "amyloid_pet": amyloid_pet,
            "functional_decline": functional_decline
        }
        
        for param_name, param_value in parameters.items():
            if param_value not in self.valid_values[param_name]:
                raise ValueError(f"{param_name} must be one of: {self.valid_values[param_name]}")
    
    def _evaluate_criteria(self, clinical_phenotype: str, memory_impairment: str, cognitive_domains_affected: str,
                          csf_amyloid_beta: str, csf_tau: str, csf_ptau: str, amyloid_pet: str, 
                          functional_decline: str) -> str:
        """Evaluates IWG-2 diagnostic criteria"""
        
        # Check for pathophysiological biomarker evidence
        biomarker_positive = self._has_pathophysiological_biomarkers(csf_amyloid_beta, csf_tau, csf_ptau, amyloid_pet)
        
        # Asymptomatic individuals with positive biomarkers
        if clinical_phenotype == "asymptomatic":
            if biomarker_positive:
                return "asymptomatic_at_risk"
            else:
                return "insufficient_criteria"
        
        # Symptomatic individuals - need both clinical phenotype and biomarkers
        if clinical_phenotype in ["typical_ad", "atypical_ad", "mixed_ad"]:
            # Check clinical criteria
            clinical_criteria_met = self._meets_clinical_criteria(clinical_phenotype, memory_impairment, 
                                                                cognitive_domains_affected, functional_decline)
            
            if clinical_criteria_met and biomarker_positive:
                return clinical_phenotype
            else:
                return "insufficient_criteria"
        
        return "insufficient_criteria"
    
    def _has_pathophysiological_biomarkers(self, csf_amyloid_beta: str, csf_tau: str, 
                                         csf_ptau: str, amyloid_pet: str) -> bool:
        """Checks for pathophysiological biomarker evidence"""
        
        # CSF biomarkers
        csf_ab_positive = csf_amyloid_beta == "decreased"
        csf_tau_positive = csf_tau == "elevated"
        csf_ptau_positive = csf_ptau == "elevated"
        
        # Amyloid PET
        amyloid_pet_positive = amyloid_pet == "positive"
        
        # Need at least one pathophysiological biomarker
        # CSF pattern: Low Aβ1-42 and/or elevated tau markers
        csf_positive = csf_ab_positive or csf_tau_positive or csf_ptau_positive
        
        return csf_positive or amyloid_pet_positive
    
    def _meets_clinical_criteria(self, clinical_phenotype: str, memory_impairment: str, 
                               cognitive_domains_affected: str, functional_decline: str) -> bool:
        """Checks if clinical criteria are met"""
        
        if clinical_phenotype == "typical_ad":
            # Typical AD requires episodic memory impairment
            return (memory_impairment == "present" and 
                   (functional_decline in ["present", "mild"]))
        
        elif clinical_phenotype == "atypical_ad":
            # Atypical AD may not have prominent memory impairment
            return (cognitive_domains_affected == "multiple_domains" and 
                   (functional_decline in ["present", "mild"]))
        
        elif clinical_phenotype == "mixed_ad":
            # Mixed AD has variable presentations
            return (cognitive_domains_affected == "multiple_domains" and 
                   (functional_decline in ["present", "mild"]))
        
        return False
    
    def _get_interpretation(self, diagnosis: str) -> Dict[str, str]:
        """
        Determines the interpretation based on the diagnostic result
        
        Args:
            diagnosis (str): Diagnostic classification
            
        Returns:
            Dict with diagnostic interpretation
        """
        
        interpretations = {
            "typical_ad": {
                "stage": "Typical AD",
                "description": "Meets criteria for typical Alzheimer's disease",
                "interpretation": "Diagnosis of typical Alzheimer's disease confirmed. Clinical phenotype shows characteristic episodic memory impairment with pathophysiological biomarker evidence. Recommend standard AD treatment protocols, monitoring for disease progression, and consideration for appropriate clinical trials. Discuss prognosis and long-term care planning with patient and family."
            },
            "atypical_ad": {
                "stage": "Atypical AD",
                "description": "Meets criteria for atypical Alzheimer's disease",
                "interpretation": "Diagnosis of atypical Alzheimer's disease confirmed. Non-amnestic presentation with pathophysiological biomarker evidence of AD pathology. Consider specialized management for atypical presentations. Monitor for progression and adapt treatment strategies accordingly. Clinical trial enrollment may be appropriate."
            },
            "mixed_ad": {
                "stage": "Mixed AD",
                "description": "Meets criteria for mixed Alzheimer's disease",
                "interpretation": "Diagnosis of mixed Alzheimer's disease confirmed. AD pathology coexisting with other neurodegenerative processes. Comprehensive management addressing multiple pathologies may be needed. Consider interdisciplinary approach and targeted interventions for mixed presentations."
            },
            "asymptomatic_at_risk": {
                "stage": "Asymptomatic at Risk",
                "description": "Asymptomatic at risk for Alzheimer's disease",
                "interpretation": "Positive amyloid biomarkers in cognitively normal individual. Increased lifetime risk of developing symptomatic AD. Consider enrollment in prevention trials. Regular cognitive monitoring recommended. Lifestyle interventions and risk factor management may be beneficial."
            },
            "insufficient_criteria": {
                "stage": "Insufficient Criteria",
                "description": "Does not meet IWG-2 criteria for AD diagnosis",
                "interpretation": "Insufficient evidence to diagnose AD by IWG-2 criteria. Either clinical phenotype or pathophysiological biomarkers do not support AD diagnosis. Consider alternative diagnoses, additional testing, or monitoring for development of diagnostic criteria over time."
            }
        }
        
        return interpretations.get(diagnosis, interpretations["insufficient_criteria"])


def calculate_iwg2_alzheimer_criteria(clinical_phenotype: str, memory_impairment: str, cognitive_domains_affected: str,
                                    csf_amyloid_beta: str, csf_tau: str, csf_ptau: str, amyloid_pet: str, 
                                    functional_decline: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    Evaluates IWG-2 criteria for Alzheimer's disease diagnosis using clinical phenotype
    and pathophysiological biomarker evidence.
    
    Args:
        clinical_phenotype (str): Clinical presentation pattern
        memory_impairment (str): Presence of episodic memory impairment
        cognitive_domains_affected (str): Number of cognitive domains impaired
        csf_amyloid_beta (str): CSF Aβ1-42 levels
        csf_tau (str): CSF total tau levels
        csf_ptau (str): CSF phosphorylated tau levels
        amyloid_pet (str): Amyloid PET imaging results
        functional_decline (str): Progressive functional decline
        
    Returns:
        Dict with diagnostic assessment and clinical recommendations
    """
    calculator = Iwg2AlzheimerCriteriaCalculator()
    return calculator.calculate(clinical_phenotype, memory_impairment, cognitive_domains_affected,
                              csf_amyloid_beta, csf_tau, csf_ptau, amyloid_pet, functional_decline)