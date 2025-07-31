"""
International Prostate Symptom Score (IPSS)/American Urological Association Symptom Index (AUA-SI) Models

Request and response models for IPSS/AUA-SI symptom severity assessment.

References (Vancouver style):
1. Barry MJ, Fowler FJ Jr, O'Leary MP, Bruskewitz RC, Holtgrewe HL, Mebust WK, Cockett AT. 
   The American Urological Association symptom index for benign prostatic hyperplasia. 
   The Measurement Committee of the American Urological Association. J Urol. 1992 Nov;
   148(5):1549-57; discussion 1564. doi: 10.1016/s0022-5347(17)36966-5. PMID: 1279218.
2. Cockett AT, Aso Y, Denis L, Khoury S, Barry M, Carlton CE Jr, et al. World Health 
   Organization Consensus Committee recommendations concerning the diagnosis of BPH. 
   Prog Urol. 1991 Nov;1(6):957-72. PMID: 1843818.
3. Bosch JL, Hop WC, Kirkels WJ, Schröder FH. The International Prostate Symptom Score 
   in a community-based sample of men between 55 and 74 years of age: prevalence and 
   correlation of symptoms with age, prostate volume, flow rate and residual urine volume. 
   Br J Urol. 1995 Dec;76(6):625-33. doi: 10.1111/j.1464-410x.1995.tb07773.x. PMID: 8535670.

The International Prostate Symptom Score (IPSS), also known as the American Urological 
Association Symptom Index (AUA-SI), is a standardized questionnaire developed to assess 
the severity of lower urinary tract symptoms in men with benign prostatic hyperplasia (BPH).

Developed in 1992 by Barry et al. and endorsed by the World Health Organization, this 
7-question instrument quantifies urinary symptoms on a 35-point scale and serves as the 
gold standard for BPH symptom assessment worldwide.

Clinical Application:
The IPSS/AUA-SI is used for:
- Initial assessment of BPH symptom severity
- Treatment decision-making (watchful waiting vs. medical vs. surgical therapy)
- Monitoring response to treatment over time
- Research outcomes measurement
- Quality of life assessment in conjunction with optional quality of life question

Scoring System:
Each of the 7 questions is scored from 0-5 points:
- **0**: Not at all
- **1**: Less than 1 in 5 times
- **2**: Less than half the time
- **3**: About half the time
- **4**: More than half the time
- **5**: Almost always

Exception: Nocturia question is scored by actual number of episodes (0-5+).

Symptom Categories:
- **Mild (0-7 points)**: Watchful waiting with lifestyle modifications
- **Moderate (8-19 points)**: Consider medical therapy (alpha-blockers, 5-ARIs)
- **Severe (20-35 points)**: Medical therapy recommended, consider surgical options

Clinical Significance:
The IPSS has been validated in multiple populations and languages, demonstrating excellent 
reliability and correlation with objective measures of BPH such as peak flow rate and 
post-void residual volume. It remains the most widely used patient-reported outcome 
measure in BPH management.
"""

from pydantic import BaseModel, Field
from typing import Literal


