"""
LENT Prognostic Score for Malignant Pleural Effusion Models

Request and response models for LENT prognostic score calculation.

References (Vancouver style):
1. Clive AO, Kahan BC, Hopwood BE, Bhatnagar R, Morley AJ, Zahan-Evans N, et al. 
   Predicting survival in malignant pleural effusion: development and validation of the 
   LENT prognostic score. Thorax. 2014 Dec;69(12):1098-104. doi: 10.1136/thoraxjnl-2014-205285.
2. Psallidas I, Kanellakis NI, Gerry S, Theza A, Saba T, Tsim S, et al. Development and 
   validation of response markers to predict survival and pleurodesis success in patients 
   with malignant pleural effusion (PROMISE): a multicohort analysis. Lancet Oncol. 2018 
   Jul;19(7):930-939. doi: 10.1016/S1470-2045(18)30294-8.
3. Porcel JM. Malignant pleural effusion. Current opinion in Pulmonary Medicine. 2016 
   Jul;22(4):356-61. doi: 10.1097/MCP.0000000000000284.

The LENT Prognostic Score is a validated clinical prediction tool designed to estimate 
survival in patients with malignant pleural effusion. The acronym LENT represents the 
four key prognostic factors: LDH (pleural fluid lactate dehydrogenase), ECOG performance 
status, Neutrophil-to-lymphocyte ratio, and Tumor type.

Clinical Background:
Malignant pleural effusion is a common complication of advanced cancer, affecting 
approximately 150,000 patients annually in the United States. It represents a significant 
clinical challenge with poor overall prognosis, median survival typically ranging from 
3-12 months depending on various factors. Accurate prognostication is crucial for 
treatment planning, patient counseling, and resource allocation.

The LENT score was developed through analysis of 3,426 patients from 11 centers across 
7 countries, making it one of the most comprehensively validated prognostic tools for 
malignant pleural effusion. The score demonstrates excellent discriminative ability 
(C-index 0.74) and has been externally validated in multiple independent cohorts.

Prognostic Components:

1. Pleural Fluid LDH (Lactate Dehydrogenase):
   LDH is an enzyme released during cellular damage and death. Elevated pleural fluid LDH 
   (≥1,500 U/L) indicates more aggressive disease with greater tumor burden and inflammatory 
   response. High LDH levels correlate with increased pleural fluid protein, cellularity, 
   and glucose consumption by malignant cells, reflecting more advanced local disease.

2. ECOG Performance Status:
   The Eastern Cooperative Oncology Group Performance Status is a standardized measure of 
   functional capacity that strongly correlates with survival in cancer patients:
   - ECOG 0: Fully active, no restrictions
   - ECOG 1: Symptomatic but ambulatory, restricted in strenuous activity
   - ECOG 2: Ambulatory >50% of waking hours, capable of self-care but unable to work
   - ECOG 3: Limited self-care, confined to bed/chair >50% of waking hours
   - ECOG 4: Completely disabled, totally confined to bed/chair

3. Neutrophil-to-Lymphocyte Ratio (NLR):
   The NLR is a simple biomarker reflecting systemic inflammatory response and immune status. 
   Elevated NLR (≥9) indicates a pro-inflammatory state with relative immunosuppression, 
   associated with tumor progression, metastasis, and poor treatment response. High NLR 
   reflects increased neutrophil-mediated tumor promotion and decreased lymphocyte-mediated 
   anti-tumor immunity.

4. Tumor Type:
   Different malignancies have distinct biological behaviors and treatment responses:
   - Mesothelioma/Hematologic: Generally slower progression, better response to systemic therapy
   - Breast/Gynecologic/Renal: Intermediate prognosis, often hormone-sensitive or targeted therapy options
   - Lung/Other solid tumors: More aggressive course, limited treatment options in advanced stages

Clinical Applications:

Risk Stratification:
- Low Risk (0-1 points): Median survival 319 days (~10.5 months)
  - Candidates for aggressive interventions (pleurodesis, indwelling catheters)
  - May benefit from systemic therapy and clinical trials
  - Focus on disease-directed treatment alongside symptom management

- Moderate Risk (2-4 points): Median survival 130 days (~4.3 months)  
  - Individualized decision-making based on patient preferences
  - Balance between disease-directed and palliative approaches
  - Consider less invasive interventions with focus on quality of life

- High Risk (5-7 points): Median survival 44 days (~1.5 months)
  - Emphasis on comfort care and symptom palliation
  - Avoid overly aggressive interventions that may increase suffering
  - Early palliative care consultation and end-of-life planning

Treatment Decision Framework:
The LENT score helps clinicians and patients make informed decisions about:
- Aggressiveness of pleural interventions (thoracentesis vs. pleurodesis vs. indwelling catheter)
- Appropriateness of systemic anticancer therapy
- Timing of palliative care referral
- Goals of care discussions and advance care planning
- Resource allocation and healthcare economics

Limitations and Considerations:
- Score provides population-based estimates; individual outcomes may vary significantly
- Should be combined with other clinical factors, patient preferences, and quality of life considerations
- Not intended to replace clinical judgment or comprehensive patient assessment
- Performance may vary across different healthcare settings and populations
- Regular reassessment is important as clinical status changes

Quality Measures:
- Appropriate use of prognostic scoring in eligible patients
- Documentation of score results and treatment decision rationale
- Integration with palliative care referral patterns
- Patient and family understanding of prognosis and treatment options
- Alignment of care intensity with prognostic category
"""

