"""
Veterans Aging Cohort Study (VACS) 2.0 Index Router

Endpoint for calculating VACS 2.0 Index to estimate 5-year all-cause mortality 
risk in patients with HIV.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.infectious_disease.vacs_2_0_index import (
    Vacs20IndexRequest,
    Vacs20IndexResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/vacs_2_0_index",
    response_model=Vacs20IndexResponse,
    summary="Calculate Veterans Aging Cohort Study (VACS) 2.0 Index",
    description="Calculates the Veterans Aging Cohort Study (VACS) 2.0 Index to estimate 5-year all-cause mortality risk in patients with HIV. This validated prognostic tool combines HIV-specific biomarkers (CD4 count, viral load) with general health indicators and composite measures of organ system injury (FIB-4 for liver function, eGFR for kidney function) to provide comprehensive risk assessment. Version 2.0 represents an improvement over the original VACS Index with enhanced discrimination and incorporates additional biomarkers including albumin, white blood cell count, and body mass index. The index has been validated across international HIV cohorts and demonstrates superior performance compared to indices using only CD4 count and viral load. Score ranges from 0-164 points with mortality risk approximately doubling for every 10-unit increase. Clinical applications include risk stratification for intensive monitoring, treatment planning, prognosis communication, and quality improvement in HIV care programs.",
    response_description="The calculated VACS 2.0 Index score with risk stratification, component score breakdown, composite biomarkers (FIB-4 and eGFR), mortality risk estimation, and comprehensive clinical management recommendations",
    operation_id="vacs_2_0_index"
)
async def calculate_vacs_2_0_index(request: Vacs20IndexRequest):
    """
    Calculates Veterans Aging Cohort Study (VACS) 2.0 Index for HIV mortality prediction
    
    The Veterans Aging Cohort Study (VACS) 2.0 Index is a validated prognostic tool that 
    estimates 5-year all-cause mortality risk in patients with HIV. Developed through 
    analysis of one of the largest observational cohorts of HIV-infected individuals, 
    this enhanced version incorporates additional biomarkers for improved discrimination 
    and generalizability.
    
    **CLINICAL SIGNIFICANCE:**
    
    **Risk Assessment Components:**
    - **Age**: Most influential factor (27-point range)
    - **Albumin**: Second most influential (26-point range)
    - **HIV-specific markers**: CD4 count, viral load
    - **Organ system injury**: FIB-4 (liver), eGFR (kidney)
    - **General health**: Hemoglobin, WBC, BMI
    - **Co-infections**: Hepatitis C status
    
    **Composite Biomarkers:**
    - **FIB-4**: (Age × AST) / (Platelets × √ALT) - liver fibrosis indicator
    - **eGFR**: CKD-EPI equation - kidney function assessment
    
    **Score Interpretation:**
    - **0-25 points**: Low risk - routine care and monitoring
    - **26-50 points**: Moderate risk - enhanced monitoring recommended  
    - **51-75 points**: High risk - intensive management needed
    - **76+ points**: Very high risk - aggressive interventions required
    
    **Mortality Risk Model:**
    - Baseline: Score 38 = 1% 5-year mortality risk
    - Exponential relationship: risk doubles every 10 points
    - Validated C-statistic: 0.83 for 5-year mortality
    
    **Clinical Applications:**
    - **Risk Stratification**: Identify high-risk patients requiring intensive care
    - **Treatment Planning**: Guide therapy intensity and monitoring frequency
    - **Prognosis Communication**: Evidence-based mortality risk discussions
    - **Quality Improvement**: Standardized assessment for HIV programs
    
    **Version 2.0 Enhancements:**
    - Improved discrimination across patient subgroups
    - Enhanced generalizability beyond veteran populations
    - Additional biomarkers: albumin, WBC count, BMI
    - Better calibration for mortality prediction
    
    **Important Considerations:**
    - Should complement clinical judgment, not replace evaluation
    - Requires regular laboratory monitoring for accuracy
    - Score should be recalculated with updated values
    - Consider modifiable risk factors in management planning
    
    **Validation:**
    - Validated across multiple international HIV cohorts
    - Superior performance compared to CD4/viral load alone
    - Consistent discrimination across diverse populations
    - Established in clinical practice guidelines
    
    Args:
        request: VACS 2.0 Index parameters including demographics, HIV markers, 
                laboratory values, and co-infection status
        
    Returns:
        Vacs20IndexResponse: Risk score with interpretation, component breakdown, 
        composite biomarkers, and clinical recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("vacs_2_0_index", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating VACS 2.0 Index",
                    "details": {"parameters": parameters}
                }
            )
        
        # Add clinical recommendations based on score
        score = result.get("result", 0)
        result["clinical_recommendations"] = _generate_clinical_recommendations(score)
        result["important_considerations"] = _generate_important_considerations()
        
        return Vacs20IndexResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for VACS 2.0 Index",
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
                "message": "Internal error in VACS 2.0 Index calculation",
                "details": {"error": str(e)}
            }
        )


