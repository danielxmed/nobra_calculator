"""
Roth Score for Hypoxia Screening Models

Request and response models for Roth Score calculation.

References (Vancouver style):
1. Chorin E, Padegimas A, Havakuk O, Birati EY, Shacham Y, Milman A, Flint N, 
   Konigstein M, Nevzorov R, Moshe Y, Margolis G, Alcalai R, Topilsky Y. 
   Assessment of Respiratory Distress by the Roth Score. Clin Cardiol. 
   2016 Nov;39(11):636-639. doi: 10.1002/clc.22570.
2. Sánchez-Martínez C, Freitas-Alvarenga T, Puerta-García E, Navarro-Martínez S, 
   Iglesias-Vázquez JA, Rodríguez-Suárez P, Carbajales-Pérez C, Miró Ò. 
   Validity of the 'Roth score' for hypoxemia screening. Am J Emerg Med. 
   2023 May;67:1-7. doi: 10.1016/j.ajem.2023.01.038.
3. García-Villafranca M, Escolano-Casado G, González-Del Castillo J, 
   Martín-Sánchez FJ. The use of the Roth score in emergency department 
   for patients with acute exacerbation of chronic obstructive pulmonary disease. 
   Am J Emerg Med. 2024 Dec;86:164-165. doi: 10.1016/j.ajem.2024.09.025.

The Roth Score is a simple bedside test that screens for hypoxia in dyspneic 
patients using verbal counting performance. This telemedicine-compatible tool 
was developed to help risk-stratify respiratory distress when pulse oximetry 
may not be immediately available, particularly useful during pandemic screening 
situations or remote patient assessment.
"""

from pydantic import BaseModel, Field


