"""
Wound Closure Classification Router

Endpoint for wound closure classification calculation.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.general.wound_closure_classification import (
    WoundClosureClassificationRequest,
    WoundClosureClassificationResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/wound_closure_classification",
    response_model=WoundClosureClassificationResponse,
    summary="Calculate Wound Closure Classification",
    description="Classifies wound closure types to guide surgical management strategies. This evidence-based "
                "classification system evaluates wounds based on contamination level, tissue loss, time since "
                "injury, vascularization status, and anatomical location to recommend the most appropriate "
                "closure method. The three closure types are: (1) Primary closure for clean wounds with "
                "minimal tissue loss within the appropriate time window; (2) Secondary closure for wounds "
                "with significant tissue loss that heal by secondary intention; and (3) Tertiary (delayed "
                "primary) closure for contaminated wounds requiring observation before closure. This "
                "classification helps optimize wound healing outcomes, minimize complications, and guide "
                "clinical decision-making in emergency medicine, surgery, and wound care specialties.",
    response_description="The recommended wound closure classification with clinical rationale, management recommendations, and timing guidance",
    operation_id="wound_closure_classification"
)
async def calculate_wound_closure_classification(request: WoundClosureClassificationRequest):
    """
    Calculates Wound Closure Classification
    
    The Wound Closure Classification is an evidence-based system that helps clinicians 
    determine the most appropriate closure method for traumatic wounds based on multiple 
    clinical factors. This classification system was developed to optimize wound healing 
    outcomes and minimize complications such as infection, dehiscence, and poor cosmetic results.
    
    Background and Clinical Context:
    
    Wound closure is a fundamental skill in emergency medicine, surgery, and primary care. 
    The method of closure significantly impacts healing time, infection risk, cosmetic outcome, 
    and patient satisfaction. The traditional approach of immediate primary closure for all 
    wounds has evolved into a more nuanced, evidence-based classification system that considers 
    multiple wound characteristics and patient factors.
    
    Key Pathophysiology:
    - Bacterial contamination increases exponentially with time after injury
    - Tissue perfusion affects healing capacity and infection resistance
    - Wound tension influences healing and scarring outcomes
    - Location-specific factors affect blood supply and healing potential
    
    **WOUND CLOSURE CLASSIFICATION SYSTEM:**
    
    **PRIMARY CLOSURE:**
    
    Definition and Indications:
    - Direct surgical approximation of wound edges
    - Clean wounds with minimal to moderate tissue loss
    - Presentation within appropriate time window (typically 6-8 hours, up to 24 hours for facial wounds)
    - Well or moderately vascularized tissue
    
    Technical Considerations:
    - Thorough irrigation with normal saline (pressure irrigation for contaminated wounds)
    - Adequate anesthesia (local, regional, or systemic as appropriate)
    - Careful debridement of devitalized tissue and foreign material
    - Layered closure for wounds involving subcutaneous tissue or deeper structures
    - Appropriate suture selection based on wound location and tension
    
    Advantages:
    - Fastest healing (7-14 days for suture removal)
    - Best cosmetic outcome when appropriately selected
    - Lowest risk of secondary infection when criteria met
    - Single procedure with immediate wound protection
    
    **SECONDARY CLOSURE (Healing by Secondary Intention):**
    
    Definition and Indications:
    - Wound left open to heal through granulation tissue formation and contraction
    - Significant tissue loss preventing tension-free approximation
    - Wounds where primary closure would result in unacceptable tension or poor outcomes
    - Patient factors preventing adequate wound care or follow-up
    
    Technical Considerations:
    - Daily dressing changes with appropriate wound care products
    - Maintain moist wound environment to promote granulation
    - Monitor for signs of infection or healing complications
    - Consider negative pressure wound therapy for appropriate wounds
    - Nutritional optimization and management of comorbidities
    
    Advantages:
    - Allows natural wound healing without tension
    - Accommodates wounds with irregular shapes or significant tissue loss
    - Lower risk of wound dehiscence
    - Does not require patient return for suture removal
    
    **TERTIARY CLOSURE (Delayed Primary Closure):**
    
    Definition and Indications:
    - Delayed surgical closure after 3-7 days of observation and wound preparation
    - Contaminated or grossly contaminated wounds requiring debridement
    - Delayed presentation beyond safe primary closure window
    - Wounds with questionable tissue viability or perfusion
    
    Technical Considerations:
    - Immediate thorough exploration, irrigation, and debridement
    - Daily wound assessment and dressing changes during observation period
    - Antibiotic prophylaxis consideration based on contamination level
    - Re-evaluation at 3-7 days for signs of infection or tissue necrosis
    - Proceed with closure only if wound bed appears clean and viable
    
    Advantages:
    - Allows assessment of tissue viability before commitment to closure
    - Permits resolution of contamination and inflammation
    - Reduces risk of closure over infected or necrotic tissue
    - Maintains option for later surgical intervention
    
    **Clinical Decision Factors:**
    
    Contamination Assessment:
    - Clean: Surgical wounds or clean lacerations with minimal bacterial exposure
    - Contaminated: Wounds exposed to bacteria but without gross contamination
    - Grossly contaminated: Soil, feces, saliva, or other heavily contaminated material
    
    Tissue Loss Evaluation:
    - Minimal (<1cm): Edges can be approximated without significant tension
    - Moderate (1-3cm): May require some tension but achievable approximation
    - Significant (>3cm): Cannot achieve tension-free approximation
    
    Timing Considerations:
    - Golden period: 6-8 hours for most wounds
    - Extended window: Up to 24 hours for facial wounds or well-vascularized areas
    - Delayed presentation: >24 hours generally requires tertiary approach
    
    Vascularization Assessment:
    - Well-vascularized: Brisk bleeding, good color, rapid capillary refill
    - Moderately vascularized: Adequate perfusion but not optimal
    - Poorly vascularized: Pale, slow bleeding, compromised blood supply
    
    **Location-Specific Considerations:**
    
    Face and Scalp:
    - Excellent blood supply allows extended closure window (up to 24 hours)
    - High cosmetic importance favors primary closure when possible
    - Consider plastic surgery consultation for complex facial wounds
    
    Extremities:
    - Variable blood supply depending on specific location
    - Functional considerations important for hands and feet
    - Joint involvement requires specialized closure techniques
    
    Trunk:
    - Standard closure principles apply
    - Consider patient mobility and clothing friction
    - Larger wounds may benefit from staged closure
    
    **Contraindications and Special Considerations:**
    
    Primary Closure Contraindications:
    - Active signs of infection (erythema, warmth, purulent drainage)
    - Grossly contaminated wounds with foreign material
    - Significant tissue necrosis or devitalization
    - Patient inability to maintain wound care or return for follow-up
    
    Secondary Closure Considerations:
    - Large wounds may require skin grafting or flap coverage
    - Functional areas may need earlier surgical intervention
    - Cosmetically sensitive areas may require plastic surgery consultation
    
    Tertiary Closure Monitoring:
    - Daily assessment for signs of infection or tissue necrosis
    - Consider culture and antibiotic adjustment if infection develops
    - Abandon closure plan if wound deteriorates during observation
    
    **Quality Indicators and Outcomes:**
    
    Success Metrics:
    - Primary closure: <5% infection rate, good cosmetic outcome
    - Secondary closure: Complete healing within expected timeframe
    - Tertiary closure: Successful delayed closure without complications
    
    Complication Prevention:
    - Appropriate patient selection for closure type
    - Meticulous surgical technique and wound preparation
    - Adequate patient education and follow-up planning
    - Early recognition and management of complications
    
    **Limitations and Clinical Judgment:**
    
    - Classification provides guidance but cannot replace clinical experience
    - Patient-specific factors (diabetes, immunosuppression, smoking) affect healing
    - Local resources and expertise influence closure options
    - Some wounds may not fit clearly into classification categories
    - Surgeon preference and experience remain important factors
    
    Args:
        request: Wound characteristics including contamination, tissue loss, timing, vascularization, and location
        
    Returns:
        WoundClosureClassificationResponse: Closure type recommendation with clinical guidance and management strategies
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("wound_closure_classification", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Wound Closure Classification",
                    "details": {"parameters": parameters}
                }
            )
        
        return WoundClosureClassificationResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for wound closure classification",
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
                "message": "Internal error in wound closure classification calculation",
                "details": {"error": str(e)}
            }
        )