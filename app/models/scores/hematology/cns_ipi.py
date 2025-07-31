"""
Central Nervous System International Prognostic Index (CNS-IPI) Models

Request and response models for CNS-IPI calculation.

References (Vancouver style):
1. Schmitz N, Zeynalova S, Nickelsen M, Kansara R, Villa D, Sehn LH, et al. 
   CNS International Prognostic Index: A Risk Model for CNS Relapse in Patients 
   With Diffuse Large B-Cell Lymphoma Treated With R-CHOP. J Clin Oncol. 
   2016 Sep 10;34(26):3150-3156. doi: 10.1200/JCO.2015.65.6520.
2. Ma'koseh M, Rahahleh N, Abdel-Razeq H. Impact of Central Nervous System 
   International Prognostic Index on the Treatment of Diffuse Large B Cell 
   Lymphoma. Cureus. 2021 Aug 13;13(8):e17016. doi: 10.7759/cureus.17016.
3. Savage KJ, Slack GW, Mottok A, Sehn LH, Villa D, Kansara R, et al. Impact 
   of dual expression of MYC and BCL2 by immunohistochemistry on the risk of 
   CNS relapse in DLBCL. Blood. 2016 Apr 28;127(17):2182-8. 
   doi: 10.1182/blood-2015-10-676700.

The CNS-IPI is a prognostic scoring system that predicts the risk of central 
nervous system relapse in patients with diffuse large B-cell lymphoma (DLBCL) 
treated with R-CHOP chemotherapy. This validated tool helps identify patients 
who may benefit from CNS-directed prophylaxis and guides treatment planning decisions.

The CNS-IPI uses 6 clinical and laboratory parameters (each scoring 0 or 1 point):
- Age >60 years: Associated with increased CNS relapse risk
- Elevated LDH: Marker of tumor burden and aggressive disease
- ECOG Performance Status >1: Indicates significant functional impairment
- Advanced stage (III/IV): Reflects extensive disease distribution
- >1 extranodal site: Multiple organ involvement increases CNS risk
- Kidney/adrenal involvement: Specific high-risk anatomical sites

Risk Categories:
- Low Risk (0-1 points): 0.6% CNS relapse rate at 2 years (46% of patients)
- Intermediate Risk (2-3 points): 3.4% CNS relapse rate at 2 years (41% of patients)
- High Risk (4-6 points): 10.2% CNS relapse rate at 2 years (12% of patients)

Clinical Impact: Helps optimize CNS prophylaxis decisions, avoiding unnecessary 
treatment in low-risk patients while identifying high-risk patients who would 
benefit from intrathecal chemotherapy or high-dose methotrexate.
"""

from pydantic import BaseModel, Field
from typing import Literal


class CnsIpiRequest(BaseModel):
    """
    Request model for Central Nervous System International Prognostic Index (CNS-IPI)
    
    The CNS-IPI uses 6 clinical and laboratory parameters to assess CNS relapse risk 
    in patients with diffuse large B-cell lymphoma (DLBCL) treated with R-CHOP.
    
    Clinical Parameters (each scores 1 point if present):
    - Age >60 years: Advanced age associated with increased CNS relapse risk
    - Elevated LDH: Lactate dehydrogenase above normal range (marker of tumor burden)
    - ECOG Performance Status >1: Moderate to severe functional limitation (PS 2-4)
    - Advanced stage: Ann Arbor stage III or IV disease (extensive distribution)
    - >1 extranodal site: Multiple organ involvement beyond lymph nodes
    - Kidney/adrenal involvement: Specific high-risk anatomical locations
    
    Total score ranges from 0-6 points and stratifies patients into three risk categories:
    
    Low Risk (0-1 points): 
    - 46% of DLBCL patients
    - 0.6% CNS relapse rate at 2 years (95% CI: 0%-1.2%)
    - CNS prophylaxis generally not recommended
    
    Intermediate Risk (2-3 points):
    - 41% of DLBCL patients  
    - 3.4% CNS relapse rate at 2 years (95% CI: 2.2%-4.4%)
    - CNS prophylaxis may be considered based on additional risk factors
    
    High Risk (4-6 points):
    - 12% of DLBCL patients
    - 10.2% CNS relapse rate at 2 years (95% CI: 6.3%-14.1%)
    - CNS prophylaxis strongly recommended
    
    Note: Additional high-risk features not captured by CNS-IPI include involvement 
    of breast, uterus, testis, epidural space, bone marrow involvement, and 
    double-hit/triple-hit lymphomas with MYC/BCL2 dual expression.
    
    References (Vancouver style):
    1. Schmitz N, Zeynalova S, Nickelsen M, Kansara R, Villa D, Sehn LH, et al. 
    CNS International Prognostic Index: A Risk Model for CNS Relapse in Patients 
    With Diffuse Large B-Cell Lymphoma Treated With R-CHOP. J Clin Oncol. 
    2016 Sep 10;34(26):3150-3156. doi: 10.1200/JCO.2015.65.6520.
    2. Ma'koseh M, Rahahleh N, Abdel-Razeq H. Impact of Central Nervous System 
    International Prognostic Index on the Treatment of Diffuse Large B Cell 
    Lymphoma. Cureus. 2021 Aug 13;13(8):e17016. doi: 10.7759/cureus.17016.
    """
    
    age_over_60: Literal["yes", "no"] = Field(
        ...,
        description="Patient age greater than 60 years. Advanced age is associated with increased risk of CNS relapse in DLBCL. Scores 1 point if yes",
        example="no"
    )
    
    elevated_ldh: Literal["yes", "no"] = Field(
        ...,
        description="Lactate dehydrogenase (LDH) level above normal laboratory range. Elevated LDH reflects tumor burden and disease aggressiveness. Scores 1 point if yes",
        example="yes"
    )
    
    ecog_performance_status_over_1: Literal["yes", "no"] = Field(
        ...,
        description="ECOG Performance Status greater than 1 (PS 2-4: moderate to severe limitation of activity). Poor performance status correlates with advanced disease. Scores 1 point if yes",
        example="no"
    )
    
    advanced_stage: Literal["yes", "no"] = Field(
        ...,
        description="Ann Arbor stage III or IV disease (advanced stage with extensive lymph node involvement or extranodal disease). Scores 1 point if yes",
        example="yes"
    )
    
    multiple_extranodal_sites: Literal["yes", "no"] = Field(
        ...,
        description="More than 1 extranodal disease site involved (disease beyond lymph nodes in multiple organs). Multiple extranodal involvement increases CNS risk. Scores 1 point if yes",
        example="no"
    )
    
    kidney_adrenal_involvement: Literal["yes", "no"] = Field(
        ...,
        description="Involvement of kidney and/or adrenal gland. These specific anatomical sites are associated with increased CNS relapse risk. Scores 1 point if yes",
        example="no"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "age_over_60": "no",
                "elevated_ldh": "yes",
                "ecog_performance_status_over_1": "no",
                "advanced_stage": "yes",
                "multiple_extranodal_sites": "no",
                "kidney_adrenal_involvement": "no"
            }
        }


