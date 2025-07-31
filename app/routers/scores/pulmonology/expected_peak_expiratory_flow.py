"""
Estimated/Expected Peak Expiratory Flow (Peak Flow) Router

Endpoint for calculating estimated peak expiratory flow and assessing asthma severity.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.pulmonology.expected_peak_expiratory_flow import (
    ExpectedPeakExpiratoryFlowRequest,
    ExpectedPeakExpiratoryFlowResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/expected_peak_expiratory_flow",
    response_model=ExpectedPeakExpiratoryFlowResponse,
    summary="Calculate Estimated/Expected Peak Expiratory Flow",
    description="Estimates expected peak expiratory flow rate and quantifies asthma exacerbation severity based on age, height, race, and sex.",
    response_description="The calculated expected peak expiratory flow with interpretation",
    operation_id="calculate_expected_peak_expiratory_flow"
)
async def calculate_expected_peak_expiratory_flow(request: ExpectedPeakExpiratoryFlowRequest):
    """
    Calculates Estimated/Expected Peak Expiratory Flow (Peak Flow)
    
    This calculator estimates expected peak expiratory flow rate and quantifies asthma 
    exacerbation severity based on age, height, race, and sex using established regression equations.
    
    Key Features:
    - Age-appropriate formulas (5-80 years)
    - Ethnicity-specific regression equations
    - Zone-based assessment (Green/Yellow/Red zones)
    - Asthma management guidance
    
    Formulas Used:
    
    Ages 5-7 years (all ethnicities):
    PEFR = [(Height, cm - 100) × 5] + 100
    
    Ages 8-17 years (non-Caucasian/African American/Mexican American):
    PEFR = [(Height, cm - 100) × 5] + 100
    
    Ages 18-80 years (non-Caucasian/African American/Mexican American):
    - Male: PEFR = {[(Height, m × 5.48) + 1.58] - [Age × 0.041]} × 60
    - Female: PEFR = {[(Height, m × 3.72) + 2.24] - [Age × 0.03]} × 60
    
    Ages 8-80 years (Caucasian/African American/Mexican American):
    Uses Hankinson 1999 NHANES III regression equations with ethnicity-specific coefficients
    
    Zone Assessment (when measured PEF provided):
    - Green Zone (≥80%): Good asthma control, continue treatment
    - Yellow Zone (50-79%): Caution, may need treatment adjustment
    - Red Zone (<50%): Emergency, seek immediate medical attention
    
    Clinical Applications:
    - Asthma management and monitoring
    - Assessment of treatment effectiveness  
    - Early detection of exacerbations
    - Patient self-management with action plans
    - Baseline establishment for new patients
    
    Args:
        request: Parameters including age, height, sex, race/ethnicity, and optional measured PEF
        
    Returns:
        ExpectedPeakExpiratoryFlowResponse: Expected PEF, zone assessment, and clinical interpretation
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("expected_peak_expiratory_flow", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Expected Peak Expiratory Flow",
                    "details": {"parameters": parameters}
                }
            )
        
        return ExpectedPeakExpiratoryFlowResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Expected Peak Expiratory Flow",
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