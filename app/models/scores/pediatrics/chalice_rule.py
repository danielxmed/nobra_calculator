"""
CHALICE (Children's Head injury ALgorithm for the prediction of Important Clinical Events) Rule Models

Request and response models for CHALICE Rule calculation.

References (Vancouver style):
1. Dunning J, Daly JP, Lomas JP, Lecky F, Batchelor J, Mackway-Jones K. Derivation of the 
   children's head injury algorithm for the prediction of important clinical events decision 
   rule for head injury in children. Arch Dis Child. 2006;91(11):885-91.
2. Dunning J, Batchelor J, Stratford-Smith P, et al. A meta-analysis of variables that predict 
   significant intracranial injury in minor head trauma. Arch Dis Child. 2004;89(7):653-9.
3. Kuppermann N, Holmes JF, Dayan PS, et al. Identification of children at very low risk of 
   clinically-important brain injuries after head trauma: a prospective cohort study. 
   Lancet. 2009;374(9696):1160-70.

The CHALICE rule is a clinical decision tool developed to predict death, need for neurosurgical 
intervention, or CT abnormality in children (<16 years) with head trauma. The rule helps identify 
which pediatric patients require CT imaging after head injury.

CHALICE Criteria Categories:

History Criteria (any positive indicates CT):
- Witnessed loss of consciousness >5 minutes
- Amnesia (antegrade or retrograde) >5 minutes  
- Abnormal drowsiness (as reported by parent/carer)
- ≥3 vomits after head injury
- Suspicion of non-accidental injury
- Seizure after head injury (no prior epilepsy history)

Examination Criteria (any positive indicates CT):
- Glasgow Coma Score <14 (or <15 if <1 year old)
- Suspicion of penetrating/depressed skull injury
- Signs of basal skull fracture
- Positive focal neurologic sign
- Bruise/swelling/laceration >5 cm to head (if <1 year old)

Mechanism Criteria (any positive indicates CT):
- High-speed road traffic accident (>40 mph/65 km/h)
- Fall from height >3 meters (>10 feet)
- High-speed injury from projectile or object

Performance Characteristics:
- Sensitivity: 98% (95% CI: 96-100%) for clinically significant head injury
- Specificity: 87% (95% CI: 86-87%)
- CT scan rate: 14%
- Derived from study of 22,772 children over 2.5 years

Clinical Application:
The CHALICE rule provides a highly sensitive method for identifying children who should undergo 
CT scanning after head injury, helping to standardize care while maintaining safety in the 
emergency department setting.
"""

from pydantic import BaseModel, Field
from typing import Literal, Dict, Any


