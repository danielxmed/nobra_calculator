"""
Duval/CIBMTR Score for Acute Myelogenous Leukemia (AML) Survival Models

Request and response models for Duval/CIBMTR Score calculation.

References (Vancouver style):
1. Duval M, Klein JP, He W, Cahn JY, Cairo M, Camitta BM, et al. Hematopoietic stem-cell 
   transplantation for acute leukemia in relapse or primary induction failure. J Clin Oncol. 
   2010;28(23):3730-8. doi: 10.1200/JCO.2010.28.8852.
2. Oran B, de Lima M, Garcia-Manero G, Thall PF, Lin R, Popat U, et al. A phase 3 randomized 
   study of 5-azacytidine vs physicians' choice as maintenance therapy for patients with AML 
   in first remission after intensive chemotherapy ineligible for stem cell transplantation. 
   Blood. 2013;121(24):4906-14.
3. Ruggeri A, Labopin M, Ciceri F, Mohty M, Nagler A. Definition of GvHD-free, relapse-free 
   survival for registry-based studies: an ALWP-EBMT analysis on patients with AML in remission. 
   Bone Marrow Transplant. 2016;51(4):610-1.
4. Cornelissen JJ, Gratwohl A, Schlenk RF, Sierra J, Bornhäuser M, Juliusson G, et al. The 
   European LeukemiaNet AML Working Party consensus statement on allogeneic HSCT for patients 
   with AML in remission: an integrated-risk adapted approach. Nat Rev Clin Oncol. 2012;9(10):579-90. 
   doi: 10.1038/nrclinonc.2012.150.

The Duval/CIBMTR Score for Acute Myelogenous Leukemia (AML) Survival is a validated prognostic 
tool that predicts transplantation survival for AML patients undergoing allogeneic hematopoietic 
stem cell transplantation (HSCT). The score was developed from analysis of 1,673 AML patients 
with active disease at the time of conditioning, making it particularly valuable for high-risk 
transplant candidates.

The scoring system evaluates five pre-transplant risk factors:
- Disease status and remission duration
- Cytogenetic risk category
- HLA matching between donor and recipient
- Presence of circulating blasts at transplant
- Patient performance status

Scores range from 0-5 points, with lower scores indicating better prognosis:
- Score 0: 42% 3-year overall survival (excellent prognosis)
- Score 1: 28% 3-year overall survival (good prognosis)
- Score 2: 15% 3-year overall survival (intermediate prognosis)
- Score ≥3: 6% 3-year overall survival (poor prognosis)

This tool assists in transplant decision-making, patient counseling, and risk stratification 
for clinical trials and treatment planning.
"""

from pydantic import BaseModel, Field
from typing import Literal


