"""
Maintenance Fluids Calculations Router

Endpoint for calculating maintenance fluid requirements using the Holliday-Segar method.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.pediatrics.maintenance_fluids_calculations import (
    MaintenanceFluidsCalculationsRequest,
    MaintenanceFluidsCalculationsResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/maintenance_fluids_calculations",
    response_model=MaintenanceFluidsCalculationsResponse,
    summary="Calculate Maintenance Fluids using Holliday-Segar Method",
    description="Calculates maintenance fluid requirements by weight using the evidence-based Holliday-Segar "
                "method developed in 1957. This gold standard formula provides systematic fluid replacement "
                "calculations for pediatric and adult patients based on metabolic demands. The weight-based "
                "calculation uses three tiers: 0-10 kg (100 mL/kg/day), 10-20 kg (1000 mL + 50 mL/kg for "
                "each kg over 10), and >20 kg (1500 mL + 20 mL/kg for each kg over 20). The calculator "
                "provides both daily volume and hourly rate recommendations along with clinical guidance for "
                "fluid type selection, monitoring parameters, and adjustments for various clinical conditions. "
                "Essential for hospitalized patients requiring IV hydration, post-operative fluid management, "
                "and NPO patients. The results should be adjusted for ongoing losses, clinical conditions, "
                "and fluid balance status while monitoring electrolytes and urine output regularly.",
    response_description="The calculated maintenance fluid requirements with daily volume, hourly rate, and comprehensive clinical recommendations",
    operation_id="maintenance_fluids_calculations"
)
async def calculate_maintenance_fluids_calculations(request: MaintenanceFluidsCalculationsRequest):
    """
    Calculates maintenance fluid requirements using the Holliday-Segar method
    
    The Holliday-Segar method is the gold standard for calculating maintenance fluid requirements
    in both pediatric and adult patients, providing evidence-based fluid management guidance.
    
    Historical Background:
    Developed by Malcolm Holliday and William Segar in 1957, this method revolutionized
    pediatric fluid management by establishing a systematic, weight-based approach to
    maintenance fluid calculation. The formula is based on metabolic water needs and
    has been validated across different age groups and clinical conditions.
    
    Clinical Applications:
    - Maintenance IV fluid calculation for hospitalized patients
    - Post-operative fluid management and recovery
    - NPO (nothing by mouth) patients requiring IV hydration
    - Baseline calculation for adjusting additional fluid needs
    - Emergency department fluid resuscitation planning
    - ICU fluid management protocols
    - Pediatric and adult ward fluid orders
    
    Formula Breakdown:
    Weight Category 1 (0-10 kg): 100 mL/kg/day
    - Based on high metabolic rate in small children
    - Accounts for higher surface area to weight ratio
    - Examples: 5 kg infant = 500 mL/day, 8 kg toddler = 800 mL/day
    
    Weight Category 2 (10-20 kg): 1000 mL + 50 mL/kg for each kg over 10
    - Recognizes decreased metabolic rate per kg as size increases
    - Examples: 12 kg child = 1100 mL/day, 18 kg child = 1400 mL/day
    
    Weight Category 3 (>20 kg): 1500 mL + 20 mL/kg for each kg over 20
    - Further reduced rate for larger patients
    - Examples: 25 kg child = 1600 mL/day, 70 kg adult = 2500 mL/day
    
    Clinical Considerations:
    
    Fluid Type Selection:
    - Isotonic solutions preferred (0.9% NaCl, Lactated Ringer's)
    - Hypotonic solutions may cause hyponatremia
    - Consider electrolyte content based on patient needs
    
    Adjustments Required For:
    - Fever: Increase 10-15% for each degree Celsius >37°C
    - Ongoing losses: Diarrhea, vomiting, drainage, diuresis
    - Clinical conditions: Heart failure, renal disease, liver disease
    - Environmental factors: High ambient temperature, low humidity
    
    Monitoring Parameters:
    - Urine output (goal: 1-2 mL/kg/hr)
    - Serum electrolytes (sodium, potassium, chloride)
    - Fluid balance (inputs vs outputs)
    - Clinical signs of hydration status
    - Daily weights for trend monitoring
    
    Special Populations:
    
    Neonates (<1 month):
    - May require different calculations
    - Higher insensible losses
    - Immature renal function considerations
    - Monitor closely for fluid overload
    
    Elderly Patients:
    - May need fluid restriction
    - Consider comorbidities (heart, kidney, liver disease)
    - Monitor for signs of fluid overload
    
    Critical Care Patients:
    - Formula provides starting point only
    - Adjust based on hemodynamic status
    - Consider capillary leak, third spacing
    - May need goal-directed fluid therapy
    
    Contraindications and Limitations:
    - Does not replace clinical judgment
    - Not suitable for fluid resuscitation
    - May not apply to severe renal/cardiac disease
    - Requires adjustment for ongoing losses
    - Should not be used as sole guide in critical illness
    
    Quality and Safety Measures:
    - Regular reassessment of fluid needs
    - Electrolyte monitoring protocols
    - Documentation of fluid balance
    - Recognition of fluid overload signs
    - Adjustment protocols for changing conditions
    
    Evidence Base:
    The Holliday-Segar method has been validated through decades of clinical use
    and remains the standard of care endorsed by pediatric and internal medicine
    organizations worldwide. Recent studies support the use of isotonic solutions
    to prevent hospital-acquired hyponatremia.
    
    Args:
        request: Weight parameter for maintenance fluid calculation
        
    Returns:
        MaintenanceFluidsCalculationsResponse: Calculated fluid requirements with clinical guidance
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("maintenance_fluids_calculations", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Maintenance Fluids",
                    "details": {"parameters": parameters}
                }
            )
        
        return MaintenanceFluidsCalculationsResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Maintenance Fluids Calculations",
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
                "message": "Internal error in Maintenance Fluids Calculations",
                "details": {"error": str(e)}
            }
        )