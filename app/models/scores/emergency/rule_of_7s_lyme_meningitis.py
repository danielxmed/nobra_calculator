"""
Rule of 7s for Lyme Meningitis Models

Request and response models for Rule of 7s calculation.

References (Vancouver style):
1. Avery RA, Frank G, Glutting JJ, Eppes SC. Prediction of Lyme meningitis in 
   children from a Lyme disease-endemic region: a logistic-regression model using 
   history, physical, and laboratory findings. Pediatrics. 2006 Aug;118(2):e477-81. 
   doi: 10.1542/peds.2005-3043.
2. Garro AC, Rutman M, Simonsen K, Jaeger JL, Chapin K, Lockhart G. Prospective 
   validation of a clinical prediction model for Lyme meningitis in children. 
   Pediatrics. 2009 May;123(5):e829-34. doi: 10.1542/peds.2008-2048.
3. Cohn KA, Thompson AD, Shah SS, Hines EM, Lyons TW, Welsh EJ, Levas MN, 
   Lewander WJ, Bennett NJ, Nigrovic LE. Validation of a Clinical Prediction Rule 
   to Distinguish Lyme Meningitis From Aseptic Meningitis. Pediatrics. 
   2012 Jan;129(1):e46-53. doi: 10.1542/peds.2011-1215.

The Rule of 7s is a validated clinical prediction rule that distinguishes Lyme 
meningitis from aseptic meningitis in pediatric patients (ages 2-18) in Lyme 
disease-endemic areas. It identifies children at low risk for Lyme meningitis 
who can be safely managed as outpatients while awaiting serology results.
"""

from pydantic import BaseModel, Field
from typing import Literal


