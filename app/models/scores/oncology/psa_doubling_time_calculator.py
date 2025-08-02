"""
PSA Doubling Time (PSADT) Calculator Models

Request and response models for PSA Doubling Time calculation.

References (Vancouver style):
1. D'Amico AV, Moul JW, Carroll PR, Sun L, Lubeck D, Chen MH. Surrogate end point 
   for prostate cancer-specific mortality after radical prostatectomy or radiation 
   therapy. J Natl Cancer Inst. 2003;95(18):1376-83. doi: 10.1093/jnci/djg043.
2. Freedland SJ, Humphreys EB, Mangold LA, Eisenberger M, Dorey FJ, Walsh PC, et al. 
   Risk of prostate cancer-specific mortality following biochemical recurrence after 
   radical prostatectomy. JAMA. 2005;294(4):433-9. doi: 10.1001/jama.294.4.433.
3. Pound CR, Partin AW, Eisenberger MA, Chan DW, Pearson JD, Walsh PC. Natural 
   history of progression after PSA elevation following radical prostatectomy. 
   JAMA. 1999;281(17):1591-7. doi: 10.1001/jama.281.17.1591.
4. Zhou P, Chen MH, McLeod D, Carroll PR, Moul JW, D'Amico AV. Predictors of 
   prostate cancer-specific mortality after radical prostatectomy or radiation 
   therapy. J Clin Oncol. 2005;23(28):6992-8. doi: 10.1200/JCO.2005.01.2906.

The PSA Doubling Time (PSADT) Calculator is a critical prognostic tool used in prostate 
cancer patients with biochemical recurrence after primary treatment (radical prostatectomy 
or radiation therapy). This calculator uses longitudinal PSA measurements to determine 
the rate of PSA increase over time, which strongly correlates with survival outcomes 
and helps guide treatment decisions.

Clinical Applications:
- Risk stratification for metastatic disease development
- Treatment decision-making for salvage therapy
- Timing of imaging studies (bone scans, CT scans)
- Monitoring during active surveillance
- Guidance for androgen deprivation therapy initiation
- Evaluation of castration-resistant disease progression
- Clinical trial stratification

The calculation uses linear regression analysis of the natural logarithm of PSA values 
versus time to determine the slope, from which PSADT is calculated using the formula: 
PSADT = ln(2) / slope. A minimum of 2 PSA measurements is required, though 3 or more 
measurements provide greater accuracy.

Risk Stratification:
- Very High Risk (<3 months): Aggressive disease requiring urgent intervention
- High Risk (3-6 months): Increased metastasis risk, consider aggressive treatment
- Intermediate Risk (6-12 months): Moderate risk requiring close monitoring
- Low Risk (12-36 months): Better prognosis, surveillance often appropriate
- Very Low Risk (>36 months): Excellent prognosis, active surveillance recommended

Clinical Note: PSADT should be interpreted in conjunction with other prognostic factors 
including Gleason score, time to biochemical recurrence, pre-treatment PSA, and patient 
age/comorbidities. Shorter doubling times (<6 months) are associated with increased risk 
of cancer-specific mortality and may warrant more aggressive intervention.
"""

from pydantic import BaseModel, Field
from typing import Optional


class PsaDoublingTimeCalculatorRequest(BaseModel):
    """
    Request model for PSA Doubling Time (PSADT) Calculator
    
    This calculator determines PSA doubling rate in prostate cancer patients with 
    biochemical recurrence after treatment. The tool requires a minimum of 2 PSA 
    measurements with their corresponding time points (days from baseline), with 
    support for up to 5 measurements for improved accuracy.
    
    PSA Measurement Requirements:
    - All PSA values must be positive (>0.01 ng/mL)
    - Time points represent days from a consistent baseline (usually first measurement)
    - Time intervals should be adequate to detect PSA changes (typically ≥3 months)
    - More measurements improve calculation accuracy and reliability
    - All time points must be unique and properly ordered
    
    Measurement Guidelines:
    - Use consistent laboratory and assay methodology
    - Account for measurement variability and laboratory precision
    - Consider clinical context (infections, medications affecting PSA)
    - Ensure adequate time intervals between measurements
    - Document any factors that might affect PSA levels
    
    Clinical Context:
    - Used only for patients with biochemical recurrence after treatment
    - Not applicable for initial screening or untreated patients
    - Results should be interpreted with Gleason score and other risk factors
    - Serial calculations may be needed as more data becomes available
    
    Quality Considerations:
    - Laboratory standardization is critical for accurate results
    - Consider PSA measurement precision (typically ±10-20%)
    - Account for biological variation in PSA levels
    - Ensure consistent sampling conditions and timing
    
    References: See module docstring for complete citation list.
    """
    
    psa_1: float = Field(
        ...,
        ge=0.01,
        le=10000.0,
        description="First PSA measurement in ng/mL. This establishes the baseline for progression assessment. Must be >0.01 ng/mL and typically represents the earliest detectable PSA after treatment.",
        example=0.5
    )
    
    days_1: int = Field(
        ...,
        ge=0,
        le=10000,
        description="Days from baseline for first PSA measurement. This is typically set to 0 as the reference point, or represents days from end of primary treatment.",
        example=0
    )
    
    psa_2: float = Field(
        ...,
        ge=0.01,
        le=10000.0,
        description="Second PSA measurement in ng/mL. Must be obtained at least 3 months after first measurement for reliable trend analysis. Should show measurable change from baseline.",
        example=1.2
    )
    
    days_2: int = Field(
        ...,
        ge=0,
        le=10000,
        description="Days from baseline for second PSA measurement. Should be sufficiently separated from first measurement (typically ≥90 days) to detect meaningful PSA trend.",
        example=180
    )
    
    psa_3: Optional[float] = Field(
        None,
        ge=0.01,
        le=10000.0,
        description="Third PSA measurement in ng/mL (optional). Adding a third measurement significantly improves calculation accuracy and helps confirm PSA trend reliability.",
        example=2.8
    )
    
    days_3: Optional[int] = Field(
        None,
        ge=0,
        le=10000,
        description="Days from baseline for third PSA measurement (optional). If provided, PSA_3 must also be provided. Recommended interval of 3-6 months from previous measurement.",
        example=360
    )
    
    psa_4: Optional[float] = Field(
        None,
        ge=0.01,
        le=10000.0,
        description="Fourth PSA measurement in ng/mL (optional). Additional measurements further improve accuracy and help identify any changes in PSA kinetics over time.",
        example=5.1
    )
    
    days_4: Optional[int] = Field(
        None,
        ge=0,
        le=10000,
        description="Days from baseline for fourth PSA measurement (optional). If provided, PSA_4 must also be provided. Continue regular monitoring intervals.",
        example=540
    )
    
    psa_5: Optional[float] = Field(
        None,
        ge=0.01,
        le=10000.0,
        description="Fifth PSA measurement in ng/mL (optional). Maximum supported measurement for this calculator. Provides most accurate trend analysis when all five points are available.",
        example=10.3
    )
    
    days_5: Optional[int] = Field(
        None,
        ge=0,
        le=10000,
        description="Days from baseline for fifth PSA measurement (optional). If provided, PSA_5 must also be provided. Represents the most recent measurement in the series.",
        example=720
    )
    
    class Config:
        schema_extra = {
            "example": {
                "psa_1": 0.5,
                "days_1": 0,
                "psa_2": 1.2,
                "days_2": 180,
                "psa_3": 2.8,
                "days_3": 360,
                "psa_4": 5.1,
                "days_4": 540,
                "psa_5": 10.3,
                "days_5": 720
            }
        }


