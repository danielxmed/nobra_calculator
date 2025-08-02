"""
Mayo Alliance Prognostic System (MAPS) Score Calculator

Assesses prognosis of systemic mastocytosis using clinical and molecular risk factors.
Developed at Mayo Clinic to provide contemporary risk stratification for patients
with systemic mastocytosis.

References:
1. Pardanani A, Reichard KK, Zblewski D, Abdelrahman RA, Wassie EA, Koschmann J, et al. 
   Mayo alliance prognostic system for mastocytosis: clinical and hybrid clinical-molecular 
   models. Blood Adv. 2018 Nov 27;2(21):2964-2975. doi: 10.1182/bloodadvances.2018024768.
2. Sperr WR, Kundi M, Alvarez-Twose I, van Anrooij B, Oude Elberink JN, Gorska A, et al. 
   International prognostic scoring system for mastocytosis (IPSM): a retrospective cohort 
   study. Lancet Haematol. 2019 Nov;6(11):e638-e649. doi: 10.1016/S2352-3026(19)30166-8.
"""

from typing import Dict, Any


class MayoAlliancePrognosticSystemMapsScoreCalculator:
    """Calculator for Mayo Alliance Prognostic System (MAPS) Score"""
    
    def __init__(self):
        # Scoring system
        self.SM_TYPE_SCORES = {
            "indolent_smoldering_sm": 0,
            "advanced_sm": 2
        }
        
        self.AGE_THRESHOLD = 60  # Age >60 gets 1 point
        
        self.PLATELET_THRESHOLD = 150  # <150 ×10⁹/L gets 1 point
        
        self.ALP_SCORES = {
            "normal": 0,
            "elevated": 1
        }
        
        self.ADVERSE_MUTATIONS_SCORES = {
            "absent": 0,
            "present": 1
        }
        
        # Risk stratification thresholds
        self.LOW_RISK_THRESHOLD = 2  # Score ≤2
        self.INTERMEDIATE_RISK_MIN = 3
        self.INTERMEDIATE_RISK_MAX = 4
        self.HIGH_RISK_THRESHOLD = 5  # Score ≥5
        
        # Survival data
        self.SURVIVAL_DATA = {
            "low_risk": {
                "median_survival_months": 198,
                "five_year_survival_rate": 99
            },
            "intermediate_risk": {
                "median_survival_months_range": (36, 85),
                "five_year_survival_rate_range": (50, 91)
            },
            "high_risk": {
                "median_survival_months": 12,
                "five_year_survival_rate_range": (4, 24)
            }
        }
        
        # Valid options
        self.VALID_SM_TYPES = list(self.SM_TYPE_SCORES.keys())
        self.VALID_ALP_OPTIONS = list(self.ALP_SCORES.keys())
        self.VALID_MUTATION_OPTIONS = list(self.ADVERSE_MUTATIONS_SCORES.keys())
    
    def calculate(self, sm_type: str, patient_age: int, platelet_count: float,
                  serum_alp: str, adverse_mutations: str) -> Dict[str, Any]:
        """
        Calculates Mayo Alliance Prognostic System (MAPS) score
        
        Args:
            sm_type (str): Type of systemic mastocytosis
            patient_age (int): Patient age in years
            platelet_count (float): Platelet count in ×10⁹/L
            serum_alp (str): Serum alkaline phosphatase level
            adverse_mutations (str): Presence of adverse mutations
            
        Returns:
            Dict with the result and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(sm_type, patient_age, platelet_count, serum_alp, adverse_mutations)
        
        # Calculate individual component scores
        component_scores = self._calculate_component_scores(
            sm_type, patient_age, platelet_count, serum_alp, adverse_mutations
        )
        
        # Calculate total MAPS score
        total_score = sum(component_scores.values())
        
        # Get risk stratification
        risk_assessment = self._get_risk_assessment(total_score)
        
        # Get interpretation
        interpretation = self._get_interpretation(total_score)
        
        return {
            "result": {
                "maps_score": total_score,
                "component_scores": component_scores,
                "component_breakdown": {
                    "sm_type": f"SM Type ({sm_type.replace('_', ' ')}): {component_scores['sm_type']} points",
                    "age": f"Age ({patient_age} years): {component_scores['age']} points",
                    "platelets": f"Platelets ({platelet_count} ×10⁹/L): {component_scores['platelets']} points",
                    "serum_alp": f"Serum ALP ({serum_alp}): {component_scores['serum_alp']} points",
                    "adverse_mutations": f"Adverse mutations ({adverse_mutations}): {component_scores['adverse_mutations']} points"
                },
                "risk_assessment": risk_assessment
            },
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, sm_type: str, patient_age: int, platelet_count: float,
                        serum_alp: str, adverse_mutations: str):
        """Validates input parameters"""
        
        # Validate SM type
        if not isinstance(sm_type, str):
            raise ValueError("SM type must be a string")
        
        if sm_type not in self.VALID_SM_TYPES:
            raise ValueError(f"SM type must be one of {self.VALID_SM_TYPES}")
        
        # Validate age
        if not isinstance(patient_age, int):
            raise ValueError("Patient age must be an integer")
        
        if patient_age < 18 or patient_age > 100:
            raise ValueError("Patient age must be between 18 and 100 years")
        
        # Validate platelet count
        if not isinstance(platelet_count, (int, float)):
            raise ValueError("Platelet count must be a number")
        
        if platelet_count < 10 or platelet_count > 1000:
            raise ValueError("Platelet count must be between 10 and 1000 ×10⁹/L")
        
        # Validate serum ALP
        if not isinstance(serum_alp, str):
            raise ValueError("Serum ALP must be a string")
        
        if serum_alp not in self.VALID_ALP_OPTIONS:
            raise ValueError(f"Serum ALP must be one of {self.VALID_ALP_OPTIONS}")
        
        # Validate adverse mutations
        if not isinstance(adverse_mutations, str):
            raise ValueError("Adverse mutations must be a string")
        
        if adverse_mutations not in self.VALID_MUTATION_OPTIONS:
            raise ValueError(f"Adverse mutations must be one of {self.VALID_MUTATION_OPTIONS}")
    
    def _calculate_component_scores(self, sm_type: str, patient_age: int, platelet_count: float,
                                   serum_alp: str, adverse_mutations: str) -> Dict[str, int]:
        """Calculates individual MAPS component scores"""
        
        return {
            "sm_type": self.SM_TYPE_SCORES[sm_type],
            "age": 1 if patient_age > self.AGE_THRESHOLD else 0,
            "platelets": 1 if platelet_count < self.PLATELET_THRESHOLD else 0,
            "serum_alp": self.ALP_SCORES[serum_alp],
            "adverse_mutations": self.ADVERSE_MUTATIONS_SCORES[adverse_mutations]
        }
    
    def _get_risk_assessment(self, total_score: int) -> Dict[str, Any]:
        """
        Provides detailed risk assessment based on MAPS score
        
        Args:
            total_score (int): Total MAPS score
            
        Returns:
            Dict with risk assessment data
        """
        
        # Determine risk category
        if total_score <= self.LOW_RISK_THRESHOLD:
            risk_category = "Low Risk"
            survival_data = self.SURVIVAL_DATA["low_risk"]
            median_survival = f"{survival_data['median_survival_months']} months (16.5 years)"
            five_year_survival = f"{survival_data['five_year_survival_rate']}%"
            clinical_approach = "Standard monitoring and supportive care"
        elif self.INTERMEDIATE_RISK_MIN <= total_score <= self.INTERMEDIATE_RISK_MAX:
            risk_category = "Intermediate Risk"
            survival_data = self.SURVIVAL_DATA["intermediate_risk"]
            median_survival = f"{survival_data['median_survival_months_range'][0]}-{survival_data['median_survival_months_range'][1]} months (3-7 years)"
            five_year_survival = f"{survival_data['five_year_survival_rate_range'][0]}-{survival_data['five_year_survival_rate_range'][1]}%"
            clinical_approach = "Closer monitoring with earlier intervention consideration"
        else:  # High risk
            risk_category = "High Risk"
            survival_data = self.SURVIVAL_DATA["high_risk"]
            median_survival = f"{survival_data['median_survival_months']} months (1 year)"
            five_year_survival = f"{survival_data['five_year_survival_rate_range'][0]}-{survival_data['five_year_survival_rate_range'][1]}%"
            clinical_approach = "Aggressive treatment and clinical trial consideration"
        
        return {
            "risk_category": risk_category,
            "median_survival": median_survival,
            "five_year_survival_rate": five_year_survival,
            "clinical_approach": clinical_approach,
            "score_range": f"{total_score}/6 points",
            "prognosis_summary": self._get_prognosis_summary(risk_category)
        }
    
    def _get_prognosis_summary(self, risk_category: str) -> str:
        """Returns prognosis summary based on risk category"""
        
        if risk_category == "Low Risk":
            return "Excellent prognosis with prolonged survival expected"
        elif risk_category == "Intermediate Risk":
            return "Variable prognosis requiring individualized management"
        else:  # High Risk
            return "Poor prognosis requiring aggressive intervention"
    
    def _get_interpretation(self, total_score: int) -> Dict[str, str]:
        """
        Determines the clinical interpretation based on MAPS score
        
        Args:
            total_score (int): Total MAPS score
            
        Returns:
            Dict with interpretation details
        """
        
        if total_score <= self.LOW_RISK_THRESHOLD:  # Low risk (≤2 points)
            return {
                "stage": "Low Risk",
                "description": "Excellent prognosis",
                "interpretation": (
                    f"MAPS score of {total_score} indicates low risk systemic mastocytosis with "
                    f"excellent prognosis. Median survival is 198 months (16.5 years) with 5-year "
                    f"survival rate approaching 99%. These patients typically have indolent or "
                    f"smoldering disease with minimal adverse features. Standard monitoring and "
                    f"supportive care are usually sufficient, with treatment reserved for symptomatic "
                    f"disease or disease progression. Regular follow-up with complete blood counts, "
                    f"serum chemistry panels, and symptom assessment is recommended. Patient education "
                    f"about disease course and when to seek medical attention is important for optimal "
                    f"long-term management."
                )
            }
        elif self.INTERMEDIATE_RISK_MIN <= total_score <= self.INTERMEDIATE_RISK_MAX:  # Intermediate risk (3-4 points)
            return {
                "stage": "Intermediate Risk",
                "description": "Intermediate prognosis",
                "interpretation": (
                    f"MAPS score of {total_score} indicates intermediate risk systemic mastocytosis "
                    f"with variable prognosis. Median survival ranges from 36-85 months (3-7 years) "
                    f"depending on specific risk factors present. These patients require closer "
                    f"monitoring for disease progression and may benefit from earlier intervention. "
                    f"Consider treatment for symptomatic disease and regular assessment of disease "
                    f"status with appropriate supportive measures. Monitoring should include regular "
                    f"laboratory studies, bone marrow assessments as indicated, and imaging studies "
                    f"to evaluate organ involvement. Discuss treatment options and consider referral "
                    f"to specialized centers with expertise in systemic mastocytosis management."
                )
            }
        else:  # High risk (≥5 points)
            return {
                "stage": "High Risk",
                "description": "Poor prognosis",
                "interpretation": (
                    f"MAPS score of {total_score} indicates high risk systemic mastocytosis with "
                    f"poor prognosis. Median survival is approximately 12 months with 5-year survival "
                    f"rate of only 4-24%. These patients typically have advanced systemic mastocytosis "
                    f"with multiple adverse features including organ dysfunction, cytopenias, or "
                    f"aggressive disease course. Aggressive treatment should be considered, including "
                    f"targeted therapies (such as KIT inhibitors), cytoreductive treatment, or "
                    f"enrollment in clinical trials. Multidisciplinary care involving hematology, "
                    f"oncology, and supportive care services is essential. Palliative care consultation "
                    f"may be appropriate to optimize quality of life and manage symptoms. Consider "
                    f"stem cell transplantation evaluation in appropriate candidates."
                )
            }


def calculate_mayo_alliance_prognostic_system_maps_score(
    sm_type: str, patient_age: int, platelet_count: float, serum_alp: str, 
    adverse_mutations: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = MayoAlliancePrognosticSystemMapsScoreCalculator()
    return calculator.calculate(sm_type, patient_age, platelet_count, serum_alp, adverse_mutations)