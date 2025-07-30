"""
Burch-Wartofsky Point Scale (BWPS) for Thyrotoxicosis Models

Request and response models for BWPS calculation.

References (Vancouver style):
1. Burch HB, Wartofsky L. Life-threatening thyrotoxicosis. Thyroid storm. 
   Endocrinology and Metabolism Clinics of North America. 1993;22(2):263-277.
2. Akamizu T, Satoh T, Isozaki O, et al. Diagnostic criteria, clinical features, 
   and incidence of thyroid storm based on nationwide surveys. Thyroid. 
   2012;22(7):661-679.
3. Chiha M, Samarasinghe S, Kabaker AS. Thyroid storm: an updated review. 
   J Intensive Care Med. 2015;30(3):131-140.
4. Ross DS, Burch HB, Cooper DS, et al. 2016 American Thyroid Association 
   guidelines for diagnosis and management of hyperthyroidism and other causes 
   of thyrotoxicosis. Thyroid. 2016;26(10):1343-1421.

The Burch-Wartofsky Point Scale (BWPS) is an empirically derived scoring system 
that predicts the likelihood that biochemical thyrotoxicosis is thyroid storm. 
The scale evaluates multiple organ decompensation including:

- Thermoregulatory dysfunction (fever)
- Cardiovascular symptoms (tachycardia, atrial fibrillation, heart failure)
- Central nervous system effects (agitation, delirium, coma)
- Gastrointestinal-hepatic dysfunction (nausea, vomiting, jaundice)
- Precipitating factors

Score interpretation:
- <25 points: Thyroid storm unlikely
- 25-44 points: Impending thyroid storm (high suspicion)
- ≥45 points: Thyroid storm highly suggestive (life-threatening emergency)

This scale has a positive predictive value of 75% and negative predictive value 
of 100%, making it a valuable diagnostic tool for this endocrine emergency.
"""

from pydantic import BaseModel, Field
from typing import Literal, Dict, List, Any


class BurchWartofskypointScaleRequest(BaseModel):
    """
    Request model for Burch-Wartofsky Point Scale (BWPS) for Thyrotoxicosis
    
    The BWPS evaluates seven clinical parameters to assess thyroid storm likelihood:
    
    Temperature (5-30 points):
    - 99-100°F: 5 points
    - 100-101°F: 10 points  
    - 101-102°F: 15 points
    - 102-103°F: 20 points
    - 103-104°F: 25 points
    - >104°F: 30 points
    
    CNS Effects (0-30 points):
    - Absent: 0 points
    - Mild agitation: 10 points
    - Moderate (delirium, psychosis, extreme lethargy): 20 points
    - Severe (coma, seizure): 30 points
    
    GI-Hepatic Dysfunction (0-20 points):
    - Absent: 0 points
    - Moderate (diarrhea, nausea, vomiting, abdominal pain): 10 points
    - Severe (unexplained jaundice): 20 points
    
    Cardiovascular Dysfunction (0-15 points):
    - Absent: 0 points
    - Moderate (CHF, pedal edema, pulmonary edema): 5 points
    - Severe (pulmonary edema): 15 points
    
    Tachycardia (5-25 points):
    - 90-109 bpm: 5 points
    - 110-119 bpm: 10 points
    - 120-129 bpm: 15 points
    - 130-139 bpm: 20 points
    - >140 bpm: 25 points
    
    Atrial Fibrillation (0-10 points):
    - Absent: 0 points
    - Present: 10 points
    
    Precipitant History (0-10 points):
    - Absent: 0 points
    - Present: 10 points (infection, surgery, trauma, iodine, medication noncompliance)
    
    References (Vancouver style):
    1. Burch HB, Wartofsky L. Life-threatening thyrotoxicosis. Thyroid storm. 
    Endocrinology and Metabolism Clinics of North America. 1993;22(2):263-277.
    2. Akamizu T, Satoh T, Isozaki O, et al. Diagnostic criteria, clinical features, 
    and incidence of thyroid storm based on nationwide surveys. Thyroid. 
    2012;22(7):661-679.
    3. Chiha M, Samarasinghe S, Kabaker AS. Thyroid storm: an updated review. 
    J Intensive Care Med. 2015;30(3):131-140.
    4. Ross DS, Burch HB, Cooper DS, et al. 2016 American Thyroid Association 
    guidelines for diagnosis and management of hyperthyroidism and other causes 
    of thyrotoxicosis. Thyroid. 2016;26(10):1343-1421.
    """
    
    temperature: Literal["99_100", "100_101", "101_102", "102_103", "103_104", "over_104"] = Field(
        ...,
        description="Body temperature range in Fahrenheit. Higher temperatures score more points, with >104°F scoring maximum 30 points.",
        example="101_102"
    )
    
    cns_effects: Literal["absent", "mild_agitation", "moderate_delirium_psychosis_extreme_lethargy", "severe_coma_seizure"] = Field(
        ...,
        description="Central nervous system effects. Ranges from absent (0 points) to severe manifestations like coma or seizure (30 points).",
        example="mild_agitation"
    )
    
    gi_hepatic_dysfunction: Literal["absent", "moderate_diarrhea_nausea_vomiting_abdominal_pain", "severe_unexplained_jaundice"] = Field(
        ...,
        description="Gastrointestinal-hepatic dysfunction severity. Severe manifestations like unexplained jaundice score higher (20 points).",
        example="moderate_diarrhea_nausea_vomiting_abdominal_pain"
    )
    
    cardiovascular_dysfunction: Literal["absent", "moderate_chf_pedal_edema_pulmonary_edema", "severe_pulmonary_edema"] = Field(
        ...,
        description="Cardiovascular dysfunction severity. Ranges from absent to severe pulmonary edema (15 points maximum).",
        example="absent"
    )
    
    tachycardia: Literal["90_109", "110_119", "120_129", "130_139", "over_140"] = Field(
        ...,
        description="Heart rate in beats per minute. Higher heart rates correlate with more severe thyrotoxicosis and score more points.",
        example="120_129"
    )
    
    atrial_fibrillation: Literal["absent", "present"] = Field(
        ...,
        description="Presence of atrial fibrillation. A common complication of severe thyrotoxicosis that adds 10 points if present.",
        example="absent"
    )
    
    precipitant_history: Literal["absent", "present"] = Field(
        ...,
        description="History of precipitating event such as infection, surgery, trauma, iodine administration, or medication noncompliance. Adds 10 points if present.",
        example="present"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "temperature": "101_102",
                "cns_effects": "mild_agitation",
                "gi_hepatic_dysfunction": "moderate_diarrhea_nausea_vomiting_abdominal_pain",
                "cardiovascular_dysfunction": "absent",
                "tachycardia": "120_129",
                "atrial_fibrillation": "absent",
                "precipitant_history": "present"
            }
        }


