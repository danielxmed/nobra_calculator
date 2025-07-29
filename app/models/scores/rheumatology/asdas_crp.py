"""
Ankylosing Spondylitis Disease Activity Score with CRP (ASDAS-CRP) Models

Request and response models for ASDAS-CRP disease activity assessment.

References (Vancouver style):
1. Lukas C, Landewé R, Sieper J, Dougados M, Davis J, Braun J, van der Linden S, 
   van der Heijde D. Development of an ASAS-endorsed disease activity score (ASDAS) 
   in patients with ankylosing spondylitis. Ann Rheum Dis. 2009 Jan;68(1):18-24. 
   doi: 10.1136/ard.2008.094870. PMID: 18625618.
2. van der Heijde D, Lie E, Kvien TK, Sieper J, van den Bosch F, Listing J, Braun J, 
   Landewé R. ASDAS, a highly discriminatory ASAS-endorsed disease activity score in 
   patients with ankylosing spondylitis. Ann Rheum Dis. 2009 Dec;68(12):1811-8. 
   doi: 10.1136/ard.2008.100826. PMID: 19060001.
3. Machado P, Landewé R, Lie E, Kvien TK, Braun J, Baker D, van der Heijde D. 
   Ankylosing Spondylitis Disease Activity Score (ASDAS): defining cut-off values 
   for disease activity states and improvement scores. Ann Rheum Dis. 2011 Jan;70(1):47-53. 
   doi: 10.1136/ard.2010.138594. PMID: 21068095.

The Ankylosing Spondylitis Disease Activity Score with CRP (ASDAS-CRP) is the gold 
standard, ASAS-endorsed outcome measure for assessing disease activity in ankylosing 
spondylitis and axial spondyloarthritis. Developed by Lukas et al. in 2009, this 
composite index combines patient-reported outcomes with an objective inflammatory marker.

Clinical Development and Validation:
The ASDAS was developed using data from multiple international cohorts and validated 
across diverse populations. It demonstrates superior discriminatory ability compared to 
traditional measures like BASDAI and is more responsive to clinical change, making it 
the preferred endpoint for clinical trials and routine clinical care.

Formula Components:
The ASDAS-CRP formula incorporates five key elements:
- **Back Pain** (0-10): Overall spinal pain intensity over the past week
- **Morning Stiffness Duration** (0-10): Severity of morning stiffness
- **Patient Global Assessment** (0-10): Overall disease activity perception
- **Peripheral Pain/Swelling** (0-10): Extra-spinal joint involvement
- **CRP**: Objective inflammatory marker (mg/L)

Mathematical Formula:
ASDAS-CRP = 0.12 × Back Pain + 0.06 × Morning Stiffness + 0.11 × Patient Global + 
            0.07 × Peripheral Pain + 0.58 × Ln(CRP+1)

Disease Activity States:
The ASDAS-CRP provides four clinically meaningful disease activity categories with 
established cut-offs that guide treatment decisions:
- **Inactive Disease (<1.3)**: Remission state, consider therapy optimization
- **Moderate Activity (1.3-2.1)**: May require treatment intensification
- **High Activity (2.1-3.5)**: Usually requires biological therapy
- **Very High Activity (>3.5)**: Urgent need for treatment modification

Clinical Applications:
- Treatment response monitoring (important improvement ≥1.1, major improvement ≥2.0)
- Therapeutic decision-making in clinical practice
- Primary endpoint in clinical trials and registries
- Assessment of sustained remission for treatment tapering decisions
- Evaluation of treat-to-target strategies in axial spondyloarthritis

The ASDAS-CRP is preferred over ASDAS-ESR due to lower variability of CRP and better 
discriminatory properties in detecting clinically meaningful changes in disease activity.
"""

from pydantic import BaseModel, Field
from typing import Union


