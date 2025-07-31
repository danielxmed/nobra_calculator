"""
AKIN Classification for Acute Kidney Injury (AKI) Models

Request and response models for AKIN Classification calculation.

References (Vancouver style):
1. Mehta RL, Kellum JA, Shah SV, Molitoris BA, Ronco C, Warnock DG, Levin A; Acute 
   Kidney Injury Network. Acute Kidney Injury Network: report of an initiative to 
   improve outcomes in acute kidney injury. Crit Care. 2007;11(2):R31. 
   doi: 10.1186/cc5713.
2. Lopes JA, Jorge S. The RIFLE and AKIN classifications for acute kidney injury: 
   a critical and comprehensive review. Clin Kidney J. 2013;6(1):8-14. 
   doi: 10.1093/ckj/sfs160.
3. Xiong J, Tang X, Hu Z, Nie L, Wang Y, Zhao J. The RIFLE versus AKIN classification 
   for incidence and mortality of acute kidney injury in critical ill patients: 
   A meta-analysis. Sci Rep. 2015;5:17917. doi: 10.1038/srep17917.

The AKIN (Acute Kidney Injury Network) classification is a standardized system for 
diagnosing and staging acute kidney injury. It was developed to improve upon the 
RIFLE criteria and provides better sensitivity for detecting mild AKI.

Key features of AKIN classification:
- Requires changes within 48 hours
- Uses serum creatinine and urine output criteria
- More sensitive than RIFLE for detecting Stage 1 AKI
- Patients on RRT are automatically classified as Stage 3
- Associated with increased mortality even at Stage 1

AKIN Stages:
- Stage 1: Cr ≥0.3 mg/dL increase or 1.5-2x baseline OR UO <0.5 mL/kg/hr x >6h
- Stage 2: Cr 2-3x baseline OR UO <0.5 mL/kg/hr x >12h  
- Stage 3: Cr >3x baseline or ≥4.0 mg/dL with acute increase ≥0.5 mg/dL OR 
           UO <0.3 mL/kg/hr x ≥24h or anuria x 12h OR RRT
"""

from pydantic import BaseModel, Field
from typing import Optional, Literal, List


class AkinRequest(BaseModel):
    """
    Request model for AKIN Classification for Acute Kidney Injury
    
    The AKIN classification provides a standardized framework for diagnosing and 
    staging acute kidney injury based on serum creatinine and urine output criteria 
    within a 48-hour timeframe.
    
    Key Requirements:
    - Changes must occur within 48 hours
    - Adequate hydration status must be achieved
    - Urinary tract obstruction must be excluded
    - At least two creatinine measurements within 48 hours
    
    AKIN Stages:
    - Stage 1 (Mild AKI): 
      * Creatinine: ≥0.3 mg/dL increase OR 1.5-2x baseline
      * Urine output: <0.5 mL/kg/hr for >6 hours
    
    - Stage 2 (Moderate AKI):
      * Creatinine: 2-3x baseline
      * Urine output: <0.5 mL/kg/hr for >12 hours
    
    - Stage 3 (Severe AKI):
      * Creatinine: >3x baseline OR ≥4.0 mg/dL with acute increase ≥0.5 mg/dL
      * Urine output: <0.3 mL/kg/hr for ≥24 hours OR anuria for 12 hours
      * OR on renal replacement therapy
    
    Clinical Applications:
    - ICU patient monitoring
    - Risk stratification
    - Clinical decision-making
    - Prognosis assessment
    - Research standardization
    
    Advantages over RIFLE:
    - More sensitive for mild AKI
    - Defined 48-hour timeframe
    - No baseline creatinine required
    - Better mortality prediction
    - Excludes dehydration cases

    References (Vancouver style):
    1. Mehta RL, Kellum JA, Shah SV, Molitoris BA, Ronco C, Warnock DG, Levin A; Acute 
    Kidney Injury Network. Acute Kidney Injury Network: report of an initiative to 
    improve outcomes in acute kidney injury. Crit Care. 2007;11(2):R31. 
    doi: 10.1186/cc5713.
    2. Lopes JA, Jorge S. The RIFLE and AKIN classifications for acute kidney injury: 
    a critical and comprehensive review. Clin Kidney J. 2013;6(1):8-14. 
    doi: 10.1093/ckj/sfs160.
    3. Xiong J, Tang X, Hu Z, Nie L, Wang Y, Zhao J. The RIFLE versus AKIN classification 
    for incidence and mortality of acute kidney injury in critical ill patients: 
    A meta-analysis. Sci Rep. 2015;5:17917. doi: 10.1038/srep17917.
    """
    
    current_creatinine: float = Field(
        ...,
        description="Current serum creatinine level in mg/dL",
        ge=0.1,
        le=15.0,
        example=2.5
    )
    
    baseline_creatinine: Optional[float] = Field(
        None,
        description="Baseline serum creatinine in mg/dL (if known). Not required for AKIN classification",
        ge=0.1,
        le=15.0,
        example=1.0
    )
    
    creatinine_increase: Optional[float] = Field(
        None,
        description="Absolute increase in creatinine from baseline in mg/dL (if baseline known)",
        ge=0.0,
        le=10.0,
        example=1.5
    )
    
    urine_output_6h: Optional[float] = Field(
        None,
        description="Total urine output over 6 hours in mL/kg (Stage 1 criterion: <3.0 mL/kg = <0.5 mL/kg/hr)",
        ge=0.0,
        le=50.0,
        example=2.5
    )
    
    urine_output_12h: Optional[float] = Field(
        None,
        description="Total urine output over 12 hours in mL/kg (Stage 2 criterion: <6.0 mL/kg = <0.5 mL/kg/hr)",
        ge=0.0,
        le=100.0,
        example=4.0
    )
    
    urine_output_24h: Optional[float] = Field(
        None,
        description="Total urine output over 24 hours in mL/kg (Stage 3 criterion: <7.2 mL/kg = <0.3 mL/kg/hr)",
        ge=0.0,
        le=200.0,
        example=6.0
    )
    
    anuria_12h: Optional[Literal["yes", "no"]] = Field(
        None,
        description="Anuria (no urine output) for 12 hours (Stage 3 criterion)",
        example="no"
    )
    
    on_rrt: Optional[Literal["yes", "no"]] = Field(
        None,
        description="Patient on renal replacement therapy (automatically Stage 3 regardless of other criteria)",
        example="no"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "current_creatinine": 2.5,
                "baseline_creatinine": 1.0,
                "creatinine_increase": 1.5,
                "urine_output_6h": 2.5,
                "urine_output_12h": 4.0,
                "urine_output_24h": 6.0,
                "anuria_12h": "no",
                "on_rrt": "no"
            }
        }


