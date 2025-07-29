"""
Blast Lung Injury Severity Score Models

Request and response models for Blast Lung Injury Severity Score calculation.

References (Vancouver style):
1. Pizov R, Oppenheim-Eden A, Matot I, Weiss YG, Eidelman LA, Rivkind AI, et al. 
   Blast lung injury from an explosion on a civilian bus. Chest. 1999 Jan;115(1):165-72. 
   doi: 10.1378/chest.115.1.165.
2. Leibovici D, Gofrit ON, Stein M, Shapira SC, Noga Y, Heruti RJ, et al. 
   Blast injuries: bus versus open-air bombings--a comparative study of injuries 
   in survivors of open-air versus confined-space explosions. J Trauma. 1996 Dec;41(6):1030-5. 
   doi: 10.1097/00005373-199612000-00015.
3. Wolf SJ, Bebarta VS, Bonnett CJ, Pons PT, Cantrill SV. Blast injuries. 
   Lancet. 2009 Jul 18;374(9687):405-15. doi: 10.1016/S0140-6736(09)60257-9.

The Blast Lung Injury Severity Score was developed by Pizov and colleagues in 1999 
to standardize the assessment and management of primary blast lung injury (PBLI). 
This scoring system emerged from the need to systematically evaluate patients 
exposed to explosive devices and predict their clinical course.

Primary blast lung injury results from the direct effect of high-intensity pressure 
waves on lung tissue, causing alveolar rupture, hemorrhage, and air embolism. 
Unlike secondary blast injuries (penetrating trauma from debris) or tertiary 
injuries (blunt trauma from displacement), PBLI is specifically caused by the 
pressure differential across the alveolar-capillary membrane.

The score evaluates three critical parameters: oxygenation status (PaO₂/FiO₂ ratio), 
radiographic findings (chest X-ray infiltrate pattern), and presence of bronchial 
pleural fistula. These components effectively stratify patients into mild, moderate, 
and severe categories with distinct prognostic implications and treatment recommendations.

This scoring system has proven particularly valuable in both military and civilian 
settings, providing emergency physicians, trauma surgeons, and intensivists with 
evidence-based guidance for respiratory management of blast injury victims.
"""

from pydantic import BaseModel, Field
from typing import Literal


class BlastLungInjurySeverityRequest(BaseModel):
    """
    Request model for Blast Lung Injury Severity Score
    
    The Blast Lung Injury Severity Score evaluates three key parameters in patients 
    with suspected primary blast lung injury (PBLI):
    
    **1. PaO₂/FiO₂ Ratio (Oxygenation Index):**
    - **>200 mmHg (0 points)**: Normal oxygenation, minimal lung injury
    - **60-200 mmHg (1 point)**: Moderate oxygenation impairment, significant lung injury
    - **<60 mmHg (2 points)**: Severe oxygenation failure, extensive lung damage
    
    **Clinical Significance**: The PaO₂/FiO₂ ratio is the most sensitive indicator of 
    blast lung injury severity. It reflects the degree of ventilation-perfusion mismatch 
    and alveolar-capillary membrane disruption caused by the pressure wave.
    
    **2. Chest X-ray Findings (Radiographic Pattern):**
    - **Localized infiltrates (0 points)**: Limited lung involvement, focal injury
    - **Bilateral/unilateral infiltrates (1 point)**: Moderate lung involvement
    - **Massive bilateral infiltrates (2 points)**: Extensive bilateral lung injury
    
    **Clinical Significance**: Chest X-ray findings correlate with the extent of 
    alveolar damage and predict the need for mechanical ventilation. Bilateral 
    infiltrates indicate more severe injury with higher risk of ARDS development.
    
    **3. Bronchial Pleural Fistula:**
    - **Absent (0 points)**: No abnormal airway-pleural communication
    - **Present (1 point)**: Abnormal connection between airways and pleural space
    
    **Clinical Significance**: Bronchial pleural fistula results from rupture of 
    alveolar walls and indicates severe structural lung damage. Its presence 
    significantly complicates ventilatory management and increases mortality risk.
    
    **Assessment Guidelines:**
    
    **Timing**: Most effective when applied within 2 hours of blast injury, as 
    delayed assessment may not accurately reflect the initial injury severity.
    
    **Patient Selection**: Primarily used for patients with respiratory symptoms 
    following blast exposure, including dyspnea, chest pain, hemoptysis, or 
    abnormal vital signs.
    
    **Technical Considerations**:
    - PaO₂/FiO₂ ratio should be calculated from arterial blood gas on room air 
      or known FiO₂
    - Chest X-ray should be performed in standard PA/lateral views when possible
    - Bronchial pleural fistula may be evident on chest X-ray or CT scan
    
    References (Vancouver style):
    1. Pizov R, Oppenheim-Eden A, Matot I, Weiss YG, Eidelman LA, Rivkind AI, et al. 
    Blast lung injury from an explosion on a civilian bus. Chest. 1999 Jan;115(1):165-72. 
    doi: 10.1378/chest.115.1.165.
    2. Leibovici D, Gofrit ON, Stein M, Shapira SC, Noga Y, Heruti RJ, et al. 
    Blast injuries: bus versus open-air bombings--a comparative study of injuries 
    in survivors of open-air versus confined-space explosions. J Trauma. 1996 Dec;41(6):1030-5. 
    doi: 10.1097/00005373-199612000-00015.
    3. Wolf SJ, Bebarta VS, Bonnett CJ, Pons PT, Cantrill SV. Blast injuries. 
    Lancet. 2009 Jul 18;374(9687):405-15. doi: 10.1016/S0140-6736(09)60257-9.
    """
    
    pao2_fio2_ratio: float = Field(
        ...,
        ge=20,
        le=500,
        description="PaO₂/FiO₂ ratio in mmHg. >200=0 points, 60-200=1 point, <60=2 points. Key indicator of oxygenation status and lung injury severity.",
        example=150.0
    )
    
    chest_xray_findings: Literal["localized", "bilateral_or_unilateral", "massive_bilateral"] = Field(
        ...,
        description="Chest X-ray infiltrate pattern. Localized=0 points, bilateral or unilateral=1 point, massive bilateral=2 points.",
        example="bilateral_or_unilateral"
    )
    
    bronchial_pleural_fistula: Literal["no", "yes"] = Field(
        ...,
        description="Presence of bronchial pleural fistula (abnormal airway-pleural communication). No=0 points, Yes=1 point.",
        example="no"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "pao2_fio2_ratio": 150.0,
                "chest_xray_findings": "bilateral_or_unilateral",
                "bronchial_pleural_fistula": "no"
            }
        }


