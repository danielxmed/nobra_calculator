"""
Withdrawal Assessment Tool (WAT-1) for Pediatric Withdrawal Models

Request and response models for WAT-1 calculation.

References (Vancouver style):
1. Franck LS, Harris SK, Soetenga DJ, et al. The Withdrawal Assessment Tool-1 
   (WAT-1): an assessment instrument for monitoring opioid and benzodiazepine 
   withdrawal symptoms in pediatric patients. Pediatr Crit Care Med. 
   2008;9(6):573-580. doi: 10.1097/PCC.0b013e31818c8328
2. Anand KJ, Willson DF, Berger J, et al. Tolerance and withdrawal from prolonged 
   opioid use in critically ill children. Pediatrics. 2010;125(5):e1208-e1225. 
   doi: 10.1542/peds.2009-0489
3. Ista E, van Dijk M, Gamel C, et al. Withdrawal symptoms in children after 
   long-term administration of sedatives and/or analgesics: a literature review. 
   Assessment remains troublesome. Intensive Care Med. 2007;33(8):1396-1406. 
   doi: 10.1007/s00134-007-0696-x
4. Best KM, Asaro LA, Franck LS. Patterns of sedation weaning in critically ill 
   children recovering from acute respiratory failure. Pediatr Crit Care Med. 
   2015;16(3):e43-e49. doi: 10.1097/PCC.0000000000000324

The WAT-1 is a validated 12-parameter assessment tool designed to systematically 
evaluate withdrawal severity in pediatric patients following prolonged opioid or 
benzodiazepine administration. Each parameter is scored from 0-3 points based on 
clinical observations, with total scores ranging from 0-33 points. The tool helps 
guide pharmacological intervention decisions and monitoring frequency in critically 
ill children undergoing sedation weaning.
"""

from pydantic import BaseModel, Field
from typing import Literal, Dict, Any, List


