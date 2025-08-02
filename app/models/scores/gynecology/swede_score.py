"""
Swede Score Models

Request and response models for Swede Score colposcopy assessment.

References (Vancouver style):
1. Strander B, Andersson-Ellström A, Milsom I, Rådberg T, Ryd W. Liquid-based 
   cytology versus conventional Papanicolaou smear in an organized screening 
   program : a prospective randomized study. Cancer. 2007 Dec 25;111(6):285-91. 
   doi: 10.1002/cncr.23100.
2. Bowring J, Strander B, Young M, Evans H, Walker P. The Swede score: evaluation 
   of a scoring system designed to improve the predictive value of colposcopy. 
   J Low Genit Tract Dis. 2010 Oct;14(4):301-5. doi: 10.1097/LGT.0b013e3181d77756.

The Swede Score is a standardized colposcopy scoring system that evaluates five 
key characteristics of cervical lesions to predict high-grade cervical 
intraepithelial neoplasia (CIN). This tool enhances the accuracy and 
reproducibility of colposcopic assessment while guiding appropriate clinical 
management decisions in cervical cancer screening programs.
"""

from pydantic import BaseModel, Field
from typing import Literal


class SwedeScoreRequest(BaseModel):
    """
    Request model for Swede Score colposcopy assessment
    
    The Swede Score is a validated clinical prediction tool that standardizes 
    colposcopic evaluation of cervical lesions to predict the likelihood of 
    high-grade cervical intraepithelial neoplasia (CIN 2+). Developed in Sweden 
    and subsequently validated internationally, this scoring system addresses 
    the inherent subjectivity of colposcopic interpretation by providing 
    objective, standardized criteria for lesion assessment.
    
    Clinical Context and Historical Development:
    
    Background and Rationale:
    Colposcopy has been a cornerstone of cervical cancer screening programs 
    since its introduction in the 1920s, providing direct visualization of 
    the cervix under magnification to identify abnormal areas for targeted 
    biopsy. However, traditional colposcopic assessment relied heavily on 
    subjective interpretation, leading to significant inter-observer and 
    intra-observer variability in lesion evaluation and management decisions.
    
    The Swede Score was developed to address these limitations by creating 
    a systematic, objective approach to colposcopic assessment that could 
    improve diagnostic accuracy, reduce variability between practitioners, 
    and enhance training of novice colposcopists.
    
    International Validation and Adoption:
    Since its development, the Swede Score has been validated across diverse 
    populations and healthcare settings, demonstrating consistent performance 
    in predicting high-grade cervical lesions. Its simplicity and objectivity 
    have made it particularly valuable in resource-limited settings where 
    'see and treat' approaches can significantly improve screening program 
    effectiveness.
    
    Clinical Applications and Benefits:
    
    Primary Screening Enhancement:
    The Swede Score enhances the accuracy of primary cervical cancer screening 
    by providing standardized criteria for identifying women who require 
    immediate treatment versus those who can be managed conservatively with 
    surveillance or targeted biopsy.
    
    Training and Education:
    The systematic nature of the Swede Score makes it an excellent educational 
    tool for training healthcare providers in colposcopic assessment, reducing 
    the learning curve and improving consistency in lesion evaluation.
    
    Resource Optimization:
    By accurately predicting high-grade lesions, the Swede Score enables more 
    efficient use of healthcare resources, reducing unnecessary procedures 
    while ensuring appropriate treatment for those who need it.
    
    Detailed Parameter Analysis and Scoring Methodology:
    
    Acetowhite Uptake Assessment:
    
    Physiologic Basis:
    Acetowhite reaction occurs when dilute acetic acid (3-5%) is applied to 
    cervical tissue, causing proteins in abnormal cells to coagulate and 
    appear white. The intensity and characteristics of this reaction correlate 
    with the degree of cellular abnormality and nuclear density.
    
    Clinical Evaluation Technique:
    Apply 3-5% acetic acid to the cervix and observe the transformation zone 
    under colposcopic magnification. Assess the acetowhite reaction after 
    30-60 seconds, noting the intensity, opacity, and speed of development.
    
    Scoring Criteria:
    - None or transparent (0 points): No visible acetowhite reaction or only 
      faint, transparent changes suggesting normal tissue or low-grade changes
    - Shady, milky (1 point): Mild acetowhite reaction with translucent, 
      milky appearance suggesting possible low-grade abnormalities
    - Distinct, opaque white (2 points): Dense, opaque acetowhite reaction 
      that develops rapidly, highly suggestive of high-grade lesions
    
    Clinical Significance:
    Dense, opaque acetowhite reaction is strongly associated with high-grade 
    CIN due to increased nuclear density and altered cellular architecture 
    characteristic of these lesions.
    
    Margins and Surface Pattern Evaluation:
    
    Morphologic Assessment:
    The characteristics of lesion margins and surface patterns provide important 
    information about the underlying pathology. High-grade lesions typically 
    demonstrate more defined margins and surface irregularities compared to 
    low-grade changes.
    
    Evaluation Technique:
    Examine the borders of acetowhite areas and assess surface characteristics 
    under high magnification. Look for sharp demarcation from normal tissue, 
    surface elevation changes, and architectural patterns.
    
    Scoring Criteria:
    - Diffuse (0 points): Poorly defined margins that blend gradually into 
      surrounding normal tissue, typical of inflammatory changes or mild 
      abnormalities
    - Sharp but irregular, jagged (1 point): Well-defined but irregular margins 
      with jagged or scalloped borders, suggesting moderate abnormalities
    - Sharp and even, with surface level difference (2 points): Sharply 
      demarcated lesions with smooth, even borders and visible elevation 
      differences, highly characteristic of high-grade lesions
    
    Pathophysiologic Correlation:
    High-grade lesions develop sharp margins due to their monoclonal origin 
    and rapid growth pattern, while surface elevation reflects the increased 
    cellular proliferation and architectural disruption characteristic of 
    advanced dysplasia.
    
    Vascular Pattern Analysis:
    
    Angiogenic Assessment:
    Abnormal cervical lesions often develop characteristic vascular patterns 
    due to increased metabolic demands and angiogenic factors. The morphology 
    and distribution of these vessels provide important diagnostic information.
    
    Visualization Technique:
    Use high magnification and green filter (if available) to enhance vascular 
    visibility. Assess vessel caliber, pattern, and distribution within 
    acetowhite areas.
    
    Scoring Criteria:
    - Fine, regular (0 points): Normal capillary pattern with fine, regularly 
      spaced vessels suggesting normal tissue or minimal abnormalities
    - Absent (1 point): No visible vessels within the lesion, which may occur 
      in some low-grade lesions or areas of keratinization
    - Coarse or atypical (2 points): Dilated, irregular vessels with variable 
      caliber and spacing, strongly suggestive of high-grade lesions
    
    Clinical Correlation:
    Coarse, atypical vessels result from tumor angiogenesis and loss of normal 
    vascular architecture, making them reliable indicators of high-grade 
    disease and potential invasion.
    
    Lesion Size and Extent Assessment:
    
    Geographic Evaluation:
    The size and extent of cervical lesions correlate with disease severity 
    and risk of progression. Larger lesions are more likely to harbor 
    high-grade changes and have greater potential for containing occult 
    invasive disease.
    
    Measurement Technique:
    Assess the maximum diameter of acetowhite areas and determine the number 
    of cervical quadrants involved. Use colposcopic measurement tools or 
    estimate based on known cervical dimensions.
    
    Scoring Criteria:
    - <5 mm (0 points): Small, focal lesions with limited extent, typically 
      associated with low-grade changes or inflammatory conditions
    - 5-15 mm or 2 quadrants (1 point): Moderate-sized lesions involving 
      significant cervical area, suggesting more extensive abnormalities
    - >15 mm or 3-4 quadrants (2 points): Large lesions involving substantial 
      cervical surface area, highly associated with high-grade disease
    
    Risk Assessment:
    Extensive lesions have higher probability of containing high-grade changes, 
    multiple abnormal clones, and potential for harboring invasive disease, 
    making size an important predictor of lesion severity.
    
    Iodine Staining Pattern (Schiller's Test):
    
    Biochemical Basis:
    Schiller's test uses Lugol's iodine solution to identify areas of abnormal 
    cervical epithelium. Normal squamous epithelium contains glycogen that 
    stains brown with iodine, while abnormal areas lacking glycogen remain 
    unstained (iodine-negative) and appear yellow.
    
    Application Technique:
    Apply Lugol's iodine solution to the cervix after completing acetowhite 
    assessment. Allow adequate contact time and assess staining patterns 
    under colposcopic magnification.
    
    Scoring Criteria:
    - Brown (0 points): Normal brown staining indicating glycogen-rich normal 
      squamous epithelium or low-grade changes that retain glycogen
    - Faintly or patchy yellow (1 point): Irregular staining with areas of 
      faint or patchy iodine negativity, suggesting moderate abnormalities
    - Distinct yellow (2 points): Complete iodine negativity with distinct 
      yellow appearance, characteristic of high-grade lesions lacking glycogen
    
    Pathologic Correlation:
    High-grade CIN demonstrates complete loss of glycogen due to cellular 
    immaturity and altered metabolism, resulting in characteristic iodine 
    negativity that correlates strongly with histologic severity.
    
    Clinical Decision-Making Framework:
    
    Score Interpretation and Management Algorithms:
    
    Low Risk Scores (<5 points):
    These scores indicate low probability of high-grade disease with 97.3% 
    of patients having normal or low-grade lesions. Management typically 
    involves conservative surveillance with repeat cytology and HPV testing 
    according to established guidelines.
    
    Intermediate Risk Scores (5-7 points):
    This range requires individualized assessment considering patient age, 
    reproductive plans, compliance with follow-up, and cytologic/molecular 
    findings. Colposcopy-directed biopsy is generally recommended for 
    histopathologic confirmation.
    
    High Risk Scores (≥8 points):
    These scores demonstrate 90-100% specificity for high-grade lesions, 
    supporting immediate excisional treatment using 'see and treat' protocols 
    to provide both diagnosis and therapy in a single visit.
    
    Integration with Screening Programs:
    
    HPV-Based Screening:
    The Swede Score complements HPV-based screening programs by providing 
    objective triage for HPV-positive women, helping determine appropriate 
    management strategies based on colposcopic findings.
    
    Cytology Correlation:
    When used in conjunction with cytologic findings, the Swede Score enhances 
    diagnostic accuracy and helps resolve discordant results between cytology 
    and colposcopic impression.
    
    Quality Assurance Applications:
    The standardized nature of the Swede Score makes it valuable for quality 
    assurance programs, enabling monitoring of colposcopist performance and 
    consistency across different practitioners and healthcare settings.
    
    Special Populations and Considerations:
    
    Young Women:
    In adolescents and young women, conservative management is often preferred 
    even for intermediate scores due to high rates of spontaneous regression 
    and fertility preservation concerns.
    
    Pregnancy:
    The Swede Score can be used during pregnancy, but interpretation must 
    consider physiologic changes that may affect colposcopic appearance. 
    Treatment decisions should be deferred to postpartum period unless 
    invasion is suspected.
    
    Immunocompromised Patients:
    Immunocompromised women may have atypical colposcopic appearances, and 
    the Swede Score should be interpreted cautiously with consideration for 
    more aggressive management approaches.
    
    Resource-Limited Settings:
    The Swede Score is particularly valuable in resource-limited settings 
    where 'see and treat' approaches can significantly improve screening 
    program effectiveness by reducing loss to follow-up and providing 
    immediate treatment for high-risk lesions.
    
    Training and Implementation:
    
    Educational Benefits:
    The systematic approach of the Swede Score provides an excellent framework 
    for training healthcare providers in colposcopic assessment, reducing 
    inter-observer variability and improving diagnostic consistency.
    
    Implementation Strategies:
    Successful implementation requires comprehensive training programs, 
    standardized protocols, and regular quality assurance measures to ensure 
    consistent application across different practitioners and settings.
    
    Continuous Quality Improvement:
    Regular correlation of Swede Scores with histopathologic outcomes enables 
    continuous quality improvement and identification of areas for additional 
    training or protocol refinement.
    
    The Swede Score represents a significant advancement in colposcopic 
    assessment, providing objective, standardized criteria that enhance 
    diagnostic accuracy, improve training effectiveness, and optimize 
    clinical decision-making in cervical cancer screening programs.
    
    References (Vancouver style):
    1. Strander B, Andersson-Ellström A, Milsom I, Rådberg T, Ryd W. Liquid-based 
       cytology versus conventional Papanicolaou smear in an organized screening 
       program : a prospective randomized study. Cancer. 2007 Dec 25;111(6):285-91. 
       doi: 10.1002/cncr.23100.
    2. Bowring J, Strander B, Young M, Evans H, Walker P. The Swede score: evaluation 
       of a scoring system designed to improve the predictive value of colposcopy. 
       J Low Genit Tract Dis. 2010 Oct;14(4):301-5. doi: 10.1097/LGT.0b013e3181d77756.
    """
    
    aceto_uptake: Literal["None or transparent", "Shady, milky", "Distinct, opaque white"] = Field(
        ...,
        description="Acetowhite uptake after application of 3-5% acetic acid during colposcopy. "
                   "Assess reaction intensity after 30-60 seconds. None or transparent (0 points) "
                   "indicates no visible reaction or faint changes suggesting normal tissue. "
                   "Shady, milky (1 point) shows mild translucent reaction suggesting possible "
                   "low-grade abnormalities. Distinct, opaque white (2 points) demonstrates dense, "
                   "rapidly developing reaction highly suggestive of high-grade lesions.",
        example="Shady, milky"
    )
    
    margins_surface: Literal["Diffuse", "Sharp but irregular, jagged", "Sharp and even, with surface level difference"] = Field(
        ...,
        description="Characteristics of lesion margins and surface pattern under colposcopic examination. "
                   "Diffuse (0 points) shows poorly defined margins blending into normal tissue, typical "
                   "of inflammatory changes. Sharp but irregular, jagged (1 point) demonstrates well-defined "
                   "but irregular borders suggesting moderate abnormalities. Sharp and even, with surface "
                   "level difference (2 points) shows sharply demarcated lesions with smooth borders and "
                   "visible elevation, characteristic of high-grade lesions.",
        example="Sharp but irregular, jagged"
    )
    
    vessels: Literal["Fine, regular", "Absent", "Coarse or atypical"] = Field(
        ...,
        description="Vascular pattern observed during colposcopy using high magnification and green filter "
                   "if available. Fine, regular (0 points) shows normal capillary pattern with fine, "
                   "regularly spaced vessels suggesting normal tissue. Absent (1 point) indicates no "
                   "visible vessels within the lesion, may occur in low-grade lesions. Coarse or atypical "
                   "(2 points) demonstrates dilated, irregular vessels with variable caliber strongly "
                   "suggestive of high-grade lesions.",
        example="Fine, regular"
    )
    
    lesion_size: Literal["<5 mm", "5-15 mm or 2 quadrants", ">15 mm or 3-4 quadrants"] = Field(
        ...,
        description="Size of the acetowhite lesion or number of cervical quadrants involved. Measure "
                   "maximum diameter and assess extent of involvement. <5 mm (0 points) indicates small, "
                   "focal lesions typically associated with low-grade changes. 5-15 mm or 2 quadrants "
                   "(1 point) represents moderate-sized lesions suggesting more extensive abnormalities. "
                   ">15 mm or 3-4 quadrants (2 points) shows large lesions involving substantial cervical "
                   "area, highly associated with high-grade disease.",
        example="5-15 mm or 2 quadrants"
    )
    
    iodine_staining: Literal["Brown", "Faintly or patchy yellow", "Distinct yellow"] = Field(
        ...,
        description="Iodine staining pattern after application of Lugol's iodine solution (Schiller's test). "
                   "Normal squamous epithelium contains glycogen and stains brown. Brown (0 points) indicates "
                   "normal brown staining of glycogen-rich tissue. Faintly or patchy yellow (1 point) shows "
                   "irregular staining with areas of partial iodine negativity. Distinct yellow (2 points) "
                   "demonstrates complete iodine negativity characteristic of high-grade lesions lacking glycogen.",
        example="Brown"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "aceto_uptake": "Shady, milky",
                "margins_surface": "Sharp but irregular, jagged",
                "vessels": "Fine, regular",
                "lesion_size": "5-15 mm or 2 quadrants",
                "iodine_staining": "Brown"
            }
        }


