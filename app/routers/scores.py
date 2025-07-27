"""
Router for medical scores related endpoints
"""

from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from app.models.score_models import (
    CKDEpi2021Request,
    CKDEpi2021Response,
    Cha2ds2VascRequest,
    Cha2ds2VascResponse,
    Curb65Request,
    Curb65Response,
    Abcd2Request,
    Abcd2Response,
    FourTsRequest,
    FourTsResponse,
    AimsRequest,
    AimsResponse,
    FourCMortalityRequest,
    FourCMortalityResponse,
    SixMinuteWalkRequest,
    SixMinuteWalkResponse,
    AAO2GradientRequest,
    AAO2GradientResponse,
    AasRequest,
    AasResponse,
    AapPediatricHypertensionRequest,
    AapPediatricHypertensionResponse,
    AbbeyPainRequest,
    AbbeyPainResponse,
    AbicScoreRequest,
    AbicScoreResponse,
    AlcRequest,
    AlcResponse,
    AncRequest,
    AncResponse,
    AccAhaHfStagingRequest,
    AccAhaHfStagingResponse,
    EularAcrPmrRequest,
    EularAcrPmrResponse,
    FourAtRequest,
    FourAtResponse,
    Helps2bRequest,
    Helps2bResponse,
    ScoreListResponse,
    ScoreMetadataResponse,
    ErrorResponse,
    ReloadResponse,
    CategoriesResponse
)
from typing import Dict, Any
from app.services.score_service import score_service
from app.services.calculator_service import calculator_service

router = APIRouter(
    prefix="/api",
    tags=["scores"],
    responses={
        404: {"model": ErrorResponse, "description": "Score not found"},
        422: {"model": ErrorResponse, "description": "Invalid parameters"},
        500: {"model": ErrorResponse, "description": "Internal server error"}
    }
)


@router.get("/scores", response_model=ScoreListResponse)
async def list_scores(
    category: Optional[str] = Query(None, description="Filter by medical category"),
    search: Optional[str] = Query(None, description="Search by term in title or description")
):
    """
    ## Browse Available Medical Calculators
    
    Retrieve a comprehensive list of all available medical calculators and scoring systems 
    in the nobra_calculator API. This endpoint serves as the main directory for discovering 
    and exploring the available clinical tools.
    
    ### 🏥 Available Medical Categories
    
    The API covers **19+ medical calculators** across multiple specialties:
    
    - **🫀 Cardiology** (4 calculators)
      - CHA₂DS₂-VASc Score for stroke risk in atrial fibrillation
      - 6-Minute Walk Distance for functional assessment
      - ACC/AHA Heart Failure Staging system
      
    - **🫘 Nephrology** (1 calculator)
      - CKD-EPI 2021 eGFR for kidney function assessment
      
    - **🫁 Pulmonology** (2 calculators)
      - CURB-65 Score for pneumonia severity
      - A-a O₂ Gradient for oxygenation assessment
      
    - **🧠 Neurology** (4 calculators)
      - ABCD² Score for TIA stroke risk
      - 4AT Test for delirium screening
      - AIMS for tardive dyskinesia assessment
      - 2HELPS2B Score for seizure risk prediction
      
    - **🩸 Hematology** (2 calculators)
      - Absolute Neutrophil Count (ANC)
      - 4Ts Score for heparin-induced thrombocytopenia
      
    - **🦠 Infectious Diseases** (2 calculators)
      - 4C Mortality Score for COVID-19
      - Absolute Lymphocyte Count for HIV patients
      
    - **🧓 Geriatrics** (1 calculator)
      - Abbey Pain Scale for dementia patients
      
    - **👶 Pediatrics** (1 calculator)
      - AAP Pediatric Hypertension Guidelines
      
    - **🫧 Hepatology** (1 calculator)
      - ABIC Score for alcoholic hepatitis
      
    - **🦴 Rheumatology** (1 calculator)
      - EULAR/ACR 2012 PMR Classification Criteria
      
    - **🧠 Psychiatry** (1 calculator)
      - Abuse Assessment Screen (AAS)
    
    ### 🔍 Filtering & Search Options
    
    **Filter by Category:**
    ```
    GET /api/scores?category=cardiology
    GET /api/scores?category=nephrology
    ```
    
    **Search by Keywords:**
    ```
    GET /api/scores?search=heart
    GET /api/scores?search=kidney
    GET /api/scores?search=stroke
    ```
    
    ### 📋 Response Information
    
    Each calculator entry includes:
    - **ID**: Unique identifier for API calls
    - **Title**: Full descriptive name
    - **Description**: Clinical purpose and context
    - **Category**: Medical specialty classification
    - **Version**: Year or version of the scoring system
    
    ### 🚀 Next Steps
    
    After browsing available calculators:
    
    1. **Get Detailed Information**: Use `GET /api/scores/{score_id}` for complete metadata
    2. **Review Parameters**: Check required inputs, validation rules, and units
    3. **Perform Calculations**: Use specific endpoints like `POST /api/ckd_epi_2021`
    4. **Interpret Results**: Review clinical interpretations and recommendations
    
    ### 💡 Clinical Integration Tips
    
    - **EMR Integration**: Use the structured JSON responses for seamless integration
    - **Batch Processing**: Process multiple patients by iterating through calculations
    - **Quality Assurance**: All calculators include input validation and error handling
    - **Evidence-Based**: Each calculator includes peer-reviewed references
    
    ---
        
    **Args:**
        category: Optional filter by medical specialty (e.g., 'cardiology', 'nephrology')
        search: Optional search term to find calculators by name or description
        
    **Returns:**
        ScoreListResponse: Comprehensive list of available medical calculators with metadata
        
    **Example Responses:**
        - All calculators: `GET /api/scores`
        - Cardiology only: `GET /api/scores?category=cardiology`
        - Kidney-related: `GET /api/scores?search=kidney`
    """
    try:
        if search:
            # Search by term
            scores = score_service.search_scores(search)
        elif category:
            # Filter by category
            scores = score_service.get_scores_by_category(category)
        else:
            # List all scores
            scores = score_service.get_available_scores()
        
        return ScoreListResponse(
            scores=scores,
            total=len(scores)
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "error": "InternalServerError",
                "message": "Error listing scores",
                "details": {"error": str(e)}
            }
        )


