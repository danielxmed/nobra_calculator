"""
Maternal-Fetal Hemorrhage Rh(D) Immune Globulin Dosage Models

Request and response models for RhIG dosage calculation in maternal-fetal hemorrhage.

References (Vancouver style):
1. AABB Technical Manual, 18th edition. American Association of Blood Banks; 2014.
2. American College of Obstetricians and Gynecologists. Prevention of Rh D alloimmunization. 
   ACOG Practice Bulletin No. 4. Washington, DC: American College of Obstetricians and 
   Gynecologists; 1999.
3. Bowman JM. The prevention of Rh immunization. Transfus Med Rev. 1988;2(3):129-50. 
   doi: 10.1016/s0887-7963(88)70067-9.
4. Queenan JT, Tomai TP, Ural SH, King JC. Deviation in amniotic fluid optical density 
   at a wavelength of 450 nm in Rh-immunized pregnancies from 14 to 40 weeks' gestation: 
   a proposal for clinical management. Am J Obstet Gynecol. 1993;168(5):1370-6. 
   doi: 10.1016/0002-9378(93)90384-k.

The Maternal-Fetal Hemorrhage Rh(D) Immune Globulin Dosage calculator determines the 
appropriate amount of RhIG (RhoGAM) to administer to Rh-negative mothers following 
maternal-fetal hemorrhage. This calculation is crucial for preventing hemolytic disease 
of the fetus and newborn (HDFN) by suppressing maternal anti-D antibody formation. 
The calculator uses the volume of fetal blood in maternal circulation to determine 
the number of 300 μg RhIG vials needed, with specific rounding rules and safety margins 
to ensure adequate protection.
"""

from pydantic import BaseModel, Field
from typing import Dict, Any


class MaternalFetalHemorrhageRhdImmuneGlobulinDosageRequest(BaseModel):
    """
    Request model for Maternal-Fetal Hemorrhage Rh(D) Immune Globulin Dosage
    
    This calculator determines the appropriate RhIG (RhoGAM) dosage for Rh-negative 
    mothers following maternal-fetal hemorrhage to prevent hemolytic disease of the 
    fetus and newborn (HDFN).
    
    **Clinical Background:**
    
    Maternal-fetal hemorrhage occurs when fetal blood enters the maternal circulation, 
    which can lead to Rh alloimmunization in Rh-negative mothers carrying Rh-positive 
    fetuses. Even small amounts of fetal blood (0.01-0.03 mL) can trigger maternal 
    antibody formation, leading to hemolytic disease in current or future pregnancies.
    
    **Key Parameters:**
    
    1. **Maternal Blood Volume (mL)**:
       - Typical range: 3,700-4,500 mL for average adult female
       - Can be estimated using Nadler's equation: 0.3561 × height³(m) + 0.03308 × weight(kg) + 0.1833 L
       - Used to calculate total volume of fetal blood in maternal circulation
       - Critical for accurate dosing calculations
    
    2. **Fetal Cell Percentage (%)**:
       - Determined by flow cytometry (preferred) or Kleihauer-Betke test
       - Normal baseline: <0.1% in maternal circulation
       - Clinical significance: typically >0.3%
       - Range: 0-10% (higher percentages indicate massive hemorrhage)
    
    **Calculation Method:**
    
    The calculator uses the formula:
    Number of RhIG vials = (fetal cell percentage / 100) × maternal blood volume / 30 mL
    
    **Rounding Rules:**
    - If decimal portion <0.5: round up to next whole number
    - If decimal portion ≥0.5: round up and add 1 additional vial
    - Always add 1 safety margin vial
    - Minimum dose: 1 vial
    
    **Standard Dosing:**
    - Each 300 μg vial protects against 30 mL of fetal whole blood (15 mL fetal RBCs)
    - Before 12 weeks: 150 μg mini-dose may be used
    - After 12 weeks: full 300 μg dose recommended
    - Optimal timing: within 72 hours of exposure
    
    **Clinical Applications:**
    - Routine postpartum prophylaxis
    - Following obstetric procedures (amniocentesis, chorionic villus sampling)
    - Antepartum bleeding episodes
    - Abdominal trauma during pregnancy
    - Therapeutic abortion or miscarriage
    - External cephalic version
    
    **Monitoring and Follow-up:**
    - Follow-up Kleihauer-Betke testing for large hemorrhages
    - Monitor for signs of maternal alloimmunization
    - Consider hematology consultation for massive hemorrhages
    - Assess adequacy of anti-D suppression
    
    References (Vancouver style):
    1. AABB Technical Manual, 18th edition. American Association of Blood Banks; 2014.
    2. American College of Obstetricians and Gynecologists. Prevention of Rh D alloimmunization. 
       ACOG Practice Bulletin No. 4. Washington, DC: American College of Obstetricians and 
       Gynecologists; 1999.
    3. Bowman JM. The prevention of Rh immunization. Transfus Med Rev. 1988;2(3):129-50. 
       doi: 10.1016/s0887-7963(88)70067-9.
    """
    
    maternal_blood_volume: float = Field(
        ...,
        ge=2000,
        le=6000,
        description="Total maternal blood volume in mL. Typical range is 3,700-4,500 mL for average adult female. Can be estimated using Nadler's equation based on height and weight, or clinical estimation based on patient size",
        example=4000
    )
    
    fetal_cell_percentage: float = Field(
        ...,
        ge=0,
        le=10,
        description="Percentage of fetal cells in maternal bloodstream determined by flow cytometry (preferred) or Kleihauer-Betke test. Normal baseline <0.1%, clinical significance typically >0.3%. Values >2% indicate significant hemorrhage",
        example=1.5
    )
    
    class Config:
        schema_extra = {
            "example": {
                "maternal_blood_volume": 4000,
                "fetal_cell_percentage": 1.5
            }
        }


