"""
Blood Volume Calculation Router

Endpoint for calculating blood volumes using Nadler equations and age-specific formulas.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.hematology.blood_volume_calculation import (
    BloodVolumeCalculationRequest,
    BloodVolumeCalculationResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post("/blood_volume_calculation", response_model=BloodVolumeCalculationResponse)
async def calculate_blood_volume_calculation(request: BloodVolumeCalculationRequest):
    """
    Calculates Blood Volume Components Using Nadler Equations and Age-Specific Formulas
    
    This comprehensive blood volume calculator implements the gold standard methods 
    for estimating total blood volume, red blood cell volume, and plasma volume 
    across all age groups. The calculator uses validated equations established 
    through decades of clinical research and physiological studies.
    
    **Historical Foundation:**
    
    **Nadler's Landmark Study (1962):**
    The foundation of modern blood volume estimation was established by Nadler, 
    Hidalgo, and Bloch in their seminal 1962 study published in Surgery. Using 
    radioisotope labeling with ⁵¹Cr-labeled red blood cells and ¹³¹I-labeled 
    albumin, they measured actual blood volumes in 268 normal adults and derived 
    predictive equations based on sex, height, and weight.
    
    **Key Findings:**
    - Blood volume correlates strongly with body surface area and lean body mass
    - Sex-specific differences reflect body composition variations
    - Height provides better correlation than weight alone for larger individuals
    - Equations accurate within ±10% for 95% of normal adults
    
    **Clinical Validation:**
    These equations have been validated extensively in clinical practice and remain 
    the standard reference for blood volume estimation worldwide. They form the 
    basis for transfusion medicine protocols, plasma exchange procedures, and 
    research applications requiring accurate blood volume estimates.
    
    **Comprehensive Calculation Methods:**
    
    **1. Nadler Equations (Adults and Children ≥25 kg):**
    
    **Male Formula:**
    Total Blood Volume (L) = 0.3669 × (height in meters)³ + 0.03219 × (weight in kg) + 0.6041
    
    **Female Formula:**
    Total Blood Volume (L) = 0.3561 × (height in meters)³ + 0.03308 × (weight in kg) + 0.1833
    
    **Scientific Rationale:**
    - Height³ term accounts for three-dimensional body scaling
    - Weight term reflects lean body mass contribution
    - Sex-specific constants account for body composition differences
    - Results in liters, converted to mL for clinical use
    
    **Accuracy Considerations:**
    - Most accurate for normal-weight individuals
    - Less reliable in obesity due to altered body composition
    - Validated age range: 15-90 years
    - Assumes normal hydration status and absence of pathological states
    
    **2. Pediatric Weight-Based Calculations:**
    
    **Preterm Neonate (100 mL/kg):**
    
    **Physiological Basis:**
    - Higher relative blood volume due to immature cardiovascular regulation
    - Increased plasma volume relative to red cell mass
    - Compensates for smaller stroke volume and cardiac output
    
    **Clinical Applications:**
    - Exchange transfusion calculations for hyperbilirubinemia
    - Maximum blood sampling volume limits (typically <5% total blood volume)
    - Phototherapy and medication dosing considerations
    
    **Term Neonate (85 mL/kg):**
    
    **Physiological Basis:**
    - Represents transition from fetal to adult circulation patterns
    - Balanced plasma and red cell volume expansion
    - Stable cardiovascular adaptation to extrauterine life
    
    **Clinical Applications:**
    - Standard blood volume for healthy newborns
    - Transfusion volume calculations (typically 10-15 mL/kg)
    - Assessment of blood loss during delivery
    
    **Infant 1-4 Months (75 mL/kg):**
    
    **Physiological Basis:**
    - Rapid growth phase with changing body composition
    - Decreasing relative blood volume as body weight increases
    - Developing cardiovascular efficiency
    
    **Clinical Applications:**
    - Immunization-related blood sampling limits
    - Anemia assessment and treatment planning
    - Growth and development monitoring
    
    **Child <25 kg (70 mL/kg):**
    
    **Physiological Basis:**
    - Approaching adult proportional blood volume
    - Established cardiovascular regulatory mechanisms
    - Stable body composition ratios
    
    **Clinical Applications:**
    - Transfusion therapy for various conditions
    - Surgical blood loss assessment
    - Research protocol safety limits
    
    **Advanced Volume Calculations:**
    
    **Red Blood Cell Volume:**
    RBC Volume = Total Blood Volume × (Hematocrit ÷ 100)
    
    **Clinical Significance:**
    - Represents oxygen-carrying capacity
    - Guides transfusion decisions in anemia
    - Important for blood doping detection in athletics
    - Research applications in exercise physiology
    
    **Plasma Volume:**
    Plasma Volume = Total Blood Volume × (1 - Hematocrit ÷ 100)
    
    **Clinical Significance:**
    - Contains clotting factors, proteins, and electrolytes
    - Critical for plasma exchange planning
    - Guides fluid resuscitation in shock states
    - Important for pharmacokinetic calculations
    
    **Clinical Applications and Use Cases:**
    
    **Transfusion Medicine:**
    
    **Blood Product Dosing:**
    - RBC transfusion: 1 unit increases Hgb by ~1 g/dL in 70 kg adult
    - Platelet transfusion: 1 unit/10 kg body weight increases count by 50,000
    - Fresh frozen plasma: 10-15 mL/kg for coagulation factor replacement
    
    **Massive Transfusion Protocols:**
    - Definition: >1 blood volume replacement in 24 hours
    - Guides RBC:FFP:Platelet ratios (1:1:1 or 2:1:1)
    - Predicts coagulopathy development
    
    **Pediatric Transfusion:**
    - Maximum safe transfusion volumes: 10-15 mL/kg for RBCs
    - Exchange transfusion volumes: 1-2 times total blood volume
    - Blood sampling limits: <5% total blood volume per day
    
    **Therapeutic Procedures:**
    
    **Plasma Exchange (Plasmapheresis):**
    - Standard exchange volume: 1-1.5 times plasma volume
    - Frequency: Daily to every other day depending on condition
    - Replacement fluid calculations based on plasma volume
    
    **Therapeutic Phlebotomy:**
    - Polycythemia vera: Remove 450-500 mL (1 unit) initially
    - Maintenance: Adjust based on hematocrit and total blood volume
    - Hemochromatosis: Regular phlebotomy until iron depletion
    
    **Coagulation Factor Dosing:**
    - Factor VIII: 1 unit/kg increases level by 2% in normal plasma volume
    - Factor IX: 1 unit/kg increases level by 1% in normal plasma volume
    - DDAVP dosing based on plasma volume distribution
    
    **Research and Safety Applications:**
    
    **Clinical Trial Safety:**
    - Maximum blood sampling volumes for research
    - Pharmacokinetic study design parameters
    - Safety monitoring in pediatric research
    
    **Exercise Physiology:**
    - Blood doping detection through plasma volume changes
    - Altitude acclimatization studies
    - Dehydration and performance research
    
    **Physiological Research:**
    - Cardiovascular function studies
    - Fluid balance investigations
    - Metabolic research applications
    
    **Limitations and Considerations:**
    
    **Accuracy Limitations:**
    - Less accurate in obesity (BMI >30)
    - Reduced reliability in severe edema or dehydration
    - May overestimate in elderly patients due to body composition changes
    - Not validated in pregnancy (plasma volume increases 40-50%)
    
    **Clinical State Considerations:**
    - Acute blood loss: Use pre-loss estimates
    - Chronic anemia: May have expanded plasma volume
    - Heart failure: Altered distribution between intravascular and extravascular spaces
    - Renal disease: Variable fluid retention affects accuracy
    
    **Modern Developments:**
    - Enhanced accuracy with bioelectrical impedance analysis
    - Integration with body composition measurements
    - Ultrasound-based blood volume monitoring
    - Real-time blood volume measurement devices
    
    **Quality Assurance:**
    - Regular calibration of measuring devices
    - Standardized measurement techniques
    - Documentation of calculation methods used
    - Validation against clinical outcomes
    
    Args:
        request: Blood volume calculation parameters (category, weight, sex, height, hematocrit)
        
    Returns:
        BloodVolumeCalculationResponse: Calculated blood volumes with clinical interpretation
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("blood_volume_calculation", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Blood Volume",
                    "details": {"parameters": parameters}
                }
            )
        
        return BloodVolumeCalculationResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Blood Volume calculation",
                "details": {"error": str(e)}
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "error": "InternalServerError",
                "message": "Internal error in calculation",
                "details": {"error": str(e)}
            }
        )