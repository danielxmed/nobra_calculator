"""
American Diabetes Association (ADA) Risk Calculator Router

Endpoint for calculating ADA diabetes risk assessment.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.endocrinology.ada_risk_calculator import (
    AdaRiskCalculatorRequest,
    AdaRiskCalculatorResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post("/ada_risk_calculator", response_model=AdaRiskCalculatorResponse)
async def calculate_ada_risk_calculator(request: AdaRiskCalculatorRequest):
    """
    Calculates American Diabetes Association (ADA) Risk Score
    
    The ADA Risk Calculator is a clinical decision tool that uses 6 easily obtainable 
    demographic and clinical variables to identify individuals at high risk for 
    undiagnosed type 2 diabetes mellitus. This self-assessment tool allows for 
    diabetes risk stratification without requiring laboratory tests or physical 
    examinations.
    
    The calculator uses a point-based scoring system (0-10 points total) based on:
    - Age (higher age increases risk)
    - Gender (males at higher risk)
    - Family history of diabetes
    - History of hypertension
    - Physical activity level (inactivity increases risk) 
    - Body Mass Index (higher BMI increases risk)
    
    Score interpretation:
    - 0-3 points: Low risk (no immediate screening needed)
    - 4 points: High risk for prediabetes (consider screening)
    - 5-10 points: High risk for diabetes (screening recommended)
    
    Args:
        request: Demographic and clinical parameters for diabetes risk assessment
        
    Returns:
        AdaRiskCalculatorResponse: Risk score with clinical interpretation and screening recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("ada_risk_calculator", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating American Diabetes Association (ADA) Risk Calculator",
                    "details": {"parameters": parameters}
                }
            )
        
        return AdaRiskCalculatorResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for American Diabetes Association (ADA) Risk Calculator",
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