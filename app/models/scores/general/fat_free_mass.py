"""
Fat Free Mass (FFM) Models

Request and response models for Fat Free Mass calculation using body weight and BMI.

References (Vancouver style):
1. Janmahasatian S, Duffull SB, Ash S, Ward LC, Byrnes NM, Green B. Quantification of lean 
   bodyweight. Clin Pharmacokinet. 2005;44(10):1051-65. doi: 10.2165/00003088-200544100-00004.
2. La Colla L, Albertin A, La Colla G, Mangano A. Predictive value of the Janmahasatian 
   formula for lean body weight in the dosing of sugammadex in morbidly obese patients. 
   Anaesthesia. 2010 Apr;65(4):445-6. doi: 10.1111/j.1365-2044.2010.06284.x.
3. Green B, Duffull SB. What is the best size descriptor to use for pharmacokinetic studies 
   in the obese? Br J Clin Pharmacol. 2004 Aug;58(2):119-33. doi: 10.1111/j.1365-2125.2004.02157.x.

Fat Free Mass (FFM) represents the component of body weight that excludes adipose tissue, 
including muscle, bone, organs, and body water. This calculation is particularly valuable 
for medication dosing in clinical practice.
"""

from pydantic import BaseModel, Field
from typing import Literal


class FatFreeMassRequest(BaseModel):
    """
    Request model for Fat Free Mass (FFM) calculation
    
    The Fat Free Mass calculation uses the Janmahasatian formula to estimate lean body weight 
    based on total body weight and body mass index (BMI). This method provides sex-specific 
    calculations that are particularly useful in clinical pharmacology and anesthesia.
    
    Formula Background:
    The Janmahasatian formula was developed to overcome limitations of other lean body weight 
    equations, particularly in patients with obesity. It uses a rational approach based on 
    the relationship between BMI and body composition.
    
    Sex-Specific Formulas:
    - Male: FFM = (9.27 × 10³ × Body Weight) / (6.68 × 10³ + 216 × BMI)
    - Female: FFM = (9.27 × 10³ × Body Weight) / (8.78 × 10³ + 244 × BMI)
    
    Clinical Parameters:
    
    1. Sex:
       - Biological sex affects body composition
       - Men typically have higher muscle mass and lower body fat percentage
       - Women typically have higher essential fat requirements
       - Formula coefficients are optimized for each sex
    
    2. Body Weight:
       - Total body weight in kilograms
       - Should be current, accurate weight
       - Range: 10-300 kg covers pediatric to morbidly obese patients
       - Used as primary input for lean mass estimation
    
    3. Body Mass Index (BMI):
       - Weight (kg) divided by height squared (m²)
       - Normal range: 18.5-24.9 kg/m²
       - Calculator valid for BMI range 10-80 kg/m²
       - Critical for determining fat vs. lean mass distribution
    
    Clinical Applications:
    
    Medication Dosing:
    - Anesthetic drug dosing (propofol, rocuronium, sugammadex)
    - Chemotherapy dosing for certain agents
    - Avoid overdosing in obese patients
    - Improve dosing accuracy for hydrophilic drugs
    
    Body Composition Assessment:
    - Nutritional assessment and planning
    - Metabolic rate calculations
    - Fitness and athletic performance evaluation
    - Clinical research applications
    
    Advantages over Other Methods:
    - Does not require direct body fat measurement
    - More accurate than ideal body weight in obesity
    - Validated in clinical pharmacology studies
    - Simple calculation requiring only basic measurements
    - Sex-specific formulas improve accuracy
    
    Clinical Validation:
    - Originally validated against dual-energy X-ray absorptiometry (DEXA)
    - Demonstrated superior performance in obese patients
    - Validated for anesthetic drug dosing accuracy
    - Used in multiple pharmacokinetic studies
    
    Typical Fat-Free Mass Percentages:
    - Men: 75-85% of body weight (athletes may be higher)
    - Women: 65-75% of body weight (athletes may be higher)
    - Lower percentages may indicate sarcopenia or high adiposity
    - Higher percentages suggest athletic build or low body fat
    
    Important Limitations:
    - Predictive equation, not direct measurement
    - May not account for extreme body compositions
    - Should be used alongside clinical judgment
    - Not validated in all patient populations
    - May be less accurate in very elderly patients
    
    Comparison with Other Methods:
    - More accurate than ideal body weight formulas
    - Simpler than bioelectrical impedance analysis
    - Less expensive than DEXA scanning
    - More clinically relevant than BMI alone
    
    References (Vancouver style):
    1. Janmahasatian S, et al. Quantification of lean bodyweight. Clin Pharmacokinet. 2005;44(10):1051-65.
    2. La Colla L, et al. Predictive value of the Janmahasatian formula for lean body weight 
       in the dosing of sugammadex in morbidly obese patients. Anaesthesia. 2010;65(4):445-6.
    """
    
    sex: Literal["male", "female"] = Field(
        ...,
        description="Patient biological sex. Affects body composition and formula coefficients used for FFM calculation.",
        example="male"
    )
    
    body_weight_kg: float = Field(
        ...,
        description="Current body weight in kilograms. Should be accurate and recent measurement. Used as primary input for lean mass estimation.",
        ge=10.0,
        le=300.0,
        example=80.5
    )
    
    bmi: float = Field(
        ...,
        description="Body Mass Index in kg/m² (weight divided by height squared). Critical for determining fat vs. lean mass distribution. Normal range: 18.5-24.9 kg/m².",
        ge=10.0,
        le=80.0,
        example=26.5
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "sex": "male",
                "body_weight_kg": 80.5,
                "bmi": 26.5
            }
        }


