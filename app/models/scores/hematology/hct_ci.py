"""
Hematopoietic Cell Transplantation-specific Comorbidity Index (HCT-CI) Models

Request and response models for HCT-CI calculation.

References (Vancouver style):
1. Sorror ML, Maris MB, Storb R, Baron F, Sandmaier BM, Maloney DG, et al. 
   Hematopoietic cell transplantation (HCT)-specific comorbidity index: a new tool 
   for risk assessment before allogeneic HCT. Blood. 2005 Oct 15;106(8):2912-9. 
   doi: 10.1182/blood-2005-05-2004.
2. Sorror ML, Sandmaier BM, Storer BE, Franke GN, Laport GG, Chauncey TR, et al. 
   Comorbidity-age index: a clinical measure of biologic age before allogeneic 
   hematopoietic cell transplantation. J Clin Oncol. 2014 Oct 10;32(29):3249-56. 
   doi: 10.1200/JCO.2013.53.8157.
3. Sorror ML, Martin PJ, Storb RF, Bhatia S, Maziarz RT, Pulsipher MA, et al. 
   Pretransplant comorbidities predict severity of acute graft-versus-host disease 
   and subsequent mortality. Blood. 2014 Jul 10;124(2):287-95. 
   doi: 10.1182/blood-2014-01-550566.

The HCT-CI is a validated scoring system that evaluates 17 comorbidity categories 
to predict non-relapse mortality and overall survival in patients undergoing 
hematopoietic cell transplantation. It has been shown to be more sensitive than 
the Charlson Comorbidity Index for this patient population.
"""

from pydantic import BaseModel, Field, validator
from typing import Literal, Optional


