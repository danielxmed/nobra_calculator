"""
PROMISE Score for Malignant Pleural Effusion Models

Request and response models for PROMISE Score calculation.

References (Vancouver style):
1. Psallidas I, Kanellakis NI, Gerry S, Thakur N, Bamber J, Dipper A, et al. 
   Development and validation of response markers to predict survival and 
   pleurodesis success in patients with malignant pleural effusion (PROMISE): 
   a multicohort analysis. Lancet Oncol. 2018;19(7):930-939. 
   doi: 10.1016/S1470-2045(18)30294-8.
2. Clive AO, Kahan BC, Hooper CE, Bhatnagar R, Morley AJ, Zahan-Evans N, et al. 
   Predicting survival in malignant pleural effusion: development and validation 
   of the LENT prognostic score. Thorax. 2014;69(12):1098-104. 
   doi: 10.1136/thoraxjnl-2014-205285.
3. Yap E, Anderson B, Nair A, Vaska K, Ferland L, Penney B, et al. 
   The role of LENT and PROMISE scores in predicting survival in malignant 
   pleural effusion. Lung. 2022;200(4):459-465. 
   doi: 10.1007/s00408-022-00547-5.

The PROMISE Score for Malignant Pleural Effusion is the first prospectively validated 
prognostic model that combines clinical and biological parameters to accurately 
predict 3-month mortality in patients with malignant pleural effusion.
"""

from pydantic import BaseModel, Field
from typing import Literal


