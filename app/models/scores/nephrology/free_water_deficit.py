"""
Free Water Deficit in Hypernatremia Models

Request and response models for Free Water Deficit calculation.

References (Vancouver style):
1. Adrogue HJ, Madias NE. Hypernatremia. N Engl J Med. 2000;342(20):1493-9. 
   doi: 10.1056/NEJM200005183422006.
2. Moritz ML, Ayus JC. The changing pattern of hypernatremia in hospitalized children. 
   Pediatrics. 1999;104(3 Pt 1):435-9. doi: 10.1542/peds.104.3.435.
3. Verbalis JG, Goldsmith SR, Greenberg A, et al. Diagnosis, evaluation, and treatment 
   of hyponatremia: expert panel recommendations. Am J Med. 2013;126(10 Suppl 1):S1-42. 
   doi: 10.1016/j.amjmed.2013.07.006.

The Free Water Deficit calculator estimates the amount of free water needed to correct 
hypernatremia (elevated serum sodium >145 mEq/L) in patients with dehydration. This 
calculation is essential for safe fluid replacement therapy and preventing complications 
such as cerebral edema from overly rapid correction.

Key Features:
- Uses patient-specific total body water fractions based on age and sex
- Calculates deficit using the standard formula: TBW fraction × Weight × (Current Na/Desired Na - 1)
- Provides safe correction guidelines (≤0.5 mEq/L per hour)
- Accounts for different total body water percentages by demographic group

Total Body Water Fractions:
- Adult Male: 60% (0.6 of body weight)
- Adult Female: 50% (0.5 of body weight)
- Elderly Male: 50% (0.5 of body weight) - decreased muscle mass
- Elderly Female: 45% (0.45 of body weight) - decreased muscle mass
- Child: 60% (0.6 of body weight) - higher water content

Clinical Applications:
- Emergency department management of hypernatremic patients
- ICU fluid management for severe hypernatremia
- Pediatric dehydration management
- Postoperative fluid replacement planning
- Guidance for oral vs. intravenous rehydration decisions

Safety Considerations:
- Maximum safe correction rate: 0.5 mEq/L per hour
- Target initial correction: 10 mEq/L in first 24 hours
- Ongoing monitoring: Check electrolytes every 12 hours
- Additional losses: Account for insensible losses (~1L/day) and ongoing losses
- Risk of rapid correction: Cerebral edema, seizures, permanent neurologic damage

Important Limitations:
- Assumes normal kidney function and no ongoing excessive losses
- May be inaccurate in patients with significant recent weight changes
- Should only be used in hypernatremic patients who are not volume depleted
- Does not account for ongoing free water losses (requires separate calculation)
- Formula accuracy decreases with severe hypernatremia (>170 mEq/L)

Treatment Considerations:
- Mild hypernatremia (146-149 mEq/L): Often oral hydration sufficient
- Moderate hypernatremia (150-160 mEq/L): IV hypotonic fluids usually required
- Severe hypernatremia (>160 mEq/L): ICU monitoring recommended
- Critical hypernatremia (>170 mEq/L): Nephrology consultation advised
"""

from pydantic import BaseModel, Field
from typing import Literal


