"""
CRB-65 Score for Pneumonia Severity Router

Endpoint for calculating CRB-65 score for pneumonia severity assessment.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.pulmonology.crb_65_pneumonia_severity import (
    Crb65PneumoniaSeverityRequest,
    Crb65PneumoniaSeverityResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post("/crb_65_pneumonia_severity", response_model=Crb65PneumoniaSeverityResponse)
async def calculate_crb_65_pneumonia_severity(request: Crb65PneumoniaSeverityRequest):
    """
    Calculates CRB-65 Score for Pneumonia Severity
    
    Stratifies severity of community-acquired pneumonia (CAP) to determine 
    outpatient versus inpatient treatment using 4 clinical criteria. The CRB-65 
    is a simplified version of CURB-65 that does not require blood urea nitrogen 
    measurement, making it particularly useful in primary care settings.
    
    **Clinical Components (1 point each):**
    - **Confusion:** New onset confusion or altered mental status
    - **Respiratory rate:** ≥30 breaths per minute
    - **Blood pressure:** Systolic <90 mmHg OR diastolic ≤60 mmHg  
    - **Age:** ≥65 years
    
    **Risk Stratification:**
    - **Score 0:** Very low risk (<1% mortality) - Home treatment appropriate
    - **Score 1-2:** Intermediate risk (1-10% mortality) - Consider hospital evaluation or observation
    - **Score 3-4:** High risk (>10% mortality) - Hospital admission recommended, consider ICU
    
    **Clinical Advantages:**
    - **No Laboratory Tests:** Unlike CURB-65, does not require blood urea nitrogen measurement
    - **Primary Care Friendly:** Rapid assessment using readily available clinical data
    - **Evidence-Based:** Validated across multiple healthcare systems and countries
    - **Resource Guidance:** Helps optimize hospital bed utilization and treatment intensity
    
    **Clinical Applications:**
    - **Emergency Department:** Triage and disposition decisions for pneumonia patients
    - **Primary Care:** Initial assessment and referral decisions
    - **Quality Improvement:** Standardized severity assessment for pneumonia care protocols
    - **Resource Management:** Guides appropriate level of care and monitoring intensity
    
    **Validation and Performance:**
    The CRB-65 has been extensively validated in multiple international studies 
    and shows good discrimination for mortality prediction. It performs similarly 
    to CURB-65 for risk stratification while being more practical in settings 
    without immediate laboratory access.
    
    **Clinical Considerations:**
    - Should be used in conjunction with clinical judgment and local guidelines
    - Consider patient comorbidities and social circumstances in treatment decisions
    - Not validated for healthcare-associated or hospital-acquired pneumonia
    - Regular reassessment recommended as clinical status may change
    
    **References:**
    - Lim WS, et al. Defining community acquired pneumonia severity. Thorax. 2003;58(5):377-382.
    - Capelastegui A, et al. Validation of a predictive rule for CAP management. Eur Respir J. 2006;27(1):151-157.
    - McNally M, et al. Validity of CRB-65 rule in general practice. Br J Gen Pract. 2010;60(579):e423-433.
    
    Args:
        request: Parameters for 4 clinical criteria assessment
        
    Returns:
        Crb65PneumoniaSeverityResponse: Total score with risk stratification and treatment recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("crb_65_pneumonia_severity", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating CRB-65 Score for Pneumonia Severity",
                    "details": {"parameters": parameters}
                }
            )
        
        return Crb65PneumoniaSeverityResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for CRB-65 Score for Pneumonia Severity",
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