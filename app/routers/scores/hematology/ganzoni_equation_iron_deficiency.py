"""
Ganzoni Equation for Iron Deficiency Anemia Router

Endpoint for calculating iron deficit using the Ganzoni equation.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.hematology.ganzoni_equation_iron_deficiency import (
    GanzoniEquationIronDeficiencyRequest,
    GanzoniEquationIronDeficiencyResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/ganzoni_equation_iron_deficiency",
    response_model=GanzoniEquationIronDeficiencyResponse,
    summary="Calculate Ganzoni Equation for Iron Deficiency Anemia",
    description="Assesses total body iron deficit for iron replacement therapy. Calculates the precise amount of iron needed to replenish body iron stores and correct hemoglobin levels in patients with iron deficiency anemia.",
    response_description="The calculated ganzoni equation iron deficiency with interpretation",
    operation_id="ganzoni_equation_iron_deficiency"
)
async def calculate_ganzoni_equation_iron_deficiency(request: GanzoniEquationIronDeficiencyRequest):
    """
    Calculates Iron Deficit using Ganzoni Equation for Iron Deficiency Anemia
    
    The Ganzoni equation is a validated mathematical formula used to calculate the total 
    body iron deficit in patients with iron deficiency anemia. This calculation helps 
    clinicians determine the precise amount of iron replacement therapy needed to correct 
    both hemoglobin levels and replenish iron stores.
    
    **Formula**: Iron deficit (mg) = body weight (kg) × (target Hb - current Hb) (g/dL) × 2.4 + iron stores (mg)
    
    **Clinical Applications**:
    - Dosing calculations for IV iron therapy in iron deficiency anemia
    - Assessment of total body iron deficit before treatment initiation
    - Planning iron replacement therapy regimens (oral vs IV)
    - Monitoring adequacy of iron repletion therapy
    - Pre-operative iron optimization protocols
    
    **Key Parameters**:
    - **Body Weight**: Must be ≥35 kg (formula validation threshold)
    - **Current Hemoglobin**: Recent measurement representing stable state
    - **Target Hemoglobin**: Typically 15 g/dL for adults, adjusted for age/comorbidities
    - **Iron Stores**: Usually 500 mg for adults (minimum for small women)
    
    **Clinical Significance**:
    - **<500 mg**: Mild deficit - consider oral iron or single IV dose
    - **500-1000 mg**: Moderate deficit - IV iron preferred, 1-2 sessions
    - **1000-2000 mg**: Severe deficit - multiple IV iron sessions required
    - **>2000 mg**: Very severe deficit - investigate cause, specialist referral
    
    **Safety Considerations**:
    - Formula validated only for patients ≥35 kg body weight
    - Monitor for iron overload (ferritin >500 ng/mL, TSAT >50%)
    - Consider modified formula if TSAT >20% and ferritin >50 ng/mL
    - Account for ongoing blood loss and chronic inflammation
    
    Args:
        request: Patient data including body weight, current and target hemoglobin, 
                and iron stores requirement for deficit calculation
        
    Returns:
        GanzoniEquationIronDeficiencyResponse: Calculated iron deficit with 
                                             severity classification and comprehensive 
                                             treatment recommendations including 
                                             IV iron selection and monitoring protocols
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("ganzoni_equation_iron_deficiency", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Ganzoni Equation for Iron Deficiency",
                    "details": {"parameters": parameters}
                }
            )
        
        return GanzoniEquationIronDeficiencyResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Ganzoni Equation calculation",
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
                "message": "Internal error in Ganzoni Equation calculation",
                "details": {"error": str(e)}
            }
        )