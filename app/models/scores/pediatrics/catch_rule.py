"""
CATCH (Canadian Assessment of Tomography for Childhood Head injury) Rule Models

Request and response models for CATCH Rule calculation.

References (Vancouver style):
1. Osmond MH, Klassen TP, Wells GA, Correll R, Jarvis A, Joubert G, et al; Pediatric Emergency Research Canada (PERC). CATCH: a clinical decision rule for the use of computed tomography in children with minor head injury. CMAJ. 2010 Mar 9;182(4):341-8. doi: 10.1503/cmaj.091421.
2. Lyttle MD, Crowe L, Oakley E, Dunning J, Babl FE. Comparing CATCH, CHALICE and PECARN clinical decision rules for paediatric head injuries. Emerg Med J. 2012 Oct;29(10):785-94. doi: 10.1136/emermed-2011-200225.
3. Easter JS, Bakes K, Dhaliwal J, Miller M, Caruso E, Haukoos JS. Comparison of PECARN, CATCH, and CHALICE rules for children with minor head injury: a prospective cohort study. Ann Emerg Med. 2014 Aug;64(2):145-52, 152.e1-5. doi: 10.1016/j.annemergmed.2014.01.030.

The CATCH (Canadian Assessment of Tomography for Childhood Head injury) Rule predicts clinically significant head injuries in children aged 0-16 years to guide CT imaging decisions.

INCLUSION CRITERIA (all required):
- Initial Glasgow Coma Scale (GCS) ≥13
- Injury within 24 hours
- At least one of: witnessed loss of consciousness, definite amnesia, witnessed disorientation, vomiting ≥2 times (15+ minutes apart), or persistent irritability (children <2 years)

HIGH-RISK FACTORS (need for neurologic intervention):
- GCS <15 at two hours after injury
- Suspected open or depressed skull fracture
- History of worsening headache
- Irritability on examination

MEDIUM-RISK FACTORS (brain injury on CT):
- Signs of basal skull fracture (hemotympanum, raccoon eyes, CSF otorrhea/rhinorrhea)
- Large, boggy scalp hematoma (frontal, temporal, or parietal region)
- Dangerous mechanism of injury (MVC >60 km/h, fall >3 feet or 5 stairs, axial load to head)

CLINICAL PERFORMANCE:
- High-risk factors: 100% sensitive for neurologic intervention, 70.2% specific
- Medium-risk factors: 98.1% sensitive for brain injury on CT, 50.1% specific
- Developed from study of 3,866 children with minor head injury

IMPORTANT NOTE: PECARN rule is often preferred due to more extensive validation, especially for children under 2 years. Clinical judgment should always supplement decision rules in pediatric head trauma.
"""

from pydantic import BaseModel, Field
from typing import Literal


class CatchRuleRequest(BaseModel):
    """
    Request model for CATCH Rule for pediatric head injury assessment
    
    The CATCH Rule helps determine which children with minor head injury require CT imaging
    by stratifying risk into high-risk (neurologic intervention) and medium-risk (brain injury on CT) categories.
    
    INCLUSION CRITERIA:
    - Age 0-16 years with minor head injury
    - Initial GCS ≥13, injury within 24 hours
    - Must have: witnessed LOC, amnesia, disorientation, vomiting ≥2x, or irritability
    
    HIGH-RISK FACTORS (need for neurologic intervention):
    - GCS <15 at 2 hours after injury
    - Suspected open or depressed skull fracture
    - History of worsening headache
    - Irritability on examination
    
    MEDIUM-RISK FACTORS (brain injury on CT):
    - Signs of basal skull fracture
    - Large, boggy scalp hematoma
    - Dangerous mechanism of injury
    
    Clinical Performance:
    - High-risk factors: 100% sensitive for neurologic intervention
    - Medium-risk factors: 98.1% sensitive for brain injury on CT
    
    References (Vancouver style):
    1. Osmond MH, Klassen TP, Wells GA, Correll R, Jarvis A, Joubert G, et al; Pediatric Emergency Research Canada (PERC). CATCH: a clinical decision rule for the use of computed tomography in children with minor head injury. CMAJ. 2010 Mar 9;182(4):341-8. doi: 10.1503/cmaj.091421.
    2. Lyttle MD, Crowe L, Oakley E, Dunning J, Babl FE. Comparing CATCH, CHALICE and PECARN clinical decision rules for paediatric head injuries. Emerg Med J. 2012 Oct;29(10):785-94. doi: 10.1136/emermed-2011-200225.
    3. Easter JS, Bakes K, Dhaliwal J, Miller M, Caruso E, Haukoos JS. Comparison of PECARN, CATCH, and CHALICE rules for children with minor head injury: a prospective cohort study. Ann Emerg Med. 2014 Aug;64(2):145-52, 152.e1-5. doi: 10.1016/j.annemergmed.2014.01.030.
    """
    
    gcs_less_than_15: Literal["yes", "no"] = Field(
        ...,
        description="HIGH RISK: Glasgow Coma Scale <15 at two hours after injury",
        example="no"
    )
    
    suspected_skull_fracture: Literal["yes", "no"] = Field(
        ...,
        description="HIGH RISK: Suspected open or depressed skull fracture based on clinical examination",
        example="no"
    )
    
    worsening_headache: Literal["yes", "no"] = Field(
        ...,
        description="HIGH RISK: History of worsening headache since injury",
        example="no"
    )
    
    irritability_on_exam: Literal["yes", "no"] = Field(
        ...,
        description="HIGH RISK: Irritability on examination (especially important in young children)",
        example="no"
    )
    
    basal_skull_fracture_signs: Literal["yes", "no"] = Field(
        ...,
        description="MEDIUM RISK: Signs of basal skull fracture (hemotympanum, raccoon eyes, Battle's sign, CSF otorrhea/rhinorrhea)",
        example="no"
    )
    
    large_scalp_hematoma: Literal["yes", "no"] = Field(
        ...,
        description="MEDIUM RISK: Large, boggy scalp hematoma in frontal, temporal, or parietal region",
        example="no"
    )
    
    dangerous_mechanism: Literal["yes", "no"] = Field(
        ...,
        description="MEDIUM RISK: Dangerous mechanism of injury (MVC >60 km/h, fall >3 feet or 5 stairs, axial load to head)",
        example="yes"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "gcs_less_than_15": "no",
                "suspected_skull_fracture": "no", 
                "worsening_headache": "no",
                "irritability_on_exam": "no",
                "basal_skull_fracture_signs": "no",
                "large_scalp_hematoma": "no",
                "dangerous_mechanism": "yes"
            }
        }


