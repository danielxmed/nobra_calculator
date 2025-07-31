"""
Corrected Count Increment (CCI) for Platelet Transfusion Router

Endpoint for calculating CCI platelet transfusion response assessment.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.hematology.corrected_count_increment import (
    CorrectedCountIncrementRequest,
    CorrectedCountIncrementResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/corrected_count_increment",
    response_model=CorrectedCountIncrementResponse,
    summary="Calculate Corrected Count Increment",
    description="Assesses adequacy of response to platelet transfusion by measuring the expected increase in platelets adjusted for patient size and platelet dose",
    response_description="The calculated corrected count increment with interpretation",
    operation_id="calculate_corrected_count_increment"
)
async def calculate_corrected_count_increment(request: CorrectedCountIncrementRequest):
    """
    Calculates Corrected Count Increment (CCI) for Platelet Transfusion
    
    The Corrected Count Increment (CCI) is a standardized measure used to assess the adequacy 
    of response to platelet transfusion. It quantifies the expected increase in platelet count 
    following transfusion, adjusted for patient body surface area and the number of platelets 
    transfused, providing an objective assessment of platelet transfusion effectiveness.
    
    **Clinical Background and Significance**:
    
    **Platelet Transfusion Assessment Framework**:
    - Primary tool for evaluating platelet transfusion effectiveness in clinical practice
    - Standardized measure allowing comparison across patients of different sizes and platelet doses
    - Essential for identifying platelet refractoriness and guiding transfusion strategies
    - Widely used quality assurance metric in transfusion medicine services
    - Critical component of evidence-based transfusion practice protocols
    
    **Formula and Calculation Methodology**:
    - CCI = (Count Increment × Body Surface Area) / Platelet Dose
    - Count Increment = Post-transfusion count - Pre-transfusion count
    - Body Surface Area calculated using DuBois formula: sqrt((height_cm × weight_kg) / 3600)
    - Platelet Dose = Total platelet content in transfused units (×10¹¹ platelets)
    - Results expressed in platelets/μL/m²/(×10¹¹ platelets)
    
    **Clinical Interpretation Framework**:
    
    **Time-Dependent Assessment Thresholds**:
    
    **1-Hour Post-Transfusion Assessment (Standard Practice)**:
    - **CCI >7,500**: Successful transfusion with adequate immediate platelet response
    - **CCI ≤7,500**: Poor response requiring evaluation for platelet refractoriness
    - **Clinical Significance**: Optimal timing for routine assessment of transfusion effectiveness
    - **Practical Application**: Most commonly used timepoint in clinical practice
    - **Interpretation**: Reflects immediate platelet increment and early survival
    
    **20-Hour Post-Transfusion Assessment (Extended Evaluation)**:
    - **CCI >4,800**: Successful transfusion with adequate platelet survival
    - **CCI ≤4,800**: Poor survival requiring evaluation for underlying causes
    - **Clinical Significance**: Better assessment of longer-term platelet viability
    - **Research Application**: Valuable for detailed transfusion outcome studies
    - **Interpretation**: Reflects platelet survival and continued hemostatic function
    
    **Platelet Refractoriness Evaluation and Management**:
    
    **Definition and Diagnostic Criteria**:
    Platelet refractoriness is defined as the failure to achieve an acceptable platelet 
    count increment following platelet transfusion on at least two consecutive occasions, 
    in the absence of other identifiable causes of poor response.
    
    **Immune Causes of Refractoriness**:
    - **HLA Alloimmunization**: Most common cause requiring HLA-matched platelets
    - **Platelet-Specific Antibodies**: Target platelet surface antigens
    - **ABO Incompatibility**: May reduce transfusion effectiveness
    - **Previous Sensitization**: History of pregnancy or transfusion increases risk
    
    **Non-Immune Causes of Poor Response**:
    - **Fever and Sepsis**: Increase platelet consumption and reduce survival
    - **Splenomegaly**: Causes platelet sequestration and rapid clearance
    - **DIC and Active Bleeding**: Increase platelet consumption rates
    - **Drug Interactions**: Medications like amphotericin B, vancomycin, heparin
    - **Massive Transfusion**: Dilutional effects and consumption coagulopathy
    
    **Clinical Management Strategies**:
    
    **Successful Transfusion Response (CCI Above Threshold)**:
    
    **Immediate Actions**:
    - Continue current platelet transfusion protocols and strategies
    - Monitor platelet counts according to standard clinical guidelines
    - Document successful response for future transfusion planning
    - Consider optimizing transfusion intervals based on response duration
    
    **Follow-up Monitoring**:
    - Routine platelet count monitoring as clinically indicated
    - Assess for development of refractoriness in future transfusions
    - Track transfusion requirements and bleeding episodes
    - Maintain documentation of successful response patterns
    
    **Quality Assurance Applications**:
    - Use data to assess transfusion service effectiveness
    - Monitor platelet product quality and storage practices
    - Contribute to institutional transfusion outcome metrics
    - Support evidence-based inventory management decisions
    
    **Poor Transfusion Response (CCI At or Below Threshold)**:
    
    **Immediate Assessment and Verification**:
    - Verify accuracy of platelet counts and timing of blood collection
    - Review patient's clinical status for active bleeding or consumption
    - Assess for fever, infection, or other acute conditions affecting platelet survival
    - Evaluate concurrent medications that may interfere with platelet function
    
    **Refractoriness Investigation Protocol**:
    - Obtain HLA typing and antibody screening for immune causes
    - Perform platelet crossmatching to identify compatible units
    - Screen for platelet-specific antibodies (HPA-1a, HPA-5b, etc.)
    - Evaluate patient history for previous sensitizing events
    
    **Alternative Transfusion Strategies**:
    - **HLA-Matched Platelets**: For patients with HLA antibodies
    - **Platelet Crossmatched Units**: When HLA matching unavailable
    - **Fresh Platelets**: Units stored <3 days may have improved function
    - **Alternative Donors**: Consider single-donor apheresis products
    
    **Non-Transfusion Management Options**:
    - **Bleeding Management**: Direct pressure, topical hemostatics, antifibrinolytics
    - **Platelet Function Enhancement**: Desmopressin, recombinant factor VIIa
    - **Supportive Care**: Minimize invasive procedures, optimize coagulation factors
    - **Underlying Condition Treatment**: Address sepsis, DIC, or other consumptive processes
    
    **Technical and Quality Considerations**:
    
    **Data Collection Standards**:
    - Use standardized timing protocols for blood collection
    - Ensure accurate documentation of platelet unit content
    - Verify patient anthropometric measurements for BSA calculation
    - Document any clinical factors that may affect interpretation
    
    **Laboratory Quality Assurance**:
    - Use consistent platelet counting methodology across samples
    - Ensure proper sample handling and processing protocols
    - Maintain calibration and quality control of automated counters
    - Document any technical factors affecting platelet count accuracy
    
    **Clinical Documentation Requirements**:
    - Record CCI values in patient medical records
    - Document timing and circumstances of transfusion and sampling
    - Note any confounding factors (fever, bleeding, medications)
    - Track trends across multiple transfusions for pattern recognition
    
    **Research and Quality Improvement Applications**:
    
    **Clinical Research Utilization**:
    - Compare effectiveness of different platelet products and storage methods
    - Evaluate impact of new transfusion protocols and guidelines
    - Assess outcomes in specific patient populations (oncology, cardiac surgery)
    - Study factors affecting platelet transfusion effectiveness
    
    **Quality Improvement Programs**:
    - Monitor institutional transfusion effectiveness metrics
    - Identify opportunities for practice improvement and standardization
    - Assess cost-effectiveness of different transfusion strategies
    - Support evidence-based inventory management and product selection
    
    **Population Health Analysis**:
    - Track refractoriness rates across different patient populations
    - Identify risk factors for poor transfusion response
    - Guide resource allocation and specialized service development
    - Support development of personalized transfusion strategies
    
    **Limitations and Clinical Context**:
    
    **Assessment Limitations**:
    - CCI measures count increment only, not platelet function or hemostatic effectiveness
    - Normal CCI does not guarantee bleeding cessation or hemostatic adequacy
    - May be affected by concurrent medical conditions unrelated to platelet quality
    - Limited utility during active bleeding episodes or hemodynamic instability
    
    **Patient-Specific Considerations**:
    - Consider individual bleeding risk assessment and clinical presentation
    - Account for concurrent anticoagulant or antiplatelet medications
    - Evaluate patient's overall prognosis and treatment goals
    - Balance transfusion benefits against potential risks and complications
    
    **Integration with Clinical Practice**:
    - Use CCI as part of comprehensive hemostatic assessment
    - Combine with clinical bleeding assessment and other laboratory parameters
    - Consider trends over time rather than relying on single measurements
    - Integrate findings with patient's overall clinical condition and treatment plan
    
    This calculator provides a standardized, evidence-based approach to assessing platelet 
    transfusion effectiveness, supporting optimal patient care and transfusion medicine practice 
    through objective measurement and clinical decision-making guidance.
    
    Args:
        request: CCI assessment parameters including platelet counts, timing, patient size, and platelet dose
        
    Returns:
        CorrectedCountIncrementResponse: Comprehensive platelet transfusion effectiveness assessment with clinical interpretation
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("corrected_count_increment", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Corrected Count Increment (CCI)",
                    "details": {"parameters": parameters}
                }
            )
        
        return CorrectedCountIncrementResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for CCI calculation",
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