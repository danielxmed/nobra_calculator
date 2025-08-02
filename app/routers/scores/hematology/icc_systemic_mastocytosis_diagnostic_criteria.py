"""
International Consensus Classification (ICC) Diagnostic Criteria for Systemic Mastocytosis Router

Endpoint for ICC systemic mastocytosis diagnostic criteria evaluation.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.hematology.icc_systemic_mastocytosis_diagnostic_criteria import (
    IccSystemicMastocytosisDiagnosticCriteriaRequest,
    IccSystemicMastocytosisDiagnosticCriteriaResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/icc_systemic_mastocytosis_diagnostic_criteria",
    response_model=IccSystemicMastocytosisDiagnosticCriteriaResponse,
    summary="Calculate ICC Diagnostic Criteria for Systemic Mastocytosis",
    description="Evaluates diagnostic criteria for systemic mastocytosis according to the International Consensus Classification (ICC) published in 2022. This systematic diagnostic framework uses morphological, immunophenotypic, and molecular criteria to diagnose mast cell disorders with enhanced specificity compared to previous WHO criteria. The ICC diagnostic algorithm requires either the major criterion (multifocal dense mast cell infiltrates ≥15 cells in aggregates in bone marrow or extracutaneous organs) OR at least 3 minor criteria (atypical mast cell morphology >25%, aberrant immunophenotype with CD25/CD2/CD30 expression, KIT mutation detection, elevated serum tryptase >20 ng/mL). The diagnosis facilitates appropriate subtype classification into indolent SM, smoldering SM, aggressive SM, mast cell leukemia, or SM with associated myeloid neoplasm, enabling targeted therapeutic approaches. This tool is particularly valuable for hematologists, pathologists, and oncologists in establishing accurate diagnoses and determining optimal management strategies for patients with suspected systemic mastocytosis.",
    response_description="The diagnostic evaluation result with systemic mastocytosis classification and clinical management recommendations",
    operation_id="icc_systemic_mastocytosis_diagnostic_criteria"
)
async def calculate_icc_systemic_mastocytosis_diagnostic_criteria(request: IccSystemicMastocytosisDiagnosticCriteriaRequest):
    """
    Evaluates ICC Diagnostic Criteria for Systemic Mastocytosis
    
    Systematically evaluates morphological, immunophenotypic, and molecular criteria to diagnose 
    systemic mastocytosis according to international consensus standards.
    
    Args:
        request: Morphological, immunophenotypic, and molecular parameters for ICC SM diagnosis (5 criteria)
        
    Returns:
        IccSystemicMastocytosisDiagnosticCriteriaResponse: Diagnostic result with staging and management guidance
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("icc_systemic_mastocytosis_diagnostic_criteria", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error evaluating ICC Systemic Mastocytosis Diagnostic Criteria",
                    "details": {"parameters": parameters}
                }
            )
        
        return IccSystemicMastocytosisDiagnosticCriteriaResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for ICC Systemic Mastocytosis Diagnostic Criteria",
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
                "message": "Internal error in diagnostic evaluation",
                "details": {"error": str(e)}
            }
        )