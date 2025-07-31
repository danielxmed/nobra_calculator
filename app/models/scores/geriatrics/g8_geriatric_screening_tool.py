"""
G8 Geriatric Screening Tool Models

Request and response models for G8 Geriatric Screening Tool.

References (Vancouver style):
1. Bellera CA, Rainfray M, Mathoulin-Pélissier S, et al. Screening older cancer patients: 
   first evaluation of the G-8 geriatric screening tool. Ann Oncol. 2012;23(8):2166-72. 
   doi: 10.1093/annonc/mdr587.
2. Soubeyran P, Bellera C, Goyard J, et al. Screening for vulnerability in older cancer 
   patients: the ONCODAGE Prospective Multicenter Cohort Study. PLoS One. 
   2014;9(12):e115060. doi: 10.1371/journal.pone.0115060.
3. Kenis C, Decoster L, Van Puyvelde K, et al. Performance of two geriatric screening 
   tools in older patients with cancer. J Clin Oncol. 2014;32(1):19-26. 
   doi: 10.1200/JCO.2013.51.1345.

The G8 Geriatric Screening Tool is a validated instrument that identifies older cancer 
patients who could benefit from comprehensive geriatric assessment (CGA). The tool 
incorporates 7 items from the Mini Nutritional Assessment (MNA) plus patient age to 
create an 8-item screening questionnaire.

Key Features:
- Quick administration (4-10 minutes) suitable for busy oncology settings
- Validated in cancer patients aged ≥65 years
- Score range: 0-17 points (higher scores indicate better health status)
- Cut-off: ≤14 points indicates need for comprehensive geriatric assessment
- Evaluates multiple geriatric domains: nutrition, mobility, cognition, functionality

Clinical Applications:
- Routine screening of elderly cancer patients
- Treatment planning and supportive care decisions
- Identification of patients requiring geriatric intervention
- Resource allocation for comprehensive geriatric assessment
- Prognostic assessment for treatment tolerance

Scoring System:
1. Age: >85 years (0 pts), 80-85 years (1 pt), <80 years (2 pts)
2. Food intake decline: Severe (0 pts), Moderate (1 pt), None (2 pts)
3. Weight loss (3 months): >3kg (0 pts), Unknown (1 pt), 1-3kg (2 pts), None (3 pts)
4. Mobility: Bed/chair bound (0 pts), Out of bed only (1 pt), Goes out (2 pts)
5. Neuropsychology: Severe dementia/depression (0 pts), Mild dementia (1 pt), None (2 pts)
6. BMI: <19 (0 pts), 19-<21 (1 pt), 21-<23 (2 pts), ≥23 (3 pts)
7. Medications: >3 drugs/day (0 pts), ≤3 drugs/day (1 pt)
8. Health vs peers: Worse (0 pts), Unknown (0.5 pts), Same (1 pt), Better (2 pts)

Interpretation:
- ≤14 points: High risk for geriatric impairment → Comprehensive geriatric assessment recommended
- >14 points: Low risk for geriatric impairment → Standard care with monitoring

Clinical Considerations:
- Should be performed before starting cancer treatment when possible
- Results should guide treatment planning and supportive care interventions
- Reassessment may be warranted if clinical status changes during treatment
- Not a substitute for comprehensive geriatric assessment when indicated
- Consider cultural and social factors that may influence responses
"""

from pydantic import BaseModel, Field
from typing import Literal


