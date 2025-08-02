"""
Jones Criteria for Acute Rheumatic Fever Diagnosis Models

Request and response models for Jones criteria calculation.

References (Vancouver style):
1. Gewitz MH, Baltimore RS, Tani LY, Sable CA, Shulman ST, Carapetis J, et al. 
   Revision of the Jones Criteria for the diagnosis of acute rheumatic fever in 
   the era of Doppler echocardiography: a scientific statement from the American 
   Heart Association. Circulation. 2015;131(20):1806-18.
2. WHO Expert Consultation on Rheumatic Fever and Rheumatic Heart Disease. 
   WHO technical report series; no. 923. Geneva: World Health Organization; 2004.
3. Carapetis JR, Beaton A, Cunningham MW, Guilherme L, Karthikeyan G, Mayosi BM, 
   et al. Acute rheumatic fever and rheumatic heart disease. Nat Rev Dis Primers. 
   2016;2:15084.
4. Centers for Disease Control and Prevention. Diagnosing Acute Rheumatic Fever. 
   Group A Strep Clinical Guidance. Available at: https://www.cdc.gov/group-a-strep/
   hcp/clinical-guidance/diagnosing-acute-rheumatic-fever.html

The Jones Criteria are the gold standard for diagnosing acute rheumatic fever (ARF), 
a delayed autoimmune sequela of group A streptococcal pharyngitis. The 2015 revision 
introduced population risk stratification and updated criteria to improve diagnostic 
accuracy while accounting for global variations in disease presentation and prevalence.
"""

from pydantic import BaseModel, Field
from typing import Literal


