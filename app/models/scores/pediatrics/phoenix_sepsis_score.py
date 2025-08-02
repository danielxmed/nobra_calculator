"""
Phoenix Sepsis Score Models

Request and response models for Phoenix Sepsis Score calculation.

References (Vancouver style):
1. Schlapbach LJ, Watson RS, Sorce LR, Argent AC, Menon K, Hartman ME, et al. 
   International Consensus Criteria for Pediatric Sepsis and Septic Shock. 
   JAMA. 2024 Feb 27;331(8):665-674. doi: 10.1001/jama.2024.0179.
2. Watson RS, Schlapbach LJ, Sorce LR, Argent AC, Menon K, Hartman ME, et al. 
   Development and Validation of the Phoenix Criteria for Pediatric Sepsis and 
   Septic Shock. JAMA. 2024 Feb 27;331(8):675-686. doi: 10.1001/jama.2024.0196.
3. SCCM Task Force Develops New Criteria to Identify Pediatric Sepsis. Society 
   of Critical Care Medicine. 2024.

The Phoenix Sepsis Score is the first data-driven international consensus criteria 
for pediatric sepsis and septic shock, developed by the Society of Critical Care 
Medicine (SCCM) Pediatric Sepsis Definition Task Force. Published in JAMA in 
February 2024, it provides a standardized approach to identify potentially 
life-threatening organ dysfunction in children with suspected infection.
"""

from pydantic import BaseModel, Field
from typing import Literal, Dict, Any, Optional


