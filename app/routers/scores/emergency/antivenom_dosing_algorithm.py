"""
Antivenom Dosing Algorithm Router

Endpoint for calculating CroFab antivenom dosing for pit viper snakebites.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.emergency.antivenom_dosing_algorithm import (
    AntivenomDosingAlgorithmRequest,
    AntivenomDosingAlgorithmResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post("/antivenom_dosing_algorithm", response_model=AntivenomDosingAlgorithmResponse)
async def calculate_antivenom_dosing_algorithm(request: AntivenomDosingAlgorithmRequest):
    """
    Calculates Antivenom Dosing Algorithm for pit viper snakebites
    
    This unified treatment algorithm assists with CroFab dosing for crotaline (pit viper) 
    snakebites including rattlesnakes, copperheads, and cottonmouths. The algorithm provides 
    evidence-based dosing recommendations based on clinical presentation and severity.
    
    Key Features:
    - Initial dose recommendations (4-12 vials based on severity)
    - Maintenance dosing protocol (2 vials q6h x 3 doses)
    - Clinical monitoring requirements
    - Follow-up care guidance
    
    Clinical Assessment:
    - Signs of envenomation: Local, systemic, and hematologic effects
    - Severity grading: None, minimal, moderate, or severe
    - Initial control definition: Arrest local progression + resolve systemic effects + reduce hematologic abnormalities
    
    Important Notes:
    - For CroFab only (not Anavip)
    - Crotaline snakes only (not coral snakes)
    - Not valid for head/neck bites, rhabdomyolysis, or anaphylaxis
    - Always contact poison control: 1-800-222-1222
    
    Args:
        request: Clinical assessment parameters (signs of envenomation, severity grade, patient weight)
        
    Returns:
        AntivenomDosingAlgorithmResponse: Dosing recommendation with clinical guidance
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("antivenom_dosing_algorithm", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Antivenom Dosing Algorithm",
                    "details": {"parameters": parameters}
                }
            )
        
        return AntivenomDosingAlgorithmResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Antivenom Dosing Algorithm",
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