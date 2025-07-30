"""
Cerebral Perfusion Pressure Models

Request and response models for Cerebral Perfusion Pressure calculation.

References (Vancouver style):
1. Carney N, Totten AM, O'Reilly C, Ullman JS, Hawryluk GW, Bell MJ, et al. 
   Guidelines for the management of severe traumatic brain injury, fourth edition. 
   Neurosurgery. 2017;80(1):6-15. doi: 10.1227/NEU.0000000000001432.
2. Kirkman MA, Smith M. Intracranial pressure monitoring, cerebral perfusion 
   pressure estimation, and ICP/CPP-guided therapy: a standard of care or optional 
   extra after brain injury? Br J Anaesth. 2014;112(1):35-46. doi: 10.1093/bja/aet418.
3. Rosner MJ, Rosner SD, Johnson AH. Cerebral perfusion pressure: management 
   protocol and clinical results. J Neurosurg. 1995;83(6):949-62. 
   doi: 10.3171/jns.1995.83.6.0949.
4. Steiner LA, Czosnyka M, Piechnik SK, Smielewski P, Chatfield D, Menon DK, et al. 
   Continuous monitoring of cerebrovascular pressure reactivity allows determination 
   of optimal cerebral perfusion pressure in patients with traumatic brain injury. 
   Crit Care Med. 2002;30(4):733-8. doi: 10.1097/00003246-200204000-00002.

Cerebral Perfusion Pressure (CPP) is the net pressure gradient that drives oxygen 
delivery to cerebral tissue. It represents the pressure available to perfuse the 
brain and is calculated as the difference between mean arterial pressure (MAP) 
and intracranial pressure (ICP).

Formula: CPP = MAP - ICP

Clinical Significance:
- Critical parameter in neurocritical care and traumatic brain injury management
- Guides therapeutic interventions to maintain adequate cerebral blood flow
- Helps prevent secondary brain injury from cerebral ischemia
- Essential for monitoring patients with intracranial hypertension

Normal Values and Interpretation:
- Normal range: 60-80 mmHg
- Optimal for TBI: 60-70 mmHg
- Critical threshold: <50 mmHg (high risk of cerebral ischemia)
- Target maintenance: Avoid CPP <60 mmHg and >100 mmHg when possible

Measurement Requirements:
- MAP: Preferably via arterial line, measured at tragus level
- ICP: Requires invasive monitoring (intraventricular catheter preferred)
- Continuous monitoring preferred over isolated measurements
"""

from pydantic import BaseModel, Field
from typing import Dict, Any


class CerebralPerfusionPressureRequest(BaseModel):
    """
    Request model for Cerebral Perfusion Pressure calculation
    
    Cerebral Perfusion Pressure (CPP) is calculated using two hemodynamic parameters:
    
    Mean Arterial Pressure (MAP):
    - Driving pressure for cerebral blood flow
    - Normal range: 70-100 mmHg
    - Can be measured directly via arterial line (preferred)
    - Can be calculated: MAP = (Systolic BP + 2 × Diastolic BP) ÷ 3
    - Should be measured at the level of the tragus for brain injury patients
    
    Intracranial Pressure (ICP):
    - Pressure opposing cerebral blood flow
    - Normal range: 5-15 mmHg (adults), 3-7 mmHg (children), 1-5 mmHg (infants)
    - Requires invasive monitoring via intraventricular catheter (gold standard)
    - Elevated ICP (>20 mmHg) indicates intracranial hypertension
    
    Clinical Applications:
    - Traumatic brain injury management and monitoring
    - Intracranial hypertension assessment
    - Neurocritical care optimization
    - Post-neurosurgical monitoring
    - Stroke and subarachnoid hemorrhage management
    - Guide therapeutic interventions (vasopressors, ICP reduction)
    
    The calculation provides immediate assessment of cerebral perfusion adequacy
    and guides critical care decisions to prevent secondary brain injury.
    
    References (Vancouver style):
    1. Carney N, Totten AM, O'Reilly C, Ullman JS, Hawryluk GW, Bell MJ, et al. 
    Guidelines for the management of severe traumatic brain injury, fourth edition. 
    Neurosurgery. 2017;80(1):6-15. doi: 10.1227/NEU.0000000000001432.
    2. Kirkman MA, Smith M. Intracranial pressure monitoring, cerebral perfusion 
    pressure estimation, and ICP/CPP-guided therapy: a standard of care or optional 
    extra after brain injury? Br J Anaesth. 2014;112(1):35-46. doi: 10.1093/bja/aet418.
    """
    
    mean_arterial_pressure: float = Field(
        ...,
        ge=30,
        le=200,
        description="Mean arterial pressure (MAP) in mmHg. Preferably measured via arterial line at the level of the tragus. Normal range: 70-100 mmHg",
        example=85.0
    )
    
    intracranial_pressure: float = Field(
        ...,
        ge=0,
        le=80,
        description="Intracranial pressure (ICP) in mmHg. Requires invasive monitoring via intraventricular catheter. Normal range: 5-15 mmHg (adults)",
        example=15.0
    )
    
    class Config:
        schema_extra = {
            "example": {
                "mean_arterial_pressure": 85.0,
                "intracranial_pressure": 15.0
            }
        }