class FatFreeMassResponse(BaseModel):
    """
    Response model for Fat Free Mass (FFM) calculation
    
    Provides calculated fat-free mass with clinical interpretation and body composition analysis.
    
    Clinical Interpretation and Applications:
    
    Fat-Free Mass represents the metabolically active component of body weight, including:
    - Skeletal muscle mass
    - Organ mass (heart, liver, kidneys, brain)
    - Bone mass
    - Body water (intracellular and extracellular)
    - Connective tissue
    
    Body Composition Insights:
    
    Normal Fat-Free Mass Percentages:
    - Men: 75-85% of total body weight
      - Athletes/muscular: 80-90%
      - Average fitness: 75-85%
      - Low muscle mass: 65-75%
    
    - Women: 65-75% of total body weight
      - Athletes/muscular: 70-80%
      - Average fitness: 65-75%
      - Low muscle mass: 55-65%
    
    Clinical Applications:
    
    Medication Dosing:
    - Anesthetic Agents: Propofol, etomidate, thiopental dosing
    - Neuromuscular Blockers: Rocuronium, vecuronium, atracurium
    - Reversal Agents: Sugammadex dosing in obesity
    - Chemotherapy: Certain cytotoxic agents
    - Antibiotics: Aminoglycosides, vancomycin
    - Critical Care: Vasopressor and sedative dosing
    
    Nutritional Assessment:
    - Protein requirements calculation
    - Metabolic rate estimation
    - Nutritional intervention planning
    - Sarcopenia screening and monitoring
    - Weight management program design
    
    Fitness and Performance:
    - Athletic performance assessment
    - Body composition monitoring
    - Training program optimization
    - Competitive sport categorization
    - Fitness goal setting and tracking
    
    Clinical Research:
    - Pharmacokinetic studies
    - Metabolic research
    - Nutrition intervention trials
    - Body composition studies
    - Drug development and dosing studies
    
    Advantages of FFM-Based Dosing:
    - Reduces overdosing in obese patients
    - Improves drug efficacy and safety
    - Accounts for altered drug distribution
    - More physiologically relevant than total body weight
    - Reduces adverse effects from inappropriate dosing
    
    Clinical Decision Support:
    
    High Fat-Free Mass (>85% men, >80% women):
    - Indicates high muscle mass or athletic build
    - May require adjusted medication dosing
    - Suggests good metabolic health
    - Consider nutritional needs for muscle maintenance
    
    Normal Fat-Free Mass (75-85% men, 65-75% women):
    - Typical body composition for healthy individuals
    - Standard medication dosing protocols apply
    - Balanced approach to nutrition and exercise
    - Regular monitoring for age-related changes
    
    Low Fat-Free Mass (<75% men, <65% women):
    - May indicate sarcopenia or high adiposity
    - Consider body composition improvement strategies
    - May require adjusted medication dosing
    - Evaluate for underlying medical conditions
    
    Quality Improvement Applications:
    - Standardized medication dosing protocols
    - Improved patient safety in anesthesia
    - Reduced medication errors in obesity
    - Enhanced clinical research accuracy
    - Better patient outcomes through precision dosing
    
    Important Clinical Considerations:
    - FFM equation is predictive, not directly measured
    - Should complement, not replace, clinical assessment
    - May be less accurate in extreme body compositions
    - Consider age-related muscle mass changes
    - Validate with other assessment methods when possible
    
    Future Applications:
    - Personalized medicine approaches
    - Precision dosing algorithms
    - Integrated electronic health record systems
    - Point-of-care body composition assessment
    - Population health management tools
    
    Reference: Janmahasatian S, et al. Clin Pharmacokinet. 2005;44(10):1051-65.
    """
    
    result: float = Field(
        ...,
        description="Calculated fat-free mass in kilograms using the Janmahasatian formula",
        example=58.2
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for fat-free mass",
        example="kg"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation including body composition analysis and clinical applications",
        example="Calculated fat-free mass: 58.2 kg (72.3% of body weight). Fat mass: 22.3 kg (27.7% of body weight). This represents normal lean mass for a male patient. FFM includes muscle, bone, organs, and water content, excluding adipose tissue. This value is useful for medication dosing calculations, particularly in anesthesia and for drugs with specific distribution properties in lean versus adipose tissue."
    )
    
    stage: str = Field(
        ...,
        description="Calculation status",
        example="Calculated"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the calculation result",
        example="Fat-free mass estimation"
    )
    
    percentage_of_body_weight: float = Field(
        ...,
        description="Fat-free mass as percentage of total body weight",
        example=72.3
    )
    
    fat_mass: float = Field(
        ...,
        description="Calculated fat mass (total weight minus fat-free mass) in kilograms",
        example=22.3
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "result": 58.2,
                "unit": "kg",
                "interpretation": "Calculated fat-free mass: 58.2 kg (72.3% of body weight). Fat mass: 22.3 kg (27.7% of body weight). This represents normal lean mass for a male patient. FFM includes muscle, bone, organs, and water content, excluding adipose tissue. This value is useful for medication dosing calculations, particularly in anesthesia and for drugs with specific distribution properties in lean versus adipose tissue.",
                "stage": "Calculated",
                "stage_description": "Fat-free mass estimation",
                "percentage_of_body_weight": 72.3,
                "fat_mass": 22.3
            }
        }