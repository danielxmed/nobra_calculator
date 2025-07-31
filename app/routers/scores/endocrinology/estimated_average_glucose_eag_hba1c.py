"""
Estimated Average Glucose (eAG) From HbA1C Router

Endpoint for calculating estimated average glucose from HbA1c values.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.endocrinology.estimated_average_glucose_eag_hba1c import (
    EstimatedAverageGlucoseEagHba1cRequest,
    EstimatedAverageGlucoseEagHba1cResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/estimated_average_glucose_eag_hba1c",
    response_model=EstimatedAverageGlucoseEagHba1cResponse,
    summary="Calculate Estimated Average Glucose (eAG) From HbA1C",
    description="Estimates average glucose level from Hemoglobin A1C value using the linear relationship established by the A1c-Derived Average Glucose (ADAG) Study Group.",
    response_description="The calculated estimated average glucose eag hba1c with interpretation",
    operation_id="estimated_average_glucose_eag_hba1c"
)
async def calculate_estimated_average_glucose_eag_hba1c(request: EstimatedAverageGlucoseEagHba1cRequest):
    """
    Calculates Estimated Average Glucose (eAG) From HbA1C
    
    The Estimated Average Glucose (eAG) calculation provides a way to translate 
    HbA1c values into estimated average glucose levels that correspond to everyday 
    glucose meter readings. This relationship was established by the A1c-Derived 
    Average Glucose (ADAG) Study Group using comprehensive continuous glucose 
    monitoring data.
    
    Historical Context and Clinical Significance:
    
    Development of the eAG Formula:
    The eAG concept was developed to bridge the gap between laboratory HbA1c values 
    and the glucose readings that patients see on their home monitors. Prior to this 
    development, patients and healthcare providers had difficulty relating HbA1c 
    percentages to daily glucose management.
    
    The ADAG Study Group conducted extensive research involving 507 adults, 268 
    children, and adolescents with type 1, type 2, and no diabetes. Participants 
    underwent frequent glucose monitoring and continuous glucose monitoring over 
    2-3 months, with HbA1c measurements performed using standardized methods.
    
    Mathematical Relationship:
    The linear relationship eAG (mg/dL) = (28.7 × HbA1c %) - 46.7 was derived 
    through rigorous statistical analysis with a correlation coefficient (r²) of 0.84. 
    This strong correlation demonstrates the reliability of the conversion across 
    diverse populations and glucose ranges.
    
    Clinical Applications and Benefits:
    
    Patient Education and Engagement:
    - Helps patients understand HbA1c results in familiar glucose units
    - Connects long-term control (HbA1c) with daily monitoring values
    - Facilitates diabetes self-management discussions
    - Provides context for treatment goals and lifestyle modifications
    
    Healthcare Provider Benefits:
    - Standardizes communication about glycemic control
    - Facilitates treatment decision-making
    - Supports individualized target setting
    - Enhances patient counseling effectiveness
    
    Diagnostic and Monitoring Applications:
    - Assists in diabetes diagnosis when combined with other criteria
    - Monitors treatment effectiveness over time
    - Guides therapy intensification decisions
    - Assesses risk for diabetes complications
    
    Clinical Interpretation Guidelines:
    
    Diagnostic Categories:
    - Normal: HbA1c <5.7% (eAG <117 mg/dL)
    - Prediabetes: HbA1c 5.7-6.4% (eAG 117-137 mg/dL)
    - Diabetes: HbA1c ≥6.5% (eAG ≥140 mg/dL)
    
    Treatment Targets for Diabetes:
    - General target: HbA1c <7% (eAG <154 mg/dL)
    - Stringent target: HbA1c <6.5% (eAG <140 mg/dL) if achievable safely
    - Less stringent: HbA1c <8% (eAG <183 mg/dL) for patients with comorbidities
    
    Important Clinical Considerations:
    
    Limitations and Accuracy Factors:
    - Individual variation exists in the HbA1c-glucose relationship
    - Conditions affecting red blood cell lifespan may alter accuracy
    - Hemoglobin variants can interfere with HbA1c measurement
    - Recent blood loss or transfusion may affect results
    - Iron deficiency and chronic kidney disease can influence values
    
    eAG vs. Glucose Meter Averages:
    The eAG is typically higher than the average of glucose meter readings because:
    - eAG reflects 24-hour glucose patterns including overnight periods
    - Patients often check glucose more frequently when levels are low
    - Post-meal glucose peaks are usually not captured in routine monitoring
    - Sleep-time glucose elevations are included in eAG calculations
    
    Integration with Modern Diabetes Care:
    
    Continuous Glucose Monitoring (CGM):
    - CGM data provides additional context to HbA1c and eAG values
    - Time-in-range metrics complement eAG information
    - Glucose variability assessment enhances clinical picture
    - Real-time data supports immediate management decisions
    
    Precision Medicine Applications:
    - Individual HbA1c-glucose relationships may vary
    - Genetic factors may influence glycation rates
    - Personalized targets based on individual characteristics
    - Integration with other biomarkers for comprehensive assessment
    
    Quality Assurance and Standardization:
    
    Laboratory Requirements:
    - HbA1c assays must be NGSP-certified and standardized
    - Point-of-care devices should meet accuracy requirements
    - Regular calibration and quality control essential
    - Interpretation should consider assay limitations
    
    Clinical Implementation:
    - Staff training on eAG concept and applications
    - Patient education materials and resources
    - Integration with electronic health records
    - Consistent use across healthcare teams
    
    Future Directions and Research:
    
    Emerging Technologies:
    - Advanced continuous glucose monitoring systems
    - Artificial intelligence for glucose prediction
    - Integration with digital health platforms
    - Personalized glucose management algorithms
    
    Research Areas:
    - Population-specific eAG relationships
    - Impact of new diabetes medications on eAG accuracy
    - Integration with other glycemic markers
    - Long-term outcomes prediction using eAG data
    
    The eAG calculation represents a significant advancement in diabetes care, 
    providing a bridge between laboratory values and patient experience. Its 
    integration into routine clinical practice has enhanced patient understanding, 
    improved communication between patients and providers, and supported more 
    effective diabetes management strategies.
    
    By translating complex laboratory values into familiar glucose units, the 
    eAG calculation has democratized diabetes care, making it more accessible 
    and understandable for patients while maintaining the scientific rigor 
    necessary for clinical decision-making.
    
    Args:
        request: eAG calculation parameters including HbA1c percentage
        
    Returns:
        EstimatedAverageGlucoseEagHba1cResponse: eAG value with clinical interpretation and management guidance
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("estimated_average_glucose_eag_hba1c", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating estimated average glucose",
                    "details": {"parameters": parameters}
                }
            )
        
        return EstimatedAverageGlucoseEagHba1cResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for eAG calculation",
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
                "message": "Internal error in eAG calculation",
                "details": {"error": str(e)}
            }
        )