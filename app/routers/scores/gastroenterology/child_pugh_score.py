"""
Child-Pugh Score for Cirrhosis Mortality Router

Endpoint for calculating Child-Pugh Score for cirrhosis severity assessment.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.gastroenterology.child_pugh_score import (
    ChildPughScoreRequest,
    ChildPughScoreResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/child_pugh_score",
    response_model=ChildPughScoreResponse,
    summary="Calculate Child-Pugh Score for Cirrhosis Mortality",
    description="Estimates severity of cirrhosis and prognosis in patients with chronic liver disease",
    response_description="The calculated child pugh score with interpretation",
    operation_id="calculate_child_pugh_score"
)
async def calculate_child_pugh_score(request: ChildPughScoreRequest):
    """
    Calculates Child-Pugh Score for Cirrhosis Mortality
    
    The Child-Pugh Score estimates the severity of cirrhosis and prognosis in patients 
    with chronic liver disease. Originally developed to predict mortality during 
    portacaval shunt surgery, it has become a widely used tool for assessing prognosis 
    and determining treatment options in cirrhotic patients.
    
    **Historical Development**:
    
    **Original Child-Turcotte Classification (1964)**:
    - Developed by Charles Child and John Turcotte for surgical risk assessment
    - Used subjective measures of nutritional status and neurological function
    - Applied to patients undergoing portacaval shunt procedures
    - Established foundation for liver disease severity scoring
    
    **Pugh Modification (1973)**:
    - Modified by Pugh et al. to include more objective laboratory parameters
    - Replaced subjective nutritional assessment with serum albumin
    - Standardized encephalopathy grading system
    - Introduced the familiar scoring system still used today
    
    **Clinical Validation and Adoption**:
    - Extensively validated across diverse cirrhotic populations
    - Adopted worldwide as standard cirrhosis severity measure
    - Integrated into clinical guidelines and practice recommendations
    - Basis for drug dosing modifications in hepatic impairment
    
    **Child-Pugh Scoring System**:
    
    **Laboratory Parameters (Objective Measures)**:
    
    **Total Bilirubin (mg/dL)**:
    - Reflects hepatic synthetic function and biliary excretion capacity
    - Elevated levels indicate impaired liver function or obstruction
    - 1 point: <2.0 mg/dL (Normal to mild elevation)
    - 2 points: 2.0-3.0 mg/dL (Moderate elevation)
    - 3 points: >3.0 mg/dL (Severe elevation)
    
    **Serum Albumin (g/dL)**:
    - Exclusively synthesized by liver with ~20-day half-life
    - Reflects hepatic synthetic capacity and nutritional status
    - 1 point: >3.5 g/dL (Normal synthetic function)
    - 2 points: 2.8-3.5 g/dL (Mild synthetic impairment)
    - 3 points: <2.8 g/dL (Severe synthetic impairment)
    
    **International Normalized Ratio (INR)**:
    - Measures coagulation function and clotting factor synthesis
    - More standardized than prothrombin time across laboratories
    - 1 point: <1.7 (Mild coagulopathy)
    - 2 points: 1.7-2.3 (Moderate coagulopathy)
    - 3 points: >2.3 (Severe coagulopathy)
    
    **Clinical Parameters (Subjective Assessment)**:
    
    **Ascites Severity**:
    - Fluid accumulation due to portal hypertension and hypoalbuminemia
    - Assessment based on physical examination and imaging studies
    - 1 point: Absent (No detectable fluid accumulation)
    - 2 points: Slight (Mild ascites, responsive to diuretics)
    - 3 points: Moderate (Tense ascites, refractory to medical therapy)
    
    **Hepatic Encephalopathy Grade**:
    - Neuropsychiatric syndrome from hepatic dysfunction and shunting
    - West Haven criteria for standardized grading
    - 1 point: None (Normal consciousness and cognitive function)
    - 2 points: Grade 1-2 (Subtle changes, altered sleep, mild confusion)
    - 3 points: Grade 3-4 (Stupor, somnolence, coma)
    
    **Child-Pugh Classification and Prognosis**:
    
    **Grade A (5-6 points): Well-compensated Disease**:
    - **Survival**: One-year ~100%, Two-year ~85%
    - **Operative Risk**: Excellent (<5% perioperative mortality)
    - **Clinical Features**: Minimal symptoms, preserved liver function
    - **Management**: 
      - Suitable for major surgery including liver resection
      - Variceal screening and primary prophylaxis
      - Hepatocellular carcinoma surveillance
      - Standard medical therapy with minimal dose adjustments
    - **Prognosis**: Excellent long-term survival with appropriate care
    
    **Grade B (7-9 points): Significant Functional Compromise**:
    - **Survival**: One-year ~80%, Two-year ~60%
    - **Operative Risk**: Good (5-15% perioperative mortality)
    - **Clinical Features**: Moderate symptoms, functional limitations
    - **Management**:
      - Consider surgery with caution and multidisciplinary assessment
      - Liver transplant evaluation may be appropriate
      - Close monitoring for complications and disease progression
      - Drug dosing modifications often required
    - **Prognosis**: Intermediate survival requiring careful monitoring
    
    **Grade C (10-15 points): Decompensated Disease**:
    - **Survival**: One-year ~45%, Two-year ~35%
    - **Operative Risk**: Poor (>15% perioperative mortality)
    - **Clinical Features**: Severe symptoms, significant functional impairment
    - **Management**:
      - Major surgery generally contraindicated
      - Priority candidate for liver transplantation
      - Palliative care considerations for symptom management
      - Careful attention to drug interactions and dosing
    - **Prognosis**: Poor survival without intervention
    
    **Clinical Applications and Decision-Making**:
    
    **Surgical Risk Stratification**:
    - Pre-operative assessment for hepatic resection
    - Risk-benefit analysis for non-hepatic surgery
    - Perioperative monitoring and management planning
    - Post-operative complication prediction
    
    **Liver Transplant Evaluation**:
    - Initial screening for transplant candidacy
    - Timing of transplant evaluation and listing
    - Priority scoring (though MELD now used for allocation)
    - Monitoring while on transplant waiting list
    
    **Medical Management Guidance**:
    - Drug dosing modifications in hepatic impairment
    - Contraindication assessment for hepatotoxic medications
    - Monitoring frequency for disease progression
    - Palliative care referral considerations
    
    **Clinical Trial and Research Applications**:
    - Patient stratification in clinical studies
    - Inclusion/exclusion criteria for therapeutic trials
    - Outcome prediction and risk adjustment
    - Disease severity standardization across studies
    
    **Quality Improvement and Population Health**:
    - Performance metrics for cirrhosis care
    - Resource allocation and care pathway development
    - Population risk stratification
    - Healthcare utilization prediction
    
    **Monitoring and Reassessment Framework**:
    
    **Assessment Frequency**:
    - Grade A: Every 6-12 months or with clinical changes
    - Grade B: Every 3-6 months with closer monitoring
    - Grade C: Every 1-3 months or as clinically indicated
    
    **Clinical Triggers for Reassessment**:
    - New or worsening symptoms (ascites, encephalopathy)
    - Laboratory value changes
    - Complications (variceal bleeding, infection)
    - Treatment response evaluation
    - Pre-operative assessment
    
    **Integration with Other Assessment Tools**:
    - MELD/MELD-Na scores for transplant allocation
    - Barcelona Clinic Liver Cancer (BCLC) staging
    - Hepatic Venous Pressure Gradient (HVPG) measurements
    - Quality of life assessments
    
    **Limitations and Clinical Considerations**:
    
    **Score Limitations**:
    - Subjective elements (ascites, encephalopathy assessment)
    - Inter-observer variability in clinical parameters
    - Less sensitive to rapid changes in clinical condition
    - Limited utility in acute liver failure
    - May not reflect modern medical management improvements
    
    **Contemporary Alternatives**:
    - MELD and MELD-Na scores for more objective assessment
    - Chronic Liver Failure-Consortium scores for acute-on-chronic failure
    - Fibrosis-specific scores for earlier disease stages
    - Dynamic risk assessment tools
    
    **Special Populations**:
    - Pediatric patients (modified scoring systems available)
    - Acute-on-chronic liver failure (specialized scores preferred)
    - Post-liver transplant assessment (different considerations)
    - Non-cirrhotic portal hypertension (limited applicability)
    
    This calculator provides evidence-based cirrhosis severity assessment to support 
    clinical decision-making in patient management, surgical planning, and prognostic 
    counseling for patients with chronic liver disease.
    
    Args:
        request: Child-Pugh score parameters for cirrhosis severity assessment
        
    Returns:
        ChildPughScoreResponse: Score with prognostic information and clinical recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("child_pugh_score", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Child-Pugh Score",
                    "details": {"parameters": parameters}
                }
            )
        
        return ChildPughScoreResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Child-Pugh Score",
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