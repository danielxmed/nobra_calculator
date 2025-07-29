"""
BODE Index for COPD Survival Models

Request and response models for BODE Index calculation in COPD patients.

References (Vancouver style):
1. Celli BR, Cote CG, Marin JM, et al. The body-mass index, airflow obstruction, dyspnea, 
   and exercise capacity index in chronic obstructive pulmonary disease. N Engl J Med. 2004 Mar 4;350(10):1005-12. 
   doi: 10.1056/NEJMoa021322.
2. Ong KC, Earnest A, Lu SJ. A multidimensional grading system (BODE index) as predictor 
   of hospitalization for COPD. Chest. 2005 Dec;128(6):3810-6. doi: 10.1378/chest.128.6.3810.
3. Cote CG, Celli BR. Pulmonary rehabilitation and the BODE index in COPD. Eur Respir J. 2005 Oct;26(4):630-6. 
   doi: 10.1183/09031936.05.00045505.
4. Puhan MA, Garcia-Aymerich J, Frey M, et al. Expansion of the prognostic assessment of patients with chronic 
   obstructive pulmonary disease: the updated BODE index and the ADO index. Lancet. 2009 Aug 29;374(9691):704-11. 
   doi: 10.1016/S0140-6736(09)61301-5.

The BODE Index is a multidimensional grading system that predicts survival in COPD patients 
more accurately than FEV1 alone. The index incorporates four key components: Body-mass index (B), 
airflow Obstruction measured by FEV1 (O), Dyspnea assessed by the modified Medical Research Council 
scale (D), and Exercise capacity measured by 6-minute walk distance (E).

This composite score ranges from 0-10 points and stratifies patients into quartiles with 
distinct survival patterns, providing valuable prognostic information for clinical decision-making 
and patient counseling in stable COPD patients.
"""

from pydantic import BaseModel, Field
from typing import Literal


