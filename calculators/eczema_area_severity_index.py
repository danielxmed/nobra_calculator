"""
Eczema Area and Severity Index (EASI) Calculator

Stratifies eczema severity by assessing area involvement and severity signs across 
four body regions with validated clinical scoring. The EASI is the most validated 
and widely used assessment tool for atopic dermatitis severity in clinical practice 
and research.

References:
1. Hanifin JM, Thurston M, Omoto M, Cherill R, Tofte SJ, Graeber M. The eczema area 
   and severity index (EASI): assessment of reliability in atopic dermatitis. EASI 
   Evaluator Group. Exp Dermatol. 2001;10(1):11-8. doi: 10.1034/j.1600-0625.2001.100102.x.
2. Schmitt J, Langan S, Deckert S, Svensson A, von Kobyletzki L, Thomas K, et al. 
   Assessment of clinical signs of atopic dermatitis: a systematic review and 
   recommendation. J Allergy Clin Immunol. 2013;132(6):1337-47. doi: 10.1016/j.jaci.2013.07.008.
"""

from typing import Dict, Any


class EczemaAreaSeverityIndexCalculator:
    """Calculator for Eczema Area and Severity Index (EASI)"""
    
    def __init__(self):
        # Regional multipliers for different age groups
        self.REGIONAL_MULTIPLIERS = {
            'child_0_7': {
                'head_neck': 0.2,  # Children 0-7 years
                'upper_extremities': 0.2,
                'trunk': 0.3,
                'lower_extremities': 0.4
            },
            'adult_8_plus': {
                'head_neck': 0.1,  # Adults 8+ years  
                'upper_extremities': 0.2,
                'trunk': 0.3,
                'lower_extremities': 0.4
            }
        }
        
        # Body regions for calculation
        self.BODY_REGIONS = ['head_neck', 'upper_extremities', 'trunk', 'lower_extremities']
        
        # Severity signs assessed in each region
        self.SEVERITY_SIGNS = ['erythema', 'edema', 'excoriation', 'lichenification']
        
        # Area involvement scoring (0-6 scale)
        self.AREA_SCORES = {
            0: "0%",
            1: "1-9%", 
            2: "10-29%",
            3: "30-49%",
            4: "50-69%",
            5: "70-89%",
            6: "90-100%"
        }
        
        # Severity scoring (0-3 scale)
        self.SEVERITY_SCORES = {
            0: "Absent",
            1: "Mild",
            2: "Moderate", 
            3: "Severe"
        }
    
    def calculate(self, age_category: str, head_neck_area: int, head_neck_erythema: int, 
                  head_neck_edema: int, head_neck_excoriation: int, head_neck_lichenification: int,
                  upper_extremities_area: int, upper_extremities_erythema: int, 
                  upper_extremities_edema: int, upper_extremities_excoriation: int, 
                  upper_extremities_lichenification: int, trunk_area: int, trunk_erythema: int,
                  trunk_edema: int, trunk_excoriation: int, trunk_lichenification: int,
                  lower_extremities_area: int, lower_extremities_erythema: int, 
                  lower_extremities_edema: int, lower_extremities_excoriation: int,
                  lower_extremities_lichenification: int) -> Dict[str, Any]:
        """
        Calculates the EASI score using the provided parameters
        
        Args:
            age_category (str): Patient age category for multiplier selection (child_0_7 or adult_8_plus)
            head_neck_area (int): Head/neck area involvement (0-6)
            head_neck_erythema (int): Head/neck erythema severity (0-3)
            head_neck_edema (int): Head/neck edema/papulation severity (0-3)
            head_neck_excoriation (int): Head/neck excoriation severity (0-3)
            head_neck_lichenification (int): Head/neck lichenification severity (0-3)
            upper_extremities_area (int): Upper extremities area involvement (0-6)
            upper_extremities_erythema (int): Upper extremities erythema severity (0-3)
            upper_extremities_edema (int): Upper extremities edema/papulation severity (0-3)
            upper_extremities_excoriation (int): Upper extremities excoriation severity (0-3)
            upper_extremities_lichenification (int): Upper extremities lichenification severity (0-3)
            trunk_area (int): Trunk area involvement (0-6)
            trunk_erythema (int): Trunk erythema severity (0-3)
            trunk_edema (int): Trunk edema/papulation severity (0-3)
            trunk_excoriation (int): Trunk excoriation severity (0-3)
            trunk_lichenification (int): Trunk lichenification severity (0-3)
            lower_extremities_area (int): Lower extremities area involvement (0-6)
            lower_extremities_erythema (int): Lower extremities erythema severity (0-3)  
            lower_extremities_edema (int): Lower extremities edema/papulation severity (0-3)
            lower_extremities_excoriation (int): Lower extremities excoriation severity (0-3)
            lower_extremities_lichenification (int): Lower extremities lichenification severity (0-3)
            
        Returns:
            Dict with the result and interpretation
        """
        
        # Structure parameters for easier processing
        parameters = {
            'age_category': age_category,
            'head_neck': {
                'area': head_neck_area,
                'erythema': head_neck_erythema,
                'edema': head_neck_edema,
                'excoriation': head_neck_excoriation,
                'lichenification': head_neck_lichenification
            },
            'upper_extremities': {
                'area': upper_extremities_area,
                'erythema': upper_extremities_erythema,
                'edema': upper_extremities_edema,
                'excoriation': upper_extremities_excoriation,
                'lichenification': upper_extremities_lichenification
            },
            'trunk': {
                'area': trunk_area,
                'erythema': trunk_erythema,
                'edema': trunk_edema,
                'excoriation': trunk_excoriation,
                'lichenification': trunk_lichenification
            },
            'lower_extremities': {
                'area': lower_extremities_area,
                'erythema': lower_extremities_erythema,
                'edema': lower_extremities_edema,
                'excoriation': lower_extremities_excoriation,
                'lichenification': lower_extremities_lichenification
            }
        }
        
        # Validate inputs
        self._validate_inputs(parameters)
        
        # Calculate EASI score
        easi_score = self._calculate_easi_score(parameters)
        
        # Get interpretation
        interpretation = self._get_interpretation(easi_score)
        
        return {
            "result": easi_score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, parameters: Dict[str, Any]):
        """Validates input parameters"""
        
        # Validate age category
        if parameters['age_category'] not in self.REGIONAL_MULTIPLIERS:
            raise ValueError(f"Age category must be 'child_0_7' or 'adult_8_plus', got '{parameters['age_category']}'")
        
        # Validate each region's parameters
        for region in self.BODY_REGIONS:
            region_data = parameters[region]
            
            # Validate area score (0-6)
            area_score = region_data['area']
            if not isinstance(area_score, int) or area_score < 0 or area_score > 6:
                raise ValueError(f"{region} area score must be an integer between 0 and 6, got {area_score}")
            
            # Validate severity scores (0-3)
            for sign in self.SEVERITY_SIGNS:
                severity_score = region_data[sign]
                if not isinstance(severity_score, int) or severity_score < 0 or severity_score > 3:
                    raise ValueError(f"{region} {sign} severity must be an integer between 0 and 3, got {severity_score}")
    
    def _calculate_easi_score(self, parameters: Dict[str, Any]) -> float:
        """Calculates the EASI score using the standard formula"""
        
        age_category = parameters['age_category']
        multipliers = self.REGIONAL_MULTIPLIERS[age_category]
        
        total_score = 0.0
        
        # Calculate score for each body region
        for region in self.BODY_REGIONS:
            region_data = parameters[region]
            
            # Get area involvement score
            area_score = region_data['area']
            
            # Calculate sum of severity scores for this region
            severity_sum = (
                region_data['erythema'] +
                region_data['edema'] + 
                region_data['excoriation'] +
                region_data['lichenification']
            )
            
            # Get regional multiplier
            regional_multiplier = multipliers[region]
            
            # Calculate regional score: (severity_sum × area_score × regional_multiplier)
            regional_score = severity_sum * area_score * regional_multiplier
            
            total_score += regional_score
        
        # Round to 1 decimal place
        return round(total_score, 1)
    
    def _get_interpretation(self, easi_score: float) -> Dict[str, str]:
        """
        Determines the interpretation based on the EASI score
        
        Args:
            easi_score (float): Calculated EASI score
            
        Returns:
            Dict with interpretation
        """
        
        if easi_score == 0:
            return {
                "stage": "Clear",
                "description": "No eczema",
                "interpretation": "Clear skin with no signs of atopic dermatitis. Continue maintenance skincare routine with regular moisturizing and environmental management to prevent flares."
            }
        elif 0.1 <= easi_score <= 1.0:
            return {
                "stage": "Almost Clear", 
                "description": "Almost clear eczema",
                "interpretation": "Almost clear atopic dermatitis with minimal residual signs. Continue current treatment regimen and monitor for improvement or potential relapse. Maintain consistent skincare routine."
            }
        elif 1.1 <= easi_score <= 7.0:
            return {
                "stage": "Mild",
                "description": "Mild eczema",
                "interpretation": "Mild atopic dermatitis. First-line treatment with regular moisturizers, low-potency topical corticosteroids (Class VI-VII), and trigger avoidance. Focus on barrier repair and gentle skincare."
            }
        elif 7.1 <= easi_score <= 21.0:
            return {
                "stage": "Moderate",
                "description": "Moderate eczema", 
                "interpretation": "Moderate atopic dermatitis. Consider medium-potency topical corticosteroids (Class III-V), topical calcineurin inhibitors, or systemic therapy if topical treatments are inadequate. May require specialist referral."
            }
        elif 21.1 <= easi_score <= 50.0:
            return {
                "stage": "Severe",
                "description": "Severe eczema",
                "interpretation": "Severe atopic dermatitis requiring intensive treatment. High-potency topical corticosteroids (Class I-II), topical calcineurin inhibitors, systemic immunosuppressants, or biologic therapy may be indicated. Dermatology consultation recommended."
            }
        else:  # 50.1-72.0
            return {
                "stage": "Very Severe",
                "description": "Very severe eczema",
                "interpretation": "Very severe atopic dermatitis requiring aggressive multimodal treatment. Consider systemic immunosuppressants (methotrexate, cyclosporine), biologic therapy (dupilumab, tralokinumab), or referral to dermatology specialist for comprehensive management and quality of life assessment."
            }


