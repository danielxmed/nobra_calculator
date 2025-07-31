"""
Edinburgh Postnatal Depression Scale (EPDS) Router

Endpoint for calculating EPDS postpartum depression screening.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.psychiatry.edinburgh_postnatal_depression_scale import (
    EdinburghPostnatalDepressionScaleRequest,
    EdinburghPostnatalDepressionScaleResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/edinburgh_postnatal_depression_scale",
    response_model=EdinburghPostnatalDepressionScaleResponse,
    summary="Calculate Edinburgh Postnatal Depression Scale (EPDS)",
    description="Screens for depression in the postnatal period through a validated 10-item self-report questionnaire. The most widely used postpartum depression screening tool worldwide, also valid for antenatal screening.",
    response_description="The calculated edinburgh postnatal depression scale with interpretation",
    operation_id="calculate_edinburgh_postnatal_depression_scale"
)
async def calculate_edinburgh_postnatal_depression_scale(request: EdinburghPostnatalDepressionScaleRequest):
    """
    Calculates Edinburgh Postnatal Depression Scale (EPDS)
    
    The EPDS is the most widely used postpartum depression screening tool worldwide. 
    It is a 10-item self-report questionnaire that asks women to report how they have 
    felt in the past week. The scale is validated for use in both antenatal (pregnancy) 
    and postnatal (postpartum) periods.
    
    Key Clinical Features:
    - 10-item self-report questionnaire (5-10 minutes to complete)
    - Validated for pregnancy and up to 1 year postpartum
    - Available in over 25 languages with cultural validation
    - Total score ranges from 0-30 points
    - Not diagnostic but screens for those needing further assessment
    
    Scoring System:
    - Items 1, 2, and 4 are REVERSE SCORED (0=3, 1=2, 2=1, 3=0)
    - Items 3, 5-10 are scored as marked (0=0, 1=1, 2=2, 3=3)
    - Higher total scores indicate greater likelihood of depression
    
    Clinical Cut-off Scores (2020 meta-analysis):
    - ≥10 points: Good sensitivity (85%), moderate specificity (84%)
    - ≥11 points: Optimal balance - sensitivity (81%), specificity (88%)
    - ≥13 points: Lower sensitivity (66%), high specificity (95%)
    
    Risk Categories and Actions:
    - Low Risk (0-9): Minimal symptoms, routine care and monitoring
    - Moderate Risk (10-12): Possible depression, clinical assessment within 2 weeks
    - High Risk (≥13): Likely depression, refer for comprehensive evaluation
    
    Critical Safety Assessment:
    - Question 10 (self-harm thoughts): ANY score >0 requires immediate safety evaluation
    - Score 1: Same-day clinical evaluation and safety planning
    - Score 2: Urgent evaluation within 24 hours, comprehensive safety assessment
    - Score 3: IMMEDIATE intervention, consider emergency psychiatric evaluation
    
    Clinical Implementation:
    - Universal screening for all pregnant and postpartum women
    - Screen at least once during pregnancy and once postpartum (6-12 weeks)
    - Rescreening recommended in 2-4 weeks if initial score ≥13
    - Positive screens require clinical assessment, not automatic diagnosis
    
    Epidemiology:
    - Postpartum depression affects ~13% of mothers overall
    - Higher rates in women of color (18-22%)
    - Early identification improves outcomes for mothers and children
    - Untreated depression impacts maternal-infant bonding and child development
    
    Treatment Considerations:
    - Mild-Moderate: Psychotherapy, support groups, lifestyle interventions
    - Moderate-Severe: Antidepressant medication, intensive therapy, psychiatric care
    - Breastfeeding compatible medications available (sertraline, paroxetine preferred)
    - Benefits of treatment typically outweigh risks
    
    Args:
        request: EPDS questionnaire responses for all 10 items (past 7 days)
        
    Returns:
        EdinburghPostnatalDepressionScaleResponse: Score with risk category and clinical recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("edinburgh_postnatal_depression_scale", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Edinburgh Postnatal Depression Scale",
                    "details": {"parameters": parameters}
                }
            )
        
        return EdinburghPostnatalDepressionScaleResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Edinburgh Postnatal Depression Scale",
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