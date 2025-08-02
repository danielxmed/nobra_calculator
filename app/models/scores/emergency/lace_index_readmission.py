"""
LACE Index for Readmission Models

Request and response models for LACE Index readmission risk calculation.

References (Vancouver style):
1. van Walraven C, Dhalla IA, Bell C, Etchells E, Stiell IG, Zarnke K, et al. 
   Derivation and validation of an index to predict early death or unplanned 
   readmission after discharge from hospital to the community. CMAJ. 2010 Apr 
   6;182(6):551-7. doi: 10.1503/cmaj.091117.
2. Walraven C, Wong J, Forster AJ. LACE+ index: extension of a validated index 
   to predict early death or urgent readmission after hospital discharge using 
   administrative data. Open Med. 2012;6(4):e80-90. PMID: 23696773.
3. Gruneir A, Dhalla IA, van Walraven C, Fischer HD, Camacho X, Rochon PA, et al. 
   Unplanned readmissions after hospital discharge among patients identified as 
   being at high risk for readmission using a validated predictive algorithm. 
   Open Med. 2011;5(2):e104-11. PMID: 22046219.
4. Low LL, Tan SY, Ng MJ, Tay WY, Ng LB, Balasubramaniam K, et al. Applying 
   the LACE index to an Asian population to predict 30-day hospital readmissions 
   in an accountable care organization. Medicine (Baltimore). 2017 Jan;96(4):e5728. 
   doi: 10.1097/MD.0000000000005728.

The LACE Index is a validated clinical prediction tool that identifies patients at high 
risk for 30-day readmission or death after hospital discharge. It combines four key 
administrative and clinical factors available at discharge to stratify patients into 
risk categories, enabling targeted interventions and resource allocation.

LACE Components:
- L (Length of stay): Hospital length of stay in days (0-7 points)
- A (Acuity): Acute/emergent admission status (0 or 3 points)
- C (Comorbidity): Charlson Comorbidity Index score (0-5 points)
- E (Emergency visits): ED visits in prior 6 months (0-4 points)

Clinical Applications:
- Discharge planning and care coordination
- Resource allocation for high-risk patients
- Quality improvement initiatives
- Population health management
- Care transitions programs

Performance Characteristics:
- Original validation C-statistic: 0.684
- Applicable to medical and surgical patients ≥18 years
- Based on readily available administrative data
- Externally validated in multiple populations and healthcare systems
- Risk stratification: Low (0-4), Moderate (5-9), High (≥10 points)

The LACE Index has been implemented widely in healthcare systems to identify patients 
who would benefit from enhanced discharge planning, early follow-up, and care coordination 
interventions to reduce preventable readmissions and improve patient outcomes.
"""

from pydantic import BaseModel, Field
from typing import Literal


class LaceIndexReadmissionRequest(BaseModel):
    """
    Request model for LACE Index for Readmission calculation
    
    The LACE Index uses four administrative and clinical factors to predict 30-day 
    readmission or death risk. All parameters should be determined at the time of 
    discharge planning:
    
    Clinical Parameters:
    - Length of Stay: Current hospitalization duration (primary predictor)
    - Acute Admission: Whether admission was unplanned/emergent
    - Charlson Comorbidity Index: Weighted comorbidity score (0-37 scale)
    - Emergency Visits: ED utilization in 6 months prior to current admission
    
    Scoring System:
    Length of Stay Points:
    - <1 day: 0 points | 1 day: 1 point | 2 days: 2 points | 3 days: 3 points
    - 4-6 days: 4 points | 7-13 days: 5 points | ≥14 days: 7 points
    
    Acute Admission Points:
    - No (planned): 0 points | Yes (unplanned/emergent): 3 points
    
    Charlson Comorbidity Points:
    - 0: 0 points | 1: 1 point | 2: 2 points | 3: 3 points | ≥4: 5 points
    
    Emergency Visits Points:
    - 0: 0 points | 1: 1 point | 2: 2 points | 3: 3 points | ≥4: 4 points
    
    Risk Stratification:
    - Low Risk (0-4 points): Standard discharge planning
    - Moderate Risk (5-9 points): Enhanced discharge planning and follow-up
    - High Risk (≥10 points): Intensive care coordination and early follow-up
    
    Clinical Context:
    - Validated for adults ≥18 years in medical and surgical populations
    - Uses data readily available at discharge
    - Helps identify patients for targeted interventions
    - Should be combined with clinical judgment
    
    References (Vancouver style):
    1. van Walraven C, Dhalla IA, Bell C, Etchells E, Stiell IG, Zarnke K, et al. 
    Derivation and validation of an index to predict early death or unplanned 
    readmission after discharge from hospital to the community. CMAJ. 2010 Apr 
    6;182(6):551-7. doi: 10.1503/cmaj.091117.
    2. Walraven C, Wong J, Forster AJ. LACE+ index: extension of a validated index 
    to predict early death or urgent readmission after hospital discharge using 
    administrative data. Open Med. 2012;6(4):e80-90.
    """
    
    length_of_stay_days: int = Field(
        ...,
        description="Length of current hospital stay in days. Longer stays indicate higher complexity "
                   "and risk. Range: 0 to reasonable maximum (e.g., 365 days). "
                   "Scoring: <1 day=0pts, 1 day=1pt, 2 days=2pts, 3 days=3pts, 4-6 days=4pts, "
                   "7-13 days=5pts, ≥14 days=7pts.",
        ge=0,
        le=365,
        example=5
    )
    
    acute_emergent_admission: Literal["yes", "no"] = Field(
        ...,
        description="Whether this was an acute/emergent (unplanned) admission through the emergency "
                   "department versus a planned/elective admission. Acute admissions carry higher "
                   "readmission risk. Scoring: No=0 points, Yes=3 points.",
        example="yes"
    )
    
    charlson_comorbidity_index: int = Field(
        ...,
        description="Charlson Comorbidity Index score (0-37) based on ICD diagnostic codes. "
                   "Weighted index of comorbid conditions that predicts mortality and healthcare "
                   "utilization. Higher scores indicate greater disease burden. "
                   "Scoring: 0=0pts, 1=1pt, 2=2pts, 3=3pts, ≥4=5pts.",
        ge=0,
        le=37,
        example=2
    )
    
    ed_visits_6_months: int = Field(
        ...,
        description="Number of emergency department visits in the 6 months prior to the current "
                   "admission (excluding the current admission). Frequent ED use indicates higher "
                   "healthcare needs and readmission risk. Count all ED visits regardless of disposition. "
                   "Scoring: 0=0pts, 1=1pt, 2=2pts, 3=3pts, ≥4=4pts.",
        ge=0,
        le=20,
        example=1
    )
    
    class Config:
        schema_extra = {
            "example": {
                "length_of_stay_days": 5,
                "acute_emergent_admission": "yes",
                "charlson_comorbidity_index": 2,
                "ed_visits_6_months": 1
            }
        }


