"""
Follicular Lymphoma International Prognostic Index (FLIPI) Models

Request and response models for FLIPI calculation.

References (Vancouver style):
1. Solal-Céligny P, Roy P, Colombat P, White J, Armitage JO, Arranz-Saez R, 
   et al. Follicular lymphoma international prognostic index. Blood. 
   2004 Sep 1;104(5):1258-65.
2. van de Schans SA, Steyerberg EW, Nijziel MR, Creemers GJ, Janssen-Heijnen ML, 
   van Spronsen DJ. Validation, revision and extension of the Follicular 
   Lymphoma International Prognostic Index (FLIPI) in a population-based 
   setting. Ann Oncol. 2009 Oct;20(10):1697-702.
3. Federico M, Bellei M, Marcheselli L, Luminari S, Lopez-Guillermo A, Vitolo U, 
   et al. Follicular lymphoma international prognostic index 2: a new prognostic 
   index for follicular lymphoma developed by the international follicular 
   lymphoma prognostic factor project. J Clin Oncol. 2009 Sep 20;27(27):4555-62.

FLIPI is a widely validated prognostic index for follicular lymphoma that uses 
5 readily available clinical parameters to stratify patients into risk groups. 
Developed from 4167 patients, it remains the most commonly used prognostic tool 
for FL, helping guide treatment decisions and patient counseling.
"""

from pydantic import BaseModel, Field
from typing import Literal


class FlipiRequest(BaseModel):
    """
    Request model for Follicular Lymphoma International Prognostic Index (FLIPI)
    
    FLIPI evaluates 5 adverse prognostic factors:
    
    1. Age >60 years:
       - Advanced age associated with decreased overall survival
       - May reflect reduced tolerance to therapy and comorbidities
    
    2. >4 nodal sites:
       - Refers to involved nodal regions, not individual nodes
       - Standard nodal regions: cervical, axillary, inguinal-femoral, 
         para-aortic, iliac, mediastinal, hilar, epitrochlear, popliteal, 
         mesenteric, etc.
    
    3. Elevated LDH:
       - Marker of tumor burden and cell turnover
       - Use institution's upper limit of normal
    
    4. Hemoglobin <120 g/L (12 g/dL):
       - May indicate bone marrow involvement or chronic disease
       - Use actual hemoglobin value, not corrected for altitude
    
    5. Ann Arbor stage III-IV:
       - Stage III: Lymph nodes on both sides of diaphragm
       - Stage IV: Extranodal involvement (bone marrow, liver, etc.)
    
    Mnemonic: "NoLaSH" (Nodal areas, LDH, Age, Stage, Hemoglobin)
    """
    
    age_over_60: Literal["yes", "no"] = Field(
        ...,
        description=("Patient age greater than 60 years at diagnosis. "
                    "Age is one of the strongest prognostic factors in lymphoma. "
                    "'yes' = age >60 years, 'no' = age ≤60 years"),
        example="yes"
    )
    
    nodal_sites_over_4: Literal["yes", "no"] = Field(
        ...,
        description=("More than 4 nodal sites (regions) involved by lymphoma. "
                    "Count distinct anatomical regions (e.g., bilateral cervical = 2 sites). "
                    "Common sites: cervical, axillary, inguinal, mediastinal, para-aortic, "
                    "iliac, epitrochlear, popliteal. 'yes' = >4 sites, 'no' = ≤4 sites"),
        example="no"
    )
    
    ldh_elevated: Literal["yes", "no"] = Field(
        ...,
        description=("Serum lactate dehydrogenase (LDH) level above normal. "
                    "Use the upper limit of normal for your laboratory. "
                    "LDH elevation suggests high tumor burden or rapid cell turnover. "
                    "'yes' = above ULN, 'no' = normal or below"),
        example="no"
    )
    
    hemoglobin_below_120: Literal["yes", "no"] = Field(
        ...,
        description=("Hemoglobin level below 120 g/L (12 g/dL). "
                    "May indicate bone marrow involvement, bleeding, or anemia of chronic disease. "
                    "Use actual value without altitude correction. "
                    "'yes' = Hgb <120 g/L, 'no' = Hgb ≥120 g/L"),
        example="no"
    )
    
    stage_3_or_4: Literal["yes", "no"] = Field(
        ...,
        description=("Ann Arbor stage III or IV disease. "
                    "Stage III = lymph nodes on both sides of diaphragm (± spleen). "
                    "Stage IV = diffuse/disseminated involvement of extranodal organs "
                    "(bone marrow, liver, lung, etc.). "
                    "'yes' = stage III or IV, 'no' = stage I or II"),
        example="yes"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "age_over_60": "yes",
                "nodal_sites_over_4": "no",
                "ldh_elevated": "no",
                "hemoglobin_below_120": "no",
                "stage_3_or_4": "yes"
            }
        }


class FlipiResponse(BaseModel):
    """
    Response model for Follicular Lymphoma International Prognostic Index (FLIPI)
    
    FLIPI stratifies patients into three risk groups:
    - Low risk (0-1 factors): ~36% of patients, favorable prognosis
    - Intermediate risk (2 factors): ~37% of patients, moderate prognosis
    - High risk (3-5 factors): ~27% of patients, less favorable prognosis
    
    The index helps guide treatment decisions but should be considered alongside:
    - Patient symptoms and performance status
    - Tumor burden (GELF criteria)
    - Patient preferences and goals
    - Availability of clinical trials
    
    Note: FLIPI-2 and m7-FLIPI are newer versions with additional parameters
    but original FLIPI remains widely used due to simplicity and validation.
    
    References:
    1. Solal-Céligny P, et al. Blood. 2004;104(5):1258-65.
    2. van de Schans SA, et al. Ann Oncol. 2009;20(10):1697-702.
    """
    
    result: int = Field(
        ...,
        description="FLIPI score calculated as sum of adverse factors (range: 0-5 points)",
        example=2
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation including prognosis and treatment considerations",
        example=("Intermediate risk group with moderate prognosis. 10-year overall "
                "survival approximately 50%. These patients often benefit from "
                "systemic therapy when symptomatic.")
    )
    
    stage: str = Field(
        ...,
        description="Risk group classification (Low Risk, Intermediate Risk, or High Risk)",
        example="Intermediate Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Description of number of adverse factors present",
        example="2 adverse factors"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 2,
                "unit": "points",
                "interpretation": ("Intermediate risk group with moderate prognosis. 10-year overall "
                                 "survival approximately 50%. 5-year overall survival approximately "
                                 "70%. These patients often benefit from systemic therapy, particularly "
                                 "when symptomatic or with high tumor burden. Treatment options include "
                                 "rituximab monotherapy or chemoimmunotherapy depending on clinical context."),
                "stage": "Intermediate Risk",
                "stage_description": "2 adverse factors"
            }
        }