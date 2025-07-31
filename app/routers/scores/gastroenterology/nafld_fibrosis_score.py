"""
NAFLD (Non-Alcoholic Fatty Liver Disease) Fibrosis Score Router

Endpoint for calculating NAFLD Fibrosis Score.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.gastroenterology.nafld_fibrosis_score import (
    NafldFibroseScoreRequest,
    NafldFibroseScoreResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/nafld_fibrosis_score",
    response_model=NafldFibroseScoreResponse,
    summary="Calculate NAFLD",
    description="Estimates amount of scarring in the liver based on various lab tests. Distinguishes between patients with nonalcoholic fatty liver disease who have (F3-F4) and do not have (F0-F2) advanced fibrosis.",
    response_description="The calculated nafld fibrosis score with interpretation",
    operation_id="calculate_nafld_fibrosis_score"
)
async def calculate_nafld_fibrosis_score(request: NafldFibroseScoreRequest):
    """
    Calculates NAFLD (Non-Alcoholic Fatty Liver Disease) Fibrosis Score
    
    The NAFLD Fibrosis Score is a non-invasive scoring system that helps identify 
    NAFLD patients with and without advanced liver fibrosis (F3-F4). It uses 
    routinely available clinical and laboratory data to predict fibrosis severity.
    
    Key features:
    - Uses 6 variables: age, BMI, hyperglycemia, AST/ALT ratio, platelets, albumin
    - AUROC of 0.88 for detecting advanced fibrosis
    - NPV 93% for score < -1.455 (rules out F3-F4)
    - PPV 90% for score > 0.676 (rules in F3-F4)
    - ~30% of patients fall in indeterminate zone requiring additional testing
    
    The score helps reduce unnecessary liver biopsies by accurately identifying:
    - Patients unlikely to have advanced fibrosis (can avoid biopsy)
    - Patients likely to have advanced fibrosis (need close monitoring/treatment)
    
    Args:
        request: Parameters needed for calculation including age, BMI, 
                hyperglycemia status, liver enzymes, platelet count, and albumin
        
    Returns:
        NafldFibroseScoreResponse: Result with score value, fibrosis stage 
                                  classification, and clinical interpretation
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("nafld_fibrosis_score", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating NAFLD Fibrosis Score",
                    "details": {"parameters": parameters}
                }
            )
        
        return NafldFibroseScoreResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for NAFLD Fibrosis Score",
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