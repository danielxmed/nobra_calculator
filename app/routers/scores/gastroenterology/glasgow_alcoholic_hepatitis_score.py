"""
Glasgow Alcoholic Hepatitis Score (GAHS) Router

Endpoint for calculating Glasgow Alcoholic Hepatitis Score for mortality prediction.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.gastroenterology.glasgow_alcoholic_hepatitis_score import (
    GlasgowAlcoholicHepatitisScoreRequest,
    GlasgowAlcoholicHepatitisScoreResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/glasgow_alcoholic_hepatitis_score",
    response_model=GlasgowAlcoholicHepatitisScoreResponse,
    summary="Calculate Glasgow Alcoholic Hepatitis Score (GAHS)",
    description="Prognostic score for mortality prediction in patients with alcoholic hepatitis using five clinical variables: age, white blood cell count, urea, prothrombin time ratio, and bilirubin. More accurate than the modified Discriminant Function for predicting 28-day mortality",
    response_description="The calculated glasgow alcoholic hepatitis score with interpretation",
    operation_id="glasgow_alcoholic_hepatitis_score"
)
async def calculate_glasgow_alcoholic_hepatitis_score(request: GlasgowAlcoholicHepatitisScoreRequest):
    """
    Calculates Glasgow Alcoholic Hepatitis Score (GAHS)
    
    The Glasgow Alcoholic Hepatitis Score is a prognostic tool that predicts mortality 
    in patients with alcoholic hepatitis using five clinical variables. This score 
    provides superior prognostic accuracy compared to other established scoring systems 
    and helps identify patients who would benefit from corticosteroid therapy.
    
    **Clinical Context and Significance**:
    
    **Primary Purpose**: 
    Mortality prediction in patients with alcoholic hepatitis to facilitate evidence-based 
    treatment decisions, particularly regarding corticosteroid therapy initiation and 
    intensive care resource allocation in hepatology and gastroenterology practice.
    
    **Key Clinical Advantages**:
    
    **Superior Prognostic Accuracy**:
    - More accurate than modified Discriminant Function (81% vs 49% overall accuracy)
    - Sensitivity of 81% on day 1, improving to 93% on day 7 for predicting 28-day outcomes
    - Specificity of 61% on day 1, improving to 68% on day 7
    - Consistent performance across different patient populations and healthcare settings
    
    **Comprehensive Disease Assessment**:
    - Incorporates multiple organ systems (hepatic, renal, coagulation, inflammatory)
    - First alcoholic hepatitis score to include inflammatory parameter (white blood cell count)
    - Reflects disease severity through readily available laboratory parameters
    - Accounts for both acute illness severity and patient factors (age)
    
    **Clinical Decision Support Framework**:
    - Clear treatment threshold at GAHS ≥9 for corticosteroid therapy indication
    - Risk stratification guides monitoring intensity and resource allocation
    - Prognostic counseling support for patients and families
    - Clinical trial enrollment and stratification applications
    
    **Evidence-Based Risk Stratification**:
    
    **Low Risk (GAHS 5-8)**:
    - 28-day survival of approximately 87% with supportive care alone
    - No demonstrated benefit from corticosteroid therapy
    - Standard supportive care with focus on alcohol cessation and nutritional support
    - Regular monitoring for disease progression but less intensive intervention
    
    **High Risk (GAHS 9-12)**:
    - 28-day survival of 46% without treatment, improving to 78% with corticosteroids
    - Strong indication for corticosteroid therapy unless contraindicated
    - Intensive monitoring and multidisciplinary care coordination required
    - Consider liver transplant evaluation for appropriate candidates
    
    **Clinical Implementation Applications**:
    
    **Treatment Decision Making**:
    - Corticosteroid therapy initiation based on evidence-based risk stratification
    - Identification of patients requiring intensive monitoring and advanced care
    - Resource allocation decisions for hepatology specialty services and ICU care
    - Early involvement of palliative care services for high-risk patients
    
    **Monitoring and Assessment**:
    - Serial scoring to monitor disease progression and treatment response
    - Integration with other assessment tools (Lille score) for comprehensive evaluation
    - Quality improvement metrics for alcoholic hepatitis care programs
    - Clinical pathway standardization for evidence-based treatment protocols
    
    **Research and Quality Applications**:
    - Clinical trial stratification and patient selection criteria
    - Outcome prediction modeling and healthcare resource planning
    - Comparative effectiveness research for alcoholic hepatitis treatments
    - Provider education and competency assessment in hepatology care
    
    **Quality Improvement Integration**:
    - Standardized risk assessment protocols across healthcare organizations
    - Performance metrics for alcoholic hepatitis care quality and outcomes
    - Resource utilization optimization based on prognostic risk categories
    - Clinical decision support system integration for real-time scoring
    
    Args:
        request: Clinical parameters including age, white blood cell count, urea, 
                prothrombin time ratio, and bilirubin for comprehensive mortality 
                risk assessment in alcoholic hepatitis
        
    Returns:
        GlasgowAlcoholicHepatitisScoreResponse: GAHS score with detailed prognostic 
                                              interpretation, evidence-based treatment 
                                              recommendations, and comprehensive clinical 
                                              guidance based on validated mortality 
                                              outcomes from extensive validation studies
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("glasgow_alcoholic_hepatitis_score", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Glasgow Alcoholic Hepatitis Score",
                    "details": {"parameters": parameters}
                }
            )
        
        return GlasgowAlcoholicHepatitisScoreResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Glasgow Alcoholic Hepatitis Score calculation",
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
                "message": "Internal error in Glasgow Alcoholic Hepatitis Score calculation",
                "details": {"error": str(e)}
            }
        )