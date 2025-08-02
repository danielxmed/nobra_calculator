"""
Urine Anion Gap Models

Request and response models for Urine Anion Gap calculation.

References (Vancouver style):
1. Goldstein MB, Bear R, Richardson RM, Marsden PA, Halperin ML. The urine anion gap: 
   a clinically useful index of ammonium excretion. Am J Med Sci. 1986;292(4):198-202.
2. Kim GH, Han JS, Kim YS, Joo KW, Kim S, Lee JS. Evaluation of urine acidification 
   by urine anion gap versus urine osmolal gap in chronic metabolic acidosis. 
   Am J Kidney Dis. 2002;40(4):778-84.

The Urine Anion Gap is a simple calculation used to evaluate non-anion gap metabolic 
acidosis by providing an indirect assessment of urinary ammonium excretion. It helps 
differentiate between renal and extrarenal causes of normal anion gap metabolic acidosis.

Formula: Urine Anion Gap = Urine Na+ + Urine K+ - Urine Cl-

Clinical interpretation:
- Negative UAG (<-10 mEq/L): Suggests extrarenal bicarbonate loss (e.g., diarrhea)
- Normal UAG (-10 to +20 mEq/L): Typical range in healthy individuals
- Positive UAG (>+20 mEq/L): Suggests renal tubular acidosis

The calculation is based on the principle that in normal anion gap metabolic acidosis, 
the kidney should increase ammonium (NH4+) excretion to regenerate bicarbonate. Since 
ammonium is not routinely measured, the urine anion gap serves as an indirect marker: 
when ammonium excretion is high, chloride excretion increases proportionally, making 
the anion gap negative.
"""

from pydantic import BaseModel, Field
from typing import Union


class UrineAnionGapRequest(BaseModel):
    """
    Request model for Urine Anion Gap calculation
    
    The Urine Anion Gap requires measurement of three urinary electrolytes from a fresh 
    urine sample to calculate an indirect assessment of urinary ammonium excretion.
    
    Laboratory Parameters:
    - Urine Sodium (Na+): Typically ranges from 20-200 mEq/L depending on dietary intake 
      and volume status. Higher values seen with high sodium intake or diuretic use.
    - Urine Potassium (K+): Typically ranges from 25-100 mEq/L depending on dietary intake 
      and acid-base status. Higher values seen with alkalosis or high potassium intake.
    - Urine Chloride (Cl-): Typically ranges from 50-250 mEq/L depending on dietary intake 
      and acid-base status. Higher values when ammonium excretion is increased.
    
    Clinical Context:
    This calculation is specifically used in the evaluation of non-anion gap (normal anion gap) 
    metabolic acidosis to help differentiate between:
    
    1. Extrarenal causes (negative UAG):
       - Diarrhea (most common)
       - Ureteroenteric or pancreatoduodenal fistulas
       - Carbonic anhydrase inhibitor use
       - Post-hypocapnia state
    
    2. Renal causes (positive UAG):
       - Type 1 (distal) renal tubular acidosis
       - Type 2 (proximal) renal tubular acidosis  
       - Type 4 (hyperkalemic) renal tubular acidosis
       - Chronic kidney disease with impaired ammonium excretion
    
    Sample Requirements:
    - Fresh urine sample (analyze within 2 hours or refrigerate)
    - Accurate measurement of all three electrolytes from the same sample
    - Avoid contamination that could alter electrolyte concentrations
    
    Limitations:
    - Not useful in high anion gap metabolic acidosis
    - May be inaccurate in severe volume depletion
    - Should be interpreted in clinical context
    - Urine osmolar gap may be more accurate in some situations
    
    References:
    1. Goldstein MB, Bear R, Richardson RM, Marsden PA, Halperin ML. The urine anion gap: 
       a clinically useful index of ammonium excretion. Am J Med Sci. 1986;292(4):198-202.
    2. Kim GH, Han JS, Kim YS, Joo KW, Kim S, Lee JS. Evaluation of urine acidification 
       by urine anion gap versus urine osmolal gap in chronic metabolic acidosis. 
       Am J Kidney Dis. 2002;40(4):778-84.
    """
    
    urine_sodium_meq_l: float = Field(
        ...,
        description="Urine sodium concentration in milliequivalents per liter (mEq/L). Typical range 20-200 mEq/L depending on dietary intake and volume status.",
        ge=5,
        le=300,
        example=80.0
    )
    
    urine_potassium_meq_l: float = Field(
        ...,
        description="Urine potassium concentration in milliequivalents per liter (mEq/L). Typical range 25-100 mEq/L depending on dietary intake and acid-base status.",
        ge=5,
        le=200,
        example=40.0
    )
    
    urine_chloride_meq_l: float = Field(
        ...,
        description="Urine chloride concentration in milliequivalents per liter (mEq/L). Typical range 50-250 mEq/L depending on dietary intake and ammonium excretion.",
        ge=5,
        le=400,
        example=100.0
    )
    
    class Config:
        schema_extra = {
            "example": {
                "urine_sodium_meq_l": 80.0,
                "urine_potassium_meq_l": 40.0,
                "urine_chloride_meq_l": 100.0
            }
        }


