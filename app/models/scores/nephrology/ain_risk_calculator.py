"""
Acute Interstitial Nephritis (AIN) Risk Calculator Models

Request and response models for AIN Risk Calculator calculation.

References (Vancouver style):
1. Moledina DG, Luciano RL, Kukova L, Chan L, Shlipak MG, Sarnak MJ, et al. 
   Kidney biopsy-related complications in hospitalized patients with acute kidney disease. 
   Clin J Am Soc Nephrol. 2018 Nov 7;13(11):1633-1640. doi: 10.2215/CJN.04710418.
2. Moledina DG, Wilson FP, Kukova L, Luciano RL, Thiessen-Philbrook H, Shlipak MG, et al. 
   Prevalence and outcomes of kidney biopsy in hospitalized patients with acute kidney injury. 
   J Am Soc Nephrol. 2017 Apr;28(4):1342-1349. doi: 10.1681/ASN.2016050543.
3. Perazella MA, Moledina DG. Drug-induced acute interstitial nephritis. 
   Clin J Am Soc Nephrol. 2017 Dec 7;12(12):2046-2049. doi: 10.2215/CJN.07630717.

The AIN Risk Calculator is a clinical decision tool developed by Dr. Dennis G. Moledina 
at Yale School of Medicine to identify the likelihood of acute interstitial nephritis 
in patients being considered for kidney biopsy. This tool addresses a critical clinical 
challenge: distinguishing AIN from other causes of acute kidney injury using readily 
available clinical and laboratory parameters.

The calculator was developed using data from patients with biopsy-confirmed diagnoses 
from three major academic centers (Yale, Indiana University, and Johns Hopkins University) 
and validated externally with an AUC of 0.73-0.74 and a very high negative predictive 
value (>90%). This high NPV is particularly valuable for ruling out AIN and avoiding 
unnecessary biopsies or inappropriate treatments.

AIN is one of the few causes of AKI with diagnosis-specific management, including 
discontinuation of culprit medications and administration of corticosteroids. Early 
recognition and appropriate treatment can prevent permanent kidney damage, while 
misdiagnosis may lead to withdrawal of life-saving medications or administration 
of therapies with significant side effects.
"""

from pydantic import BaseModel, Field
from typing import Literal


class AinRiskCalculatorRequest(BaseModel):
    """
    Request model for Acute Interstitial Nephritis (AIN) Risk Calculator
    
    The AIN Risk Calculator uses five readily available clinical and laboratory 
    parameters to predict the probability of acute interstitial nephritis:
    
    Clinical Parameters and Their Significance:
    
    Serum Creatinine (mg/dL):
    - Range: 0.1-20.0 mg/dL
    - Higher creatinine levels may be associated with increased AIN risk
    - Essential marker of kidney function and AKI severity
    - Should be the peak creatinine during the acute episode
    
    Blood Urea Nitrogen - BUN (mg/dL):
    - Range: 1.0-300.0 mg/dL
    - Reflects both kidney function and volume status
    - BUN/creatinine ratio patterns may help distinguish AIN from other AKI causes
    - Important component of the overall clinical picture
    
    Urine Specific Gravity:
    - Range: 1.000-1.050
    - Lower specific gravity (more dilute urine) may suggest AIN
    - AIN typically causes concentrating defects due to tubular dysfunction
    - Helps differentiate from prerenal azotemia (which typically shows concentrated urine)
    
    Urine Dipstick Protein:
    - 1+ or lower: Minimal to mild proteinuria (associated with higher AIN probability)
    - 2+ or higher: Moderate to severe proteinuria (less typical for AIN)
    - AIN classically presents with minimal proteinuria compared to glomerular diseases
    - Heavy proteinuria suggests glomerular pathology rather than interstitial disease
    
    Local Prevalence of AIN:
    - Range: 0.01-1.0 (proportion, not percentage)
    - Institution-specific prevalence of AIN among all kidney biopsies
    - Default value: 0.23 (23%) if local data unavailable
    - Critical for Bayesian probability calculation
    - Reflects local patient population and referral patterns
    
    Clinical Context and Usage:
    - Should only be used for patients in whom kidney biopsy is being considered
    - Particularly useful when clinical presentation is ambiguous
    - Helps guide decisions about medication discontinuation and corticosteroid therapy
    - High negative predictive value (>90%) makes it excellent for ruling out AIN
    - Does not replace clinical judgment but provides objective probability assessment
    
    Limitations and Considerations:
    - Developed in hospitalized patients with acute kidney injury
    - May not apply to all patient populations or clinical settings
    - Should be interpreted in context of complete clinical picture
    - Kidney biopsy remains gold standard for definitive diagnosis
    
    References (Vancouver style):
    1. Moledina DG, Luciano RL, Kukova L, Chan L, Shlipak MG, Sarnak MJ, et al. 
    Kidney biopsy-related complications in hospitalized patients with acute kidney disease. 
    Clin J Am Soc Nephrol. 2018 Nov 7;13(11):1633-1640. doi: 10.2215/CJN.04710418.
    2. Moledina DG, Wilson FP, Kukova L, Luciano RL, Thiessen-Philbrook H, Shlipak MG, et al. 
    Prevalence and outcomes of kidney biopsy in hospitalized patients with acute kidney injury. 
    J Am Soc Nephrol. 2017 Apr;28(4):1342-1349. doi: 10.1681/ASN.2016050543.
    3. Perazella MA, Moledina DG. Drug-induced acute interstitial nephritis. 
    Clin J Am Soc Nephrol. 2017 Dec 7;12(12):2046-2049. doi: 10.2215/CJN.07630717.
    """
    
    creatinine: float = Field(
        ...,
        ge=0.1,
        le=20.0,
        description="Serum creatinine level in mg/dL. Peak creatinine during acute episode. Higher levels may indicate more severe AKI",
        example=2.5
    )
    
    bun: float = Field(
        ...,
        ge=1.0,
        le=300.0,
        description="Blood urea nitrogen level in mg/dL. Reflects kidney function and volume status. Important for BUN/creatinine ratio assessment",
        example=45.0
    )
    
    urine_specific_gravity: float = Field(
        ...,
        ge=1.000,
        le=1.050,
        description="Urine specific gravity measurement. Lower values (dilute urine) suggest concentrating defect typical of AIN. Range 1.000-1.050",
        example=1.010
    )
    
    urine_dipstick_protein: Literal["1_plus_or_lower", "2_plus_or_higher"] = Field(
        ...,
        description="Urine dipstick protein level. AIN typically shows minimal proteinuria (1+ or lower). Heavy proteinuria (2+ or higher) suggests glomerular disease",
        example="1_plus_or_lower"
    )
    
    local_prevalence_ain: float = Field(
        ...,
        ge=0.01,
        le=1.0,
        description="Local prevalence of AIN among all kidney biopsies as a proportion (0.01-1.0). Use 0.23 if unknown. Critical for accurate probability calculation",
        example=0.23
    )
    
    class Config:
        schema_extra = {
            "example": {
                "creatinine": 2.5,
                "bun": 45.0,
                "urine_specific_gravity": 1.010,
                "urine_dipstick_protein": "1_plus_or_lower",
                "local_prevalence_ain": 0.23
            }
        }