class FreeWaterDeficitRequest(BaseModel):
    """
    Request model for Free Water Deficit in Hypernatremia
    
    The Free Water Deficit calculator estimates the amount of free water needed to safely 
    correct hypernatremia in patients with dehydration. This calculation uses patient-specific 
    total body water fractions and provides guidelines for safe correction rates.
    
    **REQUIRED PARAMETERS**:
    
    **Demographics (affect total body water calculation)**:
    - **Sex**: Male vs female (different body composition affects water distribution)
    - **Age Category**: Child, adult, or elderly (muscle mass changes affect total body water)
    - **Weight**: Current body weight in kilograms (basis for total body water calculation)
    
    **Laboratory Values**:
    - **Current Sodium**: Measured serum sodium level (hypernatremia >145 mEq/L)
    - **Desired Sodium**: Target serum sodium for correction (typically 140 mEq/L)
    
    **TOTAL BODY WATER FRACTIONS**:
    The calculator uses established fractions of body weight to estimate total body water:
    - **Adult Male**: 60% (0.6) - higher muscle mass, more water content
    - **Adult Female**: 50% (0.5) - higher fat percentage, less water content
    - **Elderly Male**: 50% (0.5) - decreased muscle mass with aging
    - **Elderly Female**: 45% (0.45) - lowest water content due to age and sex
    - **Child**: 60% (0.6) - higher water content in pediatric patients
    
    **CALCULATION FORMULA**:
    Free Water Deficit (L) = TBW fraction × Weight (kg) × (Current Na/Desired Na - 1)
    
    Where TBW fraction is selected based on age category and sex from the table above.
    
    **SAFETY GUIDELINES**:
    - **Maximum Correction Rate**: 0.5 mEq/L per hour to prevent cerebral edema
    - **Initial Target**: Reduce sodium by 10 mEq/L in first 24 hours
    - **Ongoing Correction**: 10 mEq/L per day until normalized
    - **Monitoring**: Check electrolytes every 12 hours during active correction
    - **Additional Losses**: Add ~1L/day for insensible losses, more for ongoing losses
    
    **CLINICAL APPLICATIONS**:
    - Emergency department hypernatremia management
    - ICU fluid replacement planning
    - Pediatric dehydration correction
    - Postoperative fluid management
    - Determining oral vs. intravenous hydration needs
    
    **IMPORTANT CONTRAINDICATIONS**:
    - Volume-depleted patients (use isotonic fluids first for volume repletion)
    - Patients with ongoing high-volume losses without replacement
    - Severe kidney disease with inability to concentrate urine
    - Recent significant weight changes that affect total body water estimation
    
    **MONITORING REQUIREMENTS**:
    - Hourly neurologic assessments during active correction
    - Electrolyte panels every 12 hours initially, then daily
    - Fluid input/output monitoring
    - Daily weights to assess volume status
    - Adjustment for ongoing losses (urine, insensible, GI losses)
    
    References (Vancouver style):
    1. Adrogue HJ, Madias NE. Hypernatremia. N Engl J Med. 2000;342(20):1493-9.
    2. Moritz ML, Ayus JC. The changing pattern of hypernatremia in hospitalized children. 
       Pediatrics. 1999;104(3 Pt 1):435-9.
    3. Verbalis JG, Goldsmith SR, Greenberg A, et al. Diagnosis, evaluation, and treatment 
       of hyponatremia: expert panel recommendations. Am J Med. 2013;126(10 Suppl 1):S1-42.
    """
    
    sex: Literal["male", "female"] = Field(
        ...,
        description="Patient sex. Affects total body water fraction: males have higher water content (60% adult, 50% elderly) vs females (50% adult, 45% elderly)",
        example="male"
    )
    
    age_category: Literal["child", "adult", "elderly"] = Field(
        ...,
        description="Patient age category. Affects total body water: child 60%, adult male 60%/female 50%, elderly male 50%/female 45%",
        example="adult"
    )
    
    weight: float = Field(
        ...,
        description="Patient weight in kilograms. Used to calculate total body water (TBW = weight × TBW fraction). Valid range: 0.226-226.796 kg",
        ge=0.226,
        le=226.796,
        example=70.0
    )
    
    current_sodium: float = Field(
        ...,
        description="Current serum sodium level in mEq/L. Must be elevated (>145 mEq/L) for hypernatremia calculation. Valid range: 100-200 mEq/L",
        ge=100,
        le=200,
        example=155.0
    )
    
    desired_sodium: float = Field(
        ...,
        description="Desired target serum sodium level in mEq/L. Typically 140 mEq/L for normal correction. Must be less than current sodium. Valid range: 135-145 mEq/L",
        ge=135,
        le=145,
        example=140.0
    )
    
    class Config:
        schema_extra = {
            "example": {
                "sex": "male",
                "age_category": "adult",
                "weight": 70.0,
                "current_sodium": 155.0,
                "desired_sodium": 140.0
            }
        }


