"""
D'Amico Risk Classification for Prostate Cancer Models

Request and response models for D'Amico risk classification calculation.

References (Vancouver style):
1. D'Amico AV, Whittington R, Malkowicz SB, et al. Biochemical outcome after radical 
   prostatectomy, external beam radiation therapy, or interstitial radiation therapy 
   for clinically localized prostate cancer. JAMA. 1998;280(11):969-974. 
   doi: 10.1001/jama.280.11.969.
2. D'Amico AV, Whittington R, Malkowicz SB, et al. Clinical utility of the percentage 
   of positive prostate biopsies in defining biochemical outcome after radical 
   prostatectomy for patients with clinically localized prostate cancer. J Clin Oncol. 
   2000;18(6):1164-1172. doi: 10.1200/JCO.2000.18.6.1164.
3. Zumsteg ZS, Spratt DE, Pei I, et al. A new risk classification system for therapeutic 
   decision making with intermediate-risk prostate cancer patients undergoing 
   dose-escalated external-beam radiation therapy. Eur Urol. 2013;64(6):895-902. 
   doi: 10.1016/j.eururo.2013.03.033.
4. National Comprehensive Cancer Network. NCCN Clinical Practice Guidelines in Oncology: 
   Prostate Cancer. Version 2.2024. https://www.nccn.org/professionals/physician_gls/pdf/prostate.pdf.

The D'Amico Risk Classification for Prostate Cancer is a widely used risk stratification 
system that categorizes patients with clinically localized prostate cancer into low, 
intermediate, or high-risk groups based on three readily available clinical parameters: 
pretreatment prostate-specific antigen (PSA) level, biopsy Gleason score, and clinical 
tumor (T) stage.

Developed in 1998 by Anthony V. D'Amico and colleagues, this classification system was 
originally designed to predict the risk of biochemical recurrence following definitive 
local therapy for prostate cancer. The system has become the foundation for treatment 
decision-making and is incorporated into major clinical practice guidelines including 
those from the National Comprehensive Cancer Network (NCCN), European Association of 
Urology (EAU), and American Urological Association (AUA).

The D'Amico classification provides a simple yet effective framework for clinicians 
to counsel patients about prognosis, guide treatment selection, and stratify patients 
for clinical trials. Its widespread adoption reflects its clinical utility and the 
importance of risk-stratified care in prostate cancer management.
"""

from pydantic import BaseModel, Field
from typing import Literal, Optional, List, Dict


