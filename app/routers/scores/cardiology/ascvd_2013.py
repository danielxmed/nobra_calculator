"""
ASCVD 2013 Risk Calculator Router

Endpoint for calculating 10-year atherosclerotic cardiovascular disease risk
using the 2013 ACC/AHA Pooled Cohort Equations.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.cardiology.ascvd_2013 import (
    Ascvd2013Request,
    Ascvd2013Response
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/ascvd_2013",
    response_model=Ascvd2013Response,
    summary="Calculate ASCVD (Atherosclerotic Cardiovascular...",
    description="Estimates the 10-year risk of atherosclerotic cardiovascular disease (heart attack, stroke, or death due to coronary heart disease or stroke) using the Pooled Cohort Equations. For patients 40-79 years old with no history of ASCVD.",
    response_description="The calculated ascvd 2013 with interpretation",
    operation_id="calculate_ascvd_2013"
)
async def calculate_ascvd_2013(request: Ascvd2013Request):
    """
    Calculates 10-year ASCVD Risk using 2013 ACC/AHA Pooled Cohort Equations
    
    Estimates the 10-year risk of atherosclerotic cardiovascular disease 
    (first occurrence of nonfatal myocardial infarction, coronary heart disease death, 
    or fatal/nonfatal stroke) for patients aged 40-79 years with no prior ASCVD.
    
    **Key Features:**
    - Race- and sex-specific coefficients from the original 2013 ACC/AHA guidelines
    - Validated risk thresholds for treatment recommendations
    - Includes detailed calculation breakdown
    
    **Risk Categories:**
    - **Low Risk (<5%)**: Focus on lifestyle modifications
    - **Borderline Risk (5-7.4%)**: Consider risk enhancers, lifestyle modifications
    - **Intermediate Risk (7.5-19.9%)**: Moderate- to high-intensity statin therapy
    - **High Risk (≥20%)**: High-intensity statin therapy
    
    **Important Notes:**
    - Not applicable for patients with prior ASCVD or LDL-C ≥190 mg/dL
    - May overestimate risk in some contemporary populations
    - For "other" race, uses White race coefficients
    
    Args:
        request: ASCVD 2013 calculation parameters including age, sex, race, 
                cholesterol levels, blood pressure, and risk factors
                
    Returns:
        Ascvd2013Response: 10-year ASCVD risk percentage with clinical interpretation
        
    Raises:
        HTTPException: If calculation fails or parameters are invalid
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("ascvd_2013", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating ASCVD 2013 Risk",
                    "details": {"parameters": parameters}
                }
            )
        
        return Ascvd2013Response(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for ASCVD 2013 Risk Calculator",
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
                "message": "Internal error in ASCVD 2013 calculation",
                "details": {"error": str(e)}
            }
        )