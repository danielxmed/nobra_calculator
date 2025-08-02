"""
Light's Criteria for Exudative Effusions Models

Request and response models for Light's Criteria calculation.

References (Vancouver style):
1. Light RW, Macgregor MI, Luchsinger PC, Ball WC Jr. Pleural effusions: the 
   diagnostic separation of transudates and exudates. Ann Intern Med. 1972 
   Oct;77(4):507-13. doi: 10.7326/0003-4819-77-4-507.
2. Heffner JE, Brown LK, Barbieri C, DeLeo JM. Pleural fluid chemical analysis 
   in parapneumonic effusions. A meta-analysis. Am J Respir Crit Care Med. 1995 
   Jun;151(6):1700-8. doi: 10.1164/ajrccm.151.6.7767510.
3. Porcel JM, Light RW. Diagnostic approach to pleural effusion in adults. 
   Am Fam Physician. 2006 Apr 1;73(7):1211-20.

Light's Criteria for Exudative Effusions is the gold standard diagnostic tool for 
differentiating between exudative and transudative pleural effusions. Developed by 
Richard Light in 1972, these criteria have been the cornerstone of pleural effusion 
evaluation for over 50 years and remain the most widely used classification system 
in clinical practice worldwide.

Clinical Background:
Pleural effusion affects approximately 1.5 million people annually in the United States 
and represents a common clinical problem across multiple medical specialties. The 
fundamental distinction between exudative and transudative effusions is crucial for 
diagnostic workup and therapeutic management, as it determines the underlying pathophysiology 
and guides appropriate treatment strategies.

Pathophysiological Basis:

Transudative Effusions:
Result from altered hydrostatic or oncotic pressures across normal pleural membranes. 
The pleural surfaces remain intact, and fluid accumulation occurs due to systemic factors 
affecting fluid balance. Common causes include:
- Congestive heart failure (most common cause, ~90% of transudates)
- Cirrhosis with ascites and hypoalbuminemia
- Nephrotic syndrome with severe hypoproteinemia
- Peritoneal dialysis with diaphragmatic defects
- Superior vena cava obstruction
- Hypothyroidism with severe myxedema
- Urinothorax from urinary tract obstruction

Exudative Effusions:
Result from increased capillary permeability, impaired lymphatic drainage, or direct 
pleural surface involvement by inflammatory or neoplastic processes. The pleural membranes 
are damaged or inflamed, leading to protein-rich fluid accumulation. Common causes include:
- Bacterial pneumonia and parapneumonic effusions (most common exudative cause)
- Malignancy (lung cancer, breast cancer, lymphoma, mesothelioma)
- Pulmonary embolism with pulmonary infarction
- Viral, fungal, or tuberculous pleuritis
- Autoimmune conditions (rheumatoid arthritis, systemic lupus erythematosus)
- Post-cardiac surgery syndrome
- Esophageal rupture or perforation
- Pancreatitis with pancreatic-pleural fistula

The Three Light's Criteria:

Criterion 1: Pleural Fluid Protein to Serum Protein Ratio > 0.5
This ratio reflects the degree of protein leak across the pleural membrane. In transudative 
effusions, intact pleural membranes maintain the normal protein concentration gradient, 
keeping pleural fluid protein levels low relative to serum. In exudative effusions, 
inflammatory damage increases membrane permeability, allowing protein-rich fluid to 
accumulate. Normal serum protein ranges from 6.0-8.3 g/dL, while transudative pleural 
fluid typically contains <3.0 g/dL protein.

Criterion 2: Pleural Fluid LDH to Serum LDH Ratio > 0.6
Lactate dehydrogenase (LDH) is an intracellular enzyme released during cellular damage 
and inflammation. Elevated pleural fluid LDH indicates active cellular metabolism, 
inflammation, or tissue destruction within the pleural space. In transudative effusions, 
LDH levels remain low due to minimal cellular activity. In exudative effusions, 
inflammatory cells, malignant cells, or tissue necrosis significantly elevate LDH levels.

Criterion 3: Pleural Fluid LDH > 2/3 × Upper Limit of Normal Serum LDH
This absolute threshold (typically >148 U/L when upper normal serum LDH is 222 U/L) 
identifies effusions with significant inflammatory activity even when serum LDH levels 
are normal or only mildly elevated. This criterion is particularly useful in patients 
with normal serum LDH but active pleural inflammation.

Clinical Performance and Validation:

Original Study Results (Light et al., 1972):
- Sensitivity for exudates: 98%
- Specificity for exudates: 83%
- Studied 150 patients with known effusion etiologies
- Only 1 exudative effusion misclassified as transudate

Subsequent Validation Studies:
Multiple large-scale validation studies have confirmed the excellent performance of 
Light's criteria across diverse patient populations and clinical settings. The criteria 
maintain high sensitivity (95-99%) across different etiologies of exudative effusions, 
making them highly reliable for excluding transudative causes when any criterion is met.

Clinical Decision-Making Framework:

Positive Light's Criteria (Exudative):
- At least one criterion met → Exudative effusion
- Requires comprehensive diagnostic workup including:
  * Detailed clinical history and physical examination
  * Chest imaging (chest X-ray, CT scan, ultrasonography)
  * Pleural fluid analysis: cytology, microbiology, pH, glucose, adenosine deaminase
  * Specific testing based on clinical suspicion (malignant markers, autoimmune panels)
  * Consider pleural biopsy if initial fluid analysis inconclusive

Negative Light's Criteria (Transudative):
- No criteria met → Transudative effusion
- Focus treatment on underlying systemic condition
- Additional pleural fluid analysis generally not indicated
- Monitor response to treatment of underlying condition
- Consider echocardiography, liver function tests, renal function assessment

Special Clinical Considerations:

Pseudoexudates:
Approximately 15-20% of patients with heart failure treated with diuretics may develop 
"pseudoexudates" - transudative effusions that meet Light's criteria due to fluid and 
electrolyte shifts from diuretic therapy. Clinical indicators include:
- Known heart failure with recent diuretic use
- Clinical improvement with heart failure treatment
- Serum-pleural fluid protein gradient >3.1 g/dL
- Serum-pleural fluid albumin gradient >1.2 g/dL

Borderline Cases:
When Light's criteria suggest exudate but clinical presentation strongly suggests 
transudate, additional testing may be helpful:
- Pleural fluid cholesterol >45 mg/dL suggests exudate
- Pleural fluid cholesterol/serum cholesterol ratio >0.3 suggests exudate
- Pleural fluid bilirubin/serum bilirubin ratio >0.6 suggests exudate

Limitations and Considerations:

Technical Limitations:
- Requires simultaneous serum and pleural fluid sampling (ideally within 24 hours)
- Laboratory variability in protein and LDH measurements
- Hemolyzed samples may artificially elevate LDH levels
- Traumatic thoracentesis may increase protein levels

Clinical Limitations:
- Does not identify specific etiology, only distinguishes mechanism
- Lower specificity (83%) means some transudates classified as exudates
- May be less reliable in patients with chronic kidney disease or severe liver disease
- Performance may vary in immunocompromised patients

Quality Assurance and Implementation:

Laboratory Considerations:
- Ensure proper sample handling and timely analysis
- Use consistent laboratory methods for protein and LDH measurement
- Verify normal reference ranges for institutional LDH values
- Consider point-of-care testing for urgent clinical decision-making

Clinical Workflow Integration:
- Standardize thoracentesis procedures and sample collection
- Implement decision support tools in electronic medical records
- Train clinical staff on proper interpretation and follow-up
- Establish protocols for additional testing based on Light's criteria results

Research and Future Directions:
- Investigation of novel biomarkers for pleural effusion classification
- Development of point-of-care diagnostic tools
- Validation in specific patient populations (pediatric, elderly, immunocompromised)
- Integration with artificial intelligence and machine learning approaches
- Cost-effectiveness studies comparing different diagnostic strategies

Patient Safety and Communication:
- Clear documentation of thoracentesis procedure and complications
- Transparent communication about diagnostic uncertainty and next steps
- Patient education about the nature of pleural effusion and treatment options
- Coordination between multiple specialists (pulmonology, oncology, cardiology)

The enduring clinical utility of Light's criteria reflects their fundamental basis in 
pleural fluid physiology and robust validation across diverse clinical settings. While 
newer diagnostic approaches continue to emerge, Light's criteria remain the essential 
first step in pleural effusion evaluation and continue to guide clinical practice 
worldwide after more than five decades of successful clinical application.
"""