def _generate_clinical_recommendations(score: float) -> dict:
    """Generate clinical recommendations based on VACS 2.0 score"""
    
    if score <= 25:
        return {
            "monitoring_frequency": "Routine monitoring recommended",
            "interventions": [
                "Continue current antiretroviral therapy if virally suppressed",
                "Maintain routine HIV care schedule",
                "Implement standard preventive care measures",
                "Monitor for treatment adherence"
            ],
            "follow_up": [
                "Reassess VACS score annually or with significant clinical changes",
                "Monitor CD4 count and viral load every 6 months if stable",
                "Annual comprehensive metabolic panel",
                "Age-appropriate cancer screening and cardiovascular risk assessment"
            ],
            "counseling_points": [
                "Excellent prognosis with current management",
                "Emphasize importance of continued medication adherence",
                "Discuss healthy lifestyle maintenance",
                "Regular follow-up to maintain optimal health"
            ]
        }
    elif score <= 50:
        return {
            "monitoring_frequency": "Enhanced monitoring recommended",
            "interventions": [
                "Optimize antiretroviral therapy for viral suppression",
                "Address modifiable risk factors (nutrition, substance use)",
                "Implement age-appropriate preventive care",
                "Monitor for treatment-related complications"
            ],
            "follow_up": [
                "Reassess VACS score every 6-12 months",
                "Monitor CD4 count and viral load every 3-6 months",
                "Annual comprehensive metabolic panel and liver function tests",
                "Consider specialist referrals for significant comorbidities"
            ],
            "counseling_points": [
                "Discuss importance of medication adherence",
                "Review lifestyle modifications for risk reduction",
                "Provide education on HIV progression and prognosis",
                "Address any concerns about life expectancy"
            ]
        }
    elif score <= 75:
        return {
            "monitoring_frequency": "Intensive monitoring required",
            "interventions": [
                "Aggressive optimization of antiretroviral therapy",
                "Comprehensive management of all comorbidities",
                "Consider multidisciplinary care team approach",
                "Implement intensive preventive interventions"
            ],
            "follow_up": [
                "Reassess VACS score every 3-6 months",
                "Monitor CD4 count and viral load every 3 months",
                "Quarterly comprehensive laboratory monitoring",
                "Regular specialist consultations as indicated"
            ],
            "counseling_points": [
                "Discuss elevated mortality risk and management strategies",
                "Emphasize critical importance of treatment adherence",
                "Review all modifiable risk factors intensively",
                "Consider advance directive discussions"
            ]
        }
    else:
        return {
            "monitoring_frequency": "Very intensive monitoring required",
            "interventions": [
                "Maximum optimization of all therapeutic interventions",
                "Multidisciplinary team management essential",
                "Consider experimental or compassionate use therapies",
                "Aggressive management of all comorbid conditions"
            ],
            "follow_up": [
                "Reassess VACS score every 3 months",
                "Monitor CD4 count and viral load monthly",
                "Monthly comprehensive laboratory and clinical assessment",
                "Frequent specialist consultations and care coordination"
            ],
            "counseling_points": [
                "Discuss very high mortality risk honestly and compassionately",
                "Explore patient goals and preferences for care",
                "Consider palliative care consultation for symptom management",
                "Support advance care planning and end-of-life discussions"
            ]
        }


def _generate_important_considerations() -> dict:
    """Generate important considerations for VACS 2.0 Index interpretation"""
    
    return {
        "validation": "Validated across international HIV cohorts with C-statistic of 0.83 for 5-year mortality prediction",
        "updates": "Version 2.0 represents significant improvement over original VACS Index with enhanced discrimination",
        "limitations": [
            "Developed primarily in male veteran populations",
            "Requires regular laboratory monitoring for accuracy",
            "Should complement clinical judgment, not replace comprehensive evaluation",
            "May not fully capture all mortality determinants in diverse populations"
        ],
        "modifiable_factors": [
            "HIV viral suppression through optimal antiretroviral therapy",
            "Nutritional status improvement (albumin, BMI optimization)",
            "Hepatitis C treatment if co-infected",
            "Management of kidney and liver disease",
            "Substance use disorder treatment",
            "Cardiovascular risk factor management"
        ],
        "reassessment": "Score should be recalculated with updated laboratory values every 3-12 months depending on risk level to track disease progression or improvement over time",
        "clinical_context": "Use in conjunction with clinical judgment, patient preferences, and social determinants of health for comprehensive care planning"
    }