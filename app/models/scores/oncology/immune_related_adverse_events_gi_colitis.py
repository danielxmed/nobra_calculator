"""
Immune-Related Adverse Events for GI Toxicity - Colitis Models

Request and response models for immune-related adverse events GI colitis grading.

References (Vancouver style):
1. Brahmer JR, Lacchetti C, Schneider BJ, Atkins MB, Brassil KJ, Caterino JM, et al. 
   Management of Immune-Related Adverse Events in Patients Treated With Immune 
   Checkpoint Inhibitor Therapy: American Society of Clinical Oncology Clinical 
   Practice Guideline. J Clin Oncol. 2018 Jun 10;36(17):1714-1768. 
   doi: 10.1200/JCO.2017.77.6385.

2. Thompson JA, Schneider BJ, Brahmer J, Andrews S, Armand P, Bhatia S, et al. 
   NCCN Guidelines Insights: Management of Immunotherapy-Related Toxicities, 
   Version 1.2020. J Natl Compr Canc Netw. 2020 Mar 1;18(3):230-241. 
   doi: 10.6004/jnccn.2020.0012.

3. Wang DY, Salem JE, Cohen JV, Chandra S, Menzer C, Ye F, et al. Fatal Toxic 
   Effects Associated With Immune Checkpoint Inhibitors: A Systematic Review 
   and Meta-analysis. JAMA Oncol. 2018 Dec 1;4(12):1721-1728. 
   doi: 10.1001/jamaoncol.2018.3923.

4. Gupta A, De Felice KM, Loftus EV Jr, Khanna S. Systematic review: colitis 
   associated with anti-CTLA-4 therapy. Aliment Pharmacol Ther. 2015 Aug;42(4):406-17. 
   doi: 10.1111/apt.13281.

The immune-related adverse events (irAE) grading system for GI toxicity specifically 
addresses colitis induced by immune checkpoint inhibitors (ICPi). This grading system 
is based on Common Terminology Criteria for Adverse Events (CTCAE) Version 5.0 and 
provides standardized criteria for assessing colitis severity and guiding clinical 
management decisions. ICPi-induced colitis most frequently occurs 5-10 weeks after 
treatment initiation and is more common with anti-CTLA-4 agents (ipilimumab) than 
anti-PD-1/PD-L1 therapy, with potential for life-threatening complications requiring 
immediate recognition and appropriate management.
"""

from pydantic import BaseModel, Field
from typing import Literal


class ImmuneRelatedAdverseEventsGiColitisRequest(BaseModel):
    """
    Request model for Immune-Related Adverse Events for GI Toxicity - Colitis
    
    This grading system evaluates colitis severity in patients receiving immune 
    checkpoint inhibitor therapy based on four key clinical parameters:
    
    Grading Criteria:
    - Grade 1: <4 stools/day increase over baseline, minimal functional impact - Continue ICPi with monitoring
    - Grade 2: 4-6 stools/day increase OR moderate functional limitation - Hold ICPi, consider steroids
    - Grade 3: ≥7 stools/day increase OR incontinence OR severe limitation OR hospitalization - Consider permanent CTLA-4 discontinuation
    - Grade 4: Life-threatening consequences - Permanent ICPi discontinuation, immediate hospitalization
    
    Clinical Context:
    - Most frequently occurs 5-10 weeks after ICPi treatment initiation
    - More common with anti-CTLA-4 agents (ipilimumab) than anti-PD-1/PD-L1 agents
    - Mortality rate up to 1-2% for severe cases, mainly from perforation/sepsis
    - Grade 2+ requires holding ICPi and gastroenterology consultation
    - Corticosteroids are first-line treatment for grade 2-4 colitis
    
    Management Principles:
    - Grade 1: Continue ICPi, dietary modifications, supportive care
    - Grade 2: Hold ICPi, corticosteroids (1 mg/kg/day), GI consultation
    - Grade 3: Consider permanent CTLA-4 discontinuation, hospitalization, high-dose steroids
    - Grade 4: Permanent ICPi discontinuation, immediate hospitalization, IV steroids, infliximab
    
    Monitoring Parameters:
    - Stool frequency and consistency
    - Functional status and activities of daily living
    - Signs of complications (bleeding, perforation, sepsis)
    - Exclude infectious causes (C. diff, CMV, parasites)
    
    References (Vancouver style):
    1. Brahmer JR, Lacchetti C, Schneider BJ, Atkins MB, Brassil KJ, Caterino JM, et al. 
    Management of Immune-Related Adverse Events in Patients Treated With Immune 
    Checkpoint Inhibitor Therapy: American Society of Clinical Oncology Clinical 
    Practice Guideline. J Clin Oncol. 2018 Jun 10;36(17):1714-1768. 
    doi: 10.1200/JCO.2017.77.6385.
    2. Thompson JA, Schneider BJ, Brahmer J, Andrews S, Armand P, Bhatia S, et al. 
    NCCN Guidelines Insights: Management of Immunotherapy-Related Toxicities, 
    Version 1.2020. J Natl Compr Canc Netw. 2020 Mar 1;18(3):230-241. 
    doi: 10.6004/jnccn.2020.0012.
    3. Wang DY, Salem JE, Cohen JV, Chandra S, Menzer C, Ye F, et al. Fatal Toxic 
    Effects Associated With Immune Checkpoint Inhibitors: A Systematic Review 
    and Meta-analysis. JAMA Oncol. 2018 Dec 1;4(12):1721-1728. 
    doi: 10.1001/jamaoncol.2018.3923.
    4. Gupta A, De Felice KM, Loftus EV Jr, Khanna S. Systematic review: colitis 
    associated with anti-CTLA-4 therapy. Aliment Pharmacol Ther. 2015 Aug;42(4):406-17. 
    doi: 10.1111/apt.13281.
    """
    
    stool_increase_per_day: int = Field(
        ...,
        description="Increase in number of stools per day over baseline. Key parameter for grading severity. Grade 1: <4 increase, Grade 2: 4-6 increase, Grade 3: ≥7 increase. Baseline should be patient's normal pre-treatment bowel frequency",
        example=5,
        ge=0,
        le=20
    )
    
    incontinence_present: Literal["yes", "no"] = Field(
        ...,
        description="Presence of fecal incontinence indicating severe colitis. Any incontinence warrants at least Grade 3 classification. Associated with significant mucosal inflammation and urgency",
        example="no"
    )
    
    functional_impact: Literal["none_minimal", "moderate_limiting", "severe_limiting", "life_threatening"] = Field(
        ...,
        description="Impact on activities of daily living and functional status. None/minimal: normal activities maintained. Moderate limiting: some limitation but can perform ADLs. Severe limiting: unable to perform self-care ADLs. Life-threatening: requires urgent intervention",
        example="moderate_limiting"
    )
    
    hospitalization_indicated: Literal["yes", "no"] = Field(
        ...,
        description="Clinical indication for hospitalization based on severity, complications, or inability to maintain oral intake. Indicates at least Grade 3 severity. Consider for dehydration, electrolyte imbalances, bleeding, or perforation risk",
        example="no"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "stool_increase_per_day": 5,
                "incontinence_present": "no",
                "functional_impact": "moderate_limiting",
                "hospitalization_indicated": "no"
            }
        }


