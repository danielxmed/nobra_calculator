"""
Fractional Excretion of Urea (FEUrea) Models

Request and response models for FEUrea calculation.

References (Vancouver style):
1. Carvounis CP, Nisar S, Guro-Razuman S. Significance of the fractional excretion of 
   urea in the differential diagnosis of acute renal failure. Kidney Int. 2002;62(6):2223-9. 
   doi: 10.1046/j.1523-1755.2002.00671.x.
2. Kaplan AA, Kohn OF. Fractional excretion of urea as a guide to renal dysfunction. 
   Am J Nephrol. 1992;12(1-2):49-54. doi: 10.1159/000168429.
3. Diskin CJ, Stokes TJ, Dansby LM, et al. The comparative benefits of the fractional 
   excretion of urea and sodium in various azotemic oliguric states. Nephron Clin Pract. 
   2010;114(2):c145-50. doi: 10.1159/000254384.
4. Pahwa AK, Sperati CJ. Urinary Fractional Excretion Indices in the Evaluation of 
   Acute Kidney Injury. J Hosp Med. 2016;11(1):77-80. doi: 10.1002/jhm.2501.

The Fractional Excretion of Urea (FEUrea) is a diagnostic test used to differentiate 
between prerenal and intrinsic causes of acute kidney injury (AKI). It offers significant 
advantages over FENa as it can be used in patients receiving diuretics and has been 
shown to be more sensitive and specific for differentiating prerenal azotemia from 
acute tubular necrosis.

Key Advantages of FEUrea:
- Can be used in patients on diuretics (unlike FENa)
- More sensitive and specific than FENa for AKI differentiation
- Urea reabsorption is not significantly affected by most diuretics
- Particularly useful when FENa is unreliable due to diuretic exposure

Clinical Significance:
- FEUrea <35%: Indicates prerenal azotemia (volume depletion, heart failure)
- FEUrea 35-50%: Intermediate range requiring clinical correlation
- FEUrea >50%: Suggests intrinsic kidney disease (acute tubular necrosis)
"""

from pydantic import BaseModel, Field
from typing import Literal


class FractionalExcretionUreaRequest(BaseModel):
    """
    Request model for Fractional Excretion of Urea (FEUrea) calculation
    
    The FEUrea test helps differentiate between prerenal and intrinsic causes of acute 
    kidney injury by calculating the percentage of filtered urea that is excreted in 
    the urine. Unlike FENa, FEUrea can be reliably used in patients on diuretics.
    
    **Formula**: FEUrea (%) = [(Urine Urea × Serum Creatinine) / (Serum Urea × Urine Creatinine)] × 100
    
    **Required Laboratory Values**:
    - **Serum Urea (BUN)**: Normal range typically 7-21 mg/dL, elevated in kidney injury (5-300 mg/dL)
    - **Urine Urea**: Highly concentrated in normal urine, typically 500-3000 mg/dL
    - **Serum Creatinine**: Normal ~0.6-1.2 mg/dL, elevated in kidney injury (0.1-20.0 mg/dL)  
    - **Urine Creatinine**: Concentrated urine specimen needed, typically 20-400 mg/dL
    
    **Clinical Interpretation**:
    - **FEUrea <35%**: Prerenal azotemia (kidneys conserving urea)
      - Volume depletion, dehydration, heart failure, cirrhosis
      - Kidneys responding normally to perceived volume depletion
      - Can be used reliably even in patients on diuretics
    - **FEUrea 35-50%**: Intermediate range, may suggest early intrinsic disease
      - May occur in early ATN, mixed conditions, or recovery phase
      - Requires correlation with clinical presentation
    - **FEUrea >50%**: Intrinsic kidney disease (impaired urea reabsorption)
      - Acute tubular necrosis, acute interstitial nephritis
      - Values >70% typically seen with established ATN
    
    **Key Advantages over FENa**:
    - **Diuretic Independence**: Not significantly affected by most diuretics
    - **Higher Sensitivity**: More sensitive for detecting prerenal azotemia
    - **Better Specificity**: Better specificity for distinguishing ATN from prerenal causes
    - **Broader Applicability**: Can be used when FENa is unreliable
    
    **Important Considerations**:
    - **Sample Timing**: Should be obtained during acute phase of kidney injury
    - **Simultaneous Collection**: All samples should be obtained at the same time
    - **Clinical Context**: Always interpret with other clinical findings
    - **Protein Loading**: May be affected by high protein intake or corticosteroids
    
    References (Vancouver style):
    1. Carvounis CP, Nisar S, Guro-Razuman S. Significance of the fractional excretion of 
       urea in the differential diagnosis of acute renal failure. Kidney Int. 2002;62(6):2223-9.
    2. Kaplan AA, Kohn OF. Fractional excretion of urea as a guide to renal dysfunction. 
       Am J Nephrol. 1992;12(1-2):49-54.
    3. Diskin CJ, Stokes TJ, Dansby LM, et al. The comparative benefits of the fractional 
       excretion of urea and sodium in various azotemic oliguric states. Nephron Clin Pract. 
       2010;114(2):c145-50.
    """
    
    serum_urea: float = Field(
        ...,
        description=(
            "Serum/plasma urea concentration (also known as Blood Urea Nitrogen - BUN) in mg/dL. "
            "Normal range is typically 7-21 mg/dL. Elevated levels indicate decreased kidney function "
            "or increased protein catabolism. This value should be obtained simultaneously with other "
            "laboratory parameters for accurate FEUrea calculation."
        ),
        ge=5,
        le=300,
        example=45
    )
    
    urine_urea: float = Field(
        ...,
        description=(
            "Urine urea concentration in mg/dL from a spot urine sample. "
            "Normal concentrated urine typically contains 500-3000 mg/dL of urea. "
            "Lower values may indicate impaired concentrating ability or dilute urine. "
            "Should be obtained from fresh urine specimen collected simultaneously with other samples."
        ),
        ge=50,
        le=5000,
        example=1200
    )
    
    serum_creatinine: float = Field(
        ...,
        description=(
            "Serum/plasma creatinine concentration in mg/dL. Normal is approximately 0.6-1.2 mg/dL. "
            "Elevated levels indicate decreased kidney function. This value should be obtained "
            "simultaneously with other laboratory parameters for accurate FEUrea calculation."
        ),
        ge=0.1,
        le=20.0,
        example=2.8
    )
    
    urine_creatinine: float = Field(
        ...,
        description=(
            "Urine creatinine concentration in mg/dL from a spot urine sample. "
            "Typically ranges from 20-400 mg/dL depending on urine concentration and muscle mass. "
            "Higher values indicate more concentrated urine. Should be obtained from the same "
            "urine specimen used for urine urea measurement."
        ),
        ge=1,
        le=500,
        example=180
    )
    
    class Config:
        schema_extra = {
            "example": {
                "serum_urea": 45,
                "urine_urea": 1200,
                "serum_creatinine": 2.8,
                "urine_creatinine": 180
            }
        }


