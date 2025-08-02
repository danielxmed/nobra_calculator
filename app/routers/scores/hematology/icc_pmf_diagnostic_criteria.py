"""
International Consensus Classification (ICC) Diagnostic Criteria for Primary Myelofibrosis (PMF) Router

Endpoint for ICC PMF diagnostic criteria evaluation.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.hematology.icc_pmf_diagnostic_criteria import (
    IccPmfDiagnosticCriteriaRequest,
    IccPmfDiagnosticCriteriaResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/icc_pmf_diagnostic_criteria",
    response_model=IccPmfDiagnosticCriteriaResponse,
    summary="Calculate ICC Diagnostic Criteria for Primary Myelofibrosis",
    description="Evaluates diagnostic criteria for primary myelofibrosis according to the International Consensus Classification (ICC) published in 2022. This systematic diagnostic framework uses morphological, genetic, and clinical criteria to distinguish between prefibrotic (early) and overt (fibrotic) stages of primary myelofibrosis. The ICC criteria refine the WHO classification system by providing enhanced diagnostic specificity for myeloproliferative neoplasms. The diagnostic algorithm requires all three major criteria (megakaryocytic proliferation and atypia on bone marrow biopsy, presence of JAK2/CALR/MPL mutation or other clonal marker, and exclusion of reactive fibrosis and other myeloproliferative neoplasms) plus at least one minor criterion (anemia not from comorbidity, leukocytosis ≥11×10^9/L, palpable splenomegaly, or elevated LDH). The diagnosis must be confirmed in two consecutive determinations to ensure accuracy. Staging is determined by bone marrow fibrosis grade: prefibrotic PMF (grade 0-1) versus overt PMF (grade 2-3). This tool facilitates accurate diagnosis, appropriate staging, prognostic assessment, and treatment planning for patients with suspected primary myelofibrosis, and is particularly valuable for hematologists and pathologists in differentiating PMF from other myeloproliferative neoplasms.",
    response_description="The diagnostic evaluation result with PMF stage classification and clinical management recommendations",
    operation_id="icc_pmf_diagnostic_criteria"
)
async def calculate_icc_pmf_diagnostic_criteria(request: IccPmfDiagnosticCriteriaRequest):
    """
    Evaluates ICC Diagnostic Criteria for Primary Myelofibrosis
    
    Systematically evaluates morphological, genetic, and clinical criteria to diagnose 
    and stage primary myelofibrosis according to international consensus standards.
    
    Args:
        request: Morphological, genetic, and clinical parameters for ICC PMF diagnosis (9 criteria)
        
    Returns:
        IccPmfDiagnosticCriteriaResponse: Diagnostic result with staging and management guidance
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("icc_pmf_diagnostic_criteria", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error evaluating ICC PMF Diagnostic Criteria",
                    "details": {"parameters": parameters}
                }
            )
        
        return IccPmfDiagnosticCriteriaResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for ICC PMF Diagnostic Criteria",
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