class CatchRuleResponse(BaseModel):
    """
    Response model for CATCH Rule pediatric head injury assessment
    
    Returns stratified risk assessment and CT imaging recommendations based on the
    presence of high-risk factors (neurologic intervention) and medium-risk factors (brain injury on CT).
    
    Risk Stratification:
    - High Risk: Any high-risk factor present → CT strongly recommended
    - Medium Risk: Only medium-risk factors present → Consider CT imaging
    - Low Risk: No risk factors present → CT not routinely indicated
    
    The response includes detailed factor assessment showing which specific criteria
    are present, helping clinicians understand the basis for recommendations.
    
    Clinical Actions:
    - High Risk: CT imaging strongly recommended, consider neurosurgical consultation
    - Medium Risk: Consider CT based on clinical judgment
    - Low Risk: Clinical observation, discharge planning per protocols
    
    Reference: Osmond MH, et al. CMAJ. 2010;182(4):341-8.
    """
    
    result: dict = Field(
        ...,
        description="CATCH Rule assessment with risk stratification and detailed factor analysis",
        example={
            "high_risk_factors_present": False,
            "medium_risk_factors_present": True,
            "any_risk_factors_present": True,
            "risk_level": "Medium Risk",
            "ct_recommendation": "Consider CT imaging",
            "factor_assessment": {
                "high_risk": {
                    "gcs_less_than_15": {"present": False, "description": "GCS <15 at 2 hours after injury"},
                    "suspected_skull_fracture": {"present": False, "description": "Suspected open or depressed skull fracture"},
                    "worsening_headache": {"present": False, "description": "History of worsening headache"},
                    "irritability_on_exam": {"present": False, "description": "Irritability on examination"}
                },
                "medium_risk": {
                    "basal_skull_fracture_signs": {"present": False, "description": "Signs of basal skull fracture (hemotympanum, raccoon eyes, CSF leak)"},
                    "large_scalp_hematoma": {"present": False, "description": "Large, boggy scalp hematoma (frontal, temporal, or parietal)"},
                    "dangerous_mechanism": {"present": True, "description": "Dangerous mechanism (MVC >60 km/h, fall >3 feet/5 stairs, axial load)"}
                }
            }
        }
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the assessment",
        example="risk_level"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation and CT imaging recommendations based on CATCH Rule assessment",
        example="Medium risk for brain injury on CT. Consider CT imaging based on clinical judgment. Medium-risk factors identify brain injury on CT with 98.1% sensitivity (95% CI: 94.6%-99.4%). Absence of medium-risk factors has high negative predictive value."
    )
    
    stage: str = Field(
        ...,
        description="Risk category (High Risk, Medium Risk, or Low Risk)",
        example="Medium Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the risk category",
        example="Medium-risk factors present"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "result": {
                    "high_risk_factors_present": False,
                    "medium_risk_factors_present": True,
                    "any_risk_factors_present": True,
                    "risk_level": "Medium Risk",
                    "ct_recommendation": "Consider CT imaging",
                    "factor_assessment": {
                        "high_risk": {
                            "gcs_less_than_15": {"present": False, "description": "GCS <15 at 2 hours after injury"},
                            "suspected_skull_fracture": {"present": False, "description": "Suspected open or depressed skull fracture"},
                            "worsening_headache": {"present": False, "description": "History of worsening headache"},
                            "irritability_on_exam": {"present": False, "description": "Irritability on examination"}
                        },
                        "medium_risk": {
                            "basal_skull_fracture_signs": {"present": False, "description": "Signs of basal skull fracture (hemotympanum, raccoon eyes, CSF leak)"},
                            "large_scalp_hematoma": {"present": False, "description": "Large, boggy scalp hematoma (frontal, temporal, or parietal)"},
                            "dangerous_mechanism": {"present": True, "description": "Dangerous mechanism (MVC >60 km/h, fall >3 feet/5 stairs, axial load)"}
                        }
                    }
                },
                "unit": "risk_level",
                "interpretation": "Medium risk for brain injury on CT. Consider CT imaging based on clinical judgment. Medium-risk factors identify brain injury on CT with 98.1% sensitivity (95% CI: 94.6%-99.4%). Absence of medium-risk factors has high negative predictive value.",
                "stage": "Medium Risk",
                "stage_description": "Medium-risk factors present"
            }
        }