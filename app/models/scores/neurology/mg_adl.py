"""
Myasthenia Gravis Activities of Daily Living (MG-ADL) Scale Models

Request and response models for MG-ADL calculation.

References (Vancouver style):
1. Wolfe GI, Herbelin L, Nations SP, Foster B, Bryan WW, Barohn RJ. Myasthenia gravis 
   activities of daily living profile. Neurology. 1999;52(7):1487-9. 
   doi: 10.1212/wnl.52.7.1487.
2. Muppidi S, Wolfe GI, Conaway M, Burns TM; MG Composite and MG-QOL15 Study Group. 
   MG-ADL: still a relevant outcome measure. Muscle Nerve. 2011;44(5):727-31. 
   doi: 10.1002/mus.22140.
3. Burns TM, Conaway M, Sanders DB; MG Composite and MG-QOL15 Study Group. The MG 
   Composite: A valid and reliable outcome measure for myasthenia gravis. Neurology. 
   2010;74(18):1434-40. doi: 10.1212/WNL.0b013e3181dc1b1e.

The MG-ADL scale is an 8-item patient-reported outcome measure specifically designed 
to assess functional status and disease severity in patients with myasthenia gravis. 
It evaluates common symptoms across bulbar, respiratory, gross motor, and ocular domains 
that significantly impact daily living activities.
"""

from pydantic import BaseModel, Field
from typing import Literal


