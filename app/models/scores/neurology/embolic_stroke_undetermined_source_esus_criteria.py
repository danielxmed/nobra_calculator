"""
Embolic Stroke of Undetermined Source (ESUS) Criteria Models

Request and response models for ESUS diagnostic criteria evaluation.

References (Vancouver style):
1. Hart RG, Diener HC, Coutts SB, Easton JD, Granger CB, O'Donnell MJ, et al. Embolic 
   strokes of undetermined source: the case for a new clinical construct. Lancet Neurol. 
   2014;13(4):429-38. doi: 10.1016/S1474-4422(13)70310-7.
2. Adams HP Jr, Bendixen BH, Kappelle LJ, Biller J, Love BB, Gordon DL, et al. 
   Classification of subtype of acute ischemic stroke. Definitions for use in a multicenter 
   clinical trial. TOAST. Trial of Org 10172 in Acute Stroke Treatment. Stroke. 1993;24(1):35-41.
3. Ntaios G, Papavasileiou V, Milionis H, Makaritsis K, Manios E, Spengos K, et al. Embolic 
   strokes of undetermined source in the Athens stroke registry: an outcome analysis. Stroke. 
   2015;46(8):2087-93. doi: 10.1161/STROKEAHA.115.009334.
4. Perera KS, Vanassche T, Bosch J, Swaminathan B, Mundl H, Giruparajah M, et al. Embolic 
   strokes of undetermined source: prevalence and patient features in the ESUS Global Registry. 
   Int J Stroke. 2016;11(5):526-33. doi: 10.1177/1747493016641967.
5. Diener HC, Bernstein R, Butcher K, Campbell B, Cloud G, Davalos A, et al. Dabigatran for 
   prevention of stroke after embolic stroke of undetermined source. N Engl J Med. 2019;380(20):1906-17. 
   doi: 10.1056/NEJMoa1813959.

The Embolic Stroke of Undetermined Source (ESUS) criteria provide a standardized diagnostic 
framework for identifying patients with likely embolic strokes where the source remains 
undetermined despite comprehensive evaluation. ESUS represents approximately 15-25% of all 
ischemic strokes and is particularly prevalent in younger patients.

This diagnostic construct was developed to replace the less specific term "cryptogenic stroke" 
and to enable more focused clinical research and therapeutic trials. The criteria require 
both the fulfillment of specific clinical conditions and the completion of adequate diagnostic 
evaluation to exclude other stroke etiologies.

The ESUS classification has significant implications for secondary stroke prevention strategies, 
clinical trial enrollment, and targeted investigation of rare embolic sources. It represents 
a subset of strokes that may particularly benefit from anticoagulation therapy and extended 
cardiac monitoring strategies.
"""

from pydantic import BaseModel, Field
from typing import Literal


