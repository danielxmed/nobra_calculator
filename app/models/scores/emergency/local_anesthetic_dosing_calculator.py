"""
Local Anesthetic Dosing Calculator Models

Request and response models for Local Anesthetic Dosing Calculator.

References (Vancouver style):
1. Neal JM, Woodward CM, Harrison TK. The American Society of Regional Anesthesia 
   and Pain Medicine Checklist for Managing Local Anesthetic Systemic Toxicity: 
   2017 Version. Reg Anesth Pain Med. 2018 Feb;43(2):150-153. 
   doi: 10.1097/AAP.0000000000000726.
2. El-Boghdadly K, Pawa A, Chin KJ. Local anesthetic systemic toxicity: current 
   perspectives. Local Reg Anesth. 2018 Aug 8;11:35-44. doi: 10.2147/LRA.S154512.
3. Berde CB, Strichartz GR. Local anesthetics. In: Miller RD, ed. Miller's Anesthesia. 
   6th ed. Philadelphia, PA: Elsevier Churchill Livingstone; 2005:573-603.

The Local Anesthetic Dosing Calculator is an essential clinical tool designed to prevent 
Local Anesthetic Systemic Toxicity (LAST) by calculating maximum safe doses of commonly 
used local anesthetic agents. This evidence-based calculator helps clinicians determine 
appropriate dosing limits for regional anesthesia, nerve blocks, and local infiltration 
procedures, significantly reducing the risk of potentially life-threatening systemic 
toxicity.

Clinical Background:
Local Anesthetic Systemic Toxicity (LAST) is a rare but potentially fatal complication 
of regional anesthesia and local anesthetic procedures. LAST occurs when local anesthetic 
agents reach toxic concentrations in the systemic circulation, typically through 
inadvertent intravascular injection, absorption from highly vascularized tissues, or 
administration of excessive doses. The incidence of LAST ranges from 0.03% to 0.3% 
depending on the procedure and technique used.

LAST manifests through a biphasic pattern affecting both the central nervous system (CNS) 
and cardiovascular system. Initial CNS symptoms include perioral numbness, metallic taste, 
tinnitus, and agitation, which can rapidly progress to seizures and loss of consciousness. 
Cardiovascular toxicity typically follows CNS symptoms and may include arrhythmias, 
conduction blocks, myocardial depression, and ultimately cardiovascular collapse.

The severity and onset of LAST depend on multiple factors including the specific local 
anesthetic agent used, total dose administered, injection site vascularity, patient 
factors (age, weight, cardiac status, hepatic function), and injection technique. 
Understanding these factors and calculating appropriate maximum doses is crucial for 
safe clinical practice.

Local Anesthetic Pharmacology and Toxicity:

Mechanism of Action:
Local anesthetics work by blocking voltage-gated sodium channels in nerve cell membranes, 
preventing nerve conduction and producing reversible loss of sensation. The same mechanism 
that provides anesthesia can also affect cardiac conduction and CNS function when systemic 
concentrations become elevated.

Agent-Specific Considerations:

Bupivacaine:
Bupivacaine is a long-acting amide local anesthetic with high potency and significant 
cardiotoxicity potential. It has a maximum recommended dose of 2 mg/kg for subcutaneous 
infiltration. Bupivacaine binds strongly to cardiac sodium channels and can cause 
severe, refractory cardiac arrhythmias that are difficult to treat. The drug's long 
duration of action (4-8 hours) makes it excellent for prolonged procedures but increases 
the risk of prolonged toxicity if LAST occurs.

Clinical Properties:
- Onset: Slow (15-30 minutes)
- Duration: Long (4-8 hours)
- Potency: High (4x more potent than lidocaine)
- Cardiotoxicity: Highest among commonly used agents
- Protein binding: 95%
- Metabolism: Hepatic via CYP3A4

Lidocaine:
Lidocaine is the most commonly used local anesthetic with a well-established safety 
profile. It has a maximum recommended dose of 4.5 mg/kg for subcutaneous infiltration. 
Lidocaine has relatively low cardiotoxicity compared to other amide local anesthetics 
and is often used as the first-line agent for minor procedures.

Clinical Properties:
- Onset: Fast (2-5 minutes)
- Duration: Intermediate (1-3 hours)
- Potency: Intermediate (reference standard)
- Cardiotoxicity: Low
- Protein binding: 64%
- Metabolism: Hepatic via CYP1A2 and CYP3A4

Mepivacaine:
Mepivacaine is an intermediate-acting amide local anesthetic with properties similar 
to lidocaine but slightly longer duration. It has a maximum recommended dose of 4.4 mg/kg 
for subcutaneous infiltration. Mepivacaine is particularly useful when epinephrine 
is contraindicated, as it provides good vasoconstriction without additional agents.

Clinical Properties:
- Onset: Intermediate (5-15 minutes)
- Duration: Intermediate (2-4 hours)
- Potency: Similar to lidocaine
- Cardiotoxicity: Low
- Protein binding: 77%
- Metabolism: Hepatic via CYP1A2

Ropivacaine:
Ropivacaine is a long-acting amide local anesthetic developed as a safer alternative 
to bupivacaine. It has a maximum recommended dose of 3 mg/kg for subcutaneous infiltration. 
Ropivacaine has lower cardiotoxicity than bupivacaine while maintaining similar duration 
and efficacy, making it preferred for procedures requiring long-duration anesthesia.

Clinical Properties:
- Onset: Slow (15-30 minutes)
- Duration: Long (4-6 hours)
- Potency: High (slightly less than bupivacaine)
- Cardiotoxicity: Lower than bupivacaine
- Protein binding: 94%
- Metabolism: Hepatic via CYP1A2

Patient-Specific Factors Affecting Dosing:

Age Considerations:
Elderly patients have increased sensitivity to local anesthetics due to decreased cardiac 
output, reduced hepatic metabolism, and altered protein binding. Neonates and infants 
have immature hepatic enzyme systems and altered pharmacokinetics, requiring dose 
adjustments. The calculator uses standard adult dosing recommendations but clinical 
judgment should guide dose reduction in vulnerable populations.

Weight Considerations:
Dosing should be based on ideal body weight rather than actual body weight, particularly 
in obese patients. For most adults, ideal body weight ranges from 60-75 kg depending 
on height and sex. Using actual body weight in obese patients can lead to significant 
overdosing and increased LAST risk.

Cardiac Disease:
Patients with cardiac disease, particularly those with conduction abnormalities or 
heart failure, are at increased risk of cardiovascular toxicity. Consider dose reduction 
and avoid high-cardiotoxicity agents like bupivacaine when possible.

Hepatic Impairment:
Local anesthetics are metabolized primarily by the liver. Patients with hepatic 
impairment have reduced clearance and are at increased risk of toxicity. Consider 
dose reduction and extended monitoring in patients with significant liver disease.

Renal Disease:
While local anesthetics are primarily hepatically metabolized, some metabolites are 
renally excreted. Severe renal impairment may affect clearance of active metabolites, 
particularly for lidocaine.

Clinical Application and Safety Measures:

Pre-procedure Assessment:
- Complete medical history focusing on cardiac, hepatic, and neurologic conditions
- Current medications that may interact with local anesthetics
- Previous adverse reactions to local anesthetics
- Baseline vital signs and neurologic assessment

Injection Technique:
- Always aspirate before injection to detect intravascular placement
- Inject slowly with frequent aspiration (every 3-5 mL)
- Use smallest effective dose for desired clinical effect
- Consider fractionated dosing for large volume injections
- Avoid injection into highly vascularized areas when possible

Monitoring Requirements:
- Continuous monitoring of vital signs during and after injection
- Observe for early signs of LAST (perioral numbness, metallic taste, tinnitus)
- Monitor for 30 minutes post-injection as absorption continues
- Have emergency equipment and medications readily available

Emergency Preparedness:
- Ensure availability of lipid emulsion therapy (20% Intralipid)
- Have advanced cardiac life support capabilities immediately available
- Train staff in LAST recognition and management protocols
- Maintain emergency drug supplies (epinephrine, atropine, benzodiazepines)

Treatment of LAST:

Immediate Management:
1. Stop local anesthetic injection immediately
2. Call for help and prepare for advanced resuscitation
3. Assess and manage airway, breathing, and circulation
4. Administer 100% oxygen
5. Control seizures with benzodiazepines (avoid phenytoin, beta-blockers, calcium channel blockers)

Lipid Emulsion Therapy:
- Initial bolus: 1.5 mL/kg of 20% lipid emulsion
- Continuous infusion: 0.25 mL/kg/min
- Repeat bolus after 5 minutes if circulation not restored
- Increase infusion to 0.5 mL/kg/min if circulation not restored
- Continue until hemodynamic stability achieved
- Maximum dose: approximately 10 mL/kg over first 30 minutes

Advanced Cardiac Life Support:
- Standard ACLS protocols with modifications for LAST
- Avoid or reduce doses of epinephrine and vasopressin
- Consider cardiopulmonary bypass or extracorporeal membrane oxygenation for refractory cases
- Continue resuscitation longer than usual as recovery may be delayed

Quality Assurance and Risk Mitigation:

Institutional Protocols:
- Develop standardized protocols for local anesthetic administration
- Implement maximum dose checklists and verification procedures
- Regular staff training on LAST recognition and management
- Maintain emergency response protocols and equipment checks

Documentation:
- Record drug type, concentration, total dose, and injection sites
- Document patient monitoring and any adverse events
- Maintain records for quality improvement and medicolegal purposes

Continuous Education:
- Regular training updates on local anesthetic safety
- Simulation training for LAST management
- Review of current literature and best practices
- Interdisciplinary education for all staff involved in procedures

The Local Anesthetic Dosing Calculator serves as a critical safety tool in the 
prevention of LAST. By providing evidence-based maximum dose calculations, this 
tool helps clinicians make informed decisions about local anesthetic administration, 
ultimately improving patient safety and procedural outcomes. However, the calculator 
should be used in conjunction with sound clinical judgment, appropriate monitoring, 
and comprehensive emergency preparedness to ensure optimal patient care.
"""

