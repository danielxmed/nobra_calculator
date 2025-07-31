"""
Graded Prognostic Assessment for Gastrointestinal Cancer (GI-GPA) Calculator

The GI-GPA is a validated prognostic tool for estimating survival in patients with 
gastrointestinal cancers who develop brain metastases. It uses four key prognostic 
factors to stratify patients into different survival groups, helping guide treatment 
decisions and prognostic discussions.

The score helps clinicians:
- Estimate survival for patients with GI cancers and brain metastases
- Guide treatment selection (aggressive multimodal therapy vs. palliative care)
- Support end-of-life decision-making and goals of care discussions
- Stratify patients for clinical trials involving brain metastases
- Facilitate multidisciplinary team treatment planning

References (Vancouver style):
1. Sperduto PW, Mesko S, Li J, Cagney D, Aizer A, Lin NU, et al. Estimating survival 
   in patients with gastrointestinal cancers and brain metastases: An update of the 
   graded prognostic assessment for gastrointestinal cancers (GI-GPA). Clin Transl 
   Radiat Oncol. 2019;18:39-45. doi: 10.1016/j.ctro.2019.06.009.
2. Sperduto PW, Chao ST, Sneed PK, Luo X, Suh J, Roberge D, et al. Diagnosis-specific 
   prognostic factors, indexes, and treatment outcomes for patients with newly diagnosed 
   brain metastases: a multi-institutional analysis of 4,259 patients. Int J Radiat 
   Oncol Biol Phys. 2010;77(3):655-61. doi: 10.1016/j.ijrobp.2009.08.025.
3. Sperduto PW, Yang TJ, Beal K, Pan H, Brown PD, Bangdiwala A, et al. Estimating 
   Survival in Patients With Lung Cancer and Brain Metastases: An Update of the Graded 
   Prognostic Assessment for Lung Cancer Using Molecular Markers (Lung-molGPA). JAMA 
   Oncol. 2017;3(6):827-831. doi: 10.1001/jamaoncol.2016.3834.
"""

from typing import Dict, Any


