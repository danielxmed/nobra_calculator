"""
ACR/EULAR Gout Classification Criteria Router

Endpoint for calculating ACR/EULAR gout classification criteria.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.rheumatology.acr_eular_gout import (
    AcrEularGoutRequest,
    AcrEularGoutResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/acr_eular_gout",
    response_model=AcrEularGoutResponse,
    summary="Calculate ACR/EULAR Gout Classification Criteria",
    description="Provides formal diagnostic criteria for gout using a 3-step approach: entry criterion, sufficient criterion, and classification criteria requiring ≥7 points for positive diagnosis",
    response_description="The calculated acr eular gout with interpretation",
    operation_id="calculate_acr_eular_gout"
)
async def calculate_acr_eular_gout(request: AcrEularGoutRequest):
    """
    Calculates ACR/EULAR Gout Classification Criteria
    
    This calculator implements the 2015 ACR/EULAR classification criteria for gout,
    which provide a systematic approach to gout classification using a 3-step process:
    
    Step 1 - Entry Criterion: 
    At least one episode of swelling, pain, or tenderness in a peripheral joint or bursa
    
    Step 2 - Sufficient Criterion:
    If monosodium urate (MSU) crystals are identified in symptomatic joint, bursa, or 
    tophus by polarized light microscopy, the diagnosis is definite gout
    
    Step 3 - Classification Criteria:
    If MSU crystals are not identified or synovial fluid analysis was not performed,
    a scoring system across 8 domains is used. A total score ≥7 points indicates
    classification as gout.
    
    The classification criteria were developed through an international collaborative
    initiative to improve the accuracy of gout classification for clinical and research
    purposes. They demonstrate high sensitivity (85%) and specificity (78%) when used
    appropriately.
    
    Key clinical applications:
    - Early identification of gout in patients with acute arthritis
    - Standardized classification for clinical research
    - Guidance for appropriate therapeutic intervention
    - Differentiation from other crystal arthropathies and inflammatory conditions
    
    Prerequisites for use:
    - At least one episode of peripheral joint or bursa swelling, pain, or tenderness
    - Clinical assessment by trained healthcare provider
    - Appropriate laboratory and imaging studies as available
    
    Args:
        request: Parameters including entry criterion, MSU crystal status, clinical features,
                laboratory results, and imaging findings
        
    Returns:
        AcrEularGoutResponse: Classification result with clinical interpretation and recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("acr_eular_gout", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating ACR/EULAR gout classification criteria",
                    "details": {"parameters": parameters}
                }
            )
        
        return AcrEularGoutResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for ACR/EULAR gout classification criteria",
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