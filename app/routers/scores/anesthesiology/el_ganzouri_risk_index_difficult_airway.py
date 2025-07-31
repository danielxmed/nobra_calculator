"""
El-Ganzouri Risk Index (EGRI) for Difficult Airway Router

Endpoint for calculating EGRI airway difficulty prediction.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.anesthesiology.el_ganzouri_risk_index_difficult_airway import (
    ElGanzouriRiskIndexDifficultAirwayRequest,
    ElGanzouriRiskIndexDifficultAirwayResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post("/el_ganzouri_risk_index_difficult_airway", response_model=ElGanzouriRiskIndexDifficultAirwayResponse)
async def calculate_el_ganzouri_risk_index_difficult_airway(request: ElGanzouriRiskIndexDifficultAirwayRequest):
    """
    Calculates El-Ganzouri Risk Index (EGRI) for Difficult Airway
    
    The El-Ganzouri Risk Index (EGRI), also known as the Simplified Airway Risk Index (SARI), 
    is a validated preoperative assessment tool that predicts the likelihood of difficult airway 
    using seven clinical parameters. It provides objective, evidence-based guidance for anesthesia 
    planning and airway management strategy selection.
    
    Clinical Background and Importance:
    
    Difficult airway management represents one of the most significant challenges in anesthesia 
    practice, with potential for catastrophic outcomes including hypoxic brain injury and death. 
    The EGRI addresses this critical safety concern by providing systematic, reproducible 
    assessment of airway difficulty risk.
    
    The index was developed and validated by El-Ganzouri et al. in 1996 through analysis of 
    10,507 patients undergoing general anesthesia with endotracheal intubation. It has since 
    been validated in numerous international studies and integrated into difficult airway 
    management algorithms worldwide.
    
    Key Clinical Applications:
    
    Preoperative Assessment:
    - Primary screening tool for difficult airway prediction
    - Objective risk stratification beyond subjective clinical impression
    - Guides anesthesia planning and resource allocation
    - Supports informed consent discussions with patients
    - Facilitates interdisciplinary communication about airway risk
    
    Airway Management Strategy Selection:
    - Low risk (0-3 points): Conventional laryngoscopy appropriate
    - High risk (≥4 points): Video laryngoscopy or advanced techniques recommended
    - Very high risk (≥7 points): Consider awake fiberoptic intubation
    - Guides equipment preparation and staffing decisions
    
    Patient Safety Enhancement:
    - 93.8% specificity for predicting difficult airway
    - Reduces unexpected difficult airways through systematic screening
    - Supports standardized difficult airway protocols
    - Enables proactive rather than reactive airway management
    
    Clinical Variables and Scoring:
    
    The EGRI evaluates seven evidence-based predictors of difficult intubation:
    
    1. Mouth Opening (Inter-incisor Distance):
    - Normal: ≥4 cm (0 points)
    - Limited: <4 cm (+1 point)
    Clinical rationale: Adequate mouth opening essential for laryngoscope insertion
    
    2. Thyromental Distance:
    - Adequate: >6.5 cm (0 points)
    - Borderline: 6.0-6.5 cm (+1 point)  
    - Short: <6.0 cm (+2 points)
    Clinical rationale: Reflects laryngeal position; shorter distance indicates anterior larynx
    
    3. Modified Mallampati Classification:
    - Class I: Full pharyngeal visualization (0 points)
    - Class II: Partial pharyngeal visualization (+1 point)
    - Class III: Limited pharyngeal visualization (+2 points)
    - Class IV: Minimal pharyngeal visualization (+2 points)
    Clinical rationale: Assesses tongue size relative to oral cavity
    
    4. Neck Movement (Extension/Flexion Range):
    - Normal: >90° (0 points)
    - Limited: 80-90° (+1 point)
    - Severely limited: <80° (+2 points)
    Clinical rationale: Neck extension critical for optimal laryngoscopic positioning
    
    5. Ability to Prognath (Advance Lower Jaw):
    - Present: Can advance jaw beyond upper teeth (0 points)
    - Absent: Cannot advance jaw (+1 point)
    Clinical rationale: Indicates mandibular mobility and temporomandibular joint function
    
    6. Body Weight Category:
    - Normal: <90 kg (0 points)
    - Elevated: 90-110 kg (+1 point)
    - High: >110 kg (+2 points)
    Clinical rationale: Higher weight associated with increased soft tissue mass
    
    7. History of Difficult Intubation:
    - None: No previous difficulties (0 points)
    - Questionable: Uncertain history (+1 point)
    - Definite: Documented previous difficulty (+2 points)
    Clinical rationale: Previous difficulty strong predictor of future difficulty
    
    Score Interpretation and Management:
    
    Low Risk (0-3 points) - Standard Management:
    - Conventional laryngoscopy with Macintosh blade appropriate
    - Standard difficult airway equipment available
    - Routine backup plans sufficient
    - Primary anesthesiologist can proceed with confidence
    - Standard monitoring and documentation
    
    High Risk (4-6 points) - Enhanced Precautions:
    - Video laryngoscopy recommended as first-line approach
    - Experienced anesthesiologist involvement advised
    - Enhanced difficult airway equipment readily available
    - Multiple backup techniques prepared
    - Consider senior consultation for complex cases
    - Enhanced monitoring and documentation
    
    Very High Risk (≥7 points) - Maximum Precautions:
    - Strong consideration for awake fiberoptic intubation
    - Senior anesthesiologist mandatory involvement
    - Comprehensive difficult airway equipment setup
    - Multiple experienced providers available
    - Alternative anesthetic techniques considered
    - Detailed backup planning and documentation
    
    Validation and Performance Characteristics:
    
    The EGRI has demonstrated consistent performance across diverse populations:
    - Original validation: 10,507 patients with 93.8% specificity
    - Sensitivity: Variable (60-95%) across different populations
    - Positive predictive value: Dependent on institutional difficult airway prevalence
    - Negative predictive value: Generally high (>95%) for excluding difficulty
    - Area under ROC curve: 0.75-0.85 in validation studies
    
    Implementation Best Practices:
    
    Institutional Integration:
    - Incorporate into preoperative assessment protocols
    - Train anesthesia providers on systematic application
    - Integrate with difficult airway management algorithms
    - Establish equipment and staffing response protocols
    - Implement quality assurance monitoring
    
    Clinical Application:
    - Use as part of comprehensive airway assessment
    - Combine with clinical judgment and additional risk factors
    - Document assessment rationale and management decisions
    - Communicate risk level to surgical team and nursing staff
    - Ensure appropriate equipment and personnel availability
    
    Quality Improvement Applications:
    
    Patient Safety Initiatives:
    - Standardize difficult airway screening processes
    - Reduce unexpected difficult airway incidents
    - Improve resource allocation and staffing decisions
    - Support evidence-based practice implementation
    - Enable outcome tracking and continuous improvement
    
    Education and Training:
    - Structured teaching tool for airway assessment
    - Simulation scenario development
    - Competency assessment framework
    - Interdisciplinary communication enhancement
    - Evidence-based decision-making support
    
    Limitations and Considerations:
    
    Clinical Limitations:
    - Predictor performance varies across different populations
    - Some difficult airways may not be captured by conventional predictors
    - Clinical judgment remains essential complement to scoring
    - Regional and demographic variations in validation performance
    - Score designed for general surgical population
    
    Implementation Considerations:
    - Requires consistent provider training and application
    - Equipment and personnel resources must be available
    - Integration with existing protocols and workflows needed
    - Regular validation and outcome monitoring recommended
    - Cultural and institutional adaptation may be necessary
    
    Comparison with Alternative Assessment Tools:
    
    Other validated approaches include:
    - Individual anatomical assessments (Mallampati, thyromental distance)
    - Alternative composite scores (LEMON assessment, STOP-BANG)
    - Advanced imaging techniques (ultrasound, CT assessment)
    - Clinical gestalt and experience-based assessment
    
    The EGRI provides systematic, evidence-based approach with documented validation, 
    making it particularly suitable for standardization and quality improvement initiatives.
    
    Integration with Modern Airway Management:
    
    Contemporary Integration:
    - Complements video laryngoscopy adoption
    - Supports awake intubation decision-making
    - Integrates with supraglottic airway planning
    - Guides emergency surgical airway preparation
    - Supports shared decision-making with patients
    
    Technology Enhancement:
    - Electronic health record integration
    - Clinical decision support system incorporation
    - Mobile application development for point-of-care use
    - Outcome tracking and analytics capabilities
    - Telemedicine consultation support
    
    Patient Communication and Consent:
    
    Risk Communication:
    - Objective risk quantification for patient discussions
    - Standardized language for consent processes
    - Clear explanation of planned management approach
    - Discussion of alternative techniques and risks
    - Documentation of shared decision-making process
    
    Long-term Outcomes and Follow-up:
    
    Clinical Outcomes:
    - Reduced incidence of unexpected difficult airways
    - Improved patient safety metrics
    - Enhanced provider confidence and competence
    - Better resource utilization and efficiency
    - Decreased adverse airway events
    
    Quality Metrics:
    - Difficult airway prediction accuracy
    - First-pass intubation success rates
    - Hypoxic episodes during airway management
    - Equipment utilization and availability
    - Provider satisfaction and confidence levels
    
    Args:
        request: EGRI assessment parameters for seven clinical variables
        
    Returns:
        ElGanzouriRiskIndexDifficultAirwayResponse: Risk score with airway difficulty prediction and management recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("el_ganzouri_risk_index_difficult_airway", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating El-Ganzouri Risk Index for Difficult Airway",
                    "details": {"parameters": parameters}
                }
            )
        
        return ElGanzouriRiskIndexDifficultAirwayResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for El-Ganzouri Risk Index for Difficult Airway",
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