class RothScoreRequest(BaseModel):
    """
    Request model for Roth Score hypoxia screening assessment
    
    The Roth Score uses a simple verbal counting test to screen for hypoxia in 
    dyspneic patients. The test requires the patient to take a deep breath and 
    count from 1 to 30 as fast as possible without stopping, while recording 
    both the maximum number reached and the total time elapsed.
    
    Clinical Background and Development:
    The Roth Score was developed in 2016 as a bedside screening tool for hypoxia, 
    particularly valuable in settings where pulse oximetry may not be immediately 
    available or reliable. The original study demonstrated that counting performance 
    correlates with oxygen saturation levels, providing a quick assessment method 
    for respiratory distress.
    
    Test Administration Protocol:
    1. Patient should be seated comfortably or in their usual position
    2. Instruct patient to take a deep breath and hold it
    3. Patient counts aloud from 1 to 30 as fast as possible without stopping
    4. Record the maximum number reached before needing to breathe
    5. Record the total time elapsed during the counting attempt
    6. Patient should not be coached or prompted during the test
    7. Allow one practice attempt if patient is unfamiliar with the test
    
    Performance Characteristics and Validation:
    Original validation study (Chorin et al., 2016) with 93 patients showed:
    - Maximum count <10: 91% sensitivity for O2 saturation <95%
    - Maximum count <7: 87% sensitivity for O2 saturation <90%
    - Total time <7 seconds: 83% sensitivity for O2 saturation <95%
    - Total time <5 seconds: 82% sensitivity for O2 saturation <90%
    
    Important Clinical Considerations:
    - Does NOT replace pulse oximetry or comprehensive clinical evaluation
    - Should be used as a screening tool in conjunction with clinical judgment
    - Results may be affected by vocal cord issues, language barriers, or cognitive impairment
    - False negatives possible in compensated respiratory conditions
    - Most useful for detecting moderate to severe respiratory distress
    - Validation studies have shown variable performance across different languages
    
    Clinical Applications:
    - Emergency department triage and initial assessment
    - Telemedicine consultations and remote patient monitoring
    - Pandemic screening situations where contact should be minimized
    - Resource-limited settings where pulse oximetry may not be available
    - Home health assessments and urgent care evaluations
    - Monitoring progression of respiratory symptoms in ambulatory patients
    
    Interpretation Guidelines:
    The Roth Score assessment considers both counting performance and time duration:
    
    High Risk for Hypoxia (Emergency):
    - Maximum count <7 numbers OR total time <5 seconds
    - Suggests severe respiratory distress with high risk for O2 sat <90%
    - Requires immediate pulse oximetry and clinical evaluation
    - Consider emergency respiratory support and underlying pathology assessment
    
    Moderate to High Risk:
    - Maximum count 7-9 numbers OR total time 5-7 seconds  
    - Indicates moderate respiratory compromise with risk for O2 sat <95%
    - Pulse oximetry recommended to confirm oxygen saturation status
    - Monitor closely and consider oxygen supplementation if indicated
    
    Low to Moderate Risk:
    - Maximum count ≥10 numbers but total time <7 seconds
    - Shows mild respiratory compromise requiring clinical correlation
    - Pulse oximetry should be performed to confirm adequate oxygenation
    - Continue monitoring and evaluate for underlying respiratory conditions
    
    Low Risk:
    - Maximum count ≥10 numbers AND total time ≥7 seconds
    - Demonstrates good respiratory reserve with normal counting ability
    - Low risk for significant hypoxia, though pulse oximetry remains gold standard
    - Evaluate other clinical factors if dyspnea symptoms persist
    
    Limitations and Contraindications:
    - Not validated in pediatric populations (original study ≥16 years)
    - May be unreliable in patients with severe vocal cord pathology
    - Language barriers may affect performance and interpretation
    - Cognitive impairment or confusion may limit test validity
    - Baseline respiratory function and comorbidities should be considered
    - Does not detect all causes of hypoxia, particularly chronic compensated conditions
    
    References (Vancouver style):
    1. Chorin E, Padegimas A, Havakuk O, Birati EY, Shacham Y, Milman A, Flint N, 
       Konigstein M, Nevzorov R, Moshe Y, Margolis G, Alcalai R, Topilsky Y. 
       Assessment of Respiratory Distress by the Roth Score. Clin Cardiol. 
       2016 Nov;39(11):636-639. doi: 10.1002/clc.22570.
    2. Sánchez-Martínez C, Freitas-Alvarenga T, Puerta-García E, Navarro-Martínez S, 
       Iglesias-Vázquez JA, Rodríguez-Suárez P, Carbajales-Pérez C, Miró Ò. 
       Validity of the 'Roth score' for hypoxemia screening. Am J Emerg Med. 
       2023 May;67:1-7. doi: 10.1016/j.ajem.2023.01.038.
    3. García-Villafranca M, Escolano-Casado G, González-Del Castillo J, 
       Martín-Sánchez FJ. The use of the Roth score in emergency department 
       for patients with acute exacerbation of chronic obstructive pulmonary disease. 
       Am J Emerg Med. 2024 Dec;86:164-165. doi: 10.1016/j.ajem.2024.09.025.
    """
    
    max_number_reached: int = Field(
        ...,
        ge=0,
        le=30,
        description="Maximum number reached when counting from 1 to 30 in a single breath. "
                   "Patient takes deep breath and counts aloud as fast as possible without stopping. "
                   "Record the highest number achieved before patient needs to breathe. "
                   "Range: 0-30 (0 indicates patient could not count at all, 30 indicates complete count)",
        example=15
    )
    
    total_seconds_counted: float = Field(
        ...,
        ge=0,
        le=60,
        description="Total seconds taken to count (regardless of final number reached). "
                   "Time from start of counting until patient stops or needs to breathe. "
                   "Should be measured accurately with stopwatch or timer. "
                   "Range: 0-60 seconds (practical upper limit for clinical assessment)",
        example=8.5
    )
    
    class Config:
        schema_extra = {
            "example": {
                "max_number_reached": 15,
                "total_seconds_counted": 8.5
            }
        }


