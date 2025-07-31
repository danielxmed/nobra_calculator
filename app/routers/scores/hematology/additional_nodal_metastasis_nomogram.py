"""
Additional Nodal Metastasis Nomogram Router

Endpoint for calculating Additional Nodal Metastasis Nomogram.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.hematology.additional_nodal_metastasis_nomogram import (
    AdditionalNodalMetastasisNomogramRequest,
    AdditionalNodalMetastasisNomogramResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/additional_nodal_metastasis_nomogram",
    response_model=AdditionalNodalMetastasisNomogramResponse,
    summary="Calculate Additional Nodal Metastasis Nomogram",
    description="Predicts probability of additional non-sentinel lymph node metastases in breast cancer patients with a positive sentinel node biopsy",
    response_description="The calculated additional nodal metastasis nomogram with interpretation",
    operation_id="additional_nodal_metastasis_nomogram"
)
async def calculate_additional_nodal_metastasis_nomogram(request: AdditionalNodalMetastasisNomogramRequest):
    """
    Calculates Additional Nodal Metastasis Nomogram
    
    Predicts the probability of additional non-sentinel lymph node metastases in 
    breast cancer patients with a positive sentinel lymph node biopsy. This nomogram 
    was developed at Memorial Sloan Kettering Cancer Center and helps guide clinical 
    decision-making regarding the need for completion axillary lymph node dissection.
    
    The calculation considers:
    - Tumor characteristics (grade, size, ER status, LVI, multifocality)
    - Sentinel lymph node information (number positive/negative, detection method)
    
    Results are stratified into risk categories to guide treatment decisions:
    - Very Low Risk (<10%): Consider omitting completion ALND
    - Low Risk (10-20%): Clinical decision incorporating patient factors  
    - Moderate Risk (20-50%): Consider completion ALND or axillary radiation
    - High Risk (>50%): Strong consideration for completion ALND or axillary radiation
    
    Args:
        request: Parameters needed for nomogram calculation
        
    Returns:
        AdditionalNodalMetastasisNomogramResponse: Probability with clinical interpretation
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("additional_nodal_metastasis_nomogram", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Additional Nodal Metastasis Nomogram",
                    "details": {"parameters": parameters}
                }
            )
        
        return AdditionalNodalMetastasisNomogramResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Additional Nodal Metastasis Nomogram",
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