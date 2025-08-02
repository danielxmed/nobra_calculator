"""
Rule of 7s for Lyme Meningitis Router

Endpoint for calculating Rule of 7s for Lyme meningitis prediction.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.emergency.rule_of_7s_lyme_meningitis import (
    RuleOf7sLymeMeningitisRequest,
    RuleOf7sLymeMeningitisResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/rule_of_7s_lyme_meningitis",
    response_model=RuleOf7sLymeMeningitisResponse,
    summary="Calculate Rule of 7s for Lyme Meningitis",
    description="Calculates the Rule of 7s clinical prediction rule to distinguish Lyme meningitis from "
                "aseptic meningitis in pediatric patients (ages 2-18) in Lyme disease-endemic areas. "
                "This validated tool uses three readily available clinical criteria: duration of headache, "
                "percentage of CSF mononuclear cells, and presence of cranial nerve palsy. The rule "
                "identifies children at low risk for Lyme meningitis (score = 0) who can be safely "
                "managed as outpatients while awaiting Lyme serology results, avoiding unnecessary "
                "hospitalizations and empirical parenteral antibiotics. Validation studies demonstrate "
                "96% sensitivity and 100% negative predictive value for low-risk identification. "
                "Children with scores of 1-3 points are not low risk and require consideration for "
                "inpatient management and empirical antibiotic treatment. The rule performs significantly "
                "better than complex mathematical prediction models while being considerably easier to "
                "apply in clinical practice. Essential for emergency physicians and pediatricians in "
                "Lyme-endemic regions to make evidence-based decisions about CSF pleocytosis management.",
    response_description="Rule of 7s score with risk stratification and evidence-based clinical management recommendations",
    operation_id="rule_of_7s_lyme_meningitis"
)
async def calculate_rule_of_7s_lyme_meningitis(request: RuleOf7sLymeMeningitisRequest):
    """
    Rule of 7s for Lyme Meningitis Clinical Prediction Assessment
    
    Calculates the validated Rule of 7s clinical prediction rule to distinguish 
    Lyme meningitis from aseptic meningitis in pediatric patients presenting with 
    cerebrospinal fluid pleocytosis in Lyme disease-endemic areas. This evidence-based 
    tool supports clinical decision-making regarding outpatient versus inpatient 
    management while awaiting confirmatory Lyme serology results.
    
    Clinical Background and Epidemiologic Context:
    Lyme disease represents the most common vector-borne illness in the United States, 
    with over 30,000 cases reported annually to the CDC. Neurologic manifestations 
    occur in approximately 10-15% of untreated cases, with meningitis being the most 
    common neurologic presentation in children. The disease demonstrates significant 
    geographic clustering in endemic areas, particularly the northeastern and upper 
    midwestern United States.
    
    The clinical challenge in emergency departments and pediatric practices lies in 
    distinguishing Lyme meningitis from viral (aseptic) meningitis, as both conditions 
    present with similar symptoms including headache, neck stiffness, photophobia, 
    nausea, and fever. Cerebrospinal fluid findings also overlap significantly, with 
    both conditions typically showing lymphocytic pleocytosis, elevated protein, and 
    normal or slightly decreased glucose.
    
    Clinical Presentation and Diagnostic Challenges:
    
    Lyme Meningitis Characteristics:
    - More indolent onset with gradual progression over days to weeks
    - Associated cranial nerve palsies, particularly facial nerve (Bell's palsy)
    - History of tick exposure or erythema migrans rash (though often absent)
    - CSF typically shows lymphocytic predominance with higher mononuclear percentages
    - May be associated with other manifestations of disseminated Lyme disease
    
    Viral Meningitis Characteristics:
    - More acute onset with rapid symptom development over hours to days
    - Less commonly associated with cranial nerve involvement
    - CSF findings may show mixed cellular response early in course
    - Self-limited illness with supportive care management
    - Seasonal patterns related to specific viral etiologies
    
    Differential Diagnosis Considerations:
    The distinction between Lyme and viral meningitis has significant clinical 
    implications for treatment decisions, disposition planning, antibiotic utilization, 
    and healthcare resource allocation. Inappropriate management can result in 
    either unnecessary interventions for viral meningitis or delayed treatment 
    for Lyme meningitis with potential neurologic complications.
    
    Rule of 7s Development and Validation History:
    
    Original Model Development (2006):
    Avery et al. developed a complex logistic regression model using multiple clinical, 
    laboratory, and epidemiologic variables to predict Lyme meningitis probability. 
    While statistically robust, this model required complex mathematical calculations 
    that limited practical clinical utility in busy emergency department settings.
    
    Simplified Rule Creation (2009):
    Recognizing the need for a more practical clinical tool, investigators developed 
    the simplified "Rule of 7s" using only three readily available clinical criteria. 
    This approach maintained excellent predictive performance while dramatically 
    improving ease of use and clinical applicability.
    
    Large-Scale Validation (2012):
    The definitive validation study by Cohn et al. included 423 children with CSF 
    pleocytosis from multiple medical centers, representing the largest cohort used 
    to validate a Lyme meningitis prediction rule. This study confirmed the rule's 
    excellent performance characteristics and clinical utility.
    
    Rule of 7s Criteria and Clinical Rationale:
    
    Criterion 1: Duration of Headache ≥7 Days (1 point):
    
    Pathophysiologic Basis:
    Lyme meningitis typically results from hematogenous dissemination of Borrelia 
    burgdorferi to the central nervous system, creating a chronic inflammatory 
    process that develops gradually over days to weeks. This contrasts with viral 
    meningitis, which often has a more acute onset with rapid symptom development.
    
    Clinical Assessment:
    - Careful history-taking to determine exact onset and progression of headache
    - Distinguish between gradual worsening versus acute severe onset
    - Consider prodromal symptoms and overall illness timeline
    - Account for patient and family recall bias in symptom duration reporting
    
    Criterion 2: CSF Mononuclear Cells ≥70% (1 point):
    
    Pathophysiologic Basis:
    Lyme meningitis characteristically produces lymphocytic pleocytosis as part 
    of the chronic inflammatory response to spirochetal infection. The predominance 
    of mononuclear cells reflects the immune system's response to intracellular 
    pathogens and chronic antigen stimulation.
    
    Laboratory Considerations:
    - Requires lumbar puncture with cerebrospinal fluid cell count and differential
    - CSF cell count should be corrected for traumatic tap if RBC >500 cells/mm³
    - Timing of lumbar puncture relative to symptom onset may affect cellular composition
    - Laboratory technique and processing time can influence differential count accuracy
    
    Criterion 3: Presence of Cranial Nerve Palsy (1 point):
    
    Pathophysiologic Basis:
    Cranial nerve involvement represents peripheral nervous system manifestation 
    of neuroborreliosis, reflecting the organism's tropism for neural tissue. 
    Facial nerve palsy (Bell's palsy) is the most common cranial nerve manifestation, 
    occurring in approximately 11% of patients with Lyme disease.
    
    Clinical Examination:
    - Comprehensive cranial nerve assessment including all 12 cranial nerves
    - Particular attention to facial nerve function (symmetry, voluntary movement, reflexes)
    - Assessment for other cranial nerves (III, IV, VI for extraocular movements; VIII for hearing)
    - Documentation of unilateral versus bilateral involvement
    - Correlation with other neurologic findings and overall clinical presentation
    
    Risk Stratification and Clinical Management Framework:
    
    Low Risk Classification (Score = 0 points):
    
    Clinical Significance:
    - All three criteria absent: <7 days headache AND <70% CSF mononuclear cells AND no cranial nerve palsy
    - Probability of Lyme meningitis <10% with 100% negative predictive value
    - Validates safe outpatient management approach while awaiting serology results
    - Avoids unnecessary healthcare resource utilization and patient anxiety
    
    Outpatient Management Protocol:
    - Discharge home with structured follow-up plan within 24-48 hours
    - Symptomatic treatment with appropriate analgesics and antiemetics
    - Lyme serology testing with two-tier approach (ELISA with Western blot confirmation)
    - Comprehensive patient and family education about expected course and warning signs
    - Clear return precautions for neurologic deterioration or symptom progression
    
    Not Low Risk Classification (Score = 1-3 points):
    
    Clinical Significance:
    - One or more high-risk criteria present indicating increased Lyme meningitis probability
    - Cannot exclude Lyme meningitis with sufficient confidence for outpatient management
    - Requires more intensive evaluation, monitoring, and consideration for empirical treatment
    - Higher likelihood of complicated course and need for specialized interventions
    
    Inpatient Management Considerations:
    - Hospital admission for observation, treatment initiation, and complication monitoring
    - Empirical antibiotic therapy for Lyme meningitis pending serology confirmation
    - Standard treatment regimen: Ceftriaxone 50-75 mg/kg/day (maximum 2g/day) IV for 14-21 days
    - Neurologic monitoring for clinical improvement and complication detection
    - Multidisciplinary consultation including infectious disease and neurology specialists
    
    Diagnostic Evaluation and Laboratory Assessment:
    
    Lyme Disease Serologic Testing:
    - Two-tier testing approach recommended by CDC: ELISA screening with Western blot confirmation
    - Both IgM and IgG antibodies assessed with interpretation based on disease duration
    - False positive results possible with other spirochetal infections and autoimmune conditions
    - Timing of testing relative to symptom onset affects sensitivity and interpretation
    
    Additional CSF Studies:
    - Protein and glucose levels for additional diagnostic information
    - Gram stain and bacterial culture to exclude bacterial meningitis
    - Lyme PCR if available (limited sensitivity but high specificity in CSF)
    - Consider additional studies based on clinical presentation and differential diagnosis
    
    Imaging and Specialized Testing:
    - Neuroimaging (CT or MRI) if focal neurologic signs or increased intracranial pressure suspected
    - Electrocardiogram if cardiac manifestations of Lyme disease suspected
    - Ophthalmologic examination if visual symptoms or papilledema present
    - Additional testing based on clinical presentation and expert consultation
    
    Performance Characteristics and Evidence Base:
    
    Validation Study Results (423 children):
    - Sensitivity: 96% (95% CI: 90-99%) for identifying children with Lyme meningitis
    - Specificity: 41% (95% CI: 36-47%) for correctly identifying low-risk patients
    - Negative Predictive Value: 100% (95% CI: 82-100%) for low-risk classification
    - Positive Predictive Value: 100% (95% CI: 66-100%) for high probability cases
    
    Clinical Utility and Impact:
    - Identifies 30% of children as low risk who can be safely managed as outpatients
    - Reduces unnecessary hospitalizations and healthcare costs
    - Provides objective criteria for clinical decision-making in challenging cases
    - Demonstrates superior performance compared to complex mathematical models
    - Enables evidence-based resource allocation and clinical protocol development
    
    Special Populations and Clinical Considerations:
    
    Age-Related Factors:
    - Validated specifically in pediatric patients ages 2-18 years
    - Limited data available for adult populations with different disease presentations
    - Consider developmental factors affecting clinical presentation and examination
    - Age-appropriate communication strategies for patient and family education
    
    Geographic and Seasonal Considerations:
    - Highest utility in Lyme disease-endemic areas with established tick populations
    - Seasonal variation based on tick activity patterns (peak May through October)
    - Consider travel history and exposure risks outside traditional endemic areas
    - Local epidemiologic patterns may influence rule performance and interpretation
    
    Immunocompromised Patients:
    - Limited validation data in immunocompromised pediatric populations
    - Consider altered immune response patterns affecting CSF cellular composition
    - May require modified management approach with lower threshold for treatment
    - Enhanced monitoring and specialist consultation recommended
    
    Implementation Considerations and Quality Assurance:
    
    Clinical Protocol Development:
    - Standardized approach to rule application and interpretation
    - Training programs for emergency physicians, pediatricians, and nursing staff
    - Integration with electronic health record systems and clinical decision support
    - Regular performance monitoring and quality improvement initiatives
    
    Documentation and Communication:
    - Complete recording of all three rule criteria with supporting clinical data
    - Clear rationale for management decisions based on rule results
    - Structured communication with families about risk assessment and follow-up plans
    - Coordination with primary care providers and specialists for continuity of care
    
    Limitations and Important Clinical Caveats:
    
    Rule Application Limitations:
    - Requires presence of CSF pleocytosis (≥10 WBC/mm³) for appropriate use
    - Limited to pediatric population with different adult disease manifestations
    - Performance may vary with different laboratory techniques and institutional practices
    - Seasonal and geographic limitations based on Lyme disease epidemiology
    
    Clinical Judgment Integration:
    - Rule should complement, not replace, comprehensive clinical assessment
    - Consider patient-specific factors including comorbidities and social circumstances
    - Maintain flexibility for clinical concerns beyond rule criteria
    - Account for family preferences and shared decision-making principles
    
    The Rule of 7s represents a valuable, evidence-based clinical decision tool 
    that enhances pediatric healthcare providers' ability to make informed 
    management decisions for children with suspected Lyme meningitis, supporting 
    optimal patient care while promoting efficient healthcare resource utilization 
    in Lyme disease-endemic areas.
    
    Args:
        request: Rule of 7s assessment parameters including headache duration, CSF findings, and neurologic examination
        
    Returns:
        RuleOf7sLymeMeningitisResponse: Risk assessment with comprehensive clinical guidance and management recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("rule_of_7s_lyme_meningitis", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Rule of 7s for Lyme meningitis prediction",
                    "details": {"parameters": parameters}
                }
            )
        
        return RuleOf7sLymeMeningitisResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Rule of 7s assessment",
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
                "message": "Internal error in Rule of 7s Lyme meningitis assessment",
                "details": {"error": str(e)}
            }
        )