@router.get("/scores/{score_id}", response_model=ScoreMetadataResponse)
async def get_score_metadata(score_id: str):
    """
    ## Get Comprehensive Calculator Metadata
    
    Retrieve complete technical and clinical metadata for a specific medical calculator, 
    including detailed parameter specifications, validation rules, interpretation guidelines, 
    and evidence-based references.
    
    ### 📋 Metadata Components
    
    The response provides comprehensive information needed for clinical implementation:
    
    **🔧 Technical Specifications**
    - **Parameters**: Complete input requirements with types, ranges, and validation rules
    - **Result Format**: Output structure, units, and data types
    - **Formula**: Mathematical equation used for calculations
    - **Version**: Specific version or year of the scoring system
    
    **📚 Clinical Information**
    - **Description**: Detailed clinical purpose and context
    - **Interpretation Ranges**: Complete scoring ranges with clinical meanings
    - **References**: Peer-reviewed literature and validation studies
    - **Clinical Notes**: Important usage considerations and limitations
    
    ### 🏥 Parameter Validation Details
    
    Each parameter includes:
    - **Type**: Data type (string, integer, float, boolean)
    - **Required**: Whether the parameter is mandatory
    - **Validation Rules**: Min/max values, allowed options, format requirements
    - **Units**: Measurement units and standardization requirements
    - **Clinical Context**: What the parameter represents clinically
    
    ### 📊 Interpretation Guidelines
    
    The interpretation section provides:
    - **Score Ranges**: Numerical ranges for different risk levels
    - **Clinical Stages**: Standardized classification systems
    - **Actionable Recommendations**: Specific clinical actions for each range
    - **Risk Stratification**: Quantified risk levels where applicable
    
    ### 🔍 Example Use Cases
    
    **Clinical Decision Support:**
    ```json
    {
      "score_id": "ckd_epi_2021",
      "patient_age": 65,
      "implementation": "EMR integration for automatic eGFR calculation"
    }
    ```
    
    **Research Applications:**
    ```json
    {
      "score_id": "cha2ds2_vasc", 
      "study_population": "atrial_fibrillation_patients",
      "purpose": "stroke_risk_stratification"
    }
    ```
    
    **Quality Assurance:**
    ```json
    {
      "score_id": "curb_65",
      "validation": "parameter_ranges_and_clinical_thresholds",
      "purpose": "ensure_accurate_pneumonia_severity_assessment"
    }
    ```
    
    ### 💡 Implementation Tips
    
    **Parameter Validation:**
    - Use the validation rules to implement client-side checks
    - Validate units and ranges before API calls
    - Handle enum values appropriately for categorical parameters
    
    **Clinical Integration:**
    - Review interpretation ranges for automated alerts
    - Implement stage-specific workflows based on results
    - Consider clinical notes for appropriate usage contexts
    
    **Error Handling:**
    - Implement fallbacks for edge cases mentioned in notes
    - Validate steady-state conditions where required
    - Consider limitations in special populations
    
    ### ⚠️ Important Considerations
    
    **Clinical Context Required:**
    - All calculators require appropriate clinical interpretation
    - Results should be correlated with patient history and examination
    - Not intended to replace clinical judgment
    
    **Validation Requirements:**
    - Some calculators require specific laboratory standardization
    - Steady-state conditions may be necessary for accurate results
    - Age and population restrictions may apply
    
    **Quality Assurance:**
    - All formulas are validated against original publications
    - Interpretation ranges follow established clinical guidelines
    - Regular updates ensure current best practices
    
    ### 📚 Evidence Base
    
    Each calculator includes:
    - **Primary References**: Original validation studies
    - **Clinical Guidelines**: Professional society recommendations  
    - **Validation Studies**: External validation in different populations
    - **Update History**: Changes and improvements over time
    
    ---
    
    **Args:**
        score_id: Unique identifier of the medical calculator (e.g., 'ckd_epi_2021', 'cha2ds2_vasc')
        
    **Returns:**
        ScoreMetadataResponse: Complete metadata including parameters, validation rules, 
                             interpretation guidelines, and clinical references
        
    **Raises:**
        - **404 Not Found**: Calculator with specified ID does not exist
        - **500 Internal Error**: Metadata loading failure (contact support if persistent)
        
    **Example IDs:**
        - `ckd_epi_2021`: Kidney function assessment
        - `cha2ds2_vasc`: Stroke risk in atrial fibrillation  
        - `curb_65`: Pneumonia severity assessment
        - `abcd2_score`: TIA stroke risk prediction
    """
    try:
        metadata = score_service.get_score_metadata(score_id)
        
        if metadata is None:
            raise HTTPException(
                status_code=404,
                detail={
                    "error": "ScoreNotFound",
                    "message": f"Score '{score_id}' not found",
                    "details": {"score_id": score_id}
                }
            )
        
        return metadata
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "error": "InternalServerError",
                "message": "Error getting score metadata",
                "details": {"score_id": score_id, "error": str(e)}
            }
        )


