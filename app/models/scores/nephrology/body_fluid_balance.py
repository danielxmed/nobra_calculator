"""
Body Fluid Balance Calculator by Inputs and Outputs Models

Request and response models for body fluid balance calculation.

References (Vancouver style):
1. Kaptein EM, Sreeramoju D, Kaptein JS, Kaptein MJ. A systematic approach to factitious 
   hypernatremia: A case report and review of the literature. Clin Nephrol. 2016 Apr;85(4):246-52. 
   doi: 10.5414/CN108716.
2. Konstam MA, Gheorghiade M, Burnett JC Jr, et al. Effects of oral tolvaptan in patients 
   hospitalized for worsening heart failure: the EVEREST Outcome Trial. JAMA. 2007 Mar 28;297(12):1319-31. 
   doi: 10.1001/jama.297.12.1319.
3. Testani JM, Brisco MA, Chen J, McCauley BD, Parikh CR, Tang WH. Timing of hemoconcentration 
   during treatment of acute decompensated heart failure and subsequent survival: importance 
   of sustained decongestion. J Am Coll Cardiol. 2013 Aug 6;62(6):516-24. doi: 10.1016/j.jacc.2013.05.027.
4. Rose BD, Post TW. Clinical Physiology of Acid-Base and Electrolyte Disorders. 5th ed. 
   New York: McGraw-Hill; 2001.

The Body Fluid Balance Calculator provides comprehensive tracking of fluid inputs and outputs 
by accounting for the sodium concentration of various body fluids and administered solutions. 
This allows calculation of both isotonic (0.9% saline equivalent) and free water balance, 
critical for managing complex fluid and electrolyte disorders in hospitalized patients.
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any


class BodyFluidBalanceRequest(BaseModel):
    """
    Request model for Body Fluid Balance Calculator by Inputs and Outputs
    
    This comprehensive fluid balance calculator tracks both fluid volumes and their 
    sodium content to determine net isotonic saline and free water balance. Understanding 
    the sodium concentration of various fluids is crucial for appropriate fluid management, 
    as replacing hypotonic losses with isotonic fluids can lead to hypernatremia, while 
    replacing isotonic losses with hypotonic fluids can cause hyponatremia.
    
    **Fluid Losses and Their Sodium Content:**
    
    **Gastrointestinal Losses:**
    
    **Gastric Secretions (Na ~60 mEq/L):**
    - Hypotonic relative to plasma
    - High in HCl, low in sodium
    - Losses via NG suction, vomiting
    - Can lead to hypochloremic metabolic alkalosis
    
    **Biliary Secretions (Na ~130 mEq/L):**
    - Near isotonic with plasma
    - Contains bicarbonate
    - Losses via biliary drains, fistulas
    - Can cause metabolic acidosis with large volume losses
    
    **Small Bowel Fluid (Na ~110 mEq/L):**
    - Moderately hypotonic
    - Variable composition along bowel length
    - Losses via enterostomy, fistulas
    - Significant potassium content
    
    **Diarrheal Fluid (Na ~60 mEq/L):**
    - Hypotonic in most cases
    - Secretory diarrhea may have higher sodium
    - Contains significant potassium and bicarbonate
    - Can cause hypokalemia and metabolic acidosis
    
    **Renal Losses:**
    
    **Urine (Na variable, typically 40 mEq/L):**
    - Highly variable sodium content (10-200 mEq/L)
    - Depends on renal function and volume status
    - Diuretic use increases sodium losses
    - Consider measuring urine sodium for accuracy
    
    **Other Losses:**
    
    **Insensible Losses (Na 0 mEq/L):**
    - Pure water loss via skin and respiratory tract
    - Typically 500-1000 mL/day at baseline
    - Increases with fever (~13% per °C), tachypnea, burns
    - No electrolyte loss
    
    **Wound/Drain Losses (Na ~140 mEq/L assumed):**
    - Variable composition
    - Serous drainage typically isotonic
    - Measure electrolytes in high-volume losses
    
    **Fluid Gains and Their Sodium Content:**
    
    **Intravenous Fluids:**
    
    **0.9% Normal Saline (Na 154 mEq/L):**
    - Slightly hypertonic relative to plasma
    - No free water content
    - Risk of hyperchloremic acidosis with large volumes
    
    **0.45% Half Normal Saline (Na 77 mEq/L):**
    - Hypotonic solution
    - 50% free water content
    - Used for free water replacement
    
    **Lactated Ringer's (Na 130 mEq/L):**
    - Near isotonic with plasma
    - Contains lactate (metabolized to bicarbonate)
    - More physiologic than normal saline
    
    **D5W (Na 0 mEq/L):**
    - Pure free water after dextrose metabolism
    - Used for free water replacement
    - Risk of hyponatremia with rapid infusion
    
    **Oral Intake (Na 0 mEq/L assumed):**
    - Typically free water
    - Food contains variable sodium
    - Clear liquids usually hypotonic
    
    **Clinical Applications:**
    
    **Volume Status Assessment:**
    - Net negative balance suggests hypovolemia
    - Net positive balance suggests hypervolemia
    - Must correlate with clinical exam
    
    **Sodium Balance:**
    - Helps predict sodium changes
    - Guides fluid selection for replacement
    - Critical in hypo/hypernatremia management
    
    **Heart Failure Management:**
    - Track decongestion progress
    - Guide diuretic therapy
    - Monitor for hemoconcentration
    
    **Critical Care:**
    - Complex fluid management in shock
    - Multiple simultaneous infusions
    - High-volume GI losses
    
    **Important Considerations:**
    
    **Limitations:**
    - Assumes standard sodium concentrations
    - Does not account for third-spacing
    - Ignores other electrolytes (K, HCO3)
    - Clinical assessment always required
    
    **Accuracy Factors:**
    - Measure high-volume fluid electrolytes
    - Consider renal function impact
    - Account for all sources (nutrition, meds)
    - Document timing of measurements
    
    **Special Situations:**
    - Burns: Increased insensible losses
    - Renal failure: Altered sodium handling
    - Liver disease: Third-space losses
    - Post-operative: Variable GI losses
    
    References (Vancouver style):
    1. Kaptein EM, Sreeramoju D, Kaptein JS, Kaptein MJ. A systematic approach to factitious 
    hypernatremia: A case report and review of the literature. Clin Nephrol. 2016 Apr;85(4):246-52. 
    doi: 10.5414/CN108716.
    2. Konstam MA, Gheorghiade M, Burnett JC Jr, et al. Effects of oral tolvaptan in patients 
    hospitalized for worsening heart failure: the EVEREST Outcome Trial. JAMA. 2007 Mar 28;297(12):1319-31. 
    doi: 10.1001/jama.297.12.1319.
    3. Testani JM, Brisco MA, Chen J, McCauley BD, Parikh CR, Tang WH. Timing of hemoconcentration 
    during treatment of acute decompensated heart failure and subsequent survival: importance 
    of sustained decongestion. J Am Coll Cardiol. 2013 Aug 6;62(6):516-24. doi: 10.1016/j.jacc.2013.05.027.
    """
    
    # Fluid Losses
    gastric_losses: Optional[float] = Field(
        None,
        ge=0,
        le=10000,
        description="Volume of gastric losses in mL (NG suction, vomiting). Sodium ~60 mEq/L (hypotonic).",
        example=500.0
    )
    
    biliary_losses: Optional[float] = Field(
        None,
        ge=0,
        le=10000,
        description="Volume of biliary losses in mL (biliary drains, fistulas). Sodium ~130 mEq/L (near isotonic).",
        example=200.0
    )
    
    small_bowel_losses: Optional[float] = Field(
        None,
        ge=0,
        le=10000,
        description="Volume of small bowel losses in mL (enterostomy, fistulas). Sodium ~110 mEq/L (moderately hypotonic).",
        example=0.0
    )
    
    diarrhea_losses: Optional[float] = Field(
        None,
        ge=0,
        le=10000,
        description="Volume of diarrhea losses in mL. Sodium ~60 mEq/L (hypotonic, but variable).",
        example=300.0
    )
    
    urine_output: Optional[float] = Field(
        None,
        ge=0,
        le=10000,
        description="Volume of urine output in mL. Sodium typically ~40 mEq/L but highly variable (10-200 mEq/L).",
        example=1500.0
    )
    
    insensible_losses: Optional[float] = Field(
        None,
        ge=0,
        le=2000,
        description="Estimated insensible losses in mL (skin, respiratory). Pure water loss with no sodium. Typically 500-1000 mL/day.",
        example=800.0
    )
    
    other_losses: Optional[float] = Field(
        None,
        ge=0,
        le=10000,
        description="Other fluid losses in mL (drains, wounds). Assumed isotonic with sodium ~140 mEq/L unless specified.",
        example=0.0
    )
    
    # Fluid Gains
    normal_saline_iv: Optional[float] = Field(
        None,
        ge=0,
        le=10000,
        description="Volume of 0.9% normal saline administered IV in mL. Sodium 154 mEq/L (slightly hypertonic).",
        example=1000.0
    )
    
    half_normal_saline_iv: Optional[float] = Field(
        None,
        ge=0,
        le=10000,
        description="Volume of 0.45% half normal saline administered IV in mL. Sodium 77 mEq/L (hypotonic, 50% free water).",
        example=0.0
    )
    
    lactated_ringers_iv: Optional[float] = Field(
        None,
        ge=0,
        le=10000,
        description="Volume of lactated Ringer's solution administered IV in mL. Sodium 130 mEq/L (near isotonic).",
        example=500.0
    )
    
    d5w_iv: Optional[float] = Field(
        None,
        ge=0,
        le=10000,
        description="Volume of D5W (5% dextrose in water) administered IV in mL. No sodium, pure free water after dextrose metabolism.",
        example=0.0
    )
    
    oral_intake: Optional[float] = Field(
        None,
        ge=0,
        le=10000,
        description="Volume of oral fluid intake in mL. Assumed to be free water unless high sodium content specified.",
        example=800.0
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "gastric_losses": 500.0,
                "biliary_losses": 200.0,
                "small_bowel_losses": 0.0,
                "diarrhea_losses": 300.0,
                "urine_output": 1500.0,
                "insensible_losses": 800.0,
                "other_losses": 0.0,
                "normal_saline_iv": 1000.0,
                "half_normal_saline_iv": 0.0,
                "lactated_ringers_iv": 500.0,
                "d5w_iv": 0.0,
                "oral_intake": 800.0
            }
        }


class BodyFluidBalanceResponse(BaseModel):
    """
    Response model for Body Fluid Balance Calculator
    
    Returns comprehensive fluid balance calculations including total fluid balance, 
    isotonic saline balance, and free water balance. These calculations help guide 
    fluid replacement strategies and predict changes in serum sodium concentration.
    
    **Interpretation of Results:**
    
    **Total Fluid Balance:**
    - Net sum of all inputs minus outputs
    - Positive values indicate fluid accumulation
    - Negative values indicate fluid deficit
    - Should correlate with weight changes (1 kg = 1 L)
    
    **Saline Balance:**
    - Isotonic fluid balance (0.9% NS equivalent)
    - Affects intravascular volume primarily
    - Critical for hemodynamic stability
    
    **Free Water Balance:**
    - Hypotonic fluid balance
    - Affects serum sodium concentration
    - Positive balance → risk of hyponatremia
    - Negative balance → risk of hypernatremia
    
    **Clinical Decision Making:**
    
    **Significant Negative Balance (>500 mL deficit):**
    - High risk for hypovolemia and AKI
    - Consider IV fluid resuscitation
    - Choice of fluid based on sodium status
    - Monitor hemodynamic response
    
    **Moderate Negative Balance (200-500 mL deficit):**
    - May progress to hypovolemia
    - Increase monitoring frequency
    - Consider oral or IV replacement
    - Assess for ongoing losses
    
    **Neutral Balance (±200 mL):**
    - Appropriate fluid homeostasis
    - Continue current management
    - Routine monitoring sufficient
    - Ideal target for most patients
    
    **Positive Balance (>200 mL excess):**
    - Risk for volume overload
    - Consider fluid restriction
    - May need diuretic therapy
    - Monitor for congestion signs
    
    Reference: Rose BD, Post TW. Clinical Physiology of Acid-Base and Electrolyte Disorders. 5th ed. 2001.
    """
    
    result: Dict[str, Any] = Field(
        ...,
        description="Fluid balance calculation results including total, saline, and water balance",
        example={
            "total_fluid_balance": -500,
            "net_saline_balance": -300,
            "net_water_balance": -200,
            "total_losses": 3300,
            "total_gains": 2800
        }
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for fluid volumes",
        example="mL"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation of fluid balance with management recommendations",
        example="Total fluid balance: -500 mL (negative balance). Saline balance: -300 mL, Free water balance: -200 mL. Total inputs: 2800 mL, Total outputs: 3300 mL. Significant fluid deficit requiring prompt replacement. Assess for signs of volume depletion including hypotension, tachycardia, decreased urine output, and elevated BUN/Cr ratio. Consider IV fluid resuscitation based on sodium and free water deficits. This calculation assumes standard sodium concentrations which may vary based on individual patient factors."
    )
    
    stage: str = Field(
        ...,
        description="Fluid balance classification",
        example="Significant Negative Balance"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the fluid balance state",
        example="Net fluid loss >500 mL"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "result": {
                    "total_fluid_balance": -500,
                    "net_saline_balance": -300,
                    "net_water_balance": -200,
                    "total_losses": 3300,
                    "total_gains": 2800
                },
                "unit": "mL",
                "interpretation": "Total fluid balance: -500 mL (negative balance). Saline balance: -300 mL, Free water balance: -200 mL. Total inputs: 2800 mL, Total outputs: 3300 mL. Significant fluid deficit requiring prompt replacement. Assess for signs of volume depletion including hypotension, tachycardia, decreased urine output, and elevated BUN/Cr ratio. Consider IV fluid resuscitation based on sodium and free water deficits. This calculation assumes standard sodium concentrations which may vary based on individual patient factors.",
                "stage": "Significant Negative Balance",
                "stage_description": "Net fluid loss >500 mL"
            }
        }