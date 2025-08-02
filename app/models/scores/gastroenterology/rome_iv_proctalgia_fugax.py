"""
Rome IV Diagnostic Criteria for Proctalgia Fugax Models

Request and response models for Rome IV proctalgia fugax diagnostic assessment.

References (Vancouver style):
1. Lacy BE, Mearin F, Chang L, Chey WD, Lembo AJ, Simren M, Spiller R. Bowel Disorders. 
   Gastroenterology. 2016 May;150(6):1393-1407.e5. doi: 10.1053/j.gastro.2016.02.031.
2. Rome Foundation. Rome IV Diagnostic Criteria for Functional Gastrointestinal Disorders. 
   4th ed. Raleigh, NC: Rome Foundation; 2016.
3. Bharucha AE, Wald A, Enck P, Rao S. Functional anorectal disorders. Gastroenterology. 
   2006 Apr;130(5):1510-8. doi: 10.1053/j.gastro.2005.11.064.
4. Chiarioni G, Asteria C, Whitehead WE. Chronic proctalgia and chronic pelvic pain 
   syndromes: new etiologic insights and treatment options. World J Gastroenterol. 
   2011 Oct 21;17(39):4447-55. doi: 10.3748/wjg.v17.i39.4447.

The Rome IV diagnostic criteria for proctalgia fugax represent the international 
standard for diagnosing this functional anorectal pain disorder. Proctalgia fugax 
is characterized by sudden, severe, episodic rectal pain that is unrelated to 
defecation and lasts from seconds to 30 minutes with complete pain-free intervals 
between episodes.

Clinical Background and Significance:
Proctalgia fugax is a benign functional disorder affecting approximately 6-18% of 
adults, with higher prevalence in women. The condition is characterized by sudden 
onset of severe anorectal pain that can be intense enough to awaken patients from 
sleep or interrupt normal activities. The pathophysiology remains poorly understood 
but may involve muscle spasm of the levator ani muscle, rectal smooth muscle, or 
anal sphincter complex.

Rome IV Updates from Rome III:
- Maximum episode duration extended from 20 to 30 minutes based on clinical evidence
- Pain location specifically defined as "rectum" rather than "lower rectum or anus"
- Elimination of "chronic proctalgia" as a separate diagnostic category
- Enhanced emphasis on exclusion of organic causes

Diagnostic Criteria Requirements:
ALL of the following must be present for diagnosis:

1. Recurrent Episodes of Rectal Pain:
   - Pain specifically localized to the rectum
   - Episodes completely unrelated to defecation
   - Pain often described as sudden, severe, cramping, or stabbing
   - May be precipitated by stress, anxiety, or sexual activity

2. Specific Episode Duration:
   - Episodes last from seconds to minutes
   - Maximum duration must not exceed 30 minutes
   - Most episodes are brief, lasting only seconds to a few minutes
   - Duration is a key differentiating feature from other anorectal pain syndromes

3. Pain-Free Intervals:
   - Complete absence of anorectal pain between episodes
   - Patients are entirely asymptomatic between attacks
   - Distinguishes from chronic pain conditions like levator ani syndrome

4. Exclusion of Organic Causes:
   - Inflammatory bowel disease (Crohn's disease, ulcerative colitis)
   - Structural anorectal lesions (intramuscular abscess, anal fissure, thrombosed hemorrhoids)
   - Prostatitis in male patients
   - Coccygodynia (tailbone pain)
   - Major structural alterations of the pelvic floor

Clinical Assessment and Differential Diagnosis:
The diagnosis of proctalgia fugax is primarily clinical and requires systematic 
exclusion of organic pathology. Physical examination should include digital rectal 
examination to assess for structural abnormalities and evaluate the levator ani 
muscle. Additional investigations may include colonoscopy, pelvic imaging, or 
specialized anorectal physiology studies based on clinical presentation.

Differential diagnoses include:
- Levator ani syndrome: chronic pain with puborectalis muscle tenderness on examination
- Unspecified functional anorectal pain: episodes lasting longer than 30 minutes
- Organic causes: inflammatory, infectious, or structural anorectal pathology

Treatment and Management:
Treatment is primarily supportive and symptomatic:
- Patient education and reassurance about the benign nature of the condition
- Stress management and relaxation techniques
- Identification and avoidance of potential triggers
- Symptomatic relief during acute episodes (warm baths, topical agents)
- Rarely, muscle relaxants or calcium channel blockers for frequent episodes

Prognosis and Clinical Course:
Proctalgia fugax typically has an excellent prognosis with episodes occurring 
infrequently (often less than 5 times per year). While episodes can be intensely 
painful, they are self-limiting and do not lead to complications or long-term 
disability. The condition may improve spontaneously over time or with stress 
reduction measures.

Quality of Life Considerations:
Although episodes are brief and infrequent, the unpredictable nature and intensity 
of pain can cause anxiety and concern for patients. Proper diagnosis and education 
about the benign nature of the condition are essential for patient reassurance and 
optimal management outcomes.
"""

