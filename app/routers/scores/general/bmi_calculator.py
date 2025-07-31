"""
BMI Calculator Router

Endpoint for calculating Body Mass Index (BMI) and Body Surface Area (BSA).
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.general.bmi_calculator import (
    BmiCalculatorRequest,
    BmiCalculatorResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/bmi_calculator",
    response_model=BmiCalculatorResponse,
    summary="Calculate BMI Calculator (Body Mass Index and BSA)",
    description="Calculates body mass index (BMI) and body surface area (BSA) to assess weight appropriateness and determine medication dosages. BMI provides a quick screening tool for weight-related health risks, while BSA is used for calculating drug dosages and cardiac index measurements.",
    response_description="The calculated bmi calculator with interpretation",
    operation_id="bmi_calculator"
)
async def calculate_bmi_calculator(request: BmiCalculatorRequest):
    """
    Calculates Body Mass Index (BMI) and Body Surface Area (BSA)
    
    This comprehensive anthropometric calculator computes two fundamental measurements 
    used extensively in clinical practice and research. The calculator provides accurate 
    BMI classification according to World Health Organization standards and BSA calculation 
    using the validated Mosteller formula.
    
    **Body Mass Index (BMI) Calculation:**
    
    **Formula:** BMI = weight (kg) / [height (m)]²
    
    BMI is calculated by dividing the patient's weight in kilograms by the square of 
    their height in meters. This measurement serves as a standardized screening tool 
    for weight-related health risks and provides classification into clinically 
    meaningful categories.
    
    **WHO BMI Classification System:**
    
    **Underweight (<18.5 kg/m²):**
    - **Clinical Significance:** May indicate malnutrition, eating disorders, or underlying medical conditions
    - **Associated Risks:** Increased mortality, compromised immune function, osteoporosis risk
    - **Clinical Actions:** Nutritional assessment, screening for eating disorders, evaluation for underlying diseases
    - **Follow-up:** Monitor weight gain progress, address nutritional deficiencies
    
    **Normal Weight (18.5-24.9 kg/m²):**
    - **Clinical Significance:** Optimal weight range associated with lowest health risks
    - **Associated Benefits:** Reduced risk of cardiovascular disease, diabetes, and metabolic syndrome
    - **Clinical Actions:** Maintain current lifestyle and dietary habits
    - **Follow-up:** Routine health maintenance and periodic weight monitoring
    
    **Overweight (25.0-29.9 kg/m²):**
    - **Clinical Significance:** Increased risk of chronic diseases and cardiovascular complications
    - **Associated Risks:** Hypertension, type 2 diabetes, dyslipidemia, sleep apnea
    - **Clinical Actions:** Lifestyle counseling, dietary modifications, increased physical activity
    - **Follow-up:** Regular monitoring, consider referral to nutritionist or weight management program
    
    **Obese Class 1 (30.0-34.9 kg/m²):**
    - **Clinical Significance:** Moderate obesity with significantly increased health risks
    - **Associated Conditions:** Cardiovascular disease, diabetes, joint problems, cancer risk
    - **Clinical Actions:** Comprehensive weight management, medical monitoring, behavioral interventions
    - **Follow-up:** Intensive lifestyle intervention, consider pharmacotherapy consultation
    
    **Obese Class 2 (35.0-39.9 kg/m²):**
    - **Clinical Significance:** Severe obesity requiring intensive medical intervention
    - **Associated Complications:** High risk of cardiovascular events, diabetes complications, mobility issues
    - **Clinical Actions:** Intensive medical management, multidisciplinary approach, bariatric surgery evaluation
    - **Follow-up:** Close medical supervision, comprehensive comorbidity management
    
    **Obese Class 3 (≥40.0 kg/m²):**
    - **Clinical Significance:** Extreme obesity with very high mortality and morbidity risk
    - **Life-threatening Conditions:** Severe cardiovascular disease, respiratory failure, mobility limitations
    - **Clinical Actions:** Immediate intensive intervention, bariatric surgery consultation, specialized care
    - **Follow-up:** Multidisciplinary team management, preparation for surgical intervention if appropriate
    
    **Body Surface Area (BSA) Calculation:**
    
    **Mosteller Formula:** BSA (m²) = √[height (cm) × weight (kg) / 3600]
    
    The Mosteller formula is the most widely used method for BSA calculation in clinical practice. 
    Developed in 1987, it provides accurate estimates that correlate well with more complex formulas 
    while being simple to calculate and widely validated across diverse patient populations.
    
    **Clinical Applications of BSA:**
    
    **Oncology and Chemotherapy:**
    - **Primary Use:** Most chemotherapy agents are dosed based on BSA rather than weight
    - **Rationale:** BSA correlates better with organ function and drug metabolism than weight alone
    - **Typical Range:** Adult BSA typically ranges from 1.5-2.5 m²
    - **Safety Considerations:** BSA caps may be applied to prevent overdosing in very large patients
    
    **Cardiac Index Calculations:**
    - **Formula:** Cardiac Index = Cardiac Output (L/min) / BSA (m²)
    - **Normal Range:** 2.5-4.0 L/min/m² for healthy adults
    - **Clinical Use:** Assessment of cardiac function independent of body size
    - **Applications:** Critical care monitoring, cardiac catheterization studies
    
    **Physiological Research:**
    - **Metabolism Studies:** BSA correlates with basal metabolic rate and energy expenditure
    - **Drug Development:** Pharmacokinetic modeling and dose-finding studies
    - **Exercise Physiology:** Normalization of oxygen consumption and cardiac output
    
    **Burn Treatment:**
    - **Surface Area Assessment:** Calculation of burn percentage relative to total body surface area
    - **Fluid Resuscitation:** BSA-based formulas for fluid replacement in burn patients
    - **Skin Grafting:** Planning and quantification of graft requirements
    
    **Advanced Clinical Considerations:**
    
    **BMI Limitations and Adjustments:**
    
    **Population-Specific Considerations:**
    - **Asian Populations:** Lower BMI thresholds may be appropriate (overweight ≥23, obese ≥25)
    - **Elderly Patients:** Higher BMI may be protective against mortality (obesity paradox)
    - **Athletes:** High muscle mass may result in elevated BMI without increased health risk
    - **Children:** Age and sex-specific percentiles used instead of adult categories
    
    **Body Composition Factors:**
    - **Muscle Mass:** Resistance training and athletic populations may have high BMI with low body fat
    - **Bone Density:** Variations in skeletal mass affect weight independent of adiposity
    - **Hydration Status:** Fluid retention or dehydration can temporarily alter BMI calculations
    - **Ethnic Variations:** Different body composition patterns across ethnic groups
    
    **BSA Calculation Alternatives:**
    
    **Du Bois Formula:** BSA = 0.007184 × height^0.725 × weight^0.425
    - **Historical Significance:** Original BSA formula developed in 1916
    - **Accuracy:** Slightly more accurate than Mosteller but more complex to calculate
    - **Clinical Use:** Still used in some research applications and older protocols
    
    **Haycock Formula:** BSA = 0.024265 × height^0.3964 × weight^0.5378
    - **Pediatric Applications:** Often preferred for children and adolescents
    - **Accuracy:** Good correlation with actual measured BSA in pediatric populations
    - **Limitations:** Less validated in adult populations compared to Mosteller
    
    **Clinical Integration and Quality Assurance:**
    
    **Documentation Requirements:**
    - **Measurement Standardization:** Consistent measurement techniques for height and weight
    - **Equipment Calibration:** Regular calibration of scales and height measurement devices
    - **Recording Accuracy:** Precise documentation to nearest 0.1 kg and 0.5 cm
    - **Timing Considerations:** Consistent timing of measurements relative to meals and clothing
    
    **Interpretation Guidelines:**
    - **Clinical Context:** Always interpret BMI and BSA within broader clinical assessment
    - **Trend Analysis:** Serial measurements more valuable than single point-in-time values
    - **Risk Stratification:** Combine with other risk factors for comprehensive assessment
    - **Patient Communication:** Sensitive discussion of weight and health implications
    
    **Technology Integration:**
    - **Electronic Health Records:** Automated calculation and trend tracking
    - **Clinical Decision Support:** Alerts and reminders for screening and follow-up
    - **Population Health:** Aggregate data analysis for quality improvement initiatives
    - **Research Applications:** Standardized data collection for clinical studies
    
    Args:
        request: BMI calculation parameters (weight in kg, height in cm)
        
    Returns:
        BmiCalculatorResponse: BMI and BSA results with clinical interpretation
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("bmi_calculator", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating BMI and BSA",
                    "details": {"parameters": parameters}
                }
            )
        
        return BmiCalculatorResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for BMI calculation",
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