class PhoenixSepsisScoreRequest(BaseModel):
    """
    Request model for Phoenix Sepsis Score
    
    The Phoenix Sepsis Score is a novel pediatric sepsis scoring system that evaluates 
    organ dysfunction across four key domains: respiratory, cardiovascular, coagulation, 
    and neurologic systems. It was developed through a comprehensive process including 
    global clinician surveys, systematic reviews, multicenter electronic health record 
    analysis, and modified Delphi consensus methodology.
    
    **SCIENTIFIC BACKGROUND:**
    
    The Phoenix Sepsis Score represents a paradigm shift from previous pediatric sepsis 
    definitions that relied on systemic inflammatory response syndrome (SIRS) criteria, 
    which had poor predictive value. This new consensus definition aligns pediatric 
    sepsis criteria with adult Sepsis-3 definitions while accounting for age-specific 
    physiological differences in children.
    
    **KEY CLINICAL INNOVATIONS:**
    
    **1. Evidence-Based Development:**
    - First pediatric sepsis criteria derived from mortality outcome data
    - International multicenter validation across diverse healthcare settings
    - Integration of both higher-resource and lower-resource healthcare environments
    
    **2. Organ System Assessment:**
    
    **Respiratory System (0-3 points):**
    - **None/Room Air**: 0 points - normal oxygen requirement
    - **Supplemental Oxygen**: 1 point - low-flow oxygen via nasal cannula or mask
    - **High-Flow Nasal Cannula**: 2 points - heated humidified high-flow oxygen
    - **Non-Invasive Ventilation**: 3 points - BiPAP, CPAP, or other non-invasive support
    - **Invasive Mechanical Ventilation**: 3 points - intubation and mechanical ventilation
    - **Oxygenation Ratios**: PaO₂/FiO₂ or SpO₂/FiO₂ ratios provide additional dysfunction assessment
    
    **Cardiovascular System (0-6 points):**
    - **Vasoactive Medications**: 0 points (none), 1 point (single agent), 2 points (≥2 agents)
    - **Lactate Levels**: 0 points (<5 mmol/L), 1 point (5-10.9 mmol/L), 2 points (≥11 mmol/L)
    - **Mean Arterial Pressure**: Age-specific 5th percentile thresholds for hypotension
    
    **Coagulation System (0-2 points):**
    - **Platelet Count**: <100 ×10³/μL indicates dysfunction
    - **INR**: >1.3 suggests coagulopathy
    - **D-dimer**: Elevated levels indicate fibrinolytic activation
    - **Fibrinogen**: <1.0 g/L suggests consumption or decreased synthesis
    
    **Neurologic System (0-2 points):**
    - **Glasgow Coma Scale**: <11 indicates altered mental status
    - **Pupil Reactivity**: Fixed pupils indicate severe neurologic dysfunction
    
    **3. Age-Specific Considerations:**
    
    **Inclusion Criteria:**
    - Children <18 years of age with suspected or confirmed infection
    - Excludes birth hospitalizations and preterm infants <37 weeks postconceptional age
    
    **Age-Adjusted Parameters:**
    - Mean arterial pressure thresholds adjusted for age-specific normal values
    - Recognition that physiological parameters vary significantly with age in pediatrics
    
    **DIAGNOSTIC CRITERIA:**
    
    **Sepsis Diagnosis:**
    - Phoenix Sepsis Score ≥2 points in the presence of suspected or confirmed infection
    - Indicates potentially life-threatening organ dysfunction
    
    **Septic Shock Diagnosis:**
    - Sepsis (Phoenix score ≥2) PLUS cardiovascular dysfunction (cardiovascular subscore ≥1)
    - Represents the most severe form requiring immediate intensive intervention
    
    **CLINICAL PERFORMANCE:**
    
    **Mortality Prediction:**
    - Higher-resource settings: 7.1% mortality for children meeting sepsis criteria
    - Lower-resource settings: 28.5% mortality for children meeting sepsis criteria
    - More than 8-fold higher mortality compared to children not meeting criteria
    
    **Validation Results:**
    - Superior performance compared to existing pediatric intensive care unit criteria
    - Consistent discrimination across diverse healthcare settings and populations
    - Improved standardization for research and quality improvement initiatives
    
    **CLINICAL APPLICATIONS:**
    
    **Immediate Clinical Care:**
    - Standardized identification of children requiring urgent sepsis management
    - Objective criteria for escalation of care and resource allocation
    - Framework for systematic assessment of organ dysfunction progression
    
    **Quality Improvement:**
    - Standardized definitions for sepsis quality metrics and reporting
    - Benchmarking tool for comparing outcomes across healthcare systems
    - Framework for implementing evidence-based sepsis care bundles
    
    **Research Applications:**
    - Consistent enrollment criteria for pediatric sepsis research studies
    - Standardized outcome measures for intervention studies
    - International collaboration platform for sepsis research
    
    **IMPORTANT CLINICAL CONSIDERATIONS:**
    
    **Limitations:**
    - Not designed as a screening tool for identifying sepsis
    - Requires clinical suspicion of infection for appropriate application
    - Performance may vary in populations not represented in development cohorts
    
    **Implementation Considerations:**
    - Requires healthcare provider education on new criteria
    - Integration with electronic health record systems for automated calculation
    - Coordination with existing sepsis recognition and response protocols
    
    **Future Directions:**
    - Ongoing validation in additional pediatric populations
    - Integration with artificial intelligence and machine learning tools
    - Development of real-time monitoring and alerting systems
    
    References (Vancouver style):
    1. Schlapbach LJ, Watson RS, Sorce LR, et al. JAMA. 2024;331(8):665-674.
    2. Watson RS, Schlapbach LJ, Sorce LR, et al. JAMA. 2024;331(8):675-686.
    3. SCCM Task Force Develops New Criteria to Identify Pediatric Sepsis. 2024.
    """
    
    age: int = Field(
        ...,
        description="Patient age in years. Must be <18 years. Excludes birth hospitalizations and preterm infants with postconceptional age <37 weeks",
        ge=0,
        le=17,
        example=5
    )
    
    suspected_infection: Literal["yes", "no"] = Field(
        ...,
        description="Presence of suspected or confirmed infection. Required for sepsis diagnosis - Phoenix criteria cannot be applied without suspected infection",
        example="yes"
    )
    
    respiratory_support: Literal["none", "supplemental_oxygen", "high_flow_nasal_cannula", "non_invasive_ventilation", "invasive_mechanical_ventilation"] = Field(
        ...,
        description="Current level of respiratory support. Higher levels indicate greater respiratory dysfunction and contribute to respiratory subscore",
        example="supplemental_oxygen"
    )
    
    pao2_fio2_ratio: Optional[float] = Field(
        None,
        description="PaO₂/FiO₂ ratio from arterial blood gas if available. <100 severe dysfunction (3 pts), 100-199 moderate (2 pts), 200-299 mild (1 pt), ≥300 normal (0 pts)",
        ge=0,
        le=800,
        example=250.0
    )
    
    spo2_fio2_ratio: Optional[float] = Field(
        None,
        description="SpO₂/FiO₂ ratio if PaO₂/FiO₂ not available. <150 severe dysfunction (3 pts), 150-219 moderate (2 pts), 220-299 mild (1 pt), ≥300 normal (0 pts)",
        ge=0,
        le=1000,
        example=350.0
    )
    
    vasoactive_medications: int = Field(
        ...,
        description="Number of vasoactive medications currently administered (epinephrine, norepinephrine, dopamine, dobutamine, milrinone, vasopressin, etc.). 0 meds = 0 pts, 1 med = 1 pt, ≥2 meds = 2 pts",
        ge=0,
        le=10,
        example=0
    )
    
    lactate: Optional[float] = Field(
        None,
        description="Serum lactate level in mmol/L. Marker of tissue hypoperfusion and anaerobic metabolism. <5 normal (0 pts), 5-10.9 elevated (1 pt), ≥11 severely elevated (2 pts)",
        ge=0,
        le=50,
        example=3.2
    )
    
    mean_arterial_pressure: Optional[int] = Field(
        None,
        description="Mean arterial pressure in mmHg. Age-specific hypotension thresholds: <1yr: 31mmHg, 1-2yr: 32mmHg, 2-5yr: 32mmHg, 5-12yr: 36mmHg, 12-18yr: 44mmHg. Below threshold = 2 pts",
        ge=20,
        le=200,
        example=75
    )
    
    platelets: Optional[int] = Field(
        None,
        description="Platelet count in ×10³/μL. Reflects coagulation system function and bone marrow response. <100 ×10³/μL indicates thrombocytopenia and scores 1 point",
        ge=0,
        le=1000,
        example=250
    )
    
    inr: Optional[float] = Field(
        None,
        description="International normalized ratio. Measures coagulation cascade function, particularly extrinsic pathway. >1.3 indicates coagulopathy and scores 1 point",
        ge=0.5,
        le=10.0,
        example=1.1
    )
    
    d_dimer: Optional[float] = Field(
        None,
        description="D-dimer level in mg/L FEU (fibrinogen equivalent units). Marker of fibrinolytic system activation. Elevated levels (>2.0 mg/L) suggest ongoing coagulation activation",
        ge=0,
        le=100,
        example=1.5
    )
    
    fibrinogen: Optional[float] = Field(
        None,
        description="Fibrinogen level in g/L. Essential coagulation protein and acute phase reactant. <1.0 g/L indicates consumption, decreased synthesis, or severe dysfunction",
        ge=0,
        le=10,
        example=2.8
    )
    
    glasgow_coma_scale: int = Field(
        ...,
        description="Glasgow Coma Scale score (3-15). Age-appropriate assessment of consciousness level. <11 indicates altered mental status and neurologic dysfunction (1 point)",
        ge=3,
        le=15,
        example=15
    )
    
    pupil_reactivity: Literal["both_reactive", "one_fixed", "both_fixed"] = Field(
        ...,
        description="Pupil reactivity to light. Both reactive = normal (0 pts), one fixed = asymmetric dysfunction (1 pt), both fixed = severe bilateral dysfunction (2 pts)",
        example="both_reactive"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "age": 5,
                "suspected_infection": "yes",
                "respiratory_support": "supplemental_oxygen",
                "pao2_fio2_ratio": 250.0,
                "spo2_fio2_ratio": None,
                "vasoactive_medications": 0,
                "lactate": 3.2,
                "mean_arterial_pressure": 75,
                "platelets": 250,
                "inr": 1.1,
                "d_dimer": 1.5,
                "fibrinogen": 2.8,
                "glasgow_coma_scale": 15,
                "pupil_reactivity": "both_reactive"
            }
        }


