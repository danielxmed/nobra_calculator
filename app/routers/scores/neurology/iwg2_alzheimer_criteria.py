"""
International Working Group (IWG) 2 Criteria for Alzheimer's Disease Diagnosis Router

Endpoint for evaluating IWG-2 AD diagnostic criteria.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.neurology.iwg2_alzheimer_criteria import (
    Iwg2AlzheimerCriteriaRequest,
    Iwg2AlzheimerCriteriaResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/iwg2_alzheimer_criteria",
    response_model=Iwg2AlzheimerCriteriaResponse,
    summary="Evaluate International Working Group (IWG) 2 Criteria for Alzheimer's Disease Diagnosis",
    description="Evaluates the International Working Group (IWG-2) criteria for Alzheimer's disease diagnosis using revised research diagnostic criteria that integrate clinical phenotypes with pathophysiological biomarkers. The IWG-2 criteria represent a major advancement in AD diagnosis by requiring both an appropriate clinical AD phenotype (typical, atypical, mixed, or asymptomatic) and pathophysiological biomarker evidence of Alzheimer pathology. This framework distinguishes between pathophysiological markers (CSF Aβ1-42, T-tau, P-tau, amyloid PET) used for diagnosis and topographical markers (volumetric MRI, FDG-PET) used for progression monitoring. The core diagnostic algorithm requires: Clinical AD phenotype + Pathophysiological biomarker evidence = AD diagnosis. The criteria enable diagnosis across the full disease spectrum from asymptomatic at-risk individuals (positive amyloid biomarkers in cognitively normal patients) to typical AD (characteristic episodic memory impairment), atypical AD (non-amnestic presentations like posterior cortical atrophy or logopenic aphasia), and mixed AD (AD pathology coexisting with other neurodegenerative processes). This diagnostic framework facilitates earlier intervention, appropriate treatment planning, research enrollment, and patient counseling regarding disease prognosis and management strategies.",
    response_description="The IWG-2 diagnostic assessment with clinical recommendations and management guidance",
    operation_id="iwg2_alzheimer_criteria"
)
async def evaluate_iwg2_alzheimer_criteria(request: Iwg2AlzheimerCriteriaRequest):
    """
    Evaluates IWG-2 criteria for Alzheimer's disease diagnosis
    
    Applies the International Working Group revised diagnostic criteria that integrate 
    clinical phenotypes with pathophysiological biomarkers for comprehensive AD diagnosis.
    
    Args:
        request: Clinical and biomarker parameters for IWG-2 evaluation (8 components)
        
    Returns:
        Iwg2AlzheimerCriteriaResponse: Diagnostic assessment with clinical recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("iwg2_alzheimer_criteria", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error evaluating IWG-2 criteria",
                    "details": {"parameters": parameters}
                }
            )
        
        return Iwg2AlzheimerCriteriaResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for IWG-2 criteria",
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
                "message": "Internal error in evaluation",
                "details": {"error": str(e)}
            }
        )