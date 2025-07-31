"""
Focused Assessment with Sonography for Trauma (FAST) Models

Request and response models for FAST calculation.

References (Vancouver style):
1. Rozycki GS, Ochsner MG, Jaffin JH, Champion HR. Prospective evaluation 
   of surgeons' use of ultrasound in the evaluation of trauma patients. 
   J Trauma. 1993 Apr;34(4):516-26; discussion 526-7.
2. Rozycki GS, Ballard RB, Feliciano DV, Schmidt JA, Pennington SD. 
   Surgeon-performed ultrasound for the assessment of truncal injuries: 
   lessons learned from 1540 patients. Ann Surg. 1998 Oct;228(4):557-67.
3. Rozycki GS, Ochsner MG, Schmidt JA, Frankel HL, Davis TP, Wang D, et al. 
   A prospective study of surgeon-performed ultrasound as the primary 
   adjuvant modality for injured patient assessment. J Trauma. 1995 Sep;
   39(3):492-8; discussion 498-500.
4. American College of Emergency Physicians. Emergency ultrasound guidelines. 
   Ann Emerg Med. 2009 Apr;53(4):550-70.

FAST is a bedside ultrasound protocol used to rapidly identify free fluid 
(blood) in the peritoneal, pericardial, and pleural spaces in trauma patients. 
It evaluates four anatomical windows: pericardial, perihepatic (Morison's pouch), 
perisplenic, and pelvic. While highly specific, FAST has variable sensitivity 
and should not be used alone to exclude injury.
"""

from pydantic import BaseModel, Field
from typing import Literal


class FastRequest(BaseModel):
    """
    Request model for Focused Assessment with Sonography for Trauma (FAST)
    
    FAST evaluates four anatomical regions for free fluid:
    
    1. Pericardial view: 
       - Subxiphoid or parasternal view to assess for pericardial effusion
       - Highest priority as cardiac tamponade requires immediate intervention
    
    2. Right upper quadrant (Morison's pouch):
       - Interface between liver and right kidney
       - Most dependent portion of upper peritoneum when supine
    
    3. Left upper quadrant (splenorenal recess):
       - Interface between spleen and left kidney
       - Evaluates for perisplenic fluid
    
    4. Suprapubic/pelvic view:
       - Retrovesical or rectouterine pouch
       - Most dependent portion of peritoneum
    
    Patient stability is crucial for management decisions:
    - Unstable patients with positive FAST → immediate surgery
    - Stable patients with positive FAST → CT for further evaluation
    
    Limitations:
    - Does not detect retroperitoneal hemorrhage
    - Cannot quantify amount of free fluid
    - Poor sensitivity for solid organ injury without free fluid
    - User-dependent with variable sensitivity (22-98%)
    """
    
    pericardial_fluid: Literal["absent", "present", "equivocal"] = Field(
        ...,
        description=("Presence of pericardial fluid on ultrasound. "
                    "'Absent' = no fluid visualized, "
                    "'Present' = clear fluid collection in pericardial space, "
                    "'Equivocal' = uncertain findings requiring repeat exam or additional imaging"),
        example="absent"
    )
    
    right_upper_quadrant_fluid: Literal["absent", "present", "equivocal"] = Field(
        ...,
        description=("Presence of fluid in right upper quadrant (Morison's pouch) on ultrasound. "
                    "Morison's pouch is the hepatorenal recess between liver and right kidney. "
                    "'Absent' = no fluid, 'Present' = anechoic stripe between liver and kidney, "
                    "'Equivocal' = uncertain findings"),
        example="absent"
    )
    
    left_upper_quadrant_fluid: Literal["absent", "present", "equivocal"] = Field(
        ...,
        description=("Presence of fluid in left upper quadrant (splenorenal recess) on ultrasound. "
                    "Evaluates interface between spleen and left kidney. "
                    "'Absent' = no fluid, 'Present' = anechoic collection in splenorenal recess, "
                    "'Equivocal' = uncertain findings"),
        example="absent"
    )
    
    suprapubic_fluid: Literal["absent", "present", "equivocal"] = Field(
        ...,
        description=("Presence of suprapubic/pelvic fluid on ultrasound. "
                    "Evaluates retrovesical pouch (males) or rectouterine pouch (females). "
                    "'Absent' = no fluid, 'Present' = fluid posterior to bladder, "
                    "'Equivocal' = uncertain findings"),
        example="absent"
    )
    
    patient_stability: Literal["stable", "unstable"] = Field(
        ...,
        description=("Hemodynamic stability of the patient. "
                    "'Stable' = normal vital signs without need for vasopressor support, "
                    "'Unstable' = hypotension (SBP <90), tachycardia, altered mental status, "
                    "or signs of shock requiring resuscitation"),
        example="stable"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "pericardial_fluid": "absent",
                "right_upper_quadrant_fluid": "present",
                "left_upper_quadrant_fluid": "absent",
                "suprapubic_fluid": "absent",
                "patient_stability": "stable"
            }
        }


class FastResponse(BaseModel):
    """
    Response model for Focused Assessment with Sonography for Trauma (FAST)
    
    FAST results guide trauma management:
    - Pericardial fluid → immediate surgical intervention
    - Abdominal fluid + unstable → emergent laparotomy
    - Abdominal fluid + stable → CT scan for further evaluation
    - Negative FAST → does not exclude injury; clinical correlation required
    - Equivocal → repeat exam or proceed to CT
    
    Extended FAST (eFAST) adds thoracic views for pneumothorax/hemothorax.
    
    References:
    1. Rozycki GS, et al. J Trauma. 1993;34(4):516-26.
    2. Rozycki GS, et al. Ann Surg. 1998;228(4):557-67.
    """
    
    result: str = Field(
        ...,
        description="FAST examination result describing findings and patient status",
        example="Positive FAST - Intra-abdominal fluid (stable patient)"
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement (not applicable for FAST)",
        example=""
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation and recommended management based on FAST findings",
        example=("Intra-abdominal fluid detected in hemodynamically stable patient. "
                "Cross-sectional imaging (CT scan) is recommended for further evaluation.")
    )
    
    stage: str = Field(
        ...,
        description="FAST result classification",
        example="Positive FAST - Abdominal (Stable)"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of FAST findings",
        example="Intra-abdominal fluid with hemodynamic stability"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": "Positive FAST - Intra-abdominal fluid (stable patient)",
                "unit": "",
                "interpretation": ("Intra-abdominal fluid detected in hemodynamically stable "
                                 "patient. Cross-sectional imaging (CT scan) is recommended "
                                 "for further evaluation. Consider contrast-enhanced CT of "
                                 "abdomen/pelvis to identify source and grade of injury."),
                "stage": "Positive FAST - Abdominal (Stable)",
                "stage_description": "Intra-abdominal fluid with hemodynamic stability"
            }
        }