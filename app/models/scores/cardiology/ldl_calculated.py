"""
LDL Calculated Models

Request and response models for LDL cholesterol calculation using the Friedewald formula.

References (Vancouver style):
1. Friedewald WT, Levy RI, Fredrickson DS. Estimation of the concentration of 
   low-density lipoprotein cholesterol in plasma, without use of the preparative 
   ultracentrifuge. Clin Chem. 1972 Jun;18(6):499-502. PMID: 4337382.
2. National Cholesterol Education Program (NCEP) Expert Panel on Detection, 
   Evaluation, and Treatment of High Blood Cholesterol in Adults (Adult Treatment 
   Panel III). Third Report of the National Cholesterol Education Program (NCEP) 
   Expert Panel on Detection, Evaluation, and Treatment of High Blood Cholesterol 
   in Adults (Adult Treatment Panel III) final report. Circulation. 2002 Dec 
   17;106(25):3143-421. PMID: 12485966.
3. Stone NJ, Robinson JG, Lichtenstein AH, Bairey Merz CN, Blum CB, Eckel RH, et al. 
   2013 ACC/AHA guideline on the treatment of blood cholesterol to reduce 
   atherosclerotic cardiovascular risk in adults. Circulation. 2014 Jun 24;129(25 
   Suppl 2):S1-45. doi: 10.1161/CIR.0000000000000067.
4. Grundy SM, Stone NJ, Bailey AL, Beam C, Birtcher KK, Blumenthal RS, et al. 2018 
   AHA/ACC/AACVPR/AAPA/ABC/ACPM/ADA/AGS/APhA/ASPC/NLA/PCNA Guideline on the Management 
   of Blood Cholesterol. Circulation. 2019 Jun 18;139(25):e1082-e1143. doi: 
   10.1161/CIR.0000000000000625.

The LDL Calculated uses the Friedewald formula to estimate low-density lipoprotein 
(LDL) cholesterol from a standard lipid panel. This calculation has been a cornerstone 
of cardiovascular risk assessment since 1972, providing a cost-effective method for 
LDL estimation when direct measurement is not available.

Clinical Background:
LDL cholesterol is a key marker for cardiovascular risk assessment and a primary target 
for cholesterol-lowering therapy. The Friedewald formula estimates LDL cholesterol by 
subtracting HDL cholesterol and estimated VLDL cholesterol (triglycerides/5) from 
total cholesterol.

Formula: LDL cholesterol = Total cholesterol - HDL cholesterol - (Triglycerides/5)

Clinical Applications:
- Cardiovascular risk stratification and management
- Monitoring response to lipid-lowering therapy
- Screening for dyslipidemia in primary care settings
- Guiding statin therapy initiation and intensity
- Assessment for familial hypercholesterolemia

LDL Cholesterol Categories (ATP III Guidelines):
- Optimal: <100 mg/dL (2.6 mmol/L)
- Near optimal/above optimal: 100-129 mg/dL (2.6-3.3 mmol/L)
- Borderline high: 130-159 mg/dL (3.4-4.1 mmol/L)
- High: 160-189 mg/dL (4.1-4.9 mmol/L)
- Very high: ≥190 mg/dL (≥4.9 mmol/L)

Risk-Based LDL Targets:
- Very high risk (established ASCVD): <70 mg/dL (1.8 mmol/L)
- High risk (diabetes, 10-year ASCVD risk ≥20%): <100 mg/dL (2.6 mmol/L)
- Moderate risk (10-year ASCVD risk 7.5-19.9%): <130 mg/dL (3.4 mmol/L)
- Lower risk (10-year ASCVD risk <7.5%): <160 mg/dL (4.1 mmol/L)

Formula Limitations:
- Inaccurate when triglycerides >400 mg/dL (4.5 mmol/L)
- Requires fasting triglyceride measurement
- May underestimate LDL at low triglyceride levels (<100 mg/dL)
- Less accurate at very low or very high LDL levels
- Not applicable in Type III hyperlipoproteinemia

Modern Considerations:
While the Friedewald formula remains widely used, newer equations like the Martin-Hopkins 
formula and direct LDL measurement methods are available for improved accuracy in specific 
clinical scenarios. The choice of method should consider clinical context, laboratory 
capabilities, and cost-effectiveness.

Clinical Impact:
Accurate LDL cholesterol assessment is crucial for cardiovascular disease prevention 
and management. The Friedewald formula has enabled widespread lipid screening and 
contributed significantly to the reduction in cardiovascular mortality through 
evidence-based statin therapy.
"""

