"""
Glasgow Alcoholic Hepatitis Score (GAHS) Models

Request and response models for Glasgow Alcoholic Hepatitis Score calculation.

References (Vancouver style):
1. Forrest EH, Evans CD, Stewart S, et al. Analysis of factors predictive of mortality 
   in alcoholic hepatitis and derivation and validation of the Glasgow alcoholic hepatitis 
   score. Gut. 2005;54(8):1174-1179. doi: 10.1136/gut.2004.050781.
2. Louvet A, Naveau S, Abdelnour M, et al. The Lille model: a new tool for therapeutic 
   strategy in patients with severe alcoholic hepatitis treated with steroids. Hepatology. 
   2007;45(6):1348-1354. doi: 10.1002/hep.21607.
3. Forrest EH, Morris AJ, Stewart S, et al. The Glasgow alcoholic hepatitis score identifies 
   patients who may benefit from corticosteroids. Gut. 2007;56(12):1743-1746. 
   doi: 10.1136/gut.2006.099226.

The Glasgow Alcoholic Hepatitis Score (GAHS) is a prognostic tool that predicts mortality 
in patients with alcoholic hepatitis. It was developed from a multivariate analysis of 
factors predictive of mortality in 241 patients with alcoholic hepatitis and has been 
shown to be more accurate than the modified Discriminant Function for predicting 28-day 
outcomes. The score incorporates five clinical variables that reflect different aspects 
of disease severity and organ dysfunction.

Key Clinical Applications:
- Mortality prediction in patients with alcoholic hepatitis
- Identification of patients who may benefit from corticosteroid therapy  
- Risk stratification for clinical decision-making and resource allocation
- Prognostic counseling for patients and families
- Clinical trial enrollment and stratification

The GAHS demonstrates superior prognostic accuracy compared to other scoring systems, 
with overall accuracy of 81% on day 1 and 93% on day 7 for predicting 28-day outcomes. 
It is the first scoring system for alcoholic hepatitis to include an inflammatory 
parameter (white blood cell count), which is particularly relevant for this highly 
inflammatory condition. The score effectively identifies patients with GAHS ≥9 who 
have poor prognosis and benefit significantly from corticosteroid treatment.
"""

from pydantic import BaseModel, Field