from pydantic import BaseModel, Field
from typing import Literal, Dict, Any


class LocalAnestheticDosingCalculatorRequest(BaseModel):
    """
    Request model for Local Anesthetic Dosing Calculator
    
    The Local Anesthetic Dosing Calculator is an essential clinical safety tool designed 
    to prevent Local Anesthetic Systemic Toxicity (LAST) by calculating maximum safe doses 
    of commonly used local anesthetic agents. This evidence-based calculator helps clinicians 
    determine appropriate dosing limits for regional anesthesia, nerve blocks, and local 
    infiltration procedures, significantly reducing the risk of potentially life-threatening 
    systemic toxicity.
    
    Clinical Assessment Parameters:
    
    Drug Selection:
    The calculator supports four commonly used amide local anesthetics, each with distinct 
    pharmacological properties, onset times, duration of action, and toxicity profiles. 
    Selection should be based on procedure requirements, patient factors, and safety 
    considerations.
    
    Bupivacaine (Maximum: 2 mg/kg):
    Long-acting, high-potency local anesthetic with excellent sensory blockade. Provides 
    4-8 hours of anesthesia but carries the highest cardiotoxicity risk. Binds strongly 
    to cardiac sodium channels and can cause severe, refractory arrhythmias. Use with 
    extreme caution in patients with cardiac disease. Slow onset (15-30 minutes) makes 
    it less suitable for procedures requiring immediate anesthesia.
    
    Lidocaine (Maximum: 4.5 mg/kg):
    Most commonly used local anesthetic with well-established safety profile. Fast onset 
    (2-5 minutes) and intermediate duration (1-3 hours) make it ideal for minor procedures. 
    Relatively low cardiotoxicity and extensive clinical experience support its use as 
    first-line agent. Excellent for procedures requiring rapid onset and moderate duration.
    
    Mepivacaine (Maximum: 4.4 mg/kg):
    Intermediate-acting agent with properties similar to lidocaine but slightly longer 
    duration (2-4 hours). Provides good intrinsic vasoconstriction without epinephrine, 
    making it useful when vasoconstrictors are contraindicated. Low cardiotoxicity profile 
    and reliable onset (5-15 minutes) make it suitable for various procedures.
    
    Ropivacaine (Maximum: 3 mg/kg):
    Long-acting agent developed as safer alternative to bupivacaine. Provides 4-6 hours 
    of anesthesia with significantly lower cardiotoxicity than bupivacaine. Preferred 
    for procedures requiring prolonged anesthesia when safety is paramount. Slower onset 
    (15-30 minutes) requires advance planning for procedure timing.
    
    Patient Weight Assessment:
    Accurate weight determination is crucial for safe dosing calculations. The calculator 
    uses weight-based dosing to account for pharmacokinetic differences and distribution 
    volumes across patient populations.
    
    Weight-Based Dosing Principles:
    - Use ideal body weight for most adults (60-75 kg based on height and sex)
    - Actual body weight may be used in non-obese patients
    - Avoid using actual weight in significantly obese patients to prevent overdosing
    - Consider dose reduction in elderly patients due to altered pharmacokinetics
    - Pediatric patients may require different dosing considerations not covered by this calculator
    
    Special Populations:
    - Elderly: Reduced cardiac output and hepatic metabolism increase sensitivity
    - Cardiac disease: Increased risk of cardiovascular toxicity, consider dose reduction
    - Hepatic impairment: Reduced clearance requires dose adjustment
    - Pregnancy: Altered protein binding and pharmacokinetics require careful consideration
    
    Concentration Assessment:
    Local anesthetic concentration directly affects the volume required to achieve desired 
    dose and influences onset time, duration, and safety profile. Understanding concentration 
    conversions is essential for safe practice.
    
    Concentration Conversions:
    - Percentage to mg/mL: Multiply percentage by 10 (1% = 10 mg/mL)
    - Common concentrations: 0.25% = 2.5 mg/mL, 0.5% = 5 mg/mL, 1% = 10 mg/mL, 2% = 20 mg/mL
    - Higher concentrations provide faster onset but require smaller volumes for same dose
    - Lower concentrations allow larger volumes for extensive infiltration
    
    Clinical Considerations:
    - Use lowest effective concentration for desired clinical effect
    - Higher concentrations may cause more tissue irritation
    - Consider dilution for large volume infiltrations
    - Ensure accurate labeling and double-check concentrations before use
    
    Safety Considerations and Risk Factors:
    
    High-Risk Scenarios:
    - Highly vascularized injection sites (intercostal, epidural, caudal)
    - Large volume injections (>20 mL)
    - Multiple injection sites
    - Rapid injection without aspiration
    - Use of high-cardiotoxicity agents (bupivacaine)
    
    Risk Mitigation Strategies:
    - Always aspirate before injection to detect intravascular placement
    - Inject slowly with frequent aspiration (every 3-5 mL)
    - Use fractionated dosing for large volumes
    - Monitor continuously during and 30 minutes after injection
    - Have lipid emulsion and emergency equipment readily available
    
    Clinical Application Guidelines:
    - Calculate maximum dose before beginning procedure
    - Use smallest effective dose for desired clinical effect
    - Consider patient-specific factors that may require dose reduction
    - Maintain situational awareness for early signs of systemic toxicity
    - Ensure emergency preparedness and staff training in LAST management
    
    Contraindications and Precautions:
    - Known allergy to amide local anesthetics
    - Severe cardiac conduction abnormalities (relative contraindication)
    - Severe hepatic impairment (dose reduction required)
    - Injection site infection or inflammation
    - Coagulopathy (relative contraindication for deep blocks)
    
    References (Vancouver style):
    1. Neal JM, Woodward CM, Harrison TK. The American Society of Regional Anesthesia 
    and Pain Medicine Checklist for Managing Local Anesthetic Systemic Toxicity: 
    2017 Version. Reg Anesth Pain Med. 2018 Feb;43(2):150-153.
    2. El-Boghdadly K, Pawa A, Chin KJ. Local anesthetic systemic toxicity: current 
    perspectives. Local Reg Anesth. 2018 Aug 8;11:35-44.
    """
    
    drug_type: Literal["bupivacaine", "lidocaine", "mepivacaine", "ropivacaine"] = Field(
        ...,
        description="Type of local anesthetic drug. Bupivacaine (2 mg/kg max): long-acting, high cardiotoxicity, "
                   "4-8 hour duration, slow onset. Lidocaine (4.5 mg/kg max): most common, low cardiotoxicity, "
                   "1-3 hour duration, fast onset. Mepivacaine (4.4 mg/kg max): intermediate duration, low "
                   "cardiotoxicity, good without epinephrine. Ropivacaine (3 mg/kg max): long-acting, lower "
                   "cardiotoxicity than bupivacaine, 4-6 hour duration. Select based on procedure requirements, "
                   "patient factors, and safety considerations.",
        example="lidocaine"
    )
    
    patient_weight: float = Field(
        ...,
        description="Patient weight in kg. Use ideal body weight for most adults (60-75 kg depending on height "
                   "and sex) rather than actual weight, especially in obese patients, to prevent overdosing. "
                   "Consider dose reduction in elderly patients due to altered pharmacokinetics and increased "
                   "sensitivity. Patients with cardiac disease, hepatic impairment, or other comorbidities may "
                   "require weight-adjusted dose reductions. Accurate weight assessment is crucial for safe "
                   "maximum dose calculations.",
        ge=1.0,
        le=200.0,
        example=70.0
    )
    
    concentration_percentage: float = Field(
        ...,
        description="Concentration of local anesthetic as percentage. Common concentrations: 0.25% = 2.5 mg/mL, "
                   "0.5% = 5 mg/mL, 1% = 10 mg/mL, 2% = 20 mg/mL. Concentration conversion: multiply percentage "
                   "by 10 to get mg/mL (e.g., 1% = 10 mg/mL). Higher concentrations provide faster onset but "
                   "require smaller volumes for same total dose. Lower concentrations allow larger volumes for "
                   "extensive infiltration. Use lowest effective concentration for desired clinical effect. "
                   "Ensure accurate labeling and double-check concentrations before administration.",
        ge=0.1,
        le=5.0,
        example=1.0
    )
    
    class Config:
        schema_extra = {
            "example": {
                "drug_type": "lidocaine",
                "patient_weight": 70.0,
                "concentration_percentage": 1.0
            }
        }


