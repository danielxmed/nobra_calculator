"""
GALAD Model for Hepatocellular Carcinoma (HCC) Models

Request and response models for GALAD Model HCC detection.

References (Vancouver style):
1. Johnson PJ, Pirrie SJ, Cox TF, et al. The detection of hepatocellular carcinoma using 
   a prospectively developed and validated model based on serological biomarkers. Cancer 
   Epidemiol Biomarkers Prev. 2014;23(1):144-53. doi: 10.1158/1055-9965.EPI-13-0870.
2. Best J, Bechmann LP, Sowa JP, et al. GALAD Score Detects Early Hepatocellular Carcinoma 
   in an International Cohort of Patients With Nonalcoholic Steatohepatitis. Clin Gastroenterol 
   Hepatol. 2020;18(3):728-735.e4. doi: 10.1016/j.cgh.2019.08.012.
3. Yang JD, Addissie BD, Mara KC, et al. GALAD Score for Hepatocellular Carcinoma Detection 
   in Comparison with Liver Ultrasound and Proposal of GALADUS Score. Cancer Epidemiol 
   Biomarkers Prev. 2019;28(3):531-538. doi: 10.1158/1055-9965.EPI-18-0281.

The GALAD model is a validated diagnostic tool that combines Gender, Age, AFP-L3, AFP, 
and DCP (des-gamma-carboxy prothrombin) to detect hepatocellular carcinoma in patients 
with chronic liver disease. This model provides superior diagnostic accuracy compared 
to individual biomarkers and even ultrasound screening.

Clinical Applications:
- HCC screening in high-risk patients with chronic liver disease
- Early detection of hepatocellular carcinoma (particularly BCLC stage 0/A)
- Risk stratification for patients with cirrhosis, hepatitis B, hepatitis C, or NASH
- Decision support for further diagnostic imaging
- Surveillance monitoring in liver transplant candidates

Performance Characteristics:
- Overall HCC detection: AUC 0.95 (vs AFP alone: 0.88, AFP-L3: 0.86, DCP: 0.87)
- Early-stage HCC detection: AUC 0.92
- Sensitivity: 85.6%, Specificity: 93.3% (at threshold ≥-0.63)
- Superior to ultrasound alone: AUC 0.95 vs 0.82 (p<0.01)
"""

from pydantic import BaseModel, Field, validator
from typing import Literal


