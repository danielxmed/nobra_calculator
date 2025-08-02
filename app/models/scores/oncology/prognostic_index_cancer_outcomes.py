"""
Prognostic Index for Cancer Outcomes Models

Request and response models for Prognostic Index for Cancer Outcomes calculation.

References (Vancouver style):
1. Proctor MJ, McMillan DC, Morrison DS, Fletcher CD, Horgan PG, Clarke SJ. 
   A derived neutrophil to lymphocyte ratio predicts survival in patients with cancer. 
   Br J Cancer. 2012;107(4):695-9. doi: 10.1038/bjc.2012.292.
2. Proctor MJ, Morrison DS, Talwar D, Balmer SM, Fletcher CD, O'Reilly DS, et al. 
   A comparison of inflammation-based prognostic scores in patients with cancer. 
   A Glasgow Inflammation Outcome Study. Eur J Cancer. 2011;47(17):2633-41. 
   doi: 10.1016/j.ejca.2011.03.028.
3. McMillan DC. The systemic inflammation-based Glasgow Prognostic Score: a decade 
   of experience in patients with cancer. Cancer Treat Rev. 2013;39(5):534-40. 
   doi: 10.1016/j.ctrv.2012.08.003.

The Prognostic Index for Cancer Outcomes is a simple, validated scoring system that 
predicts cancer mortality using two readily available serum biomarkers: C-reactive 
protein (CRP) and white blood cell (WBC) count. This tool provides valuable prognostic 
information across multiple cancer types and helps guide clinical decision-making.
"""

from pydantic import BaseModel, Field
from typing import Literal


