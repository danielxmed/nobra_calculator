"""
Manning Criteria for Diagnosis of Irritable Bowel Syndrome (IBS) Router

Endpoint for calculating Manning Criteria for IBS diagnosis assessment.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.gastroenterology.manning_criteria_ibs import (
    ManningCriteriaIbsRequest,
    ManningCriteriaIbsResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/manning_criteria_ibs",
    response_model=ManningCriteriaIbsResponse,
    summary="Calculate Manning Criteria for IBS Diagnosis",
    description="Calculates the Manning Criteria score for irritable bowel syndrome diagnosis assessment. "
                "This historic clinical prediction tool uses six symptom-based criteria to determine "
                "the likelihood of IBS diagnosis. Developed in 1978 by Manning et al., it requires "
                "at least 3 of 6 criteria for IBS diagnosis suggestion, but red flag symptoms "
                "(age >50, weight loss, blood in stools, anemia, fever) must be absent. While "
                "historically important for IBS diagnosis, Rome IV criteria are now more commonly "
                "used in clinical practice. The tool provides diagnostic guidance with sensitivity "
                "of 63-90% and specificity of 70-93% depending on study population.",
    response_description="The calculated Manning Criteria assessment with diagnostic likelihood, red flag analysis, and comprehensive clinical recommendations",
    operation_id="manning_criteria_ibs"
)
async def calculate_manning_criteria_ibs(request: ManningCriteriaIbsRequest):
    """
    Calculates Manning Criteria for Diagnosis of Irritable Bowel Syndrome (IBS)
    
    The Manning Criteria is a clinical decision tool developed in 1978 to assist in the 
    diagnosis of irritable bowel syndrome. It evaluates six clinical symptoms related to 
    abdominal pain and stool characteristics:
    
    **Six Manning Criteria (1 point each):**
    1. Onset of pain linked to more frequent bowel movements
    2. Looser stools associated with onset of pain  
    3. Pain relieved by passage of stool
    4. Noticeable abdominal bloating/distension
    5. Sensation of incomplete evacuation >25% of time
    6. Diarrhea with mucus >25% of time
    
    **Diagnostic Interpretation:**
    - **<3 criteria:** IBS diagnosis unlikely
    - **≥3 criteria + no red flags:** IBS diagnosis likely
    - **≥3 criteria + red flags present:** Further evaluation required
    
    **Red Flag Exclusions (invalidate diagnosis):**
    - Age >50 years
    - Unexplained weight loss
    - Blood in stools (hematochezia/melena)
    - Anemia on laboratory testing
    - Fever with GI symptoms
    
    **Clinical Performance:**
    - Sensitivity: 63-90%
    - Specificity: 70-93%
    - More specific but less sensitive than Rome criteria
    
    **Clinical Applications:**
    - Primary care IBS screening
    - Gastroenterology consultation support
    - Functional bowel disorder assessment
    - Research and clinical trial enrollment
    
    **Important Limitations:**
    - Requires exclusion of organic GI disease
    - Red flag symptoms mandate further investigation
    - Should complement clinical judgment, not replace it
    - Rome IV criteria provide more current diagnostic standards
    
    **References:**
    1. Manning AP, Thompson WG, Heaton KW, Morris AF. Towards positive diagnosis of the 
       irritable bowel. Br Med J. 1978 Sep 2;2(6138):653-4. doi: 10.1136/bmj.2.6138.653.
    2. Thompson WG, Heaton KW, Smyth GT, Smyth C. Irritable bowel syndrome in general 
       practice: prevalence, characteristics, and referral. Gut. 2000 Jan;46(1):78-82. 
       doi: 10.1136/gut.46.1.78.
    
    Args:
        request: Manning Criteria parameters including six clinical criteria and red flag symptoms
        
    Returns:
        ManningCriteriaIbsResponse: Comprehensive assessment with criteria scores, red flag analysis, 
        diagnostic likelihood, and clinical recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("manning_criteria_ibs", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Manning Criteria for IBS",
                    "details": {"parameters": parameters}
                }
            )
        
        return ManningCriteriaIbsResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Manning Criteria for IBS",
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