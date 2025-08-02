"""
Kruis Score for Diagnosis of Irritable Bowel Syndrome (IBS) Models

Request and response models for Kruis Score calculation.

References (Vancouver style):
1. Kruis W, Thieme C, Weinzierl M, Schüssler P, Holl J, Paulus W. A diagnostic score 
   for the irritable bowel syndrome. Its value in the exclusion of organic disease. 
   Gastroenterology. 1984 Jul;87(1):1-7.
2. Frigerio G, Beretta A, Orsenigo G, Tadeo G, Imperiali G, Minoli G. Irritable bowel 
   syndrome. Still a diagnosis of exclusion? Dig Dis Sci. 1992 Jan;37(1):164-7.
3. Bellini M, Tosetti C, Costa F, Biagi S, Stasi C, Del Punta A, et al. The general 
   practitioner's approach to irritable bowel syndrome: from intention to practice. 
   Dig Liver Dis. 2005 Dec;37(12):934-9.
4. Thompson WG. The road to Rome. Gastroenterology. 2006 Nov;131(5):1622-6.

The Kruis Score for Diagnosis of Irritable Bowel Syndrome (IBS) is a clinical 
scoring system developed in 1984 by Kruis et al. to differentiate IBS from organic 
gastrointestinal disease. It was one of the first validated scoring systems for IBS 
diagnosis and introduced the important concept of incorporating both positive symptoms 
and negative "red flag" indicators.

The scoring system uses weighted criteria including:

Positive Symptoms (add points):
- Symptoms of abdominal pain, flatulence, or bowel irregularity (+34 points)
- Symptom duration > 2 years (+16 points)
- Pain described as burning, cutting, very strong (+23 points)
- Alternating constipation and diarrhea (+14 points)

Red Flags (subtract points):
- Abnormal physical findings (-47 points)
- ESR > 10 mm/hr (-13 points)
- WBC > 10,000/μL (-50 points)
- Low hemoglobin (female < 12 g/dL; male < 14 g/dL) (-98 points)
- History of blood in stool (-98 points)

Interpretation:
- Score ≥ 44 points: IBS diagnosis likely (81% sensitivity, 91% specificity)
- Score < 44 points: IBS diagnosis unlikely, consider organic disease

The Kruis Score's main contribution was introducing laboratory parameters and red 
flags into IBS diagnosis, influencing subsequent diagnostic criteria development. 
While largely superseded by Rome criteria in clinical practice, it remains valuable 
for research and provides a systematic approach to IBS diagnosis with objective 
laboratory parameters.
"""

from pydantic import BaseModel, Field
from typing import Literal, Dict


