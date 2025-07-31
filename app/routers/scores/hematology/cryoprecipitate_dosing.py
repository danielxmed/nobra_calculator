"""
Cryoprecipitate Dosing for Fibrinogen Replacement Router

Endpoint for calculating cryoprecipitate dosing requirements.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.hematology.cryoprecipitate_dosing import (
    CryoprecipitateDosIngRequest,
    CryoprecipitateDosingResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/cryoprecipitate_dosing",
    response_model=CryoprecipitateDosingResponse,
    summary="Calculate Cryoprecipitate Dosing for Fibrinogen Replacement",
    description="Calculates the required dose of cryoprecipitate units needed to achieve target fibrinogen levels in patients with fibrinogen deficiency or hypofibrinogenemia",
    response_description="The calculated cryoprecipitate dosing with interpretation",
    operation_id="calculate_cryoprecipitate_dosing"
)
async def calculate_cryoprecipitate_dosing(request: CryoprecipitateDosIngRequest):
    """
    Calculates Cryoprecipitate Dosing for Fibrinogen Replacement
    
    This calculator determines the required dose of cryoprecipitate units needed to 
    achieve target fibrinogen levels in patients with hypofibrinogenemia. It provides 
    evidence-based dosing recommendations based on validated formulas and clinical 
    guidelines from major blood banking organizations.
    
    **Clinical Background:**
    
    Cryoprecipitate is a blood component concentrate rich in fibrinogen, factor VIII, 
    factor XIII, von Willebrand factor, and fibronectin. It is the treatment of choice 
    for fibrinogen replacement in patients with congenital or acquired hypofibrinogenemia. 
    Accurate dosing is essential to achieve hemostatic fibrinogen levels while avoiding 
    unnecessary transfusion exposure and potential complications.
    
    **Calculation Methodology:**
    
    The calculator uses the validated formula:
    **Required Units = (Target Fibrinogen - Current Fibrinogen) × Plasma Volume / Fibrinogen per Unit**
    
    **Plasma Volume Calculation:**
    - Plasma Volume (dL) = Weight (kg) × Factor × (1 - Hematocrit)
    - Male factor: 0.07, Female factor: 0.065
    - Based on physiological differences in plasma distribution
    
    **Key Parameters:**
    
    **Patient Weight**: Essential for plasma volume calculation. Range: 1-300 kg.
    
    **Patient Sex**: Determines plasma volume factor (males 0.07, females 0.065).
    
    **Hematocrit**: Current hematocrit as decimal (e.g., 0.40 for 40%). Used to 
    calculate plasma volume from total blood volume. Range: 15-65%.
    
    **Current Fibrinogen**: Baseline fibrinogen level in mg/dL. Critical threshold 
    <50 mg/dL requires urgent replacement. Normal range: 200-400 mg/dL.
    
    **Target Fibrinogen**: Desired fibrinogen level in mg/dL. Standard targets:
    - 150 mg/dL: Adequate hemostasis for most procedures
    - 200 mg/dL: Major bleeding, surgery, or trauma
    - 250-300 mg/dL: Complex cardiac surgery or severe bleeding
    
    **Fibrinogen per Unit**: Content per cryoprecipitate unit (150-300 mg, default 200 mg).
    Varies by blood bank preparation method and donor characteristics.
    
    **Clinical Indications:**
    
    **Congenital Disorders:**
    - Afibrinogenemia (complete absence of fibrinogen)
    - Hypofibrinogenemia (reduced fibrinogen levels)
    - Dysfibrinogenemia (functionally abnormal fibrinogen)
    
    **Acquired Conditions:**
    - Liver disease with synthetic dysfunction
    - Disseminated intravascular coagulation (DIC)
    - Massive bleeding with consumption coagulopathy
    - Postpartum hemorrhage with hypofibrinogenemia
    - Trauma-induced coagulopathy
    - Drug-induced fibrinogen depletion (L-asparaginase)
    
    **Dosing Categories and Management:**
    
    **Low Dose (1-5 units):**
    - Small fibrinogen replacement
    - Monitor response with repeat levels at 1-2 hours
    - Suitable for mild deficiency or maintenance therapy
    
    **Standard Dose (6-15 units):**
    - Typical therapeutic replacement
    - Consider pooled units (typically 10 units per pool)
    - Expected increase: 60-100 mg/dL
    - Standard monitoring protocols apply
    
    **High Dose (16-30 units):**
    - Large fibrinogen replacement required
    - Consider fibrinogen concentrate for more efficient administration
    - Monitor for volume overload in cardiac/renal patients
    - Enhanced bleeding monitoring protocols
    
    **Very High Dose (>30 units):**
    - Massive replacement requirement
    - Strongly consider fibrinogen concentrate instead
    - Ensure adequate vascular access (large bore IV)
    - Very close monitoring for complications
    - Multidisciplinary team approach recommended
    
    **Administration Guidelines:**
    
    **Preparation:**
    - Thaw cryoprecipitate at 37°C water bath
    - Use within 4 hours of thawing
    - Pool units when possible for efficiency
    - Ensure ABO compatibility when available
    
    **Transfusion:**
    - Each unit volume: approximately 15-20 mL
    - Transfuse through standard blood filter
    - Rate: as rapidly as clinically indicated
    - Monitor for transfusion reactions
    
    **Monitoring:**
    - Baseline coagulation studies (PT, aPTT, fibrinogen)
    - Repeat fibrinogen 1-2 hours post-transfusion
    - Assess clinical hemostasis
    - Monitor for volume overload in large doses
    
    **Alternative Therapies:**
    
    **Fibrinogen Concentrate:**
    - Virally inactivated plasma-derived concentrate
    - More concentrated than cryoprecipitate (1g/vial typical)
    - Preferred for large dose requirements
    - Reduced volume load and infection risk
    - More expensive but increased safety profile
    
    **Fresh Frozen Plasma:**
    - Contains fibrinogen but much lower concentration
    - Requires large volumes for fibrinogen replacement
    - Risk of volume overload and dilution
    - Generally not recommended for isolated fibrinogen deficiency
    
    **Contraindications and Precautions:**
    
    **Absolute Contraindications:**
    - Known severe allergic reaction to plasma products
    - Religious or personal objection to blood products
    
    **Relative Contraindications:**
    - Significant volume restriction (consider concentrate)
    - History of transfusion-related acute lung injury (TRALI)
    - Multiple previous transfusion reactions
    
    **Special Considerations:**
    
    **Pediatric Patients:**
    - Weight-based dosing more reliable
    - Smaller volumes per unit may be beneficial
    - Consider splitting pooled units
    
    **Cardiac Surgery:**
    - Higher target fibrinogen often needed (200-250 mg/dL)
    - Point-of-care testing for rapid results
    - Coordinate with perfusion and anesthesia teams
    
    **Obstetric Bleeding:**
    - Postpartum hemorrhage with hypofibrinogenemia
    - Target 200 mg/dL for adequate hemostasis
    - Consider urgent replacement if <100 mg/dL
    
    **Quality Assurance:**
    
    **Documentation:**
    - Indication for transfusion
    - Pre- and post-transfusion fibrinogen levels
    - Clinical response to therapy
    - Any adverse reactions
    
    **Outcome Monitoring:**
    - Hemostatic effectiveness
    - Increment achieved per unit transfused
    - Need for repeat dosing
    - Overall clinical improvement
    
    **Evidence Base:**
    
    The calculator uses formulas validated in multiple studies and incorporated 
    into international guidelines. Dosing recommendations are based on:
    - American Association of Blood Banks (AABB) standards
    - British Committee for Standards in Haematology guidelines
    - European guidelines for perioperative bleeding management
    - International consensus statements on massive transfusion
    
    **References:**
    - American Association of Blood Banks (AABB). Technical Manual, 20th Edition. 2020.
    - British Committee for Standards in Haematology. Guidelines for cryoprecipitate use. Br J Haematol. 2004.
    - American Red Cross. Circular of Information for Human Blood Components. 2017.
    
    Args:
        request: Cryoprecipitate dosing parameters including patient demographics, 
                hematocrit, current and target fibrinogen levels, and optional 
                fibrinogen content per unit
        
    Returns:
        CryoprecipitateDosing Response: Calculated dose with detailed breakdown, 
        clinical considerations, alternative dosing methods, and administration 
        recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("cryoprecipitate_dosing", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Cryoprecipitate Dosing for Fibrinogen Replacement",
                    "details": {"parameters": parameters}
                }
            )
        
        return CryoprecipitateDosingResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Cryoprecipitate Dosing for Fibrinogen Replacement",
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