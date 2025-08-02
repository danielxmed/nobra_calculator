"""
International Ovarian Tumor Analysis (IOTA) Simple Rules Risk Assessment Models

Request and response models for IOTA Simple Rules calculation.

References (Vancouver style):
1. Timmerman D, Testa AC, Bourne T, et al. Logistic regression model to distinguish 
   between the benign and malignant adnexal mass before surgery: a multicenter study 
   by the International Ovarian Tumor Analysis Group. J Clin Oncol. 2005 Dec 1;23(34):8794-801. 
   doi: 10.1200/JCO.2005.01.7632.
2. Timmerman D, Ameye L, Fischerova D, et al. Simple ultrasound rules to distinguish 
   between benign and malignant adnexal masses before surgery: prospective validation 
   study. BMJ. 2010 Dec 14;341:c6839. doi: 10.1136/bmj.c6839.
3. Nunes N, Ambler G, Foo X, et al. Use of IOTA simple rules for diagnosis of ovarian 
   cancer: meta-analysis. Ultrasound Obstet Gynecol. 2014 Nov;44(5):503-14. 
   doi: 10.1002/uog.13437.

The IOTA Simple Rules use 10 ultrasound features (5 benign B-rules and 5 malignant M-rules) 
to classify ovarian masses as benign, malignant, or inconclusive. This system achieves 
86.8% sensitivity, 95.6% specificity, and 92.3% accuracy in distinguishing benign from 
malignant ovarian tumors. Successfully classifies 76-80% of adnexal masses with high 
diagnostic performance.
"""

from pydantic import BaseModel, Field
from typing import Literal


class IotaSimpleRulesRequest(BaseModel):
    """
    Request model for International Ovarian Tumor Analysis (IOTA) Simple Rules Risk Assessment
    
    The IOTA Simple Rules evaluate 10 ultrasound features to classify adnexal masses:
    
    Benign Features (B-rules):
    - B1: Unilocular cyst - Single chamber with smooth wall
    - B2: Solid components <7mm - Small solid areas within the mass
    - B3: Acoustic shadows - Hyperechoic areas with shadowing (calcifications/fat)
    - B4: Smooth multilocular tumor <100mm - Multiple chambers, smooth walls, <10cm
    - B5: No blood flow - Absent vascularity on color Doppler (color score 1)
    
    Malignant Features (M-rules):
    - M1: Irregular solid tumor - Completely solid mass with irregular outline
    - M2: Ascites - Free fluid in the abdomen
    - M3: At least 4 papillary structures - ≥4 solid projections into cystic cavity
    - M4: Irregular multilocular solid tumor ≥100mm - Large complex mass ≥10cm
    - M5: Very strong blood flow - Intense vascularity on color Doppler (color score 4)
    
    Classification Logic:
    - If B-features present AND no M-features → Benign (low malignancy risk)
    - If M-features present AND no B-features → Malignant (high malignancy risk)
    - If both present OR neither present → Inconclusive (requires additional evaluation)
    
    Important Usage Notes:
    - For persistent adnexal masses requiring surgical consideration
    - Excludes classical masses with pathognomonic features (corpus luteum, endometrioma, dermoid)
    - Requires adequate ultrasound training and good quality equipment
    - 10-20% of masses remain inconclusive and need further evaluation
    
    References (Vancouver style):
    1. Timmerman D, Testa AC, Bourne T, et al. Logistic regression model to distinguish 
       between the benign and malignant adnexal mass before surgery: a multicenter study 
       by the International Ovarian Tumor Analysis Group. J Clin Oncol. 2005;23(34):8794-801.
    2. Timmerman D, Ameye L, Fischerova D, et al. Simple ultrasound rules to distinguish 
       between benign and malignant adnexal masses before surgery: prospective validation 
       study. BMJ. 2010;341:c6839.
    3. Nunes N, Ambler G, Foo X, et al. Use of IOTA simple rules for diagnosis of ovarian 
       cancer: meta-analysis. Ultrasound Obstet Gynecol. 2014;44(5):503-14.
    """
    
    unilocular_cyst: Literal["absent", "present"] = Field(
        ...,
        description="B1 - Unilocular cyst: Single chamber cyst with smooth wall. This is the most common benign ovarian mass appearance. Present if mass has only one chamber without internal septations or solid components.",
        example="absent"
    )
    
    solid_components_small: Literal["absent", "present"] = Field(
        ...,
        description="B2 - Solid components <7mm in largest diameter: Small solid areas within the mass measuring less than 7mm. Includes any solid tissue, debris, or thick septations within the mass.",
        example="absent"
    )
    
    acoustic_shadows: Literal["absent", "present"] = Field(
        ...,
        description="B3 - Acoustic shadows: Hyperechoic areas with posterior acoustic shadowing suggesting calcifications, hair (dermoid), or fat content. Typically seen in mature teratomas or calcified areas.",
        example="absent"
    )
    
    smooth_multilocular_small: Literal["absent", "present"] = Field(
        ...,
        description="B4 - Smooth multilocular tumor <100mm in largest diameter: Multiple chambers separated by thin septa with smooth walls, measuring less than 10cm in largest diameter. Suggests benign cystadenoma.",
        example="absent"
    )
    
    no_blood_flow: Literal["absent", "present"] = Field(
        ...,
        description="B5 - No blood flow on color Doppler (color score 1): Absence of detectable blood flow within the mass on color Doppler ultrasound. Benign masses often have minimal or no vascularity.",
        example="present"
    )
    
    irregular_solid_tumor: Literal["absent", "present"] = Field(
        ...,
        description="M1 - Irregular solid tumor: Completely or predominantly solid mass with irregular, bumpy, or lobulated outline. Highly suspicious for malignancy, especially in postmenopausal women.",
        example="absent"
    )
    
    ascites: Literal["absent", "present"] = Field(
        ...,
        description="M2 - Ascites: Free fluid in the peritoneal cavity (abdomen). Any amount of free fluid visible on ultrasound examination. Strongly associated with malignancy when present with adnexal mass.",
        example="absent"
    )
    
    papillary_structures: Literal["absent", "present"] = Field(
        ...,
        description="M3 - At least 4 papillary structures: Four or more solid projections extending into the cystic cavity from the wall or septum. These finger-like projections are highly suspicious for malignancy.",
        example="absent"
    )
    
    irregular_multilocular_large: Literal["absent", "present"] = Field(
        ...,
        description="M4 - Irregular multilocular solid tumor with largest diameter ≥100mm: Large complex mass (≥10cm) with multiple chambers, solid components, and irregular outline. Size and complexity increase malignancy risk.",
        example="absent"
    )
    
    strong_blood_flow: Literal["absent", "present"] = Field(
        ...,
        description="M5 - Very strong blood flow on color Doppler (color score 4): Intense, abundant blood flow within the mass on color Doppler. Malignant masses often show increased vascularity and angiogenesis.",
        example="absent"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "unilocular_cyst": "present",
                "solid_components_small": "absent",
                "acoustic_shadows": "absent",
                "smooth_multilocular_small": "absent",
                "no_blood_flow": "present",
                "irregular_solid_tumor": "absent",
                "ascites": "absent",
                "papillary_structures": "absent",
                "irregular_multilocular_large": "absent",
                "strong_blood_flow": "absent"
            }
        }


