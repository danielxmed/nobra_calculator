"""
Bastion Classification of Lower Limb Blast Injuries Router

Endpoint for calculating Bastion Classification of Lower Limb Blast Injuries.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.emergency.bastion_classification import (
    BastionClassificationRequest,
    BastionClassificationResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/bastion_classification",
    response_model=BastionClassificationResponse,
    summary="Calculate Bastion Classification of Lower Limb Blast Inju...",
    description="Stratifies lower limb blast injuries to guide treatment. Developed by military surgeons at Camp Bastion, Afghanistan, to classify explosion-related lower extremity injuries and correlate with treatment needs.",
    response_description="The calculated bastion classification with interpretation",
    operation_id="calculate_bastion_classification"
)
async def calculate_bastion_classification(request: BastionClassificationRequest):
    """
    Calculates Bastion Classification of Lower Limb Blast Injuries
    
    The Bastion Classification system was developed by military surgeons at Camp Bastion, 
    Afghanistan, to stratify explosion-related lower extremity injuries. It provides a 
    comprehensive classification that correlates with treatment needs and facilitates 
    communication between clinicians.
    
    **Classification System:**
    - **Classes 1-5**: Based on anatomical level of injury
    - **Suffixes (S, A, B, C, D)**: Denote associated injuries important for treatment planning
    
    **Clinical Context:**
    - 69% of validation cohort injuries were traumatic amputations
    - 49% of casualties suffered bilateral lower limb amputation
    - Class 3 (proximal lower leg/thigh) was most common (49%)
    - Classes 4-5 (preventing effective tourniquet) accounted for 18% of injuries
    
    **Treatment Correlation:**
    - Classes 1-3: Effective tourniquet application possible
    - Classes 4-5: May require operative proximal vascular control
    - Associated injuries (suffixes) guide additional interventions
    
    Args:
        request: Parameters including injury class and associated injuries
        
    Returns:
        BastionClassificationResponse: Classification with management recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("bastion_classification", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Bastion Classification",
                    "details": {"parameters": parameters}
                }
            )
        
        return BastionClassificationResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Bastion Classification",
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