class IpssAuaSiRequest(BaseModel):
    """
    Request model for International Prostate Symptom Score (IPSS)/AUA Symptom Index
    
    The IPSS/AUA-SI assesses the severity of lower urinary tract symptoms in men 
    using 7 standardized questions, each scored from 0-5 points:
    
    Symptom Questions and Scoring:
    
    1. **Incomplete Emptying** (0-5 points):
       - Assesses the sensation of incomplete bladder emptying after urination
       - 0 = Not at all, 1 = Less than 1 in 5 times, 2 = Less than half the time,
         3 = About half the time, 4 = More than half the time, 5 = Almost always
    
    2. **Frequency** (0-5 points):
       - Evaluates urinary frequency (urinating less than every 2 hours)
       - Same scoring scale as above
    
    3. **Intermittency** (0-5 points):
       - Measures interrupted or intermittent urinary stream
       - Same scoring scale as above
    
    4. **Urgency** (0-5 points):
       - Assesses difficulty postponing urination when feeling the urge
       - Same scoring scale as above
    
    5. **Weak Stream** (0-5 points):
       - Evaluates strength of urinary stream
       - Same scoring scale as above
    
    6. **Straining** (0-5 points):
       - Measures need to strain or push to start urination
       - Same scoring scale as above
    
    7. **Nocturia** (0-5 points):
       - Number of times getting up at night to urinate
       - 0 = None, 1 = 1 time, 2 = 2 times, 3 = 3 times, 4 = 4 times, 5 = ≥5 times
    
    Clinical Context:
    The IPSS is typically completed by male patients experiencing lower urinary tract 
    symptoms suggestive of benign prostatic hyperplasia. The questionnaire should be 
    completed independently by the patient, reflecting symptoms over the past month.
    
    The total score guides treatment decisions:
    - Watchful waiting for mild symptoms
    - Medical therapy for moderate symptoms  
    - Consideration of surgical intervention for severe symptoms
    
    References (Vancouver style):
    1. Barry MJ, Fowler FJ Jr, O'Leary MP, Bruskewitz RC, Holtgrewe HL, Mebust WK, et al. 
    The American Urological Association symptom index for benign prostatic hyperplasia. 
    J Urol. 1992;148(5):1549-57.
    2. Cockett AT, Aso Y, Denis L, Khoury S, Barry M, Carlton CE Jr, et al. World Health 
    Organization Consensus Committee recommendations concerning the diagnosis of BPH. 
    Prog Urol. 1991;1(6):957-72.
    """
    
    incomplete_emptying: int = Field(
        ...,
        ge=0,
        le=5,
        description="How often have you had the sensation of not emptying your bladder? Score: Not at all (0), Less than 1 in 5 times (1), Less than half the time (2), About half the time (3), More than half the time (4), Almost always (5)",
        example=1
    )
    
    frequency: int = Field(
        ...,
        ge=0,
        le=5,
        description="How often have you had to urinate less than every two hours? Score: Not at all (0), Less than 1 in 5 times (1), Less than half the time (2), About half the time (3), More than half the time (4), Almost always (5)",
        example=2
    )
    
    intermittency: int = Field(
        ...,
        ge=0,
        le=5,
        description="How often have you found you stopped and started again several times when you urinated? Score: Not at all (0), Less than 1 in 5 times (1), Less than half the time (2), About half the time (3), More than half the time (4), Almost always (5)",
        example=1
    )
    
    urgency: int = Field(
        ...,
        ge=0,
        le=5,
        description="How often have you found it difficult to postpone urination? Score: Not at all (0), Less than 1 in 5 times (1), Less than half the time (2), About half the time (3), More than half the time (4), Almost always (5)",
        example=2
    )
    
    weak_stream: int = Field(
        ...,
        ge=0,
        le=5,
        description="How often have you had a weak urinary stream? Score: Not at all (0), Less than 1 in 5 times (1), Less than half the time (2), About half the time (3), More than half the time (4), Almost always (5)",
        example=3
    )
    
    straining: int = Field(
        ...,
        ge=0,
        le=5,
        description="How often have you had to strain to start urination? Score: Not at all (0), Less than 1 in 5 times (1), Less than half the time (2), About half the time (3), More than half the time (4), Almost always (5)",
        example=1
    )
    
    nocturia: int = Field(
        ...,
        ge=0,
        le=5,
        description="How many times do you typically get up at night to urinate? Score: None (0), 1 time (1), 2 times (2), 3 times (3), 4 times (4), ≥5 times (5)",
        example=2
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "incomplete_emptying": 1,
                "frequency": 2,
                "intermittency": 1,
                "urgency": 2,
                "weak_stream": 3,
                "straining": 1,
                "nocturia": 2
            }
        }


