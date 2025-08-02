"""
Quick Inventory of Depressive Symptomatology (QIDS-SR-16) Router

Endpoint for calculating QIDS-SR-16 depression severity score.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.psychiatry.qids_sr16 import (
    QidsSr16Request,
    QidsSr16Response
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/qids_sr16",
    response_model=QidsSr16Response,
    summary="Calculate QIDS-SR-16 Depression Score",
    description="Calculates the Quick Inventory of Depressive Symptomatology (QIDS-SR-16) score for depression severity assessment. "
                "This validated 16-item self-report instrument evaluates depressive symptoms over the past 7 days across all nine "
                "DSM-IV depression criterion symptom domains. The score ranges from 0-27 points with established severity thresholds: "
                "No Depression (0-5), Mild (6-10), Moderate (11-15), Severe (16-20), and Very Severe (21-27). "
                "Essential for screening, treatment monitoring, and research applications in mental health settings. "
                "Features special scoring rules for sleep, appetite/weight, and psychomotor domains to prevent symptom over-weighting.",
    response_description="The calculated QIDS-SR-16 score with depression severity classification, clinical interpretation, and treatment recommendations",
    operation_id="qids_sr16"
)
async def calculate_qids_sr16(request: QidsSr16Request):
    """
    Calculates Quick Inventory of Depressive Symptomatology (QIDS-SR-16) Score
    
    The QIDS-SR-16 is a validated self-report instrument that comprehensively assesses 
    depressive symptom severity over the past 7 days using 16 items covering all nine 
    DSM-IV depression criterion symptom domains. This efficient yet comprehensive tool 
    provides reliable assessment for screening, treatment monitoring, and research 
    applications in mental health care.
    
    Clinical Applications:
    - Depression screening in primary care and specialty settings
    - Treatment response monitoring and outcome measurement
    - Clinical trial endpoints and research applications
    - Treatment planning and adjustment guidance
    - Quality improvement initiatives in mental health care
    
    Special Scoring Features:
    - Sleep domain: Highest score among 4 sleep items prevents over-weighting
    - Appetite/weight domain: Highest score among 4 appetite/weight items
    - Psychomotor domain: Highest score between agitation and retardation
    - Total possible score: 0-27 points with evidence-based severity thresholds
    
    Safety Considerations:
    - Suicidal ideation scores ≥2 require immediate safety evaluation
    - Comprehensive risk assessment protocols for high-risk patients
    - Integration with clinical interview and safety planning
    
    Args:
        request: QIDS-SR-16 assessment parameters covering all 16 symptom domains
        
    Returns:
        QidsSr16Response: Score with severity classification and clinical recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("qids_sr16", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating QIDS-SR-16 depression score",
                    "details": {"parameters": parameters}
                }
            )
        
        return QidsSr16Response(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for QIDS-SR-16 assessment",
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
                "message": "Internal error in QIDS-SR-16 calculation",
                "details": {"error": str(e)}
            }
        )