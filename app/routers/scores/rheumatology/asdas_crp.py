"""
Ankylosing Spondylitis Disease Activity Score with CRP (ASDAS-CRP) Router

Endpoint for calculating ASDAS-CRP disease activity assessment.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.rheumatology.asdas_crp import (
    AsdasCrpRequest,
    AsdasCrpResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post("/asdas_crp", response_model=AsdasCrpResponse)
async def calculate_asdas_crp(request: AsdasCrpRequest):
    """
    Calculates Ankylosing Spondylitis Disease Activity Score with CRP (ASDAS-CRP)
    
    The ASDAS-CRP is the gold standard, ASAS-endorsed outcome measure for assessing 
    disease activity in ankylosing spondylitis and axial spondyloarthritis. This 
    composite index combines patient-reported outcomes with an objective inflammatory 
    marker to provide clinically meaningful disease activity stratification.
    
    Formula components and scoring:
    - Back Pain (0-10): Overall spinal pain intensity over the past week
    - Morning Stiffness (0-10): Severity of morning stiffness upon waking
    - Patient Global Assessment (0-10): Overall disease activity perception
    - Peripheral Pain/Swelling (0-10): Extra-spinal joint involvement
    - CRP (mg/L): Objective inflammatory marker
    
    Mathematical calculation:
    ASDAS-CRP = 0.12 × Back Pain + 0.06 × Morning Stiffness + 0.11 × Patient Global + 
                0.07 × Peripheral Pain + 0.58 × Ln(CRP+1)
    
    Disease activity interpretation and management:
    - Inactive Disease (<1.3): Continue therapy, consider tapering if sustained
    - Moderate Activity (1.3-2.1): Optimize treatment, consider biologics
    - High Activity (2.1-3.5): Treatment intensification, biological therapy
    - Very High Activity (>3.5): Urgent intervention, immediate therapy modification
    
    Clinical significance:
    - Clinically Important Improvement: Decrease ≥1.1 units
    - Major Improvement: Decrease ≥2.0 units
    - Superior discriminatory ability compared to traditional measures (BASDAI)
    - Highly responsive to treatment changes in clinical trials
    
    Args:
        request: Clinical parameters including patient-reported outcomes (0-10 scales) 
                and CRP level (mg/L)
        
    Returns:
        AsdasCrpResponse: ASDAS-CRP score with disease activity classification 
        and treatment recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("asdas_crp", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Ankylosing Spondylitis Disease Activity Score with CRP (ASDAS-CRP)",
                    "details": {"parameters": parameters}
                }
            )
        
        return AsdasCrpResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Ankylosing Spondylitis Disease Activity Score with CRP (ASDAS-CRP)",
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