class IotaSimpleRulesResponse(BaseModel):
    """
    Response model for International Ovarian Tumor Analysis (IOTA) Simple Rules Risk Assessment
    
    Returns the IOTA classification with clinical interpretation:
    - Benign: One or more B-features present, no M-features (low malignancy risk)
    - Malignant: One or more M-features present, no B-features (high malignancy risk)
    - Inconclusive: Both B and M features present, or no features present (needs further evaluation)
    
    The IOTA Simple Rules successfully classify 76-80% of adnexal masses with:
    - 86.8% sensitivity for malignancy detection
    - 95.6% specificity for benign classification
    - 92.3% overall accuracy
    - High negative predictive value for benign masses
    
    Clinical Applications:
    - Preoperative risk stratification of adnexal masses
    - Guide referral decisions to gynecologic oncology
    - Reduce unnecessary oncology consultations for benign masses
    - Aid in surgical planning and patient counseling
    - Complement clinical assessment and tumor markers
    
    Limitations:
    - 10-20% of masses remain inconclusive
    - Requires experienced sonographer and quality equipment
    - Not applicable to classical masses with pathognomonic features
    - Cannot replace comprehensive clinical evaluation
    
    Reference: Timmerman D, et al. BMJ. 2010;341:c6839.
    """
    
    result: str = Field(
        ...,
        description="IOTA Simple Rules classification result",
        example="Benign"
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the classification",
        example="classification"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation and management recommendations based on IOTA classification",
        example="Low risk of malignancy. Mass classified as benign based on IOTA Simple Rules. Consider routine gynecologic follow-up. Surgery may be considered for symptomatic masses or patient preference."
    )
    
    stage: str = Field(
        ...,
        description="IOTA risk category (Benign, Malignant, Inconclusive)",
        example="Benign"
    )
    
    stage_description: str = Field(
        ...,
        description="Description of the features present for this classification",
        example="One or more B-features present, no M-features"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": "Benign",
                "unit": "classification",
                "interpretation": "Low risk of malignancy. Mass classified as benign based on IOTA Simple Rules. Consider routine gynecologic follow-up. Surgery may be considered for symptomatic masses or patient preference.",
                "stage": "Benign",
                "stage_description": "One or more B-features present, no M-features"
            }
        }