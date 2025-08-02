"""
Immune-Related Adverse Events for GI Toxicity - Hepatitis Models

Request and response models for immune-related adverse events GI hepatitis grading.

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

4. De Martin E, Michot JM, Papoular B, Champiat S, Mateus C, Lambotte O, et al. 
   Characterization of liver injury induced by cancer immunotherapy using immune 
   checkpoint inhibitors. J Hepatol. 2018 Jun;68(6):1181-1190. 
   doi: 10.1016/j.jhep.2018.01.033.

The immune-related adverse events (irAE) grading system for GI toxicity specifically 
addresses hepatitis induced by immune checkpoint inhibitors (ICPi). This grading system 
is based on Common Terminology Criteria for Adverse Events (CTCAE) Version 5.0 and 
provides standardized criteria for assessing hepatitis severity and guiding clinical 
management decisions. ICPi-induced hepatitis has an incidence of 5-10% in single-agent 
therapy but severe toxicity occurs in less than 2% of cases, requiring immediate 
recognition and appropriate management to prevent life-threatening complications.
"""

from pydantic import BaseModel, Field
from typing import Literal


class ImmuneRelatedAdverseEventsGiHepatitisRequest(BaseModel):
    """
    Request model for Immune-Related Adverse Events for GI Toxicity - Hepatitis
    
    This grading system evaluates hepatitis severity in patients receiving immune 
    checkpoint inhibitor therapy based on liver function tests and clinical signs:
    
    Grading Criteria (CTCAE v5.0):
    - Grade 1: AST/ALT 1-3× ULN OR total bilirubin 1-1.5× ULN - Continue ICPi with monitoring
    - Grade 2: AST/ALT 3-5× ULN OR total bilirubin 1.5-3× ULN - Hold ICPi, consider steroids
    - Grade 3: AST/ALT 5-20× ULN OR total bilirubin 3-10× ULN - Permanently discontinue ICPi
    - Grade 4: AST/ALT >20× ULN OR total bilirubin >10× ULN OR hepatic decompensation - Immediate hospitalization
    
    Clinical Context:
    - Hepatic irAEs have incidence of 5-10% in single-agent ICI therapy
    - Severe toxicity occurs in <2% of cases but requires immediate intervention
    - Baseline liver chemistries should be obtained before ICI therapy
    - Monitor liver function before each treatment cycle
    - Consider alternative etiologies (viral, drug-induced, autoimmune, alcohol)
    
    Management Principles:
    - Grade 1: Continue ICPi, monitor closely, repeat LFTs 1-2x weekly
    - Grade 2: Hold ICPi, corticosteroids (1 mg/kg/day), hepatology consultation
    - Grade 3-4: Permanently discontinue ICPi, high-dose steroids (2 mg/kg/day), hospitalization
    - Liver biopsy should be considered when diagnosis is unclear
    
    Laboratory Parameters:
    - AST (aspartate aminotransferase): typically 10-40 U/L normal range
    - ALT (alanine aminotransferase): typically 7-56 U/L normal range  
    - Total bilirubin: typically 0.2-1.2 mg/dL normal range
    - ULN (upper limit of normal) varies by laboratory - check local reference ranges
    
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
    4. De Martin E, Michot JM, Papoular B, Champiat S, Mateus C, Lambotte O, et al. 
    Characterization of liver injury induced by cancer immunotherapy using immune 
    checkpoint inhibitors. J Hepatol. 2018 Jun;68(6):1181-1190. 
    doi: 10.1016/j.jhep.2018.01.033.
    """
    
    ast_level: float = Field(
        ...,
        description="Aspartate aminotransferase (AST) level in U/L. Key parameter for hepatitis grading. Normal range typically 10-40 U/L depending on laboratory. Used to calculate AST fold increase over upper limit of normal (ULN)",
        example=120.0,
        ge=5.0,
        le=5000.0
    )
    
    ast_uln: float = Field(
        ...,
        description="Upper limit of normal (ULN) for AST at your laboratory. Typically 40 U/L but may vary by institution. Required to calculate fold increase over normal values for CTCAE grading",
        example=40.0,
        ge=20.0,
        le=80.0
    )
    
    alt_level: float = Field(
        ...,
        description="Alanine aminotransferase (ALT) level in U/L. Key parameter for hepatitis grading. Normal range typically 7-56 U/L depending on laboratory. Used to calculate ALT fold increase over upper limit of normal (ULN)",
        example=150.0,
        ge=5.0,
        le=5000.0
    )
    
    alt_uln: float = Field(
        ...,
        description="Upper limit of normal (ULN) for ALT at your laboratory. Typically 40-56 U/L but may vary by institution. Required to calculate fold increase over normal values for CTCAE grading",
        example=40.0,
        ge=20.0,
        le=80.0
    )
    
    total_bilirubin: float = Field(
        ...,
        description="Total bilirubin level in mg/dL. Critical parameter for severe hepatitis grading. Normal range typically 0.2-1.2 mg/dL. Elevated levels indicate hepatocellular injury or cholestasis",
        example=1.8,
        ge=0.1,
        le=50.0
    )
    
    bilirubin_uln: float = Field(
        ...,
        description="Upper limit of normal (ULN) for total bilirubin at your laboratory. Typically 1.0-1.2 mg/dL but may vary by institution. Required to calculate fold increase for CTCAE grading",
        example=1.2,
        ge=0.8,
        le=2.0
    )
    
    hepatic_decompensation: Literal["yes", "no"] = Field(
        ...,
        description="Presence of signs of hepatic decompensation including ascites, hepatic encephalopathy, coagulopathy, or variceal bleeding. Any decompensation warrants Grade 4 classification regardless of laboratory values",
        example="no"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "ast_level": 120.0,
                "ast_uln": 40.0,
                "alt_level": 150.0,
                "alt_uln": 40.0,
                "total_bilirubin": 1.8,
                "bilirubin_uln": 1.2,
                "hepatic_decompensation": "no"
            }
        }


