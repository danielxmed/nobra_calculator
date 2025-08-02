"""
Modified Finnegan Neonatal Abstinence Score Router

Endpoint for assessing neonatal opioid withdrawal syndrome severity and guiding treatment decisions.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.pediatrics.modified_finnegan_neonatal_abstinence_score import (
    ModifiedFinneganNeonatalAbstinenceScoreRequest,
    ModifiedFinneganNeonatalAbstinenceScoreResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/modified_finnegan_neonatal_abstinence_score",
    response_model=ModifiedFinneganNeonatalAbstinenceScoreResponse,
    summary="Calculate Modified Finnegan Neonatal Abstinence Score",
    description="""Calculates the Modified Finnegan Neonatal Abstinence Score (NAS) for assessing neonatal opioid withdrawal syndrome severity and guiding pharmacologic treatment decisions.

The Modified Finnegan NAS is the most widely used tool for evaluating neonatal abstinence syndrome, assessing symptoms across central nervous system, metabolic/vasomotor, respiratory, and gastrointestinal domains. This standardized assessment helps healthcare providers:

- Objectively quantify withdrawal severity in opioid-exposed neonates
- Guide decisions about pharmacologic intervention timing
- Monitor treatment response and medication titration
- Standardize care across healthcare teams

**Scoring and Treatment Guidelines:**
- **0-7 points**: No treatment needed - Continue supportive care (swaddling, minimal stimulation, frequent small feeds)
- **8-11 points**: Monitor closely - Consider pharmacologic treatment if 3 consecutive scores ≥8
- **≥12 points**: Initiate treatment - Begin pharmacologic treatment if 2 consecutive scores ≥12

**Assessment Frequency:**
- Every 3-4 hours during hospitalization
- More frequent assessment if scores are elevated or trending upward

**Clinical Context:**
The score evaluates 22 parameters including crying patterns, sleep duration, reflexes, tremors, feeding difficulties, respiratory symptoms, and gastrointestinal disturbances. First-line medications include morphine or methadone, with the goal of stabilizing infants to allow normal feeding, sleeping, and weight gain.""",
    response_description="The calculated Modified Finnegan NAS score with treatment category, clinical interpretation, and evidence-based management recommendations",
    operation_id="modified_finnegan_neonatal_abstinence_score"
)
async def calculate_modified_finnegan_neonatal_abstinence_score(request: ModifiedFinneganNeonatalAbstinenceScoreRequest):
    """
    Calculates Modified Finnegan Neonatal Abstinence Score (NAS)
    
    Assesses neonatal opioid withdrawal syndrome severity across multiple domains
    to guide pharmacologic treatment decisions and optimize supportive care.
    
    Args:
        request: NAS assessment parameters across CNS, metabolic, respiratory, and GI domains
        
    Returns:
        ModifiedFinneganNeonatalAbstinenceScoreResponse: NAS score with treatment recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("modified_finnegan_neonatal_abstinence_score", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Modified Finnegan Neonatal Abstinence Score",
                    "details": {"parameters": parameters}
                }
            )
        
        return ModifiedFinneganNeonatalAbstinenceScoreResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Modified Finnegan Neonatal Abstinence Score",
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