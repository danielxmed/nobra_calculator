"""
Modified SOAR Score for Stroke Models

Request and response models for predicting short-term mortality in acute stroke.

References (Vancouver style):
1. Myint PK, Clark AB, Kwok CS, Loke YK, Yeong JK, Luben RN, et al. The SOAR 
   (Stroke subtype, Oxford Community Stroke Project classification, Age, prestroke 
   modified Rankin) score strongly predicts early outcomes in acute stroke. Int J 
   Stroke. 2014;9(3):278-83. doi: 10.1111/ijs.12088.
2. Abdul-Rahim AH, Fulton RL, Frank B, Tatlisumak T, Paciaroni M, Caso V, et al. 
   Association of improved outcome in acute ischaemic stroke patients with atrial 
   fibrillation who receive early antithrombotic therapy: analysis from VISTA. 
   Eur J Neurol. 2015;22(8):1048-55. doi: 10.1111/ene.12577.
3. Myint PK, Clark AB, Kwok CS, Loke YK, Yeong JK, Luben RN, et al. Derivation 
   and Validation of a Novel Prognostic Scale (Modified-Stroke Subtype, Oxfordshire 
   Community Stroke Project Classification, Age, and Prestroke Modified Rankin) to 
   Predict Early Mortality in Acute Stroke. J Am Heart Assoc. 2015;4(12):e002652. 
   doi: 10.1161/JAHA.115.002652.

The Modified SOAR Score improves upon the original SOAR criteria by incorporating 
stroke severity (NIHSS score), increasing the area under ROC curve from 0.79 to 0.83 
for early mortality prediction while maintaining clinical practicality.
"""

from pydantic import BaseModel, Field
from typing import Literal


