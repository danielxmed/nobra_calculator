"""
Grogan Staging System for Transthyretin Amyloid Cardiomyopathy (ATTR-CM) Router

Endpoint for calculating Grogan staging for ATTR-CM prognosis.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.cardiology.grogan_staging_attr_cm import (
    GroganStagingAttrCmRequest,
    GroganStagingAttrCmResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/grogan_staging_attr_cm",
    response_model=GroganStagingAttrCmResponse,
    summary="Calculate Grogan Staging System for Transthyret...",
    description="Classifies prognosis of patients with wild-type transthyretin amyloid cardiomyopathy using cardiac biomarkers NT-proBNP and troponin T",
    response_description="The calculated grogan staging attr cm with interpretation",
    operation_id="grogan_staging_attr_cm"
)
async def calculate_grogan_staging_attr_cm(request: GroganStagingAttrCmRequest):
    """
    Calculates Grogan Staging System for Transthyretin Amyloid Cardiomyopathy (ATTR-CM)
    
    The Grogan Staging System is a validated prognostic tool developed at Mayo Clinic for 
    patients with wild-type transthyretin amyloid cardiomyopathy (ATTRwt-CM). This biomarker-based 
    staging system uses two key cardiac biomarkers to classify patients into three prognostic 
    categories, providing crucial information for treatment planning and prognostic discussions.
    
    **Clinical Background**:
    Transthyretin amyloid cardiomyopathy (ATTR-CM) is an underdiagnosed and potentially fatal 
    disease caused by deposition of misfolded transthyretin protein in the heart muscle. 
    Wild-type ATTR-CM typically affects elderly men, with median survival from diagnosis of 
    approximately 3.5-4 years in untreated patients. However, prognosis varies significantly 
    based on disease stage at presentation, making biomarker-based staging essential for 
    optimal clinical management.
    
    **Biomarker-Based Staging System**:
    The Grogan system uses two well-established cardiac biomarkers that reflect different 
    aspects of cardiac involvement in ATTR-CM:
    
    **NT-proBNP (N-terminal pro-B-type natriuretic peptide)**:
    - Threshold: 3000 pg/mL
    - Reflects hemodynamic stress and volume overload
    - Produced by ventricular cardiomyocytes in response to wall tension
    - Values >3000 pg/mL indicate worse prognosis
    
    **Troponin T (cardiac troponin T)**:
    - Threshold: 0.05 ng/mL
    - Reflects ongoing myocardial injury and cardiomyocyte death
    - Highly specific marker of cardiac muscle damage
    - Values >0.05 ng/mL indicate worse prognosis
    
    **Three-Stage Classification with Survival Outcomes**:
    
    **Stage I (Best Prognosis)**:
    - Criteria: Both biomarkers below thresholds (NT-proBNP ≤3000 AND Troponin T ≤0.05)
    - 4-year survival: 57%
    - Median survival: 66 months
    - Clinical approach: Early disease-modifying therapy, aggressive interventions, clinical trials
    
    **Stage II (Intermediate Prognosis)**:
    - Criteria: One biomarker above threshold (mixed elevation pattern)
    - 4-year survival: 42%
    - Median survival: 42 months
    - Clinical approach: Disease-modifying therapy indicated, multidisciplinary care
    
    **Stage III (Poor Prognosis)**:
    - Criteria: Both biomarkers above thresholds (NT-proBNP >3000 AND Troponin T >0.05)
    - 4-year survival: 18%
    - Median survival: 20 months
    - Clinical approach: Urgent therapy consideration, advanced heart failure management
    
    **Key Clinical Applications**:
    1. **Prognosis Assessment**: Provides evidence-based survival estimates for patient counseling
    2. **Treatment Planning**: Guides decisions about disease-modifying therapies (tafamidis, diflunisal)
    3. **Clinical Trial Stratification**: Enables risk-stratified enrollment in research studies
    4. **Goals of Care**: Facilitates discussions about treatment intensity and end-of-life planning
    5. **Monitoring**: Serial biomarker assessment can track disease progression and treatment response
    
    **Treatment Implications by Stage**:
    - **Stage I**: Consider early intervention with disease-modifying therapy, appropriate for 
      aggressive treatments and clinical trial participation
    - **Stage II**: Disease-modifying therapy strongly indicated, initiate heart failure 
      medications as needed, multidisciplinary team approach
    - **Stage III**: Urgent consideration of all available therapies, evaluate for advanced 
      heart failure treatments including transplantation evaluation
    
    **Important Clinical Considerations**:
    - Specifically validated for wild-type ATTR-CM (not hereditary forms)
    - Should complement comprehensive clinical assessment including symptoms and imaging
    - Biomarker levels may be affected by renal function, age, atrial fibrillation, and comorbidities
    - Regular reassessment recommended as biomarkers change with disease progression
    - Multidisciplinary team approach essential involving cardiology, hematology, and heart failure specialists
    - Early diagnosis and treatment initiation associated with significantly better outcomes
    
    **Validation and Evidence**:
    The original Mayo Clinic study analyzed 244 patients with wild-type ATTR-CM, demonstrating 
    clear prognostic discrimination between stages with statistically significant survival differences. 
    Subsequent validation studies have confirmed the utility and reproducibility of this staging 
    system across different populations and healthcare systems worldwide.
    
    **Disease-Modifying Therapies**:
    - **Tafamidis**: FDA-approved transthyretin stabilizer, most effective in earlier stages
    - **Diflunisal**: Off-label NSAID with transthyretin stabilizing properties
    - **Future therapies**: Gene silencing agents and protein clearance strategies in development
    
    Args:
        request: Grogan staging parameters including NT-proBNP and troponin T levels
        
    Returns:
        GroganStagingAttrCmResponse: Grogan stage classification with prognostic information and clinical recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("grogan_staging_attr_cm", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Grogan Staging for ATTR-CM",
                    "details": {"parameters": parameters}
                }
            )
        
        return GroganStagingAttrCmResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Grogan Staging System",
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