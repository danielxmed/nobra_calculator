"""
Ganzoni Equation for Iron Deficiency Anemia Models

Request and response models for Ganzoni Equation iron deficit calculation.

References (Vancouver style):
1. Ganzoni AM. Intravenous iron-dextran: therapeutic and experimental possibilities. 
   Schweiz Med Wochenschr. 1970;100(7):301-3. (German)
2. Auerbach M, Adamson JW. How we diagnose and treat iron deficiency anemia. 
   Am J Hematol. 2016;91(1):31-8. doi: 10.1002/ajh.24201.
3. Camaschella C. Iron-deficiency anemia. N Engl J Med. 2015;372(19):1832-43. 
   doi: 10.1056/NEJMra1401038.

The Ganzoni equation is a validated mathematical formula used to calculate the total 
body iron deficit in patients with iron deficiency anemia. This calculation helps 
clinicians determine the precise amount of iron replacement therapy needed to correct 
both hemoglobin levels and replenish iron stores.

Clinical Applications:
- Dosing calculations for IV iron therapy in iron deficiency anemia
- Assessment of total body iron deficit before treatment initiation
- Planning iron replacement therapy regimens
- Monitoring adequacy of iron repletion therapy
- Research applications in iron deficiency studies

Formula: Iron deficit (mg) = body weight (kg) × (target Hb - current Hb) (g/dL) × 2.4 + iron stores (mg)

Key Components:
- Factor 2.4 = 0.0034 × 0.07 × 10,000 (iron content × blood volume × conversion factor)
- Target Hb typically 15 g/dL for adults
- Iron stores typically 500 mg (minimum for small women)
- Validated only for patients ≥35 kg body weight
"""

from pydantic import BaseModel, Field, validator
from typing import Optional


