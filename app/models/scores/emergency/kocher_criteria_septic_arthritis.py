"""
Kocher Criteria for Septic Arthritis Models

Request and response models for Kocher Criteria calculation.

References (Vancouver style):
1. Kocher MS, Zurakowski D, Kasser JR. Differentiating between septic arthritis and 
   transient synovitis of the hip in children: an evidence-based clinical prediction 
   algorithm. J Bone Joint Surg Am. 1999 Dec;81(12):1662-70.
2. Caird MS, Flynn JM, Leung YL, Millman JE, D'Italia JG, Dormans JP. Factors 
   distinguishing septic arthritis from transient synovitis of the hip in children. 
   A prospective study. J Bone Joint Surg Am. 2006 Jun;88(6):1251-7.
3. Luhmann SJ, Jones A, Schootman M, Gordon JE, Schoenecker PL, Luhmann JD. 
   Differentiation between septic arthritis and transient synovitis of the hip in 
   children with clinical prediction algorithms. J Bone Joint Surg Am. 2004 May;86(5):956-62.
4. Del Beccaro MA, Champoux AN, Bockers T, Mendelman PM. Septic arthritis versus 
   transient synovitis of the hip: the value of screening laboratory tests. Ann Emerg Med. 
   1992 Oct;21(10):1418-22.

The Kocher Criteria is a clinical prediction rule developed to differentiate septic 
arthritis from transient synovitis in pediatric patients presenting with hip pain. 
The original study by Kocher et al. (1999) identified four independent predictors 
that, when combined, provide excellent risk stratification for septic arthritis.

The four predictors are:
1. Non-weight bearing on the affected limb
2. Temperature >38.5°C (101.3°F) at presentation or in history
3. Erythrocyte sedimentation rate (ESR) >40 mm/hr
4. White blood cell count >12,000 cells/mm³

Risk stratification based on number of predictors:
- 0 predictors: <0.2-2% risk of septic arthritis
- 1 predictor: 3-9.5% risk of septic arthritis  
- 2 predictors: 35-40% risk of septic arthritis
- 3 predictors: 72.8-93.1% risk of septic arthritis
- 4 predictors: 93-99.6% risk of septic arthritis

The criteria have been extensively validated in multiple pediatric populations and 
remain one of the most widely used clinical decision tools in pediatric orthopedics 
and emergency medicine for differentiating septic arthritis from transient synovitis.
"""

from pydantic import BaseModel, Field
from typing import Literal, Dict


class KocherCriteriaSepticArthritisRequest(BaseModel):
    """
    Request model for Kocher Criteria for Septic Arthritis
    
    The Kocher Criteria assess four clinical and laboratory predictors to estimate 
    the probability of septic arthritis in pediatric patients presenting with hip 
    pain and related symptoms. Each predictor is evaluated as present ("yes") or 
    absent ("no"):
    
    Clinical Predictors:
    - Non-weight bearing: Patient's inability to bear weight on affected limb
    - Temperature >38.5°C: Fever at presentation or in recent history
    
    Laboratory Predictors:
    - ESR >40 mm/hr: Elevated erythrocyte sedimentation rate indicating inflammation
    - WBC >12,000 cells/mm³: Elevated white blood cell count suggesting infection
    
    Clinical Context:
    - Originally developed and validated in children aged 2-16 years
    - Most commonly applied to hip symptoms but may be useful for other joints
    - Should be used in conjunction with clinical judgment and imaging
    - Risk increases substantially with each additional positive predictor
    
    Important Considerations:
    - C-reactive protein (CRP) >20 mg/L has been proposed as additional predictor
    - Clinical assessment remains paramount regardless of score
    - Serial evaluation may be needed as symptoms can evolve rapidly
    - Lower reliability in very young children (<2 years) or immunocompromised patients
    
    Management Implications:
    - 0-1 predictors: Conservative management with close monitoring often appropriate
    - 2 predictors: Strong consideration for arthrocentesis or surgical intervention
    - 3-4 predictors: Urgent surgical drainage typically indicated
    
    References (Vancouver style):
    1. Kocher MS, Zurakowski D, Kasser JR. Differentiating between septic arthritis and 
       transient synovitis of the hip in children: an evidence-based clinical prediction 
       algorithm. J Bone Joint Surg Am. 1999 Dec;81(12):1662-70.
    2. Caird MS, Flynn JM, Leung YL, Millman JE, D'Italia JG, Dormans JP. Factors 
       distinguishing septic arthritis from transient synovitis of the hip in children. 
       A prospective study. J Bone Joint Surg Am. 2006 Jun;88(6):1251-7.
    """
    
    non_weight_bearing: Literal["yes", "no"] = Field(
        ...,
        description="Patient unable to bear weight on the affected limb. This clinical "
                   "finding is one of the strongest predictors of septic arthritis and "
                   "reflects significant joint inflammation and pain. Assess by observing "
                   "the patient's gait or asking them to stand on the affected leg.",
        example="no"
    )
    
    temperature_over_38_5: Literal["yes", "no"] = Field(
        ...,
        description="Temperature greater than 38.5°C (101.3°F) at presentation or in "
                   "recent history. Fever indicates systemic inflammatory response and "
                   "is a key differentiator between septic arthritis and transient synovitis. "
                   "Document highest temperature within 24-48 hours of presentation.",
        example="yes"
    )
    
    esr_over_40: Literal["yes", "no"] = Field(
        ...,
        description="Erythrocyte sedimentation rate (ESR) greater than 40 mm/hr. "
                   "Elevated ESR reflects systemic inflammation and is typically higher "
                   "in septic arthritis compared to transient synovitis. ESR should be "
                   "obtained as part of initial laboratory workup for suspected joint infection.",
        example="yes"
    )
    
    wbc_over_12000: Literal["yes", "no"] = Field(
        ...,
        description="White blood cell count greater than 12,000 cells/mm³. Elevated WBC "
                   "count suggests systemic bacterial infection and immune response. "
                   "Total WBC count should be part of complete blood count (CBC) with "
                   "differential in suspected septic arthritis cases.",
        example="no"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "non_weight_bearing": "no",
                "temperature_over_38_5": "yes", 
                "esr_over_40": "yes",
                "wbc_over_12000": "no"
            }
        }


