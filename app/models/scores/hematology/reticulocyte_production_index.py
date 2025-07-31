"""
Reticulocyte Production Index (RPI) Models

Request and response models for RPI bone marrow response assessment calculation.

References (Vancouver style):
1. Koepke JA. Laboratory hematology practice. New York: Churchill Livingstone; 1989.
2. Hillman RS, Ault KA. Hematology in clinical practice. New York: McGraw-Hill; 2002.
3. Nathan DG, Orkin SH, Look AT, Ginsburg D. Nathan and Oski's Hematology of Infancy 
   and Childhood. 6th ed. Philadelphia: W.B. Saunders; 2003.
4. Bain BJ. Blood Cells: A Practical Guide. 4th ed. Oxford: Blackwell Publishing; 2006.

The Reticulocyte Production Index (RPI) is a calculated hematologic parameter used to 
assess the appropriateness of bone marrow response to anemia. It corrects the raw 
reticulocyte count for both the degree of anemia and the maturation time of reticulocytes, 
providing a more accurate assessment of effective red blood cell production.

Clinical Background and Development:

Reticulocyte Physiology:
Reticulocytes are immature red blood cells that have recently been released from the 
bone marrow and still contain remnants of ribosomes and mitochondria. In the normal 
circulation, reticulocytes mature into fully developed erythrocytes within 1-2 days. 
The reticulocyte count reflects the rate of red blood cell production and bone marrow 
activity in response to erythropoietic stimuli.

Need for Correction in Anemia:
In anemic patients, the raw reticulocyte percentage can be misleading because:
1. The percentage is calculated against a reduced total RBC count, artificially inflating the apparent reticulocyte response
2. Severe anemia triggers premature release of reticulocytes from bone marrow, requiring longer maturation time in circulation
3. The degree of anemia affects the expected magnitude of reticulocyte response

Two-Step Correction Process:
The RPI calculation involves two essential corrections to provide accurate assessment:

Step 1 - Correction for Anemia Severity:
Corrected Reticulocyte % = Raw Reticulocyte % × (Patient Hematocrit / Normal Hematocrit)

This correction accounts for the reduced red cell mass in anemia, providing a more 
accurate reflection of absolute reticulocyte production relative to normal conditions.

Step 2 - Correction for Maturation Time:
RPI = Corrected Reticulocyte % / Maturation Factor

Maturation factors account for prolonged circulation time of prematurely released reticulocytes:
- Hematocrit ≥35%: Factor 1.0 (normal maturation, 1 day)
- Hematocrit 25-34%: Factor 1.5 (mild prolongation, 1.5 days)
- Hematocrit 20-24%: Factor 2.0 (moderate prolongation, 2 days)  
- Hematocrit <20%: Factor 2.5 (severe prolongation, 2.5 days)

Clinical Applications and Diagnostic Utility:

Anemia Classification and Differential Diagnosis:
The RPI serves as a critical tool for classifying anemia into two major categories:

Hypoproliferative Anemia (RPI <2.0):
- Bone marrow failure syndromes (aplastic anemia, myelodysplastic syndrome)
- Nutritional deficiencies (iron, B12, folate)
- Chronic kidney disease with erythropoietin deficiency
- Chronic inflammatory conditions
- Malignant bone marrow infiltration
- Drug-induced bone marrow suppression

Hyperproliferative Anemia (RPI >3.0):
- Hemolytic anemia (hereditary spherocytosis, autoimmune hemolysis)
- Acute blood loss and hemorrhage
- Microangiopathic hemolytic anemia
- Hypersplenism with increased red cell destruction
- Recovery phase from bone marrow suppression

Borderline Response (RPI 2.0-3.0):
- Early recovery from nutritional deficiency treatment
- Mild bone marrow dysfunction
- Mixed pathophysiology conditions
- Transition phases in treatment response

Clinical Assessment Framework and Interpretation:

Normal Reference Values:
In healthy individuals, the RPI typically ranges from 0.5 to 2.5, reflecting balanced 
red cell production and destruction. Values within this range indicate appropriate 
bone marrow function relative to physiologic demands.

Pathologic RPI Values and Clinical Significance:

Very Low RPI (<0.5):
Clinical Significance:
- Severe bone marrow failure or complete suppression
- Advanced malignant infiltration of bone marrow
- Severe nutritional deficiencies with profound impact
- Drug-induced severe bone marrow toxicity

Immediate Clinical Actions:
- Urgent hematology consultation for bone marrow evaluation
- Comprehensive nutritional assessment and replacement
- Medication review for potential bone marrow suppressants
- Evaluation for underlying malignancy or systemic disease

Low RPI (0.5-2.0):
Clinical Significance:
- Inadequate bone marrow response to anemic stress
- Hypoproliferative anemia requiring etiology investigation
- Chronic disease states affecting erythropoiesis
- Mild to moderate nutritional deficiencies

Diagnostic Approach:
- Iron studies (serum iron, TIBC, ferritin, transferrin saturation)
- Vitamin B12 and folate levels
- Kidney function assessment and erythropoietin levels
- Inflammatory markers (ESR, CRP) for chronic disease
- Thyroid function studies
- Consider bone marrow biopsy if unexplained

Borderline RPI (2.0-3.0):
Clinical Significance:
- Marginal bone marrow response suggesting partial recovery
- Early treatment response to nutritional replacement
- Mild bone marrow dysfunction with compensatory capacity
- Mixed pathophysiology requiring continued monitoring

Management Strategy:
- Serial RPI monitoring to assess trend and treatment response
- Continue targeted therapy for identified deficiencies
- Close clinical follow-up for symptom progression
- Consider additional diagnostic evaluation if no improvement

High RPI (>3.0):
Clinical Significance:
- Appropriate bone marrow response indicating intact erythropoiesis
- Suggests hemolytic or hemorrhagic cause of anemia
- Effective compensatory mechanism for red cell loss
- Good prognosis with treatment of underlying cause

Diagnostic Focus:
- Hemolysis evaluation (LDH, haptoglobin, bilirubin, direct Coombs)
- Source identification for acute or chronic blood loss
- Peripheral blood smear for morphologic abnormalities
- Specialized hemolysis testing (osmotic fragility, flow cytometry)

Special Clinical Considerations and Limitations:

Recent Blood Transfusions:
Blood transfusions can significantly affect RPI interpretation by:
- Artificially elevating hematocrit and reducing calculated RPI
- Suppressing endogenous reticulocyte production
- Masking underlying bone marrow dysfunction
- Requiring delay of 2-3 weeks for accurate assessment

Acute vs. Chronic Anemia:
- Acute anemia may show initially low RPI due to insufficient time for bone marrow response
- Chronic anemia allows full development of compensatory mechanisms
- Time course of anemia affects interpretation of RPI adequacy
- Serial measurements may be more informative than single values

Age and Gender Considerations:
- Elderly patients may have reduced bone marrow reserve affecting RPI response
- Gender differences in normal hematocrit values may require adjusted reference ranges
- Pediatric patients require age-specific normal values for accurate interpretation
- Pregnancy physiologically alters hematocrit and reticulocyte dynamics

Laboratory Methodology and Quality Assurance:

Reticulocyte Counting Methods:
Modern automated hematology analyzers use flow cytometry with fluorescent dyes to 
identify reticulocytes based on RNA content, providing more accurate and reproducible 
results compared to manual supravital staining methods.

Quality Control Considerations:
- Ensure proper sample handling and timely analysis
- Verify automated analyzer calibration and quality control
- Consider manual verification for discrepant results
- Account for potential interference from abnormal hemoglobins

Clinical Correlation Requirements:
- Integrate RPI results with complete blood count parameters
- Consider peripheral blood smear morphology
- Evaluate clinical presentation and symptom duration
- Coordinate with other laboratory markers of hemolysis or deficiency

Implementation in Clinical Practice:

Primary Care Applications:
- Initial evaluation of unexplained anemia
- Monitoring treatment response to iron or vitamin supplementation
- Screening for underlying hematologic disorders
- Guiding referral decisions for specialty evaluation

Hematology Specialty Use:
- Detailed anemia classification and differential diagnosis
- Monitoring of bone marrow recovery after chemotherapy
- Assessment of chronic hemolytic conditions
- Evaluation of treatment efficacy in various anemias

Critical Care and Hospital Medicine:
- Evaluation of anemia in critically ill patients
- Assessment of bone marrow function in sepsis or multiorgan failure
- Monitoring during intensive care interventions
- Guiding transfusion decisions and management strategies

This comprehensive RPI assessment provides clinicians with a validated tool for 
accurately evaluating bone marrow response to anemia, supporting evidence-based 
diagnosis and management of diverse hematologic conditions.
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any


class ReticulocyteProductionIndexRequest(BaseModel):
    """
    Request model for Reticulocyte Production Index (RPI) Calculation
    
    The RPI assesses the appropriateness of bone marrow response to anemia by correcting 
    the raw reticulocyte count for both the degree of anemia and the maturation time 
    of reticulocytes, providing accurate evaluation of effective red blood cell production.
    
    Assessment Framework and Parameter Specifications:
    
    The RPI calculation requires three essential parameters with one optional parameter 
    for comprehensive hematologic assessment:
    
    Reticulocyte Percentage:
    The reticulocyte percentage represents the proportion of circulating red blood cells 
    that are immature reticulocytes, typically reported as a percentage of total RBCs. 
    This value reflects the recent output of red blood cells from the bone marrow.
    
    Laboratory Measurement Standards:
    - Obtained from complete blood count with reticulocyte count
    - Modern automated analyzers use flow cytometry with fluorescent RNA stains
    - More accurate than historical manual supravital staining methods
    - Results typically available within 1-2 hours of sample collection
    - Normal reference range varies by age and laboratory methodology
    
    Clinical Significance:
    - Reflects bone marrow erythropoietic activity over past 1-2 days
    - Elevated values suggest increased red cell production
    - Low values may indicate bone marrow suppression or dysfunction
    - Raw percentage requires correction for anemia severity
    
    Quality Considerations:
    - Sample should be analyzed within 4-6 hours of collection
    - EDTA anticoagulated blood preferred for stability
    - Avoid hemolyzed or clotted specimens
    - Verify automated results if clinically discrepant
    
    Measured Hematocrit:
    The patient's measured hematocrit represents the percentage of blood volume occupied 
    by red blood cells, serving as the primary indicator of anemia severity and the 
    baseline for reticulocyte correction calculations.
    
    Clinical Assessment Guidelines:
    - Standard component of complete blood count
    - Reflects current red cell mass and anemia severity
    - Used to determine appropriate maturation correction factor
    - Should correlate with hemoglobin and clinical presentation
    
    Anemia Severity Classification:
    - Hematocrit ≥35%: No anemia or mild anemia
    - Hematocrit 25-34%: Mild to moderate anemia
    - Hematocrit 20-24%: Moderate anemia
    - Hematocrit <20%: Severe anemia requiring urgent evaluation
    
    Clinical Context:
    - Recent blood loss may show disproportionate hematocrit changes
    - Dehydration can artificially elevate hematocrit values
    - Fluid overload may dilute and reduce apparent hematocrit
    - Consider clinical presentation when interpreting values
    
    Normal Hematocrit Reference:
    The normal hematocrit reference value represents the expected hematocrit for a 
    healthy individual of similar demographics, typically 45% for adults, used as 
    the denominator in the anemia correction calculation.
    
    Reference Value Selection:
    - Standard adult reference: 45% (commonly used)
    - May adjust for age: pediatric values vary by age group
    - Gender considerations: male 42-52%, female 37-47%
    - Population-specific references may apply
    - Laboratory-specific normal ranges should be considered
    
    Calculation Significance:
    - Provides normalization factor for anemia correction
    - Higher reference values increase calculated RPI
    - Lower reference values decrease calculated RPI
    - Should match population characteristics when possible
    
    Quality Assurance:
    - Use consistent reference value for serial measurements
    - Document reference value used for interpretation
    - Consider laboratory-specific normal ranges
    - Adjust for demographic factors when appropriate
    
    Red Blood Cell Count (Optional):
    The RBC count enables calculation of absolute reticulocyte count, providing additional 
    clinical information about total reticulocyte production independent of percentage 
    calculations, useful for comprehensive hematologic assessment.
    
    Absolute Reticulocyte Count Calculation:
    Absolute Count = (Reticulocyte % / 100) × RBC Count × 10⁶
    
    Clinical Utility:
    - Provides absolute measure of reticulocyte production
    - Independent of percentage variations due to total RBC changes
    - Useful for monitoring treatment response over time
    - Helps distinguish true production changes from dilutional effects
    
    Normal Reference Ranges:
    - Adult absolute count: 25,000-100,000 cells/μL
    - Varies with age, gender, and altitude
    - Higher values in infants and children
    - Pregnancy may show physiologic elevation
    
    Interpretation Considerations:
    - Absolute count may be more informative than percentage in some cases
    - Useful for tracking bone marrow recovery after treatment
    - Consider in context of total RBC count and clinical presentation
    - May be particularly valuable in patients with very low or high RBC counts
    
    Clinical Implementation and Quality Assurance:
    
    Sample Collection and Handling:
    - Use EDTA anticoagulated blood for optimal stability
    - Analyze within 4-6 hours of collection for accuracy
    - Avoid hemolyzed, clotted, or lipemic specimens
    - Maintain appropriate storage temperature (2-8°C) if delayed
    
    Laboratory Methodology:
    - Automated flow cytometric methods preferred for accuracy
    - Manual methods may be used for verification
    - Ensure proper instrument calibration and quality control
    - Consider methodology limitations and interference factors
    
    Clinical Correlation:
    - Integrate results with complete clinical presentation
    - Consider recent transfusions, medications, and treatments
    - Evaluate trends over time rather than isolated values
    - Coordinate with other hematologic parameters and studies
    
    Result Validation:
    - Verify automated results if clinically unexpected
    - Check for mathematical calculation errors
    - Consider repeat testing if results are borderline
    - Document any technical or clinical factors affecting interpretation
    
    References (Vancouver style):
    1. Koepke JA. Laboratory hematology practice. New York: Churchill Livingstone; 1989.
    2. Hillman RS, Ault KA. Hematology in clinical practice. New York: McGraw-Hill; 2002.
    3. Nathan DG, Orkin SH, Look AT, Ginsburg D. Nathan and Oski's Hematology of Infancy 
       and Childhood. 6th ed. Philadelphia: W.B. Saunders; 2003.
    """
    
    reticulocyte_percentage: float = Field(
        ...,
        ge=0.0,
        le=50.0,
        description="Reticulocyte percentage from laboratory report. Obtained from complete blood count with automated flow cytometry. Normal range varies by age and methodology",
        example=2.5
    )
    
    measured_hematocrit: float = Field(
        ...,
        ge=5.0,
        le=65.0,
        description="Patient's measured hematocrit percentage from CBC. Reflects anemia severity and determines maturation correction factor. Consider clinical context for interpretation",
        example=25.0
    )
    
    normal_hematocrit: float = Field(
        ...,
        ge=35.0,
        le=50.0,
        description="Normal hematocrit reference value for demographic comparison. Typically 45% for adults. Use consistent value for serial measurements",
        example=45.0
    )
    
    rbc_count: Optional[float] = Field(
        None,
        ge=1.0,
        le=8.0,
        description="Red blood cell count (×10⁶/μL) for absolute reticulocyte count calculation. Optional parameter providing additional clinical information",
        example=2.8
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "reticulocyte_percentage": 2.5,
                "measured_hematocrit": 25.0,
                "normal_hematocrit": 45.0,
                "rbc_count": 2.8
            }
        }


class CalculationDetails(BaseModel):
    """Detailed calculation information for RPI assessment"""
    
    reticulocyte_percentage: float = Field(
        ...,
        description="Original reticulocyte percentage from laboratory",
        example=2.5
    )
    
    corrected_reticulocyte_percentage: float = Field(
        ...,
        description="Reticulocyte percentage corrected for anemia severity",
        example=1.39
    )
    
    maturation_factor: float = Field(
        ...,
        description="Correction factor for reticulocyte maturation time based on hematocrit",
        example=1.5
    )
    
    maturation_level: str = Field(
        ...,
        description="Anemia severity level determining maturation factor",
        example="mild"
    )
    
    hematocrit_severity: str = Field(
        ...,
        description="Clinical assessment of anemia severity based on hematocrit",
        example="Mild to moderate anemia"
    )
    
    absolute_reticulocyte_count: Optional[float] = Field(
        None,
        description="Absolute reticulocyte count in cells/μL (if RBC count provided)",
        example=70000
    )
    
    bone_marrow_response: str = Field(
        ...,
        description="Assessment of bone marrow response adequacy",
        example="Impaired"
    )
    
    clinical_significance: str = Field(
        ...,
        description="Clinical significance of the calculated RPI value",
        example="Hypoproliferative anemia"
    )


class ReticulocyteProductionIndexResponse(BaseModel):
    """
    Response model for Reticulocyte Production Index (RPI) Calculation
    
    Provides comprehensive RPI assessment with clinical interpretation, bone marrow 
    response evaluation, and evidence-based recommendations for anemia diagnosis 
    and management based on validated hematologic principles.
    
    RPI Assessment Framework and Clinical Interpretation:
    
    Scale Overview and Diagnostic Significance:
    The RPI represents a corrected measure of reticulocyte production that accounts 
    for anemia severity and reticulocyte maturation time, providing accurate assessment 
    of bone marrow response to anemic stress. This correction enables clinicians to 
    distinguish between hypoproliferative and hyperproliferative causes of anemia.
    
    Clinical Applications and Diagnostic Framework:
    
    Normal RPI Assessment (0.5-2.5):
    
    Clinical Significance:
    - Normal bone marrow response to physiologic demands
    - Balanced red cell production and destruction
    - No evidence of pathologic erythropoietic stress
    - Appropriate reticulocyte output for clinical condition
    
    Management Recommendations:
    - Routine hematologic monitoring as clinically indicated
    - No specific intervention required for RPI findings
    - Focus on underlying condition management
    - Document baseline for future comparison
    
    Quality of Life Implications:
    - Normal erythropoietic capacity with good prognosis
    - No restrictions related to bone marrow function
    - Standard medical care without hematologic concerns
    - Normal response expected to future erythropoietic stress
    
    Very Low RPI Assessment (<0.5):
    
    Critical Clinical Significance:
    - Severe bone marrow failure or complete suppression
    - Advanced malignant infiltration of bone marrow
    - Severe nutritional deficiencies with profound impact
    - Drug-induced severe bone marrow toxicity
    
    Immediate Clinical Actions:
    - Urgent hematology consultation for comprehensive evaluation
    - Bone marrow biopsy consideration for definitive diagnosis
    - Comprehensive medication review for bone marrow suppressants
    - Nutritional assessment and aggressive replacement therapy
    
    Specialized Care Requirements:
    - Multidisciplinary hematology team involvement
    - Consider bone marrow transplant evaluation if appropriate
    - Intensive supportive care including transfusion support
    - Close monitoring for complications and infection risk
    
    Prognosis and Long-term Considerations:
    - Variable prognosis depending on underlying etiology
    - Potential for recovery with appropriate treatment
    - May require long-term hematologic follow-up
    - Family counseling regarding potential genetic conditions
    
    Low RPI Assessment (0.5-2.0) - Hypoproliferative Anemia:
    
    Clinical Significance and Differential Diagnosis:
    - Inadequate bone marrow response to anemic stress
    - Hypoproliferative anemia requiring etiology investigation
    - Bone marrow dysfunction or nutritional deficiency
    - Chronic disease states affecting erythropoiesis
    
    Comprehensive Diagnostic Approach:
    - Iron studies: serum iron, TIBC, ferritin, transferrin saturation
    - Vitamin deficiency assessment: B12, folate, thiamine
    - Kidney function and erythropoietin levels
    - Inflammatory markers for chronic disease assessment
    - Thyroid function studies and hormonal evaluation
    
    Common Etiologies:
    - Iron deficiency anemia (most common globally)
    - Chronic kidney disease with erythropoietin deficiency
    - Chronic inflammatory conditions and infections
    - Bone marrow infiltration by malignancy
    - Drug-induced bone marrow suppression
    - Aplastic anemia and myelodysplastic syndromes
    
    Treatment Strategy:
    - Targeted therapy based on specific deficiency identified
    - Iron replacement with monitoring of response
    - Vitamin supplementation with appropriate dosing
    - Treatment of underlying chronic conditions
    - Discontinuation of offending medications when possible
    
    Monitoring and Follow-up:
    - Serial RPI measurements to assess treatment response
    - Expected improvement within 2-4 weeks of appropriate therapy
    - Bone marrow biopsy if no response to empirical treatment
    - Long-term monitoring for relapse or progression
    
    Borderline RPI Assessment (2.0-3.0):
    
    Clinical Significance:
    - Marginal bone marrow response suggesting partial recovery
    - Early treatment response to nutritional replacement
    - Mild bone marrow dysfunction with compensatory capacity
    - Transition phase requiring continued monitoring
    
    Management Strategy:
    - Continue current treatment regimen with close monitoring
    - Serial RPI measurements to assess trend and progression
    - Optimize nutritional replacement and supportive care
    - Consider additional diagnostic evaluation if no improvement
    
    Prognostic Implications:
    - Generally favorable with continued appropriate treatment
    - May progress to normal RPI with adequate therapy
    - Indicates retained bone marrow reserve and function
    - Good response expected to optimal medical management
    
    High RPI Assessment (>3.0) - Hyperproliferative Anemia:
    
    Clinical Significance and Diagnostic Focus:
    - Appropriate bone marrow response indicating intact erythropoiesis
    - Suggests hemolytic or hemorrhagic cause of anemia
    - Effective compensatory mechanism for red cell loss
    - Good prognosis with treatment of underlying cause
    
    Hemolysis Evaluation Protocol:
    - Laboratory markers: LDH, haptoglobin, indirect bilirubin
    - Direct antiglobulin test (Coombs) for autoimmune hemolysis
    - Peripheral blood smear for morphologic abnormalities
    - Specialized testing: osmotic fragility, flow cytometry
    - Hemoglobin electrophoresis for hemoglobinopathies
    
    Hemorrhage Assessment:
    - Detailed history for obvious and occult bleeding sources
    - Physical examination for signs of blood loss
    - Stool testing for occult blood
    - Upper and lower gastrointestinal evaluation if indicated
    - Gynecologic evaluation for menstrual blood loss
    
    Common Etiologies:
    - Hereditary spherocytosis and other membrane defects
    - Autoimmune hemolytic anemia
    - Acute or chronic blood loss
    - Microangiopathic hemolytic anemia
    - Drug-induced hemolysis
    - Hypersplenism with increased red cell destruction
    
    Treatment Approach:
    - Address underlying cause of hemolysis or bleeding
    - Supportive care with transfusions if severe
    - Immunosuppressive therapy for autoimmune conditions
    - Splenectomy consideration for hereditary conditions
    - Discontinuation of offending medications
    
    Prognosis and Outcomes:
    - Generally excellent with treatment of underlying cause
    - Normal bone marrow function suggests good recovery potential
    - May require long-term monitoring for specific conditions
    - Quality of life typically good with appropriate management
    
    Special Clinical Considerations and Limitations:
    
    Recent Blood Transfusions:
    - Transfusions suppress endogenous reticulocyte production
    - Artificially elevate hematocrit reducing calculated RPI
    - Mask underlying bone marrow dysfunction
    - Require 2-3 week delay for accurate RPI assessment
    
    Acute vs. Chronic Anemia:
    - Acute anemia may show initially low RPI due to insufficient response time
    - Chronic anemia allows full compensatory mechanism development
    - Serial measurements more informative than single values
    - Time course affects interpretation of RPI adequacy
    
    Age and Demographic Considerations:
    - Elderly patients may have reduced bone marrow reserve
    - Pediatric patients require age-specific reference values
    - Gender differences in normal hematocrit values
    - Pregnancy physiologically alters hematocrit and reticulocyte dynamics
    
    Quality Assurance and Implementation:
    
    Laboratory Methodology:
    - Modern automated analyzers provide accurate flow cytometric results
    - Manual verification for discrepant or unexpected results
    - Proper sample handling and timely analysis essential
    - Quality control measures for reliability and accuracy
    
    Clinical Correlation:
    - Integrate RPI with complete hematologic assessment
    - Consider peripheral blood smear morphology
    - Evaluate clinical presentation and symptom duration
    - Coordinate with other diagnostic studies and specialist consultation
    
    This comprehensive RPI assessment provides clinicians with accurate evaluation 
    of bone marrow response to anemia, supporting evidence-based diagnosis and 
    management of diverse hematologic conditions with validated interpretation 
    criteria and clinical guidance.
    
    Reference: Koepke JA. Laboratory hematology practice. New York: Churchill Livingstone; 1989.
    """
    
    result: float = Field(
        ...,
        description="Reticulocyte Production Index (RPI) value indicating bone marrow response adequacy",
        example=0.93
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the RPI assessment",
        example="index"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation of the RPI value with specific recommendations and diagnostic implications",
        example="RPI of 0.93 is <2.0, indicating inadequate bone marrow response to anemia. This suggests hypoproliferative anemia due to bone marrow dysfunction, nutritional deficiencies, chronic disease, or renal failure."
    )
    
    stage: str = Field(
        ...,
        description="Bone marrow response classification (Very Low Response, Inadequate Response, Borderline Response, Appropriate Response)",
        example="Inadequate Response"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the bone marrow response category",
        example="Inadequate bone marrow response"
    )
    
    calculation_details: CalculationDetails = Field(
        ...,
        description="Detailed calculation information including correction factors and clinical significance"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "result": 0.93,
                "unit": "index",
                "interpretation": "RPI of 0.93 is <2.0, indicating inadequate bone marrow response to anemia. This suggests hypoproliferative anemia due to bone marrow dysfunction, nutritional deficiencies, chronic disease, or renal failure. Patient has mild to moderate anemia (Hct 25.0%).",
                "stage": "Inadequate Response",
                "stage_description": "Inadequate bone marrow response",
                "calculation_details": {
                    "reticulocyte_percentage": 2.5,
                    "corrected_reticulocyte_percentage": 1.39,
                    "maturation_factor": 1.5,
                    "maturation_level": "mild",
                    "hematocrit_severity": "Mild to moderate anemia",
                    "absolute_reticulocyte_count": 70000,
                    "bone_marrow_response": "Impaired",
                    "clinical_significance": "Hypoproliferative anemia"
                }
            }
        }