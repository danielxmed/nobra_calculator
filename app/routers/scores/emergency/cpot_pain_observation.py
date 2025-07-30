"""
Critical Care Pain Observation Tool (CPOT) Router

Endpoint for calculating CPOT pain assessment scores.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.emergency.cpot_pain_observation import (
    CpotPainObservationRequest,
    CpotPainObservationResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post("/cpot_pain_observation", response_model=CpotPainObservationResponse)
async def calculate_cpot_pain_observation(request: CpotPainObservationRequest):
    """
    Calculates Critical Care Pain Observation Tool (CPOT) Score
    
    The CPOT is a validated behavioral pain assessment tool designed for critically 
    ill adults who cannot self-report pain. It evaluates pain using four domains 
    of behavioral indicators, each scored 0-2 points for a total range of 0-8 points.
    
    **Assessment Domains:**
    
    1. **Facial Expression (0-2 points):**
       - 0: Relaxed, neutral - No muscular tension observed
       - 1: Tense - Frowning, brow lowering, orbit tightening
       - 2: Grimacing - All previous movements plus eyelids tightly closed
    
    2. **Body Movements (0-2 points):**
       - 0: Absence of movements - Does not move at all
       - 1: Protection - Slow cautious movements, touching pain site
       - 2: Restlessness - Pulling tube, attempting to sit up, thrashing
    
    3. **Muscle Tension (0-2 points):**
       - 0: Relaxed - No resistance to passive movements
       - 1: Tense, rigid - Resistance to passive movements
       - 2: Very tense or rigid - Strong resistance, unable to complete movements
    
    4. **Patient Status-Specific Domain (0-2 points):**
       
       **For Intubated Patients - Ventilator Compliance:**
       - 0: Tolerating ventilator or movement
       - 1: Coughing but tolerating
       - 2: Fighting ventilator
       
       **For Extubated Patients - Vocalization:**
       - 0: Talking in normal tone or no sound
       - 1: Sighing, moaning
       - 2: Crying out, sobbing
    
    **Score Interpretation:**
    - **≤2 points:** Minimal to no pain (acceptable level)
    - **>2 points:** Unacceptable pain level requiring intervention
    
    **Clinical Applications:**
    - Pain assessment in sedated ICU patients who cannot self-report
    - Post-surgical pain monitoring in critical care settings
    - Evaluation of pain management intervention effectiveness
    - Quality improvement initiatives for ICU pain management protocols
    - Part of the ABCDEF bundle for comprehensive ICU care
    
    **Assessment Guidelines:**
    - **Observation Period:** Observe patient at rest for 60 seconds before scoring
    - **Timing:** Assess before, during, and after procedures for comparison
    - **Context:** Consider patient's baseline behavior and cultural expressions
    - **Documentation:** Record specific behaviors observed for each domain
    - **Reassessment:** Within 30 minutes after pain interventions
    
    **Clinical Integration:**
    - Use in conjunction with physiological indicators when available
    - Consider impact of sedatives on behavioral responses
    - Validate findings with clinical assessment and patient history
    - Integrate with multimodal pain management approaches
    
    **Quality Indicators:**
    - **Sensitivity:** 76.5% for detecting pain in critically ill patients
    - **Specificity:** 70.8% for ruling out pain when absent
    - **Validation:** Extensively validated in conscious and unconscious ICU patients
    - **Reliability:** Intraclass correlation coefficients 0.73-0.99
    
    **Evidence Base:**
    The CPOT has been validated across multiple critical care settings including:
    - Post-cardiac surgery patients
    - Medical and surgical ICU patients
    - Trauma and neurological ICU patients
    - Both conscious and unconscious patient populations
    
    **Clinical Recommendations:**
    
    **For Scores ≤2:**
    - Continue current analgesic regimen
    - Routine pain assessments every 4 hours
    - Maintain current comfort measures
    - Assess for positioning and environmental needs
    
    **For Scores >2:**
    - Consider increasing analgesic dose or alternative medications
    - Frequent reassessments (every 30 minutes after intervention)
    - Non-pharmacological comfort measures (positioning, massage, distraction)
    - Environmental modifications (noise reduction, dimmed lighting)
    - Notify physician if score remains elevated after interventions
    
    **Implementation Considerations:**
    - Staff training on behavioral pain indicators essential
    - Integration with electronic health records for trending
    - Regular inter-rater reliability assessments
    - Consider patient-specific factors affecting expression
    
    **References:**
    - Gélinas C, Fillion L, Puntillo KA, et al. Validation of the critical-care pain observation tool in adult patients. Am J Crit Care. 2006;15(4):420-427.
    - Gélinas C, Harel F, Fillion L, et al. Sensitivity and specificity of the critical-care pain observation tool for the detection of pain in intubated adults after cardiac surgery. J Pain Symptom Manage. 2009;37(1):58-67.
    
    Args:
        request: CPOT assessment parameters including behavioral observations
        
    Returns:
        CpotPainObservationResponse: CPOT score with clinical interpretation and management recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("cpot_pain_observation", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Critical Care Pain Observation Tool (CPOT)",
                    "details": {"parameters": parameters}
                }
            )
        
        return CpotPainObservationResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Critical Care Pain Observation Tool (CPOT)",
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