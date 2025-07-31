"""
Arterial Blood Gas (ABG) Analyzer Router

Endpoint for calculating ABG analysis and interpretation.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.emergency.abg_analyzer import (
    AbgAnalyzerRequest,
    AbgAnalyzerResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/abg_analyzer",
    response_model=AbgAnalyzerResponse,
    summary="Calculate Arterial Blood Gas (ABG) Analyzer",
    description="Interprets arterial blood gas results to determine acid-base status, respiratory compensation, and metabolic derangements",
    response_description="The calculated abg analyzer with interpretation",
    operation_id="calculate_abg_analyzer"
)
async def calculate_abg_analyzer(request: AbgAnalyzerRequest):
    """
    Calculates Arterial Blood Gas (ABG) Analysis
    
    Interprets arterial blood gas results to determine acid-base status, 
    assess respiratory and metabolic compensation, and evaluate oxygenation.
    
    The ABG Analyzer uses established physiological principles including:
    - pH assessment to determine acidemia vs alkalemia
    - Primary disorder identification (metabolic vs respiratory)
    - Compensation assessment using Winter's formula and other established rules
    - Oxygenation evaluation (if PO2 provided)
    - Clinical interpretation and recommendations
    
    Normal ranges:
    - pH: 7.35-7.45
    - PCO2: 35-45 mmHg
    - HCO3: 22-26 mEq/L
    - PO2: 80-100 mmHg (on room air)
    
    Args:
        request: ABG parameters including pH, PCO2, HCO3, and optional PO2/FiO2
        
    Returns:
        AbgAnalyzerResponse: Primary disorder, compensation assessment, and clinical interpretation
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("abg_analyzer", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating ABG Analysis",
                    "details": {"parameters": parameters}
                }
            )
        
        return AbgAnalyzerResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for ABG Analysis",
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
                "message": "Internal error in ABG calculation",
                "details": {"error": str(e)}
            }
        )
