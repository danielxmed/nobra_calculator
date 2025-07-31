"""
Framingham Heart Failure Diagnostic Criteria Models

Request and response models for Framingham Heart Failure Diagnostic Criteria.

References (Vancouver style):
1. McKee PA, Castelli WP, McNamara PM, Kannel WB. The natural history of congestive 
   heart failure: the Framingham study. N Engl J Med. 1971;285(26):1441-6. 
   doi: 10.1056/NEJM197112232852601.
2. Carlson KJ, Lee DC, Goroll AH, Leahy M, Johnson RA. An analysis of physicians' 
   reasons for prescribing long-term digitalis therapy in outpatients. J Chronic Dis. 
   1985;38(9):733-9. doi: 10.1016/0021-9681(85)90114-2.
3. Marantz PR, Tobin JN, Wassertheil-Smoller S, et al. The relationship between left 
   ventricular systolic function and congestive heart failure diagnosed by clinical criteria. 
   Circulation. 1988;77(3):607-12. doi: 10.1161/01.cir.77.3.607.
4. Remes J, Miettinen H, Reunanen A, Pyörälä K. Validity of clinical diagnosis of heart 
   failure in primary health care. Eur Heart J. 1991;12(3):315-21. doi: 10.1093/oxfordjournals.eurheartj.a059896.

The Framingham Heart Failure Diagnostic Criteria were developed in 1971 based on data 
from the landmark Framingham Heart Study. These criteria provide a systematic approach 
to diagnosing congestive heart failure using clinical signs and symptoms that can be 
assessed through history-taking and physical examination.

Key Features:
- Developed from the Framingham Heart Study (1971)
- Uses 7 major and 6 minor clinical criteria
- 97% sensitivity and 79% specificity for heart failure diagnosis
- Excellent negative predictive value (LR- = 0.04)
- Higher sensitivity for systolic (97%) vs diastolic (89%) heart failure

Diagnostic Algorithm:
- Heart failure diagnosed if: ≥2 major criteria OR 1 major + ≥2 minor criteria
- Minor criteria only counted if not attributable to other medical conditions
- Exclusions: pulmonary hypertension, chronic lung disease, cirrhosis, ascites, nephrotic syndrome

Clinical Applications:
- Primary care and emergency department screening
- Research studies requiring standardized heart failure diagnosis
- Resource-limited settings where advanced diagnostics unavailable
- Excellent tool for ruling out heart failure when criteria not met

Limitations:
- Developed in era before modern heart failure classification
- Does not distinguish between HFrEF and HFpEF
- Some criteria subjective and require clinical expertise
- Should be supplemented with modern diagnostics (echo, BNP/NT-proBNP)
"""

from pydantic import BaseModel, Field
from typing import Literal


