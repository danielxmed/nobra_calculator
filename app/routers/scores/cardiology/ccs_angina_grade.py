"""
Canadian Cardiovascular Society (CCS) Angina Grade Router

Endpoint for calculating CCS Angina Grade.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.cardiology.ccs_angina_grade import (
    CcsAnginaGradeRequest,
    CcsAnginaGradeResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/ccs_angina_grade",
    response_model=CcsAnginaGradeResponse,
    summary="Calculate Canadian Cardiovascular Society (CCS)...",
    description="The Canadian Cardiovascular Society (CCS) Angina Grade classifies the severity of exertional angina based on the degree of effort necessary to induce angina symptoms. This standardized grading system helps clinicians communicate about functional limitations and symptom severity in patients with coronary artery disease.",
    response_description="The calculated ccs angina grade with interpretation",
    operation_id="calculate_ccs_angina_grade"
)
async def calculate_ccs_angina_grade(request: CcsAnginaGradeRequest):
    """
    Calculates Canadian Cardiovascular Society (CCS) Angina Grade
    
    The CCS Angina Grade classifies the severity of exertional angina based on 
    the degree of effort necessary to induce angina symptoms. This standardized 
    grading system helps clinicians communicate about functional limitations and 
    symptom severity in patients with coronary artery disease.
    
    Key features:
    - Four grades (I-IV) based on functional limitation
    - Grade I: Angina only with strenuous exertion
    - Grade II: Slight limitation of ordinary activity
    - Grade III: Marked limitation of ordinary physical activity
    - Grade IV: Inability to carry out any physical activity without discomfort
    
    Clinical applications:
    - Standardizes terminology for coronary artery disease studies
    - Used to assess fitness to fly (British Cardiovascular Society)
    - Associated with mortality and morbidity (though not designed as prognostic tool)
    - Analogous to NYHA classification for heart failure
    
    Args:
        request: Level of physical activity that triggers angina symptoms
        
    Returns:
        CcsAnginaGradeResponse: CCS grade with interpretation
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("ccs_angina_grade", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating CCS Angina Grade",
                    "details": {"parameters": parameters}
                }
            )
        
        return CcsAnginaGradeResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for CCS Angina Grade",
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