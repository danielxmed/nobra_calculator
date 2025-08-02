"""
Murray Score for Acute Lung Injury Models

Request and response models for Murray Score calculation.

References (Vancouver style):
1. Murray JF, Matthay MA, Luce JM, Flick MR. An expanded definition of the adult 
   respiratory distress syndrome. Am Rev Respir Dis. 1988;138(3):720-3. 
   doi: 10.1164/ajrccm/138.3.720.
2. Bernard GR, Artigas A, Brigham KL, Carlet J, Falke K, Hudson L, et al. 
   The American-European Consensus Conference on ARDS. Definitions, mechanisms, 
   relevant outcomes, and clinical trial coordination. Am J Respir Crit Care Med. 
   1994;149(3 Pt 1):818-24. doi: 10.1164/ajrccm.149.3.7509706.
3. Peek GJ, Mugford M, Tiruvoipati R, Wilson A, Allen E, Thalanany MM, et al. 
   Efficacy and economic assessment of conventional ventilatory support versus 
   extracorporeal membrane oxygenation for severe adult respiratory failure (CESAR): 
   a multicentre randomised controlled trial. Lancet. 2009;374(9698):1351-63. 
   doi: 10.1016/S0140-6736(09)61069-2.

The Murray Score is a validated tool for stratifying acute lung injury severity 
and ARDS, providing objective assessment using four physiological parameters: 
chest X-ray consolidation, oxygenation deficit, PEEP requirements, and lung compliance.
"""

from pydantic import BaseModel, Field
from typing import Literal


