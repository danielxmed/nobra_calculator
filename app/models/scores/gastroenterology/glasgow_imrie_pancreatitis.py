"""
Glasgow-Imrie Criteria for Severity of Acute Pancreatitis Models

Request and response models for Glasgow-Imrie Criteria calculation.

References (Vancouver style):
1. Imrie CW, Benjamin IS, Ferguson JC, et al. A single-centre double-blind trial of 
   Trasylol therapy in primary acute pancreatitis. Br J Surg. 1978;65(5):337-341.
2. Blamey SL, Imrie CW, O'Neill J, Gilmour WH, Carter DC. Prognostic factors in 
   acute pancreatitis. Gut. 1984;25(12):1340-1346. doi: 10.1136/gut.25.12.1340.
3. Ranson JH, Rifkind KM, Roses DF, Fink SD, Eng K, Spencer FC. Prognostic signs 
   and the role of operative management in acute pancreatitis. Surg Gynecol Obstet. 
   1974;139(1):69-81.
4. Banks PA, Bollen TL, Dervenis C, et al. Classification of acute pancreatitis--2012: 
   revision of the Atlanta classification and definitions by international consensus. 
   Gut. 2013;62(1):102-111. doi: 10.1136/gutjnl-2012-302779.

The Glasgow-Imrie Criteria is a clinical scoring system used to assess the severity 
of acute pancreatitis using 8 laboratory and clinical parameters. Originally developed 
as a modification of Ranson's criteria, it helps predict mortality risk and guide 
management decisions including ICU admission and treatment intensity. The criteria 
use the PANCREAS mnemonic (PaO2, Age, Neutrophils, Calcium, Renal function, 
Enzymes, Albumin, Sugar) for easy clinical recall.

The scoring system assigns 1 point for each positive criterion:
- P: PaO2 <59.3 mmHg (hypoxemia)
- A: Age >55 years  
- N: Neutrophils (WBC) >15×10⁹/L (leukocytosis)
- C: Calcium <8 mg/dL (hypocalcemia)
- R: Renal function (Urea/BUN) >44.8 mg/dL (elevated BUN)
- E: Enzymes (LDH) >600 IU/L (elevated lactate dehydrogenase)
- A: Albumin <3.2 g/dL (hypoalbuminemia)
- S: Sugar (Glucose) >180 mg/dL (hyperglycemia)

Total scores range from 0-8 points, with scores ≥3 indicating significant likelihood 
of severe pancreatitis requiring intensive monitoring and management.
"""

from pydantic import BaseModel, Field


class GlasgowImriePancreatitisRequest(BaseModel):
    """
    Request model for Glasgow-Imrie Criteria for Severity of Acute Pancreatitis
    
    The Glasgow-Imrie Criteria uses 8 clinical and laboratory parameters following 
    the PANCREAS mnemonic to assess acute pancreatitis severity:
    
    PANCREAS Mnemonic Components:
    - P: PaO2 <59.3 mmHg scores 1 point (indicates respiratory compromise)
    - A: Age >55 years scores 1 point (advanced age increases severity risk)
    - N: Neutrophils (WBC) >15×10⁹/L scores 1 point (systemic inflammatory response)
    - C: Calcium <8 mg/dL scores 1 point (hypocalcemia indicates severe disease)
    - R: Renal function (Urea/BUN) >44.8 mg/dL scores 1 point (renal impairment)
    - E: Enzymes (LDH) >600 IU/L scores 1 point (tissue damage marker)
    - A: Albumin <3.2 g/dL scores 1 point (hypoalbuminemia from capillary leak)
    - S: Sugar (Glucose) >180 mg/dL scores 1 point (stress hyperglycemia)
    
    Scoring Interpretation:
    - 0-2 points: Mild pancreatitis (7-16% risk of severe disease)
    - 3-4 points: Moderate pancreatitis (20-61% risk of severe disease)  
    - 5-8 points: Severe pancreatitis (55-100% risk of severe disease)
    
    The score should be assessed within 48 hours of admission for accurate 
    prognostication and is used to guide management decisions including ICU 
    admission, monitoring intensity, and resource allocation.

    References (Vancouver style):
    1. Imrie CW, Benjamin IS, Ferguson JC, et al. A single-centre double-blind trial of 
    Trasylol therapy in primary acute pancreatitis. Br J Surg. 1978;65(5):337-341.
    2. Blamey SL, Imrie CW, O'Neill J, Gilmour WH, Carter DC. Prognostic factors in 
    acute pancreatitis. Gut. 1984;25(12):1340-1346. doi: 10.1136/gut.25.12.1340.
    3. Banks PA, Bollen TL, Dervenis C, et al. Classification of acute pancreatitis--2012: 
    revision of the Atlanta classification and definitions by international consensus. 
    Gut. 2013;62(1):102-111. doi: 10.1136/gutjnl-2012-302779.
    """
    
    pao2: float = Field(
        ...,
        description="Partial pressure of oxygen (PaO2) from arterial blood gas in mmHg. Values <59.3 mmHg score 1 point and indicate respiratory compromise requiring monitoring for ARDS development",
        ge=30.0,
        le=150.0,
        example=85.0
    )
    
    age: int = Field(
        ...,
        description="Patient age in years. Ages >55 years score 1 point as advanced age is associated with increased severity and mortality risk in acute pancreatitis",
        ge=18,
        le=120,
        example=62
    )
    
    wbc: float = Field(
        ...,
        description="White blood cell count (neutrophil count) in cells × 10⁹/L. Values >15×10⁹/L score 1 point and indicate significant systemic inflammatory response syndrome (SIRS)",
        ge=1.0,
        le=50.0,
        example=12.5
    )
    
    calcium: float = Field(
        ...,
        description="Serum calcium level in mg/dL (corrected for albumin if possible). Values <8 mg/dL score 1 point and indicate severe disease with potential fat necrosis and calcium sequestration",
        ge=4.0,
        le=15.0,
        example=9.2
    )
    
    urea: float = Field(
        ...,
        description="Blood urea nitrogen (BUN) level in mg/dL. Values >44.8 mg/dL score 1 point and indicate renal impairment from hypovolemia, hypotension, or direct renal toxicity",
        ge=5.0,
        le=200.0,
        example=25.0
    )
    
    ldh: int = Field(
        ...,
        description="Lactate dehydrogenase (LDH) level in IU/L. Values >600 IU/L score 1 point and indicate significant tissue damage and cellular necrosis in pancreatic and peripancreatic tissues",
        ge=100,
        le=5000,
        example=450
    )
    
    albumin: float = Field(
        ...,
        description="Serum albumin level in g/dL. Values <3.2 g/dL score 1 point and indicate capillary leak syndrome, third-spacing of fluid, and nutritional compromise",
        ge=1.0,
        le=6.0,
        example=3.8
    )
    
    glucose: float = Field(
        ...,
        description="Blood glucose level in mg/dL (fasting or random). Values >180 mg/dL score 1 point and indicate stress hyperglycemia from counter-regulatory hormones and insulin resistance",
        ge=50.0,
        le=800.0,
        example=140.0
    )
    
    class Config:
        schema_extra = {
            "example": {
                "pao2": 85.0,
                "age": 62,
                "wbc": 12.5,
                "calcium": 9.2,
                "urea": 25.0,
                "ldh": 450,
                "albumin": 3.8,
                "glucose": 140.0
            }
        }


