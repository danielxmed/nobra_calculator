"""
King's College Criteria for Acetaminophen Toxicity Models

Request and response models for King's College Criteria calculation.

References (Vancouver style):
1. O'Grady JG, Alexander GJ, Hayllar KM, Williams R. Early indicators of prognosis 
   in fulminant hepatic failure. Gastroenterology. 1989 Aug;97(2):439-45.
2. Bailey B, Amre DK, Gaudreault P. Fulminant hepatic failure secondary to 
   acetaminophen poisoning: a systematic review and meta-analysis of prognostic 
   criteria determining the need for liver transplantation. Crit Care Med. 2003 
   Jan;31(1):299-305.
3. Bernal W, Auzinger G, Dhawan A, Wendon J. Acute liver failure. Lancet. 2010 
   Jul 17;376(9736):190-201.
4. Larson AM, Polson J, Fontana RJ, Davern TJ, Lalani E, Hynan LS, et al. 
   Acetaminophen-induced acute liver failure: results of a United States multicenter, 
   prospective study. Hepatology. 2005 Dec;42(6):1364-72.

The King's College Criteria for Acetaminophen Toxicity is a clinical decision tool 
developed to identify patients with acetaminophen-induced acute liver failure who 
have a poor prognosis and require urgent consideration for liver transplantation. 
The criteria were first described by O'Grady et al. in 1989 and remain the gold 
standard for liver transplant decision-making in acetaminophen toxicity.

The criteria identify two patient groups with poor prognosis:
1. Arterial pH <7.30 (regardless of other factors)
2. All three of: INR >6.5, creatinine >3.4 mg/dL, and Grade III/IV encephalopathy

Additional prognostic markers that may enhance prediction include elevated lactate 
(>3.5 mmol/L after early resuscitation or >3.0 mmol/L after full resuscitation) 
and elevated phosphate (>3.75 mg/dL at 48-96 hours).

Clinical performance: 95% specificity, 58% sensitivity for predicting mortality. 
The criteria are highly specific but not sensitive, meaning that meeting the criteria 
indicates poor prognosis, but not meeting them does not guarantee good outcomes.
"""

from pydantic import BaseModel, Field
from typing import Literal, Dict, Optional


class KingsCollegeCriteriaAcetaminophenRequest(BaseModel):
    """
    Request model for King's College Criteria for Acetaminophen Toxicity
    
    The King's College Criteria require assessment of four core parameters plus 
    optional additional prognostic markers:
    
    Core Parameters:
    - Arterial pH: Must be from arterial blood gas (not venous)
    - INR: International Normalized Ratio for coagulation assessment
    - Creatinine: Serum creatinine reflecting kidney function
    - Hepatic Encephalopathy: Neurological grade from clinical assessment
    
    Optional Additional Markers:
    - Lactate: Elevated levels suggest poor tissue perfusion
    - Phosphate: Elevated levels at 48-96 hours indicate poor prognosis
    
    Clinical Context:
    - Used in patients with confirmed acetaminophen-induced liver failure
    - Should be applied after adequate resuscitation and N-acetylcysteine therapy
    - Meeting criteria indicates need for urgent liver transplant evaluation
    - Serial assessment may be more valuable than single timepoint
    
    Limitations:
    - Developed before routine N-acetylcysteine use
    - High specificity but moderate sensitivity
    - PT values may vary between laboratories (INR preferred)
    - Does not account for modern supportive care improvements
    
    References (Vancouver style):
    1. O'Grady JG, Alexander GJ, Hayllar KM, Williams R. Early indicators of prognosis 
       in fulminant hepatic failure. Gastroenterology. 1989 Aug;97(2):439-45.
    2. Bailey B, Amre DK, Gaudreault P. Fulminant hepatic failure secondary to 
       acetaminophen poisoning: a systematic review and meta-analysis of prognostic 
       criteria determining the need for liver transplantation. Crit Care Med. 2003 
       Jan;31(1):299-305.
    """
    
    arterial_ph: float = Field(
        ...,
        description="Arterial pH from arterial blood gas analysis. Must be arterial, "
                   "not venous pH. pH <7.30 alone meets King's College Criteria.",
        ge=6.0,
        le=8.0,
        example=7.25
    )
    
    inr: float = Field(
        ...,
        description="International Normalized Ratio (INR) for coagulation assessment. "
                   "INR >6.5 is one component of the combined criteria. Use INR rather "
                   "than PT when possible due to standardization across laboratories.",
        ge=0.5,
        le=20.0,
        example=4.2
    )
    
    creatinine: float = Field(
        ...,
        description="Serum creatinine in mg/dL. Creatinine >3.4 mg/dL is one component "
                   "of the combined criteria, reflecting kidney dysfunction in acute liver failure.",
        ge=0.1,
        le=25.0,
        example=2.8
    )
    
    hepatic_encephalopathy_grade: Literal["none", "grade_i", "grade_ii", "grade_iii", "grade_iv"] = Field(
        ...,
        description="Grade of hepatic encephalopathy based on clinical assessment. "
                   "Grade III or IV encephalopathy is required for the combined criteria. "
                   "Grade I: mild confusion, euphoria. Grade II: lethargy, inappropriate behavior. "
                   "Grade III: marked confusion, sleeping but rousable. Grade IV: coma.",
        example="grade_ii"
    )
    
    lactate: Optional[float] = Field(
        None,
        description="Serum lactate in mmol/L (optional additional prognostic marker). "
                   "Levels >3.5 mmol/L after early resuscitation or >3.0 mmol/L after "
                   "full resuscitation suggest poor prognosis and may enhance prediction.",
        ge=0.1,
        le=30.0,
        example=4.2
    )
    
    phosphate: Optional[float] = Field(
        None,
        description="Serum phosphate in mg/dL (optional additional prognostic marker). "
                   "Levels >3.75 mg/dL at 48-96 hours after overdose suggest poor prognosis "
                   "and may enhance prediction accuracy.",
        ge=0.5,
        le=15.0,
        example=4.8
    )
    
    class Config:
        schema_extra = {
            "example": {
                "arterial_ph": 7.25,
                "inr": 4.2,
                "creatinine": 2.8,
                "hepatic_encephalopathy_grade": "grade_ii",
                "lactate": 4.2,
                "phosphate": 4.8
            }
        }


