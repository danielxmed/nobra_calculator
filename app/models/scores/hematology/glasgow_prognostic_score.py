"""
Glasgow Prognostic Score (GPS) Models

Request and response models for Glasgow Prognostic Score calculation.

References (Vancouver style):
1. Forrest LM, McMillan DC, McArdle CS, Angerson WJ, Dunlop DJ. Evaluation of 
   cumulative prognostic scores based on the systemic inflammatory response in 
   patients with inoperable non-small-cell lung cancer. Br J Cancer. 2003;89(5):1028-1030. 
   doi: 10.1038/sj.bjc.6601242.
2. McMillan DC. The systemic inflammation-based Glasgow Prognostic Score: a decade 
   of experience in patients with cancer. Cancer Treat Rev. 2013;39(5):534-540. 
   doi: 10.1016/j.ctrv.2012.08.003.
3. Roxburgh CS, McMillan DC. Role of systemic inflammatory response in predicting 
   survival in patients with primary operable cancer. Future Oncol. 2010;6(1):149-163. 
   doi: 10.2217/fon.09.136.
4. Proctor MJ, Morrison DS, Talwar D, et al. A comparison of inflammation-based 
   prognostic scores in patients with cancer. A Glasgow Inflammation Outcome Study. 
   Eur J Cancer. 2011;47(17):2633-2641. doi: 10.1016/j.ejca.2011.03.028.

The Glasgow Prognostic Score (GPS) is a systemic inflammation-based prognostic 
score that combines serum C-reactive protein and albumin levels to predict survival 
outcomes in cancer patients. Developed and validated across multiple cancer types, 
the GPS reflects both the presence of systemic inflammatory response (elevated CRP) 
and progressive nutritional decline (decreased albumin) commonly observed in cancer 
patients with poor prognosis.

Key Clinical Applications:
- Prognostication across multiple cancer types (colorectal, lung, hepatocellular, sarcoma)
- Patient stratification for clinical trials and treatment planning
- Assessment of systemic inflammatory burden and nutritional status
- Guide supportive care interventions and palliative care discussions
- Monitor treatment response and disease progression

Clinical Significance and Validation:
The GPS is the most extensively validated systemic inflammation-based prognostic 
score, with over 60 studies encompassing more than 30,000 cancer patients 
demonstrating its prognostic value. The score has independent prognostic significance 
in both operable and inoperable disease, across various cancer stages, and in 
patients receiving different treatment modalities including surgery, chemotherapy, 
and radiotherapy.

The modified GPS (mGPS) variant prioritizes CRP elevation over isolated albumin 
reduction, assigning intermediate scores only when CRP is elevated, based on 
evidence that CRP elevation is more strongly associated with poor outcomes than 
isolated albumin reduction in certain cancer contexts.
"""

from pydantic import BaseModel, Field
from typing import Literal


