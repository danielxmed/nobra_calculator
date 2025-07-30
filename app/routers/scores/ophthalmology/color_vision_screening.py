"""
Color Vision Screening (Ishihara Test) Router

Endpoint for calculating Color Vision Screening assessment.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.ophthalmology.color_vision_screening import (
    ColorVisionScreeningRequest,
    ColorVisionScreeningResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post("/color_vision_screening", response_model=ColorVisionScreeningResponse)
async def calculate_color_vision_screening(request: ColorVisionScreeningRequest):
    """
    Calculates Color Vision Screening (Ishihara Test) Assessment
    
    The Ishihara color vision test is the most widely used screening tool for detecting 
    red-green color blindness in clinical practice. This standardized assessment uses 
    an abbreviated 14-plate version to provide efficient screening while maintaining 
    clinical accuracy for identifying the most common forms of color vision deficiency.
    
    **Clinical Background and Epidemiology**:
    
    **Prevalence and Genetics**:
    - Red-green color blindness affects approximately 8% of males and 0.5% of females
    - X-linked recessive inheritance pattern explains the gender disparity
    - Most common forms: protanomaly (red-weak) and deuteranomaly (green-weak)
    - Usually congenital condition that remains stable throughout life
    - Rarely affects overall visual acuity or general eye health
    
    **Types of Color Vision Deficiency**:
    
    **Protanomaly (Red-Weak)**:
    - Reduced sensitivity to red light wavelengths
    - Difficulty distinguishing red from green in certain contexts
    - May appear as red colors looking dimmer or more brownish
    - Affects approximately 1% of males
    
    **Deuteranomaly (Green-Weak)**:
    - Reduced sensitivity to green light wavelengths
    - Most common form of color vision deficiency
    - Green colors may appear more reddish or less vibrant
    - Affects approximately 5% of males
    
    **Complete Color Blindness (Rare)**:
    - Protanopia: Complete absence of red cone function
    - Deuteranopia: Complete absence of green cone function
    - Much less common than the partial deficiencies above
    
    **Ishihara Test Methodology**:
    
    **Test Design Principles**:
    - Uses pseudoisochromatic plates with colored dots of varying sizes
    - Numbers or patterns embedded within dot matrices
    - Normal color vision allows clear identification of embedded figures
    - Color deficient vision may see different numbers or no patterns
    - Plates designed to specifically challenge red-green discrimination
    
    **Standardized Administration**:
    
    **Environmental Requirements**:
    - Natural daylight illumination preferred (north-facing window)
    - Bright white LED lighting acceptable if daylight unavailable
    - Avoid fluorescent lighting which may alter color appearance
    - Consistent lighting throughout testing session
    - Test distance of 75cm (30 inches) for physical plates
    
    **Testing Protocol**:
    - Present each plate for maximum 3-4 seconds
    - Test each eye independently, completely covering the other eye
    - Use appropriate refractive correction (glasses/contacts)
    - Allow brief light adaptation period before testing
    - Record exact response without feedback or prompting
    
    **Scoring Methodology**:
    - Plate 1: Demonstration plate (visible to all, not scored)
    - Plates 2-14: Diagnostic plates for red-green discrimination
    - Count only clear, confident responses as correct
    - Hesitant or uncertain responses counted as incorrect
    - More than 2 incorrect plates indicates possible deficiency
    
    **Clinical Interpretation Framework**:
    
    **Normal Color Vision (12-14 correct plates)**:
    - **Clinical Significance**: Intact red-green color discrimination ability
    - **Functional Impact**: No significant limitations in color-dependent activities
    - **Occupational Considerations**: No restrictions for color-critical careers
    - **Follow-up**: Routine eye care as appropriate for age
    - **Patient Counseling**: Reassurance of normal color vision
    
    **Possible Color Vision Deficiency (8-11 correct plates)**:
    - **Clinical Significance**: Mild color discrimination difficulties possible
    - **Functional Impact**: May notice subtle difficulties with certain color combinations
    - **Occupational Considerations**: May affect performance in highly color-critical roles
    - **Follow-up**: Consider repeat testing or ophthalmology consultation
    - **Patient Counseling**: Explain potential mild limitations and adaptive strategies
    
    **Color Vision Deficiency Likely (0-7 correct plates)**:
    - **Clinical Significance**: Significant red-green color vision impairment probable
    - **Functional Impact**: Noticeable difficulties with red-green color discrimination
    - **Occupational Considerations**: Limitations likely in color-critical occupations
    - **Follow-up**: Ophthalmology referral for comprehensive color vision evaluation
    - **Patient Counseling**: Comprehensive education about condition and adaptations
    
    **Age-Specific Considerations**:
    
    **Pediatric Testing (Ages 1-4)**:
    - **Reliability Limitations**: Attention span and comprehension challenges
    - **Modified Approaches**: Picture-based or matching tests may be more appropriate
    - **Interpretation Caution**: Results may not be fully reliable
    - **Recommendation**: Repeat testing at age 5-6 years for confirmation
    
    **School-Age Testing (Ages 5-17)**:
    - **High Reliability**: Standard testing methodology usually successful
    - **Educational Implications**: Early identification allows for accommodations
    - **Career Planning**: Results inform future educational and career decisions
    - **Family Screening**: Consider testing siblings if deficiency identified
    
    **Adult Testing (Ages 18+)**:
    - **Optimal Reliability**: Highest accuracy with standard methodology
    - **Occupational Impact**: Results may affect current or future employment
    - **Stability Expected**: Congenital condition typically stable throughout life
    - **Genetic Counseling**: Consider implications for children if planning family
    
    **Visual Acuity Impact on Test Accuracy**:
    
    **Adequate Visual Acuity (≥20/100)**:
    - **Test Accuracy**: Optimal sensitivity and specificity
    - **Result Reliability**: High confidence in screening results
    - **Clinical Validity**: Results suitable for clinical decision-making
    
    **Inadequate Visual Acuity (<20/100)**:
    - **Reduced Accuracy**: Significant decrease in test reliability
    - **False Positives**: Poor acuity may mimic color vision deficiency
    - **Recommendation**: Address refractive errors before color vision testing
    - **Alternative Approach**: Consider ophthalmologic evaluation first
    
    **Occupational and Regulatory Considerations**:
    
    **High Color-Dependence Occupations**:
    
    **Aviation Industry**:
    - Commercial pilots: Strict color vision requirements
    - Air traffic controllers: Color-coded radar and communication systems
    - Aircraft maintenance: Color-coded wiring and safety systems
    - Regulatory standards vary by country and certification level
    
    **Transportation Sector**:
    - Railroad engineers: Signal light recognition critical for safety
    - Maritime officers: Navigation light interpretation
    - Commercial drivers: Traffic signal recognition (usually not restrictive)
    - Emergency vehicle operators: Color-coded warning systems
    
    **Medical and Healthcare**:
    - Pathology: Color differentiation in tissue samples and cultures
    - Dermatology: Skin color changes and lesion characteristics
    - Laboratory medicine: Colorimetric assays and reagent systems
    - Emergency medicine: Color changes in patient monitoring
    
    **Technical and Industrial**:
    - Electrical work: Color-coded wire identification systems
    - Quality control: Product color consistency and defect detection
    - Graphic design: Color accuracy and aesthetic considerations
    - Photography/printing: Color reproduction and correction
    
    **Accommodations and Adaptive Strategies**:
    
    **Technological Solutions**:
    - Smartphone apps for color identification and labeling
    - Digital color meters and analyzers for precise measurement
    - Enhanced contrast displays and lighting systems
    - Color-blind friendly software palettes and interfaces
    
    **Workplace Adaptations**:
    - Color-coding alternatives (patterns, shapes, labels)
    - Enhanced lighting for improved color discrimination
    - Colleague assistance for color-critical tasks
    - Modified procedures that reduce color-dependence
    
    **Personal Strategies**:
    - Learning alternative visual cues (brightness, position, context)
    - Clothing coordination assistance from family/friends
    - Traffic light recognition by position rather than color
    - Using technology aids for uncertain color situations
    
    **Clinical Decision-Making and Follow-up**:
    
    **Normal Results Management**:
    - **Immediate Actions**: Reassure patient of normal color vision
    - **Documentation**: Record normal results in medical record
    - **Follow-up**: No specific color vision follow-up needed
    - **Re-screening**: Only if new symptoms or concerns arise
    
    **Abnormal Results Management**:
    - **Immediate Actions**: Explain screening results and limitations
    - **Referral Timing**: Ophthalmology consultation within 3-6 months
    - **Additional Testing**: Formal color vision assessment (Farnsworth-Munsell)
    - **Documentation**: Detailed recording of results and referrals made
    
    **Patient Education Priorities**:
    - Nature of condition (usually congenital and stable)
    - Functional impact on daily activities (typically minimal)
    - Occupational considerations and potential limitations
    - Available accommodations and adaptive strategies
    - Genetic implications for family members
    
    **Quality Assurance and Validation**:
    
    **Test Administration Standards**:
    - Consistent environmental conditions for all patients
    - Standardized presentation timing and methodology
    - Proper documentation of testing conditions
    - Regular calibration of digital displays if used
    
    **Result Interpretation Consistency**:
    - Clear scoring criteria and thresholds
    - Consistent application of diagnostic categories
    - Documentation of any unusual circumstances
    - Appropriate use of clinical judgment for borderline results
    
    **Evidence-Based Performance Metrics**:
    - Sensitivity: Approximately 92% for red-green deficiencies
    - Specificity: Approximately 100% (very low false positive rate)
    - Optimal performance with adequate visual acuity and proper administration
    - Reduced reliability in very young children and poor visual acuity
    
    This calculator provides standardized assessment and evidence-based interpretation 
    of Ishihara color vision screening results to support clinical decision-making, 
    occupational counseling, and patient education in ophthalmologic and primary care settings.
    
    Args:
        request: Color vision screening parameters including bilateral plate scores and patient factors
        
    Returns:
        ColorVisionScreeningResponse: Comprehensive assessment with clinical recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("color_vision_screening", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Color Vision Screening",
                    "details": {"parameters": parameters}
                }
            )
        
        return ColorVisionScreeningResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Color Vision Screening",
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