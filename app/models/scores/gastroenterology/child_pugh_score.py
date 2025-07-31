"""
Child-Pugh Score for Cirrhosis Mortality Models

Request and response models for Child-Pugh Score calculation.

References (Vancouver style):
1. Child CG, Turcotte JG. Surgery and portal hypertension. In: The liver and portal 
   hypertension. Edited by CG Child. Philadelphia: Saunders 1964:50-64.
2. Pugh RN, Murray-Lyon IM, Dawson JL, Pietroni MC, Williams R. Transection of the 
   oesophagus for bleeding oesophageal varices. Br J Surg. 1973 Aug;60(8):646-9.
3. Durand F, Valla D. Assessment of prognosis of cirrhosis. Semin Liver Dis. 2008 
   Feb;28(1):110-22.

The Child-Pugh Score estimates the severity of cirrhosis and prognosis in patients with 
chronic liver disease. Originally developed to predict mortality during portacaval shunt 
surgery, it has become widely used for assessing prognosis and determining treatment options 
in cirrhotic patients.

Child-Pugh Scoring Components:

Total Bilirubin (mg/dL):
- 1 point: <2.0 mg/dL (Normal to mildly elevated)
- 2 points: 2.0-3.0 mg/dL (Moderately elevated)
- 3 points: >3.0 mg/dL (Severely elevated)

Serum Albumin (g/dL):
- 1 point: >3.5 g/dL (Normal)
- 2 points: 2.8-3.5 g/dL (Mildly decreased)
- 3 points: <2.8 g/dL (Severely decreased)

International Normalized Ratio (INR):
- 1 point: <1.7 (Mild coagulopathy)
- 2 points: 1.7-2.3 (Moderate coagulopathy)
- 3 points: >2.3 (Severe coagulopathy)

Ascites:
- 1 point: Absent (No fluid accumulation)
- 2 points: Slight (Mild ascites, controlled with diuretics)
- 3 points: Moderate (Tense ascites, refractory to treatment)

Hepatic Encephalopathy:
- 1 point: None (Normal mental status)
- 2 points: Grade 1-2 (Mild confusion, altered sleep pattern)
- 3 points: Grade 3-4 (Stupor, coma)

Child-Pugh Classification:

Grade A (5-6 points): Well-compensated disease
- One-year survival: ~100%
- Two-year survival: ~85%
- Operative risk: Excellent
- Clinical management: Suitable for major surgery and liver resection

Grade B (7-9 points): Significant functional compromise
- One-year survival: ~80%
- Two-year survival: ~60%
- Operative risk: Good
- Clinical management: Consider surgery with caution; may need transplant evaluation

Grade C (10-15 points): Decompensated disease
- One-year survival: ~45%
- Two-year survival: ~35%
- Operative risk: Poor
- Clinical management: High surgical mortality; priority for liver transplantation

Clinical Applications:
- Prognosis assessment in cirrhotic patients
- Surgical risk stratification
- Treatment decision-making
- Liver transplant evaluation
- Clinical trial stratification
- Drug dosing adjustments in liver disease

Limitations:
- Subjective assessment of ascites and encephalopathy
- MELD and MELD-Na scores now preferred for transplant allocation
- Less accurate for very advanced disease
- May not reflect rapid changes in clinical condition
- Limited utility in acute liver failure
"""

from pydantic import BaseModel, Field
from typing import Literal, Dict, Any