class RuleOf7sLymeMeningitisRequest(BaseModel):
    """
    Request model for Rule of 7s for Lyme Meningitis assessment
    
    The Rule of 7s is a validated clinical prediction rule designed to distinguish 
    Lyme meningitis from aseptic meningitis in pediatric patients (ages 2-18 years) 
    presenting with cerebrospinal fluid pleocytosis in Lyme disease-endemic areas.
    
    Clinical Background and Development:
    Lyme disease is the most common vector-borne illness in the United States, 
    with neurologic manifestations occurring in approximately 10-15% of untreated 
    cases. Lyme meningitis represents one of the most common neurologic presentations 
    in children, particularly during peak tick season (May through October) in 
    endemic regions including the northeastern and upper midwestern United States.
    
    The clinical challenge lies in distinguishing Lyme meningitis from more common 
    viral (aseptic) meningitis, as both conditions present with similar symptoms 
    and cerebrospinal fluid findings including lymphocytic pleocytosis. This 
    distinction is clinically important because Lyme meningitis requires specific 
    antibiotic treatment and may be associated with more serious complications 
    if left untreated.
    
    Rule Development and Validation History:
    
    Original Model Development (2006):
    Avery et al. developed the initial logistic regression model using clinical, 
    laboratory, and epidemiologic factors to predict Lyme meningitis in children 
    from a Lyme disease-endemic region. This complex mathematical model required 
    multiple variables and calculations, limiting its practical clinical utility.
    
    Simplified Rule Creation (2009-2012):
    Recognizing the need for a more practical clinical tool, investigators developed 
    and validated the simplified "Rule of 7s" that uses only three readily available 
    clinical criteria. This rule was prospectively validated in multiple pediatric 
    cohorts and demonstrated excellent performance characteristics.
    
    Multi-center Validation (2012):
    The largest validation study included 423 children with cerebrospinal fluid 
    pleocytosis, of whom 117 (28%) had Lyme meningitis and 306 (72%) had aseptic 
    meningitis. The rule demonstrated 96% sensitivity and 41% specificity for 
    identifying low-risk patients.
    
    Rule of 7s Criteria and Scoring System:
    
    The Rule of 7s assigns one point for each of the following three criteria:
    
    1. Duration of Headache ≥7 Days (1 point if present):
    - Rationale: Lyme meningitis typically has a more indolent, gradual onset 
      compared to viral meningitis which often presents more acutely
    - Clinical significance: Prolonged headache duration suggests chronic 
      inflammatory process consistent with Lyme disease pathophysiology
    - Assessment: Careful history-taking to determine exact onset and duration 
      of headache symptoms prior to presentation
    
    2. CSF Mononuclear Cells ≥70% (1 point if present):
    - Rationale: Lyme meningitis characteristically causes lymphocytic pleocytosis 
      with higher percentage of mononuclear cells compared to early viral meningitis
    - Clinical significance: Reflects the chronic inflammatory response and immune 
      activation characteristic of Borrelia burgdorferi CNS infection
    - Assessment: Requires lumbar puncture with cerebrospinal fluid cell count 
      and differential analysis
    - Technical considerations: CSF cell count should be corrected if RBC >500 cells/mm³
    
    3. Presence of Cranial Nerve Palsy (1 point if present):
    - Rationale: Cranial nerve involvement, particularly facial nerve palsy (Bell's palsy), 
      is a characteristic feature of Lyme disease neurologic manifestations
    - Clinical significance: Indicates peripheral nervous system involvement 
      consistent with neuroborreliosis pathophysiology
    - Assessment: Comprehensive neurologic examination focusing on cranial nerves, 
      with particular attention to facial nerve function
    - Common presentations: Unilateral or bilateral facial nerve palsy, less 
      commonly other cranial nerves (III, IV, VI, VIII)
    
    Risk Stratification and Clinical Interpretation:
    
    Low Risk (Score = 0 points):
    - All three criteria absent: <7 days headache AND <70% CSF mononuclear cells AND no cranial nerve palsy
    - Probability of Lyme meningitis: <10%
    - Clinical management: Safe for outpatient management while awaiting serology results
    - Performance: 100% negative predictive value in validation studies
    
    Not Low Risk (Score = 1-3 points):
    - One or more criteria present
    - Probability of Lyme meningitis: Cannot be excluded (>10%)
    - Clinical management: Consider inpatient management and empirical antibiotic treatment
    - Performance: Requires further evaluation and close monitoring
    
    Clinical Application Guidelines and Eligibility Criteria:
    
    Patient Population:
    - Age: 2-18 years (pediatric population only)
    - Geographic: Lyme disease-endemic areas (primarily northeastern and upper midwestern US)
    - Clinical presentation: Suspected meningitis with CSF pleocytosis (≥10 WBC/mm³)
    - Seasonal consideration: Highest utility during peak tick season (May-October)
    
    Prerequisites for Rule Application:
    - Documented cerebrospinal fluid pleocytosis (white blood cell count ≥10 cells/mm³)
    - Exclusion of bacterial meningitis through appropriate diagnostic evaluation
    - Clinical suspicion for central nervous system infection
    - Geographic residence or travel history in Lyme disease-endemic area
    
    Clinical Decision-Making Framework:
    
    Low Risk Management (Score = 0):
    - Outpatient management with close follow-up within 24-48 hours
    - Symptomatic treatment for headache, nausea, and other meningeal symptoms
    - Lyme serology testing (ELISA with Western blot confirmation if positive)
    - Clear return precautions for worsening symptoms or new neurologic findings
    - Avoid empirical parenteral antibiotics pending serology results
    - Patient/family education about expected course and warning signs
    
    Not Low Risk Management (Score ≥1):
    - Consider hospital admission for observation and treatment
    - Empirical antibiotic therapy for Lyme meningitis (typically ceftriaxone)
    - Comprehensive Lyme disease serologic testing
    - Neurologic monitoring for complications or deterioration
    - Consider additional diagnostic evaluation based on clinical presentation
    - Multidisciplinary consultation (infectious disease, neurology) as appropriate
    
    Diagnostic Testing Considerations:
    
    Cerebrospinal Fluid Analysis:
    - Cell count with differential (corrected for RBC if >500 cells/mm³)
    - Protein and glucose levels
    - Gram stain and bacterial culture to exclude bacterial meningitis
    - Consider Lyme PCR if available (limited sensitivity in CSF)
    
    Serologic Testing:
    - Two-tier testing approach: ELISA screening followed by Western blot confirmation
    - Both IgM and IgG antibodies should be assessed
    - Results interpretation requires understanding of Lyme disease epidemiology
    - False positives possible with other spirochetal infections
    
    Additional Considerations:
    - Neuroimaging if focal neurologic signs or increased intracranial pressure suspected
    - Electrocardiogram if cardiac manifestations of Lyme disease suspected
    - Ophthalmologic examination if visual symptoms present
    
    Performance Characteristics and Evidence Base:
    
    Validation Study Results:
    - Sensitivity: 96% (95% CI: 90-99%) for identifying children with Lyme meningitis
    - Specificity: 41% (95% CI: 36-47%) for correctly identifying low-risk patients
    - Negative Predictive Value: 100% (95% CI: 82-100%) for low-risk classification
    - Positive Predictive Value: 100% (95% CI: 66-100%) for high probability cases
    
    Clinical Utility:
    - Identifies low-risk children who can avoid hospitalization and empirical antibiotics
    - Reduces healthcare costs and unnecessary interventions
    - Provides objective criteria for clinical decision-making
    - Superior performance compared to complex mathematical prediction models
    
    Limitations and Important Considerations:
    
    Population Limitations:
    - Validated only in pediatric patients (ages 2-18 years)
    - Limited applicability outside Lyme disease-endemic areas
    - Seasonal variation in test performance based on tick activity
    - Requires presence of CSF pleocytosis for appropriate application
    
    Clinical Limitations:
    - Does not replace comprehensive clinical assessment and judgment
    - May be less reliable in immunocompromised patients
    - Performance may vary with different laboratory techniques and cutoff values
    - Requires accurate history-taking and neurologic examination
    
    Technical Considerations:
    - CSF cell count accuracy depends on timely processing and proper technique
    - Cranial nerve examination requires appropriate pediatric assessment skills
    - History of headache duration may be subjective or difficult to determine accurately
    
    Quality Assurance and Implementation:
    
    Standardization Requirements:
    - Consistent approach to CSF collection and analysis
    - Standardized neurologic examination techniques
    - Uniform application of rule criteria and interpretation
    - Regular training for healthcare providers on proper rule application
    
    Documentation Standards:
    - Clear recording of all three rule criteria
    - Detailed neurologic examination findings
    - Rationale for management decisions based on rule results
    - Follow-up plans and patient education provided
    
    Continuous Quality Improvement:
    - Monitor correlation between rule predictions and final diagnoses
    - Track patient outcomes for both low-risk and not-low-risk classifications
    - Evaluate adherence to rule-based management recommendations
    - Assess impact on length of stay, antibiotic use, and patient satisfaction
    
    The Rule of 7s represents a valuable, evidence-based clinical decision tool 
    that helps pediatric healthcare providers make informed management decisions 
    for children with suspected Lyme meningitis in endemic areas, potentially 
    reducing unnecessary hospitalizations while maintaining patient safety.
    
    References (Vancouver style):
    1. Avery RA, Frank G, Glutting JJ, Eppes SC. Prediction of Lyme meningitis in 
       children from a Lyme disease-endemic region: a logistic-regression model using 
       history, physical, and laboratory findings. Pediatrics. 2006 Aug;118(2):e477-81. 
       doi: 10.1542/peds.2005-3043.
    2. Garro AC, Rutman M, Simonsen K, Jaeger JL, Chapin K, Lockhart G. Prospective 
       validation of a clinical prediction model for Lyme meningitis in children. 
       Pediatrics. 2009 May;123(5):e829-34. doi: 10.1542/peds.2008-2048.
    3. Cohn KA, Thompson AD, Shah SS, Hines EM, Lyons TW, Welsh EJ, Levas MN, 
       Lewander WJ, Bennett NJ, Nigrovic LE. Validation of a Clinical Prediction Rule 
       to Distinguish Lyme Meningitis From Aseptic Meningitis. Pediatrics. 
       2012 Jan;129(1):e46-53. doi: 10.1542/peds.2011-1215.
    """
    
    headache_days: int = Field(
        ...,
        ge=1,
        le=30,
        description="Number of days of headache symptoms prior to presentation. "
                   "Lyme meningitis typically presents with more gradual onset and longer duration "
                   "compared to viral meningitis. Duration ≥7 days scores 1 point and suggests "
                   "chronic inflammatory process consistent with neuroborreliosis. "
                   "Range: 1-30 days (typical acute viral: 1-3 days, Lyme: often ≥7 days)",
        example=5
    )
    
    csf_mononuclear_percentage: float = Field(
        ...,
        ge=0,
        le=100,
        description="Percentage of mononuclear cells (lymphocytes and monocytes) in cerebrospinal fluid analysis. "
                   "Lyme meningitis characteristically causes lymphocytic pleocytosis with higher percentage "
                   "of mononuclear cells. Percentage ≥70% scores 1 point. CSF cell count should be corrected "
                   "if RBC >500 cells/mm³. Requires lumbar puncture with cell count and differential. "
                   "Range: 0-100% (viral meningitis often <70%, Lyme meningitis typically ≥70%)",
        example=65.0
    )
    
    cranial_nerve_palsy: Literal["present", "absent"] = Field(
        ...,
        description="Presence of cranial nerve palsy on neurologic examination, most commonly facial nerve (CN VII) palsy. "
                   "Cranial nerve involvement is characteristic of Lyme disease neurologic manifestations and "
                   "indicates peripheral nervous system involvement. Presence scores 1 point. "
                   "Requires comprehensive neurologic examination with attention to all cranial nerves. "
                   "Options: 'present' (any cranial nerve palsy detected) or 'absent' (normal cranial nerve function)",
        example="absent"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "headache_days": 5,
                "csf_mononuclear_percentage": 65.0,
                "cranial_nerve_palsy": "absent"
            }
        }


