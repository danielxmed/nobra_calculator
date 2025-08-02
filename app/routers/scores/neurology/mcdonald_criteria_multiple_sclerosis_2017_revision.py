"""
McDonald Criteria for Multiple Sclerosis (2017 Revision) Router

Endpoint for diagnosing multiple sclerosis using 2017 McDonald Criteria.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.neurology.mcdonald_criteria_multiple_sclerosis_2017_revision import (
    McdonaldCriteriaMultipleSclerosis2017RevisionRequest,
    McdonaldCriteriaMultipleSclerosis2017RevisionResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/mcdonald_criteria_multiple_sclerosis_2017_revision",
    response_model=McdonaldCriteriaMultipleSclerosis2017RevisionResponse,
    summary="Diagnose Multiple Sclerosis using McDonald Criteria (2017 Revision)",
    description="Applies the McDonald Criteria for Multiple Sclerosis (2017 Revision) to diagnose MS "
                "using clinical attacks, objective clinical evidence, MRI findings, and CSF analysis. "
                "The 2017 revision represents the current gold standard for MS diagnosis, introducing "
                "key innovations including the use of CSF oligoclonal bands to substitute for "
                "dissemination in time when dissemination in space is demonstrated, acceptance of "
                "cortical lesions for DIS criteria, and inclusion of symptomatic brainstem/spinal "
                "cord lesions. This diagnostic framework systematically evaluates six critical "
                "parameters: number of clinical attacks (inflammatory demyelinating CNS events "
                "lasting ≥24 hours), lesions with objective clinical evidence (neurological exam "
                "abnormalities, visual evoked potentials, or MRI correlation), dissemination in "
                "space (lesions in ≥2 of 4 CNS locations), dissemination in time (disease progression "
                "evidence), CSF oligoclonal bands (≥2 bands in CSF not in serum), and exclusion of "
                "alternative diagnoses. The calculator provides three diagnostic outcomes: MS Diagnosed "
                "(criteria fulfilled, initiate disease-modifying therapy), Possible MS (suggestive "
                "findings but incomplete criteria, continue monitoring), or MS Not Diagnosed (criteria "
                "not met, consider alternatives). This tool facilitates earlier diagnosis while "
                "preserving specificity, reducing misdiagnosis rates, and enabling timely therapeutic "
                "intervention to improve long-term patient outcomes in multiple sclerosis management.",
    response_description="The MS diagnosis with detailed criteria evaluation and clinical management recommendations",
    operation_id="mcdonald_criteria_multiple_sclerosis_2017_revision"
)
async def calculate_mcdonald_criteria_multiple_sclerosis_2017_revision(request: McdonaldCriteriaMultipleSclerosis2017RevisionRequest):
    """
    Diagnoses Multiple Sclerosis using McDonald Criteria (2017 Revision)
    
    The McDonald Criteria for Multiple Sclerosis (2017 Revision) provide the current 
    gold standard diagnostic framework for MS, systematically evaluating clinical, 
    radiological, and laboratory evidence to enable accurate and timely diagnosis.
    
    Args:
        request: McDonald Criteria parameters including clinical attacks, objective evidence, 
                DIS/DIT demonstration, CSF oligoclonal bands, and alternative diagnosis exclusion
        
    Returns:
        McdonaldCriteriaMultipleSclerosis2017RevisionResponse: MS diagnosis with detailed 
        criteria evaluation and management recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("mcdonald_criteria_multiple_sclerosis_2017_revision", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error evaluating McDonald Criteria for Multiple Sclerosis (2017 Revision)",
                    "details": {"parameters": parameters}
                }
            )
        
        return McdonaldCriteriaMultipleSclerosis2017RevisionResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for McDonald Criteria for Multiple Sclerosis (2017 Revision)",
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