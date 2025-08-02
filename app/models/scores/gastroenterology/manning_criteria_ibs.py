"""
Manning Criteria for Diagnosis of Irritable Bowel Syndrome (IBS) Models

Request and response models for Manning Criteria IBS diagnosis calculation.

References (Vancouver style):
1. Manning AP, Thompson WG, Heaton KW, Morris AF. Towards positive diagnosis of the 
   irritable bowel. Br Med J. 1978 Sep 2;2(6138):653-4. doi: 10.1136/bmj.2.6138.653.
2. Thompson WG, Heaton KW, Smyth GT, Smyth C. Irritable bowel syndrome in general 
   practice: prevalence, characteristics, and referral. Gut. 2000 Jan;46(1):78-82. 
   doi: 10.1136/gut.46.1.78.
3. Drossman DA, Chang L, Bellamy N, Gallo-Torres HE, Lembo A, Mearin F, et al. Severity 
   in irritable bowel syndrome: a Rome Foundation Working Team report. Am J Gastroenterol. 
   2011 Oct;106(10):1749-59. doi: 10.1038/ajg.2011.201.

The Manning Criteria for IBS diagnosis was developed in 1978 by Manning et al. from a study 
of 109 patients with abdominal symptoms. It uses six clinical criteria related to abdominal 
pain and stool characteristics to determine likelihood of IBS diagnosis. The criteria requires 
at least 3 of 6 symptoms to suggest IBS, but red flag symptoms (age >50, weight loss, blood 
in stools, anemia, fever) must be absent. While historically important, Rome IV criteria are 
now more commonly used for IBS diagnosis.
"""

from pydantic import BaseModel, Field
from typing import Literal, Dict, Any


class ManningCriteriaIbsRequest(BaseModel):
    """
    Request model for Manning Criteria for Diagnosis of Irritable Bowel Syndrome (IBS)
    
    The Manning Criteria evaluates six clinical symptoms to assess IBS likelihood:
    
    Six Manning Criteria (1 point each):
    1. Onset of pain linked to more frequent bowel movements
    2. Looser stools associated with onset of pain
    3. Pain relieved by passage of stool
    4. Noticeable abdominal bloating/distension
    5. Sensation of incomplete evacuation >25% of time
    6. Diarrhea with mucus >25% of time
    
    Diagnostic Threshold:
    - ≥3 criteria met: Suggests IBS diagnosis
    - <3 criteria met: IBS unlikely
    
    Red Flag Exclusions (any present invalidates diagnosis):
    - Age >50 years
    - Unexplained weight loss
    - Blood in stools (hematochezia/melena)
    - Anemia on laboratory testing
    - Fever with GI symptoms
    
    Clinical Performance:
    - Sensitivity: 63-90%
    - Specificity: 70-93%
    - More specific but less sensitive than Rome criteria
    
    Clinical Applications:
    - Primary care IBS screening
    - Gastroenterology consultation support
    - Functional bowel disorder assessment
    - Research and clinical trial enrollment
    - Quality assurance in GI practice
    
    Important Limitations:
    - Requires exclusion of organic GI disease
    - Red flag symptoms mandate further investigation
    - Should complement clinical judgment, not replace it
    - Rome IV criteria provide more current standards
    - Consider IBD, celiac disease, gastroparesis in differential
    
    References (Vancouver style):
    1. Manning AP, Thompson WG, Heaton KW, Morris AF. Towards positive diagnosis of the 
       irritable bowel. Br Med J. 1978 Sep 2;2(6138):653-4. doi: 10.1136/bmj.2.6138.653.
    2. Thompson WG, Heaton KW, Smyth GT, Smyth C. Irritable bowel syndrome in general 
       practice: prevalence, characteristics, and referral. Gut. 2000 Jan;46(1):78-82. 
       doi: 10.1136/gut.46.1.78.
    """
    
    pain_onset_frequent_bowel_movements: Literal["yes", "no"] = Field(
        ...,
        description="Onset of abdominal pain linked to more frequent bowel movements. This association suggests functional bowel disorder rather than structural pathology",
        example="yes"
    )
    
    looser_stools_with_pain_onset: Literal["yes", "no"] = Field(
        ...,
        description="Looser stools associated with onset of abdominal pain. Change in stool consistency concurrent with pain onset is characteristic of IBS",
        example="yes"
    )
    
    pain_relief_with_defecation: Literal["yes", "no"] = Field(
        ...,
        description="Abdominal pain relieved by passage of stool. Pain relief with bowel movement is a hallmark feature of IBS distinguishing it from other causes of abdominal pain",
        example="yes"
    )
    
    noticeable_abdominal_bloating: Literal["yes", "no"] = Field(
        ...,
        description="Visible abdominal distension or bloating. Subjective or objective abdominal distension is common in functional bowel disorders",
        example="no"
    )
    
    incomplete_evacuation_sensation: Literal["yes", "no"] = Field(
        ...,
        description="Sensation of incomplete evacuation more than 25% of the time. Feeling that bowel movement is incomplete despite attempting defecation",
        example="no"
    )
    
    diarrhea_with_mucus: Literal["yes", "no"] = Field(
        ...,
        description="Diarrhea with mucus more than 25% of the time. Passage of mucus with loose stools suggests colonic irritation characteristic of IBS",
        example="no"
    )
    
    patient_age: int = Field(
        ...,
        ge=10,
        le=100,
        description="Patient age in years. Age >50 years is a red flag requiring exclusion of organic disease before IBS diagnosis",
        example=35
    )
    
    weight_loss: Literal["yes", "no"] = Field(
        ...,
        description="Presence of unexplained weight loss. Weight loss is a red flag symptom that suggests organic disease rather than functional bowel disorder",
        example="no"
    )
    
    blood_in_stools: Literal["yes", "no"] = Field(
        ...,
        description="Presence of blood in stools (hematochezia or melena). Blood in stools is a red flag requiring investigation for organic pathology",
        example="no"
    )
    
    anemia: Literal["yes", "no"] = Field(
        ...,
        description="Presence of anemia on laboratory testing. Anemia may indicate gastrointestinal bleeding or malabsorption requiring further evaluation",
        example="no"
    )
    
    fever: Literal["yes", "no"] = Field(
        ...,
        description="Presence of fever with gastrointestinal symptoms. Fever suggests inflammatory or infectious process rather than functional disorder",
        example="no"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "pain_onset_frequent_bowel_movements": "yes",
                "looser_stools_with_pain_onset": "yes",
                "pain_relief_with_defecation": "yes",
                "noticeable_abdominal_bloating": "no",
                "incomplete_evacuation_sensation": "no",
                "diarrhea_with_mucus": "no",
                "patient_age": 35,
                "weight_loss": "no",
                "blood_in_stools": "no",
                "anemia": "no",
                "fever": "no"
            }
        }


