"""
Edmonton Obesity Staging System (EOSS) Router

Endpoint for calculating EOSS obesity health impact assessment.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.endocrinology.edmonton_obesity_staging_system import (
    EdmontonObesityStagingSystemRequest,
    EdmontonObesityStagingSystemResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post("/edmonton_obesity_staging_system", response_model=EdmontonObesityStagingSystemResponse)
async def calculate_edmonton_obesity_staging_system(request: EdmontonObesityStagingSystemRequest):
    """
    Calculates Edmonton Obesity Staging System (EOSS)
    
    The Edmonton Obesity Staging System (EOSS) stratifies the presence and severity of 
    obesity-related health impairments across medical, functional, and psychological domains 
    to guide treatment decisions and predict outcomes. This system moves beyond traditional 
    BMI classification to provide a comprehensive assessment of obesity-related health impacts.
    
    Clinical Background and Rationale:
    
    Traditional obesity classification relies primarily on BMI, which has limitations as it 
    doesn't account for the actual health impact of obesity on individual patients. The EOSS 
    addresses this limitation by evaluating three key domains:
    
    1. Medical Risk Factors and Comorbidities:
       - Assesses presence and severity of obesity-related diseases
       - Ranges from subclinical risk factors to end-stage disease
       - Includes conditions like diabetes, hypertension, sleep apnea, and cardiovascular disease
    
    2. Physical Symptoms and Functional Limitations:
       - Evaluates impact on activities of daily living
       - Assesses physical symptoms related to obesity
       - Considers functional capacity and quality of life
    
    3. Psychological Symptoms and Mental Health Impact:
       - Evaluates psychological impact of obesity
       - Assesses mental health symptoms and quality of life
       - Considers social and emotional functioning
    
    Staging Algorithm:
    Each domain is scored from 0-4, with the final EOSS stage determined by the highest 
    stage rating across all three domains. This approach ensures that significant 
    impairment in any domain is reflected in the overall staging.
    
    Clinical Validation and Outcomes:
    - EOSS stages correlate with mortality risk independent of BMI
    - Stage 2 patients have HR 1.57 for death (95% CI 1.16-2.13)
    - Stage 3 patients have HR 2.69 for death (95% CI 1.98-3.67)
    - Clear survival curve divergence when stratified by EOSS stage
    - More predictive of health outcomes than obesity class alone
    
    Clinical Applications:
    - Treatment planning and resource allocation
    - Bariatric surgery candidacy assessment
    - Prognosis estimation beyond BMI
    - Communication of obesity-related health risks
    - Research and epidemiological studies
    
    Treatment Implications by Stage:
    - Stage 0: Prevention focus, lifestyle counseling
    - Stage 1: Intensive lifestyle interventions, risk factor monitoring
    - Stage 2: Comprehensive obesity treatment, pharmacotherapy consideration
    - Stage 3: Aggressive management, bariatric surgery evaluation
    - Stage 4: Most aggressive interventions, palliative care considerations
    
    Implementation Guidelines:
    - Use in conjunction with BMI, not as replacement
    - Requires comprehensive clinical assessment
    - Regular reassessment recommended as health status may change
    - Most effective when integrated into comprehensive obesity care
    - Particularly valuable for treatment intensity decisions
    
    Quality Improvement and Healthcare Planning:
    - Helps standardize obesity care approaches
    - Supports evidence-based treatment decisions
    - Facilitates appropriate resource allocation
    - Improves communication between healthcare providers
    - Supports quality metrics for obesity care programs
    
    Research Applications:
    - Obesity outcomes research
    - Treatment effectiveness studies
    - Healthcare utilization analysis
    - Population health assessment
    - Clinical trial stratification
    
    Args:
        request: EOSS assessment parameters across three domains (medical, physical, psychological)
        
    Returns:
        EdmontonObesityStagingSystemResponse: EOSS stage with clinical interpretation and management recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("edmonton_obesity_staging_system", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Edmonton Obesity Staging System",
                    "details": {"parameters": parameters}
                }
            )
        
        return EdmontonObesityStagingSystemResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Edmonton Obesity Staging System",
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