class BurchWartofskypointScaleResponse(BaseModel):
    """
    Response model for Burch-Wartofsky Point Scale (BWPS) for Thyrotoxicosis
    
    The BWPS provides critical risk stratification for thyroid storm:
    
    Score Interpretation:
    - <25 points: Thyroid storm unlikely - Continue monitoring but diagnosis 
      not supported by current findings
    - 25-44 points: Impending thyroid storm - High clinical suspicion, consider 
      immediate treatment and close monitoring
    - ≥45 points: Thyroid storm highly suggestive - Life-threatening emergency 
      requiring immediate aggressive treatment
    
    Clinical Significance:
    - Thyroid storm has 10-30% mortality rate if untreated
    - Treatment should not be delayed for laboratory confirmation
    - The scale has 75% positive predictive value and 100% negative predictive value
    - Helps guide urgency of treatment and level of care needed
    
    Emergency Treatment (for scores ≥45):
    - Antithyroid drugs (methimazole or propylthiouracil)
    - Beta-blockers (propranolol preferred)
    - Iodine therapy
    - Corticosteroids
    - Aggressive supportive care
    
    Reference: Burch HB, Wartofsky L. Endocrinology and Metabolism Clinics of 
    North America. 1993;22(2):263-277.
    """
    
    result: int = Field(
        ...,
        description="Total BWPS score (range: 5-140 points, practical range typically 5-100)",
        example=45
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation and urgency assessment based on the score",
        example="Score ≥45 is highly suggestive of thyroid storm. This is a life-threatening endocrine emergency requiring immediate aggressive treatment including antithyroid drugs, beta-blockers, iodine, corticosteroids, and supportive care."
    )
    
    stage: str = Field(
        ...,
        description="Risk category (Unlikely_TS, Impending_TS, Highly_Suggestive_TS)",
        example="Highly_Suggestive_TS"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the risk category",
        example="Thyroid storm highly suggestive"
    )
    
    clinical_recommendations: Dict[str, List[str]] = Field(
        ...,
        description="Categorized clinical recommendations based on the score",
        example={
            "immediate_actions": [
                "Initiate immediate thyroid storm treatment protocol",
                "Transfer to ICU or high-dependency unit",
                "Multidisciplinary team approach (endocrinology, ICU, pharmacy)"
            ],
            "medications": [
                "Antithyroid drugs: methimazole 20-30mg q8h OR propylthiouracil 300-400mg q6h",
                "Beta-blocker: propranolol 1-2mg IV q5min or 40-80mg PO q6h",
                "Iodine: SSKI 5 drops PO q6h or sodium iodide 1-2g IV daily",
                "Corticosteroids: hydrocortisone 300mg IV then 100mg q8h"
            ],
            "supportive_care": [
                "Aggressive cooling measures for hyperthermia",
                "IV fluid resuscitation for dehydration",
                "Electrolyte monitoring and correction",
                "Nutritional support"
            ]
        }
    )
    
    score_breakdown: Dict[str, Dict[str, Any]] = Field(
        ...,
        description="Detailed breakdown of points awarded for each component",
        example={
            "temperature": {
                "category": "101-102°F",
                "points": 15,
                "max_points": 30
            },
            "cns_effects": {
                "category": "Mild agitation",
                "points": 10,
                "max_points": 30
            },
            "gi_hepatic_dysfunction": {
                "category": "Moderate (diarrhea, nausea, vomiting, abdominal pain)",
                "points": 10,
                "max_points": 20
            },
            "cardiovascular_dysfunction": {
                "category": "Absent",
                "points": 0,
                "max_points": 15
            },
            "tachycardia": {
                "category": "120-129 bpm",
                "points": 15,
                "max_points": 25
            },
            "atrial_fibrillation": {
                "category": "Absent",
                "points": 0,
                "max_points": 10
            },
            "precipitant_history": {
                "category": "Present",
                "points": 10,
                "max_points": 10
            }
        }
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 60,
                "unit": "points",
                "interpretation": "Score ≥45 is highly suggestive of thyroid storm. This is a life-threatening endocrine emergency requiring immediate aggressive treatment including antithyroid drugs, beta-blockers, iodine, corticosteroids, and supportive care.",
                "stage": "Highly_Suggestive_TS",
                "stage_description": "Thyroid storm highly suggestive",
                "clinical_recommendations": {
                    "immediate_actions": [
                        "Initiate immediate thyroid storm treatment protocol",
                        "Transfer to ICU or high-dependency unit",
                        "Multidisciplinary team approach (endocrinology, ICU, pharmacy)"
                    ],
                    "medications": [
                        "Antithyroid drugs: methimazole 20-30mg q8h OR propylthiouracil 300-400mg q6h",
                        "Beta-blocker: propranolol 1-2mg IV q5min or 40-80mg PO q6h",
                        "Iodine: SSKI 5 drops PO q6h or sodium iodide 1-2g IV daily",
                        "Corticosteroids: hydrocortisone 300mg IV then 100mg q8h"
                    ],
                    "supportive_care": [
                        "Aggressive cooling measures for hyperthermia",
                        "IV fluid resuscitation for dehydration",
                        "Electrolyte monitoring and correction",
                        "Nutritional support"
                    ],
                    "monitoring": [
                        "Continuous cardiac and hemodynamic monitoring",
                        "Frequent neurological assessments",
                        "Monitor for complications (heart failure, arrhythmias)"
                    ]
                },
                "score_breakdown": {
                    "temperature": {
                        "category": "101-102°F", 
                        "points": 15,
                        "max_points": 30
                    },
                    "cns_effects": {
                        "category": "Mild agitation",
                        "points": 10,
                        "max_points": 30
                    },
                    "gi_hepatic_dysfunction": {
                        "category": "Moderate (diarrhea, nausea, vomiting, abdominal pain)",
                        "points": 10,
                        "max_points": 20
                    },
                    "cardiovascular_dysfunction": {
                        "category": "Absent",
                        "points": 0,
                        "max_points": 15
                    },
                    "tachycardia": {
                        "category": "120-129 bpm",
                        "points": 15,
                        "max_points": 25
                    },
                    "atrial_fibrillation": {
                        "category": "Absent",
                        "points": 0,
                        "max_points": 10
                    },
                    "precipitant_history": {
                        "category": "Present",
                        "points": 10,
                        "max_points": 10
                    }
                }
            }
        }