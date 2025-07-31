"""
Common Terminology Criteria for Adverse Events (CTCAE) v5.0 Router

Endpoint for calculating CTCAE hematologic adverse event grading.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.oncology.ctcae import (
    CtcaeRequest,
    CtcaeResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/ctcae",
    response_model=CtcaeResponse,
    summary="Calculate Common Terminology Criteria for Adverse Events",
    description="Grades severity of hematologic and lymphatic adverse events from cancer treatment using standardized criteria. Assesses anemia, neutropenia, thrombocytopenia, and other blood disorders according to laboratory values and clinical presentations.",
    response_description="The calculated ctcae with interpretation",
    operation_id="calculate_ctcae"
)
async def calculate_ctcae(request: CtcaeRequest):
    """
    Calculates Common Terminology Criteria for Adverse Events (CTCAE) v5.0 Grading
    
    The CTCAE v5.0 is the standard terminology used by the oncology community to report 
    adverse events in a clear, precise, and reproducible manner. This calculator provides 
    standardized grading criteria for hematologic and lymphatic adverse events commonly 
    encountered in cancer treatment.
    
    **Clinical Background and Significance**:
    
    **CTCAE Development and Purpose**:
    - Developed by the National Cancer Institute (NCI) for standardized adverse event reporting
    - Version 5.0 published November 2017, current standard for clinical trials
    - Facilitates consistent grading across institutions, studies, and treatment modalities
    - Supports evidence-based medicine, regulatory submissions, and clinical decision-making
    - Enables meaningful comparisons between studies and treatment regimens
    
    **Grading Philosophy and Framework**:
    
    **5-Point Severity Scale**:
    - **Grade 1 (Mild)**: Asymptomatic or mild symptoms; clinical observations only; no intervention indicated
    - **Grade 2 (Moderate)**: Minimal intervention indicated; may limit instrumental activities of daily living
    - **Grade 3 (Severe)**: Medically significant; hospitalization may be indicated; limits self-care activities
    - **Grade 4 (Life-threatening)**: Life-threatening consequences; urgent intervention required
    - **Grade 5 (Death)**: Death related to adverse event
    
    **Clinical Decision Framework**:
    - Grades 1-2: Generally manageable with supportive care and monitoring
    - Grade 3: Often requires treatment delays, dose reductions, or intensive management
    - Grade 4: May necessitate treatment discontinuation and alternative therapy consideration
    - Standardized grading informs protocol-driven dose modification algorithms
    
    **Hematologic Adverse Events Coverage**:
    
    **Anemia Assessment**:
    
    **Clinical Significance**: Most common hematologic toxicity in cancer patients
    - Affects 70-90% of patients receiving chemotherapy
    - Significantly impacts quality of life, functional capacity, and treatment tolerance
    - Associated with fatigue, decreased cognitive function, and reduced survival in some studies
    - Early recognition and management prevent complications and improve outcomes
    
    **Grading Criteria** (Sex-specific normal ranges):
    - **Normal Ranges**: Male 14.0-18.0 g/dL, Female 12.0-16.0 g/dL
    - **Grade 1**: Hemoglobin <LLN to 10.0 g/dL (Male <13.9, Female <11.9 g/dL)
    - **Grade 2**: Hemoglobin <10.0-8.0 g/dL
    - **Grade 3**: Hemoglobin <8.0 g/dL; transfusion indicated
    - **Grade 4**: Life-threatening consequences; urgent intervention indicated
    
    **Management Considerations**:
    - Grade 1-2: Iron supplementation, nutritional support, erythropoiesis-stimulating agents
    - Grade 3-4: Transfusion support, comprehensive hematologic evaluation
    - Consider underlying causes: bleeding, hemolysis, nutritional deficiencies
    
    **Neutropenia Assessment**:
    
    **Clinical Significance**: Major dose-limiting toxicity affecting infection risk
    - Primary cause of treatment delays and dose reductions in many regimens
    - Grade 3-4 neutropenia increases risk of serious bacterial and fungal infections
    - Timing typically occurs 7-14 days after chemotherapy administration
    - Recovery generally within 21-28 days unless persistent bone marrow suppression
    
    **Grading Criteria** (Absolute Neutrophil Count):
    - **Normal Range**: 1,500-8,000 cells/mm³
    - **Grade 1**: ANC <LLN to 1,500 cells/mm³
    - **Grade 2**: ANC <1,500-1,000 cells/mm³
    - **Grade 3**: ANC <1,000-500 cells/mm³
    - **Grade 4**: ANC <500 cells/mm³
    
    **Management Protocol**:
    - Grade 1-2: Patient education, infection precautions, monitoring
    - Grade 3: Strict hygiene measures, avoid crowds, consider G-CSF support
    - Grade 4: Protective isolation, prophylactic antibiotics, growth factor support
    
    **Thrombocytopenia Assessment**:
    
    **Clinical Significance**: Critical bleeding risk factor in cancer patients
    - Dose-limiting toxicity for many chemotherapy regimens and targeted therapies
    - Grade 3-4 thrombocytopenia associated with increased bleeding complications
    - May limit ability to perform procedures, biopsies, or surgical interventions
    - Platelet transfusion thresholds vary by clinical situation and bleeding risk
    
    **Grading Criteria** (Platelet Count):
    - **Normal Range**: 150,000-450,000 cells/mm³
    - **Grade 1**: Platelets <LLN to 75,000 cells/mm³
    - **Grade 2**: Platelets <75,000-50,000 cells/mm³
    - **Grade 3**: Platelets <50,000-25,000 cells/mm³
    - **Grade 4**: Platelets <25,000 cells/mm³
    
    **Management Strategy**:
    - Grade 1-2: Bleeding precautions, avoid anticoagulants and antiplatelet agents
    - Grade 3: Platelet transfusion consideration, procedure restrictions
    - Grade 4: Active bleeding assessment, urgent transfusion support
    
    **Febrile Neutropenia Assessment**:
    
    **Clinical Significance**: Medical emergency requiring immediate intervention
    - Potentially life-threatening complication of cancer treatment
    - Associated with significant morbidity and mortality if not promptly treated
    - Broad-spectrum antibiotics must be initiated within 1 hour of recognition
    - Hospitalization typically required for IV antibiotic therapy and monitoring
    
    **Diagnostic Criteria**:
    - **Neutropenia**: ANC <1,000 cells/mm³ (<1.0 x 10⁹/L)
    - **Fever**: Temperature >38.3°C (101°F) or sustained ≥38.0°C (100.4°F) for >1 hour
    - **Grading**: Always Grade 3 when both criteria are met
    
    **Emergency Management Protocol**:
    - Immediate blood cultures (before antibiotics if possible)
    - Broad-spectrum empirical antibiotic therapy within 1 hour
    - Daily reassessment and culture monitoring
    - Growth factor (G-CSF) support per institutional guidelines
    
    **Leukocytosis Assessment**:
    
    **Clinical Significance**: Elevated WBC count requiring evaluation
    - May indicate infection, inflammation, or hematologic malignancy progression
    - Can affect treatment decisions and require additional diagnostic workup
    - Hyperleukocytosis (>100,000 cells/mm³) may cause leukostasis complications
    - Important to differentiate reactive versus malignant causes
    
    **Grading Criteria** (Total WBC Count):
    - **Normal Range**: 4,000-11,000 cells/mm³
    - **Grade 1**: WBC >ULN to 20,000 cells/mm³
    - **Grade 2**: WBC >20,000-50,000 cells/mm³
    - **Grade 3**: WBC >50,000-100,000 cells/mm³
    - **Grade 4**: WBC >100,000 cells/mm³ (hyperleukocytosis)
    
    **Lymphopenia Assessment**:
    
    **Clinical Significance**: Immune suppression affecting infection and vaccine responses
    - Common with lymphocyte-targeting therapies and radiation
    - Increases risk of opportunistic infections and viral reactivation
    - May affect vaccine efficacy and immune surveillance
    - Can be prolonged with certain immunosuppressive regimens
    
    **Grading Criteria** (Absolute Lymphocyte Count):
    - **Normal Range**: 1,000-4,000 cells/mm³
    - **Grade 1**: Lymphocytes <LLN to 800 cells/mm³
    - **Grade 2**: Lymphocytes <800-500 cells/mm³
    - **Grade 3**: Lymphocytes <500-200 cells/mm³
    - **Grade 4**: Lymphocytes <200 cells/mm³
    
    **Clinical Implementation Standards**:
    
    **Assessment Requirements**:
    - Complete blood count with differential for comprehensive evaluation
    - Vital signs including temperature for febrile neutropenia screening
    - Clinical evaluation for symptoms, functional status, and quality of life impact
    - Review of concurrent medications, comorbidities, and recent procedures
    
    **Laboratory Considerations**:
    - Use laboratory-specific reference ranges when available
    - Consider patient baseline values and pre-treatment blood counts
    - Account for hydration status, medications, and timing relative to treatment
    - Document exact values and reference ranges used for grading
    
    **Quality Assurance Framework**:
    - Standardized training on CTCAE criteria improves inter-rater reliability
    - Regular calibration exercises maintain consistency across providers
    - Documentation should include clinical context and grade rationale
    - Version control important as CTCAE criteria continue to evolve
    
    **Treatment Integration and Decision Support**:
    
    **Dose Modification Algorithms**:
    - Grade 0-1: Continue treatment as planned with standard monitoring
    - Grade 2: Consider dose delays; monitor for progression to higher grades
    - Grade 3: Hold treatment until improvement; dose reduction typically required
    - Grade 4: Discontinue treatment; consider alternative regimens after recovery
    
    **Monitoring Strategies**:
    - Grade-specific monitoring intervals and intensity
    - Symptom assessment and functional status evaluation
    - Laboratory trending and response to interventions
    - Patient education on signs and symptoms requiring immediate medical attention
    
    **Research and Quality Improvement Applications**:
    
    **Clinical Trial Integration**:
    - Standardized CTCAE reporting enables cross-study comparisons
    - Facilitates meta-analyses and systematic reviews
    - Supports regulatory submissions and drug approval processes
    - Informs development of predictive models for toxicity risk
    
    **Quality Metrics**:
    - Institutional toxicity rates by treatment regimen and patient population
    - Time to toxicity recognition and appropriate intervention
    - Correlation between CTCAE grades and patient-reported outcomes
    - Effectiveness of supportive care interventions by toxicity grade
    
    This calculator provides automated, standardized CTCAE v5.0 grading for common 
    hematologic adverse events, supporting evidence-based clinical decision-making, 
    research applications, and quality improvement initiatives in oncology care.
    
    Args:
        request: CTCAE assessment parameters including adverse event type and relevant laboratory values
        
    Returns:
        CtcaeResponse: Comprehensive CTCAE grading with clinical interpretation and management recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("ctcae", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating CTCAE assessment",
                    "details": {"parameters": parameters}
                }
            )
        
        return CtcaeResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for CTCAE assessment",
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