class ChildPughScoreRequest(BaseModel):
    """
    Request model for Child-Pugh Score for Cirrhosis Mortality
    
    The Child-Pugh Score uses 5 clinical parameters to assess cirrhosis severity and 
    prognosis. Each parameter is scored 1-3 points based on severity, with higher scores 
    indicating more advanced liver disease.
    
    Laboratory Parameters:
    
    Total Bilirubin (mg/dL):
    Serum total bilirubin reflects hepatic synthetic function and biliary excretion.
    Elevated levels indicate impaired liver function or biliary obstruction.
    - Normal: <1.2 mg/dL
    - Scoring: <2.0 (1 pt), 2.0-3.0 (2 pts), >3.0 (3 pts)
    
    Serum Albumin (g/dL):
    Albumin is synthesized exclusively by the liver and has a half-life of ~20 days.
    Low levels indicate impaired hepatic synthetic function.
    - Normal: 3.5-5.0 g/dL
    - Scoring: >3.5 (1 pt), 2.8-3.5 (2 pts), <2.8 (3 pts)
    
    International Normalized Ratio (INR):
    INR measures coagulation function, reflecting synthesis of clotting factors.
    Elevated INR indicates impaired hepatic synthetic function.
    - Normal: 0.8-1.2
    - Scoring: <1.7 (1 pt), 1.7-2.3 (2 pts), >2.3 (3 pts)
    
    Clinical Parameters:
    
    Ascites:
    Fluid accumulation in the peritoneal cavity due to portal hypertension and 
    hypoalbuminemia. Assessment based on physical examination and imaging.
    - Absent: No detectable fluid
    - Slight: Mild ascites controlled with diuretics
    - Moderate: Tense ascites, refractory to medical management
    
    Hepatic Encephalopathy:
    Neuropsychiatric syndrome caused by hepatic dysfunction and portosystemic shunting.
    Assessment based on clinical examination and mental status testing.
    - None: Normal consciousness and cognitive function
    - Grade 1-2: Altered mood, sleep disturbance, mild confusion
    - Grade 3-4: Stupor, somnolence, coma
    
    Clinical Context:
    Originally developed in 1964-1973 for surgical risk assessment in patients undergoing 
    portacaval shunt procedures. Now widely used for:
    - Cirrhosis prognosis and staging
    - Surgical risk stratification
    - Treatment planning and liver transplant evaluation
    - Clinical trial enrollment criteria
    - Drug dosing modifications in hepatic impairment
    
    Interpretation Guidelines:
    The total score (5-15 points) classifies patients into three prognostic groups:
    - Class A (5-6): Well-compensated, excellent prognosis
    - Class B (7-9): Moderate dysfunction, intermediate prognosis  
    - Class C (10-15): Decompensated, poor prognosis
    
    Limitations and Considerations:
    - Subjective elements (ascites, encephalopathy assessment)
    - MELD/MELD-Na scores preferred for liver transplant allocation
    - Should be reassessed with changes in clinical status
    - Less accurate in acute liver failure or rapidly changing conditions
    
    References (Vancouver style):
    1. Child CG, Turcotte JG. Surgery and portal hypertension. In: The liver and portal 
    hypertension. Edited by CG Child. Philadelphia: Saunders 1964:50-64.
    2. Pugh RN, Murray-Lyon IM, Dawson JL, Pietroni MC, Williams R. Transection of the 
    oesophagus for bleeding oesophageal varices. Br J Surg. 1973 Aug;60(8):646-9.
    """
    
    total_bilirubin: float = Field(
        ...,
        ge=0.1,
        le=50.0,
        description="Serum total bilirubin level in mg/dL. Scoring: <2.0 (1 pt), 2.0-3.0 (2 pts), >3.0 (3 pts)",
        example=2.5
    )
    
    serum_albumin: float = Field(
        ...,
        ge=1.0,
        le=5.0,
        description="Serum albumin level in g/dL. Scoring: >3.5 (1 pt), 2.8-3.5 (2 pts), <2.8 (3 pts)",
        example=3.2
    )
    
    inr: float = Field(
        ...,
        ge=0.8,
        le=10.0,
        description="International Normalized Ratio. Scoring: <1.7 (1 pt), 1.7-2.3 (2 pts), >2.3 (3 pts)",
        example=1.8
    )
    
    ascites: Literal["absent", "slight", "moderate"] = Field(
        ...,
        description="Presence and severity of ascites. Absent (1 pt), slight/controlled (2 pts), moderate/refractory (3 pts)",
        example="slight"
    )
    
    encephalopathy: Literal["none", "grade_1_2", "grade_3_4"] = Field(
        ...,
        description="Hepatic encephalopathy grade. None (1 pt), Grade 1-2/mild (2 pts), Grade 3-4/severe (3 pts)",
        example="grade_1_2"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "total_bilirubin": 2.5,
                "serum_albumin": 3.2,
                "inr": 1.8,
                "ascites": "slight",
                "encephalopathy": "grade_1_2"
            }
        }