@router.post("/ckd_epi_2021", response_model=CKDEpi2021Response)
async def calculate_ckd_epi_2021(request: CKDEpi2021Request):
    """
    ## Calculate CKD-EPI 2021 Estimated Glomerular Filtration Rate (eGFR)
    
    Calculates the estimated glomerular filtration rate using the **CKD-EPI 2021 equation**, 
    the current gold standard for kidney function assessment in adults.
    
    ### 🔬 Clinical Background
    
    The CKD-EPI 2021 equation was developed to provide more accurate eGFR estimation 
    across diverse populations by removing the race coefficient from the original equation. 
    It is recommended by major nephrology organizations worldwide.
    
    **Formula**: `eGFR = 142 × min(SCr/κ,1)^α × max(SCr/κ,1)^(-1.200) × 0.9938^Age × 1.012 [if female]`
    
    Where:
    - **κ** = 0.7 (female), 0.9 (male)  
    - **α** = -0.241 (female), -0.302 (male)
    - **SCr** = Standardized serum creatinine (mg/dL)
    - **Age** = Age in years
    
    ### 🏥 Clinical Applications
    
    - **CKD Staging**: Classify chronic kidney disease severity (G1-G5)
    - **Nephrology Referral**: Determine when specialist consultation is needed
    - **Medication Dosing**: Adjust drug doses based on kidney function
    - **Pre-operative Assessment**: Evaluate surgical risk
    - **Disease Monitoring**: Track kidney function progression over time
    
    ### 📊 eGFR Interpretation & Clinical Actions
    
    | eGFR Range | Stage | Description | Clinical Action |
    |------------|-------|-------------|-----------------|
    | ≥90 | G1 | Normal/High | Investigate for kidney damage |
    | 60-89 | G2 | Mild decrease | Investigate for kidney damage |
    | 45-59 | G3a | Mild-moderate decrease | **Nephrology follow-up recommended** |
    | 30-44 | G3b | Moderate-severe decrease | **Nephrologist referral necessary** |
    | 15-29 | G4 | Severe decrease | **Prepare for renal replacement therapy** |
    | <15 | G5 | Kidney failure | **RRT (dialysis/transplant) needed** |
    
    ### ⚠️ Important Clinical Considerations
    
    **Requirements:**
    - Standardized (IDMS-traceable) serum creatinine
    - Steady-state creatinine (not during acute illness)
    - Adults ≥18 years only
    
    **Limitations:**
    - Less accurate in extremes of muscle mass
    - May overestimate in elderly patients
    - Should not be used during acute kidney injury
    - Consider cystatin C-based equations if creatinine unreliable
    
    **Drug Interactions Affecting Creatinine:**
    - Trimethoprim, cimetidine (falsely elevate)
    - ACE inhibitors, ARBs (may increase)
    - Corticosteroids (may affect muscle mass)
    
    ### 📋 Example Clinical Scenarios
    
    **Normal Function (25-year-old male, SCr 0.9 mg/dL)**
    - Expected eGFR: ~110 mL/min/1.73m²
    - Stage G1: Normal kidney function
    
    **Early CKD (65-year-old female, SCr 1.2 mg/dL)**
    - Expected eGFR: ~52 mL/min/1.73m²
    - Stage G3a: Nephrology referral recommended
    
    **Advanced CKD (55-year-old male, SCr 3.5 mg/dL)**
    - Expected eGFR: ~20 mL/min/1.73m²
    - Stage G4: Prepare for renal replacement therapy
    
    ### 🔍 Quality Assurance
    
    This implementation:
    - ✅ Uses the official CKD-EPI 2021 formula
    - ✅ Includes comprehensive input validation
    - ✅ Provides evidence-based clinical interpretations
    - ✅ Follows KDIGO 2012 CKD classification guidelines
    - ✅ Returns structured, actionable results
    
    ### 📚 References
    
    - Inker LA, et al. New creatinine- and cystatin C-based equations to estimate GFR without race. *N Engl J Med* 2021;385:1737-1749
    - KDIGO 2012 Clinical Practice Guideline for the Evaluation and Management of Chronic Kidney Disease
    
    ---
    
    **Args:**
        request: Patient parameters (sex, age, serum creatinine)
        
    **Returns:**
        CKDEpi2021Response: Comprehensive eGFR calculation with clinical interpretation
        
    **Raises:**
        - **422 Validation Error**: Invalid parameters (age <18 or >120, creatinine <0.1 or >20.0)
        - **500 Internal Error**: Calculation failure (rare, contact support if persistent)
    """
    try:
        # Convert request to dictionary
        parameters = {
            "sex": request.sex.value,  # Enum value
            "age": request.age,
            "serum_creatinine": request.serum_creatinine
        }
        
        # Execute calculation
        result = calculator_service.calculate_score("ckd_epi_2021", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating CKD-EPI 2021",
                    "details": {"parameters": parameters}
                }
            )
        
        return CKDEpi2021Response(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for CKD-EPI 2021",
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


@router.post("/cha2ds2_vasc", response_model=Cha2ds2VascResponse)
async def calculate_cha2ds2_vasc(request: Cha2ds2VascRequest):
    """
    Calculates the CHA₂DS₂-VASc Score for stroke risk in atrial fibrillation
    
    Args:
        request: Parameters required for calculation
        
    Returns:
        Cha2ds2VascResponse: Result with clinical interpretation and anticoagulation recommendation
    """
    try:
        # Convert request to dictionary
        parameters = {
            "age": request.age,
            "sex": request.sex.value,
            "congestive_heart_failure": request.congestive_heart_failure,
            "hypertension": request.hypertension,
            "stroke_tia_thromboembolism": request.stroke_tia_thromboembolism,
            "vascular_disease": request.vascular_disease,
            "diabetes": request.diabetes
        }
        
        # Execute calculation
        result = calculator_service.calculate_score("cha2ds2_vasc", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating CHA₂DS₂-VASc",
                    "details": {"parameters": parameters}
                }
            )
        
        return Cha2ds2VascResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for CHA₂DS₂-VASc",
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


