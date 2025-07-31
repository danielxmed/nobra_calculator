"""
EVendo Score for Esophageal Varices Router

Endpoint for calculating EVendo Score to predict presence and size of esophageal varices 
prior to screening endoscopy in cirrhotic patients.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.gastroenterology.evendo_score import (
    EvendoScoreRequest,
    EvendoScoreResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/evendo_score",
    response_model=EvendoScoreResponse,
    summary="Calculate EVendo Score for Esophageal Varices",
    description="Predicts presence and size of esophageal varices prior to screening endoscopy in patients with cirrhosis. Helps identify patients who may safely defer endoscopic screening.",
    response_description="The calculated evendo score with interpretation",
    operation_id="evendo_score"
)
async def calculate_evendo_score(request: EvendoScoreRequest):
    """
    Calculates EVendo Score for Esophageal Varices
    
    The EVendo Score is a machine learning-derived tool that predicts the presence 
    and size of esophageal varices in patients with cirrhosis using readily 
    available laboratory values and clinical findings.
    
    Key Features:
    - Machine learning-derived (random forest algorithm)
    - Uses 6 readily available clinical parameters
    - Risk threshold: ≤3.90 = Low Risk, >3.90 = High Risk
    - High sensitivity (95.1%) and negative predictive value (95.8%)
    - Validated across multiple medical centers
    
    Formula Components:
    A = (8.5 × INR) + (AST / 35)
    B = (Platelet count / 150) + (BUN / 20) + (Hemoglobin / 15)
    EVendo Score = (A / B) + 1 (if ascites present)
    
    Clinical Parameters:
    
    International Normalized Ratio (INR):
    - Measures coagulation function and synthetic liver capacity
    - Normal range: 0.8-1.2, elevated in cirrhosis
    - Higher values indicate worse liver function
    - Reflects severity of liver synthetic dysfunction
    
    Aspartate Aminotransferase (AST):
    - Liver enzyme indicating hepatocellular injury
    - Normal range: 15-41 U/L
    - May be chronically elevated in cirrhosis
    - Reflects ongoing liver inflammation or damage
    
    Platelet Count:
    - Reflects portal hypertension severity
    - Normal range: 150-350 ×10³/µL
    - Thrombocytopenia common due to hypersplenism
    - Lower counts correlate with higher portal pressure
    
    Blood Urea Nitrogen (BUN):
    - Reflects renal function and volume status
    - Normal range: 8-20 mg/dL
    - May be elevated in hepatorenal syndrome
    - Indicates severity of liver disease complications
    
    Hemoglobin:
    - Reflects anemia common in cirrhosis
    - Normal range: 12-17 g/dL
    - May indicate GI bleeding or chronic disease
    - Lower levels suggest more advanced disease
    
    Ascites:
    - Clinical sign of portal hypertension
    - Binary variable: present or absent
    - Strong independent predictor of variceal presence
    - Detected by physical examination or imaging
    
    Risk Stratification and Management:
    
    Low Risk (Score ≤3.90):
    - Probability of esophageal varices: <5%
    - Sensitivity for varices needing treatment: 95.1%
    - Negative predictive value: 95.8%
    - Management: Expectant management, screening may be deferred
    - Follow-up: Routine clinical monitoring, reassess in 1-2 years
    - Clinical benefit: Spares 30.5% of patients from endoscopy
    
    High Risk (Score >3.90):
    - Probability of esophageal varices: ≥5%
    - Management: Endoscopic screening recommended
    - Timing: Should be performed within appropriate timeframe
    - Further evaluation: Assess varix size and bleeding risk
    - Primary prophylaxis: Consider based on findings
    
    Clinical Applications:
    - Screening tool for patients >18 years with known/suspected cirrhosis
    - Resource optimization through risk-based endoscopy
    - Patient-centered care with reduced unnecessary procedures
    - Quality improvement in cirrhosis management
    - Cost-effective healthcare delivery
    
    Model Development and Validation:
    - Developed using machine learning (random forest algorithm)
    - Training set: Large cohort of cirrhotic patients
    - Multi-center prospective validation
    - AUROC: 0.82-0.84 for detecting varices
    - Robust performance across different populations
    - Superior to clinical assessment alone
    
    Performance Characteristics:
    - Sensitivity: 95.1% for varices needing treatment
    - Negative predictive value: 95.8%
    - Would spare 30.5% of patients from endoscopy
    - Misses only 2.8% of varices needing treatment
    - Particularly effective in Child-Pugh A patients
    
    Important Contraindications:
    - Do not use in patients with overt GI bleeding
    - Not for patients with history of acute variceal hemorrhage
    - Should not delay urgent endoscopy when clinically indicated
    - Requires clinical judgment for borderline scores
    
    Advantages:
    - Uses routinely available laboratory values
    - No additional testing required
    - Machine learning-optimized performance
    - Multi-center validation
    - Simple calculation with online tools available
    - Cost-effective screening approach
    
    Clinical Decision Support:
    - Risk-based endoscopic screening strategy
    - Resource allocation optimization
    - Patient counseling about variceal risk
    - Quality improvement in cirrhosis care
    - Standardized approach to screening decisions
    
    Comparison with Other Methods:
    - More accurate than clinical judgment alone
    - Complementary to Baveno VI criteria
    - Higher sensitivity than traditional ratios
    - Validated across diverse etiologies of cirrhosis
    - Superior performance in machine learning studies
    
    Healthcare System Benefits:
    - Reduces unnecessary endoscopic procedures
    - Optimizes resource utilization
    - Maintains high safety with excellent sensitivity
    - Standardizes screening approach
    - Supports value-based healthcare delivery
    - Improves patient satisfaction with risk-based care
    
    Future Considerations:
    - Ongoing validation in diverse populations
    - Integration with electronic health records
    - Combination with other non-invasive markers
    - Cost-effectiveness studies across healthcare systems
    - Refinement with additional variables as available
    
    Args:
        request: Parameters including INR, AST, platelet count, BUN, hemoglobin, and ascites status
        
    Returns:
        EvendoScoreResponse: Score, risk level, probability of varices, and management recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("evendo_score", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating EVendo Score",
                    "details": {"parameters": parameters}
                }
            )
        
        return EvendoScoreResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for EVendo Score",
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