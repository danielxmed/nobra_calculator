"""
Maternal-Fetal Hemorrhage Rh(D) Immune Globulin Dosage Router

Endpoint for calculating RhIG (RhoGAM) dosage for maternal-fetal hemorrhage prevention.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.hematology.maternal_fetal_hemorrhage_rhd_immune_globulin_dosage import (
    MaternalFetalHemorrhageRhdImmuneGlobulinDosageRequest,
    MaternalFetalHemorrhageRhdImmuneGlobulinDosageResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/maternal_fetal_hemorrhage_rhd_immune_globulin_dosage",
    response_model=MaternalFetalHemorrhageRhdImmuneGlobulinDosageResponse,
    summary="Calculate Maternal-Fetal Hemorrhage Rh(D) Immune Globulin Dosage",
    description="Calculates the appropriate amount of RhIG (RhoGAM) to administer to "
                "Rh-negative mothers following maternal-fetal hemorrhage to prevent "
                "hemolytic disease of the fetus and newborn (HDFN). This evidence-based "
                "calculator uses maternal blood volume and fetal cell percentage to determine "
                "the number of 300 μg RhIG vials required, applying standardized rounding "
                "rules and safety margins. Essential for preventing maternal anti-D antibody "
                "formation when Rh-negative mothers are exposed to Rh-positive fetal blood. "
                "The calculator accounts for different severities of maternal-fetal hemorrhage, "
                "from routine prophylaxis requiring 1 vial to massive hemorrhages requiring "
                "multiple vials and specialized management. Incorporates clinical assessment "
                "of hemorrhage severity, alloimmunization risk, and provides comprehensive "
                "management recommendations including timing of administration, follow-up "
                "testing requirements, and monitoring protocols. Based on AABB Technical "
                "Manual guidelines and ACOG recommendations for Rh D alloimmunization prevention.",
    response_description="The calculated RhIG dosage with hemorrhage severity assessment, clinical management recommendations, and comprehensive dosing rationale",
    operation_id="maternal_fetal_hemorrhage_rhd_immune_globulin_dosage"
)
async def calculate_maternal_fetal_hemorrhage_rhd_immune_globulin_dosage(request: MaternalFetalHemorrhageRhdImmuneGlobulinDosageRequest):
    """
    Calculates Maternal-Fetal Hemorrhage Rh(D) Immune Globulin Dosage
    
    The Maternal-Fetal Hemorrhage Rh(D) Immune Globulin Dosage calculator is a critical 
    clinical tool for preventing hemolytic disease of the fetus and newborn (HDFN) in 
    Rh-negative mothers exposed to Rh-positive fetal blood.
    
    **Clinical Background and Significance:**
    
    Maternal-fetal hemorrhage (MFH) occurs when fetal blood crosses the placental barrier 
    into the maternal circulation. In Rh-negative mothers carrying Rh-positive fetuses, 
    even small amounts of fetal blood (as little as 0.01-0.03 mL) can trigger maternal 
    alloimmunization, leading to the formation of anti-D antibodies. These antibodies 
    can cross the placenta in subsequent pregnancies and cause severe hemolytic anemia, 
    hydrops fetalis, and fetal death.
    
    **Calculation Methodology:**
    
    **Primary Formula:**
    Number of RhIG vials = (fetal cell percentage / 100) × maternal blood volume (mL) / 30 mL
    
    **Standard Parameters:**
    - **Vial Strength**: 300 μg per vial (standard dose)
    - **Protection Coverage**: Each vial protects against 30 mL fetal whole blood (15 mL fetal RBCs)
    - **Safety Margin**: Additional vial added for safety
    - **Minimum Dose**: 1 vial regardless of calculation
    
    **Rounding Rules (Critical for Safety):**
    1. If decimal portion <0.5: round up to next whole number
    2. If decimal portion ≥0.5: round up and add 1 additional vial
    3. Always add 1 safety margin vial
    4. Never give less than 1 vial
    
    **Input Parameters and Clinical Significance:**
    
    **1. Maternal Blood Volume (2,000-6,000 mL):**
    - **Typical Range**: 3,700-4,500 mL for average adult female
    - **Estimation Methods**:
      - Nadler's Formula: 0.3561 × height³(m) + 0.03308 × weight(kg) + 0.1833 L
      - Clinical estimation based on patient body habitus
      - Standard values: ~4,000 mL for average adult
    - **Clinical Impact**: Directly affects calculation of total fetal blood volume
    
    **2. Fetal Cell Percentage (0-10%):**
    - **Testing Methods**:
      - **Flow Cytometry**: More accurate, preferred method
      - **Kleihauer-Betke Test**: Traditional method, less precise
    - **Reference Ranges**:
      - Normal baseline: <0.1%
      - Clinical significance threshold: >0.3%
      - Moderate hemorrhage: 0.5-2.0%
      - Large hemorrhage: 2.0-5.0%
      - Massive hemorrhage: >5.0%
    - **Clinical Correlation**: Higher percentages indicate more severe hemorrhage
    
    **Hemorrhage Severity Categories and Management:**
    
    **Standard Dose (1 vial, 300 μg):**
    - **Indication**: Minimal maternal-fetal hemorrhage, routine prophylaxis
    - **Coverage**: Protects against up to 30 mL fetal blood exposure
    - **Management**: Standard postpartum prophylaxis protocol
    - **Timing**: Within 72 hours of delivery or hemorrhage event
    - **Follow-up**: Routine obstetric care, monitor in subsequent pregnancies
    
    **Moderate Hemorrhage (2-3 vials, 600-900 μg):**
    - **Indication**: Moderate maternal-fetal hemorrhage
    - **Coverage**: 60-90 mL fetal blood protection
    - **Management**: Enhanced monitoring, consider follow-up testing
    - **Administration**: May require multiple injection sites
    - **Follow-up**: Kleihauer-Betke testing to confirm coverage adequacy
    
    **Large Hemorrhage (4-10 vials, 1,200-3,000 μg):**
    - **Indication**: Significant maternal-fetal hemorrhage
    - **Coverage**: 120-300 mL fetal blood protection
    - **Management**: Obstetric consultation required
    - **Monitoring**: Intensive follow-up, serial testing
    - **Considerations**: Consider hematology consultation
    
    **Massive Hemorrhage (>10 vials, >3,000 μg):**
    - **Indication**: Rare but life-threatening hemorrhage
    - **Coverage**: >300 mL fetal blood protection
    - **Management**: Emergency obstetric and hematology consultation
    - **Administration**: Consider intravenous RhIG if available
    - **Protocols**: May require exchange transfusion consideration
    - **Monitoring**: ICU-level monitoring, frequent laboratory assessment
    
    **Clinical Applications and Indications:**
    
    **Routine Prophylaxis:**
    - Postpartum administration in Rh-negative mothers
    - 28-week antepartum prophylaxis
    - Following therapeutic or spontaneous abortion
    - After ectopic pregnancy management
    
    **Obstetric Procedures:**
    - Amniocentesis, chorionic villus sampling
    - Cordocentesis, fetal blood sampling
    - External cephalic version
    - Fetal surgery or invasive procedures
    
    **Hemorrhage Events:**
    - Antepartum bleeding (placenta previa, abruption)
    - Third-trimester bleeding episodes
    - Abdominal trauma during pregnancy
    - Unexplained fetal anemia or hydrops
    
    **Laboratory Testing and Monitoring:**
    
    **Initial Assessment:**
    - Maternal and fetal Rh typing
    - Maternal antibody screen (indirect Coombs test)
    - Kleihauer-Betke test or flow cytometry
    - Complete blood count with differential
    
    **Follow-up Testing:**
    - Repeat Kleihauer-Betke at 24-48 hours post-administration
    - Maternal antibody screen at 6 months postpartum
    - Monitoring in subsequent pregnancies
    - Assessment of anti-D suppression adequacy
    
    **Timing and Administration Considerations:**
    
    **Optimal Timing:**
    - **Best**: Within 72 hours of exposure
    - **Acceptable**: Up to 28 days post-exposure (reduced efficacy)
    - **Emergency**: Immediate administration for massive hemorrhage
    
    **Administration Routes:**
    - **Standard**: Intramuscular injection (deltoid or gluteal)
    - **Large Doses**: Multiple injection sites may be required
    - **Massive Doses**: Consider intravenous administration if available
    
    **Contraindications and Precautions:**
    
    **Absolute Contraindications:**
    - Known severe allergic reaction to human immunoglobulin
    - Rh-positive mother (no indication for treatment)
    - Pre-existing anti-D antibodies (treatment ineffective)
    
    **Relative Contraindications:**
    - IgA deficiency with anti-IgA antibodies
    - Severe thrombocytopenia
    - Coagulation disorders
    
    **Special Populations and Considerations:**
    
    **High-Risk Pregnancies:**
    - Multiple gestations (increased risk of MFH)
    - Placental abnormalities (increased bleeding risk)
    - Fetal growth restriction (potential for increased surveillance)
    
    **Massive Hemorrhage Management:**
    - Multidisciplinary team approach
    - Consider plasma exchange in extreme cases
    - Monitor for volume overload with large doses
    - Assess need for additional blood products
    
    **Quality Assurance and Documentation:**
    
    **Essential Documentation:**
    - Maternal and fetal Rh status verification
    - Indication for RhIG administration
    - Kleihauer-Betke or flow cytometry results
    - Calculation methodology and dose rationale
    - Time of hemorrhage and time of administration
    
    **Quality Checks:**
    - Verify absence of existing anti-D antibodies
    - Confirm appropriate storage and handling
    - Document lot number and expiration date
    - Ensure proper administration technique
    
    **Outcome Monitoring:**
    - Track efficacy of alloimmunization prevention
    - Monitor for adverse reactions
    - Assess need for additional doses
    - Follow-up in subsequent pregnancies
    
    **Recent Developments and Future Directions:**
    
    **Advanced Testing Methods:**
    - Cell-free fetal DNA for non-invasive Rh typing
    - Quantitative flow cytometry improvements
    - Point-of-care testing development
    
    **Dosing Refinements:**
    - Population-specific dosing algorithms
    - Weight-based dosing considerations
    - Personalized medicine approaches
    
    **Clinical Outcomes Research:**
    - Long-term efficacy studies
    - Cost-effectiveness analyses
    - Optimal timing studies
    - Massive hemorrhage management protocols
    
    **References:**
    1. AABB Technical Manual, 18th edition. American Association of Blood Banks; 2014.
    2. American College of Obstetricians and Gynecologists. Prevention of Rh D 
       alloimmunization. ACOG Practice Bulletin No. 4. Washington, DC: American 
       College of Obstetricians and Gynecologists; 1999.
    3. Bowman JM. The prevention of Rh immunization. Transfus Med Rev. 1988;2(3):129-50.
    4. Queenan JT, Tomai TP, Ural SH, King JC. Deviation in amniotic fluid optical 
       density at a wavelength of 450 nm in Rh-immunized pregnancies from 14 to 40 
       weeks' gestation: a proposal for clinical management. Am J Obstet Gynecol. 
       1993;168(5):1370-6.
    
    Args:
        request: Maternal blood volume and fetal cell percentage parameters
        
    Returns:
        MaternalFetalHemorrhageRhdImmuneGlobulinDosageResponse: Calculated RhIG dosage with 
        comprehensive clinical assessment, management recommendations, and monitoring guidance
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("maternal_fetal_hemorrhage_rhd_immune_globulin_dosage", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Maternal-Fetal Hemorrhage Rh(D) Immune Globulin Dosage",
                    "details": {"parameters": parameters}
                }
            )
        
        return MaternalFetalHemorrhageRhdImmuneGlobulinDosageResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Maternal-Fetal Hemorrhage Rh(D) Immune Globulin Dosage",
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