class FreeWaterDeficitResponse(BaseModel):
    """
    Response model for Free Water Deficit in Hypernatremia
    
    The response provides the calculated free water deficit needed to correct hypernatremia, 
    along with detailed clinical interpretation, safety guidelines, and management recommendations 
    based on established protocols for hypernatremia correction.
    
    **DEFICIT CATEGORIES AND MANAGEMENT**:
    
    **Mild Deficit (<2L)**:
    - **Management**: Often manageable with oral hydration if patient can tolerate
    - **Monitoring**: Serum sodium every 12 hours
    - **Safety**: Still follow maximum 0.5 mEq/L per hour correction rate
    - **Duration**: Can often be corrected safely within 24-48 hours
    - **Setting**: May be managed in regular medical unit with close monitoring
    
    **Moderate Deficit (2-5L)**:
    - **Management**: IV fluid replacement typically required (5% dextrose or hypotonic saline)
    - **Target**: 10 mEq/L correction in first 24 hours, then 10 mEq/L per day
    - **Monitoring**: Electrolytes every 12 hours, neurologic checks every 4-6 hours
    - **Additional**: Account for insensible losses (~1L/day) and ongoing losses
    - **Setting**: Medical unit with experienced nursing care
    
    **Severe Deficit (5-10L)**:
    - **Management**: Careful IV fluid management with intensive monitoring
    - **Setting**: Consider ICU monitoring for complex cases
    - **Rate**: Strict adherence to maximum 0.5 mEq/L per hour correction
    - **Monitoring**: Consider hourly electrolytes initially, then every 12 hours
    - **Consultation**: Consider nephrology consultation for complex cases
    - **Duration**: Typically requires 3-5 days for safe correction
    
    **Critical Deficit (>10L)**:
    - **Management**: Intensive monitoring with nephrology consultation mandatory
    - **Setting**: ICU management recommended
    - **Monitoring**: Hourly electrolytes and neurologic assessments initially
    - **Rate**: Extreme caution with correction rate - consider even slower than 0.5 mEq/L per hour
    - **Consultation**: Nephrology and critical care medicine involvement
    - **Complications**: High risk for correction-related complications
    
    **FLUID REPLACEMENT OPTIONS**:
    
    **5% Dextrose in Water (D5W)**:
    - **Indication**: Pure free water deficit without volume depletion
    - **Benefits**: Provides free water without additional sodium
    - **Monitoring**: Watch for hyperglycemia, especially in diabetics
    - **Rate**: Based on calculated deficit and safe correction rate
    
    **0.45% Saline (Half-Normal Saline)**:
    - **Indication**: Hypernatremia with mild volume depletion
    - **Benefits**: Provides some free water plus small amount of sodium
    - **Calculation**: Provides approximately 0.5L free water per liter infused
    - **Use**: When pure free water may be too hypotonic
    
    **0.25% Saline (Quarter-Normal Saline)**:
    - **Indication**: Severe hypernatremia where very hypotonic fluid needed
    - **Benefits**: Maximum free water content with minimal sodium
    - **Availability**: May need to be specially prepared by pharmacy
    - **Use**: Reserved for most severe cases under specialist guidance
    
    **MONITORING PARAMETERS**:
    
    **Laboratory Monitoring**:
    - **Electrolytes**: Every 12 hours initially, then daily once stable
    - **Osmolality**: If available, helps confirm correction adequacy
    - **Glucose**: If using dextrose-containing solutions
    - **Kidney Function**: BUN/creatinine to assess renal response
    
    **Clinical Monitoring**:
    - **Neurologic Status**: Mental status, seizure activity, focal deficits
    - **Volume Status**: Daily weights, input/output, vital signs
    - **Correction Rate**: Calculate actual vs. target sodium change hourly
    - **Complications**: Signs of cerebral edema or overcorrection
    
    **COMPLICATIONS TO AVOID**:
    
    **Overly Rapid Correction (>0.5 mEq/L per hour)**:
    - **Risk**: Cerebral edema from rapid fluid shifts into brain cells
    - **Signs**: Altered mental status, seizures, focal neurologic deficits
    - **Prevention**: Strict adherence to maximum correction rates
    - **Management**: Stop correction, consider hypertonic saline if severe
    
    **Undercorrection**:
    - **Risk**: Persistent hypernatremia with ongoing neurologic dysfunction
    - **Causes**: Inadequate fluid replacement, ongoing losses not replaced
    - **Prevention**: Account for all fluid losses, adequate monitoring
    - **Management**: Reassess losses, increase replacement rate if safe
    
    **SPECIAL POPULATIONS**:
    
    **Pediatric Patients**:
    - **Calculation**: Use child TBW fraction (60%) regardless of sex
    - **Monitoring**: More frequent assessments due to smaller fluid volumes
    - **Complications**: Higher risk for cerebral edema with rapid correction
    - **Expertise**: Pediatric nephrology consultation for severe cases
    
    **Elderly Patients**:
    - **Calculation**: Use reduced TBW fractions (male 50%, female 45%)
    - **Comorbidities**: Consider heart failure, kidney disease
    - **Monitoring**: May need slower correction rates due to comorbidities
    - **Volume**: Higher risk for volume overload during correction
    
    **Quality Measures**:
    - Established formula validated in clinical practice
    - Evidence-based correction rate guidelines
    - Widely used in emergency medicine and nephrology
    - Included in major clinical practice guidelines
    
    Reference: Adrogue HJ, Madias NE. N Engl J Med. 2000;342(20):1493-9.
    """
    
    result: float = Field(
        ...,
        description="Free water deficit in liters needed to correct hypernatremia from current to desired sodium level",
        example=6.3
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the deficit calculation",
        example="L"
    )
    
    interpretation: str = Field(
        ...,
        description="Comprehensive clinical interpretation including deficit severity, correction strategy, monitoring requirements, and safety guidelines",
        example="Free water deficit of 6.30 L calculated to correct serum sodium from 155.0 to 140.0 mEq/L. Severe deficit requiring careful IV fluid management with close monitoring. Correction should not exceed 0.5 mEq/L per hour to prevent cerebral edema (minimum 30.0 hours for safe correction). Use 5% dextrose or hypotonic solutions. Consider ICU monitoring. Target maximum 10 mEq/L correction in 24 hours, then 10 mEq/L per day. Account for ongoing losses and insensible losses."
    )
    
    stage: str = Field(
        ...,
        description="Deficit severity category (Mild Deficit, Moderate Deficit, Severe Deficit, Critical Deficit)",
        example="Severe Deficit"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the deficit severity",
        example="Severe free water deficit"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 6.3,
                "unit": "L",
                "interpretation": "Free water deficit of 6.30 L calculated to correct serum sodium from 155.0 to 140.0 mEq/L. Severe deficit requiring careful IV fluid management with close monitoring. Correction should not exceed 0.5 mEq/L per hour to prevent cerebral edema (minimum 30.0 hours for safe correction). Use 5% dextrose or hypotonic solutions. Consider ICU monitoring. Target maximum 10 mEq/L correction in 24 hours, then 10 mEq/L per day. Account for ongoing losses and insensible losses.",
                "stage": "Severe Deficit",
                "stage_description": "Severe free water deficit"
            }
        }