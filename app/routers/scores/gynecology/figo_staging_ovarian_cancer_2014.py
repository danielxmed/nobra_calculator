"""
FIGO Staging for Ovarian Cancer (2014) Router

Endpoint for calculating FIGO staging.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.gynecology.figo_staging_ovarian_cancer_2014 import (
    FigoStagingOvarianCancer2014Request,
    FigoStagingOvarianCancer2014Response
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/figo_staging_ovarian_cancer_2014",
    response_model=FigoStagingOvarianCancer2014Response,
    summary="Calculate FIGO Staging for Ovarian Cancer (2014)",
    description="Stages ovarian, fallopian tube, and peritoneal cancer based on anatomical spread of disease",
    response_description="The calculated figo staging ovarian cancer 2014 with interpretation",
    operation_id="calculate_figo_staging_ovarian_cancer_2014"
)
async def calculate_figo_staging_ovarian_cancer_2014(request: FigoStagingOvarianCancer2014Request):
    """
    Calculates FIGO Staging for Ovarian Cancer (2014)
    
    The FIGO 2014 staging system provides a standardized anatomical classification 
    for ovarian, fallopian tube, and primary peritoneal cancer. It stratifies 
    patients based on the extent of disease spread, which correlates with prognosis 
    and guides treatment decisions.
    
    Args:
        request: Tumor location and extent for FIGO staging
        
    Returns:
        FigoStagingOvarianCancer2014Response: FIGO stage with prognosis and treatment recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("figo_staging_ovarian_cancer_2014", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating FIGO staging",
                    "details": {"parameters": parameters}
                }
            )
        
        return FigoStagingOvarianCancer2014Response(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for FIGO staging",
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