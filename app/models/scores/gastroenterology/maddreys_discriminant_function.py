"""
Maddrey's Discriminant Function Models

Request and response models for Maddrey's Discriminant Function calculation
to predict prognosis and steroid benefit in alcoholic hepatitis.

References (Vancouver style):
1. Maddrey WC, Boitnott JK, Bedine MS, Weber FL Jr, Mezey E, White RI Jr. 
   Corticosteroid therapy of alcoholic hepatitis. Gastroenterology. 1978 Aug;75(2):193-9. 
   PMID: 352788.
2. Carithers RL Jr, Herlong HF, Diehl AM, Shaw EW, Combes B, Fallon HJ, Maddrey WC. 
   Methylprednisolone therapy in patients with severe alcoholic hepatitis. A randomized 
   multicenter trial. Ann Intern Med. 1989 May 1;110(9):685-90. 
   doi: 10.7326/0003-4819-110-9-685.
3. Louvet A, Naveau S, Abdelnour M, Ramond MJ, Diaz E, Fartoux L, et al. The Lille model: 
   a new tool for therapeutic strategy in patients with severe alcoholic hepatitis treated 
   with steroids. Hepatology. 2007 Jun;45(6):1348-54. doi: 10.1002/hep.21607.

Maddrey's Discriminant Function is the first established clinical prognostic score for 
alcoholic hepatitis, developed in 1978. It uses prothrombin time prolongation and total 
bilirubin elevation to predict short-term mortality and guide corticosteroid therapy 
decisions. A score ≥32 indicates severe disease with poor prognosis and potential benefit 
from steroid treatment, while scores <32 indicate mild to moderate disease with excellent 
prognosis (90% 30-day survival) without steroid therapy.
"""

from pydantic import BaseModel, Field
from typing import Union


class MaddreysDiscriminantFunctionRequest(BaseModel):
    """
    Request model for Maddrey's Discriminant Function
    
    Maddrey's Discriminant Function uses three laboratory parameters to assess 
    alcoholic hepatitis severity and guide treatment decisions:
    
    Formula: Maddrey's DF = 4.6 × (Patient's PT - Control PT) + Total Bilirubin
    
    Laboratory Parameters:
    - Patient's Prothrombin Time (PT): Measured coagulation time in seconds
      - Normal range: typically 11-13 seconds
      - In alcoholic hepatitis: often prolonged due to decreased hepatic synthesis
      - Reflects severity of hepatocellular dysfunction
    
    - Control/Reference PT: Laboratory's normal reference PT value
      - Typically ranges from 11-13 seconds depending on laboratory
      - Used to normalize for laboratory-specific reagents and methods
      - Should be obtained from same laboratory as patient's PT
    
    - Total Bilirubin: Sum of conjugated and unconjugated bilirubin
      - Normal range: 0.2-1.2 mg/dL
      - In alcoholic hepatitis: elevated due to hepatocellular injury and cholestasis
      - Reflects both hepatocyte dysfunction and biliary obstruction
      - Higher levels correlate with worse prognosis
    
    Clinical Context:
    - Use in patients with suspected alcoholic hepatitis
    - Requires recent history of heavy alcohol use (typically >80g/day for men, >60g/day for women)
    - Should exclude other causes of acute hepatitis
    - Consider concurrent conditions affecting PT (anticoagulation, vitamin K deficiency)
    
    Interpretation Thresholds:
    - Score <32: Mild to moderate disease (90% 30-day survival without steroids)
    - Score ≥32: Severe disease (35-45% 30-day mortality, consider steroids)
    
    References (Vancouver style):
    1. Maddrey WC, Boitnott JK, Bedine MS, Weber FL Jr, Mezey E, White RI Jr. 
    Corticosteroid therapy of alcoholic hepatitis. Gastroenterology. 1978 Aug;75(2):193-9. 
    PMID: 352788.
    2. Carithers RL Jr, Herlong HF, Diehl AM, Shaw EW, Combes B, Fallon HJ, Maddrey WC. 
    Methylprednisolone therapy in patients with severe alcoholic hepatitis. A randomized 
    multicenter trial. Ann Intern Med. 1989 May 1;110(9):685-90. 
    doi: 10.7326/0003-4819-110-9-685.
    """
    
    patient_pt: Union[int, float] = Field(
        ...,
        description="Patient's prothrombin time in seconds. Measures coagulation function "
                   "and hepatic synthetic capacity. Typically prolonged in alcoholic hepatitis",
        ge=8.0,
        le=120.0,
        example=18.5
    )
    
    control_pt: Union[int, float] = Field(
        ...,
        description="Control/reference prothrombin time in seconds from the same laboratory. "
                   "Typically ranges 11-13 seconds depending on laboratory reagents and methods",
        ge=8.0,
        le=20.0,
        example=12.0
    )
    
    total_bilirubin: Union[int, float] = Field(
        ...,
        description="Total bilirubin level in mg/dL. Sum of conjugated and unconjugated bilirubin. "
                   "Elevated in alcoholic hepatitis due to hepatocellular injury and cholestasis",
        ge=0.1,
        le=50.0,
        example=8.2
    )
    
    class Config:
        schema_extra = {
            "example": {
                "patient_pt": 18.5,
                "control_pt": 12.0,
                "total_bilirubin": 8.2
            }
        }