class KocherCriteriaSepticArthritisResponse(BaseModel):
    """
    Response model for Kocher Criteria for Septic Arthritis
    
    Provides comprehensive risk assessment for septic arthritis based on the number 
    of positive predictors, with detailed clinical interpretation and management 
    recommendations. The response stratifies patients into risk categories ranging 
    from very low risk (0 predictors) to very high risk (4 predictors).
    
    Risk Stratification:
    - Very Low Risk (0 predictors): <0.2-2% probability - Conservative management
    - Low Risk (1 predictor): 3-9.5% probability - Close monitoring with follow-up
    - Moderate Risk (2 predictors): 35-40% probability - Consider arthrocentesis
    - High Risk (3 predictors): 72.8-93.1% probability - Urgent surgical intervention
    - Very High Risk (4 predictors): 93-99.6% probability - Emergency surgery required
    
    Clinical Decision Making:
    - The criteria provide probability estimates to guide clinical decision-making
    - Higher predictor counts warrant more aggressive intervention
    - Clinical judgment remains essential regardless of score
    - Consider additional factors like patient age, comorbidities, and clinical trajectory
    
    Management Principles:
    - Early recognition and treatment prevent joint destruction and complications
    - Arthrocentesis is both diagnostic and therapeutic when indicated
    - Empiric antibiotic therapy should be considered for moderate to high-risk patients
    - Orthopedic consultation urgency increases with higher predictor counts
    
    Validation and Performance:
    - Extensively validated across multiple pediatric populations
    - High negative predictive value for low predictor counts
    - Excellent positive predictive value for high predictor counts
    - Maintains good performance across different clinical settings
    
    Reference: Kocher MS, et al. J Bone Joint Surg Am. 1999;81(12):1662-70.
    """
    
    result: Dict = Field(
        ...,
        description="Detailed Kocher Criteria assessment including predictor count, individual predictors, and risk range",
        example={
            "predictor_count": 2,
            "predictors": {
                "non_weight_bearing": False,
                "temperature_over_38_5": True,
                "esr_over_40": True,
                "wbc_over_12000": False
            },
            "risk_range": {
                "min_risk_percent": 35.0,
                "max_risk_percent": 40.0
            },
            "stage": "Moderate Risk",
            "description": "2 predictors present"
        }
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the assessment",
        example="predictors"
    )
    
    interpretation: str = Field(
        ...,
        description="Comprehensive clinical interpretation including probability assessment, "
                   "clinical recommendations, and management guidance based on risk stratification",
        example="Moderate risk of septic arthritis (35-40% probability). Strong consideration for arthrocentesis or surgical drainage is warranted. Urgent orthopedic consultation recommended within hours. Consider empiric antibiotic therapy while awaiting definitive diagnosis. Remember that clinical judgment remains paramount, and the Kocher criteria should be used as an adjunct to, not a replacement for, thorough clinical assessment. Serial evaluation may be necessary as the clinical picture can evolve rapidly."
    )
    
    stage: str = Field(
        ...,
        description="Risk category (Very Low Risk, Low Risk, Moderate Risk, High Risk, Very High Risk)",
        example="Moderate Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the risk level and predictor count",
        example="2 predictors present"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": {
                    "predictor_count": 2,
                    "predictors": {
                        "non_weight_bearing": False,
                        "temperature_over_38_5": True,
                        "esr_over_40": True,
                        "wbc_over_12000": False
                    },
                    "risk_range": {
                        "min_risk_percent": 35.0,
                        "max_risk_percent": 40.0
                    },
                    "stage": "Moderate Risk",
                    "description": "2 predictors present"
                },
                "unit": "predictors",
                "interpretation": "Moderate risk of septic arthritis (35-40% probability). Strong consideration for arthrocentesis or surgical drainage is warranted. Urgent orthopedic consultation recommended within hours. Consider empiric antibiotic therapy while awaiting definitive diagnosis. Remember that clinical judgment remains paramount, and the Kocher criteria should be used as an adjunct to, not a replacement for, thorough clinical assessment. Serial evaluation may be necessary as the clinical picture can evolve rapidly.",
                "stage": "Moderate Risk",
                "stage_description": "2 predictors present"
            }
        }