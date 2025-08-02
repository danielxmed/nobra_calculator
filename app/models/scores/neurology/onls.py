"""
Overall Neuropathy Limitations Scale (ONLS) Models

Request and response models for ONLS calculation.

References (Vancouver style):
1. Graham RC, Hughes RA. A modified peripheral neuropathy scale: the Overall 
   Neuropathy Limitations Scale. J Neurol Neurosurg Psychiatry. 2006;77(8):973-6. 
   doi: 10.1136/jnnp.2005.081547.
2. Hughes RA, Donofrio P, Bril V, Dalakas MC, Deng C, Hanna K, et al. 
   Intravenous immune globulin (10% caprylate-chromatography purified) for the 
   treatment of chronic inflammatory demyelinating polyradiculoneuropathy 
   (ICE study): a randomised placebo-controlled trial. Lancet Neurol. 
   2008;7(2):136-44. doi: 10.1016/S1474-4422(07)70329-0.
3. van Nes SI, Vanhoutte EK, van Doorn PA, Hermans M, Bakkers M, Kuitwaard K, et al. 
   Rasch-built Overall Disability Scale (R-ODS) for immune-mediated peripheral 
   neuropathies. Neurology. 2011;76(4):337-45. doi: 10.1212/WNL.0b013e318208824b.

The Overall Neuropathy Limitations Scale (ONLS) is a validated functional assessment 
tool that quantifies disability in patients with peripheral neuropathy by evaluating 
upper and lower extremity functional activities. This scale is widely used in clinical 
practice and research to monitor disease progression and treatment response.
"""

from pydantic import BaseModel, Field
from typing import Literal


