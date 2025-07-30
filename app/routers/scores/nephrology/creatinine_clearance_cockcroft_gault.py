"""
Creatinine Clearance (Cockcroft-Gault Equation) Router

Endpoint for calculating creatinine clearance using the Cockcroft-Gault equation.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.nephrology.creatinine_clearance_cockcroft_gault import (
    CreatinineClearanceCockcroftGaultRequest,
    CreatinineClearanceCockcroftGaultResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post("/creatinine_clearance_cockcroft_gault", response_model=CreatinineClearanceCockcroftGaultResponse)
async def calculate_creatinine_clearance_cockcroft_gault(request: CreatinineClearanceCockcroftGaultRequest):
    """
    Calculates Creatinine Clearance using the Cockcroft-Gault Equation
    
    Estimates creatinine clearance for kidney function assessment and medication 
    dosing using patient demographics and serum creatinine. The Cockcroft-Gault 
    equation, developed in 1973, remains clinically relevant for specific 
    medication dosing decisions despite being largely superseded by newer equations.
    
    **Formula:**
    CrCl (mL/min) = [(140 - age) × weight(kg) × (0.85 if female)] / (72 × serum creatinine mg/dL)
    
    **Required Parameters:**
    - **Age:** Patient age in years (18-120)
    - **Weight:** Patient weight in kilograms (30-300 kg)
    - **Sex:** Biological sex (male/female) - females receive 0.85 correction factor
    - **Serum Creatinine:** Level in mg/dL (0.3-15.0)
    
    **Optional Parameter:**
    - **Height:** In centimeters (for BMI calculation and weight recommendations)
    
    **Clinical Interpretation:**
    - **≥90 mL/min:** Normal kidney function - Standard medication dosing
    - **60-89 mL/min:** Mildly decreased - Monitor closely, consider dose adjustments
    - **30-59 mL/min:** Moderately decreased - Dose adjustments required for many medications
    - **15-29 mL/min:** Severely decreased - Significant dose reductions or alternatives needed
    - **<15 mL/min:** Kidney failure - Avoid nephrotoxic drugs, consider dialysis dosing
    
    **Clinical Applications:**
    - **Drug Dosing:** Particularly for medications with narrow therapeutic windows
    - **Regulatory Compliance:** Some regulatory guidance specifically recommends Cockcroft-Gault
    - **Medication Safety:** Assessment of renal elimination capacity for drug clearance
    - **Clinical Research:** Historical standard for pharmacokinetic studies
    
    **Advantages:**
    - **Simplicity:** Requires only basic demographic and laboratory data
    - **Widespread Familiarity:** Well-established in clinical practice
    - **Regulatory Acceptance:** Specifically recommended for certain drug dosing decisions
    - **Historical Validation:** Extensive use in drug development studies
    
    **Limitations and Considerations:**
    - **Accuracy:** Tends to overestimate GFR by 10-20% compared to measured values
    - **Weight Extremes:** Less accurate in underweight or obese patients
    - **Muscle Mass:** Assumes normal muscle mass, may be inaccurate with muscle wasting or excess
    - **Age Bias:** Less accurate in elderly patients due to age-related muscle mass changes
    - **Standardization:** Not adjusted for body surface area unlike newer equations
    
    **Weight Considerations:**
    - **Underweight (BMI <18.5):** Use actual body weight
    - **Normal weight (BMI 18.5-24.9):** Use actual or ideal body weight
    - **Overweight/Obese (BMI ≥25):** Consider adjusted body weight or ideal body weight
    
    **Modern Context:**
    While the 2021 CKD-EPI equation is now preferred for general GFR estimation,
    the Cockcroft-Gault equation remains relevant for:
    - Direct-acting oral anticoagulant (DOAC) dosing
    - Certain antimicrobial dosing decisions
    - Regulatory submissions and drug labeling
    - Clinical scenarios where regulatory guidance specifically recommends its use
    
    **Clinical Integration:**
    Results should be interpreted in conjunction with:
    - Clinical assessment of kidney function
    - Other laboratory markers of kidney function
    - Patient-specific factors affecting creatinine production
    - Medication-specific dosing guidelines
    
    **References:**
    - Cockcroft DW, Gault MH. Prediction of creatinine clearance from serum creatinine. Nephron. 1976;16(1):31-41.
    - Stevens LA, et al. Assessing kidney function--measured and estimated GFR. N Engl J Med. 2006;354(23):2473-2483.
    - Levey AS, et al. GFR estimation: from physiology to public health. Am J Kidney Dis. 2014;63(5):820-834.
    
    Args:
        request: Parameters for creatinine clearance calculation
        
    Returns:
        CreatinineClearanceCockcroftGaultResponse: Estimated creatinine clearance with clinical interpretation
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("creatinine_clearance_cockcroft_gault", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Creatinine Clearance (Cockcroft-Gault Equation)",
                    "details": {"parameters": parameters}
                }
            )
        
        return CreatinineClearanceCockcroftGaultResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Creatinine Clearance (Cockcroft-Gault Equation)",
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