from pydantic import BaseModel, Field
from typing import Literal


class RomeIvProctalgieFugaxRequest(BaseModel):
    """
    Request model for Rome IV Diagnostic Criteria for Proctalgia Fugax
    
    The Rome IV criteria provide the international standard for diagnosing proctalgia 
    fugax, a functional anorectal pain disorder characterized by sudden, severe, 
    episodic rectal pain. All criteria must be fulfilled for a positive diagnosis.
    
    Clinical Assessment Guidelines:
    
    Pain Characteristics:
    - Sudden onset of severe rectal pain unrelated to bowel movements
    - Pain often described as cramping, stabbing, or spasm-like
    - Intensity can be severe enough to awaken patients from sleep
    - Episodes are unpredictable and may be triggered by stress or anxiety
    
    Episode Pattern:
    - Brief duration (seconds to minutes, maximum 30 minutes)
    - Complete pain-free intervals between episodes
    - Frequency typically low (<5 episodes per year in most patients)
    - Episodes are self-limiting without intervention
    
    Exclusion of Organic Causes:
    - Thorough history and physical examination required
    - Digital rectal examination to assess for structural abnormalities
    - Consider colonoscopy if inflammatory bowel disease suspected
    - Evaluate for prostatitis in male patients with appropriate symptoms
    - Assess for coccygodynia with focused musculoskeletal examination
    
    Differential Diagnosis Considerations:
    - Levator ani syndrome: chronic pain with puborectalis muscle tenderness
    - Unspecified functional anorectal pain: episodes >30 minutes duration
    - Organic anorectal pathology: fissures, abscesses, thrombosed hemorrhoids
    - Inflammatory conditions: Crohn's disease, ulcerative colitis
    - Urologic conditions: prostatitis, urethritis
    
    Treatment Planning:
    - Patient education about benign nature of condition
    - Stress management and relaxation techniques
    - Trigger identification and avoidance
    - Symptomatic relief measures for acute episodes
    - Reassurance and psychological support
    
    References: See module docstring for complete citation list.
    """
    
    recurrent_rectal_pain_unrelated_defecation: Literal["yes", "no"] = Field(
        ...,
        description="Recurrent episodes of pain localized to the rectum and unrelated to defecation. Pain occurs independently of bowel movements and is specifically felt in the rectal area.",
        example="yes"
    )
    
    episode_duration_seconds_to_30_minutes: Literal["yes", "no"] = Field(
        ...,
        description="Episodes lasting from seconds to minutes, with a maximum duration of 30 minutes. Duration is a key diagnostic criterion - episodes lasting longer than 30 minutes suggest alternative diagnoses.",
        example="yes"
    )
    
    no_anorectal_pain_between_episodes: Literal["yes", "no"] = Field(
        ...,
        description="No anorectal pain between episodes (complete pain-free intervals). Patients are entirely asymptomatic between discrete episodes, distinguishing proctalgia fugax from chronic pain conditions.",
        example="yes"
    )
    
    exclusion_inflammatory_causes: Literal["yes", "no"] = Field(
        ...,
        description="Exclusion of inflammatory bowel disease as cause of rectal pain. Crohn's disease and ulcerative colitis must be ruled out through appropriate clinical evaluation and testing.",
        example="yes"
    )
    
    exclusion_structural_anorectal_lesions: Literal["yes", "no"] = Field(
        ...,
        description="Exclusion of structural anorectal lesions (intramuscular abscess, anal fissure, thrombosed hemorrhoids). Physical examination and appropriate imaging should rule out these organic causes.",
        example="yes"
    )
    
    exclusion_prostatitis: Literal["yes", "no"] = Field(
        ...,
        description="Exclusion of prostatitis as cause of rectal pain. In male patients, prostate examination and appropriate urologic evaluation should exclude prostatitis as the pain source.",
        example="yes"
    )
    
    exclusion_coccygodynia: Literal["yes", "no"] = Field(
        ...,
        description="Exclusion of coccygodynia (tailbone pain) as cause of symptoms. Musculoskeletal examination should differentiate coccygeal pain from true rectal pain.",
        example="yes"
    )
    
    exclusion_pelvic_floor_alterations: Literal["yes", "no"] = Field(
        ...,
        description="Exclusion of major structural alterations of the pelvic floor. Pelvic examination and appropriate imaging should rule out significant pelvic floor dysfunction or structural abnormalities.",
        example="yes"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "recurrent_rectal_pain_unrelated_defecation": "yes",
                "episode_duration_seconds_to_30_minutes": "yes",
                "no_anorectal_pain_between_episodes": "yes",
                "exclusion_inflammatory_causes": "yes",
                "exclusion_structural_anorectal_lesions": "yes",
                "exclusion_prostatitis": "yes",
                "exclusion_coccygodynia": "yes",
                "exclusion_pelvic_floor_alterations": "yes"
            }
        }


