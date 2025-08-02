"""
Oxygenation Index Models

Request and response models for Oxygenation Index calculation.

References (Vancouver style):
1. Ortega M, Ramos AD, Platzker AC, Atkinson JB, Bowman CM, Laks H, et al. 
   Early prediction of ultimate outcome in newborn infants with severe 
   respiratory failure. J Pediatr. 1988;113(4):744-7. 
   doi: 10.1016/s0022-3476(88)80394-8.
2. Bartlett RH, Roloff DW, Custer JR, Younger JG, Hirschl RB. Extracorporeal 
   life support: the University of Michigan experience. JAMA. 2000;283(7):904-8. 
   doi: 10.1001/jama.283.7.904.
3. ELSO Guidelines for Cardiopulmonary Extracorporeal Life Support. 
   Extracorporeal Life Support Organization (ELSO). Ann Arbor, MI. 2017.

The Oxygenation Index is a validated tool for assessing the severity of respiratory 
failure in pediatric patients and determining the need for extracorporeal membrane 
oxygenation (ECMO). This index quantifies the intensity of ventilatory support 
required to maintain adequate oxygenation.
"""

from pydantic import BaseModel, Field
from typing import Union


class OxygenationIndexRequest(BaseModel):
    """
    Request model for Oxygenation Index calculation
    
    The Oxygenation Index (OI) is a critical assessment tool in pediatric intensive 
    care medicine, specifically designed to evaluate the severity of respiratory 
    failure and guide treatment decisions for patients with acute lung injury and 
    acute respiratory distress syndrome (ARDS). This validated measure serves as 
    a key criterion for determining the appropriateness of extracorporeal membrane 
    oxygenation (ECMO) intervention.
    
    Clinical Context and Importance:
    
    Acute respiratory failure in pediatric patients, particularly neonates, presents 
    unique challenges requiring specialized assessment tools and intervention criteria. 
    The Oxygenation Index provides an objective, standardized method for quantifying 
    the severity of respiratory impairment and predicting patient outcomes, enabling 
    clinicians to make informed decisions about advanced life support interventions.
    
    Historical Development:
    
    The Oxygenation Index was developed by Dr. Robert H. Bartlett and colleagues 
    at the University of Michigan as part of their pioneering work in extracorporeal 
    life support. This tool emerged from the need for objective criteria to identify 
    patients who would benefit from ECMO while avoiding unnecessary exposure to 
    this high-risk intervention in patients who might recover with conventional therapy.
    
    Formula and Calculation:
    
    The Oxygenation Index is calculated using the formula:
    OI = (FiO₂ × Mean Airway Pressure) ÷ PaO₂
    
    Where each component reflects critical aspects of respiratory function:
    
    Fraction of Inspired Oxygen (FiO₂):
    Represents the percentage of oxygen being delivered to the patient, ranging 
    from 21% (room air) to 100% (pure oxygen). Higher FiO₂ requirements indicate 
    more severe respiratory impairment and greater risk of oxygen toxicity with 
    prolonged exposure. FiO₂ is expressed as a percentage but used as a decimal 
    in some calculations.
    
    Mean Airway Pressure (PAW):
    Reflects the average pressure applied to the airways throughout the respiratory 
    cycle during mechanical ventilation. This parameter encompasses both peak 
    inspiratory pressure and positive end-expiratory pressure (PEEP), providing 
    a comprehensive measure of ventilatory support intensity. Higher mean airway 
    pressures indicate more aggressive ventilatory support and greater risk of 
    ventilator-induced lung injury.
    
    Partial Pressure of Arterial Oxygen (PaO₂):
    Measures the effectiveness of oxygen transfer from the lungs to the bloodstream. 
    Lower PaO₂ values despite high FiO₂ and ventilatory support indicate severe 
    impairment in gas exchange, often due to ventilation-perfusion mismatch, 
    intrapulmonary shunting, or diffusion abnormalities.
    
    Clinical Interpretation and Thresholds:
    
    The Oxygenation Index provides stratified risk assessment based on established 
    thresholds validated through extensive clinical research:
    
    OI < 25 (Good Outcome):
    - Mortality Risk: Low (<20%)
    - Clinical Significance: Mild to moderate respiratory failure
    - Management: Conventional mechanical ventilation likely sufficient
    - Prognosis: Excellent recovery potential with standard care
    - Monitoring: Regular assessment for improvement trends
    
    OI 25-40 (High Risk):
    - Mortality Risk: Significant (>40%)
    - Clinical Significance: Moderate to severe respiratory failure
    - Management: Optimize conventional therapy, consider advanced strategies
    - Interventions: High-frequency oscillatory ventilation, inhaled nitric oxide
    - Monitoring: Frequent reassessment, preparation for potential ECMO
    
    OI ≥40 (ECMO Consideration):
    - Mortality Risk: Very High (>80% without ECMO)
    - Clinical Significance: Severe respiratory failure with conventional therapy failure
    - Management: Strong indication for ECMO evaluation and implementation
    - Criteria: Sustained OI ≥40 (typically 3 of 5 measurements over 30-60 minutes)
    - Timing: Early intervention associated with better outcomes
    
    ECMO Decision-Making:
    
    The Oxygenation Index serves as a primary criterion in ECMO decision algorithms:
    
    Traditional Criteria:
    The original criteria established by Bartlett and colleagues require an OI >40 
    sustained over multiple measurements to minimize false positives and ensure 
    that patients have truly refractory respiratory failure. This approach prevents 
    premature ECMO initiation in patients who might still respond to conventional therapy.
    
    Modern Applications:
    Contemporary ECMO centers often use OI in combination with other factors including:
    - Duration of mechanical ventilation
    - Reversibility of underlying condition
    - Presence of contraindications
    - Overall clinical trajectory
    - Institutional experience and resources
    
    Timing Considerations:
    Research has demonstrated that earlier ECMO initiation, guided by OI trends 
    rather than waiting for extreme values, may improve outcomes. This has led 
    to more proactive approaches in many centers.
    
    Clinical Applications Beyond ECMO:
    
    Research and Clinical Trials:
    The OI serves as a standardized outcome measure in pediatric respiratory 
    failure research, enabling comparison across studies and assessment of 
    treatment effectiveness for various interventions.
    
    Quality Improvement:
    Healthcare institutions use OI trends to evaluate the effectiveness of 
    respiratory care protocols and identify opportunities for process improvement 
    in managing critically ill children.
    
    Resource Allocation:
    OI values help predict resource utilization, length of stay, and the need 
    for specialized interventions, supporting healthcare planning and cost 
    management decisions.
    
    Limitations and Considerations:
    
    Age-Specific Validation:
    While primarily validated in neonates and infants, the OI has shown utility 
    across pediatric age groups, though threshold values may require adjustment 
    for different populations.
    
    Disease-Specific Factors:
    Certain conditions (congenital diaphragmatic hernia, persistent pulmonary 
    hypertension) may require modified interpretation due to unique pathophysiology.
    
    Technical Considerations:
    Accurate calculation requires precise measurement of arterial blood gases, 
    ventilator parameters, and consistent timing of assessments relative to 
    ventilator changes.
    
    Alternative Indices:
    
    Oxygen Saturation Index (OSI):
    For patients without arterial access, the OSI uses oxygen saturation instead 
    of PaO₂: OSI = (FiO₂ × Mean Airway Pressure) ÷ SpO₂
    An OSI >17.4 has been proposed as equivalent to OI >40 for ECMO consideration.
    
    Ventilation Index (VI):
    Assesses CO₂ removal efficiency: VI = (PaCO₂ × Rate × PIP - PEEP) ÷ 1000
    Used in conjunction with OI for comprehensive respiratory failure assessment.
    
    Best Practices for Implementation:
    
    Standardized Protocols:
    Institutions should establish clear protocols for OI calculation timing, 
    measurement techniques, and decision-making algorithms to ensure consistent 
    application and optimal patient outcomes.
    
    Multidisciplinary Teams:
    ECMO decisions based on OI should involve multidisciplinary teams including 
    intensivists, surgeons, respiratory therapists, and ECMO specialists to 
    ensure comprehensive patient evaluation.
    
    Family Communication:
    OI values and their implications should be clearly communicated to families 
    as part of shared decision-making processes regarding advanced life support 
    interventions.
    
    References (Vancouver style):
    1. Ortega M, Ramos AD, Platzker AC, Atkinson JB, Bowman CM, Laks H, et al. 
    Early prediction of ultimate outcome in newborn infants with severe 
    respiratory failure. J Pediatr. 1988;113(4):744-7. 
    doi: 10.1016/s0022-3476(88)80394-8.
    2. Bartlett RH, Roloff DW, Custer JR, Younger JG, Hirschl RB. Extracorporeal 
    life support: the University of Michigan experience. JAMA. 2000;283(7):904-8. 
    doi: 10.1001/jama.283.7.904.
    3. ELSO Guidelines for Cardiopulmonary Extracorporeal Life Support. 
    Extracorporeal Life Support Organization (ELSO). Ann Arbor, MI. 2017.
    """
    
    fio2: float = Field(
        ...,
        ge=21.0,
        le=100.0,
        description="Fraction of inspired oxygen (FiO2) as percentage. Range: 21% (room air) to 100% (pure oxygen). Higher values indicate more severe respiratory impairment requiring greater oxygen supplementation",
        example=80.0
    )
    
    mean_airway_pressure: float = Field(
        ...,
        ge=1.0,
        le=50.0,
        description="Mean airway pressure (PAW) in cmH2O during mechanical ventilation. Represents average pressure applied throughout respiratory cycle including PEEP and peak pressures. Higher values indicate more intensive ventilatory support",
        example=15.0
    )
    
    pao2: float = Field(
        ...,
        ge=20.0,
        le=600.0,
        description="Partial pressure of arterial oxygen (PaO2) in mmHg from arterial blood gas analysis. Measures effectiveness of oxygen transfer from lungs to blood. Lower values despite high support indicate severe gas exchange impairment",
        example=60.0
    )
    
    class Config:
        schema_extra = {
            "example": {
                "fio2": 80.0,
                "mean_airway_pressure": 15.0,
                "pao2": 60.0
            }
        }


