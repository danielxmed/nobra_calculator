"""
MASCC Risk Index for Febrile Neutropenia Calculator

Identifies febrile neutropenia patients at low risk for poor outcome including death,
intensive care unit admission, confusion, cardiac complications, respiratory failure,
renal failure, hypotension, bleeding, and other serious medical complications.

References:
1. Klastersky J, Paesmans M, Rubenstein EB, Boyer M, Elting L, Feld R, et al. 
   The Multinational Association for Supportive Care in Cancer risk index: 
   A multinational scoring system for identifying low-risk febrile neutropenic 
   cancer patients. J Clin Oncol. 2000 Aug;18(16):3038-51. doi: 10.1200/JCO.2000.18.16.3038.
2. Freifeld AG, Bow EJ, Sepkowitz KA, Boeckh MJ, Ito JI, Mullen CA, et al. 
   Clinical practice guideline for the use of antimicrobial agents in neutropenic 
   patients with cancer: 2010 update by the infectious diseases society of america. 
   Clin Infect Dis. 2011 Feb 15;52(4):e56-93. doi: 10.1093/cid/cir073.
"""

from typing import Dict, Any


class MasccRiskIndexFebrileNeutropeniaCalculator:
    """Calculator for MASCC Risk Index for Febrile Neutropenia"""
    
    def __init__(self):
        # Risk threshold
        self.LOW_RISK_THRESHOLD = 21  # Score ≥21 is low risk
        
        # Scoring system
        self.BURDEN_OF_ILLNESS_SCORES = {
            "none_mild": 5,
            "moderate": 3,
            "severe": 0
        }
        
        self.HYPOTENSION_SCORES = {
            "no": 5,
            "yes": 0
        }
        
        self.COPD_SCORES = {
            "no": 4,
            "yes": 0
        }
        
        self.CANCER_TYPE_SCORES = {
            "solid_tumor_or_hematologic_no_prior_fungal": 4,
            "hematologic_with_prior_fungal": 0
        }
        
        self.DEHYDRATION_SCORES = {
            "no": 3,
            "yes": 0
        }
        
        self.FEVER_ONSET_SCORES = {
            "outpatient": 3,
            "inpatient": 0
        }
        
        self.AGE_THRESHOLD = 60  # Age ≥60 gets 0 points, <60 gets 2 points
        
        # Valid options
        self.VALID_BURDEN_OPTIONS = ["none_mild", "moderate", "severe"]
        self.VALID_YES_NO_OPTIONS = ["yes", "no"]
        self.VALID_CANCER_OPTIONS = ["solid_tumor_or_hematologic_no_prior_fungal", "hematologic_with_prior_fungal"]
        self.VALID_FEVER_ONSET_OPTIONS = ["outpatient", "inpatient"]
    
    def calculate(self, burden_of_illness: str, hypotension: str, active_copd: str,
                  cancer_type: str, dehydration_requiring_iv: str, fever_onset_status: str,
                  patient_age: int) -> Dict[str, Any]:
        """
        Calculates MASCC Risk Index for febrile neutropenia
        
        Args:
            burden_of_illness (str): Symptom severity ("none_mild", "moderate", "severe")
            hypotension (str): Systolic BP <90 mmHg ("yes", "no")
            active_copd (str): Active COPD ("yes", "no")
            cancer_type (str): Cancer type and fungal history
            dehydration_requiring_iv (str): Dehydration requiring IV fluids ("yes", "no")
            fever_onset_status (str): Status at fever onset ("outpatient", "inpatient")
            patient_age (int): Patient age in years
            
        Returns:
            Dict with the result and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(burden_of_illness, hypotension, active_copd, cancer_type,
                             dehydration_requiring_iv, fever_onset_status, patient_age)
        
        # Calculate individual component scores
        component_scores = self._calculate_component_scores(
            burden_of_illness, hypotension, active_copd, cancer_type,
            dehydration_requiring_iv, fever_onset_status, patient_age
        )
        
        # Calculate total score
        total_score = sum(component_scores.values())
        
        # Get interpretation
        interpretation = self._get_interpretation(total_score)
        
        # Get detailed assessment
        assessment_data = self._get_assessment_data(total_score, component_scores)
        
        return {
            "result": {
                "total_score": total_score,
                "component_scores": component_scores,
                "component_breakdown": {
                    "burden_of_illness": f"Burden of illness ({burden_of_illness.replace('_', ' ')}): {component_scores['burden_of_illness']} points",
                    "hypotension": f"Hypotension: {component_scores['hypotension']} points",
                    "active_copd": f"Active COPD: {component_scores['active_copd']} points",
                    "cancer_type": f"Cancer type: {component_scores['cancer_type']} points",
                    "dehydration": f"Dehydration requiring IV: {component_scores['dehydration']} points",
                    "fever_onset": f"Fever onset status ({fever_onset_status}): {component_scores['fever_onset']} points",
                    "age": f"Age ({patient_age} years): {component_scores['age']} points"
                },
                "assessment_data": assessment_data
            },
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, burden_of_illness: str, hypotension: str, active_copd: str,
                        cancer_type: str, dehydration_requiring_iv: str, fever_onset_status: str,
                        patient_age: int):
        """Validates input parameters"""
        
        # Validate burden of illness
        if not isinstance(burden_of_illness, str):
            raise ValueError("Burden of illness must be a string")
        
        if burden_of_illness not in self.VALID_BURDEN_OPTIONS:
            raise ValueError(f"Burden of illness must be one of {self.VALID_BURDEN_OPTIONS}")
        
        # Validate yes/no parameters
        yes_no_params = {
            "hypotension": hypotension,
            "active_copd": active_copd,
            "dehydration_requiring_iv": dehydration_requiring_iv
        }
        
        for param_name, param_value in yes_no_params.items():
            if not isinstance(param_value, str):
                raise ValueError(f"{param_name} must be a string")
            
            if param_value.lower() not in [option.lower() for option in self.VALID_YES_NO_OPTIONS]:
                raise ValueError(f"{param_name} must be 'yes' or 'no'")
        
        # Validate cancer type
        if not isinstance(cancer_type, str):
            raise ValueError("Cancer type must be a string")
        
        if cancer_type not in self.VALID_CANCER_OPTIONS:
            raise ValueError(f"Cancer type must be one of {self.VALID_CANCER_OPTIONS}")
        
        # Validate fever onset status
        if not isinstance(fever_onset_status, str):
            raise ValueError("Fever onset status must be a string")
        
        if fever_onset_status not in self.VALID_FEVER_ONSET_OPTIONS:
            raise ValueError(f"Fever onset status must be one of {self.VALID_FEVER_ONSET_OPTIONS}")
        
        # Validate age
        if not isinstance(patient_age, int):
            raise ValueError("Patient age must be an integer")
        
        if patient_age < 18 or patient_age > 100:
            raise ValueError("Patient age must be between 18 and 100 years")
    
    def _calculate_component_scores(self, burden_of_illness: str, hypotension: str,
                                   active_copd: str, cancer_type: str, dehydration_requiring_iv: str,
                                   fever_onset_status: str, patient_age: int) -> Dict[str, int]:
        """Calculates individual MASCC component scores"""
        
        return {
            "burden_of_illness": self.BURDEN_OF_ILLNESS_SCORES[burden_of_illness],
            "hypotension": self.HYPOTENSION_SCORES[hypotension.lower()],
            "active_copd": self.COPD_SCORES[active_copd.lower()],
            "cancer_type": self.CANCER_TYPE_SCORES[cancer_type],
            "dehydration": self.DEHYDRATION_SCORES[dehydration_requiring_iv.lower()],
            "fever_onset": self.FEVER_ONSET_SCORES[fever_onset_status],
            "age": 2 if patient_age < self.AGE_THRESHOLD else 0
        }
    
    def _get_assessment_data(self, total_score: int, component_scores: Dict[str, int]) -> Dict[str, str]:
        """
        Returns detailed assessment data based on MASCC score
        
        Args:
            total_score (int): Total MASCC score
            component_scores (Dict[str, int]): Individual component scores
            
        Returns:
            Dict with assessment information
        """
        
        # Determine risk category and recommendations
        if total_score >= self.LOW_RISK_THRESHOLD:
            risk_level = "Low Risk"
            ppv = "91%"
            recommendation = "Consider oral antibiotic therapy and/or outpatient management"
            management = "Outpatient management with close follow-up may be appropriate"
            monitoring = "Reliable access to medical care and ability to return if worsening"
        else:
            risk_level = "High Risk"
            ppv = "Not applicable"
            recommendation = "Admit for empiric intravenous antibiotics if not already inpatient"
            management = "Inpatient monitoring and aggressive supportive care essential"
            monitoring = "ICU-level care may be required for severe complications"
        
        return {
            "risk_level": risk_level,
            "positive_predictive_value": ppv,
            "recommendation": recommendation,
            "management_approach": management,
            "monitoring_requirements": monitoring,
            "score_threshold": f"Cut-off ≥{self.LOW_RISK_THRESHOLD} points for low risk",
            "original_validation": "PPV 91%, Sensitivity 71%, Specificity 68%",
            "external_validation": "PPV range 83-98%, Sensitivity range 59-95%",
            "clinical_judgment": "Clinical assessment should always override score when indicated"
        }
    
    def _get_interpretation(self, total_score: int) -> Dict[str, str]:
        """
        Determines the risk category and interpretation
        
        Args:
            total_score (int): Total MASCC score
            
        Returns:
            Dict with risk category and clinical interpretation
        """
        
        if total_score >= self.LOW_RISK_THRESHOLD:  # ≥21 points
            return {
                "stage": "Low Risk",
                "description": "Low risk for complications",
                "interpretation": (
                    f"MASCC Risk Index score of {total_score} indicates low risk for serious "
                    f"complications of febrile neutropenia with 91% positive predictive value for "
                    f"uncomplicated course. These patients may be considered for oral antibiotic "
                    f"therapy and/or outpatient management with close follow-up. However, clinical "
                    f"judgment should always override the score, and patients must have reliable "
                    f"access to medical care with ability to return immediately if symptoms worsen. "
                    f"Outpatient management requires careful patient selection, adequate social "
                    f"support, and comprehensive patient education about warning signs requiring "
                    f"immediate medical attention."
                )
            }
        else:  # <21 points
            return {
                "stage": "High Risk",
                "description": "High risk for complications",
                "interpretation": (
                    f"MASCC Risk Index score of {total_score} indicates high risk for serious "
                    f"complications of febrile neutropenia. These patients require admission for "
                    f"empiric intravenous antibiotics if not already hospitalized. High-risk patients "
                    f"have increased likelihood of developing life-threatening complications including "
                    f"death, intensive care unit admission, confusion, cardiac complications, "
                    f"respiratory failure, renal failure, hypotension, bleeding, and other serious "
                    f"medical complications. Inpatient monitoring with prompt recognition and "
                    f"treatment of complications is essential. Consider early infectious disease "
                    f"consultation and aggressive supportive care measures."
                )
            }


def calculate_mascc_risk_index_febrile_neutropenia(burden_of_illness: str, hypotension: str,
                                                  active_copd: str, cancer_type: str,
                                                  dehydration_requiring_iv: str, fever_onset_status: str,
                                                  patient_age: int) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = MasccRiskIndexFebrileNeutropeniaCalculator()
    return calculator.calculate(burden_of_illness, hypotension, active_copd, cancer_type,
                               dehydration_requiring_iv, fever_onset_status, patient_age)