"""
Wisconsin Criteria for Maxillofacial Trauma CT Router

Endpoint for calculating CT imaging recommendations after facial trauma using Wisconsin Criteria.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.emergency.wisconsin_criteria_maxillofacial_trauma import (
    WisconsinCriteriaMaxillofacialTraumaRequest,
    WisconsinCriteriaMaxillofacialTraumaResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/wisconsin_criteria_maxillofacial_trauma",
    response_model=WisconsinCriteriaMaxillofacialTraumaResponse,
    summary="Calculate Wisconsin Criteria for Maxillofacial Trauma CT",
    description="Applies the Wisconsin Criteria clinical decision rule to determine the need for CT "
                "imaging after maxillofacial trauma. This validated tool evaluates eight high-risk "
                "clinical factors (high-energy mechanism, facial deformity, malocclusion, facial "
                "numbness, periorbital swelling, diplopia, palpable step-off, epistaxis) to help "
                "emergency physicians avoid unnecessary radiation exposure while ensuring appropriate "
                "imaging for patients at risk of significant facial fractures. The presence of any "
                "criterion indicates CT is recommended.",
    response_description="CT imaging recommendation with detailed clinical assessment and management guidance",
    operation_id="wisconsin_criteria_maxillofacial_trauma"
)
async def calculate_wisconsin_criteria_maxillofacial_trauma(request: WisconsinCriteriaMaxillofacialTraumaRequest):
    """
    Calculates Wisconsin Criteria for Maxillofacial Trauma CT Recommendation
    
    The Wisconsin Criteria is a validated clinical decision rule that helps emergency 
    physicians determine which patients with facial trauma require CT imaging.
    
    Clinical Applications:
    - Standardizes imaging decisions in facial trauma evaluation
    - Reduces unnecessary radiation exposure in low-risk patients
    - High sensitivity for detecting clinically significant facial fractures
    - Guides appropriate use of healthcare resources
    
    Eight High-Risk Criteria Evaluated:
    1. High-energy mechanism (MVCs, falls >3 feet, assault with object, sports)
    2. Visible facial deformity or asymmetry
    3. Dental malocclusion or limited mouth opening
    4. Facial numbness (especially infraorbital distribution)
    5. Significant periorbital swelling or hematoma
    6. Double vision or diplopia
    7. Palpable step-off deformity of facial bones
    8. Epistaxis or nasal deformity
    
    Decision Rule:
    - ANY positive criterion → CT indicated (high sensitivity approach)
    - ALL negative criteria → CT not indicated (low-risk observation)
    
    Important Considerations:
    - Validated for adult patients in emergency department settings
    - Not validated for pediatric patients or penetrating trauma
    - Complements but does not replace clinical judgment
    - Consider patient factors and institutional protocols
    
    Args:
        request: Clinical parameters including mechanism and examination findings
        
    Returns:
        WisconsinCriteriaMaxillofacialTraumaResponse: CT recommendation with detailed assessment
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("wisconsin_criteria_maxillofacial_trauma", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Wisconsin Criteria for Maxillofacial Trauma",
                    "details": {"parameters": parameters}
                }
            )
        
        return WisconsinCriteriaMaxillofacialTraumaResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Wisconsin Criteria calculation",
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
                "message": "Internal error in Wisconsin Criteria calculation",
                "details": {"error": str(e)}
            }
        )