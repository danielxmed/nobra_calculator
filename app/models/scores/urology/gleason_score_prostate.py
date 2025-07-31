"""
Gleason Score for Prostate Cancer Models

Request and response models for Gleason Score calculation.

References (Vancouver style):
1. Gleason DF, Mellinger GT. Prediction of prognosis for prostatic adenocarcinoma by 
   combined histological grading and clinical staging. J Urol. 1974;111(1):58-64.
2. Epstein JI, Egevad L, Amin MB, et al. The 2014 International Society of Urological 
   Pathology (ISUP) Consensus Conference on Gleason Grading of Prostatic Carcinoma: 
   Definition of Grading Patterns and Proposal for a New Grading System. Am J Surg 
   Pathol. 2016;40(2):244-252. doi: 10.1097/PAS.0000000000000530.
3. Pierorazio PM, Walsh PC, Partin AW, Epstein JI. Prognostic Gleason grade grouping: 
   data based on the modified Gleason scoring system. BJU Int. 2013;111(5):753-760. 
   doi: 10.1111/j.1464-410X.2012.11611.x.
4. D'Amico AV, Whittington R, Malkowicz SB, et al. Biochemical outcome after radical 
   prostatectomy, external beam radiation therapy, or interstitial radiation therapy 
   for clinically localized prostate cancer. JAMA. 1998;280(11):969-974. 
   doi: 10.1001/jama.280.11.969.

The Gleason Score is the most widely used histologic grading system for prostate cancer, 
developed by Dr. Donald Gleason in the 1960s and modified by the International Society 
of Urological Pathology (ISUP) in 2014. It evaluates the microscopic architecture of 
prostate cancer cells and assigns grades based on how closely they resemble normal 
prostate tissue.

The scoring system combines two grades:
- Primary Grade (3-5): Most predominant tumor pattern (>50% of tumor volume)
- Secondary Grade (3-5): Second most common pattern (≥5% but <50% of tumor)

Gleason Grade Patterns:
- Grade 3: Well-formed glands with minimal architectural distortion
- Grade 4: Fused glands, ill-defined glands, or cribriform pattern  
- Grade 5: No glandular formation, solid sheets, or comedonecrosis

Total scores range from 6-10, with corresponding ISUP Grade Groups 1-5:
- Grade Group 1: Gleason 6 (3+3) - Favorable prognosis
- Grade Group 2: Gleason 7 (3+4) - Intermediate-favorable prognosis  
- Grade Group 3: Gleason 7 (4+3) - Intermediate-unfavorable prognosis
- Grade Group 4: Gleason 8 - Unfavorable prognosis
- Grade Group 5: Gleason 9-10 - Very unfavorable prognosis

The distinction between 3+4=7 and 4+3=7 is clinically significant, as the primary 
pattern influences prognosis and treatment decisions. This scoring system is essential 
for prostate cancer risk stratification and treatment planning.
"""

from pydantic import BaseModel, Field
from typing import Literal


class GleasonScoreProstateRequest(BaseModel):
    """
    Request model for Gleason Score for Prostate Cancer
    
    The Gleason Score uses two histologic grades to assess prostate cancer aggressiveness:
    
    Primary Grade (3-5): The most predominant tumor pattern observed microscopically
    - Must represent >50% of the total tumor volume
    - Reflects the dominant cellular architecture and differentiation
    - Has the greatest influence on prognosis and treatment decisions
    
    Secondary Grade (3-5): The second most common tumor pattern 
    - Must represent ≥5% but <50% of the tumor volume
    - Provides additional prognostic information
    - Important for distinguishing Grade Groups 2 and 3 when total score is 7
    
    Gleason Grade Descriptions:
    - Grade 3: Well-formed, distinct glands with minimal architectural distortion
      Cells maintain normal glandular appearance and organization
    - Grade 4: Fused glands, ill-defined glandular borders, or cribriform pattern
      Loss of normal glandular architecture with more aggressive appearance
    - Grade 5: No glandular formation, solid sheets of cells, or comedonecrosis
      Complete loss of glandular differentiation, most aggressive pattern
    
    Clinical Significance:
    The primary grade has greater prognostic impact than secondary grade. For example:
    - 3+4=7 (Grade Group 2): Better prognosis, primary well-differentiated pattern
    - 4+3=7 (Grade Group 3): Worse prognosis, primary poorly-differentiated pattern
    
    Modern pathology practice no longer assigns grades 1-2 as they represent normal 
    or benign tissue patterns. Current scoring uses only grades 3-5 for malignant tissue.

    References (Vancouver style):
    1. Gleason DF, Mellinger GT. Prediction of prognosis for prostatic adenocarcinoma by 
    combined histological grading and clinical staging. J Urol. 1974;111(1):58-64.
    2. Epstein JI, Egevad L, Amin MB, et al. The 2014 International Society of Urological 
    Pathology (ISUP) Consensus Conference on Gleason Grading of Prostatic Carcinoma: 
    Definition of Grading Patterns and Proposal for a New Grading System. Am J Surg 
    Pathol. 2016;40(2):244-252. doi: 10.1097/PAS.0000000000000530.
    """
    
    primary_grade: Literal[3, 4, 5] = Field(
        ...,
        description="Primary Gleason grade (3-5) representing the most predominant tumor pattern (>50% of tumor volume). Grade 3: well-formed glands; Grade 4: fused/ill-defined glands; Grade 5: no glandular formation",
        example=3
    )
    
    secondary_grade: Literal[3, 4, 5] = Field(
        ...,
        description="Secondary Gleason grade (3-5) representing the second most common tumor pattern (≥5% but <50% of tumor volume). Essential for distinguishing Grade Groups 2 (3+4) vs 3 (4+3)",
        example=4
    )
    
    class Config:
        schema_extra = {
            "example": {
                "primary_grade": 3,
                "secondary_grade": 4
            }
        }


