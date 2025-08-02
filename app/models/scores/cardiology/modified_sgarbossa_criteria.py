"""
Modified Sgarbossa's Criteria for MI in Left Bundle Branch Block Models

Request and response models for diagnosing acute myocardial infarction in patients with 
prior left bundle branch block using improved ECG criteria.

References (Vancouver style):
1. Smith SW, Dodd KW, Henry TD, Dvorak DM, Pearce LA. Diagnosis of ST-elevation 
   myocardial infarction in the presence of left bundle branch block with the 
   ST-elevation to S-wave ratio in a modified Sgarbossa rule. Ann Emerg Med. 
   2012;60(6):766-76. doi: 10.1016/j.annemergmed.2012.07.119.
2. Sgarbossa EB, Pinski SL, Barbagelata A, Underwood DA, Gates KB, Topol EJ, et al. 
   Electrocardiographic diagnosis of evolving acute myocardial infarction in the 
   presence of left bundle-branch block. GUSTO-1 (Global Utilization of Streptokinase 
   and Tissue Plasminogen Activator for Occluded Coronary Arteries) Investigators. 
   N Engl J Med. 1996;334(8):481-7. doi: 10.1056/NEJM199602223340801.
3. Aslanger EK, Yalin K. Electrophysiologic basis, electrocardiographic features, 
   and clinical implications of aVR sign. Ann Noninvasive Electrocardiol. 2015;20(1):12-20. 
   doi: 10.1111/anec.12140.

The Modified Sgarbossa criteria improve upon the original Sgarbossa criteria by replacing 
the third criterion (excessive discordance ≥5 mm) with a proportional measurement 
(ST/S ratio ≥-0.25), significantly improving sensitivity from 36% to 80% while 
maintaining 99% specificity for diagnosing acute MI in patients with LBBB.
"""

from pydantic import BaseModel, Field
from typing import Literal