class KruisScoreIbsRequest(BaseModel):
    """
    Request model for Kruis Score for Diagnosis of Irritable Bowel Syndrome (IBS)
    
    The Kruis Score evaluates nine parameters to differentiate IBS from organic 
    gastrointestinal disease using a weighted scoring system that incorporates both 
    positive symptoms and negative red flag indicators:
    
    Positive Symptom Components (add points):
    - Abdominal pain, flatulence, or bowel irregularity: Core IBS symptoms
    - Symptom duration > 2 years: Chronic nature typical of IBS
    - Severe pain descriptors: Quality of pain characteristic of IBS
    - Alternating bowel habits: Classic IBS pattern
    
    Red Flag Components (subtract points):
    - Abnormal physical findings: Suggests organic disease
    - Elevated ESR: Indicates inflammation or systemic disease
    - Elevated WBC: Suggests infection or inflammatory condition
    - Low hemoglobin: May indicate bleeding or chronic disease
    - History of blood in stool: Strong indicator of organic pathology
    
    Clinical Context:
    - Developed in 1984 as one of the first validated IBS diagnostic tools
    - Score ≥44 points suggests IBS with 81% sensitivity and 91% specificity
    - Red flags require exclusion of organic disease regardless of total score
    - Incorporates laboratory parameters unlike purely symptom-based criteria
    
    Diagnostic Approach:
    - Any red flag present warrants investigation for organic disease
    - Laboratory tests (CBC, ESR) are integral to the assessment
    - Emphasizes symptom duration and quality in diagnosis
    - Provides objective scoring system for clinical decision-making
    
    Clinical Limitations:
    - Developed before modern understanding of IBS pathophysiology
    - Has been largely superseded by Rome criteria in clinical practice
    - May be too restrictive for some IBS presentations
    - Requires laboratory testing that may not always be available
    
    References (Vancouver style):
    1. Kruis W, Thieme C, Weinzierl M, Schüssler P, Holl J, Paulus W. A diagnostic score 
       for the irritable bowel syndrome. Its value in the exclusion of organic disease. 
       Gastroenterology. 1984 Jul;87(1):1-7.
    2. Frigerio G, Beretta A, Orsenigo G, Tadeo G, Imperiali G, Minoli G. Irritable bowel 
       syndrome. Still a diagnosis of exclusion? Dig Dis Sci. 1992 Jan;37(1):164-7.
    """
    
    symptoms_present: Literal["yes", "no"] = Field(
        ...,
        description="Presence of symptoms of abdominal pain, flatulence, or bowel irregularity. "
                   "These are the core symptoms of IBS and contribute +34 points to the score. "
                   "Abdominal pain is typically cramping and related to bowel movements. "
                   "Flatulence includes bloating, gas, and abdominal distension. "
                   "Bowel irregularity includes changes in frequency, consistency, or form.",
        example="yes"
    )
    
    duration_over_2_years: Literal["yes", "no"] = Field(
        ...,
        description="Symptom duration greater than 2 years. The Kruis criteria emphasize "
                   "chronic symptom duration as a key feature of IBS, contributing +16 points. "
                   "This distinguishes IBS from acute gastrointestinal conditions and supports "
                   "the chronic, functional nature of the disorder.",
        example="yes"
    )
    
    pain_description: Literal["yes", "no"] = Field(
        ...,
        description="Pain described as burning, cutting, very strong, or similar severe descriptors. "
                   "This qualitative assessment of pain intensity and character contributes +23 points. "
                   "IBS pain is often described with emotionally charged terms and may be "
                   "disproportionate to physical findings.",
        example="no"
    )
    
    alternating_bowel_habits: Literal["yes", "no"] = Field(
        ...,
        description="Alternating constipation and diarrhea pattern. This classic IBS symptom "
                   "contributes +14 points and represents the mixed bowel habit subtype of IBS. "
                   "Patients experience periods of both constipation and diarrhea, often with "
                   "unpredictable patterns.",
        example="yes"
    )
    
    abnormal_physical_findings: Literal["yes", "no"] = Field(
        ...,
        description="Abnormal physical findings on examination (RED FLAG). This contributes "
                   "-47 points as it suggests organic disease rather than functional IBS. "
                   "Examples include abdominal masses, organomegaly, lymphadenopathy, or "
                   "signs of inflammation. IBS typically has normal physical examination.",
        example="no"
    )
    
    esr_over_10: Literal["yes", "no"] = Field(
        ...,
        description="Erythrocyte sedimentation rate (ESR) greater than 10 mm/hr (RED FLAG). "
                   "This contributes -13 points as elevated ESR suggests inflammatory or "
                   "systemic disease rather than functional IBS. Normal ESR is expected in "
                   "IBS patients and helps differentiate from inflammatory bowel disease.",
        example="no"
    )
    
    wbc_over_10000: Literal["yes", "no"] = Field(
        ...,
        description="White blood cell count greater than 10,000/μL (RED FLAG). This contributes "
                   "-50 points as leukocytosis suggests infection, inflammation, or other organic "
                   "pathology. Normal WBC count is expected in IBS and helps exclude conditions "
                   "like inflammatory bowel disease or infectious colitis.",
        example="no"
    )
    
    low_hemoglobin: Literal["yes", "no"] = Field(
        ...,
        description="Low hemoglobin indicating anemia (female < 12 g/dL; male < 14 g/dL) "
                   "(RED FLAG). This contributes -98 points as anemia suggests bleeding, "
                   "malabsorption, or chronic disease rather than functional IBS. Anemia "
                   "warrants investigation for colorectal cancer, inflammatory bowel disease, "
                   "or other organic conditions.",
        example="no"
    )
    
    history_blood_in_stool: Literal["yes", "no"] = Field(
        ...,
        description="History of blood in stool (RED FLAG). This contributes -98 points as "
                   "rectal bleeding is not a feature of IBS and suggests organic pathology. "
                   "Any history of blood in stool requires investigation for colorectal cancer, "
                   "inflammatory bowel disease, or other structural abnormalities.",
        example="no"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "symptoms_present": "yes",
                "duration_over_2_years": "yes",
                "pain_description": "no",
                "alternating_bowel_habits": "yes",
                "abnormal_physical_findings": "no",
                "esr_over_10": "no",
                "wbc_over_10000": "no",
                "low_hemoglobin": "no",
                "history_blood_in_stool": "no"
            }
        }