class LocalAnestheticDosingCalculatorResponse(BaseModel):
    """
    Response model for Local Anesthetic Dosing Calculator
    
    Provides calculated maximum safe doses in both mg and mL with comprehensive clinical 
    interpretation and safety guidance to prevent Local Anesthetic Systemic Toxicity (LAST). 
    The response includes drug-specific properties, monitoring requirements, emergency 
    preparedness guidelines, and evidence-based management recommendations for safe local 
    anesthetic administration.
    
    Calculated Results and Clinical Significance:
    
    Maximum Dose (mg):
    The total amount of local anesthetic that can be safely administered based on the 
    patient's weight and the specific agent's toxicity profile. This represents the 
    upper safety limit to prevent systemic toxicity and should not be exceeded under 
    normal circumstances. The dose is calculated using evidence-based maximum mg/kg 
    recommendations derived from clinical studies and expert consensus.
    
    Maximum Volume (mL):
    The corresponding volume of local anesthetic solution that contains the maximum 
    safe dose. This practical measurement helps clinicians prepare and administer 
    the correct amount during procedures. Volume calculations account for the specific 
    concentration being used, providing direct guidance for clinical application.
    
    Concentration (mg/mL):
    The calculated concentration of the local anesthetic solution in mg/mL, derived 
    from the percentage concentration. This conversion facilitates accurate dosing 
    calculations and helps prevent medication errors related to concentration confusion.
    
    Drug-Specific Clinical Properties:
    
    Each local anesthetic agent has unique pharmacological characteristics that influence 
    clinical decision-making:
    
    Onset Time: Determines how quickly anesthesia develops after injection
    - Fast onset (2-5 min): Suitable for procedures requiring immediate anesthesia
    - Intermediate onset (5-15 min): Balanced option for most procedures
    - Slow onset (15-30 min): Requires advance planning but provides reliable blockade
    
    Duration of Action: Influences procedure planning and post-operative care
    - Short duration (1-3 hours): Minor procedures, outpatient settings
    - Intermediate duration (2-4 hours): Most surgical procedures
    - Long duration (4-8 hours): Extensive procedures, prolonged analgesia needed
    
    Cardiotoxicity Profile: Critical safety consideration for agent selection
    - Low risk: Lidocaine, mepivacaine - safer in cardiac patients
    - High risk: Bupivacaine - requires extreme caution and monitoring
    - Intermediate risk: Ropivacaine - safer alternative to bupivacaine
    
    Safety Monitoring and Risk Management:
    
    Pre-procedure Assessment:
    - Complete medical history focusing on cardiac, hepatic, and neurologic conditions
    - Review current medications for potential interactions
    - Assess for previous adverse reactions to local anesthetics
    - Establish baseline vital signs and neurologic function
    
    Injection Technique Safety:
    - Always aspirate before injection to detect intravascular placement
    - Inject slowly with frequent aspiration every 3-5 mL
    - Use smallest effective dose for desired clinical effect
    - Consider fractionated dosing for large volume injections (>10 mL)
    - Avoid injection into highly vascularized areas when possible
    
    Continuous Monitoring Requirements:
    - Monitor vital signs continuously during injection and for 30 minutes after
    - Observe for early signs of LAST: perioral numbness, metallic taste, tinnitus
    - Watch for progressive symptoms: agitation, confusion, seizures
    - Monitor cardiovascular status: heart rate, blood pressure, ECG changes
    - Maintain verbal contact with patient throughout procedure
    
    Emergency Recognition and Management:
    
    Early Warning Signs of LAST:
    - CNS symptoms: perioral numbness, metallic taste, tinnitus, lightheadedness
    - Neurologic symptoms: agitation, confusion, slurred speech, muscle twitching
    - Cardiovascular symptoms: palpitations, chest discomfort, hypotension
    
    Progressive LAST Symptoms:
    - Severe CNS toxicity: seizures, loss of consciousness, respiratory depression
    - Cardiovascular collapse: severe hypotension, arrhythmias, cardiac arrest
    - These symptoms may occur rapidly and require immediate intervention
    
    Immediate LAST Management Protocol:
    1. Stop local anesthetic injection immediately
    2. Call for emergency assistance and advanced life support
    3. Maintain airway, breathing, and circulation (ABC approach)
    4. Administer 100% oxygen and ensure adequate ventilation
    5. Control seizures with benzodiazepines (avoid phenytoin, beta-blockers)
    6. Initiate lipid emulsion therapy as per established protocols
    7. Begin advanced cardiac life support if indicated
    8. Continue resuscitation longer than usual as recovery may be delayed
    
    Lipid Emulsion Therapy:
    - Initial bolus: 1.5 mL/kg of 20% lipid emulsion over 1 minute
    - Continuous infusion: 0.25 mL/kg/min
    - Repeat bolus after 5 minutes if circulation not restored
    - Increase infusion to 0.5 mL/kg/min if circulation not restored
    - Continue until hemodynamic stability achieved
    - Maximum recommended dose: approximately 10 mL/kg over first 30 minutes
    
    Quality Assurance and Risk Mitigation:
    
    Institutional Safety Measures:
    - Develop standardized protocols for local anesthetic administration
    - Implement maximum dose verification and double-check procedures
    - Maintain emergency response equipment and medications readily available
    - Ensure staff competency in LAST recognition and management
    - Conduct regular emergency drills and simulation training
    
    Documentation Requirements:
    - Record drug type, concentration, total dose administered, and injection sites
    - Document patient monitoring findings and any adverse events
    - Maintain accurate records for quality improvement and medicolegal purposes
    - Note any deviations from standard protocols and rationale
    
    Patient Education and Informed Consent:
    - Explain procedure risks and benefits to patient
    - Discuss signs and symptoms to report during and after injection
    - Provide post-procedure instructions and emergency contact information
    - Document informed consent process and patient understanding
    
    Continuous Quality Improvement:
    - Regular review of local anesthetic protocols and outcomes
    - Analysis of adverse events and near-miss incidents
    - Integration of new evidence and best practices
    - Ongoing staff education and competency verification
    - Collaboration with pharmacy and emergency departments for LAST preparedness
    
    The Local Anesthetic Dosing Calculator serves as a fundamental safety tool in 
    preventing LAST and ensuring optimal patient outcomes. By providing evidence-based 
    dose calculations combined with comprehensive clinical guidance, this tool supports 
    safe practice while enabling effective regional anesthesia and pain management 
    procedures. However, clinical judgment, appropriate monitoring, and emergency 
    preparedness remain essential components of safe local anesthetic administration.
    
    Reference: Neal JM, et al. Reg Anesth Pain Med. 2018;43(2):150-153.
    """
    
    result: Dict[str, Any] = Field(
        ...,
        description="Maximum safe doses including total dose in mg, maximum volume in mL, and concentration in mg/mL",
        example={"max_dose_mg": 315.0, "max_volume_ml": 31.5, "concentration_mg_ml": 10.0}
    )
    
    unit: str = Field(
        ...,
        description="Units of measurement for the calculated doses",
        example="mg and mL"
    )
    
    interpretation: str = Field(
        ...,
        description="Comprehensive clinical interpretation including drug properties, maximum safe doses, "
                   "safety considerations, monitoring requirements, and emergency management guidance",
        example="Local Anesthetic Dosing Calculation for Lidocaine:\n\nPatient Parameters:\n• Weight: 70.0 kg\n• Drug: Lidocaine 1.0% solution\n• Concentration: 10.0 mg/mL\n\nMaximum Safe Doses:\n• Maximum total dose: 315.0 mg\n• Maximum volume: 31.5 mL\n• Dose limit: 4.5 mg/kg\n\nDrug Properties:\n• Onset: Fast (2-5 min)\n• Duration: Intermediate (1-3 hours)\n• Potency: Intermediate\n• Cardiotoxicity risk: Low"
    )
    
    stage: str = Field(
        ...,
        description="Safety classification category",
        example="Safe Dosing Range"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the safety classification",
        example="Maximum safe dose calculated to prevent LAST"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": {
                    "max_dose_mg": 315.0,
                    "max_volume_ml": 31.5,
                    "concentration_mg_ml": 10.0
                },
                "unit": "mg and mL",
                "interpretation": "Local Anesthetic Dosing Calculation for Lidocaine:\n\nPatient Parameters:\n• Weight: 70.0 kg\n• Drug: Lidocaine 1.0% solution\n• Concentration: 10.0 mg/mL\n\nMaximum Safe Doses:\n• Maximum total dose: 315.0 mg\n• Maximum volume: 31.5 mL\n• Dose limit: 4.5 mg/kg\n\nDrug Properties:\n• Onset: Fast (2-5 min)\n• Duration: Intermediate (1-3 hours)\n• Potency: Intermediate\n• Cardiotoxicity risk: Low\n\nSafety Considerations:\n• These doses are for subcutaneous infiltration and nerve blocks\n• Consider lower doses in elderly patients, cardiac disease, or hepatic impairment\n• Monitor for signs of Local Anesthetic Systemic Toxicity (LAST)\n• CNS symptoms: altered mental status, seizures, metallic taste\n• Cardiovascular symptoms: arrhythmias, hypotension, cardiac arrest\n• Have lipid emulsion (Intralipid) readily available for LAST treatment",
                "stage": "Safe Dosing Range",
                "stage_description": "Maximum safe dose calculated to prevent LAST"
            }
        }