"""
DSM-5 Criteria for Posttraumatic Stress Disorder Models

Request and response models for DSM-5 PTSD diagnostic evaluation.

References (Vancouver style):
1. American Psychiatric Association. Diagnostic and statistical manual of mental disorders: 
   DSM-5. 5th ed. Washington, DC: American Psychiatric Association; 2013.
2. Weathers FW, Litz BT, Keane TM, Palmieri PA, Marx BP, Schnurr PP. The PTSD Checklist 
   for DSM-5 (PCL-5). National Center for PTSD; 2013.
3. Bovin MJ, Marx BP, Weathers FW, Gallagher MW, Rodriguez P, Schnurr PP, Keane TM. 
   Psychometric properties of the PTSD Checklist for Diagnostic and Statistical Manual 
   of Mental Disorders-Fifth Edition (PCL-5) in veterans. Psychol Assess. 2016;28(11):1379-1391. 
   doi: 10.1037/pas0000254.

The DSM-5 criteria for PTSD requires exposure to a traumatic event plus symptoms from four 
clusters: (B) intrusion symptoms, (C) avoidance symptoms, (D) negative alterations in 
cognitions and mood, and (E) alterations in arousal and reactivity. Specific requirements 
include at least 1 symptom from Criterion B, 1 from Criterion C, 2 from Criterion D, and 
2 from Criterion E, with duration >1 month and functional impairment. A dissociative subtype 
is diagnosed when depersonalization or derealization symptoms are also present.
"""

from pydantic import BaseModel, Field
from typing import Literal


