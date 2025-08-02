"""
Kawasaki Disease Diagnostic Criteria Router

Endpoint for calculating Kawasaki Disease diagnostic criteria.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.pediatrics.kawasaki_disease_diagnostic_criteria import (
    KawasakiDiseaseRequest,
    KawasakiDiseaseResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/kawasaki_disease_diagnostic_criteria",
    response_model=KawasakiDiseaseResponse,
    summary="Calculate Kawasaki Disease Diagnostic Criteria",
    description="Evaluates Kawasaki Disease diagnostic criteria based on fever duration and principal "
                "clinical features. Kawasaki disease is a systemic vasculitis of childhood that can cause "
                "coronary artery aneurysms if untreated. The criteria distinguish between classic Kawasaki "
                "disease (fever ≥4 days + ≥4 principal features) and incomplete Kawasaki disease (fever ≥5 days "
                "+ 2-3 principal features with supportive findings). Principal features include bilateral "
                "conjunctival injection, oral changes, cervical lymphadenopathy, extremity changes, and "
                "polymorphous rash. Early diagnosis and treatment with IVIG and aspirin within 10 days of "
                "fever onset significantly reduces the risk of coronary artery abnormalities. This tool helps "
                "clinicians systematically evaluate patients and determine appropriate treatment and monitoring.",
    response_description="Diagnostic assessment with treatment recommendations and monitoring guidance based on Kawasaki disease criteria",
    operation_id="kawasaki_disease_diagnostic_criteria"
)
async def calculate_kawasaki_disease_diagnostic_criteria(request: KawasakiDiseaseRequest):
    """
    Calculates Kawasaki Disease Diagnostic Criteria
    
    Kawasaki disease is the leading cause of acquired heart disease in children in 
    developed countries. Early recognition and treatment are essential to prevent 
    coronary artery complications.
    
    Diagnostic Criteria:
    - Classic Kawasaki Disease: Fever ≥4 days + ≥4/5 principal clinical features
    - Incomplete Kawasaki Disease: Fever ≥5 days + 2-3/5 principal features + 
      supportive laboratory findings or coronary abnormalities
    
    Principal Clinical Features:
    1. Bilateral conjunctival injection without exudate
    2. Oral changes (cracked lips, strawberry tongue, oral erythema)
    3. Cervical lymphadenopathy (≥1.5 cm diameter)
    4. Extremity changes (erythema, induration, desquamation)
    5. Polymorphous rash (not vesicular or bullous)
    
    Treatment Recommendations:
    - IVIG (2 g/kg) plus high-dose aspirin for classic disease
    - Consider treatment for incomplete disease with supportive findings
    - Optimal treatment within 10 days of fever onset
    - Echocardiography at diagnosis, 2 weeks, and 6-8 weeks
    - Long-term cardiology follow-up based on coronary involvement
    
    Risk Factors for Incomplete Presentation:
    - Age <6 months or >8 years
    - Male gender
    - Asian ethnicity
    
    Args:
        request: Kawasaki Disease diagnostic parameters
        
    Returns:
        KawasakiDiseaseResponse: Diagnostic assessment with clinical recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("kawasaki_disease_diagnostic_criteria", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Kawasaki Disease Diagnostic Criteria",
                    "details": {"parameters": parameters}
                }
            )
        
        return KawasakiDiseaseResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Kawasaki Disease Diagnostic Criteria",
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