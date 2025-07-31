"""
Diabetes Distress Scale (DDS17) Router

Endpoint for calculating DDS17 for diabetes-related emotional distress assessment.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.endocrinology.diabetes_distress_scale import (
    DiabetesDistressScaleRequest,
    DiabetesDistressScaleResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/diabetes_distress_scale",
    response_model=DiabetesDistressScaleResponse,
    summary="Calculate Diabetes Distress Scale (DDS17)",
    description="Measures diabetes-related emotional distress across four domains to identify sources of distress and guide targeted interventions for patients with diabetes.",
    response_description="The calculated diabetes distress scale with interpretation",
    operation_id="diabetes_distress_scale"
)
async def calculate_diabetes_distress_scale(request: DiabetesDistressScaleRequest):
    """
    Calculates Diabetes Distress Scale (DDS17) for Diabetes-Related Emotional Distress Assessment
    
    The Diabetes Distress Scale (DDS17) is a validated 17-item questionnaire that measures 
    diabetes-related emotional distress across four key domains. Developed by Polonsky et al. 
    in 2005, this instrument has become a cornerstone tool for identifying and quantifying 
    diabetes-specific psychological distress in clinical and research settings.
    
    **Historical Context and Development:**
    
    **Recognition of Diabetes Distress:**
    Prior to the development of the DDS17, diabetes-related psychological issues were often 
    assessed using general depression and anxiety scales that failed to capture the unique 
    emotional challenges associated with living with diabetes. Healthcare providers recognized 
    the need for a diabetes-specific tool that could identify the particular sources of 
    distress that patients experience in managing their condition.
    
    **Development Process:**
    The DDS17 was developed through extensive research involving focus groups with diabetes 
    patients, clinical experts, and rigorous psychometric testing. The researchers identified 
    four distinct domains of diabetes distress that emerged consistently across different 
    patient populations and clinical settings.
    
    **Validation and Psychometric Properties:**
    The scale has been extensively validated across diverse populations, including patients 
    with Type 1 and Type 2 diabetes, different age groups, and various cultural backgrounds. 
    The DDS17 demonstrates excellent internal consistency (Cronbach's alpha = 0.938) and 
    strong construct validity.
    
    **DDS17 Domains and Clinical Assessment:**
    
    **1. Emotional Burden (5 Items):**
    
    **Clinical Significance:**
    The Emotional Burden subscale captures the psychological weight of living with diabetes, 
    including feelings of being overwhelmed, discouraged, and the mental energy required 
    for constant diabetes management. This domain reflects the pervasive nature of diabetes 
    as a condition that affects nearly every aspect of daily life.
    
    **Assessment Components:**
    - **Overwhelming Demands:** Measures the extent to which diabetes management feels 
      unmanageable or excessive, often related to the complexity of self-care tasks and 
      the need for constant vigilance about blood glucose levels, medications, and lifestyle factors.
    
    - **Discouragement with Regimen:** Assesses feelings of hopelessness or frustration 
      about the effectiveness of diabetes management strategies, particularly when blood 
      glucose control remains suboptimal despite adherent self-care efforts.
    
    - **Sense of Failure:** Evaluates self-perception of inadequacy in diabetes management, 
      which can lead to guilt, shame, and reduced self-efficacy for continued self-care behaviors.
    
    - **Emotional Reactions:** Captures negative emotions specifically triggered by thinking 
      about living with diabetes, including anger, fear, and depression that are directly 
      related to the condition rather than general psychological distress.
    
    - **Mental and Physical Energy Depletion:** Measures the extent to which diabetes 
      management consumes cognitive and physical resources, potentially leaving patients 
      feeling exhausted and unable to engage fully in other life activities.
    
    **Clinical Implications:**
    High emotional burden scores are associated with poorer glycemic control, reduced 
    quality of life, and increased risk for clinical depression. Patients with elevated 
    emotional burden often benefit from diabetes-specific psychological interventions, 
    stress management training, and potentially mental health referrals.
    
    **2. Physician Distress (4 Items):**
    
    **Clinical Significance:**
    The Physician Distress subscale assesses the quality of the patient-provider relationship 
    specifically as it relates to diabetes care. This domain recognizes that diabetes 
    management is fundamentally collaborative and that problems in the healthcare relationship 
    can significantly impact patient outcomes and emotional well-being.
    
    **Assessment Components:**
    - **Provider Satisfaction:** Evaluates overall satisfaction with the diabetes care team, 
      including accessibility, responsiveness, and perceived competence in diabetes management.
    
    - **Provider Knowledge and Expertise:** Assesses patient confidence in their healthcare 
      provider's diabetes knowledge and ability to provide appropriate guidance for complex 
      diabetes management decisions.
    
    - **Communication Quality:** Measures the clarity and adequacy of provider communication, 
      including the specificity of diabetes management instructions and the provider's 
      ability to explain complex medical concepts in understandable terms.
    
    - **Provider Responsiveness:** Evaluates whether the provider takes patient concerns 
      seriously, responds appropriately to patient questions and problems, and demonstrates 
      empathy for the challenges of living with diabetes.
    
    **Clinical Implications:**
    High physician distress scores may indicate need for improved patient-provider 
    communication, care coordination changes, or referral to diabetes specialists. 
    Addressing provider relationship issues is crucial for optimizing diabetes management 
    and patient satisfaction with care.
    
    **3. Regimen Distress (5 Items):**
    
    **Clinical Significance:**
    The Regimen Distress subscale focuses on the burden and challenges associated with 
    diabetes self-management tasks. This domain recognizes that diabetes requires extensive 
    daily self-care activities that can become overwhelming, confusing, or interfere 
    significantly with normal life activities.
    
    **Assessment Components:**
    - **Regimen Complexity and Burden:** Assesses whether the prescribed diabetes management 
      regimen feels overwhelming in scope or complexity, potentially leading to non-adherence 
      or selective adherence to certain components of care.
    
    - **Blood Glucose Monitoring Stress:** Evaluates the emotional impact of frequent 
      blood glucose checking, including anxiety about results, pain or inconvenience of 
      testing, and the burden of constant self-monitoring.
    
    - **Dietary Interference:** Measures the extent to which diabetes dietary requirements 
      interfere with normal eating patterns, social dining, and food enjoyment, which can 
      significantly impact quality of life and social participation.
    
    - **Regimen Logic and Understanding:** Assesses whether the prescribed diabetes regimen 
      makes sense to the patient and whether they understand the rationale behind specific 
      recommendations, as poor understanding can lead to non-adherence and frustration.
    
    - **Goal Clarity:** Evaluates whether patients have clear, concrete, and achievable 
      goals for their diabetes management, as ambiguous or unrealistic goals can contribute 
      to discouragement and poor outcomes.
    
    **Clinical Implications:**
    High regimen distress scores suggest need for diabetes education, regimen simplification, 
    or exploration of alternative management strategies. These patients may benefit from 
    diabetes technology solutions, personalized education, or motivational interviewing 
    approaches to enhance self-care engagement.
    
    **4. Interpersonal Distress (3 Items):**
    
    **Clinical Significance:**
    The Interpersonal Distress subscale addresses the social and family dynamics surrounding 
    diabetes management. This domain recognizes that diabetes affects not only the individual 
    but also their relationships and social interactions, and that family and social support 
    can either facilitate or hinder effective diabetes management.
    
    **Assessment Components:**
    - **Support Adequacy:** Evaluates whether family members and friends provide appropriate 
      and helpful support for diabetes management efforts, or whether patients feel unsupported 
      in their self-care endeavors.
    
    - **Social Interference:** Assesses the extent to which family members or friends engage 
      in counterproductive "policing" behaviors that may create tension and resentment 
      rather than helpful support.
    
    - **Understanding and Empathy:** Measures whether family and friends understand the 
      challenges and complexities of living with diabetes, or whether the patient feels 
      misunderstood or judged by their social network.
    
    **Clinical Implications:**
    High interpersonal distress scores may indicate need for family education, communication 
    skills training, or family therapy. These patients may benefit from peer support groups 
    or interventions that involve family members in diabetes education and support training.
    
    **Clinical Applications and Implementation:**
    
    **Screening and Assessment:**
    The DDS17 can be administered in various clinical settings as part of routine diabetes 
    care to identify patients experiencing significant diabetes-related distress. It serves 
    as both a screening tool and a comprehensive assessment instrument for understanding 
    the specific sources of patient distress.
    
    **Treatment Planning:**
    The subscale structure of the DDS17 allows clinicians to identify specific areas of 
    distress and tailor interventions accordingly. For example, patients with high emotional 
    burden may benefit from stress management interventions, while those with high regimen 
    distress may need diabetes education or regimen simplification.
    
    **Outcome Monitoring:**
    The DDS17 can be administered repeatedly to monitor response to interventions and 
    track changes in diabetes distress over time. This longitudinal application helps 
    clinicians adjust treatment approaches and evaluate the effectiveness of distress-reduction 
    interventions.
    
    **Research Applications:**
    The DDS17 has been extensively used in diabetes research to study the relationship 
    between diabetes distress and various outcomes, including glycemic control, quality 
    of life, self-care behaviors, and healthcare utilization.
    
    **Scoring and Interpretation:**
    
    **Total Score Calculation:**
    The total DDS17 score is calculated by summing all 17 item responses and dividing 
    by 17 to obtain a mean item score ranging from 1.0 to 6.0. This approach allows 
    for meaningful comparison across patients and over time.
    
    **Subscale Score Calculation:**
    Each subscale score is calculated by summing the responses to items within that 
    subscale and dividing by the number of items in the subscale. This provides specific 
    information about the domains of greatest concern for individual patients.
    
    **Clinical Significance Thresholds:**
    Research has established that a mean item score of 3.0 or higher indicates clinically 
    significant diabetes distress that warrants clinical attention and intervention. 
    This threshold has been validated across diverse populations and consistently predicts 
    poor diabetes outcomes.
    
    **Subscale Interpretation:**
    Each subscale can be interpreted independently, with scores of 3.0 or higher in 
    any domain indicating need for targeted intervention in that specific area of diabetes 
    distress.
    
    **Clinical Recommendations by Distress Level:**
    
    **Low Distress (1.0-1.9):**
    Patients with low distress scores typically demonstrate good emotional adaptation 
    to diabetes management. Clinical recommendations include maintaining current support 
    structures, routine monitoring for changes in distress levels, and continuing effective 
    diabetes education and self-management support.
    
    **Moderate Distress (2.0-2.9):**
    Patients with moderate distress may benefit from targeted support and intervention 
    to prevent progression to high distress levels. Recommendations include discussing 
    specific sources of distress, developing targeted coping strategies, considering 
    diabetes education or support group referrals, and more frequent monitoring of 
    distress levels.
    
    **High Distress (3.0-6.0):**
    Patients with high distress require immediate clinical attention and comprehensive 
    intervention. Recommendations include referral to diabetes educators or mental health 
    professionals, development of comprehensive distress management plans, frequent 
    monitoring and follow-up, and addressing specific high-scoring subscale areas through 
    targeted interventions.
    
    **Integration with Diabetes Care:**
    
    **Routine Clinical Assessment:**
    The DDS17 should be integrated into routine diabetes care as part of comprehensive 
    diabetes management. Regular assessment allows for early identification of emerging 
    distress and proactive intervention to prevent deterioration in diabetes outcomes.
    
    **Multidisciplinary Care Coordination:**
    DDS17 results should inform multidisciplinary care planning, including coordination 
    between primary care providers, endocrinologists, diabetes educators, and mental 
    health professionals to address both medical and psychosocial aspects of diabetes care.
    
    **Quality Improvement:**
    Healthcare systems can use DDS17 implementation to monitor and improve the psychosocial 
    quality of diabetes care, track patient-reported outcomes, and identify system-level 
    interventions to reduce diabetes distress across patient populations.
    
    **Patient Engagement and Empowerment:**
    Sharing DDS17 results with patients can facilitate meaningful conversations about 
    diabetes-related challenges, validate patient experiences, and engage patients as 
    active participants in developing solutions to address sources of distress.
    
    **Evidence Base for Interventions:**
    
    **Diabetes-Specific Psychological Interventions:**
    Research has demonstrated the effectiveness of diabetes-specific cognitive behavioral 
    therapy, mindfulness-based interventions, and group therapy approaches in reducing 
    diabetes distress and improving both psychological and medical outcomes.
    
    **Educational Interventions:**
    Diabetes self-management education programs that address emotional aspects of diabetes 
    management, in addition to clinical knowledge and skills, have shown effectiveness 
    in reducing diabetes distress and improving patient outcomes.
    
    **Family and Social Interventions:**
    Interventions that involve family members and social support networks in diabetes 
    education and communication skills training have demonstrated effectiveness in reducing 
    interpersonal distress and improving family support for diabetes management.
    
    **Healthcare System Interventions:**
    Improvements in care coordination, patient-provider communication training, and 
    implementation of patient-centered care models have shown effectiveness in reducing 
    physician distress and improving overall diabetes care satisfaction.
    
    **Future Directions and Considerations:**
    
    **Technology Integration:**
    As diabetes technology continues to evolve, the DDS17 may need adaptation to assess 
    distress related to continuous glucose monitors, insulin pumps, and digital health 
    platforms that are increasingly integrated into diabetes management.
    
    **Cultural Adaptation:**
    Continued research is needed to ensure the DDS17 remains culturally appropriate 
    and valid across diverse populations, with potential adaptations for specific 
    cultural contexts and healthcare systems.
    
    **Personalized Medicine Applications:**
    Future research may explore how DDS17 profiles can inform personalized approaches 
    to diabetes management, including tailored intervention strategies based on individual 
    distress patterns and preferences.
    
    **Population Health Applications:**
    The DDS17 has potential applications in population health initiatives to identify 
    communities with high diabetes distress burden and implement targeted public health 
    interventions to address social determinants of diabetes distress.
    
    Args:
        request: DDS17 parameters including all 17 items rated on 6-point scale assessing 
                diabetes-related distress across emotional burden, physician distress, 
                regimen distress, and interpersonal distress domains
        
    Returns:
        DiabetesDistressScaleResponse: Comprehensive diabetes distress assessment including 
        total score, subscale scores, clinical significance determination, targeted 
        intervention recommendations, and follow-up guidance
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("diabetes_distress_scale", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Diabetes Distress Scale",
                    "details": {"parameters": parameters}
                }
            )
        
        return DiabetesDistressScaleResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Diabetes Distress Scale",
                "details": {"error": str(e)}
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "error": "InternalServerError",
                "message": "Internal error in calculation",
                "details": {"error": str(e)}
            }
        )