class ModifiedSgarbossaCriteriaRequest(BaseModel):
    """
    Request model for Modified Sgarbossa's Criteria for MI in Left Bundle Branch Block
    
    The Modified Sgarbossa criteria consist of three ECG findings that help diagnose 
    acute myocardial infarction in patients with pre-existing left bundle branch block:
    
    **Clinical Background:**
    
    **Challenge of MI Diagnosis in LBBB:**
    - Left bundle branch block masks the typical ECG changes of acute myocardial infarction
    - ST elevation and Q waves are difficult to interpret in the presence of LBBB
    - Traditional STEMI criteria are not reliable when LBBB is present
    - Delays in diagnosis can lead to delayed reperfusion therapy and worse outcomes
    
    **Original Sgarbossa Criteria (1996):**
    - Developed from the GUSTO-I trial with 131 patients with LBBB and MI
    - Three criteria with point values: concordant ST elevation ≥1 mm (5 points), 
      concordant ST depression ≥1 mm in V1-V3 (3 points), excessive discordant 
      ST elevation ≥5 mm (2 points)
    - Score ≥3 points indicated acute MI
    - High specificity (90%) but poor sensitivity (36%)
    
    **Smith Modification (2012):**
    - Key improvement: replaced absolute ST elevation measurement (≥5 mm) with 
      proportional measurement (ST/S ratio ≥-0.25)
    - Dramatically improved sensitivity from 36% to 80%
    - Maintained excellent specificity at 99%
    - Any single positive criterion indicates acute MI
    
    **ECG Criteria Assessment:**
    
    **1. Concordant ST Elevation ≥1 mm:**
    - Definition: ST elevation in same direction as QRS complex
    - Look for: Leads where QRS is predominantly positive (upward deflection)
    - Measurement: ST elevation ≥1 mm above baseline in these leads
    - Clinical significance: Most specific finding for acute MI in LBBB
    - Typical locations: Often seen in lateral leads (I, aVL, V5-V6) in anterior MI
    - Interpretation: When present, strongly suggests acute coronary occlusion
    
    **2. Concordant ST Depression ≥1 mm in V1-V3:**
    - Definition: ST depression in leads V1, V2, or V3 where QRS is predominantly negative
    - Look for: ST segments below baseline by ≥1 mm in precordial leads V1-V3
    - Clinical significance: Indicates posterior wall MI or reciprocal changes
    - Measurement technique: Measure from baseline to ST segment 80 ms after J-point
    - Common finding: Often accompanies inferior or posterior MI
    - Important note: Must be in leads where QRS is predominantly negative (downward)
    
    **3. Discordant ST Elevation with ST/S Ratio ≥-0.25 (Modified Criterion):**
    - Definition: ST elevation opposite to QRS direction with proportional measurement
    - Original criterion: Excessive discordant ST elevation ≥5 mm (poor sensitivity)
    - Modified criterion: ST elevation divided by depth of S wave ≥-0.25
    - Measurement technique: 
      * Measure ST elevation in mm above baseline
      * Measure depth of S wave in mm below baseline
      * Calculate ratio: ST elevation / S wave depth
      * Positive if ratio ≥-0.25 (e.g., 2 mm ST elevation / 10 mm S wave = -0.2, which is ≥-0.25)
    - Clinical significance: Most common positive finding in acute MI with LBBB
    - Rationale: Accounts for different QRS amplitudes between patients
    
    **Clinical Applications:**
    
    **Emergency Department Use:**
    - Apply to patients with chest pain and known or new LBBB
    - Any single positive criterion warrants emergent cardiology consultation
    - Consider immediate cardiac catheterization for positive criteria
    - Useful for triage decisions in acute coronary syndrome protocols
    
    **Diagnostic Performance:**
    - Sensitivity: 80% (significantly improved from original 36%)
    - Specificity: 99% (maintained high specificity)
    - Positive likelihood ratio: 9 (very strong evidence for MI when positive)
    - Negative likelihood ratio: 0.1 (strong evidence against MI when negative)
    - Validated in multiple external cohorts and real-world settings
    
    **Limitations and Considerations:**
    
    **When to Use:**
    - Patients with chest pain or ACS symptoms AND pre-existing LBBB
    - New LBBB in setting of suspected acute MI
    - When standard STEMI criteria cannot be reliably assessed
    - As adjunct to clinical assessment and cardiac biomarkers
    
    **When NOT to Use:**
    - Patients without LBBB (use standard STEMI criteria)
    - Right bundle branch block (different criteria apply)
    - Paced rhythms (requires different approach)
    - When ECG quality is poor or uninterpretable
    
    **Clinical Integration:**
    - Always correlate with clinical presentation and cardiac biomarkers
    - Serial ECGs may be helpful if initial assessment is negative
    - Consider other causes of chest pain if criteria are negative
    - Positive criteria should prompt urgent revascularization consideration
    
    **Recent Developments:**
    - Barcelona algorithm incorporates additional criteria for further improvement
    - Ongoing research into artificial intelligence applications
    - Integration with high-sensitivity troponin assays
    - Application to other bundle branch blocks and conduction abnormalities
    
    References (Vancouver style):
    1. Smith SW, Dodd KW, Henry TD, et al. Diagnosis of ST-elevation myocardial 
       infarction in the presence of left bundle branch block with the ST-elevation 
       to S-wave ratio in a modified Sgarbossa rule. Ann Emerg Med. 2012;60(6):766-76.
    2. Sgarbossa EB, Pinski SL, Barbagelata A, et al. Electrocardiographic diagnosis 
       of evolving acute myocardial infarction in the presence of left bundle-branch 
       block. N Engl J Med. 1996;334(8):481-7.
    """
    
    concordant_st_elevation: Literal["present", "absent"] = Field(
        ...,
        description="Concordant ST elevation ≥1 mm in leads with positive (upward) QRS complex. Look for ST elevation in the same direction as the main QRS deflection. This is the most specific finding for acute MI in LBBB and often seen in lateral leads during anterior MI.",
        example="absent"
    )
    
    concordant_st_depression: Literal["present", "absent"] = Field(
        ...,
        description="Concordant ST depression ≥1 mm in leads V1, V2, or V3 where QRS is predominantly negative (downward). Measure ST segment depression ≥1 mm below baseline in precordial leads V1-V3. This finding suggests posterior wall MI or reciprocal changes.",
        example="absent"
    )
    
    discordant_st_elevation_ratio: Literal["present", "absent"] = Field(
        ...,
        description="Discordant ST elevation with ST/S ratio ≥-0.25 (Modified criterion replacing original ≥5 mm rule). Measure ST elevation opposite to QRS direction, divide by depth of S wave. If ratio ≥-0.25, criterion is positive. This proportional measurement significantly improves sensitivity while maintaining specificity.",
        example="present"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "concordant_st_elevation": "absent",
                "concordant_st_depression": "absent", 
                "discordant_st_elevation_ratio": "present"
            }
        }