class JonesCriteriaAcuteRheumaticFeverRequest(BaseModel):
    """
    Request model for Jones Criteria for Acute Rheumatic Fever Diagnosis
    
    The Jones Criteria require evidence of antecedent group A streptococcal infection 
    plus either 2 major criteria OR 1 major + 2 minor criteria for diagnosis.
    
    Population Risk Stratification (2015 Revision):
    
    Low-Risk Population:
    - Acute RF incidence <2 per 100,000 school-age children
    - Rheumatic heart disease prevalence ≤1 per 1000 population per year
    - Includes most developed countries
    
    Moderate-High Risk Population:
    - Acute RF incidence ≥2 per 100,000 school-age children
    - Rheumatic heart disease prevalence >1 per 1000 population per year
    - Includes developing countries, indigenous populations, overcrowded settings
    
    Major Criteria (5 total):
    
    1. Carditis: Clinical and/or subclinical inflammation of the heart
       - Clinical: new murmur, cardiomegaly, CHF, pericarditis
       - Subclinical: echocardiographic evidence of valvulitis
       - Most common and serious manifestation
    
    2. Arthritis: Joint inflammation
       - Low-risk: Polyarthritis (≥2 joints) required
       - Moderate-high risk: Monoarthritis or polyarthralgia acceptable
       - Large joints typically affected (knees, ankles, elbows, wrists)
       - Migratory pattern characteristic but not required
    
    3. Chorea: Sydenham's chorea (involuntary, irregular movements)
       - Late manifestation (2-6 months post-strep infection)
       - Affects hands, feet, face; emotional lability common
       - May be sole manifestation (chorea minor)
    
    4. Erythema Marginatum: Characteristic skin rash
       - Pink rings with clear centers and wavy margins
       - Non-pruritic, appears on trunk/limbs, spares face
       - Rare but pathognomonic when present
    
    5. Subcutaneous Nodules: Small, painless nodules
       - Over bony surfaces or tendons (elbows, knuckles, knees)
       - Usually associated with severe carditis
       - Rare in developed countries
    
    Minor Criteria (varies by population risk):
    
    Universal Minor Criteria:
    - Fever: ≥38°C (moderate-high risk), ≥38.5°C (low-risk)
    - Elevated acute phase reactants: ESR >60 mm/h or CRP >3.0 mg/dL
    - Prolonged PR interval: Age-adjusted, unless carditis present
    - Previous RF/RHD: History of prior rheumatic fever or heart disease
    
    Population-Specific Minor Criteria:
    - Arthralgia: Only minor criterion in LOW-RISK populations
    - NOT a minor criterion in moderate-high risk populations
    
    Evidence of Antecedent Streptococcal Infection (Required):
    - Elevated or rising ASO (antistreptolysin O) titers
    - Elevated anti-DNase B antibodies
    - Positive throat culture for group A strep
    - Recent scarlet fever
    - Rapid antigen detection test (if positive)
    
    Special Considerations:
    - Isolated chorea or insidious carditis may warrant diagnosis without meeting criteria
    - Echocardiography recommended for all suspected cases
    - Recurrent episodes have lower threshold for diagnosis
    
    Clinical Implications:
    - Early diagnosis enables prompt treatment and secondary prevention
    - Primary prevention: Adequate treatment of strep pharyngitis
    - Secondary prevention: Long-term penicillin prophylaxis
    - Cardiac complications are leading cause of morbidity/mortality
    
    References (Vancouver style):
    1. Gewitz MH, Baltimore RS, Tani LY, Sable CA, Shulman ST, Carapetis J, et al. 
       Revision of the Jones Criteria for the diagnosis of acute rheumatic fever in 
       the era of Doppler echocardiography: a scientific statement from the American 
       Heart Association. Circulation. 2015;131(20):1806-18.
    2. Carapetis JR, Beaton A, Cunningham MW, Guilherme L, Karthikeyan G, Mayosi BM, 
       et al. Acute rheumatic fever and rheumatic heart disease. Nat Rev Dis Primers. 
       2016;2:15084.
    """
    
    population_risk: Literal["low_risk", "moderate_high_risk"] = Field(
        ...,
        description="Population risk category. Low-risk: acute RF incidence <2/100,000 school-age children, RHD prevalence ≤1/1000. Moderate-high risk: higher incidence/prevalence, includes developing countries and high-risk populations",
        example="low_risk"
    )
    
    strep_evidence: Literal["yes", "no"] = Field(
        ...,
        description="Evidence of antecedent group A streptococcal infection (REQUIRED for diagnosis). Includes elevated ASO/anti-DNase B titers, positive throat culture, recent scarlet fever, or rapid strep test positive",
        example="yes"
    )
    
    carditis: Literal["yes", "no"] = Field(
        ...,
        description="Carditis (Major Criterion): Clinical and/or subclinical inflammation of the heart. Clinical signs include new murmur, cardiomegaly, CHF, pericarditis. Subclinical detected by echocardiography showing valvulitis",
        example="no"
    )
    
    arthritis: Literal["polyarthritis", "monoarthritis_polyarthralgia", "none"] = Field(
        ...,
        description="Arthritis (Major Criterion): Joint involvement. Low-risk populations require polyarthritis (≥2 joints). Moderate-high risk populations accept monoarthritis or polyarthralgia. Typically affects large joints in migratory pattern",
        example="polyarthritis"
    )
    
    chorea: Literal["yes", "no"] = Field(
        ...,
        description="Chorea (Major Criterion): Sydenham's chorea - involuntary, irregular, purposeless movements affecting primarily hands, feet, and face. Often accompanied by emotional lability. May appear 2-6 months after strep infection",
        example="no"
    )
    
    erythema_marginatum: Literal["yes", "no"] = Field(
        ...,
        description="Erythema Marginatum (Major Criterion): Characteristic non-pruritic skin rash with pink rings having clear centers and wavy, serpiginous margins. Appears on trunk and limbs, spares face. Rare but pathognomonic",
        example="no"
    )
    
    subcutaneous_nodules: Literal["yes", "no"] = Field(
        ...,
        description="Subcutaneous Nodules (Major Criterion): Small, painless, firm nodules over bony surfaces or tendons (elbows, knuckles, knees, spine). Usually associated with severe carditis. Rare in developed countries",
        example="no"
    )
    
    fever: Literal["yes", "no"] = Field(
        ...,
        description="Fever (Minor Criterion): Temperature ≥38°C (100.4°F) for moderate-high risk populations, ≥38.5°C (101.3°F) for low-risk populations. Document peak temperature during illness",
        example="yes"
    )
    
    arthralgia: Literal["yes", "no"] = Field(
        ...,
        description="Arthralgia (Minor Criterion): Joint pain without objective signs of inflammation. ONLY counts as minor criterion in LOW-RISK populations. Not a minor criterion in moderate-high risk populations where it may fulfill major arthritis criterion",
        example="no"
    )
    
    elevated_acute_phase_reactants: Literal["yes", "no"] = Field(
        ...,
        description="Elevated Acute Phase Reactants (Minor Criterion): ESR >60 mm in first hour OR CRP >3.0 mg/dL (30 mg/L). Indicates active inflammation. Should be measured during acute phase of illness",
        example="yes"
    )
    
    prolonged_pr_interval: Literal["yes", "no"] = Field(
        ...,
        description="Prolonged PR Interval (Minor Criterion): First-degree AV block on ECG after accounting for age variability. Does NOT count as minor criterion if carditis is present as major criterion. Age-adjusted normal values required",
        example="no"
    )
    
    previous_rf_rhd: Literal["yes", "no"] = Field(
        ...,
        description="Previous RF/RHD (Minor Criterion): History of previous rheumatic fever or established rheumatic heart disease. Documented by medical records, characteristic murmurs, or echocardiographic findings",
        example="no"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "population_risk": "low_risk",
                "strep_evidence": "yes",
                "carditis": "no",
                "arthritis": "polyarthritis",
                "chorea": "no",
                "erythema_marginatum": "no",
                "subcutaneous_nodules": "no",
                "fever": "yes",
                "arthralgia": "no",
                "elevated_acute_phase_reactants": "yes",
                "prolonged_pr_interval": "no",
                "previous_rf_rhd": "no"
            }
        }