class BodeIndexCopdRequest(BaseModel):
    """
    Request model for BODE Index for COPD Survival
    
    The BODE Index is a validated multidimensional grading system that predicts mortality 
    in patients with Chronic Obstructive Pulmonary Disease (COPD). This comprehensive 
    assessment tool incorporates four key clinical domains that reflect different aspects 
    of COPD severity and functional impact.
    
    **Four Components of BODE Index:**
    
    **1. Body-Mass Index (B):**
    The BMI component reflects the nutritional and systemic effects of COPD. Lower BMI 
    in COPD patients is associated with worse prognosis, representing the "obesity paradox" 
    where underweight status indicates more severe systemic disease impact.
    
    **Scoring:**
    - **0 points**: BMI >21 kg/m² (better prognosis)
    - **1 point**: BMI ≤21 kg/m² (worse prognosis due to muscle wasting and systemic effects)
    
    **2. Obstruction - FEV1 (O):**
    Forced Expiratory Volume in 1 second as percentage of predicted normal values based 
    on age, sex, height, and ethnicity. This measures the degree of airflow limitation, 
    the fundamental pathophysiologic abnormality in COPD.
    
    **Scoring:**
    - **0 points**: FEV1 ≥65% predicted (mild obstruction)
    - **1 point**: FEV1 50-64% predicted (moderate obstruction)
    - **2 points**: FEV1 36-49% predicted (severe obstruction)
    - **3 points**: FEV1 ≤35% predicted (very severe obstruction)
    
    **3. Dyspnea - Modified Medical Research Council Scale (D):**
    The mMRC dyspnea scale assesses functional disability due to breathlessness in 
    daily activities. It captures the patient's subjective experience of disease impact 
    on quality of life and functional capacity.
    
    **Scoring:**
    - **Grade 0 (0 points)**: "I only get breathless with strenuous exercise"
    - **Grade 1 (1 point)**: "I get short of breath when hurrying on level ground or walking up a slight hill"
    - **Grade 2 (2 points)**: "On level ground, I walk slower than people of the same age because of breathlessness, or I have to stop for breath when walking at my own pace on level ground"
    - **Grade 3 (3 points)**: "I stop for breath after walking about 100 meters or after a few minutes on level ground"
    - **Grade 4 (3 points)**: "I am too breathless to leave the house or breathless when dressing"
    
    **4. Exercise Capacity - 6-Minute Walk Distance (E):**
    The 6-minute walk test measures functional exercise capacity and reflects the 
    integrated response of pulmonary, cardiovascular, and musculoskeletal systems. 
    It correlates with activities of daily living and quality of life.
    
    **Scoring:**
    - **0 points**: ≥350 meters (good exercise capacity)
    - **1 point**: 250-349 meters (mild impairment)
    - **2 points**: 150-249 meters (moderate impairment)
    - **3 points**: ≤149 meters (severe impairment)
    
    **Clinical Applications:**
    
    **Prognostic Stratification:**
    - Quartile 1 (0-2 points): 80% 4-year survival - Low risk
    - Quartile 2 (3-4 points): 67% 4-year survival - Moderate risk
    - Quartile 3 (5-6 points): 57% 4-year survival - High risk
    - Quartile 4 (7-10 points): 18% 4-year survival - Very high risk
    
    **Treatment Planning:**
    - Guide intensity of medical management
    - Identify candidates for pulmonary rehabilitation
    - Inform decisions about oxygen therapy
    - Consider advanced interventions (lung volume reduction, transplantation)
    - Support palliative care discussions in high-risk patients
    
    **Important Limitations:**
    
    **Patient Selection:**
    - Only use in clinically stable COPD patients (not during exacerbations)
    - Requires ability to perform 6-minute walk test safely
    - Not validated in patients with significant comorbidities that limit walking
    
    **Clinical Context:**
    - Provides prognostic information but does not dictate specific treatments
    - Should be used in conjunction with clinical judgment
    - Regular reassessment recommended as disease progresses
    - Consider cultural and socioeconomic factors affecting walk test performance
    
    **Testing Requirements:**
    - FEV1 should be performed according to ATS/ERS spirometry standards
    - 6-minute walk test should follow standardized protocols (ATS guidelines)
    - BMI calculated from accurate height and weight measurements
    - mMRC scale requires patient understanding and honest self-assessment
    
    References (Vancouver style):
    1. Celli BR, Cote CG, Marin JM, et al. The body-mass index, airflow obstruction, dyspnea, 
    and exercise capacity index in chronic obstructive pulmonary disease. N Engl J Med. 2004 Mar 4;350(10):1005-12. 
    doi: 10.1056/NEJMoa021322.
    2. Ong KC, Earnest A, Lu SJ. A multidimensional grading system (BODE index) as predictor 
    of hospitalization for COPD. Chest. 2005 Dec;128(6):3810-6. doi: 10.1378/chest.128.6.3810.
    3. Cote CG, Celli BR. Pulmonary rehabilitation and the BODE index in COPD. Eur Respir J. 2005 Oct;26(4):630-6. 
    doi: 10.1183/09031936.05.00045505.
    4. Puhan MA, Garcia-Aymerich J, Frey M, et al. Expansion of the prognostic assessment of patients with chronic 
    obstructive pulmonary disease: the updated BODE index and the ADO index. Lancet. 2009 Aug 29;374(9691):704-11. 
    doi: 10.1016/S0140-6736(09)61301-5.
    """
    
    fev1_percent_predicted: float = Field(
        ...,
        ge=10,
        le=150,
        description="FEV1 as percentage of predicted normal value based on age, sex, height, and ethnicity. Should be measured according to ATS/ERS spirometry standards.",
        example=45.0
    )
    
    six_minute_walk_distance: int = Field(
        ...,
        ge=0,
        le=1000,
        description="Distance walked in meters during standardized 6-minute walk test performed according to ATS guidelines. Test should be conducted on level ground with standardized encouragement.",
        example=200
    )
    
    mmrc_dyspnea_scale: Literal[
        "grade_0_strenuous_only",
        "grade_1_walks_slower", 
        "grade_2_stops_100m",
        "grade_3_too_dyspneic"
    ] = Field(
        ...,
        description="Modified Medical Research Council Dyspnea Scale grade assessing functional disability due to breathlessness. Grade 0: dyspnea only with strenuous exercise. Grade 1: walks slower than peers due to dyspnea. Grade 2: stops for breath after walking 100m. Grade 3: too dyspneic to leave house.",
        example="grade_2_stops_100m"
    )
    
    body_mass_index: float = Field(
        ...,
        ge=10,
        le=50,
        description="Body mass index in kg/m² calculated from accurate height and weight measurements. Lower BMI indicates worse prognosis in COPD (obesity paradox).",
        example=19.5
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "fev1_percent_predicted": 45.0,
                "six_minute_walk_distance": 200,
                "mmrc_dyspnea_scale": "grade_2_stops_100m",
                "body_mass_index": 19.5
            }
        }


