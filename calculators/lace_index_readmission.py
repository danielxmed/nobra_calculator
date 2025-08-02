"""
LACE Index for Readmission Calculator

Predicts 30-day readmission or death in medical and surgical ward patients using four 
key clinical factors: Length of stay, Acuity of admission, Comorbidities, and Emergency 
department visits. This validated index helps healthcare teams identify high-risk patients 
who may benefit from enhanced discharge planning and follow-up care.

References:
1. van Walraven C, Dhalla IA, Bell C, et al. Derivation and validation of an index to 
   predict early death or unplanned readmission after discharge from hospital to the 
   community. CMAJ. 2010 Apr 6;182(6):551-7.
2. Walraven C, Wong J, Forster AJ. LACE+ index: extension of a validated index to predict 
   early death or urgent readmission after hospital discharge using administrative data. 
   Open Med. 2012;6(4):e80-90.
"""

from typing import Dict, Any


class LaceIndexReadmissionCalculator:
    """Calculator for LACE Index for Readmission Risk Assessment"""
    
    def __init__(self):
        """Initialize LACE scoring parameters and risk thresholds"""
        
        # Length of stay scoring (L)
        self.length_of_stay_scoring = [
            (0, 0, 0),      # <1 day: 0 points
            (1, 1, 1),      # 1 day: 1 point
            (2, 2, 2),      # 2 days: 2 points
            (3, 3, 3),      # 3 days: 3 points
            (4, 6, 4),      # 4-6 days: 4 points
            (7, 13, 5),     # 7-13 days: 5 points
            (14, 999, 7)    # ≥14 days: 7 points
        ]
        
        # Charlson Comorbidity Index scoring (C)
        self.charlson_scoring = [
            (0, 0, 0),      # 0 points: 0 points
            (1, 1, 1),      # 1 point: 1 point
            (2, 2, 2),      # 2 points: 2 points
            (3, 3, 3),      # 3 points: 3 points
            (4, 999, 5)     # ≥4 points: 5 points
        ]
        
        # ED visits scoring (E)
        self.ed_visits_scoring = [
            (0, 0, 0),      # 0 visits: 0 points
            (1, 1, 1),      # 1 visit: 1 point
            (2, 2, 2),      # 2 visits: 2 points
            (3, 3, 3),      # 3 visits: 3 points
            (4, 999, 4)     # ≥4 visits: 4 points
        ]
        
        # Risk classification thresholds
        self.low_risk_threshold = 4      # 0-4: Low risk
        self.moderate_risk_threshold = 9  # 5-9: Moderate risk
        # ≥10: High risk
    
    def calculate(self, length_of_stay_days: int, acute_emergent_admission: str,
                 charlson_comorbidity_index: int, ed_visits_6_months: int) -> Dict[str, Any]:
        """
        Calculates LACE Index for readmission risk assessment
        
        Args:
            length_of_stay_days (int): Length of current hospital stay in days
            acute_emergent_admission (str): "yes" if acute/emergent, "no" if planned
            charlson_comorbidity_index (int): Charlson Comorbidity Index score (0-37)
            ed_visits_6_months (int): Number of ED visits in past 6 months
            
        Returns:
            Dict with LACE score and risk assessment
        """
        
        # Validate inputs
        self._validate_inputs(length_of_stay_days, acute_emergent_admission, 
                            charlson_comorbidity_index, ed_visits_6_months)
        
        # Calculate individual component scores
        length_score = self._calculate_length_score(length_of_stay_days)
        acute_score = self._calculate_acute_score(acute_emergent_admission)
        charlson_score = self._calculate_charlson_score(charlson_comorbidity_index)
        ed_score = self._calculate_ed_score(ed_visits_6_months)
        
        # Calculate total LACE score
        total_score = length_score + acute_score + charlson_score + ed_score
        
        # Get risk assessment
        risk_assessment = self._assess_risk(total_score)
        
        # Generate interpretation
        interpretation = self._generate_interpretation(
            total_score, length_score, acute_score, charlson_score, ed_score, risk_assessment
        )
        
        return {
            "result": total_score,
            "unit": "points",
            "interpretation": interpretation,
            "stage": risk_assessment["stage"],
            "stage_description": risk_assessment["description"]
        }
    
    def _validate_inputs(self, length_of_stay_days: int, acute_emergent_admission: str,
                        charlson_comorbidity_index: int, ed_visits_6_months: int):
        """Validates input parameters"""
        
        if not isinstance(length_of_stay_days, int) or length_of_stay_days < 0:
            raise ValueError("Length of stay must be a non-negative integer")
        
        if length_of_stay_days > 365:
            raise ValueError("Length of stay should not exceed 365 days")
        
        if acute_emergent_admission not in ["yes", "no"]:
            raise ValueError("Acute emergent admission must be 'yes' or 'no'")
        
        if not isinstance(charlson_comorbidity_index, int) or charlson_comorbidity_index < 0:
            raise ValueError("Charlson Comorbidity Index must be a non-negative integer")
        
        if charlson_comorbidity_index > 37:
            raise ValueError("Charlson Comorbidity Index should not exceed 37")
        
        if not isinstance(ed_visits_6_months, int) or ed_visits_6_months < 0:
            raise ValueError("ED visits must be a non-negative integer")
        
        if ed_visits_6_months > 20:
            raise ValueError("ED visits should be reasonable (≤20 in 6 months)")
    
    def _calculate_length_score(self, days: int) -> int:
        """Calculate Length of stay score (L component)"""
        
        for min_days, max_days, score in self.length_of_stay_scoring:
            if min_days <= days <= max_days:
                return score
        
        # Should not reach here with proper validation
        return 7  # Maximum score for very long stays
    
    def _calculate_acute_score(self, acute_admission: str) -> int:
        """Calculate Acute admission score (A component)"""
        
        return 3 if acute_admission == "yes" else 0
    
    def _calculate_charlson_score(self, charlson_index: int) -> int:
        """Calculate Charlson comorbidity score (C component)"""
        
        for min_score, max_score, lace_score in self.charlson_scoring:
            if min_score <= charlson_index <= max_score:
                return lace_score
        
        # Should not reach here with proper validation
        return 5  # Maximum score for very high comorbidity
    
    def _calculate_ed_score(self, ed_visits: int) -> int:
        """Calculate Emergency department visits score (E component)"""
        
        for min_visits, max_visits, score in self.ed_visits_scoring:
            if min_visits <= ed_visits <= max_visits:
                return score
        
        # Should not reach here with proper validation
        return 4  # Maximum score for frequent ED visits
    
    def _assess_risk(self, total_score: int) -> Dict[str, str]:
        """
        Assess readmission risk based on total LACE score
        
        Args:
            total_score (int): Total LACE score
            
        Returns:
            Dict with risk assessment
        """
        
        if total_score <= self.low_risk_threshold:
            return {
                "stage": "Low Risk",
                "description": "Low risk of 30-day readmission or death"
            }
        elif total_score <= self.moderate_risk_threshold:
            return {
                "stage": "Moderate Risk",
                "description": "Moderate risk of 30-day readmission or death"
            }
        else:
            return {
                "stage": "High Risk",
                "description": "High risk of 30-day readmission or death"
            }
    
    def _generate_interpretation(self, total_score: int, length_score: int, 
                               acute_score: int, charlson_score: int, ed_score: int,
                               risk_assessment: Dict) -> str:
        """
        Generates comprehensive clinical interpretation
        
        Args:
            total_score (int): Total LACE score
            length_score, acute_score, charlson_score, ed_score (int): Component scores
            risk_assessment (Dict): Risk assessment results
            
        Returns:
            str: Detailed clinical interpretation
        """
        
        # Base interpretation
        component_breakdown = (
            f"LACE Index = {total_score} points "
            f"(L:{length_score} + A:{acute_score} + C:{charlson_score} + E:{ed_score}). "
        )
        
        # Risk assessment
        risk_description = f"This score indicates {risk_assessment['stage'].lower()} for 30-day readmission or death. "
        
        # Clinical recommendations based on risk level
        if total_score <= self.low_risk_threshold:
            recommendations = (
                "Standard discharge planning and routine follow-up are appropriate. "
                "Patients with low LACE scores typically have good outcomes with standard care. "
            )
        elif total_score <= self.moderate_risk_threshold:
            recommendations = (
                "Consider enhanced discharge planning with structured follow-up within 7-14 days. "
                "Care coordination and patient education may help reduce readmission risk. "
                "Monitor for early signs of clinical deterioration. "
            )
        else:
            recommendations = (
                "Intensive discharge planning and care coordination strongly recommended. "
                "Consider early post-discharge follow-up within 48-72 hours. "
                "Medication reconciliation, home health services, and patient/caregiver education are crucial. "
                "Multidisciplinary team approach with case management may be beneficial. "
            )
        
        # Additional clinical context
        additional_context = (
            "The LACE Index is validated for adults ≥18 years and considers key predictors: "
            "length of stay, admission acuity, comorbidity burden, and recent healthcare utilization. "
            "Use in conjunction with clinical judgment and institutional discharge protocols."
        )
        
        return component_breakdown + risk_description + recommendations + additional_context


def calculate_lace_index_readmission(length_of_stay_days, acute_emergent_admission, 
                                   charlson_comorbidity_index, ed_visits_6_months) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = LaceIndexReadmissionCalculator()
    return calculator.calculate(length_of_stay_days, acute_emergent_admission,
                              charlson_comorbidity_index, ed_visits_6_months)