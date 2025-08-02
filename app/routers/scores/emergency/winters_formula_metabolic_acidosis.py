"""
Winters' Formula for Metabolic Acidosis Compensation Router

Endpoint for calculating expected arterial pCO₂ compensation in metabolic acidosis.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.emergency.winters_formula_metabolic_acidosis import (
    WintersFormulaMetabolicAcidosisRequest,
    WintersFormulaMetabolicAcidosisResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/winters_formula_metabolic_acidosis",
    response_model=WintersFormulaMetabolicAcidosisResponse,
    summary="Calculate Winters' Formula for Metabolic Acidosis Compensation",
    description="Calculates the expected arterial pCO₂ compensation in pure metabolic acidosis using "
                "Winters' Formula: Expected pCO₂ = 1.5 × [HCO₃⁻] + 8 (± 2 mmHg). This validated "
                "formula helps clinicians assess whether respiratory compensation is appropriate, "
                "insufficient, or excessive in patients with metabolic acidosis. The measured pCO₂ "
                "should fall within ± 2 mmHg of the calculated value for appropriate compensation. "
                "Essential for acid-base disorder evaluation and mechanical ventilation management.",
    response_description="The calculated expected pCO₂ with compensation analysis and clinical management recommendations",
    operation_id="winters_formula_metabolic_acidosis"
)
async def calculate_winters_formula_metabolic_acidosis(request: WintersFormulaMetabolicAcidosisRequest):
    """
    Calculates Winters' Formula for Metabolic Acidosis Compensation
    
    Winters' Formula predicts the expected arterial pCO₂ in patients with pure 
    metabolic acidosis to assess the adequacy of respiratory compensation.
    
    Clinical Applications:
    - Assessment of respiratory compensation in metabolic acidosis
    - Detection of mixed acid-base disorders
    - Evaluation of respiratory function adequacy
    - Guidance for mechanical ventilation settings in critically ill patients
    
    Formula: Expected pCO₂ = 1.5 × [HCO₃⁻] + 8 (± 2 mmHg)
    
    Interpretation:
    - Within ± 2 mmHg: Appropriate respiratory compensation
    - >2 mmHg higher: Inadequate compensation or concurrent respiratory acidosis
    - >2 mmHg lower: Overcompensation or concurrent respiratory alkalosis
    
    Important Considerations:
    - Formula applies only to pure metabolic acidosis (not mixed disorders)
    - Requires steady-state conditions (6-24 hours after onset)
    - Should be used with arterial blood gas analysis for accurate assessment
    - pH should be <7.35 to confirm metabolic acidosis
    
    Args:
        request: Parameters including bicarbonate level and optional measured pCO₂
        
    Returns:
        WintersFormulaMetabolicAcidosisResponse: Expected pCO₂ with compensation analysis and recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("winters_formula_metabolic_acidosis", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Winters' Formula for Metabolic Acidosis Compensation",
                    "details": {"parameters": parameters}
                }
            )
        
        return WintersFormulaMetabolicAcidosisResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Winters' Formula calculation",
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
                "message": "Internal error in Winters' Formula calculation",
                "details": {"error": str(e)}
            }
        )