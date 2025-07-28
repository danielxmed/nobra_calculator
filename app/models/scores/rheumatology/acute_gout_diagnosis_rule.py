"""
Acute Gout Diagnosis Rule Models

Request and response models for Acute Gout Diagnosis Rule calculation.

References (Vancouver style):
1. Janssens HJ, Fransen J, van de Lisdonk EH, van Riel PL, van Weel C, Janssen M. 
   A diagnostic rule for acute gouty arthritis in primary care without joint fluid 
   analysis. Arch Intern Med. 2010 Jul 12;170(13):1120-6. 
   doi: 10.1001/archinternmed.2010.196.
2. Kienhorst LB, Janssens HJ, Fransen J, Janssen M. The validation of a diagnostic 
   rule for gout without joint fluid analysis: a prospective study. Rheumatology 
   (Oxford). 2015 Apr;54(4):609-14. doi: 10.1093/rheumatology/keu378.

The Acute Gout Diagnosis Rule is a clinical decision tool developed for primary 
care settings to help diagnose acute gout without joint fluid analysis. This rule 
uses seven readily available clinical parameters to risk stratify patients for 
gout vs non-gout arthritis and helps determine which patients benefit most from 
joint aspiration.

The rule was derived from a study of 328 patients with monoarthritis in primary 
care and validated in secondary care (rheumatology clinic) settings. It provides 
excellent diagnostic utility with scores ≤4 having a negative predictive value 
of 95% and scores ≥8 having a positive predictive value of 87%.

This tool is particularly valuable when joint aspiration is not readily available 
or feasible, allowing clinicians to make informed decisions about empirical 
treatment or the need for further diagnostic testing.
"""

from pydantic import BaseModel, Field
from typing import Literal


class AcuteGoutDiagnosisRuleRequest(BaseModel):
    """
    Request model for Acute Gout Diagnosis Rule
    
    The Acute Gout Diagnosis Rule uses seven clinical parameters to assess the 
    likelihood of acute gout:
    
    Clinical Parameters and Scoring:
    
    Male Sex (0 or 2 points):
    - no: Female sex (0 points)
    - yes: Male sex (+2 points) - Male patients have higher risk of gout
    
    Previous Patient-Reported Arthritis Attack (0 or 2 points):
    - no: No previous arthritis attacks (0 points)
    - yes: Previous arthritis attack reported by patient (+2 points)
    
    Onset Within 1 Day (0 or 0.5 points):
    - no: Onset longer than 1 day (0 points)
    - yes: Acute onset within 1 day (+0.5 points) - Typical for gout flares
    
    Joint Redness (0 or 1 point):
    - no: No joint redness observed (0 points)
    - yes: Joint redness present (+1 point) - Common sign of acute inflammation
    
    First Metatarsophalangeal Joint Involvement (0 or 2.5 points):
    - no: First MTP joint not involved (0 points)
    - yes: First MTP joint involved (+2.5 points) - Classic "podagra" presentation
    
    Hypertension or Cardiovascular Disease (0 or 1.5 points):
    - no: No hypertension or cardiovascular disease (0 points)
    - yes: Hypertension or ≥1 cardiovascular disease (+1.5 points)
    - Cardiovascular diseases include: angina, MI, CHF, stroke/TIA, PVD
    
    Elevated Serum Uric Acid (0 or 3.5 points):
    - no: Serum uric acid ≤5.88 mg/dL (≤0.35 mmol/L) (0 points)
    - yes: Serum uric acid >5.88 mg/dL (>0.35 mmol/L) (+3.5 points)
    
    Score Interpretation:
    - ≤4 points: Low risk (2.2% prevalence) - Gout unlikely
    - 4.5-7.5 points: Intermediate risk (31.2% prevalence) - Consider joint aspiration
    - ≥8 points: High risk (80.4-82.5% prevalence) - Gout highly likely
    
    References (Vancouver style):
    1. Janssens HJ, Fransen J, van de Lisdonk EH, van Riel PL, van Weel C, Janssen M. 
    A diagnostic rule for acute gouty arthritis in primary care without joint fluid 
    analysis. Arch Intern Med. 2010 Jul 12;170(13):1120-6. 
    doi: 10.1001/archinternmed.2010.196.
    2. Kienhorst LB, Janssens HJ, Fransen J, Janssen M. The validation of a diagnostic 
    rule for gout without joint fluid analysis: a prospective study. Rheumatology 
    (Oxford). 2015 Apr;54(4):609-14. doi: 10.1093/rheumatology/keu378.
    """
    
    male_sex: Literal["no", "yes"] = Field(
        ...,
        description="Patient's sex. Male sex increases gout risk and scores 2 points",
        example="yes"
    )
    
    previous_arthritis_attack: Literal["no", "yes"] = Field(
        ...,
        description="Previous patient-reported arthritis attack. History of arthritis attacks scores 2 points",
        example="no"
    )
    
    onset_within_one_day: Literal["no", "yes"] = Field(
        ...,
        description="Onset of symptoms within 1 day. Acute onset typical of gout flares scores 0.5 points",
        example="yes"
    )
    
    joint_redness: Literal["no", "yes"] = Field(
        ...,
        description="Joint redness present on examination. Visible redness indicates acute inflammation and scores 1 point",
        example="yes"
    )
    
    first_mtp_involvement: Literal["no", "yes"] = Field(
        ...,
        description="First metatarsophalangeal joint involvement (podagra). Classic gout presentation affecting the big toe scores 2.5 points",
        example="yes"
    )
    
    hypertension_or_cardiovascular: Literal["no", "yes"] = Field(
        ...,
        description="Hypertension or presence of ≥1 cardiovascular disease (angina, MI, CHF, stroke/TIA, PVD). Scores 1.5 points if present",
        example="no"
    )
    
    elevated_uric_acid: Literal["no", "yes"] = Field(
        ...,
        description="Serum uric acid >5.88 mg/dL (>0.35 mmol/L). Hyperuricemia strongly associated with gout and scores 3.5 points",
        example="yes"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "male_sex": "yes",
                "previous_arthritis_attack": "no",
                "onset_within_one_day": "yes",
                "joint_redness": "yes",
                "first_mtp_involvement": "yes",
                "hypertension_or_cardiovascular": "no",
                "elevated_uric_acid": "yes"
            }
        }