class FractionalExcretionUreaResponse(BaseModel):
    """
    Response model for Fractional Excretion of Urea (FEUrea) calculation
    
    The FEUrea result provides superior diagnostic accuracy compared to FENa for 
    distinguishing between prerenal and intrinsic causes of acute kidney injury, 
    especially in patients receiving diuretics.
    
    **Result Interpretation**:
    
    **FEUrea <35% (Prerenal Azotemia)**:
    - Indicates kidneys are functioning normally but responding to volume depletion
    - Common causes: dehydration, heart failure, cirrhosis, hepatorenal syndrome
    - Management: Address underlying cause, optimize volume status, avoid nephrotoxins
    - Prognosis: Usually reversible with appropriate treatment
    - Advantage: Reliable even in patients on diuretics
    
    **FEUrea 35-50% (Intermediate Range)**:
    - May indicate early intrinsic disease or mixed conditions
    - Can occur in early or recovering ATN, partial obstruction
    - Requires correlation with clinical presentation and serial measurements
    - Management guided by overall clinical assessment
    
    **FEUrea >50% (Intrinsic Kidney Disease)**:
    - Indicates impaired tubular urea reabsorption
    - Common causes: acute tubular necrosis, acute interstitial nephritis
    - Values >70% typically associated with established ATN
    - Management: supportive care, avoid nephrotoxins, nephrology consultation
    
    **Clinical Applications**:
    - Primary choice when patients have received diuretics within 24-48 hours
    - Emergency department evaluation of acute kidney injury
    - ICU monitoring when diuretic use complicates FENa interpretation
    - More accurate differentiation of prerenal vs intrinsic AKI
    
    **Advantages over FENa**:
    - Not affected by diuretic therapy
    - Higher sensitivity for detecting prerenal azotemia
    - Better specificity for distinguishing ATN from prerenal causes
    - Can be used in a broader range of clinical scenarios
    
    **Clinical Decision Making**:
    - FEUrea <35%: Focus on volume optimization and prerenal causes
    - FEUrea 35-50%: Consider mixed picture, monitor closely
    - FEUrea >50%: Evaluate for intrinsic kidney disease, consider nephrology consultation
    
    Reference: Carvounis CP, et al. Kidney Int. 2002;62(6):2223-9.
    """
    
    result: float = Field(
        ...,
        description="Fractional Excretion of Urea as percentage (range typically 0-100%)",
        ge=0,
        example=23.8
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for FEUrea",
        example="%"
    )
    
    interpretation: str = Field(
        ...,
        description=(
            "Clinical interpretation including likely cause of kidney injury, "
            "recommended management approach, and advantages of FEUrea over FENa"
        ),
        example=(
            "FEUrea 23.8% indicates prerenal cause of acute kidney injury. "
            "The kidneys are conserving urea due to decreased blood flow or volume depletion. "
            "Common causes include dehydration, heart failure, cirrhosis, or hepatorenal syndrome. "
            "Consider volume resuscitation and address underlying cause. FEUrea is reliable even "
            "in patients receiving diuretics."
        )
    )
    
    stage: str = Field(
        ...,
        description="Diagnostic category based on FEUrea value (Prerenal AKI, Indeterminate, Intrinsic AKI)",
        example="Prerenal AKI"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the diagnostic category",
        example="Suggests prerenal azotemia"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 23.8,
                "unit": "%",
                "interpretation": (
                    "FEUrea 23.8% indicates prerenal cause of acute kidney injury. "
                    "The kidneys are conserving urea due to decreased blood flow or volume depletion. "
                    "Common causes include dehydration, heart failure, cirrhosis, or hepatorenal syndrome. "
                    "Consider volume resuscitation and address underlying cause. FEUrea is reliable even "
                    "in patients receiving diuretics."
                ),
                "stage": "Prerenal AKI",
                "stage_description": "Suggests prerenal azotemia"
            }
        }