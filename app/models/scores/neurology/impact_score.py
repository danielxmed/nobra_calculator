"""
IMPACT Score for Outcomes in Head Injury Models

Request and response models for IMPACT Score calculation.

References (Vancouver style):
1. Steyerberg EW, Mushkudiani N, Perel P, et al. Predicting outcome after traumatic 
   brain injury: development and international validation of prognostic scores based 
   on admission characteristics. PLoS Med. 2008 Aug 5;5(8):e165. 
   doi: 10.1371/journal.pmed.0050165.
2. Lingsma HF, Roozenbeek B, Steyerberg EW, et al. Early prognosis in traumatic 
   brain injury: from prophecies to predictions. Lancet Neurol. 2010 May;9(5):543-54. 
   doi: 10.1016/S1474-4422(10)70065-X.
3. Roozenbeek B, Lingsma HF, Lecky FE, et al. Prediction of outcome after moderate 
   and severe traumatic brain injury: external validation of the International Mission 
   on Prognosis and Analysis of Clinical Trials (IMPACT) and Corticoid Randomisation 
   After Significant Head injury (CRASH) prognostic models. Crit Care Med. 2012 
   May;40(5):1609-17. doi: 10.1097/CCM.0b013e31824519ce.
4. Raj R, Siironen J, Skrifvars MB, et al. Predicting outcome in traumatic brain 
   injury: development of a novel computerized tomography classification system 
   (Helsinki computerized tomography score). Neurosurgery. 2014 Dec;75(6):632-46. 
   doi: 10.1227/NEU.0000000000000533.

The IMPACT Score is a validated prognostic tool that predicts 6-month mortality and 
unfavorable outcomes in patients with moderate to severe traumatic brain injury (TBI). 
The International Mission on Prognosis and Analysis of Clinical Trials developed 
three progressive models from 8,509 TBI patients: Core (clinical variables only), 
Extended (adds CT findings), and Lab (adds laboratory values). This evidence-based 
tool assists clinicians in prognosis counseling, treatment planning, and family 
discussions for severe TBI patients with GCS ≤12.
"""

from pydantic import BaseModel, Field
from typing import Literal, Optional, Dict


class ImpactScoreResult(BaseModel):
    """
    Result component for IMPACT Score containing mortality and unfavorable outcome probabilities
    """
    
    mortality_probability: float = Field(
        ...,
        description="6-month mortality probability as percentage",
        example=25.5,
        ge=0.0,
        le=100.0
    )
    
    unfavorable_outcome_probability: float = Field(
        ...,
        description="6-month unfavorable outcome probability as percentage (death, persistent vegetative state, severe disability)",
        example=42.3,
        ge=0.0,
        le=100.0
    )
    
    model_used: str = Field(
        ...,
        description="IMPACT model variant used for calculation (CORE, EXTENDED, or LAB)",
        example="EXTENDED"
    )


