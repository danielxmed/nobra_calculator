"""
Expanded Disability Status Scale (EDSS) / Functional Systems Score (FSS) Models

Request and response models for EDSS calculation.

References (Vancouver style):
1. Kurtzke JF. Rating neurologic impairment in multiple sclerosis: an expanded 
   disability status scale (EDSS). Neurology. 1983 Nov;33(11):1444-52.
2. Slater RJ, LaRocca NG, Scheinberg LC. Development and testing of a minimal 
   record of disability in multiple sclerosis. Ann N Y Acad Sci. 1984;436:453-68.
3. Fouad AM, Abdel Naseer M, Farghaly M, Hegazy MI. New algorithmic approach for 
   easier and faster extended disability status scale calculation. Mult Scler J Exp 
   Transl Clin. 2023 Feb 9;9(1):20552173231155055.

The EDSS is the most widely used method of quantifying disability in multiple sclerosis.
It is based on a neurological examination by a clinician and ranges from 0 (normal 
neurological exam) to 10 (death due to MS) in 0.5 unit increments. The scale combines
functional systems (FS) scores with ambulation assessment to provide a comprehensive 
disability rating.
"""

from pydantic import BaseModel, Field, field_validator
from typing import Literal


class EdssRequest(BaseModel):
    """
    Request model for Expanded Disability Status Scale (EDSS) / Functional Systems Score (FSS)
    
    The EDSS requires assessment of 7 functional systems plus ambulation status:
    
    Functional Systems (FS):
    - Pyramidal: Motor function and strength (0-6)
    - Cerebellar: Coordination and balance (0-5)
    - Brainstem: Eye movements, speech, swallowing (0-5)
    - Sensory: Touch, pain, temperature sensation (0-6)
    - Bowel/Bladder: Bowel and bladder control (0-6)
    - Visual: Visual acuity and fields (0-6)
    - Cerebral: Mental and mood functions (0-5)
    
    Ambulation: Walking ability and assistance needed (0-10)
    
    Special Notes:
    - Visual scores 5-6 are converted to 4 for EDSS calculation
    - Bowel/bladder score 6 is converted to 5 for EDSS calculation
    - EDSS 0-4.5 is based primarily on FS scores
    - EDSS 5.0-9.5 is based primarily on ambulation
    - Exception: Five FS scores of 2 results in EDSS 5.0
    
    References (Vancouver style):
    1. Kurtzke JF. Rating neurologic impairment in multiple sclerosis: an expanded 
       disability status scale (EDSS). Neurology. 1983 Nov;33(11):1444-52.
    2. Slater RJ, LaRocca NG, Scheinberg LC. Development and testing of a minimal 
       record of disability in multiple sclerosis. Ann N Y Acad Sci. 1984;436:453-68.
    """
    
    pyramidal: int = Field(
        ...,
        ge=0,
        le=6,
        description="Pyramidal Functions score (Motor/Strength). 0=Normal, 1=Abnormal signs without disability, 2=Minimal disability, 3=Mild to moderate paraparesis or hemiparesis, 4=Marked paraparesis or hemiparesis, 5=Paraplegia/hemiplegia/marked quadriparesis, 6=Quadriplegia",
        example=2
    )
    
    cerebellar: int = Field(
        ...,
        ge=0,
        le=5,
        description="Cerebellar Functions score (Coordination/Balance). 0=Normal, 1=Abnormal signs without disability, 2=Mild ataxia, 3=Moderate truncal or limb ataxia, 4=Severe ataxia all limbs, 5=Unable to perform coordinated movements due to ataxia",
        example=1
    )
    
    brainstem: int = Field(
        ...,
        ge=0,
        le=5,
        description="Brainstem Functions score (Eye movements, Speech, Swallowing). 0=Normal, 1=Signs only, 2=Moderate nystagmus or other mild disability, 3=Severe nystagmus/marked weakness/moderate disability, 4=Marked dysarthria or other marked disability, 5=Inability to swallow or speak",
        example=0
    )
    
    sensory: int = Field(
        ...,
        ge=0,
        le=6,
        description="Sensory Functions score (Touch, Pain, Temperature). 0=Normal, 1=Vibration or figure-writing decrease only, 2=Mild decrease touch/pain/position sense, 3=Moderate decrease touch/pain/position sense, 4=Marked decrease touch/pain or loss of proprioception, 5=Loss of sensation one or two limbs, 6=Sensation essentially lost below the head",
        example=1
    )
    
    bowel_bladder: int = Field(
        ...,
        ge=0,
        le=6,
        description="Bowel and Bladder Functions score. 0=Normal, 1=Mild urinary hesitancy/urgency/retention, 2=Moderate hesitancy/urgency/retention or rare incontinence, 3=Frequent urinary incontinence, 4=In need of almost constant catheterization, 5=Loss of bladder function, 6=Loss of bowel and bladder function",
        example=0
    )
    
    visual: int = Field(
        ...,
        ge=0,
        le=6,
        description="Visual Functions score. 0=Normal, 1=Scotoma with visual acuity >20/30, 2=Worse eye with scotoma and acuity 20/30-20/59, 3=Worse eye with large scotoma or acuity 20/60-20/99, 4=Worse eye with marked visual field decrease and acuity 20/100-20/200, 5=Worse eye with acuity <20/200 or grade 4 plus better eye ≤20/60, 6=Grade 5 plus better eye with acuity ≤20/60",
        example=0
    )
    
    cerebral: int = Field(
        ...,
        ge=0,
        le=5,
        description="Cerebral/Mental Functions score. 0=Normal, 1=Mood alteration only, 2=Mild decrease in mentation, 3=Moderate decrease in mentation, 4=Marked decrease in mentation, 5=Dementia or chronic brain syndrome",
        example=0
    )
    
    ambulation: int = Field(
        ...,
        ge=0,
        le=10,
        description="Ambulation score based on walking ability. 0=Fully ambulatory, 1=Fully ambulatory but fatigue limits, 2=Can walk 500m without aid, 3=Can walk 300m without aid, 4=Can walk 200m without aid, 5=Can walk 100m without aid, 6=Unilateral assistance to walk 100m, 7=Cannot walk 5m even with aid/restricted to wheelchair, 8=Restricted to bed/chair, 9=Helpless bed patient, 10=Death due to MS",
        example=2
    )
    
    @field_validator('pyramidal', 'cerebellar', 'brainstem', 'sensory', 'bowel_bladder', 'visual', 'cerebral', 'ambulation')
    def validate_integer_type(cls, v, info):
        if not isinstance(v, int):
            raise ValueError(f"{info.field_name} must be an integer")
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "pyramidal": 2,
                "cerebellar": 1,
                "brainstem": 0,
                "sensory": 1,
                "bowel_bladder": 0,
                "visual": 0,
                "cerebral": 0,
                "ambulation": 2
            }
        }


