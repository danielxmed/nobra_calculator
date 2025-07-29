"""
Berlin Criteria for Acute Respiratory Distress Syndrome (ARDS) Router

Endpoint for calculating ARDS diagnosis and severity classification using the Berlin Definition.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.pulmonology.berlin_criteria_ards import (
    BerlinCriteriaArdsRequest,
    BerlinCriteriaArdsResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post("/berlin_criteria_ards", response_model=BerlinCriteriaArdsResponse)
async def calculate_berlin_criteria_ards(request: BerlinCriteriaArdsRequest):
    """
    Calculates Berlin Criteria for Acute Respiratory Distress Syndrome (ARDS)
    
    The Berlin Definition for ARDS (2012) is the current international standard for 
    diagnosing and classifying acute respiratory distress syndrome. It replaced the 
    previous American-European Consensus Conference definition and provides improved 
    diagnostic accuracy and prognostic value.
    
    **Required Diagnostic Criteria (ALL must be met):**
    
    **1. Timing:**
    - Acute onset within 1 week of known clinical insult
    - OR new/worsening respiratory symptoms within 1 week
    
    **2. Chest Imaging:**
    - Bilateral opacities on chest X-ray or CT scan
    - Not fully explained by effusions, lobar/lung collapse, or nodules
    
    **3. Origin of Pulmonary Edema:**
    - Respiratory failure NOT fully explained by cardiac failure or fluid overload
    - May require objective assessment (echocardiography) if no ARDS risk factors
    
    **4. Oxygenation (with PEEP ≥5 cm H2O):**
    - Measured PaO2/FiO2 ratio determines severity classification
    
    **ARDS Severity Classifications:**
    
    **Mild ARDS:**
    - PaO2/FiO2 >200 to ≤300 mmHg with PEEP ≥5 cm H2O
    - Mortality: ~27%
    - Management: Lung-protective ventilation, conservative fluid strategy
    
    **Moderate ARDS:**
    - PaO2/FiO2 >100 to ≤200 mmHg with PEEP ≥5 cm H2O
    - Mortality: ~32%
    - Management: Enhanced strategies, consider prone positioning
    
    **Severe ARDS:**
    - PaO2/FiO2 ≤100 mmHg with PEEP ≥5 cm H2O
    - Mortality: ~45%
    - Management: Aggressive interventions, prone positioning, consider ECMO
    
    **Common ARDS Risk Factors:**
    
    **Direct Lung Injury:**
    - Pneumonia (bacterial, viral, fungal)
    - Aspiration of gastric contents
    - Pulmonary contusion from trauma
    - Inhalation injury (smoke, toxic gases)
    - Near drowning
    - Fat embolism syndrome
    
    **Indirect Lung Injury:**
    - Sepsis (most common cause)
    - Severe trauma with shock
    - Acute pancreatitis
    - Massive blood transfusion
    - Drug overdose or toxicity
    - Severe burns
    - Transfusion-related acute lung injury (TRALI)
    
    **Clinical Assessment Guidelines:**
    
    **Oxygenation Measurement:**
    - PaO2/FiO2 ratio MUST be measured with PEEP or CPAP ≥5 cm H2O
    - Use arterial blood gas for accurate PaO2 measurement
    - If altitude >1000m, apply correction: PaO2/FiO2 × (barometric pressure/760)
    
    **Imaging Interpretation:**
    - Bilateral opacities should be consistent with pulmonary edema
    - May be subtle in early stages
    - CT scan more sensitive than chest X-ray for bilateral involvement
    
    **Cardiac Assessment:**
    - Clinical assessment may suffice if clear ARDS risk factors present
    - Echocardiography recommended if cardiac cause suspected
    - BNP/NT-proBNP may help distinguish from cardiogenic pulmonary edema
    
    **Management Principles:**
    
    **All ARDS Patients:**
    - Low tidal volume ventilation (6 mL/kg predicted body weight)
    - Plateau pressure <30 cm H2O
    - Conservative fluid management when hemodynamically stable
    - Avoid unnecessary sedation
    
    **Moderate-Severe ARDS:**
    - Higher PEEP strategies (PEEP titration tables)
    - Prone positioning for >12 hours daily
    - Consider neuromuscular blockade (first 48 hours)
    - Monitor for ventilator-associated complications
    
    **Severe ARDS:**
    - All above interventions
    - Consider ECMO if conventional therapy failing
    - Recruitment maneuvers in selected patients
    - Inhaled pulmonary vasodilators in selected cases
    
    **Prognosis and Outcomes:**
    - Overall ARDS mortality has improved but remains significant
    - Long-term survivors may have cognitive impairment, weakness, PTSD
    - Pulmonary function typically recovers within first year
    - Quality of life generally returns to baseline over time
    
    **Differential Diagnosis:**
    - Cardiogenic pulmonary edema
    - Diffuse alveolar hemorrhage
    - Acute interstitial pneumonia
    - Hypersensitivity pneumonitis
    - Drug-induced lung injury
    
    Args:
        request: Berlin Criteria ARDS assessment parameters
        
    Returns:
        BerlinCriteriaArdsResponse: ARDS diagnosis and severity with clinical recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("berlin_criteria_ards", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Berlin Criteria for ARDS",
                    "details": {"parameters": parameters}
                }
            )
        
        return BerlinCriteriaArdsResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Berlin Criteria ARDS calculation",
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