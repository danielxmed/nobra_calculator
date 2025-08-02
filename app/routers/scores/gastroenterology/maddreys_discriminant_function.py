"""
Maddrey's Discriminant Function Router

Endpoint for calculating Maddrey's Discriminant Function to predict prognosis 
and guide steroid therapy in alcoholic hepatitis.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.gastroenterology.maddreys_discriminant_function import (
    MaddreysDiscriminantFunctionRequest,
    MaddreysDiscriminantFunctionResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/maddreys_discriminant_function",
    response_model=MaddreysDiscriminantFunctionResponse,
    summary="Calculate Maddrey's Discriminant Function",
    description="Calculates Maddrey's Discriminant Function to predict prognosis and guide corticosteroid "
                "therapy in alcoholic hepatitis. This classic prognostic score, developed in 1978, uses "
                "prothrombin time prolongation and total bilirubin elevation to assess disease severity. "
                "A score ≥32 indicates severe disease with poor prognosis (35-45% 30-day mortality) and "
                "potential benefit from steroid therapy, while scores <32 indicate mild to moderate disease "
                "with excellent prognosis (90% 30-day survival) without steroid treatment. The score helps "
                "clinicians make evidence-based treatment decisions and assess short-term prognosis.",
    response_description="The calculated Maddrey's score with severity classification and comprehensive treatment recommendations",
    operation_id="maddreys_discriminant_function"
)
async def calculate_maddreys_discriminant_function(request: MaddreysDiscriminantFunctionRequest):
    """
    Calculates Maddrey's Discriminant Function for alcoholic hepatitis prognosis and treatment guidance
    
    Maddrey's Discriminant Function is the first established clinical prognostic score for
    alcoholic hepatitis, providing evidence-based guidance for corticosteroid therapy decisions.
    
    Formula: Maddrey's DF = 4.6 × (Patient's PT - Control PT) + Total Bilirubin
    
    Clinical Applications:
    - Short-term prognosis prediction (30-day mortality risk)
    - Treatment decision-making for corticosteroid therapy
    - Risk stratification for hospital vs. outpatient management
    - Clinical trial enrollment and research applications
    - Quality metrics and outcome assessment
    
    Severity Classification:
    - Mild to Moderate (<32 points): 90% 30-day survival, steroids not recommended
    - Severe (≥32 points): 35-45% 30-day mortality, consider prednisolone 40mg daily
    
    Treatment Considerations:
    - Screen for steroid contraindications: active GI bleeding, infection, acute pancreatitis,
      acute renal failure, hepatorenal syndrome, severe psychiatric illness
    - Combine with Lille score at day 7 to assess treatment response
    - Consider MELD score for additional prognostic information
    - Nutritional support and alcohol cessation counseling essential
    
    Historical Significance:
    Developed in 1978 by Maddrey et al. following a landmark randomized controlled trial
    of prednisolone vs. placebo in 55 patients with alcoholic hepatitis. This seminal
    work established the foundation for evidence-based treatment of severe alcoholic hepatitis.
    
    Args:
        request: Maddrey's calculation parameters including PT values and total bilirubin
        
    Returns:
        MaddreysDiscriminantFunctionResponse: Score with severity assessment and treatment recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("maddreys_discriminant_function", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Maddrey's Discriminant Function",
                    "details": {"parameters": parameters}
                }
            )
        
        return MaddreysDiscriminantFunctionResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Maddrey's Discriminant Function",
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
                "message": "Internal error in Maddrey's Discriminant Function calculation",
                "details": {"error": str(e)}
            }
        )