class KingsCollegeCriteriaAcetaminophenResponse(BaseModel):
    """
    Response model for King's College Criteria for Acetaminophen Toxicity
    
    Provides comprehensive assessment of transplant criteria with detailed clinical 
    interpretation and management recommendations. The response indicates whether 
    the patient meets criteria for liver transplant evaluation and provides specific 
    guidance for clinical management.
    
    Result Interpretation:
    - Meets Criteria: 95% specificity for poor prognosis, urgent transplant evaluation needed
    - Does Not Meet Criteria: Does not guarantee good outcome due to 58% sensitivity
    
    Clinical Actions Based on Results:
    - Meets Criteria: Immediate liver transplant center referral and evaluation
    - Does Not Meet: Continued intensive monitoring and supportive care
    
    Management Considerations:
    - All patients require continued N-acetylcysteine therapy
    - Serial assessment may be more valuable than single timepoint
    - Consider transplant center consultation even if criteria not met but clinical deterioration
    - Modern supportive care may improve outcomes compared to original studies
    
    Performance Characteristics:
    - Sensitivity: 58% (moderate - may miss some patients who will die)
    - Specificity: 95% (high - rarely wrong when criteria are met)
    - Positive Predictive Value: 70-100% depending on population
    
    Reference: O'Grady JG, et al. Gastroenterology. 1989;97(2):439-45.
    """
    
    result: Dict = Field(
        ...,
        description="Detailed King's College Criteria assessment including individual criteria evaluation",
        example={
            "criteria_met": False,
            "ph_criterion": False,
            "ph_value": 7.25,
            "combined_criterion": False,
            "inr_criterion": False,
            "inr_value": 4.2,
            "creatinine_criterion": False,
            "creatinine_value": 2.8,
            "encephalopathy_criterion": False,
            "encephalopathy_grade": "grade_ii",
            "additional_markers": {
                "high_lactate": True,
                "lactate_value": 4.2,
                "high_phosphate": True,
                "phosphate_value": 4.8
            }
        }
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the criteria assessment",
        example="criteria"
    )
    
    interpretation: str = Field(
        ...,
        description="Comprehensive clinical interpretation including criteria assessment, "
                   "prognosis, and detailed management recommendations for liver transplant "
                   "evaluation and supportive care",
        example="Does not meet King's College Criteria for liver transplantation. However, criteria are specific but not sensitive (58% sensitivity), so close monitoring and continued aggressive medical management are essential. Current values: pH 7.25, INR 4.2, creatinine 2.8 mg/dL, encephalopathy grade ii. Continue N-acetylcysteine, monitor for deterioration, and reassess criteria frequently. Consider early transplant center consultation if clinical deterioration occurs. Additional prognostic markers: Elevated lactate 4.2 mmol/L (>3.5) suggests poor prognosis. Elevated phosphate 4.8 mg/dL (>3.75) at 48-96h suggests poor prognosis."
    )
    
    stage: str = Field(
        ...,
        description="Overall assessment (Meets Criteria, Does Not Meet Criteria)",
        example="Does Not Meet Criteria"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the clinical significance",
        example="Does not meet transplant criteria but requires close monitoring"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": {
                    "criteria_met": False,
                    "ph_criterion": False,
                    "ph_value": 7.25,
                    "combined_criterion": False,
                    "inr_criterion": False,
                    "inr_value": 4.2,
                    "creatinine_criterion": False,
                    "creatinine_value": 2.8,
                    "encephalopathy_criterion": False,
                    "encephalopathy_grade": "grade_ii",
                    "additional_markers": {
                        "high_lactate": True,
                        "lactate_value": 4.2,
                        "high_phosphate": True,
                        "phosphate_value": 4.8
                    }
                },
                "unit": "criteria",
                "interpretation": "Does not meet King's College Criteria for liver transplantation. However, criteria are specific but not sensitive (58% sensitivity), so close monitoring and continued aggressive medical management are essential. Current values: pH 7.25, INR 4.2, creatinine 2.8 mg/dL, encephalopathy grade ii. Continue N-acetylcysteine, monitor for deterioration, and reassess criteria frequently. Consider early transplant center consultation if clinical deterioration occurs. Additional prognostic markers: Elevated lactate 4.2 mmol/L (>3.5) suggests poor prognosis. Elevated phosphate 4.8 mg/dL (>3.75) at 48-96h suggests poor prognosis.",
                "stage": "Does Not Meet Criteria",
                "stage_description": "Does not meet transplant criteria but requires close monitoring"
            }
        }