class RuleOf7sLymeMeningitisResponse(BaseModel):
    """
    Response model for Rule of 7s for Lyme Meningitis assessment
    
    The Rule of 7s provides evidence-based risk stratification for pediatric patients 
    with suspected Lyme meningitis, helping clinicians determine appropriate management 
    strategies while awaiting confirmatory serology results.
    
    Risk Categories and Clinical Management Framework:
    
    Low Risk for Lyme Meningitis (Score = 0 points):
    
    Clinical Significance:
    - Meets all three low-risk criteria: <7 days headache, <70% CSF mononuclear cells, no cranial nerve palsy
    - Probability of Lyme meningitis <10% (validated negative predictive value 100%)
    - Safe for outpatient management while awaiting Lyme serology results
    - Avoids unnecessary hospitalization and empirical parenteral antibiotics
    
    Outpatient Management Protocol:
    - Discharge home with close outpatient follow-up within 24-48 hours
    - Symptomatic treatment for headache, nausea, photophobia, and neck stiffness
    - Appropriate analgesics and antiemetics as needed for comfort
    - Lyme serology testing (two-tier ELISA and Western blot) with results follow-up
    - Patient and family education about expected clinical course and warning signs
    
    Follow-up and Monitoring:
    - Primary care or emergency department follow-up within 24-48 hours
    - Clear return precautions for worsening headache, new neurologic symptoms, or fever
    - Telephone contact for clinical deterioration or family concerns
    - Serology results review and management adjustment based on findings
    - Consider alternative diagnoses if symptoms persist beyond expected viral course
    
    Patient Education and Safety Instructions:
    - Expected resolution timeline for viral meningitis (typically 7-10 days)
    - Warning signs requiring immediate medical attention (altered mental status, seizures, focal deficits)
    - Importance of completing follow-up appointments and serology testing
    - Activity restrictions and gradual return to normal activities
    - Recognition that symptoms may fluctuate during recovery period
    
    Not Low Risk for Lyme Meningitis (Score = 1-3 points):
    
    Clinical Significance:
    - One or more high-risk criteria present (≥7 days headache, ≥70% CSF mononuclear cells, cranial nerve palsy)
    - Cannot exclude Lyme meningitis with sufficient confidence for outpatient management
    - Higher probability of Lyme meningitis requiring more intensive evaluation and treatment
    - Risk stratification indicates need for inpatient assessment and potential empirical therapy
    
    Inpatient Management Considerations:
    - Hospital admission for observation, monitoring, and treatment initiation
    - Empirical antibiotic therapy for Lyme meningitis while awaiting serology confirmation
    - Standard treatment: Ceftriaxone 50-75 mg/kg/day (max 2g/day) IV for 14-21 days
    - Alternative agents: Penicillin G or doxycycline (age ≥8 years) based on clinical factors
    - Neurologic monitoring for complications or clinical deterioration
    
    Diagnostic Evaluation:
    - Comprehensive Lyme disease serologic testing (IgM and IgG with Western blot confirmation)
    - Consider Lyme PCR of CSF if available (limited sensitivity but high specificity)
    - Additional CSF studies if clinically indicated (protein, glucose, additional cultures)
    - Neuroimaging if focal neurologic signs or increased intracranial pressure suspected
    - Electrocardiogram if cardiac involvement suspected (heart block, myocarditis)
    
    Multidisciplinary Care:
    - Infectious disease consultation for antibiotic selection and treatment duration
    - Neurology consultation if significant neurologic findings or complications
    - Ophthalmology evaluation if visual symptoms or papilledema present
    - Cardiology consultation if cardiac manifestations suspected
    
    Treatment Response Monitoring:
    - Clinical improvement typically seen within 48-72 hours of appropriate treatment
    - Neurologic examination monitoring for resolution of cranial nerve palsies
    - Headache and meningeal symptom improvement assessment
    - Laboratory monitoring for treatment-related adverse effects
    - Duration of treatment based on clinical response and expert guidelines
    
    Specific Score Interpretations:
    
    Score = 1 point:
    - Intermediate risk requiring careful clinical assessment
    - Consider patient-specific factors (age, comorbidities, family preference)
    - May be appropriate for close outpatient monitoring in select cases
    - Requires shared decision-making with family regarding management approach
    
    Score = 2-3 points:
    - High risk strongly suggesting Lyme meningitis
    - Inpatient management and empirical treatment strongly recommended
    - Multiple risk factors present indicating significant probability of Lyme disease
    - Aggressive evaluation and treatment to prevent complications
    
    Prognostic Considerations and Expected Outcomes:
    
    Lyme Meningitis Treatment Response:
    - Excellent prognosis with appropriate antibiotic treatment
    - Neurologic symptoms typically resolve within days to weeks
    - Cranial nerve palsies may take weeks to months for complete resolution
    - Long-term neurologic sequelae rare with prompt treatment
    - Post-treatment Lyme disease syndrome possible but uncommon in children
    
    Viral Meningitis Expected Course:
    - Self-limited illness with supportive care
    - Symptom resolution typically within 7-10 days
    - Gradual improvement in headache, fever, and meningeal signs
    - Full recovery expected without specific antiviral treatment
    - Rare complications in immunocompetent children
    
    Quality Assurance and Documentation Requirements:
    
    Essential Documentation Elements:
    - Complete neurologic examination findings with specific cranial nerve assessment
    - Exact headache duration and symptom progression timeline
    - CSF analysis results including cell count, differential, and correction calculations
    - Clinical reasoning for management decisions based on Rule of 7s results
    - Patient and family education provided and understanding confirmed
    
    Follow-up Documentation:
    - Clinical response to initial management approach
    - Serology results and impact on diagnosis and treatment
    - Any complications or unexpected clinical developments
    - Final diagnosis confirmation and treatment outcomes
    - Lessons learned for future similar clinical scenarios
    
    Performance Monitoring and Quality Improvement:
    
    Outcome Tracking:
    - Correlation between Rule of 7s predictions and final confirmed diagnoses
    - Patient outcomes for both low-risk and not-low-risk management strategies
    - Adherence to rule-based management recommendations
    - Length of stay, antibiotic utilization, and healthcare resource usage
    
    Continuous Quality Improvement:
    - Regular review of rule application accuracy and consistency
    - Staff education and training on proper rule implementation
    - Integration with electronic health record clinical decision support
    - Benchmarking against published validation study performance characteristics
    
    The Rule of 7s serves as a valuable evidence-based tool to guide clinical 
    decision-making for pediatric patients with suspected Lyme meningitis, 
    supporting optimal patient care while promoting efficient healthcare 
    resource utilization in Lyme disease-endemic areas.
    
    Reference: Cohn KA, et al. Pediatrics. 2012;129(1):e46-53.
    """
    
    result: int = Field(
        ...,
        ge=0,
        le=3,
        description="Rule of 7s score calculated from clinical criteria (0-3 points). "
                   "Score of 0 indicates low risk for Lyme meningitis (<10% probability), "
                   "while scores of 1-3 indicate not low risk requiring further evaluation.",
        example=0
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the Rule of 7s score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Comprehensive clinical interpretation of the Rule of 7s score with specific "
                   "recommendations for patient management, risk stratification, and clinical decision-making. "
                   "Includes detailed guidance for outpatient versus inpatient management strategies.",
        example="Low risk for Lyme meningitis (<10% probability). Patient meets all three 'Rule of 7s' "
                "criteria for low risk: <7 days of headache, <70% CSF mononuclear cells, and no cranial "
                "nerve palsy. Clinical parameters: 5 days of headache, 65.0% CSF mononuclear cells, "
                "cranial nerve palsy absent. These children can be safely managed as outpatients while "
                "awaiting Lyme serology results."
    )
    
    stage: str = Field(
        ...,
        description="Risk stratification category for Lyme meningitis likelihood",
        example="Low Risk for Lyme Meningitis"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the risk category and recommended management approach",
        example="Outpatient management appropriate"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 0,
                "unit": "points",
                "interpretation": "Low risk for Lyme meningitis (<10% probability). Patient meets all three 'Rule of 7s' criteria for low risk: <7 days of headache, <70% CSF mononuclear cells, and no cranial nerve palsy. Clinical parameters: 5 days of headache, 65.0% CSF mononuclear cells, cranial nerve palsy absent. These children can be safely managed as outpatients while awaiting Lyme serology results. Consider discharge home with close outpatient follow-up, symptomatic treatment, and clear return precautions.",
                "stage": "Low Risk for Lyme Meningitis",
                "stage_description": "Outpatient management appropriate"
            }
        }