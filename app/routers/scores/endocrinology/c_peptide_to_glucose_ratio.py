"""
C-Peptide to Glucose Ratio Router

Endpoint for calculating C-Peptide to Glucose Ratio.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.endocrinology.c_peptide_to_glucose_ratio import (
    CPeptideToGlucoseRatioRequest,
    CPeptideToGlucoseRatioResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post("/c_peptide_to_glucose_ratio", response_model=CPeptideToGlucoseRatioResponse)
async def calculate_c_peptide_to_glucose_ratio(request: CPeptideToGlucoseRatioRequest):
    """
    Calculates C-Peptide to Glucose Ratio
    
    Assesses beta cell secretory function in patients with diabetes/pre-diabetes by 
    evaluating the relationship between C-peptide secretion and glucose levels.
    
    The C-peptide to glucose ratio (CGR) provides a simple marker of endogenous insulin 
    secretion capacity that can help:
    - Differentiate between Type 1 and Type 2 diabetes
    - Assess residual beta cell function
    - Guide insulin therapy decisions
    - Monitor disease progression
    - Identify patients who may transition from insulin to oral agents
    
    Interpretation:
    - Ratio < 2: Severe insulin secretion deficit - insulin therapy necessary
    - Ratio 2-5: Impaired insulin secretion - may need basal insulin plus other agents
    - Ratio > 5: Preserved insulin secretion - insulin usually unnecessary
    
    Important notes:
    - Best measured postprandially (1-2 hours after meal)
    - Not recommended for patients with chronic kidney disease
    - Should be interpreted in clinical context
    - C-peptide has longer half-life than insulin and is not extracted by liver
    
    Args:
        request: Parameters needed for CGR calculation (C-peptide and glucose levels)
        
    Returns:
        CPeptideToGlucoseRatioResponse: Calculated ratio with clinical interpretation
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("c_peptide_to_glucose_ratio", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating C-Peptide to Glucose Ratio",
                    "details": {"parameters": parameters}
                }
            )
        
        return CPeptideToGlucoseRatioResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for C-Peptide to Glucose Ratio",
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