class ModifiedSoarScoreRequest(BaseModel):
    """
    Request model for Modified SOAR Score for Stroke
    
    The Modified SOAR (mSOAR) Score predicts short-term mortality in acute stroke 
    patients by incorporating five clinical variables easily available at bedside:
    
    **Clinical Background:**
    
    **Stroke Prognostication Challenge:**
    - Accurate early prognosis is essential for clinical decision-making in acute stroke
    - Helps guide treatment intensity, family discussions, and resource allocation
    - Traditional prognostic factors often complex or require extensive testing
    - Need for simple, bedside-available tools for immediate clinical use
    
    **Evolution from SOAR to Modified SOAR:**
    - Original SOAR score included 4 variables (Stroke type, Oxfordshire classification, Age, prestroke Rankin)
    - Area under ROC curve of 0.79 for mortality prediction
    - Modified version adds NIHSS score as fifth variable
    - Improved area under ROC curve to 0.83 with better discrimination
    - Maintains simplicity while enhancing prognostic accuracy
    
    **Component Assessment:**
    
    **1. Age Category:**
    - **≤65 years (0 points)**: Younger patients with better physiologic reserve
    - **66-85 years (1 point)**: Middle-aged with moderate age-related risk
    - **≥85 years (2 points)**: Elderly with highest age-related mortality risk
    - Clinical significance: Age is strongest independent predictor of stroke outcomes
    - Physiologic basis: Reduced cerebral autoregulation, comorbidities, frailty
    - Practical application: Easily obtained from patient history or medical records
    
    **2. Stroke Subtype:**
    - **Ischemic (0 points)**: Generally better short-term prognosis
    - **Hemorrhagic (1 point)**: Higher early mortality risk
    - Assessment method: Clinical presentation plus neuroimaging (CT or MRI)
    - Clinical significance: Hemorrhagic strokes have 30-day mortality rates of 35-52%
    - Pathophysiology: Mass effect, increased intracranial pressure, perilesional edema
    - Important considerations: Includes intracerebral hemorrhage and subarachnoid hemorrhage
    
    **3. Oxfordshire Community Stroke Project Classification:**
    - **Partial Anterior Circulation/Lacunar (0 points)**: Smaller infarcts, better outcomes
    - **Posterior Circulation (1 point)**: Brainstem/cerebellar involvement, moderate risk
    - **Total Anterior Circulation (2 points)**: Large vessel occlusion, worst prognosis
    - Assessment basis: Clinical syndrome classification from initial examination
    - Neuroimaging correlation: Confirms anatomical location and extent
    - Prognostic value: Reflects both stroke size and functional importance of affected region
    
    **Detailed Oxfordshire Classification:**
    
    **Total Anterior Circulation Syndrome (TACS):**
    - All three of: hemiparesis, hemianopia, higher cortical dysfunction
    - Large vessel occlusion (internal carotid, proximal middle cerebral artery)
    - Highest mortality and dependency rates
    - Often requires intensive monitoring and intervention
    
    **Partial Anterior Circulation Syndrome (PACS):**
    - Two of three TACS criteria, or higher cortical dysfunction alone
    - Smaller cortical infarcts or subcortical involvement
    - More favorable prognosis than TACS
    - May still have significant functional impact
    
    **Posterior Circulation Syndrome (POCS):**
    - Brainstem, cerebellar, or occipital cortex involvement
    - Cranial nerve deficits, ataxia, bilateral weakness
    - Variable prognosis depending on location and extent
    - Risk of hydrocephalus, respiratory compromise
    
    **Lacunar Syndrome (LACS):**
    - Small subcortical infarcts (<15mm diameter)
    - Pure motor, pure sensory, or mixed deficits
    - Generally good prognosis for survival
    - Lower risk of early complications
    
    **4. Pre-stroke Modified Rankin Scale (mRS):**
    - **0-2 (0 points)**: Independent or minimally dependent baseline
    - **3-4 (1 point)**: Moderate to moderately severe disability
    - **5 (2 points)**: Severe disability, bedridden
    - Assessment focus: Functional status immediately before current stroke
    - Prognostic importance: Baseline function strongly predicts post-stroke outcomes
    - Clinical application: Often obtained from patient/family history or medical records
    
    **Detailed mRS Categories:**
    
    **mRS 0:** No symptoms at all
    **mRS 1:** No significant disability despite symptoms; able to carry out usual duties
    **mRS 2:** Slight disability; unable to carry out all previous activities but looks after own affairs
    **mRS 3:** Moderate disability; requires some help but walks without assistance
    **mRS 4:** Moderately severe disability; walks without assistance, unable to attend bodily needs
    **mRS 5:** Severe disability; bedridden, incontinent, requires constant nursing care
    
    **5. NIHSS Score (Modified Component):**
    - **1-4 points (0 mSOAR points)**: Mild stroke severity
    - **5-10 points (1 mSOAR point)**: Moderate stroke severity
    - **11-20 points (2 mSOAR points)**: Severe stroke severity
    - **≥21 points (2 mSOAR points)**: Very severe stroke severity
    - Assessment timing: Admission NIHSS score within first 24 hours
    - Clinical significance: Direct measure of neurological deficit severity
    - Prognostic value: Strong predictor of both mortality and functional outcomes
    
    **Clinical Applications:**
    
    **Emergency Department Use:**
    - Rapid prognostic assessment within first hours of presentation
    - Guides decisions about level of care (ICU vs. stroke unit vs. general ward)
    - Informs family discussions about expected outcomes
    - Helps prioritize resources in busy emergency settings
    
    **Stroke Unit Application:**
    - Daily prognostic updates as clinical condition evolves
    - Identifies patients requiring intensive monitoring
    - Supports multidisciplinary team decision-making
    - Assists with discharge planning and rehabilitation referrals
    
    **Research and Quality Improvement:**
    - Risk stratification for clinical trials
    - Quality metrics and outcome benchmarking
    - Resource utilization planning
    - Healthcare policy and guideline development
    
    **Limitations and Considerations:**
    
    **When to Use:**
    - Acute stroke patients within first 48-72 hours of symptom onset
    - When baseline functional status can be reliably determined
    - As adjunct to clinical judgment, not replacement
    - For prognostic discussions with patients and families
    
    **When NOT to Use:**
    - Transient ischemic attacks (TIAs) without persistent deficits
    - Stroke mimics or uncertain diagnoses
    - When baseline mRS cannot be reliably determined
    - As sole criterion for treatment decisions
    
    **Clinical Integration:**
    - Combine with other prognostic markers (biomarkers, advanced imaging)
    - Consider trajectory of improvement or deterioration
    - Account for patient preferences and values
    - Regular reassessment as clinical condition changes
    
    **Performance Characteristics:**
    - Area under ROC curve: 0.83 (95% CI: 0.79-0.86)
    - External validation AUC: 0.84 (95% CI: 0.82-0.88)
    - Mortality risk range: 3% (score 0-2) to >35% (score 7-9)
    - Validated across multiple healthcare systems and populations
    
    References (Vancouver style):
    1. Myint PK, Clark AB, Kwok CS, et al. The SOAR score strongly predicts early 
       outcomes in acute stroke. Int J Stroke. 2014;9(3):278-83.
    2. Myint PK, Clark AB, Kwok CS, et al. Derivation and Validation of a Novel 
       Prognostic Scale to Predict Early Mortality in Acute Stroke. J Am Heart Assoc. 
       2015;4(12):e002652.
    """
    
    age_category: Literal["65_or_less", "66_to_85", "85_or_more"] = Field(
        ...,
        description="Patient age category for stroke prognosis assessment. Age ≤65 years (0 points) represents younger patients with better physiologic reserve, 66-85 years (1 point) indicates moderate age-related risk, and ≥85 years (2 points) represents elderly patients with highest age-related mortality risk.",
        example="66_to_85"
    )
    
    stroke_subtype: Literal["ischemic", "hemorrhagic"] = Field(
        ...,
        description="Type of stroke based on clinical presentation and neuroimaging findings. Ischemic stroke (0 points) generally has better short-term prognosis, while hemorrhagic stroke (1 point) carries higher early mortality risk due to mass effect and increased intracranial pressure.",
        example="ischemic"
    )
    
    oxfordshire_classification: Literal["partial_anterior_lacunar", "posterior_circulation", "total_anterior_circulation"] = Field(
        ...,
        description="Oxfordshire Community Stroke Project classification based on clinical syndrome and neuroimaging. Partial anterior circulation/lacunar (0 points) represents smaller infarcts with better outcomes, posterior circulation (1 point) involves brainstem/cerebellar structures with moderate risk, and total anterior circulation (2 points) indicates large vessel occlusion with worst prognosis.",
        example="partial_anterior_lacunar"
    )
    
    prestroke_mrs: Literal["0_to_2", "3_to_4", "5"] = Field(
        ...,
        description="Pre-stroke modified Rankin Scale score indicating baseline functional status immediately before current stroke. Score 0-2 (0 points) represents independent or minimally dependent baseline, 3-4 (1 point) indicates moderate to moderately severe disability, and 5 (2 points) represents severe disability requiring constant care.",
        example="0_to_2"
    )
    
    nihss_score: int = Field(
        ...,
        ge=0,
        le=42,
        description="National Institutes of Health Stroke Scale score on admission assessing neurological deficit severity. Score 1-4 points (0 mSOAR points) indicates mild stroke, 5-10 points (1 mSOAR point) moderate stroke, 11-20 points (2 mSOAR points) severe stroke, and ≥21 points (2 mSOAR points) very severe stroke.",
        example=8
    )
    
    class Config:
        schema_extra = {
            "example": {
                "age_category": "66_to_85",
                "stroke_subtype": "ischemic",
                "oxfordshire_classification": "partial_anterior_lacunar",
                "prestroke_mrs": "0_to_2",
                "nihss_score": 8
            }
        }


