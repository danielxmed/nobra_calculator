"""
COVID Home Safely Now (CHOSEN) Risk Score Calculator

Predicts suitability for discharge in COVID-19 patients by assessing risk of 
needing supplemental oxygen, ICU-level care, or death within 14 days.

References:
1. Levine DM, Ouchi K, Blanchfield B, Diamond A, Licurse A, Pu CT, et al. 
   Hospital-level care at home for acutely ill adults: a pilot randomized 
   controlled trial. J Gen Intern Med. 2018;33(5):729-736.
2. Levine DM, Ouchi K, Blanchfield B, Saenz A, Burke K, Paz M, et al. 
   Hospital-Level Care at Home for Acutely Ill Adults: A Randomized Controlled Trial. 
   Ann Intern Med. 2020;172(2):77-85.
"""

from typing import Dict, Any, Optional


class ChosenCovidDischargeCalculator:
    """Calculator for COVID Home Safely Now (CHOSEN) Risk Score"""
    
    def __init__(self):
        # Age scoring system
        self.AGE_SCORES = [
            {"min": 74, "max": 999, "points": 0},   # >73 years
            {"min": 60, "max": 73, "points": 1},    # 60-73 years
            {"min": 46, "max": 59, "points": 2},    # 46-59 years
            {"min": 18, "max": 45, "points": 5}     # 18-45 years
        ]
        
        # Oxygen saturation scoring system
        self.SPO2_SCORES = [
            {"min": 0, "max": 93, "points": 0},     # <94%
            {"min": 94, "max": 96, "points": 9},    # 94-96%
            {"min": 97, "max": 98, "points": 14},   # 97-98%
            {"min": 99, "max": 100, "points": 21}   # >98%
        ]
        
        # Albumin scoring system (for full CHOSEN score)
        self.ALBUMIN_SCORES = [
            {"min": 0.0, "max": 2.7, "points": 0},    # <2.8 g/dL
            {"min": 2.8, "max": 3.3, "points": 5},    # 2.8-3.3 g/dL
            {"min": 3.4, "max": 3.7, "points": 15},   # 3.4-3.7 g/dL
            {"min": 3.8, "max": 10.0, "points": 29}   # >3.7 g/dL
        ]
        
        # Respiratory rate scoring system (for modified CHOSEN score)
        self.RESPIRATORY_RATE_SCORES = [
            {"min": 0, "max": 20, "points": 10},      # ≤20 breaths/min
            {"min": 21, "max": 24, "points": 5},      # 21-24 breaths/min
            {"min": 25, "max": 999, "points": 0}      # ≥25 breaths/min
        ]
        
        # Interpretation thresholds
        self.FULL_CHOSEN_THRESHOLD = 30
        self.MODIFIED_CHOSEN_THRESHOLD = 20
    
    def calculate(
        self,
        age: int,
        oxygen_saturation: int,
        albumin_level: Optional[float] = None,
        respiratory_rate: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Calculates the CHOSEN Risk Score for COVID-19 discharge suitability
        
        Args:
            age: Patient age in years (18-120)
            oxygen_saturation: SpO2 on room air (80-100%)
            albumin_level: Serum albumin level in g/dL (optional, for full CHOSEN)
            respiratory_rate: Respiratory rate in breaths/min (optional, for modified CHOSEN)
            
        Returns:
            Dict with CHOSEN score and clinical interpretation
        """
        
        # Validate inputs
        self._validate_inputs(age, oxygen_saturation, albumin_level, respiratory_rate)
        
        # Calculate age points
        age_points = self._calculate_age_points(age)
        
        # Calculate SpO2 points
        spo2_points = self._calculate_spo2_points(oxygen_saturation)
        
        # Determine which version to use and calculate third component
        if albumin_level is not None:
            # Use full CHOSEN score with albumin
            albumin_points = self._calculate_albumin_points(albumin_level)
            total_score = age_points + spo2_points + albumin_points
            score_type = "Full CHOSEN Score"
            threshold = self.FULL_CHOSEN_THRESHOLD
            third_component = f"Albumin: {albumin_level} g/dL ({albumin_points} pts)"
        elif respiratory_rate is not None:
            # Use modified CHOSEN score with respiratory rate
            rr_points = self._calculate_respiratory_rate_points(respiratory_rate)
            total_score = age_points + spo2_points + rr_points
            score_type = "Modified CHOSEN Score"
            threshold = self.MODIFIED_CHOSEN_THRESHOLD
            third_component = f"Respiratory Rate: {respiratory_rate} breaths/min ({rr_points} pts)"
        else:
            raise ValueError("Either albumin_level or respiratory_rate must be provided")
        
        # Get clinical interpretation
        interpretation = self._get_interpretation(total_score, threshold, score_type)
        
        return {
            "result": total_score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"],
            "calculation_details": {
                "score_type": score_type,
                "age_points": age_points,
                "spo2_points": spo2_points,
                "third_component": third_component,
                "total_score": total_score,
                "threshold_used": threshold,
                "discharge_recommendation": interpretation["recommendation"],
                "clinical_considerations": interpretation["considerations"]
            }
        }
    
    def _validate_inputs(
        self, 
        age: int, 
        oxygen_saturation: int, 
        albumin_level: Optional[float], 
        respiratory_rate: Optional[int]
    ):
        """Validates input parameters"""
        
        # Validate age
        if not isinstance(age, int) or age < 18 or age > 120:
            raise ValueError("Age must be between 18 and 120 years")
        
        # Validate oxygen saturation
        if not isinstance(oxygen_saturation, int) or oxygen_saturation < 80 or oxygen_saturation > 100:
            raise ValueError("Oxygen saturation must be between 80 and 100%")
        
        # Validate albumin if provided
        if albumin_level is not None:
            if not isinstance(albumin_level, (int, float)) or albumin_level < 1.0 or albumin_level > 6.0:
                raise ValueError("Albumin level must be between 1.0 and 6.0 g/dL")
        
        # Validate respiratory rate if provided
        if respiratory_rate is not None:
            if not isinstance(respiratory_rate, int) or respiratory_rate < 8 or respiratory_rate > 50:
                raise ValueError("Respiratory rate must be between 8 and 50 breaths/min")
        
        # Ensure at least one of albumin or respiratory rate is provided
        if albumin_level is None and respiratory_rate is None:
            raise ValueError("Either albumin_level or respiratory_rate must be provided")
    
    def _calculate_age_points(self, age: int) -> int:
        """Calculate points based on age"""
        for age_range in self.AGE_SCORES:
            if age_range["min"] <= age <= age_range["max"]:
                return age_range["points"]
        return 0  # Default fallback
    
    def _calculate_spo2_points(self, spo2: int) -> int:
        """Calculate points based on oxygen saturation"""
        for spo2_range in self.SPO2_SCORES:
            if spo2_range["min"] <= spo2 <= spo2_range["max"]:
                return spo2_range["points"]
        return 0  # Default fallback
    
    def _calculate_albumin_points(self, albumin: float) -> int:
        """Calculate points based on albumin level"""
        for albumin_range in self.ALBUMIN_SCORES:
            if albumin_range["min"] <= albumin <= albumin_range["max"]:
                return albumin_range["points"]
        return 0  # Default fallback
    
    def _calculate_respiratory_rate_points(self, rr: int) -> int:
        """Calculate points based on respiratory rate"""
        for rr_range in self.RESPIRATORY_RATE_SCORES:
            if rr_range["min"] <= rr <= rr_range["max"]:
                return rr_range["points"]
        return 0  # Default fallback
    
    def _get_interpretation(self, score: int, threshold: int, score_type: str) -> Dict[str, Any]:
        """
        Determines the interpretation based on CHOSEN score and threshold
        
        Args:
            score: Calculated CHOSEN score
            threshold: Threshold for discharge suitability (30 for full, 20 for modified)
            score_type: Type of score calculated
            
        Returns:
            Dict with interpretation details
        """
        
        if score < threshold:
            if score_type == "Full CHOSEN Score" and score < 20:
                stage = "Unlikely Suitable for Discharge"
                description = "High risk - strongly consider inpatient management"
                recommendation = "Not recommended for discharge"
                considerations = [
                    "High risk for clinical deterioration within 14 days",
                    "Consider need for supplemental oxygen, ICU care, or increased mortality risk",
                    "Evaluate for continued inpatient monitoring",
                    "Assess social support and follow-up capabilities"
                ]
            else:
                stage = "Borderline Risk"
                description = "Intermediate risk - clinical judgment required"
                recommendation = "Use clinical judgment for discharge decision"
                considerations = [
                    "Intermediate risk for clinical deterioration",
                    "Consider additional risk factors and patient-specific circumstances",
                    "Evaluate social support, comorbidities, and follow-up availability",
                    "May benefit from close outpatient monitoring if discharged"
                ]
            
            interpretation = (
                f"{score_type} of {score} points is below the threshold of {threshold}, "
                f"indicating the patient is {stage.lower()}. Consider continued inpatient "
                f"management or very close outpatient monitoring if discharge is considered."
            )
        else:
            stage = "Likely Suitable for Discharge"
            description = "Low risk - may be appropriate for home management"
            recommendation = "Consider for home discharge"
            considerations = [
                "Low risk for clinical deterioration within 14 days",
                "Ensure appropriate follow-up is arranged",
                "Provide clear instructions for symptom monitoring",
                "Consider telemedicine or nursing follow-up",
                "Ensure patient has adequate social support"
            ]
            
            interpretation = (
                f"{score_type} of {score} points is above the threshold of {threshold}, "
                f"indicating the patient is likely suitable for home discharge with appropriate "
                f"follow-up and monitoring arrangements."
            )
        
        return {
            "stage": stage,
            "description": description,
            "interpretation": interpretation,
            "recommendation": recommendation,
            "considerations": considerations
        }


def calculate_chosen_covid_discharge(
    age: int,
    oxygen_saturation: int,
    albumin_level: Optional[float] = None,
    respiratory_rate: Optional[int] = None
) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = ChosenCovidDischargeCalculator()
    return calculator.calculate(
        age=age,
        oxygen_saturation=oxygen_saturation,
        albumin_level=albumin_level,
        respiratory_rate=respiratory_rate
    )