"""
Mantle Cell Lymphoma International Prognostic Index (MIPI) Router

Endpoint for calculating MIPI for mantle cell lymphoma prognosis assessment.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.hematology.mantle_cell_lymphoma_international_prognostic_index import (
    MantleCellLymphomaInternationalPrognosticIndexRequest,
    MantleCellLymphomaInternationalPrognosticIndexResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/mantle_cell_lymphoma_international_prognostic_index",
    response_model=MantleCellLymphomaInternationalPrognosticIndexResponse,
    summary="Calculate Mantle Cell Lymphoma International Prognostic Index (MIPI)",
    description="Calculates the Mantle Cell Lymphoma International Prognostic Index (MIPI) "
                "for predicting survival in patients with advanced-stage mantle cell lymphoma. "
                "This evidence-based prognostic tool combines four independent factors (age, "
                "ECOG performance status, LDH level, and WBC count) to stratify patients into "
                "low, intermediate, and high risk categories. When Ki-67 proliferation index "
                "is available, the biological MIPI (MIPIb) provides enhanced prognostic accuracy. "
                "The MIPI is more specific to mantle cell lymphoma than the International "
                "Prognostic Index (IPI) and helps guide treatment decisions, clinical trial "
                "stratification, and discussions about prognosis. Risk stratification ranges "
                "from low risk (5-year OS ~60%) to high risk (median OS ~29 months), with "
                "treatment recommendations varying from standard chemotherapy to intensive "
                "regimens with stem cell transplantation consideration.",
    response_description="The calculated MIPI or MIPIb score with risk stratification, survival estimates, and comprehensive treatment recommendations",
    operation_id="mantle_cell_lymphoma_international_prognostic_index"
)
async def calculate_mantle_cell_lymphoma_international_prognostic_index(request: MantleCellLymphomaInternationalPrognosticIndexRequest):
    """
    Calculates Mantle Cell Lymphoma International Prognostic Index (MIPI)
    
    The MIPI is the first prognostic index specifically developed for mantle cell lymphoma 
    (MCL) patients. It combines four independent prognostic factors to predict survival 
    and guide treatment decisions in advanced-stage MCL.
    
    **Four Prognostic Factors:**
    1. **Age**: Continuous variable with significant prognostic impact
    2. **ECOG Performance Status**: Functional status (0-1 vs 2-4)
    3. **Serum LDH**: Reflects tumor burden and cellular turnover
    4. **WBC Count**: Indicates disease burden and bone marrow involvement
    
    **Calculation Formulas:**
    - **MIPI**: (0.03535 × age) + 0.6978 (if ECOG 2-4) + [1.367 × log10(LDH/ULN)] + [0.9393 × log10(WBC)]
    - **MIPIb**: MIPI + (0.02142 × Ki-67 %) when Ki-67 proliferation index available
    
    **Risk Stratification:**
    
    **MIPI Categories:**
    - **Low Risk (<5.7)**: 5-year overall survival ~60%, median survival not reached
    - **Intermediate Risk (5.7-6.2)**: Median survival ~51 months
    - **High Risk (≥6.2)**: Median survival ~29 months
    
    **MIPIb Categories (when Ki-67 available):**
    - **Low Risk (<5.7)**: Median survival not reached
    - **Intermediate Risk (5.7-6.5)**: Median survival ~58 months
    - **High Risk (≥6.5)**: Median survival ~37 months
    
    **Clinical Applications:**
    - **Treatment Stratification**: Guides intensity of initial therapy
    - **Transplant Consideration**: Helps determine candidacy for autologous SCT
    - **Clinical Trial Eligibility**: Standard stratification factor in MCL trials
    - **Prognostic Counseling**: Provides evidence-based survival estimates
    - **Risk-Adapted Therapy**: Informs treatment selection and intensity
    
    **Treatment Implications by Risk Group:**
    
    **Low Risk:**
    - Standard chemotherapy regimens (R-CHOP, R-bendamustine)
    - Less intensive approaches may be considered
    - Observation possible in very select cases
    
    **Intermediate Risk:**
    - Intensive chemotherapy recommended
    - Clinical trial participation encouraged
    - Consider autologous SCT consolidation
    - Risk-adapted approach based on age and comorbidities
    
    **High Risk:**
    - Immediate intensive treatment required
    - Aggressive chemotherapy regimens
    - Strong consideration for autologous SCT
    - Clinical trial participation highly recommended
    - Novel targeted therapies consideration
    - Maintenance therapy evaluation
    
    **Important Clinical Considerations:**
    - Most MCL patients require treatment at diagnosis regardless of risk group
    - MIPI should be used in conjunction with other clinical factors
    - Performance status significantly impacts treatment tolerance
    - Age remains important for treatment selection
    - Ki-67 provides additional prognostic value when available
    - Regular reassessment during treatment for modifications
    
    **Validation and Performance:**
    - Developed from 455 advanced MCL patients in European clinical trials
    - More specific to MCL than International Prognostic Index (IPI)
    - Validated across multiple independent cohorts
    - Applicable across different treatment eras
    - Maintains prognostic value in modern therapy era
    
    **References:**
    1. Hoster E, Dreyling M, Klapper W, et al. A new prognostic index (MIPI) for patients 
       with advanced-stage mantle cell lymphoma. Blood. 2008;111(2):558-65.
    2. Hoster E, Klapper W, Hermine O, et al. Confirmation of the mantle-cell lymphoma 
       International Prognostic Index in randomized trials of the European Mantle-Cell 
       Lymphoma Network. J Clin Oncol. 2014;32(13):1338-46.
    3. Geisler CH, Kolstad A, Laurell A, et al. Long-term progression-free survival of 
       mantle cell lymphoma after intensive front-line immunochemotherapy with in vivo-purged 
       stem cell rescue. Blood. 2008;112(7):2687-93.
    
    Args:
        request: MIPI parameters including age, performance status, LDH, WBC count, and optional Ki-67
        
    Returns:
        MantleCellLymphomaInternationalPrognosticIndexResponse: Calculated score with risk 
        stratification, survival estimates, and treatment recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("mantle_cell_lymphoma_international_prognostic_index", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Mantle Cell Lymphoma International Prognostic Index (MIPI)",
                    "details": {"parameters": parameters}
                }
            )
        
        return MantleCellLymphomaInternationalPrognosticIndexResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Mantle Cell Lymphoma International Prognostic Index (MIPI)",
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