class EmbolicStrokeUndeterminedSourceEsusCriteriaRequest(BaseModel):
    """
    Request model for Embolic Stroke of Undetermined Source (ESUS) Criteria
    
    ESUS diagnostic criteria require ALL four clinical criteria to be met AND adequate 
    diagnostic evaluation to be completed:
    
    Clinical Criteria (All Must Be Present):
    
    1. Non-lacunar Stroke on Imaging:
    - Yes: Stroke detected by CT or MRI that is NOT lacunar
    - No: Lacunar stroke or no stroke on imaging
    
    Lacunar Definition: Subcortical infarct ≤1.5 cm (≤2.0 cm on MRI diffusion images) 
    in largest dimension, located in the distribution of small penetrating cerebral arteries 
    of the cerebral hemispheres and pons.
    
    2. No Significant Atherosclerosis:
    - Yes: No atherosclerosis causing ≥50% luminal stenosis in arteries supplying ischemic area
    - No: Presence of ≥50% stenosis in extracranial or intracranial arteries
    
    This requires imaging of both extracranial and intracranial arteries supplying the 
    area of brain ischemia. Acceptable imaging methods include catheter angiography, 
    MR/CT angiography, or cervical duplex plus transcranial Doppler ultrasonography.
    
    3. No Major Cardioembolic Source:
    - Yes: No major cardioembolic sources identified after adequate cardiac evaluation
    - No: Presence of major cardioembolic source
    
    Major cardioembolic sources to exclude:
    - Permanent or paroxysmal atrial fibrillation
    - Sustained atrial flutter
    - Intracardiac thrombus
    - Prosthetic cardiac valve
    - Atrial myxoma or other cardiac tumors
    - Mitral stenosis
    - Recent myocardial infarction (<4 weeks)
    - Left ventricular ejection fraction <30%
    - Valvular vegetations
    - Infective endocarditis
    
    4. No Other Specific Stroke Cause:
    - Yes: No other specific etiology identified after comprehensive evaluation
    - No: Specific stroke cause identified
    
    Other specific causes to exclude:
    - Arteritis (infectious, autoimmune, or drug-induced)
    - Arterial dissection
    - Migraine/vasospasm
    - Drug misuse (cocaine, amphetamines)
    - Genetic disorders (CADASIL, Fabry disease, mitochondrial disorders)
    - Hypercoagulable states (when clearly causative)
    - Vasculitis
    - Moyamoya disease
    
    Minimum Required Diagnostic Evaluation:
    
    5. Adequate Cardiac Monitoring:
    - Yes: ≥24 hours of cardiac rhythm monitoring with automated rhythm detection completed
    - No: <24 hours of monitoring or no automated rhythm detection
    
    This is the minimum requirement. Extended monitoring (48-72 hours or longer) 
    may be considered based on clinical judgment and is often recommended to 
    detect paroxysmal atrial fibrillation.
    
    6. Adequate Vascular Imaging:
    - Yes: Comprehensive vascular imaging of extracranial and intracranial circulation completed
    - No: Incomplete or inadequate vascular imaging
    
    Acceptable methods include:
    - Catheter angiography (gold standard)
    - Magnetic resonance angiography (MRA)
    - Computed tomography angiography (CTA)
    - Cervical duplex ultrasonography PLUS transcranial Doppler ultrasonography
    
    7. Adequate Cardiac Imaging:
    - Yes: Appropriate cardiac imaging completed to exclude cardioembolic sources
    - No: Inadequate or incomplete cardiac imaging
    
    Minimum requirement includes transthoracic echocardiography (TTE). 
    Transesophageal echocardiography (TEE) is recommended when TTE is inadequate 
    or when high suspicion for cardioembolic source exists.
    
    Clinical Context and Application:
    
    Patient Population: ESUS typically affects younger patients (mean age 65) with 
    relatively mild strokes (mean NIHSS 5). The annual stroke recurrence rate is 
    approximately 4.5%, similar to cardioembolic stroke.
    
    Clinical Significance: ESUS diagnosis has important implications for:
    - Secondary stroke prevention strategy selection
    - Clinical trial enrollment eligibility
    - Extended diagnostic workup planning
    - Anticoagulation vs antiplatelet therapy decisions
    - Long-term monitoring and follow-up strategies
    
    Temporal Considerations: The diagnostic evaluation should be completed in a 
    timely manner, typically during the acute hospitalization or within the first 
    few weeks after stroke onset. Some evaluations may need to be repeated or 
    extended based on initial findings.

    References (Vancouver style):
    1. Hart RG, Diener HC, Coutts SB, Easton JD, Granger CB, O'Donnell MJ, et al. Embolic 
    strokes of undetermined source: the case for a new clinical construct. Lancet Neurol. 
    2014;13(4):429-38. doi: 10.1016/S1474-4422(13)70310-7.
    2. Adams HP Jr, Bendixen BH, Kappelle LJ, Biller J, Love BB, Gordon DL, et al. 
    Classification of subtype of acute ischemic stroke. Definitions for use in a multicenter 
    clinical trial. TOAST. Trial of Org 10172 in Acute Stroke Treatment. Stroke. 1993;24(1):35-41.
    3. Ntaios G, Papavasileiou V, Milionis H, Makaritsis K, Manios E, Spengos K, et al. Embolic 
    strokes of undetermined source in the Athens stroke registry: an outcome analysis. Stroke. 
    2015;46(8):2087-93. doi: 10.1161/STROKEAHA.115.009334.
    4. Perera KS, Vanassche T, Bosch J, Swaminathan B, Mundl H, Giruparajah M, et al. Embolic 
    strokes of undetermined source: prevalence and patient features in the ESUS Global Registry. 
    Int J Stroke. 2016;11(5):526-33. doi: 10.1177/1747493016641967.
    5. Diener HC, Bernstein R, Butcher K, Campbell B, Cloud G, Davalos A, et al. Dabigatran for 
    prevention of stroke after embolic stroke of undetermined source. N Engl J Med. 2019;380(20):1906-17. 
    doi: 10.1056/NEJMoa1813959.
    """
    
    stroke_type_non_lacunar: Literal["Yes", "No"] = Field(
        ...,
        description="Non-lacunar stroke detected by CT or MRI (lacunar defined as subcortical infarct ≤1.5 cm or ≤2.0 cm on MRI diffusion images)",
        example="Yes"
    )
    
    no_significant_atherosclerosis: Literal["Yes", "No"] = Field(
        ...,
        description="Absence of extracranial or intracranial atherosclerosis causing ≥50% luminal stenosis in arteries supplying the area of ischemia",
        example="Yes"
    )
    
    no_major_cardioembolic_source: Literal["Yes", "No"] = Field(
        ...,
        description="No major cardioembolic sources identified (atrial fibrillation, intracardiac thrombus, prosthetic valve, cardiac tumors, mitral stenosis, recent MI <4 weeks, LVEF <30%, valvular vegetations, infective endocarditis)",
        example="Yes"
    )
    
    no_other_specific_cause: Literal["Yes", "No"] = Field(
        ...,
        description="No other specific cause of stroke identified (arteritis, dissection, migraine/vasospasm, drug misuse, genetic disorders)",
        example="Yes"
    )
    
    adequate_cardiac_monitoring: Literal["Yes", "No"] = Field(
        ...,
        description="Cardiac rhythm monitoring for ≥24 hours with automated rhythm detection completed",
        example="Yes"
    )
    
    adequate_vascular_imaging: Literal["Yes", "No"] = Field(
        ...,
        description="Adequate vascular imaging completed (catheter angiography, MR/CT angiography, or cervical duplex plus transcranial Doppler ultrasonography)",
        example="Yes"
    )
    
    adequate_cardiac_imaging: Literal["Yes", "No"] = Field(
        ...,
        description="Adequate cardiac imaging completed (transthoracic echocardiography and/or transesophageal echocardiography)",
        example="Yes"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "stroke_type_non_lacunar": "Yes",
                "no_significant_atherosclerosis": "Yes",
                "no_major_cardioembolic_source": "Yes",
                "no_other_specific_cause": "Yes",
                "adequate_cardiac_monitoring": "Yes",
                "adequate_vascular_imaging": "Yes",
                "adequate_cardiac_imaging": "Yes"
            }
        }