from pydantic import BaseModel, Field
from typing import Literal


class LentPrognosticScoreRequest(BaseModel):
    """
    Request model for LENT Prognostic Score for Malignant Pleural Effusion
    
    The LENT Prognostic Score uses four clinical and laboratory parameters to predict 
    survival in patients with malignant pleural effusion. This validated tool helps 
    inform treatment decisions and facilitate discussions about prognosis and goals of care.
    
    Clinical Parameters:
    
    Pleural Fluid LDH (Lactate Dehydrogenase):
    LDH is an intracellular enzyme released during cell damage and death. In malignant 
    pleural effusion, elevated LDH levels indicate:
    - Increased tumor burden and metabolic activity
    - Greater degree of pleural inflammation
    - More extensive malignant cell infiltration
    - Threshold: ≥1,500 U/L suggests more aggressive disease (1 point vs 0 points)
    
    ECOG Performance Status (Eastern Cooperative Oncology Group):
    Standardized scale assessing functional capacity and disease impact on daily activities:
    - 0 points: ECOG 0 (fully active, no restrictions on activity)
    - 1 point: ECOG 1 (symptomatic but ambulatory, restricted in strenuous activity)
    - 2 points: ECOG 2 (ambulatory >50% waking hours, capable of self-care, unable to work)
    - 3 points: ECOG 3-4 (limited self-care, confined to bed/chair >50% waking hours or completely disabled)
    
    Neutrophil-to-Lymphocyte Ratio (NLR):
    Simple biomarker reflecting systemic inflammation and immune status:
    - Calculated as: (Absolute neutrophil count) / (Absolute lymphocyte count)
    - Elevated NLR indicates pro-inflammatory state with relative immunosuppression
    - Associated with tumor progression, metastasis, and poor treatment response
    - Threshold: ≥9 suggests adverse prognosis (1 point vs 0 points)
    
    Tumor Type Categories:
    Different malignancies demonstrate distinct biological behaviors and prognoses:
    - Mesothelioma/Hematologic (0 points): Generally slower progression, better treatment response
    - Breast/Gynecologic/Renal (1 point): Intermediate prognosis, often have targeted therapy options
    - Lung/Other solid tumors (2 points): More aggressive course, limited treatment options in advanced stages
    
    Clinical Assessment Guidelines:
    - Apply to patients with confirmed malignant pleural effusion
    - Obtain pleural fluid analysis including LDH measurement
    - Assess functional status using standardized ECOG criteria
    - Calculate NLR from complete blood count with differential
    - Accurately classify primary tumor type
    - Consider patient's overall clinical condition and comorbidities
    
    Treatment Planning Considerations:
    - Low risk patients may benefit from aggressive interventions and systemic therapy
    - Moderate risk patients require individualized decision-making
    - High risk patients should focus on palliative care and comfort measures
    - Integrate results with patient preferences and goals of care
    - Use for clinical trial stratification and research purposes
    
    Quality Assurance:
    - Ensure accurate pleural fluid sampling and laboratory analysis
    - Verify ECOG assessment by trained healthcare provider
    - Confirm NLR calculation from recent laboratory values
    - Validate tumor type classification through pathology and imaging
    - Document rationale for treatment decisions based on score results
    
    References (Vancouver style):
    1. Clive AO, Kahan BC, Hopwood BE, Bhatnagar R, Morley AJ, Zahan-Evans N, et al. 
    Predicting survival in malignant pleural effusion: development and validation of the 
    LENT prognostic score. Thorax. 2014 Dec;69(12):1098-104.
    2. Psallidas I, Kanellakis NI, Gerry S, Theza A, Saba T, Tsim S, et al. Development and 
    validation of response markers to predict survival and pleurodesis success in patients 
    with malignant pleural effusion (PROMISE): a multicohort analysis. Lancet Oncol. 2018 
    Jul;19(7):930-939.
    """
    
    pleural_fluid_ldh: float = Field(
        ...,
        description="Pleural fluid lactate dehydrogenase (LDH) level in U/L. LDH is an intracellular enzyme "
                   "released during cell damage. Elevated levels (≥1,500 U/L) indicate more aggressive disease "
                   "with greater tumor burden, pleural inflammation, and malignant cell infiltration. "
                   "Normal pleural fluid LDH is typically <200 U/L; levels >1,500 U/L suggest extensive disease.",
        ge=0.0,
        le=10000.0,
        example=2200.0
    )
    
    ecog_performance_status: Literal[0, 1, 2, 3, 4] = Field(
        ...,
        description="Eastern Cooperative Oncology Group Performance Status (0-4). Standardized functional "
                   "assessment: 0=fully active (0 pts); 1=symptomatic but ambulatory, restricted in strenuous "
                   "activity (1 pt); 2=ambulatory >50% waking hours, self-care capable, unable to work (2 pts); "
                   "3=limited self-care, bed/chair >50% waking hours (3 pts); 4=completely disabled, "
                   "totally confined to bed/chair (3 pts). Higher scores indicate worse functional status.",
        example=1
    )
    
    neutrophil_lymphocyte_ratio: float = Field(
        ...,
        description="Serum neutrophil-to-lymphocyte ratio calculated from complete blood count with differential. "
                   "Reflects systemic inflammatory response and immune status. Calculated as absolute neutrophil "
                   "count divided by absolute lymphocyte count. Elevated ratio (≥9) indicates pro-inflammatory "
                   "state with relative immunosuppression, associated with tumor progression and poor prognosis. "
                   "Normal range typically 1-3; values ≥9 suggest adverse outcomes.",
        ge=0.0,
        le=100.0,
        example=5.2
    )
    
    tumor_type: Literal["mesothelioma_hematologic", "breast_gynecologic_renal", "lung_other"] = Field(
        ...,
        description="Primary tumor type category based on biological behavior and prognosis. "
                   "'mesothelioma_hematologic' (0 pts): mesothelioma or hematologic malignancies (lymphoma, leukemia) "
                   "- generally slower progression with better treatment responses; "
                   "'breast_gynecologic_renal' (1 pt): breast, gynecologic (ovarian, uterine, cervical), or "
                   "renal cell carcinoma - intermediate prognosis with targeted therapy options; "
                   "'lung_other' (2 pts): lung cancer or other solid tumors - more aggressive course with "
                   "limited treatment options in advanced stages.",
        example="breast_gynecologic_renal"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "pleural_fluid_ldh": 2200.0,
                "ecog_performance_status": 1,
                "neutrophil_lymphocyte_ratio": 5.2,
                "tumor_type": "breast_gynecologic_renal"
            }
        }


