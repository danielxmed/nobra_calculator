"""
Children's Hospital of Eastern Ontario Pain Scale (CHEOPS) Router

Endpoint for calculating CHEOPS pain score for post-operative pediatric pain assessment.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.pediatrics.cheops_pain_scale import (
    CheopsPainScaleRequest,
    CheopsPainScaleResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/cheops_pain_scale",
    response_model=CheopsPainScaleResponse,
    summary="Calculate Children's Hospital of Eastern Ontario Pain Scale",
    description="Quantifies post-operative pain in pediatric patients aged 1-5 years using behavioral observations",
    response_description="The calculated cheops pain scale with interpretation",
    operation_id="calculate_cheops_pain_scale"
)
async def calculate_cheops_pain_scale(request: CheopsPainScaleRequest):
    """
    Calculates Children's Hospital of Eastern Ontario Pain Scale (CHEOPS)
    
    The Children's Hospital of Eastern Ontario Pain Scale (CHEOPS) is a validated 
    behavioral pain assessment tool specifically designed for post-operative pain 
    evaluation in pediatric patients aged 1-5 years. This observational scale provides 
    objective, standardized assessment of pain intensity through systematic evaluation 
    of six key behavioral categories.
    
    **Historical Development and Validation**:
    
    **Original Development (1985)**:
    - Developed at Children's Hospital of Eastern Ontario by McGrath et al.
    - Designed specifically for post-operative pain assessment in young children
    - Created to address need for objective pain measurement in non-verbal patients
    - Established foundation for behavioral pain assessment in pediatric settings
    
    **Clinical Validation**:
    - Extensively validated across diverse pediatric populations
    - Demonstrated reliability and validity in post-operative settings
    - Cross-validated in multiple cultural and clinical contexts
    - Recognized as gold standard for preverbal pain assessment
    - Widely adopted in pediatric hospitals and research settings
    
    **Contemporary Applications**:
    - Standard tool in pediatric post-anesthesia care units (PACU)
    - Integrated into electronic health records and clinical protocols
    - Used in pediatric pain research and quality improvement initiatives
    - Training tool for healthcare providers in pediatric pain recognition
    
    **CHEOPS Behavioral Assessment Framework**:
    
    **Systematic Observation Approach**:
    The CHEOPS scale employs systematic behavioral observation across six categories, 
    each representing different aspects of pain expression in young children. This 
    comprehensive approach captures the multidimensional nature of pediatric pain 
    response and provides objective scoring criteria for clinical decision-making.
    
    **Category 1: Cry Assessment (1-3 points)**:
    
    **No Crying (1 point)**:
    - Child is quiet, not vocalizing distress
    - May include normal vocalizations unrelated to pain
    - Indicates absence of vocal pain indicators
    - Baseline state for comfortable, pain-free child
    
    **Moaning/Crying (2 points)**:
    - Intermittent moaning, whimpering, or soft crying
    - Vocalizations suggest discomfort but not severe distress
    - May include restless sounds or mild complaints
    - Indicates moderate pain or discomfort
    
    **Screaming (3 points)**:
    - Loud crying, screaming, or intense vocal distress
    - Continuous or frequent intense vocalizations
    - High-pitched crying characteristic of significant pain
    - Indicates severe pain requiring immediate attention
    
    **Category 2: Facial Expression Assessment (0-2 points)**:
    
    **Smiling (0 points)**:
    - Happy, content facial expression
    - Positive emotional state indicated by facial features
    - Suggests absence of pain and presence of comfort
    - Optimal state indicating effective pain management
    
    **Composed/Neutral (1 point)**:
    - Calm, neutral facial expression
    - Neither positive nor negative emotional indicators
    - Baseline facial state for comfortable child
    - Indicates adequate pain control
    
    **Grimace (2 points)**:
    - Frowning, grimacing, or facial tension
    - Brow furrowing, mouth turned down, eyes squinted
    - Clear facial indicators of discomfort or pain
    - Suggests need for pain management intervention
    
    **Category 3: Verbal Response Assessment (0-2 points)**:
    
    **Positive Statements (0 points)**:
    - Positive comments, appears compliant and comfortable
    - Age-appropriate positive verbal interactions
    - Indicates good pain control and emotional state
    - Optimal verbal response category
    
    **Not Talking/Other Complaints (1 point)**:
    - Silent or making non-pain related complaints
    - May include general fussiness or non-specific complaints
    - Intermediate verbal response indicating some distress
    - Common in children experiencing mild discomfort
    
    **Pain Complaints (2 points)**:
    - Verbal expressions of pain, discomfort, or requests for help
    - Direct statements about hurt, pain, or need for relief
    - Age-appropriate pain verbalizations
    - Clear indicator of significant pain requiring intervention
    
    **Category 4: Torso Position Assessment (1-2 points)**:
    
    **Neutral Position (1 point)**:
    - Comfortable resting position, appears relaxed
    - Normal posture for age and clinical situation
    - Body positioning suggests comfort and absence of guarding
    - Indicates effective pain management
    
    **Shifting/Tense (2 points)**:
    - Restless movement, body tension, or protective positioning
    - May include shivering, sitting upright when should be recumbent
    - Requires physical restraint to maintain safe positioning
    - Body language indicating discomfort and pain
    
    **Category 5: Touch/Wound Interaction Assessment (1-2 points)**:
    
    **Not Touching Wound (1 point)**:
    - No reaching toward or touching of surgical site
    - Hands positioned away from wound area
    - Absence of protective or guarding behaviors
    - Indicates absence of localized pain at surgical site
    
    **Reaching/Touching Wound (2 points)**:
    - Reaching toward, touching, or attempting to protect wound area
    - Hands drawn to surgical site in protective manner
    - May require restraint to prevent wound interference
    - Strong indicator of localized surgical site pain
    
    **Category 6: Legs Position Assessment (1-2 points)**:
    
    **Neutral Position (1 point)**:
    - Legs in relaxed, comfortable position
    - Normal positioning for age and clinical situation
    - Lower extremities appear relaxed and comfortable
    - Indicates overall comfort and pain control
    
    **Squirming/Tensed (2 points)**:
    - Squirming, tensed leg muscles, or abnormal positioning
    - May include standing when should be resting
    - Requires restraint to maintain appropriate positioning
    - Lower extremity positioning indicating pain or discomfort
    
    **Clinical Interpretation and Management Guidelines**:
    
    **Score 4 (Minimum Possible): No Significant Pain**:
    - **Clinical Significance**: Minimal or no pain present
    - **Patient Presentation**: Child appears comfortable, relaxed, not distressed
    - **Intervention**: No analgesic intervention typically required
    - **Monitoring**: Continue routine post-operative monitoring and comfort measures
    - **Reassessment**: Every 3 hours or as clinically indicated
    - **Family Education**: Normal recovery pattern, continue comfort measures
    - **Documentation**: Note effective pain management, continue current plan
    
    **Score 5-7: Mild to Moderate Pain**:
    - **Clinical Significance**: Pain present requiring clinical judgment for intervention
    - **Patient Presentation**: Some distress behaviors present, variable comfort level
    - **Intervention**: Consider administering appropriate analgesic medication
    - **Clinical Decision Factors**:
      - Time since last analgesic dose
      - Type and extent of surgical procedure
      - Individual patient pain tolerance and history
      - Presence of anxiety versus pain components
    - **Monitoring**: Reassess pain level after intervention, provide comfort measures
    - **Reassessment**: 15-20 minutes after IV, 30-45 minutes after PO/PR analgesics
    - **Non-pharmacologic Interventions**: Position changes, comfort items, distraction
    
    **Score 8-13 (Maximum Possible): Severe Pain**:
    - **Clinical Significance**: Significant pain requiring immediate intervention
    - **Patient Presentation**: Multiple distress behaviors, clear pain indicators
    - **Intervention**: Analgesic medication required immediately
    - **Urgency**: Priority intervention to prevent prolonged suffering
    - **Monitoring**: Comprehensive pain management strategies, frequent monitoring
    - **Reassessment**: Frequent reassessment until adequate pain control achieved
    - **Escalation**: Consider multimodal pain management, anesthesia consultation
    - **Quality Measures**: Rapid response to severe pain indicators
    
    **Implementation Framework and Best Practices**:
    
    **Assessment Protocol**:
    - Systematic observation of all six behavioral categories required
    - Observe child in natural state when possible (avoid stimulation during assessment)
    - Allow adequate observation time (2-3 minutes minimum)
    - Consider individual developmental and behavioral patterns
    - Document specific behaviors observed in each category
    
    **Observer Training Requirements**:
    - Healthcare providers must be trained in CHEOPS administration
    - Understanding of normal developmental behaviors for 1-5 year age group
    - Recognition of individual variations in pain expression
    - Ability to differentiate pain from anxiety, fear, or general distress
    - Knowledge of factors that may influence behavioral observations
    
    **Quality Assurance Measures**:
    - Regular inter-rater reliability assessments
    - Standardized training programs for new staff
    - Integration with electronic health records for consistent documentation
    - Regular review of pain management outcomes and score effectiveness
    - Feedback mechanisms for continuous improvement
    
    **Clinical Decision Support Integration**:
    - Automated alerts for scores requiring intervention (≥5 points)
    - Integration with medication administration records
    - Trending capabilities to track pain management effectiveness
    - Support for clinical pathways and standardized pain protocols
    
    **Special Considerations and Limitations**:
    
    **Developmental Considerations**:
    - Individual variations in behavioral expression across age range (1-5 years)
    - Cultural factors may influence pain expression and interpretation
    - Baseline behavioral patterns should be considered when known
    - Developmental delays may affect behavioral indicators
    
    **Clinical Context Factors**:
    - Type and extent of surgical procedure affects expected pain levels
    - Time since surgery influences pain trajectory and expected scores
    - Presence of other medical conditions may affect pain expression
    - Medication effects (sedation, muscle relaxants) may influence scoring
    
    **Assessment Limitations**:
    - Requires direct visual observation by trained healthcare provider
    - Not validated for procedural pain assessment (designed for post-operative use)
    - May have limited validity beyond immediate post-operative period
    - Individual behavioral variations may affect scoring accuracy
    - Observer bias and interpretation differences possible
    
    **Integration with Comprehensive Pain Management**:
    
    **Multimodal Assessment Approach**:
    - Use alongside physiological indicators when available
    - Consider parent/caregiver observations of child's behavior
    - Integrate with self-report measures when developmentally appropriate
    - Document response to previous pain management interventions
    
    **Family-Centered Care Integration**:
    - Educate families about pain assessment process and findings
    - Incorporate family observations and concerns into assessment
    - Support family understanding of pain management plan
    - Provide education about home pain management strategies
    
    **Quality Improvement Applications**:
    - Performance metrics for pediatric pain management programs
    - Standardized tool for research and quality improvement initiatives
    - Benchmark for evaluating effectiveness of pain management protocols
    - Support for accreditation and regulatory compliance requirements
    
    This calculator provides evidence-based pediatric pain assessment to support 
    clinical decision-making and optimize post-operative pain management for young 
    children, ensuring appropriate and timely interventions based on standardized 
    behavioral observations.
    
    Args:
        request: CHEOPS behavioral assessment parameters
        
    Returns:
        CheopsPainScaleResponse: Pain score with clinical recommendations and intervention guidance
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("cheops_pain_scale", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating CHEOPS Pain Scale",
                    "details": {"parameters": parameters}
                }
            )
        
        return CheopsPainScaleResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for CHEOPS Pain Scale",
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