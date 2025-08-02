"""
Surgical Apgar Score (SAS) Router

Endpoint for calculating Surgical Apgar Score for postoperative risk assessment.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.general.surgical_apgar_score import (
    SurgicalApgarScoreRequest,
    SurgicalApgarScoreResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/surgical_apgar_score",
    response_model=SurgicalApgarScoreResponse,
    summary="Calculate Surgical Apgar Score (SAS)",
    description="Calculates the Surgical Apgar Score (SAS) to predict postoperative risk of major "
                "complications and death in patients undergoing major surgery. This validated 10-point "
                "scoring system, developed by Atul Gawande and colleagues, provides immediate postoperative "
                "risk stratification using three intraoperative parameters: estimated blood loss, lowest "
                "mean arterial pressure, and lowest heart rate measured during surgery. Unlike preoperative "
                "risk assessment tools, the SAS incorporates real-time intraoperative data to provide "
                "dynamic risk assessment reflecting what actually transpired during the surgical procedure. "
                "The score ranges from 0-10 points, with higher scores indicating better outcomes and lower "
                "complication risk. Patients with scores ≤4 have a 58.6% risk of 30-day mortality or major "
                "morbidity requiring immediate ICU admission and intensive monitoring, while those with "
                "scores ≥7 have low risk (3.6% for scores 9-10) suitable for standard postoperative care. "
                "This tool enables evidence-based decisions for ICU admission, monitoring intensity, and "
                "resource allocation while improving perioperative patient safety through objective risk "
                "stratification. The SAS has been validated across multiple surgical specialties and "
                "healthcare systems, demonstrating consistent correlation with postoperative outcomes, "
                "length of stay, and healthcare resource utilization.",
    response_description="Calculated Surgical Apgar Score with comprehensive postoperative risk assessment and clinical management recommendations",
    operation_id="surgical_apgar_score"
)
async def calculate_surgical_apgar_score(request: SurgicalApgarScoreRequest):
    """
    Surgical Apgar Score (SAS) - Intraoperative Risk Assessment Tool
    
    Calculates the Surgical Apgar Score, a validated clinical prediction tool 
    that provides immediate postoperative risk stratification for patients 
    undergoing major surgery. This innovative scoring system represents a 
    paradigm shift in perioperative medicine by incorporating real-time 
    intraoperative data to predict postoperative outcomes.
    
    Revolutionary Approach to Surgical Risk Assessment:
    
    The Surgical Apgar Score addresses a fundamental gap in perioperative 
    medicine by providing objective, standardized assessment of surgical 
    outcomes based on what actually occurs during the procedure, rather than 
    relying solely on preoperative patient characteristics and planned 
    surgical procedures.
    
    Historical Context and Development:
    Inspired by Virginia Apgar's revolutionary scoring system for newborns, 
    which transformed neonatal care through standardized assessment criteria, 
    the SAS was developed to bring similar standardization and objectivity 
    to surgical outcome prediction. Just as the Apgar score provides immediate 
    assessment of neonatal condition to guide care decisions, the SAS offers 
    immediate postoperative risk assessment to optimize patient care.
    
    Clinical Problem and Solution:
    Traditional preoperative risk assessment tools fail to account for 
    intraoperative events that can dramatically influence outcomes. Unexpected 
    bleeding, hemodynamic instability, or technical complications during 
    surgery can fundamentally alter a patient's risk profile regardless of 
    their preoperative status. The SAS captures these dynamic changes through 
    three carefully selected intraoperative parameters.
    
    Scientific Foundation and Parameter Selection:
    
    Estimated Blood Loss (EBL):
    Blood loss during surgery serves as a comprehensive indicator of surgical 
    complexity, technical difficulty, and physiologic stress. Excessive bleeding 
    correlates with increased infection risk, coagulopathy, respiratory 
    complications, cardiovascular stress, and prolonged recovery. The scoring 
    thresholds reflect the clinical significance of increasing blood loss on 
    postoperative outcomes.
    
    Lowest Mean Arterial Pressure (MAP):
    MAP represents the driving pressure for organ perfusion and is a critical 
    determinant of tissue oxygenation and cellular function. Intraoperative 
    hypotension has been consistently associated with acute kidney injury, 
    myocardial ischemia, cerebral hypoperfusion, hepatic dysfunction, and 
    impaired wound healing. The scoring system reflects the clinical importance 
    of maintaining adequate perfusion pressure throughout surgery.
    
    Lowest Heart Rate:
    Heart rate reflects autonomic nervous system function, intravascular volume 
    status, cardiac function, and response to surgical stress. The optimal 
    scoring for moderate heart rates (56-65 bpm) reflects that controlled, 
    stable heart rates often indicate optimal surgical conditions with adequate 
    anesthesia and hemodynamic stability, while extreme values suggest 
    physiologic compromise.
    
    Clinical Implementation and Decision-Making:
    
    Timing and Data Collection:
    The SAS should be calculated at the conclusion of surgery, after skin 
    closure but before transfer to recovery. This timing ensures all 
    intraoperative events are captured while information remains immediately 
    relevant for postoperative care decisions.
    
    Risk Stratification Framework:
    
    Very High Risk (≤4 points):
    These patients require immediate intensive intervention with ICU admission, 
    continuous monitoring, and aggressive supportive care. The 58.6% risk of 
    major complications demands proactive management to prevent adverse outcomes.
    
    High Risk (5-6 points):
    Enhanced surveillance with step-down unit care, frequent monitoring, and 
    low threshold for escalation. These patients benefit from proactive 
    intervention and close observation to prevent deterioration.
    
    Low Risk (≥7 points):
    Standard postoperative care with routine monitoring protocols. The low 
    complication rate (3.6% for scores 9-10) supports normal recovery pathways 
    and discharge planning.
    
    Healthcare System Benefits:
    
    Resource Optimization:
    The SAS enables more efficient allocation of ICU beds, nursing resources, 
    and monitoring equipment based on objective risk assessment rather than 
    subjective clinical judgment alone.
    
    Quality Improvement:
    Systematic use of the SAS provides opportunities for benchmarking surgical 
    and anesthetic performance, identifying process improvement opportunities, 
    and monitoring outcomes across different patient populations and procedures.
    
    Cost-Effectiveness:
    By enabling appropriate level of care placement, the SAS can reduce 
    unnecessary ICU admissions for low-risk patients while ensuring high-risk 
    patients receive appropriate intensive care, optimizing both clinical 
    outcomes and healthcare costs.
    
    Integration with Modern Healthcare:
    
    Electronic Health Record Integration:
    Modern implementations include automated calculation tools, real-time 
    alerts for high-risk scores, integration with postoperative order sets, 
    and trending analysis for quality improvement initiatives.
    
    Interdisciplinary Communication:
    The SAS provides a common language for communication between surgical, 
    anesthetic, nursing, and critical care teams, facilitating coordinated 
    care decisions and appropriate resource allocation.
    
    Validation and Outcomes:
    
    Extensive Validation:
    The SAS has been validated across diverse surgical specialties, patient 
    populations, and healthcare systems, consistently demonstrating correlation 
    with postoperative complications, mortality, length of stay, and resource 
    utilization.
    
    Predictive Accuracy:
    Studies consistently show strong correlation between SAS scores and 
    30-day mortality, major morbidity, ICU admission requirements, readmission 
    rates, and overall healthcare resource consumption.
    
    Continuous Improvement:
    Ongoing research continues to refine the tool, validate its use in 
    specialized populations, and explore integration with other risk assessment 
    tools for enhanced predictive accuracy.
    
    The Surgical Apgar Score represents a significant advancement in 
    perioperative medicine, providing objective, immediate, and actionable 
    risk assessment that enhances clinical decision-making and potentially 
    improves patient outcomes through better risk stratification and 
    resource allocation.
    
    Args:
        request: Surgical Apgar Score parameters including estimated blood loss, lowest MAP, and lowest heart rate
        
    Returns:
        SurgicalApgarScoreResponse: Calculated score with comprehensive postoperative risk assessment and management recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("surgical_apgar_score", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Surgical Apgar Score",
                    "details": {"parameters": parameters}
                }
            )
        
        return SurgicalApgarScoreResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Surgical Apgar Score calculation",
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
                "message": "Internal error in Surgical Apgar Score calculation",
                "details": {"error": str(e)}
            }
        )