class DuvalCibmtrScoreAmlSurvivalRequest(BaseModel):
    """
    Request model for Duval/CIBMTR Score for Acute Myelogenous Leukemia (AML) Survival
    
    The Duval/CIBMTR Score uses five clinical parameters to assess transplant survival probability:
    
    Disease Status Parameters:
    
    1. Disease Group (Remission Status):
    - Primary induction failure or first CR >6 months: No increase in risk (0 points)
      * Primary induction failure: Failure to achieve complete remission after initial induction
      * First complete remission >6 months: Durable first remission
    - First CR <6 months: Short-duration remission indicating aggressive disease (+1 point)
      * Indicates early relapse potential and chemotherapy resistance
    
    2. Cytogenetics Prior to HSCT:
    - Good or intermediate: Favorable or standard-risk genetic profile (0 points)
      * Good: t(8;21), inv(16)/t(16;16), t(15;17)
      * Intermediate: Normal karyotype, other abnormalities not classified as good/poor
    - Poor: High-risk genetic abnormalities (+1 point)
      * Complex karyotype (≥3 abnormalities), -5/del(5q), -7/del(7q)
      * inv(3q), t(6;9), t(9;22), 11q23 abnormalities
    
    Transplant-Related Parameters:
    
    3. HLA Match Group (Donor Compatibility):
    - HLA identical sibling or well/partially matched unrelated: Optimal matching (0 points)
      * HLA identical sibling: 6/6 HLA match with sibling donor
      * Well-matched unrelated: 8/8 or 10/10 HLA match with unrelated donor
      * Partially matched unrelated: Single HLA mismatch with unrelated donor
    - Mismatched unrelated: Multiple HLA mismatches with unrelated donor (+1 point)
    - Related other than HLA identical sibling: Haploidentical or mismatched family (+2 points)
      * Includes haploidentical parents, children, or mismatched siblings
    
    4. Circulating Blasts:
    - Absent: No detectable blasts in peripheral blood (0 points)
      * Indicates better disease control at time of transplant
    - Present: Detectable blasts in peripheral blood (+1 point)
      * Any level of circulating blasts indicates active disease
      * Associated with higher relapse risk and worse outcomes
    
    Patient Performance Parameters:
    
    5. Karnofsky/Lansky Scale:
    - 90-100: Excellent functional status (0 points)
      * Karnofsky 90-100: Normal activity with minor symptoms
      * Lansky 90-100: Normal activity level for pediatric patients
    - <90: Impaired functional status (+1 point)
      * Indicates significant functional limitation
      * Associated with increased transplant-related mortality
    
    Score Interpretation and Clinical Management:
    
    Score 0 (Excellent Prognosis - 42% 3-year survival):
    - Proceed with standard transplant protocols
    - Routine supportive care and monitoring
    - Excellent candidate for myeloablative conditioning
    
    Score 1 (Good Prognosis - 28% 3-year survival):
    - Enhanced supportive care measures
    - Close post-transplant monitoring
    - Consider intensified GVHD prophylaxis
    
    Score 2 (Intermediate Prognosis - 15% 3-year survival):
    - Careful risk-benefit analysis required
    - Intensive supportive care protocols
    - Early intervention strategies for complications
    - Consider reduced-intensity conditioning in appropriate cases
    
    Score ≥3 (Poor Prognosis - 6% 3-year survival):
    - Multidisciplinary team discussion essential
    - Consider alternative treatment approaches
    - Palliative care consultation recommended
    - Clinical trial enrollment if available
    - Comprehensive family counseling required

    References (Vancouver style):
    1. Duval M, Klein JP, He W, Cahn JY, Cairo M, Camitta BM, et al. Hematopoietic stem-cell 
    transplantation for acute leukemia in relapse or primary induction failure. J Clin Oncol. 
    2010;28(23):3730-8. doi: 10.1200/JCO.2010.28.8852.
    2. Oran B, de Lima M, Garcia-Manero G, Thall PF, Lin R, Popat U, et al. A phase 3 randomized 
    study of 5-azacytidine vs physicians' choice as maintenance therapy for patients with AML 
    in first remission after intensive chemotherapy ineligible for stem cell transplantation. 
    Blood. 2013;121(24):4906-14.
    3. Ruggeri A, Labopin M, Ciceri F, Mohty M, Nagler A. Definition of GvHD-free, relapse-free 
    survival for registry-based studies: an ALWP-EBMT analysis on patients with AML in remission. 
    Bone Marrow Transplant. 2016;51(4):610-1.
    4. Cornelissen JJ, Gratwohl A, Schlenk RF, Sierra J, Bornhäuser M, Juliusson G, et al. The 
    European LeukemiaNet AML Working Party consensus statement on allogeneic HSCT for patients 
    with AML in remission: an integrated-risk adapted approach. Nat Rev Clin Oncol. 2012;9(10):579-90. 
    doi: 10.1038/nrclinonc.2012.150.
    """
    
    disease_group: Literal["Primary induction failure or first CR >6 months", "First CR <6 months"] = Field(
        ...,
        description="Disease status at time of transplantation. Primary induction failure or first CR >6 months scores 0 points, first CR <6 months scores 1 point",
        example="Primary induction failure or first CR >6 months"
    )
    
    cytogenetics: Literal["Good or intermediate", "Poor"] = Field(
        ...,
        description="Cytogenetic risk category prior to HSCT. Good or intermediate risk scores 0 points, poor risk scores 1 point",
        example="Good or intermediate"
    )
    
    hla_match_group: Literal["HLA identical sibling or well/partially matched unrelated", "Mismatched unrelated", "Related other than HLA identical sibling"] = Field(
        ...,
        description="HLA matching status between donor and recipient. HLA identical sibling or well/partially matched unrelated scores 0 points, mismatched unrelated scores 1 point, related other than HLA identical sibling scores 2 points",
        example="HLA identical sibling or well/partially matched unrelated"
    )
    
    circulating_blasts: Literal["Absent", "Present"] = Field(
        ...,
        description="Presence of circulating blasts at time of transplantation. Absent scores 0 points, present scores 1 point",
        example="Absent"
    )
    
    karnofsky_lansky_scale: Literal["90-100", "<90"] = Field(
        ...,
        description="Karnofsky (adults) or Lansky (pediatric) performance status scale. 90-100 scores 0 points, <90 scores 1 point",
        example="90-100"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "disease_group": "Primary induction failure or first CR >6 months",
                "cytogenetics": "Good or intermediate",
                "hla_match_group": "HLA identical sibling or well/partially matched unrelated",
                "circulating_blasts": "Absent",
                "karnofsky_lansky_scale": "90-100"
            }
        }