class GaladModelHccRequest(BaseModel):
    """
    Request model for GALAD Model Hepatocellular Carcinoma Detection
    
    The GALAD model uses demographic data and three serum biomarkers to calculate 
    the probability of hepatocellular carcinoma in patients with chronic liver disease.
    
    **CLINICAL INDICATION**:
    This model should be used for HCC screening and detection in patients with:
    - Chronic liver disease (any etiology)
    - Cirrhosis of any cause
    - Chronic hepatitis B infection
    - Chronic hepatitis C infection
    - Non-alcoholic steatohepatitis (NASH)
    - Alcoholic liver disease
    - Other chronic liver conditions with HCC risk
    
    **BIOMARKER INTERPRETATION GUIDE**:
    
    **1. Alpha-Fetoprotein (AFP)**:
    - **Normal Range**: <10 ng/mL in healthy adults
    - **Interpretation**:
      - <20 ng/mL: Generally normal, but HCC can occur with normal AFP
      - 20-200 ng/mL: Mildly elevated, consider other causes (hepatitis, cirrhosis)
      - 200-400 ng/mL: Moderately elevated, high suspicion for HCC if chronic liver disease
      - >400 ng/mL: Highly elevated, very suspicious for HCC
    - **Limitations**: Can be elevated in hepatitis, cirrhosis, pregnancy, testicular cancer
    
    **2. AFP-L3 Percentage**:
    - **Normal Range**: <10% in healthy adults and most benign liver conditions
    - **Clinical Significance**:
      - <10%: Low risk for HCC development
      - 10-15%: Intermediate risk, monitor closely
      - >15%: High risk for HCC, strong indicator for malignancy
    - **Key Points**:
      - Most useful when total AFP ≤200 ng/mL
      - More specific for HCC than total AFP
      - ≥10% associated with 7-fold increased risk of developing HCC
      - Less affected by benign liver inflammation compared to total AFP
    
    **3. Des-gamma-carboxy Prothrombin (DCP/PIVKA-II)**:
    - **Normal Range**: <40 mAU/mL in healthy adults
    - **Interpretation**:
      - <40 mAU/mL: Normal range
      - 40-100 mAU/mL: Mildly elevated, consider vitamin K deficiency or early HCC
      - 100-400 mAU/mL: Moderately elevated, suspicious for HCC
      - >400 mAU/mL: Highly elevated, very suspicious for HCC
    - **Clinical Notes**:
      - Independent marker, complements AFP
      - Can be elevated before AFP rises
      - Less affected by hepatitis activity than AFP
      - May be elevated in vitamin K deficiency, anticoagulant use
    
    **GALAD FORMULA**:
    Z = -10.08 + 0.09 × age + 1.67 × sex + 2.34 × log₁₀(AFP) + 0.04 × AFP-L3 + 1.33 × log₁₀(DCP)
    Where: sex = 1 for males, 0 for females
    
    **INTERPRETATION THRESHOLD**:
    - **GALAD Score <-0.63**: Low probability of HCC
    - **GALAD Score ≥-0.63**: High probability of HCC (requires further evaluation)
    
    **CLINICAL DECISION SUPPORT**:
    
    **Low Risk (GALAD <-0.63)**:
    - Continue routine HCC surveillance (every 6 months)
    - Maintain current management of underlying liver disease
    - Repeat GALAD testing in 3-6 months if high-risk patient
    - Consider imaging if clinical suspicion remains high
    
    **High Risk (GALAD ≥-0.63)**:
    - **Immediate Actions**:
      - Order contrast-enhanced CT or MRI of liver within 2 weeks
      - Consider urgent hepatology consultation
      - Multidisciplinary team discussion (hepatology, oncology, interventional radiology)
    - **Further Evaluation**:
      - Review all imaging within past 3 months
      - Consider PET-CT if CT/MRI inconclusive
      - Tumor board discussion for treatment planning
      - Genetic counseling if family history of liver cancer
    
    **QUALITY CONSIDERATIONS**:
    - Ensure fasting status for accurate biomarker measurement
    - Consider timing relative to acute hepatitis flares
    - Document vitamin K status and anticoagulant use
    - Note any recent transfusions or hemolysis
    - Correlate with recent liver function tests
    
    **SURVEILLANCE STRATEGY**:
    - High-risk patients: GALAD + imaging every 6 months
    - Very high-risk patients: Consider every 3-4 months
    - Liver transplant candidates: More frequent monitoring
    - Post-treatment patients: Modified surveillance protocols
    
    References (Vancouver style):
    1. Johnson PJ, Pirrie SJ, Cox TF, et al. The detection of hepatocellular carcinoma using 
       a prospectively developed and validated model based on serological biomarkers. Cancer 
       Epidemiol Biomarkers Prev. 2014;23(1):144-53.
    2. Best J, Bechmann LP, Sowa JP, et al. GALAD Score Detects Early Hepatocellular Carcinoma 
       in an International Cohort of Patients With Nonalcoholic Steatohepatitis. Clin Gastroenterol 
       Hepatol. 2020;18(3):728-735.e4.
    3. Yang JD, Addissie BD, Mara KC, et al. GALAD Score for Hepatocellular Carcinoma Detection 
       in Comparison with Liver Ultrasound and Proposal of GALADUS Score. Cancer Epidemiol 
       Biomarkers Prev. 2019;28(3):531-538.
    """
    
    age: int = Field(
        ...,
        description="Patient's age in years. Age is a significant risk factor for HCC development",
        ge=18,
        le=100,
        example=65
    )
    
    sex: Literal["male", "female"] = Field(
        ...,
        description="Patient's biological sex. Males have significantly higher risk of HCC development",
        example="male"
    )
    
    afp: float = Field(
        ...,
        description="Alpha-fetoprotein level in ng/mL. Standard tumor marker for HCC. Normal <10 ng/mL, suspicious >20 ng/mL",
        ge=0.1,
        le=100000,
        example=15.5
    )
    
    afp_l3_percentage: float = Field(
        ...,
        description="AFP-L3 percentage (0-100%). More specific for HCC than total AFP. ≥10% associated with 7-fold increased HCC risk",
        ge=0,
        le=100,
        example=8.2
    )
    
    dcp: float = Field(
        ...,
        description="Des-gamma-carboxy prothrombin (PIVKA-II) in mAU/mL. Independent HCC marker. Normal <40 mAU/mL, suspicious >100 mAU/mL",
        ge=1,
        le=100000,
        example=35.0
    )
    
    class Config:
        schema_extra = {
            "example": {
                "age": 65,
                "sex": "male",
                "afp": 15.5,
                "afp_l3_percentage": 8.2,
                "dcp": 35.0
            }
        }


