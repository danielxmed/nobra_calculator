"""
Drug Resistance in Pneumonia (DRIP) Score Models

Request and response models for DRIP Score calculation.

References (Vancouver style):
1. Webb BJ, Dascomb K, Stenehjem E, Dean N. Derivation and multicenter validation 
   of the drug resistance in pneumonia clinical prediction score. Antimicrob Agents 
   Chemother. 2016;60(5):2652-63. doi: 10.1128/AAC.03071-15.
2. Attridge RT, Frei CR, Restrepo MI, et al. Guideline-concordant therapy and outcomes 
   in healthcare-associated pneumonia. Eur Respir J. 2011;38(4):878-87. 
   doi: 10.1183/09031936.00141110.
3. Webb BJ, Dangerfield B, Pasha JS, et al. Guideline-concordant antibiotic therapy 
   and clinical outcomes in healthcare-associated pneumonia. Respir Med. 2012;106(11):1606-12. 
   doi: 10.1016/j.rmed.2012.08.010.

The DRIP Score predicts risk for community-acquired pneumonia due to drug-resistant 
pathogens (CAP-DRP). It helps determine when broad-spectrum antibiotics should be used 
to ensure effective treatment while avoiding unnecessary antibiotic resistance. The score 
consists of 4 major risk factors (2 points each) and 6 minor risk factors (1 point each), 
with a threshold of ≥4 points indicating high risk for drug-resistant pneumonia.
"""

from pydantic import BaseModel, Field
from typing import Literal


class DripScoreRequest(BaseModel):
    """
    Request model for Drug Resistance in Pneumonia (DRIP) Score
    
    The DRIP Score consists of 10 yes/no questions about risk factors for drug-resistant 
    pneumonia, categorized as major (2 points) or minor (1 point) risk factors:
    
    Major Risk Factors (2 points each):
    - Antibiotic use within 60 days
    - Residence in a long-term-care facility
    - Tube feeding
    - Prior infection with a drug-resistant pathogen
    
    Minor Risk Factors (1 point each):
    - Chronic pulmonary disease
    - Prior hospitalization within 60 days
    - Poor functional status
    - MRSA colonization
    - Wound care
    - Gastric acid suppression
    
    Scoring and Interpretation:
    - Total score range: 0-14 points
    - Score <4: Low risk - standard empirical antibiotics appropriate
    - Score ≥4: High risk - extended-spectrum antibiotic coverage recommended
    
    Clinical Performance (at threshold ≥4):
    - Sensitivity: 0.82 (95% CI: 0.67-0.88)
    - Specificity: 0.81 (95% CI: 0.73-0.87)
    - Positive Predictive Value: 0.68 (95% CI: 0.56-0.78)
    - Negative Predictive Value: 0.90 (95% CI: 0.81-0.93)

    References (Vancouver style):
    1. Webb BJ, Dascomb K, Stenehjem E, Dean N. Derivation and multicenter validation 
       of the drug resistance in pneumonia clinical prediction score. Antimicrob Agents 
       Chemother. 2016;60(5):2652-63. doi: 10.1128/AAC.03071-15.
    2. Attridge RT, Frei CR, Restrepo MI, et al. Guideline-concordant therapy and outcomes 
       in healthcare-associated pneumonia. Eur Respir J. 2011;38(4):878-87. 
       doi: 10.1183/09031936.00141110.
    3. Webb BJ, Dangerfield B, Pasha JS, et al. Guideline-concordant antibiotic therapy 
       and clinical outcomes in healthcare-associated pneumonia. Respir Med. 2012;106(11):1606-12. 
       doi: 10.1016/j.rmed.2012.08.010.
    """
    
    antibiotic_use_60_days: Literal["yes", "no"] = Field(
        ...,
        description="Antibiotic use within 60 days (MAJOR risk factor: 2 points if yes)",
        example="no"
    )
    
    long_term_care_facility: Literal["yes", "no"] = Field(
        ...,
        description="Residence in a long-term-care facility (MAJOR risk factor: 2 points if yes)",
        example="no"
    )
    
    tube_feeding: Literal["yes", "no"] = Field(
        ...,
        description="Tube feeding (MAJOR risk factor: 2 points if yes)",
        example="no"
    )
    
    prior_drug_resistant_infection: Literal["yes", "no"] = Field(
        ...,
        description="Prior infection with a drug-resistant pathogen (MAJOR risk factor: 2 points if yes)",
        example="no"
    )
    
    chronic_pulmonary_disease: Literal["yes", "no"] = Field(
        ...,
        description="Chronic pulmonary disease (MINOR risk factor: 1 point if yes)",
        example="no"
    )
    
    hospitalization_60_days: Literal["yes", "no"] = Field(
        ...,
        description="Prior hospitalization within 60 days (MINOR risk factor: 1 point if yes)",
        example="no"
    )
    
    poor_functional_status: Literal["yes", "no"] = Field(
        ...,
        description="Poor functional status (MINOR risk factor: 1 point if yes)",
        example="no"
    )
    
    mrsa_colonization: Literal["yes", "no"] = Field(
        ...,
        description="MRSA colonization (MINOR risk factor: 1 point if yes)",
        example="no"
    )
    
    wound_care: Literal["yes", "no"] = Field(
        ...,
        description="Wound care (MINOR risk factor: 1 point if yes)",
        example="no"
    )
    
    gastric_acid_suppression: Literal["yes", "no"] = Field(
        ...,
        description="Gastric acid suppression (MINOR risk factor: 1 point if yes)",
        example="no"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "antibiotic_use_60_days": "no",
                "long_term_care_facility": "no",
                "tube_feeding": "no",
                "prior_drug_resistant_infection": "no",
                "chronic_pulmonary_disease": "no",
                "hospitalization_60_days": "no",
                "poor_functional_status": "no",
                "mrsa_colonization": "no",
                "wound_care": "no",
                "gastric_acid_suppression": "no"
            }
        }


