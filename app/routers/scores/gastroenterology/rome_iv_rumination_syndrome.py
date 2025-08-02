"""
Rome IV Diagnostic Criteria for Rumination Syndrome Router

Endpoint for Rome IV rumination syndrome diagnostic assessment.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.gastroenterology.rome_iv_rumination_syndrome import (
    RomeIvRuminationSyndromeRequest,
    RomeIvRuminationSyndromeResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/rome_iv_rumination_syndrome",
    response_model=RomeIvRuminationSyndromeResponse,
    summary="Rome IV Diagnostic Criteria for Rumination Syndrome",
    description="Applies the official Rome IV diagnostic criteria for rumination syndrome, a functional gastroduodenal "
                "disorder characterized by effortless regurgitation of recently ingested food followed by remastication "
                "and reswallowing or expulsion. This validated diagnostic tool evaluates both positive criteria "
                "(persistent regurgitation with remastication for ≥3 months with onset ≥6 months ago, and effortless "
                "regurgitation without retching) and exclusion criteria (absence of GI bleeding, iron deficiency anemia, "
                "heartburn/reflux, weight loss, masses/lymphadenopathy, dysphagia, and persistent vomiting). ALL criteria "
                "must be met for positive diagnosis. Distinguished from GERD by absence of heartburn, from gastroparesis "
                "by normal gastric emptying, and from eating disorders by involuntary nature. Prevalence approximately "
                "3.1% in general population. Treatment primarily involves behavioral interventions with 80-90% success rate.",
    response_description="Rome IV diagnostic assessment with criteria fulfillment status, clinical interpretation, and comprehensive treatment recommendations",
    operation_id="rome_iv_rumination_syndrome"
)
async def calculate_rome_iv_rumination_syndrome(request: RomeIvRuminationSyndromeRequest):
    """
    Rome IV Diagnostic Criteria for Rumination Syndrome Assessment
    
    Applies the international standard Rome IV diagnostic criteria for rumination syndrome, 
    a functional gastroduodenal disorder affecting approximately 3.1% of the general 
    population. This evidence-based diagnostic framework enables precise identification 
    of patients with rumination syndrome through systematic evaluation of positive 
    criteria and exclusion of organic pathology.
    
    Clinical Significance and Diagnostic Utility:
    Rumination syndrome was historically considered rare and primarily affecting infants 
    or individuals with intellectual disabilities. However, recent recognition under 
    Rome IV criteria has revealed significant prevalence in adults. The disorder involves 
    learned voluntary intra-abdominal pressure increases through unconscious contraction 
    of abdominal wall muscles against a closed glottis, creating effortless regurgitation 
    of recently ingested food for remastication and reswallowing.
    
    Key Diagnostic Features:
    - Effortless regurgitation within 10-30 minutes of eating distinguishes from vomiting
    - Pleasant-tasting regurgitated material initially distinguishes from acid reflux
    - Remastication behavior distinguishes from simple regurgitation
    - Temporal criteria (≥3 months, onset ≥6 months ago) ensure chronicity
    - Systematic exclusion of alarm symptoms and organic causes
    
    Rome IV Diagnostic Criteria:
    
    POSITIVE CRITERIA (both required):
    1. Persistent or recurrent regurgitation of recently ingested food into the mouth 
       with subsequent spitting or remastication and swallowing for ≥3 months with 
       onset ≥6 months before diagnosis
    2. Regurgitation is not preceded by retching (effortless regurgitation)
    
    EXCLUSION CRITERIA (all must be absent):
    3. No gastrointestinal bleeding (melena, hematemesis, hematochezia)
    4. No unexplained iron deficiency anemia
    5. No significant heartburn or esophageal reflux symptoms
    6. No unintentional weight loss (>10% body weight over 6 months)
    7. No palpable abdominal mass or lymphadenopathy
    8. No dysphagia (difficulty swallowing solids or liquids)
    9. No persistent vomiting episodes distinct from regurgitation
    
    Pathophysiology and Clinical Characteristics:
    
    Mechanism:
    - Learned voluntary increase in intra-abdominal pressure
    - Unconscious contraction of abdominal wall muscles against closed glottis
    - Creates pressure gradient forcing gastric contents into esophagus and mouth
    - Process typically occurs within 30 minutes of eating
    - Continues until regurgitated material becomes acidic and unpalatable
    
    Temporal Pattern:
    - Postprandial timing distinguishes from nocturnal GERD
    - No symptoms during sleep (nocturnal regurgitation makes diagnosis less likely)
    - May worsen with stress, anxiety, or specific triggering foods
    - Often initially pleasant-tasting material becomes unpalatable when acidified
    
    Behavioral Aspects:
    - Often described as involuntary but effortless process
    - Patients may not be fully aware when regurgitation occurs
    - Social embarrassment may lead to avoidance of public eating
    - Frequently associated with psychological stress or learned responses
    
    Required Clinical Evaluation:
    
    History and Physical Examination:
    - Detailed characterization of regurgitation episodes with meal timing
    - Assessment for alarm symptoms requiring organic evaluation
    - Psychological assessment for underlying stressors or trauma
    - Family history of gastrointestinal or eating disorders
    - Physical examination to exclude masses or lymphadenopathy
    
    Laboratory Studies:
    - Complete blood count to exclude iron deficiency anemia
    - Comprehensive metabolic panel to assess nutritional status
    - Consider B12, folate levels if nutritional deficiency suspected
    - Inflammatory markers (ESR, CRP) if organic disease suspected
    
    Imaging and Endoscopy (if indicated):
    - Upper endoscopy if alarm symptoms present or diagnosis uncertain
    - Excludes erosive esophagitis, malignancy, structural abnormalities
    - Gastric emptying study if gastroparesis suspected (typically normal)
    - Esophageal manometry not routinely required but may show characteristic patterns
    
    Differential Diagnosis Considerations:
    
    Gastroesophageal Reflux Disease (GERD):
    - Heartburn and acid reflux symptoms prominent
    - Regurgitation typically acidic and unpalatable
    - May have erosive esophagitis on endoscopy
    - Responds to acid suppression therapy
    - Often worse in supine position
    
    Gastroparesis:
    - Associated with delayed gastric emptying on scintigraphy
    - Nausea, vomiting, and early satiety prominent
    - Often secondary to diabetes mellitus or other systemic conditions
    - May have bezoar formation or food retention
    
    Eating Disorders (Bulimia Nervosa):
    - Intentional self-induced vomiting for weight control
    - Associated with psychological distress and body image concerns
    - Often secretive behavior with guilt and shame
    - May have dental erosion and electrolyte abnormalities
    
    Achalasia:
    - Primary esophageal motility disorder with progressive dysphagia
    - Chest pain and weight loss common
    - Manometry shows impaired lower esophageal sphincter relaxation
    - Barium swallow shows characteristic bird's beak appearance
    
    Cyclic Vomiting Syndrome:
    - Episodic, stereotypical vomiting episodes with symptom-free intervals
    - Often associated with migraine headaches
    - Typically begins in childhood or adolescence
    - Episodes may last hours to days with complete recovery between
    
    Clinical Applications and Treatment Implications:
    
    Positive Diagnosis Management:
    1. Behavioral Interventions (First-line with 80-90% success rate):
       - Diaphragmatic breathing training to prevent abdominal contractions
       - Habit reversal therapy to identify triggers and alternative behaviors
       - Biofeedback therapy with real-time physiologic monitoring
       - Patient education about functional nature and treatment expectations
    
    2. Dietary Modifications:
       - Smaller, more frequent meals to reduce gastric volume
       - Slower eating with thorough chewing
       - Remaining upright for 1-2 hours after meals
       - Avoiding specific trigger foods or textures as identified
    
    3. Psychological Support:
       - Stress management and relaxation techniques
       - Cognitive-behavioral therapy for anxiety or depression
       - Address underlying psychological stressors when present
       - Family counseling if psychosocial factors identified
    
    Negative Diagnosis Evaluation:
    - Systematic investigation for alternative conditions based on specific criteria not met
    - Upper endoscopy for structural evaluation if alarm symptoms present
    - Gastric emptying study if gastroparesis suspected
    - Psychological evaluation if eating disorder suspected
    - Cardiac evaluation for chest pain as clinically indicated
    
    Prognosis and Follow-up:
    
    Treatment Response:
    - 80-90% of patients respond to behavioral interventions
    - Improvement typically seen within 2-8 weeks of consistent therapy
    - Complete resolution possible in majority of motivated patients
    - Relapse may occur during stress requiring booster sessions
    
    Long-term Outcomes:
    - Generally excellent prognosis with appropriate treatment
    - No increased risk of malignancy or serious complications
    - Quality of life significantly improves with symptom resolution
    - Maintenance of behavioral techniques important for sustained improvement
    
    Quality Assurance and Monitoring:
    - Documentation of all diagnostic criteria with supporting evidence
    - Clear treatment plan with realistic expectations for improvement
    - Regular monitoring of therapeutic response and adherence
    - Reassessment if significant change in clinical presentation
    - Coordination with gastroenterology and behavioral specialists as needed
    
    Args:
        request: Rome IV diagnostic criteria assessment parameters for rumination syndrome
        
    Returns:
        RomeIvRuminationSyndromeResponse: Diagnostic outcome with comprehensive clinical guidance
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("rome_iv_rumination_syndrome", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error applying Rome IV diagnostic criteria for rumination syndrome",
                    "details": {"parameters": parameters}
                }
            )
        
        return RomeIvRuminationSyndromeResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Rome IV rumination syndrome assessment",
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
                "message": "Internal error in Rome IV rumination syndrome diagnostic assessment",
                "details": {"error": str(e)}
            }
        )