class SwedeScoreResponse(BaseModel):
    """
    Response model for Swede Score colposcopy assessment
    
    The Swede Score provides objective risk stratification for cervical lesions 
    with scores ranging from 0-10 points. Higher scores indicate greater likelihood 
    of high-grade cervical intraepithelial neoplasia (CIN 2+) and guide appropriate 
    clinical management decisions.
    
    Clinical Interpretation and Management Framework:
    
    Low Risk Category (Scores <5):
    
    Clinical Significance:
    Scores below 5 indicate low probability of high-grade cervical lesions, 
    with studies demonstrating that 97.3% of patients in this category have 
    normal or low-grade findings on histopathology. This high negative 
    predictive value makes conservative management appropriate for most 
    patients in this category.
    
    Pathophysiologic Implications:
    Low scores typically reflect benign conditions, inflammatory changes, 
    immature squamous metaplasia, or low-grade CIN that may spontaneously 
    regress. The colposcopic features suggest minimal cellular abnormalities 
    and preserved tissue architecture.
    
    Management Recommendations:
    - Routine surveillance with repeat cytology and HPV testing per guidelines
    - Consider 12-month follow-up cytology for women with prior abnormal results
    - Patient education about normal results and routine screening intervals
    - Reassurance that immediate intervention is not required
    - Maintain routine screening schedule appropriate for patient age and risk factors
    
    Special Considerations:
    - Young women: Conservative management is particularly appropriate due to high regression rates
    - HPV-positive patients: May require closer surveillance despite low Swede Score
    - Immunocompromised patients: Consider shorter surveillance intervals
    - Patient anxiety: Provide adequate counseling about benign nature of findings
    
    Intermediate Risk Category (Scores 5-7):
    
    Clinical Significance:
    Intermediate scores indicate uncertain risk requiring individualized assessment 
    and clinical correlation. This range represents a diagnostic gray zone where 
    additional information is needed to guide appropriate management decisions.
    
    Diagnostic Approach:
    The intermediate score range necessitates histopathologic confirmation through 
    colposcopy-directed biopsy to accurately determine the presence and grade of 
    any underlying cervical intraepithelial neoplasia.
    
    Biopsy Strategy:
    - Multiple targeted biopsies from areas with highest Swede Score components
    - Include endocervical curettage if transformation zone not fully visible
    - Consider random biopsies if acetowihte areas are extensive
    - Ensure adequate tissue sampling for reliable histopathologic diagnosis
    
    Management Algorithm:
    - Colposcopy-directed biopsy for histopathologic confirmation
    - Correlation with cytology and HPV results for comprehensive assessment
    - Consider patient age, reproductive goals, and compliance with follow-up
    - Multidisciplinary discussion for complex cases
    - Close follow-up regardless of initial biopsy results
    
    Follow-up Protocols:
    - Repeat colposcopy and cytology at 6-month intervals
    - HPV testing to assess viral persistence or clearance
    - Consider excisional procedure if persistent abnormalities
    - Patient counseling about importance of adherence to follow-up
    
    High Risk Category (Scores ≥8):
    
    Clinical Significance:
    Scores of 8 or higher demonstrate 90-100% specificity for high-grade 
    cervical lesions, indicating very high probability of CIN 2+ requiring 
    immediate intervention. This score range supports definitive treatment 
    without delay.
    
    'See and Treat' Approach:
    High Swede Scores support immediate excisional treatment during the same 
    visit as colposcopy, providing both diagnostic and therapeutic benefits 
    while reducing patient visits and preventing loss to follow-up.
    
    Excisional Procedures:
    - Loop electrosurgical excision procedure (LEEP): Most commonly used
    - Cold knife cone biopsy: For specific indications (pregnancy, adenocarcinoma)
    - Laser cone biopsy: Alternative when available
    - Ensure adequate excision margins (5-7 mm depth, 3-4 mm lateral)
    
    Procedural Considerations:
    - Obtain informed consent for both diagnostic and therapeutic procedures
    - Ensure adequate anesthesia and patient comfort
    - Send entire specimen for histopathologic evaluation
    - Assess margins of excision for completeness
    - Provide post-procedure care instructions and follow-up planning
    
    Post-Treatment Surveillance:
    - Cytology and HPV co-testing at 12 and 24 months post-treatment
    - Annual screening thereafter if results remain normal
    - Consider more frequent follow-up for positive margins or persistent HPV
    - Long-term surveillance due to increased risk of recurrence and progression
    
    Resource Allocation and Healthcare System Benefits:
    
    Efficiency Optimization:
    The Swede Score enables more efficient use of healthcare resources by:
    - Reducing unnecessary biopsies for low-risk lesions
    - Streamlining treatment pathways for high-risk lesions
    - Minimizing loss to follow-up through immediate treatment when appropriate
    - Optimizing colposcopy clinic scheduling and resource allocation
    
    Cost-Effectiveness:
    Studies demonstrate cost-effectiveness through:
    - Reduced number of patient visits required
    - Decreased need for multiple biopsies and procedures
    - Earlier treatment of high-grade lesions preventing progression
    - Improved patient satisfaction through streamlined care pathways
    
    Quality Assurance Applications:
    
    Performance Monitoring:
    The standardized nature of the Swede Score enables:
    - Monitoring of individual colposcopist performance
    - Benchmarking across different healthcare facilities
    - Identification of training needs and quality improvement opportunities
    - Correlation of colposcopic assessment with histopathologic outcomes
    
    Training Enhancement:
    Educational benefits include:
    - Standardized training curricula for colposcopy programs
    - Objective assessment of trainee competency
    - Reduced inter-observer variability among practitioners
    - Improved consistency in clinical decision-making
    
    Special Clinical Scenarios:
    
    Pregnancy Considerations:
    - Swede Score can be used during pregnancy with careful interpretation
    - Physiologic changes may affect colposcopic appearance
    - Conservative management preferred unless invasion suspected
    - Definitive treatment deferred to postpartum period in most cases
    
    Adolescent and Young Women:
    - Higher threshold for intervention due to high regression rates
    - Emphasis on fertility preservation and minimal intervention
    - Extended surveillance periods often appropriate
    - Patient and family counseling about conservative management
    
    Immunocompromised Patients:
    - May require modified interpretation due to atypical presentations
    - Consider more aggressive management for intermediate scores
    - Shorter surveillance intervals and closer monitoring
    - Multidisciplinary care coordination with immunology specialists
    
    Global Health Applications:
    
    Resource-Limited Settings:
    The Swede Score is particularly valuable in resource-limited settings where:
    - 'See and treat' approaches significantly improve program effectiveness
    - Reduced loss to follow-up through immediate treatment
    - Simplified training requirements for healthcare providers
    - Cost-effective screening and treatment protocols
    
    Program Implementation:
    Successful implementation requires:
    - Comprehensive training programs for healthcare providers
    - Quality assurance measures and ongoing education
    - Integration with existing screening programs
    - Monitoring and evaluation systems for continuous improvement
    
    Research and Future Directions:
    
    Ongoing Validation:
    Continued research focuses on:
    - Validation in diverse populations and healthcare settings
    - Integration with molecular biomarkers and advanced imaging
    - Artificial intelligence applications for automated scoring
    - Optimization of score thresholds for specific populations
    
    Technology Integration:
    Future developments may include:
    - Digital colposcopy with automated Swede Score calculation
    - Telemedicine applications for remote colposcopy interpretation
    - Integration with electronic health records for decision support
    - Mobile health applications for point-of-care assessment
    
    The Swede Score serves as a valuable clinical decision support tool that 
    enhances the accuracy, reproducibility, and efficiency of colposcopic 
    assessment while supporting evidence-based management decisions in 
    cervical cancer screening and prevention programs.
    
    Reference: Bowring J, et al. J Low Genit Tract Dis. 2010;14(4):301-5.
    """
    
    result: int = Field(
        ...,
        ge=0,
        le=10,
        description="Calculated Swede Score based on five colposcopic parameters. Total score ranges "
                   "from 0-10 points with higher scores indicating greater likelihood of high-grade "
                   "cervical lesions. Score calculated by summing points from aceto uptake (0-2), "
                   "margins/surface (0-2), vessels (0-2), lesion size (0-2), and iodine staining (0-2).",
        example=4
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the calculated score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Comprehensive clinical interpretation of the Swede Score with specific recommendations "
                   "for cervical lesion management, including risk stratification, biopsy indications, "
                   "treatment considerations, and follow-up protocols based on evidence-based guidelines "
                   "and clinical best practices.",
        example="Swede Score of 4 indicates low risk for high-grade cervical lesion. Studies show that "
                "97.3% of patients with scores <5 have normal or low-grade lesions. Consider routine "
                "follow-up with repeat cytology and HPV testing per guidelines, or targeted biopsy only "
                "if high clinical suspicion persists."
    )
    
    stage: str = Field(
        ...,
        description="Risk category based on calculated Swede Score",
        example="Low Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the risk category and recommended clinical approach",
        example="Low suspicion for high-grade lesion"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 4,
                "unit": "points",
                "interpretation": "Swede Score of 4 indicates low risk for high-grade cervical lesion. Studies show that 97.3% of patients with scores <5 have normal or low-grade lesions. Consider routine follow-up with repeat cytology and HPV testing per guidelines, or targeted biopsy only if high clinical suspicion persists. This score has high negative predictive value for excluding high-grade disease, making conservative management appropriate in most cases.",
                "stage": "Low Risk",
                "stage_description": "Low suspicion for high-grade lesion"
            }
        }