class GleasonScoreProstateResponse(BaseModel):
    """
    Response model for Gleason Score for Prostate Cancer
    
    The Gleason score ranges from 6-10 points and corresponds to ISUP Grade Groups 1-5:
    
    Grade Group Classification:
    - Grade Group 1: Gleason 6 (3+3) - Low-grade cancer, favorable prognosis
    - Grade Group 2: Gleason 7 (3+4) - Intermediate-grade, more favorable  
    - Grade Group 3: Gleason 7 (4+3) - Intermediate-grade, less favorable
    - Grade Group 4: Gleason 8 - High-grade cancer, unfavorable prognosis
    - Grade Group 5: Gleason 9-10 - Very high-grade, very unfavorable prognosis
    
    Prognostic Significance:
    - Grade Group 1: >95% 10-year cancer-specific survival, often managed with surveillance
    - Grade Groups 2-3: 85-95% 10-year survival, typically require definitive treatment
    - Grade Group 4: 60-80% 10-year survival, aggressive multimodal treatment needed
    - Grade Group 5: 40-60% 10-year survival, immediate aggressive treatment required
    
    Treatment Implications:
    The Gleason Score influences treatment selection including active surveillance, 
    radical prostatectomy, radiation therapy, hormone therapy, and systemic treatments.
    It is also a key component of prostate cancer risk stratification systems.
    
    Reference: Epstein JI, et al. Am J Surg Pathol. 2016;40(2):244-252.
    """
    
    result: int = Field(
        ...,
        description="Total Gleason score calculated as primary + secondary grade (range: 6-10 points)",
        ge=6,
        le=10,
        example=7
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Comprehensive clinical interpretation including grade group, prognosis, and treatment recommendations based on the Gleason score and pattern",
        example="Gleason Score: 3+4=7. Grade Group 2 (3+4). Primary pattern 3 (Well-formed glands with minimal architectural distortion); Secondary pattern 4 (Fused glands, ill-defined glands, or cribriform pattern). Intermediate-grade prostate cancer with moderate aggressiveness and metastatic potential. Grade Group 2 (3+4=7) has more favorable prognosis than Grade Group 3 (4+3=7) due to predominant well-differentiated pattern. 10-year cancer-specific survival ranges 85-95%. Typically requires definitive treatment with curative intent."
    )
    
    stage: str = Field(
        ...,
        description="Cancer grade classification based on ISUP Grade Groups and prognostic risk (Low-Grade, Intermediate-Grade, High-Grade, Very High-Grade)",
        example="Intermediate-Grade Cancer (Grade Group 2-3)"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the grade level, differentiation status, and general prognosis",
        example="Moderately differentiated, intermediate prognosis"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 7,
                "unit": "points",
                "interpretation": "Gleason Score: 3+4=7. Grade Group 2 (3+4). Primary pattern 3 (Well-formed glands with minimal architectural distortion); Secondary pattern 4 (Fused glands, ill-defined glands, or cribriform pattern). Intermediate-grade prostate cancer with moderate aggressiveness and metastatic potential. Grade Group 2 (3+4=7) has more favorable prognosis than Grade Group 3 (4+3=7) due to predominant well-differentiated pattern. 10-year cancer-specific survival ranges 85-95%. Typically requires definitive treatment with curative intent. Treatment options include: radical prostatectomy, external beam radiation therapy (EBRT), brachytherapy, or combination therapies.",
                "stage": "Intermediate-Grade Cancer (Grade Group 2-3)",
                "stage_description": "Moderately differentiated, intermediate prognosis"
            }
        }