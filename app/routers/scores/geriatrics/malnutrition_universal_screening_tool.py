"""
Malnutrition Universal Screening Tool (MUST) Router

Endpoint for calculating MUST score for malnutrition risk assessment.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.geriatrics.malnutrition_universal_screening_tool import (
    MalnutritionUniversalScreeningToolRequest,
    MalnutritionUniversalScreeningToolResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/malnutrition_universal_screening_tool",
    response_model=MalnutritionUniversalScreeningToolResponse,
    summary="Calculate Malnutrition Universal Screening Tool (MUST)",
    description="Calculates the Malnutrition Universal Screening Tool (MUST) score, a validated screening "
                "tool developed by BAPEN in 2003 to identify adults who are malnourished or at risk of "
                "malnutrition. MUST uses three key indicators: BMI (≥20, 18.5-19.9, <18.5 kg/m²), recent "
                "unplanned weight loss (<5%, 5-10%, >10% in 3-6 months), and acute disease effects (no "
                "nutritional intake for >5 days). The tool provides systematic risk stratification into "
                "Low (0 points), Medium (1 point), or High (≥2 points) risk categories, each linked to "
                "specific evidence-based care pathways. MUST is widely implemented across UK healthcare "
                "settings including hospitals, care homes, and community services. Essential for identifying "
                "patients who would benefit from nutritional intervention, preventing complications of "
                "malnutrition, and optimizing clinical outcomes. The tool includes specific screening "
                "frequencies and clear action plans for each risk level, making it practical for routine "
                "clinical use by healthcare professionals.",
    response_description="The calculated MUST score with risk stratification and comprehensive nutritional care recommendations",
    operation_id="malnutrition_universal_screening_tool"
)
async def calculate_malnutrition_universal_screening_tool(request: MalnutritionUniversalScreeningToolRequest):
    """
    Calculates MUST score for comprehensive malnutrition risk assessment
    
    The Malnutrition Universal Screening Tool (MUST) is a validated, evidence-based screening
    tool that provides systematic identification of malnutrition risk in adult patients.
    
    Development and Validation:
    Developed by the British Association for Parenteral and Enteral Nutrition (BAPEN) in 2003,
    MUST underwent extensive validation studies demonstrating its effectiveness in identifying
    patients at nutritional risk across diverse healthcare settings. The tool has been validated
    in hospitals, care homes, and community settings with proven reliability and clinical utility.
    
    Clinical Applications and Settings:
    
    Hospital Settings:
    - Admission screening for all adult patients
    - Weekly re-screening during hospitalization
    - Pre-operative assessment and planning
    - Post-operative recovery monitoring
    - Discharge planning and transition of care
    
    Care Home Settings:
    - Admission assessment for new residents
    - Monthly ongoing screening for all residents
    - Monitoring during illness or medication changes
    - Annual comprehensive nutritional review
    - Integration with care planning processes
    
    Community Healthcare:
    - Primary care routine health assessments
    - Home healthcare nutritional screening
    - Outpatient clinic appointments
    - Annual screening for high-risk groups (>75 years)
    - Chronic disease management programs
    
    Three-Component Assessment System:
    
    1. Body Mass Index (BMI) Assessment:
       - Reflects current nutritional status
       - ≥20.0 kg/m²: 0 points (normal/overweight)
       - 18.5-19.9 kg/m²: 1 point (mild underweight)
       - <18.5 kg/m²: 2 points (significantly underweight)
       
       Clinical Considerations:
       - Use measured height and weight when possible
       - Consider alternative measurements if standard BMI cannot be obtained
       - Account for fluid retention or dehydration
       - Consider muscle mass in elderly patients
    
    2. Weight Loss Assessment:
       - Evaluates recent nutritional decline
       - <5% weight loss: 0 points (minimal concern)
       - 5-10% weight loss: 1 point (moderate concern)
       - >10% weight loss: 2 points (significant concern)
       
       Documentation Requirements:
       - Unplanned weight loss over past 3-6 months
       - Baseline weight comparison essential
       - Consider clothing and scales consistency
       - Note any contributing factors (illness, medication changes)
    
    3. Acute Disease Effect:
       - Assesses current impact on nutritional intake
       - No acute illness: 0 points
       - Acutely ill with no intake >5 days: 2 points
       
       Clinical Examples:
       - Post-operative patients unable to eat
       - Acute illness causing nausea/vomiting
       - Dysphagia affecting safe swallowing
       - Severe depression affecting appetite
       - Critical illness requiring intensive care
    
    Risk Stratification and Care Pathways:
    
    Low Risk (0 points):
    - Minimal malnutrition risk
    - Routine clinical care appropriate
    - Regular diet and normal food choices
    - Screening frequency: Weekly (hospital), Monthly (care home), Annually (community special groups)
    - Monitor for changes in condition or appetite
    - Document screening results in medical records
    
    Medium Risk (1 point):
    - Moderate malnutrition risk requiring monitoring
    - Document dietary intake for 3 consecutive days
    - Assess food preferences and barriers to eating
    - If improvement noted: Continue monitoring with reduced concern
    - If no improvement: Implement high-risk interventions
    - Screening frequency: Weekly (hospital), Monthly (care home/community)
    - Consider referral to dietitian if concerns persist
    
    High Risk (≥2 points):
    - Significant malnutrition risk requiring immediate intervention
    - Urgent referral to registered dietitian
    - Nutritional support team consultation
    - Implement local nutritional care protocols
    - Comprehensive nutritional assessment required
    - Increase overall nutritional intake through:
      * Food fortification and enrichment
      * Oral nutritional supplements
      * Modified texture diets if appropriate
      * Consider enteral nutrition if indicated
      * Parenteral nutrition in specific circumstances
    - Regular monitoring and care plan review
    - Screening frequency: Weekly (hospital), Monthly (care home/community)
    
    Implementation Considerations:
    
    Training and Competency:
    - All healthcare staff should receive MUST training
    - Competency assessment for accurate screening
    - Regular updates on nutritional care pathways
    - Documentation requirements and quality standards
    
    Quality Assurance:
    - Regular audit of screening completion rates
    - Monitoring of appropriate referrals and interventions
    - Outcome measurement for nutritional interventions
    - Integration with clinical governance processes
    
    Special Populations:
    
    Elderly Patients:
    - Consider multiple comorbidities affecting nutrition
    - Assess social factors and support systems
    - Evaluate medication effects on appetite
    - Screen for depression and cognitive impairment
    - Consider cultural and personal food preferences
    
    Post-Surgical Patients:
    - Enhanced protein and energy requirements
    - Wound healing nutritional needs
    - Potential complications affecting intake
    - Early mobilization and feeding protocols
    
    Chronic Disease Patients:
    - Disease-specific nutritional requirements
    - Medication interactions with nutrition
    - Progressive conditions requiring adapted care
    - Palliative care nutritional considerations
    
    Evidence Base and Outcomes:
    Multiple studies demonstrate that MUST implementation leads to:
    - Improved identification of malnourished patients
    - Reduced length of hospital stay
    - Decreased complications and readmissions
    - Cost-effective nutritional interventions
    - Better patient satisfaction and quality of life
    - Reduced mortality in high-risk patients
    
    Integration with Care Planning:
    - Links to local nutritional care protocols
    - Supports multidisciplinary team communication
    - Enables targeted resource allocation
    - Facilitates quality improvement initiatives
    - Supports clinical audit and research activities
    
    Args:
        request: MUST assessment parameters including BMI, weight loss, and acute disease effects
        
    Returns:
        MalnutritionUniversalScreeningToolResponse: Comprehensive malnutrition risk assessment with care recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("malnutrition_universal_screening_tool", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating MUST score",
                    "details": {"parameters": parameters}
                }
            )
        
        return MalnutritionUniversalScreeningToolResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for MUST calculation",
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
                "message": "Internal error in MUST calculation",
                "details": {"error": str(e)}
            }
        )