class FraminghamHeartFailureCriteriaRequest(BaseModel):
    """
    Request model for Framingham Heart Failure Diagnostic Criteria
    
    The Framingham criteria use 13 clinical parameters (7 major, 6 minor) to diagnose 
    congestive heart failure. The diagnosis requires either ≥2 major criteria or 
    1 major criterion plus ≥2 minor criteria.
    
    **MAJOR CRITERIA (7 total)**:
    Each represents significant clinical evidence of heart failure
    
    **MINOR CRITERIA (6 total)**:
    Supportive clinical findings that may indicate heart failure
    Important: Minor criteria are only counted if they cannot be attributed to other 
    medical conditions (e.g., pulmonary hypertension, chronic lung disease, cirrhosis, 
    ascites, nephrotic syndrome)
    
    **DIAGNOSTIC ALGORITHM**:
    - **Heart Failure Diagnosed**: ≥2 major criteria OR 1 major + ≥2 minor criteria
    - **Heart Failure Not Diagnosed**: <2 major criteria AND <1 major + 2 minor criteria
    
    **CLINICAL PERFORMANCE**:
    - **Sensitivity**: 97% (excellent for ruling out heart failure)
    - **Specificity**: 79% (good for confirming heart failure)
    - **Negative Likelihood Ratio**: 0.04 (effectively rules out HF when criteria not met)
    - **Systolic HF**: 97% sensitivity
    - **Diastolic HF**: 89% sensitivity
    
    **CLINICAL APPLICATIONS**:
    - Primary care screening for heart failure
    - Emergency department evaluation of dyspnea
    - Research studies requiring standardized HF diagnosis
    - Resource-limited settings without advanced diagnostics
    - Excellent screening tool due to high sensitivity
    
    **IMPORTANT CONSIDERATIONS**:
    - Requires skilled clinical examination
    - Minor criteria must not be attributable to other conditions
    - Should be combined with modern diagnostics when available
    - Particularly useful for ruling out heart failure
    - Does not distinguish between HFrEF and HFpEF
    
    References (Vancouver style):
    1. McKee PA, Castelli WP, McNamara PM, Kannel WB. The natural history of congestive 
       heart failure: the Framingham study. N Engl J Med. 1971;285(26):1441-6.
    2. Marantz PR, Tobin JN, Wassertheil-Smoller S, et al. The relationship between left 
       ventricular systolic function and congestive heart failure diagnosed by clinical criteria. 
       Circulation. 1988;77(3):607-12.
    """
    
    # MAJOR CRITERIA (7 total)
    acute_pulmonary_edema: Literal["yes", "no"] = Field(
        ...,
        description=(
            "Acute pulmonary edema (MAJOR CRITERION). Clinical or radiographic evidence of acute "
            "fluid accumulation in the lungs with rapid onset dyspnea, orthopnea, and bilateral "
            "pulmonary rales. May include frothy sputum and severe respiratory distress."
        ),
        example="no"
    )
    
    cardiomegaly: Literal["yes", "no"] = Field(
        ...,
        description=(
            "Cardiomegaly on chest X-ray (MAJOR CRITERION). Enlarged cardiac silhouette with "
            "cardiothoracic ratio >0.50 on standard PA chest radiograph. Indicates chronic "
            "cardiac enlargement due to volume or pressure overload."
        ),
        example="yes"
    )
    
    hepatojugular_reflex: Literal["yes", "no"] = Field(
        ...,
        description=(
            "Hepatojugular reflex (MAJOR CRITERION). Sustained elevation of jugular venous pressure "
            "≥3 cm when firm pressure is applied to the right upper quadrant of the abdomen for "
            "10-15 seconds. Indicates elevated right heart filling pressures."
        ),
        example="no"
    )
    
    neck_vein_distention: Literal["yes", "no"] = Field(
        ...,
        description=(
            "Neck vein distention/Jugular venous distention (MAJOR CRITERION). Visible elevation "
            "of external jugular veins >3 cm above the sternal angle when patient positioned at "
            "45-degree angle. Indicates elevated right atrial pressure."
        ),
        example="yes"
    )
    
    paroxysmal_nocturnal_dyspnea_orthopnea: Literal["yes", "no"] = Field(
        ...,
        description=(
            "Paroxysmal nocturnal dyspnea OR orthopnea (MAJOR CRITERION). PND: sudden dyspnea "
            "awakening patient from sleep, requiring sitting upright for relief. Orthopnea: "
            "dyspnea when lying flat, requiring multiple pillows or sleeping upright."
        ),
        example="yes"
    )
    
    pulmonary_rales: Literal["yes", "no"] = Field(
        ...,
        description=(
            "Pulmonary rales on examination (MAJOR CRITERION). Fine, wet, crackling sounds heard "
            "on inspiration, typically bilateral and beginning at lung bases. May progress upward "
            "with worsening heart failure. Not cleared by coughing."
        ),
        example="yes"
    )
    
    third_heart_sound: Literal["yes", "no"] = Field(
        ...,
        description=(
            "Third heart sound - S3 gallop rhythm (MAJOR CRITERION). Low-pitched sound heard "
            "immediately after S2, creating 'gallop' rhythm. Best heard at apex with bell of "
            "stethoscope. Indicates elevated left ventricular filling pressure."
        ),
        example="no"
    )
    
    # MINOR CRITERIA (6 total)
    ankle_edema: Literal["yes", "no"] = Field(
        ...,
        description=(
            "Ankle edema (MINOR CRITERION). Bilateral pitting edema of the ankles and feet, "
            "typically developing over days to weeks. May progress to involve legs and thighs. "
            "Only counted if not attributable to venous insufficiency, liver disease, or renal disease."
        ),
        example="yes"
    )
    
    dyspnea_on_exertion: Literal["yes", "no"] = Field(
        ...,
        description=(
            "Dyspnea on exertion (MINOR CRITERION). Shortness of breath during physical activity "
            "that is disproportionate to the level of exertion. May represent decreased exercise "
            "tolerance compared to baseline. Only counted if not due to lung disease or deconditioning."
        ),
        example="yes"
    )
    
    hepatomegaly: Literal["yes", "no"] = Field(
        ...,
        description=(
            "Hepatomegaly (MINOR CRITERION). Enlarged liver palpable below the right costal margin "
            "or demonstrated by percussion/imaging. May be tender in acute heart failure. Only "
            "counted if not attributable to liver disease, malignancy, or other causes."
        ),
        example="no"
    )
    
    nocturnal_cough: Literal["yes", "no"] = Field(
        ...,
        description=(
            "Nocturnal cough (MINOR CRITERION). Persistent cough that is worse at night or when "
            "lying flat, often dry and non-productive. May interfere with sleep. Only counted "
            "if not attributable to respiratory tract infection, asthma, or other lung diseases."
        ),
        example="yes"
    )
    
    pleural_effusion: Literal["yes", "no"] = Field(
        ...,
        description=(
            "Pleural effusion (MINOR CRITERION). Fluid accumulation in pleural space demonstrated "
            "by chest X-ray, physical examination (dullness to percussion, decreased breath sounds), "
            "or other imaging. May be bilateral in heart failure."
        ),
        example="no"
    )
    
    tachycardia: Literal["yes", "no"] = Field(
        ...,
        description=(
            "Tachycardia - heart rate >120 beats per minute (MINOR CRITERION). Compensatory "
            "increase in heart rate due to decreased cardiac output. Should be persistent and "
            "not attributable to fever, anxiety, hyperthyroidism, or other causes."
        ),
        example="no"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "acute_pulmonary_edema": "no",
                "cardiomegaly": "yes",
                "hepatojugular_reflex": "no",
                "neck_vein_distention": "yes",
                "paroxysmal_nocturnal_dyspnea_orthopnea": "yes",
                "pulmonary_rales": "yes",
                "third_heart_sound": "no",
                "ankle_edema": "yes",
                "dyspnea_on_exertion": "yes",
                "hepatomegaly": "no",
                "nocturnal_cough": "yes",
                "pleural_effusion": "no",
                "tachycardia": "no"
            }
        }


