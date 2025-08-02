"""
Urinary Protein Excretion Estimation Router

Endpoint for calculating Urinary Protein Excretion Estimation.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.nephrology.urinary_protein_excretion_estimation import (
    UrinaryProteinExcretionEstimationRequest,
    UrinaryProteinExcretionEstimationResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/urinary_protein_excretion_estimation",
    response_model=UrinaryProteinExcretionEstimationResponse,
    summary="Calculate Urinary Protein Excretion Estimation",
    description="Calculates the estimated 24-hour urinary protein excretion using the protein/creatinine "
                "ratio from a single random daytime urine sample. This validated method provides a convenient "
                "alternative to cumbersome 24-hour urine collection for estimating daily protein excretion in "
                "patients with stable renal function. The calculation uses the principle that creatinine excretion "
                "is relatively constant throughout the day, making the protein/creatinine ratio a reliable indicator "
                "of daily protein excretion. Clinical interpretation includes normal (<0.2 g/day), abnormal proteinuria "
                "requiring investigation (0.2-3.5 g/day), and nephrotic range proteinuria requiring urgent evaluation "
                "(>3.5 g/day). First validated by Ginsberg et al. in 1983, this method is widely used for screening "
                "and monitoring proteinuria in clinical practice.",
    response_description="The estimated 24-hour urinary protein excretion with clinical interpretation and management recommendations",
    operation_id="urinary_protein_excretion_estimation"
)
async def calculate_urinary_protein_excretion_estimation(request: UrinaryProteinExcretionEstimationRequest):
    """
    Calculates Urinary Protein Excretion Estimation
    
    The Urinary Protein Excretion Estimation provides a practical alternative to 24-hour 
    urine collection for quantifying proteinuria. Using a simple protein/creatinine ratio 
    from a single random daytime urine sample, it estimates 24-hour protein excretion with 
    good correlation to formal 24-hour collections.
    
    Method and Formula:
    24-hour Urinary Protein Excretion (g/day) = Urine Protein (mg/dL) / Urine Creatinine (mg/dL)
    
    This calculation is based on the principle that creatinine excretion is relatively 
    constant at approximately 1 g/day in most adults with stable renal function, making 
    the protein/creatinine ratio a reliable surrogate for daily protein excretion.
    
    Clinical Applications:
    - Screening for proteinuria in diabetes, hypertension, or suspected kidney disease
    - Monitoring chronic kidney disease progression
    - Evaluating patients for nephrotic syndrome
    - Alternative to 24-hour collection when patient convenience is important
    
    Sample Requirements:
    - Random daytime urine sample (avoid overnight or first morning samples)
    - Same sample used for both protein and creatinine measurements
    - Patient must have stable renal function (stable GFR)
    
    Interpretation Guidelines:
    - <0.2 g/day: Normal protein excretion, routine monitoring
    - 0.2-3.5 g/day: Abnormal proteinuria, investigate further
    - >3.5 g/day: Nephrotic range, urgent nephrology evaluation
    
    Advantages over 24-hour collection:
    - More convenient for patients and providers
    - Eliminates collection errors and incomplete samples
    - Immediate results available
    - Suitable for outpatient screening and monitoring
    
    Limitations:
    - Requires stable renal function (not reliable in AKI)
    - Less accurate in type 1 diabetes when ratio >3.5 g/g
    - Consider formal 24-hour collection if proteinuria >10 g/day
    
    Args:
        request: Urine protein and creatinine concentrations from same sample
        
    Returns:
        UrinaryProteinExcretionEstimationResponse: Estimated protein excretion with interpretation
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("urinary_protein_excretion_estimation", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Urinary Protein Excretion Estimation",
                    "details": {"parameters": parameters}
                }
            )
        
        return UrinaryProteinExcretionEstimationResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Urinary Protein Excretion Estimation",
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