class AsdasCrpRequest(BaseModel):
    """
    Request model for Ankylosing Spondylitis Disease Activity Score with CRP (ASDAS-CRP)
    
    The ASDAS-CRP assesses ankylosing spondylitis disease activity using 5 components:
    4 patient-reported outcomes (each scored 0-10) and C-reactive protein (mg/L).
    
    Patient-Reported Outcomes (0-10 numerical rating scale):
    
    1. **Back Pain** (0-10):
       - Question: "How would you describe the overall level of AS neck, back, or hip pain you have had?"
       - Assesses axial skeletal pain, the hallmark symptom of ankylosing spondylitis
       - 0 = No pain, 10 = Most severe pain imaginable
       - Reflects inflammatory back pain characteristic of axial spondyloarthritis
    
    2. **Morning Stiffness Duration** (0-10):
       - Question: "How would you describe the overall level of morning stiffness you have had from the time you wake up?"
       - Evaluates inflammatory stiffness, a key feature of AS
       - 0 = No stiffness, 10 = Most severe stiffness
       - Typically improves with activity and worsens with rest
    
    3. **Patient Global Assessment of Disease Activity** (0-10):
       - Question: "How active was your spondylitis, on average, during the last week?"
       - Captures patient's overall perception of disease activity
       - 0 = Not active at all, 10 = Most active possible
       - Integrates all aspects of disease impact from patient perspective
    
    4. **Peripheral Pain/Swelling** (0-10):
       - Question: "How would you describe the overall level of pain/swelling in joints other than neck, back, or hips you have had?"
       - Assesses extra-axial manifestations (peripheral arthritis)
       - 0 = No peripheral symptoms, 10 = Most severe peripheral involvement
       - Important for patients with concomitant peripheral arthritis
    
    5. **C-Reactive Protein (CRP)**:
       - Objective inflammatory biomarker measured in mg/L
       - Reflects systemic inflammation associated with disease activity
       - Should be measured using standardized high-sensitivity methods
       - Values typically range from <1 mg/L (normal) to >100 mg/L (severe inflammation)
    
    Clinical Context:
    The ASDAS-CRP should be assessed at regular intervals (every 3-6 months) to monitor 
    treatment response and guide therapeutic decisions. All patient-reported measures 
    should reflect symptoms over the past week for consistency and reliability.
    
    References (Vancouver style):
    1. Lukas C, Landewé R, Sieper J, Dougados M, Davis J, Braun J, et al. Development 
    of an ASAS-endorsed disease activity score (ASDAS) in patients with ankylosing 
    spondylitis. Ann Rheum Dis. 2009;68(1):18-24.
    2. van der Heijde D, Lie E, Kvien TK, Sieper J, van den Bosch F, Listing J, et al. 
    ASDAS, a highly discriminatory ASAS-endorsed disease activity score in patients 
    with ankylosing spondylitis. Ann Rheum Dis. 2009;68(12):1811-8.
    """
    
    back_pain: Union[int, float] = Field(
        ...,
        ge=0,
        le=10,
        description="Overall level of AS neck, back, or hip pain over the past week. Rate from 0 (no pain) to 10 (most severe pain). This assesses the characteristic inflammatory back pain of ankylosing spondylitis",
        example=4.5
    )
    
    morning_stiffness: Union[int, float] = Field(
        ...,
        ge=0,
        le=10,
        description="Overall level of morning stiffness from the time you wake up. Rate from 0 (no stiffness) to 10 (most severe stiffness). Morning stiffness is a hallmark feature of inflammatory arthritis and typically improves with movement",
        example=3.0
    )
    
    patient_global: Union[int, float] = Field(
        ...,
        ge=0,
        le=10,
        description="Patient global assessment: How active was your spondylitis on average during the last week? Rate from 0 (not active at all) to 10 (most active possible). This captures your overall perception of disease activity",
        example=5.0
    )
    
    peripheral_pain: Union[int, float] = Field(
        ...,
        ge=0,
        le=10,
        description="Overall level of pain/swelling in joints other than neck, back, or hips over the past week. Rate from 0 (no peripheral symptoms) to 10 (most severe peripheral involvement). This assesses extra-axial manifestations of AS",
        example=2.0
    )
    
    crp: Union[int, float] = Field(
        ...,
        ge=0,
        le=300,
        description="C-reactive protein (CRP) level in mg/L. This objective inflammatory biomarker should be measured using standardized laboratory methods. Normal values are typically <3 mg/L, with higher values indicating systemic inflammation",
        example=12.5
    )
    
    class Config:
        schema_extra = {
            "example": {
                "back_pain": 4.5,
                "morning_stiffness": 3.0,
                "patient_global": 5.0,
                "peripheral_pain": 2.0,
                "crp": 12.5
            }
        }


