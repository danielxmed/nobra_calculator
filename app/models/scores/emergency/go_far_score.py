"""
GO-FAR (Good Outcome Following Attempted Resuscitation) Score Models

Request and response models for GO-FAR score calculation.

References (Vancouver style):
1. Ebell MH, Jang W, Shen Y, Geocadin RG. Get With the Guidelines-Resuscitation 
   Investigators. Development and validation of the Good Outcome Following Attempted 
   Resuscitation (GO-FAR) score to predict neurologically intact survival after 
   in-hospital cardiopulmonary resuscitation. JAMA Intern Med. 2013;173(20):1872-8. 
   doi: 10.1001/jamainternmed.2013.10037.
2. Piscator E, Hedberg P, Göransson K, Djarv T. Prearrest prediction of survival with 
   good neurologic recovery among in-hospital cardiac arrest patients. Resuscitation. 
   2018;128:63-69. doi: 10.1016/j.resuscitation.2018.05.006.
3. Perman SM, Stanton E, Soar J, et al. Location of in-hospital cardiac arrest in the 
   United States—variability in event rate and outcomes. J Am Heart Assoc. 
   2016;5(10):e003638. doi: 10.1161/JAHA.116.003638.

The GO-FAR (Good Outcome Following Attempted Resuscitation) score is an evidence-based 
tool that predicts survival to discharge with good neurological outcome after in-hospital 
cardiac arrest. It uses 13 pre-arrest clinical variables to stratify patients into risk 
categories, enabling healthcare providers to have informed discussions with patients and 
families about resuscitation preferences and code status decisions.

**Clinical Applications**:
1. **Shared Decision-Making**: Facilitates informed discussions about resuscitation preferences
2. **Risk Stratification**: Identifies patients unlikely to benefit from resuscitation attempts
3. **Code Status Discussions**: Provides evidence-based framework for DNAR considerations
4. **Quality Improvement**: Supports appropriate resource allocation and care planning
5. **Family Counseling**: Helps communicate realistic expectations about resuscitation outcomes

**Scoring System (13 Variables)**:
The score ranges from -15 to approximately +47 points, with higher scores indicating 
worse prognosis:

**Age Categories**:
- Under 70 years: 0 points
- 70-74 years: 2 points  
- 75-79 years: 5 points
- 80-84 years: 6 points
- 85+ years: 11 points

**Clinical Variables (Yes/No)**:
- Neurologically intact at admission: -15 points (protective factor)
- Major trauma: +10 points
- Acute stroke: +8 points
- Metastatic/hematologic cancer: +7 points
- Septicemia: +7 points
- Medical non-cardiac diagnosis: +7 points
- Hepatic insufficiency: +6 points
- Admitted from skilled nursing facility: +6 points
- Hypotension/hypoperfusion: +5 points
- Renal insufficiency/dialysis: +4 points
- Respiratory insufficiency: +4 points
- Pneumonia: +1 point

**Survival Probability Categories**:
- Above Average (Score -15 to -6): >15% probability
- Average (Score -5 to 13): 3-15% probability  
- Low (Score 14 to 23): 1-3% probability
- Very Low (Score ≥24): <1% probability

**Important Clinical Considerations**:
- Developed specifically for in-hospital cardiac arrests
- Neurologically intact survival defined as CPC (Cerebral Performance Category) score of 1
- Should complement, not replace, clinical judgment and patient/family preferences
- Variables assessed at hospital admission or current clinical status
- Designed to support shared decision-making, not mandate care decisions
- Consider cultural, spiritual, and individual factors in addition to probability estimates

The GO-FAR score provides valuable prognostic information but should always be used 
within the context of comprehensive clinical assessment and patient-centered care 
planning. It serves as a tool to facilitate meaningful conversations about goals of 
care and treatment preferences.
"""

from pydantic import BaseModel, Field
from typing import Literal