class ModifiedSgarbossaCriteriaResponse(BaseModel):
    """
    Response model for Modified Sgarbossa's Criteria for MI in Left Bundle Branch Block
    
    The result indicates whether acute myocardial infarction is present based on ECG criteria 
    specifically designed for patients with left bundle branch block:
    
    **Interpretation Categories:**
    
    **Positive Result (Any criterion met):**
    - Indicates high likelihood of acute ST-elevation myocardial infarction (STEMI)
    - Sensitivity: 80% for detecting acute coronary occlusion
    - Specificity: 99% for ruling out false positives
    - Positive likelihood ratio: 9 (very strong evidence for acute MI)
    - Clinical action: Urgent cardiology consultation and consider emergent cardiac catheterization
    
    **Negative Result (No criteria met):**
    - Significantly reduces likelihood of acute STEMI in LBBB setting
    - Negative likelihood ratio: 0.1 (strong evidence against acute MI)
    - Does not completely rule out myocardial infarction
    - Clinical action: Continue evaluation with cardiac biomarkers and clinical correlation
    
    **Clinical Decision Making:**
    
    **When Positive:**
    - Treat as STEMI equivalent regardless of which specific criterion is positive
    - Activate cardiac catheterization laboratory protocols
    - Consider fibrinolytic therapy if primary PCI not immediately available
    - Monitor for complications of acute MI (arrhythmias, heart failure, mechanical complications)
    - Optimize medical therapy including dual antiplatelet therapy, anticoagulation
    
    **When Negative:**
    - Does not exclude non-STEMI or unstable angina
    - Continue evaluation with serial troponins and clinical assessment
    - Consider stress testing or coronary CT angiography if biomarkers negative
    - Evaluate for other causes of chest pain if MI ruled out
    - Consider serial ECGs if symptoms persist
    
    **Performance Characteristics:**
    
    **Comparison to Original Sgarbossa:**
    - Original criteria: 36% sensitivity, 90% specificity
    - Modified criteria: 80% sensitivity, 99% specificity
    - Key improvement: ST/S ratio criterion replaces absolute ST elevation measurement
    - Clinical impact: Fewer missed acute MIs while maintaining diagnostic accuracy
    
    **Validation Studies:**
    - Externally validated in multiple independent cohorts
    - Consistent performance across different healthcare systems
    - Applicable to both emergency department and inpatient settings
    - Effective in both academic and community hospital environments
    
    **Integration with Other Diagnostic Tools:**
    
    **Cardiac Biomarkers:**
    - Use in conjunction with high-sensitivity troponin assays
    - Positive criteria may predict elevated biomarkers
    - Negative criteria do not exclude troponin elevation
    - Serial biomarker measurement recommended regardless of ECG findings
    
    **Clinical Assessment:**
    - Consider patient's risk factors, symptoms, and hemodynamic status
    - Evaluate for signs of acute heart failure or cardiogenic shock
    - Assess for mechanical complications if acute MI confirmed
    - Monitor for reperfusion arrhythmias after intervention
    
    **Quality Improvement Applications:**
    
    **Door-to-Balloon Time:**
    - Positive criteria should trigger rapid activation protocols
    - May improve time to reperfusion in LBBB patients
    - Useful for quality metrics in STEMI care programs
    - Reduces diagnostic uncertainty in challenging cases
    
    **Education and Training:**
    - Important tool for emergency medicine and cardiology training
    - Useful for ECG interpretation education programs
    - Helps standardize approach to MI diagnosis in LBBB
    - Reduces inter-physician variability in ECG interpretation
    
    Reference: Smith SW, et al. Ann Emerg Med. 2012;60(6):766-76.
    """
    
    result: Literal["Positive", "Negative"] = Field(
        ...,
        description="Overall result of Modified Sgarbossa criteria assessment for acute MI in LBBB",
        example="Positive"
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the result",
        example="interpretation"
    )
    
    interpretation: str = Field(
        ...,
        description="Detailed clinical interpretation with specific criteria met, diagnostic implications, and recommended clinical actions based on Modified Sgarbossa criteria result",
        example="Modified Sgarbossa criteria POSITIVE for acute myocardial infarction in the setting of left bundle branch block. Positive criteria: Discordant ST elevation with ST/S ratio ≥-0.25. This result indicates a high likelihood of acute ST-elevation myocardial infarction (STEMI) despite the presence of LBBB."
    )
    
    stage: str = Field(
        ...,
        description="Diagnostic category based on criteria assessment",
        example="Positive"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the diagnostic result",
        example="At least one criterion met"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": "Positive",
                "unit": "interpretation",
                "interpretation": "Modified Sgarbossa criteria POSITIVE for acute myocardial infarction in the setting of left bundle branch block. Positive criteria: Discordant ST elevation with ST/S ratio ≥-0.25. This result indicates a high likelihood of acute ST-elevation myocardial infarction (STEMI) despite the presence of LBBB. The Modified Sgarbossa criteria have 80% sensitivity and 99% specificity for acute MI in LBBB. Immediate cardiology consultation and emergent cardiac catheterization should be considered.",
                "stage": "Positive",
                "stage_description": "At least one criterion met"
            }
        }