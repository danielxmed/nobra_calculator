"""
Fractional Excretion of Sodium (FENa) Models

Request and response models for FENa calculation.

References (Vancouver style):
1. Espinel CH. The FENa test. Use in the differential diagnosis of acute renal failure. 
   JAMA. 1976;236(6):579-81. doi: 10.1001/jama.1976.03270060029025.
2. Miller TR, Anderson RJ, Linas SL, et al. Urinary diagnostic indices in acute renal 
   failure: a prospective study. Ann Intern Med. 1978;89(1):47-50. 
   doi: 10.7326/0003-4819-89-1-47.
3. Steiner RW. Interpreting the fractional excretion of sodium. Am J Med. 1984;77(4):699-702. 
   doi: 10.1016/0002-9343(84)90368-1.
4. Pahwa AK, Sperati CJ. Urinary Fractional Excretion Indices in the Evaluation of 
   Acute Kidney Injury. J Hosp Med. 2016;11(1):77-80. doi: 10.1002/jhm.2501.

The Fractional Excretion of Sodium (FENa) is a diagnostic test used to differentiate 
between prerenal and intrinsic causes of acute kidney injury (AKI). It calculates 
the percentage of filtered sodium that is excreted in the urine, helping clinicians 
determine the underlying pathophysiology of kidney dysfunction.

Clinical Significance:
- FENa <1%: Typically indicates prerenal azotemia (volume depletion, heart failure)
- FENa 1-2%: Intermediate range requiring clinical correlation
- FENa >2%: Usually suggests intrinsic kidney disease (acute tubular necrosis)

Important Limitations:
- Should not be used in patients recently treated with diuretics
- May be unreliable in chronic kidney disease
- Clinical context and other diagnostic tests should always be considered
- Some conditions may present with atypical FENa values
"""

from pydantic import BaseModel, Field
from typing import Literal


class FractionalExcretionSodiumRequest(BaseModel):
    """
    Request model for Fractional Excretion of Sodium (FENa) calculation
    
    The FENa test helps differentiate between prerenal and intrinsic causes of acute 
    kidney injury by calculating the percentage of filtered sodium that is excreted 
    in the urine.
    
    **Formula**: FENa (%) = [(Urine Sodium × Serum Creatinine) / (Serum Sodium × Urine Creatinine)] × 100
    
    **Required Laboratory Values**:
    - **Serum Sodium**: Normal range typically 136-145 mEq/L, but calculator accepts 120-180 mEq/L
    - **Urine Sodium**: Highly variable depending on intake and kidney function (1-300 mEq/L)
    - **Serum Creatinine**: Normal ~0.6-1.2 mg/dL, elevated in kidney injury (0.1-20.0 mg/dL)
    - **Urine Creatinine**: Concentrated urine specimen needed, typically 20-400 mg/dL
    
    **Clinical Interpretation**:
    - **FENa <1%**: Prerenal azotemia (kidneys conserving sodium)
      - Volume depletion, dehydration, heart failure, cirrhosis
      - Kidneys responding normally to perceived volume depletion
    - **FENa 1-2%**: Intermediate range, requires clinical correlation
      - May occur in early ATN, mixed conditions, or recovery phase
    - **FENa >2%**: Intrinsic kidney disease (impaired sodium reabsorption)
      - Acute tubular necrosis, acute interstitial nephritis
      - Post-renal obstruction with kidney injury
    
    **Important Considerations**:
    - **Diuretic Use**: Invalidates the test - avoid if diuretics used within 24-48 hours
    - **Sample Timing**: Should be obtained during acute phase of kidney injury
    - **Clinical Context**: Always interpret with other clinical findings and urine microscopy
    - **Limitations**: May be unreliable in CKD, sepsis, or conditions affecting proximal tubule function
    
    References (Vancouver style):
    1. Espinel CH. The FENa test. Use in the differential diagnosis of acute renal failure. 
       JAMA. 1976;236(6):579-81.
    2. Miller TR, Anderson RJ, Linas SL, et al. Urinary diagnostic indices in acute renal 
       failure: a prospective study. Ann Intern Med. 1978;89(1):47-50.
    3. Steiner RW. Interpreting the fractional excretion of sodium. Am J Med. 1984;77(4):699-702.
    4. Pahwa AK, Sperati CJ. Urinary Fractional Excretion Indices in the Evaluation of 
       Acute Kidney Injury. J Hosp Med. 2016;11(1):77-80.
    """
    
    serum_sodium: float = Field(
        ...,
        description=(
            "Serum/plasma sodium concentration in mEq/L. Normal range is typically 136-145 mEq/L. "
            "This represents the filtered load of sodium available for reabsorption. "
            "Obtain from the same time point as other laboratory values for accuracy."
        ),
        ge=120,
        le=180,
        example=140
    )
    
    urine_sodium: float = Field(
        ...,
        description=(
            "Urine sodium concentration in mEq/L from a spot urine sample. "
            "This value varies greatly depending on dietary intake, volume status, and kidney function. "
            "Low values (<20 mEq/L) suggest sodium retention, while high values (>40 mEq/L) suggest sodium wasting. "
            "Should be obtained from fresh urine specimen."
        ),
        ge=1,
        le=300,
        example=25
    )
    
    serum_creatinine: float = Field(
        ...,
        description=(
            "Serum/plasma creatinine concentration in mg/dL. Normal is approximately 0.6-1.2 mg/dL. "
            "Elevated levels indicate decreased kidney function. This value should be obtained "
            "simultaneously with other laboratory parameters for accurate FENa calculation."
        ),
        ge=0.1,
        le=20.0,
        example=2.5
    )
    
    urine_creatinine: float = Field(
        ...,
        description=(
            "Urine creatinine concentration in mg/dL from a spot urine sample. "
            "Typically ranges from 20-400 mg/dL depending on urine concentration. "
            "Higher values indicate more concentrated urine. Should be obtained from the same "
            "urine specimen used for urine sodium measurement."
        ),
        ge=1,
        le=500,
        example=150
    )
    
    class Config:
        schema_extra = {
            "example": {
                "serum_sodium": 140,
                "urine_sodium": 25,
                "serum_creatinine": 2.5,
                "urine_creatinine": 150
            }
        }


