"""
Clinical Disease Activity Index (CDAI) for Rheumatoid Arthritis Router

Endpoint for calculating CDAI rheumatoid arthritis disease activity score.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.rheumatology.cdai_rheumatoid_arthritis import (
    CdaiRheumatoidArthritisRequest,
    CdaiRheumatoidArthritisResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post("/cdai_rheumatoid_arthritis", response_model=CdaiRheumatoidArthritisResponse)
async def calculate_cdai_rheumatoid_arthritis(request: CdaiRheumatoidArthritisRequest):
    """
    Calculates Clinical Disease Activity Index (CDAI) for Rheumatoid Arthritis
    
    The CDAI is a validated composite measure for assessing rheumatoid arthritis disease 
    activity using only clinical parameters, without requiring laboratory tests. This 
    practical tool enables immediate treatment decision-making at the point of care and 
    supports evidence-based treat-to-target strategies.
    
    Key Advantages:
    - Immediate availability - no laboratory tests required
    - Simple calculation enables real-time clinical decision-making
    - More practical than DAS-28 for routine clinical use
    - Cost-effective monitoring without additional laboratory costs
    - Incorporates patient perspective through global assessment
    
    Assessment Components:
    1. Tender Joint Count (0-28 joints): Reflects subjective pain and inflammation
    2. Swollen Joint Count (0-28 joints): Objective measure of inflammatory involvement
    3. Patient Global Assessment (0-10 scale): Patient's overall disease impact perspective
    4. Provider Global Assessment (0-10 scale): Clinician's overall disease activity assessment
    
    CDAI Formula:
    CDAI = Tender Joint Count + Swollen Joint Count + Patient Global + Provider Global
    
    Disease Activity Categories:
    - Remission: CDAI ≤ 2.8 (target for all patients)
    - Low Disease Activity: CDAI > 2.8 to ≤ 10 (acceptable alternative target)
    - Moderate Disease Activity: CDAI > 10 to ≤ 22 (requires treatment intensification)
    - High Disease Activity: CDAI > 22 (urgent need for aggressive treatment)
    
    Clinical Applications:
    - Routine monitoring of RA disease activity
    - Treatment response assessment and optimization
    - Treat-to-target strategy implementation
    - Shared decision-making with patients
    - Quality improvement and outcome measurement
    
    Evidence Base:
    - Extensively validated in clinical practice and research
    - Moderate to good correlation with DAS-28 (Kappa = 0.533)
    - Recommended by international rheumatology organizations
    - Widely adopted in clinical practice worldwide
    
    The CDAI represents a significant advancement in practical rheumatoid arthritis 
    management, providing immediate, validated assessment that supports optimal 
    patient care and treatment outcomes.
    
    Args:
        request: CDAI assessment parameters including tender and swollen joint counts 
                and patient/provider global assessments on 0-10 scales
        
    Returns:
        CdaiRheumatoidArthritisResponse: Comprehensive disease activity assessment 
        with CDAI score, activity category, treatment recommendations, and detailed 
        clinical guidance for RA management
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("cdai_rheumatoid_arthritis", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating CDAI for Rheumatoid Arthritis",
                    "details": {"parameters": parameters}
                }
            )
        
        return CdaiRheumatoidArthritisResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for CDAI Rheumatoid Arthritis calculation",
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
                "message": "Internal error in CDAI calculation",
                "details": {"error": str(e)}
            }
        )