class KruisScoreIbsResponse(BaseModel):
    """
    Response model for Kruis Score for Diagnosis of Irritable Bowel Syndrome (IBS)
    
    Provides comprehensive IBS diagnostic assessment based on the Kruis scoring system 
    with detailed breakdown of symptom scores, red flag evaluation, and clinical 
    interpretation. The response indicates whether the patient meets criteria for IBS 
    diagnosis and provides specific guidance for clinical management.
    
    Score Interpretation:
    - Score ≥ 44 points: IBS diagnosis likely (81% sensitivity, 91% specificity)
    - Score < 44 points: IBS diagnosis unlikely, consider organic disease evaluation
    
    Clinical Actions Based on Results:
    - Positive Score without Red Flags: IBS diagnosis can be made confidently
    - Positive Score with Red Flags: Exclude organic disease before IBS diagnosis
    - Negative Score: Investigate for organic gastrointestinal conditions
    - Any Red Flags Present: Mandatory evaluation for organic pathology
    
    Management Considerations:
    - IBS diagnosis requires exclusion of red flags regardless of symptom score
    - Laboratory parameters are integral to the assessment
    - Chronic symptom duration (>2 years) supports IBS diagnosis
    - Normal physical examination and laboratory values are expected in IBS
    
    Performance Characteristics:
    - Sensitivity: 81% (good detection of IBS cases)
    - Specificity: 91% (excellent exclusion of non-IBS cases)
    - Positive Predictive Value: Variable depending on population prevalence
    - Historical significance: First validated IBS scoring system
    
    Clinical Context:
    - Originally designed to differentiate IBS from organic bowel disease
    - Incorporated laboratory testing before this became standard practice
    - Influenced development of subsequent IBS diagnostic criteria
    - Remains useful for research and systematic approach to IBS diagnosis
    
    Reference: Kruis W, et al. Gastroenterology. 1984;87(1):1-7.
    """
    
    result: Dict = Field(
        ...,
        description="Detailed Kruis Score calculation including total score, component scores, and red flag assessment",
        example={
            "total_score": 64,
            "symptom_score": 64,
            "red_flag_score": 0,
            "individual_scores": {
                "symptoms_present": 34,
                "duration_over_2_years": 16,
                "pain_description": 0,
                "alternating_bowel_habits": 14,
                "abnormal_physical_findings": 0,
                "esr_over_10": 0,
                "wbc_over_10000": 0,
                "low_hemoglobin": 0,
                "history_blood_in_stool": 0
            },
            "red_flags_present": [],
            "diagnostic_threshold": 44,
            "meets_threshold": True
        }
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Comprehensive clinical interpretation including score assessment, "
                   "red flag evaluation, and detailed management recommendations for IBS "
                   "diagnosis and organic disease exclusion",
        example="Score of 64 points indicates IBS diagnosis is likely. Patient meets Kruis criteria threshold (≥44 points) for irritable bowel syndrome. No red flags identified, which supports the diagnostic assessment. With positive Kruis criteria and absence of red flags, IBS diagnosis can be made with confidence (81% sensitivity, 91% specificity). Consider initiating IBS management including dietary modifications, symptom-targeted therapies, and patient education. Note: The Kruis Score (1984) was one of the first validated IBS diagnostic tools but has largely been superseded by Rome criteria in clinical practice."
    )
    
    stage: str = Field(
        ...,
        description="Overall diagnostic assessment (Positive for IBS, Negative for IBS)",
        example="Positive for IBS"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the score result and diagnostic threshold",
        example="Score ≥ 44 points"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": {
                    "total_score": 64,
                    "symptom_score": 64,
                    "red_flag_score": 0,
                    "individual_scores": {
                        "symptoms_present": 34,
                        "duration_over_2_years": 16,
                        "pain_description": 0,
                        "alternating_bowel_habits": 14,
                        "abnormal_physical_findings": 0,
                        "esr_over_10": 0,
                        "wbc_over_10000": 0,
                        "low_hemoglobin": 0,
                        "history_blood_in_stool": 0
                    },
                    "red_flags_present": [],
                    "diagnostic_threshold": 44,
                    "meets_threshold": True
                },
                "unit": "points",
                "interpretation": "Score of 64 points indicates IBS diagnosis is likely. Patient meets Kruis criteria threshold (≥44 points) for irritable bowel syndrome. No red flags identified, which supports the diagnostic assessment. With positive Kruis criteria and absence of red flags, IBS diagnosis can be made with confidence (81% sensitivity, 91% specificity). Consider initiating IBS management including dietary modifications, symptom-targeted therapies, and patient education. Note: The Kruis Score (1984) was one of the first validated IBS diagnostic tools but has largely been superseded by Rome criteria in clinical practice.",
                "stage": "Positive for IBS",
                "stage_description": "Score ≥ 44 points"
            }
        }