class AinRiskCalculatorResponse(BaseModel):
    """
    Response model for Acute Interstitial Nephritis (AIN) Risk Calculator
    
    The AIN Risk Calculator provides a probability score (0.0-1.0) that stratifies 
    patients into three risk categories for acute interstitial nephritis:
    
    Risk Categories and Clinical Interpretation:
    
    Low Risk (Probability < 0.2 or 20%):
    - AIN is unlikely with high confidence
    - Negative predictive value >90%
    - Focus evaluation on alternative AKI causes
    - Consider prerenal azotemia, acute tubular necrosis, or glomerular diseases
    - Kidney biopsy less likely to show AIN
    
    Intermediate Risk (Probability 0.2-0.5 or 20-50%):
    - Moderate probability requiring clinical correlation
    - Additional testing may be helpful (urinalysis with microscopy, eosinophiluria)
    - Careful medication history review essential
    - Kidney biopsy consideration based on clinical judgment
    - May warrant empirical trial of corticosteroids in appropriate clinical context
    
    High Risk (Probability ≥ 0.5 or ≥50%):
    - High likelihood of AIN
    - Strong consideration for immediate intervention:
      * Discontinue potentially causative medications (NSAIDs, antibiotics, PPIs, diuretics)
      * Initiate corticosteroid therapy if no contraindications
      * Consider urgent nephrology consultation
    - Kidney biopsy may confirm diagnosis but should not delay treatment
    - Early intervention critical to prevent permanent kidney damage
    
    Clinical Decision Making:
    - Probabilities should guide but not replace clinical judgment
    - Consider patient-specific factors (comorbidities, medication history, clinical course)
    - Integrate with other diagnostic information (urinalysis, imaging, clinical presentation)
    - High NPV makes this tool particularly useful for ruling out AIN
    - Helps optimize use of kidney biopsy resources
    
    Treatment Implications:
    - AIN-specific therapy includes medication discontinuation and corticosteroids
    - Early recognition and treatment can prevent chronic kidney disease
    - Delayed diagnosis may result in irreversible kidney damage
    - False positive diagnosis may lead to unnecessary medication withdrawal or steroid exposure
    
    Reference: Moledina DG, et al. Clin J Am Soc Nephrol. 2018;13(11):1633-1640.
    """
    
    result: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Probability of acute interstitial nephritis (0.0-1.0). Values closer to 1.0 indicate higher likelihood of AIN",
        example=0.325
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the probability score",
        example="probability"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation and recommended management approach based on the AIN probability",
        example="Moderate probability of AIN (20-50%). Clinical correlation is essential. Consider additional testing including urinalysis with microscopy, eosinophiluria, and careful medication history review. Kidney biopsy may be warranted based on clinical judgment, especially if AIN-specific therapy (corticosteroids) is being considered."
    )
    
    stage: str = Field(
        ...,
        description="Risk category based on AIN probability (Low Risk, Intermediate Risk, High Risk)",
        example="Intermediate Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the probability range for this risk category",
        example="Intermediate probability of AIN"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 0.325,
                "unit": "probability",
                "interpretation": "Moderate probability of AIN (20-50%). Clinical correlation is essential. Consider additional testing including urinalysis with microscopy, eosinophiluria, and careful medication history review. Kidney biopsy may be warranted based on clinical judgment, especially if AIN-specific therapy (corticosteroids) is being considered.",
                "stage": "Intermediate Risk",
                "stage_description": "Intermediate probability of AIN"
            }
        }