class PrognosticIndexCancerOutcomesRequest(BaseModel):
    """
    Request model for Prognostic Index for Cancer Outcomes calculation
    
    The Prognostic Index for Cancer Outcomes is a validated clinical tool designed 
    to predict cancer mortality using two fundamental inflammatory biomarkers: 
    C-reactive protein (CRP) and white blood cell (WBC) count. This simple yet 
    effective scoring system provides essential prognostic information to support 
    clinical decision-making across diverse cancer populations.
    
    Clinical Context and Rationale:
    
    Systemic inflammation plays a crucial role in cancer progression, metastasis, 
    and patient outcomes. The relationship between inflammatory markers and cancer 
    prognosis has been extensively studied, leading to the development of various 
    inflammation-based prognostic scores. The Prognostic Index for Cancer Outcomes 
    represents a simplified, practical approach that maintains strong predictive value 
    while using only two commonly available laboratory parameters.
    
    Historical Development and Validation:
    
    This prognostic index emerged from comprehensive research comparing various 
    inflammation-based scoring systems in cancer patients. The Glasgow Inflammation 
    Outcome Study and related research demonstrated that simple combinations of 
    inflammatory markers could effectively stratify cancer patients into distinct 
    prognostic groups. The two-parameter approach was selected for its balance 
    of simplicity, availability, and predictive accuracy across multiple cancer types.
    
    Biomarker Significance:
    
    C-reactive Protein (CRP):
    CRP is an acute-phase protein synthesized by the liver in response to inflammatory 
    cytokines, particularly interleukin-6 (IL-6). In cancer patients, elevated CRP 
    levels reflect:
    
    Tumor-Associated Inflammation:
    - Direct inflammatory response to tumor presence and growth
    - Release of pro-inflammatory cytokines by tumor cells and surrounding tissue
    - Activation of immune responses against malignant cells
    - Tissue necrosis and cellular damage associated with cancer progression
    
    Systemic Inflammatory Response:
    - Systemic activation of inflammatory pathways
    - Enhanced production of acute-phase proteins
    - Metabolic alterations associated with cancer cachexia
    - Immune system dysfunction and chronic inflammation
    
    Clinical Implications:
    Persistently elevated CRP (>10 mg/L) in cancer patients indicates:
    - Active inflammatory processes that may promote tumor growth
    - Potential for accelerated disease progression
    - Increased risk of complications and reduced treatment tolerance
    - Association with poorer overall survival across multiple cancer types
    
    White Blood Cell (WBC) Count:
    Elevated WBC count in cancer patients reflects various pathophysiological processes:
    
    Immune System Activation:
    - Natural immune response to malignant cells
    - Recruitment of inflammatory cells to tumor sites
    - Systemic immune activation in response to cancer antigens
    - Stress response to illness and treatment
    
    Disease-Related Factors:
    - Bone marrow involvement in hematologic malignancies
    - Paraneoplastic syndromes affecting white cell production
    - Secondary infections due to immunosuppression
    - Steroid effects from treatment or disease-related hormone production
    
    Treatment-Related Effects:
    - Recovery phase following chemotherapy-induced neutropenia
    - Growth factor administration (G-CSF, GM-CSF)
    - Corticosteroid therapy effects
    - Stress response to surgical interventions
    
    Clinical Interpretation and Risk Stratification:
    
    Score 0 (Low Risk - Both CRP ≤10 mg/L AND WBC ≤11 × 10⁹/L):
    - Clinical Significance: Minimal systemic inflammatory response
    - Prognosis: Generally favorable outcomes with better treatment tolerance
    - Management Focus: Standard oncologic care with routine monitoring
    - Survival Implications: Associated with longer overall survival
    - Monitoring: Regular assessment to detect changes in inflammatory status
    
    Score 1 (Intermediate Risk - Either CRP >10 mg/L OR WBC >11 × 10⁹/L):
    - Clinical Significance: Moderate inflammatory burden
    - Prognosis: Intermediate outcomes between low and high-risk groups
    - Management Focus: Enhanced supportive care and inflammation monitoring
    - Treatment Considerations: May benefit from anti-inflammatory interventions
    - Surveillance: More frequent assessment of inflammatory markers
    
    Score 2 (High Risk - Both CRP >10 mg/L AND WBC >11 × 10⁹/L):
    - Clinical Significance: Significant systemic inflammatory response
    - Prognosis: Associated with reduced survival and treatment resistance
    - Management Focus: Aggressive supportive care and symptom management
    - Treatment Implications: May require modified treatment approaches
    - Monitoring: Intensive surveillance and frequent reassessment
    
    Clinical Applications and Utility:
    
    Prognostic Assessment:
    The index provides valuable prognostic information that complements traditional 
    staging systems and performance status assessments. It helps clinicians:
    - Stratify patients into distinct prognostic groups
    - Identify patients at higher risk for poor outcomes
    - Guide discussions about prognosis and treatment goals
    - Support clinical trial stratification and research applications
    
    Treatment Planning:
    Integration of inflammatory status into treatment decisions enables:
    - Risk-adapted treatment approaches
    - Enhanced supportive care for high-risk patients
    - Consideration of anti-inflammatory interventions
    - Optimization of nutritional and metabolic support
    
    Monitoring and Follow-up:
    Serial assessment of the prognostic index allows:
    - Tracking of disease progression and treatment response
    - Early identification of deteriorating inflammatory status
    - Guidance for intervention timing and intensity
    - Quality improvement in cancer care delivery
    
    Limitations and Considerations:
    
    Clinical Context Dependency:
    - Results must be interpreted within the broader clinical context
    - Acute infections or inflammatory conditions may affect interpretation
    - Medication effects (corticosteroids, immunosuppressants) should be considered
    - Timing of assessment relative to treatment cycles is important
    
    Cancer Type Variability:
    - Prognostic significance may vary across different cancer types
    - Some malignancies may have disease-specific inflammatory patterns
    - Hematologic malignancies may require modified interpretation
    - Primary inflammatory conditions may confound results
    
    Treatment Era Considerations:
    - Original validation predates many modern immunotherapies
    - Immunotherapy may alter inflammatory marker patterns
    - Targeted therapies may have specific effects on biomarkers
    - Supportive care advances may modify prognostic relationships
    
    Integration with Other Prognostic Tools:
    
    Complementary Assessment:
    The Prognostic Index should be used alongside:
    - TNM staging and disease-specific prognostic factors
    - Performance status scales (ECOG, Karnofsky)
    - Laboratory assessments (albumin, hemoglobin, organ function)
    - Imaging studies and disease burden assessment
    
    Enhanced Risk Stratification:
    Combined use with other inflammation-based scores:
    - Glasgow Prognostic Score (GPS) using CRP and albumin
    - Modified Glasgow Prognostic Score (mGPS)
    - Neutrophil-to-lymphocyte ratio (NLR)
    - Platelet-to-lymphocyte ratio (PLR)
    
    Best Practices for Implementation:
    
    Standardized Assessment:
    - Obtain laboratory values during stable clinical periods when possible
    - Consider timing relative to acute illness, infections, or recent treatments
    - Document concurrent medications that may affect inflammatory markers
    - Ensure consistent laboratory methodology and reference ranges
    
    Clinical Integration:
    - Incorporate results into multidisciplinary team discussions
    - Use as part of comprehensive prognostic assessment
    - Consider serial monitoring to track changes over time
    - Integrate with patient and family discussions about prognosis
    
    Quality Assurance:
    - Validate local laboratory reference ranges and methodology
    - Train clinical staff on appropriate interpretation and application
    - Monitor outcomes to assess local predictive performance
    - Maintain awareness of factors that may affect biomarker interpretation
    
    References (Vancouver style):
    1. Proctor MJ, McMillan DC, Morrison DS, Fletcher CD, Horgan PG, Clarke SJ. 
    A derived neutrophil to lymphocyte ratio predicts survival in patients with cancer. 
    Br J Cancer. 2012;107(4):695-9. doi: 10.1038/bjc.2012.292.
    2. Proctor MJ, Morrison DS, Talwar D, Balmer SM, Fletcher CD, O'Reilly DS, et al. 
    A comparison of inflammation-based prognostic scores in patients with cancer. 
    A Glasgow Inflammation Outcome Study. Eur J Cancer. 2011;47(17):2633-41. 
    doi: 10.1016/j.ejca.2011.03.028.
    3. McMillan DC. The systemic inflammation-based Glasgow Prognostic Score: a decade 
    of experience in patients with cancer. Cancer Treat Rev. 2013;39(5):534-40. 
    doi: 10.1016/j.ctrv.2012.08.003.
    """
    
    crp: Literal["≤10", ">10"] = Field(
        ...,
        description="C-reactive protein (CRP) level category in mg/L. CRP is an acute-phase protein that reflects systemic inflammation. Levels ≤10 mg/L are considered normal, while >10 mg/L indicate elevated inflammatory response associated with worse cancer prognosis",
        example="≤10"
    )
    
    wbc_count: Literal["≤11", ">11"] = Field(
        ...,
        description="White blood cell (WBC) count category in ×10⁹/L. Elevated WBC count (>11 × 10⁹/L) may indicate immune activation, infection, or disease progression. Normal counts (≤11 × 10⁹/L) suggest less systemic inflammatory burden",
        example="≤11"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "crp": "≤10",
                "wbc_count": "≤11"
            }
        }


