"""
Forrest Classification of Upper GI Bleeding Models

Request and response models for Forrest Classification calculation.

References (Vancouver style):
1. Forrest JA, Finlayson ND, Shearman DJ. Endoscopy in gastrointestinal bleeding. 
   Lancet. 1974;2(7877):394-7. doi: 10.1016/s0140-6736(74)91770-x.
2. Laine L, Peterson WL. Bleeding peptic ulcer. N Engl J Med. 1994;331(11):717-27. 
   doi: 10.1056/NEJM199409153311107.
3. Rockall TA, Logan RF, Devlin HB, Northfield TC. Risk assessment after acute upper 
   gastrointestinal haemorrhage. Gut. 1996;38(3):316-21. doi: 10.1136/gut.38.3.316.
4. Sung JJ, Tsoi KK, Ma TK, Yung MY, Lau JY, Chiu PW. Causes of mortality in patients 
   with peptic ulcer bleeding: a prospective cohort study of 10,428 cases. 
   Am J Gastroenterol. 2010;105(1):84-9. doi: 10.1038/ajg.2009.518.

The Forrest Classification is a widely used endoscopic classification system for upper 
gastrointestinal bleeding, specifically peptic ulcer bleeding. Developed by Dr. John A. H. 
Forrest in 1974, this classification system stratifies patients based on endoscopic findings 
to predict rebleeding risk, mortality, and guide therapeutic interventions.

The classification consists of six categories:
- Class 1A: Active spurting bleeding (highest risk)
- Class 1B: Active oozing bleeding (high risk)
- Class 2A: Non-bleeding visible vessel (high risk)
- Class 2B: Adherent clot (intermediate risk)
- Class 2C: Flat pigmented spot (low risk)
- Class 3: Clean ulcer base (lowest risk)

Clinical Application:
- Risk stratification for rebleeding and mortality
- Guidance for endoscopic therapeutic interventions
- Decision-making for discharge versus continued monitoring
- Standardized communication among healthcare providers
- Research and quality improvement initiatives

Treatment Implications:
- Classes 1A, 1B, and 2A typically require immediate endoscopic therapy
- Class 2B may require intervention depending on clinical context
- Classes 2C and 3 usually managed conservatively with medical therapy
"""

from pydantic import BaseModel, Field
from typing import Literal


class ForrestClassificationRequest(BaseModel):
    """
    Request model for Forrest Classification of Upper GI Bleeding
    
    The Forrest Classification uses endoscopic findings to categorize peptic ulcer bleeding 
    into six distinct classes based on the appearance of the ulcer during upper endoscopy.
    
    **Classification Categories:**
    
    **Active Bleeding (Class 1):**
    - **Active Spurting (Class 1A)**: Arterial spurting from ulcer base
      - Highest risk category (rebleeding 55%, mortality 11%)
      - Requires immediate endoscopic intervention
    
    - **Active Oozing (Class 1B)**: Active oozing bleeding without visible vessel
      - High risk category (rebleeding 55%, mortality 11%)
      - Requires endoscopic intervention
    
    **Recent Bleeding Stigmata (Class 2):**
    - **Non-bleeding Visible Vessel (Class 2A)**: Protuberant vessel or pigmented spot
      - High rebleeding risk (43%, mortality 11%)
      - Strong indication for endoscopic therapy
    
    - **Adherent Clot (Class 2B)**: Clot overlying ulcer base
      - Intermediate risk (rebleeding 22%, mortality 7%)
      - Consider intervention after clot removal
    
    - **Flat Pigmented Spot (Class 2C)**: Hematin on ulcer base
      - Low risk (rebleeding 10%, mortality 3%)
      - Usually managed medically
    
    **No Active or Recent Bleeding (Class 3):**
    - **Clean Ulcer Base (Class 3)**: No visible stigmata of recent hemorrhage
      - Lowest risk (rebleeding 5%, mortality 2%)
      - Medical management appropriate
    
    **Clinical Decision Making:**
    - Classes 1A, 1B, 2A: Urgent endoscopic therapy indicated
    - Class 2B: Consider intervention, controversial management
    - Classes 2C, 3: Conservative medical management usually sufficient
    
    References (Vancouver style):
    1. Forrest JA, Finlayson ND, Shearman DJ. Endoscopy in gastrointestinal bleeding. 
       Lancet. 1974;2(7877):394-7. doi: 10.1016/s0140-6736(74)91770-x.
    2. Laine L, Peterson WL. Bleeding peptic ulcer. N Engl J Med. 1994;331(11):717-27.
    3. Rockall TA, Logan RF, Devlin HB, Northfield TC. Risk assessment after acute upper 
       gastrointestinal haemorrhage. Gut. 1996;38(3):316-21.
    """
    
    endoscopic_finding: Literal[
        "active_spurting", 
        "active_oozing", 
        "nonbleeding_visible_vessel", 
        "adherent_clot", 
        "flat_pigmented_spot", 
        "clean_ulcer_base"
    ] = Field(
        ...,
        description=(
            "Endoscopic appearance of the bleeding peptic ulcer. "
            "Active spurting (Class 1A): Arterial spurting from ulcer base, highest risk. "
            "Active oozing (Class 1B): Active bleeding without visible vessel, high risk. "
            "Non-bleeding visible vessel (Class 2A): Protuberant vessel, high rebleeding risk. "
            "Adherent clot (Class 2B): Clot overlying ulcer, intermediate risk. "
            "Flat pigmented spot (Class 2C): Hematin on ulcer base, low risk. "
            "Clean ulcer base (Class 3): No stigmata of recent bleeding, lowest risk."
        ),
        example="nonbleeding_visible_vessel"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "endoscopic_finding": "nonbleeding_visible_vessel"
            }
        }