class PsaDoublingTimeCalculatorResponse(BaseModel):
    """
    Response model for PSA Doubling Time (PSADT) Calculator
    
    The PSA Doubling Time represents the time required for PSA to double based on 
    the current rate of increase. This prognostic indicator is strongly correlated 
    with survival outcomes and helps guide treatment decisions in prostate cancer 
    patients with biochemical recurrence.
    
    Clinical Interpretation by Risk Category:
    
    Very High Risk (<3 months):
    - Indicates very aggressive disease with high metastatic potential
    - Associated with poor survival outcomes
    - Requires urgent treatment consideration and imaging evaluation
    - May warrant immediate systemic therapy initiation
    - Monthly PSA monitoring recommended
    
    High Risk (3-6 months):
    - Rapid PSA progression with increased mortality risk
    - Consider aggressive salvage therapy options
    - Imaging studies recommended to evaluate for metastases
    - Evaluate for clinical trial enrollment
    - Close monitoring with frequent PSA measurements
    
    Intermediate Risk (6-12 months):
    - Moderate risk requiring close surveillance
    - Treatment decisions based on patient factors and preferences
    - Consider salvage therapy options including radiation or hormonal therapy
    - Monitor PSA every 3-6 months with imaging as indicated
    
    Low Risk (12-36 months):
    - Better prognosis with lower risk of aggressive progression
    - Active surveillance often appropriate
    - PSA monitoring every 6 months typically sufficient
    - Treatment consideration if doubling time shortens or other risk factors emerge
    
    Very Low Risk (>36 months):
    - Excellent prognosis with minimal risk of clinical progression
    - Active surveillance with PSA monitoring every 6-12 months
    - Treatment typically deferred unless other high-risk features develop
    - Reassuring for patient counseling regarding disease trajectory
    
    Treatment Decision Guidance:
    - PSADT <6 months: Strong consideration for immediate intervention
    - PSADT 6-12 months: Individualized treatment decisions
    - PSADT >12 months: Active surveillance often appropriate
    - Consider patient age, comorbidities, and treatment goals
    
    Monitoring Recommendations:
    - PSADT should be recalculated as new PSA values become available
    - Changes in PSADT over time may indicate altered disease biology
    - Use in conjunction with imaging and other biomarkers
    - Document any factors that might influence PSA kinetics
    
    Reference: See module docstring for complete citation list.
    """
    
    result: float = Field(
        ...,
        description="PSA doubling time calculated using linear regression analysis of ln(PSA) vs time. Values are reported in months with range from very rapid progression (<3 months) to very slow progression (>36 months).",
        example=8.4
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for PSA doubling time",
        example="months"
    )
    
    interpretation: str = Field(
        ...,
        description="Comprehensive clinical interpretation including risk assessment, prognosis, treatment recommendations, and monitoring guidance based on calculated PSADT value.",
        example="Intermediate risk PSA progression. Moderate PSA doubling time indicates intermediate risk for progression requiring close monitoring and treatment consideration. Consider salvage therapy options based on patient factors and preferences. Monitor PSA every 3-6 months with imaging if indicated."
    )
    
    stage: str = Field(
        ...,
        description="Risk stratification category based on PSA doubling time (Very High Risk, High Risk, Intermediate Risk, Low Risk, Very Low Risk)",
        example="Intermediate Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the risk category and PSA progression rate",
        example="Moderate PSA progression"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 8.4,
                "unit": "months",
                "interpretation": "Intermediate risk PSA progression. Moderate PSA doubling time indicates intermediate risk for progression requiring close monitoring and treatment consideration. Consider salvage therapy options based on patient factors and preferences. Monitor PSA every 3-6 months with imaging if indicated.",
                "stage": "Intermediate Risk", 
                "stage_description": "Moderate PSA progression"
            }
        }