class BodeIndexCopdResponse(BaseModel):
    """
    Response model for BODE Index for COPD Survival
    
    Returns the calculated BODE Index score with comprehensive prognostic interpretation 
    and survival predictions based on the original validation studies.
    
    **BODE Index Quartiles and Survival:**
    
    **Quartile 1 (0-2 points): Low Risk**
    - **4-year survival**: 80%
    - **Characteristics**: Relatively preserved lung function, good exercise capacity, minimal dyspnea
    - **Management**: Continue current therapy, routine monitoring
    
    **Quartile 2 (3-4 points): Moderate Risk**
    - **4-year survival**: 67%
    - **Characteristics**: Moderate impairment across multiple domains
    - **Management**: Consider intensification of bronchodilator therapy, pulmonary rehabilitation
    
    **Quartile 3 (5-6 points): High Risk**
    - **4-year survival**: 57%
    - **Characteristics**: Significant functional impairment
    - **Management**: Optimize medical therapy, pulmonary rehabilitation, consider oxygen therapy
    
    **Quartile 4 (7-10 points): Very High Risk**
    - **4-year survival**: 18%
    - **Characteristics**: Severe disease with marked functional limitations
    - **Management**: Aggressive treatment, oxygen therapy, consider advanced interventions, palliative care planning
    
    **Clinical Interpretation:**
    The BODE Index provides more accurate prognostic information than FEV1 alone by 
    incorporating multiple dimensions of COPD severity. Higher scores indicate worse 
    prognosis and need for more intensive management approaches.
    
    Reference: Celli BR, et al. N Engl J Med. 2004;350(10):1005-12.
    """
    
    result: int = Field(
        ...,
        ge=0,
        le=10,
        description="BODE Index score ranging from 0-10 points, with higher scores indicating worse prognosis",
        example=6
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the BODE score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Comprehensive clinical interpretation including component scores, survival rate, and management recommendations",
        example="BODE Index: 6 points (FEV1: 2, 6MWD: 2, mMRC: 2, BMI: 0). 4-year survival rate: 57%. High mortality risk with 57% 4-year survival rate. Significant impairment across multiple domains requiring comprehensive management including optimization of medical therapy, pulmonary rehabilitation, and consideration of oxygen therapy. The BODE Index provides more accurate prognosis than FEV1 alone by incorporating multiple dimensions of COPD severity including lung function, exercise capacity, symptom burden, and nutritional status."
    )
    
    stage: str = Field(
        ...,
        description="BODE Index risk quartile classification",
        example="Quartile 3 (High Risk)"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the BODE Index score range",
        example="BODE Index 5-6 points"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "result": 6,
                "unit": "points",
                "interpretation": "BODE Index: 6 points (FEV1: 2, 6MWD: 2, mMRC: 2, BMI: 0). 4-year survival rate: 57%. High mortality risk with 57% 4-year survival rate. Significant impairment across multiple domains requiring comprehensive management including optimization of medical therapy, pulmonary rehabilitation, and consideration of oxygen therapy. The BODE Index provides more accurate prognosis than FEV1 alone by incorporating multiple dimensions of COPD severity including lung function, exercise capacity, symptom burden, and nutritional status.",
                "stage": "Quartile 3 (High Risk)",
                "stage_description": "BODE Index 5-6 points"
            }
        }