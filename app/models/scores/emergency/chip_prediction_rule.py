"""
CHIP (CT in Head Injury Patients) Prediction Rule Models

Request and response models for CHIP prediction rule calculation.

References (Vancouver style):
1. Smits M, Dippel DW, Steyerberg EW, de Haan GG, Dekker HM, Vos PE, et al. 
   Predicting intracranial traumatic findings on computed tomography in patients 
   with minor head injury: the CHIP prediction rule. Ann Intern Med. 2007 Mar 
   6;146(6):397-405.
2. Smits M, Dippel DW, de Haan GG, Dekker HM, Vos PE, Kool DR, et al. External 
   validation of the Canadian CT Head Rule and the New Orleans Criteria for CT 
   scanning in patients with minor head injury. JAMA. 2005 Sep 28;294(12):1519-25.
3. van den Brand CL, Rambach AH, Postma K, et al. Update of the CHIP (CT in Head 
   Injury Patients) decision rule for patients with minor head injury based on a 
   multicenter consecutive case series. Emerg Med J. 2022 Dec;39(12):897-902.

The CHIP (CT in Head Injury Patients) Prediction Rule is a validated clinical 
decision tool designed to guide CT imaging decisions in patients with minor head 
trauma. Developed in the Netherlands and externally validated, this rule helps 
clinicians identify patients at risk for intracranial traumatic findings while 
minimizing unnecessary radiation exposure and healthcare costs.

CHIP Rule Structure:

The rule divides clinical criteria into two categories with different decision thresholds:

Major Criteria (Any ONE present → CT recommended):
These criteria represent high-risk factors with significant association to intracranial injury:

1. Pedestrian/cyclist vs. vehicle collision: High-energy mechanism with substantial risk
2. Ejected from vehicle: Indicates severe trauma mechanism  
3. Vomiting: Post-traumatic vomiting suggests increased intracranial pressure
4. Post-traumatic amnesia ≥4 hours: Extended amnesia indicates significant brain injury
5. Clinical signs of skull fracture: Physical examination findings suggesting fracture
6. GCS <15: Decreased level of consciousness
7. GCS deterioration ≥2 points: Significant neurological decline
8. Anticoagulant use: Increased bleeding risk with minor trauma
9. Post-traumatic seizure: Indicates cortical irritation/injury
10. Age ≥60 years: Advanced age increases intracranial injury risk

Minor Criteria (TWO OR MORE present → CT recommended):
These criteria represent moderate risk factors requiring combination for CT indication:

1. Fall from any elevation: Mechanism suggesting potential head impact
2. Persistent anterograde amnesia: Ongoing memory formation difficulty
3. Post-traumatic amnesia 2-<4 hours: Moderate duration memory loss
4. Skull contusion: Visible external trauma to head
5. Neurologic deficit: Any focal neurological finding
6. Loss of consciousness: Any period of unconsciousness
7. GCS deterioration of 1 point: Mild neurological decline
8. Age 40-60 years: Intermediate age risk factor

Clinical Implementation:

Target Population:
- Adults ≥16 years of age
- Minor head injury (GCS 13-15)
- Within 24 hours of blunt head trauma
- Patients being considered for CT imaging

Decision Framework:
- Any major criterion present → CT recommended
- ≥2 minor criteria present → CT recommended  
- 1 minor criterion only → Clinical judgment
- No criteria present → CT not indicated

Performance Characteristics:
- Original study: 100% sensitivity for neurosurgical interventions
- Specificity: 23-30% (reduces unnecessary CTs)
- Negative predictive value: Very high for clinically important injuries
- Validated across multiple healthcare systems

Clinical Applications:
- Emergency department evaluation of head trauma
- Reduction of unnecessary CT imaging
- Standardized approach to minor head injury
- Risk stratification for intracranial injury
- Quality improvement in trauma care
- Medical-legal documentation support

Limitations and Considerations:
- Not validated for pediatric populations (use PECARN or CHALICE)
- Requires clinical judgment integration
- Based on Dutch healthcare system validation
- May not account for all individual patient factors
- Should complement, not replace, physician assessment
"""