class MgAdlRequest(BaseModel):
    """
    Request model for Myasthenia Gravis Activities of Daily Living (MG-ADL) Scale
    
    The MG-ADL scale is a well-validated, patient-reported outcome measure that 
    comprehensively assesses functional impairment in myasthenia gravis across 
    eight domains that commonly affect daily living activities. This scale is 
    based on patient recall of symptoms during the prior week.
    
    Scoring System:
    Each of the 8 items is scored from 0 (normal function) to 3 (most severe 
    impairment), providing a total score range of 0-24 points. Higher scores 
    indicate greater functional impairment and disease severity.
    
    Clinical Significance:
    - A 2-point reduction in total score represents clinically meaningful improvement
    - Individual item scores can be clinically significant even when total score appears low
    - Correlates well with other MG severity measures (QMG score r=0.58, MG Composite r=0.85)
    - Used as both primary and secondary endpoints in clinical trials
    
    Domain Categories:
    
    Bulbar Functions (Items 1-3):
    Assess muscles innervated by cranial nerves affecting speech, swallowing, and chewing.
    These symptoms are particularly distressing and can significantly impact nutrition,
    communication, and quality of life.
    
    Respiratory Function (Item 4):
    Evaluates respiratory muscle weakness, which can be life-threatening and requires
    careful monitoring. Respiratory involvement may indicate disease exacerbation
    or myasthenic crisis.
    
    Gross Motor Functions (Items 5-6):
    Assess proximal muscle strength affecting arm elevation and leg function.
    These activities are essential for independence in personal care and mobility.
    
    Ocular Functions (Items 7-8):
    Evaluate extraocular muscle weakness causing ptosis and diplopia, which are
    often the presenting symptoms of myasthenia gravis and significantly impact
    visual function and quality of life.
    
    Clinical Applications:
    - Routine clinical monitoring of disease severity and treatment response
    - Clinical trial endpoints for assessing therapeutic efficacy
    - Documentation of functional status for disability assessments
    - Treatment decision-making and therapeutic goal setting
    - Patient education and shared decision-making
    
    Administration Guidelines:
    - Patient completes based on symptoms experienced in the prior week
    - Takes less than 10 minutes to complete
    - No special training required for administration
    - Can be used in clinic visits, telemedicine, or patient self-assessment
    
    References (Vancouver style):
    1. Wolfe GI, Herbelin L, Nations SP, Foster B, Bryan WW, Barohn RJ. Myasthenia gravis 
    activities of daily living profile. Neurology. 1999;52(7):1487-9. 
    doi: 10.1212/wnl.52.7.1487.
    2. Muppidi S, Wolfe GI, Conaway M, Burns TM; MG Composite and MG-QOL15 Study Group. 
    MG-ADL: still a relevant outcome measure. Muscle Nerve. 2011;44(5):727-31. 
    doi: 10.1002/mus.22140.
    3. Burns TM, Conaway M, Sanders DB; MG Composite and MG-QOL15 Study Group. The MG 
    Composite: A valid and reliable outcome measure for myasthenia gravis. Neurology. 
    2010;74(18):1434-40. doi: 10.1212/WNL.0b013e3181dc1b1e.
    """
    
    talking: Literal[0, 1, 2, 3] = Field(
        ...,
        description="Speech difficulty due to vocal cord and oral muscle weakness. 0=Normal speech, 1=Intermittent slurring or nasal speech, 2=Constant slurring or nasal speech but understandable, 3=Difficult to understand speech",
        example=1
    )
    
    chewing: Literal[0, 1, 2, 3] = Field(
        ...,
        description="Masticatory muscle weakness affecting food intake. 0=Normal chewing, 1=Fatigue with solid food, 2=Fatigue with soft food, 3=Gastric tube required",
        example=0
    )
    
    swallowing: Literal[0, 1, 2, 3] = Field(
        ...,
        description="Pharyngeal and esophageal muscle weakness affecting deglutition. 0=Normal swallowing, 1=Rare episode of choking, 2=Frequent choking necessitating dietary changes, 3=Gastric tube required",
        example=1
    )
    
    breathing: Literal[0, 1, 2, 3] = Field(
        ...,
        description="Respiratory muscle weakness affecting ventilation. 0=Normal breathing, 1=Shortness of breath with exertion, 2=Shortness of breath at rest, 3=Ventilator dependency",
        example=0
    )
    
    brushing_teeth_combing_hair: Literal[0, 1, 2, 3] = Field(
        ...,
        description="Proximal arm muscle strength for elevated arm activities and personal care. 0=Normal function, 1=Fatigue after prolonged activity, 2=Fatigue after brief activity, 3=Cannot perform activity",
        example=2
    )
    
    rising_from_chair: Literal[0, 1, 2, 3] = Field(
        ...,
        description="Proximal leg muscle strength for mobility and transfers. 0=Normal function, 1=Mild difficulty, 2=Moderate difficulty requiring assistance, 3=Severe difficulty, cannot rise without help",
        example=1
    )
    
    eyelid_droop: Literal[0, 1, 2, 3] = Field(
        ...,
        description="Ptosis severity due to levator palpebrae muscle weakness. 0=No ptosis, 1=Mild ptosis not affecting vision, 2=Moderate ptosis slightly affecting vision, 3=Severe ptosis completely affecting vision",
        example=2
    )
    
    double_vision: Literal[0, 1, 2, 3] = Field(
        ...,
        description="Diplopia frequency due to extraocular muscle weakness. 0=No double vision, 1=Occasional double vision, 2=Double vision relieved by patching one eye, 3=Constant double vision",
        example=1
    )
    
    class Config:
        schema_extra = {
            "example": {
                "talking": 1,
                "chewing": 0,
                "swallowing": 1,
                "breathing": 0,
                "brushing_teeth_combing_hair": 2,
                "rising_from_chair": 1,
                "eyelid_droop": 2,
                "double_vision": 1
            }
        }


