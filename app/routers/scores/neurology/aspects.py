"""
Alberta Stroke Program Early CT Score (ASPECTS) Router

Endpoint for calculating ASPECTS Score for stroke prognostication.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.neurology.aspects import (
    AspectsRequest,
    AspectsResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/aspects",
    response_model=AspectsResponse,
    summary="Calculate Alberta Stroke Program Early CT Score (ASPECTS)",
    description="Quantifies early ischemic changes in MCA territory on non-contrast CT to predict stroke outcome and guide treatment decisions",
    response_description="The calculated aspects with interpretation",
    operation_id="aspects"
)
async def calculate_aspects(request: AspectsRequest):
    """
    Calculates Alberta Stroke Program Early CT Score (ASPECTS)
    
    The ASPECTS score is a 10-point quantitative topographic CT scan score that 
    quantifies early ischemic changes in the middle cerebral artery (MCA) territory 
    on non-contrast CT to predict stroke outcome and guide treatment decisions.
    
    Key Features:
    - Evaluates 10 specific brain regions on non-contrast CT
    - Start with 10 points, subtract 1 for each abnormal region
    - Correlates inversely with NIHSS score and stroke severity
    - Predicts 3-month functional outcome and symptomatic ICH risk
    - Used for treatment selection in acute stroke
    
    Brain Regions Assessed:
    
    Basal Ganglia Level (7 regions):
    - Caudate nucleus
    - Lentiform nucleus (putamen + globus pallidus)
    - Internal capsule
    - Insular ribbon/cortex
    - M1: Anterior MCA cortex (frontal operculum)
    - M2: MCA cortex lateral to insular ribbon (anterior temporal)
    - M3: Posterior MCA cortex (posterior temporal)
    
    Supraganglionic Level (3 regions):
    - M4: Anterior MCA cortex (superior to M1)
    - M5: Lateral MCA cortex (superior to M2)
    - M6: Posterior MCA cortex (superior to M3)
    
    Score Interpretation:
    
    ASPECTS 8-10 (Favorable):
    - Limited early ischemic changes
    - Good prognosis for functional outcome
    - Low risk of symptomatic hemorrhage
    - Good candidate for reperfusion therapy
    - Greater benefit from IV thrombolysis expected
    
    ASPECTS 5-7 (Large Infarction):
    - Large MCA territory involvement
    - Poor functional outcome likely
    - High risk (14%) of symptomatic ICH with IV thrombolysis
    - Mechanical thrombectomy may be considered if ASPECTS ≥6
    
    ASPECTS 0-4 (Extensive Infarction):
    - Extensive MCA territory involvement
    - Very poor prognosis
    - Very high risk of symptomatic hemorrhage
    - Consider palliative care discussions
    
    Clinical Applications:
    - Acute stroke prognostication and outcome prediction
    - Treatment selection (IV thrombolysis, mechanical thrombectomy)
    - Risk stratification for symptomatic hemorrhage
    - Resource allocation and care planning decisions
    - Research standardization in stroke trials
    
    Important Clinical Notes:
    - Evaluate all axial CT cuts, not just two standardized levels
    - Requires focal edema or parenchymal hypoattenuation
    - Subtract 1 point for each region with ≥1/3 area involvement
    - Good interrater reliability with proper training
    - Used in major stroke trials (ESCAPE, SWIFT-PRIME)
    - Should be combined with clinical assessment and time from onset
    
    Advantages:
    - Simple and rapid assessment
    - Widely validated and standardized
    - Strong correlation with clinical outcomes
    - Guides evidence-based treatment decisions
    - Improves stroke care quality and consistency
    
    Args:
        request: Parameters needed for ASPECTS calculation
        
    Returns:
        AspectsResponse: ASPECTS score with clinical interpretation and treatment recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("aspects", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating ASPECTS Score",
                    "details": {"parameters": parameters}
                }
            )
        
        return AspectsResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for ASPECTS Score",
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