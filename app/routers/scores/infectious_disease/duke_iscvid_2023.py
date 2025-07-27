"""
2023 Duke-ISCVID Criteria Router

Endpoint for calculating 2023 Duke-ISCVID Criteria for infective endocarditis.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.infectious_disease.duke_iscvid_2023 import (
    DukeIscvid2023Request,
    DukeIscvid2023Response
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post("/duke_iscvid_2023", response_model=DukeIscvid2023Response)
async def calculate_duke_iscvid_2023(request: DukeIscvid2023Request):
    """
    Calculates 2023 Duke-ISCVID Criteria for Infective Endocarditis
    
    Updated diagnostic criteria for infective endocarditis incorporating modern 
    diagnostic techniques including PET/CT imaging and molecular diagnostics.
    Provides improved sensitivity and specificity over original Duke criteria.
    
    Args:
        request: Parameters including major criteria (microbiologic, imaging, surgical),
                minor criteria (predisposing conditions, clinical manifestations),
                and pathologic criteria
        
    Returns:
        DukeIscvid2023Response: Diagnosis result with clinical interpretation
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("duke_iscvid_2023", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating 2023 Duke-ISCVID Criteria",
                    "details": {"parameters": parameters}
                }
            )
        
        return DukeIscvid2023Response(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for 2023 Duke-ISCVID Criteria",
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