class PrognosticIndexCancerOutcomesResponse(BaseModel):
    """
    Response model for Prognostic Index for Cancer Outcomes calculation
    
    The Prognostic Index response provides critical risk stratification for cancer 
    patients based on inflammatory markers, enabling clinicians to make informed 
    decisions about prognosis, treatment planning, and supportive care interventions.
    
    Clinical Interpretation and Management Guidelines:
    
    Low Risk (Score 0 - Both CRP ≤10 mg/L AND WBC ≤11 × 10⁹/L):
    - Clinical Significance: Minimal systemic inflammatory response indicating 
      less aggressive disease and better potential for favorable outcomes
    - Prognosis: Generally good with better treatment tolerance and response rates
    - Management Strategy: Standard oncologic care with routine monitoring protocols
    - Supportive Care: Standard nutritional and symptomatic support
    - Monitoring Frequency: Regular assessment as per standard cancer care protocols
    - Patient Counseling: Reassuring prognostic information while maintaining 
      realistic expectations about cancer treatment
    - Quality of Life: Focus on maintaining functional status and normal activities
    
    Intermediate Risk (Score 1 - Either CRP >10 mg/L OR WBC >11 × 10⁹/L):
    - Clinical Significance: Moderate inflammatory burden suggesting intermediate 
      disease activity and prognosis between low and high-risk categories
    - Prognosis: Intermediate outcomes with variable treatment response patterns
    - Management Strategy: Enhanced monitoring with consideration of supportive 
      interventions to address inflammatory burden
    - Anti-inflammatory Considerations: Evaluate for appropriate anti-inflammatory 
      strategies if clinically indicated and compatible with cancer treatment
    - Nutritional Support: Enhanced nutritional assessment and intervention to 
      address inflammatory cachexia if present
    - Monitoring Frequency: More frequent assessment of inflammatory markers and 
      overall clinical status
    - Patient Counseling: Balanced prognostic discussions emphasizing the 
      intermediate nature of risk and potential for intervention
    
    High Risk (Score 2 - Both CRP >10 mg/L AND WBC >11 × 10⁹/L):
    - Clinical Significance: Significant systemic inflammatory response indicating 
      potentially aggressive disease with substantial inflammatory burden
    - Prognosis: Associated with reduced survival and increased treatment resistance
    - Management Strategy: Aggressive supportive care with intensive monitoring 
      and symptom management approaches
    - Infection Evaluation: Thorough assessment for underlying infections that 
      may contribute to inflammatory markers and require treatment
    - Nutritional Intervention: Intensive nutritional support to address 
      inflammation-associated cachexia and metabolic derangements
    - Supportive Care: Enhanced palliative care consultation and symptom management
    - Treatment Modifications: Consider dose modifications or alternative approaches 
      based on tolerance and performance status
    - Monitoring Frequency: Intensive surveillance with frequent reassessment 
      of clinical status and laboratory parameters
    - Patient and Family Support: Comprehensive discussions about prognosis and 
      goals of care with enhanced psychosocial support services
    
    Clinical Decision-Making Applications:
    
    Treatment Planning:
    - Risk-adapted treatment approaches based on inflammatory burden
    - Consideration of treatment intensity modifications for high-risk patients
    - Integration with performance status and comorbidity assessments
    - Enhanced pre-treatment optimization for patients with elevated scores
    
    Prognostic Discussions:
    - Structured framework for discussing prognosis with patients and families
    - Objective data to support clinical impressions about disease trajectory
    - Basis for shared decision-making about treatment goals and intensity
    - Support for palliative care and end-of-life planning when appropriate
    
    Monitoring and Follow-up:
    - Serial assessment to track inflammatory burden over time
    - Early identification of patients developing higher risk profiles
    - Guidance for timing and intensity of supportive care interventions
    - Quality metrics for cancer care programs and outcome assessment
    
    Research and Quality Improvement:
    - Stratification tool for clinical trials and research studies
    - Outcome prediction for healthcare resource planning
    - Quality improvement initiatives targeting high-risk patient populations
    - Biomarker development and validation studies
    
    Integration with Comprehensive Care:
    
    Multidisciplinary Team Coordination:
    - Oncology team awareness of inflammatory risk status
    - Palliative care consultation triggers for high-risk patients
    - Nutritionist involvement for inflammatory burden management
    - Social work and chaplaincy support for prognostic discussions
    
    Patient and Family Education:
    - Clear explanation of inflammatory markers and their significance
    - Discussion of modifiable factors that may influence inflammation
    - Preparation for potential complications and treatment challenges
    - Resources for coping with cancer prognosis and treatment decisions
    
    Healthcare System Integration:
    - Electronic health record integration for automated risk calculation
    - Clinical decision support tools incorporating prognostic information
    - Quality metrics and outcome tracking for patient populations
    - Care coordination pathways based on risk stratification
    
    Long-term Monitoring and Adaptation:
    
    Serial Assessment Value:
    - Tracking changes in inflammatory burden over disease course
    - Response to treatment reflected in biomarker improvements
    - Early detection of disease progression or treatment resistance
    - Guidance for adaptive treatment strategies
    
    Intervention Response:
    - Monitoring effectiveness of anti-inflammatory interventions
    - Assessment of nutritional and supportive care impact
    - Evaluation of treatment modifications on inflammatory status
    - Long-term outcome correlation with baseline and serial measurements
    
    Reference: Proctor MJ, et al. Eur J Cancer. 2011;47(17):2633-41.
    """
    
    result: int = Field(
        ...,
        description="Prognostic index score (0-2 points) based on inflammatory markers indicating cancer mortality risk",
        example=0
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Comprehensive clinical interpretation with management recommendations and prognostic guidance",
        example="GOOD PROGNOSIS (Score: 0): Minimal systemic inflammatory response with both CRP ≤10 mg/L and WBC ≤11 × 10⁹/L. This suggests less aggressive disease and better potential outcomes. CLINICAL SIGNIFICANCE: Lower inflammatory burden is associated with improved survival across multiple cancer types. MANAGEMENT: Continue standard oncologic care with regular monitoring. FOLLOW-UP: Monitor inflammatory markers during treatment to track response."
    )
    
    stage: str = Field(
        ...,
        description="Risk stratification category based on inflammatory burden",
        example="Low Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the inflammatory response level",
        example="Minimal inflammatory response"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 0,
                "unit": "points",
                "interpretation": "GOOD PROGNOSIS (Score: 0): Minimal systemic inflammatory response with both CRP ≤10 mg/L and WBC ≤11 × 10⁹/L. This suggests less aggressive disease and better potential outcomes. CLINICAL SIGNIFICANCE: Lower inflammatory burden is associated with improved survival across multiple cancer types. MANAGEMENT: Continue standard oncologic care with regular monitoring. FOLLOW-UP: Monitor inflammatory markers during treatment to track response.",
                "stage": "Low Risk",
                "stage_description": "Minimal inflammatory response"
            }
        }