class Dsm5PtsdRequest(BaseModel):
    """
    Request model for DSM-5 Criteria for Posttraumatic Stress Disorder
    
    The DSM-5 diagnostic criteria for PTSD requires the following:
    
    Criterion A: Exposure to actual or threatened death, serious injury, or sexual violence 
    in one or more ways: directly experiencing, witnessing, learning it happened to close 
    family/friend, or repeated/extreme exposure to aversive details.
    
    Criterion B (Intrusion - at least 1 required):
    1. Recurrent, involuntary, intrusive distressing memories
    2. Recurrent distressing dreams related to trauma
    3. Dissociative reactions (flashbacks)
    4. Intense psychological distress at trauma cues
    5. Marked physiological reactions to trauma cues
    
    Criterion C (Avoidance - at least 1 required):
    1. Avoidance of distressing memories, thoughts, or feelings
    2. Avoidance of external reminders that arouse distressing memories
    
    Criterion D (Negative Alterations in Cognitions and Mood - at least 2 required):
    1. Inability to remember important aspects of trauma
    2. Persistent negative beliefs about self, others, or world
    3. Persistent distorted cognitions about cause/consequences leading to blame
    4. Persistent negative emotional state (fear, horror, anger, guilt, shame)
    5. Markedly diminished interest or participation in activities
    6. Feelings of detachment or estrangement from others
    7. Persistent inability to experience positive emotions
    
    Criterion E (Alterations in Arousal and Reactivity - at least 2 required):
    1. Irritable behavior and angry outbursts
    2. Reckless or self-destructive behavior
    3. Hypervigilance
    4. Exaggerated startle response
    5. Problems with concentration
    6. Sleep disturbance
    
    Criterion F: Duration >1 month
    Criterion G: Functional impairment
    Criterion H: Not due to substance/medical condition
    
    Dissociative Subtype: Depersonalization or derealization symptoms

    References (Vancouver style):
    1. American Psychiatric Association. Diagnostic and statistical manual of mental disorders: 
       DSM-5. 5th ed. Washington, DC: American Psychiatric Association; 2013.
    2. Weathers FW, Litz BT, Keane TM, Palmieri PA, Marx BP, Schnurr PP. The PTSD Checklist 
       for DSM-5 (PCL-5). National Center for PTSD; 2013.
    3. Bovin MJ, Marx BP, Weathers FW, Gallagher MW, Rodriguez P, Schnurr PP, Keane TM. 
       Psychometric properties of the PTSD Checklist for Diagnostic and Statistical Manual 
       of Mental Disorders-Fifth Edition (PCL-5) in veterans. Psychol Assess. 2016;28(11):1379-1391.
    """
    
    trauma_exposure: Literal["yes", "no"] = Field(
        ...,
        description="CRITERION A: Exposure to actual or threatened death, serious injury, or sexual violence through direct experience, witnessing, learning it happened to close family/friend, or repeated/extreme exposure to aversive details",
        example="yes"
    )
    
    intrusive_memories: Literal["yes", "no"] = Field(
        ...,
        description="CRITERION B1: Recurrent, involuntary, and intrusive distressing memories of the traumatic event(s)",
        example="yes"
    )
    
    traumatic_nightmares: Literal["yes", "no"] = Field(
        ...,
        description="CRITERION B2: Recurrent distressing dreams in which the content and/or affect of the dream are related to the traumatic event(s)",
        example="yes"
    )
    
    dissociative_reactions: Literal["yes", "no"] = Field(
        ...,
        description="CRITERION B3: Dissociative reactions (e.g., flashbacks) in which the individual feels or acts as if the traumatic event(s) were recurring",
        example="no"
    )
    
    psychological_distress: Literal["yes", "no"] = Field(
        ...,
        description="CRITERION B4: Intense or prolonged psychological distress at exposure to internal or external cues that symbolize or resemble an aspect of the traumatic event(s)",
        example="yes"
    )
    
    physiological_reactions: Literal["yes", "no"] = Field(
        ...,
        description="CRITERION B5: Marked physiological reactions to internal or external cues that symbolize or resemble an aspect of the traumatic event(s)",
        example="yes"
    )
    
    avoidance_thoughts: Literal["yes", "no"] = Field(
        ...,
        description="CRITERION C1: Avoidance of or efforts to avoid distressing memories, thoughts, or feelings about or closely associated with the traumatic event(s)",
        example="yes"
    )
    
    avoidance_reminders: Literal["yes", "no"] = Field(
        ...,
        description="CRITERION C2: Avoidance of or efforts to avoid external reminders (people, places, conversations, activities, objects, situations) that arouse distressing memories, thoughts, or feelings about or closely associated with the traumatic event(s)",
        example="no"
    )
    
    inability_remember: Literal["yes", "no"] = Field(
        ...,
        description="CRITERION D1: Inability to remember an important aspect of the traumatic event(s) (typically due to dissociative amnesia and not to head injury, alcohol, or drugs)",
        example="no"
    )
    
    negative_beliefs: Literal["yes", "no"] = Field(
        ...,
        description="CRITERION D2: Persistent and exaggerated negative beliefs or expectations about oneself, others, or the world (e.g., 'I am bad,' 'No one can be trusted,' 'The world is completely dangerous')",
        example="yes"
    )
    
    distorted_blame: Literal["yes", "no"] = Field(
        ...,
        description="CRITERION D3: Persistent, distorted cognitions about the cause or consequences of the traumatic event that lead the individual to blame himself/herself or others",
        example="no"
    )
    
    negative_emotional_state: Literal["yes", "no"] = Field(
        ...,
        description="CRITERION D4: Persistent negative emotional state (e.g., fear, horror, anger, guilt, or shame)",
        example="yes"
    )
    
    diminished_interest: Literal["yes", "no"] = Field(
        ...,
        description="CRITERION D5: Markedly diminished interest or participation in significant activities",
        example="yes"
    )
    
    detachment_estrangement: Literal["yes", "no"] = Field(
        ...,
        description="CRITERION D6: Feelings of detachment or estrangement from others",
        example="yes"
    )
    
    inability_positive_emotions: Literal["yes", "no"] = Field(
        ...,
        description="CRITERION D7: Persistent inability to experience positive emotions (e.g., happiness, satisfaction, love, joy)",
        example="no"
    )
    
    irritability_aggression: Literal["yes", "no"] = Field(
        ...,
        description="CRITERION E1: Irritable behavior and angry outbursts (with little or no provocation) typically expressed as verbal or physical aggression toward people or objects",
        example="yes"
    )
    
    reckless_behavior: Literal["yes", "no"] = Field(
        ...,
        description="CRITERION E2: Reckless or self-destructive behavior",
        example="no"
    )
    
    hypervigilance: Literal["yes", "no"] = Field(
        ...,
        description="CRITERION E3: Hypervigilance",
        example="yes"
    )
    
    exaggerated_startle: Literal["yes", "no"] = Field(
        ...,
        description="CRITERION E4: Exaggerated startle response",
        example="no"
    )
    
    concentration_problems: Literal["yes", "no"] = Field(
        ...,
        description="CRITERION E5: Problems with concentration",
        example="yes"
    )
    
    sleep_disturbance: Literal["yes", "no"] = Field(
        ...,
        description="CRITERION E6: Sleep disturbance (e.g., difficulty falling or staying asleep or restless sleep)",
        example="yes"
    )
    
    duration_one_month: Literal["yes", "no"] = Field(
        ...,
        description="CRITERION F: Duration of the disturbance is more than 1 month",
        example="yes"
    )
    
    functional_impairment: Literal["yes", "no"] = Field(
        ...,
        description="CRITERION G: The disturbance causes clinically significant distress or impairment in social, occupational, or other important areas of functioning",
        example="yes"
    )
    
    not_substance_medical: Literal["yes", "no"] = Field(
        ...,
        description="CRITERION H: The disturbance is NOT attributable to the physiological effects of a substance (e.g., medication, alcohol) or another medical condition",
        example="yes"
    )
    
    dissociative_symptoms: Literal["yes", "no"] = Field(
        ...,
        description="DISSOCIATIVE SUBTYPE: Persistent or recurrent symptoms of depersonalization (feelings of unreality, detachment from oneself) or derealization (feelings of unreality about surroundings)",
        example="no"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "trauma_exposure": "yes",
                "intrusive_memories": "yes",
                "traumatic_nightmares": "yes",
                "dissociative_reactions": "no",
                "psychological_distress": "yes",
                "physiological_reactions": "yes",
                "avoidance_thoughts": "yes",
                "avoidance_reminders": "no",
                "inability_remember": "no",
                "negative_beliefs": "yes",
                "distorted_blame": "no",
                "negative_emotional_state": "yes",
                "diminished_interest": "yes",
                "detachment_estrangement": "yes",
                "inability_positive_emotions": "no",
                "irritability_aggression": "yes",
                "reckless_behavior": "no",
                "hypervigilance": "yes",
                "exaggerated_startle": "no",
                "concentration_problems": "yes",
                "sleep_disturbance": "yes",
                "duration_one_month": "yes",
                "functional_impairment": "yes",
                "not_substance_medical": "yes",
                "dissociative_symptoms": "no"
            }
        }


