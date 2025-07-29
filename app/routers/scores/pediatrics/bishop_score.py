"""
Bishop Score for Vaginal Delivery and Induction of Labor Router

Endpoint for calculating Bishop Score to predict successful vaginal delivery.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.pediatrics.bishop_score import (
    BishopScoreRequest,
    BishopScoreResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post("/bishop_score", response_model=BishopScoreResponse)
async def calculate_bishop_score(request: BishopScoreRequest):
    """
    Calculates Bishop Score for Vaginal Delivery and Induction of Labor
    
    The Bishop Score, developed by Dr. Edward Bishop in 1964, is a standardized 
    pelvic scoring system that has become the gold standard for assessing cervical 
    readiness for labor and predicting the likelihood of successful vaginal delivery. 
    This comprehensive assessment tool is essential in modern obstetric practice for 
    making evidence-based decisions about labor management.
    
    **Historical Significance and Development:**
    
    **Original Purpose:**
    - Developed to predict success of elective labor induction
    - Based on systematic evaluation of 500 elective inductions
    - Replaced subjective clinical assessment with objective scoring
    - Established standardized criteria for cervical favorability
    
    **Clinical Evolution:**
    - Initially used primarily for elective inductions
    - Now applied to spontaneous labor assessment
    - Extended to predict cesarean section risk
    - Incorporated into modern labor management protocols
    
    **Comprehensive Assessment Framework:**
    
    **Five Core Components (0-3 or 0-2 points each):**
    
    **1. Cervical Dilation (0-3 points):**
    - **Assessment Method**: Digital cervical examination with gentle pressure
    - **Closed (0 points)**: External os admits fingertip only
    - **1-2 cm (1 point)**: Os admits one finger easily, minimal opening
    - **3-4 cm (2 points)**: Os admits two fingers, moderate opening
    - **≥5 cm (3 points)**: Significant dilation, often indicates active labor
    
    **2. Cervical Effacement (0-3 points):**
    - **Assessment Method**: Palpation of cervical length and thickness
    - **0-30% (0 points)**: Thick cervix, minimal shortening from normal 3-4 cm
    - **40-50% (1 point)**: Moderate thinning, approximately half normal thickness
    - **60-70% (2 points)**: Significant thinning, marked cervical shortening
    - **≥80% (3 points)**: Nearly complete effacement, minimal cervical length
    
    **3. Fetal Station (0-3 points):**
    - **Assessment Method**: Relationship of presenting part to ischial spines
    - **-3 (0 points)**: Presenting part well above ischial spines, high and mobile
    - **-2 (1 point)**: Presenting part moderately high, some descent noted
    - **-1/0 (2 points)**: Presenting part at or near ischial spine level
    - **+1/+2 (3 points)**: Presenting part descended below spines, engaged
    
    **4. Cervical Position (0-2 points):**
    - **Assessment Method**: Direction of cervix relative to vaginal axis
    - **Posterior (0 points)**: Cervix directed toward sacrum, harder to reach
    - **Mid-position (1 point)**: Cervix in intermediate position
    - **Anterior (2 points)**: Cervix directed forward, easily accessible
    
    **5. Cervical Consistency (0-2 points):**
    - **Assessment Method**: Palpation of cervical firmness
    - **Firm (0 points)**: Cervix feels firm like nasal tip, resistant
    - **Moderately firm (1 point)**: Intermediate consistency, some softening
    - **Soft (2 points)**: Cervix feels soft like lips, easily deformable
    
    **Clinical Score Interpretation and Management:**
    
    **Unfavorable Cervix (0-5 points):**
    
    **Clinical Characteristics:**
    - Closed or minimally dilated cervix
    - Minimal effacement and softening
    - High fetal station with poor engagement
    - Posterior cervical position
    
    **Management Approach:**
    - **Cervical Ripening**: Consider prostaglandins (PGE2, misoprostol)
    - **Mechanical Methods**: Foley catheter, laminaria, or double-balloon catheter
    - **Expectant Management**: Wait for spontaneous cervical change
    - **Patient Counseling**: Discuss increased cesarean delivery risk (15-20%)
    
    **Monitoring Requirements:**
    - Continuous fetal monitoring during cervical ripening
    - Assess cervical change every 6-12 hours
    - Monitor for complications (hypertonicity, fetal distress)
    
    **Indeterminate Range (6-7 points):**
    
    **Clinical Characteristics:**
    - Mixed favorable and unfavorable factors
    - Moderate cervical dilation or effacement
    - Variable fetal station and cervical consistency
    
    **Management Approach:**
    - **Individualized Assessment**: Consider maternal factors, fetal status
    - **Modified Induction**: May proceed with caution and close monitoring
    - **Cervical Ripening**: Consider mild ripening agents if needed
    - **Clinical Judgment**: Factor in obstetric history, indication urgency
    
    **Monitoring Strategy:**
    - Enhanced surveillance during induction
    - Frequent cervical assessment
    - Early intervention for labor dystocia
    
    **Favorable Cervix (8-13 points):**
    
    **Clinical Characteristics:**
    - Good cervical dilation and effacement
    - Engaged or descended fetal station
    - Soft, anterior cervical position
    
    **Management Approach:**
    - **Direct Induction**: Proceed with oxytocin or amniotomy
    - **Expectant Management**: May wait for spontaneous labor
    - **Patient Counseling**: High success rate (>90% vaginal delivery)
    
    **Induction Protocol:**
    - Lower starting doses of oxytocin often effective
    - Amniotomy may be sufficient in some cases
    - Anticipate shorter labor duration
    
    **Modern Clinical Applications:**
    
    **Labor Induction Planning:**
    - **Risk Stratification**: Identify candidates likely to succeed
    - **Method Selection**: Guide choice of induction agent
    - **Resource Allocation**: Plan staffing and bed utilization
    - **Patient Counseling**: Set realistic expectations
    
    **Cesarean Delivery Prediction:**
    - **Low Bishop Score**: 15-20% cesarean rate
    - **High Bishop Score**: 2-5% cesarean rate
    - **Risk Factors**: Nulliparity, advanced maternal age, macrosomia
    
    **Quality Metrics:**
    - **Successful Induction**: Vaginal delivery within 24 hours
    - **Failed Induction**: No cervical change after 12-18 hours
    - **Cesarean for Failed Induction**: Primary indication tracking
    
    **Limitations and Considerations:**
    
    **Inter-observer Variability:**
    - **Training**: Requires standardized examination technique
    - **Experience**: Accuracy improves with clinical experience
    - **Documentation**: Use standardized terminology and measurements
    
    **Patient Factors Not Assessed:**
    - **Maternal**: Age, BMI, obstetric history, medical comorbidities
    - **Fetal**: Estimated weight, presentation, fetal well-being
    - **Pregnancy**: Gestational age, indication for delivery
    
    **Modern Refinements:**
    - **Modified Bishop Score**: Includes additional factors
    - **Simplified Scores**: Reduce components for easier use
    - **Digital Assessment**: Ultrasound-based cervical length measurement
    
    **Evidence-Based Practice Integration:**
    
    **Clinical Guidelines:**
    - **ACOG Recommendations**: Incorporate Bishop Score in induction protocols
    - **Institutional Protocols**: Standardize assessment and documentation
    - **Quality Improvement**: Monitor outcomes based on scores
    
    **Research Applications:**
    - **Clinical Trials**: Stratification variable for induction studies
    - **Outcome Prediction**: Primary endpoint for induction success
    - **Quality Metrics**: Benchmark for institutional performance
    
    **Patient Safety Considerations:**
    
    **Examination Safety:**
    - **Sterile Technique**: Reduce infection risk
    - **Gentle Assessment**: Minimize maternal discomfort
    - **Contraindications**: Avoid if placenta previa or active bleeding
    
    **Clinical Decision Making:**
    - **Multifactorial Assessment**: Consider score with other factors
    - **Shared Decision Making**: Involve patient in delivery planning
    - **Risk-Benefit Analysis**: Balance induction risks and benefits
    
    Args:
        request: Bishop Score assessment parameters (5 cervical/fetal components)
        
    Returns:
        BishopScoreResponse: Bishop score with clinical interpretation and management guidance
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("bishop_score", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Bishop Score",
                    "details": {"parameters": parameters}
                }
            )
        
        return BishopScoreResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Bishop Score calculation",
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