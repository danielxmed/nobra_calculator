"""
EUTOS Score for Chronic Myelogenous Leukemia (CML) Router

Endpoint for calculating EUTOS Score to predict treatment outcomes in newly-diagnosed CML patients.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.hematology.eutos_score import (
    EutosScoreRequest,
    EutosScoreResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/eutos_score",
    response_model=EutosScoreResponse,
    summary="Calculate EUTOS Score for Chronic Myelogenous Leukemia (CML)",
    description="Predicts outcomes after CML treatments, specifically adjusted for tyrosine kinase inhibitor treatments. Predicts probability of complete cytogenetic response at 18 months and progression-free survival.",
    response_description="The calculated eutos score with interpretation",
    operation_id="eutos_score"
)
async def calculate_eutos_score(request: EutosScoreRequest):
    """
    Calculates EUTOS Score for Chronic Myelogenous Leukemia (CML)
    
    The EUTOS Score is a prognostic tool for newly-diagnosed chronic myelogenous leukemia 
    patients that predicts treatment outcomes using two simple clinical parameters:
    
    Key Features:
    - Simple formula: (7 × basophil %) + (4 × spleen size cm)
    - Risk stratification: ≤87 = Low Risk, >87 = High Risk
    - Predicts complete cytogenetic response at 18 months
    - Predicts 5-year progression-free survival
    - Developed for patients treated with imatinib
    
    Clinical Parameters:
    
    Basophil Percentage:
    - Basophils as percentage of peripheral blood leukocytes
    - Obtained from complete blood count with differential
    - Higher percentages associated with worse prognosis
    - Normal range typically 0-2%, elevated in CML
    
    Spleen Size:
    - Maximum distance palpable below left costal margin (cm)
    - Clinical examination finding
    - 0 cm indicates non-palpable spleen (normal)
    - Larger spleen associated with higher tumor burden
    
    Risk Stratification and Outcomes:
    
    Low Risk (Score ≤87):
    - 5-year progression-free survival: 90%
    - Complete cytogenetic response at 18 months: 86%
    - Standard imatinib therapy recommended
    - Routine monitoring protocols
    - Excellent prognosis expected
    
    High Risk (Score >87):
    - 5-year progression-free survival: 82%
    - Complete cytogenetic response at 18 months: 66%
    - Consider more intensive monitoring
    - Earlier treatment response assessment
    - May benefit from alternative strategies
    - Enhanced clinical surveillance
    
    Clinical Applications:
    - Newly-diagnosed CML patients before starting therapy
    - Treatment planning and resource allocation
    - Informed consent and prognostic discussions
    - Risk-stratified monitoring approaches
    - Clinical trial stratification
    
    Model Development and Validation:
    - Derived from 2,060 patients in European LeukemiaNet registry
    - Validated across multiple international cohorts
    - Good discrimination between risk groups
    - Practical for routine clinical use
    - Maintains prognostic value across age groups
    
    Important Limitations:
    - Developed in imatinib-treated patients
    - Outcomes may differ with newer TKIs
    - Spleen assessment is subjective
    - Mixed validation results in some studies
    - Should complement comprehensive assessment
    
    Advantages over Other CML Scores:
    - Simpler than Sokal or Hasford scores
    - Only requires two easily obtained parameters
    - Good discrimination with fewer variables
    - Practical for routine clinical implementation
    - Validated in contemporary patient cohorts
    
    Clinical Decision Support:
    - Treatment selection and planning
    - Monitoring frequency determination
    - Patient and family counseling
    - Resource allocation for care
    - Quality improvement and benchmarking
    
    Model Performance:
    - Positive predictive value for not achieving CCyR: 34%
    - Good separation of risk groups
    - Maintains discrimination across subgroups
    - Practical clinical implementation
    - Contemporary validation in multiple cohorts
    
    Args:
        request: Parameters including basophil percentage and spleen size
        
    Returns:
        EutosScoreResponse: Score, risk level, prognosis, and clinical recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("eutos_score", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating EUTOS Score",
                    "details": {"parameters": parameters}
                }
            )
        
        return EutosScoreResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for EUTOS Score",
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