class MgAdlResponse(BaseModel):
    """
    Response model for Myasthenia Gravis Activities of Daily Living (MG-ADL) Scale
    
    The MG-ADL scale provides comprehensive assessment of functional impairment 
    in myasthenia gravis, enabling precise monitoring of disease severity, 
    treatment response, and impact on daily living activities.
    
    Score Interpretation and Clinical Management:
    
    Minimal Impairment (0-2 points) - Excellent Functional Status:
    - Normal or near-normal daily activities with little impact on quality of life
    - Continue current treatment regimen if stable
    - Routine monitoring every 3-6 months
    - Focus on medication compliance and symptom awareness
    - Excellent prognosis with minimal disease burden
    
    Mild Impairment (3-6 points) - Good Functional Status:
    - Some limitation in daily activities requiring minor adjustments
    - Generally maintains independence with good quality of life
    - Consider treatment optimization if symptoms are progressive
    - Monitor every 2-4 months for stability and treatment response
    - Adjust anticholinesterase dosing, consider immunosuppressive therapy
    - Physical therapy consultation may be beneficial
    
    Moderate Impairment (7-12 points) - Noticeable Limitations:
    - Significant impact on daily activities requiring some assistance
    - Active treatment optimization needed with multidisciplinary approach
    - Immunosuppressive therapy recommended if not already implemented
    - Close monitoring every 1-2 months with comprehensive assessments
    - Consider corticosteroids, azathioprine, or mycophenolate mofetil
    - Occupational therapy and rehabilitation services recommended
    
    Severe Impairment (13-18 points) - Significant Disability:
    - Major limitations requiring assistance for many daily activities
    - Aggressive immunosuppressive therapy and rescue treatments needed
    - Intensive monitoring every 2-4 weeks with crisis vigilance
    - High-dose corticosteroids, plasma exchange, or IVIG consideration
    - Thymectomy evaluation if appropriate candidate
    - Multidisciplinary care including respiratory monitoring and nutrition support
    
    Very Severe Impairment (19-24 points) - Critical Status:
    - Dependency for most activities with potential life-threatening complications
    - Emergency evaluation for myasthenic crisis with immediate intervention
    - Intensive care monitoring with respiratory and nutritional support
    - Mechanical ventilation consideration if respiratory compromise
    - Plasma exchange or IVIG with high-dose immunosuppression
    - Comprehensive critical care with neurology, pulmonology, and nutrition teams
    
    Treatment Response Monitoring:
    - Clinically meaningful improvement defined as ≥2-point reduction in total score
    - Individual item improvement may be significant even with stable total score
    - Regular reassessment recommended to guide treatment adjustments
    - Document changes in specific domains to target therapeutic interventions
    
    Quality of Life Considerations:
    - Strong correlation with MG-QOL15 (r=0.76) for quality of life assessment
    - Bulbar and respiratory symptoms particularly impact quality of life
    - Early intervention can prevent progression to more severe impairment
    - Patient education about symptom recognition and crisis prevention essential
    
    Clinical Trial Applications:
    - Primary or secondary endpoint in therapeutic efficacy studies
    - Minimal clinically important difference established at 2 points
    - Correlates with physician global assessment and other objective measures
    - Suitable for regulatory submissions and drug approval studies
    
    Reference: Wolfe GI, et al. Neurology. 1999;52(7):1487-9.
    """
    
    result: int = Field(
        ...,
        description="Total MG-ADL score (range 0-24 points)",
        example=8
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Detailed clinical interpretation with functional assessment and comprehensive management recommendations",
        example="MODERATE FUNCTIONAL IMPAIRMENT (MG-ADL Score: 8): Noticeable limitations in daily activities requiring some assistance and therapeutic intervention. MANAGEMENT: Active treatment optimization needed. Consider immunosuppressive therapy if not already implemented. TREATMENT: Evaluate for steroid therapy, immunosuppressants (azathioprine, mycophenolate), or other disease-modifying treatments. MONITORING: Close follow-up every 1-2 months. Assess for treatment response and side effects. SUPPORT: May benefit from physical therapy and occupational therapy consultation."
    )
    
    stage: str = Field(
        ...,
        description="Functional impairment severity category",
        example="Moderate"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the functional impairment level",
        example="Moderate functional impairment"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 8,
                "unit": "points",
                "interpretation": "MODERATE FUNCTIONAL IMPAIRMENT (MG-ADL Score: 8): Noticeable limitations in daily activities requiring some assistance and therapeutic intervention. MANAGEMENT: Active treatment optimization needed. Consider immunosuppressive therapy if not already implemented. TREATMENT: Evaluate for steroid therapy, immunosuppressants (azathioprine, mycophenolate), or other disease-modifying treatments. MONITORING: Close follow-up every 1-2 months. Assess for treatment response and side effects. SUPPORT: May benefit from physical therapy and occupational therapy consultation.",
                "stage": "Moderate",
                "stage_description": "Moderate functional impairment"
            }
        }