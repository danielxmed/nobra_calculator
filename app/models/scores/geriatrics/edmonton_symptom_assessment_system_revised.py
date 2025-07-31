"""
Edmonton Symptom Assessment System-revised (ESAS-r) Models

Request and response models for ESAS-r palliative care symptom assessment.

References (Vancouver style):
1. Watanabe S, Nekolaichuk C, Beaumont C, Johnson L, Myers J, Strasser F. A multicenter study 
   comparing two numerical versions of the Edmonton Symptom Assessment System in palliative 
   care patients. J Pain Symptom Manage. 2011;41(2):456-68. doi: 10.1016/j.jpainsymman.2010.04.020.
2. Hui D, Bruera E. The Edmonton Symptom Assessment System 25 years later: Past, present, and 
   future developments. J Pain Symptom Manage. 2017;53(3):630-643. doi: 10.1016/j.jpainsymman.2016.10.370.
3. Bruera E, Kuehn N, Miller MJ, Selmser P, Macmillan K. The Edmonton Symptom Assessment System 
   (ESAS): a simple method for the assessment of palliative care patients. J Palliat Care. 1991;7(2):6-9.
4. Chang VT, Hwang SS, Feuerman M. Validation of the Edmonton Symptom Assessment Scale. Cancer. 
   2000;88(9):2164-71. doi: 10.1002/(sici)1097-0142(20000501)88:9<2164::aid-cncr24>3.0.co;2-5.

The Edmonton Symptom Assessment System-revised (ESAS-r) is a validated 9-item self-report 
symptom intensity tool designed for palliative care patients. It represents an improved 
version of the original ESAS with enhanced clarity and definitions for better patient 
understanding and clinical utility.
"""

from pydantic import BaseModel, Field


