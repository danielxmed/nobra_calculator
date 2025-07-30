"""
Centor Score (Modified/McIsaac) for Strep Pharyngitis Models

Request and response models for Centor Score calculation.

References (Vancouver style):
1. Centor RM, Witherspoon JM, Dalton HP, Brody CE, Link K. The diagnosis of strep throat 
   in adults in the emergency room. Med Decis Making. 1981;1(3):239-46. 
   doi: 10.1177/0272989X8100100304.
2. McIsaac WJ, White D, Tannenbaum D, Low DE. A clinical score to reduce unnecessary 
   antibiotic use in patients with sore throat. CMAJ. 1998 Jan 13;158(1):75-83.
3. McIsaac WJ, Kellner JD, Aufricht P, Vanjaka A, Low DE. Empirical validation of 
   guidelines for the management of pharyngitis in children and adults. JAMA. 2004 
   Apr 7;291(13):1587-95. doi: 10.1001/jama.291.13.1587.
4. Shulman ST, Bisno AL, Clegg HW, Gerber MA, Kaplan EL, Lee G, Martin JM, Van Beneden C. 
   Clinical practice guideline for the diagnosis and management of group A streptococcal 
   pharyngitis: 2012 update by the Infectious Diseases Society of America. Clin Infect Dis. 
   2012 Nov 15;55(10):e86-102. doi: 10.1093/cid/cis629.

The Modified Centor Score estimates the likelihood that pharyngitis is streptococcal and 
suggests management course. It includes age adjustment for improved accuracy compared to 
the original Centor criteria. The score helps reduce unnecessary antibiotic prescriptions 
by providing evidence-based approach to testing and treatment decisions.

Clinical Criteria (1 point each):
- Tonsillar exudate: Presence of tonsillar swelling or exudate
- Tender cervical nodes: Swollen, tender anterior cervical lymph nodes  
- History of fever: History of fever (>38°C or 100.4°F)
- Absence of cough: Absence of cough

Age Adjustment:
- Age 3-14 years: +1 point (higher risk of streptococcal infection)
- Age 15-44 years: 0 points (baseline risk)
- Age ≥45 years: -1 point (lower risk of streptococcal infection)

Score ranges from -1 to +5 points with probability assessments:
- Score ≤1: Low probability (1-10% GAS) - No testing or antibiotics
- Score 2-3: Moderate probability (11-35% GAS) - RADT/culture recommended
- Score ≥4: High probability (51-53% GAS) - Consider empiric treatment
"""

from pydantic import BaseModel, Field
from typing import Literal, Dict, Any


class CentorScoreRequest(BaseModel):
    """
    Request model for Centor Score (Modified/McIsaac) for Strep Pharyngitis
    
    The Modified Centor Score uses 4 clinical criteria plus age adjustment to assess 
    the probability of Group A Streptococcus (GAS) pharyngitis in patients presenting 
    with sore throat.
    
    Clinical Criteria (each worth 1 point if present):
    - Tonsillar exudate: Presence of tonsillar swelling or exudate
    - Tender cervical nodes: Swollen, tender anterior cervical lymph nodes
    - History of fever: History of fever (>38°C or 100.4°F)  
    - Absence of cough: Absence of cough (respiratory viral symptoms less likely)
    
    Age Adjustment (McIsaac modification):
    - Age 3-14 years: +1 point (children have higher risk of streptococcal infection)
    - Age 15-44 years: 0 points (baseline adult risk)
    - Age ≥45 years: -1 point (older adults have lower risk of streptococcal infection)
    
    Total score ranges from -1 to +5 points and guides management decisions:
    - Score ≤1: Low probability (1-10%) - No testing or antibiotics needed
    - Score 2-3: Moderate probability (11-35%) - RADT and/or culture recommended
    - Score ≥4: High probability (51-53%) - Consider empiric treatment or testing
    
    References (Vancouver style):
    1. Centor RM, Witherspoon JM, Dalton HP, Brody CE, Link K. The diagnosis of strep throat 
    in adults in the emergency room. Med Decis Making. 1981;1(3):239-46. 
    doi: 10.1177/0272989X8100100304.
    2. McIsaac WJ, White D, Tannenbaum D, Low DE. A clinical score to reduce unnecessary 
    antibiotic use in patients with sore throat. CMAJ. 1998 Jan 13;158(1):75-83.
    3. McIsaac WJ, Kellner JD, Aufricht P, Vanjaka A, Low DE. Empirical validation of 
    guidelines for the management of pharyngitis in children and adults. JAMA. 2004 
    Apr 7;291(13):1587-95. doi: 10.1001/jama.291.13.1587.
    4. Shulman ST, Bisno AL, Clegg HW, Gerber MA, Kaplan EL, Lee G, Martin JM, Van Beneden C. 
    Clinical practice guideline for the diagnosis and management of group A streptococcal 
    pharyngitis: 2012 update by the Infectious Diseases Society of America. Clin Infect Dis. 
    2012 Nov 15;55(10):e86-102. doi: 10.1093/cid/cis629.
    """
    
    tonsillar_exudate: Literal["yes", "no"] = Field(
        ...,
        description="Presence of tonsillar swelling or exudate on physical examination. Scores 1 point if present",
        example="yes"
    )
    
    tender_cervical_nodes: Literal["yes", "no"] = Field(
        ...,
        description="Swollen, tender anterior cervical lymph nodes on palpation. Scores 1 point if present",
        example="yes"
    )
    
    history_of_fever: Literal["yes", "no"] = Field(
        ...,
        description="History of fever greater than 38°C (100.4°F) during current illness. Scores 1 point if present",
        example="yes"
    )
    
    absence_of_cough: Literal["yes", "no"] = Field(
        ...,
        description="Absence of cough (lack of upper respiratory symptoms suggests bacterial rather than viral etiology). Scores 1 point if cough is absent",
        example="no"
    )
    
    age_years: int = Field(
        ...,
        ge=3,
        le=120,
        description="Patient age in years. Age adjustment: 3-14 years (+1 point), 15-44 years (0 points), ≥45 years (-1 point)",
        example=25
    )
    
    class Config:
        schema_extra = {
            "example": {
                "tonsillar_exudate": "yes",
                "tender_cervical_nodes": "yes", 
                "history_of_fever": "yes",
                "absence_of_cough": "no",
                "age_years": 25
            }
        }


