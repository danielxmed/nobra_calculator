"""
ACR/EULAR 2010 Rheumatoid Arthritis Classification Criteria Router

Endpoint for calculating ACR/EULAR 2010 RA classification criteria.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.rheumatology.acr_eular_2010_ra import (
    AcrEular2010RaRequest,
    AcrEular2010RaResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post("/acr_eular_2010_ra", response_model=AcrEular2010RaResponse)
async def calculate_acr_eular_2010_ra(request: AcrEular2010RaRequest):
    """
    Calculates ACR/EULAR 2010 Rheumatoid Arthritis Classification Criteria
    
    This calculator implements the 2010 ACR/EULAR classification criteria for 
    rheumatoid arthritis, which were developed to facilitate early identification 
    of RA in patients with undifferentiated inflammatory synovitis. The criteria 
    enable timely initiation of disease-modifying antirheumatic drugs (DMARDs) 
    before irreversible joint damage occurs.
    
    The criteria assess four domains:
    - Joint involvement (0-5 points): Based on number and type of affected joints
    - Serology (0-3 points): RF and ACPA status with highest score used
    - Acute-phase reactants (0-1 point): CRP and/or ESR elevation
    - Duration of symptoms (0-1 point): <6 weeks vs ≥6 weeks
    
    A total score ≥6 points indicates definite RA and warrants consideration 
    for early DMARD therapy.
    
    Prerequisites for use:
    - At least one swollen joint present
    - No better explanation for synovitis
    - At least one serology test result available
    - At least one acute-phase reactant test result available
    
    Args:
        request: Parameters including joint involvement, serology, acute-phase reactants, and symptom duration
        
    Returns:
        AcrEular2010RaResponse: Total score with RA classification and management recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("acr_eular_2010_ra", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating ACR/EULAR 2010 RA classification criteria",
                    "details": {"parameters": parameters}
                }
            )
        
        return AcrEular2010RaResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for ACR/EULAR 2010 RA classification criteria",
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