class FraminghamHeartFailureCriteriaResponse(BaseModel):
    """
    Response model for Framingham Heart Failure Diagnostic Criteria
    
    The response indicates whether the patient meets the diagnostic criteria for 
    congestive heart failure based on the Framingham criteria, along with detailed 
    clinical interpretation and management recommendations.
    
    **DIAGNOSTIC OUTCOMES**:
    
    **Heart Failure Diagnosed (result = 1)**:
    - Criteria met: ≥2 major criteria OR 1 major + ≥2 minor criteria
    - 97% sensitivity and 79% specificity support the diagnosis
    - Immediate evaluation and treatment warranted
    - Recommendations: echocardiography, BNP/NT-proBNP, guideline-based management
    
    **Heart Failure Not Diagnosed (result = 0)**:
    - Criteria not met: <2 major criteria AND <1 major + 2 minor criteria
    - High sensitivity (97%) makes heart failure unlikely when criteria not met
    - Negative likelihood ratio of 0.04 effectively rules out heart failure
    - Consider alternative diagnoses for patient's symptoms
    
    **CLINICAL IMPLICATIONS**:
    
    **When Diagnosis Made**:
    - Initiate appropriate heart failure workup (echo, labs, chest X-ray)
    - Assess left ventricular function and ejection fraction
    - Evaluate for underlying etiology (ischemic, valvular, etc.)
    - Begin guideline-directed medical therapy as appropriate
    - Consider cardiology consultation
    - Patient education on diet, fluid restriction, daily weights
    
    **When Diagnosis Not Made**:
    - Consider alternative causes of symptoms (lung disease, anemia, etc.)
    - If high clinical suspicion remains, consider BNP/NT-proBNP or echocardiography
    - The high negative predictive value supports looking for other diagnoses
    - May still warrant cardiac evaluation if risk factors present
    
    **MANAGEMENT CONSIDERATIONS**:
    - Modern heart failure classification (HFrEF vs HFpEF) requires echocardiography
    - These criteria developed before contemporary HF understanding
    - Should be combined with modern diagnostic tools when available
    - Particularly valuable in resource-limited settings
    - Excellent screening tool due to high sensitivity
    
    **QUALITY MEASURES**:
    - Validated in multiple populations and settings
    - Widely used in clinical practice and research
    - Maintains relevance despite age of criteria
    - Complements modern diagnostic approaches
    
    Reference: McKee PA, et al. N Engl J Med. 1971;285(26):1441-6.
    """
    
    result: Literal[0, 1] = Field(
        ...,
        description="Diagnostic result: 1 = Heart failure diagnosed, 0 = Heart failure not diagnosed",
        example=1
    )
    
    unit: str = Field(
        ...,
        description="Unit for the diagnostic result",
        example="diagnosis"
    )
    
    interpretation: str = Field(
        ...,
        description=(
            "Comprehensive clinical interpretation including diagnostic rationale, "
            "criteria met, clinical significance, and management recommendations"
        ),
        example=(
            "Framingham criteria met for heart failure diagnosis (4 major criteria and 3 minor criteria present). "
            "The diagnostic criteria are 97% sensitive and 79% specific for congestive heart failure. "
            "Initiate appropriate heart failure evaluation including echocardiography, BNP/NT-proBNP, "
            "and management according to current heart failure guidelines. Consider evaluation for "
            "underlying etiology and assessment of left ventricular function."
        )
    )
    
    stage: str = Field(
        ...,
        description="Diagnostic category (Heart Failure Diagnosed or Heart Failure Not Diagnosed)",
        example="Heart Failure Diagnosed"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the diagnostic outcome",
        example="Criteria met for heart failure diagnosis"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 1,
                "unit": "diagnosis",
                "interpretation": (
                    "Framingham criteria met for heart failure diagnosis (4 major criteria and 3 minor criteria present). "
                    "The diagnostic criteria are 97% sensitive and 79% specific for congestive heart failure. "
                    "Initiate appropriate heart failure evaluation including echocardiography, BNP/NT-proBNP, "
                    "and management according to current heart failure guidelines. Consider evaluation for "
                    "underlying etiology and assessment of left ventricular function."
                ),
                "stage": "Heart Failure Diagnosed",
                "stage_description": "Criteria met for heart failure diagnosis"
            }
        }