class EdmontonSymptomAssessmentSystemRevisedRequest(BaseModel):
    """
    Request model for Edmonton Symptom Assessment System-revised (ESAS-r)
    
    The ESAS-r assesses nine common symptoms experienced by palliative care patients using 
    an 11-point numeric rating scale (0-10) for each symptom. The revised version provides 
    improved clarity and specific definitions for potentially confusing items, making it 
    easier for patients to understand and complete.
    
    Clinical Context and Assessment Framework:
    
    The ESAS-r is designed for routine symptom screening and longitudinal monitoring in 
    patients receiving palliative care. It has been psychometrically validated and 
    translated into over 20 languages, making it a globally recognized standard for 
    symptom assessment in palliative care settings.
    
    Key Improvements in ESAS-r:
    - Provides specific definitions for potentially confusing symptoms
    - Specifies the time frame as "right now" for all assessments
    - Reorganizes symptoms: physical symptoms first, psychosocial second, wellbeing last
    - Has been shown to be significantly easier to understand than the original ESAS
    - Preferred by patients compared to the original version
    
    Assessment Domains:
    
    Physical Symptoms (Items 1-6):
    1. Pain: Physical discomfort or suffering caused by illness or injury
    2. Tiredness: Weariness, weakness, or lack of energy (fatigue)
    3. Drowsiness: Feeling sleepy or having difficulty staying awake
    4. Nausea: Feeling sick to your stomach or queasy
    5. Lack of Appetite: Not feeling like eating or decreased interest in food
    6. Shortness of Breath: Difficulty breathing or feeling breathless
    
    Psychosocial Symptoms (Items 7-8):
    7. Depression: Feeling sad, blue, or unhappy
    8. Anxiety: Feeling nervous, worried, or fearful
    
    Overall Assessment (Item 9):
    9. Wellbeing: How you feel overall (global assessment)
    
    Scoring Instructions:
    Each symptom is rated on an 11-point numeric rating scale:
    - 0 = No symptom (best possible state)
    - 10 = Worst possible symptom (worst possible state)
    - Patients rate how they feel "right now" at the time of assessment
    
    Clinical Significance Thresholds:
    - Individual symptom scores ≥4 are often considered clinically significant
    - These symptoms typically warrant targeted intervention
    - Scores ≥7 generally indicate severe symptoms requiring urgent attention
    
    Assessment Guidelines:
    - Can be self-administered by patients or completed with assistance
    - Takes approximately 2-5 minutes to complete
    - Should be used for regular monitoring (daily, weekly, or as clinically indicated)
    - Ideal for tracking symptom changes over time and treatment response
    
    Clinical Applications:
    - Routine symptom screening in palliative care settings
    - Monitoring treatment effectiveness and symptom progression
    - Communication tool between patients and healthcare teams
    - Quality improvement initiatives in palliative care programs
    - Research applications in symptom management studies
    
    Target Patient Populations:
    - Advanced cancer patients receiving palliative care
    - Patients with life-limiting illnesses
    - Individuals in hospice care settings
    - Patients in oncology, nephrology, and other specialty clinics
    - Any patient receiving symptom-focused care
    
    Implementation Considerations:
    - Regular staff training on administration and interpretation
    - Integration with electronic health record systems
    - Development of standardized protocols for responding to high scores
    - Patient education on the purpose and importance of symptom reporting
    - Cultural sensitivity in implementation across diverse populations
    
    Quality Indicators:
    - Completion rates and patient compliance
    - Clinician response to high symptom scores
    - Time trends in symptom burden
    - Correlation with other quality of life measures
    - Patient satisfaction with symptom management
    
    References (Vancouver style):
    1. Watanabe S, Nekolaichuk C, Beaumont C, Johnson L, Myers J, Strasser F. A multicenter study 
       comparing two numerical versions of the Edmonton Symptom Assessment System in palliative 
       care patients. J Pain Symptom Manage. 2011;41(2):456-68.
    2. Hui D, Bruera E. The Edmonton Symptom Assessment System 25 years later: Past, present, and 
       future developments. J Pain Symptom Manage. 2017;53(3):630-643.
    3. Bruera E, Kuehn N, Miller MJ, Selmser P, Macmillan K. The Edmonton Symptom Assessment System 
       (ESAS): a simple method for the assessment of palliative care patients. J Palliat Care. 1991;7(2):6-9.
    """
    
    pain: int = Field(
        ...,
        ge=0, le=10,
        description="Pain intensity right now (0 = no pain, 10 = worst possible pain)",
        example=3
    )
    
    tiredness: int = Field(
        ...,
        ge=0, le=10,
        description="Tiredness (weariness, weakness, or lack of energy) right now (0 = no tiredness, 10 = worst possible tiredness)",
        example=6
    )
    
    drowsiness: int = Field(
        ...,
        ge=0, le=10,
        description="Drowsiness (feeling sleepy) right now (0 = no drowsiness, 10 = worst possible drowsiness)",
        example=4
    )
    
    nausea: int = Field(
        ...,
        ge=0, le=10,
        description="Nausea (feeling sick to your stomach) right now (0 = no nausea, 10 = worst possible nausea)",
        example=2
    )
    
    lack_of_appetite: int = Field(
        ...,
        ge=0, le=10,
        description="Lack of appetite (not feeling like eating) right now (0 = no lack of appetite, 10 = worst possible lack of appetite)",
        example=5
    )
    
    shortness_of_breath: int = Field(
        ...,
        ge=0, le=10,
        description="Shortness of breath (difficulty breathing) right now (0 = no shortness of breath, 10 = worst possible shortness of breath)",
        example=3
    )
    
    depression: int = Field(
        ...,
        ge=0, le=10,
        description="Depression (feeling sad, blue, or unhappy) right now (0 = no depression, 10 = worst possible depression)",
        example=4
    )
    
    anxiety: int = Field(
        ...,
        ge=0, le=10,
        description="Anxiety (feeling nervous, worried, or fearful) right now (0 = no anxiety, 10 = worst possible anxiety)",
        example=5
    )
    
    wellbeing: int = Field(
        ...,
        ge=0, le=10,
        description="Wellbeing (how you feel overall) right now (0 = best wellbeing, 10 = worst possible wellbeing)",
        example=6
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "pain": 3,
                "tiredness": 6,
                "drowsiness": 4,
                "nausea": 2,
                "lack_of_appetite": 5,
                "shortness_of_breath": 3,
                "depression": 4,
                "anxiety": 5,
                "wellbeing": 6
            }
        }