class DripScoreResponse(BaseModel):
    """
    Response model for Drug Resistance in Pneumonia (DRIP) Score
    
    The DRIP Score ranges from 0 to 14 points and indicates:
    - Score <4: Low risk of drug-resistant pneumonia - standard empirical antibiotics appropriate
    - Score ≥4: High risk of drug-resistant pneumonia - extended-spectrum antibiotic coverage recommended
    
    The DRIP score is more predictive than healthcare-associated pneumonia (HCAP) criteria 
    for drug-resistant pathogens and may decrease antibiotic overutilization by 46% compared 
    to HCAP criteria.
    
    Important considerations:
    - Should only be used for bacterial causes of pneumonia
    - False negatives may occur with MRSA, P. aeruginosa, severe COPD, IV drug use, 
      psychiatric illness, and homelessness
    - False positives may occur with S. pneumoniae and methicillin-susceptible S. aureus (MSSA)
    - Local validation and institutional antibiotic resistance patterns should be considered
    
    Reference: Webb BJ, et al. Antimicrob Agents Chemother. 2016;60(5):2652-63.
    """
    
    result: int = Field(
        ...,
        description="DRIP score calculated from risk factors (range: 0-14 points)",
        example=3
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation and antibiotic recommendations based on the DRIP score",
        example="Scores <4 were associated with lower risk of drug-resistant pneumonia. Consider treating without extended-spectrum antibiotics. Standard empirical antibiotics appropriate."
    )
    
    stage: str = Field(
        ...,
        description="Risk level category (Low Risk or High Risk)",
        example="Low Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the risk level category",
        example="Low risk of drug-resistant pneumonia"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "result": 3,
                "unit": "points",
                "interpretation": "Scores <4 were associated with lower risk of drug-resistant pneumonia. Consider treating without extended-spectrum antibiotics. Standard empirical antibiotics appropriate.",
                "stage": "Low Risk",
                "stage_description": "Low risk of drug-resistant pneumonia"
            }
        }