"""
Modified Response Evaluation Criteria in Solid Tumors (mRECIST) Models

Request and response models for mRECIST assessment of treatment response in hepatocellular carcinoma.

References (Vancouver style):
1. Lencioni R, Llovet JM. Modified RECIST (mRECIST) assessment for hepatocellular 
   carcinoma. Semin Liver Dis. 2010;30(1):52-60. doi: 10.1055/s-0030-1247132.
2. Forner A, Ayuso C, Varela M, Rimola J, Burrel M, Darnell A, et al. Evaluation of 
   tumor response after locoregional therapies in hepatocellular carcinoma: are response 
   evaluation criteria in solid tumors reliable? Cancer. 2009;115(3):616-23. doi: 10.1002/cncr.24050.
3. Edeline J, Boucher E, Rolland Y, Vauleon E, Pracht M, Perrin C, et al. Comparison of 
   tumor response by Response Evaluation Criteria in Solid Tumors (RECIST) and modified 
   RECIST in patients treated with sorafenib for hepatocellular carcinoma. Cancer. 
   2012;118(1):147-56. doi: 10.1002/cncr.26255.

The Modified Response Evaluation Criteria in Solid Tumors (mRECIST) is specifically 
designed for hepatocellular carcinoma (HCC) and assesses treatment response based on 
viable tumor enhancement rather than just size changes. It is superior to standard 
RECIST 1.1 for HCC assessment, particularly with targeted therapies and locoregional 
treatments.
"""

from pydantic import BaseModel, Field
from typing import Literal


class ModifiedRecistRequest(BaseModel):
    """
    Request model for Modified Response Evaluation Criteria in Solid Tumors (mRECIST)
    
    The mRECIST criteria assess treatment response in hepatocellular carcinoma (HCC) 
    patients based on viable tumor enhancement patterns on contrast-enhanced imaging:
    
    **Key Concepts:**
    
    **Viable Tumor Definition:**
    - Tumor tissue showing uptake (enhancement) in the arterial phase of contrast-enhanced 
      CT or MRI imaging
    - Represents metabolically active, vascularized tumor tissue
    - Distinguished from necrotic, non-enhancing tissue induced by treatment
    - Must be accurately measurable (≥1.0 cm in diameter)
    
    **Target Lesion Selection:**
    - Up to 2 lesions per organ and up to 5 lesions total
    - Must be ≥1.0 cm in smallest diameter on cross-sectional imaging
    - Must show intratumoral arterial enhancement
    - Must be suitable for accurate repeated measurements
    - Should represent the most significant disease burden
    
    **Measurement Methodology:**
    - Perform measurements on CT or MRI obtained in arterial phase
    - Measure longest diameter of viable (enhancing) tumor tissue only
    - Exclude necrotic (non-enhancing) areas from measurements
    - Sum of all target lesion diameters used for response assessment
    - Baseline measurements establish reference for follow-up comparisons
    
    **Imaging Technical Requirements:**
    - Multiphase contrast-enhanced CT or MRI required
    - Arterial phase timing: 20-35 seconds after contrast injection for CT
    - Portal venous phase: 60-70 seconds after contrast injection
    - Consistent imaging protocol between baseline and follow-up studies
    - Same imaging modality recommended for serial assessments
    
    **Enhancement Assessment:**
    - **Present**: Target lesions show intratumoral arterial enhancement
    - **Absent**: Complete loss of arterial enhancement in all target lesions
    - **New Lesions**: Appearance of new enhancing lesions ≥1.0 cm
    
    **Clinical Applications:**
    
    **Treatment Response Monitoring:**
    - Particularly valuable for antiangiogenic therapies (sorafenib, regorafenib)
    - Locoregional treatments (TACE, TARE, ablation)
    - Immune checkpoint inhibitors and combination therapies
    - Clinical trial endpoint assessment
    
    **Timing of Assessment:**
    - European Association for the Study of the Liver (EASL) guidelines recommend 
      evaluation 1 month after treatment initiation
    - Follow-up assessments every 2-3 months during active treatment
    - Earlier assessment if clinical deterioration suspected
    - Post-treatment surveillance every 3-6 months
    
    **Advantages over Standard RECIST:**
    - Accounts for tumor necrosis induced by treatment
    - More accurately reflects antiangiogenic effects
    - Better correlation with overall survival outcomes
    - Identifies non-responders earlier in treatment course
    - Validated specifically for HCC patient population
    
    **Clinical Decision Making:**
    - Response assessment guides treatment continuation vs. modification
    - Progressive disease may warrant immediate treatment change
    - Stable disease can represent clinical benefit with targeted therapies
    - Complete/partial response supports treatment continuation
    
    **Quality Assurance:**
    - Consistent measurement technique across time points
    - Same radiologist review recommended when possible
    - Centralized imaging review for clinical trials
    - Documentation of enhancement patterns and measurement sites
    
    **Integration with Clinical Assessment:**
    - Combine with alpha-fetoprotein (AFP) levels when applicable
    - Consider clinical symptoms and physical examination
    - Evaluate liver function and performance status
    - Assess treatment-related adverse events
    
    References (Vancouver style):
    1. Lencioni R, Llovet JM. Modified RECIST (mRECIST) assessment for hepatocellular 
       carcinoma. Semin Liver Dis. 2010;30(1):52-60.
    2. Forner A, Ayuso C, Varela M, et al. Evaluation of tumor response after locoregional 
       therapies in hepatocellular carcinoma: are response evaluation criteria in solid 
       tumors reliable? Cancer. 2009;115(3):616-23.
    3. Edeline J, Boucher E, Rolland Y, et al. Comparison of tumor response by Response 
       Evaluation Criteria in Solid Tumors (RECIST) and modified RECIST in patients 
       treated with sorafenib for hepatocellular carcinoma. Cancer. 2012;118(1):147-56.
    """
    
    baseline_sum_diameters: float = Field(
        ...,
        ge=0.1,
        le=50.0,
        description="Sum of baseline diameters of viable (enhancing) target lesions in centimeters. Measured on arterial phase CT or MRI. Include only tumor tissue showing intratumoral arterial enhancement. Exclude necrotic (non-enhancing) areas.",
        example=5.2
    )
    
    current_sum_diameters: float = Field(
        ...,
        ge=0.0,
        le=50.0,
        description="Sum of current diameters of viable (enhancing) target lesions in centimeters. Measured using same technique as baseline. A value of 0.0 indicates complete loss of enhancement in all target lesions.",
        example=3.1
    )
    
    intratumoral_enhancement: Literal["present", "absent", "new_lesions"] = Field(
        ...,
        description="Assessment of intratumoral arterial enhancement status in target lesions. 'Present': target lesions show arterial phase enhancement. 'Absent': complete loss of enhancement in all targets (suggests complete response). 'New_lesions': appearance of new enhancing lesions ≥1.0 cm.",
        example="present"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "baseline_sum_diameters": 5.2,
                "current_sum_diameters": 3.1,
                "intratumoral_enhancement": "present"
            }
        }


