"""
Fetal Biophysical Profile (BPP) Score Models

Request and response models for Fetal BPP Score calculation.

References (Vancouver style):
1. Manning FA, Platt LD, Sipos L. Antepartum fetal evaluation: development of a 
   fetal biophysical profile. Am J Obstet Gynecol. 1980 Mar 15;136(6):787-95. 
   PMID: 7369252.
2. Kim SY, Khandelwal M, Gaughan JP, Agar MH, Reece EA. Is the intrapartum 
   biophysical profile useful? Obstet Gynecol. 2003 Sep;102(3):471-6. 
   doi: 10.1016/s0029-7844(03)00570-2. PMID: 12962928.

The Fetal Biophysical Profile (BPP) is a prenatal test used to evaluate fetal 
well-being, combining ultrasound assessment of fetal movements, tone, breathing, 
and amniotic fluid volume with non-stress test (NST) results. It is particularly 
useful in high-risk pregnancies to guide decisions about timing of delivery.
"""

from pydantic import BaseModel, Field, field_validator
from typing import Literal


class FetalBppScoreRequest(BaseModel):
    """
    Request model for Fetal Biophysical Profile (BPP) Score calculation
    
    The BPP evaluates 5 parameters, each scored as 0 (abnormal) or 2 (normal):
    
    1. Fetal Breathing Movements: Assesses the presence of rhythmic breathing
       movements as an indicator of fetal neurological maturity and well-being.
       Normal: ≥1 episode lasting ≥30 seconds within 30 minutes.
    
    2. Gross Body Movements: Evaluates fetal activity level. Active fetuses are
       generally healthy, while decreased movement may indicate hypoxia.
       Normal: ≥3 discrete body or limb movements within 30 minutes.
    
    3. Fetal Tone: Assesses neuromuscular development and function. Loss of tone
       is a late sign of fetal compromise.
       Normal: ≥1 episode of active extension with return to flexion.
    
    4. Amniotic Fluid Volume: Reflects chronic uteroplacental function. 
       Oligohydramnios may indicate chronic hypoxia or placental insufficiency.
       Normal: At least one pocket ≥2 cm in two perpendicular planes.
    
    5. Non-Stress Test (NST): Evaluates fetal heart rate reactivity as an
       indicator of autonomic nervous system function.
       Normal: ≥2 accelerations of ≥15 bpm for ≥15 seconds within 20-40 minutes.
    
    Note: Each parameter scores either 0 or 2 points (no 1-point scores).
    
    References (Vancouver style):
    1. Manning FA, Platt LD, Sipos L. Antepartum fetal evaluation: development of a 
       fetal biophysical profile. Am J Obstet Gynecol. 1980 Mar 15;136(6):787-95.
    """
    
    fetal_breathing: Literal[0, 2] = Field(
        ...,
        description="Fetal breathing movements. 0: <30 sec of breathing within 30 min. 2: ≥1 episode of rhythmic breathing lasting ≥30 sec within 30 min",
        example=2
    )
    
    fetal_movement: Literal[0, 2] = Field(
        ...,
        description="Gross body movements. 0: <3 discrete movements. 2: ≥3 discrete body or limb movements within 30 min",
        example=2
    )
    
    fetal_tone: Literal[0, 2] = Field(
        ...,
        description="Fetal muscle tone. 0: 0 extension/flexion events. 2: ≥1 episode of extremity extension and subsequent return to flexion",
        example=2
    )
    
    amniotic_fluid: Literal[0, 2] = Field(
        ...,
        description="Amniotic fluid volume. 0: Largest single vertical pocket ≤2 cm. 2: A pocket of amniotic fluid ≥2 cm in 2 perpendicular planes",
        example=2
    )
    
    nonstress_test: Literal[0, 2] = Field(
        ...,
        description="Non-stress test (NST). 0: 0 or 1 acceleration within 20-40 min. 2: ≥2 accelerations of ≥15 beats/min for ≥15 sec within 20-40 min",
        example=2
    )
    
    @field_validator('fetal_breathing', 'fetal_movement', 'fetal_tone', 'amniotic_fluid', 'nonstress_test')
    def validate_scores(cls, v):
        if v not in [0, 2]:
            raise ValueError("Each BPP parameter must be scored as either 0 or 2")
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "fetal_breathing": 2,
                "fetal_movement": 2,
                "fetal_tone": 2,
                "amniotic_fluid": 2,
                "nonstress_test": 2
            }
        }


class FetalBppScoreResponse(BaseModel):
    """
    Response model for Fetal Biophysical Profile (BPP) Score calculation
    
    The BPP score ranges from 0 to 10:
    - 10: Normal fetus, no intervention needed
    - 8: Normal fetus (but check amniotic fluid status)
    - 6: Possible fetal asphyxia, requires further evaluation
    - 4: Probable fetal asphyxia, delivery often indicated
    - 0-2: Almost certain fetal asphyxia, immediate delivery indicated
    
    Special consideration for score of 8:
    - 8/10 with normal amniotic fluid: No intervention needed
    - 8/10 with oligohydramnios: May require delivery evaluation
    
    The BPP is typically performed after 28-32 weeks of pregnancy and may be
    repeated once or twice weekly in high-risk pregnancies.
    
    Reference: Manning FA, et al. Am J Obstet Gynecol. 1980;136(6):787-95.
    """
    
    result: int = Field(
        ...,
        description="BPP score (0-10 points)",
        example=10
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation and recommended management based on the BPP score",
        example="Normal, non-asphyxiated fetus. No intervention required. Repeat test weekly."
    )
    
    stage: str = Field(
        ...,
        description="Risk classification based on BPP score",
        example="Normal"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the risk category",
        example="Low risk"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "result": 10,
                "unit": "points",
                "interpretation": "Normal, non-asphyxiated fetus. No intervention required. Repeat test weekly.",
                "stage": "Normal",
                "stage_description": "Low risk"
            }
        }