class GaladModelHccResponse(BaseModel):
    """
    Response model for GALAD Model Hepatocellular Carcinoma Detection
    
    The GALAD score provides a probability estimate for hepatocellular carcinoma based on 
    demographic factors and serum biomarkers. The model has been extensively validated 
    across multiple populations and shows superior performance compared to individual 
    biomarkers or ultrasound screening.
    
    **CLINICAL INTERPRETATION FRAMEWORK**:
    
    **Score Range and Risk Categories**:
    - **Low Risk (GALAD <-0.63)**: Probability of HCC is low based on current biomarker profile
    - **High Risk (GALAD ≥-0.63)**: Probability of HCC is high, requires immediate evaluation
    
    **Clinical Management by Risk Category**:
    
    **Low Risk Management**:
    - **Surveillance**: Continue routine HCC screening every 6 months
    - **Biomarker Monitoring**: Repeat GALAD assessment in 3-6 months
    - **Imaging**: Maintain standard surveillance imaging schedule
    - **Patient Counseling**: Discuss importance of continued surveillance despite low current risk
    - **Risk Factor Management**: Optimize treatment of underlying liver disease
    
    **High Risk Management**:
    - **Immediate Evaluation**:
      - Schedule contrast-enhanced CT or MRI within 1-2 weeks
      - Consider urgent hepatology referral if not already established
      - Review recent imaging studies for interval changes
      - Assess need for expedited multidisciplinary team consultation
    
    - **Diagnostic Workup**:
      - **First-line Imaging**: Contrast-enhanced CT or MRI with liver protocol
      - **If Inconclusive**: Consider PET-CT, repeat imaging in 3 months, or liver biopsy
      - **Staging if HCC Confirmed**: CT chest, bone scan if clinically indicated
      
    - **Multidisciplinary Care**:
      - Hepatology for liver disease optimization and transplant evaluation
      - Oncology for treatment planning if HCC confirmed
      - Interventional radiology for potential therapeutic interventions
      - Surgical consultation for resection candidacy
    
    **Performance Characteristics to Communicate**:
    - **Sensitivity**: 85.6% (correctly identifies 85.6% of HCC cases)
    - **Specificity**: 93.3% (correctly identifies 93.3% of non-HCC cases)
    - **Positive Predictive Value**: Depends on HCC prevalence in population
    - **Negative Predictive Value**: High in screening populations
    
    **Limitations to Discuss**:
    - Model validated in populations with HCC prevalence 35-49%
    - Performance may vary in different ethnic populations
    - Cannot replace clinical judgment and imaging evaluation
    - May have false positives in acute hepatitis or other liver inflammation
    - Requires correlation with clinical presentation and imaging findings
    
    **Follow-up Recommendations**:
    
    **For Low Risk Results**:
    - Next GALAD assessment in 3-6 months (sooner if clinical change)
    - Continue routine HCC surveillance per guidelines
    - Optimize management of underlying liver disease
    - Patient education on symptoms requiring immediate evaluation
    
    **For High Risk Results**:
    - Imaging within 1-2 weeks as described above
    - Hepatology follow-up within 1-4 weeks depending on clinical urgency
    - Patient counseling about need for immediate evaluation
    - Clear instructions for seeking care if symptoms develop
    - Plan for multidisciplinary discussion once imaging completed
    
    **Documentation Requirements**:
    - Record all biomarker values and laboratory details
    - Document clinical context and liver disease status
    - Note patient counseling provided about results and next steps
    - Include clear follow-up plan with specific timelines
    - Communicate results urgently if high-risk
    
    **Quality Assurance**:
    - Verify biomarker values and ensure appropriate assays used
    - Confirm patient eligibility (chronic liver disease risk factors)
    - Cross-reference with recent imaging and clinical findings
    - Ensure appropriate urgency of follow-up based on risk level
    
    Reference: Johnson PJ, et al. Cancer Epidemiol Biomarkers Prev. 2014;23(1):144-53.
    """
    
    result: float = Field(
        ...,
        description="GALAD score calculated from demographic data and serum biomarkers. Threshold for high HCC risk is ≥-0.63",
        example=-1.25
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the GALAD score",
        example="score"
    )
    
    interpretation: str = Field(
        ...,
        description="Comprehensive clinical interpretation including risk assessment, recommended actions, and follow-up plan",
        example="GALAD score of -1.25 is below the threshold of -0.63, suggesting low probability of hepatocellular carcinoma. Continue routine surveillance in high-risk patients with chronic liver disease. Consider repeat assessment in 3-6 months or if clinical status changes."
    )
    
    stage: str = Field(
        ...,
        description="Risk category based on GALAD score threshold (Low Risk, High Risk)",
        example="Low Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the risk level",
        example="Low probability of HCC"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": -1.25,
                "unit": "score",
                "interpretation": "GALAD score of -1.25 is below the threshold of -0.63, suggesting low probability of hepatocellular carcinoma. Continue routine surveillance in high-risk patients with chronic liver disease. Consider repeat assessment in 3-6 months or if clinical status changes.",
                "stage": "Low Risk",
                "stage_description": "Low probability of HCC"
            }
        }