class ManningCriteriaIbsResponse(BaseModel):
    """
    Response model for Manning Criteria for Diagnosis of Irritable Bowel Syndrome (IBS)
    
    The Manning Criteria provides diagnostic guidance for IBS based on symptom patterns:
    
    IBS Unlikely (<3 criteria):
    - Insufficient symptom pattern for IBS diagnosis
    - Consider alternative diagnoses (IBD, celiac, gastroparesis)
    - Further evaluation may be warranted
    - Rome IV criteria may provide additional guidance
    
    IBS Likely (≥3 criteria, no red flags):
    - Symptom pattern supports IBS diagnosis
    - Consider symptomatic treatment and lifestyle modifications
    - Low FODMAP diet, antispasmodics, probiotics may help
    - Patient education about chronic nature important
    
    Further Evaluation Required (≥3 criteria, red flags present):
    - Sufficient criteria but concerning features present
    - Must exclude organic disease before IBS diagnosis
    - Consider CBC, inflammatory markers, celiac serology
    - Colonoscopy or imaging may be indicated
    
    The Manning Criteria serves as a clinical decision support tool but should be used in 
    conjunction with clinical judgment and appropriate investigations. Modern practice often 
    favors Rome IV criteria for IBS diagnosis, but Manning criteria remains useful for initial 
    screening and assessment.
    
    Reference: Manning AP, et al. Br Med J. 1978;2(6138):653-4.
    """
    
    result: Dict[str, Any] = Field(
        ...,
        description="Manning Criteria assessment results including criteria scores, red flag analysis, and detailed diagnostic guidance",
        example={
            "total_criteria": 3,
            "criteria_scores": {
                "pain_onset_frequent_bm": 1,
                "looser_stools_with_pain": 1,
                "pain_relief_defecation": 1,
                "abdominal_bloating": 0,
                "incomplete_evacuation": 0,
                "diarrhea_with_mucus": 0
            },
            "red_flags": {
                "age_over_50": False,
                "weight_loss": False,
                "blood_in_stools": False,
                "anemia": False,
                "fever": False
            },
            "has_red_flags": False,
            "assessment_data": {
                "diagnostic_likelihood": "IBS diagnosis supported",
                "recommendation": "Consider IBS treatment and management",
                "criteria_threshold": "≥3 criteria needed",
                "present_red_flags": "None",
                "sensitivity_range": "63-90%",
                "specificity_range": "70-93%",
                "next_steps": "Consider Rome IV criteria and appropriate investigations"
            }
        }
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="criteria"
    )
    
    interpretation: str = Field(
        ...,
        description="Comprehensive clinical interpretation with diagnostic likelihood, red flag assessment, and management recommendations",
        example="3 of 6 Manning criteria met with no red flag symptoms present. This supports a diagnosis of irritable bowel syndrome. Consider initiating symptomatic treatment including dietary modifications."
    )
    
    stage: str = Field(
        ...,
        description="Diagnostic category (IBS Unlikely, IBS Likely, Further Evaluation Required)",
        example="IBS Likely"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the diagnostic category and implications",
        example="Sufficient criteria for IBS diagnosis with no red flags"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": {
                    "total_criteria": 3,
                    "criteria_scores": {
                        "pain_onset_frequent_bm": 1,
                        "looser_stools_with_pain": 1,
                        "pain_relief_defecation": 1,
                        "abdominal_bloating": 0,
                        "incomplete_evacuation": 0,
                        "diarrhea_with_mucus": 0
                    },
                    "red_flags": {
                        "age_over_50": False,
                        "weight_loss": False,
                        "blood_in_stools": False,
                        "anemia": False,
                        "fever": False
                    },
                    "has_red_flags": False,
                    "assessment_data": {
                        "diagnostic_likelihood": "IBS diagnosis supported",
                        "recommendation": "Consider IBS treatment and management",
                        "criteria_threshold": "≥3 criteria needed",
                        "present_red_flags": "None",
                        "sensitivity_range": "63-90%",
                        "specificity_range": "70-93%",
                        "next_steps": "Consider Rome IV criteria and appropriate investigations"
                    }
                },
                "unit": "criteria",
                "interpretation": "3 of 6 Manning criteria met with no red flag symptoms present. This supports a diagnosis of irritable bowel syndrome. Consider initiating symptomatic treatment including dietary modifications.",
                "stage": "IBS Likely",
                "stage_description": "Sufficient criteria for IBS diagnosis with no red flags"
            }
        }