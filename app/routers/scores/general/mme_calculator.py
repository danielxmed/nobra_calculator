"""
Morphine Milligram Equivalents (MME) Calculator Router

Endpoint for calculating MME for opioid risk assessment.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.general.mme_calculator import (
    MmeCalculatorRequest,
    MmeCalculatorResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/mme_calculator",
    response_model=MmeCalculatorResponse,
    summary="Calculate Morphine Milligram Equivalents (MME)",
    description="Calculates total daily morphine milligram equivalents to assess opioid overdose risk and guide "
                "safe prescribing practices. Based on CDC 2022 Clinical Practice Guidelines, this calculator converts "
                "multiple opioid medications to standardized morphine equivalents using established conversion factors. "
                "The tool helps identify patients at increased risk for opioid overdose and provides evidence-based "
                "recommendations for monitoring and risk mitigation. MME <50 mg/day indicates low risk with standard "
                "monitoring, 50-89 mg/day suggests moderate risk requiring increased monitoring and naloxone consideration, "
                "while ≥90 mg/day represents high risk necessitating careful benefit-risk evaluation and essential "
                "naloxone co-prescribing. The calculator handles complex scenarios including methadone's dose-dependent "
                "conversion factors, fentanyl patches dosed in mcg/hr, and IV versus oral route differences. It supports "
                "comprehensive opioid therapy management and overdose prevention strategies.",
    response_description="The calculated total daily MME with risk stratification and clinical management recommendations",
    operation_id="mme_calculator"
)
async def calculate_mme_calculator(request: MmeCalculatorRequest):
    """
    Calculates Morphine Milligram Equivalents (MME) for opioid risk assessment
    
    The MME Calculator standardizes opioid dosing across different medications and 
    routes to assess overdose risk using CDC 2022 conversion factors:
    
    Common Opioids and Conversion Factors:
    - Morphine (oral): 1.0, (IV): 3.0
    - Oxycodone: 1.5
    - Hydrocodone: 1.0
    - Codeine: 0.15
    - Fentanyl patch: 2.4 (mcg/hr to mg/day oral morphine)
    - Hydromorphone (oral): 4.0, (IV): 20.0
    - Methadone: 4.0-12.0 (dose-dependent conversion)
    - Tramadol: 0.1
    - Tapentadol: 0.4
    - Buprenorphine (sublingual): 30.0, (patch): 12.6
    
    Risk Categories and Recommendations:
    - <50 MME/day: Low risk - Standard monitoring and safety counseling
    - 50-89 MME/day: Moderate risk - Increased monitoring, consider tapering, naloxone recommended
    - ≥90 MME/day: High risk - Careful benefit-risk evaluation, naloxone essential, frequent monitoring
    
    Clinical Applications:
    - Opioid therapy risk assessment and management
    - Guidance for safe prescribing practices
    - Overdose prevention and naloxone co-prescribing decisions
    - Support for tapering and dose reduction strategies
    - Documentation of rationale for high-dose opioid therapy
    
    Special Considerations:
    - Methadone conversion varies by total daily dose (higher doses = higher conversion factors)
    - Fentanyl and buprenorphine patches are continuous dosing (frequency = 1)
    - IV formulations have higher conversion factors than oral routes
    - Individual patient factors may affect actual equivalency
    - Incomplete cross-tolerance requires caution when rotating opioids
    
    Args:
        request: MME calculation parameters including JSON array of opioid medications with dosing details
        
    Returns:
        MmeCalculatorResponse: Total daily MME with risk stratification and clinical recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("mme_calculator", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating MME",
                    "details": {"parameters": parameters}
                }
            )
        
        return MmeCalculatorResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for MME calculation",
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
                "message": "Internal error in MME calculation",
                "details": {"error": str(e)}
            }
        )