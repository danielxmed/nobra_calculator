"""
Myxedema Coma Diagnostic Score Models

Request and response models for Myxedema Coma Diagnostic Score calculation.

References (Vancouver style):
1. Popoveniuc G, Chandra T, Sud A, Sharma M, Blackman MR, Burman KD, et al. 
   A diagnostic scoring system for myxedema coma. Endocr Pract. 2014;20(8):808-17. 
   doi: 10.4158/EP13460.OR.
2. Mathew V, Misgar RA, Ghosh S, Mukhopadhyay P, Roychowdhury P, Pandit K, et al. 
   Myxedema coma: a new look into an old crisis. J Thyroid Res. 2011;2011:493462. 
   doi: 10.4061/2011/493462.
3. Wall CR. Myxedema coma: diagnosis and treatment. Am Fam Physician. 2000;62(11):2485-90.

The Myxedema Coma Diagnostic Score is a validated clinical tool for early recognition 
and diagnosis of myxedema coma, a rare but life-threatening decompensated state of 
extreme hypothyroidism with mortality rates of 25-50% if untreated.
"""

from pydantic import BaseModel, Field
from typing import Literal


class MyxedemaComatDiagnosticScoreRequest(BaseModel):
    """
    Request model for Myxedema Coma Diagnostic Score
    
    The Myxedema Coma Diagnostic Score represents a critical advancement in the 
    early recognition and diagnosis of myxedema coma, a rare but life-threatening 
    endocrine emergency. This validated scoring system evaluates multiple organ 
    systems affected by severe hypothyroidism to facilitate prompt diagnosis and 
    life-saving treatment.
    
    Clinical Context and Importance:
    
    Myxedema coma is the most severe manifestation of hypothyroidism, representing 
    complete decompensation of multiple organ systems. It occurs predominantly in 
    elderly patients with long-standing, untreated hypothyroidism, particularly 
    during winter months or following precipitating events. The condition has a 
    mortality rate of 25-50% even with treatment, making early recognition crucial.
    
    Diagnostic Challenge:
    
    Myxedema coma diagnosis has historically been challenging due to:
    - Rarity of the condition leading to low clinical suspicion
    - Nonspecific presenting symptoms that overlap with other conditions
    - Absence of pathognomonic signs requiring clinical synthesis
    - Need for rapid decision-making before laboratory confirmation
    - High mortality risk demanding immediate intervention
    
    Scoring System Components:
    
    The diagnostic score evaluates six critical domains affected by severe hypothyroidism:
    
    1. Thermoregulatory Dysfunction (0-20 points):
    Core body temperature reflects the severity of metabolic decompensation. 
    Hypothermia is present in 80% of patients and correlates with prognosis.
    - Normal ≥37°C: 0 points (preserved thermoregulation)
    - Mild hypothermia 35-37°C: 10 points (early decompensation)
    - Moderate hypothermia 32-35°C: 15 points (significant dysfunction)
    - Severe hypothermia <32°C: 20 points (life-threatening)
    
    2. Central Nervous System Dysfunction (0-30 points):
    Progressive CNS depression is the hallmark of myxedema coma, reflecting 
    decreased cerebral metabolism and potential cerebral edema.
    - Normal mental status: 0 points (intact consciousness)
    - Mild lethargy, decreased concentration: 10 points (early changes)
    - Moderate somnolence, disorientation: 20 points (significant impairment)
    - Stupor, semicoma: 25 points (severe depression)
    - Coma: 30 points (complete unconsciousness)
    
    3. Cardiovascular Dysfunction (0-15 points):
    Cardiac manifestations reflect decreased cardiac output, bradycardia, 
    and potential pericardial effusion with hemodynamic compromise.
    - Normal cardiovascular function: 0 points (stable hemodynamics)
    - Mild bradycardia (HR 60-70 bpm): 5 points (early cardiac effects)
    - Moderate bradycardia (HR <60 bpm) or hypotension: 10 points (significant compromise)
    - Severe shock, cardiac arrest: 15 points (cardiovascular collapse)
    
    4. Gastrointestinal Dysfunction (0-15 points):
    GI manifestations include decreased motility, constipation, and potential 
    ileus reflecting decreased metabolic activity of smooth muscle.
    - Normal gastrointestinal function: 0 points (normal motility)
    - Mild constipation: 5 points (early motility changes)
    - Moderate abdominal distension, decreased bowel sounds: 10 points (significant dysfunction)
    - Severe ileus, absent bowel sounds: 15 points (complete motility failure)
    
    5. Metabolic Dysfunction (0-15 points):
    Metabolic abnormalities include hyponatremia (most common), hypoglycemia, 
    and other electrolyte disturbances reflecting impaired renal function.
    - Normal metabolic parameters: 0 points (preserved homeostasis)
    - Mild hyponatremia (Na+ 130-135 mEq/L): 5 points (early disturbance)
    - Moderate hyponatremia (Na+ 120-129 mEq/L): 10 points (significant imbalance)
    - Severe hyponatremia (Na+ <120 mEq/L) or hypoglycemia: 15 points (life-threatening)
    
    6. Precipitating Events (0-15 points):
    Precipitating factors are present in 80% of cases and often trigger 
    decompensation in patients with severe baseline hypothyroidism.
    - No identifiable precipitating event: 0 points (spontaneous)
    - Minor stress (medication changes, mild illness): 5 points (low-grade stressor)
    - Moderate stress (infection, surgery): 10 points (significant stressor)
    - Major stress (severe infection, major surgery, trauma): 15 points (severe stressor)
    
    Diagnostic Thresholds and Clinical Implications:
    
    Score <25 (Unlikely):
    - Myxedema coma diagnosis unlikely
    - Consider alternative diagnoses for altered consciousness
    - May still have severe hypothyroidism requiring treatment
    - Obtain thyroid function tests for confirmation
    
    Score 25-44 (Possible):
    - Low probability but cannot be excluded
    - Continue evaluation for other causes
    - Urgent thyroid function assessment recommended
    - Monitor closely for clinical deterioration
    
    Score 45-59 (At Risk):
    - Intermediate probability with significant risk
    - Patient at risk for progression to myxedema coma
    - Urgent thyroid function testing and close monitoring
    - Consider empirical treatment if high clinical suspicion
    
    Score ≥60 (Diagnostic):
    - High probability, potentially diagnostic for myxedema coma
    - Immediate emergency treatment indicated
    - 100% sensitivity and 85.71% specificity at this threshold
    - Do not delay treatment for laboratory confirmation
    
    Common Precipitating Events:
    
    Infectious:
    - Pneumonia, urinary tract infections, sepsis
    - Respiratory infections (most common)
    
    Pharmacological:
    - Sedatives, narcotics, anesthesia
    - Lithium, amiodarone, iodine contrast
    - Discontinuation of thyroid hormone therapy
    
    Environmental/Physical:
    - Cold exposure, hypothermia
    - Surgery, trauma, burns
    - Myocardial infarction, stroke
    
    Treatment Considerations:
    
    Immediate Management (Score ≥60):
    - IV levothyroxine 200-400 mcg bolus, then 50-100 mcg daily
    - IV liothyronine (T3) 10-20 mcg every 8 hours if available
    - Stress-dose corticosteroids (hydrocortisone 100-300 mg q8h)
    - Intensive care monitoring with hemodynamic support
    - Passive rewarming, mechanical ventilation if needed
    
    Supportive Care:
    - Treat precipitating factors aggressively
    - Correct electrolyte abnormalities (hyponatremia, hypoglycemia)
    - Avoid sedatives and narcotics that may worsen CNS depression
    - Monitor for complications (cardiac arrhythmias, respiratory failure)
    
    Validation and Performance:
    
    The scoring system demonstrated excellent diagnostic performance in validation studies:
    - Area under ROC curve: 0.88 (95% CI: 0.65-1.00)
    - Sensitivity: 100% at score ≥60
    - Specificity: 85.71% at score ≥60
    - All 14 myxedema coma patients scored ≥60
    - 6 of 7 non-myxedema coma patients scored 25-50
    
    Clinical Applications:
    
    Emergency Department:
    - Early recognition in patients with altered consciousness
    - Risk stratification for patients with hypothermia
    - Decision support for empirical thyroid hormone therapy
    
    Intensive Care Unit:
    - Monitoring patients at risk for progression
    - Guiding treatment intensity and monitoring frequency
    - Prognostic assessment for family discussions
    
    Limitations and Considerations:
    
    - Requires clinical assessment of multiple organ systems
    - Some parameters may be subjective (CNS assessment)
    - Should be used in conjunction with clinical judgment
    - Laboratory confirmation (TSH, free T4) still important when possible
    - Does not replace the need for comprehensive medical evaluation
    
    References (Vancouver style):
    1. Popoveniuc G, Chandra T, Sud A, Sharma M, Blackman MR, Burman KD, et al. 
    A diagnostic scoring system for myxedema coma. Endocr Pract. 2014;20(8):808-17. 
    doi: 10.4158/EP13460.OR.
    2. Mathew V, Misgar RA, Ghosh S, Mukhopadhyay P, Roychowdhury P, Pandit K, et al. 
    Myxedema coma: a new look into an old crisis. J Thyroid Res. 2011;2011:493462. 
    doi: 10.4061/2011/493462.
    3. Wall CR. Myxedema coma: diagnosis and treatment. Am Fam Physician. 2000;62(11):2485-90.
    """
    
    body_temperature: Literal[
        "normal_37", 
        "mild_hypothermia_35_37", 
        "moderate_hypothermia_32_35", 
        "severe_hypothermia_below_32"
    ] = Field(
        ...,
        description="Core body temperature category reflecting thermoregulatory dysfunction. Normal ≥37°C (0 pts), mild hypothermia 35-37°C (10 pts), moderate hypothermia 32-35°C (15 pts), severe hypothermia <32°C (20 pts)",
        example="moderate_hypothermia_32_35"
    )
    
    central_nervous_system: Literal[
        "normal", 
        "mild_lethargy", 
        "moderate_somnolence", 
        "stupor_semicoma", 
        "coma"
    ] = Field(
        ...,
        description="Central nervous system manifestations reflecting cerebral metabolism depression. Normal (0 pts), mild lethargy/decreased concentration (10 pts), moderate somnolence/disorientation (20 pts), stupor/semicoma (25 pts), coma (30 pts)",
        example="moderate_somnolence"
    )
    
    cardiovascular_dysfunction: Literal[
        "normal", 
        "mild_bradycardia", 
        "moderate_bradycardia_hypotension", 
        "severe_shock"
    ] = Field(
        ...,
        description="Cardiovascular manifestations including heart rate and blood pressure abnormalities. Normal (0 pts), mild bradycardia HR 60-70 (5 pts), moderate bradycardia HR <60 or hypotension (10 pts), severe shock/cardiac arrest (15 pts)",
        example="moderate_bradycardia_hypotension"
    )
    
    gastrointestinal_dysfunction: Literal[
        "normal", 
        "mild_constipation", 
        "moderate_distension", 
        "severe_ileus"
    ] = Field(
        ...,
        description="Gastrointestinal motility dysfunction manifestations. Normal function (0 pts), mild constipation (5 pts), moderate abdominal distension/decreased bowel sounds (10 pts), severe ileus/absent bowel sounds (15 pts)",
        example="mild_constipation"
    )
    
    metabolic_dysfunction: Literal[
        "normal", 
        "mild_hyponatremia", 
        "moderate_hyponatremia", 
        "severe_hyponatremia_hypoglycemia"
    ] = Field(
        ...,
        description="Metabolic abnormalities including electrolyte disturbances. Normal parameters (0 pts), mild hyponatremia Na+ 130-135 mEq/L (5 pts), moderate hyponatremia Na+ 120-129 mEq/L (10 pts), severe hyponatremia Na+ <120 mEq/L or hypoglycemia (15 pts)",
        example="moderate_hyponatremia"
    )
    
    precipitating_event: Literal[
        "none", 
        "minor_stress", 
        "moderate_stress", 
        "major_stress"
    ] = Field(
        ...,
        description="Presence and severity of precipitating events that may trigger myxedema coma. None identified (0 pts), minor stress like medication changes/mild illness (5 pts), moderate stress like infection/surgery (10 pts), major stress like severe infection/major surgery/trauma (15 pts)",
        example="moderate_stress"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "body_temperature": "moderate_hypothermia_32_35",
                "central_nervous_system": "moderate_somnolence",
                "cardiovascular_dysfunction": "moderate_bradycardia_hypotension",
                "gastrointestinal_dysfunction": "mild_constipation",
                "metabolic_dysfunction": "moderate_hyponatremia",
                "precipitating_event": "moderate_stress"
            }
        }


