"""
Immune-Related Adverse Events for Endocrine Toxicities - Diabetes Mellitus Models

Request and response models for immune-related adverse events endocrine diabetes mellitus grading.

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

The immune-related adverse events (irAE) grading system for endocrine toxicities 
specifically addresses diabetes mellitus induced by immune checkpoint inhibitors (ICPi). 
This grading system is based on Common Terminology Criteria for Adverse Events (CTCAE) 
Version 5.0 and provides standardized criteria for assessing hyperglycemia severity 
and guiding clinical management decisions. Immune checkpoint inhibitor-induced diabetes 
mellitus often presents as fulminant Type 1 diabetes with diabetic ketoacidosis (DKA) 
in 67.4% of cases, requiring immediate recognition and appropriate management.
"""

from pydantic import BaseModel, Field
from typing import Literal


class ImmuneRelatedAdverseEventsEndocrineDiabetesRequest(BaseModel):
    """
    Request model for Immune-Related Adverse Events for Endocrine Toxicities - Diabetes Mellitus
    
    This grading system evaluates hyperglycemia severity in patients receiving immune 
    checkpoint inhibitor therapy based on three key clinical parameters:
    
    Grading Criteria:
    - Grade 1: Fasting glucose >160 mg/dL (>8.9 mmol/L), no ketosis/T1DM, asymptomatic/mild symptoms
    - Grade 2: Glucose 160-250 mg/dL (8.9-13.9 mmol/L) OR ketosis/T1DM at any level, moderate symptoms
    - Grade 3: Glucose 250-500 mg/dL (13.9-27.8 mmol/L), severe symptoms, unable to perform ADLs
    - Grade 4: Glucose >500 mg/dL (>27.8 mmol/L), life-threatening symptoms, unable to perform ADLs
    
    Clinical Context:
    - ICPi-induced diabetes mellitus often presents as fulminant Type 1 diabetes
    - 67.4% of cases present with diabetic ketoacidosis (DKA)
    - Low C-peptide levels in 91.8% indicating acute onset insulin deficiency
    - Ketosis or T1DM evidence at any glucose level warrants at least Grade 2 classification
    - Urgent endocrine consultation required for Grade 2+ toxicity
    
    Management Principles:
    - Grade 1: Continue ICPi, close monitoring, consider oral medications
    - Grade 2: May hold ICPi, urgent endocrine consultation, consider insulin
    - Grade 3-4: Hold ICPi, urgent consultation, initiate insulin, hospital admission if DKA
    
    Monitoring Parameters:
    - HbA1c, fasting C-peptide, GADA autoantibodies
    - Distinguish from pre-existing diabetes or steroid-induced hyperglycemia
    - Consider continuous glucose monitoring for severe cases
    
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
    
    fasting_glucose_mg_dl: float = Field(
        ...,
        description="Fasting glucose level in mg/dL. Key parameter for grading hyperglycemia severity. Normal <100 mg/dL, prediabetes 100-125 mg/dL, diabetes ≥126 mg/dL. Grade 1: >160, Grade 2: 160-250, Grade 3: 250-500, Grade 4: >500 mg/dL",
        example=280.5,
        ge=70.0,
        le=1000.0
    )
    
    ketosis_or_t1dm_evidence: Literal["yes", "no"] = Field(
        ...,
        description="Evidence of ketosis or Type 1 Diabetes Mellitus at any glucose level. Includes: positive urine/serum ketones, metabolic acidosis (pH <7.3), low C-peptide (<0.6 ng/mL), positive GADA/IA-2 antibodies, or clinical presentation consistent with T1DM. If present, automatically warrants at least Grade 2 classification regardless of glucose level",
        example="yes"
    )
    
    symptom_severity: Literal["asymptomatic_mild", "moderate_able_adls", "severe_unable_adls"] = Field(
        ...,
        description="Patient symptom severity and functional status assessment. Asymptomatic/mild: no or minimal symptoms, normal daily activities. Moderate (able ADLs): noticeable symptoms (polydipsia, polyuria, fatigue) but can still perform activities of daily living. Severe (unable ADLs): significant symptoms preventing normal activities, may include nausea, vomiting, altered mental status, signs of dehydration",
        example="severe_unable_adls"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "fasting_glucose_mg_dl": 280.5,
                "ketosis_or_t1dm_evidence": "yes",
                "symptom_severity": "severe_unable_adls"
            }
        }


class ImmuneRelatedAdverseEventsEndocrineDiabetesResponse(BaseModel):
    """
    Response model for Immune-Related Adverse Events for Endocrine Toxicities - Diabetes Mellitus
    
    The irAE grading system provides standardized assessment of hyperglycemia severity 
    and evidence-based management recommendations for immune checkpoint inhibitor-induced 
    diabetes mellitus:
    
    Grade 1 (Mild): Continue ICPi with close monitoring
    Grade 2 (Moderate): May hold ICPi, urgent endocrine consultation
    Grade 3-4 (Severe/Life-threatening): Hold ICPi, insulin therapy, hospitalization
    
    Clinical Implications:
    - Grade 2+ requires urgent endocrine consultation and potential ICPi interruption
    - ICPi therapy can often be resumed after glucose control (Grade 1-2)
    - Grade 3-4 may require permanent discontinuation
    - Multidisciplinary approach recommended (oncology, endocrinology, pharmacy)
    
    Reference: Brahmer JR, et al. J Clin Oncol. 2018;36(17):1714-1768.
    """
    
    result: int = Field(
        ...,
        description="irAE grade for endocrine diabetes mellitus based on CTCAE v5.0 criteria (range: 1-4)",
        example=3,
        ge=1,
        le=4
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the grading system",
        example="grade"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation with detailed management recommendations including ICPi therapy decisions, monitoring requirements, treatment interventions, and consultation needs",
        example="Hold ICPi until toxicity recovers to grade ≤1. Urgent endocrine consultation required. Initiate insulin therapy. Admit if concern for diabetic ketoacidosis or symptomatic. Fasting glucose 250-500 mg/dL (13.9-27.8 mmol/L) with severe symptoms."
    )
    
    stage: str = Field(
        ...,
        description="irAE grade classification with severity descriptor",
        example="Grade 3"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the grade severity and clinical presentation",
        example="Severe - Severe symptoms, unable to perform ADLs"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 3,
                "unit": "grade",
                "interpretation": "Hold ICPi until toxicity recovers to grade ≤1. Urgent endocrine consultation required. Initiate insulin therapy. Admit if concern for diabetic ketoacidosis or symptomatic. Fasting glucose 250-500 mg/dL (13.9-27.8 mmol/L) with severe symptoms.",
                "stage": "Grade 3",
                "stage_description": "Severe - Severe symptoms, unable to perform ADLs"
            }
        }