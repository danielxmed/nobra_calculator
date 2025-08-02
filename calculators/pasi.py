"""
Psoriasis Area and Severity Index (PASI) Calculator

Quantifies the severity of psoriasis by combining assessment of lesion severity 
and affected body surface area. This standardized measurement tool evaluates 
four body regions with scoring for erythema, induration, and desquamation.

References:
1. Fredriksson T, Pettersson U. Severe psoriasis--oral therapy with a new retinoid. 
   Dermatologica. 1978;157(4):238-44. doi: 10.1159/000250839.
2. Langley RG, Ellis CN. Evaluating psoriasis with Psoriasis Area and Severity 
   Index, Psoriasis Global Assessment, and Lattice System Physician's Global 
   Assessment. J Am Acad Dermatol. 2004;51(4):563-9. doi: 10.1016/j.jaad.2004.04.012.
3. Schmitt J, Wozel G. The psoriasis area and severity index is the adequate 
   criterion to define severity in chronic plaque-type psoriasis. Dermatology. 
   2005;210(3):194-9. doi: 10.1159/000083509.
"""

from typing import Dict, Any


class PasiCalculator:
    """Calculator for Psoriasis Area and Severity Index (PASI)"""
    
    def __init__(self):
        # Body surface area weights
        self.HEAD_WEIGHT = 0.1  # 10% of body surface area
        self.ARMS_WEIGHT = 0.2  # 20% of body surface area
        self.TRUNK_WEIGHT = 0.3  # 30% of body surface area
        self.LEGS_WEIGHT = 0.4  # 40% of body surface area
        
        # Severity thresholds
        self.MILD_THRESHOLD = 5.0
        self.MODERATE_THRESHOLD = 10.0
        self.SEVERE_THRESHOLD = 20.0
    
    def calculate(self, head_erythema: int, head_induration: int, head_desquamation: int, head_area: int,
                 arms_erythema: int, arms_induration: int, arms_desquamation: int, arms_area: int,
                 trunk_erythema: int, trunk_induration: int, trunk_desquamation: int, trunk_area: int,
                 legs_erythema: int, legs_induration: int, legs_desquamation: int, legs_area: int) -> Dict[str, Any]:
        """
        Calculates PASI score for psoriasis severity assessment
        
        Args:
            head_erythema (int): Erythema severity in head/neck (0-4)
            head_induration (int): Induration severity in head/neck (0-4)
            head_desquamation (int): Desquamation severity in head/neck (0-4)
            head_area (int): Area affected in head/neck (0-6)
            arms_erythema (int): Erythema severity in arms (0-4)
            arms_induration (int): Induration severity in arms (0-4)
            arms_desquamation (int): Desquamation severity in arms (0-4)
            arms_area (int): Area affected in arms (0-6)
            trunk_erythema (int): Erythema severity in trunk (0-4)
            trunk_induration (int): Induration severity in trunk (0-4)
            trunk_desquamation (int): Desquamation severity in trunk (0-4)
            trunk_area (int): Area affected in trunk (0-6)
            legs_erythema (int): Erythema severity in legs (0-4)
            legs_induration (int): Induration severity in legs (0-4)
            legs_desquamation (int): Desquamation severity in legs (0-4)
            legs_area (int): Area affected in legs (0-6)
            
        Returns:
            Dict with PASI score and clinical interpretation
        """
        
        # Validate inputs
        self._validate_inputs(
            head_erythema, head_induration, head_desquamation, head_area,
            arms_erythema, arms_induration, arms_desquamation, arms_area,
            trunk_erythema, trunk_induration, trunk_desquamation, trunk_area,
            legs_erythema, legs_induration, legs_desquamation, legs_area
        )
        
        # Calculate regional scores
        head_score = self._calculate_regional_score(
            head_erythema, head_induration, head_desquamation, head_area, self.HEAD_WEIGHT
        )
        
        arms_score = self._calculate_regional_score(
            arms_erythema, arms_induration, arms_desquamation, arms_area, self.ARMS_WEIGHT
        )
        
        trunk_score = self._calculate_regional_score(
            trunk_erythema, trunk_induration, trunk_desquamation, trunk_area, self.TRUNK_WEIGHT
        )
        
        legs_score = self._calculate_regional_score(
            legs_erythema, legs_induration, legs_desquamation, legs_area, self.LEGS_WEIGHT
        )
        
        # Calculate total PASI score
        total_pasi = head_score + arms_score + trunk_score + legs_score
        
        # Get interpretation
        interpretation = self._get_interpretation(total_pasi)
        
        return {
            "result": round(total_pasi, 1),
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, head_erythema: int, head_induration: int, head_desquamation: int, head_area: int,
                        arms_erythema: int, arms_induration: int, arms_desquamation: int, arms_area: int,
                        trunk_erythema: int, trunk_induration: int, trunk_desquamation: int, trunk_area: int,
                        legs_erythema: int, legs_induration: int, legs_desquamation: int, legs_area: int):
        """Validates input parameters"""
        
        # Define severity parameters (0-4)
        severity_params = [
            (head_erythema, "head_erythema"), (head_induration, "head_induration"), 
            (head_desquamation, "head_desquamation"), (arms_erythema, "arms_erythema"),
            (arms_induration, "arms_induration"), (arms_desquamation, "arms_desquamation"),
            (trunk_erythema, "trunk_erythema"), (trunk_induration, "trunk_induration"),
            (trunk_desquamation, "trunk_desquamation"), (legs_erythema, "legs_erythema"),
            (legs_induration, "legs_induration"), (legs_desquamation, "legs_desquamation")
        ]
        
        # Define area parameters (0-6)
        area_params = [
            (head_area, "head_area"), (arms_area, "arms_area"),
            (trunk_area, "trunk_area"), (legs_area, "legs_area")
        ]
        
        # Validate severity parameters
        for param, name in severity_params:
            if not isinstance(param, int) or param < 0 or param > 4:
                raise ValueError(f"{name} must be an integer between 0 and 4")
        
        # Validate area parameters
        for param, name in area_params:
            if not isinstance(param, int) or param < 0 or param > 6:
                raise ValueError(f"{name} must be an integer between 0 and 6")
    
    def _calculate_regional_score(self, erythema: int, induration: int, desquamation: int, 
                                 area: int, weight: float) -> float:
        """
        Calculates PASI score for a specific body region
        
        Formula: Weight × (Erythema + Induration + Desquamation) × Area
        """
        severity_sum = erythema + induration + desquamation
        regional_score = weight * severity_sum * area
        return regional_score
    
    def _get_interpretation(self, pasi_score: float) -> Dict[str, str]:
        """
        Determines clinical interpretation based on PASI score
        
        Args:
            pasi_score (float): Calculated PASI score
            
        Returns:
            Dict with clinical interpretation
        """
        
        if pasi_score < self.MILD_THRESHOLD:  # < 5
            return {
                "stage": "Mild",
                "description": "Mild psoriasis",
                "interpretation": "Mild psoriasis with minimal impact. Consider topical therapy including corticosteroids, vitamin D analogues, calcineurin inhibitors, or combination treatments. Lifestyle modifications including stress management, smoking cessation, and weight management may be beneficial. Regular monitoring and patient education essential. Most patients can be managed effectively with topical treatments and supportive care."
            }
        elif pasi_score < self.MODERATE_THRESHOLD:  # 5-10
            return {
                "stage": "Moderate",
                "description": "Moderate psoriasis",
                "interpretation": "Moderate psoriasis requiring active treatment consideration. Evaluate for phototherapy (narrowband UV-B), systemic conventional therapy (methotrexate, cyclosporine), or biologic therapy based on patient factors, treatment response, and quality of life impact. Regular monitoring with dermatology follow-up and adjustment of therapy may be needed. Consider combination treatments for optimal outcomes."
            }
        elif pasi_score < self.SEVERE_THRESHOLD:  # 10-20
            return {
                "stage": "Severe",
                "description": "Severe psoriasis",
                "interpretation": "Severe psoriasis requiring aggressive treatment intervention. Strong consideration for systemic therapy including biologics (TNF-α inhibitors, IL-17 inhibitors, IL-23 inhibitors), conventional immunosuppressants, or phototherapy. May significantly impact quality of life requiring multidisciplinary care including dermatology, rheumatology if psoriatic arthritis present, and mental health support. Regular monitoring for treatment response and adverse effects essential."
            }
        else:  # ≥ 20
            return {
                "stage": "Very Severe",
                "description": "Very severe psoriasis",
                "interpretation": "Very severe psoriasis with major impact on quality of life and functional status. Requires immediate and aggressive systemic treatment, likely biologics or combination therapy with careful monitoring. Consider hospitalization for severe extensive disease, erythrodermic psoriasis, or treatment complications. Regular specialist follow-up essential with multidisciplinary team approach. Address comorbidities including cardiovascular disease, metabolic syndrome, and psychological impact."
            }


def calculate_pasi(head_erythema: int, head_induration: int, head_desquamation: int, head_area: int,
                  arms_erythema: int, arms_induration: int, arms_desquamation: int, arms_area: int,
                  trunk_erythema: int, trunk_induration: int, trunk_desquamation: int, trunk_area: int,
                  legs_erythema: int, legs_induration: int, legs_desquamation: int, legs_area: int) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = PasiCalculator()
    return calculator.calculate(
        head_erythema, head_induration, head_desquamation, head_area,
        arms_erythema, arms_induration, arms_desquamation, arms_area,
        trunk_erythema, trunk_induration, trunk_desquamation, trunk_area,
        legs_erythema, legs_induration, legs_desquamation, legs_area
    )