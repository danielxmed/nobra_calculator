"""
Milan Criteria for Liver Transplantation Models

Request and response models for Milan criteria assessment.

References (Vancouver style):
1. Mazzaferro V, Regalia E, Doci R, Andreola S, Pulvirenti A, Bozzetti F, et al. 
   Liver transplantation for the treatment of small hepatocellular carcinomas in 
   patients with cirrhosis. N Engl J Med. 1996 Mar 14;334(11):693-9. 
   doi: 10.1056/NEJM199603143341104.
2. Mazzaferro V, Llovet JM, Miceli R, Bhoori S, Schiavo M, Mariani L, et al. 
   Predicting survival after liver transplantation in patients with hepatocellular 
   carcinoma beyond the Milan criteria: a retrospective, exploratory analysis. 
   Lancet Oncol. 2009 Jan;10(1):35-43. doi: 10.1016/S1470-2045(08)70284-5.
3. Mazzaferro V, Bhoori S, Sposito C, Bongini M, Langer M, Miceli R, et al. 
   Milan criteria in liver transplantation for hepatocellular carcinoma: an 
   evidence-based analysis of 15 years of experience. Liver Transpl. 2011 Oct;
   17 Suppl 2:S44-57. doi: 10.1002/lt.22365.
4. Marrero JA, Kulik LM, Sirlin CB, Zhu AX, Finn RS, Abecassis MM, et al. 
   Diagnosis, Staging, and Management of Hepatocellular Carcinoma: 2018 Practice 
   Guidance by the American Association for the Study of Liver Diseases. 
   Hepatology. 2018 Aug;68(2):723-750. doi: 10.1002/hep.29913.

The Milan criteria define eligibility for liver transplantation in patients with 
hepatocellular carcinoma (HCC) and cirrhosis. The criteria specify: single tumor 
≤5 cm OR 2-3 tumors each ≤3 cm, with no extrahepatic disease and no major vascular 
invasion. Patients meeting these criteria have excellent post-transplant outcomes 
with 4-year survival rates around 75%.
"""

from pydantic import BaseModel, Field
from typing import Literal, Optional


