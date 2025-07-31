"""
Barcelona-Clinic Liver Cancer (BCLC) Staging Classification Models

Request and response models for BCLC staging calculation.

References (Vancouver style):
1. Reig M, Forner A, Rimola J, Ferrer-Fàbrega J, Burrel M, Garcia-Criado Á, et al. 
   BCLC strategy for prognosis prediction and treatment recommendation: The 2022 
   update. J Hepatol. 2022 Mar;76(3):681-693. doi: 10.1016/j.jhep.2021.11.018.
2. Llovet JM, Brú C, Bruix J. Prognosis of hepatocellular carcinoma: the BCLC 
   staging classification. Semin Liver Dis. 1999;19(3):329-38. 
   doi: 10.1055/s-2007-1007122.
3. Cillo U, Vitale A, Grigoletto F, Farinati F, Brolese A, Zanus G, et al. 
   Prospective validation of the Barcelona Clinic Liver Cancer staging system. 
   J Hepatol. 2006 Apr;44(4):723-31. doi: 10.1016/j.jhep.2005.12.015.

The BCLC staging system is the most widely used staging classification for 
hepatocellular carcinoma (HCC) as it integrates tumor characteristics, liver 
function status, and performance status to both stage disease and guide treatment 
decisions. It classifies patients into five stages (0, A, B, C, D) with specific 
evidence-based treatment recommendations for each stage.
"""

from pydantic import BaseModel, Field, field_validator
from typing import Literal


class BclcStagingRequest(BaseModel):
    """
    Request model for Barcelona-Clinic Liver Cancer (BCLC) Staging Classification
    
    The BCLC staging system uses the following parameters to classify HCC:
    
    Performance Status:
    - Uses Eastern Cooperative Oncology Group (ECOG) scale (0-4)
    - PS 0: Fully active, able to carry on all pre-disease activities
    - PS 1: Restricted in physically strenuous activity
    - PS 2: Ambulatory and capable of all self-care
    - PS 3: Capable of only limited self-care
    - PS 4: Completely disabled, confined to bed or chair
    
    Child-Pugh Classification:
    - Class A: Well-preserved liver function (5-6 points)
    - Class B: Moderate liver dysfunction (7-9 points) 
    - Class C: Severe liver damage (10-15 points)
    
    Tumor Characteristics:
    - Size of largest tumor and number of nodules
    - Presence of portal vein invasion (macrovascular)
    - Presence of extrahepatic spread
    
    References (Vancouver style):
    1. Reig M, Forner A, Rimola J, Ferrer-Fàbrega J, Burrel M, Garcia-Criado Á, et al. 
    BCLC strategy for prognosis prediction and treatment recommendation: The 2022 
    update. J Hepatol. 2022 Mar;76(3):681-693. doi: 10.1016/j.jhep.2021.11.018.
    2. European Association for the Study of the Liver. EASL Clinical Practice 
    Guidelines: Management of hepatocellular carcinoma. J Hepatol. 2018 Jul;69(1):182-236. 
    doi: 10.1016/j.jhep.2018.03.019.
    """
    
    performance_status: Literal[0, 1, 2, 3, 4] = Field(
        ...,
        description="ECOG Performance Status: 0=Fully active, 1=Restricted in strenuous activity, 2=Ambulatory and capable of self-care, 3=Capable of limited self-care, 4=Completely disabled",
        example=0
    )
    
    child_pugh_class: Literal["A", "B", "C"] = Field(
        ...,
        description="Child-Pugh classification for liver function: A=Well-preserved (5-6 points), B=Moderate dysfunction (7-9 points), C=Severe liver damage (10-15 points)",
        example="A"
    )
    
    tumor_size: float = Field(
        ...,
        description="Size of the largest tumor in centimeters",
        gt=0,
        example=2.5
    )
    
    number_of_nodules: int = Field(
        ...,
        description="Total number of tumor nodules",
        ge=0,
        example=1
    )
    
    portal_invasion: Literal["yes", "no"] = Field(
        ...,
        description="Presence of portal vein invasion (macrovascular invasion visible on imaging)",
        example="no"
    )
    
    extrahepatic_spread: Literal["yes", "no"] = Field(
        ...,
        description="Presence of extrahepatic spread (metastases to lymph nodes or other organs)",
        example="no"
    )
    
    @field_validator('tumor_size')
    def validate_tumor_size(cls, v):
        if v <= 0:
            raise ValueError('Tumor size must be greater than 0')
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "performance_status": 0,
                "child_pugh_class": "A",
                "tumor_size": 2.5,
                "number_of_nodules": 1,
                "portal_invasion": "no",
                "extrahepatic_spread": "no"
            }
        }


class BclcStagingResponse(BaseModel):
    """
    Response model for Barcelona-Clinic Liver Cancer (BCLC) Staging Classification
    
    The BCLC stages and their treatment recommendations:
    - Stage 0 (Very Early): Single <2cm, PS 0, Child-Pugh A → Ablation
    - Stage A (Early): Single or ≤3 nodules ≤3cm, PS 0, Child-Pugh A-B → Resection/Transplant/Ablation
    - Stage B (Intermediate): Multinodular, PS 0, Child-Pugh A-B → TACE
    - Stage C (Advanced): Portal invasion/Extrahepatic spread, PS 1-2 → Systemic therapy
    - Stage D (Terminal): PS >2 or Child-Pugh C → Best supportive care
    
    Reference: Reig M, et al. J Hepatol. 2022;76(3):681-693.
    """
    
    result: str = Field(
        ...,
        description="BCLC stage (0, A, B, C, or D)",
        example="A"
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement (empty for staging)",
        example=""
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation including stage description, treatment recommendations, and prognosis",
        example="BCLC Stage A - Early Stage. Treatment recommendation: Resection, transplantation, or ablation depending on portal pressure and bilirubin. Prognosis: 5-year survival 50-70%"
    )
    
    stage: str = Field(
        ...,
        description="BCLC stage classification",
        example="Stage A"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the stage",
        example="Early Stage"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "result": "A",
                "unit": "",
                "interpretation": "BCLC Stage A - Early Stage. Treatment recommendation: Resection, transplantation, or ablation depending on portal pressure and bilirubin. Prognosis: 5-year survival 50-70%",
                "stage": "Stage A",
                "stage_description": "Early Stage"
            }
        }