class OnlsRequest(BaseModel):
    """
    Request model for Overall Neuropathy Limitations Scale (ONLS)
    
    The Overall Neuropathy Limitations Scale (ONLS) is a validated clinical assessment 
    tool designed to quantify functional disability in patients with peripheral neuropathy. 
    This scale represents a significant advancement in neuropathy assessment, providing 
    a standardized, reliable method for evaluating and monitoring functional limitations 
    in patients with various peripheral nerve disorders.
    
    Clinical Context and Importance:
    
    Peripheral neuropathies encompass a diverse group of disorders affecting the peripheral 
    nervous system, including immune-mediated conditions like chronic inflammatory 
    demyelinating polyneuropathy (CIDP), Guillain-Barré syndrome, diabetic neuropathy, 
    and hereditary neuropathies. These conditions can cause progressive functional 
    impairment that significantly impacts patients' quality of life and independence.
    
    Development and Validation:
    
    The ONLS was developed as a modification of the Overall Disability Sum Score (ODSS) 
    to address limitations in existing disability scales. The key improvement was the 
    addition of running and stair climbing assessments to the legs evaluation, reducing 
    ceiling effects and improving content validity for detecting functional changes 
    in patients with milder disabilities.
    
    Scale Components and Clinical Rationale:
    
    The ONLS consists of two main components that comprehensively assess functional 
    disability across the spectrum of peripheral neuropathy severity:
    
    Arms Grade Assessment (0-5 points):
    
    This component evaluates upper extremity functional capacity, focusing on activities 
    of daily living that require fine motor control, grip strength, and coordinated 
    arm movements. The assessment considers the impact of sensory and motor deficits 
    on practical hand and arm functions.
    
    Grade 0 - Normal Function:
    Complete preservation of all arm and hand functions with no symptoms or signs 
    affecting daily activities. Patients can perform all tasks requiring fine motor 
    control, strength, and coordination without limitation.
    
    Grade 1 - Minor Symptoms:
    Presence of neuropathic symptoms (numbness, tingling, mild weakness) that are 
    noticeable to the patient but do not interfere with any functional activities. 
    All arm and hand functions remain intact despite subjective symptoms.
    
    Grade 2 - Mild Disability:
    Functional limitations that affect the ease or speed of performing activities 
    but do not prevent any specific functions. Examples include difficulty with 
    fine tasks like buttoning clothes or writing, but all activities remain possible.
    
    Grade 3 - Moderate Disability:
    Disability that prevents at least one specific arm or hand function while 
    allowing others to be performed. May affect activities like opening jars, 
    typing, or precise manipulation tasks.
    
    Grade 4 - Severe Disability:
    Disability affecting both arms that prevents all specific arm functions, 
    though some purposeful movements remain possible. Gross motor movements 
    may be preserved while fine motor control is severely impaired.
    
    Grade 5 - Complete Disability:
    Complete loss of purposeful arm movements with profound weakness or 
    paralysis preventing any functional use of the arms.
    
    Legs Grade Assessment (0-7 points):
    
    This component evaluates lower extremity function with particular attention 
    to mobility, ambulation, and the need for assistive devices. The expanded 
    scale (compared to arms) reflects the greater functional impact of leg 
    disability on independence and quality of life.
    
    Grade 0 - Normal Function:
    Walking, climbing stairs, and running are completely unaffected. No 
    gait abnormalities or mobility limitations. Complete preservation 
    of lower extremity function.
    
    Grade 1 - Affected but Normal Gait:
    Walking, stair climbing, and running are affected by neuropathic symptoms 
    (weakness, numbness, pain) but gait appears normal to observers. 
    Subjective limitations without visible gait changes.
    
    Grade 2 - Abnormal Gait:
    Independent walking is maintained but with clearly abnormal gait pattern. 
    May include steppage gait, wide-based walking, or other compensatory 
    patterns. No assistive devices required.
    
    Grade 3 - Unilateral Support Required:
    Requires unilateral support (cane, crutch, or wall support) to walk 
    10 meters safely. Represents significant balance or strength impairment 
    requiring external support for stability.
    
    Grade 4 - Bilateral Support Required:
    Requires bilateral support (walker, two crutches, or assistance from 
    two people) to walk 10 meters. Severe mobility impairment with 
    substantial balance and strength deficits.
    
    Grade 5 - Wheelchair with Limited Standing:
    Primarily wheelchair-dependent but retains ability to stand briefly 
    and walk short distances (approximately 1 meter) with assistance. 
    Some residual lower extremity function preserved.
    
    Grade 6 - Wheelchair with Leg Movement:
    Completely wheelchair-dependent but retains some purposeful leg 
    movements. May be able to transfer with assistance or perform 
    limited leg exercises.
    
    Grade 7 - Complete Immobility:
    Complete restriction to wheelchair or bed with no purposeful leg 
    movements. Represents profound lower extremity paralysis with 
    complete loss of motor function.
    
    Clinical Applications and Utility:
    
    Disease Monitoring:
    The ONLS provides objective tracking of functional changes over time, 
    allowing clinicians to monitor disease progression or improvement 
    following treatment interventions. Regular assessments can detect 
    subtle changes before they become clinically obvious.
    
    Treatment Response Assessment:
    In clinical trials and practice, the ONLS serves as a primary outcome 
    measure for evaluating treatment efficacy. Changes in ONLS scores 
    can demonstrate meaningful clinical improvement or deterioration.
    
    Functional Prognosis:
    ONLS scores help predict functional outcomes and guide rehabilitation 
    planning. Higher scores indicate greater need for assistive devices, 
    environmental modifications, and support services.
    
    Clinical Decision Making:
    Results inform decisions about treatment intensity, rehabilitation 
    referrals, disability determinations, and long-term care planning.
    
    Validation and Psychometric Properties:
    
    Reliability:
    The ONLS demonstrates excellent inter-rater reliability with an 
    intraclass correlation coefficient of 0.97, indicating high consistency 
    between different evaluators.
    
    Validity:
    Strong correlation with the original ODSS (r = 0.97) while showing 
    improved content validity and reduced ceiling effects. Significant 
    correlations with quality of life measures and participation scales.
    
    Responsiveness:
    Acceptable responsiveness with standardized response mean of 0.76, 
    indicating ability to detect clinically meaningful changes over time.
    
    Clinical Considerations and Best Practices:
    
    Assessment Method:
    Direct observation by trained healthcare professionals is preferred 
    over patient self-reporting to ensure accuracy and consistency. 
    Standardized assessment conditions improve reliability.
    
    Timing:
    Assessments should be performed when patients are at their functional 
    baseline, avoiding periods of acute illness or fatigue that might 
    temporarily affect performance.
    
    Documentation:
    Detailed documentation of specific functional limitations helps track 
    patterns of change and guides targeted interventions.
    
    Interpretation Guidelines:
    
    Scores 0-3: Generally preserved independence with minimal impact on 
    daily activities. Appropriate for outpatient management with regular 
    monitoring.
    
    Scores 4-6: Moderate disability requiring assessment for assistive 
    devices, rehabilitation services, and environmental modifications.
    
    Scores 7-9: Severe disability necessitating comprehensive rehabilitation, 
    adaptive equipment, and potentially caregiver support.
    
    Scores 10-12: Profound disability requiring extensive care coordination, 
    disability services, and comprehensive support systems.
    
    Limitations and Considerations:
    
    Age Considerations:
    The ONLS has not been validated in pediatric populations and may not 
    be appropriate for children with developmental considerations.
    
    Cognitive Factors:
    The scale focuses on motor and sensory function and does not account 
    for cognitive impairments that might affect functional performance.
    
    Acute vs. Chronic:
    Most validation has been in chronic neuropathies; applicability to 
    acute conditions may vary.
    
    Cultural Factors:
    Some functional assessments may be influenced by cultural differences 
    in activity expectations and assistive device use.
    
    References (Vancouver style):
    1. Graham RC, Hughes RA. A modified peripheral neuropathy scale: the Overall 
    Neuropathy Limitations Scale. J Neurol Neurosurg Psychiatry. 2006;77(8):973-6. 
    doi: 10.1136/jnnp.2005.081547.
    2. Hughes RA, Donofrio P, Bril V, Dalakas MC, Deng C, Hanna K, et al. 
    Intravenous immune globulin (10% caprylate-chromatography purified) for the 
    treatment of chronic inflammatory demyelinating polyradiculoneuropathy 
    (ICE study): a randomised placebo-controlled trial. Lancet Neurol. 
    2008;7(2):136-44. doi: 10.1016/S1474-4422(07)70329-0.
    3. van Nes SI, Vanhoutte EK, van Doorn PA, Hermans M, Bakkers M, Kuitwaard K, et al. 
    Rasch-built Overall Disability Scale (R-ODS) for immune-mediated peripheral 
    neuropathies. Neurology. 2011;76(4):337-45. doi: 10.1212/WNL.0b013e318208824b.
    """
    
    arms_grade: Literal[0, 1, 2, 3, 4, 5] = Field(
        ...,
        description="Arms functional disability grade. 0=Normal function, 1=Minor symptoms not affecting function, 2=Mild disability affecting but not preventing function, 3=Moderate disability preventing some functions, 4=Severe disability preventing all functions with some purposeful movement, 5=Complete disability preventing all purposeful movements",
        example=1
    )
    
    legs_grade: Literal[0, 1, 2, 3, 4, 5, 6, 7] = Field(
        ...,
        description="Legs functional disability grade. 0=Normal walking/stairs/running, 1=Affected but normal gait, 2=Independent walking with abnormal gait, 3=Requires unilateral support for 10m, 4=Requires bilateral support for 10m, 5=Wheelchair-bound but can stand/walk 1m with help, 6=Wheelchair-restricted with some purposeful leg movements, 7=Wheelchair/bed-restricted with no purposeful leg movements",
        example=2
    )
    
    class Config:
        schema_extra = {
            "example": {
                "arms_grade": 1,
                "legs_grade": 2
            }
        }


