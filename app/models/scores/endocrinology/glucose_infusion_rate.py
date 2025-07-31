"""
Glucose Infusion Rate (GIR) Models

Request and response models for Glucose Infusion Rate calculation.

References (Vancouver style):
1. Kalhan SC, Parimi PS. Gluconeogenesis in the fetus and neonate. Semin Perinatol. 
   2000;24(2):94-106. doi: 10.1053/sp.2000.6360.
2. Ditzenberger GR, Collins SD, Binder N. Continuous insulin infusion in the management 
   of hyperglycemia in the pediatric intensive care unit. Pediatr Crit Care Med. 
   2004;5(1):27-32. doi: 10.1097/01.PCC.0000102223.83245.02.
3. Sinclair JC, Bottino M, Cowett RM. Interventions for prevention of neonatal 
   hyperglycemia in very low birth weight infants. Cochrane Database Syst Rev. 
   2011;(10):CD007615. doi: 10.1002/14651858.CD007615.pub3.
4. Hay WW Jr, Raju TN, Higgins RD, Kalhan SC, Devaskar SU. Knowledge gaps and research 
   needs for understanding and treating neonatal hypoglycemia: workshop report from 
   Eunice Kennedy Shriver National Institute of Child Health and Human Development. 
   J Pediatr. 2009;155(5):612-617. doi: 10.1016/j.jpeds.2009.06.044.

The Glucose Infusion Rate (GIR) is a fundamental calculation in neonatal and pediatric 
medicine that quantifies the rate at which glucose is delivered intravenously. This 
measurement is critical for:

1. **Preventing Hypoglycemia**: Ensuring adequate glucose delivery to maintain blood 
   glucose levels, particularly in preterm infants and critically ill children
2. **Optimizing Nutrition**: Guiding parenteral nutrition protocols to provide 
   appropriate caloric intake for growth and development
3. **Managing Hyperglycemia**: Avoiding excessive glucose administration that can 
   lead to metabolic complications
4. **Insulin Therapy Decisions**: Determining when insulin co-administration is needed

**Clinical Formula**:
GIR (mg/kg/min) = [Infusion rate (mL/hr) × Dextrose concentration (%) × 10] / [Weight (kg) × 60]

**Simplified Mental Calculation**:
GIR ≈ (Dextrose % × mL/kg/hr) / 6

**Clinical Ranges**:
- **Physiologic**: 4-8 mg/kg/min (normal glucose utilization)
- **Therapeutic**: 8-12 mg/kg/min (enhanced delivery for growth)
- **High Therapeutic**: 12-18 mg/kg/min (full parenteral nutrition)
- **Excessive**: >18 mg/kg/min (risk of complications)

**Key Clinical Considerations**:
- Baseline glucose utilization in term infants: 4-6 mg/kg/min
- Preterm infants typically need 5-8 mg/kg/min initially
- GIR should not fall below 4 mg/kg/min in non-feeding infants
- GIR >10-12 mg/kg/min may require intensive care monitoring
- High-concentration dextrose (>12.5%) typically requires central venous access

This calculation is essential for safe and effective glucose management in vulnerable 
pediatric populations, helping prevent both hypoglycemic and hyperglycemic complications.
"""

from pydantic import BaseModel, Field


class GlucoseInfusionRateRequest(BaseModel):
    """
    Request model for Glucose Infusion Rate (GIR) calculation
    
    The GIR calculation requires three essential parameters to determine the rate of 
    intravenous glucose delivery:
    
    **Infusion Rate**: The volumetric flow rate of the IV dextrose solution
    - Measured in mL/hr (milliliters per hour)
    - Represents the continuous infusion rate set on IV pump
    - Typical ranges: 1-100 mL/hr depending on patient size and clinical needs
    - Higher rates may be needed for total parenteral nutrition protocols
    
    **Dextrose Concentration**: The percentage strength of glucose in the IV solution
    - Expressed as percentage (w/v): e.g., D5W = 5%, D10W = 10%
    - Common concentrations:
      * D2.5W (2.5%): Very dilute, rarely used
      * D5W (5%): Standard maintenance fluid
      * D10W (10%): Common in neonatal care
      * D12.5W (12.5%): Higher concentration, often requires central line
      * D15W-D25W (15-25%): High concentrations for parenteral nutrition
    - Concentrations >12.5% typically require central venous access for safe administration
    
    **Patient Weight**: Essential for calculating per-kilogram dosing
    - Measured in kilograms (kg)
    - Critical for pediatric and neonatal dosing calculations
    - Should be current/accurate weight, as GIR is weight-dependent
    - Preterm infants may weigh <1 kg, while pediatric patients can weigh up to adult sizes
    
    **Clinical Applications**:
    - Neonatal intensive care unit (NICU) glucose management
    - Pediatric intensive care unit (PICU) nutritional support
    - Total parenteral nutrition (TPN) protocols
    - Prevention and management of neonatal hypoglycemia
    - Guidance for insulin therapy initiation
    - Transition planning from IV to enteral nutrition

    References (Vancouver style):
    1. Kalhan SC, Parimi PS. Gluconeogenesis in the fetus and neonate. Semin Perinatol. 
    2000;24(2):94-106. doi: 10.1053/sp.2000.6360.
    2. Hay WW Jr, Raju TN, Higgins RD, Kalhan SC, Devaskar SU. Knowledge gaps and research 
    needs for understanding and treating neonatal hypoglycemia: workshop report from 
    Eunice Kennedy Shriver National Institute of Child Health and Human Development. 
    J Pediatr. 2009;155(5):612-617. doi: 10.1016/j.jpeds.2009.06.044.
    """
    
    infusion_rate: float = Field(
        ...,
        description="Intravenous infusion rate of dextrose solution in mL/hr. Represents the continuous IV pump rate delivering glucose to the patient. Typical ranges: 1-100 mL/hr depending on patient size and clinical indication",
        gt=0.0,
        le=1000.0,
        example=18.0
    )
    
    dextrose_concentration: float = Field(
        ...,
        description="Concentration of dextrose in the IV solution as percentage (e.g., 5.0 for D5W, 10.0 for D10W, 12.5 for D12.5W). Higher concentrations (>12.5%) typically require central venous access for safe administration",
        ge=1.0,
        le=50.0,
        example=10.0
    )
    
    weight: float = Field(
        ...,
        description="Patient weight in kilograms. Essential for calculating per-kilogram glucose delivery rate. Should be current and accurate weight as GIR is weight-dependent. Ranges from <1 kg (extreme preterm) to adult weights",
        gt=0.0,
        le=200.0,
        example=3.0
    )
    
    class Config:
        schema_extra = {
            "example": {
                "infusion_rate": 18.0,
                "dextrose_concentration": 10.0,
                "weight": 3.0
            }
        }