class GoFarScoreRequest(BaseModel):
    """
    Request model for GO-FAR (Good Outcome Following Attempted Resuscitation) Score
    
    The GO-FAR score uses 13 clinical variables to predict survival to discharge with 
    good neurological outcome after in-hospital cardiac arrest. Each variable is 
    assessed as present or absent at the time of hospital admission or current clinical 
    status.
    
    **Age Categories**:
    - under_70: Age <70 years (0 points)
    - 70_to_74: Age 70-74 years (2 points)
    - 75_to_79: Age 75-79 years (5 points)
    - 80_to_84: Age 80-84 years (6 points)
    - 85_or_over: Age ≥85 years (11 points)
    
    **Clinical Variables (Yes/No Response)**:
    Each clinical variable receives points only if present ("yes"):
    
    - **Neurologically Intact (-15 points if yes)**: Patient has normal neurological 
      function at admission (CPC score of 1). This is the only protective factor.
      
    - **Major Trauma (+10 points if yes)**: Major trauma as primary diagnosis or 
      significant contributing factor to current hospitalization.
      
    - **Acute Stroke (+8 points if yes)**: Acute cerebrovascular accident as primary 
      diagnosis or significant contributing factor.
      
    - **Metastatic/Hematologic Cancer (+7 points if yes)**: Active metastatic solid 
      tumor or hematologic malignancy (leukemia, lymphoma, multiple myeloma).
      
    - **Septicemia (+7 points if yes)**: Systemic infection with documented bacteremia 
      or clinical sepsis syndrome.
      
    - **Medical Non-cardiac Diagnosis (+7 points if yes)**: Medical (non-surgical, 
      non-cardiac) condition as primary reason for current hospitalization.
      
    - **Hepatic Insufficiency (+6 points if yes)**: Liver dysfunction including 
      cirrhosis, acute hepatitis, or liver failure.
      
    - **Skilled Nursing Facility (+6 points if yes)**: Patient admitted from skilled 
      nursing facility, long-term care facility, or similar institution.
      
    - **Hypotension/Hypoperfusion (+5 points if yes)**: Requiring vasopressors, 
      inotropes, or other hemodynamic support.
      
    - **Renal Insufficiency (+4 points if yes)**: Chronic kidney disease with 
      creatinine >2 mg/dL or requiring dialysis.
      
    - **Respiratory Insufficiency (+4 points if yes)**: Requiring mechanical 
      ventilation, BiPAP, or supplemental oxygen for respiratory failure.
      
    - **Pneumonia (+1 point if yes)**: Pneumonia as primary or secondary diagnosis.

    References (Vancouver style):
    1. Ebell MH, Jang W, Shen Y, Geocadin RG. Get With the Guidelines-Resuscitation 
    Investigators. Development and validation of the Good Outcome Following Attempted 
    Resuscitation (GO-FAR) score to predict neurologically intact survival after 
    in-hospital cardiopulmonary resuscitation. JAMA Intern Med. 2013;173(20):1872-8. 
    doi: 10.1001/jamainternmed.2013.10037.
    2. Piscator E, Hedberg P, Göransson K, Djarv T. Prearrest prediction of survival with 
    good neurologic recovery among in-hospital cardiac arrest patients. Resuscitation. 
    2018;128:63-69. doi: 10.1016/j.resuscitation.2018.05.006.
    """
    
    age_category: Literal["under_70", "70_to_74", "75_to_79", "80_to_84", "85_or_over"] = Field(
        ...,
        description="Patient age category. Older age increases points: under 70 (0 pts), 70-74 (2 pts), 75-79 (5 pts), 80-84 (6 pts), 85+ (11 pts)",
        example="70_to_74"
    )
    
    neurologically_intact: Literal["yes", "no"] = Field(
        ...,
        description="Patient neurologically intact at admission (CPC score of 1). This is the only protective factor, scoring -15 points if yes",
        example="yes"
    )
    
    major_trauma: Literal["yes", "no"] = Field(
        ...,
        description="Major trauma as primary diagnosis or significant contributing factor. Scores +10 points if yes",
        example="no"
    )
    
    acute_stroke: Literal["yes", "no"] = Field(
        ...,
        description="Acute stroke (cerebrovascular accident) as primary diagnosis or significant contributing factor. Scores +8 points if yes",
        example="no"
    )
    
    metastatic_hematologic_cancer: Literal["yes", "no"] = Field(
        ...,
        description="Active metastatic solid tumor or hematologic malignancy (leukemia, lymphoma, multiple myeloma). Scores +7 points if yes",
        example="no"
    )
    
    septicemia: Literal["yes", "no"] = Field(
        ...,
        description="Septicemia - systemic infection with documented bacteremia or clinical sepsis syndrome. Scores +7 points if yes",
        example="no"
    )
    
    medical_noncardiac_diagnosis: Literal["yes", "no"] = Field(
        ...,
        description="Medical non-cardiac diagnosis as primary reason for current hospitalization (excludes surgical and cardiac admissions). Scores +7 points if yes",
        example="yes"
    )
    
    hepatic_insufficiency: Literal["yes", "no"] = Field(
        ...,
        description="Hepatic insufficiency including cirrhosis, acute hepatitis, or liver failure. Scores +6 points if yes",
        example="no"
    )
    
    skilled_nursing_facility: Literal["yes", "no"] = Field(
        ...,
        description="Patient admitted from skilled nursing facility, long-term care facility, or similar institution. Scores +6 points if yes",
        example="no"
    )
    
    hypotension_hypoperfusion: Literal["yes", "no"] = Field(
        ...,
        description="Hypotension or hypoperfusion requiring vasopressors, inotropes, or other hemodynamic support. Scores +5 points if yes",
        example="no"
    )
    
    renal_insufficiency: Literal["yes", "no"] = Field(
        ...,
        description="Renal insufficiency with creatinine >2 mg/dL or requiring dialysis. Scores +4 points if yes",
        example="no"
    )
    
    respiratory_insufficiency: Literal["yes", "no"] = Field(
        ...,
        description="Respiratory insufficiency requiring mechanical ventilation, BiPAP, or supplemental oxygen for respiratory failure. Scores +4 points if yes",
        example="no"
    )
    
    pneumonia: Literal["yes", "no"] = Field(
        ...,
        description="Pneumonia as primary or secondary diagnosis. Scores +1 point if yes",
        example="no"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "age_category": "70_to_74",
                "neurologically_intact": "yes",
                "major_trauma": "no",
                "acute_stroke": "no",
                "metastatic_hematologic_cancer": "no",
                "septicemia": "no",
                "medical_noncardiac_diagnosis": "yes",
                "hepatic_insufficiency": "no",
                "skilled_nursing_facility": "no",
                "hypotension_hypoperfusion": "no",
                "renal_insufficiency": "no",
                "respiratory_insufficiency": "no",
                "pneumonia": "no"
            }
        }


