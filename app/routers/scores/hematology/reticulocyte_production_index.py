"""
Reticulocyte Production Index (RPI) Router

Endpoint for calculating Reticulocyte Production Index (RPI) to assess bone marrow response to anemia.

The RPI is a critical hematologic parameter that corrects the raw reticulocyte count 
for both the degree of anemia and the maturation time of reticulocytes, providing 
accurate assessment of bone marrow erythropoietic function and guiding anemia diagnosis.

Clinical Applications:
- Distinguishes hypoproliferative from hyperproliferative anemia
- Assesses bone marrow response adequacy to anemic stress
- Guides diagnostic workup for unexplained anemia
- Monitors treatment response in various hematologic conditions

References (Vancouver style):
1. Koepke JA. Laboratory hematology practice. New York: Churchill Livingstone; 1989.
2. Hillman RS, Ault KA. Hematology in clinical practice. New York: McGraw-Hill; 2002.
3. Nathan DG, Orkin SH, Look AT, Ginsburg D. Nathan and Oski's Hematology of Infancy 
   and Childhood. 6th ed. Philadelphia: W.B. Saunders; 2003.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.hematology.reticulocyte_production_index import (
    ReticulocyteProductionIndexRequest,
    ReticulocyteProductionIndexResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/reticulocyte_production_index",
    response_model=ReticulocyteProductionIndexResponse,
    summary="Calculate Corrected Reticulocyte Percentage/Reticulocyte ...",
    description="Assesses bone marrow response to anemia by correcting reticulocyte count for degree of anemia and maturation time",
    response_description="The calculated reticulocyte production index with interpretation",
    operation_id="reticulocyte_production_index"
)
async def calculate_reticulocyte_production_index(request: ReticulocyteProductionIndexRequest):
    """
    Calculates Reticulocyte Production Index (RPI) for Bone Marrow Response Assessment
    
    The RPI provides a corrected measure of reticulocyte production that accounts for 
    anemia severity and reticulocyte maturation time, enabling accurate evaluation of 
    bone marrow response to anemic stress and classification of anemia etiology.
    
    Clinical Background:
    In anemic patients, the raw reticulocyte percentage can be misleading because:
    1. The percentage is calculated against a reduced total RBC count
    2. Severe anemia triggers premature release of reticulocytes requiring longer maturation
    3. The degree of anemia affects the expected magnitude of response
    
    Two-Step Correction Process:
    Step 1 - Anemia Correction: Corrected % = Raw % × (Patient Hct / Normal Hct)
    Step 2 - Maturation Correction: RPI = Corrected % / Maturation Factor
    
    Maturation Factors by Hematocrit:
    - Hct ≥35%: Factor 1.0 (normal maturation, 1 day)
    - Hct 25-34%: Factor 1.5 (mild prolongation, 1.5 days)  
    - Hct 20-24%: Factor 2.0 (moderate prolongation, 2 days)
    - Hct <20%: Factor 2.5 (severe prolongation, 2.5 days)
    
    Clinical Interpretation Framework:
    
    Very Low RPI (<0.5):
    - Severe bone marrow failure or complete suppression
    - Advanced malignant infiltration requiring urgent evaluation
    - Severe nutritional deficiencies with profound erythropoietic impact
    - Drug-induced severe bone marrow toxicity
    
    Low RPI (0.5-2.0) - Hypoproliferative Anemia:
    - Inadequate bone marrow response requiring etiology investigation
    - Iron deficiency anemia (most common cause globally)
    - Chronic kidney disease with erythropoietin deficiency
    - Chronic inflammatory conditions affecting erythropoiesis
    - Bone marrow infiltration or myelodysplastic syndromes
    
    Borderline RPI (2.0-3.0):
    - Marginal bone marrow response suggesting partial recovery
    - Early treatment response to nutritional replacement
    - Mild bone marrow dysfunction with compensatory capacity
    - Transition phase requiring continued monitoring
    
    High RPI (>3.0) - Hyperproliferative Anemia:
    - Appropriate bone marrow response indicating intact erythropoiesis
    - Hemolytic anemia with compensatory reticulocytosis
    - Acute or chronic blood loss with increased production
    - Good prognosis with treatment of underlying cause
    
    Diagnostic Approach by RPI Category:
    
    Hypoproliferative (RPI <2.0):
    - Iron studies: serum iron, TIBC, ferritin, transferrin saturation
    - Vitamin assessment: B12, folate levels
    - Kidney function and erythropoietin levels
    - Inflammatory markers for chronic disease evaluation
    - Consider bone marrow biopsy if unexplained
    
    Hyperproliferative (RPI >3.0):
    - Hemolysis markers: LDH, haptoglobin, indirect bilirubin
    - Direct antiglobulin test for autoimmune hemolysis
    - Peripheral blood smear for morphologic abnormalities
    - Evaluate for bleeding sources and blood loss
    - Specialized hemolysis testing as indicated
    
    Special Considerations:
    - Recent blood transfusions can suppress endogenous production
    - Acute anemia may show initially low RPI due to insufficient response time
    - Serial measurements often more informative than single values
    - Age and gender may affect normal reference ranges
    
    Quality Assurance Requirements:
    - Use automated flow cytometric reticulocyte counting when available
    - Ensure proper sample handling and timely analysis
    - Integrate results with complete blood count and clinical presentation
    - Consider peripheral blood smear morphology for comprehensive assessment
    
    Args:
        request: ReticulocyteProductionIndexRequest containing reticulocyte percentage,
                measured hematocrit, normal hematocrit reference, and optional RBC count
        
    Returns:
        ReticulocyteProductionIndexResponse: Calculated RPI with comprehensive clinical 
        interpretation, bone marrow response assessment, and detailed calculation 
        information including correction factors and clinical significance
        
    Raises:
        HTTPException 422: Invalid parameters (reticulocyte % 0-50%, hematocrit 5-65%, 
                          normal hematocrit 35-50%, RBC count 1.0-8.0 if provided)
        HTTPException 500: Calculation error or internal server error
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation using the calculator service
        result = calculator_service.calculate_score("reticulocyte_production_index", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Reticulocyte Production Index",
                    "details": {
                        "parameters": parameters,
                        "possible_causes": [
                            "Invalid parameter combination",
                            "Mathematical calculation error",
                            "Calculator module not found"
                        ]
                    }
                }
            )
        
        return ReticulocyteProductionIndexResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Reticulocyte Production Index calculation",
                "details": {
                    "error": str(e),
                    "parameter_requirements": {
                        "reticulocyte_percentage": "0.0-50.0%",
                        "measured_hematocrit": "5.0-65.0%",
                        "normal_hematocrit": "35.0-50.0%",
                        "rbc_count": "1.0-8.0 ×10⁶/μL (optional)"
                    }
                }
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "error": "InternalServerError",
                "message": "Internal error in Reticulocyte Production Index calculation",
                "details": {
                    "error": str(e),
                    "suggestion": "Please verify input parameters and try again"
                }
            }
        )