class CentorScoreResponse(BaseModel):
    """
    Response model for Centor Score (Modified/McIsaac) for Strep Pharyngitis
    
    The Modified Centor Score ranges from -1 to +5 points and provides:
    - Probability assessment for Group A Streptococcus (GAS) infection
    - Risk stratification (Low/Moderate/High Risk)  
    - Evidence-based management recommendations
    - Detailed scoring breakdown for clinical decision-making
    
    Risk Categories:
    - Low Risk (≤1 points): 1-10% GAS probability, no testing/antibiotics needed
    - Moderate Risk (2-3 points): 11-35% GAS probability, RADT/culture recommended
    - High Risk (≥4 points): 51-53% GAS probability, consider empiric treatment
    
    Clinical Impact:
    - Reduces unnecessary antibiotic prescriptions by 48%
    - Guides appropriate use of rapid antigen detection tests (RADT)
    - Endorsed by IDSA guidelines for pharyngitis management
    - Validated across multiple healthcare settings for both children and adults
    
    Reference: McIsaac WJ, et al. CMAJ. 1998;158(1):75-83.
    """
    
    result: Dict[str, Any] = Field(
        ...,
        description="Detailed Centor Score assessment including total score, probability, risk level, and scoring breakdown",
        example={
            "total_score": 3,
            "gas_probability_percent": "28-35%",
            "risk_level": "Moderate Risk",
            "management_recommendation": "RADT and/or throat culture recommended",
            "scoring_breakdown": {
                "clinical_criteria": {
                    "tonsillar_exudate": {"present": True, "points": 1, "description": "Tonsillar swelling or exudate"},
                    "tender_cervical_nodes": {"present": True, "points": 1, "description": "Swollen, tender anterior cervical lymph nodes"},
                    "history_of_fever": {"present": True, "points": 1, "description": "History of fever (>38°C or 100.4°F)"},
                    "absence_of_cough": {"present": False, "points": 0, "description": "Absence of cough"}
                },
                "age_adjustment": {"age_years": 25, "age_category": "15-44 years (baseline risk)", "points": 0, "description": "Age-based risk adjustment"}
            }
        }
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation with probability assessment and evidence-based management recommendations",
        example="Centor Score 3: Moderate probability of Group A Streptococcus (28-35%). Rapid antigen detection test (RADT) and/or throat culture recommended. Prescribe antibiotics only if test results are positive. Avoid empiric antibiotic treatment."
    )
    
    stage: str = Field(
        ...,
        description="Risk stratification category (Low Risk, Moderate Risk, High Risk)",
        example="Moderate Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the risk category",
        example="Moderate probability of streptococcal infection"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": {
                    "total_score": 3,
                    "gas_probability_percent": "28-35%",
                    "risk_level": "Moderate Risk",
                    "management_recommendation": "RADT and/or throat culture recommended",
                    "scoring_breakdown": {
                        "clinical_criteria": {
                            "tonsillar_exudate": {
                                "present": True,
                                "points": 1,
                                "description": "Tonsillar swelling or exudate"
                            },
                            "tender_cervical_nodes": {
                                "present": True,
                                "points": 1, 
                                "description": "Swollen, tender anterior cervical lymph nodes"
                            },
                            "history_of_fever": {
                                "present": True,
                                "points": 1,
                                "description": "History of fever (>38°C or 100.4°F)"
                            },
                            "absence_of_cough": {
                                "present": False,
                                "points": 0,
                                "description": "Absence of cough"
                            }
                        },
                        "age_adjustment": {
                            "age_years": 25,
                            "age_category": "15-44 years (baseline risk)",
                            "points": 0,
                            "description": "Age-based risk adjustment"
                        }
                    }
                },
                "unit": "points",
                "interpretation": "Centor Score 3: Moderate probability of Group A Streptococcus (28-35%). Rapid antigen detection test (RADT) and/or throat culture recommended. Prescribe antibiotics only if test results are positive. Avoid empiric antibiotic treatment.",
                "stage": "Moderate Risk",
                "stage_description": "Moderate probability of streptococcal infection"
            }
        }