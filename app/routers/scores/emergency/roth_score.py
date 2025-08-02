"""
Roth Score for Hypoxia Screening Router

Endpoint for calculating Roth Score hypoxia screening assessment.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.emergency.roth_score import (
    RothScoreRequest,
    RothScoreResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/roth_score",
    response_model=RothScoreResponse,
    summary="Calculate Roth Score for Hypoxia Screening",
    description="Calculates the Roth Score for hypoxia screening using a simple verbal counting test. "
                "This bedside assessment tool evaluates respiratory distress by measuring how high a patient "
                "can count from 1 to 30 in a single breath and the total time elapsed. Originally developed "
                "for telemedicine applications, the Roth Score provides risk stratification for hypoxia when "
                "pulse oximetry may not be immediately available. The test demonstrates 91% sensitivity for "
                "detecting oxygen saturation <95% when maximum count is <10 numbers, and 87% sensitivity for "
                "oxygen saturation <90% when maximum count is <7 numbers. Results categorize patients into "
                "four risk levels from low risk (normal respiratory function) to high risk (severe respiratory "
                "distress requiring immediate intervention). Particularly useful in emergency department triage, "
                "telemedicine consultations, pandemic screening situations, and resource-limited settings where "
                "rapid respiratory assessment is needed.",
    response_description="Roth Score hypoxia screening assessment with risk stratification and clinical management recommendations",
    operation_id="roth_score"
)
async def calculate_roth_score(request: RothScoreRequest):
    """
    Roth Score for Hypoxia Screening Assessment
    
    Calculates the Roth Score using verbal counting performance to screen for hypoxia 
    in dyspneic patients. This validated bedside tool provides rapid risk stratification 
    when pulse oximetry may not be immediately available, particularly valuable in 
    telemedicine consultations, emergency department triage, and pandemic screening situations.
    
    Clinical Background and Validation:
    The Roth Score was developed as a simple, non-invasive screening tool for hypoxia 
    detection using verbal counting performance. The original validation study by Chorin 
    et al. (2016) demonstrated strong correlation between counting ability and oxygen 
    saturation levels in 93 patients with various respiratory conditions.
    
    Test Methodology and Administration:
    The Roth Score assessment requires patients to take a deep breath and count aloud 
    from 1 to 30 as fast as possible without stopping. Healthcare providers record both 
    the maximum number reached before the patient needs to breathe and the total time 
    elapsed during the counting attempt. This dual-parameter approach enhances the 
    sensitivity and specificity of hypoxia detection.
    
    Performance Characteristics and Clinical Validation:
    
    Sensitivity for Oxygen Saturation Detection:
    - Maximum count <10 numbers: 91% sensitive for O2 saturation <95%
    - Maximum count <7 numbers: 87% sensitive for O2 saturation <90%
    - Total time <7 seconds: 83% sensitive for O2 saturation <95%
    - Total time <5 seconds: 82% sensitive for O2 saturation <90%
    
    Risk Stratification Framework:
    The Roth Score categorizes patients into four distinct risk levels based on 
    counting performance and time duration, providing structured clinical decision-making 
    support for healthcare providers across various clinical settings.
    
    High Risk for Hypoxia (Emergency Priority):
    - Maximum count <7 numbers OR total time <5 seconds
    - Indicates severe respiratory distress with high probability of O2 saturation <90%
    - Requires immediate pulse oximetry measurement and clinical evaluation
    - Consider emergency oxygen supplementation and urgent respiratory assessment
    - May warrant hospital admission for monitoring and treatment of underlying pathology
    
    Moderate to High Risk (Close Monitoring):
    - Maximum count 7-9 numbers OR total time 5-7 seconds
    - Suggests moderate respiratory compromise with risk for O2 saturation <95%
    - Pulse oximetry measurement recommended for confirmation of oxygen status
    - Clinical assessment for underlying respiratory conditions and monitoring required
    - Consider oxygen supplementation based on clinical presentation and pulse oximetry results
    
    Low to Moderate Risk (Clinical Correlation):
    - Maximum count ≥10 numbers but total time <7 seconds
    - Indicates mild respiratory compromise requiring clinical correlation
    - Pulse oximetry should be performed to confirm adequate oxygenation
    - Continue monitoring and evaluate for underlying respiratory conditions
    - Outpatient management may be appropriate with close follow-up
    
    Low Risk (Routine Monitoring):
    - Maximum count ≥10 numbers AND total time ≥7 seconds
    - Demonstrates good respiratory reserve with normal counting ability
    - Low probability of significant hypoxia, though pulse oximetry remains gold standard
    - Evaluate other potential causes of dyspnea if symptoms persist
    - Routine follow-up appropriate based on overall clinical presentation
    
    Clinical Applications and Use Cases:
    
    Emergency Department Triage:
    - Rapid initial assessment of respiratory distress severity
    - Risk stratification for patients presenting with dyspnea or respiratory complaints
    - Objective tool for resident training and standardized assessment protocols
    - Supports clinical decision-making for admission versus discharge planning
    
    Telemedicine and Remote Consultations:
    - Enables respiratory assessment when physical examination is not possible
    - Particularly valuable during pandemic situations requiring social distancing
    - Allows family members or caregivers to perform assessment under provider guidance
    - Supports remote monitoring of patients with chronic respiratory conditions
    
    Resource-Limited Settings:
    - Provides hypoxia screening when pulse oximetry equipment is unavailable
    - Useful in rural or developing healthcare environments with limited resources
    - Enables screening in field conditions or disaster response situations
    - Cost-effective assessment tool requiring no additional equipment
    
    Home Health and Urgent Care:
    - Supports assessment in home health visits and community clinic settings
    - Enables monitoring of progression in ambulatory patients with respiratory symptoms
    - Provides objective data for healthcare provider communication and documentation
    - Assists in determining need for emergency department referral
    
    Important Clinical Considerations and Limitations:
    
    Test Administration Factors:
    - Patient should be in comfortable seated position or usual position of comfort
    - Clear instructions and demonstration may improve test reliability
    - Allow one practice attempt if patient is unfamiliar with the counting test
    - Avoid coaching or prompting during the actual assessment
    - Record ambient conditions and patient cooperation level
    
    Factors Affecting Test Performance:
    - Language barriers may significantly impact counting performance and accuracy
    - Vocal cord pathology or laryngeal disorders may affect voice production
    - Cognitive impairment or confusion may limit patient understanding and cooperation
    - Anxiety or pain may affect patient effort and concentration during testing
    - Baseline respiratory function and chronic conditions influence interpretation
    
    Clinical Context and Integration:
    - Results should be interpreted within the broader clinical context
    - Does NOT replace comprehensive clinical evaluation or pulse oximetry measurement
    - Consider patient's baseline functional status and chronic respiratory conditions
    - Validate findings with objective measurements when available
    - Use as screening tool in conjunction with clinical judgment and other assessments
    
    Validation Limitations and Evidence Gaps:
    - Original validation study limited to 93 patients in single healthcare system
    - Limited validation in pediatric populations (original study ≥16 years)
    - Variable performance reported across different languages and cultural contexts
    - May be less reliable in patients with chronic compensated respiratory conditions
    - Requires additional validation in diverse patient populations and healthcare settings
    
    Quality Assurance and Documentation:
    - Ensure consistent test administration technique across healthcare providers
    - Document factors that may affect test performance or interpretation
    - Record both counting parameters and correlate with pulse oximetry when available
    - Consider repeat testing if results are inconsistent with clinical presentation
    - Provide patient education about test results and follow-up recommendations
    
    Integration with Clinical Decision-Making:
    The Roth Score serves as a valuable screening tool that complements traditional 
    clinical assessment methods, providing objective data to support respiratory 
    evaluation and risk stratification. When integrated appropriately into clinical 
    workflows, it enhances provider confidence in decision-making while supporting 
    optimal resource utilization and patient safety outcomes.
    
    Args:
        request: Roth Score assessment parameters including counting performance and time
        
    Returns:
        RothScoreResponse: Risk assessment with detailed clinical interpretation and management recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("roth_score", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Roth Score for hypoxia screening",
                    "details": {"parameters": parameters}
                }
            )
        
        return RothScoreResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Roth Score assessment",
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
                "message": "Internal error in Roth Score hypoxia screening assessment",
                "details": {"error": str(e)}
            }
        )