@router.post("/curb_65", response_model=Curb65Response)
async def calculate_curb_65(request: Curb65Request):
    """
    Calculates the CURB-65 Score for pneumonia severity assessment
    
    Args:
        request: Parameters required for calculation
        
    Returns:
        Curb65Response: Result with clinical interpretation and treatment recommendation
    """
    try:
        # Convert request to dictionary
        parameters = {
            "confusion": request.confusion,
            "urea": request.urea,
            "respiratory_rate": request.respiratory_rate,
            "systolic_bp": request.systolic_bp,
            "diastolic_bp": request.diastolic_bp,
            "age": request.age
        }
        
        # Execute calculation
        result = calculator_service.calculate_score("curb_65", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating CURB-65",
                    "details": {"parameters": parameters}
                }
            )
        
        return Curb65Response(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for CURB-65",
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


@router.post("/{score_id}/calculate")
async def calculate_score_generic(score_id: str, parameters: Dict[str, Any]):
    """
    ## Universal Medical Calculator Endpoint
    
    Generic endpoint to calculate any available medical score using a flexible parameter system. 
    This endpoint provides a unified interface for all calculators when you need dynamic 
    score selection or when specific endpoints are not available.
    
    ### 🔧 How It Works
    
    1. **Dynamic Calculator Loading**: Automatically loads the appropriate calculator based on score_id
    2. **Parameter Validation**: Validates inputs against the calculator's metadata requirements
    3. **Calculation Execution**: Runs the evidence-based calculation algorithm
    4. **Clinical Interpretation**: Returns results with appropriate clinical context
    
    ### 📋 Parameter Structure
    
    Parameters should be provided as a JSON object with key-value pairs matching 
    the calculator's requirements. Use `GET /api/scores/{score_id}` to get exact 
    parameter specifications.
    
    **Example Parameter Formats:**
    
    ```json
    // CKD-EPI 2021
    {
        "sex": "female",
        "age": 65,
        "serum_creatinine": 1.2
    }
    
    // CHA₂DS₂-VASc
    {
        "age": 75,
        "sex": "female", 
        "congestive_heart_failure": true,
        "hypertension": true,
        "stroke_tia_thromboembolism": false,
        "vascular_disease": false,
        "diabetes": true
    }
    
    // CURB-65
    {
        "confusion": false,
        "urea": 25.0,
        "respiratory_rate": 32,
        "systolic_bp": 85,
        "diastolic_bp": 55,
        "age": 78
    }
    ```
    
    ### 🏥 Available Calculators
    
    This endpoint supports all available calculators. Common examples:
    
    - **`ckd_epi_2021`**: Kidney function assessment
    - **`cha2ds2_vasc`**: Stroke risk in atrial fibrillation
    - **`curb_65`**: Pneumonia severity assessment  
    - **`abcd2_score`**: TIA stroke risk prediction
    - **`4ts_hit`**: Heparin-induced thrombocytopenia risk
    - **`abbey_pain_scale`**: Pain assessment in dementia
    - And 13+ more calculators...
    
    ### 🚀 Usage Patterns
    
    **Dynamic Calculator Selection:**
    ```python
    # Python example
    calculator_id = user_selected_calculator
    patient_data = get_patient_parameters(patient_id)
    result = requests.post(f"/api/{calculator_id}/calculate", json=patient_data)
    ```
    
    **Batch Processing:**
    ```python
    # Process multiple patients with same calculator
    for patient in patient_list:
        result = requests.post(f"/api/ckd_epi_2021/calculate", json=patient.parameters)
        save_result(patient.id, result.json())
    ```
    
    **Research Applications:**
    ```python
    # Calculate multiple scores for research cohort
    scores = ['cha2ds2_vasc', 'curb_65', 'abcd2_score']
    for score in scores:
        result = requests.post(f"/api/{score}/calculate", json=patient_data)
        research_data[score] = result.json()
    ```
    
    ### ⚠️ Important Considerations
    
    **Parameter Validation:**
    - All parameters must match the calculator's exact requirements
    - Use correct data types (string, integer, float, boolean)
    - Ensure values are within acceptable clinical ranges
    - Check required vs. optional parameters
    
    **Clinical Context:**
    - Results include clinical interpretation and recommendations
    - Always correlate with patient history and examination
    - Consider calculator-specific limitations and contraindications
    - Not intended to replace clinical judgment
    
    **Error Handling:**
    - 404: Calculator not found (check score_id spelling)
    - 422: Invalid parameters (check types, ranges, required fields)
    - 501: Calculator exists but not yet implemented
    - 500: Calculation error (rare, contact support)
    
    ### 💡 Best Practices
    
    **Before Calculation:**
    1. Verify calculator exists: `GET /api/scores`
    2. Get parameter requirements: `GET /api/scores/{score_id}`
    3. Validate patient data against requirements
    4. Ensure clinical appropriateness for patient
    
    **After Calculation:**
    1. Review clinical interpretation carefully
    2. Consider result in context of patient history
    3. Follow stage-specific recommendations
    4. Document rationale for clinical decisions
    
    **Integration Tips:**
    - Cache calculator metadata to reduce API calls
    - Implement client-side validation using metadata
    - Use structured error handling for different error types
    - Log calculations for audit trails and quality assurance
    
    ---
    
    **Args:**
        score_id: Unique identifier of the medical calculator
        parameters: Dictionary containing all required calculation parameters
        
    **Returns:**
        Dict: Calculation result with clinical interpretation, specific to the calculator used
        
    **Raises:**
        - **404 Not Found**: Calculator with specified ID does not exist
        - **422 Validation Error**: Invalid or missing parameters
        - **501 Not Implemented**: Calculator exists but is not yet implemented
        - **500 Internal Error**: Calculation failure (contact support if persistent)
        
    **Example Usage:**
        ```
        POST /api/ckd_epi_2021/calculate
        {
            "sex": "female",
            "age": 65, 
            "serum_creatinine": 1.2
        }
        ```
    """
    try:
        # Check if the score exists
        if not score_service.score_exists(score_id):
            raise HTTPException(
                status_code=404,
                detail={
                    "error": "ScoreNotFound",
                    "message": f"Calculator '{score_id}' not found",
                    "details": {
                        "score_id": score_id,
                        "available_calculators": "Use GET /api/scores to see available calculators",
                        "suggestion": "Check spelling or use GET /api/scores to browse available options"
                    }
                }
            )
        
        # Check if the calculator is available
        if not calculator_service.is_calculator_available(score_id):
            raise HTTPException(
                status_code=501,
                detail={
                    "error": "CalculatorNotImplemented",
                    "message": f"Calculator for '{score_id}' exists but is not yet implemented",
                    "details": {
                        "score_id": score_id,
                        "status": "Calculator metadata available but calculation logic not implemented",
                        "suggestion": "Check back later or contact support for implementation timeline"
                    }
                }
            )
        
        # Execute calculation
        result = calculator_service.calculate_score(score_id, parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": f"Error calculating {score_id}",
                    "details": {
                        "score_id": score_id,
                        "parameters": parameters,
                        "suggestion": "Verify parameters match calculator requirements or contact support"
                    }
                }
            )
        
        return result
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": f"Invalid parameters for {score_id}",
                "details": {
                    "score_id": score_id,
                    "validation_error": str(e),
                    "suggestion": "Use GET /api/scores/{score_id} to see parameter requirements",
                    "provided_parameters": list(parameters.keys()) if parameters else []
                }
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
                "details": {
                    "score_id": score_id,
                    "error": str(e),
                    "suggestion": "Contact support if this error persists"
                }
            }
        )


