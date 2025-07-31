"""
Edmonton Symptom Assessment System-revised (ESAS-r) Router

Endpoint for calculating ESAS-r palliative care symptom assessment.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.geriatrics.edmonton_symptom_assessment_system_revised import (
    EdmontonSymptomAssessmentSystemRevisedRequest,
    EdmontonSymptomAssessmentSystemRevisedResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post("/edmonton_symptom_assessment_system_revised", response_model=EdmontonSymptomAssessmentSystemRevisedResponse)
async def calculate_edmonton_symptom_assessment_system_revised(request: EdmontonSymptomAssessmentSystemRevisedRequest):
    """
    Calculates Edmonton Symptom Assessment System-revised (ESAS-r)
    
    The Edmonton Symptom Assessment System-revised (ESAS-r) is a validated 9-item self-report 
    symptom intensity tool designed specifically for palliative care patients. This revised 
    version represents a significant improvement over the original ESAS with enhanced clarity, 
    specific definitions, and better patient understanding.
    
    Clinical Background and Development:
    
    The original Edmonton Symptom Assessment System (ESAS) was developed in 1991 as a simple 
    method for assessing palliative care patients. Over 25 years of clinical use and research 
    led to the development of the revised version (ESAS-r) in 2011, which addressed limitations 
    identified through extensive patient feedback and clinical validation studies.
    
    Key Improvements in ESAS-r:
    - Provides specific definitions for potentially confusing symptoms (tiredness, drowsiness, 
      depression, anxiety, and wellbeing)
    - Specifies clear time frame: "right now" for all assessments
    - Reorganizes symptoms logically: physical symptoms first (1-6), psychosocial symptoms 
      second (7-8), and overall wellbeing last (9)
    - Significantly easier for patients to understand and complete
    - Preferred by patients compared to the original ESAS
    - Better inter-rater reliability and validity
    
    Clinical Assessment Framework:
    
    The ESAS-r assesses nine core symptoms commonly experienced by palliative care patients:
    
    Physical Symptoms (Items 1-6):
    1. Pain: Physical discomfort, suffering, or hurt
    2. Tiredness: Weariness, weakness, or lack of energy (fatigue)
    3. Drowsiness: Feeling sleepy or having difficulty staying awake
    4. Nausea: Feeling sick to stomach or queasy
    5. Lack of Appetite: Not feeling like eating or decreased interest in food
    6. Shortness of Breath: Difficulty breathing or feeling breathless
    
    Psychosocial Symptoms (Items 7-8):
    7. Depression: Feeling sad, blue, or unhappy
    8. Anxiety: Feeling nervous, worried, or fearful
    
    Overall Assessment (Item 9):
    9. Wellbeing: How you feel overall (global quality of life assessment)
    
    Scoring and Interpretation:
    
    Each symptom is rated on an 11-point numeric rating scale (0-10):
    - 0 = No symptom (best possible state)
    - 10 = Worst possible symptom (worst possible state)
    - Total score ranges from 0-90 points (sum of all nine symptoms)
    
    Clinical Significance Thresholds:
    - Individual symptoms ≥4/10: Clinically significant, warrant targeted intervention
    - Individual symptoms ≥7/10: Severe symptoms requiring urgent attention
    - Total score 0-17: Mild symptom burden (manageable with standard care)
    - Total score 18-35: Moderate symptom burden (requires intensified interventions)
    - Total score 36-90: Severe symptom burden (urgent comprehensive review needed)
    
    Clinical Applications and Uses:
    
    Primary Applications:
    - Routine symptom screening in palliative care settings
    - Longitudinal monitoring of symptom progression and treatment response
    - Communication tool between patients, families, and healthcare teams
    - Quality improvement initiatives in palliative care programs
    - Research applications in symptom management and palliative care outcomes
    
    Target Patient Populations:
    - Advanced cancer patients receiving palliative care
    - Patients with life-limiting illnesses (heart failure, COPD, kidney disease)
    - Individuals in hospice care settings
    - Patients in oncology, nephrology, cardiology, and other specialty clinics
    - Any patient receiving symptom-focused or supportive care
    
    Implementation and Administration:
    
    Administration Methods:
    - Self-administered by patients (preferred when possible)
    - Administered with healthcare provider assistance for patients with limitations
    - Can be completed by proxy (family/caregiver) when necessary
    - Electronic or paper-based formats available
    
    Time Requirements:
    - Typically takes 2-5 minutes to complete
    - Can be integrated into routine clinical assessments
    - Suitable for frequent monitoring (daily, weekly, or as clinically indicated)
    
    Clinical Decision-Making and Care Planning:
    
    The ESAS-r results should guide:
    - Treatment intensity and intervention strategies
    - Frequency of symptom monitoring and follow-up
    - Need for specialist palliative care consultation
    - Medication adjustments and symptom management approaches
    - Psychosocial support services and interventions
    - Family education and support needs
    
    Quality Improvement Applications:
    
    Healthcare systems can use ESAS-r for:
    - Benchmarking symptom management effectiveness
    - Identifying areas for improvement in palliative care services
    - Monitoring program outcomes and patient satisfaction
    - Supporting evidence-based practice improvements
    - Staff education and training programs
    
    Research and Validation:
    
    The ESAS-r has been:
    - Psychometrically validated in multiple studies
    - Translated into over 20 languages with cultural validation
    - Used in numerous clinical trials and outcomes research
    - Compared favorably to other symptom assessment tools
    - Endorsed by palliative care professional organizations
    
    Technology Integration:
    
    Modern implementations include:
    - Electronic health record integration
    - Mobile and tablet-based applications
    - Real-time reporting and alerting systems
    - Trend analysis and visualization tools
    - Integration with clinical decision support systems
    
    Training and Education:
    
    Successful implementation requires:
    - Staff training on administration and interpretation
    - Patient and family education on the purpose and importance
    - Development of standardized response protocols
    - Regular competency assessment and updates
    - Integration with institutional palliative care policies
    
    Limitations and Considerations:
    
    Important limitations to consider:
    - Cultural differences in symptom expression and reporting
    - Cognitive limitations may affect completion ability
    - Language barriers may require translated versions
    - Some symptoms may be better assessed through clinical observation
    - Not a diagnostic tool but rather a screening and monitoring instrument
    
    Args:
        request: ESAS-r symptom assessment parameters for all nine symptoms (0-10 scale each)
        
    Returns:
        EdmontonSymptomAssessmentSystemRevisedResponse: Total score with symptom burden category and clinical recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("edmonton_symptom_assessment_system_revised", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Edmonton Symptom Assessment System-revised",
                    "details": {"parameters": parameters}
                }
            )
        
        return EdmontonSymptomAssessmentSystemRevisedResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Edmonton Symptom Assessment System-revised",
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