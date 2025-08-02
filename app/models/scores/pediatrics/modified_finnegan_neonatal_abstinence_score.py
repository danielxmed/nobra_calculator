"""
Modified Finnegan Neonatal Abstinence Score (NAS) Models

Request and response models for Modified Finnegan NAS assessment of neonatal opioid withdrawal.

References (Vancouver style):
1. Finnegan LP, Connaughton JF Jr, Kron RE, Emich JP. Neonatal abstinence syndrome: 
   assessment and management. Addict Dis. 1975;2(1-2):141-58.
2. Jansson LM, Velez M, Harrow C. The opioid-exposed newborn: assessment and 
   pharmacologic management. J Opioid Manag. 2009 Jan-Feb;5(1):47-55.
3. Hudak ML, Tan RC; Committee on Drugs; Committee on Fetus and Newborn; American 
   Academy of Pediatrics. Neonatal drug withdrawal. Pediatrics. 2012 Feb;129(2):e540-60. 
   doi: 10.1542/peds.2011-3212.

The Modified Finnegan Neonatal Abstinence Score (NAS) is the most widely used tool 
for assessing neonatal opioid withdrawal syndrome. It evaluates symptoms across 
central nervous system, metabolic/vasomotor, respiratory, and gastrointestinal 
domains to guide treatment decisions. Scores ≥8 (three consecutive) or ≥12 (two 
consecutive) typically indicate need for pharmacologic intervention.
"""

from pydantic import BaseModel, Field
from typing import Literal


