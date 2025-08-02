"""
Metabolic Score for Insulin Resistance (METS-IR) Models

Request and response models for METS-IR calculation.

References (Vancouver style):
1. Bello-Chavolla OY, Almeda-Valdes P, Gomez-Velasco D, Viveros-Ruiz T, Cruz-Bautista I, 
   Romo-Romo A, et al. METS-IR, a novel score to evaluate insulin sensitivity, is 
   predictive of visceral adiposity and incident type 2 diabetes. Eur J Endocrinol. 
   2018 May;178(5):533-544. doi: 10.1530/EJE-17-0883.
2. Zhang M, Liu D, Qin P, Liu Y, Sun X, Li H, et al. Association of metabolic score 
   for insulin resistance and its 6-year change with incident type 2 diabetes mellitus. 
   J Diabetes. 2021 Sep;13(9):725-734. doi: 10.1111/1753-0407.13167.
3. Bello-Chavolla OY, Antonio-Villa NE, Vargas-Vázquez A, Martagón AJ, Mehta R, 
   Arellano-Campos O, et al. Metabolic Score for Visceral Fat (METS-VF), a novel 
   estimator of intra-abdominal fat content and cardio-metabolic health. Clin Nutr. 
   2020 May;39(5):1613-1621. doi: 10.1016/j.clnu.2019.07.012.

The METS-IR is a practical, non-insulin dependent marker for insulin resistance that 
predicts visceral adiposity and incident type 2 diabetes. It uses routine metabolic 
parameters (fasting glucose, triglycerides, BMI, and HDL cholesterol) making it ideal 
for primary care settings where insulin measurements may not be readily available.
"""

from pydantic import BaseModel, Field, validator


class MetsIrRequest(BaseModel):
    """
    Request model for Metabolic Score for Insulin Resistance (METS-IR) calculation
    
    The METS-IR uses four readily available metabolic parameters to assess insulin 
    resistance and predict type 2 diabetes risk:
    
    Formula: METS-IR = (ln((2 × Fasting Glucose) + Triglycerides) × BMI) / ln(HDL Cholesterol)
    
    Key Features:
    - Does not require insulin measurements (unlike HOMA-IR)
    - Correlates with visceral adiposity and metabolic dysfunction
    - Predicts incident type 2 diabetes with good accuracy
    - Simple calculation using routine lab values
    
    Clinical Context:
    Insulin resistance is a key pathophysiological feature of type 2 diabetes and 
    metabolic syndrome. The METS-IR was developed using data from Mexican populations 
    and validated in Asian cohorts, showing superior performance compared to other 
    non-insulin based indices for predicting diabetes risk.
    
    References (Vancouver style):
    1. Bello-Chavolla OY, Almeda-Valdes P, Gomez-Velasco D, Viveros-Ruiz T, Cruz-Bautista I, 
       Romo-Romo A, et al. METS-IR, a novel score to evaluate insulin sensitivity, is 
       predictive of visceral adiposity and incident type 2 diabetes. Eur J Endocrinol. 
       2018 May;178(5):533-544. doi: 10.1530/EJE-17-0883.
    """
    
    fasting_glucose: float = Field(
        ...,
        description="Fasting plasma glucose level in mg/dL. Should be measured after at least "
                    "8 hours of fasting. Normal range is 70-105 mg/dL. Values above 126 mg/dL "
                    "on two occasions indicate diabetes.",
        ge=40,
        le=700,
        example=95.0
    )
    
    triglycerides: float = Field(
        ...,
        description="Fasting triglyceride level in mg/dL. Should be measured after 9-12 hours "
                    "of fasting. Normal is <150 mg/dL. Elevated triglycerides are associated "
                    "with insulin resistance and metabolic syndrome.",
        ge=10,
        le=2000,
        example=120.0
    )
    
    bmi: float = Field(
        ...,
        description="Body Mass Index calculated as weight(kg)/height(m)². Normal range is "
                    "18.5-24.9 kg/m². BMI is included as it reflects adiposity, which is "
                    "closely linked to insulin resistance.",
        ge=10,
        le=70,
        example=27.5
    )
    
    hdl_cholesterol: float = Field(
        ...,
        description="High-density lipoprotein cholesterol in mg/dL. Protective cholesterol "
                    "that is typically low in insulin resistance. Normal is ≥40 mg/dL for "
                    "men and ≥50 mg/dL for women.",
        ge=10,
        le=200,
        example=45.0
    )
    
    @validator('fasting_glucose')
    def validate_glucose(cls, v):
        """Validate fasting glucose is within physiological range"""
        if v < 40:
            raise ValueError("Fasting glucose below 40 mg/dL is critically low")
        if v > 700:
            raise ValueError("Fasting glucose above 700 mg/dL requires immediate medical attention")
        return v
    
    @validator('triglycerides')
    def validate_triglycerides(cls, v):
        """Validate triglycerides are within measurable range"""
        if v < 10:
            raise ValueError("Triglycerides below 10 mg/dL is unusually low")
        if v > 2000:
            raise ValueError("Triglycerides above 2000 mg/dL indicates severe hypertriglyceridemia")
        return v
    
    class Config:
        schema_extra = {
            "example": {
                "fasting_glucose": 95.0,
                "triglycerides": 120.0,
                "bmi": 27.5,
                "hdl_cholesterol": 45.0
            }
        }


class MetsIrResponse(BaseModel):
    """
    Response model for Metabolic Score for Insulin Resistance (METS-IR) calculation
    
    The METS-IR provides a quantitative assessment of insulin resistance and diabetes risk:
    
    - Score ≤50.39: Low risk of developing type 2 diabetes
    - Score >50.39: High risk of developing type 2 diabetes
    
    Clinical Applications:
    - Primary care screening for diabetes risk
    - Identifying candidates for lifestyle interventions
    - Monitoring metabolic health changes over time
    - Risk stratification in preventive medicine
    
    Important Considerations:
    - Not a diagnostic tool for diabetes
    - Should be interpreted alongside clinical context
    - May need adjustment for different ethnic populations
    - All measurements should be taken in fasting state
    
    Reference: Bello-Chavolla OY, et al. Eur J Endocrinol. 2018;178(5):533-544.
    """
    
    result: float = Field(
        ...,
        description="The calculated METS-IR score. Higher values indicate greater insulin "
                    "resistance and increased diabetes risk.",
        example=48.75
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score (dimensionless)",
        example=""
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation of the score including risk level and "
                    "recommended actions",
        example="Low risk of developing Type 2 Diabetes. Continue routine screening "
                "and maintain healthy lifestyle habits including diet and exercise."
    )
    
    stage: str = Field(
        ...,
        description="Risk category classification (Low Risk or High Risk)",
        example="Low Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Description of the risk category based on cutoff value",
        example="METS-IR ≤50.39"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 48.75,
                "unit": "",
                "interpretation": "Low risk of developing Type 2 Diabetes. Continue routine "
                                "screening and maintain healthy lifestyle habits including "
                                "diet and exercise.",
                "stage": "Low Risk",
                "stage_description": "METS-IR ≤50.39"
            }
        }