"""
Wisconsin Criteria for Maxillofacial Trauma CT Models

Request and response models for Wisconsin Criteria calculation.

References (Vancouver style):
1. Koller KE, Sabatino MJ, Skalski KA, et al. Implementation of clinical decision 
   rules for emergency department patients with facial trauma. AEM Educ Train. 
   2018;2(4):269-275. doi: 10.1002/aet2.10103
2. Dreyer SJ, Wolf SJ, Mayglothling J, et al. Clinical policy: critical issues in 
   the evaluation and management of patients presenting to the emergency department 
   with acute blunt facial trauma. Ann Emerg Med. 2023;82(1):94-114. 
   doi: 10.1016/j.annemergmed.2023.03.032
3. Hopper RA, Salemy S, Sze RW. Diagnosis of midface fractures with CT: what the 
   surgeon needs to know. Radiographics. 2006;26(3):783-793. doi: 10.1148/rg.263055031
4. Hashim H, Iqbal S. Chronic pain after facial trauma. Br J Oral Maxillofac Surg. 
   2010;48(4):270-274. doi: 10.1016/j.bjoms.2009.07.024

The Wisconsin Criteria is a validated clinical decision rule that helps emergency 
physicians determine which patients with maxillofacial trauma require CT imaging. 
The rule evaluates eight high-risk criteria, and the presence of any criterion 
indicates the need for CT imaging to detect clinically significant facial fractures 
while avoiding unnecessary radiation exposure in low-risk patients.
"""

from pydantic import BaseModel, Field
from typing import Literal


class WisconsinCriteriaMaxillofacialTraumaRequest(BaseModel):
    """
    Request model for Wisconsin Criteria for Maxillofacial Trauma CT
    
    The Wisconsin Criteria evaluates eight high-risk clinical factors to determine 
    the need for CT imaging after facial trauma:
    
    High-Risk Criteria:
    1. High-energy mechanism of injury (MVCs, falls >3 feet, assault with object, sports)
    2. Visible facial deformity or asymmetry on inspection
    3. Dental malocclusion or inability to open mouth normally
    4. Facial numbness or altered sensation (especially infraorbital distribution)
    5. Significant periorbital swelling or hematoma
    6. Double vision or diplopia
    7. Palpable step-off deformity of facial bones
    8. Epistaxis (nosebleed) or nasal deformity
    
    Decision Rule:
    - ANY positive criterion = CT indicated
    - ALL negative criteria = CT not indicated
    
    Clinical Applications:
    - Reduces unnecessary radiation exposure in low-risk patients
    - High sensitivity for detecting clinically significant facial fractures
    - Validated for adult patients in emergency department settings
    - Helps standardize imaging decisions in facial trauma
    
    Important Considerations:
    - Not validated for pediatric patients or penetrating trauma
    - Does not replace clinical judgment in complex cases
    - Consider patient age, medical comorbidities, and social factors
    - High-energy mechanisms have higher fracture probability
    
    References (Vancouver style):
    1. Koller KE, Sabatino MJ, Skalski KA, et al. Implementation of clinical decision 
       rules for emergency department patients with facial trauma. AEM Educ Train. 
       2018;2(4):269-275. doi: 10.1002/aet2.10103
    2. Dreyer SJ, Wolf SJ, Mayglothling J, et al. Clinical policy: critical issues in 
       the evaluation and management of patients presenting to the emergency department 
       with acute blunt facial trauma. Ann Emerg Med. 2023;82(1):94-114. 
       doi: 10.1016/j.annemergmed.2023.03.032
    """
    
    high_energy_mechanism: Literal["yes", "no"] = Field(
        ...,
        description="High-energy mechanism of injury present (motor vehicle collision, fall >3 feet, assault with object, sports injury with significant force). High-energy mechanisms have higher probability of significant fractures",
        example="yes"
    )
    
    facial_deformity: Literal["yes", "no"] = Field(
        ...,
        description="Visible facial deformity or asymmetry on inspection. Look for obvious depression, swelling, or structural changes compared to normal facial contours",
        example="no"
    )
    
    malocclusion: Literal["yes", "no"] = Field(
        ...,
        description="Dental malocclusion or inability to open mouth normally. Ask patient to bite down and assess if teeth fit together properly. May indicate mandibular or maxillary fractures",
        example="no"
    )
    
    facial_numbness: Literal["yes", "no"] = Field(
        ...,
        description="Facial numbness or altered sensation, especially in infraorbital distribution. Test light touch sensation over cheeks, lips, and gums. Often indicates orbital floor fractures affecting infraorbital nerve",
        example="yes"
    )
    
    periorbital_swelling: Literal["yes", "no"] = Field(
        ...,
        description="Significant periorbital swelling or hematoma. Assess for marked swelling around the eyes that may indicate orbital fractures or complex facial injuries",
        example="no"
    )
    
    diplopia: Literal["yes", "no"] = Field(
        ...,
        description="Double vision or diplopia. Ask patient about seeing double images. May indicate orbital fracture with extraocular muscle entrapment or nerve injury",
        example="no"
    )
    
    palpable_step_off: Literal["yes", "no"] = Field(
        ...,
        description="Palpable step-off deformity of facial bones on examination. Feel along orbital rims, zygomatic arches, and mandible for bone discontinuity or irregularities",
        example="no"
    )
    
    epistaxis: Literal["yes", "no"] = Field(
        ...,
        description="Epistaxis (nosebleed) or visible nasal deformity. May indicate nasal fractures or nasoethmoid complex injuries, especially with significant trauma",
        example="no"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "high_energy_mechanism": "yes",
                "facial_deformity": "no",
                "malocclusion": "no", 
                "facial_numbness": "yes",
                "periorbital_swelling": "no",
                "diplopia": "no",
                "palpable_step_off": "no",
                "epistaxis": "no"
            }
        }


