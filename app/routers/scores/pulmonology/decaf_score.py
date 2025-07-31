"""
DECAF Score for Acute Exacerbation of COPD Router

Endpoint for calculating DECAF score for COPD exacerbation mortality prediction.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.pulmonology.decaf_score import (
    DecafScoreRequest,
    DecafScoreResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/decaf_score",
    response_model=DecafScoreResponse,
    summary="Calculate DECAF Score for Acute Exacerbation of COPD",
    description="Predicts in-hospital mortality in acute COPD exacerbation using five clinical variables: Dyspnoea, Eosinopenia, Consolidation, Acidaemia, and atrial Fibrillation.",
    response_description="The calculated decaf score with interpretation",
    operation_id="decaf_score"
)
async def calculate_decaf_score(request: DecafScoreRequest):
    """
    Calculates DECAF Score for Acute Exacerbation of COPD
    
    The DECAF Score for Acute Exacerbation of COPD is a validated clinical decision 
    tool that predicts in-hospital mortality in patients hospitalized with acute 
    COPD exacerbation. The acronym DECAF represents the five strongest predictors 
    of mortality: Dyspnoea, Eosinopenia, Consolidation, Acidaemia, and atrial Fibrillation.
    
    **Clinical Background and Development:**
    
    Chronic obstructive pulmonary disease (COPD) is a leading cause of morbidity 
    and mortality worldwide, with acute exacerbations representing a major cause 
    of hospital admissions and healthcare costs. Accurate risk stratification of 
    patients admitted with acute COPD exacerbation is crucial for optimal resource 
    allocation, treatment intensity decisions, and prognostic discussions.
    
    The DECAF score was developed through rigorous analysis of prospective cohort 
    studies, identifying the five clinical variables most strongly associated with 
    in-hospital mortality. The tool demonstrates excellent discrimination for 
    mortality prediction (area under ROC curve = 0.86) and superior performance 
    compared to other clinical prediction tools.
    
    **Evidence Base and Validation:**
    
    **Original Development Study:**
    The DECAF score was derived from a prospective cohort study in the UK that 
    analyzed multiple clinical variables in patients hospitalized with acute COPD 
    exacerbation. Through multivariate analysis, five variables emerged as the 
    strongest independent predictors of in-hospital mortality.
    
    **External Validation Studies:**
    Multiple subsequent studies have validated the DECAF score across different 
    populations, healthcare systems, and geographic regions, consistently 
    demonstrating its predictive accuracy and clinical utility.
    
    **Meta-Analysis Evidence:**
    Systematic reviews and meta-analyses have confirmed the DECAF score's superior 
    prognostic accuracy compared to other scoring systems used in COPD, with pooled 
    sensitivity of 74% and specificity of 76% for predicting in-hospital mortality.
    
    **DECAF Score Components and Interpretation:**
    
    **D - Dyspnoea (Extended MRC Dyspnoea Scale): 0-2 Points**
    
    **Not too dyspneic to leave house (0 points):**
    Patient can leave house and perform activities of daily living without 
    significant limitation from breathlessness. This represents relatively 
    preserved functional status despite acute exacerbation.
    
    **Too dyspneic to leave house but independent with washing/dressing (1 point):**
    Patient experiences significant dyspnea that prevents leaving the house but 
    can still perform personal care activities independently. This indicates 
    moderate functional limitation.
    
    **Too dyspneic to leave house and requires assistance with washing/dressing (2 points):**
    Patient has severe dyspnea that prevents leaving home and requires assistance 
    with basic activities of daily living. This represents severe functional 
    impairment and highest risk.
    
    **E - Eosinopenia (<0.05×10⁹/L): 0-1 Point**
    
    **Pathophysiology:**
    Eosinopenia (low eosinophil count) in acute COPD exacerbation indicates 
    systemic inflammation and stress response. Low eosinophil counts are associated 
    with bacterial infections, severe systemic illness, and poor prognosis.
    
    **Clinical Significance:**
    Eosinopenia serves as a biomarker of disease severity and systemic impact 
    of the acute exacerbation. Patients with eosinopenia typically have more 
    severe inflammation and higher mortality risk.
    
    **C - Consolidation on Chest X-ray: 0-1 Point**
    
    **Clinical Significance:**
    Consolidation on chest imaging indicates pneumonic process, which significantly 
    increases mortality risk in COPD exacerbation. The presence of consolidation 
    suggests bacterial infection requiring antimicrobial therapy and more intensive 
    monitoring.
    
    **Management Implications:**
    Patients with consolidation typically require antibiotic therapy in addition 
    to standard COPD exacerbation treatment. The combination of COPD exacerbation 
    and pneumonia represents a particularly high-risk clinical scenario.
    
    **A - Acidaemia (pH <7.30): 0-1 Point**
    
    **Pathophysiology:**
    Acidaemia in COPD exacerbation typically results from respiratory acidosis 
    due to ventilatory failure and CO2 retention. pH <7.30 indicates significant 
    respiratory failure requiring urgent intervention.
    
    **Clinical Implications:**
    Acidaemia is a strong predictor of need for ventilatory support and intensive 
    care. Patients with pH <7.30 require immediate assessment for non-invasive 
    or invasive mechanical ventilation.
    
    **F - Atrial Fibrillation: 0-1 Point**
    
    **Pathophysiology:**
    Atrial fibrillation in COPD patients often reflects right heart strain, 
    hypoxemia, or medication effects (theophylline, beta-agonists). It may be 
    chronic or acute-onset during exacerbation.
    
    **Clinical Significance:**
    Atrial fibrillation increases mortality risk through hemodynamic compromise, 
    thromboembolic risk, and indication of more severe underlying disease. It 
    may require rate control and anticoagulation consideration.
    
    **Risk Stratification and Clinical Application:**
    
    **Low Risk (DECAF 0-1): 0-1.5% Mortality**
    
    **Clinical Characteristics:**
    - Preserved functional status with minimal dyspnea limitation
    - Normal or elevated eosinophil count
    - Clear chest X-ray without consolidation
    - Normal arterial pH (≥7.30)
    - No atrial fibrillation
    
    **Management Approach:**
    - Standard ward-based care is appropriate
    - Routine COPD exacerbation protocol with bronchodilators and corticosteroids
    - Standard nursing monitoring and observation
    - Focus on early mobilization and discharge planning
    - Outpatient follow-up with pulmonology
    
    **Intermediate Risk (DECAF 2): 5.4% Mortality**
    
    **Clinical Characteristics:**
    - Moderate functional limitation or single high-risk feature
    - Elevated mortality risk requiring careful assessment
    - Need for individualized clinical decision-making
    
    **Management Approach:**
    - Enhanced monitoring and frequent clinical assessment
    - Consider higher level of nursing care or step-down unit
    - Aggressive medical therapy with close response monitoring
    - Early identification and management of complications
    - Consider respiratory therapy consultation
    
    **High Risk (DECAF 3-6): 15.3-50% Mortality**
    
    **Clinical Characteristics:**
    - Multiple high-risk features present
    - Severe functional limitation and/or physiologic derangement
    - Significant risk of deterioration and death
    
    **Management Approach:**
    - Strong consideration for HDU/ICU level care
    - Intensive monitoring for respiratory failure and complications
    - Early assessment for non-invasive or invasive ventilation
    - Multidisciplinary team involvement
    - Goals of care discussion and potential palliative care consultation
    
    **Clinical Decision Support and Implementation:**
    
    **Disposition Decisions:**
    The DECAF score provides objective data to support decisions about level of 
    care, from standard ward care for low-risk patients to intensive care 
    consideration for high-risk patients.
    
    **Resource Allocation:**
    Hospitals can use DECAF scoring to optimize resource allocation, ensuring 
    high-risk patients receive appropriate monitoring and intervention while 
    avoiding unnecessary escalation for low-risk patients.
    
    **Prognostic Communication:**
    The quantitative mortality risk estimates facilitate honest prognostic 
    discussions with patients and families, supporting informed decision-making 
    about treatment goals and intensity.
    
    **Quality Improvement:**
    DECAF scoring can support quality improvement initiatives by standardizing 
    risk assessment, reducing practice variation, and enabling outcome monitoring.
    
    **Special Considerations and Limitations:**
    
    **Patient Population:**
    The DECAF score is validated specifically for patients ≥35 years old with 
    acute COPD exacerbation requiring hospitalization and ≥10 pack-year smoking 
    history. It should not be used in outpatient settings or stable COPD patients.
    
    **Clinical Judgment:**
    While the DECAF score provides valuable objective risk assessment, it should 
    supplement rather than replace clinical judgment. Individual patient factors 
    not captured by the score should be considered in final decision-making.
    
    **Dynamic Assessment:**
    Patient risk can change during hospitalization, requiring reassessment and 
    potential modification of management approach based on clinical response to 
    initial therapy.
    
    **Goals of Care:**
    For high-risk patients, early goals of care discussions are important to 
    ensure treatment plans align with patient values and preferences, potentially 
    including palliative care consultation.
    
    **Comparative Performance:**
    
    **Superior to Other Scores:**
    Studies have demonstrated that DECAF score has superior prognostic accuracy 
    compared to other scoring systems used in COPD, including APACHE II, BAP-65, 
    and CURB-65 (when pneumonia is present).
    
    **Clinical Utility:**
    The DECAF score incorporates readily available clinical variables, making it 
    practical for implementation in various healthcare settings without requiring 
    complex calculations or specialized laboratory tests.
    
    **Implementation Best Practices:**
    
    **Staff Training:**
    Successful implementation requires training healthcare providers on proper 
    assessment of DECAF components, particularly the extended MRC dyspnea scale 
    and interpretation of results.
    
    **Documentation:**
    Clear documentation of DECAF components and scores supports continuity of 
    care and enables quality improvement monitoring.
    
    **Integration with Protocols:**
    DECAF scoring can be integrated into existing COPD exacerbation management 
    protocols and clinical pathways to standardize care and improve outcomes.
    
    Args:
        request: DECAF score parameters including extended MRC dyspnea scale, 
                eosinopenia status, consolidation presence, acidemia, and atrial 
                fibrillation, with optional age and smoking history for validity
        
    Returns:
        DecafScoreResponse: Comprehensive risk assessment including DECAF score, 
        mortality risk, risk category classification, clinical management 
        recommendations, and disposition guidance
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("decaf_score", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating DECAF Score",
                    "details": {"parameters": parameters}
                }
            )
        
        return DecafScoreResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for DECAF Score",
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