class GlasgowPrognosticScoreRequest(BaseModel):
    """
    Request model for Glasgow Prognostic Score (GPS)
    
    The GPS provides systematic assessment of systemic inflammation and nutritional 
    status using two routine laboratory parameters: C-reactive protein and serum 
    albumin. This standardized approach enables consistent evaluation across 
    healthcare settings and cancer types, facilitating prognostic assessment 
    and treatment planning decisions.
    
    **CLINICAL ASSESSMENT FRAMEWORK**:
    
    **Laboratory Parameter Assessment**:
    
    **C-Reactive Protein (CRP) Assessment**:
    
    **Clinical Significance**: Acute-phase protein marker of systemic inflammation
    - **Pathophysiology**: Synthesized by hepatocytes in response to inflammatory cytokines (IL-6, TNF-α)
    - **Cancer Context**: Elevated in response to tumor-induced inflammation and tissue necrosis
    - **Prognostic Value**: Strong predictor of cancer survival across multiple tumor types
    - **Cut-off Threshold**: >1.0 mg/dL indicates clinically significant systemic inflammation
    
    **CRP Elevation Mechanisms in Cancer**:
    - **Tumor-Associated Inflammation**: Direct inflammatory response to tumor presence
    - **Cytokine Production**: Tumor and immune cell release of inflammatory mediators
    - **Tissue Necrosis**: Inflammatory response to tumor necrosis and breakdown
    - **Host Response**: Systemic inflammatory response to cancer burden
    - **Treatment Effects**: Inflammatory response to chemotherapy or radiation
    
    **Clinical Interpretation of CRP Levels**:
    - **≤1.0 mg/dL**: Normal, minimal systemic inflammatory response
    - **1.1-3.0 mg/dL**: Mild to moderate elevation, early inflammatory response
    - **3.1-10.0 mg/dL**: Significant elevation, substantial inflammatory burden
    - **>10.0 mg/dL**: Severe elevation, indicates major inflammatory response
    
    **Serum Albumin Assessment**:
    
    **Clinical Significance**: Marker of nutritional status and liver synthetic function
    - **Synthesis**: Produced exclusively by hepatocytes with 20-day half-life
    - **Functions**: Oncotic pressure maintenance, drug binding, antioxidant properties
    - **Cancer Impact**: Decreased due to reduced synthesis, increased catabolism, and losses
    - **Cut-off Threshold**: <3.5 g/dL indicates clinically significant hypoalbuminemia
    
    **Albumin Reduction Mechanisms in Cancer**:
    - **Decreased Synthesis**: Hepatic dysfunction, inflammatory cytokine inhibition
    - **Increased Catabolism**: Tumor-induced protein breakdown and muscle wasting
    - **Increased Losses**: Gastrointestinal losses, renal losses, third-spacing
    - **Malnutrition**: Reduced protein intake due to cancer effects
    - **Inflammatory Response**: Negative acute-phase protein response
    
    **Clinical Interpretation of Albumin Levels**:
    - **≥3.5 g/dL**: Normal, adequate nutritional status and hepatic function
    - **3.0-3.4 g/dL**: Mild hypoalbuminemia, early nutritional compromise
    - **2.5-2.9 g/dL**: Moderate hypoalbuminemia, significant nutritional deficit
    - **<2.5 g/dL**: Severe hypoalbuminemia, critical nutritional status
    
    **GPS Scoring Systems**:
    
    **Original GPS Methodology**:
    - **Score 0**: Both CRP ≤1.0 mg/dL AND albumin ≥3.5 g/dL (optimal status)
    - **Score 1**: Either CRP >1.0 mg/dL OR albumin <3.5 g/dL (single abnormality)
    - **Score 2**: Both CRP >1.0 mg/dL AND albumin <3.5 g/dL (dual abnormality)
    
    **Modified GPS (mGPS) Methodology**:
    - **Score 0**: CRP ≤1.0 mg/dL (regardless of albumin level)
    - **Score 1**: CRP >1.0 mg/dL AND albumin ≥3.5 g/dL (inflammation without malnutrition)
    - **Score 2**: CRP >1.0 mg/dL AND albumin <3.5 g/dL (inflammation with malnutrition)
    
    **Clinical Decision Framework**:
    
    **Score Selection Guidance**:
    - **Original GPS**: Use when both inflammation and nutrition equally important
    - **Modified GPS**: Use when inflammation is primary prognostic concern
    - **Cancer Type**: Some cancers may favor one scoring method over another
    - **Clinical Context**: Treatment goals and patient condition may influence choice
    
    **Laboratory Requirements**:
    - **Sample Type**: Serum or plasma for both parameters
    - **Timing**: Obtain before treatment initiation when possible
    - **Fasting**: Not required for either parameter
    - **Stability**: Both parameters stable in routine laboratory conditions
    
    **Clinical Applications by Cancer Type**:
    
    **Colorectal Cancer**:
    - Strong prognostic value in both operable and metastatic disease
    - GPS 2 associated with 5-year survival rate of ~35% vs ~80% for GPS 0
    - May guide adjuvant therapy decisions and surveillance intensity
    
    **Lung Cancer**:
    - Validated in both small cell and non-small cell lung cancer
    - Particularly valuable in advanced disease for treatment planning
    - May influence performance status assessment and therapy selection
    
    **Hepatocellular Carcinoma**:
    - Strong correlation with tumor size, liver function, and survival
    - May complement staging systems like Barcelona Clinic Liver Cancer
    - Useful for patient selection for liver transplantation or resection
    
    **Other Cancer Types**:
    - Validated in sarcoma, renal cell carcinoma, gastric cancer, pancreatic cancer
    - Consistent prognostic value across different treatment modalities
    - May be particularly valuable in rare cancers with limited prognostic tools
    
    **CLINICAL INTEGRATION AND INTERPRETATION**:
    
    **Integration with Other Prognostic Factors**:
    - **TNM Staging**: GPS provides complementary prognostic information
    - **Performance Status**: May correlate with and enhance performance status assessment
    - **Biomarkers**: Can be combined with tumor-specific biomarkers
    - **Comorbidities**: Should be interpreted in context of overall health status
    
    **Treatment Planning Applications**:
    - **Surgical Candidates**: High GPS may predict post-operative complications
    - **Chemotherapy**: May influence dose modifications and supportive care needs
    - **Radiotherapy**: Could guide concurrent treatment approaches
    - **Palliative Care**: High scores may prompt earlier palliative care involvement
    
    **Monitoring and Follow-up**:
    - **Serial Measurements**: Changes in GPS may reflect treatment response
    - **Disease Progression**: Rising scores may indicate disease progression
    - **Treatment Toxicity**: May help identify patients at risk for treatment complications
    - **Supportive Care**: Guide nutritional interventions and anti-inflammatory measures
    
    References (Vancouver style):
    1. Forrest LM, McMillan DC, McArdle CS, Angerson WJ, Dunlop DJ. Evaluation of 
       cumulative prognostic scores based on the systemic inflammatory response in 
       patients with inoperable non-small-cell lung cancer. Br J Cancer. 2003;89(5):1028-1030.
    2. McMillan DC. The systemic inflammation-based Glasgow Prognostic Score: a decade 
       of experience in patients with cancer. Cancer Treat Rev. 2013;39(5):534-540.
    3. Roxburgh CS, McMillan DC. Role of systemic inflammatory response in predicting 
       survival in patients with primary operable cancer. Future Oncol. 2010;6(1):149-163.
    4. Proctor MJ, Morrison DS, Talwar D, et al. A comparison of inflammation-based 
       prognostic scores in patients with cancer. Eur J Cancer. 2011;47(17):2633-2641.
    """
    
    crp: float = Field(
        ...,
        description="C-reactive protein level in mg/dL. Marker of systemic inflammation (normal ≤1.0 mg/dL)",
        ge=0,
        le=50,
        example=0.8
    )
    
    albumin: float = Field(
        ...,
        description="Serum albumin level in g/dL. Marker of nutritional status and liver synthetic function (normal ≥3.5 g/dL)",
        ge=1.0,
        le=6.0,
        example=3.8
    )
    
    score_type: Literal["original", "modified"] = Field(
        ...,
        description="Type of GPS calculation. Original considers both CRP and albumin abnormalities equally. Modified prioritizes CRP elevation",
        example="original"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "crp": 0.8,
                "albumin": 3.8,
                "score_type": "original"
            }
        }