class ModifiedFinneganNeonatalAbstinenceScoreRequest(BaseModel):
    """
    Request model for Modified Finnegan Neonatal Abstinence Score (NAS)
    
    The Modified Finnegan NAS assesses neonatal opioid withdrawal across four domains:
    
    **Central Nervous System Disturbances:**
    - Cry patterns, sleep duration, Moro reflex, tremors
    - Muscle tone, excoriation, myoclonic jerks, convulsions
    
    **Metabolic, Vasomotor, and Respiratory Disturbances:**
    - Sweating, hyperthermia, yawning, mottling
    - Nasal flaring, respiratory rate, sneezing, nasal stuffiness
    
    **Gastrointestinal Disturbances:**
    - Feeding patterns, regurgitation, vomiting, stool consistency
    
    **Treatment Guidelines:**
    - Score 0-7: No treatment needed, continue supportive care
    - Score 8-11: Monitor closely, consider treatment if 3 consecutive scores ≥8
    - Score ≥12: Initiate pharmacologic treatment if 2 consecutive scores ≥12
    
    **Scoring Schedule:**
    - Every 3-4 hours during hospitalization
    - More frequent assessment if scores are elevated
    
    References (Vancouver style):
    1. Finnegan LP, Connaughton JF Jr, Kron RE, Emich JP. Neonatal abstinence syndrome: 
       assessment and management. Addict Dis. 1975;2(1-2):141-58.
    2. Jansson LM, Velez M, Harrow C. The opioid-exposed newborn: assessment and 
       pharmacologic management. J Opioid Manag. 2009 Jan-Feb;5(1):47-55.
    3. Hudak ML, Tan RC; Committee on Drugs; Committee on Fetus and Newborn; American 
       Academy of Pediatrics. Neonatal drug withdrawal. Pediatrics. 2012 Feb;129(2):e540-60. 
       doi: 10.1542/peds.2011-3212.
    """
    
    cry: Literal["normal", "excessive_high_pitched_under_5min", "continuous_high_pitched_over_5min"] = Field(
        ...,
        description="Crying pattern assessment. Normal (0 pts), excessive high-pitched <5 min (2 pts), continuous high-pitched >5 min (3 pts)",
        example="normal"
    )
    
    sleep: Literal["normal", "sleeps_under_3hrs", "sleeps_under_2hrs", "sleeps_under_1hr"] = Field(
        ...,
        description="Sleep duration after feeding. Normal (0 pts), <3 hrs (1 pt), <2 hrs (2 pts), <1 hr (3 pts)",
        example="normal"
    )
    
    moro_reflex: Literal["normal", "hyperactive", "markedly_hyperactive"] = Field(
        ...,
        description="Moro reflex activity. Normal (0 pts), hyperactive (2 pts), markedly hyperactive (3 pts)",
        example="normal"
    )
    
    tremors: Literal["none", "mild_when_disturbed", "moderate_severe_when_disturbed", "mild_when_undisturbed", "moderate_severe_when_undisturbed"] = Field(
        ...,
        description="Tremor severity and occurrence. None (0 pts), mild when disturbed (1 pt), moderate-severe when disturbed (2 pts), mild when undisturbed (3 pts), moderate-severe when undisturbed (4 pts)",
        example="none"
    )
    
    increased_muscle_tone: Literal["no", "yes"] = Field(
        ...,
        description="Presence of increased muscle tone or hypertonia. No (0 pts), Yes (1 pt)",
        example="no"
    )
    
    excoriation: Literal["no", "yes"] = Field(
        ...,
        description="Skin excoriation from excessive movement or rubbing. No (0 pts), Yes (1 pt)",
        example="no"
    )
    
    myoclonic_jerks: Literal["no", "yes"] = Field(
        ...,
        description="Presence of myoclonic jerks (sudden, brief muscle contractions). No (0 pts), Yes (3 pts)",
        example="no"
    )
    
    generalized_convulsions: Literal["no", "yes"] = Field(
        ...,
        description="Presence of generalized convulsions or seizures. No (0 pts), Yes (5 pts)",
        example="no"
    )
    
    sweating: Literal["no", "yes"] = Field(
        ...,
        description="Excessive sweating not related to ambient temperature. No (0 pts), Yes (1 pt)",
        example="no"
    )
    
    hyperthermia: Literal["normal", "mild_99_to_100_9F", "severe_over_100_9F"] = Field(
        ...,
        description="Body temperature elevation. Normal (0 pts), 99.0-100.9°F/37.2-38.3°C (1 pt), >100.9°F/>38.3°C (2 pts)",
        example="normal"
    )
    
    frequent_yawning: Literal["no", "yes"] = Field(
        ...,
        description="Frequent yawning (>3-4 times per assessment interval). No (0 pts), Yes (1 pt)",
        example="no"
    )
    
    mottling: Literal["no", "yes"] = Field(
        ...,
        description="Skin mottling or discoloration pattern. No (0 pts), Yes (1 pt)",
        example="no"
    )
    
    nasal_flaring: Literal["no", "yes"] = Field(
        ...,
        description="Nasal flaring during breathing. No (0 pts), Yes (2 pts)",
        example="no"
    )
    
    respiratory_rate: Literal["normal", "over_60_no_retractions", "over_60_with_retractions"] = Field(
        ...,
        description="Respiratory rate and retractions. Normal (0 pts), >60/min no retractions (1 pt), >60/min with retractions (2 pts)",
        example="normal"
    )
    
    sneezing: Literal["no", "yes"] = Field(
        ...,
        description="Frequent sneezing (>3-4 times per assessment interval). No (0 pts), Yes (1 pt)",
        example="no"
    )
    
    nasal_stuffiness: Literal["no", "yes"] = Field(
        ...,
        description="Nasal congestion or stuffiness affecting breathing. No (0 pts), Yes (1 pt)",
        example="no"
    )
    
    excessive_sucking: Literal["no", "yes"] = Field(
        ...,
        description="Excessive or frantic sucking behavior on fists, fingers, or pacifier. No (0 pts), Yes (1 pt)",
        example="no"
    )
    
    poor_feeding: Literal["no", "yes"] = Field(
        ...,
        description="Poor feeding with infrequent, weak, or uncoordinated suck. No (0 pts), Yes (2 pts)",
        example="no"
    )
    
    regurgitation: Literal["no", "yes"] = Field(
        ...,
        description="Regurgitation ≥2 times during or immediately after feeding. No (0 pts), Yes (2 pts)",
        example="no"
    )
    
    projectile_vomiting: Literal["no", "yes"] = Field(
        ...,
        description="Forceful, projectile vomiting. No (0 pts), Yes (3 pts)",
        example="no"
    )
    
    loose_stools: Literal["no", "yes"] = Field(
        ...,
        description="Loose stools with curds or seedy appearance. No (0 pts), Yes (2 pts)",
        example="no"
    )
    
    watery_stools: Literal["no", "yes"] = Field(
        ...,
        description="Watery, liquid stools. No (0 pts), Yes (3 pts)",
        example="no"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "cry": "normal",
                "sleep": "normal",
                "moro_reflex": "normal",
                "tremors": "none",
                "increased_muscle_tone": "no",
                "excoriation": "no",
                "myoclonic_jerks": "no",
                "generalized_convulsions": "no",
                "sweating": "no",
                "hyperthermia": "normal",
                "frequent_yawning": "no",
                "mottling": "no",
                "nasal_flaring": "no",
                "respiratory_rate": "normal",
                "sneezing": "no",
                "nasal_stuffiness": "no",
                "excessive_sucking": "no",
                "poor_feeding": "no",
                "regurgitation": "no",
                "projectile_vomiting": "no",
                "loose_stools": "no",
                "watery_stools": "no"
            }
        }