class AcuteGoutDiagnosisRuleResponse(BaseModel):
    """
    Response model for Acute Gout Diagnosis Rule
    
    The Acute Gout Diagnosis Rule provides a score from 0 to 13 points that 
    stratifies patients into three risk categories:
    
    - Low Risk (≤4 points): 2.2% prevalence of gout, NPV 97.8%
    - Intermediate Risk (4.5-7.5 points): 31.2% prevalence of gout
    - High Risk (≥8 points): 80.4-82.5% prevalence of gout, PPV 87%
    
    This scoring system helps clinicians make informed decisions about:
    - Need for joint aspiration and synovial fluid analysis
    - Empirical treatment initiation
    - Further diagnostic workup
    - Patient counseling and follow-up planning
    
    Reference: Janssens HJ, et al. Arch Intern Med. 2010;170(13):1120-6.
    """
    
    result: float = Field(
        ...,
        description="Acute Gout Diagnosis Rule score (0-13 points)",
        example=9.5
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation and recommended management approach based on the risk category",
        example="High likelihood of acute gout (80.4-82.5% prevalence). Gout is highly likely. Consider empirical treatment with anti-inflammatory therapy while awaiting confirmatory testing if needed. PPV 87%."
    )
    
    stage: str = Field(
        ...,
        description="Risk category (Low Risk, Intermediate Risk, High Risk)",
        example="High Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the score range for this risk category",
        example="Score ≥8"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 9.5,
                "unit": "points",
                "interpretation": "High likelihood of acute gout (80.4-82.5% prevalence). Gout is highly likely. Consider empirical treatment with anti-inflammatory therapy while awaiting confirmatory testing if needed. PPV 87%.",
                "stage": "High Risk",
                "stage_description": "Score ≥8"
            }
        }