"""
Kocher Criteria for Septic Arthritis Router

Endpoint for calculating Kocher Criteria risk assessment for septic arthritis in pediatric patients.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.emergency.kocher_criteria_septic_arthritis import (
    KocherCriteriaSepticArthritisRequest,
    KocherCriteriaSepticArthritisResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/kocher_criteria_septic_arthritis",
    response_model=KocherCriteriaSepticArthritisResponse,
    summary="Calculate Kocher Criteria for Septic Arthritis",
    description="Calculates the Kocher Criteria risk assessment for septic arthritis in pediatric "
                "patients presenting with hip pain and related symptoms. This validated clinical "
                "prediction rule uses four independent predictors (non-weight bearing, fever >38.5°C, "
                "ESR >40 mm/hr, and WBC >12,000 cells/mm³) to differentiate septic arthritis from "
                "transient synovitis. The tool provides probability-based risk stratification from "
                "very low risk (<0.2-2%) with 0 predictors to very high risk (93-99.6%) with 4 predictors. "
                "Originally developed and validated in children aged 2-16 years, the criteria guide "
                "clinical decision-making regarding the need for arthrocentesis, surgical drainage, "
                "and antibiotic therapy. Higher predictor counts warrant more aggressive intervention, "
                "with 2 or more predictors typically indicating need for urgent orthopedic consultation "
                "and consideration of surgical intervention. The tool should be used as an adjunct to "
                "clinical judgment, not as a replacement for thorough clinical assessment.",
    response_description="The calculated Kocher Criteria risk assessment with probability range and clinical management recommendations",
    operation_id="kocher_criteria_septic_arthritis"
)
async def calculate_kocher_criteria_septic_arthritis(request: KocherCriteriaSepticArthritisRequest):
    """
    Calculates Kocher Criteria for Septic Arthritis
    
    The Kocher Criteria is a clinical prediction rule developed to differentiate septic 
    arthritis from transient synovitis in pediatric patients presenting with hip pain. 
    Originally described by Kocher et al. in 1999, this tool has been extensively 
    validated and remains one of the most widely used clinical decision aids in 
    pediatric orthopedics and emergency medicine.
    
    Clinical Background:
    Differentiating between septic arthritis and transient synovitis in children is 
    challenging but critical, as septic arthritis requires urgent surgical intervention 
    to prevent joint destruction and long-term complications. Transient synovitis is 
    benign and self-limiting, requiring only conservative management.
    
    Four Independent Predictors:
    1. Non-weight bearing on the affected limb
    2. Temperature >38.5°C (101.3°F) at presentation or in history
    3. Erythrocyte sedimentation rate (ESR) >40 mm/hr
    4. White blood cell count >12,000 cells/mm³
    
    Risk Stratification by Predictor Count:
    - 0 predictors: <0.2-2% risk - Very low risk, consider transient synovitis
    - 1 predictor: 3-9.5% risk - Low risk, may observe with close follow-up
    - 2 predictors: 35-40% risk - Moderate risk, consider arthrocentesis
    - 3 predictors: 72.8-93.1% risk - High risk, urgent surgical intervention indicated
    - 4 predictors: 93-99.6% risk - Very high risk, emergency surgery required
    
    Clinical Performance:
    - Extensively validated across multiple pediatric populations
    - High negative predictive value for low predictor counts
    - Excellent positive predictive value for high predictor counts
    - Maintains good discriminative ability across different clinical settings
    
    Clinical Applications:
    - Risk stratification in pediatric patients with hip pain and suspected joint infection
    - Guide decision-making for arthrocentesis and surgical intervention
    - Determine urgency of orthopedic consultation
    - Assist in antibiotic therapy decisions
    - Support family counseling and prognostic discussions
    
    Management Based on Results:
    - 0-1 predictors: Conservative management with close monitoring and reliable follow-up
    - 2 predictors: Strong consideration for arthrocentesis, urgent orthopedic consultation
    - 3-4 predictors: Urgent/emergent surgical drainage, immediate orthopedic consultation
    
    Important Considerations:
    - Originally developed for children aged 2-16 years with hip symptoms
    - Should be used in conjunction with clinical judgment and other diagnostic modalities
    - Clinical assessment remains paramount regardless of score
    - Serial evaluation may be necessary as clinical picture can evolve rapidly
    - Consider additional factors like C-reactive protein (CRP) >20 mg/L in some studies
    - May be less reliable in very young children (<2 years) or immunocompromised patients
    
    Contraindications for Use:
    - Non-hip joint symptoms (validation primarily in hip arthritis)
    - Chronic joint conditions or previous joint surgery
    - Immunocompromised patients (may have atypical presentations)
    - Very young infants (<2 years) where clinical assessment is more challenging
    
    When to Use:
    - Pediatric patients (typically 2-16 years) presenting with hip pain
    - Clinical suspicion of septic arthritis vs. transient synovitis
    - When laboratory studies and clinical assessment are available
    - To guide urgency of orthopedic consultation and intervention decisions
    
    Args:
        request: Kocher Criteria parameters including clinical and laboratory predictors
        
    Returns:
        KocherCriteriaSepticArthritisResponse: Risk assessment with clinical recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("kocher_criteria_septic_arthritis", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Kocher Criteria for Septic Arthritis",
                    "details": {"parameters": parameters}
                }
            )
        
        return KocherCriteriaSepticArthritisResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Kocher Criteria for Septic Arthritis",
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