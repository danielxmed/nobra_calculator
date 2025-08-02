"""
Montreal Classification for Inflammatory Bowel Disease (IBD) Router

Endpoint for calculating Montreal Classification for IBD.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.gastroenterology.montreal_classification_ibd import (
    MontrealClassificationIbdRequest,
    MontrealClassificationIbdResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/montreal_classification_ibd",
    response_model=MontrealClassificationIbdResponse,
    summary="Calculate Montreal Classification for Inflammatory Bowel Disease (IBD)",
    description="Calculates the Montreal Classification for Crohn's disease and ulcerative colitis to provide standardized "
                "phenotypic characterization for clinical management and research. The classification system replaced the "
                "Vienna Classification in 2005 and includes age at diagnosis (A1-A3), anatomical distribution (location "
                "for Crohn's: L1-L4, extent for UC: E1-E3), and disease behavior/severity (behavior for Crohn's: B1-B3 "
                "with optional perianal modifier 'p', severity for UC: S0-S3). This classification helps predict disease "
                "course, guide treatment decisions, and standardize clinical research. For Crohn's disease, the classification "
                "evolves over time as inflammatory disease (B1) may progress to stricturing (B2) or penetrating (B3) behavior. "
                "The system is essential for personalized IBD management and risk stratification.",
    response_description="The Montreal Classification code with detailed phenotypic characterization and clinical management recommendations",
    operation_id="montreal_classification_ibd"
)
async def calculate_montreal_classification_ibd(request: MontrealClassificationIbdRequest):
    """
    Calculates Montreal Classification for Inflammatory Bowel Disease (IBD)
    
    The Montreal Classification provides standardized phenotypic characterization 
    of IBD based on three main components:
    
    1. Age at diagnosis (A1: <17 years, A2: 17-40 years, A3: >40 years)
    2. Anatomical distribution:
       - Crohn's Location: L1 (ileal), L2 (colonic), L3 (ileocolonic), L4 (upper GI)
       - UC Extent: E1 (proctitis), E2 (left-sided), E3 (extensive)
    3. Disease behavior/severity:
       - Crohn's Behavior: B1 (inflammatory), B2 (stricturing), B3 (penetrating)
       - UC Severity: S0 (remission), S1 (mild), S2 (moderate), S3 (severe)
    
    Additional modifiers:
    - Perianal disease modifier 'p' can be added to any Crohn's behavior
    
    Classification examples:
    - Crohn's: A2L3B1p = Young adult, ileocolonic, inflammatory with perianal disease
    - UC: A1E3S2 = Pediatric, extensive colitis, moderate activity
    
    Clinical significance:
    - Predicts disease course and complications
    - Guides treatment intensity and surveillance strategies
    - Standardizes phenotyping for clinical research
    - Essential for personalized IBD management
    
    Args:
        request: Montreal Classification parameters including disease type, age, and disease-specific characteristics
        
    Returns:
        MontrealClassificationIbdResponse: Classification code with clinical interpretation and management recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("montreal_classification_ibd", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Montreal Classification for IBD",
                    "details": {"parameters": parameters}
                }
            )
        
        return MontrealClassificationIbdResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Montreal Classification IBD calculation",
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
                "message": "Internal error in Montreal Classification IBD calculation",
                "details": {"error": str(e)}
            }
        )