class MurrayScoreRequest(BaseModel):
    """
    Request model for Murray Score for Acute Lung Injury
    
    The Murray Score stratifies severity of acute lung injury (ALI) and acute respiratory 
    distress syndrome (ARDS) using four objective physiological parameters:
    
    1. Chest X-ray Score (0-4 points):
    - Systematic evaluation of all four lung quadrants for alveolar consolidation
    - 0 points: No consolidation in any quadrant
    - 1 point: Consolidation confined to one quadrant only
    - 2 points: Consolidation present in two quadrants
    - 3 points: Consolidation present in three quadrants  
    - 4 points: Consolidation present in all four quadrants
    - Reflects extent of lung parenchymal involvement and disease severity
    
    2. Hypoxemia Score (0-4 points):
    - Based on PaO2/FiO2 ratio from arterial blood gas analysis
    - 0 points: PaO2/FiO2 ≥300 (normal oxygenation)
    - 1 point: PaO2/FiO2 225-299 (mild hypoxemia)
    - 2 points: PaO2/FiO2 175-224 (moderate hypoxemia)
    - 3 points: PaO2/FiO2 100-174 (severe hypoxemia)
    - 4 points: PaO2/FiO2 <100 (life-threatening hypoxemia)
    - Primary indicator of gas exchange impairment and lung function
    
    3. PEEP Score (0-4 points):
    - Based on positive end-expiratory pressure requirements for adequate oxygenation
    - 0 points: PEEP ≤5 cmH2O (minimal support required)
    - 1 point: PEEP 6-8 cmH2O (mild support required)
    - 2 points: PEEP 9-11 cmH2O (moderate support required)
    - 3 points: PEEP 12-14 cmH2O (high support required)
    - 4 points: PEEP ≥15 cmH2O (very high support required)
    - Reflects severity of lung collapse and recruitment needs
    
    4. Lung Compliance Score (0-4 points):
    - Based on static respiratory system compliance when available
    - 0 points: Compliance ≥80 mL/cmH2O (normal compliance)
    - 1 point: Compliance 60-79 mL/cmH2O (mildly reduced)
    - 2 points: Compliance 40-59 mL/cmH2O (moderately reduced)
    - 3 points: Compliance 20-39 mL/cmH2O (severely reduced)
    - 4 points: Compliance ≤19 mL/cmH2O (critically reduced)
    - Measures lung stiffness and reflects severity of lung injury
    
    Murray Score Calculation:
    Final score = (Chest X-ray + Hypoxemia + PEEP + Compliance) / 4
    
    Clinical Interpretation and Applications:
    
    No Lung Injury (Score <1.0):
    - No evidence of acute lung injury requiring specific interventions
    - Standard respiratory care and monitoring sufficient
    - ECMO not indicated based on lung injury severity
    - Continue routine care with clinical reassessment as needed
    
    Mild to Moderate Lung Injury (Score 1.0-2.4):
    - Acute lung injury present requiring supportive care measures
    - Implement lung-protective ventilation strategies (low tidal volume)
    - Monitor for progression and adjust ventilator settings accordingly
    - ECMO generally not indicated unless other critical factors present
    - Good potential for recovery with appropriate management
    
    Severe Lung Injury (Score 2.5-2.9):
    - Severe acute lung injury consistent with ARDS diagnosis
    - Implement comprehensive lung-protective ventilation protocols
    - Consider advanced therapies: prone positioning, recruitment maneuvers
    - ECMO evaluation may be appropriate in select refractory cases
    - Requires intensive monitoring and aggressive supportive care
    
    Very Severe Lung Injury (Score ≥3.0):
    - Very severe acute lung injury with poor prognosis
    - Maximize all available lung-protective and rescue therapies
    - Strong consideration for ECMO in appropriate candidates
    - Multidisciplinary care with family counseling regarding prognosis
    - High mortality risk despite aggressive intervention
    
    ECMO Selection Criteria:
    - Murray Score ≥3.0 has historically been used as one criterion for ECMO candidacy
    - Should be combined with other clinical factors and institutional protocols
    - Consider patient age, comorbidities, and overall prognosis
    - Ensure availability of experienced ECMO center and transport capabilities
    
    Clinical Limitations and Considerations:
    - Score may vary over time as patient condition evolves during treatment
    - Not a standalone decision tool but one component of comprehensive assessment
    - Requires accurate measurement of all physiological parameters
    - Should be interpreted in context of overall clinical picture
    - May not capture all aspects of lung injury severity or patient prognosis
    
    Research and Quality Applications:
    - Originally developed for standardizing ARDS research protocols
    - Useful for comparing patient populations in clinical studies
    - Can track disease progression and response to interventions over time
    - Helps standardize communication between healthcare providers
    - Facilitates quality improvement initiatives in critical care
    
    References (Vancouver style):
    1. Murray JF, Matthay MA, Luce JM, Flick MR. An expanded definition of the adult 
    respiratory distress syndrome. Am Rev Respir Dis. 1988;138(3):720-3. 
    doi: 10.1164/ajrccm/138.3.720.
    2. Bernard GR, Artigas A, Brigham KL, Carlet J, Falke K, Hudson L, et al. 
    The American-European Consensus Conference on ARDS. Definitions, mechanisms, 
    relevant outcomes, and clinical trial coordination. Am J Respir Crit Care Med. 
    1994;149(3 Pt 1):818-24. doi: 10.1164/ajrccm.149.3.7509706.
    3. Peek GJ, Mugford M, Tiruvoipati R, Wilson A, Allen E, Thalanany MM, et al. 
    Efficacy and economic assessment of conventional ventilatory support versus 
    extracorporeal membrane oxygenation for severe adult respiratory failure (CESAR): 
    a multicentre randomised controlled trial. Lancet. 2009;374(9698):1351-63. 
    doi: 10.1016/S0140-6736(09)61069-2.
    """
    
    chest_xray_score: Literal[0, 1, 2, 3, 4] = Field(
        ...,
        description="Chest X-ray score based on number of quadrants with alveolar consolidation. 0=no consolidation, 1=1 quadrant, 2=2 quadrants, 3=3 quadrants, 4=all 4 quadrants affected",
        example=2
    )
    
    hypoxemia_score: Literal[0, 1, 2, 3, 4] = Field(
        ...,
        description="Hypoxemia score based on PaO2/FiO2 ratio. 0=≥300, 1=225-299, 2=175-224, 3=100-174, 4=<100. Lower ratios indicate worse oxygenation and higher scores",
        example=3
    )
    
    peep_score: Literal[0, 1, 2, 3, 4] = Field(
        ...,
        description="PEEP score based on positive end-expiratory pressure requirement. 0=≤5 cmH2O, 1=6-8 cmH2O, 2=9-11 cmH2O, 3=12-14 cmH2O, 4=≥15 cmH2O. Higher PEEP indicates more severe lung injury",
        example=2
    )
    
    compliance_score: Literal[0, 1, 2, 3, 4] = Field(
        ...,
        description="Lung compliance score based on static compliance when available. 0=≥80 mL/cmH2O, 1=60-79, 2=40-59, 3=20-39, 4=≤19 mL/cmH2O. Lower compliance indicates stiffer lungs and higher scores",
        example=3
    )
    
    class Config:
        schema_extra = {
            "example": {
                "chest_xray_score": 2,
                "hypoxemia_score": 3,
                "peep_score": 2,
                "compliance_score": 3
            }
        }