class ModifiedFinneganNeonatalAbstinenceScoreResponse(BaseModel):
    """
    Response model for Modified Finnegan Neonatal Abstinence Score (NAS)
    
    The NAS score guides treatment decisions for neonatal opioid withdrawal:
    
    **Score Interpretation:**
    - 0-7 points: No treatment needed
      * Continue supportive care (swaddling, minimal stimulation, frequent small feeds)
      * Monitor every 3-4 hours
      * No pharmacologic intervention indicated
    
    - 8-11 points: Monitor closely
      * Increase monitoring frequency
      * Optimize non-pharmacologic interventions
      * Consider pharmacologic treatment if 3 consecutive scores ≥8
    
    - ≥12 points: Initiate treatment
      * Begin pharmacologic treatment if 2 consecutive scores ≥12
      * First-line medications: morphine or methadone
      * Goal: stabilize infant to allow feeding, sleeping, and weight gain
    
    **Non-pharmacologic Interventions:**
    - Swaddling and minimal environmental stimulation
    - Frequent small volume feeds
    - Quiet, dimly lit environment
    - Rooming-in with mother when possible
    - Skin-to-skin contact and breastfeeding support
    
    **Pharmacologic Treatment:**
    - Morphine: 0.1 mg/kg/dose q3-4h, titrate based on scores
    - Methadone: 0.05-0.1 mg/kg/dose q6h, longer half-life
    - Adjunct: phenobarbital for refractory cases or polysubstance exposure
    
    Reference: Hudak ML, et al. Pediatrics. 2012;129(2):e540-60.
    """
    
    result: int = Field(
        ...,
        ge=0,
        le=50,
        description="Total Modified Finnegan NAS score indicating severity of neonatal opioid withdrawal (0-50+ points)",
        example=4
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation with treatment recommendations and monitoring guidelines based on NAS score",
        example="NAS score of 4 indicates mild or no withdrawal symptoms. Continue supportive care including swaddling, minimal stimulation, frequent small feeds, and quiet environment. Monitor every 3-4 hours. No pharmacologic treatment indicated at this time."
    )
    
    stage: str = Field(
        ...,
        description="Treatment category (No Treatment, Monitor Closely, Treat)",
        example="No Treatment"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the severity level",
        example="Mild or no withdrawal symptoms"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 4,
                "unit": "points",
                "interpretation": "NAS score of 4 indicates mild or no withdrawal symptoms. Continue supportive care including swaddling, minimal stimulation, frequent small feeds, and quiet environment. Monitor every 3-4 hours. No pharmacologic treatment indicated at this time.",
                "stage": "No Treatment",
                "stage_description": "Mild or no withdrawal symptoms"
            }
        }