class Dsm5PtsdResponse(BaseModel):
    """
    Response model for DSM-5 Criteria for Posttraumatic Stress Disorder
    
    Diagnostic results based on DSM-5 PTSD criteria evaluation:
    - Criteria Not Met: Does not meet diagnostic criteria for PTSD
    - PTSD: Meets all DSM-5 criteria for Posttraumatic Stress Disorder
    - PTSD with Dissociative Subtype: Meets PTSD criteria plus dissociative symptoms
    
    Key DSM-5 Requirements for PTSD Diagnosis:
    - Criterion A: Trauma exposure (mandatory)
    - Criterion B: At least 1 intrusion symptom
    - Criterion C: At least 1 avoidance symptom 
    - Criterion D: At least 2 negative cognition/mood symptoms
    - Criterion E: At least 2 arousal/reactivity symptoms
    - Criterion F: Duration >1 month
    - Criterion G: Functional impairment
    - Criterion H: Not due to substance/medical condition
    
    Clinical Implications:
    - PTSD → Requires trauma-informed psychiatric evaluation and evidence-based treatment
    - Consider trauma-focused psychotherapy (CPT, PE, EMDR) and/or pharmacotherapy
    - PTSD with Dissociative Subtype → Requires specialized treatment approach
    - Assess for suicide risk and implement safety planning as needed
    
    Important Considerations:
    - This tool aids clinical assessment but does not replace comprehensive evaluation
    - Consider other trauma-related disorders if criteria not fully met
    - Use validated instruments like PCL-5 for comprehensive symptom assessment
    - Address comorbid conditions and substance use disorders
    
    Reference: American Psychiatric Association. DSM-5. Washington, DC: APA; 2013.
    """
    
    result: str = Field(
        ...,
        description="Diagnostic result based on DSM-5 PTSD criteria evaluation",
        example="PTSD"
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the diagnostic result",
        example="diagnosis"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation and treatment recommendations based on diagnostic result",
        example="Meets DSM-5 criteria for Posttraumatic Stress Disorder. Requires comprehensive trauma-informed psychiatric evaluation and treatment planning. Consider evidence-based treatments such as trauma-focused psychotherapy (CPT, PE, EMDR) and/or pharmacotherapy."
    )
    
    stage: str = Field(
        ...,
        description="Diagnostic stage (Criteria Not Met, PTSD, or PTSD with Dissociative Subtype)",
        example="PTSD"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the diagnostic stage",
        example="Meets criteria for PTSD"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "result": "PTSD",
                "unit": "diagnosis",
                "interpretation": "Meets DSM-5 criteria for Posttraumatic Stress Disorder. Requires comprehensive trauma-informed psychiatric evaluation and treatment planning. Consider evidence-based treatments such as trauma-focused psychotherapy (CPT, PE, EMDR) and/or pharmacotherapy.",
                "stage": "PTSD",
                "stage_description": "Meets criteria for PTSD"
            }
        }