class OnlsResponse(BaseModel):
    """
    Response model for Overall Neuropathy Limitations Scale (ONLS)
    
    The ONLS response provides comprehensive assessment of functional disability 
    in peripheral neuropathy, offering detailed clinical interpretation and 
    management guidance based on the calculated score.
    
    Score Interpretation and Clinical Management:
    
    No Disability (Score 0):
    - Functional Status: Complete preservation of arm and leg function
    - Clinical Significance: No evidence of functional impairment from neuropathy
    - Management: Routine monitoring and preventive care
    - Prognosis: Excellent functional outlook
    - Follow-up: Regular neurological assessments to detect early changes
    
    Mild Disability (Scores 1-3):
    - Functional Status: Minimal impact on daily activities with preserved independence
    - Clinical Significance: Early neuropathic changes with functional compensation
    - Management: Continue current treatment, monitor progression, symptom management
    - Interventions: Physical therapy for symptom relief, balance training
    - Prognosis: Generally favorable with appropriate management
    - Quality of Life: Usually maintained with minor adaptations
    
    Moderate Disability (Scores 4-6):
    - Functional Status: Noticeable limitations requiring some adaptations
    - Clinical Significance: Progressive neuropathy affecting daily function
    - Management: Treatment optimization, rehabilitation services
    - Interventions: Assistive devices, environmental modifications, adaptive strategies
    - Monitoring: Regular assessment for progression and treatment response
    - Support: Occupational therapy for adaptive techniques
    
    Severe Disability (Scores 7-9):
    - Functional Status: Substantial impairment requiring significant assistance
    - Clinical Significance: Advanced neuropathy with major functional impact
    - Management: Aggressive treatment optimization, comprehensive rehabilitation
    - Interventions: Mobility aids, home modifications, caregiver training
    - Support: Disability services, social work consultation
    - Monitoring: Frequent assessments and multidisciplinary care coordination
    
    Very Severe Disability (Scores 10-12):
    - Functional Status: Profound disability requiring extensive care
    - Clinical Significance: End-stage neuropathy with complete functional dependence
    - Management: Comprehensive multidisciplinary care, palliative approaches
    - Interventions: Full-time care assistance, complete environmental adaptation
    - Support: Disability services, respite care, family support programs
    - Quality of Life: Focus on comfort, dignity, and emotional support
    
    Clinical Applications:
    
    Disease Monitoring:
    - Track functional changes over time to assess disease progression
    - Identify early deterioration requiring treatment adjustment
    - Monitor treatment response and effectiveness
    - Guide timing of interventions and referrals
    
    Treatment Planning:
    - Determine appropriate treatment intensity based on functional status
    - Guide rehabilitation goals and strategies
    - Inform prognosis and family counseling
    - Support clinical trial eligibility and outcome assessment
    
    Resource Allocation:
    - Identify patients requiring assistive devices or home modifications
    - Guide referrals to rehabilitation services and disability support
    - Inform insurance coverage and disability determinations
    - Plan for long-term care needs and caregiver support
    
    Prognostic Indicators:
    
    Favorable Indicators:
    - Low baseline ONLS scores with stable or improving trends
    - Responsiveness to treatment with functional improvements
    - Preserved proximal strength and sensory function
    - Early intervention and appropriate treatment adherence
    
    Concerning Indicators:
    - Rapid progression to higher ONLS scores
    - Poor treatment response with continued deterioration
    - Development of severe proximal weakness
    - Respiratory or bulbar involvement
    
    Multidisciplinary Care Coordination:
    
    Neurology:
    - Disease-specific treatment optimization
    - Monitoring for complications and comorbidities
    - Coordination with subspecialists as needed
    - Long-term management planning
    
    Rehabilitation Medicine:
    - Functional assessment and goal setting
    - Prescription of assistive devices and orthotics
    - Coordination of therapy services
    - Adaptive strategies and techniques
    
    Physical Therapy:
    - Strength and balance training programs
    - Gait analysis and mobility optimization
    - Fall prevention strategies
    - Equipment training and safety education
    
    Occupational Therapy:
    - Activities of daily living assessment and training
    - Adaptive equipment evaluation and training
    - Home safety assessment and modification recommendations
    - Work capacity evaluation and job modification strategies
    
    Social Work:
    - Resource coordination and advocacy
    - Disability benefits and insurance navigation
    - Community resource identification
    - Caregiver support and education
    
    Quality of Life Considerations:
    
    Psychosocial Impact:
    - Assessment for depression and anxiety related to functional loss
    - Counseling and support group referrals
    - Family education and coping strategies
    - Vocational rehabilitation and return-to-work planning
    
    Environmental Modifications:
    - Home accessibility assessments and modifications
    - Transportation alternatives and mobility solutions
    - Workplace accommodations and ergonomic adjustments
    - Recreation and leisure activity adaptations
    
    Long-term Planning:
    - Advanced directive discussions for progressive conditions
    - Estate planning and legal considerations
    - Long-term care planning and resource identification
    - Emergency planning and safety considerations
    
    Reference: Graham RC, Hughes RA. J Neurol Neurosurg Psychiatry. 2006;77(8):973-6.
    """
    
    result: int = Field(
        ...,
        description="Total ONLS score (range 0-12 points) representing overall neuropathy severity",
        example=3
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Detailed clinical interpretation with functional assessment and comprehensive management recommendations",
        example="MILD FUNCTIONAL DISABILITY (ONLS Score: 3): Mild peripheral neuropathy with minimal impact on daily activities. ARMS: Minor symptoms not affecting function LEGS: Independent walking with abnormal gait FUNCTIONAL STATUS: Some symptoms present but function largely preserved. Patient remains independent in most activities. MANAGEMENT: Continue current treatment, monitor for progression, consider physical therapy for symptom management. PROGNOSIS: Generally good functional outcome with appropriate management."
    )
    
    stage: str = Field(
        ...,
        description="Functional disability category",
        example="Mild Disability"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the disability level",
        example="Minimal functional limitations"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 3,
                "unit": "points",
                "interpretation": "MILD FUNCTIONAL DISABILITY (ONLS Score: 3): Mild peripheral neuropathy with minimal impact on daily activities. ARMS: Minor symptoms not affecting function LEGS: Independent walking with abnormal gait FUNCTIONAL STATUS: Some symptoms present but function largely preserved. Patient remains independent in most activities. MANAGEMENT: Continue current treatment, monitor for progression, consider physical therapy for symptom management. PROGNOSIS: Generally good functional outcome with appropriate management.",
                "stage": "Mild Disability",
                "stage_description": "Minimal functional limitations"
            }
        }