class GanzoniEquationIronDeficiencyRequest(BaseModel):
    """
    Request model for Ganzoni Equation Iron Deficiency Assessment
    
    The Ganzoni equation calculates total body iron deficit to guide IV iron dosing 
    in patients with iron deficiency anemia. This validated formula accounts for both 
    hemoglobin correction and iron store repletion.
    
    **CLINICAL INDICATIONS**:
    - Iron deficiency anemia requiring IV iron therapy
    - Patients with poor oral iron tolerance or absorption
    - Chronic blood loss with ongoing iron deficiency
    - Functional iron deficiency in chronic disease
    - Pre-operative iron optimization
    - Post-partum iron deficiency anemia
    
    **ELIGIBILITY CRITERIA**:
    
    **Inclusion Criteria**:
    - Body weight ≥35 kg (formula validation threshold)
    - Confirmed iron deficiency anemia (low ferritin, transferrin saturation <20%)
    - Hemoglobin below target levels
    - Clinical indication for iron replacement therapy
    
    **Exclusion Criteria**:
    - Body weight <35 kg (pediatric patients - formula not validated)
    - Iron overload conditions (hemochromatosis, transfusional iron overload)
    - Active infection or inflammation (may affect iron absorption)
    - Hypersensitivity to IV iron preparations
    
    **PARAMETER INTERPRETATION GUIDE**:
    
    **1. Body Weight (≥35 kg)**:
    - **Critical Requirement**: Formula only validated for patients ≥35 kg
    - **Actual vs Ideal Weight**: Use actual body weight, not ideal body weight
    - **Obesity Considerations**: Formula remains valid in obese patients
    - **Fluid Status**: Use dry weight if significant edema present
    
    **2. Current Hemoglobin (3.0-12.0 g/dL)**:
    - **Measurement Timing**: Should be recent (within 1 week) and stable
    - **Laboratory Considerations**: Ensure proper sample handling, avoid hemolysis
    - **Clinical Context**: Consider recent transfusions or blood loss
    - **Normal Ranges**:
      - Adult males: 13.5-17.5 g/dL
      - Adult females: 12.0-16.0 g/dL
      - Elderly: May be slightly lower
    
    **3. Target Hemoglobin (10.0-18.0 g/dL)**:
    - **Standard Target**: 15 g/dL for most adults
    - **Age-Adjusted Targets**:
      - Young adults: 15-16 g/dL
      - Elderly (>65 years): 12-14 g/dL may be appropriate
      - Pregnancy: 11-12 g/dL in later trimesters
    - **Comorbidity Adjustments**:
      - Heart failure: Lower targets (11-12 g/dL) may be appropriate
      - Chronic kidney disease: 10-12 g/dL per guidelines
      - Cancer patients: 10-12 g/dL typically targeted
    - **Clinical Judgment**: Always individualize based on symptoms and comorbidities
    
    **4. Iron Stores (0-1000 mg)**:
    - **Standard Value**: 500 mg for most adults
    - **Rationale**: Represents minimum iron stores for small women
    - **Adjustments**:
      - Large men: May use 600-800 mg
      - Small women: 300-500 mg
      - Elderly: May use 300-400 mg
    - **Modified Formula**: Consider 0 mg if TSAT >20% and ferritin >50 ng/mL
    
    **CLINICAL DECISION FRAMEWORK**:
    
    **Pre-Calculation Assessment**:
    - Confirm iron deficiency: Ferritin <30 ng/mL or <100 ng/mL with inflammation
    - Check transferrin saturation <20%
    - Rule out other causes of anemia
    - Assess for ongoing blood loss
    - Review contraindications to IV iron
    
    **Post-Calculation Planning**:
    - **Mild Deficit (<500 mg)**: Consider oral iron or single IV dose
    - **Moderate Deficit (500-1000 mg)**: IV iron preferred, 1-2 doses
    - **Severe Deficit (1000-2000 mg)**: Multiple IV iron sessions required
    - **Very Severe Deficit (>2000 mg)**: Investigate underlying cause, specialist referral
    
    **SAFETY CONSIDERATIONS**:
    - **Iron Overload Risk**: Monitor ferritin and transferrin saturation
    - **Hypersensitivity**: Pre-medication may be required
    - **Cardiac Status**: Consider slower infusion rates in heart failure
    - **Kidney Disease**: Adjust expectations for hemoglobin response
    
    **MONITORING PLAN**:
    - **Hemoglobin**: Check in 2-4 weeks, then monthly until stable
    - **Iron Studies**: Repeat in 4-8 weeks after completion of therapy
    - **Ferritin Target**: 100-300 ng/mL indicates adequate repletion
    - **Transferrin Saturation**: Target >20% indicates adequate iron availability
    
    **DRUG SELECTION GUIDANCE**:
    - **Iron Sucrose**: 200 mg weekly, well-tolerated, multiple doses needed
    - **Ferric Carboxymaltose**: 500-1000 mg per dose, fewer visits required
    - **Iron Dextran**: High dose possible but higher hypersensitivity risk
    - **Ferric Gluconate**: 125 mg per dose, multiple visits required
    
    References (Vancouver style):
    1. Ganzoni AM. Intravenous iron-dextran: therapeutic and experimental possibilities. 
       Schweiz Med Wochenschr. 1970;100(7):301-3.
    2. Auerbach M, Adamson JW. How we diagnose and treat iron deficiency anemia. 
       Am J Hematol. 2016;91(1):31-8.
    3. Camaschella C. Iron-deficiency anemia. N Engl J Med. 2015;372(19):1832-43.
    """
    
    body_weight: float = Field(
        ...,
        description="Patient's body weight in kilograms. Must be ≥35 kg as formula not validated for lower weights",
        ge=35,
        le=200,
        example=70.0
    )
    
    current_hemoglobin: float = Field(
        ...,
        description="Current hemoglobin level in g/dL. Should be recent measurement (<1 week) and representative of stable state",
        ge=3.0,
        le=12.0,
        example=8.5
    )
    
    target_hemoglobin: float = Field(
        ...,
        description="Target hemoglobin level in g/dL. Standard is 15 g/dL for adults, but may be adjusted for age and comorbidities",
        ge=10.0,
        le=18.0,
        example=15.0
    )
    
    iron_stores: int = Field(
        ...,
        description="Iron stores to be replenished in mg. Typically 500 mg for adults (minimum for small women). Use 0 if TSAT >20% and ferritin >50 ng/mL",
        ge=0,
        le=1000,
        example=500
    )
    
    @validator('target_hemoglobin')
    def target_must_exceed_current(cls, v, values):
        if 'current_hemoglobin' in values and v <= values['current_hemoglobin']:
            raise ValueError('Target hemoglobin must be higher than current hemoglobin')
        return v
    
    class Config:
        schema_extra = {
            "example": {
                "body_weight": 70.0,
                "current_hemoglobin": 8.5,
                "target_hemoglobin": 15.0,
                "iron_stores": 500
            }
        }


