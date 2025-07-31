"""
Cerebral Perfusion Pressure Router

Endpoint for calculating Cerebral Perfusion Pressure for neurocritical care assessment.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.neurology.cerebral_perfusion_pressure import (
    CerebralPerfusionPressureRequest,
    CerebralPerfusionPressureResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/cerebral_perfusion_pressure",
    response_model=CerebralPerfusionPressureResponse,
    summary="Calculate Cerebral Perfusion Pressure",
    description="Calculates cerebral perfusion pressure (CPP), the net pressure gradient that drives oxygen delivery to cerebral tissue. Critical parameter in neurocritical care for monitoring patients with traumatic brain injury, intracranial hypertension, and other neurological conditions.",
    response_description="The calculated cerebral perfusion pressure with interpretation",
    operation_id="calculate_cerebral_perfusion_pressure"
)
async def calculate_cerebral_perfusion_pressure(request: CerebralPerfusionPressureRequest):
    """
    Calculates Cerebral Perfusion Pressure (CPP)
    
    Cerebral Perfusion Pressure is the net pressure gradient that drives oxygen delivery 
    to cerebral tissue. It represents the pressure available to perfuse the brain and is 
    a critical parameter in neurocritical care for monitoring patients with traumatic 
    brain injury, intracranial hypertension, and other neurological conditions.
    
    **Formula**: CPP = MAP - ICP
    
    Where:
    - CPP = Cerebral Perfusion Pressure (mmHg)
    - MAP = Mean Arterial Pressure (mmHg)
    - ICP = Intracranial Pressure (mmHg)
    
    **Clinical Parameters**:
    
    Mean Arterial Pressure (MAP):
    - Driving pressure for cerebral blood flow
    - Normal range: 70-100 mmHg
    - Measured preferably via arterial line at tragus level
    - Can be calculated: MAP = (Systolic BP + 2 × Diastolic BP) ÷ 3
    
    Intracranial Pressure (ICP):
    - Pressure opposing cerebral blood flow
    - Normal range: 5-15 mmHg (adults), 3-7 mmHg (children)
    - Requires invasive monitoring via intraventricular catheter
    - Elevated ICP (>20 mmHg) indicates intracranial hypertension
    
    **CPP Interpretation and Management**:
    
    - **Critical (<30 mmHg)**: Risk of brain death, immediate intervention required
    - **Severely Low (30-50 mmHg)**: High ischemia risk, urgent optimization needed
    - **Low (50-60 mmHg)**: Below optimal, consider interventions
    - **Optimal (60-80 mmHg)**: Target range for most patients, maintain management
    - **Adequate (80-100 mmHg)**: Good perfusion, monitor for complications
    - **High (>100 mmHg)**: Risk of complications, balance perfusion vs. pressure
    
    **Clinical Applications**:
    - **Traumatic Brain Injury**: Primary monitoring parameter in severe TBI
    - **Neurocritical Care**: Stroke, subarachnoid hemorrhage, brain tumor management
    - **Post-surgical Monitoring**: Neurosurgical patients requiring ICP monitoring
    - **Treatment Guidance**: Vasopressor therapy, fluid management, positioning
    - **Secondary Brain Injury Prevention**: Maintain adequate cerebral blood flow
    
    **Evidence-Based Guidelines**:
    - Brain Trauma Foundation guidelines recommend maintaining CPP 60-70 mmHg in TBI
    - Continuous monitoring preferred over isolated measurements
    - Individual optimal CPP may vary based on autoregulation status
    - Balance perfusion needs with systemic complications
    
    **Important Considerations**:
    - Cerebral autoregulation may be impaired in brain injury
    - Age-related normal values may differ (children vs adults)
    - Individual patient factors affect optimal CPP targets
    - Should be interpreted alongside other neurological parameters
    - Measurement accuracy depends on proper transducer positioning
    
    This calculator provides immediate assessment of cerebral perfusion adequacy and 
    evidence-based management recommendations to guide neurocritical care decisions.
    
    Args:
        request: MAP and ICP values needed for CPP calculation
        
    Returns:
        CerebralPerfusionPressureResponse: CPP value with clinical interpretation and management guidance
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("cerebral_perfusion_pressure", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Cerebral Perfusion Pressure",
                    "details": {"parameters": parameters}
                }
            )
        
        return CerebralPerfusionPressureResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Cerebral Perfusion Pressure",
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