class Wat1PediatricWithdrawalRequest(BaseModel):
    """
    Request model for Withdrawal Assessment Tool (WAT-1) for Pediatric Withdrawal
    
    The WAT-1 evaluates 12 clinical parameters to assess withdrawal severity in 
    pediatric patients (term infants to 18 years) following prolonged opioid or 
    benzodiazepine administration. Each parameter is scored 0-3 points based on 
    severity of clinical findings.
    
    Clinical Assessment Parameters:
    
    Age Consideration:
    - post_menstrual_age_weeks: Used for developmental context and interpretation
    
    Neurologic/Behavioral Parameters:
    - state_sleep_wake_cycle: Sleep pattern disturbances and agitation
    - tremor: Involuntary shaking movements
    - increased_muscle_tone: Hypertonia and rigidity
    - myoclonus_seizures: Jerky movements and seizure activity
    
    Autonomic Parameters:
    - tachypnea: Elevated respiratory rate
    - sweating: Diaphoresis and temperature dysregulation
    - fever: Hyperthermia
    
    Other Physical Signs:
    - excoriation: Self-inflicted scratching marks
    - frequent_yawning_sneezing: Autonomic responses
    - nasal_stuffiness: Nasal congestion and rhinorrhea
    - poor_feeding_vomiting: Gastrointestinal symptoms
    
    Scoring Guidelines:
    - 0 points: Normal or absent findings
    - 1 point: Mild symptoms
    - 2 points: Moderate symptoms  
    - 3 points: Severe symptoms
    
    Clinical Interpretation:
    - 0-2 points: No significant withdrawal (supportive care)
    - 3-8 points: Mild-moderate withdrawal (consider pharmacological intervention)
    - ≥9 points: Moderate-severe withdrawal (pharmacological intervention indicated)
    
    References (Vancouver style):
    1. Franck LS, Harris SK, Soetenga DJ, et al. The Withdrawal Assessment Tool-1 
    (WAT-1): an assessment instrument for monitoring opioid and benzodiazepine 
    withdrawal symptoms in pediatric patients. Pediatr Crit Care Med. 
    2008;9(6):573-580. doi: 10.1097/PCC.0b013e31818c8328
    2. Anand KJ, Willson DF, Berger J, et al. Tolerance and withdrawal from prolonged 
    opioid use in critically ill children. Pediatrics. 2010;125(5):e1208-e1225. 
    doi: 10.1542/peds.2009-0489
    3. Ista E, van Dijk M, Gamel C, et al. Withdrawal symptoms in children after 
    long-term administration of sedatives and/or analgesics: a literature review. 
    Assessment remains troublesome. Intensive Care Med. 2007;33(8):1396-1406. 
    doi: 10.1007/s00134-007-0696-x
    4. Best KM, Asaro LA, Franck LS. Patterns of sedation weaning in critically ill 
    children recovering from acute respiratory failure. Pediatr Crit Care Med. 
    2015;16(3):e43-e49. doi: 10.1097/PCC.0000000000000324
    """
    
    post_menstrual_age_weeks: int = Field(
        ...,
        description="Post-menstrual age in weeks (gestational age + chronological age). Used for developmental context and age-appropriate interpretation of withdrawal signs",
        ge=25,
        le=200,
        example=40
    )
    
    state_sleep_wake_cycle: Literal[0, 1, 2, 3] = Field(
        ...,
        description="State/sleep-wake cycle disturbance. 0=normal sleep pattern, 1=mild restlessness, 2=moderate agitation, 3=severe sleep disturbance with continuous irritability",
        example=1
    )
    
    tremor: Literal[0, 1, 2, 3] = Field(
        ...,
        description="Tremor severity. 0=no tremor, 1=mild tremor when stimulated, 2=moderate tremor when awake, 3=severe continuous tremor",
        example=0
    )
    
    increased_muscle_tone: Literal[0, 1, 2, 3] = Field(
        ...,
        description="Increased muscle tone/hypertonia. 0=normal muscle tone, 1=mild increase in tone, 2=moderate increase in tone, 3=severe rigidity",
        example=1
    )
    
    excoriation: Literal[0, 1, 2, 3] = Field(
        ...,
        description="Excoriation marks from scratching. 0=no excoriation marks, 1=red marks from scratching, 2=scratches without bleeding, 3=bleeding scratches",
        example=0
    )
    
    myoclonus_seizures: Literal[0, 1, 2, 3] = Field(
        ...,
        description="Myoclonus/seizure activity. 0=no myoclonus or seizures, 1=occasional jerky movements, 2=frequent jerky movements, 3=continuous movements or seizures",
        example=0
    )
    
    tachypnea: Literal[0, 1, 2, 3] = Field(
        ...,
        description="Tachypnea/respiratory distress. 0=normal respiratory rate for age, 1=mildly elevated rate, 2=moderately elevated rate, 3=severely elevated or respiratory distress",
        example=1
    )
    
    sweating: Literal[0, 1, 2, 3] = Field(
        ...,
        description="Sweating/diaphoresis. 0=no sweating, 1=mild sweating, 2=moderate sweating, 3=profuse sweating",
        example=0
    )
    
    fever: Literal[0, 1, 2, 3] = Field(
        ...,
        description="Fever/hyperthermia. 0=temperature <37.2°C, 1=temperature 37.2-37.8°C, 2=temperature 37.9-38.3°C, 3=temperature >38.3°C",
        example=0
    )
    
    frequent_yawning_sneezing: Literal[0, 1, 2, 3] = Field(
        ...,
        description="Frequent yawning/sneezing. 0=no yawning/sneezing, 1=occasional yawning/sneezing, 2=frequent yawning/sneezing, 3=continuous yawning/sneezing",
        example=0
    )
    
    nasal_stuffiness: Literal[0, 1, 2, 3] = Field(
        ...,
        description="Nasal stuffiness/rhinorrhea. 0=no nasal symptoms, 1=mild nasal stuffiness, 2=moderate nasal stuffiness, 3=severe nasal stuffiness",
        example=0
    )
    
    poor_feeding_vomiting: Literal[0, 1, 2, 3] = Field(
        ...,
        description="Poor feeding/vomiting. 0=normal feeding, 1=poor feeding, 2=refusal to feed, 3=vomiting",
        example=1
    )
    
    class Config:
        schema_extra = {
            "example": {
                "post_menstrual_age_weeks": 40,
                "state_sleep_wake_cycle": 1,
                "tremor": 0,
                "increased_muscle_tone": 1,
                "excoriation": 0,
                "myoclonus_seizures": 0,
                "tachypnea": 1,
                "sweating": 0,
                "fever": 0,
                "frequent_yawning_sneezing": 0,
                "nasal_stuffiness": 0,
                "poor_feeding_vomiting": 1
            }
        }


