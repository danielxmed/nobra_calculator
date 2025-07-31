"""
ASA Physical Status Classification System Router

FastAPI router for ASA Physical Status Classification System endpoints.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.anesthesiology.asa_physical_status import (
    AsaPhysicalStatusRequest, 
    AsaPhysicalStatusResponse
)
from app.services.calculator_service import CalculatorService

# Create router with tags for OpenAPI documentation
router = APIRouter(
    prefix="/anesthesiology",
    tags=["Anesthesiology Scores"]
)

# Initialize calculator service
calculator_service = CalculatorService()


@router.post("/asa-physical-status", response_model=AsaPhysicalStatusResponse, summary="Calculate ASA Physical Status", description="Calculates ASA Physical Status Classification System", response_description="ASA classification with risk level assessment and clinical interpretation", operation_id="calculate_asa_physical_status")
async def calculate_asa_physical_status(request: AsaPhysicalStatusRequest):
    """
    Calculate ASA Physical Status Classification
    
    The American Society of Anesthesiologists Physical Status Classification System 
    classifies patients based on their systemic disease and functional limitations 
    to help assess preoperative risk.
    
    **Classification System:**
    - **ASA I**: Normal healthy patient
    - **ASA II**: Patient with mild systemic disease  
    - **ASA III**: Patient with severe systemic disease
    - **ASA IV**: Patient with severe systemic disease that is constant threat to life
    - **ASA V**: Moribund patient not expected to survive without operation
    - **ASA VI**: Brain-dead patient for organ donation
    
    **Emergency Modifier (E):** Added when delay in treatment would significantly 
    increase threat to life or body part.
    
    **Key Points:**
    - Used for over 60 years in perioperative medicine
    - Should be combined with other factors for comprehensive risk assessment
    - Final assignment made by anesthesiologist on day of procedure
    - Subjective system with potential for interrater variability
    
    **Parameters:**
    - **physical_status**: Patient's ASA classification (I-VI)
    - **emergency_surgery**: Whether this is emergency surgery requiring immediate intervention
    
    **Returns:**
    - Final ASA classification with emergency modifier if applicable
    - Risk level assessment
    - Clinical interpretation and recommendations
    """
    try:
        result = calculator_service.calculate_score(
            "asa_physical_status",
            physical_status=request.physical_status,
            emergency_surgery=request.emergency_surgery
        )
        
        return AsaPhysicalStatusResponse(**result)
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Calculation error: {str(e)}")