class WisconsinCriteriaMaxillofacialTraumaResponse(BaseModel):
    """
    Response model for Wisconsin Criteria for Maxillofacial Trauma CT
    
    The Wisconsin Criteria provides a binary recommendation for CT imaging based on 
    the presence or absence of high-risk clinical factors:
    
    CT Indicated:
    - One or more high-risk criteria present
    - Proceed with facial CT with coronal and sagittal reconstructions
    - Consider specialist consultation based on suspected injury pattern
    
    CT Not Indicated:
    - No high-risk criteria present
    - Clinical observation and symptomatic treatment appropriate
    - Consider plain radiographs only if specific clinical indication
    
    Clinical Significance:
    - High sensitivity for detecting clinically significant facial fractures
    - Reduces unnecessary radiation exposure in low-risk patients
    - Standardizes imaging decisions in emergency department
    - Complements clinical judgment rather than replacing it
    
    Follow-up Considerations:
    - High-risk patients: Close specialist follow-up within 1-2 days
    - Low-risk patients: Primary care follow-up in 1 week or PRN
    - Return precautions for worsening symptoms or new concerns
    
    Reference: Koller KE, et al. AEM Educ Train. 2018;2(4):269-275.
    """
    
    result: str = Field(
        ...,
        description="CT imaging recommendation based on Wisconsin Criteria (CT indicated or CT not indicated)",
        example="CT indicated"
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement (not applicable for this decision rule)",
        example=""
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation with management recommendations based on criteria assessment",
        example="One or more high-risk criteria present: High-energy mechanism of injury, Facial numbness or altered sensation. According to the Wisconsin Criteria, CT imaging is indicated to evaluate for significant facial fractures."
    )
    
    stage: str = Field(
        ...,
        description="Risk category (Low Risk or High Risk) based on presence of criteria",
        example="High Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the risk category and imaging recommendation",
        example="CT indicated"
    )
    
    positive_criteria_count: int = Field(
        ...,
        description="Number of positive high-risk criteria identified (0-8)",
        example=2
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": "CT indicated",
                "unit": "",
                "interpretation": "One or more high-risk criteria present: High-energy mechanism of injury, Facial numbness or altered sensation. According to the Wisconsin Criteria, CT imaging is indicated to evaluate for significant facial fractures. Proceed with facial CT with coronal and sagittal reconstructions.",
                "stage": "High Risk",
                "stage_description": "CT indicated",
                "positive_criteria_count": 2
            }
        }