from pydantic import BaseModel, Field
from typing import Optional


class LdlCalculatedRequest(BaseModel):
    """
    Request model for LDL cholesterol calculation using the Friedewald formula
    
    The Friedewald formula calculates LDL cholesterol from a standard lipid panel, 
    providing an estimated LDL value when direct measurement is not available. This 
    calculation requires fasting triglyceride levels for accuracy.
    
    Clinical Parameters:
    - Total Cholesterol: Complete cholesterol content in blood
    - HDL Cholesterol: High-density lipoprotein cholesterol ("good cholesterol")
    - Triglycerides: Fasting triglyceride level (required for formula accuracy)
    
    Formula: LDL cholesterol = Total cholesterol - HDL cholesterol - (Triglycerides/5)
    
    Laboratory Requirements:
    - Fasting lipid panel (9-12 hours fasting required)
    - Standardized laboratory methods for cholesterol measurement
    - Quality control procedures to ensure accurate results
    
    Clinical Context:
    - Used for cardiovascular risk assessment and management
    - Essential for determining statin therapy eligibility and intensity
    - Monitoring tool for lipid-lowering treatment effectiveness
    - Screening tool for dyslipidemia in preventive care
    
    Accuracy Considerations:
    - Most accurate when triglycerides are 100-400 mg/dL
    - Inaccurate when triglycerides >400 mg/dL (use direct LDL measurement)
    - May underestimate LDL when triglycerides <100 mg/dL
    - Less reliable at very low (<70 mg/dL) or very high (>130 mg/dL) LDL levels when triglycerides >200 mg/dL
    
    Quality Assurance:
    - Ensure proper fasting status before blood draw
    - Verify laboratory calibration and quality control
    - Consider direct LDL measurement if accuracy is questioned
    - Account for biological variation in repeat measurements
    
    References (Vancouver style):
    1. Friedewald WT, Levy RI, Fredrickson DS. Estimation of the concentration of 
    low-density lipoprotein cholesterol in plasma, without use of the preparative 
    ultracentrifuge. Clin Chem. 1972 Jun;18(6):499-502.
    2. National Cholesterol Education Program (NCEP) Expert Panel on Detection, 
    Evaluation, and Treatment of High Blood Cholesterol in Adults (Adult Treatment 
    Panel III). Third Report of the National Cholesterol Education Program (NCEP) 
    Expert Panel on Detection, Evaluation, and Treatment of High Blood Cholesterol 
    in Adults (Adult Treatment Panel III) final report. Circulation. 2002 Dec 
    17;106(25):3143-421.
    """
    
    total_cholesterol: float = Field(
        ...,
        description="Total cholesterol level in mg/dL from fasting lipid panel. Represents the sum of "
                   "all cholesterol-containing lipoproteins (LDL, HDL, VLDL). Normal range typically "
                   "considered <200 mg/dL, borderline high 200-239 mg/dL, high ≥240 mg/dL.",
        ge=50.0,
        le=1000.0,
        example=220.0
    )
    
    hdl_cholesterol: float = Field(
        ...,
        description="High-density lipoprotein (HDL) cholesterol level in mg/dL, often called 'good cholesterol'. "
                   "HDL cholesterol helps remove other forms of cholesterol from the bloodstream. "
                   "Low HDL (<40 mg/dL men, <50 mg/dL women) is associated with increased cardiovascular risk. "
                   "High HDL (≥60 mg/dL) is considered protective.",
        ge=10.0,
        le=200.0,
        example=45.0
    )
    
    triglycerides: float = Field(
        ...,
        description="Triglyceride level in mg/dL from fasting lipid panel (9-12 hours fasting required). "
                   "Used to estimate VLDL cholesterol in the Friedewald formula. Normal <150 mg/dL, "
                   "borderline high 150-199 mg/dL, high 200-499 mg/dL, very high ≥500 mg/dL. "
                   "Formula accuracy decreases when >400 mg/dL.",
        ge=30.0,
        le=5000.0,
        example=180.0
    )
    
    class Config:
        schema_extra = {
            "example": {
                "total_cholesterol": 220.0,
                "hdl_cholesterol": 45.0,
                "triglycerides": 180.0
            }
        }