from pydantic import BaseModel, Field
from typing import Literal, Dict, Any, List


class ChipPredictionRuleRequest(BaseModel):
    """
    Request model for CHIP (CT in Head Injury Patients) Prediction Rule
    
    The CHIP prediction rule uses clinical criteria to guide CT imaging decisions 
    in adults with minor head trauma. The rule categorizes risk factors into major 
    and minor criteria with specific decision thresholds for CT recommendation.
    
    Major Criteria Assessment (Any ONE triggers CT recommendation):
    
    High-Energy Mechanism Factors:
    These criteria represent trauma mechanisms associated with significant force 
    and higher likelihood of intracranial injury.
    
    Pedestrian/Cyclist vs. Vehicle:
    Collision between pedestrian or cyclist and motor vehicle represents high-energy 
    mechanism with substantial risk for intracranial injury due to significant force 
    transmission and potential for multiple impact sites.
    
    Ejected from Vehicle:
    Patient ejection from vehicle during motor vehicle accident indicates extremely 
    high-energy mechanism with multiple trauma potential and very high risk for brain injury.
    
    Neurological Indicators:
    These criteria represent direct evidence of brain dysfunction or injury.
    
    Post-traumatic Vomiting:
    Vomiting following head trauma may indicate increased intracranial pressure, 
    brain stem dysfunction, or vestibular injury, warranting immediate imaging evaluation.
    
    Extended Amnesia (≥4 hours):
    Post-traumatic amnesia lasting 4 hours or longer indicates significant brain 
    injury affecting memory formation and consolidation processes.
    
    Glasgow Coma Scale <15:
    Any depression in level of consciousness below normal (GCS 15) indicates 
    neurological impairment requiring immediate assessment for intracranial pathology.
    
    GCS Deterioration ≥2 points:
    Significant neurological decline suggests progressive intracranial pathology 
    such as expanding hematoma or increasing cerebral edema.
    
    Physical Examination Findings:
    Direct evidence of skull injury or neurological dysfunction.
    
    Clinical Signs of Skull Fracture:
    Physical examination findings suggesting skull fracture including palpable 
    step-off, depressed areas, or other signs of bony injury.
    
    Post-traumatic Seizure:
    Seizure activity following head trauma indicates cortical irritation or injury 
    requiring immediate evaluation for underlying structural abnormalities.
    
    Patient Factors:
    Individual characteristics affecting bleeding risk and injury susceptibility.
    
    Anticoagulant Use:
    Current anticoagulation therapy significantly increases risk of intracranial 
    hemorrhage even with minor trauma mechanisms.
    
    Age ≥60 Years:
    Advanced age increases risk of intracranial injury due to brain atrophy, 
    increased subdural space, and fragile bridging veins.
    
    Minor Criteria Assessment (TWO OR MORE trigger CT recommendation):
    
    Mechanism and Historical Factors:
    These represent moderate risk factors requiring combination for significance.
    
    Fall from Elevation:
    Any fall from height (including from standing) represents mechanism with 
    potential for head impact and brain injury.
    
    Memory and Consciousness:
    Indicators of brain dysfunction that may suggest underlying injury.
    
    Persistent Anterograde Amnesia:
    Ongoing difficulty forming new memories indicates hippocampal dysfunction 
    or more widespread brain injury.
    
    Moderate Amnesia (2-<4 hours):
    Post-traumatic amnesia of intermediate duration suggesting moderate brain 
    injury affecting memory processes.
    
    Loss of Consciousness:
    Any period of unconsciousness, regardless of duration, indicates brain 
    dysfunction that may be associated with structural injury.
    
    Physical and Neurological Findings:
    External signs of trauma and neurological dysfunction.
    
    Skull Contusion:
    Visible external trauma to head including bruising, swelling, or lacerations 
    suggesting significant impact to skull.
    
    Neurologic Deficit:
    Any focal neurological finding including motor weakness, sensory loss, 
    cranial nerve dysfunction, or coordination problems.
    
    Mild Neurological Change:
    
    GCS Deterioration of 1 Point:
    Mild decline in neurological status that may indicate developing intracranial 
    pathology requiring monitoring and potential intervention.
    
    Age Factor:
    
    Age 40-60 Years:
    Intermediate age range with moderately increased risk for intracranial injury 
    compared to younger patients.
    
    Clinical Decision Integration:
    
    Risk Stratification:
    - High risk: Any major criterion present
    - Moderate-high risk: ≥2 minor criteria present
    - Low-moderate risk: 1 minor criterion present
    - Low risk: No criteria present
    
    Clinical Judgment Considerations:
    - Patient and family preferences
    - Availability of CT imaging
    - Ability for close observation
    - Presence of other concerning factors
    - Medical-legal considerations
    
    Quality Measures:
    - Appropriate CT utilization
    - Missed injury rates
    - Patient safety outcomes
    - Resource utilization efficiency
    
    References (Vancouver style):
    1. Smits M, Dippel DW, Steyerberg EW, de Haan GG, Dekker HM, Vos PE, et al. 
    Predicting intracranial traumatic findings on computed tomography in patients 
    with minor head injury: the CHIP prediction rule. Ann Intern Med. 2007 Mar 
    6;146(6):397-405.
    2. van den Brand CL, Rambach AH, Postma K, et al. Update of the CHIP (CT in Head 
    Injury Patients) decision rule for patients with minor head injury based on a 
    multicenter consecutive case series. Emerg Med J. 2022 Dec;39(12):897-902.
    """
    
    # Major Criteria (any one present → CT recommended)
    pedestrian_cyclist_vehicle: Literal["yes", "no"] = Field(
        ...,
        description="Pedestrian or cyclist struck by vehicle. High-energy mechanism with substantial intracranial injury risk",
        example="no"
    )
    
    ejected_from_vehicle: Literal["yes", "no"] = Field(
        ...,
        description="Patient ejected from vehicle during accident. Indicates extremely high-energy trauma mechanism",
        example="no"
    )
    
    vomiting: Literal["yes", "no"] = Field(
        ...,
        description="Post-traumatic vomiting. May indicate increased intracranial pressure or brain stem dysfunction",
        example="no"
    )
    
    amnesia_4_hours_or_more: Literal["yes", "no"] = Field(
        ...,
        description="Post-traumatic amnesia ≥4 hours. Extended amnesia indicates significant brain injury",
        example="no"
    )
    
    clinical_skull_fracture: Literal["yes", "no"] = Field(
        ...,
        description="Clinical signs of skull fracture. Physical examination findings suggesting bony injury",
        example="no"
    )
    
    gcs_less_than_15: Literal["yes", "no"] = Field(
        ...,
        description="Glasgow Coma Scale <15. Any depression in consciousness level below normal",
        example="no"
    )
    
    gcs_deterioration_2_points: Literal["yes", "no"] = Field(
        ...,
        description="GCS deterioration ≥2 points. Significant neurological decline suggesting progressive pathology",
        example="no"
    )
    
    anticoagulant_use: Literal["yes", "no"] = Field(
        ...,
        description="Current anticoagulant medication use. Increases intracranial hemorrhage risk with minor trauma",
        example="no"
    )
    
    post_traumatic_seizure: Literal["yes", "no"] = Field(
        ...,
        description="Post-traumatic seizure. Indicates cortical irritation or injury",
        example="no"
    )
    
    age_60_or_older: Literal["yes", "no"] = Field(
        ...,
        description="Age ≥60 years. Advanced age increases intracranial injury risk due to brain atrophy",
        example="no"
    )
    
    # Minor Criteria (≥2 present → CT recommended)
    fall_from_elevation: Literal["yes", "no"] = Field(
        ...,
        description="Fall from any elevation. Mechanism with potential for head impact and brain injury",
        example="yes"
    )
    
    anterograde_amnesia: Literal["yes", "no"] = Field(
        ...,
        description="Persistent anterograde amnesia. Ongoing difficulty forming new memories",
        example="no"
    )
    
    amnesia_2_to_4_hours: Literal["yes", "no"] = Field(
        ...,
        description="Post-traumatic amnesia 2-<4 hours. Moderate duration memory loss",
        example="no"
    )
    
    skull_contusion: Literal["yes", "no"] = Field(
        ...,
        description="Skull contusion present. Visible external trauma including bruising or swelling",
        example="yes"
    )
    
    neurologic_deficit: Literal["yes", "no"] = Field(
        ...,
        description="Neurologic deficit present. Any focal neurological finding",
        example="no"
    )
    
    loss_of_consciousness: Literal["yes", "no"] = Field(
        ...,
        description="Loss of consciousness. Any period of unconsciousness regardless of duration",
        example="no"
    )
    
    gcs_deterioration_1_point: Literal["yes", "no"] = Field(
        ...,
        description="GCS deterioration of 1 point. Mild neurological decline",
        example="no"
    )
    
    age_40_to_60: Literal["yes", "no"] = Field(
        ...,
        description="Age 40-60 years. Intermediate age range with moderately increased injury risk",
        example="no"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "pedestrian_cyclist_vehicle": "no",
                "ejected_from_vehicle": "no",
                "vomiting": "no",
                "amnesia_4_hours_or_more": "no",
                "clinical_skull_fracture": "no",
                "gcs_less_than_15": "no",
                "gcs_deterioration_2_points": "no",
                "anticoagulant_use": "no",
                "post_traumatic_seizure": "no",
                "age_60_or_older": "no",
                "fall_from_elevation": "yes",
                "anterograde_amnesia": "no",
                "amnesia_2_to_4_hours": "no",
                "skull_contusion": "yes",
                "neurologic_deficit": "no",
                "loss_of_consciousness": "no",
                "gcs_deterioration_1_point": "no",
                "age_40_to_60": "no"
            }
        }