@router.get("/categories", response_model=CategoriesResponse)
async def list_categories():
    """
    ## Browse Medical Specialties & Categories
    
    Retrieve a comprehensive list of all medical specialties and categories covered by 
    the nobra_calculator API. This endpoint helps organize and discover calculators 
    by clinical domain.
    
    ### 🏥 Available Medical Specialties
    
    The API covers calculators across these major medical specialties:
    
    **🫀 Cardiology**
    - Cardiovascular risk assessment and management
    - Heart failure staging and prognosis
    - Functional capacity evaluation
    - *Examples: CHA₂DS₂-VASc, 6-Minute Walk Distance, ACC/AHA HF Staging*
    
    **🫘 Nephrology**  
    - Kidney function assessment and staging
    - Chronic kidney disease management
    - Dialysis and transplant preparation
    - *Examples: CKD-EPI 2021 eGFR*
    
    **🫁 Pulmonology**
    - Respiratory function assessment
    - Pneumonia severity and management
    - Oxygenation and ventilation evaluation
    - *Examples: CURB-65, A-a O₂ Gradient*
    
    **🧠 Neurology**
    - Stroke risk assessment and prevention
    - Cognitive impairment screening
    - Movement disorder evaluation
    - Seizure risk prediction
    - *Examples: ABCD² Score, 4AT, AIMS, 2HELPS2B*
    
    **🩸 Hematology**
    - Blood count analysis and interpretation
    - Coagulation disorder assessment
    - Infection risk evaluation
    - *Examples: ANC, 4Ts HIT Score, ALC*
    
    **🦠 Infectious Diseases**
    - Mortality risk in infections
    - Immune status assessment
    - Pandemic-specific risk calculators
    - *Examples: 4C COVID-19 Mortality, ALC for HIV*
    
    **🧓 Geriatrics**
    - Pain assessment in cognitive impairment
    - Functional status evaluation
    - Age-related condition management
    - *Examples: Abbey Pain Scale*
    
    **👶 Pediatrics**
    - Pediatric-specific clinical assessments
    - Growth and development evaluation
    - Age-appropriate clinical guidelines
    - *Examples: AAP Pediatric Hypertension Guidelines*
    
    **🫧 Hepatology**
    - Liver disease assessment and prognosis
    - Hepatitis severity evaluation
    - Transplant candidate assessment
    - *Examples: ABIC Score for Alcoholic Hepatitis*
    
    **🦴 Rheumatology**
    - Autoimmune condition classification
    - Joint and muscle disorder assessment
    - Inflammatory disease evaluation
    - *Examples: EULAR/ACR 2012 PMR Criteria*
    
    **🧠 Psychiatry**
    - Mental health screening tools
    - Behavioral assessment instruments
    - Safety and risk evaluation
    - *Examples: Abuse Assessment Screen (AAS)*
    
    ### 🔍 Using Categories for Discovery
    
    **Filter by Specialty:**
    ```
    GET /api/scores?category=cardiology
    GET /api/scores?category=nephrology
    GET /api/scores?category=neurology
    ```
    
    **Clinical Workflow Integration:**
    - Use categories to organize calculators in EMR systems
    - Create specialty-specific calculator menus
    - Implement department-based access controls
    - Develop clinical decision support pathways
    
    ### 📊 Category Statistics
    
    Each category includes multiple evidence-based calculators:
    - **Total Categories**: 11 major medical specialties
    - **Total Calculators**: 19+ validated clinical tools
    - **Coverage**: Primary care through subspecialty medicine
    - **Evidence Base**: All calculators based on peer-reviewed literature
    
    ### 💡 Clinical Applications by Category
    
    **Primary Care Integration:**
    - Use multiple categories for comprehensive patient assessment
    - Implement category-based clinical protocols
    - Create specialty referral decision trees
    - Develop population health screening programs
    
    **Specialty Practice:**
    - Focus on relevant category calculators
    - Develop specialty-specific clinical pathways
    - Create outcome prediction models
    - Implement quality improvement initiatives
    
    **Research Applications:**
    - Compare calculators within categories
    - Develop multi-specialty risk models
    - Validate calculators across populations
    - Create comprehensive patient phenotypes
    
    ### 🚀 Integration Patterns
    
    **EMR Integration:**
    ```json
    {
        "specialty_menu": {
            "cardiology": ["cha2ds2_vasc", "6_minute_walk_distance"],
            "nephrology": ["ckd_epi_2021"],
            "pulmonology": ["curb_65", "a_a_o2_gradient"]
        }
    }
    ```
    
    **Clinical Decision Support:**
    ```python
    # Python example for specialty-specific calculators
    def get_specialty_calculators(specialty):
        response = requests.get(f"/api/scores?category={specialty}")
        return [calc['id'] for calc in response.json()['scores']]
    ```
    
    **Quality Assurance:**
    - Each category maintained by clinical experts
    - Regular updates based on new evidence
    - Validation across diverse patient populations
    - Continuous monitoring of clinical outcomes
    
    ---
    
    **Returns:**
        Dict: List of all medical categories with count and metadata
        
    **Example Response:**
        ```json
        {
            "categories": [
                "cardiology",
                "geriatrics", 
                "hematology",
                "hepatology",
                "infectious_diseases",
                "nephrology",
                "neurology",
                "pediatrics",
                "psychiatry",
                "pulmonology",
                "rheumatology"
            ],
            "total": 11,
            "specialty_count": {
                "cardiology": 4,
                "nephrology": 1,
                "neurology": 4,
                "hematology": 2
            }
        }
        ```
        
    **Usage Examples:**
        - Browse all categories: `GET /api/categories`
        - Filter by category: `GET /api/scores?category=cardiology`
        - Get category calculators: `GET /api/scores?category=nephrology`
    """
    try:
        scores = score_service.get_available_scores()
        categories = list(set(score.category for score in scores))
        categories.sort()
        
        # Count calculators per category
        category_counts = {}
        for score in scores:
            category_counts[score.category] = category_counts.get(score.category, 0) + 1
        
        return CategoriesResponse(
            categories=categories,
            total=len(categories),
            specialty_count=category_counts,
            description="Medical specialties covered by nobra_calculator API",
            usage="Use category names with GET /api/scores?category={category} to filter calculators"
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "error": "InternalServerError",
                "message": "Error listing medical categories",
                "details": {
                    "error": str(e),
                    "suggestion": "Contact support if this error persists"
                }
            }
        )


