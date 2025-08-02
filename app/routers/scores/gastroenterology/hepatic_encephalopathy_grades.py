"""
Hepatic Encephalopathy Grades/Stages (West Haven Criteria) Router

Endpoint for classifying hepatic encephalopathy severity.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.gastroenterology.hepatic_encephalopathy_grades import (
    HepaticEncephalopathyGradesRequest,
    HepaticEncephalopathyGradesResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/hepatic_encephalopathy_grades",
    response_model=HepaticEncephalopathyGradesResponse,
    summary="Classify Hepatic Encephalopathy Grade",
    description="Classifies hepatic encephalopathy severity using the West Haven Criteria, "
                "the most widely used grading system for this condition. The criteria provides "
                "a semi-quantitative assessment based on changes in consciousness, intellectual "
                "function, behavior, and neuromuscular abnormalities. The system includes 5 grades "
                "(0-4), with Grades 0-1 considered 'Covert HE' and Grades 2-4 'Overt HE'. "
                "Grade 0 (Minimal HE) requires psychometric testing for diagnosis, while higher "
                "grades show progressively more severe clinical manifestations from subtle behavioral "
                "changes to coma. This standardized grading helps guide treatment decisions and "
                "assess prognosis in patients with acute or chronic liver disease.",
    response_description="The West Haven grade with detailed clinical interpretation and stage classification",
    operation_id="hepatic_encephalopathy_grades"
)
async def calculate_hepatic_encephalopathy_grades(request: HepaticEncephalopathyGradesRequest):
    """
    Classifies Hepatic Encephalopathy using West Haven Criteria
    
    The West Haven Criteria is essential for standardizing the assessment and
    management of hepatic encephalopathy. It helps clinicians communicate
    effectively about disease severity and track progression over time.
    
    Args:
        request: Clinical features corresponding to West Haven grades
        
    Returns:
        HepaticEncephalopathyGradesResponse: Grade classification with interpretation
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("hepatic_encephalopathy_grades", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error classifying hepatic encephalopathy grade",
                    "details": {"parameters": parameters}
                }
            )
        
        return HepaticEncephalopathyGradesResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for hepatic encephalopathy grading",
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
                "message": "Internal error in hepatic encephalopathy grading",
                "details": {"error": str(e)}
            }
        )