class ChipPredictionRuleResponse(BaseModel):
    """
    Response model for CHIP (CT in Head Injury Patients) Prediction Rule
    
    The CHIP response provides evidence-based CT imaging recommendations with 
    detailed clinical rationale for emergency department evaluation of minor 
    head trauma patients. The rule stratifies patients into risk categories 
    with specific management guidance.
    
    CT Recommendation Categories:
    
    CT Recommended (High Risk):
    - Triggers: Any major criterion OR ≥2 minor criteria present
    - Clinical significance: High likelihood of intracranial traumatic findings
    - Management: Proceed with CT imaging immediately
    - Follow-up: Neurosurgical consultation if positive findings
    - Disposition: Based on CT results and clinical condition
    
    Clinical Judgment (Low-Moderate Risk):
    - Triggers: Exactly 1 minor criterion present
    - Clinical significance: Low to moderate risk requiring individual assessment
    - Management: Consider CT based on clinical factors, patient preferences
    - Considerations: Ability for observation, patient reliability, other risk factors
    - Follow-up: Close observation if CT deferred, clear return instructions
    
    CT Not Indicated (Low Risk):
    - Triggers: No major or minor criteria present
    - Clinical significance: Very low risk for intracranial injury
    - Management: Clinical observation, discharge planning
    - Follow-up: Standard head injury precautions and return instructions
    - Quality: Appropriate resource utilization
    
    Clinical Implementation Framework:
    
    Emergency Department Workflow:
    - Initial assessment and history taking
    - Systematic evaluation of CHIP criteria
    - Risk stratification based on criteria present
    - Clinical decision-making integration
    - Patient and family counseling
    - Appropriate disposition planning
    
    Quality Improvement Applications:
    - Standardized approach to minor head trauma
    - Reduction in unnecessary CT imaging
    - Improved resource utilization
    - Enhanced clinical documentation
    - Risk management and patient safety
    - Performance metrics and benchmarking
    
    Patient Communication:
    - Explanation of risk assessment findings
    - Discussion of CT recommendation rationale
    - Shared decision-making when appropriate
    - Clear instructions for observation or follow-up
    - Head injury precautions and return criteria
    
    Clinical Context Considerations:
    
    Risk-Benefit Assessment:
    - Radiation exposure vs. diagnostic benefit
    - Patient age and developmental considerations
    - Available resources and imaging capability
    - Time constraints and emergency department flow
    - Patient preferences and values
    
    Integration with Clinical Judgment:
    - Rule provides framework, not replacement for assessment
    - Individual patient factors may override rule recommendations
    - Clinical experience and gestalt remain important
    - Medical-legal considerations in decision-making
    - Documentation of rationale for decisions
    
    Limitations and Special Considerations:
    - Not validated for pediatric populations
    - Based on Dutch healthcare system validation
    - May not account for all individual risk factors
    - Requires appropriate clinical interpretation
    - Should be updated with new evidence as available
    
    Reference: Smits M, et al. Ann Intern Med. 2007;146(6):397-405.
    """
    
    result: Dict[str, Any] = Field(
        ...,
        description="Comprehensive CHIP assessment including CT recommendation, risk stratification, and clinical rationale",
        example={
            "recommendation": "CT Recommended",
            "risk_level": "Moderate to High Risk", 
            "major_criteria_count": 0,
            "minor_criteria_count": 2,
            "major_criteria_present": [],
            "minor_criteria_present": [
                "Fall from any elevation",
                "Skull contusion present"
            ],
            "clinical_rationale": "Two or more minor criteria present (2 minor criteria met)",
            "assessment_breakdown": {
                "criteria_analysis": {
                    "major_criteria": {
                        "definition": "Any one major criterion present indicates CT recommended",
                        "count_present": 0,
                        "criteria_met": [],
                        "all_major_criteria": [
                            "Pedestrian or cyclist struck by vehicle",
                            "Patient ejected from vehicle during accident",
                            "Post-traumatic vomiting",
                            "Post-traumatic amnesia ≥4 hours",
                            "Clinical signs of skull fracture",
                            "Glasgow Coma Scale <15",
                            "GCS deterioration ≥2 points",
                            "Current anticoagulant medication use",
                            "Post-traumatic seizure",
                            "Age ≥60 years"
                        ]
                    },
                    "minor_criteria": {
                        "definition": "Two or more minor criteria present indicate CT recommended",
                        "count_present": 2,
                        "criteria_met": [
                            "Fall from any elevation",
                            "Skull contusion present"
                        ]
                    }
                }
            }
        }
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement (empty for decision rules)",
        example=""
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation with CT recommendation and evidence-based rationale",
        example="CHIP Rule: CT RECOMMENDED. 2 minor criteria present indicating moderate to high risk for intracranial traumatic findings. Proceed with CT imaging for evaluation."
    )
    
    stage: str = Field(
        ...,
        description="CT recommendation category (CT Recommended, Clinical Judgment, CT Not Indicated)",
        example="CT Recommended"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the risk level and recommendation",
        example="Moderate to high risk for intracranial injury"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": {
                    "recommendation": "CT Recommended",
                    "risk_level": "Moderate to High Risk",
                    "major_criteria_count": 0,
                    "minor_criteria_count": 2,
                    "major_criteria_present": [],
                    "minor_criteria_present": [
                        "Fall from any elevation",
                        "Skull contusion present"
                    ],
                    "clinical_rationale": "Two or more minor criteria present (2 minor criteria met)",
                    "assessment_breakdown": {
                        "criteria_analysis": {
                            "major_criteria": {
                                "definition": "Any one major criterion present indicates CT recommended",
                                "count_present": 0,
                                "criteria_met": []
                            },
                            "minor_criteria": {
                                "definition": "Two or more minor criteria present indicate CT recommended",
                                "count_present": 2,
                                "criteria_met": [
                                    "Fall from any elevation",
                                    "Skull contusion present"
                                ]
                            }
                        }
                    }
                },
                "unit": "",
                "interpretation": "CHIP Rule: CT RECOMMENDED. 2 minor criteria present indicating moderate to high risk for intracranial traumatic findings. Proceed with CT imaging for evaluation.",
                "stage": "CT Recommended",
                "stage_description": "Moderate to high risk for intracranial injury"
            }
        }