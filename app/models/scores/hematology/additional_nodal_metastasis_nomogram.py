"""
Additional Nodal Metastasis Nomogram Models

Request and response models for Additional Nodal Metastasis Nomogram calculation.

References (Vancouver style):
1. Van Zee KJ, Manasseh DM, Bevilacqua JL, Boolbol SK, Fey JV, Tan LK, Borgen PI, 
   Cody HS 3rd, Kattan MW. A nomogram for predicting the likelihood of additional 
   nodal metastases in breast cancer patients with a positive sentinel node biopsy. 
   Ann Surg Oncol. 2003 Dec;10(10):1140-51. doi: 10.1245/ASO.2003.03.018.
2. Specht MC, Kattan MW, Gonen M, Fey J, Van Zee KJ. Predicting nonsentinel node 
   status after positive sentinel lymph biopsy for breast cancer: clinicians versus 
   nomogram. Ann Surg Oncol. 2005 Aug;12(8):654-9. doi: 10.1245/ASO.2005.08.019.

The Additional Nodal Metastasis Nomogram is a clinical decision tool developed at 
Memorial Sloan Kettering Cancer Center to predict the probability of additional 
non-sentinel lymph node metastases in breast cancer patients with a positive 
sentinel lymph node biopsy. This tool helps surgeons and patients make informed 
decisions about the need for completion axillary lymph node dissection.
"""

from pydantic import BaseModel, Field
from typing import Literal


class AdditionalNodalMetastasisNomogramRequest(BaseModel):
    """
    Request model for Additional Nodal Metastasis Nomogram
    
    This nomogram uses 8 clinical and pathological variables to predict the 
    probability of additional non-sentinel lymph node metastases in breast cancer 
    patients with a positive sentinel lymph node biopsy:
    
    Tumor Characteristics:
    - Nuclear grade and histologic type (ductal I, II, III or lobular)
    - Pathologic tumor size in centimeters
    - Lymphovascular invasion (LVI) presence
    - Multifocal disease (tumor in multiple breast locations)
    - Estrogen receptor (ER) status
    
    Sentinel Lymph Node Information:
    - Number of negative sentinel lymph nodes removed
    - Number of positive sentinel lymph nodes
    - Method used to detect sentinel lymph node metastases
    
    The nomogram provides a probability percentage that can guide clinical 
    decision-making regarding the need for completion axillary lymph node 
    dissection versus observation or axillary radiation therapy.

    References (Vancouver style):
    1. Van Zee KJ, Manasseh DM, Bevilacqua JL, Boolbol SK, Fey JV, Tan LK, Borgen PI, 
    Cody HS 3rd, Kattan MW. A nomogram for predicting the likelihood of additional 
    nodal metastases in breast cancer patients with a positive sentinel node biopsy. 
    Ann Surg Oncol. 2003 Dec;10(10):1140-51. doi: 10.1245/ASO.2003.03.018.
    2. Specht MC, Kattan MW, Gonen M, Fey J, Van Zee KJ. Predicting nonsentinel node 
    status after positive sentinel lymph biopsy for breast cancer: clinicians versus 
    nomogram. Ann Surg Oncol. 2005 Aug;12(8):654-9. doi: 10.1245/ASO.2005.08.019.
    """
    
    nuclear_grade: Literal["ductal_i", "ductal_ii", "ductal_iii", "lobular"] = Field(
        ...,
        description="Nuclear grade and histologic type. Ductal I: minimal nuclear pleomorphism, Ductal II: moderate nuclear pleomorphism, Ductal III: marked nuclear pleomorphism, Lobular: invasive lobular carcinoma",
        example="ductal_ii"
    )
    
    lymphovascular_invasion: Literal["no", "yes"] = Field(
        ...,
        description="Presence of lymphovascular invasion (LVI). Tumor cells present in blood vessels or lymphatic structures on pathological examination",
        example="no"
    )
    
    multifocal: Literal["no", "yes"] = Field(
        ...,
        description="Multifocal disease. Tumor present in multiple separate locations within the same breast",
        example="no"
    )
    
    estrogen_receptor_status: Literal["negative", "positive"] = Field(
        ...,
        description="Estrogen receptor (ER) status by immunohistochemistry. Positive typically defined as ≥1% nuclear staining",
        example="positive"
    )
    
    negative_slns: int = Field(
        ...,
        ge=0,
        le=14,
        description="Number of sentinel lymph nodes that were negative for metastases on pathological examination (range: 0-14)",
        example=2
    )
    
    positive_slns: int = Field(
        ...,
        ge=1,
        le=7,
        description="Number of sentinel lymph nodes that were positive for metastases on pathological examination (range: 1-7, must be ≥1 for this nomogram)",
        example=1
    )
    
    pathologic_size: float = Field(
        ...,
        ge=0.0,
        le=9.0,
        description="Pathologic size of the primary tumor in centimeters based on final surgical pathology (range: 0-9 cm)",
        example=2.1
    )
    
    detection_method: Literal["ihc", "serial_he", "routine", "frozen"] = Field(
        ...,
        description="Method used to detect sentinel lymph node metastases. IHC: immunohistochemistry, Serial H&E: serial hematoxylin and eosin sections, Routine: routine H&E, Frozen: frozen section analysis",
        example="routine"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "nuclear_grade": "ductal_ii",
                "lymphovascular_invasion": "no",
                "multifocal": "no", 
                "estrogen_receptor_status": "positive",
                "negative_slns": 2,
                "positive_slns": 1,
                "pathologic_size": 2.1,
                "detection_method": "routine"
            }
        }


class AdditionalNodalMetastasisNomogramResponse(BaseModel):
    """
    Response model for Additional Nodal Metastasis Nomogram
    
    The nomogram provides a probability percentage for additional non-sentinel 
    lymph node metastases, along with risk stratification:
    
    - Very Low Risk (<10%): Consider omitting completion ALND
    - Low Risk (10-20%): Clinical decision incorporating patient factors
    - Moderate Risk (20-50%): Consider completion ALND or axillary RT
    - High Risk (>50%): Strong consideration for completion ALND or axillary RT
    
    Reference: Van Zee KJ, et al. Ann Surg Oncol. 2003;10(10):1140-51.
    """
    
    result: float = Field(
        ...,
        ge=0.0,
        le=100.0,
        description="Probability of additional non-sentinel lymph node metastases (percentage, range: 0-100%)",
        example=25.7
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the probability",
        example="%"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation and management recommendations based on the calculated probability",
        example="Moderate probability (20-50%) of additional non-sentinel lymph node metastases. Consider completion axillary lymph node dissection or axillary radiation therapy."
    )
    
    stage: str = Field(
        ...,
        description="Risk category based on probability (Very Low Risk, Low Risk, Moderate Risk, High Risk)",
        example="Moderate Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the risk category",
        example="Moderate probability"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "result": 25.7,
                "unit": "%",
                "interpretation": "Moderate probability (20-50%) of additional non-sentinel lymph node metastases. Consider completion axillary lymph node dissection or axillary radiation therapy.",
                "stage": "Moderate Risk",
                "stage_description": "Moderate probability"
            }
        }