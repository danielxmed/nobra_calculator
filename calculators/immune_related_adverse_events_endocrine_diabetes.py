"""
Immune-Related Adverse Events for Endocrine Toxicities - Diabetes Mellitus Calculator

Grades severity of hyperglycemia secondary to immune checkpoint inhibitor therapy
and provides management recommendations based on CTCAE Version 5.0 criteria.

References (Vancouver style):
1. Brahmer JR, Lacchetti C, Schneider BJ, Atkins MB, Brassil KJ, Caterino JM, et al. 
   Management of Immune-Related Adverse Events in Patients Treated With Immune 
   Checkpoint Inhibitor Therapy: American Society of Clinical Oncology Clinical 
   Practice Guideline. J Clin Oncol. 2018 Jun 10;36(17):1714-1768. 
   doi: 10.1200/JCO.2017.77.6385.

2. Thompson JA, Schneider BJ, Brahmer J, Andrews S, Armand P, Bhatia S, et al. 
   NCCN Guidelines Insights: Management of Immunotherapy-Related Toxicities, 
   Version 1.2020. J Natl Compr Canc Netw. 2020 Mar 1;18(3):230-241. 
   doi: 10.6004/jnccn.2020.0012.

3. Stamatouli AM, Quandt Z, Perdigoto AL, Clark PL, Kluger H, Weiss SA, et al. 
   Collateral Damage: Insulin-Dependent Diabetes Induced by Immune Checkpoint 
   Inhibitors. Diabetes. 2018 Aug;67(8):1471-1480. doi: 10.2337/dbi18-0002.

4. Akturk HK, Alkanani A, Karanchi H, Nair V, Michels AW, Ostrom QT, et al. 
   Immune checkpoint inhibitor-induced Type 1 diabetes: a systematic review 
   and meta-analysis. Diabet Med. 2019 Sep;36(9):1075-1081. doi: 10.1111/dme.14050.
"""

from typing import Dict, Any


