"""
Tokyo Guidelines 2018 for Acute Cholecystitis Router

Endpoint for calculating Tokyo Guidelines 2018 diagnostic criteria and severity grading.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.gastroenterology.tokyo_guidelines_2018 import (
    TokyoGuidelines2018Request,
    TokyoGuidelines2018Response
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/tokyo_guidelines_2018",
    response_model=TokyoGuidelines2018Response,
    summary="Calculate Tokyo Guidelines 2018 for Acute Cholecystitis",
    description="Provides diagnostic criteria and severity grading for acute cholecystitis according to "
                "Tokyo Guidelines 2018 (TG18). The guidelines use a three-part diagnostic approach: "
                "Part A (local signs), Part B (systemic signs), and Part C (imaging findings). "
                "Suspected diagnosis requires Parts A+B, while definite diagnosis requires all three parts. "
                "Severity is graded as: Grade I (mild) with 1.1% mortality, Grade II (moderate with local "
                "inflammation) with 5.4% mortality, or Grade III (severe with organ dysfunction) with 18.8% "
                "30-day mortality. TG18 recommends early laparoscopic cholecystectomy for all grades when "
                "feasible, with timing based on severity and response to initial treatment.",
    response_description="The diagnostic result with severity grading, mortality rate, and treatment recommendations",
    operation_id="tokyo_guidelines_2018"
)
async def calculate_tokyo_guidelines_2018(request: TokyoGuidelines2018Request):
    """
    Calculates Tokyo Guidelines 2018 diagnosis and severity grading for acute cholecystitis
    
    The TG18 criteria provide standardized diagnosis and risk stratification for acute
    cholecystitis, helping guide treatment decisions including timing of surgery and
    need for urgent intervention or ICU care.
    
    Args:
        request: Clinical and laboratory parameters for TG18 assessment
        
    Returns:
        TokyoGuidelines2018Response: Diagnosis, severity grade, mortality risk, and recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("tokyo_guidelines_2018", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Tokyo Guidelines 2018",
                    "details": {"parameters": parameters}
                }
            )
        
        return TokyoGuidelines2018Response(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Tokyo Guidelines 2018",
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