class GiGpaCalculator:
    """Calculator for Graded Prognostic Assessment for Gastrointestinal Cancer (GI-GPA)"""
    
    def __init__(self):
        # Age category points
        self.AGE_POINTS = {
            "under_60": 0.5,
            "60_or_over": 0.0
        }
        
        # Karnofsky Performance Status points
        self.KPS_POINTS = {
            "under_80": 0.0,
            "80": 1.0,
            "90_to_100": 2.0
        }
        
        # Extracranial metastases points
        self.EXTRACRANIAL_POINTS = {
            "present": 0.0,
            "absent": 0.5
        }
        
        # Number of brain metastases points
        self.BRAIN_METS_POINTS = {
            "more_than_3": 0.0,
            "2_to_3": 0.5,
            "1": 1.0
        }
        
        # Survival estimates by GI-GPA score ranges
        self.SURVIVAL_CATEGORIES = [
            {
                "min": 0.0, "max": 1.0,
                "stage": "Poor Prognosis",
                "description": "Worst survival group",
                "median_survival": "3 months"
            },
            {
                "min": 1.5, "max": 2.0,
                "stage": "Intermediate-Poor Prognosis",
                "description": "Below average survival",
                "median_survival": "9 months"
            },
            {
                "min": 2.5, "max": 3.0,
                "stage": "Intermediate Prognosis",
                "description": "Average survival",
                "median_survival": "12 months"
            },
            {
                "min": 3.5, "max": 4.0,
                "stage": "Good Prognosis",
                "description": "Best survival group",
                "median_survival": "17 months"
            }
        ]
    
    def calculate(self, age_category: str, kps: str, extracranial_metastases: str,
                 number_brain_metastases: str) -> Dict[str, Any]:
        """
        Calculates GI-GPA score from prognostic factors
        
        Args:
            age_category (str): Age category (under_60, 60_or_over)
            kps (str): Karnofsky Performance Status (under_80, 80, 90_to_100)
            extracranial_metastases (str): Presence of extracranial metastases (present, absent)
            number_brain_metastases (str): Number of brain metastases (more_than_3, 2_to_3, 1)
            
        Returns:
            Dict with GI-GPA score and clinical interpretation
        """
        
        # Validate inputs
        self._validate_inputs(age_category, kps, extracranial_metastases, number_brain_metastases)
        
        # Calculate component scores
        age_score = self.AGE_POINTS[age_category]
        kps_score = self.KPS_POINTS[kps]
        extracranial_score = self.EXTRACRANIAL_POINTS[extracranial_metastases]
        brain_mets_score = self.BRAIN_METS_POINTS[number_brain_metastases]
        
        # Calculate total GI-GPA score
        total_score = age_score + kps_score + extracranial_score + brain_mets_score
        
        # Get clinical interpretation
        interpretation = self._get_interpretation(total_score, age_category, kps,
                                                extracranial_metastases, number_brain_metastases)
        
        return {
            "result": round(total_score, 1),
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, age_category: str, kps: str, extracranial_metastases: str,
                        number_brain_metastases: str):
        """Validates input parameters"""
        
        if age_category not in self.AGE_POINTS:
            raise ValueError(f"Age category must be one of: {list(self.AGE_POINTS.keys())}")
        
        if kps not in self.KPS_POINTS:
            raise ValueError(f"KPS must be one of: {list(self.KPS_POINTS.keys())}")
        
        if extracranial_metastases not in self.EXTRACRANIAL_POINTS:
            raise ValueError(f"Extracranial metastases must be one of: {list(self.EXTRACRANIAL_POINTS.keys())}")
        
        if number_brain_metastases not in self.BRAIN_METS_POINTS:
            raise ValueError(f"Number of brain metastases must be one of: {list(self.BRAIN_METS_POINTS.keys())}")
    
    def _get_interpretation(self, score: float, age_category: str, kps: str,
                          extracranial_metastases: str, number_brain_metastases: str) -> Dict[str, str]:
        """
        Provides clinical interpretation based on GI-GPA score
        
        Returns:
            Dict with survival category, median survival, and clinical recommendations
        """
        
        # Find appropriate survival category
        survival_category = None
        for category in self.SURVIVAL_CATEGORIES:
            if category["min"] <= score <= category["max"]:
                survival_category = category
                break
        
        # Handle intermediate scores that fall between defined ranges
        if survival_category is None:
            if 1.0 < score < 1.5:
                # Between Poor and Intermediate-Poor
                survival_category = {
                    "stage": "Poor-Intermediate Prognosis",
                    "description": "Below average survival",
                    "median_survival": "6 months (estimated)"
                }
            elif 2.0 < score < 2.5:
                # Between Intermediate-Poor and Intermediate
                survival_category = {
                    "stage": "Intermediate-Poor Prognosis",
                    "description": "Below average survival",
                    "median_survival": "10 months (estimated)"
                }
            elif 3.0 < score < 3.5:
                # Between Intermediate and Good
                survival_category = {
                    "stage": "Intermediate-Good Prognosis",
                    "description": "Above average survival",
                    "median_survival": "14 months (estimated)"
                }
            else:
                # Default to closest category
                survival_category = self.SURVIVAL_CATEGORIES[0] if score <= 1.0 else self.SURVIVAL_CATEGORIES[-1]
        
        # Build parameter summary
        age_descriptions = {
            "under_60": "Age <60 years",
            "60_or_over": "Age ≥60 years"
        }
        
        kps_descriptions = {
            "under_80": "KPS <80",
            "80": "KPS 80",
            "90_to_100": "KPS 90-100"
        }
        
        extracranial_descriptions = {
            "present": "Extracranial metastases present",
            "absent": "No extracranial metastases"
        }
        
        brain_mets_descriptions = {
            "more_than_3": ">3 brain metastases",
            "2_to_3": "2-3 brain metastases",
            "1": "1 brain metastasis"
        }
        
        parameter_summary = (
            f"Clinical parameters: {age_descriptions[age_category]}, "
            f"{kps_descriptions[kps]}, {extracranial_descriptions[extracranial_metastases]}, "
            f"{brain_mets_descriptions[number_brain_metastases]}. "
        )
        
        # Generate prognostic group-specific recommendations
        if score <= 1.0:  # Poor Prognosis
            recommendations = (
                "Very poor prognosis with limited treatment options. Consider palliative care "
                "focus and comfort measures. Discuss goals of care with patient and family. "
                "Whole brain radiation therapy may be considered for symptom palliation. "
                "Avoid aggressive interventions that may worsen quality of life."
            )
        elif score <= 2.0:  # Intermediate-Poor Prognosis
            recommendations = (
                "Below average prognosis. Consider limited aggressive interventions with focus "
                "on quality of life. Palliative radiation therapy may be appropriate for "
                "symptomatic lesions. Systemic therapy decisions should weigh benefits against "
                "potential toxicity. Consider multidisciplinary team discussion."
            )
        elif score <= 3.0:  # Intermediate Prognosis
            recommendations = (
                "Moderate prognosis. Consider radiation therapy and/or surgical resection for "
                "selected patients with good performance status and limited brain disease. "
                "Systemic therapy may be beneficial. Multidisciplinary team approach recommended "
                "for treatment planning."
            )
        else:  # Good Prognosis (score > 3.0)
            recommendations = (
                "Best prognosis group. Consider aggressive multimodal therapy including surgical "
                "resection for solitary lesions, stereotactic radiosurgery for limited disease, "
                "and systemic therapy. These patients may benefit from clinical trial enrollment. "
                "Multidisciplinary team approach essential for optimal outcomes."
            )
        
        # Build comprehensive interpretation
        interpretation = (
            f"{parameter_summary}GI-GPA Score: {score:.1f} points. "
            f"Prognostic category: {survival_category['stage']} "
            f"(Median survival: {survival_category['median_survival']}). "
            f"Clinical recommendations: {recommendations} "
            f"Important note: This score should be used in conjunction with clinical judgment "
            f"and patient preferences. Consider patient's overall condition, primary tumor "
            f"control, and quality of life goals when making treatment decisions."
        )
        
        return {
            "stage": survival_category["stage"],
            "description": survival_category["description"],
            "interpretation": interpretation
        }


def calculate_gi_gpa(age_category: str, kps: str, extracranial_metastases: str,
                    number_brain_metastases: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_gi_gpa pattern
    """
    calculator = GiGpaCalculator()
    return calculator.calculate(age_category, kps, extracranial_metastases, number_brain_metastases)