"""
Multiple Myeloma Diagnostic Criteria (IMWG) Router

Endpoint for evaluating multiple myeloma diagnostic criteria according to the
International Myeloma Working Group (IMWG) guidelines.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.hematology.multiple_myeloma_diagnostic_criteria import (
    MultipleMyelomaDiagnosticCriteriaRequest,
    MultipleMyelomaDiagnosticCriteriaResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/multiple_myeloma_diagnostic_criteria",
    response_model=MultipleMyelomaDiagnosticCriteriaResponse,
    summary="Evaluate Multiple Myeloma Diagnostic Criteria (IMWG)",
    description="Evaluates multiple myeloma diagnostic criteria according to the International Myeloma Working Group (IMWG) "
                "updated 2014 guidelines. This diagnostic tool requires both clonal plasma cell evidence (≥10% bone marrow "
                "plasma cells OR biopsy-proven plasmacytoma) AND myeloma defining events including traditional CRAB criteria "
                "(Calcium elevation, Renal dysfunction, Anemia, Bone lesions) or newer SLiM biomarkers (≥60% plasma cells, "
                "Light chain ratio ≥100, MRI >1 focal lesion). The SLiM criteria allow diagnosis before end-organ damage "
                "occurs, enabling earlier treatment intervention for high-risk patients.",
    response_description="Diagnostic assessment with detailed clinical interpretation and management recommendations",
    operation_id="multiple_myeloma_diagnostic_criteria"
)
async def calculate_multiple_myeloma_diagnostic_criteria(request: MultipleMyelomaDiagnosticCriteriaRequest):
    """
    Evaluates Multiple Myeloma Diagnostic Criteria (IMWG)
    
    The International Myeloma Working Group (IMWG) diagnostic criteria distinguish 
    multiple myeloma from other plasma cell disorders including MGUS and smoldering 
    myeloma. The 2014 update introduced SLiM biomarkers alongside traditional CRAB 
    criteria to enable earlier diagnosis.
    
    Args:
        request: Clinical parameters including clonal plasma cell evidence and 
                myeloma defining events (CRAB criteria and SLiM biomarkers)
        
    Returns:
        MultipleMyelomaDiagnosticCriteriaResponse: Diagnostic assessment with clinical recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("multiple_myeloma_diagnostic_criteria", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error evaluating Multiple Myeloma Diagnostic Criteria",
                    "details": {"parameters": parameters}
                }
            )
        
        return MultipleMyelomaDiagnosticCriteriaResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Multiple Myeloma Diagnostic Criteria",
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