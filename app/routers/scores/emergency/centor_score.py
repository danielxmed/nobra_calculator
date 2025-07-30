"""
Centor Score (Modified/McIsaac) for Strep Pharyngitis Router

Endpoint for calculating Centor Score for streptococcal pharyngitis assessment.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.emergency.centor_score import (
    CentorScoreRequest,
    CentorScoreResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post("/centor_score", response_model=CentorScoreResponse)
async def calculate_centor_score(request: CentorScoreRequest):
    """
    Calculates Centor Score (Modified/McIsaac) for Strep Pharyngitis
    
    The Modified Centor Score estimates the likelihood that pharyngitis is streptococcal 
    and suggests management course. This evidence-based tool helps reduce unnecessary 
    antibiotic prescriptions by 48% while maintaining appropriate care for bacterial infections.
    
    The score uses 4 clinical criteria plus age adjustment:
    
    CLINICAL CRITERIA (1 point each):
    - Tonsillar exudate: Presence of tonsillar swelling or exudate
    - Tender cervical nodes: Swollen, tender anterior cervical lymph nodes
    - History of fever: History of fever (>38°C or 100.4°F)
    - Absence of cough: Absence of cough (suggests bacterial vs viral etiology)
    
    AGE ADJUSTMENT (McIsaac modification):
    - Age 3-14 years: +1 point (higher risk of streptococcal infection)
    - Age 15-44 years: 0 points (baseline risk)
    - Age ≥45 years: -1 point (lower risk of streptococcal infection)
    
    SCORE INTERPRETATION:
    - Score ≤1: Low probability (1-10% GAS) - No testing or antibiotics needed
    - Score 2-3: Moderate probability (11-35% GAS) - RADT and/or culture recommended
    - Score ≥4: High probability (51-53% GAS) - Consider empiric treatment or testing
    
    Clinical Performance:
    - Validated in both children and adults with sore throat
    - Endorsed by IDSA guidelines for pharyngitis management
    - Reduces inappropriate antibiotic use while maintaining sensitivity
    - Cost-effective approach to pharyngitis evaluation
    
    Note: Should not be used as sole decision-making tool - clinical judgment 
    remains important. Does not apply to patients with recent streptococcal exposure.
    
    Args:
        request: Parameters needed for Centor Score calculation
        
    Returns:
        CentorScoreResponse: Score with probability assessment and management recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("centor_score", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Centor Score",
                    "details": {"parameters": parameters}
                }
            )
        
        return CentorScoreResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Centor Score",
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