class JonesCriteriaAcuteRheumaticFeverResponse(BaseModel):
    """
    Response model for Jones Criteria for Acute Rheumatic Fever Diagnosis
    
    The Jones Criteria provide a systematic approach to diagnosing acute rheumatic fever,
    helping distinguish it from other post-infectious inflammatory conditions.
    
    Diagnostic Categories:
    
    Acute Rheumatic Fever Diagnosed:
    - Meets revised 2015 Jones criteria
    - Evidence of strep infection + (2 major OR 1 major + 2 minor criteria)
    - Requires immediate anti-inflammatory treatment and penicillin prophylaxis
    - Echocardiography recommended for all confirmed cases
    
    Jones Criteria Not Met:
    - Insufficient criteria for diagnosis
    - Consider alternative diagnoses (viral arthritis, post-infectious arthritis)
    - May warrant monitoring for development of additional criteria
    - Consider isolated manifestations that may not require full criteria
    
    Insufficient Evidence - No Strep Infection:
    - No evidence of antecedent streptococcal infection
    - Cannot diagnose acute rheumatic fever without strep evidence
    - Consider testing for streptococcal antibodies or recent infection
    - Special consideration for isolated chorea or insidious carditis
    
    Clinical Management Implications:
    
    If Diagnosed:
    - Anti-inflammatory therapy (aspirin, corticosteroids for carditis)
    - Eradication of residual strep infection (penicillin)
    - Secondary prevention with long-term penicillin prophylaxis
    - Cardiac monitoring and follow-up
    - Activity restriction if carditis present
    
    If Not Diagnosed:
    - Consider alternative diagnoses
    - Symptom monitoring and reassessment
    - May still warrant empiric treatment in high-risk populations
    - Follow-up for development of additional criteria
    
    Long-term Considerations:
    - Risk of recurrent episodes (higher than initial episode)
    - Progressive cardiac damage with repeated episodes
    - Duration of secondary prophylaxis based on cardiac involvement
    - Regular cardiology follow-up for established RHD
    
    Reference: Gewitz MH, et al. Circulation. 2015;131(20):1806-18.
    """
    
    result: str = Field(
        ...,
        description="Diagnostic conclusion based on Jones criteria assessment",
        example="Acute Rheumatic Fever Diagnosed"
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the assessment",
        example="criteria"
    )
    
    interpretation: str = Field(
        ...,
        description="Detailed clinical interpretation including diagnostic rationale, criteria counts, treatment recommendations, and follow-up guidance",
        example="Patient meets the revised 2015 Jones criteria for acute rheumatic fever diagnosis with 1 major criteria and 2 minor criteria. Requires evidence of streptococcal infection plus either 2 major criteria OR 1 major + 2 minor criteria. Immediate treatment with anti-inflammatory therapy and penicillin prophylaxis is recommended. Consider echocardiography for all patients."
    )
    
    stage: str = Field(
        ...,
        description="Diagnostic stage (Diagnosed, Not Diagnosed, Insufficient Evidence)",
        example="Diagnosed"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the diagnostic conclusion",
        example="Meets Jones criteria for acute rheumatic fever"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": "Acute Rheumatic Fever Diagnosed",
                "unit": "criteria",
                "interpretation": "Patient meets the revised 2015 Jones criteria for acute rheumatic fever diagnosis with 1 major criteria and 2 minor criteria. Requires evidence of streptococcal infection plus either 2 major criteria OR 1 major + 2 minor criteria. Immediate treatment with anti-inflammatory therapy and penicillin prophylaxis is recommended. Consider echocardiography for all patients.",
                "stage": "Diagnosed",
                "stage_description": "Meets Jones criteria for acute rheumatic fever"
            }
        }