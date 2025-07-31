"""
Drug Resistance in Pneumonia (DRIP) Score Router

Endpoint for calculating DRIP scores.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.infectious_disease.drip_score import (
    DripScoreRequest,
    DripScoreResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/drip_score",
    response_model=DripScoreResponse,
    summary="Calculate Drug Resistance in Pneumonia (DRIP) Score",
    description="Predicts risk for community-acquired pneumonia due to drug-resistant pathogens (CAP-DRP). Helps determine when broad-spectrum antibiotics should be used to ensure effective treatment while avoiding unnecessary antibiotic resistance.",
    response_description="The calculated drip score with interpretation",
    operation_id="calculate_drip_score"
)
async def calculate_drip_score(request: DripScoreRequest):
    """
    Calculates Drug Resistance in Pneumonia (DRIP) Score
    
    The DRIP Score predicts risk for community-acquired pneumonia due to drug-resistant 
    pathogens (CAP-DRP). It helps determine when broad-spectrum antibiotics should be used 
    to ensure effective treatment while avoiding unnecessary antibiotic resistance.
    
    Scoring System:
    - Major Risk Factors (2 points each): Antibiotic use within 60 days, long-term care 
      facility residence, tube feeding, prior drug-resistant infection
    - Minor Risk Factors (1 point each): Chronic pulmonary disease, hospitalization within 
      60 days, poor functional status, MRSA colonization, wound care, gastric acid suppression
    - Total score range: 0-14 points
    
    Interpretation:
    - Score <4: Low risk - standard empirical antibiotics appropriate
    - Score ≥4: High risk - extended-spectrum antibiotic coverage recommended
    
    Clinical Performance (at threshold ≥4):
    - Sensitivity: 0.82, Specificity: 0.81, PPV: 0.68, NPV: 0.90
    - More predictive than HCAP criteria, may reduce unnecessary antibiotics by 46%
    
    Args:
        request: DRIP score parameters (10 risk factors: 4 major, 6 minor)
        
    Returns:
        DripScoreResponse: DRIP score with antibiotic recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("drip_score", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Drug Resistance in Pneumonia (DRIP) Score",
                    "details": {"parameters": parameters}
                }
            )
        
        return DripScoreResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Drug Resistance in Pneumonia (DRIP) Score",
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