class MurrayScoreResponse(BaseModel):
    """
    Response model for Murray Score for Acute Lung Injury
    
    The Murray Score provides objective stratification of acute lung injury severity 
    with specific clinical management recommendations for each severity level:
    
    No Lung Injury (Score <1.0):
    - No evidence of acute lung injury requiring specific interventions
    - Continue standard respiratory care with routine monitoring
    - No indication for advanced ventilatory support or ECMO
    - Regular reassessment if clinical condition changes
    - Good prognosis with standard supportive care
    
    Mild to Moderate Lung Injury (Score 1.0-2.4):
    - Acute lung injury present requiring lung-protective ventilation
    - Implement low tidal volume strategy (6 mL/kg predicted body weight)
    - Maintain plateau pressure <30 cmH2O and appropriate PEEP levels
    - Monitor arterial blood gases and adjust ventilator settings accordingly
    - Close surveillance for progression to more severe injury
    - ECMO generally not indicated unless other critical factors present
    - Good potential for recovery with appropriate supportive care
    
    Severe Lung Injury (Score 2.5-2.9):
    - Severe acute lung injury consistent with ARDS requiring intensive management
    - Strict adherence to lung-protective ventilation protocols
    - Consider prone positioning for 12-16 hours daily if feasible
    - Evaluate for neuromuscular blockade if severe hypoxemia persists
    - Implement conservative fluid management strategies
    - Consider advanced rescue therapies: inhaled nitric oxide, recruitment maneuvers
    - ECMO evaluation may be appropriate in select patients with refractory hypoxemia
    - Multidisciplinary critical care team involvement recommended
    - Guarded prognosis requiring aggressive intervention and close monitoring
    
    Very Severe Lung Injury (Score ≥3.0):
    - Very severe acute lung injury with poor prognosis
    - Maximize all available lung-protective and rescue therapy strategies
    - Ensure optimal prone positioning, neuromuscular blockade, and fluid management
    - Strong consideration for ECMO in appropriate candidates
    - Immediate consultation with ECMO center if not available locally
    - Comprehensive multidisciplinary care planning and family communication
    - Discussion of goals of care and prognosis with patient/family
    - Very poor prognosis with high mortality risk despite aggressive intervention
    
    ECMO Considerations:
    - Murray Score ≥3.0 has been used as one criterion for ECMO candidacy
    - Must be combined with assessment of overall prognosis and patient factors
    - Consider patient age, comorbidities, and likelihood of recovery
    - Ensure experienced ECMO center availability and transport capabilities
    - Timing of ECMO initiation critical for optimal outcomes
    
    Monitoring and Reassessment:
    - Murray Score may change over time as patient condition evolves
    - Serial scoring can help track disease progression and treatment response
    - Reassess score with significant changes in clinical status or ventilator settings
    - Use as one component of comprehensive clinical assessment
    - Document trends to guide treatment decisions and prognostic discussions
    
    Quality Improvement Applications:
    - Standardize communication about lung injury severity between providers
    - Track outcomes by severity category for quality improvement initiatives
    - Compare patient populations in clinical research and quality studies
    - Benchmark institutional performance in ARDS management
    - Facilitate education about lung injury severity assessment
    
    Reference: Murray JF, et al. Am Rev Respir Dis. 1988;138(3):720-3.
    """
    
    result: float = Field(
        ...,
        description="Murray Score calculated as average of four component scores (range 0-4)",
        example=2.5
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for Murray Score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Detailed clinical interpretation with severity assessment and management recommendations",
        example="SEVERE ACUTE LUNG INJURY (ARDS): The Murray Score indicates severe acute lung injury consistent with ARDS requiring intensive management. MANAGEMENT: Implement strict lung-protective ventilation, consider prone positioning for 12-16 hours daily, neuromuscular blockade for 48 hours if severe hypoxemia persists, and conservative fluid management. ADVANCED THERAPIES: Consider inhaled nitric oxide, recruitment maneuvers, or high-frequency oscillatory ventilation in refractory cases. ECMO CONSIDERATION: ECMO evaluation may be appropriate in select patients with refractory hypoxemia despite optimal conventional therapy. PROGNOSIS: Guarded with significant mortality risk requiring aggressive intervention."
    )
    
    stage: str = Field(
        ...,
        description="Lung injury severity category",
        example="Severe Lung Injury"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the severity level",
        example="Severe acute lung injury"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 2.5,
                "unit": "points",
                "interpretation": "SEVERE ACUTE LUNG INJURY (ARDS): The Murray Score indicates severe acute lung injury consistent with ARDS requiring intensive management. MANAGEMENT: Implement strict lung-protective ventilation, consider prone positioning for 12-16 hours daily, neuromuscular blockade for 48 hours if severe hypoxemia persists, and conservative fluid management. ADVANCED THERAPIES: Consider inhaled nitric oxide, recruitment maneuvers, or high-frequency oscillatory ventilation in refractory cases. ECMO CONSIDERATION: ECMO evaluation may be appropriate in select patients with refractory hypoxemia despite optimal conventional therapy. PROGNOSIS: Guarded with significant mortality risk requiring aggressive intervention.",
                "stage": "Severe Lung Injury",
                "stage_description": "Severe acute lung injury"
            }
        }