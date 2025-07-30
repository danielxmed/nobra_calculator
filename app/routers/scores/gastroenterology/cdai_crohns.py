"""
Crohn's Disease Activity Index (CDAI) Router

Endpoint for calculating CDAI scores for Crohn's disease activity assessment.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.gastroenterology.cdai_crohns import (
    CdaiCrohnsRequest,
    CdaiCrohnsResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post("/cdai_crohns", response_model=CdaiCrohnsResponse)
async def calculate_cdai_crohns(request: CdaiCrohnsRequest):
    """
    Calculates Crohn's Disease Activity Index (CDAI)
    
    The CDAI is the gold standard for quantifying disease activity in Crohn's disease, 
    incorporating 8 weighted clinical variables to produce a score ranging from 0 to 
    approximately 600 points. Developed in 1976 by the National Cooperative Crohn's 
    Disease Study Group, it remains the primary endpoint in clinical trials.
    
    **Calculation Components:**
    
    1. **Liquid Stools (past 7 days)**: Total count × 2
       - Patient diary records all liquid/loose stools over one week
       - Include all episodes regardless of volume
    
    2. **Abdominal Pain (0-3 scale)**: Average daily rating × 5
       - 0: None - No abdominal pain
       - 1: Mild - Occasional discomfort, doesn't interfere with activities
       - 2: Moderate - Regular pain that may limit some activities
       - 3: Severe - Intense pain that significantly limits daily activities
    
    3. **General Well-being (0-4 scale)**: Average daily rating × 7
       - 0: Generally well - Feeling normal, energetic
       - 1: Slightly under par - Mildly decreased energy or mood
       - 2: Poor - Noticeably unwell, reduced function
       - 3: Very poor - Significantly impaired well-being
       - 4: Terrible - Severely compromised overall condition
    
    4. **Extraintestinal Complications**: Number present × 20
       - **Arthritis/Arthralgias**: Joint pain or inflammation
       - **Iritis/Uveitis**: Eye inflammation (redness, pain, vision changes)
       - **Erythema Nodosum**: Painful red nodules, typically on legs
       - **Anal Complications**: Fissures, fistulas, or abscesses
       - **Other Fistulas**: Enteroenteric, enterovesical, enterocutaneous
       - **Fever**: Temperature >37.8°C (100°F) in past 7 days
    
    5. **Antidiarrheal Use**: Present (1) or absent (0) × 30
       - Include loperamide, diphenoxylate, codeine, or antispasmodics
       - Any use during the 7-day assessment period
    
    6. **Abdominal Mass**: Clinical examination findings × 10
       - None: No palpable mass (0 points)
       - Questionable: Uncertain or soft mass (2 points)
       - Definite: Clear, firm palpable mass (5 points)
    
    7. **Hematocrit Deficit**: (Expected - observed) × 6
       - Expected values: Men 47%, Women 42%
       - Reflects inflammatory anemia and blood loss
    
    8. **Weight Deficit**: Percentage below ideal weight × 1
       - Calculated as: (Ideal weight - Current weight) / Ideal weight × 100
       - Use pre-illness weight or calculated ideal body weight
    
    **Score Interpretation:**
    
    - **<150 points**: Clinical Remission
      - Patients typically rated as "very well" by physicians
      - Continue maintenance therapy, routine monitoring
    
    - **150-219 points**: Mild Disease Activity
      - Consider therapy optimization or step-up treatment
      - Monitor closely, reassess in 2-4 weeks
    
    - **220-299 points**: Moderate Disease Activity
      - Consider corticosteroids, immunomodulators, or biologics
      - May require therapy intensification
    
    - **300-450 points**: Severe Disease Activity
      - Often requires hospitalization and intensive therapy
      - Consider corticosteroids, immunosuppressants, or biologics
    
    - **>450 points**: Very Severe Disease Activity
      - May require hospitalization or surgical intervention
      - Immediate specialist consultation recommended
    
    **Treatment Response Criteria:**
    - **Significant Response**: ≥70 point decrease from baseline
    - **Major Clinical Response**: ≥100 point decrease from baseline
    - **Sustained Remission**: Maintain score <150 over time
    
    **Clinical Applications:**
    - **Primary endpoint** in most Crohn's disease clinical trials
    - **Treatment monitoring** and response assessment
    - **Disease severity stratification** for clinical decision-making
    - **Research standardization** across studies and centers
    
    **Assessment Requirements:**
    - **7-day patient diary** for symptoms (stool frequency, pain, well-being)
    - **Physical examination** for abdominal mass and complications
    - **Laboratory tests** for current hematocrit
    - **Accurate measurements** of current and ideal body weight
    
    **Clinical Integration:**
    - Use alongside endoscopic and biomarker assessments
    - Consider patient-reported outcomes and quality of life
    - Account for medication effects on symptom reporting
    - Integrate with treatment goals and patient preferences
    
    **Limitations and Considerations:**
    - Does not include endoscopic findings or mucosal healing
    - May not fully capture quality of life impacts
    - Requires patient compliance with symptom diary
    - Can be influenced by concurrent medications
    - May not reflect transmural inflammation extent
    
    **References:**
    - Best WR, Becktel JM, Singleton JW, Kern F Jr. Development of a Crohn's disease activity index. National Cooperative Crohn's Disease Study. Gastroenterology. 1976;70(3):439-444.
    - Sandborn WJ, Feagan BG, Hanauer SB, et al. A review of activity indices and efficacy endpoints for clinical trials of medical therapy in adults with Crohn's disease. Gastroenterology. 2002;122(2):512-530.
    
    Args:
        request: CDAI calculation parameters including symptoms, complications, and laboratory values
        
    Returns:
        CdaiCrohnsResponse: CDAI score with clinical interpretation and treatment guidance
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("cdai_crohns", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Crohn's Disease Activity Index (CDAI)",
                    "details": {"parameters": parameters}
                }
            )
        
        return CdaiCrohnsResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Crohn's Disease Activity Index (CDAI)",
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