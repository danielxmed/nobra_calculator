"""
Urine Anion Gap Router

Endpoint for calculating Urine Anion Gap.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.nephrology.urine_anion_gap import (
    UrineAnionGapRequest,
    UrineAnionGapResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/urine_anion_gap",
    response_model=UrineAnionGapResponse,
    summary="Calculate Urine Anion Gap",
    description="Calculates the Urine Anion Gap for evaluation of non-anion gap metabolic acidosis. "
                "This validated diagnostic tool helps differentiate between renal and extrarenal causes of "
                "normal anion gap metabolic acidosis by providing an indirect assessment of urinary ammonium "
                "excretion capacity. The calculation uses three urinary electrolytes (sodium, potassium, chloride) "
                "from a fresh urine sample. A negative gap (<-10 mEq/L) suggests extrarenal bicarbonate loss "
                "(typically diarrhea), while a positive gap (>+20 mEq/L) suggests renal tubular acidosis. "
                "Normal range is -10 to +20 mEq/L. This tool is essential for nephrologists and emergency "
                "physicians evaluating acid-base disorders and helps guide appropriate treatment strategies.",
    response_description="The calculated urine anion gap with diagnostic interpretation and management recommendations",
    operation_id="urine_anion_gap"
)
async def calculate_urine_anion_gap(request: UrineAnionGapRequest):
    """
    Calculates Urine Anion Gap
    
    The Urine Anion Gap is a simple but powerful diagnostic tool used specifically 
    in the evaluation of non-anion gap (normal anion gap) metabolic acidosis. It 
    provides an indirect assessment of the kidney's ability to excrete ammonium (NH4+) 
    in response to acidosis.
    
    Formula and Calculation:
    Urine Anion Gap = Urine Na+ + Urine K+ - Urine Cl-
    
    The calculation is based on the principle that ammonium (NH4+) is not routinely 
    measured in clinical laboratories, but its excretion can be estimated indirectly. 
    When the kidney appropriately increases ammonium excretion in response to acidosis, 
    chloride excretion increases proportionally, making the anion gap negative.
    
    Clinical Applications:
    
    1. **Differential Diagnosis of Normal Anion Gap Metabolic Acidosis:**
       - Distinguishes renal from extrarenal causes
       - Guides further diagnostic workup
       - Helps determine appropriate treatment approach
    
    2. **Evaluation for Renal Tubular Acidosis:**
       - Screening tool for RTA when clinical suspicion exists
       - Helps classify type of RTA in conjunction with other tests
       - Monitors treatment response in known RTA patients
    
    3. **Assessment of Renal Acidification Capacity:**
       - Evaluates kidney's ability to respond to acid load
       - Useful in chronic kidney disease evaluation
    
    Interpretation Guidelines:
    
    **Negative UAG (<-10 mEq/L) - Extrarenal Cause:**
    - Indicates appropriate renal response to acidosis
    - Most commonly: diarrhea, fistulas, carbonic anhydrase inhibitors
    - Treatment: Address underlying GI cause, supportive care
    
    **Normal UAG (-10 to +20 mEq/L) - Normal Range:**
    - May be normal variant or early acid-base disorder
    - Requires clinical correlation and possibly repeat testing
    - Consider other diagnostic modalities if acidosis present
    
    **Positive UAG (>+20 mEq/L) - Renal Cause:**
    - Suggests impaired renal ammonium excretion (RTA)
    - Requires further evaluation: urine pH, citrate, calcium levels
    - Treatment: Alkali therapy, management of underlying kidney disease
    
    Clinical Pearls:
    - Use only in normal anion gap metabolic acidosis (serum AG 8-12 mEq/L)
    - Requires fresh urine sample analyzed within 2 hours
    - Less reliable in severe volume depletion or very low urine chloride
    - Consider urine osmolar gap as alternative in complex cases
    - Hyperchloremic IV fluids can worsen these acidoses
    
    Limitations:
    - Not applicable to high anion gap metabolic acidosis
    - May be inaccurate in severe dehydration
    - Requires accurate measurement of all three electrolytes
    - Should be interpreted in clinical context, not in isolation
    
    Args:
        request: Urine electrolyte concentrations (Na+, K+, Cl-) from fresh sample
        
    Returns:
        UrineAnionGapResponse: Calculated gap with diagnostic interpretation
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("urine_anion_gap", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Urine Anion Gap",
                    "details": {"parameters": parameters}
                }
            )
        
        return UrineAnionGapResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Urine Anion Gap calculation",
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