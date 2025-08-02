"""
Prostate Tumor Volume & Density Models

Request and response models for Prostate Tumor Volume & Density calculation.

References (Vancouver style):
1. Terris MK, Stamey TA. Determination of prostate volume by transrectal 
   ultrasound. J Urol. 1991;145(5):984-7. doi: 10.1016/s0022-5347(17)38491-9.
2. Benson MC, Whang IS, Olsson CA, McMahon DJ, Cooner WH. The use of prostate 
   specific antigen density to enhance the predictive value of intermediate 
   levels of serum prostate specific antigen. J Urol. 1992;147(3 Pt 2):817-21. 
   doi: 10.1016/s0022-5347(17)37394-9.
3. Kalish J, Cooner WH, Graham SD Jr. Serum PSA adjusted for volume of transition 
   zone (PSATZ) is more accurate than PSA adjusted for total gland volume (PSAD) 
   in detecting adenocarcinoma of the prostate. Urology. 1994;43(5):601-6. 
   doi: 10.1016/0090-4295(94)90170-8.

The Prostate Tumor Volume & Density calculator provides essential measurements 
for prostate cancer risk assessment, combining volumetric analysis with PSA 
density calculations to enhance diagnostic accuracy beyond PSA alone.
"""

from pydantic import BaseModel, Field
from typing import Dict, Any


