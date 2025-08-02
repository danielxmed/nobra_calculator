"""
International IgA Nephropathy Prediction Tool Router

Endpoint for calculating International IgAN Prediction Tool.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.nephrology.international_igan_prediction_tool import (
    InternationalIganPredictionToolRequest,
    InternationalIganPredictionToolResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/international_igan_prediction_tool",
    response_model=InternationalIganPredictionToolResponse,
    summary="Calculate International IgA Nephropathy Prediction Tool",
    description="Calculates the International IgA Nephropathy Prediction Tool to predict the 5-year risk of a 50% decline in eGFR or end-stage kidney disease in patients with biopsy-proven IgA nephropathy. This validated prognostic tool was developed using an international multi-ethnic cohort of 2,781 patients and is endorsed by the 2021 KDIGO guidelines as the preferred method for risk prediction in IgA nephropathy. The tool uses clinical parameters (age, eGFR, mean arterial pressure, proteinuria), Oxford MEST histological scores (M: mesangial hypercellularity, E: endocapillary hypercellularity, S: segmental sclerosis, T: interstitial fibrosis/tubular atrophy), and treatment factors (RASB use, immunosuppression) available at the time of kidney biopsy. Two prediction models are available: a race-free model (primary) and a race-inclusive model, both providing excellent discrimination (C-statistic ~0.72) for predicting kidney outcomes. The tool facilitates clinical decision-making by stratifying patients into risk categories from very low (<10% 5-year risk) to very high (>75% 5-year risk), guiding treatment intensity, monitoring frequency, and timing of kidney replacement therapy discussions. It is particularly valuable for patient counseling, treatment planning, clinical trial enrollment, and implementing personalized management strategies in IgA nephropathy care.",
    response_description="The calculated 5-year risk percentage with clinical risk stratification and management recommendations",
    operation_id="international_igan_prediction_tool"
)
async def calculate_international_igan_prediction_tool(request: InternationalIganPredictionToolRequest):
    """
    Calculates International IgA Nephropathy Prediction Tool for kidney outcome risk
    
    Predicts 5-year risk of 50% eGFR decline or ESKD using clinical, laboratory, 
    and histological parameters to guide treatment decisions and patient counseling.
    
    Args:
        request: Clinical and histological parameters for International IgAN Prediction Tool (11 parameters)
        
    Returns:
        InternationalIganPredictionToolResponse: 5-year risk percentage with management guidance
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("international_igan_prediction_tool", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating International IgAN Prediction Tool",
                    "details": {"parameters": parameters}
                }
            )
        
        return InternationalIganPredictionToolResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for International IgAN Prediction Tool",
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