"""
Maximum Allowable Blood Loss (ABL) Without Transfusion Router

Endpoint for calculating maximum allowable blood loss during surgery before transfusion.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.hematology.maximum_allowable_blood_loss_without_transfusion import (
    MaximumAllowableBloodLossWithoutTransfusionRequest,
    MaximumAllowableBloodLossWithoutTransfusionResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/maximum_allowable_blood_loss_without_transfusion",
    response_model=MaximumAllowableBloodLossWithoutTransfusionResponse,
    summary="Calculate Maximum Allowable Blood Loss (ABL) Without Transfusion",
    description="Calculates the maximum allowable blood loss during surgery before "
                "transfusion should be considered using the Gross formula. This essential "
                "perioperative tool helps anesthesiologists and surgeons make evidence-based "
                "decisions about blood transfusion timing and guide intraoperative blood "
                "management strategies. The calculator uses patient age group, body weight, "
                "initial hemoglobin, and acceptable final hemoglobin to estimate blood loss "
                "tolerance using established blood volume coefficients. Developed by Jeffrey "
                "Gross in 1983, this calculation provides objective guidance for transfusion "
                "decisions while accounting for individual patient factors including age-specific "
                "blood volume differences, baseline hemoglobin levels, and clinical transfusion "
                "thresholds. The tool is particularly valuable for procedures with anticipated "
                "significant blood loss, helping optimize patient safety through appropriate "
                "blood conservation strategies and timely transfusion decisions. Results include "
                "comprehensive clinical assessment, risk stratification, monitoring recommendations, "
                "and accuracy limitations to ensure appropriate clinical application.",
    response_description="The calculated maximum allowable blood loss with clinical assessment, risk stratification, and comprehensive management recommendations",
    operation_id="maximum_allowable_blood_loss_without_transfusion"
)
async def calculate_maximum_allowable_blood_loss_without_transfusion(request: MaximumAllowableBloodLossWithoutTransfusionRequest):
    """
    Calculates Maximum Allowable Blood Loss (ABL) Without Transfusion
    
    The Maximum Allowable Blood Loss (ABL) calculator is a critical perioperative tool 
    that provides evidence-based guidance for transfusion decisions during surgery by 
    estimating the maximum volume of blood loss a patient can tolerate before transfusion 
    becomes necessary.
    
    **Historical Development and Validation:**
    
    Developed by Jeffrey Gross in 1983, this calculator emerged from the need for 
    objective, mathematical guidance in perioperative blood management. The Gross 
    formula was derived through mathematical modeling of blood volume dilution and 
    hemoglobin changes during controlled blood loss scenarios. This tool has become 
    a standard component of anesthesia practice worldwide, particularly valuable in 
    an era of increasingly restrictive transfusion practices and emphasis on patient 
    blood management.
    
    **Mathematical Foundation - The Gross Formula:**
    
    **Primary Formula**: ABL = [EBV × (Hi - Hf)] / Hav
    
    **Component Calculations**:
    - **EBV (Estimated Blood Volume)**: Body weight (kg) × Blood volume coefficient (mL/kg)
    - **Hi (Initial Hemoglobin)**: Preoperative hemoglobin level (g/dL)
    - **Hf (Final Hemoglobin)**: Lowest acceptable hemoglobin before transfusion (g/dL)
    - **Hav (Average Hemoglobin)**: (Hi + Hf) / 2
    
    **Blood Volume Coefficients by Age Group:**
    
    These coefficients reflect physiological differences in blood volume distribution 
    across different patient populations:
    
    **Adult Male (75 mL/kg):**
    - Highest coefficient due to greater muscle mass and larger frame
    - Reflects lower percentage of body fat compared to females
    - Accounts for higher baseline hemoglobin levels
    - Suitable for males ≥18 years of age
    
    **Adult Female (65 mL/kg):**
    - Lower than males due to body composition differences
    - Accounts for higher percentage of adipose tissue
    - Reflects hormonal influences on blood volume regulation
    - Suitable for females ≥18 years of age
    
    **Infant (80 mL/kg) - Ages 1 month to 2 years:**
    - Higher relative blood volume to support rapid growth
    - Accounts for higher metabolic demands per unit body weight
    - Reflects immature cardiovascular compensatory mechanisms
    - Critical for procedures in this vulnerable population
    
    **Neonate (85 mL/kg) - Birth to 1 month:**
    - High relative blood volume for organ development
    - Accounts for transition from fetal to adult circulation
    - Reflects limited physiological reserves
    - Essential for neonatal surgical procedures
    
    **Premature Neonate (96 mL/kg) - <37 weeks gestation:**
    - Highest coefficient reflecting developmental immaturity
    - Accounts for incomplete cardiovascular development
    - Critical for this extremely vulnerable population
    - Even small blood losses can be life-threatening
    
    **Clinical Parameters and Interpretation:**
    
    **Body Weight Considerations (0.5-200 kg):**
    - Direct multiplier for blood volume calculation
    - Particularly critical in pediatric patients where small changes matter
    - Must be current and accurate for reliable calculations
    - Consider recent weight changes due to illness or fluid status
    
    **Initial Hemoglobin Assessment (3.0-25.0 g/dL):**
    - **Normal Ranges**:
      - Adult males: 13.5-17.5 g/dL
      - Adult females: 12.0-15.5 g/dL
      - Children: 11.0-15.0 g/dL
      - Neonates: 14.0-20.0 g/dL
    - **Clinical Significance**: Higher initial levels provide greater blood loss tolerance
    - **Optimization**: Consider preoperative iron therapy for low levels
    
    **Final Hemoglobin Thresholds (3.0-15.0 g/dL):**
    - **Universal Threshold**: <6 g/dL almost always requires transfusion
    - **Standard Patients**: 7-8 g/dL typical threshold
    - **Cardiac Patients**: 8-10 g/dL may be appropriate
    - **Critical Care**: 7-9 g/dL commonly used
    - **Healthy Young Patients**: 6-7 g/dL may be acceptable
    
    **Clinical Applications and Use Cases:**
    
    **Preoperative Planning:**
    - Calculate ABL for all procedures with anticipated blood loss >500 mL
    - Guide decision for preoperative autologous blood donation
    - Inform consent discussions about transfusion probability
    - Plan intraoperative monitoring intensity and frequency
    - Determine need for preoperative hematologic optimization
    
    **Intraoperative Management:**
    - Real-time reference for transfusion decision-making
    - Guide timing of hemoglobin monitoring
    - Inform decisions about blood conservation techniques
    - Provide objective framework for clinical judgment
    - Support communication among surgical team members
    
    **Procedure-Specific Applications:**
    
    **Orthopedic Surgery:**
    - Hip and knee replacements with predictable blood loss
    - Spine surgery with variable bleeding patterns
    - Trauma surgery with unpredictable blood loss
    - Pediatric orthopedic procedures requiring precision
    
    **Cardiac Surgery:**
    - Cardiopulmonary bypass procedures
    - Valve replacement surgeries
    - Coronary artery bypass grafting
    - Congenital heart disease repairs
    
    **General Surgery:**
    - Major hepatic resections
    - Extensive cancer surgeries
    - Trauma laparotomy procedures
    - Transplant surgeries
    
    **Obstetric Surgery:**
    - Cesarean sections with complications
    - Postpartum hemorrhage management
    - Placenta accreta procedures
    - Peripartum hysterectomy
    
    **Blood Conservation Strategies:**
    
    **When ABL is Low (<500 mL):**
    - Meticulous surgical hemostasis essential
    - Consider preoperative autologous donation
    - Implement acute normovolemic hemodilution
    - Use antifibrinolytic agents (tranexamic acid)
    - Apply topical hemostatic agents liberally
    - Consider staged procedures if feasible
    
    **When ABL is Moderate (500-1500 mL):**
    - Standard blood conservation measures
    - Intraoperative cell salvage when appropriate
    - Controlled hypotension if indicated
    - Optimize coagulation status preoperatively
    - Use blood-sparing surgical techniques
    
    **When ABL is High (>1500 mL):**
    - Full range of conservation techniques available
    - Consider preoperative phlebotomy with hemodilution
    - Aggressive cell salvage protocols
    - Multiple autologous donation sessions
    - Advanced hemostatic techniques
    
    **Monitoring and Assessment Protocols:**
    
    **Continuous Monitoring:**
    - Heart rate, blood pressure, and cardiac output
    - Central venous pressure when indicated
    - Urine output as indicator of perfusion
    - Oxygen saturation and end-tidal CO2
    - Temperature and metabolic parameters
    
    **Laboratory Monitoring:**
    - **Hemoglobin/Hematocrit**: Every 1-2 hours during active bleeding
    - **Arterial Blood Gas**: For oxygen delivery assessment
    - **Coagulation Studies**: PT/INR, aPTT, fibrinogen, platelet count
    - **Comprehensive Metabolic Panel**: Electrolytes, renal function
    - **Lactate Levels**: Indicator of tissue perfusion adequacy
    
    **Clinical Assessment Parameters:**
    - **Hemodynamic Stability**: Response to fluid resuscitation
    - **Oxygen Delivery**: Tissue perfusion indicators
    - **Functional Capacity**: Exercise tolerance if assessable
    - **Symptoms**: Fatigue, dyspnea, chest pain, dizziness
    - **End-Organ Function**: Renal, cardiac, neurologic status
    
    **Limitations and Important Considerations:**
    
    **Mathematical Limitations:**
    - **20% Rule**: Calculation becomes unreliable when blood loss >20% of EBV
    - **Steady-State Assumption**: Formula assumes gradual, controlled blood loss
    - **Dilution Effects**: May not account for crystalloid/colloid administration
    - **Individual Variation**: Does not account for patient-specific factors
    
    **Clinical Limitations:**
    - **Cardiac Function**: Does not consider cardiac reserve or dysfunction
    - **Pulmonary Status**: Ignores respiratory compromise or lung disease  
    - **Metabolic Demands**: Does not account for fever, infection, or stress
    - **Coagulation**: Assumes normal hemostatic function
    - **Ongoing Losses**: May not apply to continued active bleeding
    
    **Risk Factors for Earlier Transfusion:**
    - **Cardiovascular Disease**: Coronary artery disease, heart failure
    - **Pulmonary Disease**: COPD, pulmonary hypertension
    - **Renal Dysfunction**: Chronic kidney disease, dialysis dependence
    - **Advanced Age**: Reduced physiologic reserve
    - **Active Bleeding**: Ongoing hemorrhage beyond surgical site
    
    **Special Populations and Considerations:**
    
    **Pediatric Patients:**
    - Small absolute blood volumes make precision critical
    - Higher blood volume coefficients reflect developmental physiology
    - Limited compensatory mechanisms compared to adults
    - Family preferences and religious considerations
    - Growth and development considerations
    
    **Elderly Patients:**
    - Reduced cardiovascular reserve and compensation
    - Multiple comorbidities affecting tolerance
    - Polypharmacy interactions with hemostasis
    - Higher risk of adverse outcomes from both anemia and transfusion
    - Cognitive considerations for consent and monitoring
    
    **Critically Ill Patients:**
    - Altered physiology and metabolism
    - Multiorgan dysfunction considerations
    - Inflammatory states affecting oxygen utilization
    - Fluid balance and volume status complexities
    - Concurrent therapies affecting calculation validity
    
    **Quality Assurance and Documentation:**
    
    **Essential Documentation:**
    - Preoperative ABL calculation with parameters used
    - Intraoperative blood loss estimation methods
    - Transfusion decisions and rationale
    - Patient response to blood loss and transfusion
    - Post-operative hemoglobin levels and clinical status
    
    **Quality Metrics:**
    - Accuracy of blood loss estimation compared to calculated ABL
    - Appropriateness of transfusion decisions
    - Patient outcomes including morbidity and mortality
    - Length of stay and recovery parameters
    - Transfusion-related complications or reactions
    
    **Institutional Protocols:**
    - Standardized calculation procedures
    - Clear triggers for calculation requirement
    - Communication protocols among team members
    - Regular review of outcomes and practices
    - Continuing education on appropriate use
    
    **Recent Developments and Future Directions:**
    
    **Enhanced Calculations:**
    - Integration with real-time hemodynamic monitoring
    - Artificial intelligence-assisted decision support
    - Population-specific refinements of blood volume coefficients
    - Dynamic adjustment based on ongoing clinical parameters
    
    **Technology Integration:**
    - Electronic health record integration
    - Mobile applications for point-of-care calculation
    - Integration with intraoperative monitoring systems
    - Real-time updates based on measured blood loss
    
    **Research Frontiers:**
    - Validation in specific surgical populations
    - Comparison with alternative calculation methods
    - Integration with newer transfusion triggers
    - Outcomes research on calculation-guided management
    
    **References:**
    1. Gross JB. Estimating allowable blood loss: corrected for dilution. 
       Anesthesiology. 1983 Mar;58(3):277-80. doi: 10.1097/00000542-198303000-00016.
    2. Miller RD, ed. Miller's Anesthesia. 8th ed. Philadelphia, PA: Elsevier Saunders; 2015.
    3. American Society of Anesthesiologists Task Force on Perioperative Blood Management. 
       Practice guidelines for perioperative blood management: an updated report by the 
       American Society of Anesthesiologists Task Force on Perioperative Blood Management. 
       Anesthesiology. 2015;122(2):241-75.
    4. Carson JL, Grossman BJ, Kleinman S, Tinmouth AT, Marques MB, Fung MK, et al. 
       Red blood cell transfusion: a clinical practice guideline from the AABB. 
       Ann Intern Med. 2012;157(1):49-58.
    
    Args:
        request: Patient parameters including age group, weight, initial and final hemoglobin
        
    Returns:
        MaximumAllowableBloodLossWithoutTransfusionResponse: Calculated ABL with comprehensive 
        clinical assessment, risk stratification, and management recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("maximum_allowable_blood_loss_without_transfusion", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Maximum Allowable Blood Loss Without Transfusion",
                    "details": {"parameters": parameters}
                }
            )
        
        return MaximumAllowableBloodLossWithoutTransfusionResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Maximum Allowable Blood Loss Without Transfusion",
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