class ImpactScoreRequest(BaseModel):
    """
    Request model for IMPACT Score for Outcomes in Head Injury
    
    Predicts 6-month mortality and unfavorable outcomes after moderate to severe 
    traumatic brain injury (TBI) using validated prognostic models.
    
    Model Types:
    - Core: Uses only clinical variables (age, motor score, pupillary reactivity)
    - Extended: Adds CT findings and secondary injury factors
    - Lab: Adds laboratory values for maximum accuracy
    
    Clinical Variables:
    - Age: Strong predictor, worse outcomes with increasing age
    - Motor Score: Best motor response from Glasgow Coma Scale (6=obeys commands to 1=none)
    - Pupillary Reactivity: Both reactive (best) to both non-reactive (worst)
    - Secondary Injury: Hypoxia and hypotension worsen prognosis significantly
    - CT Findings: Marshall classification grades injury severity from CT
    - Laboratory: Glucose (hyperglycemia worsens outcome) and hemoglobin (anemia)
    
    Patient Selection Criteria:
    - Age ≥14 years
    - Glasgow Coma Scale ≤12 (moderate to severe TBI)
    - Evaluated within first 24 hours of admission
    
    Unfavorable outcome is defined as death, persistent vegetative state, 
    or severe disability at 6 months post-injury.

    References (Vancouver style):
    1. Steyerberg EW, Mushkudiani N, Perel P, et al. Predicting outcome after traumatic 
       brain injury: development and international validation of prognostic scores based 
       on admission characteristics. PLoS Med. 2008 Aug 5;5(8):e165. 
       doi: 10.1371/journal.pmed.0050165.
    2. Lingsma HF, Roozenbeek B, Steyerberg EW, et al. Early prognosis in traumatic 
       brain injury: from prophecies to predictions. Lancet Neurol. 2010 May;9(5):543-54. 
       doi: 10.1016/S1474-4422(10)70065-X.
    3. Roozenbeek B, Lingsma HF, Lecky FE, et al. Prediction of outcome after moderate 
       and severe traumatic brain injury: external validation of the International Mission 
       on Prognosis and Analysis of Clinical Trials (IMPACT) and Corticoid Randomisation 
       After Significant Head injury (CRASH) prognostic models. Crit Care Med. 2012 
       May;40(5):1609-17. doi: 10.1097/CCM.0b013e31824519ce.
    """
    
    age: int = Field(
        ...,
        description="Patient age in years. Age is a strong predictor of outcome in TBI, with older patients having worse prognosis. Used in all IMPACT model variants",
        example=45,
        ge=14,
        le=100
    )
    
    motor_score: Literal[
        "obeys_commands", 
        "localizes_pain", 
        "withdraws_from_pain", 
        "abnormal_flexion", 
        "abnormal_extension", 
        "no_motor_response"
    ] = Field(
        ...,
        description="Best motor response component of Glasgow Coma Scale. Reflects level of consciousness and neurological function. Key predictor in all IMPACT models. Scale: 6=obeys commands (best), 5=localizes pain, 4=withdraws from pain, 3=abnormal flexion, 2=abnormal extension, 1=no motor response (worst)",
        example="localizes_pain"
    )
    
    pupillary_reactivity: Literal["both_reactive", "one_reactive", "both_nonreactive"] = Field(
        ...,
        description="Pupillary light reflex response. Both pupils reactive indicates better prognosis. One or both non-reactive pupils suggest brainstem dysfunction and worse outcome",
        example="both_reactive"
    )
    
    model_type: Literal["core", "extended", "lab"] = Field(
        ...,
        description="IMPACT model variant to use. Core uses basic clinical variables only. Extended adds CT findings and secondary injury factors. Lab adds laboratory values for maximum accuracy",
        example="extended"
    )
    
    hypoxia: Optional[Literal["yes", "no"]] = Field(
        None,
        description="History of hypoxia (SpO2 <90% or PaO2 <60 mmHg) before or at admission. Secondary brain injury factor that worsens prognosis. Required for Extended and Lab models",
        example="no"
    )
    
    hypotension: Optional[Literal["yes", "no"]] = Field(
        None,
        description="History of hypotension (systolic BP <90 mmHg) before or at admission. Secondary brain injury factor that significantly worsens outcome. Required for Extended and Lab models",
        example="no"
    )
    
    marshall_ct_classification: Optional[Literal[
        "diffuse_injury_i", 
        "diffuse_injury_ii", 
        "diffuse_injury_iii", 
        "diffuse_injury_iv", 
        "evacuated_mass_lesion", 
        "non_evacuated_mass_lesion"
    ]] = Field(
        None,
        description="Marshall CT classification for traumatic brain injury. Grades severity of brain injury based on initial head CT findings. Higher grades indicate worse prognosis. I=normal CT, II=diffuse injury <5mm midline shift, III=diffuse injury 5-25mm shift, IV=diffuse injury >25mm shift, V=evacuated mass lesion, VI=non-evacuated mass lesion >25cc. Required for Extended and Lab models",
        example="diffuse_injury_ii"
    )
    
    traumatic_sah: Optional[Literal["yes", "no"]] = Field(
        None,
        description="Presence of traumatic subarachnoid hemorrhage on initial head CT. Indicates more severe brain injury and worse prognosis. Required for Extended and Lab models",
        example="no"
    )
    
    epidural_hematoma: Optional[Literal["yes", "no"]] = Field(
        None,
        description="Presence of epidural hematoma on initial head CT. Mass lesion that may require surgical evacuation. Paradoxically may have better prognosis if evacuated promptly. Required for Extended and Lab models",
        example="no"
    )
    
    glucose: Optional[float] = Field(
        None,
        description="Initial glucose level in mg/dL. Hyperglycemia is associated with worse outcomes in TBI through secondary brain injury mechanisms. Required for Lab model only",
        example=120.0,
        ge=50.0,
        le=800.0
    )
    
    hemoglobin: Optional[float] = Field(
        None,
        description="Initial hemoglobin level in g/dL. Anemia may worsen cerebral oxygen delivery and outcome. Required for Lab model only",
        example=12.5,
        ge=5.0,
        le=20.0
    )
    
    class Config:
        schema_extra = {
            "example": {
                "age": 45,
                "motor_score": "localizes_pain",
                "pupillary_reactivity": "both_reactive",
                "model_type": "extended",
                "hypoxia": "no",
                "hypotension": "no",
                "marshall_ct_classification": "diffuse_injury_ii",
                "traumatic_sah": "no",
                "epidural_hematoma": "no"
            }
        }