class Wat1PediatricWithdrawalResponse(BaseModel):
    """
    Response model for Withdrawal Assessment Tool (WAT-1) for Pediatric Withdrawal
    
    The WAT-1 score ranges from 0-33 points and guides clinical intervention decisions:
    
    Score Interpretation:
    - 0-2 points: No significant withdrawal or very mild symptoms
      * Continue supportive care and monitoring
      * Reassess every 8-12 hours
      * Environmental modifications and comfort measures
      
    - 3-8 points: Mild to moderate withdrawal symptoms
      * Consider pharmacological intervention
      * Increase monitoring frequency (every 4-6 hours)
      * Medications: methadone, morphine, or clonidine as appropriate
      
    - ≥9 points: Moderate to severe withdrawal symptoms
      * Immediate pharmacological intervention indicated
      * Intensive monitoring (every 1-2 hours)
      * Consider ICU-level care if symptoms severe
      
    Age Considerations:
    - Preterm infants may have different withdrawal manifestations
    - Younger children may require modified assessment approaches
    - Older children can better communicate symptoms
    
    Reference: Franck LS, et al. Pediatr Crit Care Med. 2008;9(6):573-580.
    """
    
    result: int = Field(
        ...,
        description="WAT-1 total score calculated from 12 clinical parameters (range: 0-33 points)",
        ge=0,
        le=33,
        example=4
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation and recommended management based on the WAT-1 score and patient age",
        example="WAT-1 score of 4 suggests mild to moderate withdrawal symptoms requiring intervention. For term infants, withdrawal may manifest differently than in older children. Consider pharmacological management with appropriate medications (methadone, morphine, or clonidine as per protocol). Increase monitoring frequency to every 2-4 hours. Provide comfort measures, environmental modifications, and consider non-pharmacological interventions. Notify attending physician for medication orders."
    )
    
    stage: str = Field(
        ...,
        description="Withdrawal severity category (None to Mild, Mild to Moderate, Moderate to Severe)",
        example="Mild to Moderate"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the withdrawal severity category",
        example="Mild to moderate withdrawal symptoms"
    )
    
    age_category: Dict[str, Any] = Field(
        ...,
        description="Age categorization with developmental considerations for assessment interpretation",
        example={
            "category": "term_infant",
            "description": "Term infant",
            "post_menstrual_age": 40,
            "considerations": "Standard infant withdrawal assessment applicable"
        }
    )
    
    parameter_breakdown: Dict[str, Any] = Field(
        ...,
        description="Detailed breakdown of individual parameter scores and their clinical significance",
        example={
            "individual_scores": {
                "state_sleep_wake_cycle": {
                    "score": 1,
                    "description": "State/sleep-wake cycle disturbance",
                    "score_description": "Mild restlessness",
                    "severity": "mild"
                }
            },
            "high_scoring_parameters": [],
            "total_possible_score": 33,
            "percentage_of_maximum": 12.1
        }
    )
    
    detailed_assessment: Dict[str, Any] = Field(
        ...,
        description="Comprehensive clinical assessment including intervention recommendations, monitoring guidelines, and family education",
        example={
            "severity_assessment": {
                "severity": "mild_to_moderate",
                "urgency": "prompt",
                "description": "Withdrawal symptoms requiring intervention",
                "score": 4,
                "max_possible": 33,
                "intervention_threshold": True
            },
            "intervention_recommendations": [
                "Consider pharmacological intervention",
                "Initiate or adjust withdrawal protocol",
                "Increase monitoring frequency",
                "Enhance comfort measures"
            ],
            "monitoring_recommendations": [
                "Assess WAT-1 every 4-6 hours",
                "Monitor vital signs every 2 hours",
                "Continuous cardiorespiratory monitoring"
            ]
        }
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 4,
                "unit": "points",
                "interpretation": "WAT-1 score of 4 suggests mild to moderate withdrawal symptoms requiring intervention. For term infants, withdrawal may manifest differently than in older children. Consider pharmacological management with appropriate medications (methadone, morphine, or clonidine as per protocol). Increase monitoring frequency to every 2-4 hours. Provide comfort measures, environmental modifications, and consider non-pharmacological interventions. Notify attending physician for medication orders.",
                "stage": "Mild to Moderate",
                "stage_description": "Mild to moderate withdrawal symptoms",
                "age_category": {
                    "category": "term_infant",
                    "description": "Term infant",
                    "post_menstrual_age": 40,
                    "considerations": "Standard infant withdrawal assessment applicable"
                },
                "parameter_breakdown": {
                    "individual_scores": {
                        "state_sleep_wake_cycle": {
                            "score": 1,
                            "description": "State/sleep-wake cycle disturbance",
                            "score_description": "Mild restlessness",
                            "severity": "mild"
                        }
                    },
                    "high_scoring_parameters": [],
                    "total_possible_score": 33,
                    "percentage_of_maximum": 12.1
                },
                "detailed_assessment": {
                    "severity_assessment": {
                        "severity": "mild_to_moderate",
                        "urgency": "prompt",
                        "description": "Withdrawal symptoms requiring intervention",
                        "score": 4,
                        "max_possible": 33,
                        "intervention_threshold": True
                    },
                    "intervention_recommendations": [
                        "Consider pharmacological intervention",
                        "Initiate or adjust withdrawal protocol",
                        "Increase monitoring frequency",
                        "Enhance comfort measures"
                    ],
                    "monitoring_recommendations": [
                        "Assess WAT-1 every 4-6 hours",
                        "Monitor vital signs every 2 hours",
                        "Continuous cardiorespiratory monitoring"
                    ]
                }
            }
        }