class G8GeriatricScreeningToolRequest(BaseModel):
    """
    Request model for G8 Geriatric Screening Tool
    
    The G8 is an 8-item screening questionnaire that evaluates geriatric domains to identify 
    older cancer patients who would benefit from comprehensive geriatric assessment (CGA). 
    It incorporates 7 items from the Mini Nutritional Assessment (MNA) plus patient age.
    
    **ADMINISTRATION INSTRUCTIONS**:
    
    This screening tool should be administered to cancer patients aged ≥65 years as part 
    of routine oncological care. It can be completed by nursing staff, clinical research 
    associates, or physicians in approximately 4-10 minutes.
    
    **G8 SCREENING QUESTIONNAIRE**:
    
    1. **Patient Age**
       - >85 years: 0 points
       - 80-85 years: 1 point  
       - <80 years: 2 points
    
    2. **Food Intake Decline Over Past 3 Months**
       - Severe decrease in food intake: 0 points
       - Moderate decrease in food intake: 1 point
       - No decrease in food intake: 2 points
    
    3. **Weight Loss During Last 3 Months**
       - Weight loss >3 kg (>6.6 lb): 0 points
       - Does not know/cannot determine: 1 point
       - Weight loss 1-3 kg (2.2-6.6 lb): 2 points
       - No weight loss: 3 points
    
    4. **Mobility Status**
       - Bed or chair bound: 0 points
       - Able to get out of bed/chair but does not go outside: 1 point
       - Goes out regularly: 2 points
    
    5. **Neuropsychological Conditions**
       - Severe dementia or depression: 0 points
       - Mild dementia: 1 point
       - No psychological conditions: 2 points
    
    6. **Body Mass Index (BMI)**
       - BMI <19 kg/m²: 0 points
       - BMI 19 to <21 kg/m²: 1 point
       - BMI 21 to <23 kg/m²: 2 points
       - BMI ≥23 kg/m²: 3 points
    
    7. **Multiple Medications**
       - Takes more than 3 prescription drugs per day: 0 points
       - Takes 3 or fewer prescription drugs per day: 1 point
    
    8. **Health Status Compared to Peers**
       - Not as good as peers of same age: 0 points
       - Does not know: 0.5 points
       - As good as peers of same age: 1 point
       - Better than peers of same age: 2 points
    
    **SCORING AND INTERPRETATION**:
    
    **Total Score Range**: 0-17 points (higher scores indicate better health status)
    
    **Clinical Decision Threshold**:
    - **≤14 points**: High risk for geriatric impairment → Comprehensive geriatric assessment recommended
    - **>14 points**: Low risk for geriatric impairment → Standard oncological care with monitoring
    
    **COMPREHENSIVE GERIATRIC ASSESSMENT (CGA) DOMAINS**:
    
    When G8 score ≤14, the following domains should be evaluated in CGA:
    - **Functional Status**: Activities of daily living (ADL), instrumental ADL (IADL)
    - **Comorbidities**: Burden of concurrent medical conditions
    - **Cognition**: Memory, executive function, orientation
    - **Mental Health**: Depression, anxiety, psychological distress
    - **Social Support**: Family support, social network, caregiver availability
    - **Nutrition**: Nutritional status, appetite, dietary intake
    - **Geriatric Syndromes**: Falls, frailty, polypharmacy, sensory impairments
    
    **CLINICAL APPLICATIONS**:
    - Routine screening in elderly cancer patients (≥65 years)
    - Treatment planning and modification decisions
    - Supportive care intervention planning
    - Resource allocation for geriatric services
    - Prognosis and treatment tolerance assessment
    
    References (Vancouver style):
    1. Bellera CA, Rainfray M, Mathoulin-Pélissier S, et al. Screening older cancer patients: 
       first evaluation of the G-8 geriatric screening tool. Ann Oncol. 2012;23(8):2166-72.
    2. Soubeyran P, Bellera C, Goyard J, et al. Screening for vulnerability in older cancer 
       patients: the ONCODAGE Prospective Multicenter Cohort Study. PLoS One. 2014;9(12):e115060.
    3. Kenis C, Decoster L, Van Puyvelde K, et al. Performance of two geriatric screening 
       tools in older patients with cancer. J Clin Oncol. 2014;32(1):19-26.
    """
    
    age_category: Literal["over_85", "80_to_85", "under_80"] = Field(
        ...,
        description="Patient age category. >85 years = 0 pts, 80-85 years = 1 pt, <80 years = 2 pts",
        example="under_80"
    )
    
    food_intake_decline: Literal["severe_decrease", "moderate_decrease", "no_decrease"] = Field(
        ...,
        description="Food intake decline over past 3 months. Severe decrease = 0 pts, Moderate decrease = 1 pt, No decrease = 2 pts",
        example="no_decrease"
    )
    
    weight_loss: Literal["over_3kg", "does_not_know", "1_to_3kg", "no_weight_loss"] = Field(
        ...,
        description="Weight loss during last 3 months. >3kg = 0 pts, Does not know = 1 pt, 1-3kg = 2 pts, No weight loss = 3 pts",
        example="no_weight_loss"
    )
    
    mobility: Literal["bed_chair_bound", "out_of_bed_no_outside", "goes_out"] = Field(
        ...,
        description="Patient mobility status. Bed/chair bound = 0 pts, Out of bed but not outside = 1 pt, Goes out = 2 pts",
        example="goes_out"
    )
    
    neuropsychological_conditions: Literal["severe_dementia_depression", "mild_dementia", "no_psychological_conditions"] = Field(
        ...,
        description="Neuropsychological conditions. Severe dementia/depression = 0 pts, Mild dementia = 1 pt, No psychological conditions = 2 pts",
        example="no_psychological_conditions"
    )
    
    bmi_category: Literal["under_19", "19_to_21", "21_to_23", "23_or_over"] = Field(
        ...,
        description="Body Mass Index category. <19 kg/m² = 0 pts, 19-<21 = 1 pt, 21-<23 = 2 pts, ≥23 = 3 pts",
        example="23_or_over"
    )
    
    multiple_medications: Literal["yes", "no"] = Field(
        ...,
        description="Takes more than 3 prescription drugs per day. Yes = 0 pts, No = 1 pt",
        example="no"
    )
    
    health_status_vs_peers: Literal["not_as_good", "does_not_know", "as_good", "better"] = Field(
        ...,
        description="Self-perceived health status compared to peers of same age. Not as good = 0 pts, Does not know = 0.5 pts, As good = 1 pt, Better = 2 pts",
        example="as_good"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "age_category": "under_80",
                "food_intake_decline": "no_decrease",
                "weight_loss": "no_weight_loss",
                "mobility": "goes_out",
                "neuropsychological_conditions": "no_psychological_conditions",
                "bmi_category": "23_or_over",
                "multiple_medications": "no",
                "health_status_vs_peers": "as_good"
            }
        }