class LaceIndexReadmissionResponse(BaseModel):
    """
    Response model for LACE Index for Readmission calculation
    
    Provides comprehensive readmission risk stratification with clinical recommendations 
    for discharge planning and care coordination. The LACE Index score ranges from 0-19 
    points and stratifies patients into three risk categories with specific interventions.
    
    Score Components and Interpretation:
    - Total Score: Sum of L+A+C+E components (0-19 points possible)
    - Risk Categories: Low (0-4), Moderate (5-9), High (≥10 points)
    - Component Breakdown: Individual scores for transparency and clinical insight
    
    Clinical Risk Stratification:
    
    Low Risk (0-4 points):
    - Estimated 30-day readmission/death risk: ~5-10%
    - Standard discharge planning appropriate
    - Routine follow-up within 1-2 weeks
    - Standard patient education and medication reconciliation
    
    Moderate Risk (5-9 points):
    - Estimated 30-day readmission/death risk: ~10-15%
    - Enhanced discharge planning recommended
    - Follow-up within 7-14 days post-discharge
    - Care coordination and structured patient education
    - Consider post-discharge phone calls
    
    High Risk (≥10 points):
    - Estimated 30-day readmission/death risk: ~15-25%
    - Intensive discharge planning and care coordination
    - Early follow-up within 48-72 hours
    - Multidisciplinary team involvement
    - Home health services consideration
    - Comprehensive medication reconciliation
    - Case management and social services as needed
    
    Implementation Considerations:
    - Use as part of comprehensive discharge planning
    - Combine with clinical judgment and patient-specific factors
    - Consider local healthcare system resources and capabilities
    - Monitor outcomes and adjust interventions based on performance
    - Document interventions for quality improvement purposes
    
    Performance Characteristics:
    - Original validation C-statistic: 0.684 (moderate discrimination)
    - Calibration: Good across risk deciles
    - Generalizability: Validated in multiple populations and healthcare systems
    - Reliability: Based on objective, readily available data
    
    Reference: van Walraven C, et al. CMAJ. 2010;182(6):551-7.
    """
    
    result: int = Field(
        ...,
        description="Total LACE Index score calculated from four components (range: 0-19 points)",
        example=11
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the LACE score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Comprehensive clinical interpretation including component breakdown, risk assessment, "
                   "and specific recommendations for discharge planning and care coordination",
        example="LACE Index = 11 points (L:4 + A:3 + C:2 + E:1). This score indicates high risk for 30-day readmission or death. Intensive discharge planning and care coordination strongly recommended. Consider early post-discharge follow-up within 48-72 hours. Medication reconciliation, home health services, and patient/caregiver education are crucial. Multidisciplinary team approach with case management may be beneficial. The LACE Index is validated for adults ≥18 years and considers key predictors: length of stay, admission acuity, comorbidity burden, and recent healthcare utilization. Use in conjunction with clinical judgment and institutional discharge protocols."
    )
    
    stage: str = Field(
        ...,
        description="Risk category classification based on total LACE score",
        example="High Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the risk level",
        example="High risk of 30-day readmission or death"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 11,
                "unit": "points",
                "interpretation": "LACE Index = 11 points (L:4 + A:3 + C:2 + E:1). This score indicates high risk for 30-day readmission or death. Intensive discharge planning and care coordination strongly recommended. Consider early post-discharge follow-up within 48-72 hours. Medication reconciliation, home health services, and patient/caregiver education are crucial. Multidisciplinary team approach with case management may be beneficial. The LACE Index is validated for adults ≥18 years and considers key predictors: length of stay, admission acuity, comorbidity burden, and recent healthcare utilization. Use in conjunction with clinical judgment and institutional discharge protocols.",
                "stage": "High Risk",
                "stage_description": "High risk of 30-day readmission or death"
            }
        }