class PromiseScoreMalignantPleuralEffusionRequest(BaseModel):
    """
    Request model for PROMISE Score for Malignant Pleural Effusion calculation
    
    The PROMISE (Prognostic Markers to predict survival and pleurodesis success 
    in malignant pleural effusion) Score represents a significant advancement in 
    prognostication for patients with malignant pleural effusion. This validated 
    clinical tool was developed through rigorous multicohort analysis to provide 
    accurate 3-month mortality predictions, enabling clinicians to make informed 
    treatment decisions and guide prognostic discussions.
    
    Clinical Context and Significance:
    
    Malignant pleural effusion is a common complication affecting approximately 
    150,000 patients annually in the United States alone. These patients face 
    complex treatment decisions regarding drainage procedures, pleurodesis, and 
    palliative interventions. The PROMISE score addresses the critical need for 
    accurate prognostic information to guide these decisions and optimize patient 
    care while avoiding futile interventions in patients with very limited survival.
    
    Development and Validation:
    
    The PROMISE score was developed through comprehensive analysis of multiple 
    patient cohorts, incorporating both clinical parameters readily available 
    in routine practice and biological markers that reflect disease burden and 
    systemic inflammation. The prospective validation demonstrated superior 
    performance compared to existing tools such as the LENT score and ECOG 
    Performance Status alone.
    
    Clinical Parameters and Biological Rationale:
    
    Previous Chemotherapy History:
    Prior exposure to chemotherapy (4 points if yes) reflects advanced disease 
    stage and potential treatment resistance. Patients who have already received 
    chemotherapy often have more aggressive tumors or disease progression despite 
    treatment, indicating poorer prognosis and limited remaining therapeutic options.
    
    Previous Radiotherapy History:
    History of radiotherapy (2 points if yes) suggests either advanced locoregional 
    disease requiring radiation or previous treatment attempts. This parameter 
    helps identify patients with more complex treatment histories and potentially 
    worse outcomes.
    
    Hemoglobin Level:
    Anemia is a powerful prognostic indicator in cancer patients, reflecting:
    - Bone marrow involvement or suppression
    - Chronic inflammation and cytokine effects
    - Nutritional depletion and cancer cachexia
    - Treatment-related toxicity
    - Overall disease burden and functional decline
    
    Scoring: ≥16 g/dL (0 points), 14-<16 (1 point), 12-<14 (2 points), 
    10-<12 (3 points), <10 (4 points)
    
    White Blood Cell Count:
    Elevated WBC count indicates systemic inflammatory response and immune activation:
    - Higher counts suggest greater inflammatory burden
    - May reflect infection, tumor burden, or stress response
    - Associated with worse outcomes across cancer types
    - Can indicate bone marrow stimulation or leukemoid reactions
    
    Scoring: <4 (0 points), 4-<6.3 (2 points), 6.3-<10 (4 points), 
    10-<15.8 (7 points), ≥15.8 (9 points)
    
    C-reactive Protein (CRP):
    CRP is a key inflammatory marker with strong prognostic significance:
    - Reflects systemic inflammatory response to cancer
    - Associated with tumor burden and metastatic disease
    - Correlates with poor nutritional status and cachexia
    - Predicts treatment resistance and shorter survival
    
    Scoring: <3 mg/L (0 points), 3-<10 (3 points), 10-<32 (5 points), 
    32-<100 (8 points), ≥100 (11 points)
    
    ECOG Performance Status:
    Functional status is one of the strongest predictors of cancer outcomes:
    - Status 0-1 indicates good functional capacity
    - Status 2-4 reflects significant functional decline
    - Correlates with treatment tolerance and quality of life
    - Essential for treatment decision-making
    
    Scoring: 0-1 (0 points), 2-4 (7 points)
    
    Cancer Type:
    Different cancer types have varying prognoses in the pleural space:
    - Mesothelioma (0 points): Often confined to pleural space initially
    - Lung cancer (6 points): Aggressive with poor prognosis
    - Other cancers (5 points): Variable behavior depending on primary site
    
    Risk Stratification and Clinical Application:
    
    Low Risk (Score 0-20, <25% 3-month mortality):
    - Excellent short-term prognosis
    - Candidates for aggressive interventions
    - Consider pleurodesis, indwelling catheters, or thoracoscopic procedures
    - Comprehensive treatment planning appropriate
    
    Intermediate-Low Risk (Score 21-30, 25-50% 3-month mortality):
    - Moderate prognosis requiring balanced approach
    - Treatment decisions based on individual factors
    - Consider benefits versus burdens of interventions
    - Regular reassessment of goals and preferences
    
    Intermediate-High Risk (Score 31-40, 50-75% 3-month mortality):
    - Limited prognosis requiring careful consideration
    - Focus on symptom control with selective interventions
    - Less invasive approaches preferred
    - Emphasis on quality of life and comfort
    
    High Risk (Score >40, >75% 3-month mortality):
    - Very poor prognosis
    - Primarily palliative approach
    - Avoid invasive procedures unless essential for comfort
    - Focus on end-of-life planning and support
    
    Clinical Decision-Making Applications:
    
    Treatment Selection:
    - Guides choice between aggressive and palliative interventions
    - Helps determine appropriateness of pleurodesis procedures
    - Influences decisions about indwelling pleural catheter placement
    - Supports timing of palliative care consultation
    
    Prognostic Communication:
    - Provides objective framework for difficult conversations
    - Supports shared decision-making with patients and families
    - Enables realistic goal-setting and care planning
    - Facilitates transition to comfort-focused care when appropriate
    
    Healthcare Resource Allocation:
    - Optimizes use of limited healthcare resources
    - Guides intensity of monitoring and follow-up
    - Supports quality improvement initiatives
    - Enables outcome prediction for care planning
    
    Integration with Comprehensive Care:
    
    Multidisciplinary Team Coordination:
    - Pulmonology: Procedure planning and symptom management
    - Oncology: Treatment sequencing and prognosis discussion
    - Palliative Care: Symptom control and end-of-life planning
    - Surgery: Risk assessment for invasive procedures
    
    Patient and Family Support:
    - Clear communication about prognosis and expectations
    - Preparation for potential complications and decline
    - Resources for coping with advanced cancer
    - Support for difficult treatment decisions
    
    Quality Metrics and Research:
    - Outcome prediction for quality improvement
    - Risk stratification for clinical trials
    - Benchmark for healthcare performance
    - Tool for advancing pleural disease research
    
    References (Vancouver style):
    1. Psallidas I, Kanellakis NI, Gerry S, Thakur N, Bamber J, Dipper A, et al. 
    Development and validation of response markers to predict survival and 
    pleurodesis success in patients with malignant pleural effusion (PROMISE): 
    a multicohort analysis. Lancet Oncol. 2018;19(7):930-939. 
    doi: 10.1016/S1470-2045(18)30294-8.
    2. Clive AO, Kahan BC, Hooper CE, Bhatnagar R, Morley AJ, Zahan-Evans N, et al. 
    Predicting survival in malignant pleural effusion: development and validation 
    of the LENT prognostic score. Thorax. 2014;69(12):1098-104. 
    doi: 10.1136/thoraxjnl-2014-205285.
    3. Yap E, Anderson B, Nair A, Vaska K, Ferland L, Penney B, et al. 
    The role of LENT and PROMISE scores in predicting survival in malignant 
    pleural effusion. Lung. 2022;200(4):459-465. 
    doi: 10.1007/s00408-022-00547-5.
    """
    
    previous_chemotherapy: Literal["no", "yes"] = Field(
        ...,
        description="History of previous chemotherapy treatment. 'Yes' indicates prior exposure to systemic chemotherapy, suggesting advanced disease stage or treatment resistance (4 points if yes)",
        example="no"
    )
    
    previous_radiotherapy: Literal["no", "yes"] = Field(
        ...,
        description="History of previous radiotherapy treatment. 'Yes' indicates prior radiation therapy, suggesting advanced locoregional disease or previous treatment attempts (2 points if yes)",
        example="no"
    )
    
    hemoglobin: Literal["≥16", "14_to_<16", "12_to_<14", "10_to_<12", "<10"] = Field(
        ...,
        description="Hemoglobin level in g/dL. Lower levels indicate anemia reflecting bone marrow involvement, chronic inflammation, or cancer cachexia. Scoring: ≥16 (0 pts), 14-<16 (1 pt), 12-<14 (2 pts), 10-<12 (3 pts), <10 (4 pts)",
        example="12_to_<14"
    )
    
    wbc_count: Literal["<4", "4_to_<6.3", "6.3_to_<10", "10_to_<15.8", "≥15.8"] = Field(
        ...,
        description="Serum white blood cell count in ×10⁹ cells/L. Higher counts indicate systemic inflammatory response and immune activation. Scoring: <4 (0 pts), 4-<6.3 (2 pts), 6.3-<10 (4 pts), 10-<15.8 (7 pts), ≥15.8 (9 pts)",
        example="6.3_to_<10"
    )
    
    crp: Literal["<3", "3_to_<10", "10_to_<32", "32_to_<100", "≥100"] = Field(
        ...,
        description="C-reactive protein level in mg/L. Higher levels reflect systemic inflammatory response associated with tumor burden and poor prognosis. Scoring: <3 (0 pts), 3-<10 (3 pts), 10-<32 (5 pts), 32-<100 (8 pts), ≥100 (11 pts)",
        example="10_to_<32"
    )
    
    ecog_status: Literal["0-1", "2-4"] = Field(
        ...,
        description="ECOG Performance Status reflecting functional capacity. 0-1 indicates good functional status, 2-4 indicates significant functional decline affecting treatment tolerance and prognosis (7 points for 2-4)",
        example="0-1"
    )
    
    cancer_type: Literal["mesothelioma", "lung", "other"] = Field(
        ...,
        description="Primary cancer type. Different cancers have varying prognoses in pleural space: mesothelioma (0 pts) often confined initially, lung cancer (6 pts) aggressive with poor prognosis, other cancers (5 pts) variable behavior",
        example="lung"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "previous_chemotherapy": "no",
                "previous_radiotherapy": "no",
                "hemoglobin": "12_to_<14",
                "wbc_count": "6.3_to_<10",
                "crp": "10_to_<32",
                "ecog_status": "0-1",
                "cancer_type": "lung"
            }
        }


