"""
Kruis Score for Diagnosis of Irritable Bowel Syndrome (IBS) Router

Endpoint for calculating Kruis Score for IBS diagnosis in patients with gastrointestinal symptoms.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.gastroenterology.kruis_score_ibs import (
    KruisScoreIbsRequest,
    KruisScoreIbsResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/kruis_score_ibs",
    response_model=KruisScoreIbsResponse,
    summary="Calculate Kruis Score for Diagnosis of Irritable Bowel Syndrome (IBS)",
    description="Calculates the Kruis Score for IBS diagnosis using a validated scoring system "
                "that incorporates both positive symptoms and negative red flag indicators. "
                "Developed in 1984 by Kruis et al., this was one of the first objective scoring "
                "systems for IBS diagnosis and introduced the important concept of using laboratory "
                "parameters to differentiate IBS from organic gastrointestinal disease. The score "
                "evaluates symptoms (abdominal pain/flatulence/bowel irregularity, symptom duration "
                ">2 years, severe pain descriptors, alternating bowel habits) and red flags "
                "(abnormal physical findings, elevated ESR >10 mm/hr, elevated WBC >10,000/μL, "
                "anemia, history of blood in stool). Score ≥44 points suggests IBS diagnosis with "
                "81% sensitivity and 91% specificity. Any red flag present mandates investigation "
                "for organic disease regardless of total score. While largely superseded by Rome "
                "criteria in clinical practice, the Kruis Score remains valuable for systematic "
                "IBS assessment and provides objective laboratory criteria for diagnosis.",
    response_description="The calculated Kruis Score with IBS diagnostic assessment and clinical management recommendations",
    operation_id="kruis_score_ibs"
)
async def calculate_kruis_score_ibs(request: KruisScoreIbsRequest):
    """
    Calculates Kruis Score for Diagnosis of Irritable Bowel Syndrome (IBS)
    
    The Kruis Score for IBS diagnosis is a clinical scoring system developed in 1984 
    by Kruis et al. to differentiate irritable bowel syndrome from organic gastrointestinal 
    disease. It was one of the first validated scoring systems for IBS diagnosis and 
    introduced the revolutionary concept of incorporating both positive symptoms and 
    negative "red flag" indicators into a systematic diagnostic approach.
    
    Historical Context:
    Before the Kruis Score, IBS diagnosis was largely based on subjective clinical 
    assessment without standardized criteria. The Kruis system provided an objective, 
    reproducible method for IBS diagnosis that incorporated laboratory parameters, 
    setting the foundation for subsequent diagnostic criteria development including 
    the Manning criteria and eventually the Rome criteria.
    
    Scoring Components:
    
    Positive Symptoms (Add Points):
    - Symptoms of abdominal pain, flatulence, or bowel irregularity: +34 points
    - Symptom duration > 2 years: +16 points (emphasizes chronic nature of IBS)
    - Pain described as burning, cutting, very strong: +23 points (qualitative assessment)
    - Alternating constipation and diarrhea: +14 points (classic IBS pattern)
    
    Red Flags (Subtract Points):
    - Abnormal physical findings: -47 points (suggests organic disease)
    - ESR > 10 mm/hr: -13 points (indicates inflammation)
    - WBC > 10,000/μL: -50 points (suggests infection/inflammation)  
    - Low hemoglobin (F<12, M<14 g/dL): -98 points (indicates bleeding/chronic disease)
    - History of blood in stool: -98 points (strong indicator of organic pathology)
    
    Diagnostic Interpretation:
    - Score ≥ 44 points: IBS diagnosis likely (81% sensitivity, 91% specificity)
    - Score < 44 points: IBS diagnosis unlikely, consider organic disease evaluation
    
    Clinical Performance:
    The original validation study demonstrated excellent diagnostic accuracy:
    - Sensitivity: 81% (good detection of IBS cases)
    - Specificity: 91% (excellent exclusion of non-IBS cases)
    - The score effectively discriminated IBS from organic gastrointestinal disease
    - Combined with Manning criteria, achieved 80% sensitivity and 97% specificity
    
    Clinical Applications:
    - Systematic approach to IBS diagnosis in primary care and gastroenterology
    - Differentiation of functional vs. organic gastrointestinal disorders
    - Risk stratification for patients requiring further investigation
    - Research tool for IBS diagnosis standardization
    - Educational tool for understanding IBS diagnostic principles
    
    Red Flag Assessment:
    A critical feature of the Kruis Score is its emphasis on red flags that suggest 
    organic disease. Any red flag present requires investigation regardless of symptom 
    score, including:
    - Colonoscopy for bleeding, anemia, or concerning physical findings
    - Laboratory evaluation for elevated inflammatory markers
    - Imaging studies for abnormal physical examination findings
    - Age-appropriate cancer screening for relevant red flags
    
    Important Considerations:
    - Laboratory tests (CBC, ESR) are integral to the assessment
    - Chronic symptom duration (>2 years) strongly supports IBS diagnosis
    - Normal physical examination and laboratory values are expected in IBS
    - Red flags mandate organic disease exclusion before IBS diagnosis
    - The score may be less applicable to patients with recent symptom onset
    
    Clinical Limitations:
    - Developed before modern understanding of IBS pathophysiology
    - Does not account for IBS subtypes (constipation-predominant, diarrhea-predominant, mixed)
    - May be too restrictive for some IBS presentations
    - Requires laboratory testing that may not always be readily available
    - Has been largely superseded by symptom-based Rome criteria in clinical practice
    
    Historical Impact:
    The Kruis Score's main contribution was demonstrating that objective, laboratory-based 
    criteria could effectively diagnose IBS while excluding organic disease. This influenced 
    all subsequent IBS diagnostic criteria development and established the principle that 
    IBS diagnosis should consider both positive symptoms and absence of red flags.
    
    Modern Context:
    While the Rome criteria have become the gold standard for IBS diagnosis in clinical 
    practice, the Kruis Score remains valuable for:
    - Research studies requiring objective diagnostic criteria
    - Systematic approach to differential diagnosis
    - Educational purposes to understand diagnostic principles
    - Settings where laboratory confirmation of normal inflammatory markers is desired
    
    Args:
        request: Kruis Score parameters including symptoms and laboratory red flags
        
    Returns:
        KruisScoreIbsResponse: Score calculation with IBS diagnostic assessment
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("kruis_score_ibs", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Kruis Score for IBS",
                    "details": {"parameters": parameters}
                }
            )
        
        return KruisScoreIbsResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Kruis Score for IBS",
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