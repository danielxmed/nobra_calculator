"""
Rome IV Diagnostic Criteria for Unspecified Functional Bowel Disorder Router

Endpoint for Rome IV unspecified functional bowel disorder diagnostic assessment.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.gastroenterology.rome_iv_unspecified_functional_bowel_disorder import (
    RomeIvUnspecifiedFunctionalBowelDisorderRequest,
    RomeIvUnspecifiedFunctionalBowelDisorderResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/rome_iv_unspecified_functional_bowel_disorder",
    response_model=RomeIvUnspecifiedFunctionalBowelDisorderResponse,
    summary="Rome IV Diagnostic Criteria for Unspecified Functional Bowel Disorder",
    description="Applies the official Rome IV diagnostic criteria for unspecified functional bowel disorder, a catch-all "
                "diagnosis for functional bowel symptoms that do not meet specific criteria for IBS, functional constipation, "
                "functional diarrhea, or functional abdominal bloating/distension. This validated diagnostic tool evaluates "
                "temporal criteria (symptoms ≥3 months with onset ≥6 months ago), functional etiology, exclusion of other "
                "specific functional disorders, and absence of alarm symptoms (GI bleeding, iron deficiency anemia, weight "
                "loss, masses/lymphadenopathy, family history without screening, age >50 without screening, sudden bowel "
                "habit changes). ALL criteria must be met for positive diagnosis. This diagnosis acknowledges that functional "
                "bowel disorders represent a spectrum rather than isolated entities. Management is symptom-directed using "
                "individualized multimodal approaches including dietary modifications, pharmacologic interventions, and "
                "behavioral support. Essential for patients with atypical or mixed functional bowel symptom patterns.",
    response_description="Rome IV diagnostic assessment with criteria fulfillment status, clinical interpretation, and comprehensive symptom-directed treatment recommendations",
    operation_id="rome_iv_unspecified_functional_bowel_disorder"
)
async def calculate_rome_iv_unspecified_functional_bowel_disorder(request: RomeIvUnspecifiedFunctionalBowelDisorderRequest):
    """
    Rome IV Diagnostic Criteria for Unspecified Functional Bowel Disorder Assessment
    
    Applies the international standard Rome IV diagnostic criteria for unspecified 
    functional bowel disorder, a catch-all diagnosis within the functional bowel 
    disorders classification system. This evidence-based diagnostic framework provides 
    a systematic approach for patients with functional bowel symptoms that don't meet 
    criteria for more specific disorders such as IBS, functional constipation, 
    functional diarrhea, or functional abdominal bloating/distension.
    
    Clinical Significance and Diagnostic Utility:
    The Rome IV criteria recognize that functional bowel disorders constitute a spectrum 
    of gastrointestinal disorders rather than isolated entities. While characterized 
    as distinct disorders based on diagnostic criteria, significant overlap exists 
    between different functional conditions. The unspecified functional bowel disorder 
    category acknowledges this complexity and provides a diagnostic option for patients 
    whose symptoms don't fit neatly into specific categories.
    
    Diagnostic Framework:
    This catch-all diagnosis is deliberately broad yet specific in its exclusions, 
    requiring both positive criteria (temporal requirements and functional etiology) 
    and multiple exclusion criteria (other functional disorders and alarm symptoms). 
    The diagnosis serves patients with mixed symptom patterns, atypical presentations, 
    or symptoms that fluctuate between different functional disorder criteria.
    
    Rome IV Diagnostic Criteria:
    
    INCLUSION CRITERIA (both required):
    1. Bowel symptoms present for ≥3 months with symptom onset ≥6 months prior to diagnosis
    2. Bowel symptoms not attributable to an organic etiology
    
    EXCLUSION OF OTHER FUNCTIONAL DISORDERS (all must be excluded):
    3. Does not meet Rome IV criteria for Irritable Bowel Syndrome (IBS)
    4. Does not meet Rome IV criteria for functional constipation
    5. Does not meet Rome IV criteria for functional diarrhea
    6. Does not meet Rome IV criteria for functional abdominal bloating/distension
    
    EXCLUSION OF ALARM SYMPTOMS (all must be absent):
    7. No gastrointestinal bleeding (melena, hematemesis, hematochezia)
    8. No unexplained iron deficiency anemia
    9. No unintentional weight loss (>10% body weight over 6 months)
    10. No palpable abdominal mass or lymphadenopathy
    11. No family history of colon cancer without appropriate screening
    12. No symptom onset after age 50 without cancer screening
    13. No sudden change in bowel habits
    
    Clinical Characteristics and Patient Presentation:
    
    Symptom Patterns:
    - Mixed constipation and diarrhea not meeting IBS criteria
    - Abdominal discomfort not meeting IBS pain criteria
    - Bloating not meeting functional bloating criteria
    - Altered bowel habits without clear predominant pattern
    - Symptoms may fluctuate or change over time
    - Often atypical presentations of common functional symptoms
    
    Temporal Features:
    - Chronic symptoms with insidious onset (distinguishes from acute conditions)
    - Symptoms may be intermittent but fulfill temporal criteria overall
    - Often history of symptoms for years with variable severity
    - May have periods of symptom remission and exacerbation
    - Stress and life events may trigger symptom flares
    
    Psychosocial Factors:
    - Frequently associated with psychological stress or trauma
    - Common comorbidity with anxiety and depression
    - Social and occupational impact from chronic symptoms
    - Patient frustration from lack of specific diagnosis
    - Quality of life impairment despite absence of organic disease
    
    Required Clinical Evaluation:
    
    History and Physical Examination:
    - Comprehensive symptom characterization with temporal patterns
    - Assessment of functional impact on daily activities and quality of life
    - Review of prior evaluations, treatments attempted, and responses
    - Detailed family history of gastrointestinal and malignant diseases
    - Medication history including antibiotics, NSAIDs, and supplements
    - Dietary history with identification of potential triggers
    - Psychosocial assessment including stress factors and coping mechanisms
    
    Laboratory Studies:
    - Complete blood count with differential to exclude anemia
    - Comprehensive metabolic panel including liver function tests
    - Inflammatory markers (ESR, CRP) to exclude inflammatory conditions
    - Tissue transglutaminase antibodies for celiac disease screening
    - Thyroid function tests if symptoms suggest hyperthyroidism
    - Stool studies if diarrhea component (culture, parasites, calprotectin)
    
    Additional Testing (when indicated):
    - Colonoscopy if alarm symptoms present or screening indicated
    - Upper endoscopy if upper gastrointestinal symptoms predominant
    - Cross-sectional imaging (CT abdomen/pelvis) if structural concerns
    - Breath testing for small intestinal bacterial overgrowth (SIBO)
    - Anorectal manometry if defecation disorders suspected
    - Gastric emptying study if gastroparesis symptoms present
    
    Differential Diagnosis Considerations:
    
    Specific Functional Bowel Disorders:
    
    Irritable Bowel Syndrome (IBS):
    - Requires predominant abdominal pain with altered bowel habits
    - Pain related to defecation, stool frequency, or stool form changes
    - Clear criteria for IBS-C, IBS-D, or IBS-M subtypes
    - Pain is the defining feature distinguishing IBS from other disorders
    
    Functional Constipation:
    - Specific criteria for difficult, infrequent, or incomplete defecation
    - Bristol stool types 1-2 predominant with associated symptoms
    - Straining, incomplete evacuation, manual maneuvers required
    - Rarely meets IBS criteria due to absence of pain
    
    Functional Diarrhea:
    - Loose stools (Bristol types 6-7) in ≥75% of bowel movements
    - Absence of predominant abdominal pain (key distinction from IBS-D)
    - No inflammatory markers or structural abnormalities
    - Chronic course meeting temporal criteria
    
    Functional Abdominal Bloating/Distension:
    - Predominant complaint of bloating or visible distension
    - Not predominantly pain or altered bowel habits
    - May have associated bowel symptoms but bloating predominates
    - Significant functional impact from bloating symptoms
    
    Organic Bowel Disorders:
    
    Inflammatory Bowel Disease (IBD):
    - Crohn's disease or ulcerative colitis with inflammatory markers
    - Endoscopic and histologic evidence of chronic inflammation
    - May have extraintestinal manifestations and complications
    - Requires immunosuppressive therapy and specialized management
    
    Celiac Disease:
    - Positive serology and characteristic duodenal biopsy findings
    - Malabsorption with nutritional deficiencies
    - Symptoms improve with strict gluten-free diet
    - Associated autoimmune conditions common
    
    Colorectal Malignancy:
    - Alarm symptoms including bleeding, weight loss, anemia
    - Progressive symptom course rather than fluctuating pattern
    - Family history or genetic predisposition factors
    - Requires urgent evaluation and staging if suspected
    
    Clinical Applications and Management Implications:
    
    Positive Diagnosis Management Strategy:
    
    1. Patient Education and Counseling:
       - Explanation of functional disorder concept and benign nature
       - Reassurance about absence of serious underlying disease
       - Discussion of chronic nature with fluctuating symptoms
       - Setting realistic expectations for symptom improvement
       - Importance of lifestyle modifications and stress management
    
    2. Symptom-Directed Dietary Interventions:
       - Comprehensive dietary assessment and trigger identification
       - Elimination of known problematic foods (gas-producing, high-fat)
       - Fiber modification based on predominant symptom pattern
       - Trial of low FODMAP diet if IBS-like symptoms predominate
       - Probiotics for microbiome modulation and symptom relief
       - Regular meal timing and adequate hydration
    
    3. Pharmacologic Management Options:
       - Antispasmodics (dicyclomine, hyoscyamine) for cramping and discomfort
       - Loperamide for diarrhea-predominant symptoms with dosing adjustment
       - Osmotic laxatives (polyethylene glycol) for constipation components
       - Simethicone for gas-related bloating and abdominal distension
       - Probiotics and prebiotics for overall gut health improvement
    
    4. Advanced Therapeutic Considerations:
       - Tricyclic antidepressants for pain modulation and bowel regulation
       - SSRIs for anxiety, depression, and gut-brain axis modulation
       - Rifaximin for suspected small intestinal bacterial overgrowth
       - Prescription medications targeting specific symptom patterns
       - Psychological interventions for stress management and coping
    
    5. Behavioral and Lifestyle Interventions:
       - Stress reduction techniques including mindfulness and meditation
       - Regular exercise program appropriate for functional status
       - Sleep hygiene and adequate rest for symptom management
       - Cognitive-behavioral therapy for chronic symptom coping
       - Support groups for patients with functional gastrointestinal disorders
    
    Negative Diagnosis Evaluation and Next Steps:
    
    1. Specific Functional Disorder Assessment:
       - If IBS criteria met: implement IBS-specific management protocols
       - If functional constipation: constipation-focused treatment approach
       - If functional diarrhea: diarrhea-specific interventions and evaluation
       - If functional bloating: bloating-targeted therapy and dietary modifications
    
    2. Alarm Symptom Investigation Protocols:
       - GI bleeding: urgent gastroenterology consultation and endoscopic evaluation
       - Iron deficiency anemia: comprehensive evaluation including bidirectional endoscopy
       - Unintentional weight loss: imaging studies and malignancy screening
       - Palpable masses/lymphadenopathy: tissue diagnosis and staging evaluation
       - Family history concerns: genetic counseling and enhanced screening protocols
       - Age >50 without screening: colonoscopy evaluation per current guidelines
       - Sudden bowel habit changes: comprehensive organic disease evaluation
    
    3. Temporal Criteria and Follow-up Requirements:
       - Symptoms <3 months duration: symptomatic management and reassessment
       - Recent symptom onset: evaluation for acute conditions and infections
       - Documentation of symptom evolution and response to interventions
       - Regular follow-up to monitor for development of specific criteria
    
    Prognosis and Long-term Management:
    
    Expected Clinical Course:
    - Variable response to treatment depending on symptom pattern complexity
    - Many patients benefit from multimodal management approach
    - Symptoms typically fluctuate with stress, diet, and life circumstances
    - Overall good prognosis with appropriate symptom-directed management
    - Quality of life improvement is the primary therapeutic goal
    
    Follow-up and Monitoring Requirements:
    - Regular assessment of treatment response and symptom evolution
    - Monitoring for development of alarm symptoms requiring investigation
    - Periodic reassessment of diagnosis as symptoms may change over time
    - Adjustment of therapeutic interventions based on symptom patterns
    - Consideration of specialist referral for refractory or complex cases
    
    Quality Assurance and Documentation:
    - Comprehensive documentation of diagnostic criteria assessment
    - Clear rationale for excluding other functional and organic disorders
    - Treatment plan with specific interventions and monitoring schedule
    - Patient education documentation and shared decision-making
    - Coordination with primary care and specialist providers as needed
    
    Args:
        request: Rome IV diagnostic criteria assessment parameters for unspecified functional bowel disorder
        
    Returns:
        RomeIvUnspecifiedFunctionalBowelDisorderResponse: Diagnostic outcome with comprehensive management guidance
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("rome_iv_unspecified_functional_bowel_disorder", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error applying Rome IV diagnostic criteria for unspecified functional bowel disorder",
                    "details": {"parameters": parameters}
                }
            )
        
        return RomeIvUnspecifiedFunctionalBowelDisorderResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Rome IV unspecified functional bowel disorder assessment",
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
                "message": "Internal error in Rome IV unspecified functional bowel disorder diagnostic assessment",
                "details": {"error": str(e)}
            }
        )