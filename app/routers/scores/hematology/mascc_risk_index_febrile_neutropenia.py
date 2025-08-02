"""
MASCC Risk Index for Febrile Neutropenia Router

Endpoint for calculating MASCC Risk Index for febrile neutropenia risk assessment.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.hematology.mascc_risk_index_febrile_neutropenia import (
    MasccRiskIndexFebrileNeutropeniaRequest,
    MasccRiskIndexFebrileNeutropeniaResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/mascc_risk_index_febrile_neutropenia",
    response_model=MasccRiskIndexFebrileNeutropeniaResponse,
    summary="Calculate MASCC Risk Index for Febrile Neutropenia",
    description="Calculates the MASCC (Multinational Association for Supportive Care in Cancer) "
                "Risk Index for identifying febrile neutropenia patients at low risk for poor "
                "outcome. This validated clinical prediction tool uses seven clinical variables "
                "to generate a score ranging from 0-26 points, with ≥21 points indicating low "
                "risk for serious complications including death, ICU admission, confusion, "
                "cardiac complications, respiratory failure, renal failure, hypotension, bleeding, "
                "and other serious medical complications. The index demonstrates 91% positive "
                "predictive value for uncomplicated course in low-risk patients, enabling "
                "evidence-based decisions regarding outpatient management with oral antibiotics "
                "versus inpatient care with intravenous therapy. Developed from international "
                "multicenter data and validated across diverse cancer populations, this tool "
                "is endorsed by the Infectious Diseases Society of America (IDSA) for "
                "standardizing febrile neutropenia management in adult cancer patients.",
    response_description="The calculated MASCC Risk Index score with risk stratification, positive predictive value, and comprehensive management recommendations",
    operation_id="mascc_risk_index_febrile_neutropenia"
)
async def calculate_mascc_risk_index_febrile_neutropenia(request: MasccRiskIndexFebrileNeutropeniaRequest):
    """
    Calculates MASCC Risk Index for Febrile Neutropenia Risk Assessment
    
    The MASCC Risk Index is a validated clinical prediction tool developed by the 
    Multinational Association for Supportive Care in Cancer to identify cancer patients 
    with febrile neutropenia who are at low risk for serious complications.
    
    **Seven Clinical Variables (Point Values):**
    
    1. **Burden of Illness (Symptom Severity)**:
       - **None/Mild (5 points)**: Well-appearing patient with minimal symptoms
       - **Moderate (3 points)**: Moderate symptoms affecting daily function
       - **Severe (0 points)**: Severe symptoms with significant distress or impairment
    
    2. **Hypotension**:
       - **No (5 points)**: Systolic BP ≥90 mmHg, hemodynamically stable
       - **Yes (0 points)**: Systolic BP <90 mmHg, hemodynamic compromise
    
    3. **Active COPD**:
       - **No (4 points)**: No active chronic obstructive pulmonary disease
       - **Yes (0 points)**: Active COPD increasing respiratory complication risk
    
    4. **Cancer Type and Fungal History**:
       - **Solid tumor OR hematologic without prior fungal (4 points)**: Lower infection risk
       - **Hematologic malignancy WITH prior fungal infection (0 points)**: Higher risk profile
    
    5. **Dehydration Requiring IV Fluids**:
       - **No (3 points)**: Adequate hydration status
       - **Yes (0 points)**: Volume depletion requiring intravenous fluid resuscitation
    
    6. **Status at Fever Onset**:
       - **Outpatient (3 points)**: Community-acquired episode, typically lower risk
       - **Inpatient (0 points)**: Nosocomial episode with higher complication potential
    
    7. **Age**:
       - **<60 years (2 points)**: Lower age-related complication risk
       - **≥60 years (0 points)**: Higher age-related risk for complications
    
    **Risk Stratification and Clinical Management:**
    
    **Low Risk (≥21 points):**
    - **Positive Predictive Value**: 91% for uncomplicated clinical course
    - **Management Options**: 
      - Oral antibiotic therapy consideration
      - Outpatient management with close follow-up
      - Early discharge from emergency department or hospital
    - **Monitoring Requirements**:
      - Reliable access to medical care within 24 hours
      - Patient education about warning signs
      - Ability to return immediately if symptoms worsen
      - Daily follow-up during first 48-72 hours
    - **Antibiotic Regimens**: 
      - Oral fluoroquinolone + amoxicillin-clavulanate
      - Alternative oral regimens based on local resistance patterns
    - **Patient Selection Criteria**:
      - Adequate social support system
      - Geographic proximity to medical facilities
      - Patient understanding and compliance
      - Absence of concerning clinical features
    
    **High Risk (<21 points):**
    - **Complication Risk**: Increased likelihood of serious complications
    - **Management Requirements**:
      - **Immediate hospitalization** if not already inpatient
      - **Empiric intravenous antibiotics** within 1 hour of presentation
      - **Intensive monitoring** for early complication recognition
    - **Potential Complications**:
      - Death, intensive care unit admission
      - Confusion, cardiac complications
      - Respiratory failure, renal failure
      - Hypotension, significant bleeding
      - Secondary infections, septic shock
    - **Treatment Approach**:
      - Broad-spectrum IV antibiotics (anti-pseudomonal coverage)
      - Aggressive supportive care measures
      - Early infectious disease consultation
      - ICU-level monitoring if unstable
    
    **Validation and Performance Characteristics:**
    - **Development**: 756 patients (derivation), 383 patients (validation)
    - **Original Performance**: PPV 91%, Sensitivity 71%, Specificity 68%
    - **External Validation**: Multiple studies showing PPV 83-98%, Sensitivity 59-95%
    - **Clinical Impact**: Demonstrated reduction in unnecessary hospitalizations
    - **Geographic Validation**: Confirmed across diverse healthcare systems globally
    - **Population Validation**: Consistent performance across cancer types
    
    **Clinical Applications:**
    - **Treatment Setting Decision**: Outpatient vs. inpatient management
    - **Antibiotic Route Selection**: Oral vs. intravenous therapy
    - **Resource Allocation**: Efficient use of hospital resources
    - **Quality Improvement**: Standardization of febrile neutropenia protocols
    - **Patient Counseling**: Evidence-based risk communication
    - **Clinical Research**: Risk stratification for clinical trials
    
    **Important Limitations and Considerations:**
    - **Population**: Adult patients only (≥18 years)
    - **Exclusions**: 
      - Acute leukemia patients (limited validation)
      - Stem cell transplant recipients (insufficient data)
      - Patients with obvious severe infections
    - **Not Incorporated**:
      - Absolute neutrophil count levels
      - Expected duration of neutropenia
      - Specific pathogen risks
      - Institutional resistance patterns
    - **Clinical Judgment Override**: Score should supplement, not replace clinical assessment
    - **Social Factors**: Consider patient's social circumstances and support systems
    - **Geographic Considerations**: Access to emergency medical care
    
    **Quality Assurance and Implementation:**
    - **Professional Endorsement**: IDSA guidelines recommendation
    - **Institutional Integration**: EMR integration and clinical decision support
    - **Outcome Monitoring**: Track complications in low-risk outpatients
    - **Staff Education**: Training on appropriate score application
    - **Patient Education**: Clear instructions on warning signs and follow-up
    - **Continuous Improvement**: Regular review of outcomes and score performance
    
    **Recent Developments:**
    - **Alternative Scores**: CISNE (Clinical Index of Stable Febrile Neutropenia)
    - **Population-Specific Refinements**: Hematologic malignancy modifications
    - **Technology Integration**: Mobile apps and clinical decision support systems
    - **Outcome Studies**: Long-term safety data in outpatient populations
    
    **References:**
    1. Klastersky J, Paesmans M, Rubenstein EB, et al. The Multinational Association 
       for Supportive Care in Cancer risk index: A multinational scoring system for 
       identifying low-risk febrile neutropenic cancer patients. J Clin Oncol. 
       2000;18(16):3038-51.
    2. Freifeld AG, Bow EJ, Sepkowitz KA, et al. Clinical practice guideline for the 
       use of antimicrobial agents in neutropenic patients with cancer: 2010 update 
       by the infectious diseases society of america. Clin Infect Dis. 2011;52(4):e56-93.
    3. Uys A, Rapoport BL, Anderson R. Febrile neutropenia: a prospective study to 
       validate the Multinational Association of Supportive Care of Cancer (MASCC) 
       risk-index score. Support Care Cancer. 2004;12(8):555-60.
    
    Args:
        request: MASCC Risk Index parameters including burden of illness, hypotension, 
        COPD status, cancer type, dehydration, fever onset status, and age
        
    Returns:
        MasccRiskIndexFebrileNeutropeniaResponse: Calculated score with risk stratification, 
        positive predictive value, and comprehensive management recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("mascc_risk_index_febrile_neutropenia", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating MASCC Risk Index for Febrile Neutropenia",
                    "details": {"parameters": parameters}
                }
            )
        
        return MasccRiskIndexFebrileNeutropeniaResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for MASCC Risk Index for Febrile Neutropenia",
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