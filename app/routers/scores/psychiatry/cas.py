"""
Coronavirus Anxiety Scale (CAS) Router

Endpoint for calculating CAS coronavirus-related anxiety assessment.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.psychiatry.cas import (
    CasRequest,
    CasResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post("/cas", response_model=CasResponse)
async def calculate_cas(request: CasRequest):
    """
    Calculates Coronavirus Anxiety Scale (CAS) Assessment
    
    The Coronavirus Anxiety Scale (CAS) is a brief, validated mental health screening tool 
    designed to identify individuals experiencing dysfunctional levels of anxiety specifically 
    related to the COVID-19 pandemic. This 5-item self-report measure focuses on 
    physiologically-based symptoms triggered by coronavirus-related information and thoughts.
    
    **Clinical Background and Significance**:
    
    **Pandemic-Specific Mental Health Assessment**:
    - Developed specifically to address the unique psychological impact of COVID-19
    - Fills critical gap in pandemic-related mental health screening tools
    - Focuses on coronavirus-specific anxiety symptoms not captured by general anxiety scales
    - Validated across diverse populations and cultural contexts globally
    - Essential tool for identifying individuals requiring targeted pandemic-related mental health support
    
    **Scale Development and Psychometric Properties**:
    - Developed using rigorous psychometric methodology during early pandemic period
    - Excellent internal consistency (Cronbach's α = 0.92) across validation studies
    - Stable, unidimensional factor structure invariant across gender, race, and age
    - Demonstrates strong test-retest reliability and construct validity
    - Brief administration (2-3 minutes) suitable for clinical screening and research
    
    **Diagnostic Performance and Clinical Utility**:
    
    **Optimized Cut-off Threshold**:
    - Cut-off Score: ≥9 points indicates dysfunctional coronavirus-related anxiety
    - Diagnostic Performance: 90% sensitivity and 85% specificity
    - Performance comparable to established psychiatric screening instruments
    - Optimal balance between sensitivity and specificity for clinical decision-making
    - Validated across multiple studies and populations confirming diagnostic accuracy
    
    **Clinical Decision Framework**:
    - Scores 0-8: No dysfunctional anxiety, normal pandemic-related concerns
    - Scores 9-20: Dysfunctional anxiety requiring clinical evaluation and intervention
    - Higher scores indicate greater severity and functional impairment
    - Provides actionable information for treatment planning and resource allocation
    
    **Five-Item Assessment Domains**:
    
    **Item 1 - Physiological Response to Coronavirus News**:
    "I felt dizzy, lightheaded, or faint when I read or listened to news about the coronavirus"
    
    **Clinical Significance**: 
    - Assesses somatic anxiety symptoms triggered by coronavirus information exposure
    - Reflects autonomic nervous system activation and physiological stress response
    - Indicates potential need for media consumption strategies and exposure management
    - Common manifestation of pandemic-related anxiety affecting daily information processing
    
    **Assessment Focus**: 
    - Physical symptoms directly linked to coronavirus news consumption
    - Severity ranges from no symptoms to daily physical distress
    - May indicate broader patterns of anxiety-related avoidance behaviors
    - Important for understanding information processing difficulties
    
    **Item 2 - Sleep Disruption from Coronavirus Thoughts**:
    "I had trouble falling or staying asleep because I was thinking about the coronavirus"
    
    **Clinical Significance**: 
    - Evaluates sleep disturbance specifically related to coronavirus preoccupation
    - Sleep disruption is key indicator of anxiety severity and functional impairment
    - Persistent sleep problems can exacerbate anxiety and compromise immune function
    - Critical factor in treatment planning and intervention strategies
    
    **Assessment Focus**: 
    - Coronavirus-specific intrusive thoughts affecting sleep initiation and maintenance
    - Sleep quality impact on overall mental and physical health
    - Potential need for sleep hygiene interventions and anxiety management
    - Connection between pandemic worries and circadian rhythm disruption
    
    **Item 3 - Paralytic Response to Coronavirus Information**:
    "I felt paralyzed or frozen when I thought about or was exposed to information about the coronavirus"
    
    **Clinical Significance**: 
    - Assesses immobilizing anxiety responses to coronavirus-related stimuli
    - Reflects severe anxiety symptoms that significantly impair daily functioning
    - May indicate avoidance behaviors and information processing difficulties
    - Suggests potential need for graduated exposure and cognitive restructuring
    
    **Assessment Focus**: 
    - Degree of functional impairment from coronavirus-related anxiety
    - Cognitive and behavioral paralysis affecting decision-making and activities
    - Potential impact on ability to process pandemic-related information effectively
    - Indication of severe anxiety requiring intensive intervention approaches
    
    **Item 4 - Appetite Changes Related to Coronavirus Thoughts**:
    "I lost interest in eating when I thought about or was exposed to information about the coronavirus"
    
    **Clinical Significance**: 
    - Evaluates appetite disruption as somatic manifestation of coronavirus anxiety
    - Changes in eating patterns can affect physical health and nutritional status
    - May reflect broader health and survival concerns related to the pandemic
    - Important to monitor for potential weight loss and nutritional complications
    
    **Assessment Focus**: 
    - Coronavirus-specific impact on appetite regulation and eating behaviors
    - Physical health implications of anxiety-related appetite changes
    - Connection between pandemic fears and basic physiological needs
    - Potential need for nutritional monitoring and medical evaluation
    
    **Item 5 - Gastrointestinal Symptoms with Coronavirus Thoughts**:
    "I felt nauseous or had stomach problems when I thought about or was exposed to information about the coronavirus"
    
    **Clinical Significance**: 
    - Assesses gastrointestinal manifestations of coronavirus-related anxiety
    - Gut-brain connection makes GI symptoms common in anxiety disorders
    - May reflect visceral anxiety responses to pandemic-related stress
    - Important to differentiate from potential COVID-19 symptoms or medical conditions
    
    **Assessment Focus**: 
    - Physical manifestations of anxiety specifically triggered by coronavirus thoughts
    - Potential impact on daily functioning and comfort levels
    - Need for medical evaluation to rule out other causes
    - Connection between psychological stress and gastrointestinal symptoms
    
    **Clinical Implementation and Assessment Guidelines**:
    
    **Administration Standards**:
    - Self-administered questionnaire requiring 2-3 minutes to complete
    - Can be administered in-person, via telephone, or through electronic platforms
    - Appropriate for adults (18+ years) across diverse cultural backgrounds
    - Time frame: Assessment covers symptoms experienced over the past 2 weeks
    - May require interpretation assistance for individuals with literacy challenges
    
    **Scoring and Interpretation Framework**:
    
    **Response Scale**: 
    Each item rated on 5-point frequency scale over past 2 weeks:
    - 0 = Not at all
    - 1 = Rare, less than a day or two
    - 2 = Several days
    - 3 = More than 7 days
    - 4 = Nearly every day over the last 2 weeks
    
    **Score Calculation**: 
    - Total Score Range: 0-20 points (sum of all 5 items)
    - Clinical Threshold: ≥9 points indicates dysfunctional anxiety
    - Severity Levels: Higher scores indicate greater symptom severity and impairment
    
    **Clinical Interpretation by Score Range**:
    
    **Scores 0-8 (No Dysfunctional Anxiety)**:
    - **Clinical Significance**: Normal levels of coronavirus-related concern
    - **Intervention Level**: Preventive education and routine monitoring
    - **Recommendations**: Maintain healthy coping strategies, stress management
    - **Follow-up**: Reassess if circumstances change or symptoms worsen
    - **Prognosis**: Generally favorable with appropriate self-care
    
    **Scores 9-12 (Mild Dysfunctional Anxiety)**:
    - **Clinical Significance**: Clinically significant coronavirus-related anxiety
    - **Intervention Level**: Supportive counseling and psychoeducation
    - **Recommendations**: Brief therapy, anxiety management techniques, monitoring
    - **Follow-up**: Bi-weekly to monthly assessment during intervention
    - **Prognosis**: Good response to supportive interventions typically expected
    
    **Scores 13-16 (Moderate Dysfunctional Anxiety)**:
    - **Clinical Significance**: Moderate to severe coronavirus-related anxiety
    - **Intervention Level**: Professional mental health evaluation and treatment
    - **Recommendations**: Cognitive-behavioral therapy, comprehensive assessment
    - **Follow-up**: Weekly to bi-weekly monitoring during active treatment
    - **Prognosis**: Requires active treatment but generally responsive to intervention
    
    **Scores 17-20 (Severe Dysfunctional Anxiety)**:
    - **Clinical Significance**: Severe coronavirus-related anxiety with high impairment
    - **Intervention Level**: Immediate professional intervention and comprehensive care
    - **Recommendations**: Intensive therapy, possible medication consultation, crisis evaluation
    - **Follow-up**: Frequent monitoring with clinical discretion
    - **Prognosis**: Requires intensive treatment; may need coordinated care approach
    
    **Treatment Planning and Intervention Strategies**:
    
    **Evidence-Based Interventions by Severity Level**:
    
    **Preventive Interventions (Scores 0-8)**:
    - Psychoeducation about normal pandemic-related stress responses
    - Stress management and resilience building techniques
    - Maintenance of healthy lifestyle and established coping strategies
    - Information about when to seek additional support
    
    **Supportive Interventions (Scores 9-12)**:
    - Brief supportive counseling focused on coronavirus-related concerns
    - Cognitive-behavioral techniques for anxiety management
    - Structured problem-solving for pandemic-related stressors
    - Self-help resources and guided self-management strategies
    
    **Active Treatment (Scores 13-16)**:
    - Comprehensive mental health evaluation and treatment planning
    - Cognitive-behavioral therapy specifically adapted for pandemic-related anxiety
    - Mindfulness-based interventions and stress reduction techniques
    - Assessment for comorbid mental health conditions and integrated treatment
    
    **Intensive Intervention (Scores 17-20)**:
    - Immediate comprehensive psychiatric evaluation including risk assessment
    - Intensive cognitive-behavioral therapy or other evidence-based treatments
    - Consideration of pharmacological intervention in consultation with psychiatry
    - Coordinated care approach with multiple providers as indicated
    
    **Quality Assurance and Implementation Considerations**:
    
    **Cultural Sensitivity and Adaptation**:
    - Consider cultural differences in anxiety expression and symptom reporting
    - Adapt communication style to cultural background and language preferences
    - Account for cultural factors affecting pandemic-related concerns and responses
    - Provide culturally appropriate interpretation and support services
    
    **Professional Training and Competency Requirements**:
    - Ensure adequate training in pandemic-related mental health assessment
    - Maintain competency in evidence-based anxiety interventions
    - Stay informed about evolving pandemic conditions and psychological impacts
    - Coordinate appropriately with other healthcare providers and specialists
    
    **Ethical and Safety Considerations**:
    - Maintain confidentiality and privacy, particularly in telehealth contexts
    - Provide appropriate crisis intervention resources and emergency contacts
    - Consider mandatory reporting requirements for imminent risk situations
    - Ensure equitable access to care regardless of socioeconomic status
    
    **Research and Quality Improvement Applications**:
    
    **Population Health Monitoring**:
    - Track coronavirus-related anxiety prevalence across different populations
    - Monitor effectiveness of public health interventions on mental health outcomes
    - Identify vulnerable populations requiring additional mental health support
    - Inform resource allocation and mental health service planning decisions
    
    **Treatment Outcome Research**:
    - Measure intervention effectiveness using CAS scores as outcome measure
    - Compare different treatment approaches for pandemic-related anxiety disorders
    - Develop predictive models for treatment response and recovery patterns
    - Contribute to evidence base for pandemic-related mental health interventions
    
    This calculator provides standardized, validated assessment of coronavirus-related 
    anxiety symptoms, supporting evidence-based clinical decision-making, mental health 
    service delivery, and research applications in pandemic-related psychological care.
    
    Args:
        request: CAS assessment parameters including 5 symptom domain scores
        
    Returns:
        CasResponse: Comprehensive coronavirus anxiety assessment with clinical interpretation and recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("cas", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating CAS assessment",
                    "details": {"parameters": parameters}
                }
            )
        
        return CasResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for CAS assessment",
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