class IpssAuaSiResponse(BaseModel):
    """
    Response model for International Prostate Symptom Score (IPSS)/AUA Symptom Index
    
    The IPSS provides symptom severity classification and treatment guidance based on 
    total score (0-35 points):
    
    Symptom Severity Categories and Management:
    
    **Mild Symptoms (0-7 points)**:
    - Clinical Significance: Mild BPH symptoms with minimal impact on quality of life
    - Management: Watchful waiting is appropriate as first-line approach
    - Interventions: Lifestyle modifications (fluid management, bladder training, 
      avoiding caffeine/alcohol before bedtime)
    - Monitoring: Annual reassessment with IPSS and clinical evaluation
    - Medical Therapy: Generally not required unless symptoms are bothersome to patient
    - Follow-up: Regular monitoring for symptom progression
    
    **Moderate Symptoms (8-19 points)**:
    - Clinical Significance: Moderate BPH symptoms causing noticeable impact on daily life
    - Management: Medical therapy typically recommended as first-line treatment
    - Medications: Alpha-blockers (tamsulosin, alfuzosin, doxazosin, terazosin) for 
      immediate symptom relief, or 5-alpha reductase inhibitors (finasteride, dutasteride) 
      for prostate size reduction in larger glands
    - Combination Therapy: Consider alpha-blocker plus 5-ARI for optimal symptom control
    - Lifestyle: Continue behavioral modifications alongside medical therapy
    - Monitoring: Reassess symptoms every 3-6 months, monitor for treatment response
    
    **Severe Symptoms (20-35 points)**:
    - Clinical Significance: Severe BPH symptoms significantly impacting quality of life
    - Management: Medical therapy strongly recommended, consider surgical intervention
    - Initial Treatment: Combination medical therapy (alpha-blocker + 5-ARI)
    - Surgical Consideration: If medical therapy fails, patient preference, or complications 
      present (recurrent UTIs, bladder stones, gross hematuria, renal insufficiency)
    - Surgical Options: TURP, laser procedures, minimally invasive therapies based on 
      prostate size and patient factors
    - Monitoring: Close follow-up every 1-3 months initially, then every 6 months
    - Complications: Screen for urinary retention, UTIs, and upper urinary tract changes
    
    Clinical Validation:
    The IPSS has been extensively validated with strong test-retest reliability (r=0.92) 
    and significant correlation with objective measures including peak flow rate (r=-0.51) 
    and post-void residual volume (r=0.28). The questionnaire is available in over 30 
    languages and is endorsed by major urological societies worldwide.
    
    Quality of Life Impact:
    While not included in the total score calculation, the optional quality of life 
    question provides important context for treatment decisions and should be considered 
    alongside the symptom score when counseling patients about treatment options.
    
    Reference: Barry MJ, et al. J Urol. 1992;148(5):1549-57.
    """
    
    result: int = Field(
        ...,
        ge=0,
        le=35,
        description="Total IPSS/AUA-SI score calculated by summing all 7 symptom questions (range: 0-35 points)",
        example=12
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation with specific treatment recommendations based on symptom severity classification",
        example="Moderate benign prostatic hyperplasia symptoms. Consider medical treatment with alpha-blockers, 5-alpha reductase inhibitors, or combination therapy. Lifestyle modifications and regular follow-up recommended."
    )
    
    stage: str = Field(
        ...,
        description="BPH symptom severity classification (Mild, Moderate, Severe)",
        example="Moderate"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the symptom severity category",
        example="Moderate BPH symptoms"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "result": 12,
                "unit": "points",
                "interpretation": "Moderate benign prostatic hyperplasia symptoms. Consider medical treatment with alpha-blockers, 5-alpha reductase inhibitors, or combination therapy. Lifestyle modifications and regular follow-up recommended.",
                "stage": "Moderate",
                "stage_description": "Moderate BPH symptoms"
            }
        }