class GoFarScoreResponse(BaseModel):
    """
    Response model for GO-FAR (Good Outcome Following Attempted Resuscitation) Score
    
    Provides the calculated GO-FAR score with clinical interpretation and management 
    recommendations based on survival probability categories.
    
    **Survival Probability Categories**:
    
    **Above Average Survival (-15 to -6 points, >15% probability)**:
    - Good prognosis for neurologically intact survival
    - Resuscitation generally appropriate and should be discussed
    - Consider patient values and preferences in decision-making
    - Full resuscitation measures typically warranted unless patient expressed different preferences
    
    **Average Survival (-5 to 13 points, 3-15% probability)**:
    - Intermediate prognosis for neurologically intact survival
    - Individualized decision-making recommended based on patient values and preferences
    - Discuss benefits and risks of resuscitation with patient and family
    - Consider patient's quality of life expectations and advance directives
    
    **Low Survival (14 to 23 points, 1-3% probability)**:
    - Poor prognosis for neurologically intact survival
    - Consider discussing limitations of resuscitation with patient and family
    - Focus on comfort measures and quality of life considerations
    - Explore patient's values regarding aggressive interventions
    - Consider palliative care consultation
    
    **Very Low Survival (≥24 points, <1% probability)**:
    - Very poor prognosis for neurologically intact survival
    - Strong consideration for do-not-attempt-resuscitation (DNAR) order
    - Focus on comfort care and symptom management
    - Consider palliative care consultation and transition to comfort-focused goals
    
    **Important Clinical Considerations**:
    - This score should be used as part of comprehensive clinical assessment
    - Supports shared decision-making, not mandated care decisions
    - Consider patient autonomy, cultural factors, and individual circumstances
    - Neurologically intact survival defined as CPC (Cerebral Performance Category) score of 1
    - Developed specifically for in-hospital cardiac arrest prediction
    - Should complement, not replace, clinical judgment and patient/family preferences
    
    Reference: Ebell MH, et al. JAMA Intern Med. 2013;173(20):1872-8.
    """
    
    result: int = Field(
        ...,
        description="GO-FAR score calculated from weighted clinical variables (range: -15 to approximately +47 points)",
        ge=-15,
        le=50,
        example=-6
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the GO-FAR score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Comprehensive clinical interpretation including score, survival probability category, clinical recommendations, and important considerations for shared decision-making",
        example="GO-FAR Score: -6 points. Survival probability category: Above Average Survival (>15%). Clinical recommendations: Above average probability of survival with good neurological outcome. Resuscitation is generally appropriate and should be discussed with patient and family. Consider patient values and preferences in decision-making. Full resuscitation measures are typically warranted unless patient has expressed different preferences. Important note: This score should be used as part of comprehensive clinical assessment and shared decision-making, not as the sole determinant of resuscitation status. Consider patient autonomy, cultural factors, and individual circumstances."
    )
    
    stage: str = Field(
        ...,
        description="Survival probability category (Above Average Survival, Average Survival, Low Survival, Very Low Survival)",
        example="Above Average Survival"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the prognosis category",
        example="Good prognosis"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": -6,
                "unit": "points",
                "interpretation": "GO-FAR Score: -6 points. Survival probability category: Above Average Survival (>15%). Clinical recommendations: Above average probability of survival with good neurological outcome. Resuscitation is generally appropriate and should be discussed with patient and family. Consider patient values and preferences in decision-making. Full resuscitation measures are typically warranted unless patient has expressed different preferences. Important note: This score should be used as part of comprehensive clinical assessment and shared decision-making, not as the sole determinant of resuscitation status. Consider patient autonomy, cultural factors, and individual circumstances.",
                "stage": "Above Average Survival",
                "stage_description": "Good prognosis"
            }
        }