"""
Basic Statistics Calculator Router

Endpoint for calculating common epidemiological values for diagnostic tests and treatments.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.emergency.basic_statistics_calc import (
    BasicStatisticsCalcRequest,
    BasicStatisticsCalcResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/basic_statistics_calc",
    response_model=BasicStatisticsCalcResponse,
    summary="Calculate Basic Statistics Calculator",
    description="Calculates common epidemiological values for diagnostic tests and treatments, including sensitivity, specificity, predictive values, likelihood ratios, and treatment effectiveness measures.",
    response_description="The calculated basic statistics calc with interpretation",
    operation_id="basic_statistics_calc"
)
async def calculate_basic_statistics_calc(request: BasicStatisticsCalcRequest):
    """
    Calculates Basic Statistics for diagnostic tests and treatments
    
    This calculator provides comprehensive statistical analysis for:
    
    1. **Diagnostic Test Analysis**:
       - Sensitivity, specificity, predictive values
       - Likelihood ratios (positive and negative)
       - Pre/post-test probabilities
       - Can accept either rates (prevalence, sensitivity, specificity) or 
         counts (TP, FP, FN, TN) as input
    
    2. **Treatment Analysis**:
       - Event rates (experimental and control)
       - Relative risk and odds ratio with confidence intervals
       - Absolute and relative risk reduction
       - Number needed to treat (NNT)
    
    Essential tool for evidence-based medicine decision making.
    
    Args:
        request: Parameters for calculation based on type (diagnostic test or treatment)
        
    Returns:
        BasicStatisticsCalcResponse: Comprehensive statistical analysis with interpretation
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict(exclude_none=True)
        
        # Execute calculation
        result = calculator_service.calculate_score("basic_statistics_calc", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Basic Statistics",
                    "details": {"parameters": parameters}
                }
            )
        
        return BasicStatisticsCalcResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Basic Statistics Calculator",
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