class CnsIpiResponse(BaseModel):
    """
    Response model for Central Nervous System International Prognostic Index (CNS-IPI)
    
    The CNS-IPI provides risk stratification for CNS relapse in DLBCL patients with:
    - Total score (0-6 points) based on 6 clinical/laboratory parameters
    - Risk category classification (Low/Intermediate/High Risk)
    - 2-year CNS relapse rate with confidence intervals
    - Patient distribution percentages from validation studies
    - Evidence-based prophylaxis recommendations
    - Detailed scoring breakdown for clinical decision-making
    
    Risk Categories and Clinical Management:
    
    Low Risk (0-1 points):
    - Represents 46% of DLBCL patients
    - Very low CNS relapse risk (0.6% at 2 years)
    - Standard R-CHOP treatment appropriate
    - CNS prophylaxis generally not recommended
    
    Intermediate Risk (2-3 points):
    - Represents 41% of DLBCL patients
    - Low to moderate CNS relapse risk (3.4% at 2 years)
    - Consider CNS prophylaxis based on additional risk factors
    - Individual clinical judgment important
    
    High Risk (4-6 points):
    - Represents 12% of DLBCL patients
    - High CNS relapse risk (10.2% at 2 years)
    - CNS prophylaxis strongly recommended
    - Options include intrathecal chemotherapy or high-dose methotrexate
    
    Additional Considerations:
    The CNS-IPI does not capture all high-risk patients. Additional features 
    that may increase CNS risk include involvement of breast, uterus, testis, 
    epidural space, bone marrow involvement, and molecular features such as 
    double-hit lymphomas or MYC/BCL2 dual expression.
    
    Reference: Schmitz N, et al. J Clin Oncol. 2016;34(26):3150-3156.
    """
    
    result: int = Field(
        ...,
        description="CNS-IPI score calculated from the 6 clinical parameters (range: 0-6 points)",
        example=2
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation with risk assessment and evidence-based prophylaxis recommendations",
        example="CNS-IPI Score 2: Low to moderate risk of CNS relapse (3.4% at 2 years, 95% CI: 2.2%-4.4%). CNS prophylaxis may be considered based on additional high-risk features and clinical judgment. Represents 41% of DLBCL patients."
    )
    
    stage: str = Field(
        ...,
        description="Risk category classification (Low Risk, Intermediate Risk, High Risk)",
        example="Intermediate Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the risk category",
        example="Low to moderate CNS relapse risk"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "result": 2,
                "unit": "points",
                "interpretation": "CNS-IPI Score 2: Low to moderate risk of CNS relapse (3.4% at 2 years, 95% CI: 2.2%-4.4%). CNS prophylaxis may be considered based on additional high-risk features and clinical judgment. Represents 41% of DLBCL patients.",
                "stage": "Intermediate Risk",
                "stage_description": "Low to moderate CNS relapse risk"
            }
        }