from pydantic import BaseModel, Field
from typing import Optional


class LightsCriteriaRequest(BaseModel):
    """
    Request model for Light's Criteria for Exudative Effusions
    
    Light's Criteria for Exudative Effusions represents the gold standard for 
    differentiating between exudative and transudative pleural effusions. This 
    diagnostic framework, established by Richard Light in 1972, provides clinicians 
    with a reliable, evidence-based approach to pleural effusion classification that 
    guides subsequent diagnostic workup and therapeutic management decisions.
    
    Clinical Assessment Parameters:
    
    Serum Protein (Total):
    Normal serum protein concentration ranges from 6.0-8.3 g/dL and reflects overall 
    nutritional status, hepatic synthetic function, and protein loss or dilution. 
    In the context of pleural effusion evaluation, serum protein serves as the reference 
    standard for calculating the pleural fluid to serum protein ratio. Conditions 
    affecting serum protein (hypoalbuminemia, liver disease, malnutrition) may influence 
    the interpretation of Light's criteria and should be considered in clinical correlation.
    
    Pleural Fluid Protein:
    Pleural fluid protein concentration directly reflects pleural membrane permeability 
    and the underlying pathophysiological mechanism of effusion formation. Transudative 
    effusions typically contain <3.0 g/dL protein due to intact pleural membranes that 
    maintain normal selective permeability. Exudative effusions contain >3.0 g/dL protein 
    due to inflammatory damage that increases membrane permeability, allowing protein-rich 
    fluid to leak into the pleural space. The protein concentration provides crucial 
    information about the nature and severity of the underlying pleural process.
    
    Serum LDH (Lactate Dehydrogenase):
    Serum LDH is an intracellular enzyme found in multiple tissues including heart, 
    liver, muscle, kidney, and lung. Normal serum LDH ranges from 140-280 U/L (varies 
    by laboratory and method). Elevated serum LDH may indicate tissue damage, hemolysis, 
    or cellular turnover, but alone does not provide specific diagnostic information 
    about pleural pathology. In Light's criteria, serum LDH serves as the reference 
    for calculating pleural fluid to serum LDH ratios and establishing the absolute 
    threshold for pleural fluid LDH elevation.
    
    Pleural Fluid LDH:
    Pleural fluid LDH elevation indicates active cellular metabolism, inflammation, 
    tissue destruction, or malignant cellular activity within the pleural space. 
    Transudative effusions typically have low LDH levels (<200 U/L) reflecting minimal 
    cellular activity and intact pleural surfaces. Exudative effusions demonstrate 
    elevated LDH levels due to inflammatory cell infiltration, tissue necrosis, 
    malignant cell metabolism, or bacterial fermentation. Extremely high pleural fluid 
    LDH levels (>1000 U/L) suggest empyema, complicated parapneumonic effusion, or 
    extensive malignant involvement.
    
    Upper Limit of Normal Serum LDH:
    The upper limit of normal for serum LDH varies by laboratory, analytical method, 
    and reference population. Common reference ranges include 222 U/L, 245 U/L, or 
    480 U/L depending on the assay used. This parameter is essential for calculating 
    the third Light's criterion (pleural fluid LDH > 2/3 × upper normal limit). 
    When not specified, the calculator uses 222 U/L as the default, but clinicians 
    should verify their institution's specific reference range for optimal accuracy.
    
    Clinical Application Guidelines:
    - Obtain pleural fluid and serum samples simultaneously (ideally within 24 hours)
    - Ensure proper sample handling to prevent hemolysis or protein degradation
    - Consider clinical context when interpreting borderline results
    - Verify laboratory reference ranges for accurate threshold calculations
    - Document timing of diuretic administration if patient has heart failure
    - Correlate results with clinical presentation and imaging findings
    
    Diagnostic Decision Framework:
    - ANY single criterion positive → Exudative effusion (requires comprehensive workup)
    - ALL criteria negative → Transudative effusion (treat underlying condition)
    - Consider pseudoexudate if heart failure patient on diuretics meets criteria
    - Use additional tests (albumin gradient, cholesterol) for ambiguous cases
    
    Quality Assurance Considerations:
    - Verify simultaneous sampling of serum and pleural fluid
    - Check for sample hemolysis that may artificially elevate LDH
    - Ensure consistent laboratory methodology for protein and LDH measurement
    - Validate institutional LDH reference ranges and update as needed
    - Monitor clinical outcomes and diagnostic accuracy in local patient population
    
    References (Vancouver style):
    1. Light RW, Macgregor MI, Luchsinger PC, Ball WC Jr. Pleural effusions: the 
    diagnostic separation of transudates and exudates. Ann Intern Med. 1972 
    Oct;77(4):507-13. doi: 10.7326/0003-4819-77-4-507.
    2. Heffner JE, Brown LK, Barbieri C, DeLeo JM. Pleural fluid chemical analysis 
    in parapneumonic effusions. A meta-analysis. Am J Respir Crit Care Med. 1995 
    Jun;151(6):1700-8. doi: 10.1164/ajrccm.151.6.7767510.
    3. Porcel JM, Light RW. Diagnostic approach to pleural effusion in adults. 
    Am Fam Physician. 2006 Apr 1;73(7):1211-20.
    """
    
    serum_protein: float = Field(
        ...,
        description="Total serum protein concentration in g/dL. Normal range: 6.0-8.3 g/dL. "
                   "Reflects overall nutritional status, hepatic synthetic function, and protein "
                   "balance. Used as the reference standard for calculating pleural fluid to serum "
                   "protein ratio in Light's first criterion. Conditions affecting serum protein "
                   "(hypoalbuminemia, liver disease, malnutrition, protein-losing nephropathy) may "
                   "influence interpretation and should be considered in clinical correlation.",
        ge=1.0,
        le=15.0,
        example=7.2
    )
    
    pleural_fluid_protein: float = Field(
        ...,
        description="Pleural fluid protein concentration in g/dL. Directly reflects pleural membrane "
                   "permeability and underlying pathophysiology. Transudative effusions typically "
                   "contain <3.0 g/dL protein due to intact pleural membranes maintaining selective "
                   "permeability. Exudative effusions contain >3.0 g/dL protein due to inflammatory "
                   "damage increasing membrane permeability. Values >5.0 g/dL strongly suggest "
                   "exudative process with significant inflammation or malignant involvement.",
        ge=0.1,
        le=10.0,
        example=4.1
    )
    
    serum_ldh: float = Field(
        ...,
        description="Serum lactate dehydrogenase (LDH) level in U/L. Normal range varies by laboratory "
                   "(typically 140-280 U/L). LDH is an intracellular enzyme found in heart, liver, "
                   "muscle, kidney, and lung tissues. Elevated serum LDH may indicate tissue damage, "
                   "hemolysis, or increased cellular turnover. In Light's criteria, serves as reference "
                   "for calculating pleural fluid to serum LDH ratio and establishing absolute threshold "
                   "for pleural fluid LDH elevation. Verify institutional reference ranges for accuracy.",
        ge=50.0,
        le=2000.0,
        example=180.0
    )
    
    pleural_fluid_ldh: float = Field(
        ...,
        description="Pleural fluid lactate dehydrogenase (LDH) level in U/L. Elevation indicates active "
                   "cellular metabolism, inflammation, tissue destruction, or malignant activity within "
                   "pleural space. Transudative effusions typically have low LDH (<200 U/L) reflecting "
                   "minimal cellular activity. Exudative effusions show elevated LDH due to inflammatory "
                   "cells, tissue necrosis, malignant metabolism, or bacterial activity. Extremely high "
                   "levels (>1000 U/L) suggest empyema, complicated parapneumonic effusion, or extensive "
                   "malignant involvement requiring urgent intervention.",
        ge=10.0,
        le=5000.0,
        example=350.0
    )
    
    serum_ldh_upper_normal: Optional[float] = Field(
        222.0,
        description="Upper limit of normal for serum LDH at your institution in U/L. This value varies "
                   "by laboratory, analytical method, and reference population. Common ranges include "
                   "222 U/L, 245 U/L, or 480 U/L depending on assay methodology. Essential for calculating "
                   "Light's third criterion (pleural fluid LDH > 2/3 × upper normal limit). Default value "
                   "is 222 U/L, but clinicians should verify and use their institution's specific reference "
                   "range for optimal diagnostic accuracy. Contact laboratory for current reference values.",
        ge=100.0,
        le=500.0,
        example=222.0
    )
    
    class Config:
        schema_extra = {
            "example": {
                "serum_protein": 7.2,
                "pleural_fluid_protein": 4.1,
                "serum_ldh": 180.0,
                "pleural_fluid_ldh": 350.0,
                "serum_ldh_upper_normal": 222.0
            }
        }