class EdssResponse(BaseModel):
    """
    Response model for Expanded Disability Status Scale (EDSS) / Functional Systems Score (FSS)
    
    The EDSS score ranges from 0 to 10 in 0.5 unit increments:
    - 0: Normal neurological exam
    - 1.0-1.5: No disability, minimal signs
    - 2.0-2.5: Minimal disability
    - 3.0-3.5: Moderate disability but fully ambulatory
    - 4.0-4.5: Relatively severe disability but ambulatory for 500m without aid
    - 5.0-5.5: Disability severe enough to impair full daily activities
    - 6.0-6.5: Requires unilateral assistance to walk 100m
    - 7.0-7.5: Unable to walk beyond 5m, restricted to wheelchair
    - 8.0-8.5: Restricted to bed or chair
    - 9.0-9.5: Helpless bed patient
    - 10: Death due to MS
    
    Reference: Kurtzke JF. Neurology. 1983;33(11):1444-52.
    """
    
    result: float = Field(
        ...,
        description="EDSS score from 0 (normal) to 10 (death due to MS) in 0.5 unit increments",
        example=2.5
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation of the EDSS score and functional impact",
        example="Minimal disability in one functional system."
    )
    
    stage: str = Field(
        ...,
        description="Disability stage classification",
        example="Mild Disability"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the disability stage",
        example="Minimal disability in one FS"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "result": 2.5,
                "unit": "points",
                "interpretation": "Minimal disability in one functional system.",
                "stage": "Mild Disability",
                "stage_description": "Minimal disability in one FS"
            }
        }