class ImmuneRelatedAdverseEventsGiColitisResponse(BaseModel):
    """
    Response model for Immune-Related Adverse Events for GI Toxicity - Colitis
    
    The irAE grading system provides standardized assessment of colitis severity 
    and evidence-based management recommendations for immune checkpoint inhibitor-induced 
    gastrointestinal toxicity:
    
    Grade 1 (Mild): Continue ICPi with dietary modifications and monitoring
    Grade 2 (Moderate): Hold ICPi, corticosteroids, gastroenterology consultation
    Grade 3 (Severe): Consider permanent CTLA-4 discontinuation, hospitalization, high-dose steroids
    Grade 4 (Life-threatening): Permanent ICPi discontinuation, immediate hospitalization, IV steroids, infliximab
    
    Clinical Implications:
    - Grade 2+ requires holding ICPi and gastroenterology consultation
    - CTLA-4 agents should be permanently discontinued for grade 3-4 colitis
    - Anti-PD-1/PD-L1 agents may be resumed after grade 2-3 resolution
    - Monitor for life-threatening complications: perforation, bleeding, sepsis
    
    Reference: Brahmer JR, et al. J Clin Oncol. 2018;36(17):1714-1768.
    """
    
    result: int = Field(
        ...,
        description="irAE grade for GI colitis based on CTCAE v5.0 criteria (range: 1-4)",
        example=2,
        ge=1,
        le=4
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the grading system",
        example="grade"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation with detailed management recommendations including ICPi therapy decisions, corticosteroid treatment, gastroenterology consultation needs, and monitoring for complications",
        example="Hold ICPi until symptoms improve to grade ≤1. Consider corticosteroids (prednisone 1 mg/kg/day). Provide supportive care including loperamide, hydration, electrolyte monitoring. Obtain gastroenterology consultation. Consider endoscopy evaluation to assess mucosal inflammation. Monitor for progression to higher grade. Resume ICPi when symptoms controlled."
    )
    
    stage: str = Field(
        ...,
        description="irAE grade classification with severity descriptor",
        example="Grade 2"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the grade severity and clinical presentation",
        example="Moderate - Increase of 4-6 stools per day over baseline"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 2,
                "unit": "grade",
                "interpretation": "Hold ICPi until symptoms improve to grade ≤1. Consider corticosteroids (prednisone 1 mg/kg/day). Provide supportive care including loperamide, hydration, electrolyte monitoring. Obtain gastroenterology consultation. Consider endoscopy evaluation to assess mucosal inflammation. Monitor for progression to higher grade. Resume ICPi when symptoms controlled.",
                "stage": "Grade 2",
                "stage_description": "Moderate - Increase of 4-6 stools per day over baseline"
            }
        }