class MaddreysDiscriminantFunctionResponse(BaseModel):
    """
    Response model for Maddrey's Discriminant Function
    
    Provides risk stratification and treatment guidance for alcoholic hepatitis:
    
    Score Interpretation:
    - <32 points: Mild to Moderate Disease
      Excellent prognosis with 90% 30-day survival without steroid therapy
      Corticosteroid treatment not recommended
      Focus on supportive care and alcohol cessation
    
    - ≥32 points: Severe Disease  
      Poor prognosis with 35-45% 30-day mortality risk
      Consider corticosteroid therapy (prednisolone 40mg daily) if no contraindications
      Requires close monitoring and aggressive supportive care
    
    Clinical Applications:
    - Short-term prognosis prediction (30-day mortality)
    - Treatment decision-making for corticosteroid therapy
    - Risk stratification for clinical trials and research
    - Hospital vs. outpatient management decisions
    
    Treatment Considerations:
    - Steroid contraindications: active GI bleeding, infection, acute pancreatitis,
      acute renal failure, hepatorenal syndrome, severe psychiatric illness
    - Combine with Lille score at day 7 to assess treatment response
    - Consider MELD score for additional prognostic information
    - Liver transplant evaluation for appropriate candidates
    
    Limitations:
    - Less useful for long-term prognosis prediction
    - Should be interpreted in clinical context
    - May be affected by other causes of PT prolongation
    - Requires exclusion of other forms of acute hepatitis
    
    Reference: Maddrey WC, et al. Gastroenterology. 1978;75(2):193-9.
    """
    
    result: float = Field(
        ...,
        description="Maddrey's Discriminant Function score calculated from PT difference and bilirubin",
        example=38.1
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the Maddrey's score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Comprehensive clinical interpretation with severity assessment and treatment recommendations",
        example="Maddrey's Discriminant Function Assessment:\\n\\nCalculation Components:\\n• Patient's PT: 18.5 seconds\\n• Control PT: 12.0 seconds\\n• PT difference: 6.5 seconds\\n• Total bilirubin: 8.2 mg/dL"
    )
    
    stage: str = Field(
        ...,
        description="Disease severity category based on Maddrey's score",
        example="Severe"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of disease severity and treatment implications",
        example="Poor prognosis, consider steroid therapy"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 38.1,
                "unit": "points",
                "interpretation": "Maddrey's Discriminant Function Assessment:\\n\\nCalculation Components:\\n• Patient's PT: 18.5 seconds\\n• Control PT: 12.0 seconds\\n• PT difference: 6.5 seconds\\n• Total bilirubin: 8.2 mg/dL\\n• Formula: 4.6 × (18.5 - 12.0) + 8.2\\n• Maddrey's score: 38.1 points\\n\\nSeverity Assessment:\\n• Classification: Severe Alcoholic Hepatitis\\n• Prognosis: 35-45% 30-day mortality\\n• Threshold: Score ≥ 32 indicates severe disease\\n\\nTreatment Recommendations:\\n• Steroid therapy: Consider corticosteroids if no contraindications\\n• Prognosis: Poor (35-45% mortality risk within first month)\\n• Monitoring: Close monitoring, consider ICU care\\n• Additional therapy: Prednisolone 40mg daily, nutritional support, infection screening",
                "stage": "Severe",
                "stage_description": "Poor prognosis, consider steroid therapy"
            }
        }