class GlasgowPrognosticScoreResponse(BaseModel):
    """
    Response model for Glasgow Prognostic Score (GPS)
    
    The response provides the calculated GPS score with comprehensive clinical 
    interpretation and evidence-based prognostic information based on extensive 
    validation studies across multiple cancer types and patient populations.
    
    **CLINICAL INTERPRETATION FRAMEWORK**:
    
    **GPS Score Validation and Clinical Significance**:
    - **Scoring Range**: 0-2 points combining inflammation and nutritional markers
    - **Clinical Validation**: Validated in >60 studies with >30,000 cancer patients
    - **Prognostic Power**: Independent predictor of survival across multiple cancer types
    - **Clinical Utility**: Cost-effective using routine laboratory parameters
    
    **Prognostic Categories and Clinical Outcomes**:
    
    **GPS 0 - Low Risk (Optimal Status)**:
    - **Laboratory Profile**: CRP ≤1.0 mg/dL AND albumin ≥3.5 g/dL (original GPS)
    - **Clinical Significance**: Minimal systemic inflammation and adequate nutrition
    - **Survival Outcomes**: Best prognosis with longest overall survival
    - **5-Year Survival**: Approximately 70-80% in most cancer types
    - **Clinical Implications**: Standard treatment approaches, routine monitoring
    
    **GPS 1 - Intermediate Risk (Single Abnormality)**:
    - **Laboratory Profile**: Either elevated CRP OR low albumin (original GPS)
    - **Clinical Significance**: Either inflammatory response or nutritional compromise
    - **Survival Outcomes**: Intermediate prognosis with moderate survival reduction
    - **5-Year Survival**: Approximately 50-60% in most cancer types
    - **Clinical Implications**: Enhanced monitoring, supportive care consideration
    
    **GPS 2 - High Risk (Dual Abnormality)**:
    - **Laboratory Profile**: CRP >1.0 mg/dL AND albumin <3.5 g/dL
    - **Clinical Significance**: Combined inflammation and nutritional compromise
    - **Survival Outcomes**: Worst prognosis with shortest overall survival
    - **5-Year Survival**: Approximately 25-35% in most cancer types
    - **Clinical Implications**: Aggressive supportive care, palliative care discussion
    
    **EVIDENCE-BASED CLINICAL MANAGEMENT**:
    
    **Risk Stratification Applications**:
    
    **Treatment Planning**:
    - **Low Risk (GPS 0)**: Standard treatment protocols, full-dose therapy consideration
    - **Intermediate Risk (GPS 1)**: Monitor closely, consider supportive interventions
    - **High Risk (GPS 2)**: Dose modifications, enhanced supportive care, goals of care discussion
    
    **Supportive Care Interventions**:
    
    **Nutritional Management**:
    - **Low Albumin**: Nutritional assessment, protein supplementation, dietitian referral
    - **Severe Hypoalbuminemia**: Consider albumin infusion in appropriate clinical contexts
    - **Comprehensive Assessment**: Evaluate for underlying causes of malnutrition
    - **Monitoring**: Serial albumin levels to assess intervention effectiveness
    
    **Anti-Inflammatory Considerations**:
    - **Elevated CRP**: Investigate underlying causes of inflammation
    - **Cancer-Related Inflammation**: Consider anti-inflammatory medications if appropriate
    - **Infection Screening**: Rule out concurrent infections contributing to inflammation
    - **Monitoring**: Serial CRP to assess inflammatory burden changes
    
    **Clinical Monitoring and Follow-up**:
    
    **Serial Assessment Protocol**:
    - **Baseline**: Obtain GPS before treatment initiation when possible
    - **Treatment Monitoring**: Reassess at regular intervals during treatment
    - **Response Assessment**: Changes may reflect treatment efficacy
    - **Progression Monitoring**: Rising scores may indicate disease progression
    
    **Integration with Clinical Care**:
    - **Multidisciplinary Teams**: Share GPS results with oncology, nutrition, palliative care
    - **Clinical Trials**: Use for patient stratification and outcome analysis
    - **Quality Metrics**: Track GPS improvement as quality indicator
    - **Patient Education**: Explain prognostic significance and intervention opportunities
    
    **SPECIAL CLINICAL CONSIDERATIONS**:
    
    **Limitations and Confounding Factors**:
    - **Acute Illness**: Intercurrent infections may elevate CRP temporarily
    - **Liver Disease**: Hepatic dysfunction may affect albumin synthesis independent of nutrition
    - **Renal Disease**: Proteinuria may contribute to hypoalbuminemia
    - **Medications**: Corticosteroids may affect both CRP and albumin levels
    
    **Cancer-Specific Applications**:
    - **Surgical Planning**: High GPS may predict post-operative complications
    - **Chemotherapy Tolerance**: May guide dose modifications and monitoring frequency
    - **Radiation Therapy**: Could influence concurrent treatment decisions
    - **Immunotherapy**: May predict response to immune checkpoint inhibitors
    
    **Palliative Care Integration**:
    - **Goals of Care**: High GPS scores may prompt earlier palliative care referral
    - **Prognostic Discussions**: Provide objective data for survival expectations
    - **Resource Allocation**: Guide intensity of interventions and monitoring
    - **Advance Care Planning**: Inform discussions about treatment preferences
    
    **Quality Improvement Applications**:
    - **Clinical Protocols**: Standardize GPS assessment and response protocols
    - **Performance Metrics**: Track GPS improvement rates as quality indicators
    - **Provider Education**: Train staff on GPS interpretation and clinical applications
    - **Research Applications**: Use for clinical trial stratification and outcome studies
    
    Reference: McMillan DC. Cancer Treat Rev. 2013;39(5):534-540.
    """
    
    result: int = Field(
        ...,
        description="Glasgow Prognostic Score calculated from CRP and albumin levels (0-2 points)",
        ge=0,
        le=2,
        example=0
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for GPS score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Comprehensive clinical interpretation with prognostic assessment and evidence-based management recommendations",
        example="GPS: 0/2. [CRP: 0.8 mg/dL (normal), Albumin: 3.8 g/dL (normal)]. Low risk category with normal inflammatory markers and nutritional status. CRP ≤1.0 mg/dL indicates minimal systemic inflammatory response. Albumin ≥3.5 g/dL suggests adequate nutritional status and liver synthetic function. This profile is associated with the best prognosis and longest survival in cancer patients. Continue routine oncological management and monitoring. Consider this favorable prognostic indicator in treatment planning and patient counseling regarding expected outcomes."
    )
    
    stage: str = Field(
        ...,
        description="Risk category based on GPS score (GPS 0, GPS 1, GPS 2)",
        example="GPS 0"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of risk level and clinical significance",
        example="Low risk - Normal inflammation and nutrition"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 0,
                "unit": "points",
                "interpretation": "GPS: 0/2. [CRP: 0.8 mg/dL (normal), Albumin: 3.8 g/dL (normal)]. Low risk category with normal inflammatory markers and nutritional status. CRP ≤1.0 mg/dL indicates minimal systemic inflammatory response. Albumin ≥3.5 g/dL suggests adequate nutritional status and liver synthetic function. This profile is associated with the best prognosis and longest survival in cancer patients. Continue routine oncological management and monitoring. Consider this favorable prognostic indicator in treatment planning and patient counseling regarding expected outcomes.",
                "stage": "GPS 0",
                "stage_description": "Low risk - Normal inflammation and nutrition"
            }
        }