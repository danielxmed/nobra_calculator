"""
Rome IV Diagnostic Criteria for Reflux Hypersensitivity Router

Endpoint for Rome IV reflux hypersensitivity diagnostic assessment.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.gastroenterology.rome_iv_reflux_hypersensitivity import (
    RomeIvRefluxHypersensitivityRequest,
    RomeIvRefluxHypersensitivityResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/rome_iv_reflux_hypersensitivity",
    response_model=RomeIvRefluxHypersensitivityResponse,
    summary="Rome IV Diagnostic Criteria for Reflux Hypersensitivity",
    description="Applies the official Rome IV diagnostic criteria for reflux hypersensitivity, a functional esophageal "
                "disorder characterized by retrosternal symptoms triggered by normal amounts of gastroesophageal reflux. "
                "This validated diagnostic tool evaluates 6 essential criteria including retrosternal symptoms for ≥3 months "
                "(onset ≥6 months ago, ≥2x/week), normal endoscopy, exclusion of eosinophilic esophagitis and major motor "
                "disorders, normal acid exposure time (<4%) with positive symptom-reflux association on ambulatory pH "
                "monitoring, and absence of alarm symptoms. ALL criteria must be met for positive diagnosis. Distinguished "
                "from GERD by normal acid exposure and from functional heartburn by positive symptom-reflux association. "
                "Essential for accurate classification and targeted treatment of functional esophageal disorders.",
    response_description="Rome IV diagnostic assessment with criteria fulfillment status, clinical interpretation, and multimodal treatment recommendations",
    operation_id="rome_iv_reflux_hypersensitivity"
)
async def calculate_rome_iv_reflux_hypersensitivity(request: RomeIvRefluxHypersensitivityRequest):
    """
    Rome IV Diagnostic Criteria for Reflux Hypersensitivity Assessment
    
    Applies the international standard Rome IV diagnostic criteria for reflux hypersensitivity, 
    a functional esophageal disorder affecting 7-15% of patients with heartburn symptoms. 
    This evidence-based diagnostic framework enables precise identification of patients 
    with heightened esophageal sensitivity to physiologic amounts of gastroesophageal reflux.
    
    Clinical Significance and Diagnostic Utility:
    Reflux hypersensitivity represents a paradigm shift in understanding esophageal 
    disorders, bridging GERD and functional heartburn through recognition of visceral 
    hypersensitivity mechanisms. Accurate diagnosis using Rome IV criteria enables 
    targeted multimodal therapy and avoids ineffective treatments.
    
    Key Diagnostic Features:
    - Normal acid exposure time (<4%) distinguishes from typical GERD
    - Positive symptom-reflux association (SAP >95% or SI >50%) distinguishes from functional heartburn
    - Requires systematic exclusion of structural and motor abnormalities
    - Temporal criteria ensure chronicity and clinical significance
    
    Required Investigations for Diagnosis:
    
    Upper Endoscopy with Biopsy:
    - High-definition endoscopy to exclude erosive esophagitis
    - Esophageal biopsies to rule out eosinophilic esophagitis (<15 eos/hpf)
    - Assessment for Barrett's esophagus and other complications
    - Evaluation for subtle mucosal changes and inflammatory conditions
    
    Esophageal Manometry:
    - High-resolution manometry with Chicago Classification v4.0
    - Exclusion of achalasia, EGJ outflow obstruction, and spastic disorders
    - Assessment of lower esophageal sphincter function and peristalsis
    - Identification of major motor disorders requiring specific management
    
    Ambulatory pH Monitoring:
    - 24-48 hour pH monitoring for acid exposure time calculation
    - Symptom-reflux association analysis using validated metrics
    - Normal acid exposure time <4.0% total recording time
    - pH-impedance monitoring may provide enhanced diagnostic accuracy
    
    Clinical Applications and Treatment Implications:
    
    Positive Diagnosis Management:
    - Acid suppression therapy despite normal acid exposure (PPI once or twice daily)
    - Visceral pain modulators: tricyclic antidepressants, gabapentinoids
    - Psychological interventions: CBT, stress management, relaxation techniques
    - Lifestyle modifications: dietary changes, weight reduction, meal timing
    - Patient education about functional nature and treatment expectations
    
    Negative Diagnosis Evaluation:
    - Systematic evaluation for alternative conditions
    - GERD with abnormal acid exposure (≥4% acid exposure time)
    - Functional heartburn with negative symptom association
    - Eosinophilic esophagitis with characteristic histology
    - Major motor disorders requiring specialized treatment
    - Cardiac evaluation for chest pain as clinically indicated
    
    Differential Diagnosis Considerations:
    - GERD: abnormal acid exposure time, may have erosive changes
    - Functional heartburn: normal acid exposure, negative symptom association
    - Eosinophilic esophagitis: >15 eosinophils/hpf, allergic history
    - Achalasia: impaired LES relaxation, aperistalsis on manometry
    - Cardiac conditions: coronary artery disease, pericarditis
    
    Quality Assurance and Follow-up:
    - Documentation of all diagnostic criteria with supporting evidence
    - Clear treatment plan with realistic expectations for symptom improvement
    - Regular monitoring of therapeutic response and quality of life
    - Reassessment if significant change in clinical presentation
    - Coordination with gastroenterology and other specialists as needed
    
    Args:
        request: Rome IV diagnostic criteria assessment parameters for reflux hypersensitivity
        
    Returns:
        RomeIvRefluxHypersensitivityResponse: Diagnostic outcome with comprehensive clinical guidance
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("rome_iv_reflux_hypersensitivity", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error applying Rome IV diagnostic criteria for reflux hypersensitivity",
                    "details": {"parameters": parameters}
                }
            )
        
        return RomeIvRefluxHypersensitivityResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Rome IV reflux hypersensitivity assessment",
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
                "message": "Internal error in Rome IV reflux hypersensitivity diagnostic assessment",
                "details": {"error": str(e)}
            }
        )