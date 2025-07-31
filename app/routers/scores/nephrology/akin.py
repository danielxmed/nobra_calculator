"""
AKIN Classification for Acute Kidney Injury (AKI) Router

Endpoint for calculating AKIN Classification for acute kidney injury staging.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.nephrology.akin import (
    AkinRequest,
    AkinResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/akin",
    response_model=AkinResponse,
    summary="Calculate AKIN Classification for Acute Kidney Injury (AKI)",
    description="Classifies severity of acute kidney injury based on serum creatinine and urine output criteria within 48 hours",
    response_description="The calculated akin with interpretation",
    operation_id="calculate_akin"
)
async def calculate_akin(request: AkinRequest):
    """
    Calculates AKIN Classification for Acute Kidney Injury
    
    The AKIN (Acute Kidney Injury Network) classification provides a standardized 
    framework for diagnosing and staging acute kidney injury based on serum 
    creatinine and urine output criteria within a 48-hour timeframe.
    
    Key Features:
    - More sensitive than RIFLE for detecting mild AKI
    - Requires changes within 48 hours
    - Uses serum creatinine and urine output criteria
    - Patients on RRT are automatically classified as Stage 3
    - Associated with increased mortality even at Stage 1
    
    AKIN Stages:
    
    Stage 1 (Mild AKI):
    - Creatinine: ≥0.3 mg/dL increase OR 1.5-2x baseline
    - Urine output: <0.5 mL/kg/hr for >6 hours
    - Management: Close monitoring, consider nephrology consultation
    
    Stage 2 (Moderate AKI):
    - Creatinine: 2-3x baseline
    - Urine output: <0.5 mL/kg/hr for >12 hours
    - Management: Intensive monitoring, nephrology consultation recommended
    
    Stage 3 (Severe AKI):
    - Creatinine: >3x baseline OR ≥4.0 mg/dL with acute increase ≥0.5 mg/dL
    - Urine output: <0.3 mL/kg/hr for ≥24 hours OR anuria for 12 hours
    - OR on renal replacement therapy
    - Management: Urgent nephrology consultation, consider RRT
    
    Clinical Applications:
    - ICU patient monitoring and risk stratification
    - Clinical decision-making for AKI management
    - Prognosis assessment and mortality prediction
    - Research standardization and clinical trials
    - Nephrology consultation timing
    
    Advantages over RIFLE:
    - More sensitive for detecting mild AKI (Stage 1)
    - Defined 48-hour timeframe for changes
    - Baseline creatinine not required (can use first reference)
    - Better mortality prediction capabilities
    - Excludes dehydration cases (requires adequate hydration)
    
    Requirements:
    - Changes must occur within 48 hours
    - Adequate hydration status must be achieved
    - Urinary tract obstruction must be excluded
    - At least two creatinine measurements within 48 hours
    
    Important Notes:
    - Stage corresponds to highest criterion met (creatinine or urine output)
    - Associated with increased mortality at all stages
    - Should be used with clinical context and judgment
    - Helpful for medication dosing adjustments
    - Guides monitoring intensity and resource allocation
    
    Args:
        request: Parameters needed for AKIN classification
        
    Returns:
        AkinResponse: AKIN stage with clinical interpretation and management recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("akin", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating AKIN Classification",
                    "details": {"parameters": parameters}
                }
            )
        
        return AkinResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for AKIN Classification",
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