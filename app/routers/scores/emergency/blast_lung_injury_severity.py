"""
Blast Lung Injury Severity Score Router

Endpoint for calculating Blast Lung Injury Severity Score to guide ventilatory management.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.emergency.blast_lung_injury_severity import (
    BlastLungInjurySeverityRequest,
    BlastLungInjurySeverityResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/blast_lung_injury_severity",
    response_model=BlastLungInjurySeverityResponse,
    summary="Calculate Blast Lung Injury Severity Score",
    description="Stratifies primary blast lung injuries into three severity categories to guide ventilatory treatment and predict clinical outcomes",
    response_description="The calculated blast lung injury severity with interpretation",
    operation_id="calculate_blast_lung_injury_severity"
)
async def calculate_blast_lung_injury_severity(request: BlastLungInjurySeverityRequest):
    """
    Calculates Blast Lung Injury Severity Score for Primary Blast Lung Injury Assessment
    
    The Blast Lung Injury Severity Score, developed by Pizov and colleagues in 1999, 
    represents a critical tool for the systematic assessment and management of primary 
    blast lung injury (PBLI). This scoring system emerged from the clinical need to 
    standardize care for victims of explosive incidents in both military and civilian 
    settings.
    
    **Historical Context and Development:**
    
    **Original Research:**
    - Developed from analysis of civilian bus bombing survivors in Jerusalem
    - Validated through retrospective analysis of blast injury patients
    - Represents first systematic approach to PBLI severity assessment
    - Based on pathophysiological understanding of blast wave effects on lung tissue
    
    **Clinical Problem Addressed:**
    - Need for rapid, objective assessment of blast lung injury severity
    - Requirement for evidence-based ventilatory management guidelines
    - Standardization of care across different healthcare settings
    - Prediction of clinical outcomes and resource allocation needs
    
    **Pathophysiology of Primary Blast Lung Injury:**
    
    **Mechanism of Injury:**
    Primary blast lung injury results from the direct effect of high-intensity pressure 
    waves on lung tissue. Unlike secondary (debris penetration) or tertiary (body 
    displacement) blast injuries, PBLI is caused by the rapid pressure changes that 
    occur during explosive detonation.
    
    **Pressure Wave Dynamics:**
    - **Positive Phase**: Initial high-pressure wave compression
    - **Negative Phase**: Subsequent rarefaction and tissue expansion
    - **Frequency**: Multiple pressure oscillations cause tissue shearing
    - **Amplitude**: Pressure differential determines injury severity
    
    **Tissue-Level Changes:**
    - **Alveolar Rupture**: Direct mechanical disruption of alveolar walls
    - **Hemorrhage**: Capillary bleeding into alveolar spaces
    - **Air Embolism**: Gas bubble formation in pulmonary circulation
    - **Inflammatory Response**: Cytokine release and neutrophil infiltration
    
    **Clinical Manifestations:**
    - **Immediate**: Dyspnea, chest pain, hemoptysis, hypoxemia
    - **Early**: Pneumothorax, pneumomediastinum, subcutaneous emphysema
    - **Late**: ARDS development, secondary bacterial pneumonia
    
    **Comprehensive Score Components:**
    
    **1. PaO₂/FiO₂ Ratio (0-2 points):**
    
    **Physiological Significance:**
    The PaO₂/FiO₂ ratio represents the most sensitive indicator of blast lung injury 
    severity, reflecting the degree of ventilation-perfusion mismatch and alveolar-
    capillary membrane disruption.
    
    **Scoring Criteria:**
    - **>200 mmHg (0 points)**: Normal gas exchange, minimal injury
    - **60-200 mmHg (1 point)**: Moderate impairment, significant V/Q mismatch
    - **<60 mmHg (2 points)**: Severe hypoxemia, extensive lung damage
    
    **Clinical Correlation:**
    - Correlates directly with extent of alveolar flooding
    - Predicts need for mechanical ventilation
    - Guides oxygen supplementation requirements
    
    **2. Chest X-ray Findings (0-2 points):**
    
    **Radiographic Patterns:**
    Chest X-ray findings in PBLI reflect the anatomical distribution and extent 
    of lung injury, providing visual confirmation of clinical severity.
    
    **Scoring Criteria:**
    - **Localized infiltrates (0 points)**: Focal injury, limited lung involvement
    - **Bilateral/unilateral infiltrates (1 point)**: Moderate lung involvement
    - **Massive bilateral infiltrates (2 points)**: Extensive bilateral damage
    
    **Radiographic Evolution:**
    - **Initial**: May appear normal immediately post-blast
    - **Early (2-6 hours)**: Infiltrates develop as hemorrhage accumulates
    - **Late (12-24 hours)**: Full extent of injury becomes apparent
    
    **Advanced Imaging:**
    - **CT Scan**: More sensitive for detecting pneumothorax and contusions
    - **Ground Glass**: Indicates alveolar hemorrhage and edema
    - **Air Bronchograms**: Suggest alveolar filling processes
    
    **3. Bronchial Pleural Fistula (0-1 point):**
    
    **Pathophysiology:**
    Bronchial pleural fistula represents severe structural lung damage with abnormal 
    communication between the airways and pleural space. This complication significantly 
    complicates ventilatory management and increases mortality risk.
    
    **Clinical Recognition:**
    - **Persistent Air Leak**: Continuous bubbling in chest tube system
    - **Failure to Expand**: Lung remains collapsed despite chest drainage
    - **Subcutaneous Emphysema**: Air tracking through tissue planes
    - **Pneumomediastinum**: Air collection in mediastinal space
    
    **Management Challenges:**
    - **Ventilatory**: High airway pressures worsen air leak
    - **Surgical**: May require thoracotomy and surgical repair
    - **Hemodynamic**: Can cause tension pneumothorax
    
    **Severity Classification and Clinical Management:**
    
    **Mild Blast Lung Injury (0 points):**
    
    **Clinical Characteristics:**
    - Minimal respiratory symptoms
    - Normal or near-normal oxygenation
    - Localized or absent chest X-ray changes
    - No structural complications
    
    **Management Approach:**
    - **Ventilation**: Volume-controlled or pressure support modes
    - **PEEP**: ≤5 cm H₂O to maintain alveolar recruitment
    - **Monitoring**: Standard vital signs and pulse oximetry
    - **Disposition**: May be suitable for ward-level care
    
    **Prognosis**: Excellent (ARDS risk ~0%, Mortality ~0%)
    
    **Moderate Blast Lung Injury (1-4 points):**
    
    **Clinical Characteristics:**
    - Moderate respiratory compromise
    - Significant hypoxemia requiring supplemental oxygen
    - Bilateral or unilateral infiltrates on imaging
    - Possible minor air leaks
    
    **Management Approach:**
    - **Ventilation**: Conventional modes with lung-protective strategies
    - **PEEP**: 5-10 cm H₂O to optimize recruitment/over-distension balance
    - **Inverse Ratio**: Consider if conventional ventilation inadequate
    - **Monitoring**: Intensive care unit level monitoring required
    
    **Complications to Monitor:**
    - **Pneumothorax**: High index of suspicion
    - **ARDS Development**: 33% risk within 24-48 hours
    - **Secondary Infection**: Bacterial pneumonia risk
    
    **Prognosis**: Good (ARDS risk 33%, Mortality ~0%)
    
    **Severe Blast Lung Injury (5 points):**
    
    **Clinical Characteristics:**
    - Severe respiratory failure requiring immediate intervention
    - Profound hypoxemia refractory to conventional oxygen therapy
    - Massive bilateral infiltrates indicating extensive lung damage
    - Bronchial pleural fistula complicating ventilatory management
    
    **Management Approach:**
    - **Conventional Ventilation**: Lung-protective strategies with low tidal volumes
    - **PEEP**: >10 cm H₂O with careful monitoring for pneumothorax
    - **Advanced Therapies**: Multiple rescue interventions often required
    
    **Advanced Rescue Therapies:**
    - **Inhaled Nitric Oxide**: Selective pulmonary vasodilation
    - **High-Frequency Jet Ventilation**: Alternative ventilation mode
    - **Independent Lung Ventilation**: Differential lung management
    - **ECMO**: Extracorporeal membrane oxygenation for refractory cases
    
    **Surgical Interventions:**
    - **Thoracotomy**: For persistent bronchial pleural fistula
    - **Lung Isolation**: Independent lung ventilation techniques
    - **Pleurodesis**: For recurrent pneumothorax
    
    **Prognosis**: Poor (ARDS risk 100%, Mortality 75%)
    
    **Contemporary Clinical Applications:**
    
    **Military Medicine:**
    - Standardized triage in combat zone medical facilities
    - Resource allocation in austere environments
    - Evacuation priority determination
    - Inter-facility communication of injury severity
    
    **Civilian Emergency Medicine:**
    - Mass casualty incident management
    - Terrorist attack medical response
    - Industrial explosion assessment
    - Quality improvement and benchmarking
    
    **Critical Care Medicine:**
    - Ventilator weaning protocols
    - ECMO candidacy assessment
    - Family counseling and prognostication
    - Research stratification for clinical trials
    
    **Limitations and Considerations:**
    
    **Temporal Factors:**
    - Most accurate within 2 hours of injury
    - Later assessment may not reflect initial severity
    - Dynamic changes in clinical status require reassessment
    
    **Patient-Specific Factors:**
    - Age and comorbidities affect outcomes
    - Pregnancy considerations for management
    - Pediatric patients may require modified approaches
    
    **Technical Limitations:**
    - Requires arterial blood gas analysis
    - Quality chest X-ray may be challenging in trauma setting
    - Inter-observer variability in radiographic interpretation
    
    **Modern Developments:**
    - Integration with lung-protective ventilation protocols
    - Incorporation of newer imaging modalities
    - Combination with other trauma scoring systems
    - Adaptation for pediatric populations
    
    Args:
        request: Blast lung injury assessment parameters (PaO₂/FiO₂, chest X-ray, fistula)
        
    Returns:
        BlastLungInjurySeverityResponse: Severity score with ventilatory management guidance
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("blast_lung_injury_severity", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Blast Lung Injury Severity Score",
                    "details": {"parameters": parameters}
                }
            )
        
        return BlastLungInjurySeverityResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Blast Lung Injury Severity Score calculation",
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