class UrineAnionGapResponse(BaseModel):
    """
    Response model for Urine Anion Gap calculation
    
    The Urine Anion Gap result provides important diagnostic information for evaluating 
    the cause of non-anion gap metabolic acidosis:
    
    Clinical Interpretation:
    
    **Negative UAG (<-10 mEq/L) - Extrarenal Cause:**
    - Indicates adequate renal ammonium excretion in response to acidosis
    - Suggests gastrointestinal bicarbonate losses (most commonly diarrhea)
    - Other causes: ureteroenteric fistulas, carbonic anhydrase inhibitors
    - Management: Address underlying cause, consider bicarbonate replacement
    
    **Normal UAG (-10 to +20 mEq/L) - Normal Range:**
    - May be seen in healthy individuals or early acid-base disorders
    - Requires clinical correlation to determine significance
    - Consider other diagnostic tests if metabolic acidosis present
    
    **Positive UAG (>+20 mEq/L) - Renal Cause:**
    - Indicates impaired renal ammonium excretion (renal tubular acidosis)
    - Types include: distal RTA (Type 1), proximal RTA (Type 2), hyperkalemic RTA (Type 4)
    - May require further testing: urine pH, citrate, calcium, bicarbonate loading test
    - Management: Alkali therapy, address underlying kidney disease
    
    Clinical Applications:
    - Differential diagnosis of normal anion gap metabolic acidosis
    - Evaluation for suspected renal tubular acidosis
    - Monitoring response to treatment in acid-base disorders
    - Assessment of renal acidification capacity
    
    Important Considerations:
    - Use only in normal anion gap metabolic acidosis (serum AG 8-12 mEq/L)
    - Requires fresh urine sample with accurate electrolyte measurements
    - May be inaccurate in severe volume depletion or very low chloride excretion
    - Consider urine osmolar gap as alternative in complex cases
    - Interpret in conjunction with serum chemistries and clinical presentation
    
    Treatment Implications:
    - Negative UAG: Focus on treating underlying GI losses, consider anti-diarrheal agents
    - Positive UAG: Consider alkali therapy (sodium bicarbonate, potassium citrate)
    - Monitor response with serial blood gases and electrolytes
    
    Reference: Goldstein MB, et al. Am J Med Sci. 1986;292(4):198-202.
    """
    
    result: float = Field(
        ...,
        description="Calculated urine anion gap in milliequivalents per liter (typical range -20 to +30 mEq/L)",
        example=20.0
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the urine anion gap",
        example="mEq/L"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation with diagnostic implications and management recommendations based on the urine anion gap value",
        example="Positive urine anion gap of 20.0 mEq/L suggests a renal cause of non-anion gap metabolic acidosis. This indicates impaired renal ammonium excretion, typically seen in renal tubular acidosis (Type 1 distal RTA, Type 2 proximal RTA, Type 4 hyperkalemic RTA). The kidney is unable to adequately acidify urine or excrete ammonium despite systemic acidosis."
    )
    
    stage: str = Field(
        ...,
        description="Classification of urine anion gap result (Negative UAG, Normal UAG, Positive UAG)",
        example="Positive UAG"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the clinical implication",
        example="Renal cause likely"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 20.0,
                "unit": "mEq/L",
                "interpretation": "Positive urine anion gap of 20.0 mEq/L suggests a renal cause of non-anion gap metabolic acidosis. This indicates impaired renal ammonium excretion, typically seen in renal tubular acidosis (Type 1 distal RTA, Type 2 proximal RTA, Type 4 hyperkalemic RTA). The kidney is unable to adequately acidify urine or excrete ammonium despite systemic acidosis.",
                "stage": "Positive UAG",
                "stage_description": "Renal cause likely"
            }
        }