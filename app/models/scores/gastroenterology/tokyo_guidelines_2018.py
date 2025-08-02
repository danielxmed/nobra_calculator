"""
Tokyo Guidelines 2018 for Acute Cholecystitis Models

Request and response models for Tokyo Guidelines 2018 diagnostic criteria and severity grading.

References (Vancouver style):
1. Yokoe M, Hata J, Takada T, Strasberg SM, Asbun HJ, Wakabayashi G, et al. Tokyo Guidelines 
   2018: diagnostic criteria and severity grading of acute cholecystitis (with videos). 
   J Hepatobiliary Pancreat Sci. 2018 Jan;25(1):41-54. doi: 10.1002/jhbp.515.
2. Takada T, Strasberg SM, Solomkin JS, Pitt HA, Gomi H, Yoshida M, et al. TG13: Updated 
   Tokyo Guidelines for the management of acute cholangitis and cholecystitis. J Hepatobiliary 
   Pancreat Sci. 2013 Jan;20(1):1-7. doi: 10.1007/s00534-012-0566-y.
3. Gomi H, Solomkin JS, Schlossberg D, Okamoto K, Takada T, Strasberg SM, et al. Tokyo 
   Guidelines 2018: antimicrobial therapy for acute cholangitis and cholecystitis. 
   J Hepatobiliary Pancreat Sci. 2018 Jan;25(1):3-16. doi: 10.1002/jhbp.518.

The Tokyo Guidelines 2018 (TG18) provide evidence-based diagnostic criteria and severity 
grading for acute cholecystitis. TG18 maintains the same diagnostic criteria as TG13, 
requiring local signs of inflammation (Part A), systemic signs of inflammation (Part B), 
and imaging findings (Part C) for definite diagnosis. The severity grading stratifies 
patients into Grade I (mild), Grade II (moderate with local inflammation), and Grade III 
(severe with organ dysfunction), with corresponding 30-day mortality rates of 1.1%, 5.4%, 
and 18.8% respectively.
"""

from pydantic import BaseModel, Field
from typing import Literal, Optional


class TokyoGuidelines2018Request(BaseModel):
    """
    Request model for Tokyo Guidelines 2018 for Acute Cholecystitis
    
    The TG18 diagnostic criteria consist of three parts:
    
    Part A - Local signs of inflammation:
    - Murphy's sign: Cessation of breathing during RUQ palpation
    - RUQ pain/tenderness/mass
    
    Part B - Systemic signs of inflammation:
    - Fever >38°C (>100.4°F)
    - Elevated CRP >3 mg/dL
    - Elevated WBC >10,000/mm³
    
    Part C - Imaging findings:
    - Characteristic findings of acute cholecystitis
    
    Severity grading criteria include:
    - Grade III: Organ dysfunction
    - Grade II: Local inflammation markers
    - Grade I: Neither Grade II nor III criteria
    
    References (Vancouver style):
    1. Yokoe M, Hata J, Takada T, Strasberg SM, Asbun HJ, Wakabayashi G, et al. Tokyo Guidelines 
       2018: diagnostic criteria and severity grading of acute cholecystitis (with videos). 
       J Hepatobiliary Pancreat Sci. 2018 Jan;25(1):41-54. doi: 10.1002/jhbp.515.
    """
    
    # Part A: Local signs of inflammation
    murphys_sign: Literal["yes", "no"] = Field(
        ...,
        description="Murphy's sign present - Cessation of breathing during deep palpation of right upper quadrant",
        example="yes"
    )
    
    ruq_pain: Literal["yes", "no"] = Field(
        ...,
        description="Right upper abdominal quadrant mass, pain, or tenderness",
        example="yes"
    )
    
    # Part B: Systemic signs of inflammation
    fever: Literal["yes", "no"] = Field(
        ...,
        description="Fever present (>38°C or >100.4°F)",
        example="yes"
    )
    
    elevated_crp: Literal["yes", "no"] = Field(
        ...,
        description="Elevated CRP (>3 mg/dL)",
        example="no"
    )
    
    elevated_wbc: Literal["yes", "no"] = Field(
        ...,
        description="Elevated WBC count (>10,000/mm³)",
        example="yes"
    )
    
    # Part C: Imaging findings
    imaging_findings: Literal["yes", "no"] = Field(
        ...,
        description="Imaging findings characteristic of acute cholecystitis (e.g., pericholecystic fluid, gallstones/debris, gallbladder wall thickening >4mm, sonographic Murphy sign)",
        example="yes"
    )
    
    # Grade III criteria - Organ dysfunction
    cardiovascular_dysfunction: Literal["yes", "no"] = Field(
        ...,
        description="Cardiovascular dysfunction - Hypotension requiring treatment with dopamine ≥5 μg/kg per min or any dose of norepinephrine",
        example="no"
    )
    
    neurological_dysfunction: Literal["yes", "no"] = Field(
        ...,
        description="Neurological dysfunction - Decreased level of consciousness",
        example="no"
    )
    
    respiratory_dysfunction: Literal["yes", "no"] = Field(
        ...,
        description="Respiratory dysfunction - PaO2/FiO2 ratio <300",
        example="no"
    )
    
    renal_dysfunction: Literal["yes", "no"] = Field(
        ...,
        description="Renal dysfunction - Oliguria or creatinine >2.0 mg/dL",
        example="no"
    )
    
    hepatic_dysfunction: Literal["yes", "no"] = Field(
        ...,
        description="Hepatic dysfunction - PT-INR >1.5",
        example="no"
    )
    
    hematological_dysfunction: Literal["yes", "no"] = Field(
        ...,
        description="Hematological dysfunction - Platelet count <100,000/mm³",
        example="no"
    )
    
    # Grade II criteria - Local inflammation
    wbc_over_18000: Literal["yes", "no"] = Field(
        ...,
        description="Elevated WBC count >18,000/mm³",
        example="no"
    )
    
    palpable_mass: Literal["yes", "no"] = Field(
        ...,
        description="Palpable tender mass in the right upper abdominal quadrant",
        example="no"
    )
    
    duration_over_72h: Literal["yes", "no"] = Field(
        ...,
        description="Duration of complaints >72 hours",
        example="no"
    )
    
    marked_inflammation: Literal["yes", "no"] = Field(
        ...,
        description="Marked local inflammation (gangrenous cholecystitis, pericholecystic abscess, hepatic abscess, biliary peritonitis, emphysematous cholecystitis)",
        example="no"
    )
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "murphys_sign": "yes",
                "ruq_pain": "yes",
                "fever": "yes",
                "elevated_crp": "no",
                "elevated_wbc": "yes",
                "imaging_findings": "yes",
                "cardiovascular_dysfunction": "no",
                "neurological_dysfunction": "no",
                "respiratory_dysfunction": "no",
                "renal_dysfunction": "no",
                "hepatic_dysfunction": "no",
                "hematological_dysfunction": "no",
                "wbc_over_18000": "no",
                "palpable_mass": "no",
                "duration_over_72h": "no",
                "marked_inflammation": "no"
            }
        }
    }


