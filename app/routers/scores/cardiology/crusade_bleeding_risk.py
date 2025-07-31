"""
CRUSADE Score for Post-MI Bleeding Risk Router

Endpoint for calculating CRUSADE bleeding risk scores.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.cardiology.crusade_bleeding_risk import (
    CrusadeBleedingRiskRequest,
    CrusadeBleedingRiskResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/crusade_bleeding_risk",
    response_model=CrusadeBleedingRiskResponse,
    summary="Calculate CRUSADE Score for Post-MI Bleeding Risk",
    description="Risk stratifies patients with NSTEMI undergoing anticoagulation to determine their risk of major bleeding during hospitalization",
    response_description="The calculated crusade bleeding risk with interpretation",
    operation_id="calculate_crusade_bleeding_risk"
)
async def calculate_crusade_bleeding_risk(request: CrusadeBleedingRiskRequest):
    """
    Calculates CRUSADE Score for Post-MI Bleeding Risk
    
    The CRUSADE bleeding risk score is a validated tool for stratifying major bleeding 
    risk in patients with acute coronary syndromes undergoing antithrombotic therapy. 
    Developed from over 71,000 NSTEMI patients in the CRUSADE Quality Improvement 
    Initiative, it helps clinicians balance thrombotic and bleeding risks when 
    selecting treatment strategies.
    
    **Clinical Background:**
    
    Acute coronary syndrome management involves potent antithrombotic medications and 
    invasive procedures that reduce ischemic complications but increase bleeding risk. 
    Major bleeding events are independently associated with increased mortality, 
    longer hospital stays, and worse long-term outcomes. The CRUSADE score provides 
    objective risk stratification to guide treatment decisions.
    
    **Scoring Components (8 Variables):**
    
    1. **Baseline Hematocrit (%)**:
       - <31%: 9 points - Severe anemia indicating bleeding risk
       - 31-33.9%: 7 points - Moderate anemia  
       - 34-36.9%: 3 points - Mild anemia
       - 37-39.9%: 2 points - Low-normal
       - ≥40%: 0 points - Normal hematocrit
    
    2. **Creatinine Clearance (mL/min)**:
       - ≤15: 39 points - Severe renal impairment
       - 15-30: 35 points - Moderate-severe impairment
       - 30-60: 28 points - Moderate impairment
       - 60-90: 17 points - Mild impairment
       - 90-120: 7 points - Low-normal function
       - >120: 0 points - Normal function
    
    3. **Heart Rate (bpm)**:
       - ≤70: 0 points - Normal/bradycardic
       - 71-80: 1 point - Normal
       - 81-90: 3 points - Mildly elevated
       - 91-100: 6 points - Moderately elevated
       - 101-110: 8 points - Significantly elevated
       - 111-120: 10 points - Markedly elevated
       - ≥121: 11 points - Severe tachycardia
    
    4. **Patient Sex**:
       - Male: 0 points
       - Female: 8 points - Independent risk factor for bleeding
    
    5. **Signs of CHF at Presentation**:
       - No: 0 points
       - Yes: 7 points - Dyspnea, rales, elevated JVP, S3 gallop
    
    6. **Diabetes Mellitus**:
       - No: 0 points  
       - Yes: 6 points - Type 1 or Type 2 diabetes
    
    7. **Prior Vascular Disease**:
       - No: 0 points
       - Yes: 6 points - PAD, CVD, aortic aneurysm
    
    8. **Systolic Blood Pressure (mmHg)**:
       - ≤90: 10 points - Hypotension/shock
       - 91-100: 8 points - Severe hypotension
       - 101-120: 5 points - Moderate hypotension
       - 121-180: 1 point - Normal range
       - 181-200: 3 points - Moderate hypertension
       - ≥201: 5 points - Severe hypertension
    
    **Risk Stratification and Bleeding Rates:**
    
    - **≤20 points**: Very Low Risk (3.1% bleeding rate)
      - Standard antithrombotic therapy appropriate
      - Routine bleeding monitoring
    
    - **21-30 points**: Low Risk (5.5% bleeding rate)
      - Standard therapy with routine monitoring
      - Consider patient education on bleeding signs
    
    - **31-40 points**: Moderate Risk (8.6% bleeding rate)
      - Consider dose modification or alternative agents
      - Enhanced bleeding monitoring and PPI therapy
    
    - **41-50 points**: High Risk (11.9% bleeding rate)
      - Reduced-dose regimens preferred
      - Intensive monitoring and shorter duration therapy
    
    - **>50 points**: Very High Risk (19.5% bleeding rate)
      - Minimal effective antithrombotic therapy
      - Very close monitoring and alternative strategies
    
    **Major Bleeding Definition:**
    - Hematocrit drop ≥12% from baseline
    - RBC transfusion when baseline hematocrit ≥28%
    - RBC transfusion with witnessed bleeding when baseline hematocrit <28%
    
    **Clinical Applications:**
    
    **Treatment Selection**:
    - Guide choice between full-dose vs reduced-dose antithrombotics
    - Selection of specific antiplatelet or anticoagulant agents
    - Duration of dual antiplatelet therapy optimization
    - Timing and extent of invasive interventions
    
    **Monitoring Strategies**:
    - Frequency of laboratory monitoring
    - Clinical assessment intervals
    - Bleeding education and prevention measures
    - Access site management protocols
    
    **Risk-Benefit Balance**:
    - Quantify bleeding risk to balance against ischemic benefit
    - Inform shared decision-making with patients
    - Guide multidisciplinary team discussions
    - Support quality improvement initiatives
    
    **Validation and Performance**:
    - Originally developed in 71,277 NSTEMI patients
    - Validated in independent cohort of 17,857 patients
    - Subsequently validated in STEMI patients
    - Demonstrates good discrimination (C-statistic 0.71)
    - Calibration maintained across multiple populations
    
    **Implementation Considerations**:
    - Calculate score before initiating antithrombotic therapy
    - Reassess if clinical status changes significantly
    - Consider concurrent ischemic risk assessment (e.g., GRACE score)
    - Integrate with institutional bleeding prevention protocols
    - Document risk assessment and treatment rationale
    
    **Evidence-Based Recommendations**:
    - Use in all ACS patients before antithrombotic initiation
    - Consider proton pump inhibitor for moderate to high risk patients
    - Implement enhanced monitoring protocols for high-risk patients
    - Evaluate alternative treatment strategies for very high-risk patients
    
    **References:**
    - Subherwal S, Bach RG, Chen AY, et al. Baseline risk of major bleeding in non-ST-segment-elevation myocardial infarction: the CRUSADE Bleeding Score. Circulation. 2009;119(14):1873-1882.
    - Abu-Assi E, Raposeiras-Roubin S, Lear P, et al. The risk of bleeding according to the CRUSADE, ACUITY and HAS-BLED scores in acute coronary syndrome patients treated with prasugrel. Thromb Res. 2013;132(6):652-658.
    
    Args:
        request: CRUSADE score parameters including clinical variables and laboratory values
        
    Returns:
        CrusadeBleedingRiskResponse: CRUSADE score with bleeding risk assessment and management recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("crusade_bleeding_risk", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating CRUSADE Score for Post-MI Bleeding Risk",
                    "details": {"parameters": parameters}
                }
            )
        
        return CrusadeBleedingRiskResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for CRUSADE Score for Post-MI Bleeding Risk",
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