def calculate_eczema_area_severity_index(age_category: str, head_neck_area: int, head_neck_erythema: int, 
                                       head_neck_edema: int, head_neck_excoriation: int, head_neck_lichenification: int,
                                       upper_extremities_area: int, upper_extremities_erythema: int, 
                                       upper_extremities_edema: int, upper_extremities_excoriation: int, 
                                       upper_extremities_lichenification: int, trunk_area: int, trunk_erythema: int,
                                       trunk_edema: int, trunk_excoriation: int, trunk_lichenification: int,
                                       lower_extremities_area: int, lower_extremities_erythema: int, 
                                       lower_extremities_edema: int, lower_extremities_excoriation: int,
                                       lower_extremities_lichenification: int) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_eczema_area_severity_index pattern
    """
    calculator = EczemaAreaSeverityIndexCalculator()
    return calculator.calculate(age_category, head_neck_area, head_neck_erythema, 
                              head_neck_edema, head_neck_excoriation, head_neck_lichenification,
                              upper_extremities_area, upper_extremities_erythema, 
                              upper_extremities_edema, upper_extremities_excoriation, 
                              upper_extremities_lichenification, trunk_area, trunk_erythema,
                              trunk_edema, trunk_excoriation, trunk_lichenification,
                              lower_extremities_area, lower_extremities_erythema, 
                              lower_extremities_edema, lower_extremities_excoriation,
                              lower_extremities_lichenification)