class MilanCriteriaRequest(BaseModel):
    """
    Request model for Milan Criteria for Liver Transplantation
    
    The Milan criteria assess eligibility for liver transplantation in patients 
    with hepatocellular carcinoma (HCC) and cirrhosis based on:
    
    Tumor Burden:
    - single: One HCC tumor (requires size ≤5 cm)
    - two_three: 2-3 HCC tumors (each must be ≤3 cm)
    - more_than_three: >3 HCC tumors (automatically excludes from transplant)
    
    Exclusion Criteria:
    - Extrahepatic involvement: Any metastases outside the liver
    - Major vessel involvement: Portal vein or hepatic vein thrombosis
    
    Additional considerations:
    - Count only viable tumors (exclude completely necrotic lesions after treatment)
    - High-quality multiphasic CT or MRI required for accurate assessment
    - AFP levels >1000 ng/mL require downstaging to <500 ng/mL
    - Successful downstaging must be maintained for 3-6 months before eligibility

    References (Vancouver style):
    1. Mazzaferro V, Regalia E, Doci R, Andreola S, Pulvirenti A, Bozzetti F, et al. 
       Liver transplantation for the treatment of small hepatocellular carcinomas in 
       patients with cirrhosis. N Engl J Med. 1996 Mar 14;334(11):693-9. 
       doi: 10.1056/NEJM199603143341104.
    2. Mazzaferro V, Llovet JM, Miceli R, Bhoori S, Schiavo M, Mariani L, et al. 
       Predicting survival after liver transplantation in patients with hepatocellular 
       carcinoma beyond the Milan criteria: a retrospective, exploratory analysis. 
       Lancet Oncol. 2009 Jan;10(1):35-43. doi: 10.1016/S1470-2045(08)70284-5.
    3. Mazzaferro V, Bhoori S, Sposito C, Bongini M, Langer M, Miceli R, et al. 
       Milan criteria in liver transplantation for hepatocellular carcinoma: an 
       evidence-based analysis of 15 years of experience. Liver Transpl. 2011 Oct;
       17 Suppl 2:S44-57. doi: 10.1002/lt.22365.
    4. Marrero JA, Kulik LM, Sirlin CB, Zhu AX, Finn RS, Abecassis MM, et al. 
       Diagnosis, Staging, and Management of Hepatocellular Carcinoma: 2018 Practice 
       Guidance by the American Association for the Study of Liver Diseases. 
       Hepatology. 2018 Aug;68(2):723-750. doi: 10.1002/hep.29913.
    """
    
    tumor_count: Literal["single", "two_three", "more_than_three"] = Field(
        ...,
        description="Number of HCC tumors identified on imaging. Single tumor requires ≤5cm, 2-3 tumors each require ≤3cm, >3 tumors automatically excludes transplant eligibility",
        example="single"
    )
    
    single_tumor_size: Optional[float] = Field(
        None,
        ge=0,
        le=20,
        description="Size of single tumor in cm (required only if tumor_count is 'single'). Must be ≤5 cm to meet Milan criteria",
        example=4.2
    )
    
    largest_tumor_size: Optional[float] = Field(
        None,
        ge=0,
        le=20,
        description="Size of largest tumor in cm (required only if tumor_count is 'two_three'). Each tumor must be ≤3 cm to meet Milan criteria",
        example=2.8
    )
    
    extrahepatic_involvement: Literal["no", "yes"] = Field(
        ...,
        description="Evidence of extrahepatic disease (metastases outside the liver). Any extrahepatic involvement excludes transplant eligibility",
        example="no"
    )
    
    major_vessel_involvement: Literal["no", "yes"] = Field(
        ...,
        description="Major vascular invasion including portal vein or hepatic vein thrombosis. Any major vessel involvement excludes transplant eligibility",
        example="no"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "tumor_count": "single",
                "single_tumor_size": 4.2,
                "largest_tumor_size": None,
                "extrahepatic_involvement": "no",
                "major_vessel_involvement": "no"
            }
        }


class MilanCriteriaResponse(BaseModel):
    """
    Response model for Milan Criteria for Liver Transplantation
    
    Determines transplant eligibility based on tumor burden and absence of 
    extrahepatic disease or major vascular invasion:
    
    Meets Criteria:
    - Single tumor ≤5 cm OR 2-3 tumors each ≤3 cm
    - No extrahepatic involvement
    - No major vessel involvement
    - Excellent post-transplant outcomes (4-year survival ~75%)
    - Qualifies for MELD exception points after 6-month waiting period
    
    Does Not Meet Criteria:
    - Consider downstaging with locoregional therapies
    - Monitor AFP levels (<500 ng/mL required for eligibility)
    - Re-evaluate after successful downstaging maintained 3-6 months
    
    Reference: Mazzaferro V, et al. N Engl J Med. 1996;334(11):693-9.
    """
    
    result: str = Field(
        ...,
        description="Whether patient meets Milan criteria ('Meets Criteria' or 'Does Not Meet Criteria')",
        example="Meets Criteria"
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement (empty string for categorical result)",
        example=""
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation with transplant eligibility and management recommendations",
        example="Patient meets Milan criteria and is eligible for liver transplantation consideration. Excellent post-transplant outcomes expected with 4-year survival ~75%. Qualifies for MELD exception points (MMaT-3) after 6-month waiting period."
    )
    
    stage: str = Field(
        ...,
        description="Eligibility category (Meets Criteria or Does Not Meet Criteria)",
        example="Meets Criteria"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of eligibility status",
        example="Eligible for liver transplantation"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": "Meets Criteria",
                "unit": "",
                "interpretation": "Patient meets Milan criteria and is eligible for liver transplantation consideration. Excellent post-transplant outcomes expected with 4-year survival ~75%. Qualifies for MELD exception points (MMaT-3) after 6-month waiting period.",
                "stage": "Meets Criteria",
                "stage_description": "Eligible for liver transplantation"
            }
        }