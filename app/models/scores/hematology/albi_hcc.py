"""
ALBI (Albumin-Bilirubin) Grade for Hepatocellular Carcinoma (HCC) Models

Request and response models for ALBI Grade calculation.

References (Vancouver style):
1. Johnson PJ, Berhane S, Kagebayashi C, Senyurek I, Yazan E, Fox R, et al. 
   Assessment of liver function in patients with hepatocellular carcinoma: a new 
   evidence-based approach-the ALBI grade. J Clin Oncol. 2015 Feb 20;33(6):550-8. 
   doi: 10.1200/JCO.2014.57.9151.
2. Hiraoka A, Michitaka K, Kumada T, Izumi N, Kadoya M, Kokudo N, et al. 
   Validation and Potential of Albumin-Bilirubin Grade and Prognostication in a 
   Nationwide Survey of 46,681 Hepatocellular Carcinoma Patients in Japan: The Need 
   for a More Detailed Evaluation of Hepatic Function. Liver Cancer. 2017;6(4):325-336. 
   doi: 10.1159/000479984.
3. Chen B, Lin S. Albumin-bilirubin (ALBI) score at admission predicts possible 
   outcomes in patients with acute-on-chronic liver failure. Medicine (Baltimore). 
   2017 Jun;96(24):e7142. doi: 10.1097/MD.0000000000007142.

The ALBI (Albumin-Bilirubin) Grade is a simple, objective model that predicts 
survival in hepatocellular carcinoma (HCC) patients based on serum albumin and 
bilirubin concentrations. It serves as an alternative to the Child-Pugh grade 
without the need for subjective variables like ascites and encephalopathy. The 
ALBI score uses the formula: (log10 bilirubin × 0.66) + (albumin × -0.085), 
where bilirubin is in μmol/L and albumin is in g/L.
"""

from pydantic import BaseModel, Field
from typing import Literal


class AlbiHccRequest(BaseModel):
    """
    Request model for ALBI (Albumin-Bilirubin) Grade for Hepatocellular Carcinoma (HCC)
    
    The ALBI Grade employs objective measures of liver function to predict survival 
    in HCC patients. It uses only two laboratory parameters:
    
    Serum Albumin (g/L):
    - Normal range: 35-50 g/L
    - Reflects synthetic function of the liver
    - Lower values indicate impaired liver function
    - Influences oncotic pressure and drug binding
    
    Serum Bilirubin (μmol/L):
    - Normal range: 3-20 μmol/L  
    - Reflects liver's ability to conjugate and excrete bilirubin
    - Elevated levels indicate liver dysfunction or biliary obstruction
    - Important marker of hepatic clearance capacity
    
    The ALBI formula: (log10 bilirubin × 0.66) + (albumin × -0.085)
    Results in three grades:
    - Grade 1 (≤-2.60): Best prognosis, 18.5-85.6 months median survival
    - Grade 2 (>-2.60 to ≤-1.39): Intermediate prognosis, 5.3-46.5 months median survival  
    - Grade 3 (>-1.39): Poorest prognosis, 2.3-15.5 months median survival

    This grading system provides prognostic information for treatment planning 
    and patient counseling in HCC management.

    References (Vancouver style):
    1. Johnson PJ, Berhane S, Kagebayashi C, Senyurek I, Yazan E, Fox R, et al. 
    Assessment of liver function in patients with hepatocellular carcinoma: a new 
    evidence-based approach-the ALBI grade. J Clin Oncol. 2015 Feb 20;33(6):550-8. 
    doi: 10.1200/JCO.2014.57.9151.
    2. Hiraoka A, Michitaka K, Kumada T, Izumi N, Kadoya M, Kokudo N, et al. 
    Validation and Potential of Albumin-Bilirubin Grade and Prognostication in a 
    Nationwide Survey of 46,681 Hepatocellular Carcinoma Patients in Japan: The Need 
    for a More Detailed Evaluation of Hepatic Function. Liver Cancer. 2017;6(4):325-336. 
    doi: 10.1159/000479984.
    3. Chen B, Lin S. Albumin-bilirubin (ALBI) score at admission predicts possible 
    outcomes in patients with acute-on-chronic liver failure. Medicine (Baltimore). 
    2017 Jun;96(24):e7142. doi: 10.1097/MD.0000000000007142.
    """
    
    albumin: float = Field(
        ...,
        ge=1.0,
        le=6.0,
        description="Serum albumin concentration in g/L. Normal range: 35-50 g/L. Lower values indicate impaired hepatic synthetic function",
        example=3.5
    )
    
    bilirubin: float = Field(
        ...,
        ge=3.0,
        le=500.0,
        description="Serum bilirubin concentration in μmol/L. Normal range: 3-20 μmol/L. Elevated values indicate hepatic dysfunction or biliary obstruction",
        example=25.0
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "albumin": 3.5,
                "bilirubin": 25.0
            }
        }


class AlbiHccResponse(BaseModel):
    """
    Response model for ALBI (Albumin-Bilirubin) Grade for Hepatocellular Carcinoma (HCC)
    
    The ALBI Grade provides objective assessment of liver function in HCC patients:
    
    Grade 1 (Score ≤-2.60): 
    - Best liver function and prognosis
    - Median survival: 18.5-85.6 months
    - Suitable for more aggressive treatment approaches
    
    Grade 2 (Score >-2.60 to ≤-1.39):
    - Intermediate liver function and prognosis  
    - Median survival: 5.3-46.5 months
    - Moderate treatment considerations
    
    Grade 3 (Score >-1.39):
    - Poorest liver function and prognosis
    - Median survival: 2.3-15.5 months
    - Conservative treatment approach recommended
    
    The ALBI Grade has been validated as an alternative to Child-Pugh grade 
    with superior objectivity and reproducibility.
    
    Reference: Johnson PJ, et al. J Clin Oncol. 2015;33(6):550-8.
    """
    
    result: float = Field(
        ...,
        description="ALBI score calculated using the formula: (log10 bilirubin × 0.66) + (albumin × -0.085)",
        example=-2.85
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the ALBI score",
        example="score"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation with survival prediction and treatment considerations",
        example="ALBI Grade 1 (score ≤-2.60). Median survival: 18.5 - 85.6 months. Best liver function and prognosis in HCC patients. This grade indicates relatively preserved liver function with the longest expected survival among HCC patients."
    )
    
    stage: str = Field(
        ...,
        description="ALBI Grade classification (Grade 1, Grade 2, or Grade 3)",
        example="Grade 1"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the prognostic category",
        example="Best prognosis"
    )
    
    grade: int = Field(
        ...,
        ge=1,
        le=3,
        description="Numeric ALBI grade (1=best, 2=intermediate, 3=poorest prognosis)",
        example=1
    )
    
    survival_range: str = Field(
        ...,
        description="Expected median survival range for the assigned ALBI grade",
        example="18.5 - 85.6 months"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "result": -2.85,
                "unit": "score", 
                "interpretation": "ALBI Grade 1 (score ≤-2.60). Median survival: 18.5 - 85.6 months. Best liver function and prognosis in HCC patients. This grade indicates relatively preserved liver function with the longest expected survival among HCC patients.",
                "stage": "Grade 1",
                "stage_description": "Best prognosis",
                "grade": 1,
                "survival_range": "18.5 - 85.6 months"
            }
        }