class ProstateTumorVolumeDensityRequest(BaseModel):
    """
    Request model for Prostate Tumor Volume & Density calculation
    
    The Prostate Tumor Volume & Density calculator represents a fundamental 
    tool in modern urological practice for evaluating prostate cancer risk 
    and guiding biopsy decisions. This comprehensive assessment combines 
    geometric volume calculations with biochemical markers to provide enhanced 
    diagnostic accuracy beyond PSA testing alone.
    
    Clinical Background and Significance:
    
    Prostate-specific antigen (PSA) testing has revolutionized prostate cancer 
    screening, but PSA levels can be elevated due to various benign conditions 
    including benign prostatic hyperplasia (BPH), prostatitis, and normal 
    age-related prostate growth. The concept of PSA density was developed to 
    account for prostate size and improve the specificity of PSA testing, 
    particularly in the diagnostic "gray zone" of PSA levels between 4-10 ng/mL.
    
    Historical Development:
    
    The ellipsoid formula for prostate volume calculation was established through 
    extensive correlation studies comparing transrectal ultrasound measurements 
    with actual prostate weights. The PSA density concept was introduced by 
    Benson and colleagues in 1992, who demonstrated that adjusting PSA levels 
    for prostate volume significantly improved the ability to distinguish 
    between benign and malignant conditions.
    
    Measurement Parameters and Clinical Significance:
    
    Prostate Length (Anteroposterior Diameter):
    The maximum anteroposterior dimension measured from the base to the apex 
    of the prostate. This measurement typically ranges from 2.5-4.5 cm in 
    normal adult males and increases with age and BPH development. Accurate 
    measurement requires proper transrectal ultrasound probe positioning 
    and identification of the prostatic capsule boundaries.
    
    Technical Considerations:
    - Measured in the sagittal plane at the point of maximum dimension
    - Should include the entire glandular tissue from base to apex
    - Accuracy depends on proper probe placement and tissue visualization
    - May be affected by bladder filling and patient positioning
    
    Prostate Width (Transverse Diameter):
    The maximum left-to-right dimension of the prostate measured in the 
    axial plane. This measurement reflects lateral prostatic enlargement 
    commonly seen in BPH and contributes significantly to total volume 
    calculation. Normal width typically ranges from 3.5-5.5 cm.
    
    Measurement Standards:
    - Obtained at the level of maximum transverse dimension
    - Should encompass the entire glandular tissue laterally
    - Important for detecting asymmetric enlargement patterns
    - May reveal focal lesions or irregular contours suspicious for malignancy
    
    Prostate Height (Craniocaudal Diameter):
    The superior-to-inferior dimension representing the vertical height of 
    the prostate. This measurement is particularly important as it reflects 
    the transition zone enlargement pattern typical of BPH. Normal height 
    ranges from 2.5-4.0 cm in healthy adults.
    
    Clinical Implications:
    - Reflects primarily transition zone enlargement in BPH
    - Important for predicting urinary obstruction symptoms
    - Correlates with bladder outlet obstruction severity
    - Essential for accurate volume calculations and treatment planning
    
    PSA Value (Prostate-Specific Antigen):
    Serum PSA level measured in ng/mL, representing the total PSA including 
    both free and complexed forms. PSA is produced exclusively by prostatic 
    epithelial cells and serves as a biomarker for prostate tissue volume, 
    inflammation, and malignancy. Normal values vary by age but generally 
    range from 0-4 ng/mL in men under 60 years.
    
    Factors Affecting PSA:
    - Age: Gradual increase with aging due to prostate growth
    - BPH: Proportional increase with enlarged prostate volume
    - Prostatitis: Acute elevation that may persist for weeks
    - Medications: 5-alpha reductase inhibitors reduce PSA by ~50%
    - Recent procedures: DRE, biopsy, or catheterization may elevate PSA
    - Ejaculation: May cause transient PSA elevation for 48-72 hours
    
    Volume Calculation Methodology:
    
    Ellipsoid Formula Application:
    The prostate volume is calculated using the ellipsoid formula: 
    Volume = Length × Width × Height × π/6 (≈0.52). This formula assumes 
    the prostate approximates an ellipsoid shape, which has been validated 
    through extensive correlation studies with actual prostate weights.
    
    Mathematical Basis:
    - π/6 ≈ 0.523599 (precise correction factor for ellipsoid volume)
    - Formula accounts for three-dimensional prostatic geometry
    - Validated against radical prostatectomy specimen weights
    - Accuracy: ±15-20% correlation with actual tissue volume
    - Superior to earlier formulas using different correction factors
    
    Clinical Volume Interpretation:
    - Normal: 25-30 mL (typical for men aged 40-50 years)
    - Mild enlargement: 30-50 mL (early BPH changes)
    - Moderate enlargement: 50-80 mL (symptomatic BPH)
    - Severe enlargement: >80 mL (significant obstruction likely)
    - Very large: >150 mL (candidate for surgical intervention)
    
    PSA Density Calculation and Interpretation:
    
    Calculation Method:
    PSA Density = PSA (ng/mL) ÷ Prostate Volume (mL)
    Result expressed in ng/mL/mL or ng/mL² (equivalent units)
    
    Clinical Thresholds and Risk Stratification:
    
    Low Risk (PSA Density <0.10 ng/mL²):
    - Cancer probability: <10% for clinically significant disease
    - Clinical action: Continue routine screening, consider active surveillance
    - Biopsy indication: Generally not recommended based on PSA density alone
    - Monitoring: Annual PSA with clinical correlation
    
    Intermediate Risk (PSA Density 0.10-0.15 ng/mL²):
    - Cancer probability: 10-25% for clinically significant disease
    - Clinical action: Consider additional risk factors and patient preferences
    - Biopsy indication: Individualized decision based on overall risk profile
    - Monitoring: More frequent PSA monitoring (6-12 months)
    
    High Risk (PSA Density 0.15-0.20 ng/mL²):
    - Cancer probability: 25-40% for clinically significant disease
    - Clinical action: Strong consideration for prostate biopsy
    - Biopsy indication: Generally recommended unless contraindicated
    - Monitoring: Close follow-up with urologic consultation
    
    Very High Risk (PSA Density >0.20 ng/mL²):
    - Cancer probability: >40% for clinically significant disease
    - Clinical action: Urgent urologic referral for biopsy consideration
    - Biopsy indication: Strongly recommended in appropriate candidates
    - Monitoring: Expedited evaluation and treatment planning
    
    Clinical Applications and Decision-Making:
    
    Biopsy Decision Support:
    PSA density provides crucial information for determining the need for 
    prostate biopsy, particularly in the PSA "gray zone" of 4-10 ng/mL 
    where cancer risk is uncertain. Studies demonstrate that PSA density 
    >0.15 ng/mL² significantly increases the likelihood of detecting 
    clinically significant prostate cancer on biopsy.
    
    Active Surveillance Criteria:
    For patients diagnosed with low-risk prostate cancer, PSA density 
    serves as a prognostic factor for disease progression. Lower PSA 
    density values support active surveillance approaches, while higher 
    values may indicate more aggressive disease requiring treatment.
    
    Treatment Planning:
    Prostate volume measurements guide treatment selection for BPH, 
    including medical therapy dosing, minimally invasive procedures, 
    and surgical planning. Large volumes (>80 mL) often require 
    different treatment approaches compared to smaller prostates.
    
    Integration with Advanced Diagnostics:
    
    Multiparametric MRI Correlation:
    PSA density correlates with PI-RADS scoring on multiparametric MRI 
    and helps determine the need for targeted biopsy. Higher PSA density 
    values increase the likelihood of significant lesions on MRI imaging.
    
    Biomarker Enhancement:
    PSA density can be combined with other biomarkers such as PSA velocity, 
    free/total PSA ratio, and novel markers (PHI, 4Kscore) to further 
    improve diagnostic accuracy and risk stratification.
    
    Genetic Risk Integration:
    Family history and genetic risk factors should be considered alongside 
    PSA density calculations, as hereditary prostate cancer may present 
    with different PSA patterns and require modified screening approaches.
    
    Limitations and Considerations:
    
    Measurement Accuracy:
    The accuracy of PSA density depends critically on precise prostate 
    volume measurements. Operator experience, equipment quality, and 
    measurement technique all affect reliability. Interobserver variability 
    can be 10-20% even among experienced practitioners.
    
    Clinical Context Dependency:
    PSA density should not be used in isolation but rather as part of 
    comprehensive clinical assessment including digital rectal examination, 
    patient symptoms, family history, and other risk factors.
    
    Temporal Considerations:
    PSA levels can fluctuate due to various factors, and volume measurements 
    may change with treatment or disease progression. Serial measurements 
    often provide more reliable information than single assessments.
    
    References (Vancouver style):
    1. Terris MK, Stamey TA. Determination of prostate volume by transrectal 
    ultrasound. J Urol. 1991;145(5):984-7. doi: 10.1016/s0022-5347(17)38491-9.
    2. Benson MC, Whang IS, Olsson CA, McMahon DJ, Cooner WH. The use of prostate 
    specific antigen density to enhance the predictive value of intermediate 
    levels of serum prostate specific antigen. J Urol. 1992;147(3 Pt 2):817-21. 
    doi: 10.1016/s0022-5347(17)37394-9.
    3. Kalish J, Cooner WH, Graham SD Jr. Serum PSA adjusted for volume of transition 
    zone (PSATZ) is more accurate than PSA adjusted for total gland volume (PSAD) 
    in detecting adenocarcinoma of the prostate. Urology. 1994;43(5):601-6. 
    doi: 10.1016/0090-4295(94)90170-8.
    """
    
    prostate_length: float = Field(
        ...,
        ge=1.0,
        le=20.0,
        description="Maximum anteroposterior (AP) diameter of prostate in centimeters, measured from base to apex. Typically ranges 2.5-4.5 cm in normal adults. Essential for accurate volume calculation and treatment planning",
        example=3.5
    )
    
    prostate_width: float = Field(
        ...,
        ge=1.0,
        le=20.0,
        description="Maximum transverse (left-right) diameter of prostate in centimeters, measured at widest point. Normal range 3.5-5.5 cm. Reflects lateral enlargement patterns and contributes significantly to total volume",
        example=4.2
    )
    
    prostate_height: float = Field(
        ...,
        ge=1.0,
        le=20.0,
        description="Maximum craniocaudal (superior-inferior) diameter of prostate in centimeters. Normal range 2.5-4.0 cm. Primarily reflects transition zone enlargement typical of benign prostatic hyperplasia",
        example=3.8
    )
    
    psa_value: float = Field(
        ...,
        ge=0.1,
        le=1000.0,
        description="Serum prostate-specific antigen (PSA) level in ng/mL. Biomarker for prostate tissue volume, inflammation, and malignancy. Normal values typically 0-4 ng/mL in men under 60, but varies with age",
        example=6.5
    )
    
    class Config:
        schema_extra = {
            "example": {
                "prostate_length": 3.5,
                "prostate_width": 4.2,
                "prostate_height": 3.8,
                "psa_value": 6.5
            }
        }


