"""
Urine Output and Fluid Balance Calculator Models

Request and response models for urine output and fluid balance calculation.

References (Vancouver style):
1. Kellum JA, Lameire N, Aspelin P, et al. Kidney disease: improving global 
   outcomes (KDIGO) acute kidney injury work group. KDIGO clinical practice 
   guideline for acute kidney injury. Kidney Int Suppl. 2012;2(1):1-138.
2. Macedo E, Malhotra R, Bouchard J, Wynn SK, Mehta RL. Oliguria is an early 
   predictor of higher mortality in critically ill patients. Kidney Int. 2011;80(7):760-767.

The Urine Output and Fluid Balance calculator assesses renal function and fluid status by
calculating the urine output rate per kg body weight per hour. This tool helps identify
oliguria, polyuria, and fluid imbalances in hospitalized patients, particularly those 
at risk for acute kidney injury.

Clinical significance:
- Normal urine output: 1.0-2.0 mL/kg/hr (800-2000 mL/24h in adults)
- Oliguria: <0.5 mL/kg/hr for >6 hours (<400 mL/24h)
- Anuria: <0.3 mL/kg/hr or <50 mL/24h
- Polyuria: >2.0 mL/kg/hr (>3000 mL/24h or >50 mL/kg/24h)

Fluid balance calculation helps assess net fluid retention or loss, important for
management of critically ill patients and those with cardiovascular or renal disease.
"""

from pydantic import BaseModel, Field


class UrineOutputFluidBalanceRequest(BaseModel):
    """
    Request model for Urine Output and Fluid Balance Calculator
    
    This calculator assesses renal function and fluid status by measuring urine output
    rate and calculating fluid balance over a specified collection period.
    
    Parameters:
    - weight_kg: Patient body weight in kilograms (1-300 kg)
    - urine_output_ml: Total urine output in milliliters during collection period (0-10000 mL)
    - collection_hours: Duration of collection period in hours (1-48 hours)
    - fluid_intake_ml: Total fluid intake in milliliters during same period (0-20000 mL)
    
    The calculator determines urine output rate using the formula:
    Urine Output Rate (mL/kg/hr) = Total Urine Output (mL) / (Weight (kg) × Collection Hours)
    
    Normal ranges:
    - Normal: 1.0-2.0 mL/kg/hr
    - Oliguria: 0.3-0.5 mL/kg/hr  
    - Anuria/Severe Oliguria: <0.3 mL/kg/hr
    - Polyuria: >2.0 mL/kg/hr
    
    References (Vancouver style):
    1. Kellum JA, Lameire N, Aspelin P, et al. Kidney disease: improving global 
    outcomes (KDIGO) acute kidney injury work group. KDIGO clinical practice 
    guideline for acute kidney injury. Kidney Int Suppl. 2012;2(1):1-138.
    2. Macedo E, Malhotra R, Bouchard J, Wynn SK, Mehta RL. Oliguria is an early 
    predictor of higher mortality in critically ill patients. Kidney Int. 2011;80(7):760-767.
    """
    
    weight_kg: float = Field(
        ...,
        ge=1,
        le=300,
        description="Patient body weight in kilograms. Used to normalize urine output rate per kilogram of body weight",
        example=70.0
    )
    
    urine_output_ml: float = Field(
        ...,
        ge=0,
        le=10000,
        description="Total urine output in milliliters measured during the collection period. Include all urine collected via catheter, collection bag, or other methods",
        example=1200.0
    )
    
    collection_hours: float = Field(
        ...,
        ge=1,
        le=48,
        description="Number of hours for the urine collection period. Standard periods are 6, 8, 12, or 24 hours. Must match the timeframe for both urine output and fluid intake measurements",
        example=24.0
    )
    
    fluid_intake_ml: float = Field(
        ...,
        ge=0,
        le=20000,
        description="Total fluid intake in milliliters during the same collection period. Include all IV fluids, oral intake, tube feeding fluids, and any other fluid sources",
        example=2000.0
    )
    
    class Config:
        schema_extra = {
            "example": {
                "weight_kg": 70.0,
                "urine_output_ml": 1200.0,
                "collection_hours": 24.0,
                "fluid_intake_ml": 2000.0
            }
        }


class UrineOutputFluidBalanceResponse(BaseModel):
    """
    Response model for Urine Output and Fluid Balance Calculator
    
    Returns the calculated urine output rate, fluid balance, and clinical interpretation.
    
    The urine output rate is expressed in mL/kg/hr and categorized as:
    - Anuria/Severe Oliguria: <0.3 mL/kg/hr (critical, requires immediate intervention)
    - Oliguria: 0.3-0.5 mL/kg/hr (concerning, monitor closely)
    - Normal Low: 0.5-1.0 mL/kg/hr (acceptable but monitor trends)
    - Normal: 1.0-2.0 mL/kg/hr (optimal range)
    - Polyuria: >2.0 mL/kg/hr (investigate underlying causes)
    
    Fluid balance indicates net fluid retention (positive) or loss (negative).
    Values >500 mL positive suggest fluid overload, while <-500 mL suggests dehydration.
    
    Reference: Kellum JA, et al. KDIGO clinical practice guideline for acute kidney injury. 
    Kidney Int Suppl. 2012;2(1):1-138.
    """
    
    result: float = Field(
        ...,
        description="Calculated urine output rate in mL per kg body weight per hour",
        example=0.71
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for urine output rate",
        example="mL/kg/hr"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation of the urine output rate, fluid balance, and recommendations for monitoring or intervention",
        example="Lower normal urine output (0.71 mL/kg/hr). Extrapolated 24-hour output: 1200 mL (normal: 800-2000 mL). Current negative fluid balance (loss) of 800 mL. This is within acceptable range but monitor for trends. Ensure adequate hydration and evaluate if sustained at lower end of range with clinical signs of volume depletion."
    )
    
    stage: str = Field(
        ...,
        description="Clinical classification category based on urine output rate",
        example="Normal Low"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the clinical classification",
        example="Lower normal range"
    )
    
    fluid_balance_ml: float = Field(
        ...,
        description="Calculated fluid balance (intake minus output) in milliliters. Positive values indicate fluid retention, negative values indicate fluid loss",
        example=-800.0
    )
    
    extrapolated_24h_output_ml: float = Field(
        ...,
        description="Calculated 24-hour equivalent urine output for comparison with normal daily ranges (800-2000 mL in adults)",
        example=1200.0
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 0.71,
                "unit": "mL/kg/hr",
                "interpretation": "Lower normal urine output (0.71 mL/kg/hr). Extrapolated 24-hour output: 1200 mL (normal: 800-2000 mL). Current negative fluid balance (loss) of 800 mL. This is within acceptable range but monitor for trends. Ensure adequate hydration and evaluate if sustained at lower end of range with clinical signs of volume depletion.",
                "stage": "Normal Low",
                "stage_description": "Lower normal range",
                "fluid_balance_ml": -800.0,
                "extrapolated_24h_output_ml": 1200.0
            }
        }