class AkinResponse(BaseModel):
    """
    Response model for AKIN Classification for Acute Kidney Injury
    
    The response provides the AKIN stage classification with detailed clinical 
    interpretation and management recommendations for patients with suspected 
    or confirmed acute kidney injury.
    
    AKIN Stage Interpretations:
    
    No AKI:
    * No criteria met for acute kidney injury
    * Continue routine monitoring
    * Ensure adequate hydration and avoid nephrotoxins
    
    Stage 1 (Mild AKI):
    * Mortality risk: Increased
    * Close monitoring required
    * Consider nephrology consultation
    * Daily creatinine monitoring
    * Review medications and optimize fluid status
    
    Stage 2 (Moderate AKI):
    * Mortality risk: Significantly increased
    * Intensive monitoring required
    * Nephrology consultation recommended
    * Daily creatinine monitoring
    * Consider underlying causes
    
    Stage 3 (Severe AKI):
    * Mortality risk: Markedly increased
    * Urgent nephrology consultation required
    * Consider renal replacement therapy
    * Intensive monitoring
    * Address underlying causes aggressively
    
    Clinical Decision Support:
    - Risk stratification for mortality
    - Nephrology consultation timing
    - Monitoring intensity requirements
    - RRT consideration
    - Medication dosing adjustments
    
    Important Considerations:
    - Requires changes within 48 hours
    - Adequate hydration must be ensured
    - Urinary obstruction must be excluded
    - Use with clinical context and judgment
    - Associated with increased mortality at all stages
    
    Reference: Mehta RL, et al. Crit Care. 2007;11(2):R31.
    """
    
    result: str = Field(
        ...,
        description="AKIN stage classification result",
        example="Stage 1"
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the classification",
        example="stage"
    )
    
    interpretation: str = Field(
        ...,
        description="Comprehensive clinical interpretation with management recommendations",
        example="AKIN Stage 1: Mild AKI. Current creatinine: 2.5 mg/dL. Baseline creatinine: 1.0 mg/dL. Criteria met: Creatinine 1.5-2x baseline (2.5x); Absolute creatinine increase ≥0.3 mg/dL (1.5 mg/dL); Urine output <0.5 mL/kg/hr for >6 hours (0.42 mL/kg/hr). MANAGEMENT: Close monitoring required. Consider nephrology consultation. Review medications and optimize fluid status. Monitor creatinine daily. IMPORTANT: AKIN classification requires changes within 48 hours, adequate hydration, and exclusion of urinary obstruction. Use with clinical context."
    )
    
    stage: str = Field(
        ...,
        description="AKIN stage name",
        example="Stage 1"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the AKI severity",
        example="Mild AKI"
    )
    
    stage_number: int = Field(
        ...,
        description="Numeric stage (0=No AKI, 1=Stage 1, 2=Stage 2, 3=Stage 3)",
        ge=0,
        le=3,
        example=1
    )
    
    criteria_met: List[str] = Field(
        ...,
        description="List of AKIN criteria that were met",
        example=[
            "Creatinine 1.5-2x baseline (2.5x)",
            "Absolute creatinine increase ≥0.3 mg/dL (1.5 mg/dL)",
            "Urine output <0.5 mL/kg/hr for >6 hours (0.42 mL/kg/hr)"
        ]
    )
    
    mortality_risk: str = Field(
        ...,
        description="Associated mortality risk level",
        example="Increased"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "result": "Stage 1",
                "unit": "stage",
                "interpretation": "AKIN Stage 1: Mild AKI. Current creatinine: 2.5 mg/dL. Baseline creatinine: 1.0 mg/dL. Criteria met: Creatinine 1.5-2x baseline (2.5x); Absolute creatinine increase ≥0.3 mg/dL (1.5 mg/dL); Urine output <0.5 mL/kg/hr for >6 hours (0.42 mL/kg/hr). MANAGEMENT: Close monitoring required. Consider nephrology consultation. Review medications and optimize fluid status. Monitor creatinine daily. IMPORTANT: AKIN classification requires changes within 48 hours, adequate hydration, and exclusion of urinary obstruction. Use with clinical context.",
                "stage": "Stage 1",
                "stage_description": "Mild AKI",
                "stage_number": 1,
                "criteria_met": [
                    "Creatinine 1.5-2x baseline (2.5x)",
                    "Absolute creatinine increase ≥0.3 mg/dL (1.5 mg/dL)",
                    "Urine output <0.5 mL/kg/hr for >6 hours (0.42 mL/kg/hr)"
                ],
                "mortality_risk": "Increased"
            }
        }