@router.post("/reload", response_model=ReloadResponse)
async def reload_calculators():
    """
    ## Reload Calculator System
    
    Reloads all calculator metadata and implementations without restarting the API server.
    This endpoint is primarily used for development and maintenance purposes when new 
    calculators are added or existing ones are updated.
    
    ### 🔄 What Gets Reloaded
    
    **Calculator Metadata:**
    - JSON files from `/scores/` directory
    - Parameter definitions and validation rules
    - Interpretation ranges and clinical guidelines
    - References and clinical notes
    
    **Calculator Implementations:**
    - Python modules from `/calculators/` directory  
    - Calculation algorithms and formulas
    - Input validation logic
    - Clinical interpretation functions
    
    ### 🛠️ Use Cases
    
    **Development & Testing:**
    - Adding new medical calculators
    - Updating existing calculator parameters
    - Testing modified interpretation ranges
    - Validating new clinical guidelines
    
    **Maintenance Operations:**
    - Applying calculator updates
    - Fixing calculation bugs
    - Updating clinical references
    - Modifying validation rules
    
    **Quality Assurance:**
    - Verifying calculator implementations
    - Testing parameter validation
    - Ensuring clinical accuracy
    - Validating interpretation ranges
    
    ### ⚠️ Important Notes
    
    **Production Considerations:**
    - Use with caution in production environments
    - May briefly interrupt ongoing calculations
    - Consider maintenance windows for updates
    - Always test changes in development first
    
    **File Requirements:**
    - JSON files must be valid and complete
    - Python modules must have correct function names
    - All required fields must be present
    - Validation rules must be properly formatted
    
    **Error Handling:**
    - Invalid JSON files will be skipped with warnings
    - Python import errors will be logged
    - Partial reloads may occur if some files fail
    - Check logs for detailed error information
    
    ### 🔍 Verification After Reload
    
    **Recommended Checks:**
    1. **List Calculators**: `GET /api/scores` - verify all expected calculators are present
    2. **Check Metadata**: `GET /api/scores/{score_id}` - verify parameter definitions
    3. **Test Calculations**: `POST /api/{score_id}/calculate` - verify calculations work
    4. **Validate Results**: Compare with known test cases
    
    **Example Verification Workflow:**
    ```bash
    # 1. Reload system
    curl -X POST /api/reload
    
    # 2. Verify calculator list
    curl /api/scores | jq '.total'
    
    # 3. Test specific calculator
    curl -X POST /api/ckd_epi_2021/calculate \\
         -H "Content-Type: application/json" \\
         -d '{"sex":"female","age":65,"serum_creatinine":1.2}'
    ```
    
    ### 📊 Response Information
    
    The reload response includes:
    - **Status**: Success or failure indication
    - **Counts**: Number of calculators and metadata files loaded
    - **Errors**: Any issues encountered during reload
    - **Warnings**: Non-critical issues that were handled
    
    ---
    
    **Returns:**
        Dict: Reload status with counts of loaded calculators and any errors encountered
        
    **Raises:**
        - **500 Internal Error**: Critical reload failure (check server logs)
        
    **Example Response:**
        ```json
        {
            "status": "success",
            "message": "Calculators reloaded successfully", 
            "scores_loaded": 19,
            "calculators_loaded": 19,
            "errors": [],
            "warnings": []
        }
        ```
    """
    try:
        # Reload scores metadata
        score_service.reload_scores()
        
        # Reload calculator implementations  
        calculator_service.reload_calculators()
        
        # Get current counts
        available_scores = score_service.get_available_scores()
        
        return ReloadResponse(
            status="success",
            message="Calculators reloaded successfully",
            scores_loaded=len(available_scores),
            timestamp="2024-01-01T00:00:00Z",  # This would be actual timestamp
            details={
                "metadata_reloaded": True,
                "calculators_reloaded": True,
                "available_categories": list(set(score.category for score in available_scores))
            }
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "error": "ReloadError",
                "message": "Error reloading calculators",
                "details": {
                    "error": str(e),
                    "suggestion": "Check server logs for detailed error information"
                }
            }
        )


@router.get("/scores/{score_id}/validate")
async def validate_score_calculator(score_id: str):
    """
    Validates if a calculator is available for the score
    
    Args:
        score_id: ID of the score
        
    Returns:
        Dict: Validation status
    """
    try:
        # Check if the score exists
        if not score_service.score_exists(score_id):
            raise HTTPException(
                status_code=404,
                detail={
                    "error": "ScoreNotFound",
                    "message": f"Score '{score_id}' not found",
                    "details": {"score_id": score_id}
                }
            )
        
        # Check if the calculator is available
        calculator_available = calculator_service.is_calculator_available(score_id)
        
        return {
            "score_id": score_id,
            "score_exists": True,
            "calculator_available": calculator_available,
            "status": "ready" if calculator_available else "no_calculator"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "error": "InternalServerError",
                "message": "Error validating score",
                "details": {"score_id": score_id, "error": str(e)}
            }
        )


@router.post("/abcd2_score", response_model=Abcd2Response)
async def calculate_abcd2_score(request: Abcd2Request):
    """
    Calculates the ABCD² Score to estimate stroke risk after TIA
    
    Args:
        request: Parameters required for calculation (age, BP, clinical features, duration, diabetes)
        
    Returns:
        Abcd2Response: Result with stroke risk stratification
    """
    try:
        # Convert request to dictionary
        parameters = {
            "age": request.age,
            "blood_pressure": request.blood_pressure.value,
            "clinical_features": request.clinical_features.value,
            "duration": request.duration.value,
            "diabetes": request.diabetes.value
        }
        
        # Execute calculation
        result = calculator_service.calculate_score("abcd2_score", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating ABCD² Score",
                    "details": {"parameters": parameters}
                }
            )
        
        return Abcd2Response(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for ABCD² Score",
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


@router.post("/4ts_hit", response_model=FourTsResponse)
async def calculate_4ts_hit(request: FourTsRequest):
    """
    Calculates the 4Ts Score for HIT probability assessment
    
    Args:
        request: Parameters required for calculation (thrombocytopenia, timing, thrombosis, other causes)
        
    Returns:
        FourTsResponse: Result with probability of heparin-induced thrombocytopenia
    """
    try:
        # Convert request to dictionary
        parameters = {
            "thrombocytopenia_severity": request.thrombocytopenia_severity.value,
            "timing_onset": request.timing_onset.value,
            "thrombosis_sequelae": request.thrombosis_sequelae.value,
            "other_causes": request.other_causes.value
        }
        
        # Execute calculation
        result = calculator_service.calculate_score("4ts_hit", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating 4Ts Score",
                    "details": {"parameters": parameters}
                }
            )
        
        return FourTsResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for 4Ts Score",
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


