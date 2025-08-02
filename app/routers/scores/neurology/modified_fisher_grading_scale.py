"""
Modified Fisher Grading Scale for Subarachnoid Hemorrhage Router

Endpoint for assessing aneurysmal SAH severity and predicting vasospasm risk.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.neurology.modified_fisher_grading_scale import (
    ModifiedFisherGradingScaleRequest,
    ModifiedFisherGradingScaleResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/modified_fisher_grading_scale",
    response_model=ModifiedFisherGradingScaleResponse,
    summary="Calculate Modified Fisher Grading Scale for SAH",
    description="""Calculates the Modified Fisher Grading Scale for aneurysmal subarachnoid hemorrhage (SAH) to assess severity and predict vasospasm risk based on CT scan findings.

The Modified Fisher Grading Scale improves upon the original Fisher scale by providing better prediction of symptomatic vasospasm after aneurysmal subarachnoid hemorrhage. This validated radiographic assessment tool helps healthcare providers:

- Stratify vasospasm risk from 0% to 40% based on CT findings
- Guide intensity of neurological monitoring and surveillance
- Inform decisions about prophylactic interventions (nimodipine)
- Predict likelihood of delayed cerebral ischemia

**Assessment Parameters:**
- **SAH Thickness**: Measured on CT scan as thin (<1mm) or thick (≥1mm)
- **Intraventricular Hemorrhage (IVH)**: Presence or absence of blood in ventricular system

**Grading System:**
- **Grade 0**: No SAH present (0% vasospasm risk)
- **Grade 1**: Focal/thin SAH, no IVH (6-24% vasospasm risk)
- **Grade 2**: Focal/thin SAH with IVH (15-33% vasospasm risk)
- **Grade 3**: Focal/thick SAH, no IVH (33-35% vasospasm risk)
- **Grade 4**: Focal/thick SAH with IVH (34-40% vasospasm risk)

**Clinical Applications:**
- Only applies to aneurysmal subarachnoid hemorrhage (not traumatic or AVM-related)
- Should be assessed on initial non-contrast head CT scan
- Higher grades warrant intensive monitoring and prophylactic measures
- Guides decisions about angiographic surveillance and intervention timing

**Advantages over Original Fisher Scale:**
- Progressive increase in vasospasm risk with each grade
- Better prediction of symptomatic vasospasm
- Accounts for combined thick SAH and intraventricular hemorrhage""",
    response_description="The calculated Modified Fisher grade with vasospasm risk assessment and evidence-based monitoring recommendations",
    operation_id="modified_fisher_grading_scale"
)
async def calculate_modified_fisher_grading_scale(request: ModifiedFisherGradingScaleRequest):
    """
    Calculates Modified Fisher Grading Scale for Subarachnoid Hemorrhage
    
    Assesses aneurysmal SAH severity based on CT findings to predict vasospasm risk
    and guide clinical monitoring and intervention strategies.
    
    Args:
        request: SAH thickness and intraventricular hemorrhage parameters from CT scan
        
    Returns:
        ModifiedFisherGradingScaleResponse: Modified Fisher grade with vasospasm risk and management recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("modified_fisher_grading_scale", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Modified Fisher Grading Scale",
                    "details": {"parameters": parameters}
                }
            )
        
        return ModifiedFisherGradingScaleResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Modified Fisher Grading Scale",
                "details": {"error": str(e)}
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "error": "InternalServerError",
                "message": "Internal error in calculation",
                "details": {"error": str(e)}
            }
        )