class DamicoRiskClassificationRequest(BaseModel):
    """
    Request model for D'Amico Risk Classification for Prostate Cancer
    
    The D'Amico Risk Classification stratifies patients with clinically localized 
    prostate cancer into three risk groups using three key clinical parameters 
    that are routinely available at the time of diagnosis.
    
    **Clinical Parameters:**
    
    **PSA Level (Prostate-Specific Antigen):**
    - psa_level: Pretreatment serum PSA level in ng/mL
    - Normal range: Typically <4 ng/mL in healthy men
    - Risk thresholds: ≤10 (low), 10-20 (intermediate), >20 (high)
    - Considerations: Age-adjusted normal values, medications affecting PSA, 
      prostate volume, recent procedures, and inflammation
    
    **Gleason Score:**
    - gleason_score: Histologic grading system based on prostate biopsy
    - Scale: 2-10 (sum of primary and secondary Gleason patterns)
    - Risk thresholds: ≤6 (low), 7 (intermediate), ≥8 (high)
    - Modern reporting: Gleason 6 is well-differentiated, 7 is moderately 
      differentiated, 8-10 is poorly differentiated
    - Grade Groups: WHO/ISUP Grade Groups 1-5 correspond to specific Gleason scores
    
    **Clinical Stage (TNM System):**
    - clinical_stage: Clinical tumor stage based on digital rectal examination 
      and imaging studies
    - T1a/T1b: Incidental finding in tissue removed for benign disease
    - T1c: Needle biopsy finding due to elevated PSA
    - T2a: Involves ≤50% of one lobe
    - T2b: Involves >50% of one lobe  
    - T2c: Involves both lobes
    - T3a: Extracapsular extension (unilateral or bilateral)
    - T3b: Invades seminal vesicle(s)
    - T4: Fixed or invades adjacent structures
    
    **Risk Group Definitions:**
    
    **Low Risk:** ALL of the following criteria must be met:
    - PSA ≤10 ng/mL AND
    - Gleason score ≤6 AND  
    - Clinical stage T1-T2a
    
    **Intermediate Risk:** ANY of the following criteria:
    - PSA 10-20 ng/mL OR
    - Gleason score 7 OR
    - Clinical stage T2b
    
    **High Risk:** ANY of the following criteria:
    - PSA >20 ng/mL OR
    - Gleason score ≥8 OR
    - Clinical stage ≥T2c
    
    **Clinical Applications:**
    - Treatment decision-making and patient counseling
    - Risk stratification for clinical trials
    - Active surveillance eligibility assessment
    - Treatment intensity determination
    - Prognosis estimation and follow-up planning
    
    **Limitations:**
    - Based on traditional clinical parameters only
    - Does not incorporate newer imaging (mpMRI) or genomic markers
    - Intermediate risk group is heterogeneous and may benefit from substratification
    - Developed before widespread PSA screening era
    
    References (Vancouver style):
    1. D'Amico AV, Whittington R, Malkowicz SB, et al. Biochemical outcome after radical 
    prostatectomy, external beam radiation therapy, or interstitial radiation therapy 
    for clinically localized prostate cancer. JAMA. 1998;280(11):969-974. 
    doi: 10.1001/jama.280.11.969.
    2. National Comprehensive Cancer Network. NCCN Clinical Practice Guidelines in Oncology: 
    Prostate Cancer. Version 2.2024.
    """
    
    psa_level: float = Field(
        ...,
        ge=0.1,
        le=500.0,
        description="Preoperative prostate-specific antigen (PSA) level in ng/mL. Normal <4 ng/mL, risk thresholds: ≤10 (low), 10-20 (intermediate), >20 (high)",
        example=8.5
    )
    
    gleason_score: int = Field(
        ...,
        ge=2,
        le=10,
        description="Biopsy Gleason score (sum of primary and secondary patterns). Risk thresholds: ≤6 (low grade), 7 (intermediate grade), ≥8 (high grade)",
        example=6
    )
    
    clinical_stage: Literal["T1a", "T1b", "T1c", "T2a", "T2b", "T2c", "T3a", "T3b", "T4"] = Field(
        ...,
        description="Clinical tumor (T) stage based on digital rectal examination and imaging. Risk thresholds: T1-T2a (low), T2b (intermediate), ≥T2c (high)",
        example="T1c"
    )
    
    patient_age: Optional[int] = Field(
        None,
        ge=40,
        le=100,
        description="Patient age in years for additional prognostic context and treatment planning considerations",
        example=65
    )
    
    treatment_planned: Optional[Literal["radical_prostatectomy", "external_beam_radiation", "brachytherapy", "active_surveillance", "not_specified"]] = Field(
        None,
        description="Planned treatment modality for additional clinical context and treatment-specific recommendations",
        example="radical_prostatectomy"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "psa_level": 8.5,
                "gleason_score": 6,
                "clinical_stage": "T1c",
                "patient_age": 65,
                "treatment_planned": "radical_prostatectomy"
            }
        }


