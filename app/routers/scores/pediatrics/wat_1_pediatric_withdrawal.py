"""
Withdrawal Assessment Tool (WAT-1) for Pediatric Withdrawal Router

Endpoint for calculating pediatric withdrawal severity using the validated WAT-1 assessment tool.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.pediatrics.wat_1_pediatric_withdrawal import (
    Wat1PediatricWithdrawalRequest,
    Wat1PediatricWithdrawalResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/wat_1_pediatric_withdrawal",
    response_model=Wat1PediatricWithdrawalResponse,
    summary="Calculate Withdrawal Assessment Tool (WAT-1) for Pediatric Withdrawal",
    description="Calculates the validated WAT-1 score for assessing opioid and benzodiazepine withdrawal "
                "severity in pediatric patients. This 12-parameter assessment tool systematically evaluates "
                "withdrawal symptoms across neurologic, autonomic, and behavioral domains to guide clinical "
                "management decisions. The tool helps standardize withdrawal assessment, determine "
                "pharmacological intervention needs, and establish appropriate monitoring frequency in "
                "critically ill children undergoing sedation weaning. Scores range from 0-33 points, "
                "with scores ≥3 typically warranting pharmacological intervention. The assessment considers "
                "age-specific developmental factors and provides comprehensive clinical recommendations "
                "including medication considerations, monitoring guidelines, comfort measures, and family education.",
    response_description="The calculated WAT-1 score with comprehensive clinical assessment, intervention recommendations, and age-appropriate management guidance",
    operation_id="wat_1_pediatric_withdrawal"
)
async def calculate_wat_1_pediatric_withdrawal(request: Wat1PediatricWithdrawalRequest):
    """
    Calculates Withdrawal Assessment Tool (WAT-1) for Pediatric Withdrawal
    
    The WAT-1 is a validated clinical assessment tool designed to systematically evaluate 
    withdrawal severity in pediatric patients following prolonged opioid or benzodiazepine 
    administration. This evidence-based tool provides standardized assessment methodology 
    for critically ill children undergoing sedation weaning.
    
    Clinical Applications:
    - Standardizes withdrawal assessment across healthcare providers
    - Guides pharmacological intervention decision-making
    - Determines appropriate monitoring frequency and intensity
    - Facilitates communication between healthcare team members
    - Supports evidence-based weaning protocols
    - Helps optimize patient comfort during withdrawal process
    
    Assessment Domains (12 Parameters, 0-3 points each):
    
    Neurologic/Behavioral:
    - State/sleep-wake cycle disturbances
    - Tremor severity and frequency
    - Increased muscle tone and rigidity
    - Myoclonus and seizure activity
    
    Autonomic Symptoms:
    - Tachypnea and respiratory distress
    - Sweating and diaphoresis
    - Fever and hyperthermia
    - Frequent yawning and sneezing
    
    Physical Signs:
    - Excoriation marks from scratching
    - Nasal stuffiness and rhinorrhea
    - Poor feeding and vomiting
    
    Score Interpretation and Management:
    
    0-2 points (No Significant Withdrawal):
    - Continue current supportive care
    - Monitor for symptom progression
    - Reassess every 8-12 hours
    - Implement comfort measures and environmental modifications
    
    3-8 points (Mild to Moderate Withdrawal):
    - Consider pharmacological intervention
    - Initiate or adjust withdrawal medication protocol
    - Increase monitoring frequency (every 4-6 hours)
    - Enhance comfort measures and supportive care
    - Medications: methadone, morphine, or clonidine as appropriate
    
    ≥9 points (Moderate to Severe Withdrawal):
    - Immediate pharmacological intervention required
    - Urgent physician notification and possible specialist consultation
    - Intensive monitoring (every 1-2 hours)
    - Consider ICU-level monitoring for severe symptoms
    - Comprehensive withdrawal protocol implementation
    
    Age-Specific Considerations:
    - Preterm infants: Consider developmental immaturity and different manifestations
    - Term infants: Standard assessment applicable with age-appropriate expectations
    - Young children: Account for motor development and behavioral expectations
    - Older children: Consider communication abilities and developmental milestones
    
    Important Clinical Notes:
    - Validated for term infants through 18 years of age
    - Requires trained healthcare providers for reliable administration
    - Should be used in conjunction with clinical judgment
    - Not validated for alcohol or other substance withdrawal
    - Environmental factors may affect assessment accuracy
    - Consider pain versus withdrawal as differential diagnosis
    
    Args:
        request: Clinical parameters including post-menstrual age and 12 withdrawal assessment scores
        
    Returns:
        Wat1PediatricWithdrawalResponse: WAT-1 score with comprehensive clinical assessment and management recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("wat_1_pediatric_withdrawal", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Withdrawal Assessment Tool (WAT-1) for Pediatric Withdrawal",
                    "details": {"parameters": parameters}
                }
            )
        
        return Wat1PediatricWithdrawalResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for WAT-1 pediatric withdrawal assessment",
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
                "message": "Internal error in WAT-1 calculation",
                "details": {"error": str(e)}
            }
        )