class ModifiedRecistResponse(BaseModel):
    """
    Response model for Modified Response Evaluation Criteria in Solid Tumors (mRECIST)
    
    The mRECIST response assessment provides four standardized categories that guide 
    clinical decision-making in hepatocellular carcinoma treatment:
    
    **Response Categories and Clinical Significance:**
    
    **Complete Response (CR):**
    - Disappearance of any intratumoral arterial enhancement in all target lesions
    - Represents optimal treatment outcome with complete tumor devascularization
    - Associated with significantly improved overall survival
    - Achieved in 5-15% of patients with modern targeted therapies
    - Warrants continued current treatment with close monitoring
    
    **Partial Response (PR):**
    - At least 30% decrease in sum of diameters of viable target lesions
    - Indicates significant treatment efficacy with substantial tumor burden reduction
    - Correlates with improved progression-free and overall survival
    - Achieved in 10-25% of patients depending on treatment modality
    - Supports continuation of current therapeutic regimen
    
    **Stable Disease (SD):**
    - Neither sufficient shrinkage for PR nor sufficient increase for PD
    - Can represent meaningful clinical benefit, especially with targeted therapies
    - Disease stabilization may indicate slowed tumor progression
    - Consider duration of stable disease in clinical decision making
    - May warrant treatment continuation with regular reassessment
    
    **Progressive Disease (PD):**
    - At least 20% increase in sum of diameters of viable target lesions
    - Appearance of new lesions also constitutes progressive disease
    - Indicates treatment failure requiring immediate reassessment
    - Warrants consideration of alternative therapeutic approaches
    - Associated with poorer prognosis and reduced survival
    
    **Clinical Applications:**
    
    **Treatment Decision Making:**
    - CR/PR: Continue current treatment, monitor for sustained response
    - SD: Consider treatment continuation vs. modification based on duration
    - PD: Immediate treatment change, alternative therapy assessment
    
    **Prognostic Value:**
    - Early response (1-2 months) predicts long-term outcomes
    - mRECIST response correlates better with survival than standard RECIST
    - Response assessment helps stratify patients for clinical trials
    
    **Monitoring Strategy:**
    - Responders (CR/PR): Follow-up imaging every 2-3 months
    - Stable disease: More frequent assessment (monthly) initially
    - Progressive disease: Immediate reassessment and treatment modification
    
    **Integration with Other Assessments:**
    - Combine with alpha-fetoprotein (AFP) trends when applicable
    - Consider clinical symptoms and performance status
    - Evaluate treatment-related adverse events
    - Assess liver function parameters
    
    **Quality Metrics:**
    - Inter-observer reliability: κ > 0.8 for experienced radiologists
    - Reproducibility superior to standard RECIST in HCC patients
    - Validated across multiple treatment modalities and patient populations
    - Recommended by major hepatology societies (EASL, AASLD)
    
    Reference: Lencioni R, Llovet JM. Semin Liver Dis. 2010;30(1):52-60.
    """
    
    result: str = Field(
        ...,
        description="mRECIST response category based on viable tumor assessment",
        example="Partial Response"
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the assessment",
        example="response_category"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation with detailed assessment of treatment response, prognosis, and recommended management based on mRECIST criteria",
        example="mRECIST Partial Response: At least 30% decrease in the sum of diameters of viable (enhancement in arterial phase) target lesions (change: -40.4%). This indicates good treatment response with significant reduction in viable tumor burden. Partial response correlates with improved overall survival in HCC patients. Continue current treatment and reassess response in 1-2 months."
    )
    
    stage: str = Field(
        ...,
        description="Response category classification",
        example="Partial Response"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the response level",
        example="≥30% decrease in viable tumor"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": "Partial Response",
                "unit": "response_category",
                "interpretation": "mRECIST Partial Response: At least 30% decrease in the sum of diameters of viable (enhancement in arterial phase) target lesions (change: -40.4%). This indicates good treatment response with significant reduction in viable tumor burden. Partial response correlates with improved overall survival in HCC patients. Continue current treatment and reassess response in 1-2 months.",
                "stage": "Partial Response",
                "stage_description": "≥30% decrease in viable tumor"
            }
        }