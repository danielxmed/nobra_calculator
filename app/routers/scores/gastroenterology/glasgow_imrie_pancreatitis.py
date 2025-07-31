"""
Glasgow-Imrie Criteria for Severity of Acute Pancreatitis Router

Endpoint for calculating Glasgow-Imrie Criteria for Severity of Acute Pancreatitis.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.gastroenterology.glasgow_imrie_pancreatitis import (
    GlasgowImriePancreatitisRequest,
    GlasgowImriePancreatitisResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/glasgow_imrie_pancreatitis",
    response_model=GlasgowImriePancreatitisResponse,
    summary="Calculate Glasgow-Imrie Criteria for Severity of Acute Pa...",
    description="Clinical scoring system to assess the severity of acute pancreatitis using 8 laboratory and clinical parameters. Helps predict mortality risk and guide management decisions including ICU admission and treatment intensity. Uses the PANCREAS mnemonic for easy recall.",
    response_description="The calculated glasgow imrie pancreatitis with interpretation",
    operation_id="glasgow_imrie_pancreatitis"
)
async def calculate_glasgow_imrie_pancreatitis(request: GlasgowImriePancreatitisRequest):
    """
    Calculates Glasgow-Imrie Criteria for Severity of Acute Pancreatitis
    
    The Glasgow-Imrie Criteria is a clinical scoring system used to assess the severity 
    of acute pancreatitis using 8 laboratory and clinical parameters. Originally developed 
    as a modification of Ranson's criteria, it helps predict mortality risk and guide 
    management decisions including ICU admission and treatment intensity. The criteria 
    use the PANCREAS mnemonic (PaO2, Age, Neutrophils, Calcium, Renal function, 
    Enzymes, Albumin, Sugar) for easy clinical recall.
    
    The scoring system assigns 1 point for each positive criterion, with total scores 
    ranging from 0-8 points. Scores ≥3 indicate significant likelihood of severe 
    pancreatitis requiring intensive monitoring and management.
    
    Args:
        request: Parameters including PaO2, age, WBC, calcium, urea, LDH, albumin, and glucose
        
    Returns:
        GlasgowImriePancreatitisResponse: Total Glasgow-Imrie score with severity assessment and management recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("glasgow_imrie_pancreatitis", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Glasgow-Imrie Criteria for Severity of Acute Pancreatitis",
                    "details": {"parameters": parameters}
                }
            )
        
        return GlasgowImriePancreatitisResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Glasgow-Imrie Criteria",
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