class DamicoRiskClassificationResponse(BaseModel):
    """
    Response model for D'Amico Risk Classification for Prostate Cancer
    
    Provides comprehensive risk assessment with D'Amico classification, biochemical 
    recurrence risk estimation, treatment recommendations, and prognostic information 
    for patients with clinically localized prostate cancer.
    
    **Risk Group Classifications:**
    
    **Low Risk:**
    - Criteria: PSA ≤10 ng/mL AND Gleason score ≤6 AND clinical stage T1-T2a
    - 5-year biochemical recurrence risk: 5-15%
    - Prognosis: Excellent (>95% 10-year disease-specific survival)
    - Treatment options: Active surveillance, radical prostatectomy, radiation therapy
    
    **Intermediate Risk:**
    - Criteria: PSA 10-20 ng/mL OR Gleason score 7 OR clinical stage T2b
    - 5-year biochemical recurrence risk: 15-45%
    - Prognosis: Good to very good (85-95% 10-year disease-specific survival)
    - Treatment: Definitive local therapy typically recommended
    
    **High Risk:**
    - Criteria: PSA >20 ng/mL OR Gleason score ≥8 OR clinical stage ≥T2c
    - 5-year biochemical recurrence risk: 45-65%
    - Prognosis: Guarded to good (60-85% 10-year disease-specific survival)
    - Treatment: Multimodal therapy often recommended
    
    **Treatment Implications:**
    
    **Low Risk Management:**
    - Active surveillance is appropriate for many patients
    - Radical prostatectomy offers excellent cure rates
    - External beam radiation provides equivalent outcomes
    - Brachytherapy is effective for suitable candidates
    
    **Intermediate Risk Management:**
    - Definitive local therapy typically recommended
    - Consider adjuvant or neoadjuvant therapy
    - Multidisciplinary consultation valuable
    
    **High Risk Management:**
    - Aggressive multimodal therapy recommended
    - Radiation with long-term androgen deprivation therapy
    - Radical surgery with extended lymph node dissection
    - Close surveillance for recurrence
    
    Reference: D'Amico AV, et al. JAMA. 1998;280(11):969-974.
    """
    
    result: str = Field(
        ...,
        description="D'Amico risk group classification (low, intermediate, high)",
        example="low"
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the risk classification",
        example="risk group"
    )
    
    interpretation: str = Field(
        ...,
        description="Comprehensive clinical interpretation with risk assessment, prognosis, and treatment guidance",
        example="D'Amico Low Risk classification based on PSA 8.5 ng/mL, Gleason score 6, and clinical stage T1c. Patient has excellent prognosis with 5-15% 5-year biochemical recurrence risk. Active surveillance may be appropriate for select patients, though definitive treatment offers excellent cure rates."
    )
    
    stage: str = Field(
        ...,
        description="Risk group classification with descriptive label",
        example="Low Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the risk category characteristics",
        example="Low risk of treatment failure"
    )
    
    risk_group: str = Field(
        ...,
        description="D'Amico risk group (low, intermediate, high)",
        example="low"
    )
    
    risk_category: str = Field(
        ...,
        description="Full risk category name with descriptive label",
        example="Low Risk"
    )
    
    criteria_met: str = Field(
        ...,
        description="Specific D'Amico criteria that define this risk group",
        example="PSA ≤10 ng/mL AND Gleason score ≤6 AND clinical stage T1-T2a"
    )
    
    biochemical_recurrence_risk: str = Field(
        ...,
        description="Risk category for biochemical recurrence with percentage range",
        example="Low (5-15%)"
    )
    
    five_year_recurrence_rate: str = Field(
        ...,
        description="5-year biochemical recurrence rate percentage range",
        example="5-15%"
    )
    
    clinical_assessment: Dict = Field(
        ...,
        description="Detailed clinical assessment including PSA, Gleason score, stage analysis, and risk factors",
        example={
            "psa_level": 8.5,
            "gleason_score": 6,
            "clinical_stage": "T1c",
            "risk_group": "low",
            "primary_risk_factors": ["Low PSA: 8.5 ng/mL (≤10)", "Low-grade cancer: Gleason 6 (≤6)", "Early local stage: T1c (T1-T2a)"],
            "disease_characteristics": ["Clinically localized prostate cancer", "Risk stratification based on D'Amico criteria", "Classified as low risk for biochemical recurrence"]
        }
    )
    
    treatment_recommendations: Dict = Field(
        ...,
        description="Comprehensive treatment recommendations including primary options, additional considerations, and multidisciplinary approach",
        example={
            "primary_recommendations": [
                "Active surveillance may be appropriate for select patients",
                "Radical prostatectomy offers excellent cure rates",
                "External beam radiation therapy provides equivalent outcomes",
                "Brachytherapy is an effective option for suitable candidates",
                "Regular PSA monitoring every 3-6 months if on active surveillance"
            ],
            "additional_considerations": [],
            "multidisciplinary_approach": [
                "Urologist for treatment planning and monitoring",
                "Consider radiation oncologist consultation for treatment options",
                "Patient education and support services"
            ],
            "follow_up_intensity": "PSA every 6 months for 2 years, then annually if stable"
        }
    )
    
    prognosis: Dict = Field(
        ...,
        description="Prognostic assessment including survival estimates, disease control rates, and prognostic factors",
        example={
            "prognosis": "Excellent",
            "disease_specific_survival": ">95% at 10 years",
            "biochemical_control": "85-95% at 5 years",
            "metastasis_risk": "Very low (<5%)"
        }
    )
    
    monitoring_recommendations: Dict = Field(
        ...,
        description="Monitoring recommendations including routine parameters, risk-specific monitoring, and frequency",
        example={
            "routine_monitoring": ["Serial PSA measurements", "Digital rectal examination", "Clinical assessment"],
            "risk_specific_monitoring": [
                "Annual assessment if on active surveillance",
                "Consider repeat biopsy in 12-18 months if on active surveillance",
                "Monitor for PSA doubling time"
            ],
            "frequency": "PSA every 6 months for 2 years, then annually if stable"
        }
    )
    
    risk_factors: Dict = Field(
        ...,
        description="Analysis of individual risk factors (PSA, Gleason, stage) and their contribution to overall risk",
        example={
            "psa_risk": "low",
            "gleason_risk": "low",
            "stage_risk": "low",
            "highest_risk_factor": "low"
        }
    )
    
    counseling_points: List[str] = Field(
        ...,
        description="Key counseling points for patient discussion and shared decision-making",
        example=[
            "Excellent prognosis with low risk of cancer progression",
            "Multiple effective treatment options available",
            "Active surveillance is a reasonable option for many patients",
            "Treatment side effects may outweigh benefits in some cases",
            "Regular monitoring is essential regardless of treatment choice"
        ]
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": "low",
                "unit": "risk group",
                "interpretation": "D'Amico Low Risk classification based on PSA 8.5 ng/mL, Gleason score 6, and clinical stage T1c. Patient has excellent prognosis with 5-15% 5-year biochemical recurrence risk. Active surveillance may be appropriate for select patients, though definitive treatment offers excellent cure rates.",
                "stage": "Low Risk",
                "stage_description": "Low risk of treatment failure",
                "risk_group": "low",
                "risk_category": "Low Risk",
                "criteria_met": "PSA ≤10 ng/mL AND Gleason score ≤6 AND clinical stage T1-T2a",
                "biochemical_recurrence_risk": "Low (5-15%)",
                "five_year_recurrence_rate": "5-15%",
                "clinical_assessment": {
                    "psa_level": 8.5,
                    "gleason_score": 6,
                    "clinical_stage": "T1c",
                    "risk_group": "low",
                    "primary_risk_factors": ["Low PSA: 8.5 ng/mL (≤10)", "Low-grade cancer: Gleason 6 (≤6)", "Early local stage: T1c (T1-T2a)"],
                    "disease_characteristics": ["Clinically localized prostate cancer", "Risk stratification based on D'Amico criteria", "Classified as low risk for biochemical recurrence"]
                },
                "treatment_recommendations": {
                    "primary_recommendations": [
                        "Active surveillance may be appropriate for select patients",
                        "Radical prostatectomy offers excellent cure rates",
                        "External beam radiation therapy provides equivalent outcomes",
                        "Brachytherapy is an effective option for suitable candidates",
                        "Regular PSA monitoring every 3-6 months if on active surveillance"
                    ],
                    "additional_considerations": [],
                    "multidisciplinary_approach": [
                        "Urologist for treatment planning and monitoring",
                        "Consider radiation oncologist consultation for treatment options",
                        "Patient education and support services"
                    ],
                    "follow_up_intensity": "PSA every 6 months for 2 years, then annually if stable"
                },
                "prognosis": {
                    "prognosis": "Excellent",
                    "disease_specific_survival": ">95% at 10 years",
                    "biochemical_control": "85-95% at 5 years",
                    "metastasis_risk": "Very low (<5%)"
                },
                "monitoring_recommendations": {
                    "routine_monitoring": ["Serial PSA measurements", "Digital rectal examination", "Clinical assessment"],
                    "risk_specific_monitoring": [
                        "Annual assessment if on active surveillance",
                        "Consider repeat biopsy in 12-18 months if on active surveillance",
                        "Monitor for PSA doubling time"
                    ],
                    "frequency": "PSA every 6 months for 2 years, then annually if stable"
                },
                "risk_factors": {
                    "psa_risk": "low",
                    "gleason_risk": "low",
                    "stage_risk": "low",
                    "highest_risk_factor": "low"
                },
                "counseling_points": [
                    "Excellent prognosis with low risk of cancer progression",
                    "Multiple effective treatment options available",
                    "Active surveillance is a reasonable option for many patients",
                    "Treatment side effects may outweigh benefits in some cases",
                    "Regular monitoring is essential regardless of treatment choice"
                ]
            }
        }