class GlucoseInfusionRateResponse(BaseModel):
    """
    Response model for Glucose Infusion Rate (GIR) calculation
    
    Provides the calculated GIR with clinical interpretation and management recommendations.
    
    **GIR Clinical Ranges and Interpretations**:
    
    **Below Normal (<4 mg/kg/min)**:
    - Risk of hypoglycemia in non-feeding infants
    - Insufficient to meet baseline glucose utilization
    - Requires immediate intervention to prevent complications
    
    **Normal/Physiologic (4-8 mg/kg/min)**:
    - Appropriate for maintenance glucose needs
    - Covers baseline glucose utilization in term infants (4-6 mg/kg/min)
    - Suitable for stable patients receiving IV fluids
    
    **Moderate/Therapeutic (8-12 mg/kg/min)**:
    - Enhanced glucose delivery for growth and anabolism
    - Common in parenteral nutrition protocols
    - May require intensive monitoring for hyperglycemia
    
    **High Therapeutic (12-18 mg/kg/min)**:
    - High glucose delivery for full parenteral nutrition
    - Optimal for growth in premature infants
    - Often requires insulin co-administration
    - Needs frequent glucose monitoring
    
    **Excessive (>18 mg/kg/min)**:
    - Risk of hyperglycemia and metabolic complications
    - Associated with lipogenesis and fatty liver deposits
    - Increased CO2 production and respiratory burden
    - Requires immediate intervention to reduce glucose load
    
    **Management Implications**:
    - GIR guides insulin therapy decisions
    - Helps balance nutrition between glucose, protein, and lipids
    - Influences choice of vascular access (peripheral vs. central)
    - Determines monitoring frequency and intensity of care
    
    Reference: Hay WW Jr, et al. J Pediatr. 2009;155(5):612-617.
    """
    
    result: float = Field(
        ...,
        description="Calculated Glucose Infusion Rate in mg/kg/min. Represents the rate of glucose delivery per kilogram of body weight per minute",
        ge=0.0,
        example=6.0
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for glucose infusion rate",
        example="mg/kg/min"
    )
    
    interpretation: str = Field(
        ...,
        description="Comprehensive clinical interpretation including parameter summary, GIR classification, clinical significance, monitoring recommendations, and specific management guidance based on the calculated rate",
        example="Infusion parameters: 18.0 mL/hr of D10W (10.0% dextrose) in 3.0 kg patient. Calculated GIR: 6.00 mg/kg/min. Normal/Physiologic Range. GIR 4.0-8.0 mg/kg/min represents normal glucose utilization rate. Continue current regimen with routine glucose monitoring every 4-6 hours. Appropriate for maintenance therapy in stable patients."
    )
    
    stage: str = Field(
        ...,
        description="Clinical classification of the GIR range (Below Normal, Normal/Physiologic, Moderate/Therapeutic, High Therapeutic, Excessive)",
        example="Normal/Physiologic Range"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the clinical significance of the GIR range",
        example="Appropriate glucose delivery"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 6.0,
                "unit": "mg/kg/min",
                "interpretation": "Infusion parameters: 18.0 mL/hr of D10W (10.0% dextrose) in 3.0 kg patient. Calculated GIR: 6.00 mg/kg/min. Verification (simplified formula): 6.00 mg/kg/min. GIR 4.0-8.0 mg/kg/min represents normal glucose utilization rate. This range covers baseline glucose needs and is appropriate for maintaining euglycemia in most neonates and infants receiving IV fluids without enteral nutrition. Recommendations: Continue current regimen with routine glucose monitoring every 4-6 hours. Appropriate for maintenance therapy in stable patients. Monitor for clinical signs of hypo- or hyperglycemia. Consider advancing to enteral feeds when clinically appropriate.",
                "stage": "Normal/Physiologic Range",
                "stage_description": "Appropriate glucose delivery"
            }
        }