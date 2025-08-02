"""
Modified Glasgow Prognostic Score (mGPS) for Cancer Outcomes Router

Endpoint for assessing cancer prognosis based on systemic inflammation and nutritional status.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.oncology.modified_glasgow_prognostic_score import (
    ModifiedGlasgowPrognosticScoreRequest,
    ModifiedGlasgowPrognosticScoreResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/modified_glasgow_prognostic_score",
    response_model=ModifiedGlasgowPrognosticScoreResponse,
    summary="Calculate Modified Glasgow Prognostic Score for Cancer",
    description="""Calculates the Modified Glasgow Prognostic Score (mGPS) for cancer outcomes using readily available laboratory markers (CRP and albumin) to assess prognosis across multiple cancer types.

The mGPS improves upon the original Glasgow Prognostic Score by weighting the inflammatory component more heavily, providing better prognostic discrimination. This validated biomarker-based assessment tool helps healthcare providers:

- Stratify cancer patients into prognostic groups independent of tumor site
- Guide treatment planning and patient counseling decisions
- Identify patients who may benefit from supportive interventions
- Provide prognostic information beyond traditional TNM staging

**Laboratory Parameters:**
- **C-Reactive Protein (CRP)**: Reflects systemic inflammatory response
  - Normal: ≤10 mg/L
  - Elevated: >10 mg/L (indicates systemic inflammation)
- **Serum Albumin**: Reflects nutritional status and synthetic function
  - Normal: ≥35 g/L (≥3.5 g/dL)
  - Low: <35 g/L (<3.5 g/dL) (indicates malnutrition or chronic disease)

**Scoring System:**
- **Score 0**: CRP ≤10 mg/L (regardless of albumin) - Good prognosis
- **Score 1**: CRP >10 mg/L and albumin ≥35 g/L - Intermediate prognosis  
- **Score 2**: CRP >10 mg/L and albumin <35 g/L - Poor prognosis

**Key Advantage over Original GPS:**
- Low albumin alone (without elevated CRP) scores 0 points in mGPS vs 1 point in original GPS
- This modification emphasizes the importance of systemic inflammation in cancer prognosis

**Clinical Applications:**
- Validated across multiple cancer types (gastric, renal, lung, pancreatic, colorectal)
- Useful for treatment planning and resource allocation
- Guides supportive care interventions (nutritional support, anti-inflammatory measures)
- Complements traditional staging systems with functional assessment

**Survival Associations:**
- Higher scores associated with worse overall survival, disease-specific survival, and disease-free survival
- Example from gastric cancer: Score 0 (74.6% 5-year survival), Score 1 (61.4%), Score 2 (34.6%)
- Survival outcomes vary significantly by cancer type, stage, and treatment""",
    response_description="The calculated mGPS score with prognostic implications and evidence-based management recommendations",
    operation_id="modified_glasgow_prognostic_score"
)
async def calculate_modified_glasgow_prognostic_score(request: ModifiedGlasgowPrognosticScoreRequest):
    """
    Calculates Modified Glasgow Prognostic Score for Cancer Outcomes
    
    Assesses cancer prognosis using CRP and albumin levels to reflect systemic 
    inflammation and nutritional status, providing prognostic information 
    independent of tumor site.
    
    Args:
        request: CRP and albumin laboratory values
        
    Returns:
        ModifiedGlasgowPrognosticScoreResponse: mGPS score with prognostic assessment and management recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("modified_glasgow_prognostic_score", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Modified Glasgow Prognostic Score",
                    "details": {"parameters": parameters}
                }
            )
        
        return ModifiedGlasgowPrognosticScoreResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Modified Glasgow Prognostic Score",
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