class HctCiRequest(BaseModel):
    """
    Request model for Hematopoietic Cell Transplantation-specific Comorbidity Index (HCT-CI)
    
    The HCT-CI evaluates 17 comorbidity categories, each assigned weighted scores:
    
    1-Point Comorbidities:
    - Arrhythmia: Atrial fibrillation/flutter, sick sinus syndrome, ventricular arrhythmias
    - Cardiac: CAD, CHF, MI, or EF ≤50%
    - Inflammatory bowel disease: Crohn's disease or ulcerative colitis
    - Diabetes: Requiring insulin or oral hypoglycemics
    - Cerebrovascular disease: TIA or CVA
    - Psychiatric disturbance: Depression/anxiety requiring psychiatric consultation
    - Mild hepatic: Chronic hepatitis, bilirubin >ULN to 1.5x ULN, or AST/ALT >ULN to 2.5x ULN
    - Obesity: BMI >35 kg/m²
    - Infection: Requiring antimicrobial treatment after day 0
    
    2-Point Comorbidities:
    - Rheumatologic: SLE, RA, polymyositis, mixed CTD, polymyalgia rheumatica
    - Peptic ulcer: Requiring treatment
    - Moderate/severe renal: Creatinine >2 mg/dL, on dialysis, or prior renal transplant
    - Moderate pulmonary: DLco and/or FEV1 66-80% or dyspnea on slight activity
    
    3-Point Comorbidities:
    - Prior solid tumor: Treated at any time (excluding non-melanoma skin cancer)
    - Heart valve disease: Except mitral valve prolapse
    - Severe pulmonary: DLco and/or FEV1 ≤65% or dyspnea at rest or requiring oxygen
    - Moderate/severe hepatic: Liver cirrhosis, bilirubin >1.5x ULN, or AST/ALT >2.5x ULN
    
    Age Adjustment (Sorror 2014):
    - Age ≥40 years: +1 point
    
    References (Vancouver style):
    1. Sorror ML, Maris MB, Storb R, Baron F, Sandmaier BM, Maloney DG, et al. 
       Hematopoietic cell transplantation (HCT)-specific comorbidity index: a new tool 
       for risk assessment before allogeneic HCT. Blood. 2005 Oct 15;106(8):2912-9.
    2. Sorror ML, Sandmaier BM, Storer BE, Franke GN, Laport GG, Chauncey TR, et al. 
       Comorbidity-age index: a clinical measure of biologic age before allogeneic 
       hematopoietic cell transplantation. J Clin Oncol. 2014 Oct 10;32(29):3249-56.
    """
    
    arrhythmia: Literal["none", "present"] = Field(
        ...,
        description="History of arrhythmia including atrial fibrillation/flutter, sick sinus syndrome, or ventricular arrhythmias. Scores 1 point if present",
        example="none"
    )
    
    cardiac: Literal["none", "cad_chf_mi_ef", "valve_disease"] = Field(
        ...,
        description="Cardiac dysfunction. 'cad_chf_mi_ef' includes coronary artery disease, congestive heart failure, myocardial infarction, or ejection fraction ≤50% (1 point). 'valve_disease' excludes mitral valve prolapse (3 points)",
        example="none"
    )
    
    inflammatory_bowel: Literal["none", "present"] = Field(
        ...,
        description="Inflammatory bowel disease including Crohn's disease or ulcerative colitis. Scores 1 point if present",
        example="none"
    )
    
    diabetes: Literal["none_or_diet", "treated"] = Field(
        ...,
        description="Diabetes status. 'treated' means requiring insulin or oral hypoglycemic medications. Scores 1 point if treated",
        example="none_or_diet"
    )
    
    cerebrovascular: Literal["none", "present"] = Field(
        ...,
        description="Cerebrovascular disease including transient ischemic attack (TIA) or cerebrovascular accident (CVA/stroke). Scores 1 point if present",
        example="none"
    )
    
    psychiatric: Literal["none", "requiring_treatment"] = Field(
        ...,
        description="Psychiatric disturbance such as depression or anxiety requiring psychiatric consultation or treatment. Scores 1 point if requiring treatment",
        example="none"
    )
    
    hepatic: Literal["none", "mild", "moderate_severe"] = Field(
        ...,
        description="Hepatic dysfunction. 'mild' includes chronic hepatitis, bilirubin >ULN to 1.5x ULN, or AST/ALT >ULN to 2.5x ULN (1 point). 'moderate_severe' includes liver cirrhosis, bilirubin >1.5x ULN, or AST/ALT >2.5x ULN (3 points)",
        example="none"
    )
    
    obesity: Literal["no", "yes"] = Field(
        ...,
        description="Obesity defined as body mass index (BMI) >35 kg/m². Scores 1 point if yes",
        example="no"
    )
    
    infection: Literal["none", "requiring_treatment"] = Field(
        ...,
        description="Active infection requiring continuation of antimicrobial treatment after day 0 of transplant. Scores 1 point if requiring treatment",
        example="none"
    )
    
    rheumatologic: Literal["none", "present"] = Field(
        ...,
        description="Rheumatologic disease including SLE, rheumatoid arthritis, polymyositis, mixed connective tissue disease, or polymyalgia rheumatica. Scores 2 points if present",
        example="none"
    )
    
    peptic_ulcer: Literal["none_or_no_treatment", "requiring_treatment"] = Field(
        ...,
        description="Peptic ulcer disease requiring treatment (PPIs, H2 blockers, or other therapy). Scores 2 points if requiring treatment",
        example="none_or_no_treatment"
    )
    
    renal: Literal["none_or_mild", "moderate_severe"] = Field(
        ...,
        description="Renal dysfunction. 'moderate_severe' includes serum creatinine >2 mg/dL (177 μmol/L), on dialysis, or prior renal transplant. Scores 2 points if moderate/severe",
        example="none_or_mild"
    )
    
    pulmonary: Literal["none_or_mild", "moderate", "severe"] = Field(
        ...,
        description="Pulmonary dysfunction based on DLco and/or FEV1. 'moderate' = 66-80% predicted or dyspnea on slight activity (2 points). 'severe' = ≤65% predicted or dyspnea at rest or requiring oxygen (3 points)",
        example="none_or_mild"
    )
    
    prior_solid_tumor: Literal["no", "yes"] = Field(
        ...,
        description="History of prior solid tumor treated at any time point, excluding non-melanoma skin cancer. Scores 3 points if yes",
        example="no"
    )
    
    include_age: Literal["no", "yes"] = Field(
        ...,
        description="Whether to include age adjustment in the score calculation (Sorror 2014 modification). If yes, age ≥40 years adds 1 point",
        example="no"
    )
    
    age: Optional[int] = Field(
        None,
        description="Patient age in years. Required if include_age is 'yes'. Age ≥40 years adds 1 point to the total score",
        example=45,
        ge=0,
        le=100
    )
    
    @validator('age')
    def validate_age_requirement(cls, v, values):
        """Ensure age is provided when age adjustment is requested"""
        if values.get('include_age') == 'yes' and v is None:
            raise ValueError("Age is required when age adjustment is included")
        return v
    
    class Config:
        schema_extra = {
            "example": {
                "arrhythmia": "none",
                "cardiac": "cad_chf_mi_ef",
                "inflammatory_bowel": "none",
                "diabetes": "treated",
                "cerebrovascular": "none",
                "psychiatric": "none",
                "hepatic": "mild",
                "obesity": "no",
                "infection": "none",
                "rheumatologic": "none",
                "peptic_ulcer": "none_or_no_treatment",
                "renal": "none_or_mild",
                "pulmonary": "moderate",
                "prior_solid_tumor": "no",
                "include_age": "yes",
                "age": 45
            }
        }


class HctCiResponse(BaseModel):
    """
    Response model for Hematopoietic Cell Transplantation-specific Comorbidity Index (HCT-CI)
    
    The HCT-CI stratifies patients into three risk groups:
    - Low Risk (Score 0): NRM ~14% at 2 years
    - Intermediate Risk (Score 1-2): NRM ~21% at 2 years
    - High Risk (Score ≥3): NRM ~41% at 2 years
    
    NRM = Non-relapse mortality
    
    The score helps guide transplant eligibility decisions and conditioning regimen selection.
    
    Reference: Sorror ML, et al. Blood. 2005;106(8):2912-9.
    """
    
    result: int = Field(
        ...,
        description="HCT-CI total score (range: 0-26 points without age adjustment, 0-27 with age adjustment)",
        example=6
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation including risk group classification and non-relapse mortality estimate",
        example="High risk group. Non-relapse mortality approximately 41% at 2 years. Consider alternative therapies or risk-adapted conditioning regimens."
    )
    
    stage: str = Field(
        ...,
        description="Risk category classification (Low Risk, Intermediate Risk, High Risk)",
        example="High Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Score range description for the risk category",
        example="Score ≥3"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 6,
                "unit": "points",
                "interpretation": "High risk group. Non-relapse mortality approximately 41% at 2 years. Consider alternative therapies or risk-adapted conditioning regimens.",
                "stage": "High Risk",
                "stage_description": "Score ≥3"
            }
        }