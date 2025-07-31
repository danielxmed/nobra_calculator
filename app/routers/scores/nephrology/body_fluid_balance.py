"""
Body Fluid Balance Calculator Router

Endpoint for calculating fluid balance from inputs and outputs.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.nephrology.body_fluid_balance import (
    BodyFluidBalanceRequest,
    BodyFluidBalanceResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/body_fluid_balance",
    response_model=BodyFluidBalanceResponse,
    summary="Calculate Body Fluid Balance Calculator by Inputs and Out...",
    description="Calculates fluid balance from sodium concentrations indicating 0.9% saline fluid, and free water losses (GI, urine, etc) and gains (IV fluids, PO, etc). Helps track complex fluid dynamics in hospitalized patients by accounting for different sodium concentrations in various fluids.",
    response_description="The calculated body fluid balance with interpretation",
    operation_id="calculate_body_fluid_balance"
)
async def calculate_body_fluid_balance(request: BodyFluidBalanceRequest):
    """
    Calculates Body Fluid Balance by Inputs and Outputs
    
    This comprehensive fluid balance calculator provides critical insights into 
    volume status and sodium balance by tracking the sodium content of various 
    body fluids lost and solutions administered. Understanding these differences 
    is essential for appropriate fluid management in hospitalized patients.
    
    **Physiological Principles:**
    
    **Fluid Compartments and Distribution:**
    
    **Total Body Water (TBW):**
    - Approximately 60% of body weight in men, 50% in women
    - Distributed between intracellular (2/3) and extracellular (1/3) compartments
    - Extracellular fluid divided into intravascular (25%) and interstitial (75%)
    - Sodium is the primary determinant of extracellular fluid volume
    
    **Osmotic Equilibrium:**
    - Water moves freely across cell membranes to maintain osmotic equilibrium
    - Serum sodium concentration reflects the ratio of total body sodium to TBW
    - Changes in either sodium or water affect serum sodium concentration
    - Isotonic losses/gains primarily affect volume, not sodium concentration
    
    **Effective Circulating Volume:**
    - The portion of extracellular fluid in the arterial system
    - Sensed by baroreceptors and volume receptors
    - Determines activation of neurohormonal systems (RAAS, ADH, SNS)
    - May be low despite total body fluid overload (e.g., heart failure, cirrhosis)
    
    **Understanding Fluid Tonicity:**
    
    **Isotonic Fluids (Na ~140-154 mEq/L):**
    - Remain in extracellular space
    - Expand or contract intravascular volume
    - Minimal effect on serum sodium
    - Examples: Normal saline (154), Lactated Ringer's (130)
    
    **Hypotonic Fluids (Na <130 mEq/L):**
    - Distribute throughout total body water
    - Less effective for volume expansion
    - Risk of hyponatremia with excess administration
    - Examples: D5W (0), 0.45% NS (77), gastric fluid (60)
    
    **Free Water Clearance:**
    - The volume of water cleared from plasma that is free of solute
    - Positive clearance → dilute urine → water loss → hypernatremia risk
    - Negative clearance → concentrated urine → water retention → hyponatremia risk
    - Affected by ADH, osmotic diuresis, loop diuretics
    
    **Clinical Fluid Loss Patterns:**
    
    **Upper GI Losses (Gastric):**
    - **Composition**: HCl, pepsin, intrinsic factor, water
    - **Electrolytes**: Na 60, K 10, Cl 130 mEq/L
    - **Clinical Impact**: Hypochloremic metabolic alkalosis
    - **Volume Replacement**: Consider higher chloride content fluids
    - **Common Causes**: NG suction, vomiting, gastric outlet obstruction
    
    **Biliary and Pancreatic Losses:**
    - **Composition**: Bicarbonate-rich, near isotonic
    - **Electrolytes**: Na 130-140, K 5, HCO3 30-40 mEq/L
    - **Clinical Impact**: Metabolic acidosis with large losses
    - **Volume Replacement**: Lactated Ringer's or bicarbonate-containing fluids
    - **Common Causes**: Biliary drains, pancreatic fistulas
    
    **Small Intestinal Losses:**
    - **Composition**: Variable along intestinal length
    - **Electrolytes**: Na 110, K 5-10, Cl 100, HCO3 20-30 mEq/L
    - **Clinical Impact**: Volume depletion, electrolyte imbalances
    - **Volume Replacement**: Isotonic crystalloids with K+ supplementation
    - **Common Causes**: Enterostomies, enterocutaneous fistulas
    
    **Colonic Losses (Diarrhea):**
    - **Composition**: Hypotonic, potassium and bicarbonate rich
    - **Electrolytes**: Na 60, K 30, Cl 40, HCO3 30 mEq/L
    - **Clinical Impact**: Hypokalemia, metabolic acidosis
    - **Volume Replacement**: Consider bicarbonate and potassium needs
    - **Common Causes**: Infectious, inflammatory, secretory diarrhea
    
    **Renal Losses:**
    - **Highly Variable Composition**: Na 10-200 mEq/L
    - **Factors Affecting**: Volume status, diuretics, renal function
    - **Concentrated Urine**: High ADH, volume depletion (Na <20 mEq/L)
    - **Dilute Urine**: Low ADH, volume expansion, diuretics (Na >40 mEq/L)
    - **Clinical Utility**: Measure urine Na for accurate calculations
    
    **Insensible Losses:**
    - **Pure Water Loss**: No electrolyte content
    - **Sources**: Skin (75%), respiratory tract (25%)
    - **Normal Rate**: 500-1000 mL/day
    - **Increased By**: Fever (+13% per °C), tachypnea, burns, ambient temperature
    - **Clinical Impact**: Hypernatremia with inadequate replacement
    
    **Intravenous Fluid Selection:**
    
    **0.9% Normal Saline:**
    - **Composition**: Na 154, Cl 154 mEq/L
    - **Tonicity**: Slightly hypertonic to plasma
    - **Distribution**: Remains extracellular (25% intravascular)
    - **Advantages**: Rapid volume expansion, no free water
    - **Disadvantages**: Hyperchloremic acidosis risk, no other electrolytes
    - **Indications**: Hypovolemia, hypotension, hyponatremia
    
    **Lactated Ringer's Solution:**
    - **Composition**: Na 130, Cl 109, K 4, Ca 3, Lactate 28 mEq/L
    - **Tonicity**: Isotonic with plasma
    - **Distribution**: Remains extracellular
    - **Advantages**: More physiologic, lactate → bicarbonate
    - **Disadvantages**: Contains calcium (drug interactions)
    - **Indications**: Surgical patients, burns, less acidosis risk
    
    **0.45% Half Normal Saline:**
    - **Composition**: Na 77, Cl 77 mEq/L
    - **Tonicity**: Hypotonic (50% free water)
    - **Distribution**: Throughout total body water
    - **Advantages**: Provides free water and sodium
    - **Disadvantages**: Risk of hyponatremia, less volume expansion
    - **Indications**: Hypernatremia, maintenance fluids
    
    **D5W (5% Dextrose in Water):**
    - **Composition**: No electrolytes, 50 g/L dextrose
    - **Tonicity**: Isotonic in bag, hypotonic after dextrose metabolism
    - **Distribution**: Throughout total body water
    - **Advantages**: Free water replacement
    - **Disadvantages**: No volume expansion, hyperglycemia risk
    - **Indications**: Free water deficit, drug dilution
    
    **Clinical Decision Framework:**
    
    **Step 1: Assess Volume Status**
    - Physical exam: vital signs, JVP, edema, skin turgor
    - Laboratory: BUN/Cr ratio, urine sodium, hematocrit
    - Hemodynamics: CVP, PCWP if available
    - Imaging: IVC collapsibility, lung ultrasound
    
    **Step 2: Determine Tonicity Needs**
    - Check serum sodium and calculate tonicity
    - Assess free water deficit or excess
    - Consider ongoing losses and their composition
    - Plan replacement to correct both volume and tonicity
    
    **Step 3: Calculate Replacement**
    - Use this calculator to track net balances
    - Replace ongoing losses with similar tonicity fluids
    - Correct deficits slowly (Na change <10-12 mEq/L/day)
    - Monitor response and adjust plan
    
    **Special Clinical Scenarios:**
    
    **Heart Failure:**
    - Total body sodium and water excess
    - Low effective circulating volume
    - Goal: Net negative fluid balance via diuresis
    - Monitor for hemoconcentration indicating effective decongestion
    - Fluid restriction often necessary
    
    **Cirrhosis:**
    - Total body sodium excess with hyponatremia
    - Splanchnic vasodilation reduces effective volume
    - Careful diuresis to avoid hepatorenal syndrome
    - Albumin may help maintain intravascular volume
    - Avoid rapid sodium correction
    
    **Burns:**
    - Massive fluid shifts and evaporative losses
    - Increased insensible losses proportional to BSA burned
    - Initial crystalloid resuscitation (Parkland formula)
    - Transition to colloid after 24 hours
    - Monitor for fluid creep (over-resuscitation)
    
    **Diabetic Ketoacidosis:**
    - Total body water and sodium depletion
    - Initial normal saline for volume resuscitation
    - Switch to 0.45% NS when hemodynamically stable
    - Add dextrose when glucose <250 mg/dL
    - Replace potassium aggressively
    
    **Quality Metrics:**
    
    **Accurate Assessment:**
    - Document all intake and output sources
    - Measure electrolytes in high-volume losses
    - Consider insensible losses in calculations
    - Verify IV pump volumes match orders
    
    **Clinical Correlation:**
    - Daily weights (1 kg = 1 L fluid)
    - Vital sign trends
    - Laboratory monitoring (electrolytes, renal function)
    - Physical examination changes
    
    Args:
        request: Fluid balance parameters including losses and gains
        
    Returns:
        BodyFluidBalanceResponse: Net fluid balance with clinical interpretation
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("body_fluid_balance", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Body Fluid Balance",
                    "details": {"parameters": parameters}
                }
            )
        
        return BodyFluidBalanceResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Body Fluid Balance calculation",
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