class G8GeriatricScreeningToolResponse(BaseModel):
    """
    Response model for G8 Geriatric Screening Tool
    
    The response provides the calculated G8 total score along with risk classification 
    and evidence-based clinical recommendations for geriatric assessment and management 
    in elderly cancer patients.
    
    **SCORE INTERPRETATION AND CLINICAL MANAGEMENT**:
    
    **High Risk (≤14 points)**:
    - **Clinical Significance**: High risk for geriatric impairment requiring intervention
    - **Assessment**: Comprehensive geriatric assessment (CGA) strongly recommended
    - **Timing**: CGA should be performed before initiating cancer treatment when possible
    - **CGA Domains to Evaluate**:
      - Functional status (ADL, IADL)
      - Comorbidity burden and medication review
      - Cognitive assessment (memory, executive function)
      - Mental health screening (depression, anxiety)
      - Social support and caregiver availability
      - Nutritional status and dietary assessment
      - Geriatric syndromes (falls, frailty, sensory impairments)
    - **Treatment Considerations**:
      - May require treatment modification or dose adjustment
      - Enhanced supportive care planning
      - Multidisciplinary team involvement (geriatrician, pharmacist, social worker)
      - Close monitoring during treatment
      - Consideration of palliative care consultation if appropriate
    
    **Low Risk (>14 points)**:
    - **Clinical Significance**: Low risk for significant geriatric impairment
    - **Management**: Standard oncological care with age-appropriate considerations
    - **Monitoring**: Continue routine assessment during treatment
    - **Reassessment**: Consider repeat G8 screening if clinical status changes
    - **Interventions**: Standard cancer treatment protocols with attention to:
      - Polypharmacy and drug interactions
      - Functional status monitoring
      - Treatment tolerance assessment
      - Age-related toxicity considerations
    
    **CLINICAL APPLICATIONS AND BENEFITS**:
    
    **Treatment Planning**:
    - Guides selection of appropriate cancer treatment intensity
    - Identifies patients who may benefit from modified treatment protocols
    - Informs prognosis and treatment tolerance predictions
    - Supports shared decision-making discussions
    
    **Resource Allocation**:
    - Efficiently identifies patients requiring comprehensive geriatric services
    - Prioritizes limited geriatric consultation resources
    - Guides referral patterns and care coordination
    - Supports quality improvement initiatives
    
    **Supportive Care Planning**:
    - Identifies need for enhanced supportive care interventions
    - Guides development of individualized care plans
    - Informs caregiver support and education needs
    - Supports advance care planning discussions
    
    **FOLLOW-UP AND MONITORING**:
    
    **Reassessment Indications**:
    - Significant clinical status change during treatment
    - Development of treatment-related complications
    - Functional decline or new geriatric syndromes
    - Completion of treatment and transition to survivorship care
    
    **Quality Measures**:
    - Documented G8 screening in elderly cancer patients
    - Appropriate CGA referral for high-risk patients
    - Implementation of CGA recommendations
    - Monitoring of treatment tolerance and outcomes
    
    **LIMITATIONS AND CONSIDERATIONS**:
    - Screening tool only - not a substitute for comprehensive assessment
    - Cultural and linguistic factors may influence responses
    - Requires clinical judgment in interpretation and application
    - Should be part of comprehensive oncological assessment
    - Regular validation and quality assurance recommended
    
    Reference: Bellera CA, et al. Ann Oncol. 2012;23(8):2166-72.
    """
    
    result: float = Field(
        ...,
        description="G8 total score calculated by summing all 8 item scores (range: 0-17 points)",
        ge=0,
        le=17,
        example=13.0
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the G8 score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Comprehensive clinical interpretation including risk level, clinical significance, and evidence-based management recommendations for elderly cancer patients",
        example="G8 score of 13.0 indicates high risk for geriatric impairment. A comprehensive geriatric assessment (CGA) by trained geriatric professionals is strongly recommended to evaluate functional status, comorbidities, cognition, mental health, social support, nutrition, and geriatric syndromes. This assessment will help guide appropriate cancer treatment decisions and identify opportunities for interventions to optimize patient outcomes."
    )
    
    stage: str = Field(
        ...,
        description="Risk category for geriatric impairment (High Risk, Low Risk)",
        example="High Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the risk level",
        example="Requires comprehensive geriatric assessment"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 13.0,
                "unit": "points",
                "interpretation": "G8 score of 13.0 indicates high risk for geriatric impairment. A comprehensive geriatric assessment (CGA) by trained geriatric professionals is strongly recommended to evaluate functional status, comorbidities, cognition, mental health, social support, nutrition, and geriatric syndromes. This assessment will help guide appropriate cancer treatment decisions and identify opportunities for interventions to optimize patient outcomes.",
                "stage": "High Risk",
                "stage_description": "Requires comprehensive geriatric assessment"
            }
        }