class CerebralPerfusionPressureResponse(BaseModel):
    """
    Response model for Cerebral Perfusion Pressure calculation
    
    Provides comprehensive CPP assessment including:
    - Calculated CPP value (MAP - ICP)
    - Clinical category and risk stratification
    - Management recommendations based on CPP level
    - Detailed calculation breakdown for clinical context
    
    CPP Categories and Clinical Management:
    
    Critical (<30 mmHg):
    - Critical risk of cerebral ischemia and brain death
    - Immediate aggressive intervention required
    - Emergency neurosurgical consultation indicated
    
    Severely Low (30-50 mmHg):
    - High risk of cerebral ischemia and secondary brain injury
    - Urgent intervention needed for cerebral perfusion optimization
    - Consider vasopressor support and ICP reduction measures
    
    Low (50-60 mmHg):
    - Below optimal range with moderate ischemia risk
    - Consider interventions to improve cerebral perfusion
    - Close neurological monitoring required
    
    Optimal (60-80 mmHg):
    - Target range for cerebral perfusion in most patients
    - Maintain current management with continued monitoring
    - Preferred range for traumatic brain injury management
    
    Adequate (80-100 mmHg):
    - Adequate perfusion with monitoring for complications
    - Balance perfusion needs with hemodynamic stability
    
    High (>100 mmHg):
    - Risk of complications from elevated pressures
    - Monitor for cerebral edema and respiratory complications
    - Balance perfusion needs with pressure management
    
    Clinical Impact: CPP-guided therapy has been shown to improve outcomes 
    in traumatic brain injury and other neurocritical conditions by maintaining 
    adequate cerebral blood flow while preventing secondary brain injury.
    
    Reference: Carney N, et al. Neurosurgery. 2017;80(1):6-15.
    """
    
    result: Dict[str, Any] = Field(
        ...,
        description="Detailed CPP assessment including value, clinical category, and management recommendations",
        example={
            "cpp_value": 70.0,
            "map_value": 85.0,
            "icp_value": 15.0,
            "clinical_category": "Optimal",
            "risk_level": "Low Risk",
            "urgency": "Maintain current management",
            "is_adequate": True,
            "is_critical": False,
            "management_recommendations": {
                "primary_interventions": [
                    "Maintain current management",
                    "Continue monitoring CPP trends",
                    "Optimize other neurological parameters"
                ],
                "monitoring": [
                    "Continuous CPP monitoring preferred",
                    "Monitor neurological examinations",
                    "Assess cerebral autoregulation if possible",
                    "Consider individual patient factors (age, comorbidities)"
                ],
                "considerations": []
            },
            "calculation_breakdown": {
                "formula": "CPP = MAP - ICP",
                "components": {
                    "mean_arterial_pressure": {
                        "value": 85.0,
                        "unit": "mmHg",
                        "normal_range": "70-100 mmHg",
                        "description": "Driving pressure for cerebral blood flow"
                    },
                    "intracranial_pressure": {
                        "value": 15.0,
                        "unit": "mmHg",
                        "normal_range": "5-15 mmHg (adults)",
                        "description": "Pressure opposing cerebral blood flow"
                    }
                },
                "result": {
                    "cpp_value": 70.0,
                    "unit": "mmHg",
                    "normal_range": "60-80 mmHg",
                    "critical_threshold": "<50 mmHg"
                },
                "clinical_context": {
                    "autoregulation_range": "50-150 mmHg (healthy brain)",
                    "tbi_target_range": "60-70 mmHg",
                    "measurement_notes": "MAP measured at tragus level, ICP via invasive monitoring"
                }
            }
        }
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for cerebral perfusion pressure",
        example="mmHg"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation with risk assessment and management recommendations",
        example="CPP 70.0 mmHg: Optimal range for cerebral perfusion in most patients. Maintain current management strategies while continuing to monitor for changes. Target range for TBI management."
    )
    
    stage: str = Field(
        ...,
        description="Clinical category (Critical, Severely Low, Low, Optimal, Adequate, High)",
        example="Optimal"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the CPP category",
        example="Target range for cerebral perfusion"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": {
                    "cpp_value": 70.0,
                    "map_value": 85.0,
                    "icp_value": 15.0,
                    "clinical_category": "Optimal",
                    "risk_level": "Low Risk",
                    "urgency": "Maintain current management",
                    "is_adequate": True,
                    "is_critical": False,
                    "management_recommendations": {
                        "primary_interventions": [
                            "Maintain current management",
                            "Continue monitoring CPP trends",
                            "Optimize other neurological parameters"
                        ],
                        "monitoring": [
                            "Continuous CPP monitoring preferred",
                            "Monitor neurological examinations",
                            "Assess cerebral autoregulation if possible",
                            "Consider individual patient factors (age, comorbidities)"
                        ],
                        "considerations": []
                    },
                    "calculation_breakdown": {
                        "formula": "CPP = MAP - ICP",
                        "components": {
                            "mean_arterial_pressure": {
                                "value": 85.0,
                                "unit": "mmHg",
                                "normal_range": "70-100 mmHg",
                                "description": "Driving pressure for cerebral blood flow"
                            },
                            "intracranial_pressure": {
                                "value": 15.0,
                                "unit": "mmHg",
                                "normal_range": "5-15 mmHg (adults)",
                                "description": "Pressure opposing cerebral blood flow"
                            }
                        },
                        "result": {
                            "cpp_value": 70.0,
                            "unit": "mmHg",
                            "normal_range": "60-80 mmHg",
                            "critical_threshold": "<50 mmHg"
                        },
                        "clinical_context": {
                            "autoregulation_range": "50-150 mmHg (healthy brain)",
                            "tbi_target_range": "60-70 mmHg",
                            "measurement_notes": "MAP measured at tragus level, ICP via invasive monitoring"
                        }
                    }
                },
                "unit": "mmHg",
                "interpretation": "CPP 70.0 mmHg: Optimal range for cerebral perfusion in most patients. Maintain current management strategies while continuing to monitor for changes. Target range for TBI management.",
                "stage": "Optimal",
                "stage_description": "Target range for cerebral perfusion"
            }
        }