class LentPrognosticScoreResponse(BaseModel):
    """
    Response model for LENT Prognostic Score for Malignant Pleural Effusion
    
    Provides calculated prognostic score with evidence-based survival estimates and 
    treatment recommendations for patients with malignant pleural effusion. The response 
    stratifies patients into risk categories that guide clinical decision-making and 
    facilitate discussions about prognosis and goals of care.
    
    Risk Stratification and Clinical Implications:
    
    Low Risk (0-1 points):
    - Median survival: 319 days (approximately 10.5 months)
    - Treatment approach: May benefit from aggressive interventions
    - Interventions: Consider pleurodesis, indwelling pleural catheters, systemic therapy
    - Prognosis discussions: Focus on disease-directed treatment options
    - Clinical trials: Good candidates for experimental therapies
    - Follow-up: Regular oncology and pulmonology care coordination
    
    Moderate Risk (2-4 points):
    - Median survival: 130 days (approximately 4.3 months)  
    - Treatment approach: Individualized decision-making required
    - Interventions: Balance disease-directed and palliative approaches
    - Considerations: Patient preferences, quality of life priorities, functional status
    - Care planning: Early advance directive discussions appropriate
    - Monitoring: Close follow-up with reassessment of goals of care
    
    High Risk (5-7 points):
    - Median survival: 44 days (approximately 1.5 months)
    - Treatment approach: Focus on comfort care and symptom palliation
    - Interventions: Avoid overly aggressive procedures that may increase suffering
    - Priorities: Quality of life, symptom management, family support
    - Referrals: Early palliative care consultation strongly recommended
    - Planning: End-of-life care discussions and advance care planning
    
    Treatment Decision Framework:
    
    Pleural Interventions:
    - Low risk: Aggressive options (pleurodesis, indwelling catheters) appropriate
    - Moderate risk: Consider patient preferences and functional status
    - High risk: Minimally invasive approaches, repeated thoracentesis as needed
    
    Systemic Therapy:
    - Low risk: May benefit from anticancer treatment, clinical trial participation
    - Moderate risk: Individualized assessment of benefits vs. toxicities
    - High risk: Generally not recommended unless excellent performance status
    
    Palliative Care Integration:
    - Low risk: Concurrent palliative care for symptom management
    - Moderate risk: Early palliative care consultation for care planning
    - High risk: Primary palliative care approach with specialist involvement
    
    Communication and Counseling:
    - Provide clear, compassionate prognostic information
    - Discuss treatment options aligned with patient values and preferences
    - Address goals of care and quality of life priorities
    - Support family understanding and decision-making
    - Document discussions and care decisions
    
    Clinical Quality Measures:
    - Appropriate use of prognostic scoring in eligible patients
    - Integration of score results into treatment planning
    - Timely palliative care referral based on risk stratification
    - Patient and family education about prognosis and options
    - Coordination between oncology, pulmonology, and palliative care teams
    
    Limitations and Considerations:
    - Population-based estimates; individual outcomes may vary
    - Should complement clinical judgment, not replace comprehensive assessment
    - Regular reassessment needed as clinical status changes
    - Consider other factors: comorbidities, patient preferences, social support
    - Cultural and individual factors may influence treatment decisions
    
    Reference: Clive AO, et al. Thorax. 2014;69(12):1098-104.
    """
    
    result: int = Field(
        ...,
        description="LENT prognostic score calculated from clinical and laboratory parameters (range: 0-7 points)",
        example=3
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the prognostic score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Comprehensive clinical interpretation including risk stratification, survival estimates, "
                   "treatment recommendations, and care planning guidance for malignant pleural effusion",
        example="LENT Prognostic Score: 3 points. Risk category: Moderate Risk. Median survival: 130 days (approximately 4.3 months). Moderate risk group with intermediate prognosis. Treatment decisions should be individualized based on patient preferences, performance status, and goals of care. Consider palliative interventions to improve quality of life. Discussion about advance directives and care preferences is appropriate. Key prognostic factors include: elevated pleural fluid LDH (2200.0 U/L), and breast, gynecologic, or renal cell carcinoma. The LENT score should be used in conjunction with clinical judgment and patient preferences to guide treatment decisions. It is particularly useful for identifying patients who might benefit from less invasive interventions and for facilitating discussions about prognosis and goals of care."
    )
    
    stage: str = Field(
        ...,
        description="Risk category for mortality prediction (Low Risk, Moderate Risk, High Risk)",
        example="Moderate Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the risk category",
        example="Moderate risk of mortality"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 3,
                "unit": "points",
                "interpretation": "LENT Prognostic Score: 3 points. Risk category: Moderate Risk. Median survival: 130 days (approximately 4.3 months). Moderate risk group with intermediate prognosis. Treatment decisions should be individualized based on patient preferences, performance status, and goals of care. Consider palliative interventions to improve quality of life. Discussion about advance directives and care preferences is appropriate. Key prognostic factors include: elevated pleural fluid LDH (2200.0 U/L), and breast, gynecologic, or renal cell carcinoma. The LENT score should be used in conjunction with clinical judgment and patient preferences to guide treatment decisions. It is particularly useful for identifying patients who might benefit from less invasive interventions and for facilitating discussions about prognosis and goals of care.",
                "stage": "Moderate Risk",
                "stage_description": "Moderate risk of mortality"
            }
        }