class ProstateTumorVolumeDensityResponse(BaseModel):
    """
    Response model for Prostate Tumor Volume & Density calculation
    
    The response provides comprehensive analysis of prostate measurements and 
    PSA density calculations, enabling evidence-based clinical decision-making 
    for prostate cancer risk assessment and treatment planning.
    
    Clinical Interpretation and Management Guidelines:
    
    Prostate Volume Assessment:
    The calculated prostate volume provides essential information for:
    - BPH severity assessment and treatment selection
    - Cancer risk stratification in context of PSA levels
    - Surgical planning and approach selection
    - Medical therapy dosing and effectiveness prediction
    - Long-term monitoring of prostate growth patterns
    
    Volume-Based Treatment Considerations:
    - Small prostates (<25 mL): Consider other causes of elevated PSA
    - Normal size (25-30 mL): Standard screening and evaluation protocols
    - Mild enlargement (30-50 mL): Early BPH management options
    - Moderate enlargement (50-80 mL): Comprehensive BPH evaluation
    - Severe enlargement (>80 mL): Surgical consultation recommended
    
    PSA Density Risk Stratification:
    
    Low Risk (PSA Density <0.10 ng/mL²):
    - Clinical Significance: Very low probability of clinically significant cancer
    - Management Approach: Continue routine screening with annual PSA
    - Biopsy Consideration: Generally not recommended based on density alone
    - Monitoring Strategy: Standard surveillance protocols appropriate
    - Patient Counseling: Reassuring risk profile, maintain regular screening
    
    Intermediate Risk (PSA Density 0.10-0.15 ng/mL²):
    - Clinical Significance: Moderate cancer risk requiring individualized assessment
    - Management Approach: Consider additional risk factors and patient preferences
    - Biopsy Consideration: Shared decision-making based on overall risk profile
    - Monitoring Strategy: More frequent PSA monitoring (6-12 month intervals)
    - Patient Counseling: Discuss benefits and risks of immediate vs. delayed biopsy
    
    High Risk (PSA Density 0.15-0.20 ng/mL²):
    - Clinical Significance: High probability of prostate cancer detection
    - Management Approach: Strong consideration for prostate biopsy
    - Biopsy Consideration: Generally recommended unless contraindicated
    - Monitoring Strategy: Close urologic follow-up with expedited evaluation
    - Patient Counseling: Discuss high cancer risk and biopsy benefits
    
    Very High Risk (PSA Density >0.20 ng/mL²):
    - Clinical Significance: Very high probability of clinically significant cancer
    - Management Approach: Urgent urologic referral for comprehensive evaluation
    - Biopsy Consideration: Strongly recommended in appropriate surgical candidates
    - Monitoring Strategy: Expedited workup and treatment planning
    - Patient Counseling: Discuss urgent need for definitive diagnosis
    
    Integrated Clinical Decision-Making:
    
    Biopsy Decision Framework:
    - PSA density >0.15: Strong biopsy recommendation
    - PSA density 0.10-0.15: Individualized decision based on additional factors
    - PSA density <0.10: Continue surveillance unless other high-risk features
    - Consider age, life expectancy, comorbidities, and patient preferences
    
    Additional Risk Factor Integration:
    - Family history of prostate/breast cancer: Lower threshold for biopsy
    - African American ethnicity: Increased surveillance and lower biopsy threshold
    - Previous negative biopsy: Consider PSA density trends over time
    - Abnormal DRE: Recommend biopsy regardless of PSA density
    
    Treatment Planning Applications:
    
    BPH Management:
    - Volume <30 mL: Medical therapy typically first-line
    - Volume 30-80 mL: Multiple treatment options available
    - Volume >80 mL: Consider surgical intervention
    - PSA reduction expected with 5-alpha reductase inhibitors
    
    Cancer Surveillance:
    - Active surveillance candidates: Monitor PSA density trends
    - Treatment decision-making: Volume affects surgical approach
    - Radiation planning: Prostate size influences technique selection
    - Post-treatment monitoring: Baseline for PSA interpretation
    
    Quality Assurance and Follow-up:
    
    Measurement Reliability:
    - Ensure consistent imaging technique and operator experience
    - Consider repeat measurements if results seem inconsistent
    - Document measurement methodology for future comparisons
    - Account for interobserver variability in clinical interpretation
    
    Temporal Monitoring:
    - Serial PSA density calculations provide trend information
    - Volume changes may indicate treatment response or disease progression
    - Consider medication effects on PSA levels (finasteride, dutasteride)
    - Timing of measurements relative to procedures or infections
    
    Patient Education and Counseling:
    
    Risk Communication:
    - Explain PSA density concept in understandable terms
    - Discuss individual risk profile in context of overall health
    - Address concerns about cancer risk and biopsy procedures
    - Provide realistic expectations about diagnostic accuracy
    
    Shared Decision-Making:
    - Present options for surveillance vs. immediate biopsy
    - Discuss benefits and risks of different management approaches
    - Consider patient values, preferences, and quality of life priorities
    - Involve family members in decision-making when appropriate
    
    Long-term Management:
    - Establish monitoring schedule based on risk stratification
    - Plan for potential treatment needs and referral pathways
    - Address lifestyle factors that may influence prostate health
    - Coordinate care between primary care and urology specialists
    
    Reference: Benson MC, et al. J Urol. 1992;147(3 Pt 2):817-21.
    """
    
    result: Dict[str, Any] = Field(
        ...,
        description="Comprehensive results including prostate volume, PSA density, and detailed interpretations",
        example={
            "prostate_volume": 58.7,
            "psa_density": 0.111,
            "volume_interpretation": {
                "stage": "Moderately Enlarged",
                "description": "Moderate benign prostatic hyperplasia",
                "interpretation": "Moderate enlargement, likely causing urinary symptoms."
            },
            "density_interpretation": {
                "stage": "Intermediate Risk",
                "description": "Intermediate cancer risk",
                "interpretation": "Moderate probability of prostate cancer, consider additional evaluation."
            }
        }
    )
    
    unit: str = Field(
        ...,
        description="Units of measurement for the calculated values",
        example="volume: mL, density: ng/mL²"
    )
    
    interpretation: str = Field(
        ...,
        description="Comprehensive clinical interpretation with management recommendations",
        example="PROSTATE VOLUME: 58.7 mL (Moderately Enlarged) - Moderate enlargement, likely causing urinary symptoms. PSA DENSITY: 0.111 ng/mL² (Intermediate Risk) - Moderate probability of prostate cancer, consider additional evaluation. CLINICAL CORRELATION: Large prostate volume may account for elevated PSA, reducing cancer suspicion. RECOMMENDATIONS: Monitor with serial PSA and consider advanced imaging. Consider clinical context, DRE findings, and patient risk factors for final management decisions."
    )
    
    stage: str = Field(
        ...,
        description="Risk stratification category based on PSA density",
        example="Intermediate Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description combining volume and density assessments",
        example="Volume: Moderately Enlarged, PSA Density: Intermediate Risk"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": {
                    "prostate_volume": 58.7,
                    "psa_density": 0.111,
                    "volume_interpretation": {
                        "stage": "Moderately Enlarged",
                        "description": "Moderate benign prostatic hyperplasia",
                        "interpretation": "Moderate enlargement, likely causing urinary symptoms."
                    },
                    "density_interpretation": {
                        "stage": "Intermediate Risk",
                        "description": "Intermediate cancer risk",
                        "interpretation": "Moderate probability of prostate cancer, consider additional evaluation."
                    }
                },
                "unit": "volume: mL, density: ng/mL²",
                "interpretation": "PROSTATE VOLUME: 58.7 mL (Moderately Enlarged) - Moderate enlargement, likely causing urinary symptoms. PSA DENSITY: 0.111 ng/mL² (Intermediate Risk) - Moderate probability of prostate cancer, consider additional evaluation. CLINICAL CORRELATION: Large prostate volume may account for elevated PSA, reducing cancer suspicion. RECOMMENDATIONS: Monitor with serial PSA and consider advanced imaging. Consider clinical context, DRE findings, and patient risk factors for final management decisions.",
                "stage": "Intermediate Risk",
                "stage_description": "Volume: Moderately Enlarged, PSA Density: Intermediate Risk"
            }
        }