class GlasgowAlcoholicHepatitisScoreRequest(BaseModel):
    """
    Request model for Glasgow Alcoholic Hepatitis Score (GAHS)
    
    The GAHS provides mortality prediction in patients with alcoholic hepatitis using 
    five clinical variables that reflect different aspects of disease severity and 
    organ dysfunction. This scoring system offers superior prognostic accuracy compared 
    to other established scores and helps identify patients who would benefit from 
    corticosteroid therapy.
    
    **CLINICAL CONTEXT AND INDICATIONS**:
    
    **Primary Clinical Application**:
    - **Target Population**: Patients with confirmed alcoholic hepatitis diagnosis
    - **Clinical Settings**: Hepatology units, gastroenterology services, intensive care units
    - **Assessment Timing**: Within first few days of hospitalization for optimal accuracy
    - **Diagnostic Prerequisites**: Clinical and/or histological confirmation of alcoholic hepatitis
    
    **Key Advantages for Alcoholic Hepatitis Management**:
    - **Superior Accuracy**: More accurate than modified Discriminant Function (81% vs 49% accuracy)
    - **Comprehensive Assessment**: Incorporates multiple organ systems (liver, kidney, coagulation, inflammation)
    - **Treatment Guidance**: Identifies patients who benefit from corticosteroid therapy
    - **Readily Available Parameters**: Uses standard laboratory tests available in most healthcare settings
    - **Validated Performance**: Extensively validated with consistent prognostic accuracy
    
    **PARAMETER INTERPRETATION FRAMEWORK**:
    
    **Age**:
    
    **Clinical Significance**: Reflects overall patient condition and healing capacity
    - **Prognostic Role**: Older age associated with worse outcomes in alcoholic hepatitis
    - **Threshold Rationale**: 50 years represents inflection point for increased mortality risk
    - **Scoring**: <50 years (1 point), ≥50 years (2 points)
    - **Clinical Context**: Older patients have reduced hepatic regenerative capacity and increased comorbidities
    
    **White Blood Cell Count**:
    
    **Clinical Significance**: Marker of systemic inflammatory response and disease severity
    - **Physiological Role**: Reflects inflammatory response to hepatic necrosis and systemic illness
    - **GAHS Innovation**: First alcoholic hepatitis score to include inflammatory parameter
    - **Threshold Rationale**: 15 ×10⁹/L represents significant inflammatory response
    - **Scoring**: <15 ×10⁹/L (1 point), ≥15 ×10⁹/L (2 points)
    - **Clinical Interpretation**: Elevated WBC indicates severe inflammatory response and tissue damage
    
    **Laboratory Considerations**:
    - **Units**: Expressed as ×10⁹/L (cells per liter)
    - **Normal Range**: Typically 4.0-11.0 ×10⁹/L in healthy adults
    - **Confounding Factors**: Infection, medications (corticosteroids), other inflammatory conditions
    - **Clinical Correlation**: Should be interpreted in context of clinical presentation
    
    **Urea (Blood Urea Nitrogen)**:
    
    **Clinical Significance**: Marker of renal function and fluid status
    - **Physiological Role**: Reflects kidney function and protein metabolism
    - **GAHS Rationale**: Chosen over creatinine due to bilirubin interference with creatinine assays
    - **Threshold Rationale**: 5 mmol/L represents clinically significant elevation
    - **Scoring**: <5 mmol/L (1 point), ≥5 mmol/L (2 points)
    - **Clinical Context**: Elevated urea may indicate prerenal azotemia, hepatorenal syndrome, or dehydration
    
    **Laboratory Considerations**:
    - **Units**: Expressed in mmol/L (some labs report mg/dL)
    - **Conversion**: mmol/L × 2.8 = mg/dL (approximate)
    - **Normal Range**: Typically 2.5-7.5 mmol/L (7-21 mg/dL)
    - **Advantages**: Less affected by bilirubin interference compared to creatinine
    
    **Prothrombin Time Ratio**:
    
    **Clinical Significance**: Marker of hepatic synthetic function and coagulopathy
    - **Physiological Role**: Reflects liver's ability to synthesize clotting factors
    - **Clinical Importance**: Key indicator of liver function severity in acute hepatitis
    - **Scoring**: <1.5 (1 point), 1.5-2.0 (2 points), >2.0 (3 points)
    - **Clinical Context**: Prolonged PT indicates significant hepatocellular dysfunction
    
    **Laboratory Considerations**:
    - **Expression**: Can be expressed as ratio or INR (International Normalized Ratio)
    - **Normal Range**: Typically 0.8-1.2 for PT ratio, 0.8-1.1 for INR
    - **Clinical Significance**: Values >1.5 indicate clinically significant coagulopathy
    - **Monitoring**: Important for assessing treatment response and disease progression
    
    **Bilirubin**:
    
    **Clinical Significance**: Primary marker of hepatic dysfunction and cholestasis
    - **Physiological Role**: Reflects liver's ability to conjugate and excrete bilirubin
    - **Disease Severity**: Higher levels indicate more severe hepatocellular damage
    - **Scoring**: <125 μmol/L (1 point), 125-250 μmol/L (2 points), >250 μmol/L (3 points)
    - **Clinical Context**: Progressive elevation indicates worsening hepatic function
    
    **Laboratory Considerations**:
    - **Units**: Expressed in μmol/L (some labs report mg/dL)
    - **Conversion**: μmol/L ÷ 17.1 = mg/dL (approximate)
    - **Normal Range**: Typically <20 μmol/L (<1.2 mg/dL)
    - **Clinical Significance**: Levels >125 μmol/L (>7.3 mg/dL) indicate significant dysfunction
    
    **SCORING SYSTEM FRAMEWORK**:
    
    **Score Calculation**:
    - **Total Range**: 5-12 points
    - **Component Scores**: Each parameter contributes 1-3 points
    - **Risk Stratification**: Cutoff at 9 points for high-risk category
    - **Clinical Application**: Higher scores indicate worse prognosis
    
    **Risk Categories**:
    
    **Low Risk (GAHS 5-8)**:
    - **28-day Survival**: Approximately 87% without specific treatment
    - **Clinical Significance**: Good prognosis with standard supportive care
    - **Management Approach**: Supportive care, alcohol cessation, nutritional support
    - **Corticosteroid Benefit**: No demonstrated survival benefit from corticosteroids
    
    **High Risk (GAHS 9-12)**:
    - **28-day Survival**: 46% without treatment, 78% with corticosteroids
    - **Clinical Significance**: Poor prognosis requiring intensive intervention
    - **Management Approach**: Strong indication for corticosteroid therapy if not contraindicated
    - **Treatment Benefit**: Significant survival improvement with corticosteroid treatment
    
    **CLINICAL VALIDATION AND PERFORMANCE**:
    
    **Development Study**:
    - **Population**: 241 patients with alcoholic hepatitis
    - **Methodology**: Multivariate analysis of mortality predictors
    - **Validation**: Both internal and external validation performed
    - **Follow-up**: 28-day and 84-day mortality outcomes
    
    **Performance Metrics**:
    - **Overall Accuracy**: 81% (day 1), 93% (day 7)
    - **Sensitivity**: 81% (day 1), 93% (day 7)
    - **Specificity**: 61% (day 1), 68% (day 7)
    - **Superiority**: More accurate than modified Discriminant Function
    
    **CLINICAL IMPLEMENTATION GUIDELINES**:
    
    **Assessment Timing**:
    - **Optimal Timing**: Within first few days of hospitalization
    - **Serial Assessment**: Can be repeated to monitor disease progression
    - **Treatment Response**: Useful for assessing response to interventions
    - **Clinical Decision Points**: Key timepoint for corticosteroid initiation
    
    **Laboratory Requirements**:
    - **Standard Tests**: All parameters available in routine laboratory panels
    - **Quality Assurance**: Ensure accurate laboratory calibration and reference ranges
    - **Timing**: Avoid hemolyzed specimens, obtain during stable clinical condition
    - **Interpretation**: Consider clinical context and potential confounding factors
    
    References (Vancouver style):
    1. Forrest EH, Evans CD, Stewart S, et al. Analysis of factors predictive of mortality 
       in alcoholic hepatitis and derivation and validation of the Glasgow alcoholic hepatitis 
       score. Gut. 2005;54(8):1174-1179.
    2. Louvet A, Naveau S, Abdelnour M, et al. The Lille model: a new tool for therapeutic 
       strategy in patients with severe alcoholic hepatitis treated with steroids. Hepatology. 
       2007;45(6):1348-1354.
    3. Forrest EH, Morris AJ, Stewart S, et al. The Glasgow alcoholic hepatitis score identifies 
       patients who may benefit from corticosteroids. Gut. 2007;56(12):1743-1746.
    """
    
    age: int = Field(
        ...,
        description="Patient age in years. Age ≥50 years associated with increased mortality risk and scores 2 points vs 1 point for <50 years",
        ge=18,
        le=120,
        example=55
    )
    
    white_cell_count: float = Field(
        ...,
        description="White blood cell count in ×10⁹/L. First alcoholic hepatitis score to include inflammatory parameter. WBC ≥15 ×10⁹/L indicates significant inflammatory response and scores 2 points",
        ge=1.0,
        le=100.0,
        example=18.5
    )
    
    urea: float = Field(
        ...,
        description="Blood urea nitrogen (BUN) in mmol/L. Marker of renal function chosen over creatinine due to bilirubin interference. Urea ≥5 mmol/L scores 2 points vs 1 point for <5 mmol/L",
        ge=1.0,
        le=50.0,
        example=7.2
    )
    
    prothrombin_time_ratio: float = Field(
        ...,
        description="Prothrombin time ratio or INR. Marker of hepatic synthetic function. Scoring: <1.5 (1 point), 1.5-2.0 (2 points), >2.0 (3 points)",
        ge=0.8,
        le=10.0,
        example=1.8
    )
    
    bilirubin: float = Field(
        ...,
        description="Serum total bilirubin in μmol/L. Primary marker of hepatic dysfunction. Scoring: <125 (1 point), 125-250 (2 points), >250 (3 points)",
        ge=10.0,
        le=1000.0,
        example=180.0
    )
    
    class Config:
        schema_extra = {
            "example": {
                "age": 55,
                "white_cell_count": 18.5,
                "urea": 7.2,
                "prothrombin_time_ratio": 1.8,
                "bilirubin": 180.0
            }
        }


