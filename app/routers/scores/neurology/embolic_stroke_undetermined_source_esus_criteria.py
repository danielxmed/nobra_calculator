"""
Embolic Stroke of Undetermined Source (ESUS) Criteria Router

Endpoint for evaluating ESUS diagnostic criteria.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.neurology.embolic_stroke_undetermined_source_esus_criteria import (
    EmbolicStrokeUndeterminedSourceEsusCriteriaRequest,
    EmbolicStrokeUndeterminedSourceEsusCriteriaResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/embolic_stroke_undetermined_source_esus_criteria",
    response_model=EmbolicStrokeUndeterminedSourceEsusCriteriaResponse,
    summary="Calculate Embolic Stroke of Undetermined Source",
    description="Diagnostic criteria for identifying embolic stroke of undetermined source after comprehensive evaluation excluding other specific stroke etiologies.",
    response_description="The calculated embolic stroke undetermined source esus criteria with interpretation",
    operation_id="calculate_embolic_stroke_undetermined_source_esus_criteria"
)
async def calculate_embolic_stroke_undetermined_source_esus_criteria(request: EmbolicStrokeUndeterminedSourceEsusCriteriaRequest):
    """
    Evaluates Embolic Stroke of Undetermined Source (ESUS) Diagnostic Criteria
    
    The Embolic Stroke of Undetermined Source (ESUS) criteria provide a standardized 
    diagnostic framework for identifying patients with likely embolic strokes where 
    the source remains undetermined despite comprehensive evaluation. This diagnostic 
    construct represents a paradigm shift in stroke classification, moving away from 
    the less specific term "cryptogenic stroke" toward a more precise, clinically 
    actionable diagnosis.
    
    Historical Context and Development:
    
    The ESUS concept was introduced in 2014 by Hart et al. in response to the need 
    for a more standardized approach to classifying strokes of unknown etiology. 
    Traditional stroke classification systems, particularly the TOAST criteria, 
    created a heterogeneous "cryptogenic stroke" category that included patients 
    with multiple potential etiologies, incomplete workups, or truly undetermined 
    sources.
    
    The ESUS criteria were specifically designed to:
    - Create a more homogeneous patient population for clinical research
    - Enable focused therapeutic trials in stroke of undetermined etiology
    - Provide clearer diagnostic guidance for clinicians
    - Facilitate development of targeted prevention strategies
    - Support standardized outcome measurement and comparison
    
    Clinical Significance and Epidemiology:
    
    ESUS represents approximately 15-25% of all ischemic strokes, with significant 
    variation across different populations and healthcare systems. The prevalence 
    tends to be higher in:
    - Younger patients (mean age 65 vs 70 for all strokes)
    - Patients with milder strokes (mean NIHSS 5 vs 8 for all strokes)
    - Populations with access to comprehensive diagnostic evaluation
    - Academic medical centers with advanced imaging capabilities
    
    Demographic and Clinical Characteristics:
    - Mean age: 65 years (range typically 45-75)
    - Gender distribution: 42% women, 58% men
    - Mean NIHSS at presentation: 5 (indicating relatively mild strokes)
    - Median time to presentation: Similar to other stroke subtypes
    - Functional outcomes: Generally better than cardioembolic strokes
    - Mortality rates: Lower than large vessel atherothrombotic strokes
    
    Diagnostic Framework and Clinical Criteria:
    
    The ESUS diagnosis requires ALL FOUR clinical criteria to be satisfied:
    
    1. Non-lacunar Stroke on Brain Imaging:
    
    Clinical Rationale: Lacunar strokes typically result from small vessel disease 
    and are less likely to be embolic in nature. The size threshold distinguishes 
    between small vessel occlusion and larger vessel embolic events.
    
    Imaging Requirements:
    - CT or MRI demonstration of acute ischemic stroke
    - Infarct size >1.5 cm (>2.0 cm on MRI diffusion-weighted imaging)
    - Location outside typical small vessel territories
    - Pattern consistent with embolic rather than hemodynamic mechanism
    
    Technical Considerations:
    - DWI-MRI is preferred for accurate size measurement
    - Multiple small lesions may suggest embolic shower
    - Cortical involvement supports embolic mechanism
    - Watershed infarcts may suggest hemodynamic rather than embolic cause
    
    2. Absence of Significant Large Vessel Atherosclerosis:
    
    Clinical Rationale: Significant atherosclerotic stenosis (≥50%) represents 
    a clear mechanism for stroke through either artery-to-artery embolism or 
    hemodynamic compromise, excluding ESUS diagnosis.
    
    Vascular Imaging Requirements:
    - Comprehensive evaluation of extracranial and intracranial circulation
    - Assessment of vessels supplying the ischemic territory
    - Quantitative stenosis measurement when abnormalities are present
    - Evaluation for vessel wall changes, dissection, or other abnormalities
    
    Acceptable Imaging Modalities:
    - Digital subtraction angiography (gold standard)
    - CT angiography (CTA) with adequate resolution
    - MR angiography (MRA) including time-of-flight and contrast-enhanced
    - Cervical duplex ultrasonography PLUS transcranial Doppler
    - Combined approach may be needed for complete evaluation
    
    3. Absence of Major Cardioembolic Sources:
    
    Clinical Rationale: Major cardioembolic sources carry high stroke risk and 
    warrant anticoagulation, representing a distinct therapeutic category that 
    excludes ESUS classification.
    
    Major Cardioembolic Sources (High-Risk):
    - Permanent or paroxysmal atrial fibrillation
    - Sustained atrial flutter (>30 seconds)
    - Intracardiac thrombus (left atrial or ventricular)
    - Prosthetic cardiac valves (mechanical or bioprosthetic)
    - Atrial myxoma or other cardiac tumors
    - Mitral stenosis (rheumatic or congenital)
    - Recent myocardial infarction (<4 weeks)
    - Dilated cardiomyopathy (LVEF <30%)
    - Valvular vegetations (infectious or non-bacterial)
    - Active infective endocarditis
    
    Cardiac Evaluation Requirements:
    - 12-lead electrocardiogram
    - Minimum 24-hour cardiac monitoring with automated rhythm detection
    - Transthoracic echocardiography (TTE)
    - Transesophageal echocardiography (TEE) when TTE inadequate
    - Additional monitoring based on clinical suspicion
    
    4. Exclusion of Other Specific Stroke Etiologies:
    
    Clinical Rationale: ESUS is a diagnosis of exclusion requiring systematic 
    evaluation and exclusion of other well-defined stroke mechanisms.
    
    Other Specific Causes to Exclude:
    - Large vessel atherosclerosis (≥50% stenosis)
    - Small vessel disease (lacunar mechanism)
    - Arterial dissection (spontaneous or traumatic)
    - Vasculitis (primary or secondary)
    - Arteritis (infectious, autoimmune, drug-induced)
    - Migraine-related stroke (rare)
    - Vasospasm (subarachnoid hemorrhage, reversible cerebral vasoconstriction)
    - Drug-induced stroke (cocaine, amphetamines, oral contraceptives)
    - Genetic disorders (CADASIL, Fabry disease, mitochondrial disorders)
    - Hypercoagulable states (when clearly causative)
    - Moyamoya disease or syndrome
    - Cerebral venous thrombosis
    - Fat embolism or other systemic embolic sources
    
    Minimum Diagnostic Evaluation Requirements:
    
    The ESUS criteria mandate completion of adequate diagnostic evaluation 
    to ensure reliable exclusion of other stroke etiologies:
    
    Cardiac Monitoring Requirements:
    - Minimum 24 hours of continuous cardiac rhythm monitoring
    - Automated rhythm detection and analysis capability
    - Documentation of atrial fibrillation absence during monitoring period
    - Extended monitoring (48-72 hours) often recommended
    - Implantable cardiac monitors may be considered in selected cases
    
    Vascular Imaging Requirements:
    - Comprehensive imaging of extracranial cerebral circulation
    - Complete imaging of intracranial cerebral circulation
    - Assessment of vessels supplying the area of acute ischemia
    - Quantitative measurement of any identified stenosis
    - Evaluation for dissection, vasculitis, or other vessel wall abnormalities
    
    Cardiac Imaging Requirements:
    - Standard transthoracic echocardiography (TTE)
    - Assessment of left ventricular function and wall motion
    - Evaluation of valve structure and function
    - Search for intracardiac thrombus or masses
    - Transesophageal echocardiography (TEE) when indicated
    
    Clinical Management and Treatment Implications:
    
    ESUS Diagnosis Confirmed - Management Approach:
    
    Acute Management:
    - Standard acute stroke care protocols
    - Thrombolytic therapy when appropriate and timely
    - Mechanical thrombectomy for large vessel occlusion
    - Neurological monitoring and supportive care
    - Early mobilization and rehabilitation planning
    
    Secondary Prevention Strategies:
    - Antiplatelet therapy vs anticoagulation decision
    - Individual risk-benefit assessment
    - Consider extended cardiac monitoring
    - Evaluate for patent foramen ovale
    - Assess cardiovascular risk factors
    - Lifestyle modification counseling
    
    Extended Diagnostic Evaluation:
    - Prolonged cardiac monitoring (30-day event monitors)
    - Implantable cardiac monitors in selected patients
    - Bubble study or TEE for PFO evaluation
    - Hypercoagulability testing when appropriate
    - Genetic testing in young patients or family history
    - Advanced cardiac imaging (cardiac MRI) when indicated
    
    Clinical Trial Considerations:
    - ESUS-specific therapeutic trials
    - Registry participation for outcome tracking
    - Research protocol enrollment when appropriate
    - Long-term follow-up studies
    - Novel therapeutic agent trials
    
    Recent Clinical Trial Evidence and Treatment Paradigms:
    
    Anticoagulation Trials in ESUS:
    
    NAVIGATE ESUS Trial (2019):
    - Rivaroxaban vs aspirin in ESUS patients
    - Primary outcome: stroke, systemic embolism, or cardiovascular death
    - Results: No significant benefit of rivaroxaban over aspirin
    - Increased major bleeding with anticoagulation
    - Led to reassessment of blanket anticoagulation approach
    
    RE-SPECT ESUS Trial (2019):
    - Dabigatran vs aspirin in ESUS patients
    - Similar primary composite outcome
    - Results: No significant difference between treatments
    - Consistent with NAVIGATE ESUS findings
    - Reinforced need for patient selection strategies
    
    Implications of Trial Results:
    - Routine anticoagulation not superior to antiplatelet therapy
    - Need for better patient stratification and selection
    - Importance of identifying specific embolic sources
    - Role of extended monitoring in treatment decisions
    - Development of personalized prevention approaches
    
    Current Treatment Recommendations:
    
    Evidence-Based Approach:
    - Antiplatelet therapy (aspirin or clopidogrel) as first-line
    - Extended cardiac monitoring to detect atrial fibrillation
    - Anticoagulation when paroxysmal AF detected
    - Individualized assessment of bleeding vs thrombotic risk
    - PFO closure consideration in selected young patients
    
    Patient Selection for Anticoagulation:
    - High-risk clinical or imaging features
    - Recurrent strokes despite antiplatelet therapy
    - Evidence of multiple embolic events
    - Specific biomarkers or risk stratification tools
    - Clinical trial participation when available
    
    Risk Stratification and Prognostic Factors:
    
    Stroke Recurrence Risk:
    - Annual recurrence rate: approximately 4.5%
    - Similar to cardioembolic stroke recurrence
    - Higher than large vessel atherosclerosis
    - Lower than untreated atrial fibrillation
    
    Factors Associated with Higher Recurrence Risk:
    - Younger age (<60 years)
    - Multiple acute infarcts on initial imaging
    - Cortical involvement
    - Higher initial NIHSS score
    - Diabetes mellitus
    - Prior stroke or TIA
    - Elevated inflammatory markers
    
    Protective Factors:
    - Adequate secondary prevention therapy
    - Blood pressure control
    - Statin therapy
    - Smoking cessation
    - Regular cardiovascular exercise
    - Weight management
    
    Quality Improvement and Healthcare System Implications:
    
    Standardization Benefits:
    - Consistent diagnostic criteria across institutions
    - Improved communication between providers
    - Enhanced quality metrics and outcome tracking
    - Standardized research participation criteria
    - Better resource allocation and planning
    
    Healthcare Economic Considerations:
    - Cost-effectiveness of extended diagnostic workup
    - Optimal monitoring strategies and duration
    - Prevention of recurrent strokes through appropriate treatment
    - Resource utilization for advanced imaging and monitoring
    - Long-term healthcare costs and quality of life
    
    Future Directions and Emerging Concepts:
    
    Advanced Diagnostic Technologies:
    - High-resolution cardiac MRI for subtle abnormalities
    - Advanced echocardiographic techniques
    - Implantable cardiac monitors with extended battery life
    - Artificial intelligence-enhanced rhythm analysis
    - Genetic and biomarker testing for stroke risk
    
    Precision Medicine Approaches:
    - Biomarker-guided treatment selection
    - Genetic risk stratification
    - Personalized monitoring strategies
    - Targeted therapeutic interventions
    - Machine learning-based risk prediction
    
    Novel Therapeutic Targets:
    - Direct oral anticoagulants with improved safety profiles
    - Antiplatelet agents with enhanced efficacy
    - Combination therapy approaches
    - Device-based interventions for specific sources
    - Immunomodulatory approaches for inflammatory mechanisms
    
    Educational and Training Implications:
    
    Provider Education Needs:
    - Understanding of ESUS diagnostic criteria
    - Appropriate diagnostic workup strategies
    - Treatment decision-making algorithms
    - Patient counseling and shared decision-making
    - Recognition of clinical trial opportunities
    
    Patient Education Components:
    - Understanding of stroke mechanism and prognosis
    - Importance of medication adherence
    - Recognition of stroke warning signs
    - Risk factor modification strategies
    - Long-term monitoring requirements
    
    Conclusion and Clinical Practice Integration:
    
    The ESUS criteria represent a significant advancement in stroke classification 
    and management, providing a standardized framework for identifying and treating 
    patients with embolic strokes of undetermined source. While recent clinical 
    trials have challenged assumptions about optimal treatment approaches, the 
    ESUS construct continues to evolve and inform precision medicine approaches 
    to stroke prevention.
    
    Successful implementation requires:
    - Systematic application of diagnostic criteria
    - Completion of adequate diagnostic evaluation
    - Individualized treatment decision-making
    - Patient engagement in shared decision-making
    - Participation in clinical research when appropriate
    - Long-term follow-up and reassessment
    
    The ESUS framework will continue to evolve as our understanding of stroke 
    mechanisms advances and new diagnostic and therapeutic options become available. 
    Regular reassessment of diagnostic criteria and treatment approaches will be 
    essential to optimize outcomes for this important patient population.
    
    Args:
        request: ESUS diagnostic criteria evaluation parameters
        
    Returns:
        EmbolicStrokeUndeterminedSourceEsusCriteriaResponse: Diagnostic determination with clinical guidance
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("embolic_stroke_undetermined_source_esus_criteria", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error evaluating ESUS criteria",
                    "details": {"parameters": parameters}
                }
            )
        
        return EmbolicStrokeUndeterminedSourceEsusCriteriaResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for ESUS criteria evaluation",
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
                "message": "Internal error in ESUS criteria evaluation",
                "details": {"error": str(e)}
            }
        )