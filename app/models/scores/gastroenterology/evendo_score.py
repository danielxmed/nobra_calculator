"""
EVendo Score for Esophageal Varices Models

Request and response models for EVendo Score calculation for predicting presence 
and size of esophageal varices prior to screening endoscopy in cirrhotic patients.

References (Vancouver style):
1. Dong TS, Kalani A, Aby ES, Le L, Luu K, Hauer M, et al. Machine Learning-based 
   Development and Validation of a Scoring System for Screening High-Risk Esophageal 
   Varices. Clin Gastroenterol Hepatol. 2019 Sep;17(10):1894-1901.e1. 
   doi: 10.1016/j.cgh.2019.01.025.
2. Hassan M, Hasan MW, Giordano A, Masud F, Bartoli A, Ahmad N. Validation of the 
   EVendo score for the prediction of varices in cirrhotic patients. World J Hepatol. 
   2022 Feb 27;14(2):460-474. doi: 10.4254/wjh.v14.i2.460.
3. Gibiino G, Garcovich M, Ainora ME, Zocco MA. Machine learning and artificial 
   intelligence: applications in hepatology. World J Gastroenterol. 2021 Jul 21;27(27):4384-4402. 
   doi: 10.3748/wjg.v27.i27.4384.

The EVendo Score is a machine learning-derived tool that uses readily available 
laboratory values to predict the presence of esophageal varices in patients with 
cirrhosis, helping to identify those who may safely defer endoscopic screening.
"""

from pydantic import BaseModel, Field
from typing import Literal


