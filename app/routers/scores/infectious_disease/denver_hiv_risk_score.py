"""
Denver HIV Risk Score Router

Endpoint for calculating Denver HIV Risk Score for targeted HIV screening.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.infectious_disease.denver_hiv_risk_score import (
    DenverHivRiskScoreRequest,
    DenverHivRiskScoreResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/denver_hiv_risk_score",
    response_model=DenverHivRiskScoreResponse,
    summary="Calculate Denver HIV Risk Score",
    description="Predicts probability of undiagnosed HIV infection in patients aged 13 and older using demographic and behavioral risk factors.",
    response_description="The calculated denver hiv risk score with interpretation",
    operation_id="calculate_denver_hiv_risk_score"
)
async def calculate_denver_hiv_risk_score(request: DenverHivRiskScoreRequest):
    """
    Calculates Denver HIV Risk Score for Targeted HIV Screening
    
    The Denver HIV Risk Score is a validated clinical decision tool that predicts 
    the probability of undiagnosed HIV infection in patients aged 13 and older. 
    Developed through rigorous epidemiological analysis, this score enables targeted 
    HIV screening strategies that optimize resource allocation while maintaining 
    clinical effectiveness.
    
    **Historical Context and Development:**
    
    **Public Health Challenge:**
    Despite widespread availability of HIV testing, a significant proportion of 
    HIV-positive individuals remain undiagnosed, contributing to ongoing transmission 
    and delayed treatment initiation. The CDC estimates that approximately 13% of 
    HIV-positive individuals in the United States are unaware of their infection 
    status, representing both a public health challenge and an opportunity for 
    targeted intervention.
    
    **Universal vs. Targeted Screening Debate:**
    While universal HIV screening has been recommended by the CDC since 2006, 
    implementation remains inconsistent due to resource constraints, time limitations, 
    and varying risk profiles across populations. Targeted screening approaches 
    that identify high-risk individuals can potentially achieve similar case 
    detection rates while optimizing resource utilization.
    
    **Denver HIV Risk Score Development:**
    The Denver HIV Risk Score was developed at Denver Health Medical Center through 
    a comprehensive analysis of patient populations in emergency departments and 
    sexually transmitted disease clinics. The derivation study used multivariable 
    logistic regression to identify demographic and behavioral factors most strongly 
    associated with undiagnosed HIV infection.
    
    **Evidence Base and Validation:**
    
    **Derivation Study (2012):**
    The original development study analyzed 5,770 patients aged 13-64 years across 
    multiple clinical settings. Using undiagnosed HIV infection as the primary 
    outcome, researchers identified age, gender, sexual practices, injection drug 
    use, previous HIV testing, and race/ethnicity as significant predictors.
    
    **External Validation Studies:**
    Multiple external validation studies have confirmed the score's effectiveness 
    in different populations and settings. A 2014 study in an urban emergency 
    department validated an abbreviated version, demonstrating maintained accuracy 
    with simplified implementation.
    
    **Performance Characteristics:**
    The Denver HIV Risk Score demonstrates strong discriminatory ability with a 
    C-statistic of 0.74 (95% CI: 0.68-0.80) in the derivation cohort. The score 
    effectively stratifies patients into distinct risk categories with HIV 
    prevalence ranging from 0.31% in the lowest risk group to 3.59% in the 
    highest risk category.
    
    **Denver HIV Risk Score Components and Clinical Assessment:**
    
    **Age Category (0-12 Points):**
    
    **Epidemiological Rationale:**
    Age-specific HIV risk reflects complex interactions between biological 
    susceptibility, behavioral patterns, and epidemic dynamics. The Denver 
    score incorporates nuanced age-related risk patterns that differ from 
    simple linear relationships.
    
    **Peak Risk Ages (33-46 years: 12 points):**
    This age group represents the peak of the HIV epidemic curve, with highest 
    rates of undiagnosed infection. Individuals in this category often have 
    extended periods of potential exposure and may have engaged in higher-risk 
    behaviors during the height of the HIV epidemic.
    
    **Emerging Adult Risk (22-32 years: 4-6 points):**
    Young adults show increased HIV risk due to developmental factors including 
    experimentation with sexual behaviors and substances, multiple partnerships, 
    and potentially inconsistent risk reduction practices.
    
    **Lower Risk Ages:**
    Younger adolescents (<22 years: 2 points) and older adults (>54 years: 0-3 points) 
    generally show lower HIV acquisition rates, though individual risk assessment 
    remains important.
    
    **Gender (0-21 Points):**
    
    **Male Gender (21 points):**
    Male gender receives substantial weight in the scoring system, reflecting 
    epidemiological patterns where men, particularly men who have sex with men 
    (MSM), represent the majority of new HIV infections in developed countries. 
    This includes both behavioral factors and biological susceptibility differences.
    
    **Female Gender (0 points):**
    While women certainly acquire HIV infection, the baseline scoring reflects 
    lower population-level risk in the study populations. Individual risk factors 
    such as injection drug use or specific sexual practices modify this baseline 
    assessment.
    
    **Sexual Practices (-10 to 22 Points):**
    
    **Sex with Male Partners (22 points):**
    This category captures the highest-risk sexual behavior patterns, particularly 
    relevant for both men who have sex with men and women whose male partners may 
    be at increased HIV risk. The high point value reflects consistently elevated 
    transmission rates in these populations.
    
    **Receptive Anal Intercourse (8 points):**
    Anal intercourse carries substantially higher per-act HIV transmission risk 
    compared to other sexual practices, with receptive partners at particularly 
    elevated risk due to tissue vulnerability and viral load exposure patterns.
    
    **Vaginal Intercourse (-10 points):**
    Exclusive vaginal intercourse receives negative points, reflecting lower 
    transmission risk compared to anal intercourse. This demonstrates the score's 
    ability to identify protective behaviors that reduce HIV acquisition risk.
    
    **Injection Drug Use (0-9 Points):**
    
    **Current or Recent Use (9 points):**
    Injection drug use represents one of the most significant HIV risk factors 
    due to potential sharing of contaminated equipment. The score captures both 
    direct transmission risk through shared needles and indirect risk through 
    behavioral factors associated with substance use.
    
    **Epidemiological Context:**
    Injection drug use-associated HIV transmission has shown geographic and 
    temporal variation, with recent outbreaks in rural areas highlighting the 
    continued importance of this risk factor across diverse populations.
    
    **Past HIV Testing (-4 to 0 Points):**
    
    **Previous Testing (-4 points):**
    Prior HIV testing receives negative points, indicating protective behavior 
    and health-seeking attitudes. Individuals who have been previously tested 
    demonstrate engagement with healthcare and awareness of HIV risk, factors 
    associated with lower undiagnosed infection rates.
    
    **Health-Seeking Behavior:**
    Previous testing serves as a proxy for overall health engagement, including 
    potential participation in risk reduction counseling and preventive services 
    that may reduce HIV acquisition risk.
    
    **Race/Ethnicity (0-9 Points - Optional):**
    
    **Inclusion Considerations:**
    Race/ethnicity parameters reflect documented health disparities in HIV 
    prevalence rather than biological susceptibility. These disparities result 
    from complex interactions between social determinants of health, access to 
    healthcare, and structural factors affecting HIV risk and testing patterns.
    
    **Black/African American (9 points):**
    Higher scoring reflects documented epidemiological patterns where Black 
    communities experience disproportionate HIV burden due to structural factors 
    including healthcare access barriers, socioeconomic factors, and historical 
    medical mistrust.
    
    **Hispanic/Latino (3 points):**
    Moderate increased risk reflects demographic patterns while acknowledging 
    significant heterogeneity within Hispanic/Latino populations regarding HIV 
    risk and prevalence patterns.
    
    **Implementation Considerations:**
    Many healthcare systems choose to omit race/ethnicity components to avoid 
    potential bias while focusing on behavioral and demographic factors that 
    more directly reflect individual risk.
    
    **Risk Categories and Clinical Management:**
    
    **Very Low Risk (<20 points): 0.31% HIV Prevalence**
    
    **Clinical Characteristics:**
    Patients in this category typically have minimal traditional HIV risk factors 
    and demonstrate health-seeking behaviors. The low prevalence rate suggests 
    that universal screening in this population may be less cost-effective than 
    targeted approaches.
    
    **Screening Approach:**
    Routine screening following standard CDC guidelines remains appropriate, with 
    emphasis on general prevention education and maintaining awareness of HIV 
    risk in changing life circumstances.
    
    **Resource Allocation:**
    In resource-constrained settings, screening programs might prioritize higher-risk 
    categories while ensuring that routine screening remains available for this 
    population based on patient preferences and clinical judgment.
    
    **Low Risk (20-29 points): 0.41% HIV Prevalence**
    
    **Clinical Characteristics:**
    Slightly elevated risk compared to very low category, often reflecting modest 
    behavioral or demographic risk factors. Patients may benefit from targeted 
    prevention education and periodic risk reassessment.
    
    **Screening Strategy:**
    Offer HIV testing with appropriate counseling, emphasizing the value of 
    knowing one's status and available prevention resources. Consider annual 
    screening for individuals with ongoing low-level risk factors.
    
    **Prevention Focus:**
    Emphasis on risk reduction education, safer sex practices, and maintaining 
    awareness of HIV prevention strategies including PrEP if circumstances change.
    
    **Moderate Risk (30-39 points): 0.99% HIV Prevalence**
    
    **Clinical Characteristics:**
    Nearly 1% HIV prevalence indicates substantial clinical importance, with 
    cost-effectiveness of targeted screening becoming more favorable. Patients 
    often have multiple risk factors requiring comprehensive assessment.
    
    **Screening Recommendations:**
    Strongly recommend HIV testing with comprehensive prevention counseling. 
    Consider more frequent screening intervals (every 3-6 months) for individuals 
    with persistent risk factors.
    
    **Prevention Services:**
    Provide comprehensive risk reduction counseling, discuss available prevention 
    strategies, and consider PrEP evaluation for appropriate candidates with 
    ongoing risk.
    
    **High Risk (40-49 points): 1.59% HIV Prevalence**
    
    **Clinical Characteristics:**
    Substantially elevated HIV prevalence approaching 2% indicates urgent need 
    for testing and prevention services. Patients typically have multiple or 
    high-impact risk factors requiring intensive intervention.
    
    **Urgent Testing Protocol:**
    Recommend expedited HIV testing with same-day results when possible. Implement 
    expedited linkage to care protocols if testing positive and comprehensive 
    prevention services if testing negative.
    
    **Prevention Prioritization:**
    Strong consideration for PrEP evaluation, frequent screening protocols (every 
    3 months), and linkage to specialized HIV prevention services and case 
    management support.
    
    **Very High Risk (≥50 points): 3.59% HIV Prevalence**
    
    **Clinical Characteristics:**
    Extremely high HIV prevalence exceeding 3.5% indicates immediate public health 
    and clinical priority. Patients require urgent, comprehensive intervention 
    with intensive follow-up and support services.
    
    **Immediate Testing Protocol:**
    Immediate HIV testing with same-day results essential. Implement emergency 
    protocols for linkage to care if positive and intensive prevention services 
    if negative.
    
    **Intensive Prevention Services:**
    Prioritize for PrEP evaluation and initiation, implement frequent screening 
    (monthly to quarterly), and provide intensive case management with comprehensive 
    support services to address underlying risk factors.
    
    **Clinical Applications and Implementation:**
    
    **Emergency Department Screening:**
    The Denver HIV Risk Score has demonstrated particular utility in emergency 
    department settings where brief, focused risk assessment tools are needed 
    for rapid decision-making about HIV testing offers.
    
    **Primary Care Integration:**
    Integration into primary care electronic health records can support systematic 
    risk assessment and screening recommendations, particularly for practices 
    serving diverse populations with varying HIV risk profiles.
    
    **Public Health Programs:**
    Community health programs can use the Denver HIV Risk Score to optimize 
    testing resource allocation, focusing intensive outreach and testing efforts 
    on populations most likely to benefit.
    
    **Quality Improvement Applications:**
    Healthcare systems can use Denver HIV Risk Score implementation to standardize 
    HIV risk assessment, reduce practice variation, and monitor the effectiveness 
    of targeted screening strategies.
    
    **Limitations and Considerations:**
    
    **Population Specificity:**
    The Denver HIV Risk Score was derived from specific clinical populations 
    (emergency departments and STD clinics) and may require validation or 
    recalibration for other settings or populations with different baseline 
    HIV prevalence.
    
    **Temporal Considerations:**
    HIV epidemiology continues to evolve with changing demographics, prevention 
    interventions (including PrEP), and social factors. Periodic reassessment 
    of score performance and potential recalibration may be needed.
    
    **Individual vs. Population Risk:**
    While the score provides valuable population-level risk stratification, 
    individual patients may have important risk factors not captured by the 
    scoring system, requiring ongoing clinical judgment integration.
    
    **Bias and Equity Considerations:**
    Implementation should include attention to potential bias in risk assessment 
    and ensure that targeted screening approaches do not inadvertently reduce 
    access to testing for individuals who desire it regardless of calculated risk.
    
    **Future Directions and Research:**
    
    **Digital Health Integration:**
    Development of digital tools and clinical decision support systems can 
    facilitate broader implementation of the Denver HIV Risk Score while 
    maintaining consistency and accuracy in risk assessment.
    
    **Machine Learning Enhancement:**
    Advanced analytics and machine learning approaches may enhance the predictive 
    accuracy of HIV risk assessment tools while maintaining clinical usability 
    and interpretability.
    
    **Implementation Science:**
    Research into effective implementation strategies, provider training, and 
    system-level factors affecting adoption can optimize the impact of targeted 
    HIV screening approaches.
    
    **Global Applications:**
    Adaptation and validation of risk-based HIV screening tools for different 
    global contexts and epidemic patterns may enhance worldwide HIV detection 
    and prevention efforts.
    
    Args:
        request: Denver HIV Risk Score parameters including age group, gender, 
                sexual practices, injection drug use, past HIV testing, and 
                optional race/ethnicity for comprehensive HIV risk assessment
        
    Returns:
        DenverHivRiskScoreResponse: Comprehensive HIV risk assessment including 
        Denver HIV Risk Score, risk category, HIV prevalence estimates, screening 
        recommendations, prevention guidance, and PrEP considerations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("denver_hiv_risk_score", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Denver HIV Risk Score",
                    "details": {"parameters": parameters}
                }
            )
        
        return DenverHivRiskScoreResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Denver HIV Risk Score",
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