class ForrestClassificationResponse(BaseModel):
    """
    Response model for Forrest Classification of Upper GI Bleeding
    
    The Forrest Classification provides risk stratification and treatment guidance 
    based on endoscopic findings in peptic ulcer bleeding.
    
    **Risk Stratification:**
    - **Class 1A/1B**: Active bleeding, highest risk (rebleeding 55%, mortality 11%)
    - **Class 2A**: Non-bleeding vessel, high risk (rebleeding 43%, mortality 11%)
    - **Class 2B**: Adherent clot, intermediate risk (rebleeding 22%, mortality 7%)
    - **Class 2C**: Flat spot, low risk (rebleeding 10%, mortality 3%)
    - **Class 3**: Clean base, lowest risk (rebleeding 5%, mortality 2%)
    
    **Treatment Implications:**
    - **Immediate Therapy Required**: Classes 1A, 1B, 2A
    - **Consider Therapy**: Class 2B (controversial, context-dependent)
    - **Medical Management**: Classes 2C, 3
    
    **Clinical Applications:**
    - Prognostication and risk stratification
    - Endoscopic therapeutic decision-making
    - Discharge planning and monitoring decisions
    - Standardized communication among providers
    - Quality improvement and research applications
    
    Reference: Forrest JA, et al. Lancet. 1974;2(7877):394-7.
    """
    
    result: str = Field(
        ...,
        description="Forrest classification category (Class 1A, 1B, 2A, 2B, 2C, or 3) based on endoscopic findings",
        example="Class 2A"
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the classification",
        example="class"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation including risk assessment, rebleeding/mortality rates, and treatment recommendations",
        example="Non-bleeding visible vessel. High risk of rebleeding. Rebleeding risk: 43%, mortality risk: 11%. Endoscopic therapy strongly recommended to prevent rebleeding."
    )
    
    stage: str = Field(
        ...,
        description="Forrest classification stage (Class 1A, 1B, 2A, 2B, 2C, or 3)",
        example="Class 2A"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the classification category",
        example="Non-bleeding visible vessel"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": "Class 2A",
                "unit": "class",
                "interpretation": "Non-bleeding visible vessel. High risk of rebleeding. Rebleeding risk: 43%, mortality risk: 11%. Endoscopic therapy strongly recommended to prevent rebleeding.",
                "stage": "Class 2A",
                "stage_description": "Non-bleeding visible vessel"
            }
        }