"""
Ckd Epi 2021 router endpoint
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.nephrology import CKDEpi2021Request, CKDEpi2021Response
from app.services.calculator_service import calculator_service

router = APIRouter()

@router.post("/ckd_epi_2021", 
             response_model=CKDEpi2021Response,
             summary="Calculate CKD-EPI 2021 eGFR",
             description="Estimates glomerular filtration rate using the race-free CKD-EPI 2021 equation",
             response_description="eGFR result with CKD staging and clinical recommendations")
async def calculate_ckd_epi_2021(request: CKDEpi2021Request):
    """
    **Calculate CKD-EPI 2021 Estimated Glomerular Filtration Rate**
    
    The CKD-EPI 2021 equation provides a race-free estimation of kidney function, 
    offering more equitable assessment across all populations.
    
    **Clinical Applications:**
    - Chronic kidney disease staging (G1-G5)
    - Medication dosing adjustments
    - Nephrology referral decisions
    - Cardiovascular risk stratification
    - Monitoring kidney function over time
    
    **Key Features:**
    - Race-free equation (2021 update)
    - Age, sex, and creatinine-based calculation
    - KDIGO CKD staging interpretation
    - Specific clinical recommendations per stage
    
    **Input Requirements:**
    - Standardized serum creatinine (IDMS-traceable)
    - Patient age ≥18 years
    - Biological sex (male/female)
    
    **Output Interpretation:**
    - G1 (≥90): Normal/high - investigate for kidney damage
    - G2 (60-89): Mild decrease - investigate for kidney damage
    - G3a (45-59): Mild-moderate decrease - nephrology follow-up
    - G3b (30-44): Moderate-severe decrease - nephrologist referral
    - G4 (15-29): Severe decrease - prepare for replacement therapy
    - G5 (<15): Kidney failure - dialysis/transplant needed
    """
    try:
        # Convert request to dictionary
        parameters = {
            "sex": request.sex.value,  # Enum value
            "age": request.age,
            "serum_creatinine": request.serum_creatinine
        }
        
        # Execute calculation
        result = calculator_service.calculate_score("ckd_epi_2021", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating CKD-EPI 2021",
                    "details": {"parameters": parameters}
                }
            )
        
        return CKDEpi2021Response(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for CKD-EPI 2021",
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