class ChildPughScoreResponse(BaseModel):
    """
    Response model for Child-Pugh Score for Cirrhosis Mortality
    
    The Child-Pugh Score provides comprehensive assessment of cirrhosis severity with 
    prognostic information and clinical management guidance. The score ranges from 5-15 
    points and classifies patients into three prognostic categories.
    
    Prognostic Categories:
    
    Child-Pugh Grade A (5-6 points): Well-compensated disease
    - One-year survival: ~100%
    - Two-year survival: ~85%  
    - Operative risk: Excellent
    - Management: Suitable for major surgery and liver resection
    - Prognosis: Excellent long-term survival
    
    Child-Pugh Grade B (7-9 points): Significant functional compromise  
    - One-year survival: ~80%
    - Two-year survival: ~60%
    - Operative risk: Good
    - Management: Surgery with caution; consider transplant evaluation
    - Prognosis: Intermediate survival with careful monitoring
    
    Child-Pugh Grade C (10-15 points): Decompensated disease
    - One-year survival: ~45%
    - Two-year survival: ~35%
    - Operative risk: Poor
    - Management: High surgical mortality; priority for liver transplantation
    - Prognosis: Poor survival without intervention
    
    Clinical Applications:
    
    Surgical Risk Stratification:
    - Grade A: Low perioperative mortality (<5%)
    - Grade B: Moderate risk (5-15% mortality)
    - Grade C: High risk (>15% mortality), contraindication to major surgery
    
    Liver Transplant Evaluation:
    - Grade A: May not yet require transplantation
    - Grade B: Consider evaluation and listing
    - Grade C: Urgent evaluation and high priority listing
    
    Medical Management:
    - Variceal screening and prophylaxis
    - Hepatocellular carcinoma surveillance
    - Nutritional assessment and support
    - Vaccination recommendations
    - Drug dosing adjustments
    
    Monitoring and Follow-up:
    - Grade A: Every 6-12 months
    - Grade B: Every 3-6 months
    - Grade C: Every 1-3 months or as clinically indicated
    
    Quality of Life Considerations:
    - Grade A: Generally good functional status
    - Grade B: Moderate limitations, symptom management important
    - Grade C: Significant impairment, palliative care considerations
    
    Comparison with MELD Score:
    While Child-Pugh remains widely used, MELD (Model for End-Stage Liver Disease) 
    and MELD-Na scores are now preferred for:
    - Liver transplant allocation
    - More objective assessment (no subjective components)
    - Better prediction of short-term mortality
    - More frequent reassessment capability
    
    Clinical Decision Framework:
    The Child-Pugh score should be integrated with:
    - Overall clinical condition and comorbidities
    - Patient preferences and goals of care
    - Available treatment options and resources
    - Trajectory of liver disease progression
    - Response to medical therapy
    
    Reference: Pugh RN, et al. Br J Surg. 1973;60(8):646-9.
    """
    
    result: Dict[str, Any] = Field(
        ...,
        description="Comprehensive Child-Pugh assessment including score, grade, survival data, and clinical recommendations",
        example={
            "total_score": 9,
            "grade": "B",
            "one_year_survival": 80,
            "two_year_survival": 60,
            "operative_risk": "Good",
            "surgical_recommendation": "Consider surgery with caution; may need transplant evaluation",
            "scoring_breakdown": {
                "component_scores": {
                    "total_bilirubin": {
                        "value": 2.5,
                        "unit": "mg/dL",
                        "category": "2.5 mg/dL (2.0-3.0)",
                        "points": 2,
                        "description": "Total serum bilirubin level"
                    },
                    "serum_albumin": {
                        "value": 3.2,
                        "unit": "g/dL",
                        "category": "3.2 g/dL (2.8-3.5)",
                        "points": 2,
                        "description": "Serum albumin level"
                    },
                    "inr": {
                        "value": 1.8,
                        "unit": "",
                        "category": "1.8 (1.7-2.3)",
                        "points": 2,
                        "description": "International Normalized Ratio"
                    },
                    "ascites": {
                        "value": "Slight",
                        "category": "Slight",
                        "points": 2,
                        "description": "Presence and severity of ascites"
                    },
                    "encephalopathy": {
                        "value": "Grade 1-2",
                        "category": "Grade 1-2",
                        "points": 1,
                        "description": "Hepatic encephalopathy grade"
                    }
                }
            }
        }
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation with prognostic information and management recommendations",
        example="Child-Pugh Grade B (Score 9): Significant functional compromise. Good operative risk with one-year survival ~80% and two-year survival ~60%. Consider surgery with caution; may require liver transplant evaluation."
    )
    
    stage: str = Field(
        ...,
        description="Child-Pugh grade classification (Child-Pugh A, B, or C)",
        example="Child-Pugh B"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the cirrhosis severity category",
        example="Significant functional compromise"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "result": {
                    "total_score": 9,
                    "grade": "B",
                    "one_year_survival": 80,
                    "two_year_survival": 60,
                    "operative_risk": "Good",
                    "surgical_recommendation": "Consider surgery with caution; may need transplant evaluation",
                    "scoring_breakdown": {
                        "component_scores": {
                            "total_bilirubin": {
                                "value": 2.5,
                                "unit": "mg/dL",
                                "category": "2.5 mg/dL (2.0-3.0)",
                                "points": 2,
                                "description": "Total serum bilirubin level"
                            },
                            "serum_albumin": {
                                "value": 3.2,
                                "unit": "g/dL",
                                "category": "3.2 g/dL (2.8-3.5)",
                                "points": 2,
                                "description": "Serum albumin level"
                            },
                            "inr": {
                                "value": 1.8,
                                "unit": "",
                                "category": "1.8 (1.7-2.3)",
                                "points": 2,
                                "description": "International Normalized Ratio"
                            },
                            "ascites": {
                                "value": "Slight",
                                "category": "Slight",
                                "points": 2,
                                "description": "Presence and severity of ascites"
                            },
                            "encephalopathy": {
                                "value": "Grade 1-2",
                                "category": "Grade 1-2",
                                "points": 1,
                                "description": "Hepatic encephalopathy grade"
                            }
                        }
                    }
                },
                "unit": "points",
                "interpretation": "Child-Pugh Grade B (Score 9): Significant functional compromise. Good operative risk with one-year survival ~80% and two-year survival ~60%. Consider surgery with caution; may require liver transplant evaluation.",
                "stage": "Child-Pugh B",
                "stage_description": "Significant functional compromise"
            }
        }