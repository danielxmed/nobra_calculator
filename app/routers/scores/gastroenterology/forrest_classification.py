"""
Forrest Classification of Upper GI Bleeding Router

Endpoint for calculating Forrest Classification of Upper GI Bleeding.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.gastroenterology.forrest_classification import (
    ForrestClassificationRequest,
    ForrestClassificationResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/forrest_classification",
    response_model=ForrestClassificationResponse,
    summary="Calculate Forrest Classification of Upper GI Bleeding",
    description="Stratifies severity of upper GI bleeding according to endoscopic findings. Helps prognosticate and risk stratify patients, guides endoscopic therapeutic decisions, and assists in determining discharge versus inpatient monitoring.",
    response_description="The calculated forrest classification with interpretation",
    operation_id="calculate_forrest_classification"
)
async def calculate_forrest_classification(request: ForrestClassificationRequest):
    """
    Calculates Forrest Classification of Upper GI Bleeding
    
    The Forrest Classification stratifies severity of upper GI bleeding according to 
    endoscopic findings. Originally developed by Dr. John A. H. Forrest in 1974, this 
    classification system helps prognosticate and risk stratify patients, guides 
    endoscopic therapeutic decisions, and assists in determining discharge versus 
    inpatient monitoring.
    
    **Classification System:**
    - **Class 1A**: Active spurting bleeding (highest risk)
    - **Class 1B**: Active oozing bleeding (high risk)
    - **Class 2A**: Non-bleeding visible vessel (high risk)
    - **Class 2B**: Adherent clot (intermediate risk)
    - **Class 2C**: Flat pigmented spot (low risk)
    - **Class 3**: Clean ulcer base (lowest risk)
    
    **Risk Stratification:**
    - **Class 1A/1B**: Rebleeding 55%, mortality 11% - Immediate therapy required
    - **Class 2A**: Rebleeding 43%, mortality 11% - Endoscopic therapy recommended
    - **Class 2B**: Rebleeding 22%, mortality 7% - Consider intervention
    - **Class 2C**: Rebleeding 10%, mortality 3% - Usually medical management
    - **Class 3**: Rebleeding 5%, mortality 2% - Medical management appropriate
    
    **Clinical Applications:**
    - Risk stratification for rebleeding and mortality
    - Guidance for endoscopic therapeutic interventions
    - Decision-making for discharge versus continued monitoring
    - Standardized communication among healthcare providers
    - Research and quality improvement initiatives
    
    **Treatment Implications:**
    - **Immediate Intervention**: Classes 1A, 1B require emergency endoscopic therapy
    - **Recommended Intervention**: Class 2A requires endoscopic therapy
    - **Consider Intervention**: Class 2B management somewhat controversial
    - **Conservative Management**: Classes 2C and 3 usually managed medically
    
    **Key Features:**
    - Based on direct endoscopic visualization during upper endoscopy
    - Provides quantitative risk assessment for rebleeding and mortality
    - Widely accepted standard for communication and treatment planning
    - Validated in multiple studies over 50 years of clinical use
    
    Args:
        request: Forrest Classification parameters (endoscopic finding)
        
    Returns:
        ForrestClassificationResponse: Classification result with risk assessment and treatment guidance
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("forrest_classification", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Forrest Classification",
                    "details": {"parameters": parameters}
                }
            )
        
        return ForrestClassificationResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Forrest Classification",
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
                "message": "Internal error in Forrest Classification calculation",
                "details": {"error": str(e)}
            }
        )