"""
Berg Balance Scale (BBS) Router

Endpoint for calculating Berg Balance Scale to assess balance and fall risk in older adults.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.geriatrics.berg_balance_scale import (
    BergBalanceScaleRequest,
    BergBalanceScaleResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post("/berg_balance_scale", response_model=BergBalanceScaleResponse)
async def calculate_berg_balance_scale(request: BergBalanceScaleRequest):
    """
    Calculates Berg Balance Scale (BBS) for Balance and Fall Risk Assessment
    
    The Berg Balance Scale is a validated 14-item assessment tool designed to evaluate 
    functional balance and predict fall risk in older adults and patients with neurological 
    conditions. It is widely used in clinical practice and research settings.
    
    **Target Population:**
    - Community-dwelling older adults (≥65 years)
    - Patients with neurological conditions (stroke, Parkinson's disease, multiple sclerosis)
    - Individuals with vestibular disorders or brain injury
    - Adults requiring balance assessment for rehabilitation planning
    
    **Assessment Components (14 Tasks, 0-4 points each):**
    
    **Basic Mobility Tasks:**
    1. **Sitting to Standing** - Ability to rise from chair
    2. **Standing Unsupported** - Stand for 2 minutes without support
    3. **Sitting Unsupported** - Sit without back support for 2 minutes
    4. **Standing to Sitting** - Controlled descent to sitting
    5. **Transfers** - Move between two chairs safely
    
    **Postural Control Tasks:**
    6. **Standing Eyes Closed** - Stand 10 seconds with eyes closed
    7. **Standing Feet Together** - Narrow base of support for 1 minute
    8. **Reaching Forward** - Functional reach test while standing
    9. **Picking Up Object** - Retrieve item from floor while standing
    
    **Dynamic Balance Tasks:**
    10. **Turning to Look Behind** - Head and trunk rotation
    11. **Turning 360 Degrees** - Complete turn in both directions
    12. **Placing Alternate Foot on Step** - Step up/down repetitively
    13. **Standing One Foot in Front** - Tandem stance position
    14. **Standing on One Leg** - Single limb support balance
    
    **Scoring Criteria:**
    - **4 points**: Independent and safe performance
    - **3 points**: Minimal difficulty or need for supervision
    - **2 points**: Moderate difficulty in performance
    - **1 point**: Significant difficulty or need for assistance  
    - **0 points**: Unable to perform task safely
    
    **Score Interpretation and Fall Risk:**
    - **45-56 points**: **Independent** - Good balance, low fall risk
    - **41-44 points**: **Increased Fall Risk** - Moderate impairment, intervention beneficial
    - **21-40 points**: **Walking with Assistance** - Significant impairment, high fall risk
    - **0-20 points**: **Wheelchair Bound** - Severe impairment, extremely high fall risk
    
    **Clinical Guidelines:**
    
    **Equipment Required:**
    - Two standard chairs (one with armrests)
    - Stopwatch or timer
    - Step or footstool (6 inches high)
    - Ruler (for measuring reach)
    - Shoe or slipper for pickup task
    
    **Administration:**
    - Takes approximately 15-20 minutes to complete
    - Requires trained healthcare professional
    - Safe environment with spotting capability
    - Clear instructions and demonstration for each task
    
    **Psychometric Properties:**
    - **Inter-rater Reliability**: Excellent (ICC = 0.95)
    - **Test-retest Reliability**: Excellent (ICC = 0.91)
    - **Internal Consistency**: High (Cronbach's α = 0.96)
    - **Concurrent Validity**: Strong correlations with other balance measures
    - **Predictive Validity**: Established for fall risk prediction
    
    **Clinical Applications:**
    - **Baseline Assessment**: Initial evaluation of balance function
    - **Progress Monitoring**: Track changes over time with intervention
    - **Fall Risk Screening**: Identify individuals at increased fall risk
    - **Discharge Planning**: Assess safety for community mobility
    - **Research**: Outcome measure for balance interventions
    
    **Intervention Recommendations by Score:**
    
    **Independent (45-56):**
    - Continue regular physical activity
    - Balance maintenance exercises
    - Annual reassessment
    - Environmental safety review
    
    **Increased Fall Risk (41-44):**
    - Structured balance training program
    - Physical therapy evaluation
    - Home safety assessment
    - Quarterly reassessment
    
    **Walking with Assistance (21-40):**
    - Immediate PT referral
    - Assistive device prescription
    - Comprehensive fall prevention program
    - Monthly progress monitoring
    
    **Wheelchair Bound (0-20):**
    - Comprehensive rehabilitation assessment
    - Wheelchair mobility training
    - Maximum fall prevention strategies
    - Intensive rehabilitation consideration
    
    **Limitations and Considerations:**
    - May have ceiling effect for mildly impaired individuals
    - Not suitable for acutely ill or unstable patients
    - Requires adequate cognitive function for instruction following
    - Should not be sole determinant of fall risk
    - Consider age, comorbidities, and environmental factors
    
    **Research Evidence:**
    - Validated cut-off score <45 for increased fall risk
    - Score ≤36 is 100% predictive of falls within 6 months
    - Responsive to change with balance interventions
    - Used in numerous clinical trials and outcome studies
    
    Args:
        request: Berg Balance Scale assessment parameters (14 task scores)
        
    Returns:
        BergBalanceScaleResponse: BBS score with clinical interpretation and management guidance
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("berg_balance_scale", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Berg Balance Scale",
                    "details": {"parameters": parameters}
                }
            )
        
        return BergBalanceScaleResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Berg Balance Scale calculation",
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