class EvendoScoreRequest(BaseModel):
    """
    Request model for EVendo Score for Esophageal Varices
    
    The EVendo Score predicts the presence and size of esophageal varices in patients 
    with cirrhosis using six readily available clinical parameters:
    
    Formula Components:
    A = (8.5 × INR) + (AST / 35)
    B = (Platelet count / 150) + (BUN / 20) + (Hemoglobin / 15)
    EVendo Score = (A / B) + 1 (if ascites present)
    
    Risk Stratification:
    - Score ≤3.90: Low Risk (<5% probability of varices, screening may be deferred)
    - Score >3.90: High Risk (≥5% probability of varices, endoscopy recommended)
    
    Clinical Parameters:
    
    1. International Normalized Ratio (INR):
       - Measures coagulation function
       - Reflects synthetic liver function
       - Higher values indicate worse liver function
       - Normal range: 0.8-1.2, cirrhotic patients often >1.2
    
    2. Aspartate Aminotransferase (AST):
       - Liver enzyme indicating hepatocellular injury
       - Elevated in active liver disease
       - Normal range: 15-41 U/L
       - May be chronically elevated in cirrhosis
    
    3. Platelet Count:
       - Reflects portal hypertension severity
       - Thrombocytopenia common in cirrhosis due to hypersplenism
       - Normal range: 150-350 ×10³/µL
       - Lower counts associated with higher portal pressure
    
    4. Blood Urea Nitrogen (BUN):
       - Reflects renal function and volume status
       - May be elevated in hepatorenal syndrome
       - Normal range: 8-20 mg/dL
       - Can indicate severity of liver disease complications
    
    5. Hemoglobin:
       - Reflects anemia, which is common in cirrhosis
       - May indicate GI bleeding or chronic disease
       - Normal range: 12-17 g/dL
       - Lower levels suggest more advanced disease
    
    6. Ascites:
       - Clinical sign of portal hypertension
       - Detected by physical examination or imaging
       - Binary variable: present or absent
       - Strong predictor of variceal presence
    
    Clinical Application:
    - Use in patients >18 years with known or suspected cirrhosis
    - Screening tool to reduce unnecessary endoscopies
    - Helps prioritize patients for urgent vs. routine endoscopy
    - Not for use in active GI bleeding or known variceal hemorrhage
    
    Model Development and Validation:
    - Developed using machine learning (random forest algorithm)
    - Training set: Large cohort of cirrhotic patients
    - Validation: Multi-center prospective validation
    - Performance: AUROC 0.82-0.84 for detecting varices
    - Sensitivity: 95.1% for varices needing treatment
    - Negative predictive value: 95.8%
    
    Clinical Impact:
    - Would spare 30.5% of patients from unnecessary endoscopy
    - Misses only 2.8% of varices needing treatment
    - Particularly effective in Child-Pugh A patients (40% spared, 1.1% missed)
    - Cost-effective screening approach
    
    Advantages:
    - Uses routinely available laboratory values
    - No additional testing required
    - Machine learning-derived for optimal performance
    - Validated across multiple centers and populations
    - Simple online calculator available
    
    Important Limitations:
    - Not for use in acute GI bleeding
    - Requires clinical judgment for borderline scores
    - May need local validation in different populations
    - Does not replace endoscopy when clinically indicated
    - Should be part of comprehensive cirrhosis management
    
    References (Vancouver style):
    1. Dong TS, et al. Machine Learning-based Development and Validation of a Scoring 
       System for Screening High-Risk Esophageal Varices. Clin Gastroenterol Hepatol. 2019;17(10):1894-1901.
    2. Hassan M, et al. Validation of the EVendo score for the prediction of varices 
       in cirrhotic patients. World J Hepatol. 2022;14(2):460-474.
    """
    
    inr: float = Field(
        ...,
        description="International Normalized Ratio (INR) - measures coagulation function and synthetic liver capacity. Higher values indicate worse liver function.",
        ge=0.5,
        le=10.0,
        example=1.8
    )
    
    ast_u_l: float = Field(
        ...,
        description="Aspartate aminotransferase (AST) level in U/L - liver enzyme indicating hepatocellular injury. Elevated in active liver disease.",
        ge=5.0,
        le=500.0,
        example=85.0
    )
    
    platelet_count: float = Field(
        ...,
        description="Platelet count in ×10³/µL - reflects portal hypertension severity. Thrombocytopenia is common in cirrhosis due to hypersplenism.",
        ge=10.0,
        le=1000.0,
        example=120.0
    )
    
    bun_mg_dl: float = Field(
        ...,
        description="Blood urea nitrogen (BUN) in mg/dL - reflects renal function and volume status. May be elevated in hepatorenal syndrome.",
        ge=2.0,
        le=100.0,
        example=25.0
    )
    
    hemoglobin_g_dl: float = Field(
        ...,
        description="Hemoglobin level in g/dL - reflects anemia common in cirrhosis. May indicate GI bleeding or chronic disease.",
        ge=4.0,
        le=20.0,
        example=10.5
    )
    
    ascites_present: Literal["yes", "no"] = Field(
        ...,
        description="Presence of ascites on physical examination or imaging - clinical sign of portal hypertension and strong predictor of variceal presence.",
        example="yes"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "inr": 1.8,
                "ast_u_l": 85.0,
                "platelet_count": 120.0,
                "bun_mg_dl": 25.0,
                "hemoglobin_g_dl": 10.5,
                "ascites_present": "yes"
            }
        }


