"""
Arterial Blood Gas (ABG) Analyzer Models

Request and response models for ABG analysis calculation.

References (Vancouver style):
1. Seifter JL. Acid-base disorders. In: Jameson J, Fauci AS, Kasper DL, Hauser SL, 
   Longo DL, Loscalzo J. eds. Harrison's Principles of Internal Medicine, 20e. 
   McGraw Hill; 2018.
2. Berend K, de Vries AP, Gans RO. Physiological approach to assessment of acid-base 
   disturbances. N Engl J Med. 2014;371(15):1434-45. doi: 10.1056/NEJMra1003327.
3. Kraut JA, Madias NE. Serum anion gap: its uses and limitations in clinical medicine. 
   Clin J Am Soc Nephrol. 2007;2(1):162-74. doi: 10.2215/CJN.03020906.
4. MDCalc. Arterial Blood Gas (ABG) Analyzer. Available at: 
   https://www.mdcalc.com/calc/1741/arterial-blood-gas-abg-analyzer

The ABG Analyzer interprets arterial blood gas results to determine acid-base status, 
assess respiratory and metabolic compensation, and evaluate oxygenation. It uses 
established physiological principles and compensation formulas (including Winter's 
formula for metabolic acidosis) to provide comprehensive clinical interpretation.

Key components analyzed:
- pH: Determines acidemia (pH <7.35) or alkalemia (pH >7.45)
- PCO2: Reflects respiratory component (normal 35-45 mmHg)
- HCO3: Reflects metabolic component (normal 22-26 mEq/L)
- PO2: Assesses oxygenation status (optional, normal 80-100 mmHg)
- FiO2: Fraction of inspired oxygen for oxygenation assessment (optional)

Normal ranges:
- pH: 7.35-7.45
- PCO2: 35-45 mmHg
- HCO3: 22-26 mEq/L
- PO2: 80-100 mmHg (on room air)
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any


class AbgAnalyzerRequest(BaseModel):
    """
    Request model for Arterial Blood Gas (ABG) Analyzer
    
    The ABG Analyzer requires pH, PCO2, and HCO3 values to determine acid-base status.
    PO2 and FiO2 are optional parameters for oxygenation assessment.
    
    Required Parameters:
    - pH: Arterial blood pH value (normal range: 7.35-7.45)
      Values <7.35 indicate acidemia, >7.45 indicate alkalemia
    
    - PCO2: Partial pressure of carbon dioxide in arterial blood (normal: 35-45 mmHg)
      Reflects respiratory component of acid-base balance
      High PCO2 indicates respiratory acidosis or compensation for metabolic alkalosis
      Low PCO2 indicates respiratory alkalosis or compensation for metabolic acidosis
    
    - HCO3: Bicarbonate concentration in arterial blood (normal: 22-26 mEq/L)
      Reflects metabolic component of acid-base balance
      Low HCO3 indicates metabolic acidosis or compensation for respiratory alkalosis
      High HCO3 indicates metabolic alkalosis or compensation for respiratory acidosis
    
    Optional Parameters:
    - PO2: Partial pressure of oxygen in arterial blood (normal: 80-100 mmHg on room air)
      Used to assess oxygenation status and detect hypoxemia
    
    - FiO2: Fraction of inspired oxygen (expressed as decimal, e.g., 0.21 for room air)
      Used with PO2 to calculate alveolar-arterial oxygen gradient
      Helps assess oxygen exchange efficiency

    Clinical Interpretation Approach:
    1. Assess pH to determine acidemia vs alkalemia
    2. Determine primary disorder (metabolic vs respiratory)
    3. Assess compensation using established formulas
    4. Evaluate oxygenation if PO2 provided
    5. Provide clinical recommendations

    References (Vancouver style):
    1. Seifter JL. Acid-base disorders. In: Harrison's Principles of Internal Medicine, 
       20e. McGraw Hill; 2018.
    2. Berend K, de Vries AP, Gans RO. Physiological approach to assessment of 
       acid-base disturbances. N Engl J Med. 2014;371(15):1434-45.
    3. MDCalc. Arterial Blood Gas (ABG) Analyzer. Available at: 
       https://www.mdcalc.com/calc/1741/arterial-blood-gas-abg-analyzer
    """
    
    ph: float = Field(
        ...,
        ge=6.8,
        le=7.8,
        description="Arterial blood pH value. Normal range: 7.35-7.45. Values <7.35 indicate acidemia, >7.45 indicate alkalemia",
        example=7.35
    )
    
    pco2: float = Field(
        ...,
        ge=10,
        le=100,
        description="Partial pressure of carbon dioxide in arterial blood (mmHg). Normal range: 35-45 mmHg. Reflects respiratory component of acid-base balance",
        example=40.0
    )
    
    hco3: float = Field(
        ...,
        ge=5,
        le=50,
        description="Bicarbonate concentration in arterial blood (mEq/L). Normal range: 22-26 mEq/L. Reflects metabolic component of acid-base balance",
        example=24.0
    )
    
    po2: Optional[float] = Field(
        None,
        ge=30,
        le=600,
        description="Partial pressure of oxygen in arterial blood (mmHg). Normal range: 80-100 mmHg on room air. Optional parameter for oxygenation assessment",
        example=95.0
    )
    
    fio2: Optional[float] = Field(
        None,
        ge=0.21,
        le=1.0,
        description="Fraction of inspired oxygen (decimal format: 0.21 for room air, 1.0 for 100% oxygen). Optional parameter used with PO2 for oxygenation assessment",
        example=0.21
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "ph": 7.25,
                "pco2": 28.0,
                "hco3": 15.0,
                "po2": 90.0,
                "fio2": 0.21
            }
        }


class AbgAnalyzerResponse(BaseModel):
    """
    Response model for Arterial Blood Gas (ABG) Analyzer
    
    Returns comprehensive analysis of arterial blood gas values including:
    - Primary acid-base disorder identification
    - Assessment of compensation mechanisms
    - Oxygenation evaluation (if PO2 provided)
    - Clinical interpretation and recommendations
    
    The analysis follows established physiological principles:
    - Winter's formula for metabolic acidosis compensation
    - Expected compensation ranges for all primary disorders
    - Differentiation between acute and chronic respiratory disorders
    - Assessment for mixed acid-base disorders
    
    Reference: Berend K, et al. N Engl J Med. 2014;371(15):1434-45.
    """
    
    result: str = Field(
        ...,
        description="Primary acid-base disorder identified (e.g., 'Metabolic Acidosis', 'Respiratory Alkalosis', 'Normal pH')",
        example="Metabolic Acidosis"
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement (empty string for ABG analysis as it's qualitative)",
        example=""
    )
    
    interpretation: str = Field(
        ...,
        description="Comprehensive clinical interpretation including primary disorder, compensation assessment, values summary, and clinical recommendations",
        example="Primary disorder: Metabolic Acidosis. pH 7.25 indicates acidemia. Compensation: Appropriate respiratory compensation (PCO2 28.0, expected 30.5±2). Values: pH 7.25, PCO2 28.0 mmHg, HCO3 15.0 mEq/L. Oxygenation: PO2 90.0 mmHg - Normal oxygenation. Consider calculating anion gap and assessing for underlying causes."
    )
    
    stage: str = Field(
        ...,
        description="Primary disorder category for classification purposes",
        example="Metabolic Acidosis"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the primary disorder",
        example="Primary metabolic acidosis"
    )
    
    detailed_analysis: Optional[Dict[str, Any]] = Field(
        None,
        description="Detailed analysis breakdown including pH status, compensation details, and oxygenation assessment",
        example={
            "ph": 7.25,
            "pco2": 28.0,
            "hco3": 15.0,
            "ph_status": "Acidemia",
            "primary_disorder": "Metabolic Acidosis",
            "compensation": "Appropriate respiratory compensation (PCO2 28.0, expected 30.5±2)",
            "category": "Metabolic Acidosis",
            "description": "Primary metabolic acidosis",
            "oxygenation": {
                "po2": 90.0,
                "status": "Normal",
                "severity": "Normal oxygenation"
            }
        }
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "result": "Metabolic Acidosis",
                "unit": "",
                "interpretation": "Primary disorder: Metabolic Acidosis. pH 7.25 indicates acidemia. Compensation: Appropriate respiratory compensation (PCO2 28.0, expected 30.5±2). Values: pH 7.25, PCO2 28.0 mmHg, HCO3 15.0 mEq/L. Oxygenation: PO2 90.0 mmHg - Normal oxygenation. Consider calculating anion gap and assessing for underlying causes.",
                "stage": "Metabolic Acidosis",
                "stage_description": "Primary metabolic acidosis",
                "detailed_analysis": {
                    "ph": 7.25,
                    "pco2": 28.0,
                    "hco3": 15.0,
                    "ph_status": "Acidemia",
                    "primary_disorder": "Metabolic Acidosis",
                    "compensation": "Appropriate respiratory compensation (PCO2 28.0, expected 30.5±2)",
                    "category": "Metabolic Acidosis",
                    "description": "Primary metabolic acidosis",
                    "oxygenation": {
                        "po2": 90.0,
                        "status": "Normal",
                        "severity": "Normal oxygenation"
                    }
                }
            }
        }