class LightsCriteriaResponse(BaseModel):
    """
    Response model for Light's Criteria for Exudative Effusions
    
    Provides calculated classification of pleural effusion as exudative or transudative 
    based on Light's criteria, with detailed analysis of each criterion and evidence-based 
    recommendations for clinical management. The response guides appropriate diagnostic 
    workup and therapeutic decision-making based on the underlying pathophysiology 
    suggested by the effusion classification.
    
    Classification Categories and Clinical Implications:
    
    Transudative Effusion (0 criteria met):
    - Pathophysiology: Altered hydrostatic/oncotic pressures across normal pleural membranes
    - Clinical approach: Focus treatment on underlying systemic condition
    - Common causes: Congestive heart failure (90%), cirrhosis, nephrotic syndrome, hypothyroidism
    - Diagnostic strategy: Limited additional pleural fluid analysis required
    - Management priorities: Optimize heart failure treatment, diuresis, treat liver/kidney disease
    - Prognosis: Generally good response to treatment of underlying condition
    - Monitoring: Serial chest imaging to assess response to systemic therapy
    
    Exudative Effusion (≥1 criteria met):
    - Pathophysiology: Increased capillary permeability or impaired lymphatic drainage
    - Clinical approach: Comprehensive diagnostic workup required
    - Common causes: Pneumonia (40%), malignancy (25%), pulmonary embolism, autoimmune disease
    - Diagnostic strategy: Extended pleural fluid analysis including cytology, microbiology, pH
    - Management priorities: Identify and treat specific underlying cause
    - Prognosis: Variable depending on underlying etiology and stage
    - Monitoring: Close follow-up for response to specific therapy and complications
    
    Light's Criteria Performance Characteristics:
    
    Diagnostic Accuracy:
    - Sensitivity for exudates: 98% (highly reliable for identifying inflammatory processes)
    - Specificity for exudates: 83% (some transudates may be misclassified as exudates)
    - Negative predictive value: >95% (very reliable when all criteria negative)
    - Positive predictive value: Variable depending on prevalence and clinical context
    
    Clinical Decision Framework:
    
    Exudative Classification (Any Criterion Positive):
    - Immediate actions: Comprehensive pleural fluid analysis, chest imaging
    - Laboratory studies: Cytology, Gram stain, cultures, pH, glucose, adenosine deaminase
    - Imaging: Chest CT with contrast, consider ultrasonography for loculations
    - Specialist consultation: Pulmonology for thoracic procedures, oncology if malignancy suspected
    - Treatment planning: Cause-specific therapy, consider pleural drainage for symptomatic relief
    - Monitoring: Regular assessment for response to therapy and complications
    
    Transudative Classification (All Criteria Negative):
    - Immediate actions: Optimize treatment of underlying systemic condition
    - Laboratory studies: Basic metabolic panel, liver function, cardiac biomarkers, albumin
    - Imaging: Echocardiography for heart failure assessment, abdominal imaging if cirrhosis
    - Specialist consultation: Cardiology for heart failure, hepatology for liver disease
    - Treatment planning: Diuresis, afterload reduction, sodium restriction
    - Monitoring: Clinical response and effusion resolution with systemic therapy
    
    Special Clinical Situations:
    
    Pseudoexudates (Heart Failure + Diuretics):
    - Recognition: Known heart failure patient on diuretics with "exudative" criteria
    - Additional testing: Serum-pleural fluid protein gradient >3.1 g/dL suggests transudate
    - Management approach: Continue heart failure optimization, avoid unnecessary procedures
    - Clinical correlation: Bilateral effusions, response to diuresis, no fever or chest pain
    
    Borderline or Ambiguous Cases:
    - Additional markers: Pleural fluid cholesterol, albumin gradient, NT-proBNP
    - Clinical context: Symptom onset, associated conditions, response to therapy
    - Expert consultation: Pulmonology for complex cases requiring advanced procedures
    - Repeat analysis: Consider if clinical course doesn't match initial classification
    
    Quality Assurance and Validation:
    
    Technical Considerations:
    - Verify simultaneous serum and pleural fluid sampling (ideally <24 hours apart)
    - Check for sample hemolysis that may artificially elevate LDH measurements
    - Confirm laboratory reference ranges match institutional standards
    - Ensure consistent methodology for protein and LDH analysis
    
    Clinical Correlation:
    - Integrate results with clinical presentation, imaging findings, and patient history
    - Consider alternative diagnoses if classification doesn't match clinical picture
    - Document rationale for management decisions based on Light's criteria results
    - Monitor outcomes to validate diagnostic accuracy in local patient population
    
    Communication and Documentation:
    - Clear explanation of results and implications to patients and families
    - Detailed documentation of thoracentesis procedure and sample analysis
    - Coordination between multiple specialists based on effusion classification
    - Patient education about underlying condition and treatment expectations
    
    Research and Quality Improvement:
    - Track diagnostic accuracy and clinical outcomes in institutional patient population
    - Validate performance in specific patient subgroups (elderly, immunocompromised)
    - Implement decision support tools and standardized diagnostic pathways
    - Contribute to ongoing research on pleural effusion diagnostic strategies
    
    The robust performance of Light's criteria across diverse clinical settings and patient 
    populations reflects their fundamental basis in pleural fluid physiology. After more 
    than 50 years of clinical validation, these criteria continue to provide the essential 
    framework for pleural effusion evaluation and guide evidence-based diagnostic and 
    therapeutic decision-making worldwide.
    
    Reference: Light RW, et al. Annals of Internal Medicine. 1972;77(4):507-513.
    """
    
    result: int = Field(
        ...,
        description="Number of Light's criteria met (0-3). Any positive criterion (≥1) classifies effusion as exudative",
        example=2
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for criteria count",
        example="criteria"
    )
    
    interpretation: str = Field(
        ...,
        description="Comprehensive clinical interpretation including effusion classification, criteria analysis, "
                   "underlying pathophysiology, and evidence-based recommendations for diagnostic workup and management",
        example="Light's Criteria: 2 of 3 criteria met. Classification: Exudative effusion. Criteria met: protein ratio 0.57 > 0.5, LDH ratio 1.94 > 0.6. This indicates an inflammatory process requiring further diagnostic workup. Common causes include pneumonia, malignancy, tuberculosis, pulmonary embolism, autoimmune conditions, or other inflammatory processes. Recommend thoracentesis for additional pleural fluid analysis including cytology, microbiology, and specific markers as clinically indicated. Light's criteria have 98% sensitivity for identifying exudates, making this a reliable classification for guiding further evaluation and management."
    )
    
    stage: str = Field(
        ...,
        description="Effusion classification (Exudate or Transudate)",
        example="Exudate"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the effusion type",
        example="Exudative effusion"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 2,
                "unit": "criteria",
                "interpretation": "Light's Criteria: 2 of 3 criteria met. Classification: Exudative effusion. Criteria met: protein ratio 0.57 > 0.5, LDH ratio 1.94 > 0.6. This indicates an inflammatory process requiring further diagnostic workup. Common causes include pneumonia, malignancy, tuberculosis, pulmonary embolism, autoimmune conditions, or other inflammatory processes. Recommend thoracentesis for additional pleural fluid analysis including cytology, microbiology, and specific markers as clinically indicated. Light's criteria have 98% sensitivity for identifying exudates, making this a reliable classification for guiding further evaluation and management.",
                "stage": "Exudate",
                "stage_description": "Exudative effusion"
            }
        }