class ChaliceRuleRequest(BaseModel):
    """
    Request model for CHALICE (Children's Head injury ALgorithm for the prediction of Important Clinical Events) Rule
    
    The CHALICE rule uses 15 clinical criteria across three categories (History, Examination, Mechanism) 
    to determine whether a child with head trauma requires CT imaging. The rule is designed for children 
    <16 years of age presenting to the emergency department after head injury.
    
    History Criteria (any positive indicates need for CT):
    
    Witnessed Loss of Consciousness >5 minutes:
    - Duration of unconsciousness as witnessed by reliable observer
    - Must be >5 minutes to be considered positive
    - Brief LOC ≤5 minutes is not a positive criterion
    
    Amnesia >5 minutes:
    - Either antegrade (post-traumatic) or retrograde (pre-traumatic) amnesia
    - Duration must exceed 5 minutes
    - Can be difficult to assess in very young children
    
    Abnormal Drowsiness:
    - As reported by parent or primary caregiver
    - Subjective assessment of unusual sleepiness or altered consciousness
    - Important parental concern indicator
    
    ≥3 Vomits After Head Injury:
    - Three or more episodes of vomiting following the head trauma
    - Must be post-traumatic vomiting, not pre-existing
    - Significant indicator of increased intracranial pressure
    
    Suspicion of Non-Accidental Injury:
    - Clinical suspicion based on mechanism, injuries, or history
    - Important safeguarding consideration
    - Requires careful documentation and appropriate referral
    
    Seizure After Head Injury:
    - New-onset seizure following head trauma
    - Must have no previous history of epilepsy
    - Post-traumatic seizures indicate brain injury
    
    Examination Criteria (any positive indicates need for CT):
    
    Glasgow Coma Score:
    - Age-dependent thresholds: <15 for children <1 year, <14 for children ≥1 year
    - Accounts for normal developmental differences in neurological assessment
    - Lower thresholds in infants reflect different normal ranges
    
    Suspicion of Penetrating/Depressed Skull Injury:
    - Clinical assessment of skull integrity
    - Includes visible depression, penetrating wounds, or palpable defects
    - High-risk mechanism requiring immediate imaging
    
    Signs of Basal Skull Fracture:
    - Classic signs: CSF rhinorrhea/otorrhea, periorbital ecchymoses (panda eyes), 
      Battle's sign (retroauricular ecchymosis), hemotympanum
    - Indicates significant skull base trauma
    - High association with intracranial injury
    
    Positive Focal Neurologic Sign:
    - Any new focal neurological deficit
    - Includes motor, sensory, or cranial nerve abnormalities
    - Indicates localized brain injury
    
    Bruise/Swelling/Laceration >5 cm (if <1 year old):
    - Only applies to infants <1 year of age
    - Reflects increased vulnerability in this age group
    - Size threshold of 5 cm indicates significant trauma force
    
    Mechanism Criteria (any positive indicates need for CT):
    
    High-Speed Road Traffic Accident:
    - Speed >40 mph (>65 km/h)
    - High-energy mechanism associated with severe injuries
    - Includes pedestrian struck by vehicle at high speed
    
    Fall from Height >3 meters:
    - Fall from >10 feet
    - Significant mechanism based on gravitational force
    - Height threshold based on injury severity data
    
    High-Speed Injury from Projectile/Object:
    - High-velocity impact from objects or projectiles
    - Includes sports equipment, tools, or other high-energy impacts
    - Mechanism suggests significant force transmission
    
    Clinical Decision Making:
    - If ANY criterion is positive: Proceed with head CT
    - If NO criteria are positive: Safe to monitor without CT
    - Consider clinical judgment and parental concerns in borderline cases
    
    Performance and Validation:
    - 98% sensitivity for clinically important brain injury
    - 87% specificity, resulting in 14% CT scan rate
    - Validated in 22,772 children across multiple centers
    - Designed to minimize missed significant injuries while reducing unnecessary imaging
    
    References (Vancouver style):
    1. Dunning J, Daly JP, Lomas JP, Lecky F, Batchelor J, Mackway-Jones K. Derivation of the 
    children's head injury algorithm for the prediction of important clinical events decision 
    rule for head injury in children. Arch Dis Child. 2006;91(11):885-91.
    2. Dunning J, Batchelor J, Stratford-Smith P, et al. A meta-analysis of variables that predict 
    significant intracranial injury in minor head trauma. Arch Dis Child. 2004;89(7):653-9.
    """
    
    witnessed_loc_over_5_min: Literal["yes", "no"] = Field(
        ...,
        description="Witnessed loss of consciousness greater than 5 minutes. Must be observed by reliable witness and exceed 5-minute duration",
        example="no"
    )
    
    amnesia_over_5_min: Literal["yes", "no"] = Field(
        ...,
        description="Amnesia (antegrade or retrograde) greater than 5 minutes. Memory loss before or after the injury exceeding 5 minutes",
        example="no"
    )
    
    abnormal_drowsiness: Literal["yes", "no"] = Field(
        ...,
        description="Abnormal drowsiness as reported by parent or primary caregiver. Unusual sleepiness or altered level of consciousness",
        example="no"
    )
    
    three_or_more_vomits: Literal["yes", "no"] = Field(
        ...,
        description="Three or more episodes of vomiting after head injury. Post-traumatic vomiting may indicate increased intracranial pressure",
        example="no"
    )
    
    suspicion_nai: Literal["yes", "no"] = Field(
        ...,
        description="Suspicion of non-accidental injury based on mechanism, injuries, or history. Important safeguarding consideration",
        example="no"
    )
    
    seizure_after_injury: Literal["yes", "no"] = Field(
        ...,
        description="Seizure after head injury in patient with no previous history of epilepsy. New-onset post-traumatic seizure",
        example="no"
    )
    
    age_category: Literal["under_1_year", "1_year_or_older"] = Field(
        ...,
        description="Patient age category for appropriate GCS interpretation. <1 year has different neurological assessment norms",
        example="1_year_or_older"
    )
    
    gcs_score: int = Field(
        ...,
        ge=3,
        le=15,
        description="Glasgow Coma Score (3-15). Abnormal if <15 for age <1 year or <14 for age ≥1 year",
        example=15
    )
    
    suspicion_penetrating_depressed_fracture: Literal["yes", "no"] = Field(
        ...,
        description="Suspicion of penetrating or depressed skull injury. Clinical assessment of skull integrity and penetrating wounds",
        example="no"
    )
    
    signs_basal_skull_fracture: Literal["yes", "no"] = Field(
        ...,
        description="Signs of basal skull fracture: CSF leak, panda eyes, Battle's sign, hemotympanum. Indicates skull base trauma",
        example="no"
    )
    
    positive_focal_neurologic_sign: Literal["yes", "no"] = Field(
        ...,
        description="Positive focal neurologic sign. Any new focal neurological deficit including motor, sensory, or cranial nerve abnormalities",
        example="no"
    )
    
    bruise_swelling_laceration_over_5cm: Literal["yes", "no", "not_applicable"] = Field(
        ...,
        description="Bruise, swelling, or laceration >5 cm to head (only applies if <1 year old). Use 'not_applicable' for children ≥1 year",
        example="not_applicable"
    )
    
    high_speed_rta: Literal["yes", "no"] = Field(
        ...,
        description="High-speed road traffic accident >40 mph (>65 km/h). High-energy mechanism including pedestrian struck at high speed",
        example="no"
    )
    
    fall_over_3_meters: Literal["yes", "no"] = Field(
        ...,
        description="Fall from height greater than 3 meters (>10 feet). Significant gravitational force mechanism",
        example="no"
    )
    
    high_speed_projectile: Literal["yes", "no"] = Field(
        ...,
        description="High-speed injury from projectile or object. High-velocity impact from sports equipment, tools, or other objects",
        example="no"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "witnessed_loc_over_5_min": "no",
                "amnesia_over_5_min": "no",
                "abnormal_drowsiness": "yes",
                "three_or_more_vomits": "no",
                "suspicion_nai": "no",
                "seizure_after_injury": "no",
                "age_category": "1_year_or_older",
                "gcs_score": 15,
                "suspicion_penetrating_depressed_fracture": "no",
                "signs_basal_skull_fracture": "no",
                "positive_focal_neurologic_sign": "no",
                "bruise_swelling_laceration_over_5cm": "not_applicable",
                "high_speed_rta": "no",
                "fall_over_3_meters": "no",
                "high_speed_projectile": "no"
            }
        }