class AsdasCrpResponse(BaseModel):
    """
    Response model for Ankylosing Spondylitis Disease Activity Score with CRP (ASDAS-CRP)
    
    The ASDAS-CRP provides disease activity stratification with established cut-offs 
    that guide clinical management decisions:
    
    Disease Activity Categories and Clinical Management:
    
    **Inactive Disease (<1.3)**:
    - Clinical Significance: Disease remission state with minimal inflammatory activity
    - Management Strategy: Continue current effective therapy with regular monitoring
    - Treatment Considerations: 
      * Consider gradual tapering of biological therapy if sustained remission (≥6 months)
      * Maintain non-pharmacological interventions (physiotherapy, exercise)
      * Monitor for early signs of disease flare
    - Follow-up: Every 3-6 months with ASDAS assessment
    - Goals: Maintain remission and prevent structural damage progression
    
    **Moderate Disease Activity (1.3-2.1)**:
    - Clinical Significance: Low-moderate inflammatory activity requiring optimization
    - Management Strategy: Evaluate and optimize current treatment regimen
    - Treatment Considerations:
      * If on conventional therapy: Consider biological therapy initiation
      * If on biologics: Assess adherence and consider dose optimization or switching
      * Intensify physiotherapy and educational interventions
      * Address comorbidities and lifestyle factors
    - Follow-up: Every 3 months until target achieved
    - Goals: Achieve inactive disease or low disease activity
    
    **High Disease Activity (2.1-3.5)**:
    - Clinical Significance: Significant inflammatory burden requiring intervention
    - Management Strategy: Treatment intensification strongly recommended
    - Treatment Considerations:
      * Initiate biological therapy if treatment-naive
      * Switch biological agent if current therapy inadequate
      * Consider combination therapy or dose escalation
      * Evaluate for extra-articular manifestations
      * Assess functional impact and quality of life
    - Follow-up: Monthly monitoring until improvement achieved
    - Goals: Rapid reduction in disease activity to prevent complications
    
    **Very High Disease Activity (>3.5)**:
    - Clinical Significance: Severe inflammatory state requiring urgent intervention
    - Management Strategy: Immediate treatment modification necessary
    - Treatment Considerations:
      * Urgent rheumatology consultation if not already engaged
      * Rapid initiation or switching of biological therapy
      * Consider bridging corticosteroids if appropriate
      * Screen for complications (uveitis, IBD, cardiac involvement)
      * Evaluate for infection or other secondary causes
    - Follow-up: Close monitoring every 2-4 weeks initially
    - Goals: Urgent disease control to prevent irreversible damage
    
    Treatment Response Monitoring:
    The ASDAS-CRP is highly responsive to clinical changes, with established thresholds 
    for meaningful improvement:
    - **Clinically Important Improvement**: Decrease ≥1.1 units
    - **Major Improvement**: Decrease ≥2.0 units
    
    These thresholds help clinicians assess treatment efficacy and make informed 
    decisions about therapy continuation, optimization, or modification.
    
    Clinical Validation and Evidence:
    The ASDAS-CRP has been extensively validated in multiple populations and demonstrates:
    - Superior discriminatory ability compared to BASDAI
    - Strong correlation with imaging outcomes (MRI inflammation)
    - Excellent responsiveness to treatment in clinical trials
    - Reliable prediction of long-term outcomes
    
    The score is endorsed by ASAS (Assessment of SpondyloArthritis international Society) 
    and is the recommended outcome measure for clinical trials and routine clinical practice.
    
    Reference: Lukas C, et al. Ann Rheum Dis. 2009;68(1):18-24.
    """
    
    result: float = Field(
        ...,
        description="ASDAS-CRP score calculated using the validated formula: 0.12 × Back Pain + 0.06 × Morning Stiffness + 0.11 × Patient Global + 0.07 × Peripheral Pain + 0.58 × Ln(CRP+1)",
        example=2.45
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the ASDAS-CRP score",
        example="score"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation with specific treatment recommendations based on disease activity category and established management guidelines",
        example="High disease activity requiring treatment intensification. Consider starting or switching biological therapy (TNF inhibitors, IL-17 inhibitors, JAK inhibitors). Evaluate treatment adherence and optimize conventional therapy. Close monitoring required."
    )
    
    stage: str = Field(
        ...,
        description="Disease activity classification category (Inactive Disease, Moderate Disease Activity, High Disease Activity, Very High Disease Activity)",
        example="High Disease Activity"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the disease activity category",
        example="High ankylosing spondylitis activity"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 2.45,
                "unit": "score",
                "interpretation": "High disease activity requiring treatment intensification. Consider starting or switching biological therapy (TNF inhibitors, IL-17 inhibitors, JAK inhibitors). Evaluate treatment adherence and optimize conventional therapy. Close monitoring required.",
                "stage": "High Disease Activity",
                "stage_description": "High ankylosing spondylitis activity"
            }
        }