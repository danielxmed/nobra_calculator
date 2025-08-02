"""
Hydroxychloroquine (Plaquenil) Dosing Calculator

Calculates maximum daily hydroxychloroquine dose to reduce retinopathy risk 
based on 2016 American Academy of Ophthalmology guidelines.

References:
- Marmor MF, Kellner U, Lai TY, et al. Recommendations on Screening for Chloroquine 
  and Hydroxychloroquine Retinopathy (2016 Revision). Ophthalmology. 2016;123(6):1386-94.
- Melles RB, Marmor MF. The risk of toxic retinopathy in patients on long-term 
  hydroxychloroquine therapy. JAMA Ophthalmol. 2014;132(12):1453-60.
"""

from typing import Dict, Any


class HydroxychloroquineDosingCalculator:
    """Calculator for Hydroxychloroquine (Plaquenil) Dosing"""
    
    def __init__(self):
        # Maximum recommended dose per 2016 AAO guidelines
        self.max_dose_per_kg = 5.0  # mg/kg/day
        
        # Standard tablet strengths (mg)
        self.tablet_strengths = [200, 300, 400]
        
        # Risk adjustment factors
        self.risk_adjustments = {
            "none": 1.0,
            "one_or_more": 0.85  # 15% reduction for patients with risk factors
        }
        
        # Indication-specific considerations
        self.indication_notes = {
            "rheumatoid_arthritis": "Standard dose 200-400 mg daily. Consider lower dose for long-term use.",
            "systemic_lupus_erythematosus": "Standard dose 200-400 mg daily. Monitor for flares with dose reduction.",
            "malaria_prophylaxis": "Higher doses may be used short-term. Retinopathy risk minimal with short-term use.",
            "malaria_treatment": "Short-term high-dose treatment. Retinopathy risk minimal with short-term use.",
            "other_autoimmune": "Follow rheumatologic dosing guidelines. Consider specialist consultation."
        }
    
    def calculate(self, weight_kg: float, indication: str, risk_factors: str) -> Dict[str, Any]:
        """
        Calculates maximum hydroxychloroquine dose for retinopathy prevention
        
        Args:
            weight_kg (float): Patient's actual body weight in kg
            indication (str): Clinical indication for hydroxychloroquine
            risk_factors (str): Presence of risk factors ("none" or "one_or_more")
            
        Returns:
            Dict with maximum dose recommendations and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(weight_kg, indication, risk_factors)
        
        # Calculate base maximum dose (5 mg/kg actual weight)
        base_max_dose = weight_kg * self.max_dose_per_kg
        
        # Adjust for risk factors
        risk_adjustment = self.risk_adjustments[risk_factors]
        adjusted_max_dose = base_max_dose * risk_adjustment
        
        # Round to nearest practical dose
        practical_dose = self._round_to_practical_dose(adjusted_max_dose)
        
        # Calculate dose per kg for verification
        dose_per_kg = practical_dose / weight_kg
        
        # Get interpretation
        interpretation = self._get_interpretation(practical_dose, dose_per_kg, indication, risk_factors)
        
        # Calculate retinopathy risk estimates
        retinopathy_risk = self._calculate_retinopathy_risk(dose_per_kg)
        
        # Get dosing recommendations
        dosing_schedule = self._get_dosing_schedule(practical_dose)
        
        return {
            "result": practical_dose,
            "unit": "mg",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"],
            "dose_per_kg": round(dose_per_kg, 2),
            "retinopathy_risk_10_year": retinopathy_risk["ten_year"],
            "retinopathy_risk_20_year": retinopathy_risk["twenty_year"],
            "dosing_schedule": dosing_schedule,
            "indication_notes": self.indication_notes[indication],
            "requires_eye_exam": True,
            "risk_adjusted": risk_factors == "one_or_more"
        }
    
    def _validate_inputs(self, weight_kg: float, indication: str, risk_factors: str):
        """Validates input parameters"""
        
        if not isinstance(weight_kg, (int, float)):
            raise ValueError("Weight must be a numeric value")
        
        if weight_kg < 20 or weight_kg > 300:
            raise ValueError("Weight must be between 20 and 300 kg")
        
        valid_indications = list(self.indication_notes.keys())
        if indication not in valid_indications:
            raise ValueError(f"Indication must be one of: {valid_indications}")
        
        valid_risk_factors = ["none", "one_or_more"]
        if risk_factors not in valid_risk_factors:
            raise ValueError(f"Risk factors must be one of: {valid_risk_factors}")
    
    def _round_to_practical_dose(self, dose: float) -> float:
        """
        Rounds dose to practical tablet combinations
        
        Args:
            dose (float): Calculated dose in mg
            
        Returns:
            float: Practical dose achievable with standard tablets
        """
        
        # Round to nearest 50mg for practical dosing
        return round(dose / 50) * 50
    
    def _calculate_retinopathy_risk(self, dose_per_kg: float) -> Dict[str, int]:
        """
        Calculates retinopathy risk based on dose per kg
        
        Args:
            dose_per_kg (float): Dose in mg/kg/day
            
        Returns:
            Dict with 10-year and 20-year risk percentages
        """
        
        if dose_per_kg <= 5.0:
            return {"ten_year": 2, "twenty_year": 20}
        else:
            return {"ten_year": 10, "twenty_year": 40}
    
    def _get_dosing_schedule(self, daily_dose: float) -> str:
        """
        Provides practical dosing schedule recommendations
        
        Args:
            daily_dose (float): Daily dose in mg
            
        Returns:
            str: Dosing schedule recommendation
        """
        
        if daily_dose <= 200:
            return "200 mg once daily, or 100 mg twice daily if 200 mg tablets unavailable"
        elif daily_dose <= 300:
            return "200 mg once daily + 100 mg once daily, or divide as 150 mg twice daily"
        elif daily_dose <= 400:
            return "200 mg twice daily, or 400 mg once daily (single dose preferred)"
        else:
            return "200 mg twice daily + additional 100-200 mg daily as needed (maximum practical dosing)"
    
    def _get_interpretation(self, dose: float, dose_per_kg: float, indication: str, risk_factors: str) -> Dict[str, str]:
        """
        Determines the interpretation based on calculated dose
        
        Args:
            dose (float): Daily dose in mg
            dose_per_kg (float): Dose per kg
            indication (str): Clinical indication
            risk_factors (str): Risk factor status
            
        Returns:
            Dict with interpretation details
        """
        
        if dose <= 200:
            stage = "Low Dose"
            description = "≤200 mg daily"
            
            if risk_factors == "one_or_more":
                interp = f"Conservative dosing due to risk factors. Low retinopathy risk with careful monitoring. Dose: {dose_per_kg:.1f} mg/kg/day. Annual eye exams recommended."
            else:
                interp = f"Low-dose therapy with minimal retinopathy risk. Dose: {dose_per_kg:.1f} mg/kg/day. Standard ophthalmologic monitoring recommended."
        
        elif dose <= 400:
            stage = "Standard Dose" 
            description = "201-400 mg daily"
            
            if dose_per_kg > 5.0:
                interp = f"Dose exceeds 5 mg/kg guideline ({dose_per_kg:.1f} mg/kg). Consider dose reduction or more frequent eye monitoring to minimize retinopathy risk."
            else:
                interp = f"Standard therapeutic dose within safety guidelines. Dose: {dose_per_kg:.1f} mg/kg/day. Annual eye exams after 5 years of use."
        
        else:
            stage = "High Dose"
            description = ">400 mg daily"
            
            if dose_per_kg > 5.0:
                interp = f"High dose exceeding safety guidelines ({dose_per_kg:.1f} mg/kg). Strong recommendation for dose reduction. Consider more frequent ophthalmologic monitoring."
            else:
                interp = f"Higher dose but within weight-based limits. Dose: {dose_per_kg:.1f} mg/kg/day. Consider dose reduction if therapeutic goals allow."
        
        return {
            "stage": stage,
            "description": description,
            "interpretation": interp
        }


def calculate_hydroxychloroquine_dosing(weight_kg: float, indication: str, 
                                       risk_factors: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = HydroxychloroquineDosingCalculator()
    return calculator.calculate(weight_kg, indication, risk_factors)