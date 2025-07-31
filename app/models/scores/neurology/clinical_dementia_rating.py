"""
Clinical Dementia Rating (CDR) Scale Models

Request and response models for CDR Scale calculation.

References (Vancouver style):
1. Morris JC. The Clinical Dementia Rating (CDR): current version and scoring rules. 
   Neurology. 1993 Nov;43(11):2412-4. PMID: 8232972.
2. Hughes CP, Berg L, Danziger WL, Coben LA, Martin RL. A new clinical scale for 
   the staging of dementia. Br J Psychiatry. 1982 Jun;140:566-72. PMID: 7104545.
3. Berg L. Clinical Dementia Rating (CDR). Psychopharmacol Bull. 1988;24(4):637-9. 
   PMID: 3249765.
4. O'Bryant SE, Waring SC, Cullum CM, Hall J, Lacritz L, Massman PJ, Lupo PJ, 
   Reisch JS, Doody R; Texas Alzheimer's Research Consortium. Staging dementia 
   using Clinical Dementia Rating Scale Sum of Boxes scores: a Texas Alzheimer's 
   research consortium study. Arch Neurol. 2008 Aug;65(8):1091-5. PMID: 18695059.

The CDR Scale is a 5-point scale used to characterize six domains of cognitive and 
functional performance applicable to Alzheimer disease and related dementias. It 
provides both a global score (0-3) and a sum of boxes score (0-18).
"""

from pydantic import BaseModel, Field, field_validator
from typing import Literal, Dict, Union


class ClinicalDementiaRatingRequest(BaseModel):
    """
    Request model for Clinical Dementia Rating (CDR) Scale
    
    The CDR assesses 6 cognitive and functional domains:
    
    Scoring levels:
    - 0: No impairment
    - 0.5: Questionable/very mild impairment
    - 1: Mild impairment
    - 2: Moderate impairment
    - 3: Severe impairment
    
    Note: Personal Care domain does not have a 0.5 option
    
    Domain Descriptions:
    
    Memory (Primary Domain):
    - 0: No memory loss or slight inconsistent forgetfulness
    - 0.5: Consistent slight forgetfulness; partial recollection of events
    - 1: Moderate memory loss; more marked for recent events
    - 2: Severe memory loss; only highly learned material retained
    - 3: Severe memory loss; only fragments remain
    
    Orientation:
    - 0: Fully oriented
    - 0.5: Fully oriented except for slight difficulty with time relationships
    - 1: Moderate difficulty with time relationships; oriented for place at examination
    - 2: Severe difficulty with time relationships; usually disoriented to time, often to place
    - 3: Oriented to person only
    
    Judgment & Problem Solving:
    - 0: Solves everyday problems well; judgment good
    - 0.5: Slight impairment in solving problems, similarities, and differences
    - 1: Moderate difficulty in handling problems; social judgment usually maintained
    - 2: Severely impaired in handling problems; social judgment usually impaired
    - 3: Unable to make judgments or solve problems
    
    Community Affairs:
    - 0: Independent function at usual level in job, shopping, volunteer and social groups
    - 0.5: Slight impairment in these activities
    - 1: Unable to function independently at these activities; appears normal to casual inspection
    - 2: No pretense of independent function outside home; appears well enough to be taken to functions outside family home
    - 3: No pretense of independent function outside home; appears too ill to be taken to functions outside family home
    
    Home & Hobbies:
    - 0: Life at home, hobbies, and intellectual interests well maintained
    - 0.5: Life at home, hobbies, and intellectual interests slightly impaired
    - 1: Mild but definite impairment of function at home; more difficult chores abandoned
    - 2: Only simple chores preserved; very restricted interests, poorly maintained
    - 3: No significant function in home
    
    Personal Care:
    - 0: Fully capable of self-care
    - 1: Needs prompting
    - 2: Requires assistance in dressing, hygiene, keeping of personal effects
    - 3: Requires much help with personal care; frequent incontinence
    
    References (Vancouver style):
    1. Morris JC. The Clinical Dementia Rating (CDR): current version and scoring rules. 
    Neurology. 1993 Nov;43(11):2412-4. PMID: 8232972.
    """
    
    memory: Literal["0", "0.5", "1", "2", "3"] = Field(
        ...,
        description="Memory domain score (PRIMARY DOMAIN). 0=No loss, 0.5=Slight forgetfulness, 1=Moderate loss, 2=Severe loss, 3=Only fragments remain",
        example="0.5"
    )
    
    orientation: Literal["0", "0.5", "1", "2", "3"] = Field(
        ...,
        description="Orientation domain score. 0=Fully oriented, 0.5=Slight time difficulty, 1=Moderate time difficulty, 2=Severe time/place difficulty, 3=Person only",
        example="0.5"
    )
    
    judgment_problem_solving: Literal["0", "0.5", "1", "2", "3"] = Field(
        ...,
        description="Judgment & Problem Solving score. 0=Good judgment, 0.5=Slight impairment, 1=Moderate difficulty, 2=Severely impaired, 3=Unable",
        example="0"
    )
    
    community_affairs: Literal["0", "0.5", "1", "2", "3"] = Field(
        ...,
        description="Community Affairs score. 0=Independent, 0.5=Slight impairment, 1=Unable to function independently, 2=No pretense outside home, 3=Too ill for outside",
        example="0.5"
    )
    
    home_hobbies: Literal["0", "0.5", "1", "2", "3"] = Field(
        ...,
        description="Home & Hobbies score. 0=Well maintained, 0.5=Slightly impaired, 1=Mild impairment, 2=Simple chores only, 3=No significant function",
        example="0.5"
    )
    
    personal_care: Literal["0", "1", "2", "3"] = Field(
        ...,
        description="Personal Care score (NO 0.5 OPTION). 0=Fully capable, 1=Needs prompting, 2=Requires assistance, 3=Requires much help",
        example="0"
    )
    
    @field_validator('personal_care')
    def validate_personal_care(cls, v):
        """Ensure personal care doesn't have 0.5 value"""
        if v == "0.5":
            raise ValueError("Personal Care domain does not have a 0.5 rating option")
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "memory": "0.5",
                "orientation": "0.5",
                "judgment_problem_solving": "0",
                "community_affairs": "0.5",
                "home_hobbies": "0.5",
                "personal_care": "0"
            }
        }