class BlastLungInjurySeverityResponse(BaseModel):
    """
    Response model for Blast Lung Injury Severity Score
    
    The score ranges from 0-5 points and classifies blast lung injury severity:
    
    **Mild (0 points)**:
    - ARDS Risk: ~0%
    - Mortality: ~0%
    - Ventilation: Volume-controlled or pressure support ventilation
    - PEEP: ≤5 cm H₂O
    - Management: Standard respiratory monitoring and supportive care
    
    **Moderate (1-4 points)**:
    - ARDS Risk: 33%
    - Mortality: ~0%
    - Ventilation: Conventional modes, consider inverse-ratio ventilation if needed
    - PEEP: 5-10 cm H₂O
    - Management: Close respiratory monitoring, lung-protective ventilation
    
    **Severe (5 points)**:
    - ARDS Risk: 100%
    - Mortality: 75%
    - Ventilation: Conventional modes with potential advanced therapies
    - PEEP: >10 cm H₂O
    - Advanced therapies: Consider nitric oxide, high-frequency jet ventilation, 
      independent lung ventilation, or ECMO
    
    **Clinical Management Implications:**
    
    The score directly guides ventilatory management strategies and helps predict 
    clinical outcomes. Higher scores indicate need for more aggressive respiratory 
    support and closer monitoring for complications such as pneumothorax, air 
    embolism, and hemoptysis.
    
    Reference: Pizov R, et al. Chest. 1999;115(1):165-72.
    """
    
    result: int = Field(
        ...,
        ge=0,
        le=5,
        description="Blast lung injury severity score calculated from clinical parameters (0-5 points)",
        example=2
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the severity score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation with ventilatory management recommendations based on severity score",
        example="Moderate blast lung injury with intermediate risk. ARDS risk: 33%, Mortality: ~0%. Recommended ventilation: Conventional modes, consider inverse-ratio ventilation if needed. PEEP: 5-10 cm H₂O. Close respiratory monitoring required."
    )
    
    stage: str = Field(
        ...,
        description="Severity category (Mild, Moderate, Severe)",
        example="Moderate"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the severity category",
        example="1-4 points - Moderate blast lung injury"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "result": 2,
                "unit": "points",
                "interpretation": "Moderate blast lung injury with intermediate risk. ARDS risk: 33%, Mortality: ~0%. Recommended ventilation: Conventional modes, consider inverse-ratio ventilation if needed. PEEP: 5-10 cm H₂O. Close respiratory monitoring required.",
                "stage": "Moderate",
                "stage_description": "1-4 points - Moderate blast lung injury"
            }
        }