class ImmuneRelatedAdverseEventsGiHepatitisResponse(BaseModel):
    """
    Response model for Immune-Related Adverse Events for GI Toxicity - Hepatitis
    
    The irAE grading system provides standardized assessment of hepatitis severity 
    and evidence-based management recommendations for immune checkpoint inhibitor-induced 
    hepatotoxicity:
    
    Grade 1 (Mild): Continue ICPi with close monitoring and repeat LFTs 1-2x weekly
    Grade 2 (Moderate): Hold ICPi, corticosteroids, hepatology consultation
    Grade 3 (Severe): Permanently discontinue ICPi, high-dose steroids, hospitalization
    Grade 4 (Life-threatening): Immediate hospitalization, IV steroids, intensive care consultation
    
    Clinical Implications:
    - Grade 2+ requires holding ICPi and hepatology consultation
    - Grade 3-4 requires permanent ICPi discontinuation
    - Consider alternative etiologies: viral, drug-induced, autoimmune, alcohol
    - Liver biopsy may be needed for unclear diagnosis or refractory cases
    - Monitor for hepatic decompensation in severe cases
    
    Reference: Brahmer JR, et al. J Clin Oncol. 2018;36(17):1714-1768.
    """
    
    result: int = Field(
        ...,
        description="irAE grade for GI hepatitis based on CTCAE v5.0 criteria (range: 1-4)",
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
        description="Clinical interpretation with detailed management recommendations including ICPi therapy decisions, corticosteroid treatment, hepatology consultation needs, and monitoring for complications",
        example="Hold ICPi until symptoms improve to grade ≤1. Start corticosteroids (methylprednisolone 1 mg/kg/day or equivalent). Obtain hepatology consultation. Rule out infectious and autoimmune causes. Consider liver biopsy if diagnosis unclear. Monitor liver function tests closely. Resume ICPi when grade ≤1 and steroids tapered."
    )
    
    stage: str = Field(
        ...,
        description="irAE grade classification with severity descriptor",
        example="Grade 2"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the grade severity and clinical criteria",
        example="Moderate - AST/ALT 3-5× ULN OR total bilirubin 1.5-3× ULN"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 2,
                "unit": "grade",
                "interpretation": "Hold ICPi until symptoms improve to grade ≤1. Start corticosteroids (methylprednisolone 1 mg/kg/day or equivalent). Obtain hepatology consultation. Rule out infectious and autoimmune causes. Consider liver biopsy if diagnosis unclear. Monitor liver function tests closely. Resume ICPi when grade ≤1 and steroids tapered.",
                "stage": "Grade 2",
                "stage_description": "Moderate - AST/ALT 3-5× ULN OR total bilirubin 1.5-3× ULN"
            }
        }