class ClinicalDementiaRatingResponse(BaseModel):
    """
    Response model for Clinical Dementia Rating (CDR) Scale
    
    The CDR provides two scores:
    1. Global CDR Score (0, 0.5, 1, 2, or 3) - Derived using Washington University algorithm
    2. CDR Sum of Boxes (0-18) - Sum of all domain scores
    
    Global CDR Score interpretation:
    - 0: Normal
    - 0.5: Very Mild Dementia (questionable)
    - 1: Mild Dementia
    - 2: Moderate Dementia
    - 3: Severe Dementia
    
    CDR Sum of Boxes typical ranges:
    - CDR 0: Sum = 0
    - CDR 0.5: Sum = 0.5-4.0
    - CDR 1: Sum = 4.5-9.0
    - CDR 2: Sum = 9.5-15.5
    - CDR 3: Sum = 16.0-18.0
    
    Reference: Morris JC. Neurology. 1993;43(11):2412-4.
    """
    
    result: Dict[str, float] = Field(
        ...,
        description="Contains both global_cdr score and sum_of_boxes score",
        example={"global_cdr": 0.5, "sum_of_boxes": 2.0}
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation including both Global CDR and Sum of Boxes information",
        example="Questionable or very mild dementia. Mild consistent forgetfulness with partial recollection of events. Mild difficulty with time relationships (Sum of Boxes = 2.0, typical range for CDR 0.5: CDR-SOB: 0.5-4.0)."
    )
    
    stage: str = Field(
        ...,
        description="Global CDR stage (0, 0.5, 1, 2, or 3)",
        example="0.5"
    )
    
    stage_description: str = Field(
        ...,
        description="Description of the dementia stage",
        example="Very Mild Dementia"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "result": {
                    "global_cdr": 0.5,
                    "sum_of_boxes": 2.0
                },
                "unit": "points",
                "interpretation": "Questionable or very mild dementia. Mild consistent forgetfulness with partial recollection of events. Mild difficulty with time relationships (Sum of Boxes = 2.0, typical range for CDR 0.5: CDR-SOB: 0.5-4.0).",
                "stage": "0.5",
                "stage_description": "Very Mild Dementia"
            }
        }