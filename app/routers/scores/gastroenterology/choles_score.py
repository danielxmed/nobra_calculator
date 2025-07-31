"""
CholeS Score for Duration of Laparoscopic Cholecystectomy Router

Endpoint for calculating CholeS Score for operative duration prediction.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.gastroenterology.choles_score import (
    CholesScoredRequest,
    CholesScoredResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/choles_score",
    response_model=CholesScoredResponse,
    summary="Calculate CholeS Score for Duration of Laparoscopic Chole...",
    description="Predicts operative time duration for elective laparoscopic cholecystectomy procedures",
    response_description="The calculated choles score with interpretation",
    operation_id="choles_score"
)
async def calculate_choles_score(request: CholesScoredRequest):
    """
    Calculates CholeS Score for Duration of Laparoscopic Cholecystectomy
    
    The CholeS Score for Duration of Laparoscopic Cholecystectomy is a validated 
    prediction tool designed to estimate operative time for elective laparoscopic 
    cholecystectomy procedures. This evidence-based scoring system enables optimal 
    theatre scheduling, resource allocation, and surgical planning by predicting 
    the likelihood of prolonged operative duration (>90 minutes).
    
    **Development and Validation Background**:
    
    **CholeS Study Foundation**:
    The scoring system is based on the landmark CholeS (Cholecystectomy outcomes 
    and surgical techniques) study, a comprehensive multicentre, prospective 
    population-based cohort study that represents one of the largest surgical 
    outcome studies ever conducted.
    
    **Study Characteristics**:
    - **Population**: 8,820 patients across 166 hospitals in the United Kingdom
    - **Study Period**: March to April 2014 (snapshot study design)
    - **Validation**: 99.2% accuracy through independent data validation
    - **Final Cohort**: 7,227 patients after exclusion criteria applied
    - **Geographic Scope**: Comprehensive UK healthcare system representation
    
    **Statistical Performance**:
    - **Area Under ROC Curve**: 0.708 for predicting >90-minute surgery
    - **Score Range**: 0.5-17.5 points (median score: 5.0)
    - **Risk Stratification**: Three distinct categories with clear thresholds
    - **External Validation**: Confirmed in independent patient cohorts
    
    **CholeS Score Predictive Framework**:
    
    **Ten-Factor Assessment Model**:
    The CholeS Score integrates ten independently predictive factors identified 
    through multivariate analysis of operative duration determinants:
    
    **1. Patient Age (0-1.5 points)**:
    
    **Age <40 Years (0 points)**:
    - Optimal tissue characteristics with clear fascial planes
    - Lower incidence of comorbid conditions affecting surgery
    - Reduced likelihood of previous abdominal procedures
    - Baseline category for age-related operative complexity
    
    **Age ≥40 Years (1.5 points)**:
    - Progressive anatomical changes affecting tissue handling
    - Increased prevalence of comorbid conditions
    - Higher likelihood of adhesions from previous procedures
    - Age-related factors contributing to operative complexity
    
    **2. Patient Gender (0-1 point)**:
    
    **Female Gender (0 points)**:
    - Baseline risk category established in validation studies
    - Standard anatomical considerations for laparoscopic approach
    - Reference category for gender-based risk assessment
    
    **Male Gender (1 point)**:
    - Increased operative complexity demonstrated in validation cohort
    - Anatomical differences affecting laparoscopic visualization
    - Higher conversion rates and longer operative times in study data
    
    **3. Surgical Indication (0-2.5 points)**:
    
    **Pancreatitis (0 points)**:
    - Post-inflammatory state with defined tissue planes
    - Chronic changes often create clear dissection boundaries
    - Lower conversion rates and standard operative complexity
    - Baseline category for indication-based risk
    
    **Colic/Dyskinesia/Polyp (0.5 points)**:
    - Functional gallbladder disorders or benign lesions
    - Intermediate complexity requiring careful evaluation
    - Moderate risk for prolonged operative time
    - May require additional intraoperative assessment
    
    **Common Bile Duct Stone (2 points)**:
    - Complex biliary pathology requiring meticulous dissection
    - Higher risk of complications during Calot's triangle exploration
    - Often necessitates additional procedures or cholangiography
    - Significant increase in operative complexity and duration
    
    **Acalculous/Cholecystitis (2.5 points)**:
    - Acute or chronic inflammatory conditions
    - Unclear tissue planes complicating safe dissection
    - Highest risk category for conversion to open surgery
    - Maximum points reflecting substantial operative challenges
    
    **4. Body Mass Index (0-2 points)**:
    
    **BMI <25 kg/m² (0 points)**:
    - Optimal surgical conditions with excellent visualization
    - Standard instrument reach and manipulation
    - Minimal technical challenges from body habitus
    - Baseline category for weight-related complexity
    
    **BMI 25-35 kg/m² (1 point)**:
    - Moderate increase in technical difficulty
    - Some limitation in visualization and instrument angles
    - Increased operative time due to handling challenges
    - Intermediate risk category requiring standard modifications
    
    **BMI >35 kg/m² (2 points)**:
    - Significant technical challenges affecting all operative phases
    - Substantially reduced visualization and working space
    - Increased conversion risk and operative duration
    - Maximum points reflecting major technical obstacles
    
    **5. Common Bile Duct Diameter (0-2 points)**:
    
    **Normal CBD Diameter (0 points)**:
    - Standard biliary anatomy without obstruction
    - No evidence of downstream biliary pathology
    - Routine dissection approach without additional considerations
    - Baseline category for biliary complexity
    
    **Dilated CBD Diameter (2 points)**:
    - Evidence of biliary obstruction or pathology
    - Requires careful evaluation of biliary anatomy
    - Higher risk of complications during dissection
    - Often necessitates intraoperative cholangiography
    
    **6. Gallbladder Wall Thickness (0-1.5 points)**:
    
    **Normal Wall Thickness (0 points)**:
    - Clear tissue planes facilitating standard dissection
    - Optimal visualization of critical view of safety
    - Standard operative complexity without inflammatory changes
    - Baseline category for anatomical difficulty
    
    **Thick Gallbladder Wall (1.5 points)**:
    - Inflammatory changes obscuring normal anatomy
    - Increased difficulty achieving critical view of safety
    - Higher bleeding risk and longer dissection time
    - Moderate increase in operative complexity
    
    **7. Pre-operative CT Imaging (0-1.5 points)**:
    
    **No CT Performed (0 points)**:
    - Straightforward clinical presentation
    - Standard diagnostic workup sufficient
    - No additional imaging complexity indicated
    - Baseline category for diagnostic complexity
    
    **CT Performed (1.5 points)**:
    - Complex clinical presentation requiring advanced imaging
    - Possible anatomical variants or complications
    - Additional pre-operative planning requirements
    - Moderate increase in case complexity
    
    **8. Planned Intraoperative Cholangiogram (0-3 points)**:
    
    **No Cholangiogram Planned (0 points)**:
    - Standard cholecystectomy without additional procedures
    - Routine operative duration expectations
    - No additional equipment or contrast requirements
    - Baseline operative complexity category
    
    **Cholangiogram Planned (3 points)**:
    - Significant addition to operative duration (typically 15-30 minutes)
    - Additional equipment setup and contrast administration
    - Fluoroscopy requirements and image interpretation
    - Maximum points reflecting substantial time addition
    
    **9. Previous Surgical Admissions (0-2.5 points)**:
    
    **Zero Previous Admissions (0 points)**:
    - Clear peritoneal cavity without adhesions
    - Standard anatomical relationships
    - No previous surgical alterations
    - Baseline category for surgical history complexity
    
    **1-2 Previous Admissions (1 point)**:
    - Limited adhesion formation possible
    - Some anatomical distortion potential
    - Moderate increase in dissection complexity
    - Intermediate surgical history category
    
    **>2 Previous Admissions (2.5 points)**:
    - Extensive adhesion formation likely
    - Significant anatomical distortion possible
    - Substantially increased operative complexity
    - Maximum points for surgical history impact
    
    **10. ASA Physical Status Classification (0-2.5 points)**:
    
    **ASA Grade 1 (0 points)**:
    - Healthy patient without systemic disease
    - No anesthetic or medical complications expected
    - Standard operative approach without modifications
    - Baseline category for patient fitness
    
    **ASA Grade 2 (1 point)**:
    - Mild systemic disease without functional limitation
    - Standard operative approach with minor considerations
    - Minimal impact on operative duration
    - Low-risk patient category
    
    **ASA Grade ≥3 (2.5 points)**:
    - Significant systemic disease with functional limitations
    - May require modified operative approach
    - Potential for longer operative time due to comorbidities
    - Maximum points reflecting substantial patient complexity
    
    **Risk Stratification and Clinical Decision-Making**:
    
    **Low Risk (0-3.5 points): 5.1% chance of >90-minute surgery**:
    
    **Clinical Characteristics**:
    - Younger, healthier patients with straightforward pathology
    - Minimal anatomical complexity or comorbid conditions
    - Standard operative approach with routine expectations
    - Excellent candidate for efficient operative scheduling
    
    **Operative Planning**:
    - **Theatre Scheduling**: 3 cases per half-day operating list
    - **Resource Allocation**: Standard staffing and equipment requirements
    - **Time Allocation**: Standard 60-75 minute slots
    - **Patient Counseling**: Routine operative duration expectations
    
    **Quality Metrics**:
    - High efficiency with predictable completion times
    - Low conversion rates and complication risks
    - Optimal candidates for training case supervision
    - Benchmark cases for operative efficiency assessment
    
    **Intermediate Risk (4-8 points): 5.1-41.8% chance of >90-minute surgery**:
    
    **Clinical Characteristics**:
    - Mixed risk factors requiring individualized assessment
    - Moderate complexity with variable operative challenges
    - Potential for standard or extended operative duration
    - Requires flexible operative planning approach
    
    **Operative Planning**:
    - **Theatre Scheduling**: 2-3 cases per half-day list based on total risk
    - **Resource Allocation**: Consider additional resources for complex cases
    - **Time Allocation**: Extended slots (75-105 minutes) may be appropriate
    - **Patient Counseling**: Possible extended operative time with standard outcomes
    
    **Quality Metrics**:
    - Moderate efficiency requiring case-by-case planning
    - Variable operative duration necessitating flexible scheduling
    - Appropriate for experienced surgeon primary cases
    - Quality improvement focus on efficiency optimization
    
    **High Risk (>8 points): >41.8% chance of >90-minute surgery**:
    
    **Clinical Characteristics**:
    - Multiple risk factors indicating significant technical challenges
    - High likelihood of prolonged or complex surgery
    - Potential for conversion to open approach
    - Requires comprehensive pre-operative planning
    
    **Operative Planning**:
    - **Theatre Scheduling**: Maximum 2 cases per half-day list
    - **Resource Allocation**: Enhanced staffing, senior surgeon involvement
    - **Time Allocation**: Extended slots (105+ minutes) recommended
    - **Patient Counseling**: Extended operative time with increased complexity risk
    
    **Quality Metrics**:
    - Lower efficiency requiring dedicated time and resources
    - Priority for senior surgeon primary or supervisory involvement
    - Enhanced monitoring for conversion and complication rates
    - Focus on safety outcomes rather than efficiency metrics
    
    **Clinical Implementation and Healthcare System Integration**:
    
    **Theatre Management Applications**:
    
    **Scheduling Optimization**:
    - Evidence-based case sequencing to minimize overruns
    - Realistic time allocation based on predicted complexity
    - Improved on-time performance through accurate duration prediction
    - Enhanced patient and staff satisfaction through predictable scheduling
    
    **Resource Planning**:
    - Appropriate staffing levels based on case complexity predictions
    - Equipment and consumable planning for anticipated case difficulty
    - Cost-effective resource allocation across surgical programs
    - Improved overall departmental efficiency and utilization
    
    **Quality Improvement Framework**:
    
    **Performance Benchmarking**:
    - Standardized complexity assessment for inter-surgeon comparisons
    - Risk-adjusted outcome metrics accounting for case difficulty
    - Identification of efficiency improvement opportunities
    - Data-driven surgical protocol development and refinement
    
    **Training and Education**:
    - Structured case selection based on predicted complexity
    - Progressive skill development through graded case difficulty
    - Competency-based assessment using objective complexity measures
    - Enhanced surgical education through predictive case planning
    
    This calculator provides evidence-based operative duration prediction to support 
    clinical decision-making, optimize healthcare resource utilization, and enhance 
    patient care quality in elective laparoscopic cholecystectomy procedures.
    
    Args:
        request: CholeS score parameters for operative duration prediction
        
    Returns:
        CholesScoredResponse: Score with risk stratification and operative planning recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("choles_score", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating CholeS Score",
                    "details": {"parameters": parameters}
                }
            )
        
        return CholesScoredResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for CholeS Score",
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