from fastapi import APIRouter, HTTPException
from datetime import datetime
import logging

from app.models.scores.pulmonology.airq import AIRQRequest, AIRQResponse, AIRQResult
from calculators.airq import calculate_airq

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/airq", response_model=AIRQResponse, summary="Calculate AIRQ Score")
async def calculate_airq_score(request: AIRQRequest) -> AIRQResponse:
    """
    Calculate the Asthma Impairment and Risk Questionnaire (AIRQ) score.
    
    The AIRQ is a validated 10-item questionnaire that assesses both symptom impairment 
    (7 items, 2-week recall) and exacerbation risk (3 items, 12-month recall) in patients 
    aged 12 years and older with asthma.
    
    **Clinical Use:**
    - Validated for patients aged 12+ years with physician-diagnosed asthma
    - Combines impairment and risk domains for comprehensive assessment
    - ROC AUC 0.94 for identifying well-controlled vs not well-/very poorly controlled
    - Cut-point ≥2 has sensitivity 0.90 and specificity 0.79
    - Cut-point ≥5 has specificity 0.95 (very poorly controlled)
    
    **Score Interpretation:**
    - 0-1 points: Well-controlled asthma
    - 2-4 points: Not well-controlled asthma  
    - 5-10 points: Very poorly controlled asthma
    
    **Parameters (all yes/no questions):**
    
    *Impairment Domain (past 2 weeks):*
    - daytime_symptoms: Symptoms bothering during day on >4 days
    - nighttime_awakenings: Woken from sleep >1 time
    - activity_limitation: Limited daily activities every day
    - rescue_medication_daily: Used rescue inhaler/nebulizer every day
    - social_activity_limitation: Limited social activities
    - exercise_limitation: Limited ability to exercise
    - difficult_control: Felt difficult to control asthma
    
    *Risk Domain (past 12 months):*
    - oral_steroids: Took steroid pills/shots
    - emergency_visits: ED or unplanned healthcare visits
    - hospitalization: Hospital stay overnight
    
    **Returns:**
    - Total AIRQ score (0-10)
    - Control category and interpretation
    - Domain-specific scores
    - Clinical recommendations
    - Validation notes
    """
    
    try:
        logger.info("Calculating AIRQ score")
        
        # Calculate the AIRQ score using the calculator function
        result_dict = calculate_airq(
            daytime_symptoms=request.daytime_symptoms.value,
            nighttime_awakenings=request.nighttime_awakenings.value,
            activity_limitation=request.activity_limitation.value,
            rescue_medication_daily=request.rescue_medication_daily.value,
            social_activity_limitation=request.social_activity_limitation.value,
            exercise_limitation=request.exercise_limitation.value,
            difficult_control=request.difficult_control.value,
            oral_steroids=request.oral_steroids.value,
            emergency_visits=request.emergency_visits.value,
            hospitalization=request.hospitalization.value
        )
        
        # Create the result model
        result = AIRQResult(**result_dict)
        
        # Create the response
        response = AIRQResponse(
            calculator_name="AIRQ",
            version="2020",
            timestamp=datetime.now().isoformat(),
            inputs=request,
            result=result
        )
        
        logger.info(f"AIRQ calculation completed successfully. Score: {result.airq_score}")
        return response
        
    except ValueError as e:
        logger.error(f"Validation error in AIRQ calculation: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Validation error: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error in AIRQ calculation: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error during AIRQ calculation")

@router.get("/airq/info", summary="Get AIRQ Calculator Information")
async def get_airq_info():
    """
    Get detailed information about the Asthma Impairment and Risk Questionnaire (AIRQ).
    
    Returns comprehensive information about the calculator including:
    - Description and clinical use
    - Validation data and performance metrics
    - Scoring methodology
    - Interpretation guidelines
    - References
    """
    
    return {
        "calculator_name": "Asthma Impairment and Risk Questionnaire (AIRQ)",
        "version": "2020",
        "description": "Validates asthma control in patients 12 years and older by assessing both symptom impairment and exacerbation risk domains",
        "category": "pulmonology",
        "indication": "Assessment of asthma control in patients aged 12+ years with physician-diagnosed asthma",
        "methodology": {
            "type": "Questionnaire-based assessment",
            "questions": 10,
            "domains": [
                {
                    "name": "Impairment Domain",
                    "questions": 7,
                    "timeframe": "Past 2 weeks",
                    "focus": "Symptom burden and functional limitations"
                },
                {
                    "name": "Risk Domain", 
                    "questions": 3,
                    "timeframe": "Past 12 months",
                    "focus": "Exacerbations and healthcare utilization"
                }
            ],
            "scoring": "Sum of 'yes' responses (0-10 points)"
        },
        "interpretation": {
            "categories": [
                {
                    "score": "0-1",
                    "category": "Well-controlled",
                    "description": "Well-controlled asthma",
                    "risk_level": "Low"
                },
                {
                    "score": "2-4", 
                    "category": "Not well-controlled",
                    "description": "Not well-controlled asthma",
                    "risk_level": "Moderate"
                },
                {
                    "score": "5-10",
                    "category": "Very poorly controlled", 
                    "description": "Very poorly controlled asthma",
                    "risk_level": "High"
                }
            ]
        },
        "validation": {
            "population": "Patients aged 12+ years with physician-diagnosed asthma",
            "performance_metrics": [
                "ROC AUC 0.94 for identifying well-controlled vs not well-/very poorly controlled",
                "ROC AUC 0.93 for identifying well-/not well-controlled vs very poorly controlled",
                "Sensitivity 0.90 and specificity 0.79 for cut-point ≥2",
                "Specificity 0.95 for cut-point ≥5 (very poorly controlled)"
            ],
            "reliability": "High internal consistency and test-retest reliability",
            "construct_validity": "Strong correlation with established asthma control measures"
        },
        "clinical_utility": [
            "Comprehensive assessment combining impairment and risk",
            "Validated cut-points for clinical decision-making",
            "Suitable for routine clinical practice",
            "Predictive of future exacerbation risk",
            "Useful for monitoring treatment response"
        ],
        "references": [
            "Murphy KR, Chipps B, Beuther DA, et al. Development of the Asthma Impairment and Risk Questionnaire (AIRQ): a composite control measure. J Allergy Clin Immunol Pract. 2020;8(7):2263-2274.e5.",
            "Beuther DA, Murphy KR, Zeiger RS, et al. The Asthma Impairment and Risk Questionnaire (AIRQ) Control Level Predicts Future Risk of Asthma Exacerbations. J Allergy Clin Immunol Pract. 2022;10(12):3204-3212.e2."
        ],
        "limitations": [
            "Designed for patients aged 12+ years only",
            "Requires physician-diagnosed asthma",
            "Based on patient self-report",
            "May not capture all aspects of asthma control",
            "Should be used as part of comprehensive clinical assessment"
        ]
    }