class TokyoGuidelines2018Response(BaseModel):
    """
    Response model for Tokyo Guidelines 2018 for Acute Cholecystitis
    
    Diagnostic criteria:
    - Suspected: Part A + Part B
    - Definite: Part A + Part B + Part C
    
    Severity grading (30-day mortality):
    - Grade I (Mild): 1.1% mortality
    - Grade II (Moderate): 5.4% mortality  
    - Grade III (Severe): 18.8% mortality
    
    Reference: Yokoe M, et al. J Hepatobiliary Pancreat Sci. 2018;25(1):41-54.
    """
    
    result: str = Field(
        ...,
        description="Diagnostic result and severity grade",
        example="Grade I (Mild) Acute Cholecystitis"
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement (empty for this assessment)",
        example=""
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation with management recommendations based on diagnosis and severity",
        example="Mild acute cholecystitis without organ dysfunction. 1.1% 30-day mortality. Early laparoscopic cholecystectomy recommended if patient can tolerate surgery."
    )
    
    stage: str = Field(
        ...,
        description="Diagnostic stage and severity grade",
        example="Grade I (Mild)"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the stage",
        example="Mild acute cholecystitis"
    )
    
    diagnosis: str = Field(
        ...,
        description="Diagnostic result (negative, suspected, or definite)",
        example="definite"
    )
    
    severity_grade: str = Field(
        ...,
        description="Severity grade (grade_i, grade_ii, grade_iii, or N/A)",
        example="grade_i"
    )
    
    mortality_rate: Optional[str] = Field(
        None,
        description="30-day mortality rate based on severity grade",
        example="1.1%"
    )
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "result": "Grade I (Mild) Acute Cholecystitis",
                "unit": "",
                "interpretation": "Mild acute cholecystitis without organ dysfunction. 1.1% 30-day mortality. Early laparoscopic cholecystectomy recommended if patient can tolerate surgery.",
                "stage": "Grade I (Mild)",
                "stage_description": "Mild acute cholecystitis",
                "diagnosis": "definite",
                "severity_grade": "grade_i",
                "mortality_rate": "1.1%"
            }
        }
    }