class PhoenixSepsisScoreResponse(BaseModel):
    """
    Response model for Phoenix Sepsis Score
    
    The Phoenix Sepsis Score provides standardized assessment of organ dysfunction 
    in pediatric patients with suspected infection. The response includes the total 
    score, component subscores, clinical diagnostic interpretation, and management 
    recommendations based on international consensus criteria.
    
    **SCORE INTERPRETATION:**
    
    **Total Score Range:** 0-13 points (sum of all organ system subscores)
    
    **Diagnostic Thresholds:**
    - **<2 points**: Does not meet sepsis criteria
    - **≥2 points**: Meets sepsis criteria (with suspected infection)
    - **≥2 points + cardiovascular subscore ≥1**: Meets septic shock criteria
    
    **Component Subscore Ranges:**
    - **Respiratory**: 0-3 points (support level and oxygenation status)
    - **Cardiovascular**: 0-6 points (vasopressors, lactate, MAP)
    - **Coagulation**: 0-2 points (platelets, INR, D-dimer, fibrinogen)
    - **Neurologic**: 0-2 points (GCS and pupil reactivity)
    
    **CLINICAL SIGNIFICANCE:**
    
    **Mortality Risk Stratification:**
    - Children meeting sepsis criteria (≥2 points) have significantly higher mortality:
      - Higher-resource settings: 7.1% in-hospital mortality
      - Lower-resource settings: 28.5% in-hospital mortality
      - More than 8-fold higher mortality compared to children not meeting criteria
    
    **Septic Shock Recognition:**
    - Septic shock diagnosis requires both sepsis criteria AND cardiovascular dysfunction
    - Represents the most severe form requiring immediate intensive care intervention
    - Associated with higher mortality and need for advanced life support measures
    
    **CLINICAL MANAGEMENT IMPLICATIONS:**
    
    **For Sepsis (Score ≥2):**
    - Immediate recognition as medical emergency requiring urgent intervention
    - Early antibiotic administration within 1 hour of recognition
    - Aggressive fluid resuscitation with crystalloid solutions
    - Source control measures when indicated
    - Continuous monitoring for progression to septic shock
    - Consider early involvement of pediatric intensive care
    
    **For Septic Shock (Score ≥2 + Cardiovascular ≥1):**
    - Immediate intensive care unit admission
    - Advanced hemodynamic monitoring and support
    - Vasoactive medication management and optimization
    - Mechanical ventilation support as needed
    - Renal replacement therapy consideration
    - Multidisciplinary team approach including intensivists
    
    **QUALITY IMPROVEMENT APPLICATIONS:**
    
    **Standardized Care Protocols:**
    - Consistent recognition criteria across healthcare providers
    - Standardized sepsis care bundle activation
    - Quality metrics and outcome measurement
    - Benchmarking across healthcare systems
    
    **Research Applications:**
    - Consistent enrollment criteria for pediatric sepsis studies
    - Standardized outcome measures for intervention research
    - International collaboration and data sharing
    - Development of predictive models and AI tools
    
    **IMPORTANT CONSIDERATIONS:**
    
    **Clinical Context:**
    - Score should complement, not replace, clinical judgment
    - Requires presence of suspected or confirmed infection
    - Regular reassessment as clinical condition evolves
    - Consider patient-specific factors not captured in score
    
    **Limitations:**
    - Not designed as screening tool for identifying sepsis
    - May not capture all relevant clinical factors
    - Performance may vary in populations not represented in development
    - Requires appropriate clinical context for interpretation
    
    **Implementation Guidance:**
    - Healthcare provider education on new criteria essential
    - Integration with existing sepsis protocols and pathways
    - Electronic health record integration for automated calculation
    - Regular audit and feedback for quality improvement
    
    Reference: Schlapbach LJ, et al. JAMA. 2024;331(8):665-674.
    """
    
    result: int = Field(
        ...,
        description="Total Phoenix Sepsis Score in points (0-13). Score ≥2 with suspected infection meets sepsis criteria",
        example=3
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation with diagnostic classification and management recommendations based on score and component analysis",
        example="Phoenix Sepsis Score: 3 points. Meets criteria for SEPSIS indicating potentially life-threatening organ dysfunction. Requires urgent medical evaluation, immediate antibiotic therapy, fluid resuscitation, and close monitoring for progression to septic shock."
    )
    
    stage: str = Field(
        ...,
        description="Diagnostic classification (No Sepsis, Sepsis, Septic Shock)",
        example="Sepsis"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the diagnostic classification",
        example="Meets criteria for sepsis"
    )
    
    component_scores: Dict[str, int] = Field(
        ...,
        description="Breakdown of scores from each organ system component",
        example={
            "respiratory_score": 1,
            "cardiovascular_score": 1,
            "coagulation_score": 1,
            "neurologic_score": 0
        }
    )
    
    clinical_status: Dict[str, bool] = Field(
        ...,
        description="Clinical diagnostic status for sepsis and septic shock based on Phoenix criteria",
        example={
            "sepsis": True,
            "septic_shock": False
        }
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 3,
                "unit": "points",
                "interpretation": "Phoenix Sepsis Score: 3 points. Meets criteria for SEPSIS indicating potentially life-threatening organ dysfunction. Requires urgent medical evaluation, immediate antibiotic therapy, fluid resuscitation, and close monitoring for progression to septic shock.",
                "stage": "Sepsis",
                "stage_description": "Meets criteria for sepsis",
                "component_scores": {
                    "respiratory_score": 1,
                    "cardiovascular_score": 1,
                    "coagulation_score": 1,
                    "neurologic_score": 0
                },
                "clinical_status": {
                    "sepsis": True,
                    "septic_shock": False
                }
            }
        }