class RothScoreResponse(BaseModel):
    """
    Response model for Roth Score hypoxia screening assessment
    
    The Roth Score provides a risk stratification assessment for hypoxia based on 
    verbal counting performance. Results are categorized into four risk levels 
    ranging from low risk (normal respiratory function) to high risk (severe 
    respiratory distress requiring immediate intervention).
    
    Risk Categories and Clinical Significance:
    
    High Risk for Hypoxia:
    - Severe counting impairment with very limited performance
    - High likelihood of oxygen saturation <90%
    - Requires immediate pulse oximetry and emergency respiratory assessment
    - May need urgent oxygen supplementation and underlying pathology evaluation
    
    Moderate to High Risk:
    - Moderate counting impairment suggesting respiratory compromise
    - Increased risk for oxygen saturation <95%
    - Pulse oximetry recommended for confirmation
    - Monitor closely and consider oxygen supplementation if clinically indicated
    
    Low to Moderate Risk:
    - Mild counting impairment with some respiratory compromise
    - Lower risk for severe hypoxia but clinical correlation needed
    - Pulse oximetry should be performed to confirm adequate oxygenation
    - Continue monitoring and evaluate for underlying respiratory conditions
    
    Low Risk:
    - Normal counting performance indicating good respiratory reserve
    - Low probability of significant hypoxia
    - Pulse oximetry remains gold standard but finding suggests adequate function
    - Evaluate other potential causes of dyspnea if symptoms persist
    
    Clinical Decision-Making Framework:
    
    High Risk Management:
    - Immediate pulse oximetry measurement and continuous monitoring
    - Consider emergency oxygen supplementation based on clinical presentation
    - Evaluate for underlying respiratory pathology (pneumonia, COPD exacerbation, PE)
    - May require hospital admission for monitoring and treatment
    - Comprehensive respiratory assessment including chest imaging
    
    Moderate Risk Management:
    - Pulse oximetry measurement to confirm oxygen saturation status
    - Clinical assessment for signs of respiratory distress or failure
    - Consider underlying conditions and medication review
    - Outpatient monitoring may be appropriate with close follow-up
    - Patient education about warning signs and when to seek immediate care
    
    Low Risk Management:
    - Routine pulse oximetry for documentation and baseline assessment
    - Evaluate other potential causes of dyspnea symptoms
    - Appropriate outpatient follow-up based on clinical presentation
    - Patient reassurance and education about normal findings
    - Consider pulmonary function testing if chronic symptoms persist
    
    Documentation and Follow-up:
    - Record both counting performance and time measurements
    - Document pulse oximetry results and clinical correlation
    - Note any factors that may have affected test performance
    - Plan appropriate follow-up based on risk category and clinical presentation
    - Provide patient education about test results and next steps
    
    Quality Assurance Considerations:
    - Ensure proper test administration technique and patient understanding
    - Consider repeat testing if results inconsistent with clinical presentation
    - Account for patient factors that may affect performance (anxiety, fatigue)
    - Validate findings with objective measurements when available
    - Document limitations and clinical context affecting interpretation
    
    Reference: Chorin E, et al. Clin Cardiol. 2016;39(11):636-639.
    """
    
    result: str = Field(
        ...,
        description="Roth Score risk assessment category based on counting performance. "
                   "Categories: 'High Risk for Hypoxia', 'Moderate to High Risk', "
                   "'Low to Moderate Risk', or 'Low Risk'",
        example="Low to Moderate Risk"
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the assessment result",
        example="risk level"
    )
    
    interpretation: str = Field(
        ...,
        description="Detailed clinical interpretation of the Roth Score assessment with "
                   "specific recommendations for patient management, monitoring, and follow-up. "
                   "Includes risk stratification guidance and next steps for clinical care.",
        example="Patient shows mild respiratory compromise with some counting difficulty "
                "(max: 15, time: 8.5s). Lower risk for severe hypoxia but clinical correlation "
                "recommended. Pulse oximetry should be performed to confirm oxygen saturation. "
                "Consider underlying respiratory conditions and continue monitoring."
    )
    
    stage: str = Field(
        ...,
        description="Risk stratification category for hypoxia screening assessment",
        example="Low to Moderate Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the risk category and clinical significance",
        example="Mild counting impairment"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": "Low to Moderate Risk",
                "unit": "risk level",
                "interpretation": "Patient shows mild respiratory compromise with some counting difficulty (max: 15, time: 8.5s). Lower risk for severe hypoxia but clinical correlation recommended. Pulse oximetry should be performed to confirm oxygen saturation. Consider underlying respiratory conditions and continue monitoring. May benefit from supportive care and further assessment based on clinical presentation.",
                "stage": "Low to Moderate Risk", 
                "stage_description": "Mild counting impairment"
            }
        }