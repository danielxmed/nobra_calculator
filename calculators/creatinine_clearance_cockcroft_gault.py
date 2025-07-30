"""
Creatinine Clearance (Cockcroft-Gault Equation) Calculator

Estimates creatinine clearance for kidney function assessment and medication 
dosing using patient demographics and serum creatinine.

References:
1. Cockcroft DW, Gault MH. Prediction of creatinine clearance from serum creatinine. 
   Nephron. 1976;16(1):31-41. doi:10.1159/000180580
2. Stevens LA, Coresh J, Greene T, Levey AS. Assessing kidney function--measured 
   and estimated glomerular filtration rate. N Engl J Med. 2006;354(23):2473-2483.
3. Levey AS, Inker LA, Coresh J. GFR estimation: from physiology to public health. 
   Am J Kidney Dis. 2014;63(5):820-834.
"""

import math
from typing import Dict, Any, Optional


class CreatinineClearanceCockcroftGaultCalculator:
    """Calculator for Creatinine Clearance using Cockcroft-Gault Equation"""
    
    def __init__(self):
        # Constants for the equation
        self.MALE_FACTOR = 1.0
        self.FEMALE_FACTOR = 0.85
        self.CREATININE_FACTOR = 72.0
        
        # BMI thresholds for weight interpretation
        self.BMI_UNDERWEIGHT = 18.5
        self.BMI_NORMAL_MAX = 24.9
        self.BMI_OVERWEIGHT = 25.0
    
    def calculate(
        self,
        age: int,
        weight: float,
        sex: str,
        serum_creatinine: float,
        height: Optional[float] = None
    ) -> Dict[str, Any]:
        """
        Calculates creatinine clearance using the Cockcroft-Gault equation
        
        Args:
            age: Patient age in years
            weight: Patient weight in kg
            sex: Patient sex (male/female)
            serum_creatinine: Serum creatinine in mg/dL
            height: Patient height in cm (optional, for BMI calculation)
            
        Returns:
            Dict with creatinine clearance and clinical interpretation
        """
        
        # Validate inputs
        self._validate_inputs(age, weight, sex, serum_creatinine, height)
        
        # Calculate BMI if height provided
        bmi = None
        if height is not None:
            height_m = height / 100.0  # Convert cm to meters
            bmi = weight / (height_m ** 2)
        
        # Apply Cockcroft-Gault equation
        creatinine_clearance = self._calculate_cockcroft_gault(
            age, weight, sex, serum_creatinine
        )
        
        # Get clinical interpretation
        interpretation = self._get_interpretation(creatinine_clearance)
        
        # Get weight recommendations if BMI available
        weight_recommendations = self._get_weight_recommendations(bmi, weight) if bmi else None
        
        return {
            "result": round(creatinine_clearance, 1),
            "unit": "mL/min",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"],
            "calculation_details": {
                "input_parameters": {
                    "age": age,
                    "weight": weight,
                    "sex": sex,
                    "serum_creatinine": serum_creatinine,
                    "height": height,
                    "bmi": round(bmi, 1) if bmi else None
                },
                "clinical_assessment": interpretation["clinical_assessment"],
                "medication_guidance": interpretation["medication_guidance"],
                "monitoring_recommendations": interpretation["monitoring"],
                "weight_recommendations": weight_recommendations,
                "formula_notes": [
                    "CrCl = [(140 - age) × weight × (0.85 if female)] / (72 × serum creatinine)",
                    "Historical equation, may overestimate GFR by 10-20%",
                    "Still used for specific medication dosing decisions"
                ]
            }
        }
    
    def _validate_inputs(
        self, age: int, weight: float, sex: str, 
        serum_creatinine: float, height: Optional[float]
    ):
        """Validates input parameters"""
        
        # Validate age
        if not isinstance(age, int) or age < 18 or age > 120:
            raise ValueError("Age must be between 18 and 120 years")
        
        # Validate weight
        if not isinstance(weight, (int, float)) or weight < 30.0 or weight > 300.0:
            raise ValueError("Weight must be between 30.0 and 300.0 kg")
        
        # Validate sex
        if sex not in ["male", "female"]:
            raise ValueError("Sex must be 'male' or 'female'")
        
        # Validate serum creatinine
        if not isinstance(serum_creatinine, (int, float)) or serum_creatinine < 0.3 or serum_creatinine > 15.0:
            raise ValueError("Serum creatinine must be between 0.3 and 15.0 mg/dL")
        
        # Validate height if provided
        if height is not None:
            if not isinstance(height, (int, float)) or height < 100.0 or height > 250.0:
                raise ValueError("Height must be between 100.0 and 250.0 cm")
    
    def _calculate_cockcroft_gault(
        self, age: int, weight: float, sex: str, serum_creatinine: float
    ) -> float:
        """Implements the Cockcroft-Gault equation"""
        
        # Determine sex factor
        sex_factor = self.FEMALE_FACTOR if sex == "female" else self.MALE_FACTOR
        
        # Apply the formula: [(140 - age) × weight × sex_factor] / (72 × serum_creatinine)
        numerator = (140 - age) * weight * sex_factor
        denominator = self.CREATININE_FACTOR * serum_creatinine
        
        creatinine_clearance = numerator / denominator
        
        return creatinine_clearance
    
    def _get_interpretation(self, creatinine_clearance: float) -> Dict[str, str]:
        """
        Determines clinical interpretation based on creatinine clearance
        
        Args:
            creatinine_clearance: Calculated creatinine clearance in mL/min
            
        Returns:
            Dict with interpretation details
        """
        
        if creatinine_clearance >= 90:
            stage = "Normal"
            description = "Normal kidney function"
            clinical_assessment = "Normal creatinine clearance"
            medication_guidance = "Standard dosing for most medications"
            monitoring = "Routine monitoring as clinically indicated"
            
            interpretation = (
                f"Creatinine clearance of {creatinine_clearance:.1f} mL/min indicates "
                f"normal kidney function. Standard medication dosing is appropriate "
                f"for most drugs. Continue routine monitoring as clinically indicated."
            )
            
        elif creatinine_clearance >= 60:
            stage = "Mildly Decreased"
            description = "Mildly decreased kidney function"
            clinical_assessment = "Mild kidney function impairment"
            medication_guidance = "Monitor closely, consider dose adjustments for renally eliminated drugs"
            monitoring = "Regular monitoring of kidney function recommended"
            
            interpretation = (
                f"Creatinine clearance of {creatinine_clearance:.1f} mL/min indicates "
                f"mildly decreased kidney function. Monitor closely and consider dose "
                f"adjustments for medications eliminated by the kidneys."
            )
            
        elif creatinine_clearance >= 30:
            stage = "Moderately Decreased"
            description = "Moderately decreased kidney function"
            clinical_assessment = "Moderate kidney function impairment"
            medication_guidance = "Dose adjustments required for many medications"
            monitoring = "Close monitoring and nephrology consultation recommended"
            
            interpretation = (
                f"Creatinine clearance of {creatinine_clearance:.1f} mL/min indicates "
                f"moderately decreased kidney function. Dose adjustments are required "
                f"for many medications. Consider nephrology consultation."
            )
            
        elif creatinine_clearance >= 15:
            stage = "Severely Decreased"
            description = "Severely decreased kidney function"
            clinical_assessment = "Severe kidney function impairment"
            medication_guidance = "Significant dose reductions or alternative medications required"
            monitoring = "Intensive monitoring and nephrology management required"
            
            interpretation = (
                f"Creatinine clearance of {creatinine_clearance:.1f} mL/min indicates "
                f"severely decreased kidney function. Significant medication dose "
                f"reductions or alternatives are required. Nephrology management is essential."
            )
            
        else:  # < 15
            stage = "Kidney Failure"
            description = "Kidney failure"
            clinical_assessment = "End-stage kidney disease"
            medication_guidance = "Avoid nephrotoxic medications, consider dialysis dosing"
            monitoring = "Continuous monitoring, dialysis planning, and nephrology management"
            
            interpretation = (
                f"Creatinine clearance of {creatinine_clearance:.1f} mL/min indicates "
                f"kidney failure. Avoid nephrotoxic medications, consider dialysis "
                f"dosing adjustments, and ensure appropriate nephrology management."
            )
        
        return {
            "stage": stage,
            "description": description,
            "interpretation": interpretation,
            "clinical_assessment": clinical_assessment,
            "medication_guidance": medication_guidance,
            "monitoring": monitoring
        }
    
    def _get_weight_recommendations(self, bmi: float, actual_weight: float) -> Dict[str, Any]:
        """Provides weight-based recommendations for equation accuracy"""
        
        if bmi < self.BMI_UNDERWEIGHT:
            category = "Underweight"
            recommendation = "Use actual body weight"
            accuracy_note = "Equation may underestimate clearance in underweight patients"
        elif bmi <= self.BMI_NORMAL_MAX:
            category = "Normal weight"
            recommendation = "Use actual body weight or ideal body weight"
            accuracy_note = "Equation is most accurate in normal weight range"
        else:  # BMI >= 25
            category = "Overweight/Obese"
            recommendation = "Consider using adjusted body weight or ideal body weight"
            accuracy_note = "Equation may overestimate clearance in obese patients"
        
        return {
            "bmi_category": category,
            "weight_recommendation": recommendation,
            "accuracy_note": accuracy_note,
            "clinical_note": "Consider clinical context when interpreting results at weight extremes"
        }


def calculate_creatinine_clearance_cockcroft_gault(
    age: int,
    weight: float,
    sex: str,
    serum_creatinine: float,
    height: Optional[float] = None
) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = CreatinineClearanceCockcroftGaultCalculator()
    return calculator.calculate(
        age=age,
        weight=weight,
        sex=sex,
        serum_creatinine=serum_creatinine,
        height=height
    )