class RomeIvProctalgieFugaxResponse(BaseModel):
    """
    Response model for Rome IV Diagnostic Criteria for Proctalgia Fugax
    
    The Rome IV diagnostic assessment provides evidence-based criteria for proctalgia 
    fugax diagnosis and guides appropriate clinical management. Understanding the 
    diagnostic outcome is essential for patient care, treatment planning, and prognosis.
    
    Diagnostic Interpretations and Clinical Management:
    
    Criteria Met (Positive Diagnosis):
    - All 8 Rome IV criteria fulfilled
    - Diagnosis of proctalgia fugax established
    - Condition is benign functional disorder with excellent prognosis
    - Treatment focuses on patient education, reassurance, and symptomatic management
    - Episodes typically occur <5 times per year with spontaneous resolution
    
    Clinical Management for Positive Diagnosis:
    - Patient education about benign nature and excellent prognosis
    - Reassurance that condition does not indicate serious underlying pathology
    - Stress management techniques and relaxation training
    - Identification and avoidance of potential triggers (stress, anxiety, sexual activity)
    - Symptomatic relief measures: warm baths, topical analgesics, muscle relaxants
    - Follow-up as needed for symptom monitoring and patient support
    
    Criteria Not Met (Negative Diagnosis):
    - One or more Rome IV criteria not fulfilled
    - Alternative diagnoses should be considered
    - Further evaluation may be needed to identify underlying pathology
    - Systematic approach to differential diagnosis required
    
    Alternative Diagnoses to Consider:
    
    Functional Anorectal Pain Syndromes:
    - Levator ani syndrome: chronic pain with puborectalis muscle tenderness on digital examination
    - Unspecified functional anorectal pain: episodes lasting longer than 30 minutes
    - Chronic proctalgia: persistent or recurrent pain without specific pattern
    
    Organic Anorectal Conditions:
    - Anal fissure: visible tear in anal canal with pain during defecation
    - Thrombosed hemorrhoids: acute onset, visible/palpable thrombosed hemorrhoid
    - Anorectal abscess: signs of infection, fluctuant mass, systemic symptoms
    - Proctitis: inflammatory changes on examination or imaging
    
    Systemic Conditions:
    - Inflammatory bowel disease: associated GI symptoms, endoscopic findings
    - Infectious proctitis: appropriate cultures and serology
    - Neoplastic conditions: age-appropriate screening and evaluation
    
    Musculoskeletal Conditions:
    - Coccygodynia: tailbone tenderness on palpation
    - Pelvic floor dysfunction: abnormal muscle tone or coordination
    - Piriformis syndrome: deep pelvic pain with specific trigger points
    
    Urologic Conditions (in males):
    - Prostatitis: prostate tenderness, urinary symptoms, appropriate cultures
    - Chronic pelvic pain syndrome: complex pain pattern with urologic involvement
    
    Further Evaluation Recommendations:
    - Complete history focusing on pain characteristics, triggers, associated symptoms
    - Thorough physical examination including digital rectal examination
    - Colonoscopy if inflammatory bowel disease suspected
    - Pelvic imaging (MRI) if structural abnormalities suspected
    - Anorectal physiology studies for complex functional disorders
    - Urologic evaluation for male patients with appropriate symptoms
    
    Follow-up and Monitoring:
    - Regular assessment of symptom pattern and functional impact
    - Reassessment of diagnostic criteria if clinical presentation changes
    - Psychological support for patients with significant anxiety or functional impairment
    - Referral to gastroenterology or colorectal surgery for complex cases
    
    Patient Education and Counseling:
    - Explanation of functional nature of disorder when diagnosed
    - Discussion of triggers and lifestyle modifications
    - Realistic expectations about episode frequency and management
    - Instructions for when to seek medical attention
    - Support for anxiety management and stress reduction
    
    Quality of Life Considerations:
    - Assessment of functional impact on daily activities
    - Evaluation of psychological distress related to unpredictable episodes
    - Support for coping strategies and adaptive behaviors
    - Consideration of psychological consultation for severe anxiety or depression
    
    The Rome IV criteria enable standardized, evidence-based diagnosis of proctalgia 
    fugax, facilitating appropriate management and optimal patient outcomes through 
    systematic evaluation and targeted therapeutic interventions.
    
    Reference: See module docstring for complete citation list.
    """
    
    result: str = Field(
        ...,
        description="Rome IV diagnostic assessment result for proctalgia fugax (Criteria Met or Criteria Not Met)",
        example="Criteria Met"
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the diagnostic assessment",
        example="diagnosis"
    )
    
    interpretation: str = Field(
        ...,
        description="Comprehensive clinical interpretation including diagnostic assessment, treatment recommendations, differential diagnosis considerations, and management guidance based on Rome IV criteria fulfillment.",
        example="Patient fulfills Rome IV diagnostic criteria for proctalgia fugax. Diagnosis is established when all essential criteria are met, including recurrent episodes of rectal pain lasting seconds to 30 minutes, pain-free intervals between episodes, and exclusion of organic causes. Treatment focuses on reassurance, patient education about the benign nature of the condition, stress management techniques, and symptomatic relief during acute episodes."
    )
    
    stage: str = Field(
        ...,
        description="Rome IV diagnostic category (Criteria Met or Criteria Not Met)",
        example="Criteria Met"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the diagnostic assessment outcome",
        example="Meets Rome IV criteria"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": "Criteria Met",
                "unit": "diagnosis",
                "interpretation": "Patient fulfills Rome IV diagnostic criteria for proctalgia fugax. Diagnosis is established when all essential criteria are met, including recurrent episodes of rectal pain lasting seconds to 30 minutes, pain-free intervals between episodes, and exclusion of organic causes. Treatment focuses on reassurance, patient education about the benign nature of the condition, stress management techniques, and symptomatic relief during acute episodes.",
                "stage": "Criteria Met",
                "stage_description": "Meets Rome IV criteria"
            }
        }