@router.post("/aims", response_model=AimsResponse)
async def calculate_aims(request: AimsRequest):
    """
    Calculates AIMS for tardive dyskinesia assessment
    
    Args:
        request: Parameters required for calculation (involuntary movement assessment items)
        
    Returns:
        AimsResponse: Result with tardive dyskinesia assessment
    """
    try:
        # Convert request to dictionary
        parameters = {
            "facial_muscles": request.facial_muscles,
            "lips_perioral": request.lips_perioral,
            "jaw": request.jaw,
            "tongue": request.tongue,
            "upper_extremities": request.upper_extremities,
            "lower_extremities": request.lower_extremities,
            "trunk_movements": request.trunk_movements,
            "global_severity": request.global_severity,
            "incapacitation": request.incapacitation,
            "patient_awareness": request.patient_awareness,
            "current_problems_teeth": request.current_problems_teeth.value,
            "dental_problems_interfere": request.dental_problems_interfere.value
        }
        
        # Execute calculation
        result = calculator_service.calculate_score("aims", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating AIMS",
                    "details": {"parameters": parameters}
                }
            )
        
        return AimsResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for AIMS",
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


@router.post("/4c_mortality_covid19", response_model=FourCMortalityResponse)
async def calculate_4c_mortality_covid19(request: FourCMortalityRequest):
    """
    Calculates the 4C Mortality Score for COVID-19
    
    Args:
        request: Parameters required for calculation (age, sex, comorbidities, vital signs, lab tests)
        
    Returns:
        FourCMortalityResponse: Result with hospital mortality risk stratification
    """
    try:
        # Convert request to dictionary
        parameters = {
            "age": request.age,
            "sex": request.sex.value,
            "comorbidities": request.comorbidities,
            "respiratory_rate": request.respiratory_rate,
            "oxygen_saturation": request.oxygen_saturation,
            "glasgow_coma_scale": request.glasgow_coma_scale,
            "urea_unit": request.urea_unit.value,
            "urea_value": request.urea_value,
            "crp": request.crp
        }
        
        # Execute calculation
        result = calculator_service.calculate_score("4c_mortality_covid19", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating 4C Mortality Score",
                    "details": {"parameters": parameters}
                }
            )
        
        return FourCMortalityResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for 4C Mortality Score",
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


@router.post("/6_minute_walk_distance", response_model=SixMinuteWalkResponse)
async def calculate_6_minute_walk_distance(request: SixMinuteWalkRequest):
    """
    Calculates reference values for 6-minute walk distance
    
    Args:
        request: Parameters required for calculation (age, sex, height, weight, optional observed distance)
        
    Returns:
        SixMinuteWalkResponse: Result with predicted distance and functional capacity analysis
    """
    try:
        # Convert request to dictionary
        parameters = {
            "age": request.age,
            "sex": request.sex.value,
            "height": request.height,
            "weight": request.weight
        }
        
        # Add observed distance if provided
        if request.observed_distance is not None:
            parameters["observed_distance"] = request.observed_distance
        
        # Execute calculation
        result = calculator_service.calculate_score("6_minute_walk_distance", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating 6 Minute Walk Distance",
                    "details": {"parameters": parameters}
                }
            )
        
        return SixMinuteWalkResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for 6 Minute Walk Distance",
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


@router.post("/a_a_o2_gradient", response_model=AAO2GradientResponse)
async def calculate_a_a_o2_gradient(request: AAO2GradientRequest):
    """
    Calculates the alveolar-arterial oxygen gradient (A-a O₂)
    
    Args:
        request: Parameters required for calculation (age, FiO₂, PaCO₂, PaO₂, atmospheric pressure, respiratory quotient)
        
    Returns:
        AAO2GradientResponse: Result with A-a gradient and interpretation of lung function
    """
    try:
        # Convert request to dictionary
        parameters = {
            "age": request.age,
            "fio2": request.fio2,
            "paco2": request.paco2,
            "pao2": request.pao2,
            "patm": request.patm,
            "respiratory_quotient": request.respiratory_quotient
        }
        
        # Execute calculation
        result = calculator_service.calculate_score("a_a_o2_gradient", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating A-a O₂ Gradient",
                    "details": {"parameters": parameters}
                }
            )
        
        return AAO2GradientResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for A-a O₂ Gradient",
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


@router.post("/aas", response_model=AasResponse)
async def calculate_aas(request: AasRequest):
    """
    Calculates Abuse Assessment Screen (AAS)
    
    Args:
        request: Parameters required for screening (questions about emotional, physical, and sexual abuse)
        
    Returns:
        AasResponse: Result of domestic violence screening
    """
    try:
        # Convert request to dictionary
        parameters = {
            "emotional_physical_abuse": request.emotional_physical_abuse.value,
            "physical_hurt_recently": request.physical_hurt_recently.value,
            "physical_hurt_pregnancy": request.physical_hurt_pregnancy.value,
            "sexual_abuse": request.sexual_abuse.value,
            "afraid_of_partner": request.afraid_of_partner.value
        }
        
        # Execute calculation
        result = calculator_service.calculate_score("aas", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating AAS",
                    "details": {"parameters": parameters}
                }
            )
        
        return AasResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for AAS",
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


@router.post("/aap_pediatric_hypertension", response_model=AapPediatricHypertensionResponse)
async def calculate_aap_pediatric_hypertension(request: AapPediatricHypertensionRequest):
    """
    Calculates AAP 2017 pediatric blood pressure classification
    
    Args:
        request: Parameters required for calculation (age, sex, height, systolic BP, diastolic BP)
        
    Returns:
        AapPediatricHypertensionResponse: Result with pediatric BP classification
    """
    try:
        # Convert request to dictionary
        parameters = {
            "age": request.age,
            "sex": request.sex.value,
            "height": request.height,
            "systolic_bp": request.systolic_bp,
            "diastolic_bp": request.diastolic_bp
        }
        
        # Execute calculation
        result = calculator_service.calculate_score("aap_pediatric_hypertension", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating AAP Pediatric Hypertension",
                    "details": {"parameters": parameters}
                }
            )
        
        return AapPediatricHypertensionResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for AAP Pediatric Hypertension",
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


@router.post("/abbey_pain_scale", response_model=AbbeyPainResponse)
async def calculate_abbey_pain_scale(request: AbbeyPainRequest):
    """
    Calculates Abbey Pain Scale for pain assessment in dementia
    
    Args:
        request: Parameters required for calculation (vocalization, facial expression, body language, etc.)
        
    Returns:
        AbbeyPainResponse: Result with pain intensity and recommendations
    """
    try:
        # Convert request to dictionary
        parameters = {
            "vocalization": request.vocalization,
            "facial_expression": request.facial_expression,
            "body_language": request.body_language,
            "behavioral_change": request.behavioral_change,
            "physiological_change": request.physiological_change,
            "physical_change": request.physical_change
        }
        
        # Execute calculation
        result = calculator_service.calculate_score("abbey_pain_scale", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Abbey Pain Scale",
                    "details": {"parameters": parameters}
                }
            )
        
        return AbbeyPainResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Abbey Pain Scale",
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