class EmbolicStrokeUndeterminedSourceEsusCriteriaResponse(BaseModel):
    """
    Response model for Embolic Stroke of Undetermined Source (ESUS) Criteria
    
    The ESUS criteria evaluation results in one of three diagnostic outcomes:
    
    ESUS Diagnosis Confirmed:
    - All four clinical criteria are met
    - Adequate diagnostic evaluation has been completed
    - Patient qualifies for ESUS-specific research and treatment protocols
    - Consider anticoagulation strategies and extended cardiac monitoring
    
    ESUS Diagnosis Not Met:
    - One or more clinical criteria are not fulfilled
    - Adequate diagnostic evaluation completed but specific etiology identified
    - Apply appropriate TOAST classification based on identified etiology
    - Implement etiology-specific secondary prevention strategies
    
    Inadequate Evaluation:
    - Diagnostic evaluation is insufficient to determine ESUS status
    - Complete required minimum diagnostic workup before reassessment
    - Cannot definitively classify stroke subtype without adequate evaluation
    
    Clinical Management Implications:
    
    For ESUS Diagnosis Confirmed:
    - Extended cardiac monitoring (>24-48 hours) recommended
    - Consider evaluation for patent foramen ovale
    - Assess for hypercoagulable states if clinically indicated
    - Discuss anticoagulation vs antiplatelet therapy options
    - Monitor for clinical trial eligibility
    - Plan for structured follow-up and reassessment
    
    Treatment Considerations:
    - Recent trials suggest mixed results for anticoagulation in ESUS
    - Individualized assessment of bleeding vs thrombotic risk
    - Consider patient age, comorbidities, and stroke severity
    - Extended monitoring may reveal paroxysmal atrial fibrillation
    - Genetic testing may be appropriate in young patients
    
    Long-term Management:
    - Annual stroke recurrence rate approximately 4.5%
    - Regular reassessment as new diagnostic technologies emerge
    - Monitoring for development of atrial fibrillation
    - Cardiovascular risk factor optimization
    - Patient education regarding warning signs and symptoms
    
    Research and Clinical Trial Implications:
    - ESUS patients eligible for specific clinical trials
    - Standardized definition enables consistent research participation
    - Emerging therapies specifically target ESUS population
    - Registry participation for long-term outcome tracking
    
    Reference: Hart RG, et al. Lancet Neurol. 2014;13(4):429-38.
    """
    
    result: str = Field(
        ...,
        description="ESUS diagnostic determination (ESUS Diagnosis Confirmed, ESUS Diagnosis Not Met, or Inadequate Evaluation)",
        example="ESUS Diagnosis Confirmed"
    )
    
    unit: None = Field(
        ...,
        description="No unit applicable for diagnostic criteria",
        example=None
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation and management recommendations based on ESUS criteria evaluation",
        example="Patient meets all diagnostic criteria for Embolic Stroke of Undetermined Source (ESUS). This diagnosis applies when all four clinical criteria are satisfied AND adequate diagnostic evaluation has been completed. Consider anticoagulation strategies, extended cardiac monitoring, and targeted embolic source investigation."
    )
    
    stage: str = Field(
        ...,
        description="Diagnostic category (ESUS Diagnosis Confirmed, ESUS Diagnosis Not Met, Inadequate Evaluation)",
        example="ESUS Diagnosis Confirmed"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the diagnostic outcome",
        example="Meets all ESUS criteria"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "result": "ESUS Diagnosis Confirmed",
                "unit": None,
                "interpretation": "Patient meets all diagnostic criteria for Embolic Stroke of Undetermined Source (ESUS). This diagnosis applies when all four clinical criteria are satisfied AND adequate diagnostic evaluation has been completed. Consider anticoagulation strategies, extended cardiac monitoring, and targeted embolic source investigation. Patient may be eligible for ESUS-specific clinical trials and treatment protocols. Recommended next steps: Consider extended cardiac monitoring (>24-48 hours), evaluation for patent foramen ovale, assessment for hypercoagulable states, and discussion of anticoagulation vs antiplatelet therapy. Monitor for clinical trial eligibility and emerging treatment options. Important considerations: ESUS diagnosis requires rigorous exclusion of other stroke etiologies. The classification may change with additional testing or emerging diagnostic techniques. Regular reassessment is recommended as new information becomes available.",
                "stage": "ESUS Diagnosis Confirmed",
                "stage_description": "Meets all ESUS criteria"
            }
        }