class FractionalExcretionSodiumResponse(BaseModel):
    """
    Response model for Fractional Excretion of Sodium (FENa) calculation
    
    The FENa result helps distinguish between prerenal and intrinsic causes of acute 
    kidney injury, guiding appropriate diagnostic workup and therapeutic interventions.
    
    **Result Interpretation**:
    
    **FENa <1% (Prerenal Azotemia)**:
    - Indicates kidneys are functioning normally but responding to perceived volume depletion
    - Common causes: dehydration, heart failure, cirrhosis, hepatorenal syndrome
    - Management: Address underlying cause, volume optimization, avoid nephrotoxins
    - Prognosis: Usually reversible with appropriate treatment
    
    **FENa 1-2% (Intermediate Range)**:
    - May occur in early or recovering ATN, mixed conditions
    - Requires correlation with clinical presentation and other tests
    - Consider serial measurements and additional diagnostic workup
    - Management guided by overall clinical picture
    
    **FENa >2% (Intrinsic Kidney Disease)**:
    - Indicates impaired tubular sodium reabsorption
    - Common causes: acute tubular necrosis, acute interstitial nephritis, severe obstruction
    - Management: supportive care, avoid nephrotoxins, treat underlying cause
    - May require nephrology consultation and kidney biopsy in unclear cases
    
    **Clinical Applications**:
    - Emergency department evaluation of acute kidney injury
    - Intensive care unit monitoring of kidney function
    - Distinguishing prerenal from intrinsic causes when clinical picture is unclear
    - Guiding fluid management and therapeutic interventions
    
    **Limitations and Considerations**:
    - Invalid if diuretics used within 24-48 hours
    - May be unreliable in chronic kidney disease
    - Some conditions may present with atypical values
    - Should always be interpreted with clinical context and urinalysis
    
    Reference: Espinel CH. JAMA. 1976;236(6):579-81.
    """
    
    result: float = Field(
        ...,
        description="Fractional Excretion of Sodium as percentage (range typically 0-20%)",
        ge=0,
        example=0.58
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for FENa",
        example="%"
    )
    
    interpretation: str = Field(
        ...,
        description=(
            "Clinical interpretation including likely cause of kidney injury, "
            "recommended management approach, and important clinical considerations"
        ),
        example=(
            "FENa 0.58% typically indicates prerenal cause of acute kidney injury. "
            "The kidneys are conserving sodium due to decreased blood flow or volume depletion. "
            "Common causes include dehydration, heart failure, cirrhosis, or hepatorenal syndrome. "
            "Consider volume resuscitation and address underlying cause."
        )
    )
    
    stage: str = Field(
        ...,
        description="Diagnostic category based on FENa value (Prerenal AKI, Indeterminate, Intrinsic AKI)",
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
                "result": 0.58,
                "unit": "%",
                "interpretation": (
                    "FENa 0.58% typically indicates prerenal cause of acute kidney injury. "
                    "The kidneys are conserving sodium due to decreased blood flow or volume depletion. "
                    "Common causes include dehydration, heart failure, cirrhosis, or hepatorenal syndrome. "
                    "Consider volume resuscitation and address underlying cause."
                ),
                "stage": "Prerenal AKI",
                "stage_description": "Suggests prerenal azotemia"
            }
        }