class GanzoniEquationIronDeficiencyResponse(BaseModel):
    """
    Response model for Ganzoni Equation Iron Deficiency Assessment
    
    The response provides the calculated total iron deficit along with evidence-based 
    clinical recommendations for iron replacement therapy, monitoring, and safety considerations.
    
    **CLINICAL INTERPRETATION FRAMEWORK**:
    
    **Iron Deficit Categories and Management**:
    
    **Mild Deficit (<500 mg)**:
    - **Clinical Significance**: Small iron deficit, may respond to oral therapy
    - **Treatment Options**:
      - **Oral Iron**: Ferrous sulfate 325 mg (65 mg elemental iron) 2-3 times daily
      - **IV Iron**: Single dose iron sucrose 200-300 mg or ferric carboxymaltose 500 mg
    - **Monitoring**: Hemoglobin in 2-4 weeks, iron studies in 3 months
    - **Expected Response**: Hemoglobin increase 1-2 g/dL in 3-4 weeks
    
    **Moderate Deficit (500-1000 mg)**:
    - **Clinical Significance**: Moderate iron deficiency, IV iron preferred
    - **Treatment Recommendations**:
      - **First-line**: IV iron therapy (oral likely insufficient)
      - **Iron Sucrose**: 200 mg weekly × 3-5 doses
      - **Ferric Carboxymaltose**: 500-1000 mg in 1-2 doses
    - **Monitoring**: Hemoglobin every 2 weeks initially, iron studies in 1 month
    - **Duration**: Complete repletion typically 4-8 weeks
    
    **Severe Deficit (1000-2000 mg)**:
    - **Clinical Significance**: Significant iron deficiency requiring systematic approach
    - **Treatment Strategy**:
      - **IV Iron Mandatory**: Oral iron insufficient for this deficit
      - **High-dose Protocols**: Ferric carboxymaltose 1000 mg followed by 500-1000 mg
      - **Alternative**: Iron sucrose 200 mg weekly × 5-8 doses
    - **Safety Monitoring**: Weekly hemoglobin initially, watch for iron overload
    - **Duration**: 6-12 weeks for complete repletion
    
    **Very Severe Deficit (>2000 mg)**:
    - **Clinical Significance**: Very severe deficiency, investigate underlying cause
    - **Immediate Actions**:
      - **Specialist Referral**: Hematology consultation recommended
      - **Investigate Cause**: GI bleeding, menorrhagia, malabsorption
      - **High-dose IV Iron**: Multiple sessions over 8-12 weeks
    - **Treatment Protocols**:
      - **Ferric Carboxymaltose**: 1000 mg every 1-2 weeks × 2-3 doses
      - **Iron Sucrose**: 200 mg twice weekly × 6-10 doses
    - **Enhanced Monitoring**: Weekly hemoglobin, monthly ferritin and TSAT
    
    **TREATMENT SELECTION GUIDE**:
    
    **IV Iron Preparation Selection**:
    - **Iron Sucrose (Venofer®)**:
      - Dose: 200 mg per infusion
      - Advantages: Well-tolerated, extensive safety data
      - Disadvantages: Multiple visits required for large deficits
      - Infusion time: 15-30 minutes
    
    - **Ferric Carboxymaltose (Injectafer®)**:
      - Dose: Up to 1000 mg per infusion
      - Advantages: Fewer visits, rapid infusion
      - Disadvantages: Higher cost, hypophosphatemia risk
      - Infusion time: 15 minutes for 1000 mg
    
    - **Iron Dextran (Dexferrum®, INFeD®)**:
      - Dose: Up to 1000 mg per infusion
      - Advantages: High-dose capability
      - Disadvantages: Higher anaphylaxis risk, test dose required
      - Use: Reserved for special circumstances
    
    **MONITORING AND SAFETY PROTOCOLS**:
    
    **Hemoglobin Monitoring**:
    - **Week 0**: Baseline hemoglobin and iron studies
    - **Week 2-4**: Check hemoglobin response (expect 1-2 g/dL increase)
    - **Week 6-8**: Assess near-target hemoglobin achievement
    - **Month 3**: Final assessment of treatment adequacy
    
    **Iron Parameter Monitoring**:
    - **Ferritin Target**: 100-300 ng/mL indicates adequate iron stores
    - **Transferrin Saturation**: Target >20% for adequate iron availability
    - **Timing**: Check 4-8 weeks after completing iron therapy
    - **Overload Concern**: Ferritin >500 ng/mL with TSAT >50%
    
    **Safety Monitoring**:
    - **Hypersensitivity**: Monitor during and 30 minutes post-infusion
    - **Hypophosphatemia**: Check phosphate with ferric carboxymaltose
    - **Iron Overload**: Monitor ferritin and TSAT throughout treatment
    - **Cardiac Status**: ECG monitoring if history of cardiac disease
    
    **TREATMENT FAILURE CONSIDERATIONS**:
    
    **Poor Response Evaluation**:
    - **Inadequate Dosing**: Recalculate using Ganzoni equation
    - **Ongoing Blood Loss**: Investigate and address source
    - **Malabsorption**: Consider celiac disease, IBD, H. pylori
    - **Chronic Inflammation**: May impair iron utilization
    - **Other Deficiencies**: B12, folate, or other nutritional deficits
    
    **Alternative Approaches**:
    - **Higher Iron Store Target**: Consider 800-1000 mg for iron stores
    - **Chronic Maintenance**: Ongoing IV iron every 3-6 months
    - **Combination Therapy**: IV iron plus EPO in appropriate patients
    - **Specialist Consultation**: Hematology input for complex cases
    
    **PATIENT EDUCATION POINTS**:
    - **Treatment Duration**: Iron therapy typically takes 2-3 months for full effect
    - **Side Effects**: Discuss potential IV iron reactions and monitoring
    - **Dietary Advice**: Iron-rich foods and absorption enhancers/inhibitors
    - **Follow-up Importance**: Emphasize need for monitoring labs
    - **Symptom Improvement**: Energy and fatigue improvement may take weeks
    
    Reference: Ganzoni AM. Schweiz Med Wochenschr. 1970;100(7):301-3.
    """
    
    result: float = Field(
        ...,
        description="Total iron deficit calculated using Ganzoni equation in milligrams. Represents amount of elemental iron needed for complete repletion",
        ge=0,
        example=1108.0
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for iron deficit",
        example="mg"
    )
    
    interpretation: str = Field(
        ...,
        description="Comprehensive clinical interpretation including deficit severity, treatment recommendations, monitoring plan, and safety considerations",
        example="Total iron deficit of 1108.0 mg indicates significant iron deficiency requiring IV iron replacement therapy in divided doses. Oral iron unlikely to be sufficient. Consider high-dose ferric carboxymaltose 1000 mg followed by 500-1000 mg in 1-2 weeks, or iron sucrose 200 mg weekly × 5-8 doses. Monitor for iron overload. Check hemoglobin weekly initially, iron studies monthly."
    )
    
    stage: str = Field(
        ...,
        description="Iron deficit severity category (Mild Deficit, Moderate Deficit, Severe Deficit, Very Severe Deficit)",
        example="Severe Deficit"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the deficit severity",
        example="Significant iron deficit"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 1108.0,
                "unit": "mg",
                "interpretation": "Total iron deficit of 1108.0 mg indicates significant iron deficiency requiring IV iron replacement therapy in divided doses. Oral iron unlikely to be sufficient. Consider high-dose ferric carboxymaltose 1000 mg followed by 500-1000 mg in 1-2 weeks, or iron sucrose 200 mg weekly × 5-8 doses. Monitor for iron overload. Check hemoglobin weekly initially, iron studies monthly.",
                "stage": "Severe Deficit",
                "stage_description": "Significant iron deficit"
            }
        }