"""
Body Roundness Index (BRI) Router

Endpoint for calculating Body Roundness Index.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.general.body_roundness_index import (
    BodyRoundnessIndexRequest,
    BodyRoundnessIndexResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post("/body_roundness_index", response_model=BodyRoundnessIndexResponse)
async def calculate_body_roundness_index(request: BodyRoundnessIndexRequest):
    """
    Calculates Body Roundness Index (BRI)
    
    The Body Roundness Index estimates % body fat and % visceral adipose tissue 
    based on waist circumference and height measurements. It uses a geometric 
    model that considers the body as an ellipse to assess body shape and 
    associated health risks.
    
    **Clinical Applications:**
    
    **Risk Assessment:**
    - Predicts all-cause mortality with U-shaped curve
    - Superior to BMI for cardiometabolic risk
    - Correlates with visceral adipose tissue
    - Identifies both underweight and obesity risks
    
    **Metabolic Health:**
    - Diabetes risk stratification
    - Metabolic syndrome screening
    - Insulin resistance assessment
    - Cardiovascular risk evaluation
    
    **Body Composition:**
    - Estimates body fat percentage
    - Assesses central adiposity
    - Tracks changes with interventions
    - Complements other anthropometric measures
    
    **Advantages over BMI:**
    - Accounts for body shape, not just mass
    - Better correlation with visceral fat
    - More accurate in athletic populations
    - Considers fat distribution patterns
    
    **Measurement Protocol:**
    
    **Waist Circumference:**
    1. Patient stands with feet together
    2. Arms relaxed at sides
    3. Measure at umbilicus level
    4. End of normal expiration
    5. Tape parallel to floor
    6. Snug but not compressing
    
    **Height:**
    1. Remove shoes
    2. Stand against wall/stadiometer
    3. Heels together
    4. Head in Frankfurt plane
    5. Record to nearest 0.1 cm
    
    **Interpretation Guidelines:**
    
    **BRI Categories:**
    - <3.41: Low (HR 0.57 for mortality)
    - 3.41-4.45: Below average (HR 0.81)
    - 4.45-5.46: Average/Reference (HR 1.0)
    - 5.46-6.91: Above average (HR 1.48)
    - ≥6.91: High (HR 1.62)
    
    **Clinical Actions:**
    - BRI <3.41: Assess for malnutrition
    - BRI 3.41-5.46: Routine monitoring
    - BRI >5.46: Lifestyle interventions
    - BRI >6.91: Aggressive risk modification
    
    **Special Populations:**
    - Athletes: May have higher BRI with low fat
    - Elderly: Consider muscle mass loss
    - Children: Not validated for pediatrics
    - Pregnancy: Not applicable
    
    Args:
        request: Waist circumference and height measurements
        
    Returns:
        BodyRoundnessIndexResponse: BRI value with clinical interpretation
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("body_roundness_index", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Body Roundness Index",
                    "details": {"parameters": parameters}
                }
            )
        
        return BodyRoundnessIndexResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Body Roundness Index",
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