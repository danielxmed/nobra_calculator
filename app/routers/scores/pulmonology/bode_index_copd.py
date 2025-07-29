"""
BODE Index for COPD Survival Router

Endpoint for calculating BODE Index for COPD prognosis.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.pulmonology.bode_index_copd import (
    BodeIndexCopdRequest,
    BodeIndexCopdResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post("/bode_index_copd", response_model=BodeIndexCopdResponse)
async def calculate_bode_index_copd(request: BodeIndexCopdRequest):
    """
    Calculates BODE Index for COPD Survival
    
    The BODE Index is a comprehensive multidimensional grading system that provides 
    superior prognostic information compared to FEV1 alone in patients with Chronic 
    Obstructive Pulmonary Disease (COPD). Developed by Celli and colleagues in 2004, 
    this index has become a cornerstone tool for risk stratification and clinical 
    decision-making in COPD management.
    
    **Historical Development:**
    
    **Background and Rationale:**
    Prior to the BODE Index, COPD prognosis relied primarily on FEV1, which captures 
    only the pulmonary component of this complex systemic disease. Recognizing that 
    COPD affects multiple organ systems and functional domains, researchers sought to 
    develop a more comprehensive assessment tool that would better predict mortality 
    and guide clinical management.
    
    **Original Study:**
    The seminal study by Celli et al. (N Engl J Med 2004) evaluated 207 COPD patients 
    in the derivation cohort and 625 patients in the validation cohort across three 
    countries (United States, Spain, and Venezuela). The researchers identified four 
    independent predictors of mortality that were combined into the BODE Index.
    
    **Key Findings:**
    - BODE Index was superior to FEV1 in predicting all-cause mortality
    - Clear stepwise increase in mortality with increasing BODE quartiles
    - Validated across diverse populations and healthcare systems
    - Responsive to interventions like pulmonary rehabilitation
    
    **Components and Scoring System:**
    
    **1. Body-Mass Index (B) - Nutritional Status:**
    
    **Clinical Significance:**
    - Reflects systemic effects of COPD including muscle wasting and cachexia
    - Low BMI associated with increased mortality (obesity paradox in COPD)
    - Indicator of disease severity beyond pulmonary manifestations
    
    **Scoring:**
    - BMI >21 kg/m²: 0 points (better nutritional status)
    - BMI ≤21 kg/m²: 1 point (malnutrition/cachexia risk)
    
    **Physiological Basis:**
    - Systemic inflammation leads to increased energy expenditure
    - Reduced caloric intake due to dyspnea during eating
    - Loss of skeletal muscle mass affects respiratory muscles
    - Associated with increased exacerbation frequency
    
    **2. Obstruction - FEV1 (O) - Airflow Limitation:**
    
    **Clinical Significance:**
    - Gold standard measure of airflow obstruction
    - Reflects severity of fixed airway obstruction
    - Correlates with pathological changes in airways and parenchyma
    
    **Scoring (% predicted):**
    - ≥65%: 0 points (GOLD 1 - mild)
    - 50-64%: 1 point (GOLD 2 - moderate)
    - 36-49%: 2 points (GOLD 3 - severe)
    - ≤35%: 3 points (GOLD 4 - very severe)
    
    **Technical Considerations:**
    - Must use appropriate reference equations for demographics
    - Post-bronchodilator values preferred for stability
    - Quality control essential for accurate measurements
    - Consider ethnic-specific reference values
    
    **3. Dyspnea - Modified MRC Scale (D) - Symptom Burden:**
    
    **Clinical Significance:**
    - Captures patient's subjective experience of breathlessness
    - Strong predictor of quality of life and functional status
    - Reflects disease impact on daily activities
    - Independent predictor of mortality beyond FEV1
    
    **Scoring:**
    - Grade 0: Dyspnea only with strenuous exercise (0 points)
    - Grade 1: Short of breath when hurrying or on slight hill (1 point)
    - Grade 2: Walks slower than peers, stops for breath at own pace (2 points)
    - Grade 3: Stops after 100m or few minutes on level ground (3 points)
    - Grade 4: Too breathless to leave house or when dressing (3 points)
    
    **Assessment Pearls:**
    - Ensure patient understands each grade description
    - Consider cultural factors in activity descriptions
    - Account for comorbidities affecting dyspnea
    - Regular reassessment as disease progresses
    
    **4. Exercise Capacity - 6-Minute Walk Distance (E):**
    
    **Clinical Significance:**
    - Integrated measure of cardiopulmonary and musculoskeletal function
    - Correlates with activities of daily living
    - Sensitive to therapeutic interventions
    - Strong independent predictor of mortality
    
    **Scoring:**
    - ≥350 meters: 0 points (preserved exercise capacity)
    - 250-349 meters: 1 point (mild limitation)
    - 150-249 meters: 2 points (moderate limitation)
    - ≤149 meters: 3 points (severe limitation)
    
    **Test Protocol Requirements:**
    - Follow ATS guidelines for standardization
    - 30-meter corridor with turnaround points
    - Standardized encouragement phrases
    - Monitor oxygen saturation and symptoms
    - Two tests recommended with best distance recorded
    
    **Prognostic Stratification:**
    
    **Quartile 1 (0-2 points) - Low Risk:**
    - **4-year survival**: 80%
    - **52-month mortality**: ~20%
    - **Characteristics**: Early disease, preserved function
    - **Management Focus**: 
      - Smoking cessation paramount
      - Bronchodilator optimization
      - Vaccination programs
      - Early pulmonary rehabilitation
      - Annual monitoring
    
    **Quartile 2 (3-4 points) - Moderate Risk:**
    - **4-year survival**: 67%
    - **52-month mortality**: ~30%
    - **Characteristics**: Moderate functional impairment
    - **Management Focus**:
      - Dual/triple bronchodilator therapy
      - Pulmonary rehabilitation enrollment
      - Exacerbation prevention strategies
      - Nutritional assessment
      - Biannual monitoring
    
    **Quartile 3 (5-6 points) - High Risk:**
    - **4-year survival**: 57%
    - **52-month mortality**: ~40%
    - **Characteristics**: Significant multi-domain impairment
    - **Management Focus**:
      - Optimize all medical therapies
      - Long-term oxygen therapy evaluation
      - Intensive pulmonary rehabilitation
      - Address comorbidities aggressively
      - Quarterly monitoring
    
    **Quartile 4 (7-10 points) - Very High Risk:**
    - **4-year survival**: 18%
    - **52-month mortality**: ~80%
    - **Characteristics**: End-stage disease, severe limitations
    - **Management Focus**:
      - Palliative care integration
      - Lung transplant evaluation if eligible
      - Non-invasive ventilation consideration
      - Advanced care planning
      - Frequent monitoring and support
    
    **Clinical Applications and Integration:**
    
    **Treatment Planning:**
    - **Pharmacotherapy**: Guide intensity of bronchodilator regimens
    - **Non-pharmacological**: Prioritize pulmonary rehabilitation referrals
    - **Oxygen therapy**: Lower threshold for evaluation in higher quartiles
    - **Advanced interventions**: Identify transplant or LVRS candidates
    
    **Monitoring Disease Progression:**
    - Annual BODE assessment in stable patients
    - Post-exacerbation reassessment at 6-8 weeks
    - Track response to interventions
    - Identify rapid decliners requiring intensification
    
    **Research Applications:**
    - Stratification for clinical trials
    - Outcomes assessment in intervention studies
    - Healthcare resource utilization planning
    - Quality improvement initiatives
    
    **Special Populations and Considerations:**
    
    **Elderly Patients:**
    - Adjust 6MWD expectations for age
    - Consider frailty in interpretation
    - Account for comorbidity burden
    - Focus on functional outcomes
    
    **Phenotype Considerations:**
    - Emphysema-predominant: Often lower BMI
    - Chronic bronchitis: May have preserved BMI
    - Frequent exacerbators: Faster BODE progression
    - Overlap syndromes: Modified interpretation needed
    
    **Limitations and Caveats:**
    
    **Not Applicable During:**
    - Acute exacerbations (wait 6-8 weeks)
    - Recent cardiovascular events
    - Musculoskeletal conditions limiting walking
    - Cognitive impairment affecting mMRC assessment
    
    **Does Not Capture:**
    - Exacerbation frequency
    - Comorbidity burden
    - Biomarker abnormalities
    - Radiographic severity
    
    **Future Directions:**
    - Integration with biomarkers (fibrinogen, CRP)
    - Incorporation of CT imaging parameters
    - Addition of exacerbation history (ADO index)
    - Machine learning enhancements
    
    Args:
        request: BODE Index parameters (FEV1%, 6MWD, mMRC grade, BMI)
        
    Returns:
        BodeIndexCopdResponse: BODE score with quartile classification and prognosis
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("bode_index_copd", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating BODE Index",
                    "details": {"parameters": parameters}
                }
            )
        
        return BodeIndexCopdResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for BODE Index calculation",
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