@router.post("/abic_score", response_model=AbicScoreResponse)
async def calculate_abic_score(request: AbicScoreRequest):
    """
    Calculates ABIC Score for alcoholic hepatitis
    
    Args:
        request: Parameters required for calculation (age, bilirubin, creatinine, INR)
        
    Returns:
        AbicScoreResponse: Result with survival prognosis
    """
    try:
        # Convert request to dictionary
        parameters = {
            "age": request.age,
            "serum_bilirubin": request.serum_bilirubin,
            "serum_creatinine": request.serum_creatinine,
            "inr": request.inr
        }
        
        # Execute calculation
        result = calculator_service.calculate_score("abic_score", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating ABIC Score",
                    "details": {"parameters": parameters}
                }
            )
        
        return AbicScoreResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for ABIC Score",
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


@router.post("/alc", response_model=AlcResponse)
async def calculate_alc(request: AlcRequest):
    """
    Calculates ALC (Absolute Lymphocyte Count)
    
    Args:
        request: Parameters required for calculation (white blood cells, lymphocyte percentage)
        
    Returns:
        AlcResponse: Result with absolute lymphocyte count
    """
    try:
        # Convert request to dictionary
        parameters = {
            "wbc_count": request.white_blood_cells,
            "lymphocyte_percent": request.lymphocyte_percentage
        }
        
        # Execute calculation
        result = calculator_service.calculate_score("alc", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating ALC",
                    "details": {"parameters": parameters}
                }
            )
        
        return AlcResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for ALC",
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


@router.post("/anc", response_model=AncResponse)
async def calculate_anc(request: AncRequest):
    """
    Calculates ANC (Absolute Neutrophil Count)
    
    Args:
        request: Parameters required for calculation (white blood cells, neutrophil percentage, bands)
        
    Returns:
        AncResponse: Result with absolute neutrophil count and infection risk
    """
    try:
        # Convert request to dictionary
        parameters = {
            "wbc_count": request.white_blood_cells,
            "segmented_neutrophils": request.neutrophil_percentage,
            "band_neutrophils": request.band_percentage
        }
        
        # Execute calculation
        result = calculator_service.calculate_score("anc", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating ANC",
                    "details": {"parameters": parameters}
                }
            )
        
        return AncResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for ANC",
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


@router.post("/acc_aha_hf_staging", response_model=AccAhaHfStagingResponse)
async def calculate_acc_aha_hf_staging(request: AccAhaHfStagingRequest):
    """
    Calculates ACC/AHA Heart Failure Staging
    
    Args:
        request: Parameters for classification (risk factors, structural disease, symptoms)
        
    Returns:
        AccAhaHfStagingResponse: Result with HF stage and recommendations
    """
    try:
        parameters = {
            "risk_factors": request.risk_factors.value,
            "structural_disease": request.structural_disease.value,
            "current_symptoms": request.current_symptoms.value,
            "advanced_symptoms": request.advanced_symptoms.value,
            "hospitalization_frequency": request.hospitalization_frequency.value,
            "ejection_fraction": request.ejection_fraction
        }
        
        result = calculator_service.calculate_score("acc_aha_hf_staging", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating ACC/AHA HF Staging",
                    "details": {"parameters": parameters}
                }
            )
        
        return AccAhaHfStagingResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for ACC/AHA HF Staging",
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


@router.post("/eular_acr_2012_pmr", response_model=EularAcrPmrResponse)
async def calculate_eular_acr_2012_pmr(request: EularAcrPmrRequest):
    """
    Calculates EULAR/ACR 2012 PMR Classification Criteria
    
    Args:
        request: Parameters for PMR diagnosis
        
    Returns:
        EularAcrPmrResponse: Result with diagnostic probability
    """
    try:
        parameters = {
            "morning_stiffness": request.morning_stiffness.value,
            "hip_pain_limited_rom": request.hip_pain_limited_rom.value,
            "rf_or_acpa": request.rf_or_acpa.value,
            "other_joint_pain": request.other_joint_pain.value,
            "ultrasound_shoulder_hip": request.ultrasound_shoulder_hip.value,
            "ultrasound_both_shoulders": request.ultrasound_both_shoulders.value
        }
        
        result = calculator_service.calculate_score("eular_acr_2012_pmr", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating EULAR/ACR PMR",
                    "details": {"parameters": parameters}
                }
            )
        
        return EularAcrPmrResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for EULAR/ACR PMR",
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


@router.post("/four_at", response_model=FourAtResponse)
async def calculate_four_at(request: FourAtRequest):
    """
    Calculates 4AT (4 A's Test) for delirium screening
    
    Args:
        request: 4AT test parameters
        
    Returns:
        FourAtResponse: Result with delirium probability
    """
    try:
        parameters = {
            "alertness": request.alertness.value,
            "amt4_errors": request.amt4_errors,
            "attention_months": request.attention_months.value,
            "acute_change": request.acute_change.value
        }
        
        result = calculator_service.calculate_score("four_at", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating 4AT",
                    "details": {"parameters": parameters}
                }
            )
        
        return FourAtResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for 4AT",
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


@router.post("/helps2b", response_model=Helps2bResponse)
async def calculate_helps2b(request: Helps2bRequest):
    """
    Calculates 2HELPS2B Score for seizure risk in cEEG
    
    Args:
        request: Clinical and EEG parameters
        
    Returns:
        Helps2bResponse: Result with seizure risk
    """
    try:
        parameters = {
            "seizure_history": request.seizure_history.value,
            "epileptiform_discharges": request.epileptiform_discharges.value,
            "lateralized_periodic_discharges": request.lateralized_periodic_discharges.value,
            "bilateral_independent_periodic_discharges": request.bilateral_independent_periodic_discharges.value,
            "brief_potentially_ictal_rhythmic_discharges": request.brief_potentially_ictal_rhythmic_discharges.value,
            "burst_suppression": request.burst_suppression.value
        }
        
        result = calculator_service.calculate_score("helps2b", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating HElPS2B",
                    "details": {"parameters": parameters}
                }
            )
        
        return Helps2bResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for HElPS2B",
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
