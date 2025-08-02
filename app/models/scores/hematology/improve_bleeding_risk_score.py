"""
IMPROVE Bleeding Risk Score Models

Request and response models for IMPROVE Bleeding Risk Score calculation.

References (Vancouver style):
1. Spyropoulos AC, Anderson FA Jr, FitzGerald G, et al. Predictive and associative 
   models to identify hospitalized medical patients at risk for VTE. Chest. 2011 
   Sep;140(3):706-714. doi: 10.1378/chest.10-1944.
2. Hostler DC, Marx ES, Moores LK, et al. Validation of the International Medical 
   Prevention Registry on Venous Thromboembolism bleeding risk model. Chest. 2016 
   Apr;149(4):1002-1009. doi: 10.1378/chest.15-2082.
3. Rosenberg D, Eichorn A, Alarcon M, et al. External validation of the risk assessment 
   model of the International Medical Prevention Registry on Venous Thromboembolism 
   (IMPROVE) for medical patients in a tertiary health system. J Am Heart Assoc. 2014 
   Nov 4;3(6):e001152. doi: 10.1161/JAHA.114.001152.
4. Stuck AK, Spirk D, Schaudt J, Kucher N. Risk assessment models for venous 
   thromboembolism in acutely ill medical patients. A systematic review. Thromb 
   Haemost. 2017 May 3;117(5):801-808. doi: 10.1160/TH16-08-0631.

The IMPROVE Bleeding Risk Score assesses bleeding risk at hospital admission for 
acutely ill medical patients, particularly when considering anticoagulation therapy. 
Developed from an international database of 15,156 patients across 52 hospitals in 
12 countries, this validated tool helps identify patients at high risk for bleeding 
complications. The score uses 11 clinical variables to stratify patients into low 
(<7 points) and high risk (≥7 points) categories, with high-risk patients showing 
significantly higher bleeding rates (3.9% vs 1.2% major bleeding).
"""

from pydantic import BaseModel, Field
from typing import Literal


