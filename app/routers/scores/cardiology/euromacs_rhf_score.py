"""
EUROMACS-RHF Score Router

Endpoint for calculating EUROMACS-RHF Score to predict right heart failure risk after LVAD implantation.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.cardiology.euromacs_rhf_score import (
    EuromacsRhfScoreRequest,
    EuromacsRhfScoreResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/euromacs_rhf_score",
    response_model=EuromacsRhfScoreResponse,
    summary="Calculate EUROMACS-RHF Score",
    description="Determines risk of right ventricular heart failure in patients after left ventricular assist device (LVAD) implantation.",
    response_description="The calculated euromacs rhf score with interpretation",
    operation_id="calculate_euromacs_rhf_score"
)
async def calculate_euromacs_rhf_score(request: EuromacsRhfScoreRequest):
    """
    Calculates EUROMACS-RHF Score for Right Heart Failure Risk After LVAD Implantation
    
    The EUROMACS-RHF Score determines risk of right ventricular heart failure in patients 
    after left ventricular assist device (LVAD) implantation using five validated clinical variables.
    
    Scoring System:
    - RA/PCWP ratio >0.54: 2 points
    - Hemoglobin ≤10 g/dL: 1 point  
    - Multiple IV inotropes: 2.5 points (highest weight)
    - INTERMACS Class 1-3: 2 points
    - Severe RV dysfunction: 2 points
    
    Risk Stratification:
    - Low Risk (0-2 points): 11% RHF incidence
    - Intermediate Risk (2.5-4 points): Intermediate incidence
    - High Risk (4.5-9.5 points): 43.1% RHF incidence
    
    Clinical Definition of RHF:
    Early (<30 days) severe postoperative RHF defined as:
    - Short/long-term right-sided circulatory support, OR
    - Continuous inotropic support ≥14 days, OR  
    - Nitric oxide ventilation ≥48 hours
    
    Key Features:
    - Derived from 2,988 adult patients
    - C-index: 0.70 (derivation), 0.67 (validation)
    - Outperformed existing risk scores
    - Guides surgical planning and perioperative management
    
    Clinical Applications:
    - Preoperative risk assessment for LVAD candidates
    - Surgical planning and device selection (consider BiVAD for high risk)
    - Perioperative monitoring intensity determination
    - Patient and family counseling regarding outcomes
    - Resource allocation and ICU planning
    
    High-Risk Management Considerations:
    - Consider biventricular assist device (BiVAD)
    - Consider total artificial heart
    - Intensive hemodynamic optimization
    - Advanced RV support planning
    - Extended ICU monitoring protocols
    - Multidisciplinary team approach
    
    Outcomes Associated with RHF:
    - Prolonged ICU stay: 24 vs 7 days median
    - Reduced 1-year survival: 53% vs 71%
    - Reduced 2-year survival: 45% vs 58%
    - Increased healthcare resource utilization
    
    Args:
        request: Parameters including RA/PCWP ratio, hemoglobin, inotropes, INTERMACS class, and RV function
        
    Returns:
        EuromacsRhfScoreResponse: Score, risk stratification, and detailed clinical management recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("euromacs_rhf_score", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating EUROMACS-RHF Score",
                    "details": {"parameters": parameters}
                }
            )
        
        return EuromacsRhfScoreResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for EUROMACS-RHF Score",
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