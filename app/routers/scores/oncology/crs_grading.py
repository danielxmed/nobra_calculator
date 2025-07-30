"""
Cytokine Release Syndrome (CRS) Grading Router

Endpoint for calculating CRS severity grading using ASTCT consensus criteria.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.oncology.crs_grading import (
    CrsGradingRequest,
    CrsGradingResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post("/crs_grading", response_model=CrsGradingResponse)
async def calculate_crs_grading(request: CrsGradingRequest):
    """
    Calculates Cytokine Release Syndrome (CRS) Grading using ASTCT Consensus Criteria
    
    Cytokine Release Syndrome (CRS) is an acute inflammatory process characterized by 
    systemic inflammation and a spectrum of clinical symptoms that can range from mild 
    constitutional symptoms to life-threatening organ dysfunction. CRS is most commonly 
    associated with immune effector cell therapies, particularly CAR-T cell therapy, 
    but can also occur with other immunotherapies.
    
    **Clinical Background:**
    
    The American Society for Transplantation and Cellular Therapy (ASTCT) developed 
    consensus grading criteria in 2019 to standardize CRS assessment across institutions 
    and clinical trials. This standardization is critical for:
    
    - Consistent patient management and treatment decisions
    - Reliable communication between healthcare providers
    - Meaningful comparison of clinical trial data
    - Quality improvement and safety monitoring
    - Regulatory compliance and reporting
    
    **Pathophysiology and Clinical Presentation:**
    
    CRS results from massive activation of immune cells and subsequent release of 
    inflammatory cytokines including IL-6, TNF-α, IL-1β, and interferon-γ. This 
    cytokine storm leads to:
    
    **Constitutional Symptoms:**
    - Fever (often the first and most common symptom)
    - Fatigue, malaise, and weakness
    - Headache and myalgias
    - Nausea, vomiting, and decreased appetite
    - Altered mental status in severe cases
    
    **Cardiovascular Manifestations:**
    - Hypotension progressing to shock
    - Increased capillary permeability and fluid extravasation
    - Cardiac dysfunction and arrhythmias
    - Requirement for vasopressor support
    
    **Respiratory Complications:**
    - Hypoxemia and increased oxygen requirements
    - Pulmonary edema and acute respiratory distress
    - Need for supplemental oxygen or mechanical ventilation
    
    **Multi-organ Effects:**
    - Hepatic dysfunction with elevated transaminases
    - Renal impairment and acute kidney injury
    - Coagulopathy and bleeding complications
    - Neurologic symptoms (though distinct from ICANS)
    
    **ASTCT Grading Criteria (2019):**
    
    **Grade 1 - Mild CRS:**
    - **Requirements**: Fever ≥38°C (required unless suppressed by therapy)
    - **Characteristics**: Constitutional symptoms only
    - **Management**: Symptomatic treatment and supportive care
    - **Monitoring**: Standard vital signs every 4-8 hours
    - **Prognosis**: Excellent with complete recovery expected
    
    **Grade 2 - Moderate CRS:**
    - **Requirements**: Fever plus moderate organ dysfunction
    - **Hypotension**: Responsive to IV fluids or low-dose single vasopressor
    - **Oxygen**: Low-flow supplemental oxygen (<40% FiO2)
    - **Management**: Vigilant supportive care, consider tocilizumab
    - **Monitoring**: Enhanced monitoring every 2-4 hours
    - **Setting**: Inpatient ward with step-down unit capability
    
    **Grade 3 - Severe CRS:**
    - **Requirements**: Fever plus severe organ dysfunction
    - **Hypotension**: Requires high-dose or multiple vasopressors
    - **Oxygen**: High-flow oxygen ≥40% FiO2 or high-flow nasal cannula
    - **Organ Toxicity**: Grade 3 per CTCAE or Grade 4 transaminitis
    - **Management**: Tocilizumab + corticosteroids, ICU care
    - **Monitoring**: Continuous monitoring in ICU setting
    - **Setting**: Intensive care unit required
    
    **Grade 4 - Life-threatening CRS:**
    - **Requirements**: Life-threatening organ dysfunction
    - **Respiratory**: Requires positive pressure ventilation
    - **Organ Toxicity**: Grade 4 per CTCAE (except transaminitis)
    - **Management**: Immediate tocilizumab + corticosteroids + organ support
    - **Monitoring**: Continuous ICU monitoring with advanced support
    - **Setting**: ICU with advanced life support capabilities
    
    **Grade 5 - Fatal CRS:**
    - **Definition**: Death directly attributable to CRS
    - **Management**: Comfort care and family support
    - **Documentation**: Root cause analysis for quality improvement
    
    **Clinical Assessment Parameters:**
    
    **Fever Evaluation:**
    - Temperature ≥38°C (100.4°F) measured by any route
    - Consider fever "present" if suppressed by anti-pyretics or anti-cytokine therapy
    - Document timing, pattern, and response to interventions
    - Note: Fever not required for Grades 2-4 if actively suppressed
    
    **Hypotension Assessment:**
    - Age-appropriate blood pressure thresholds
    - Response to fluid resuscitation (crystalloids, colloids)
    - Vasopressor requirements and dosing
    - Consider baseline blood pressure and comorbidities
    
    **Oxygen Requirements:**
    - Room air oxygen saturation and arterial blood gas
    - FiO2 requirements and delivery method
    - Response to oxygen therapy and position changes
    - Need for positive pressure ventilation
    
    **Organ Toxicity Evaluation:**
    - Use CTCAE v5.0 criteria for consistency
    - Focus on non-fever, non-hypotension manifestations
    - Common organs: liver, kidney, cardiac, neurologic
    - Document baseline function for comparison
    
    **Risk Factors and Modifying Factors:**
    
    **Patient-Related Factors:**
    - Age: Pediatric and elderly patients may have different presentations
    - Comorbidities: Cardiovascular, pulmonary, hepatic, renal disease
    - Performance status and baseline functional capacity
    - Previous exposure to immunotherapies
    
    **Disease-Related Factors:**
    - Tumor burden and disease activity
    - Previous treatments and response history
    - Concurrent infections or inflammatory conditions
    
    **Treatment-Related Factors:**
    - Type of immune effector cell therapy (CAR-T, TCR-T, etc.)
    - Cell dose and expansion characteristics
    - Timing since infusion (typically 1-14 days)
    - Premedication regimens used
    
    **Management Principles by Grade:**
    
    **Grade 1 Management:**
    - Supportive care with symptom management
    - Acetaminophen/paracetamol for fever control
    - Adequate hydration and electrolyte monitoring
    - Close observation for progression
    - No specific anti-cytokine therapy required
    
    **Grade 2 Management:**
    - Enhanced monitoring with frequent vital signs
    - IV fluid resuscitation for hypotension
    - Low-flow oxygen for hypoxemia
    - Consider tocilizumab if extensive comorbidities present
    - Monitor for progression to higher grades
    
    **Grade 3 Management:**
    - ICU-level care with continuous monitoring
    - Tocilizumab 8 mg/kg IV (maximum 800 mg)
    - Consider corticosteroids if no improvement in 24 hours
    - High-dose or multiple vasopressors as needed
    - Advanced respiratory support with high-flow oxygen
    
    **Grade 4 Management:**
    - Immediate ICU care with advanced life support
    - Tocilizumab + corticosteroids (methylprednisolone 1-2 mg/kg/day)
    - Mechanical ventilation and advanced organ support
    - Multidisciplinary critical care team approach
    - Consider additional immunosuppressive agents if refractory
    
    **Tocilizumab Administration:**
    - Dosing: 8 mg/kg IV (maximum 800 mg per dose)
    - May repeat after 8 hours if inadequate response
    - Maximum recommended doses: 3-4 total
    - Monitor for infections and infusion reactions
    - Document response and time to clinical improvement
    
    **Corticosteroid Use:**
    - Indication: Grade 3-4 CRS or refractory Grade 2
    - Dosing: Methylprednisolone 1-2 mg/kg/day IV
    - Duration: Typically 2-3 days with rapid taper
    - Monitor for infections, hyperglycemia, psychiatric effects
    - Consider prophylaxis for opportunistic infections
    
    **Monitoring and Assessment:**
    
    **Vital Signs Monitoring:**
    - Grade 1: Every 4-8 hours
    - Grade 2: Every 2-4 hours
    - Grade 3-4: Continuous monitoring
    
    **Laboratory Monitoring:**
    - Complete blood count with differential
    - Comprehensive metabolic panel
    - Liver function tests
    - Coagulation studies (PT/PTT, fibrinogen, D-dimer)
    - Inflammatory markers (CRP, ferritin, IL-6 if available)
    - Arterial blood gas analysis for severe cases
    
    **Imaging Studies:**
    - Chest X-ray or CT for respiratory symptoms
    - Echocardiogram for cardiac dysfunction
    - Additional imaging based on organ involvement
    
    **Infection Surveillance:**
    - Blood cultures and appropriate cultures
    - Monitor for opportunistic infections
    - Consider prophylactic antimicrobials in high-risk patients
    
    **Complications and Special Considerations:**
    
    **Infection Risk:**
    - Immunosuppressive treatments increase infection susceptibility
    - Monitor for bacterial, viral, and fungal infections
    - Maintain appropriate infection control precautions
    - Consider prophylactic antimicrobials in select cases
    
    **Concurrent ICANS:**
    - Immune effector cell-associated neurotoxicity syndrome
    - Can occur concurrently with or independently of CRS
    - Requires separate assessment and grading
    - May influence treatment decisions and timing
    
    **Refractory CRS:**
    - Inadequate response to standard therapy
    - Consider additional immunosuppressive agents
    - Evaluate for concurrent infections or complications
    - Multidisciplinary consultation recommended
    
    **Prognostic Factors:**
    
    **Favorable Prognostic Factors:**
    - Younger age and good performance status
    - Rapid response to initial therapy
    - Lower peak cytokine levels
    - Absence of significant comorbidities
    
    **Adverse Prognostic Factors:**
    - Advanced age and multiple comorbidities
    - High tumor burden at treatment
    - Delayed or inadequate response to therapy
    - Concurrent organ dysfunction
    
    **Quality Measures and Outcomes:**
    
    **Clinical Outcomes:**
    - Time to CRS resolution
    - ICU length of stay
    - Need for mechanical ventilation
    - Overall mortality related to CRS
    
    **Quality Indicators:**
    - Time to recognition and grading
    - Appropriate escalation of care
    - Adherence to treatment guidelines
    - Patient and family education and engagement
    
    **Research and Future Directions:**
    
    **Biomarker Development:**
    - Predictive biomarkers for CRS development
    - Early detection markers for intervention
    - Prognostic indicators for severity and duration
    
    **Treatment Innovations:**
    - Novel cytokine inhibitors and immunomodulators
    - Personalized treatment approaches
    - Preventive strategies and prophylactic interventions
    
    **Implementation Considerations:**
    
    **Institutional Requirements:**
    - Standardized assessment protocols and documentation
    - Staff training on CRS recognition and management
    - Availability of tocilizumab and corticosteroids
    - ICU capacity and critical care expertise
    
    **Patient and Family Education:**
    - Pre-treatment counseling on CRS risks and symptoms
    - Instructions for reporting concerning symptoms
    - Ongoing communication during treatment course
    - Post-treatment follow-up and surveillance
    
    Args:
        request: CRS grading parameters including fever, hypotension status, 
                oxygen requirements, organ toxicity grade, and optional risk factors
        
    Returns:
        CrsGradingResponse: Comprehensive CRS assessment including grade, severity 
        classification, clinical interpretation, management recommendations, and 
        monitoring guidance
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("crs_grading", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Cytokine Release Syndrome Grading",
                    "details": {"parameters": parameters}
                }
            )
        
        return CrsGradingResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Cytokine Release Syndrome Grading",
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