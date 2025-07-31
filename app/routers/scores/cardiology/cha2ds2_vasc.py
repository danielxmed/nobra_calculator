"""
Cha2Ds2 Vasc router endpoint
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.cardiology import Cha2ds2VascRequest, Cha2ds2VascResponse
from app.services.calculator_service import calculator_service

router = APIRouter()

@router.post("/cha2ds2_vasc", 
             response_model=Cha2ds2VascResponse,
             summary="Calculate CHA₂DS₂-VASc Score",
             description="Assesses stroke risk in atrial fibrillation patients for anticoagulation decisions",
             response_description="Stroke risk assessment with anticoagulation recommendations",
             operation_id="cha2ds2_vasc")
async def calculate_cha2ds2_vasc(request: Cha2ds2VascRequest):
    """
    **Calculate CHA₂DS₂-VASc Score for Atrial Fibrillation Stroke Risk**
    
    Evidence-based stroke risk stratification tool for patients with non-valvular 
    atrial fibrillation, essential for anticoagulation decision-making.
    
    **Clinical Applications:**
    - Stroke risk stratification in AF patients
    - Anticoagulation therapy decisions
    - Risk-benefit analysis (thrombotic vs bleeding risk)
    - Patient counseling and shared decision-making
    - Quality metrics and guideline compliance
    
    **Score Components (0-9 points):**
    - **C**ongestive heart failure (1 point)
    - **H**ypertension (1 point)  
    - **A**ge ≥75 years (2 points)
    - **D**iabetes (1 point)
    - **S**troke/TIA/thromboembolism history (2 points)
    - **V**ascular disease (1 point)
    - **A**ge 65-74 years (1 point)
    - **S**ex category female (1 point)
    
    **Management Guidelines:**
    - Score 0 (men): No anticoagulation recommended
    - Score 1 (men): Consider anticoagulation
    - Score ≥2: Oral anticoagulation recommended
    - Women with score 1 (sex only): No anticoagulation
    
    **Anticoagulation Options:**
    - DOACs preferred: dabigatran, rivaroxaban, apixaban, edoxaban
    - Warfarin (INR 2-3) if DOACs contraindicated
    - Consider HAS-BLED score for bleeding risk assessment
    """
    try:
        # Convert request to dictionary
        parameters = {
            "age": request.age,
            "sex": request.sex.value,
            "congestive_heart_failure": request.congestive_heart_failure,
            "hypertension": request.hypertension,
            "stroke_tia_thromboembolism": request.stroke_tia_thromboembolism,
            "vascular_disease": request.vascular_disease,
            "diabetes": request.diabetes
        }
        
        # Execute calculation
        result = calculator_service.calculate_score("cha2ds2_vasc", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating CHA₂DS₂-VASc",
                    "details": {"parameters": parameters}
                }
            )
        
        return Cha2ds2VascResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for CHA₂DS₂-VASc",
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