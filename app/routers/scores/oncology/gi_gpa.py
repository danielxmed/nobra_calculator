"""
Graded Prognostic Assessment for Gastrointestinal Cancer (GI-GPA) Router

Endpoint for calculating GI-GPA score.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.oncology.gi_gpa import (
    GiGpaRequest,
    GiGpaResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/gi_gpa",
    response_model=GiGpaResponse,
    summary="Calculate Graded Prognostic Assessment for Gastrointestin...",
    description="Estimates survival in patients with gastrointestinal cancers and brain metastases. Uses 4 prognostic factors to provide risk stratification and guide treatment decisions for patients with brain metastases from GI cancers.",
    response_description="The calculated gi gpa with interpretation",
    operation_id="calculate_gi_gpa"
)
async def calculate_gi_gpa(request: GiGpaRequest):
    """
    Calculates Graded Prognostic Assessment for Gastrointestinal Cancer (GI-GPA)
    
    The GI-GPA is a validated prognostic tool specifically designed for patients with 
    gastrointestinal cancers who develop brain metastases. This scoring system provides 
    crucial information for treatment planning and prognostic discussions in a patient 
    population with historically challenging outcomes.
    
    **Clinical Background**:
    Brain metastases occur in 10-20% of patients with gastrointestinal cancers, representing 
    a devastating complication with median survival of approximately 8 months. However, 
    survival varies significantly based on patient and disease characteristics, making 
    prognostic stratification essential for optimal care.
    
    **Scoring System (4 Prognostic Factors)**:
    The GI-GPA uses four key prognostic factors, each contributing specific point values:
    
    **Age Categories**:
    - Under 60 years: 0.5 points (better prognosis)
    - 60 years or over: 0.0 points (standard reference)
    
    **Karnofsky Performance Status (KPS)**:
    - KPS <80: 0.0 points (poor functional status)
    - KPS 80: 1.0 point (moderate functional status)  
    - KPS 90-100: 2.0 points (excellent functional status)
    
    **Extracranial Metastases**:
    - Present: 0.0 points (advanced systemic disease)
    - Absent: 0.5 points (brain-only metastatic disease)
    
    **Number of Brain Metastases**:
    - >3 brain metastases: 0.0 points (extensive intracranial disease)
    - 2-3 brain metastases: 0.5 points (moderate intracranial disease)
    - 1 brain metastasis: 1.0 point (limited intracranial disease)
    
    **Survival Outcomes and Treatment Implications**:
    - **Poor Prognosis (0-1.0 points, 3 months)**: Focus on comfort care and symptom palliation
    - **Intermediate-Poor (1.5-2.0 points, 9 months)**: Consider limited interventions, palliative radiation
    - **Intermediate (2.5-3.0 points, 12 months)**: Consider radiation therapy, selective surgical intervention
    - **Good Prognosis (3.5-4.0 points, 17 months)**: Consider aggressive multimodal therapy, clinical trials
    
    **Key Clinical Applications**:
    - Treatment selection (aggressive multimodal therapy vs. palliative care)
    - Prognostic communication with evidence-based survival estimates
    - Clinical trial stratification for research studies
    - Resource allocation and appropriate level of care determination
    - Multidisciplinary treatment planning coordination
    
    **Important Clinical Considerations**:
    - Developed from multi-institutional cohort of 845 patients with GI cancers and brain metastases
    - Applicable to various GI cancer types (colorectal, gastric, esophageal, hepatobiliary)
    - Score ranges from 0.0 (worst prognosis) to 4.0 (best prognosis)
    - Over 30% of patients present in the worst prognostic group (GI-GPA ≤1.0)
    - Should complement, not replace, clinical judgment and patient preferences
    - Free online calculator available at brainmetgpa.com for clinical reference
    
    Args:
        request: GI-GPA parameters including age, KPS, extracranial metastases, and number of brain metastases
        
    Returns:
        GiGpaResponse: GI-GPA score with prognostic category and treatment recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("gi_gpa", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating GI-GPA Score",
                    "details": {"parameters": parameters}
                }
            )
        
        return GiGpaResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for GI-GPA Score",
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