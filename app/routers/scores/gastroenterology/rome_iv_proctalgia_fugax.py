"""
Rome IV Diagnostic Criteria for Proctalgia Fugax Router

Endpoint for Rome IV proctalgia fugax diagnostic assessment.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.gastroenterology.rome_iv_proctalgia_fugax import (
    RomeIvProctalgieFugaxRequest,
    RomeIvProctalgieFugaxResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/rome_iv_proctalgia_fugax",
    response_model=RomeIvProctalgieFugaxResponse,
    summary="Rome IV Diagnostic Criteria for Proctalgia Fugax",
    description="Applies the official Rome IV diagnostic criteria for proctalgia fugax, a functional anorectal pain disorder. "
                "This validated diagnostic tool evaluates 8 essential criteria including recurrent episodes of rectal pain "
                "lasting seconds to 30 minutes, complete pain-free intervals between episodes, and systematic exclusion of "
                "organic causes. ALL criteria must be met for positive diagnosis. Proctalgia fugax is characterized by "
                "sudden, severe, episodic rectal pain unrelated to defecation with excellent prognosis. Essential for "
                "differential diagnosis of functional anorectal pain syndromes including levator ani syndrome and "
                "unspecified functional anorectal pain. Guides appropriate patient management and treatment planning.",
    response_description="Rome IV diagnostic assessment with criteria fulfillment status, clinical interpretation, and management recommendations",
    operation_id="rome_iv_proctalgia_fugax"
)
async def calculate_rome_iv_proctalgia_fugax(request: RomeIvProctalgieFugaxRequest):
    """
    Rome IV Diagnostic Criteria for Proctalgia Fugax Assessment
    
    Applies the international standard Rome IV diagnostic criteria for proctalgia fugax, 
    a benign functional anorectal pain disorder affecting 6-18% of adults. This 
    evidence-based diagnostic tool ensures systematic evaluation and accurate 
    differentiation from other anorectal pain syndromes.
    
    Clinical Significance:
    Proctalgia fugax is characterized by sudden, severe, episodic rectal pain that 
    can significantly impact quality of life despite its benign nature. Proper 
    diagnosis using Rome IV criteria enables appropriate patient reassurance, 
    targeted management, and avoidance of unnecessary invasive procedures.
    
    Diagnostic Criteria Overview:
    ALL of the following 8 criteria must be fulfilled for positive diagnosis:
    
    Core Pain Characteristics:
    1. Recurrent episodes of pain localized to the rectum, unrelated to defecation
    2. Episodes lasting from seconds to minutes (maximum 30 minutes)
    3. Complete absence of anorectal pain between episodes
    
    Exclusion of Organic Causes:
    4. Inflammatory bowel disease ruled out
    5. Structural anorectal lesions excluded (abscess, fissure, thrombosed hemorrhoids)
    6. Prostatitis excluded (in male patients)
    7. Coccygodynia excluded
    8. Major structural pelvic floor alterations excluded
    
    Clinical Applications:
    - Primary care and gastroenterology practice for anorectal pain evaluation
    - Differential diagnosis of functional anorectal pain syndromes
    - Patient education and reassurance about benign functional disorders
    - Research and clinical trial standardization
    - Quality improvement in functional GI disorder management
    
    Key Differentiating Features:
    - Episode duration <30 minutes (vs. levator ani syndrome: chronic pain)
    - Pain-free intervals (vs. unspecified functional anorectal pain: persistent symptoms)
    - Rectal location (vs. coccygodynia: tailbone pain)
    - Unrelated to defecation (vs. anal fissure: pain with bowel movements)
    
    Treatment Implications:
    Positive diagnosis enables focused management including patient education, 
    stress management, trigger avoidance, and symptomatic relief measures. 
    Negative diagnosis requires further evaluation for alternative conditions.
    
    Args:
        request: Rome IV diagnostic criteria assessment parameters
        
    Returns:
        RomeIvProctalgieFugaxResponse: Diagnostic outcome with clinical guidance
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("rome_iv_proctalgia_fugax", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error applying Rome IV diagnostic criteria for proctalgia fugax",
                    "details": {"parameters": parameters}
                }
            )
        
        return RomeIvProctalgieFugaxResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Rome IV proctalgia fugax assessment",
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
                "message": "Internal error in Rome IV proctalgia fugax diagnostic assessment",
                "details": {"error": str(e)}
            }
        )