class ChaliceRuleResponse(BaseModel):
    """
    Response model for CHALICE (Children's Head injury ALgorithm for the prediction of Important Clinical Events) Rule
    
    The CHALICE rule provides a binary decision (CT recommended vs. no CT required) based on the 
    presence or absence of any high-risk criteria. The rule achieves high sensitivity (98%) for 
    detecting clinically important brain injuries while maintaining reasonable specificity (87%).
    
    Decision Outcomes:
    
    CT Recommended (High Risk):
    - One or more CHALICE criteria are positive
    - Increased risk for clinically important brain injury
    - Proceed with urgent head CT imaging
    - 98% sensitivity ensures very few significant injuries are missed
    - Includes detailed breakdown of which criteria were positive
    
    No CT Required (Low Risk):
    - No CHALICE criteria are positive
    - Low risk for clinically important brain injury
    - Safe to monitor without CT imaging
    - Consider discharge if clinical condition remains stable
    - 87% specificity helps avoid unnecessary radiation exposure
    
    Clinical Context and Performance:
    
    Derivation Study:
    - 22,772 children recruited over 2.5 years
    - 65% male, 56% under 5 years old
    - 281 children with CT abnormalities
    - 137 required neurosurgical intervention
    - 15 deaths occurred
    
    Performance Characteristics:
    - Sensitivity: 98% (95% CI: 96-100%) for clinically significant head injury
    - Specificity: 87% (95% CI: 86-87%)
    - CT scan rate: 14% (significant reduction from routine imaging)
    - Negative predictive value: >99% for significant injury
    
    Clinical Significance:
    - Highly sensitive rule minimizes missed significant injuries
    - Reasonable specificity reduces unnecessary CT scans
    - Standardizes pediatric head trauma assessment
    - Particularly valuable in emergency department settings
    
    Implementation Considerations:
    - Designed for children <16 years with head injury
    - Requires clinical judgment for borderline cases
    - Consider parental concerns and clinical context
    - Age-specific GCS thresholds are critical
    - Bruise/laceration criterion only applies to infants <1 year
    
    Comparison with Other Rules:
    - CHALICE applicable in 97-99% of cases (higher than PECARN)
    - PECARN has slightly higher sensitivity (99-100%) but lower applicability
    - CATCH rule focuses on different population and criteria
    - CHALICE provides good balance of sensitivity and practical application
    
    Quality Improvement Applications:
    - Standardized approach to pediatric head trauma
    - Reduction in unnecessary imaging and radiation exposure
    - Improved resource utilization in emergency departments
    - Enhanced safety through systematic risk assessment
    
    Reference: Dunning J, et al. Arch Dis Child. 2006;91(11):885-91.
    """
    
    result: Dict[str, Any] = Field(
        ...,
        description="Comprehensive CHALICE rule assessment including recommendation, criteria analysis, and clinical context",
        example={
            "recommendation": "CT Recommended",
            "criteria_met": True,
            "positive_criteria_count": 1,
            "category_summary": {
                "history_positive": True,
                "examination_positive": False,
                "mechanism_positive": False
            },
            "criteria_breakdown": {
                "history_criteria": {
                    "witnessed_loc_over_5_min": {
                        "present": False,
                        "description": "Witnessed loss of consciousness >5 minutes"
                    },
                    "amnesia_over_5_min": {
                        "present": False,
                        "description": "Amnesia (antegrade or retrograde) >5 minutes"
                    },
                    "abnormal_drowsiness": {
                        "present": True,
                        "description": "Abnormal drowsiness (as reported by parent/carer)"
                    },
                    "three_or_more_vomits": {
                        "present": False,
                        "description": "≥3 vomits after head injury"
                    },
                    "suspicion_nai": {
                        "present": False,
                        "description": "Suspicion of non-accidental injury"
                    },
                    "seizure_after_injury": {
                        "present": False,
                        "description": "Seizure after head injury (no prior epilepsy)"
                    }
                },
                "examination_criteria": {
                    "age_category": {
                        "value": "1_year_or_older",
                        "description": "Patient age category for GCS interpretation"
                    },
                    "glasgow_coma_score": {
                        "value": 15,
                        "threshold": 14,
                        "abnormal": False,
                        "description": "Glasgow Coma Score (abnormal if <14 for this age)"
                    },
                    "suspicion_penetrating_depressed_fracture": {
                        "present": False,
                        "description": "Suspicion of penetrating or depressed skull injury"
                    },
                    "signs_basal_skull_fracture": {
                        "present": False,
                        "description": "Signs of basal skull fracture"
                    },
                    "positive_focal_neurologic_sign": {
                        "present": False,
                        "description": "Positive focal neurologic sign"
                    },
                    "bruise_swelling_laceration_over_5cm": {
                        "present": False,
                        "description": "Bruise, swelling, or laceration >5 cm (if <1 year old)"
                    }
                },
                "mechanism_criteria": {
                    "high_speed_rta": {
                        "present": False,
                        "description": "High-speed road traffic accident (>40 mph)"
                    },
                    "fall_over_3_meters": {
                        "present": False,
                        "description": "Fall from height >3 meters"
                    },
                    "high_speed_projectile": {
                        "present": False,
                        "description": "High-speed injury from projectile or object"
                    }
                }
            },
            "clinical_context": {
                "sensitivity": "98%",
                "specificity": "87%",
                "ct_scan_rate": "14%",
                "validation": "Validated in children <16 years with head injury",
                "study_population": "22,772 children over 2.5 years"
            }
        }
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the decision",
        example="decision"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation with specific recommendation and rationale based on CHALICE criteria",
        example="CHALICE Rule: POSITIVE. One or more criteria met. Proceed with urgent head CT to evaluate for intracranial injury requiring intervention. Total positive criteria: History (1), Examination (0), Mechanism (0)."
    )
    
    stage: str = Field(
        ...,
        description="Risk classification (High Risk for CT recommended, Low Risk for no CT required)",
        example="High Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the risk category and clinical significance",
        example="Increased risk for clinically important brain injury"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "result": {
                    "recommendation": "CT Recommended",
                    "criteria_met": True,
                    "positive_criteria_count": 1,
                    "category_summary": {
                        "history_positive": True,
                        "examination_positive": False,
                        "mechanism_positive": False
                    },
                    "criteria_breakdown": {
                        "history_criteria": {
                            "witnessed_loc_over_5_min": {
                                "present": False,
                                "description": "Witnessed loss of consciousness >5 minutes"
                            },
                            "amnesia_over_5_min": {
                                "present": False,
                                "description": "Amnesia (antegrade or retrograde) >5 minutes"
                            },
                            "abnormal_drowsiness": {
                                "present": True,
                                "description": "Abnormal drowsiness (as reported by parent/carer)"
                            },
                            "three_or_more_vomits": {
                                "present": False,
                                "description": "≥3 vomits after head injury"
                            },
                            "suspicion_nai": {
                                "present": False,
                                "description": "Suspicion of non-accidental injury"
                            },
                            "seizure_after_injury": {
                                "present": False,
                                "description": "Seizure after head injury (no prior epilepsy)"
                            }
                        },
                        "examination_criteria": {
                            "age_category": {
                                "value": "1_year_or_older",
                                "description": "Patient age category for GCS interpretation"
                            },
                            "glasgow_coma_score": {
                                "value": 15,
                                "threshold": 14,
                                "abnormal": False,
                                "description": "Glasgow Coma Score (abnormal if <14 for this age)"
                            },
                            "suspicion_penetrating_depressed_fracture": {
                                "present": False,
                                "description": "Suspicion of penetrating or depressed skull injury"
                            },
                            "signs_basal_skull_fracture": {
                                "present": False,
                                "description": "Signs of basal skull fracture"
                            },
                            "positive_focal_neurologic_sign": {
                                "present": False,
                                "description": "Positive focal neurologic sign"
                            },
                            "bruise_swelling_laceration_over_5cm": {
                                "present": False,
                                "description": "Bruise, swelling, or laceration >5 cm (if <1 year old)"
                            }
                        },
                        "mechanism_criteria": {
                            "high_speed_rta": {
                                "present": False,
                                "description": "High-speed road traffic accident (>40 mph)"
                            },
                            "fall_over_3_meters": {
                                "present": False,
                                "description": "Fall from height >3 meters"
                            },
                            "high_speed_projectile": {
                                "present": False,
                                "description": "High-speed injury from projectile or object"
                            }
                        }
                    },
                    "clinical_context": {
                        "sensitivity": "98%",
                        "specificity": "87%",
                        "ct_scan_rate": "14%",
                        "validation": "Validated in children <16 years with head injury",
                        "study_population": "22,772 children over 2.5 years"
                    }
                },
                "unit": "decision",
                "interpretation": "CHALICE Rule: POSITIVE. One or more criteria met. Proceed with urgent head CT to evaluate for intracranial injury requiring intervention. Total positive criteria: History (1), Examination (0), Mechanism (0).",
                "stage": "High Risk",
                "stage_description": "Increased risk for clinically important brain injury"
            }
        }