class EdmontonSymptomAssessmentSystemRevisedResponse(BaseModel):
    """
    Response model for Edmonton Symptom Assessment System-revised (ESAS-r)
    
    The ESAS-r total score provides a comprehensive assessment of overall symptom burden 
    in palliative care patients. Individual symptom scores and the total score guide 
    clinical decision-making and treatment planning.
    
    Score Interpretation and Clinical Action Guidelines:
    
    Total Score Ranges and Symptom Burden Categories:
    
    Mild Symptom Burden (0-17 points):
    - Clinical Significance: Low overall symptom burden with manageable symptoms
    - Management Approach:
      * Continue current symptom management strategies
      * Regular monitoring with standard assessment intervals
      * Patient education on symptom reporting and self-management
      * Maintain current palliative care plan with routine adjustments
    - Follow-up: Standard monitoring schedule (weekly or bi-weekly)
    - Quality of Life: Generally maintained with minimal impact from symptoms
    
    Moderate Symptom Burden (18-35 points):
    - Clinical Significance: Moderate symptom burden affecting quality of life and function
    - Management Approach:
      * Intensify symptom management interventions
      * Review and optimize current medications and treatments
      * Consider additional palliative care services or consultation
      * More frequent symptom assessments and monitoring
      * Assess need for psychosocial support services
    - Follow-up: Increased monitoring frequency (2-3 times weekly)
    - Quality of Life: Noticeable impact requiring active intervention
    
    Severe Symptom Burden (36-90 points):
    - Clinical Significance: High symptom burden severely impacting quality of life
    - Management Approach:
      * Urgent comprehensive symptom management review
      * Specialist palliative care consultation if not already involved
      * Aggressive symptom control measures
      * Daily or more frequent monitoring and assessment
      * Consider hospitalization or intensive palliative care services
      * Comprehensive psychosocial support for patient and family
    - Follow-up: Daily monitoring with potential for continuous assessment
    - Quality of Life: Severely compromised requiring immediate intervention
    
    Individual Symptom Significance:
    
    Clinically Significant Symptoms (≥4/10):
    - Require targeted intervention and specific treatment strategies
    - Should be addressed in treatment planning and care coordination
    - May indicate need for specialist consultation or medication adjustment
    - Warrant more frequent monitoring and follow-up
    
    Severe Individual Symptoms (≥7/10):
    - Require urgent attention and immediate intervention
    - May necessitate emergency or urgent care consultation
    - Significantly impact patient quality of life and functioning
    - Often require intensive symptom management approaches
    
    Clinical Implementation and Monitoring:
    
    Longitudinal Monitoring:
    - Use ESAS-r scores to track symptom trends over time
    - Effective treatment should show downward trends in scores
    - Identify patterns in symptom fluctuation and progression
    - Monitor treatment response and medication effectiveness
    
    Communication and Care Coordination:
    - Share results with entire healthcare team
    - Use scores to guide multidisciplinary care planning
    - Communicate findings with patient and family
    - Document interventions and responses to symptom management
    
    Quality Improvement Applications:
    - Benchmark symptom management effectiveness
    - Identify areas for improvement in palliative care services
    - Monitor program outcomes and patient satisfaction
    - Support evidence-based practice improvements
    
    Treatment Response Indicators:
    - Decreasing total ESAS-r scores over time
    - Reduction in number of clinically significant symptoms
    - Improved individual symptom scores with targeted interventions
    - Patient-reported improvement in overall wellbeing
    
    Red Flag Indicators Requiring Immediate Attention:
    - Sudden increase in total score (>10 point increase)
    - New symptoms scoring ≥7/10
    - Multiple symptoms scoring ≥4/10 simultaneously
    - Wellbeing score ≥8/10 (severe distress)
    - Pain score ≥8/10 (severe pain requiring urgent management)
    
    Family and Caregiver Considerations:
    - Involve family in understanding symptom assessment results
    - Provide education on symptom recognition and reporting
    - Support family coping with patient symptom burden
    - Consider caregiver burden and support needs
    
    Documentation and Legal Considerations:
    - Document all ESAS-r scores in patient medical record
    - Record interventions implemented in response to scores
    - Track changes in symptom burden over time
    - Use for quality assurance and performance improvement
    
    Cultural and Individual Considerations:
    - Consider cultural differences in symptom expression and reporting
    - Account for individual patient communication styles and preferences
    - Adapt assessment approach for cognitive or communication limitations
    - Respect patient autonomy in symptom management decisions
    
    Reference: Watanabe S, et al. J Pain Symptom Manage. 2011;41(2):456-68.
    """
    
    result: int = Field(
        ...,
        description="ESAS-r total score calculated as sum of all nine symptom scores (range: 0-90 points)",
        example=38
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the ESAS-r total score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation and management recommendations based on total symptom burden and individual symptom significance",
        example="Severe overall symptom burden significantly impacting quality of life. Urgent review and optimization of symptom management required. Consider specialist palliative care consultation, medication adjustments, and comprehensive care plan revision. Daily or more frequent monitoring recommended. Clinically significant symptoms (≥4/10) requiring targeted intervention: Tiredness (6/10), Lack of Appetite (5/10), Depression (4/10), Anxiety (5/10), Wellbeing (6/10). Use ESAS-r for longitudinal monitoring to track symptom changes and treatment response over time."
    )
    
    stage: str = Field(
        ...,
        description="Symptom burden category (Mild, Moderate, Severe)",
        example="Severe"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the total symptom burden level",
        example="Severe total symptom burden"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "result": 38,
                "unit": "points",
                "interpretation": "Severe overall symptom burden significantly impacting quality of life. Urgent review and optimization of symptom management required. Consider specialist palliative care consultation, medication adjustments, and comprehensive care plan revision. Daily or more frequent monitoring recommended. Clinically significant symptoms (≥4/10) requiring targeted intervention: Tiredness (6/10), Lack of Appetite (5/10), Depression (4/10), Anxiety (5/10), Wellbeing (6/10). Use ESAS-r for longitudinal monitoring to track symptom changes and treatment response over time.",
                "stage": "Severe",
                "stage_description": "Severe total symptom burden"
            }
        }