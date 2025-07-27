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
    ErrorResponse
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
    Lists all available medical scores in the API
    
    Args:
        category: Optional - filter by medical category
        search: Optional - search by term in title or description
        
    Returns:
        ScoreListResponse: List of available scores
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
    Gets the complete metadata of a specific score
    
    Args:
        score_id: ID of the score
        
    Returns:
        ScoreMetadataResponse: Detailed metadata of the score
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
    Calculates the Estimated Glomerular Filtration Rate using the CKD-EPI 2021 equation
    
    Args:
        request: Parameters required for calculation (sex, age, serum creatinine)
        
    Returns:
        CKDEpi2021Response: Calculation result with clinical interpretation
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
    Generic endpoint to calculate any available score
    
    Args:
        score_id: ID of the score to be calculated
        parameters: Dictionary with the parameters required for calculation
        
    Returns:
        Dict: Calculation result with interpretation
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
        if not calculator_service.is_calculator_available(score_id):
            raise HTTPException(
                status_code=501,
                detail={
                    "error": "CalculatorNotImplemented",
                    "message": f"Calculator for '{score_id}' not yet implemented",
                    "details": {"score_id": score_id}
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
                    "details": {"parameters": parameters}
                }
            )
        
        return result
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": f"Invalid parameters for {score_id}",
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


@router.get("/categories")
async def list_categories():
    """
    Lists available medical categories
    
    Returns:
        Dict: List of unique categories
    """
    try:
        scores = score_service.get_available_scores()
        categories = list(set(score.category for score in scores))
        categories.sort()
        
        return {
            "categories": categories,
            "total": len(categories)
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "error": "InternalServerError",
                "message": "Error listing categories",
                "details": {"error": str(e)}
            }
        )


@router.post("/reload")
async def reload_scores():
    """
    Reloads all scores and calculators in the system
    (Useful for development and updates)
    
    Returns:
        Dict: Status of the reload operation
    """
    try:
        # Reload scores and calculators
        score_service.reload_scores()
        calculator_service.reload_calculators()
        
        # Count how many scores were loaded
        scores = score_service.get_available_scores()
        
        return {
            "status": "success",
            "message": "Scores and calculators reloaded successfully",
            "scores_loaded": len(scores),
            "scores": [score.id for score in scores]
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "error": "InternalServerError", 
                "message": "Error reloading scores",
                "details": {"error": str(e)}
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