class ImpactScoreResponse(BaseModel):
    """
    Response model for IMPACT Score for Outcomes in Head Injury
    
    Returns probabilities for 6-month mortality and unfavorable outcomes in patients 
    with moderate to severe traumatic brain injury. The IMPACT models provide 
    evidence-based prognosis to assist clinicians in treatment planning and family 
    counseling.
    
    Risk Categories:
    - Very Low Risk: <10% mortality - Excellent prognosis, aggressive treatment indicated
    - Low Risk: 10-25% mortality - Good prognosis, majority achieve functional independence
    - Moderate Risk: 25-50% mortality - Significant risk, family discussion needed
    - High Risk: 50-75% mortality - Poor prognosis, careful family consultation required
    - Very High Risk: >75% mortality - Very poor prognosis, consider comfort care
    
    Unfavorable outcome includes death, persistent vegetative state, or severe 
    disability at 6 months post-injury.
    
    Reference: Steyerberg EW, et al. PLoS Med. 2008;5(8):e165.
    """
    
    result: ImpactScoreResult = Field(
        ...,
        description="IMPACT Score results containing mortality and unfavorable outcome probabilities with model type used"
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for probabilities",
        example="percentage"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation and prognostic guidance based on calculated probabilities",
        example="Moderate prognosis. Significant risk of death or severe disability. Treatment decisions should involve family discussion. Variable functional outcomes expected."
    )
    
    stage: str = Field(
        ...,
        description="Risk category based on mortality probability (Very Low Risk, Low Risk, Moderate Risk, High Risk, Very High Risk)",
        example="Moderate Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the risk category with specific probability ranges",
        example="Mortality 25.5%, Unfavorable outcome 42.3%"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": {
                    "mortality_probability": 25.5,
                    "unfavorable_outcome_probability": 42.3,
                    "model_used": "EXTENDED"
                },
                "unit": "percentage",
                "interpretation": "Moderate prognosis. Significant risk of death or severe disability. Treatment decisions should involve family discussion. Variable functional outcomes expected.",
                "stage": "Moderate Risk",
                "stage_description": "Mortality 25.5%, Unfavorable outcome 42.3%"
            }
        }