class OxygenationIndexResponse(BaseModel):
    """
    Response model for Oxygenation Index calculation
    
    The Oxygenation Index response provides critical assessment of respiratory 
    failure severity and comprehensive guidance for clinical decision-making, 
    particularly regarding the need for extracorporeal membrane oxygenation (ECMO) 
    and other advanced respiratory support interventions.
    
    Clinical Interpretation and Management Guidelines:
    
    Good Outcome (OI <25):
    - Clinical Significance: Mild to moderate respiratory failure with good prognosis
    - Mortality Risk: Low (<20%) with conventional therapy
    - Management Strategy: Continue current ventilatory support with standard care
    - Monitoring: Regular assessment for improvement, consider weaning parameters
    - Interventions: Optimize lung protective ventilation, supportive care
    - Prognosis: Excellent recovery potential with conventional management
    - Timeline: Most patients show improvement within 72-96 hours
    
    High Risk (OI 25-40):
    - Clinical Significance: Moderate to severe respiratory failure requiring optimization
    - Mortality Risk: Significant (>40%) without intervention escalation
    - Management Strategy: Aggressive optimization of conventional therapy
    - Advanced Interventions: Consider high-frequency oscillatory ventilation (HFOV), 
      inhaled nitric oxide (iNO), prone positioning, neuromuscular blockade
    - ECMO Preparation: Initiate consultation with ECMO center for guidance
    - Monitoring: Frequent reassessment every 4-6 hours, trending analysis
    - Family Communication: Discuss potential need for advanced interventions
    
    ECMO Consideration (OI ≥40):
    - Clinical Significance: Severe refractory respiratory failure
    - Mortality Risk: Very high (>80%) without ECMO intervention
    - Immediate Actions: Urgent ECMO center consultation and evaluation
    - Standard Criteria: Sustained OI ≥40 (3 of 5 measurements over 30-60 minutes)
    - Transfer Considerations: Arrange urgent transport to ECMO-capable facility
    - Bridge Therapy: Optimize current support while arranging ECMO
    - Timing: Early intervention associated with improved outcomes
    - Team Coordination: Multidisciplinary ECMO team activation
    
    ECMO Implementation Considerations:
    
    Patient Selection Criteria:
    - Reversible underlying pathology
    - Absence of significant comorbidities
    - Appropriate weight and size for available circuits
    - Family agreement with intervention goals
    - Institutional experience and resources
    
    Technical Preparations:
    - Vascular access planning (arterial and venous cannulation sites)
    - Circuit priming and equipment checks
    - Staffing allocation (perfusionist, ECMO specialist, intensivist)
    - Laboratory monitoring protocols
    - Anticoagulation management strategies
    
    Alternative Assessment Tools:
    
    Oxygen Saturation Index (OSI):
    For patients without reliable arterial access:
    OSI = (FiO₂ × Mean Airway Pressure) ÷ SpO₂
    Threshold: OSI >17.4 equivalent to OI >40 for ECMO consideration
    
    Ventilation Index (VI):
    For assessment of CO₂ removal:
    VI = (PaCO₂ × Rate × [PIP - PEEP]) ÷ 1000
    Used complementary to OI for comprehensive assessment
    
    Quality Metrics and Monitoring:
    
    Serial Assessment:
    - Trend analysis more valuable than single measurements
    - Consider 4-6 hour intervals for trending
    - Document response to interventions
    - Assess for improvement or deterioration patterns
    
    Outcome Predictors:
    - Duration of high OI values
    - Response to conventional therapy optimization
    - Underlying disease reversibility
    - Associated organ dysfunction
    
    Institutional Protocols:
    
    ECMO Activation Pathways:
    - Clear escalation protocols and contact procedures
    - Standardized evaluation criteria and contraindications
    - Transfer agreements with ECMO centers
    - Family consent and counseling procedures
    
    Quality Assurance:
    - Regular review of OI-based decisions and outcomes
    - Validation of calculation accuracy and timing
    - Correlation with other severity scores
    - Continuous protocol refinement based on outcomes
    
    Multidisciplinary Considerations:
    
    Respiratory Therapy:
    - Ventilator optimization strategies
    - Alternative mode trials (HFOV, APRV)
    - Recruitment maneuvers and PEEP titration
    - Equipment preparation for transport
    
    Critical Care Medicine:
    - Hemodynamic optimization
    - Sedation and paralysis management
    - Nutrition and metabolic support
    - Infection prevention and treatment
    
    Surgery/ECMO Team:
    - Cannulation planning and execution
    - Circuit management and troubleshooting
    - Anticoagulation protocols
    - Weaning strategies and decannulation
    
    Reference: Ortega M, et al. J Pediatr. 1988;113(4):744-7.
    """
    
    result: float = Field(
        ...,
        description="Calculated Oxygenation Index value indicating severity of respiratory failure",
        example=20.0
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the index",
        example="index"
    )
    
    interpretation: str = Field(
        ...,
        description="Detailed clinical interpretation with management recommendations and ECMO guidance",
        example="GOOD OUTCOME PREDICTED (OI: 20.0): Low-risk respiratory failure with good prognosis. MANAGEMENT: Continue conventional mechanical ventilation and standard medical management. Monitor closely for improvement. PROGNOSIS: Excellent with conventional therapy. Weaning and extubation planning appropriate. MONITORING: Serial OI measurements to track progress. Consider lung protective ventilation strategies and supportive care optimization."
    )
    
    stage: str = Field(
        ...,
        description="Risk stratification category",
        example="Good Outcome"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the risk level",
        example="Low risk respiratory failure"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 20.0,
                "unit": "index",
                "interpretation": "GOOD OUTCOME PREDICTED (OI: 20.0): Low-risk respiratory failure with good prognosis. MANAGEMENT: Continue conventional mechanical ventilation and standard medical management. Monitor closely for improvement. PROGNOSIS: Excellent with conventional therapy. Weaning and extubation planning appropriate. MONITORING: Serial OI measurements to track progress. Consider lung protective ventilation strategies and supportive care optimization.",
                "stage": "Good Outcome",
                "stage_description": "Low risk respiratory failure"
            }
        }