class PromiseScoreMalignantPleuralEffusionResponse(BaseModel):
    """
    Response model for PROMISE Score for Malignant Pleural Effusion calculation
    
    The PROMISE Score response provides critical risk stratification for patients 
    with malignant pleural effusion, enabling evidence-based treatment decisions 
    and prognostic communication. This validated tool helps clinicians balance 
    aggressive interventions with palliative care based on predicted 3-month mortality.
    
    Risk Categories and Management Guidelines:
    
    Low Risk (Score 0-20, <25% 3-month mortality):
    - Clinical Significance: Excellent short-term prognosis with good functional potential
    - Treatment Approach: Consider aggressive interventions including pleurodesis
    - Interventions: Suitable for thoracoscopic procedures, indwelling pleural catheters
    - Monitoring: Regular follow-up with focus on symptom control and quality of life
    - Prognosis Discussion: Reassuring prognosis allows comprehensive treatment planning
    - Goals of Care: Curative or long-term palliative intent appropriate
    
    Intermediate-Low Risk (Score 21-30, 25-50% 3-month mortality):
    - Clinical Significance: Moderate prognosis requiring balanced treatment approach
    - Treatment Approach: Individual assessment of benefits versus burdens
    - Interventions: Consider pleurodesis or indwelling catheter based on performance status
    - Monitoring: Close follow-up with reassessment of clinical status
    - Prognosis Discussion: Balanced conversations about treatment options
    - Goals of Care: Palliative focus with selective aggressive interventions
    
    Intermediate-High Risk (Score 31-40, 50-75% 3-month mortality):
    - Clinical Significance: Limited survival requiring careful intervention selection
    - Treatment Approach: Focus on symptom control with selective procedures
    - Interventions: Consider less invasive options like therapeutic thoracentesis
    - Monitoring: Frequent reassessment with emphasis on comfort and function
    - Prognosis Discussion: Realistic expectations with quality of life focus
    - Goals of Care: Primarily comfort-focused with selective symptom interventions
    
    High Risk (Score >40, >75% 3-month mortality):
    - Clinical Significance: Very limited survival expectation
    - Treatment Approach: Primarily palliative care with comfort-focused interventions
    - Interventions: Avoid invasive procedures unless essential for symptom relief
    - Monitoring: Symptom-based assessment with comfort measures
    - Prognosis Discussion: Compassionate communication about limited prognosis
    - Goals of Care: End-of-life planning and comfort care prioritization
    
    Clinical Application and Decision-Making:
    
    Procedural Decision-Making:
    - Pleurodesis Candidacy: Low-risk patients are ideal candidates
    - Indwelling Catheter Selection: Appropriate for intermediate-risk patients
    - Thoracentesis Frequency: Guide interval and necessity of repeat procedures
    - Surgical Risk Assessment: Inform thoracoscopic procedure planning
    
    Prognostic Communication Framework:
    - Structured approach to difficult conversations about prognosis
    - Objective data to support clinical impressions
    - Framework for shared decision-making about treatment intensity
    - Support for transition to palliative care when appropriate
    
    Care Coordination and Planning:
    - Palliative Care Consultation: Triggers for specialist involvement
    - Healthcare Resource Allocation: Guide intensity of monitoring and care
    - Advance Care Planning: Timing of goals of care discussions
    - Family Preparation: Help families understand trajectory and needs
    
    Quality Improvement Applications:
    - Outcome Prediction: Support quality metrics and performance measurement
    - Clinical Trial Stratification: Risk-based patient selection and analysis
    - Healthcare Efficiency: Optimize resource utilization based on prognosis
    - Educational Tool: Train clinicians in prognostic assessment skills
    
    Multidisciplinary Integration:
    
    Pulmonology Services:
    - Procedure planning and risk assessment
    - Symptom management strategy development
    - Follow-up scheduling and monitoring protocols
    - Patient education about prognosis and treatment options
    
    Oncology Integration:
    - Treatment sequencing and timing decisions
    - Systemic therapy considerations in context of pleural disease
    - Coordination of care between pleural and oncologic management
    - Prognosis integration with overall cancer care planning
    
    Palliative Care Coordination:
    - Appropriate timing of palliative care consultation
    - Symptom management optimization
    - End-of-life care planning and preparation
    - Family support and bereavement preparation
    
    Surgical Services:
    - Risk assessment for thoracoscopic procedures
    - Patient selection for invasive interventions
    - Perioperative care planning and optimization
    - Postoperative monitoring and complication management
    
    Long-term Monitoring and Adaptation:
    
    Serial Assessment Value:
    - Monitor changes in clinical status and laboratory values
    - Reassess prognosis as treatment response becomes apparent
    - Adapt care plans based on evolving clinical picture
    - Guide timing of care transitions and goal modifications
    
    Treatment Response Integration:
    - Correlation of score changes with treatment effectiveness
    - Early identification of treatment failure or disease progression
    - Adaptation of prognostic estimates based on intervention response
    - Long-term outcome validation and score refinement
    
    Reference: Psallidas I, et al. Lancet Oncol. 2018;19(7):930-939.
    """
    
    result: int = Field(
        ...,
        description="PROMISE score (0-80+ points) predicting 3-month mortality risk in malignant pleural effusion",
        example=17
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Comprehensive clinical interpretation with management recommendations and prognostic guidance",
        example="LOW MORTALITY RISK (PROMISE Score: 17): Predicted 3-month mortality <25%. PROGNOSIS: Excellent short-term survival expected with good quality of life potential. MANAGEMENT: Consider aggressive treatment approaches including pleurodesis, indwelling pleural catheters, or thoracoscopic procedures. INTERVENTIONS: Patient is suitable candidate for invasive procedures with curative or long-term palliative intent. MONITORING: Regular follow-up with focus on symptom control and quality of life. COUNSELING: Reassuring prognosis allows for comprehensive treatment planning."
    )
    
    stage: str = Field(
        ...,
        description="Risk stratification category based on 3-month mortality prediction",
        example="Low Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the mortality risk level",
        example="3-month mortality <25%"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 17,
                "unit": "points",
                "interpretation": "LOW MORTALITY RISK (PROMISE Score: 17): Predicted 3-month mortality <25%. PROGNOSIS: Excellent short-term survival expected with good quality of life potential. MANAGEMENT: Consider aggressive treatment approaches including pleurodesis, indwelling pleural catheters, or thoracoscopic procedures. INTERVENTIONS: Patient is suitable candidate for invasive procedures with curative or long-term palliative intent. MONITORING: Regular follow-up with focus on symptom control and quality of life. COUNSELING: Reassuring prognosis allows for comprehensive treatment planning.",
                "stage": "Low Risk",
                "stage_description": "3-month mortality <25%"
            }
        }