class MaternalFetalHemorrhageRhdImmuneGlobulinDosageResponse(BaseModel):
    """
    Response model for Maternal-Fetal Hemorrhage Rh(D) Immune Globulin Dosage
    
    Provides comprehensive RhIG dosing recommendations with clinical assessment 
    and management guidance for preventing maternal Rh alloimmunization.
    
    **Dosing Categories:**
    
    **Standard Dose (1 vial):**
    - Minimal maternal-fetal hemorrhage
    - Covers up to 30 mL fetal blood exposure
    - Standard prophylactic dose for routine deliveries
    - Administer within 72 hours for optimal efficacy
    
    **Moderate Hemorrhage (2-3 vials):**
    - Moderate hemorrhage requiring increased protection
    - Each vial provides additional 30 mL coverage
    - Consider follow-up testing to confirm adequate coverage
    - Monitor for maternal alloimmunization
    
    **Large Hemorrhage (4-10 vials):**
    - Significant hemorrhage requiring aggressive prophylaxis
    - Recommend obstetric consultation
    - Follow-up Kleihauer-Betke testing essential
    - Intensive monitoring for alloimmunization
    
    **Massive Hemorrhage (>10 vials):**
    - Rare but serious event requiring immediate consultation
    - Consider intravenous RhIG if available
    - Hematology and maternal-fetal medicine involvement
    - Potential need for exchange transfusion protocols
    
    **Clinical Management Considerations:**
    
    **Timing:**
    - Optimal: within 72 hours of exposure
    - May be effective up to 28 days but efficacy decreases
    - Earlier administration provides better protection
    
    **Administration:**
    - Intramuscular injection (standard)
    - Intravenous option for massive doses
    - Multiple injection sites may be needed for large doses
    
    **Monitoring:**
    - Follow-up testing for hemorrhages requiring >3 vials
    - Monitor for maternal alloimmunization in subsequent pregnancies
    - Assess adequacy of anti-D suppression
    
    **Quality Assurance:**
    - Verify Rh status of mother and baby
    - Confirm absence of existing anti-D antibodies
    - Document indication and dosing rationale
    - Ensure proper storage and administration
    
    Reference: AABB Technical Manual, 18th edition. American Association of Blood Banks; 2014.
    """
    
    result: Dict[str, Any] = Field(
        ...,
        description="Comprehensive RhIG dosing assessment including vial count, dosing calculations, clinical assessment, and management recommendations",
        example={
            "total_vials": 3,
            "fetal_blood_volume_ml": 60.0,
            "calculated_vials_raw": 2.0,
            "safety_margin_applied": 1,
            "vial_strength_mcg": 300,
            "total_dose_mcg": 900,
            "protection_per_vial_ml": 30,
            "clinical_assessment": {
                "fetal_cell_significance": "Clinically significant",
                "alloimmunization_risk": "Significant",
                "hemorrhage_severity": "Moderate hemorrhage",
                "total_protection_ml": 90,
                "coverage_ratio": 1.5,
                "baseline_comparison": "15.0x normal baseline",
                "time_sensitivity": "Administer within 72 hours for optimal efficacy",
                "follow_up_needed": False
            }
        }
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the dosage",
        example="vials"
    )
    
    interpretation: str = Field(
        ...,
        description="Comprehensive clinical interpretation with dosing rationale, management recommendations, timing requirements, and monitoring guidance",
        example="Moderate hemorrhage requiring 3 vials of 300 μg RhIG (total dose: 900 μg). Each vial provides protection against 30 mL of fetal blood. Total protection coverage: 90 mL. Administer within 72 hours for optimal efficacy. Consider follow-up Kleihauer-Betke testing to confirm adequate coverage and monitor for maternal alloimmunization."
    )
    
    stage: str = Field(
        ...,
        description="Hemorrhage severity category (Standard Dose, Moderate Hemorrhage, Large Hemorrhage, Massive Hemorrhage)",
        example="Moderate Hemorrhage"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the hemorrhage severity category",
        example="Moderate maternal-fetal hemorrhage"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": {
                    "total_vials": 3,
                    "fetal_blood_volume_ml": 60.0,
                    "calculated_vials_raw": 2.0,
                    "safety_margin_applied": 1,
                    "vial_strength_mcg": 300,
                    "total_dose_mcg": 900,
                    "protection_per_vial_ml": 30,
                    "clinical_assessment": {
                        "fetal_cell_significance": "Clinically significant",
                        "alloimmunization_risk": "Significant",
                        "hemorrhage_severity": "Moderate hemorrhage",
                        "total_protection_ml": 90,
                        "coverage_ratio": 1.5,
                        "baseline_comparison": "15.0x normal baseline",
                        "time_sensitivity": "Administer within 72 hours for optimal efficacy",
                        "follow_up_needed": False
                    }
                },
                "unit": "vials",
                "interpretation": "Moderate hemorrhage requiring 3 vials of 300 μg RhIG (total dose: 900 μg). Each vial provides protection against 30 mL of fetal blood. Total protection coverage: 90 mL. Administer within 72 hours for optimal efficacy. Consider follow-up Kleihauer-Betke testing to confirm adequate coverage and monitor for maternal alloimmunization.",
                "stage": "Moderate Hemorrhage",
                "stage_description": "Moderate maternal-fetal hemorrhage"
            }
        }