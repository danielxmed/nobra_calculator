"""
Hour-Specific Risk for Neonatal Hyperbilirubinemia Router

Endpoint for calculating Hour-Specific Risk using the Bhutani nomogram.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.pediatrics.hour_specific_neonatal_hyperbilirubinemia import (
    HourSpecificNeonatalHyperbilirubinemiaRequest,
    HourSpecificNeonatalHyperbilirubinemiaResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/hour_specific_neonatal_hyperbilirubinemia",
    response_model=HourSpecificNeonatalHyperbilirubinemiaResponse,
    summary="Calculate Hour-Specific Risk for Neonatal Hyperbilirubinemia",
    description="Predicts risk of hyperbilirubinemia in neonates based on total serum bilirubin "
                "measurement using the Bhutani nomogram. This validated clinical tool stratifies "
                "healthy term and near-term newborns (≥35 weeks gestation) into risk zones for "
                "developing subsequent significant hyperbilirubinemia. The nomogram plots hour-specific "
                "bilirubin values from 12-168 hours of age to classify infants into Low (<40th percentile), "
                "Low-Intermediate (40-75th), High-Intermediate (76-94th), or High Risk (≥95th percentile) "
                "zones. This helps identify infants requiring closer follow-up after hospital discharge "
                "and supports clinical decision-making for timely intervention to prevent kernicterus.",
    response_description="The calculated risk zone classification with percentile ranking and clinical "
                        "recommendations for follow-up timing",
    operation_id="hour_specific_neonatal_hyperbilirubinemia"
)
async def calculate_hour_specific_neonatal_hyperbilirubinemia(request: HourSpecificNeonatalHyperbilirubinemiaRequest):
    """
    Calculates Hour-Specific Risk for Neonatal Hyperbilirubinemia
    
    Uses the Bhutani nomogram (1999) to predict risk of subsequent significant 
    hyperbilirubinemia in healthy term and near-term newborns based on a single 
    predischarge bilirubin measurement.
    
    Args:
        request: Age in hours (12-168) and total serum bilirubin (mg/dL)
        
    Returns:
        HourSpecificNeonatalHyperbilirubinemiaResponse: Risk zone with clinical interpretation
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("hour_specific_neonatal_hyperbilirubinemia", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Hour-Specific Risk for Neonatal Hyperbilirubinemia",
                    "details": {"parameters": parameters}
                }
            )
        
        return HourSpecificNeonatalHyperbilirubinemiaResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Hour-Specific Risk calculation",
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