class DuvalCibmtrScoreAmlSurvivalResponse(BaseModel):
    """
    Response model for Duval/CIBMTR Score for Acute Myelogenous Leukemia (AML) Survival
    
    The Duval/CIBMTR score ranges from 0-5 points and classifies patients into prognostic groups:
    
    - Score 0: 42% 3-year overall survival (excellent prognosis)
    - Score 1: 28% 3-year overall survival (good prognosis)  
    - Score 2: 15% 3-year overall survival (intermediate prognosis)
    - Score ≥3: 6% 3-year overall survival (poor prognosis)
    
    Clinical Decision-Making by Score:
    
    Excellent Prognosis (Score 0):
    - Standard myeloablative conditioning recommended
    - Routine transplant protocols and supportive care
    - High likelihood of successful transplant outcome
    - Proceed with confidence in transplant decision
    
    Good Prognosis (Score 1):
    - Enhanced supportive care measures
    - Close post-transplant monitoring for complications
    - Consider prophylactic interventions for GVHD
    - Good transplant candidate with acceptable risk
    
    Intermediate Prognosis (Score 2):
    - Intensive risk-benefit analysis required
    - Enhanced supportive care and early intervention strategies
    - Consider patient-specific factors and comorbidities
    - Transplant appropriate with careful monitoring
    
    Poor Prognosis (Score ≥3):
    - Multidisciplinary team consultation mandatory
    - Consider alternative treatment approaches
    - Clinical trial enrollment preferred if available
    - Palliative care discussion and family counseling
    - Transplant decision requires consensus and careful consideration
    
    Important Limitations:
    - Score validated only for myeloablative conditioning regimens
    - Reduced-intensity conditioning outcomes may differ
    - Syngeneic and cord blood transplants not included in validation
    - Should be used in conjunction with other clinical factors
    
    Reference: Duval M, et al. J Clin Oncol. 2010;28(23):3730-8.
    """
    
    result: int = Field(
        ...,
        description="Duval/CIBMTR score calculated from five pre-transplant risk factors (range: 0-5 points)",
        example=1
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation and management recommendations based on the score",
        example="28% 3-year overall survival. Good prognosis for AML patients undergoing allogeneic HSCT. Consider enhanced supportive care measures and close monitoring post-transplant."
    )
    
    stage: str = Field(
        ...,
        description="Prognostic category (Score 0, Score 1, Score 2, Score ≥3)",
        example="Score 1"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the prognostic category",
        example="Good prognosis"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "result": 1,
                "unit": "points",
                "interpretation": "28% 3-year overall survival. Good prognosis for AML patients undergoing allogeneic HSCT. Consider enhanced supportive care measures and close monitoring post-transplant. Contributing risk factors: First CR <6 months (+1 point). Continue with standard pre-transplant preparation and conditioning regimen. Maintain optimal performance status and disease control. This score is based on myeloablative conditioning regimens and may not apply to reduced-intensity conditioning. Regular reassessment recommended throughout the transplant process.",
                "stage": "Score 1",
                "stage_description": "Good prognosis"
            }
        }