class ImmuneRelatedAdverseEventsEndocrineDiabetesCalculator:
    """Calculator for immune-related adverse events endocrine diabetes mellitus grading"""
    
    def __init__(self):
        # Glucose thresholds in mg/dL
        self.glucose_thresholds = {
            "grade_1_min": 160.0,  # >160 mg/dL for Grade 1
            "grade_2_min": 160.0,  # 160-250 mg/dL for Grade 2
            "grade_2_max": 250.0,
            "grade_3_min": 250.0,  # 250-500 mg/dL for Grade 3
            "grade_3_max": 500.0,
            "grade_4_min": 500.0   # >500 mg/dL for Grade 4
        }
        
        # Management recommendations by grade
        self.management_recommendations = {
            1: {
                "icpi_action": "Continue ICPi",
                "monitoring": "Close clinical follow-up",
                "treatment": "Consider oral medications for new-onset Type 2 diabetes",
                "consultation": "Screen for T1DM if clinically indicated"
            },
            2: {
                "icpi_action": "May hold ICPi until glucose controlled",
                "monitoring": "Urgent endocrine consultation",
                "treatment": "Titrate oral therapy or consider insulin",
                "consultation": "Potential hospital admission if ketoacidosis present"
            },
            3: {
                "icpi_action": "Hold ICPi until toxicity recovers to grade ≤1",
                "monitoring": "Urgent endocrine consultation required",
                "treatment": "Initiate insulin therapy",
                "consultation": "Admit if concern for DKA or symptomatic"
            },
            4: {
                "icpi_action": "Hold ICPi until toxicity recovers to grade ≤1",
                "monitoring": "Urgent endocrine consultation required",
                "treatment": "Initiate insulin therapy immediately",
                "consultation": "Hospital admission mandatory for DKA management"
            }
        }
    
    def calculate(self, fasting_glucose_mg_dl: float, ketosis_or_t1dm_evidence: str,
                  symptom_severity: str) -> Dict[str, Any]:
        """
        Calculates the irAE grade for endocrine diabetes mellitus
        
        Args:
            fasting_glucose_mg_dl (float): Fasting glucose level in mg/dL
            ketosis_or_t1dm_evidence (str): "yes" or "no" for ketosis/T1DM evidence
            symptom_severity (str): "asymptomatic_mild", "moderate_able_adls", or "severe_unable_adls"
            
        Returns:
            Dict with the result and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(fasting_glucose_mg_dl, ketosis_or_t1dm_evidence, symptom_severity)
        
        # Determine grade based on criteria
        grade = self._determine_grade(fasting_glucose_mg_dl, ketosis_or_t1dm_evidence, symptom_severity)
        
        # Get interpretation
        interpretation = self._get_interpretation(grade)
        
        return {
            "result": grade,
            "unit": "grade",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["grade"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, fasting_glucose_mg_dl: float, ketosis_or_t1dm_evidence: str,
                        symptom_severity: str):
        """Validates input parameters"""
        
        # Validate fasting glucose
        if not isinstance(fasting_glucose_mg_dl, (int, float)):
            raise ValueError("fasting_glucose_mg_dl must be a number")
        
        if fasting_glucose_mg_dl < 70 or fasting_glucose_mg_dl > 1000:
            raise ValueError("fasting_glucose_mg_dl must be between 70 and 1000 mg/dL")
        
        # Validate ketosis/T1DM evidence
        if ketosis_or_t1dm_evidence not in ["yes", "no"]:
            raise ValueError("ketosis_or_t1dm_evidence must be 'yes' or 'no'")
        
        # Validate symptom severity
        valid_symptoms = ["asymptomatic_mild", "moderate_able_adls", "severe_unable_adls"]
        if symptom_severity not in valid_symptoms:
            raise ValueError(f"symptom_severity must be one of: {valid_symptoms}")
    
    def _determine_grade(self, fasting_glucose_mg_dl: float, ketosis_or_t1dm_evidence: str,
                        symptom_severity: str) -> int:
        """Determines the irAE grade based on clinical criteria"""
        
        # Special case: Ketosis or T1DM evidence at any glucose level = at least Grade 2
        if ketosis_or_t1dm_evidence == "yes":
            if symptom_severity == "severe_unable_adls":
                # If severe symptoms with ketosis/T1DM, check glucose for Grade 3 vs 4
                if fasting_glucose_mg_dl >= self.glucose_thresholds["grade_4_min"]:
                    return 4
                else:
                    return 3
            else:
                return 2
        
        # No ketosis/T1DM evidence - grade based on glucose and symptoms
        if fasting_glucose_mg_dl >= self.glucose_thresholds["grade_4_min"]:
            # >500 mg/dL
            if symptom_severity == "severe_unable_adls":
                return 4
            else:
                return 3  # High glucose but not severe symptoms
                
        elif fasting_glucose_mg_dl >= self.glucose_thresholds["grade_3_min"]:
            # 250-500 mg/dL
            if symptom_severity == "severe_unable_adls":
                return 3
            else:
                return 2  # Moderate glucose, not severe symptoms
                
        elif fasting_glucose_mg_dl >= self.glucose_thresholds["grade_2_min"]:
            # 160-250 mg/dL
            if symptom_severity == "severe_unable_adls":
                return 3  # Lower glucose but severe symptoms
            elif symptom_severity == "moderate_able_adls":
                return 2
            else:
                return 1  # Mild symptoms
                
        elif fasting_glucose_mg_dl > self.glucose_thresholds["grade_1_min"]:
            # >160 mg/dL but <160 threshold (edge case)
            return 1
            
        else:
            # <160 mg/dL - likely not irAE diabetes, but return Grade 1 as minimum
            return 1
    
    def _get_interpretation(self, grade: int) -> Dict[str, str]:
        """
        Gets the clinical interpretation based on the grade
        
        Args:
            grade (int): irAE grade (1-4)
            
        Returns:
            Dict with interpretation details
        """
        
        interpretations = {
            1: {
                "grade": "Grade 1",
                "description": "Mild - Asymptomatic or mild symptoms",
                "interpretation": (
                    "Continue immune checkpoint inhibitor (ICPi). Close clinical follow-up required. "
                    "Consider oral medications for new-onset Type 2 diabetes. Screen for T1DM if "
                    "clinically indicated. Fasting glucose >160 mg/dL (>8.9 mmol/L) without ketosis "
                    "or T1DM evidence."
                )
            },
            2: {
                "grade": "Grade 2",
                "description": "Moderate - Moderate symptoms, able to perform ADLs",
                "interpretation": (
                    "May hold ICPi until glucose controlled. Titrate oral therapy or consider insulin. "
                    "Obtain urgent endocrine consultation. Potential hospital admission if ketoacidosis "
                    "present. Applies to glucose 160-250 mg/dL (8.9-13.9 mmol/L) OR ketosis/T1DM "
                    "evidence at any glucose level."
                )
            },
            3: {
                "grade": "Grade 3",
                "description": "Severe - Severe symptoms, unable to perform ADLs",
                "interpretation": (
                    "Hold ICPi until toxicity recovers to grade ≤1. Urgent endocrine consultation "
                    "required. Initiate insulin therapy. Admit if concern for diabetic ketoacidosis "
                    "or symptomatic. Fasting glucose 250-500 mg/dL (13.9-27.8 mmol/L) with severe symptoms."
                )
            },
            4: {
                "grade": "Grade 4",
                "description": "Life-threatening - Severe symptoms, life-threatening consequences",
                "interpretation": (
                    "Hold ICPi until toxicity recovers to grade ≤1. Urgent endocrine consultation "
                    "required. Initiate insulin therapy immediately. Hospital admission mandatory "
                    "for diabetic ketoacidosis management. Fasting glucose >500 mg/dL (>27.8 mmol/L) "
                    "with severe symptoms."
                )
            }
        }
        
        return interpretations.get(grade, interpretations[4])  # Default to Grade 4 if invalid


def calculate_immune_related_adverse_events_endocrine_diabetes(
    fasting_glucose_mg_dl: float, ketosis_or_t1dm_evidence: str, 
    symptom_severity: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_immune_related_adverse_events_endocrine_diabetes pattern
    """
    calculator = ImmuneRelatedAdverseEventsEndocrineDiabetesCalculator()
    return calculator.calculate(fasting_glucose_mg_dl, ketosis_or_t1dm_evidence, symptom_severity)