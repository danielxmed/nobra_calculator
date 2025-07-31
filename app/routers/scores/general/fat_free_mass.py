"""
Fat Free Mass (FFM) Router

Endpoint for calculating Fat Free Mass using body weight and BMI for clinical applications.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.general.fat_free_mass import (
    FatFreeMassRequest,
    FatFreeMassResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/fat_free_mass",
    response_model=FatFreeMassResponse,
    summary="Calculate Fat Free Mass (FFM)",
    description="Calculates the predictive value of fat-free mass from body weight and body mass index (BMI). Useful for weight-based medication dosing, especially in anesthesia, and helps calculate body composition.",
    response_description="The calculated fat free mass with interpretation",
    operation_id="fat_free_mass"
)
async def calculate_fat_free_mass(request: FatFreeMassRequest):
    """
    Calculates Fat Free Mass (FFM) using the Janmahasatian formula
    
    The Fat Free Mass calculation estimates lean body weight from total body weight 
    and body mass index (BMI) using sex-specific formulas. This calculation is 
    particularly valuable for medication dosing and body composition assessment.
    
    Key Features:
    - Sex-specific formulas for improved accuracy
    - Validated for clinical pharmacology applications
    - Useful for anesthetic drug dosing
    - Body composition assessment tool
    - Simple calculation requiring only basic measurements
    
    Janmahasatian Formula:
    - Male: FFM = (9.27 × 10³ × Body Weight) / (6.68 × 10³ + 216 × BMI)
    - Female: FFM = (9.27 × 10³ × Body Weight) / (8.78 × 10³ + 244 × BMI)
    
    Clinical Parameters:
    
    Sex:
    - Biological sex affects body composition significantly
    - Men typically have higher muscle mass and lower body fat
    - Women have higher essential fat requirements
    - Formula coefficients optimized for each sex
    
    Body Weight:
    - Current accurate body weight in kilograms
    - Range: 10-300 kg (pediatric to morbidly obese)
    - Primary input for lean mass estimation
    - Should be recent and accurate measurement
    
    Body Mass Index (BMI):
    - Weight (kg) divided by height squared (m²)
    - Normal range: 18.5-24.9 kg/m²
    - Calculator valid for BMI 10-80 kg/m²
    - Critical for fat vs. lean mass distribution
    
    Clinical Applications:
    
    Medication Dosing:
    - Anesthetic Agents: Propofol, etomidate, thiopental
    - Neuromuscular Blockers: Rocuronium, vecuronium, atracurium
    - Reversal Agents: Sugammadex dosing optimization
    - Chemotherapy: Certain cytotoxic agents
    - Critical Care: Vasopressor and sedative dosing
    - Antimicrobials: Aminoglycosides, vancomycin
    
    Body Composition Assessment:
    - Nutritional assessment and planning
    - Metabolic rate calculations
    - Fitness and athletic performance evaluation
    - Sarcopenia screening and monitoring
    - Weight management program design
    
    Clinical Research:
    - Pharmacokinetic studies
    - Drug development and dosing optimization
    - Metabolic and nutritional research
    - Body composition intervention studies
    
    Advantages:
    - Does not require direct body fat measurement
    - More accurate than ideal body weight in obesity
    - Validated in clinical pharmacology studies
    - Simple calculation with readily available inputs
    - Sex-specific optimization improves accuracy
    - Cost-effective compared to imaging methods
    
    Typical Results:
    
    Normal Fat-Free Mass Percentages:
    - Men: 75-85% of body weight
      - Athletes: 80-90%
      - Average fitness: 75-85%
      - Low muscle mass: 65-75%
    
    - Women: 65-75% of body weight
      - Athletes: 70-80%
      - Average fitness: 65-75%
      - Low muscle mass: 55-65%
    
    Clinical Interpretation:
    
    High FFM (>85% men, >80% women):
    - Athletic build or high muscle mass
    - May require adjusted medication dosing
    - Excellent metabolic health indicator
    - Consider high protein requirements
    
    Normal FFM (75-85% men, 65-75% women):
    - Typical healthy body composition
    - Standard dosing protocols applicable
    - Balanced nutrition and exercise approach
    - Regular monitoring for age-related changes
    
    Low FFM (<75% men, <65% women):
    - Possible sarcopenia or high adiposity
    - Body composition improvement indicated
    - Adjusted medication dosing may be needed
    - Evaluate for underlying conditions
    
    Medication Dosing Benefits:
    - Reduces overdosing in obese patients
    - Improves drug efficacy and safety profiles
    - Accounts for altered drug distribution
    - More physiologically relevant than total weight
    - Minimizes adverse effects from inappropriate dosing
    
    Clinical Validation:
    - Originally validated against DEXA scanning
    - Superior performance in obese patients
    - Demonstrated accuracy for anesthetic dosing
    - Extensive use in pharmacokinetic research
    - Validated across diverse patient populations
    
    Important Limitations:
    - Predictive equation, not direct measurement
    - May be less accurate in extreme body compositions
    - Should complement clinical assessment
    - Not validated in all patient populations
    - Requires accurate weight and BMI inputs
    
    Quality Improvement Applications:
    - Standardized medication dosing protocols
    - Enhanced patient safety in anesthesia
    - Reduced medication errors in obesity
    - Improved clinical research accuracy
    - Better patient outcomes through precision dosing
    
    Future Applications:
    - Personalized medicine algorithms
    - Electronic health record integration
    - Point-of-care assessment tools
    - Population health management
    - Precision dosing decision support
    
    Args:
        request: Parameters including sex, body weight, and BMI
        
    Returns:
        FatFreeMassResponse: FFM calculation, body composition analysis, and clinical interpretation
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("fat_free_mass", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Fat Free Mass",
                    "details": {"parameters": parameters}
                }
            )
        
        return FatFreeMassResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Fat Free Mass calculation",
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