class GlasgowAlcoholicHepatitisScoreResponse(BaseModel):
    """
    Response model for Glasgow Alcoholic Hepatitis Score (GAHS)
    
    The response provides the calculated GAHS with comprehensive clinical interpretation 
    and evidence-based management recommendations based on validated prognostic categories 
    from extensive clinical validation studies in alcoholic hepatitis patients.
    
    **CLINICAL INTERPRETATION FRAMEWORK**:
    
    **GAHS Components and Validation**:
    - **Scoring Range**: 5-12 points incorporating five clinical variables
    - **Prognostic Accuracy**: Superior to modified Discriminant Function (81% vs 49% accuracy)
    - **Population Validation**: Developed and validated in 241 patients with alcoholic hepatitis
    - **Clinical Significance**: First score to include inflammatory parameter (WBC count)
    
    **Risk Categories and Clinical Implications**:
    
    **Low Risk (GAHS 5-8)**:
    - **28-day Mortality**: Approximately 13% (87% survival)
    - **84-day Mortality**: 21-13% depending on specific score
    - **Clinical Significance**: Good prognosis with standard supportive care
    - **Treatment Approach**: Supportive care sufficient, no corticosteroid benefit demonstrated
    
    **High Risk (GAHS 9-12)**:
    - **28-day Mortality**: 54% without treatment, 22% with corticosteroids  
    - **84-day Mortality**: 44-83% depending on specific score and treatment
    - **Clinical Significance**: Poor prognosis requiring intensive intervention
    - **Treatment Benefit**: Significant survival improvement with corticosteroid therapy
    
    **CLINICAL MANAGEMENT BY RISK CATEGORY**:
    
    **Low Risk Management (GAHS 5-8)**:
    
    **Treatment Approach**:
    - **Supportive Care**: Focus on nutritional support, alcohol cessation, symptom management
    - **Corticosteroid Therapy**: Not recommended - no demonstrated survival benefit
    - **Monitoring Strategy**: Regular clinical assessment, laboratory monitoring for progression
    - **Alcohol Cessation**: Intensive counseling and support programs essential
    
    **Clinical Optimization**:
    - **Nutritional Support**: High-calorie, high-protein diet with vitamin supplementation
    - **Symptom Management**: Manage nausea, pain, and other symptoms supportively
    - **Complication Prevention**: Monitor for infection, bleeding, encephalopathy
    - **Patient Education**: Emphasize importance of complete alcohol cessation
    
    **High Risk Management (GAHS 9-12)**:
    
    **Urgent Intervention**:
    - **Corticosteroid Therapy**: Strong indication for prednisolone 40mg daily for 28 days
    - **Contraindication Assessment**: Screen for active infection, renal failure, GI bleeding
    - **Alternative Therapies**: Consider pentoxifylline if corticosteroids contraindicated
    - **Intensive Monitoring**: Close clinical and laboratory surveillance
    
    **Treatment Protocol**:
    - **Prednisolone**: 40mg daily for 4 weeks, then gradual taper over 2-4 weeks
    - **Response Assessment**: Lille score at day 7 to assess corticosteroid response
    - **Monitoring**: Weekly CBC, comprehensive metabolic panel, liver function tests
    - **Complication Management**: Aggressive treatment of infections, bleeding, encephalopathy
    
    **Advanced Care Considerations**:
    - **Liver Transplant Evaluation**: For appropriate candidates with continued deterioration
    - **Palliative Care**: Early involvement for symptom management and goals of care
    - **Family Support**: Education and support for caregivers and family members
    - **Nutritional Intervention**: Consider enteral nutrition if oral intake inadequate
    
    **SPECIAL CLINICAL CONSIDERATIONS**:
    
    **Corticosteroid Contraindications**:
    - **Active Infection**: Bacterial, fungal, or viral infections
    - **Renal Failure**: Creatinine >220 μmol/L (>2.5 mg/dL)
    - **Gastrointestinal Bleeding**: Active or recent significant bleeding
    - **Uncontrolled Diabetes**: Severe hyperglycemia requiring intensive management
    
    **Treatment Response Monitoring**:
    - **Lille Score**: Calculate at day 7 to assess corticosteroid response
    - **Clinical Parameters**: Improvement in jaundice, ascites, encephalopathy
    - **Laboratory Trends**: Decreasing bilirubin, improving PT/INR, stable renal function
    - **Complications**: Monitor for steroid-related side effects and disease progression
    
    **Prognostic Counseling Guidelines**:
    - **Survival Statistics**: Provide realistic but sensitive prognostic information
    - **Treatment Benefits**: Explain potential benefits and risks of corticosteroid therapy
    - **Disease Trajectory**: Discuss expected course with and without treatment
    - **Quality of Life**: Address functional outcomes and symptom management goals
    
    **Quality Improvement Applications**:
    - **Clinical Pathways**: Standardize assessment and treatment protocols
    - **Outcome Tracking**: Monitor treatment response rates and complications
    - **Resource Allocation**: Guide intensive care and specialized service needs
    - **Provider Education**: Train healthcare teams in GAHS calculation and interpretation
    
    Reference: Forrest EH, et al. Gut. 2005;54(8):1174-1179.
    """
    
    result: int = Field(
        ...,
        description="Glasgow Alcoholic Hepatitis Score calculated from clinical parameters (5-12 points)",
        ge=5,
        le=12,
        example=9
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for GAHS score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Comprehensive clinical interpretation with mortality prediction and evidence-based management recommendations",
        example="Glasgow Alcoholic Hepatitis Score: 9/12 points (Age: 55 years, WBC: 18.5 ×10⁹/L, Urea: 7.2 mmol/L, PT ratio: 1.80, Bilirubin: 180 μmol/L). GAHS ≥9 indicates poor prognosis with 28-day survival of approximately 46% without treatment, improving to 78% with corticosteroid therapy. Strong indication for corticosteroid treatment unless contraindicated. Consider prednisolone 40mg daily for 28 days if no contraindications (active infection, renal failure, gastrointestinal bleeding). Provide intensive supportive care, alcohol cessation programs, and consider liver transplant evaluation if appropriate. Monitor closely for treatment response and complications."
    )
    
    stage: str = Field(
        ...,
        description="Risk category based on GAHS score (Low Risk, High Risk)",
        example="High Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of prognostic category",
        example="Poor prognosis"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 9,
                "unit": "points",
                "interpretation": "Glasgow Alcoholic Hepatitis Score: 9/12 points (Age: 55 years, WBC: 18.5 ×10⁹/L, Urea: 7.2 mmol/L, PT ratio: 1.80, Bilirubin: 180 μmol/L). GAHS ≥9 indicates poor prognosis with 28-day survival of approximately 46% without treatment, improving to 78% with corticosteroid therapy. Strong indication for corticosteroid treatment unless contraindicated. Consider prednisolone 40mg daily for 28 days if no contraindications (active infection, renal failure, gastrointestinal bleeding). Provide intensive supportive care, alcohol cessation programs, and consider liver transplant evaluation if appropriate. Monitor closely for treatment response and complications.",
                "stage": "High Risk",
                "stage_description": "Poor prognosis"
            }
        }