class GlasgowImriePancreatitisResponse(BaseModel):
    """
    Response model for Glasgow-Imrie Criteria for Severity of Acute Pancreatitis
    
    The Glasgow-Imrie score ranges from 0-8 points and classifies acute pancreatitis into:
    - Mild (0-2 points): Low risk for severe disease (7-16% risk)
    - Moderate (3-4 points): Moderate risk for severe disease (20-61% risk)
    - Severe (5-8 points): High risk for severe disease (55-100% risk)
    
    The score helps guide clinical management decisions including:
    - ICU admission requirements
    - Monitoring intensity and frequency
    - Need for aggressive fluid resuscitation
    - Consideration of early ERCP for biliary pancreatitis
    - Resource allocation and staffing decisions
    - Family counseling regarding prognosis
    
    Scores ≥3 typically warrant intensive monitoring and may require ICU-level care.
    The score should be interpreted in conjunction with clinical assessment, imaging 
    findings, and patient comorbidities for optimal management decisions.
    
    Reference: Blamey SL, et al. Gut. 1984;25(12):1340-1346.
    """
    
    result: int = Field(
        ...,
        description="Glasgow-Imrie score calculated from PANCREAS criteria (range: 0-8 points)",
        ge=0,
        le=8,
        example=2
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Comprehensive clinical interpretation with management recommendations based on the score and individual parameter values",
        example="Glasgow-Imrie Score: 2/8. [PaO2: 85.0 mmHg; Age: 62 years; WBC: 12.5×10⁹/L; Calcium: 9.2 mg/dL; Urea: 25.0 mg/dL; LDH: 450 IU/L; Albumin: 3.8 g/dL; Glucose: 140.0 mg/dL]. Positive criteria: A - Age >55 years ✓. Low risk for severe pancreatitis (7-16% risk of severe disease). Patient can typically be managed with conservative treatment on general medical ward."
    )
    
    stage: str = Field(
        ...,
        description="Severity classification based on score (Mild, Moderate, or Severe Pancreatitis)",
        example="Mild Pancreatitis"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the severity level and associated risk",
        example="Low risk for severe pancreatitis"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 2,
                "unit": "points",
                "interpretation": "Glasgow-Imrie Score: 2/8. [PaO2: 85.0 mmHg; Age: 62 years; WBC: 12.5×10⁹/L; Calcium: 9.2 mg/dL; Urea: 25.0 mg/dL; LDH: 450 IU/L; Albumin: 3.8 g/dL; Glucose: 140.0 mg/dL]. Positive criteria: A - Age >55 years ✓. Low risk for severe pancreatitis (7-16% risk of severe disease). Patient can typically be managed with conservative treatment on general medical ward. Continue supportive care with IV fluids, pain management, and monitoring for clinical deterioration.",
                "stage": "Mild Pancreatitis",
                "stage_description": "Low risk for severe pancreatitis"
            }
        }