class MyxedemaComatDiagnosticScoreResponse(BaseModel):
    """
    Response model for Myxedema Coma Diagnostic Score
    
    The Myxedema Coma Diagnostic Score provides critical diagnostic guidance for 
    one of the most life-threatening endocrine emergencies, enabling rapid 
    recognition and immediate life-saving intervention.
    
    Score Interpretation and Clinical Management:
    
    Unlikely (<25 points) - Alternative Diagnoses:
    - Myxedema coma diagnosis unlikely though severe hypothyroidism may still be present
    - Comprehensive evaluation for alternative causes of altered consciousness
    - Consider sepsis, drug intoxication, metabolic disorders, stroke, or psychiatric conditions
    - Obtain thyroid function tests (TSH, free T4) to assess thyroid status
    - Continue supportive care and monitor for clinical changes
    - Reassess scoring if new symptoms develop or condition deteriorates
    
    Possible (25-44 points) - Low Probability Monitoring:
    - Low probability of myxedema coma but cannot be completely excluded
    - Continue evaluation for other causes while considering thyroid dysfunction
    - Urgent thyroid function assessment (TSH, free T4, free T3) recommended
    - Monitor closely for clinical deterioration or development of additional symptoms
    - Provide supportive care and address any identified precipitating factors
    - Consider endocrinology consultation if thyroid dysfunction confirmed
    
    At Risk (45-59 points) - High Vigilance Required:
    - Intermediate probability with significant risk for myxedema coma
    - Patient at substantial risk requiring urgent intervention and close monitoring
    - Immediate thyroid function testing and intensive care consultation
    - Consider empirical thyroid hormone therapy if severe hypothyroidism suspected
    - Aggressive treatment of precipitating factors and intensive supportive care
    - Prepare for potential rapid progression to full myxedema coma
    - Continuous monitoring in intensive care unit strongly recommended
    
    Diagnostic (≥60 points) - Emergency Intervention Required:
    - High probability, potentially diagnostic for myxedema coma
    - Immediate emergency treatment without delay for laboratory confirmation
    - Life-threatening condition requiring immediate intensive care management
    - 100% sensitivity and 85.71% specificity at this threshold
    
    Emergency Treatment Protocol for Score ≥60:
    
    Immediate Thyroid Hormone Replacement:
    - IV levothyroxine (T4): 200-400 mcg bolus, then 50-100 mcg daily
    - IV liothyronine (T3): 10-20 mcg every 8 hours if available and severe presentation
    - Avoid oral medications due to potential GI absorption issues
    - Monitor for cardiac arrhythmias and adjust dosing in elderly or cardiac patients
    
    Corticosteroid Support:
    - Stress-dose hydrocortisone: 100-300 mg every 8 hours IV
    - Essential due to potential concurrent adrenal insufficiency
    - Continue until hemodynamic stability achieved
    - Consider mineralocorticoid support if severe hypotension
    
    Intensive Care Management:
    - Hemodynamic monitoring with potential vasopressor support
    - Mechanical ventilation for respiratory failure or severe CNS depression
    - Continuous cardiac monitoring for arrhythmias and conduction abnormalities
    - Central venous access for medication administration and monitoring
    
    Supportive Care Interventions:
    - Passive rewarming for hypothermia (avoid active rewarming which may cause shock)
    - Careful fluid management to avoid precipitating heart failure
    - Electrolyte correction (hyponatremia, hypoglycemia, hypercarbia)
    - Infection surveillance and aggressive antimicrobial therapy as indicated
    
    Precipitating Factor Management:
    - Aggressive treatment of underlying infections
    - Discontinuation of sedating medications when possible
    - Correction of hypoxia, hypercarbia, and acid-base disturbances
    - Management of concurrent medical conditions (MI, stroke, trauma)
    
    Monitoring and Complications:
    
    Critical Monitoring Parameters:
    - Continuous cardiac monitoring for arrhythmias and QT prolongation
    - Frequent neurological assessments for improvement in consciousness
    - Core temperature monitoring and gradual rewarming
    - Arterial blood gas monitoring for ventilation adequacy
    - Electrolyte monitoring and correction (especially sodium)
    
    Potential Complications:
    - Cardiac arrhythmias from rapid thyroid hormone replacement
    - Precipitating myocardial infarction in patients with coronary disease
    - Cerebral edema and increased intracranial pressure
    - Aspiration pneumonia from decreased consciousness
    - Gastrointestinal bleeding from stress and anticoagulation
    
    Treatment Response and Prognosis:
    
    Expected Improvement Timeline:
    - Cardiovascular improvement: 24-48 hours
    - Neurological improvement: 48-72 hours
    - Temperature normalization: 24-72 hours
    - Full recovery: days to weeks depending on severity
    
    Prognostic Factors:
    - Age (elderly patients have higher mortality)
    - Severity of hypothermia and CNS depression
    - Presence of complications (pneumonia, MI, GI bleeding)
    - Time to treatment initiation
    - Adequacy of supportive care
    
    Poor Prognostic Indicators:
    - Core temperature <32°C
    - Coma or severe CNS depression
    - Cardiovascular collapse requiring vasopressors
    - Advanced age with multiple comorbidities
    - Delayed recognition and treatment
    
    Prevention and Follow-up:
    
    Preventive Measures:
    - Patient education about thyroid medication compliance
    - Regular monitoring of thyroid function in hypothyroid patients
    - Awareness of risk factors and precipitating events
    - Prompt treatment of infections and other stressors
    - Adjustment of thyroid replacement during illness
    
    Post-Recovery Management:
    - Gradual optimization of thyroid hormone replacement
    - Investigation of underlying cause of hypothyroidism
    - Patient and family education about medication compliance
    - Regular endocrinology follow-up
    - Medical alert identification for emergency situations
    
    Reference: Popoveniuc G, et al. Endocr Pract. 2014;20(8):808-17.
    """
    
    result: int = Field(
        ...,
        description="Total myxedema coma diagnostic score (range 0-100 points)",
        example=65
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Detailed clinical interpretation with diagnostic probability assessment and comprehensive emergency management recommendations",
        example="HIGHLY SUGGESTIVE OF MYXEDEMA COMA (Score: 65): High probability - potentially diagnostic for myxedema coma. IMMEDIATE TREATMENT: Emergency intervention required. Administer IV levothyroxine (200-400 mcg bolus, then 50-100 mcg daily) and IV liothyronine (T3) if available. SUPPORTIVE CARE: Intensive care monitoring, mechanical ventilation if needed, vasopressor support for shock, passive rewarming for hypothermia. MANAGEMENT: Treat precipitating factors, provide stress-dose corticosteroids (hydrocortisone 100-300 mg every 8 hours), correct electrolyte abnormalities. PROGNOSIS: High mortality risk requiring immediate aggressive treatment."
    )
    
    stage: str = Field(
        ...,
        description="Diagnostic probability category",
        example="Diagnostic"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the diagnostic likelihood",
        example="Highly suggestive of myxedema coma"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 65,
                "unit": "points",
                "interpretation": "HIGHLY SUGGESTIVE OF MYXEDEMA COMA (Score: 65): High probability - potentially diagnostic for myxedema coma. IMMEDIATE TREATMENT: Emergency intervention required. Administer IV levothyroxine (200-400 mcg bolus, then 50-100 mcg daily) and IV liothyronine (T3) if available. SUPPORTIVE CARE: Intensive care monitoring, mechanical ventilation if needed, vasopressor support for shock, passive rewarming for hypothermia. MANAGEMENT: Treat precipitating factors, provide stress-dose corticosteroids (hydrocortisone 100-300 mg every 8 hours), correct electrolyte abnormalities. PROGNOSIS: High mortality risk requiring immediate aggressive treatment.",
                "stage": "Diagnostic",
                "stage_description": "Highly suggestive of myxedema coma"
            }
        }