class ModifiedSoarScoreResponse(BaseModel):
    """
    Response model for Modified SOAR Score for Stroke
    
    The mSOAR score ranges from 0-9 points and provides four risk stratification categories 
    for early stroke mortality prediction:
    
    **Risk Stratification Categories:**
    
    **Low Risk (Score 0-2): 3-7% Early Mortality**
    - Represents favorable prognostic profile with minimal risk factors
    - Good functional outcomes expected with standard stroke care
    - Appropriate for routine stroke unit management
    - Early mobilization and rehabilitation planning indicated
    - Family discussions should emphasize positive prognosis while acknowledging stroke risks
    
    **Moderate Risk (Score 3-4): 8-20% Early Mortality**
    - Indicates moderate stroke severity requiring enhanced monitoring
    - Close neurological assessments and complication surveillance needed
    - Consider more intensive nursing care and frequent vital sign monitoring
    - Multidisciplinary team involvement recommended
    - Prepare family for potential complications while maintaining realistic hope
    
    **High Risk (Score 5-6): 21-35% Early Mortality**
    - Represents severe stroke with significant mortality risk
    - Aggressive monitoring and proactive complication management warranted
    - Consider ICU-level care or high-dependency stroke unit
    - Early palliative care consultation may be beneficial
    - Comprehensive family discussions about prognosis and treatment goals essential
    
    **Very High Risk (Score 7-9): >35% Early Mortality**
    - Indicates very severe stroke with poor short-term prognosis
    - Immediate goals of care discussions with patient/family required
    - Palliative care consultation strongly recommended
    - Focus on comfort measures alongside medical management
    - Consider limitations of care based on patient/family preferences
    
    **Clinical Utility and Performance:**
    
    **Prognostic Accuracy:**
    - Area under ROC curve: 0.83 (95% CI: 0.79-0.86) in derivation cohort
    - External validation AUC: 0.84 (95% CI: 0.82-0.88)
    - Significant improvement over original SOAR score (AUC 0.79)
    - Maintained simplicity while enhancing discrimination
    
    **Advantages over Original SOAR:**
    - Addition of NIHSS improves prognostic accuracy without complexity
    - Better discrimination across all risk categories
    - Maintains bedside applicability and ease of use
    - Validated across diverse stroke populations and healthcare systems
    
    **Clinical Decision Support:**
    - Guides intensity of monitoring and intervention
    - Supports objective family communication about prognosis
    - Assists with resource allocation during capacity constraints
    - Helps identify patients for palliative care consultation
    - Useful for quality improvement and benchmarking
    
    **Implementation Considerations:**
    
    **Optimal Timing:**
    - Best applied within first 24-48 hours of stroke onset
    - Can be recalculated as clinical condition evolves
    - Most useful for initial prognostic assessment and care planning
    - Consider serial assessments for patients with changing clinical status
    
    **Multidisciplinary Integration:**
    - Stroke physicians: Treatment intensity decisions
    - Nursing staff: Monitoring protocols and family communication
    - Rehabilitation team: Early intervention planning
    - Social work: Discharge planning and family support
    - Palliative care: Symptom management and goals of care discussions
    
    **Quality Improvement Applications:**
    
    **Outcome Prediction:**
    - Risk-adjusted mortality statistics for quality reporting
    - Benchmark performance across different stroke centers
    - Identify opportunities for early intervention and improvement
    - Support evidence-based care protocols and pathways
    
    **Research Applications:**
    - Patient stratification for clinical trials
    - Outcome prediction modeling and validation studies
    - Health services research and resource utilization analysis
    - Development of integrated prognostic models
    
    **Limitations and Cautions:**
    
    **Appropriate Use:**
    - Should complement, not replace, clinical judgment
    - Consider trajectory of improvement or deterioration
    - Account for patient preferences and values in decision-making
    - Recognize individual variation in outcomes within risk categories
    
    **Factors Not Captured:**
    - Specific medical comorbidities and frailty status
    - Socioeconomic factors affecting recovery
    - Access to rehabilitation and support systems
    - Response to acute interventions and treatments
    
    **Future Directions:**
    - Integration with advanced imaging biomarkers
    - Combination with laboratory and genetic markers
    - Development of dynamic risk models with real-time updates
    - Artificial intelligence enhancement for improved accuracy
    
    Reference: Myint PK, et al. J Am Heart Assoc. 2015;4(12):e002652.
    """
    
    result: int = Field(
        ...,
        ge=0,
        le=9,
        description="Modified SOAR score ranging from 0-9 points predicting early stroke mortality risk",
        example=3
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Comprehensive clinical interpretation with mortality risk assessment, clinical management recommendations, and prognostic guidance based on mSOAR score category",
        example="Modified SOAR Score 3: Moderate risk of early mortality. The patient has an 8-20% risk of early mortality following acute stroke. This indicates moderate stroke severity requiring close monitoring and intensive nursing care."
    )
    
    stage: str = Field(
        ...,
        description="Risk category classification for early mortality",
        example="Moderate Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the mortality risk level",
        example="8-20% early mortality risk"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 3,
                "unit": "points",
                "interpretation": "Modified SOAR Score 3: Moderate risk of early mortality. The patient has an 8-20% risk of early mortality following acute stroke. This indicates moderate stroke severity requiring close monitoring and intensive nursing care. Consider more frequent neurological assessments and monitoring for complications such as brain edema, hemorrhagic transformation, or cardiac events.",
                "stage": "Moderate Risk",
                "stage_description": "8-20% early mortality risk"
            }
        }