class ImproveBleedingRiskScoreRequest(BaseModel):
    """
    Request model for IMPROVE Bleeding Risk Score calculation
    
    Assesses bleeding risk at hospital admission for acutely ill medical patients,
    particularly when considering anticoagulation therapy.
    
    Risk Factors Assessed:
    - Demographics: Age and gender
    - Organ function: Renal function (GFR), hepatic failure
    - Comorbidities: Cancer, rheumatic disease
    - Clinical setting: ICU/CCU stay, central venous catheter
    - Hematologic: Platelet count, recent bleeding history
    - GI factors: Active gastroduodenal ulcer (highest risk factor)
    
    Scoring System:
    - Score <7 points: No increased bleeding risk (1.2% major bleeding rate)
    - Score ≥7 points: Increased bleeding risk (3.9% major bleeding rate)
    
    The score helps clinicians assess the risk-benefit ratio of pharmacological
    thromboprophylaxis and identify patients requiring enhanced bleeding monitoring.
    Developed from the IMPROVE international observational database with validation
    across multiple external cohorts.

    References (Vancouver style):
    1. Spyropoulos AC, Anderson FA Jr, FitzGerald G, et al. Predictive and associative 
       models to identify hospitalized medical patients at risk for VTE. Chest. 2011 
       Sep;140(3):706-714. doi: 10.1378/chest.10-1944.
    2. Hostler DC, Marx ES, Moores LK, et al. Validation of the International Medical 
       Prevention Registry on Venous Thromboembolism bleeding risk model. Chest. 2016 
       Apr;149(4):1002-1009. doi: 10.1378/chest.15-2082.
    3. Rosenberg D, Eichorn A, Alarcon M, et al. External validation of the risk assessment 
       model of the International Medical Prevention Registry on Venous Thromboembolism 
       (IMPROVE) for medical patients in a tertiary health system. J Am Heart Assoc. 2014 
       Nov 4;3(6):e001152. doi: 10.1161/JAHA.114.001152.
    """
    
    age_category: Literal["under_40", "40_to_84", "85_or_over"] = Field(
        ...,
        description="Patient age category. Age is a significant predictor of bleeding risk, with risk increasing progressively with advanced age due to physiological changes, comorbidities, and polypharmacy. Scores 0 points for <40 years, 1.5 points for 40-84 years, 3.5 points for ≥85 years",
        example="40_to_84"
    )
    
    gender: Literal["female", "male"] = Field(
        ...,
        description="Patient gender. Male gender is associated with increased bleeding risk in hospitalized patients, possibly due to higher rates of cardiovascular disease and antiplatelet therapy use. Scores 0 points for female, 1 point for male",
        example="male"
    )
    
    renal_function: Literal["gfr_60_or_above", "gfr_30_to_59", "gfr_under_30"] = Field(
        ...,
        description="Glomerular filtration rate (GFR) category in mL/min/m². Reduced renal function increases bleeding risk through impaired drug clearance, uremic bleeding tendency, and altered platelet function. Scores 0 points for GFR ≥60, 1 point for GFR 30-59, 2.5 points for GFR <30",
        example="gfr_60_or_above"
    )
    
    current_cancer: Literal["yes", "no"] = Field(
        ...,
        description="Active cancer within 6 months prior to admission. Cancer increases bleeding risk through tumor-related factors, chemotherapy effects, thrombocytopenia, and invasive procedures. Scores 2 points if yes",
        example="no"
    )
    
    rheumatic_disease: Literal["yes", "no"] = Field(
        ...,
        description="Presence of rheumatic disease (rheumatoid arthritis, systemic lupus erythematosus, other autoimmune conditions). Associated with increased bleeding risk due to disease-related factors and immunosuppressive medications. Scores 2 points if yes",
        example="no"
    )
    
    central_venous_catheter: Literal["yes", "no"] = Field(
        ...,
        description="Presence of central venous catheter. Central lines increase bleeding risk through direct vascular access, procedural complications, and potential for catheter-related bleeding. Scores 2 points if yes",
        example="no"
    )
    
    icu_ccu_stay: Literal["yes", "no"] = Field(
        ...,
        description="Current stay in intensive care unit (ICU) or coronary care unit (CCU). Critical care setting indicates severe illness with increased bleeding risk from procedures, medications, and hemodynamic instability. Scores 2.5 points if yes",
        example="no"
    )
    
    hepatic_failure: Literal["yes", "no"] = Field(
        ...,
        description="Hepatic failure defined as INR >1.5. Liver dysfunction significantly increases bleeding risk through reduced synthesis of coagulation factors and impaired hemostasis. Scores 2.5 points if yes",
        example="no"
    )
    
    platelet_count_category: Literal["50_or_above", "under_50"] = Field(
        ...,
        description="Platelet count category (×10⁹/L). Thrombocytopenia (<50,000/μL) significantly increases bleeding risk through impaired primary hemostasis and platelet plug formation. Scores 0 points for ≥50, 4 points for <50",
        example="50_or_above"
    )
    
    bleeding_in_3_months: Literal["yes", "no"] = Field(
        ...,
        description="History of bleeding in the 3 months prior to admission. Recent bleeding history is a strong predictor of recurrent bleeding events and indicates underlying bleeding tendency. Scores 4 points if yes",
        example="no"
    )
    
    active_gastroduodenal_ulcer: Literal["yes", "no"] = Field(
        ...,
        description="Presence of active gastroduodenal ulcer. Active peptic ulcer disease represents the highest bleeding risk factor due to ongoing mucosal erosion and potential for life-threatening hemorrhage. Scores 4.5 points if yes",
        example="no"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "age_category": "40_to_84",
                "gender": "male",
                "renal_function": "gfr_60_or_above",
                "current_cancer": "no",
                "rheumatic_disease": "no",
                "central_venous_catheter": "no",
                "icu_ccu_stay": "no",
                "hepatic_failure": "no",
                "platelet_count_category": "50_or_above",
                "bleeding_in_3_months": "no",
                "active_gastroduodenal_ulcer": "no"
            }
        }


class ImproveBleedingRiskScoreResponse(BaseModel):
    """
    Response model for IMPROVE Bleeding Risk Score calculation
    
    Returns the IMPROVE Bleeding Risk Score with risk stratification and clinical
    recommendations for bleeding risk management in hospitalized medical patients.
    
    Risk Categories:
    - No Increased Risk (<7 points): 1.2% major bleeding rate - Standard protocols
    - Increased Risk (≥7 points): 3.9% major bleeding rate - Enhanced monitoring needed
    
    The score provides evidence-based guidance for anticoagulation decisions and helps
    identify patients requiring careful risk-benefit assessment for thromboprophylaxis.
    High-risk patients may benefit from non-pharmacologic interventions or enhanced
    bleeding surveillance if anticoagulation is necessary.
    
    Reference: Spyropoulos AC, et al. Chest. 2011;140(3):706-714.
    """
    
    result: float = Field(
        ...,
        description="IMPROVE Bleeding Risk Score calculated from clinical risk factors (range 0-30.5 points)",
        example=2.5,
        ge=0.0,
        le=30.5
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation and bleeding risk management recommendations based on the score",
        example="No increased bleeding risk identified. Standard anticoagulation protocols may be followed as clinically indicated. Routine monitoring for bleeding complications recommended."
    )
    
    stage: str = Field(
        ...,
        description="Bleeding risk category (No Increased Risk or Increased Risk)",
        example="No Increased Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the risk category with score range",
        example="Score 2.5 points (<7 points)"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 2.5,
                "unit": "points",
                "interpretation": "No increased bleeding risk identified. Standard anticoagulation protocols may be followed as clinically indicated. Routine monitoring for bleeding complications recommended.",
                "stage": "No Increased Risk",
                "stage_description": "Score 2.5 points (<7 points)"
            }
        }