class EvendoScoreResponse(BaseModel):
    """
    Response model for EVendo Score for Esophageal Varices
    
    Provides EVendo Score with risk stratification and clinical management recommendations 
    for esophageal varices screening in cirrhotic patients.
    
    Risk Categories and Clinical Management:
    
    Low Risk (Score ≤3.90):
    - Probability of esophageal varices: <5%
    - Sensitivity for varices needing treatment: 95.1%
    - Negative predictive value: 95.8%
    - Clinical management: Expectant management, screening endoscopy may be deferred
    - Follow-up: Routine clinical monitoring, reassess in 1-2 years or if status changes
    - Cost-effective approach: Spares 30.5% of patients from unnecessary endoscopy
    - Quality of life: Avoids invasive procedure with minimal risk of missing important varices
    
    High Risk (Score >3.90):
    - Probability of esophageal varices: ≥5%
    - Clinical management: Endoscopic screening recommended
    - Timing: Should be performed within appropriate timeframe based on clinical context
    - Further evaluation: Assess varix size and bleeding risk
    - Primary prophylaxis: Consider based on endoscopic findings
    - Monitoring: Regular surveillance if varices present
    
    Clinical Decision Support:
    
    Screening Strategy:
    - Risk-based approach to endoscopic screening
    - Resource allocation optimization
    - Patient-centered care with reduced unnecessary procedures
    - Cost-effective healthcare delivery
    
    Endoscopy Planning:
    - Low risk: Defer screening, continue medical management
    - High risk: Schedule upper endoscopy for variceal assessment
    - Emergency situations: Clinical judgment supersedes score
    - Surveillance intervals: Based on endoscopic findings if performed
    
    Patient Communication:
    - Low risk: Reassurance about low probability of varices
    - High risk: Education about importance of screening
    - Shared decision-making about timing and approach
    - Discussion of portal hypertension management
    
    Quality Improvement:
    - Standardized screening approach
    - Reduced healthcare costs through appropriate utilization
    - Improved patient satisfaction with risk-based care
    - Performance monitoring and outcome tracking
    
    Model Performance and Validation:
    - Developed using machine learning (random forest algorithm)
    - Multi-center validation with robust performance
    - Area under ROC curve: 0.82-0.84 for detecting varices
    - Excellent negative predictive value for clinical decision-making
    - Superior to traditional clinical assessment alone
    
    Comparison with Other Approaches:
    - More accurate than clinical judgment alone
    - Complementary to Baveno VI criteria
    - Higher sensitivity than platelet count/spleen size ratios
    - Validated across diverse populations and etiologies
    
    Important Clinical Considerations:
    - Machine learning-derived tool with validated performance
    - Uses only routinely available laboratory values
    - Not for use in acute GI bleeding or known variceal hemorrhage
    - Should complement comprehensive cirrhosis care
    - Requires ongoing clinical monitoring regardless of score
    
    Healthcare System Benefits:
    - Reduces unnecessary endoscopic procedures
    - Optimizes resource utilization
    - Maintains safety with high sensitivity
    - Standardizes screening approach
    - Supports value-based healthcare delivery
    
    Limitations and Cautions:
    - Developed in specific populations (may need local validation)
    - Not a substitute for clinical judgment
    - Should not delay endoscopy when clinically indicated
    - Requires accurate laboratory values and clinical assessment
    - May not apply to all causes of portal hypertension
    
    Future Directions:
    - Ongoing validation in diverse populations
    - Integration with electronic health records
    - Combination with other non-invasive markers
    - Cost-effectiveness studies in different healthcare systems
    - Refinement with additional clinical variables
    
    Reference: Dong TS, et al. Clin Gastroenterol Hepatol. 2019;17(10):1894-1901.
    """
    
    result: float = Field(
        ...,
        description="EVendo Score calculated from laboratory values and clinical findings (range: 0-50+)",
        example=5.25
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the EVendo Score",
        example="score"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation including risk level, probability of varices, and management recommendations",
        example="EVendo Score: 5.25 (>3.90 = High Risk). Endoscopic screening recommended. Probability of esophageal varices ≥5%. Upper endoscopy should be performed to evaluate for the presence and size of varices and determine need for primary prophylaxis."
    )
    
    stage: str = Field(
        ...,
        description="Risk stratification level (Low Risk or High Risk)",
        example="High Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the risk level",
        example="High probability of esophageal varices"
    )
    
    probability_varices: str = Field(
        ...,
        description="Probability of having esophageal varices based on the score",
        example="≥5%"
    )
    
    recommendation: str = Field(
        ...,
        description="Clinical recommendation for management based on the score",
        example="Endoscopic screening recommended"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "result": 5.25,
                "unit": "score",
                "interpretation": "EVendo Score: 5.25 (>3.90 = High Risk). Endoscopic screening recommended. Probability of esophageal varices ≥5%. Upper endoscopy should be performed to evaluate for the presence and size of varices and determine need for primary prophylaxis.",
                "stage": "High Risk",
                "stage_description": "High probability of esophageal varices",
                "probability_varices": "≥5%",
                "recommendation": "Endoscopic screening recommended"
            }
        }