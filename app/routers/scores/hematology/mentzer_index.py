"""
Mentzer Index Router

Endpoint for calculating Mentzer Index to differentiate beta thalassemia from iron deficiency anemia.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.hematology.mentzer_index import (
    MentzerIndexRequest,
    MentzerIndexResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/mentzer_index",
    response_model=MentzerIndexResponse,
    summary="Calculate Mentzer Index",
    description="Calculates the Mentzer Index to help differentiate between beta thalassemia trait "
                "and iron deficiency anemia in patients with microcytic anemia. This simple screening "
                "tool uses the ratio of Mean Corpuscular Volume (MCV) to Red Blood Cell (RBC) count. "
                "An index <13 suggests beta thalassemia trait (normal RBC production with smaller cells), "
                "while an index >13 suggests iron deficiency anemia (reduced RBC production with small cells). "
                "An index of exactly 13 is indeterminate. While this index has shown sensitivity of 74-98.7% "
                "and specificity of 63-82.3% for beta thalassemia trait in various studies, it should only "
                "be used as a screening tool. Confirmatory testing with iron studies and hemoglobin "
                "electrophoresis is essential for definitive diagnosis. The index may be affected by "
                "concurrent conditions or other causes of microcytosis.",
    response_description="The calculated Mentzer Index with diagnostic interpretation and recommendations",
    operation_id="mentzer_index"
)
async def calculate_mentzer_index(request: MentzerIndexRequest):
    """
    Calculates Mentzer Index for differentiating beta thalassemia from iron deficiency anemia
    
    This simple but effective screening tool helps guide further testing in patients
    with microcytic anemia by distinguishing between two common causes.
    
    Args:
        request: MCV and RBC count values from a complete blood count
        
    Returns:
        MentzerIndexResponse: Calculated index with interpretation
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("mentzer_index", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Mentzer Index",
                    "details": {"parameters": parameters}
                }
            )
        
        return MentzerIndexResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Mentzer Index",
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