class LdlCalculatedResponse(BaseModel):
    """
    Response model for LDL cholesterol calculation using the Friedewald formula
    
    Provides calculated LDL cholesterol with clinical interpretation, accuracy assessment, 
    and evidence-based recommendations for cardiovascular risk management. The response 
    includes risk stratification and treatment guidance based on current clinical guidelines.
    
    LDL Cholesterol Interpretation:
    
    Optimal (<100 mg/dL):
    - Excellent level for cardiovascular health
    - Continue healthy lifestyle practices
    - May still require medication in very high-risk patients
    
    Near Optimal (100-129 mg/dL):
    - Above optimal but not requiring medication in most patients
    - Lifestyle modifications recommended
    - Consider medication based on overall cardiovascular risk
    
    Borderline High (130-159 mg/dL):
    - Increased cardiovascular risk
    - Lifestyle modifications strongly recommended
    - Consider medication therapy based on risk factors
    
    High (160-189 mg/dL):
    - Significantly elevated cardiovascular risk
    - Intensive lifestyle modifications required
    - Medication therapy likely indicated
    
    Very High (≥190 mg/dL):
    - Very high cardiovascular risk
    - Medication therapy strongly recommended
    - Consider familial hypercholesterolemia evaluation
    
    Clinical Decision Making:
    - Risk assessment should include additional factors: age, sex, race, blood pressure, 
      diabetes, smoking status, family history
    - Use pooled cohort equations or other risk calculators for comprehensive assessment
    - Consider calcium scoring or other advanced testing in intermediate-risk patients
    - Shared decision-making important for treatment choices
    
    Treatment Considerations:
    - Lifestyle modifications: heart-healthy diet, regular physical activity, weight management
    - Statin therapy: first-line medication for most patients requiring LDL reduction
    - Non-statin therapy: ezetimibe, PCSK9 inhibitors for additional LDL reduction if needed
    - Monitoring: repeat lipid panel 4-12 weeks after initiating or changing therapy
    
    Accuracy Limitations:
    - Formula most accurate when triglycerides 100-400 mg/dL
    - Direct LDL measurement recommended when triglycerides >400 mg/dL
    - Consider Martin-Hopkins equation for improved accuracy in some populations
    - Biological variation: ±10-15% between measurements is normal
    
    Quality Measures:
    - Ensure proper fasting status (9-12 hours)
    - Use standardized laboratory methods
    - Consider patient factors affecting lipid levels (medications, illness, pregnancy)
    - Interpret results in clinical context
    
    Reference: Friedewald WT, et al. Clin Chem. 1972;18(6):499-502.
    """
    
    result: float = Field(
        ...,
        description="Calculated LDL cholesterol level in mg/dL using the Friedewald formula",
        example=139.0
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for LDL cholesterol",
        example="mg/dL"
    )
    
    interpretation: str = Field(
        ...,
        description="Comprehensive clinical interpretation including LDL level assessment, accuracy considerations, "
                   "cardiovascular risk implications, and evidence-based management recommendations",
        example="Calculated LDL cholesterol: 139.0 mg/dL using Friedewald formula (Total cholesterol 220.0 - HDL 45.0 - Triglycerides/5 [180.0/5]). LDL level is borderline high. Lifestyle modifications strongly recommended. Consider medication therapy based on overall cardiovascular risk assessment and patient factors. LDL targets vary by cardiovascular risk: <70 mg/dL (very high risk), <100 mg/dL (high risk), <130 mg/dL (moderate risk), <160 mg/dL (lower risk). This calculation requires fasting triglycerides for accuracy. Results should be interpreted in context of overall cardiovascular risk assessment including other lipid parameters, blood pressure, diabetes, smoking status, and family history."
    )
    
    stage: str = Field(
        ...,
        description="LDL cholesterol risk category based on clinical guidelines",
        example="Borderline High"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the LDL cholesterol level",
        example="Borderline high LDL cholesterol"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 139.0,
                "unit": "mg/dL",
                "interpretation": "Calculated LDL cholesterol: 139.0 mg/dL using Friedewald formula (Total cholesterol 220.0 - HDL 45.0 - Triglycerides/5 [180.0/5]). LDL level is borderline high. Lifestyle modifications strongly recommended. Consider medication therapy based on overall cardiovascular risk assessment and patient factors. LDL targets vary by cardiovascular risk: <70 mg/dL (very high risk), <100 mg/dL (high risk), <130 mg/dL (moderate risk), <160 mg/dL (lower risk). This calculation requires fasting triglycerides for accuracy. Results should be interpreted in context of overall cardiovascular risk assessment including other lipid parameters, blood pressure, diabetes, smoking status, and family history.",
                "stage": "Borderline High",
                "stage_description": "Borderline high LDL cholesterol"
            }
        }