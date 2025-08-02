"""
King's College Criteria for Acetaminophen Toxicity Router

Endpoint for assessing liver transplant need in acetaminophen-induced liver failure.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.emergency.kings_college_criteria_acetaminophen import (
    KingsCollegeCriteriaAcetaminophenRequest,
    KingsCollegeCriteriaAcetaminophenResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/kings_college_criteria_acetaminophen",
    response_model=KingsCollegeCriteriaAcetaminophenResponse,
    summary="Calculate King's College Criteria for Acetaminophen Toxicity",
    description="Determines need for liver transplant referral in patients with acute liver failure "
                "secondary to acetaminophen overdose. This validated clinical decision tool identifies "
                "patients with poor prognosis who require urgent liver transplantation consideration. "
                "The criteria use arterial pH, INR, creatinine, and hepatic encephalopathy grade to "
                "stratify risk. Meeting criteria (pH <7.30 OR all of INR >6.5, creatinine >3.4 mg/dL, "
                "and Grade III/IV encephalopathy) indicates 95% specificity for poor outcomes. "
                "Additional prognostic markers include elevated lactate and phosphate levels. "
                "The tool has high specificity but moderate sensitivity (58%), meaning that meeting "
                "criteria strongly indicates need for transplant evaluation, but not meeting criteria "
                "does not guarantee good outcomes. All patients require continued intensive supportive "
                "care and N-acetylcysteine therapy regardless of criteria status.",
    response_description="King's College Criteria assessment with transplant recommendation and detailed clinical management guidance",
    operation_id="kings_college_criteria_acetaminophen"
)
async def calculate_kings_college_criteria_acetaminophen(request: KingsCollegeCriteriaAcetaminophenRequest):
    """
    Calculates King's College Criteria for Acetaminophen Toxicity
    
    The King's College Criteria are the gold standard for determining which patients 
    with acetaminophen-induced acute liver failure require liver transplant evaluation. 
    Developed in 1989, these criteria remain highly relevant for clinical decision-making 
    in the modern era.
    
    Criteria Components:
    1. Primary Criterion: Arterial pH <7.30 (alone meets criteria)
    2. Combined Criteria: ALL three must be present:
       - INR >6.5 (or PT >100 seconds)
       - Serum creatinine >3.4 mg/dL
       - Grade III or IV hepatic encephalopathy
    
    Additional Prognostic Markers:
    - Lactate >3.5 mmol/L (early resuscitation) or >3.0 mmol/L (full resuscitation)
    - Phosphate >3.75 mg/dL at 48-96 hours post-overdose
    
    Clinical Performance:
    - Sensitivity: 58% (moderate - may miss some patients who will deteriorate)
    - Specificity: 95% (high - rarely wrong when criteria are positive)
    - Positive Predictive Value: 70-100% depending on population
    
    Clinical Applications:
    - Liver transplant evaluation and referral decisions
    - Risk stratification in acetaminophen overdose patients
    - Intensive care triage and resource allocation
    - Family counseling and prognosis discussions
    
    Important Considerations:
    - Developed before routine N-acetylcysteine use - outcomes may be better now
    - Serial assessment may be more valuable than single timepoint
    - PT values may vary between laboratories - INR is preferred
    - Consider transplant center consultation even if criteria not met but deteriorating
    - All patients require continued N-acetylcysteine and supportive care
    
    Management Based on Results:
    - Meets Criteria: Urgent liver transplant center referral and evaluation
    - Does Not Meet: Intensive monitoring, continued supportive care, serial reassessment
    
    Contraindications for Assessment:
    - Non-acetaminophen causes of acute liver failure (different criteria apply)
    - Chronic liver disease with acute decompensation
    - Multi-organ failure from other causes
    
    When to Use:
    - Confirmed acetaminophen-induced acute liver failure
    - After adequate resuscitation and N-acetylcysteine initiation
    - When liver transplant evaluation is being considered
    - For prognostic assessment and family discussions
    
    Args:
        request: King's College Criteria parameters
        
    Returns:
        KingsCollegeCriteriaAcetaminophenResponse: Criteria assessment with recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("kings_college_criteria_acetaminophen", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating King's College Criteria",
                    "details": {"parameters": parameters}
                }
            )
        
        return KingsCollegeCriteriaAcetaminophenResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for King's College Criteria",
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