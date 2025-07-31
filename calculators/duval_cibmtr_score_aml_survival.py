"""
Duval/CIBMTR Score for Acute Myelogenous Leukemia (AML) Survival Calculator

Predicts transplantation survival of AML patients undergoing allogeneic hematopoietic 
stem cell transplantation (HSCT) based on five pre-transplant risk factors.

References:
1. Duval M, Klein JP, He W, Cahn JY, Cairo M, Camitta BM, et al. Hematopoietic stem-cell 
   transplantation for acute leukemia in relapse or primary induction failure. J Clin Oncol. 
   2010;28(23):3730-8. doi: 10.1200/JCO.2010.28.8852.
2. Oran B, de Lima M, Garcia-Manero G, Thall PF, Lin R, Popat U, et al. A phase 3 randomized 
   study of 5-azacytidine vs physicians' choice as maintenance therapy for patients with AML 
   in first remission after intensive chemotherapy ineligible for stem cell transplantation. 
   Blood. 2013;121(24):4906-14.
"""

from typing import Dict, Any


class DuvalCibmtrScoreAmlSurvivalCalculator:
    """Calculator for Duval/CIBMTR Score for AML Survival"""
    
    def __init__(self):
        # Scoring criteria and point values for each parameter
        self.SCORING_CRITERIA = {
            'disease_group': {
                'description': 'Disease status at time of transplantation',
                'points': {
                    'Primary induction failure or first CR >6 months': 0,
                    'First CR <6 months': 1
                }
            },
            'cytogenetics': {
                'description': 'Cytogenetic risk category prior to HSCT',
                'points': {
                    'Good or intermediate': 0,
                    'Poor': 1
                }
            },
            'hla_match_group': {
                'description': 'HLA matching status between donor and recipient',
                'points': {
                    'HLA identical sibling or well/partially matched unrelated': 0,
                    'Mismatched unrelated': 1,
                    'Related other than HLA identical sibling': 2
                }
            },
            'circulating_blasts': {
                'description': 'Presence of circulating blasts at time of transplantation',
                'points': {
                    'Absent': 0,
                    'Present': 1
                }
            },
            'karnofsky_lansky_scale': {
                'description': 'Karnofsky (adults) or Lansky (pediatric) performance status scale',
                'points': {
                    '90-100': 0,
                    '<90': 1
                }
            }
        }
        
        # Survival outcomes by total score
        self.SURVIVAL_OUTCOMES = {
            0: {'survival_rate': 42, 'description': 'Excellent prognosis'},
            1: {'survival_rate': 28, 'description': 'Good prognosis'},
            2: {'survival_rate': 15, 'description': 'Intermediate prognosis'},
            3: {'survival_rate': 6, 'description': 'Poor prognosis'}  # ≥3 points
        }
    
    def calculate(self, disease_group: str, cytogenetics: str, hla_match_group: str,
                  circulating_blasts: str, karnofsky_lansky_scale: str) -> Dict[str, Any]:
        """
        Calculates the Duval/CIBMTR score using the provided parameters
        
        Args:
            disease_group (str): Disease status at transplantation
            cytogenetics (str): Cytogenetic risk category
            hla_match_group (str): HLA matching status
            circulating_blasts (str): Presence of circulating blasts
            karnofsky_lansky_scale (str): Performance status scale
            
        Returns:
            Dict with the result and interpretation
        """
        
        # Map parameters for easier processing
        parameters = {
            'disease_group': disease_group,
            'cytogenetics': cytogenetics,
            'hla_match_group': hla_match_group,
            'circulating_blasts': circulating_blasts,
            'karnofsky_lansky_scale': karnofsky_lansky_scale
        }
        
        # Validate inputs
        self._validate_inputs(parameters)
        
        # Calculate total score
        total_score, score_breakdown = self._calculate_total_score(parameters)
        
        # Get interpretation
        interpretation = self._get_interpretation(total_score, score_breakdown)
        
        return {
            "result": total_score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, parameters: Dict[str, Any]):
        """Validates input parameters"""
        
        for param_name, value in parameters.items():
            if not isinstance(value, str):
                raise ValueError(f"Parameter '{param_name}' must be a string")
            
            # Check if value is in valid options for this parameter
            valid_options = list(self.SCORING_CRITERIA[param_name]['points'].keys())
            if value not in valid_options:
                raise ValueError(f"Parameter '{param_name}' must be one of {valid_options}, got '{value}'")
    
    def _calculate_total_score(self, parameters: Dict[str, Any]) -> tuple[int, Dict[str, int]]:
        """Calculates the total Duval/CIBMTR score with breakdown"""
        
        total_score = 0
        score_breakdown = {}
        
        for param_name, value in parameters.items():
            # Get points for this parameter
            points = self.SCORING_CRITERIA[param_name]['points'][value]
            total_score += points
            
            # Store breakdown for interpretation (only parameters that contribute points)
            if points > 0:
                score_breakdown[param_name] = points
        
        return total_score, score_breakdown
    
    def _get_interpretation(self, total_score: int, score_breakdown: Dict[str, int]) -> Dict[str, str]:
        """
        Determines the interpretation based on the total score
        
        Args:
            total_score (int): Calculated total score
            score_breakdown (Dict): Breakdown of contributing factors
            
        Returns:
            Dict with interpretation
        """
        
        # Determine score category (scores ≥3 are grouped together)
        if total_score >= 3:
            score_category = 3
            stage = "Score ≥3"
            survival_rate = 6
            description = "Poor prognosis"
            base_interpretation = (
                "6% 3-year overall survival. Poor prognosis for AML patients undergoing allogeneic HSCT. "
                "Consider alternative treatment strategies, palliative care discussions, and comprehensive "
                "family counseling. Transplant decision requires multidisciplinary team consensus."
            )
        else:
            score_category = total_score
            stage = f"Score {total_score}"
            survival_data = self.SURVIVAL_OUTCOMES[total_score]
            survival_rate = survival_data['survival_rate']
            description = survival_data['description']
            
            if total_score == 0:
                base_interpretation = (
                    f"{survival_rate}% 3-year overall survival. Excellent prognosis for AML patients "
                    "undergoing allogeneic HSCT. Proceed with transplantation as planned with standard "
                    "supportive care protocols."
                )
            elif total_score == 1:
                base_interpretation = (
                    f"{survival_rate}% 3-year overall survival. Good prognosis for AML patients "
                    "undergoing allogeneic HSCT. Consider enhanced supportive care measures and "
                    "close monitoring post-transplant."
                )
            elif total_score == 2:
                base_interpretation = (
                    f"{survival_rate}% 3-year overall survival. Intermediate prognosis for AML patients "
                    "undergoing allogeneic HSCT. Careful risk-benefit analysis needed. Consider intensive "
                    "supportive care and early intervention strategies."
                )
        
        # Add contributing factors if any
        interpretation_text = base_interpretation
        
        if score_breakdown:
            contributing_factors = []
            for param_name, points in score_breakdown.items():
                factor_description = self.SCORING_CRITERIA[param_name]['description']
                contributing_factors.append(f"{factor_description} (+{points} point{'s' if points > 1 else ''})")
            
            interpretation_text += f" Contributing risk factors: {'; '.join(contributing_factors)}."
        
        # Add general clinical guidance
        if total_score >= 3:
            interpretation_text += (
                " Strongly recommend multidisciplinary team discussion including hematology, "
                "transplant medicine, and palliative care specialists. Consider clinical trial "
                "enrollment if available."
            )
        elif total_score >= 2:
            interpretation_text += (
                " Close collaboration with transplant team recommended. Monitor for early signs "
                "of complications and consider prophylactic interventions where appropriate."
            )
        else:
            interpretation_text += (
                " Continue with standard pre-transplant preparation and conditioning regimen. "
                "Maintain optimal performance status and disease control."
            )
        
        # Add score limitations and considerations
        interpretation_text += (
            " This score is based on myeloablative conditioning regimens and may not apply to "
            "reduced-intensity conditioning. Regular reassessment recommended throughout the "
            "transplant process."
        )
        
        return {
            "stage": stage,
            "description": description,
            "interpretation": interpretation_text
        }


def calculate_duval_cibmtr_score_aml_survival(disease_group: str, cytogenetics: str,
                                            hla_match_group: str, circulating_blasts: str,
                                            karnofsky_lansky_scale: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_duval_cibmtr_score_aml_survival pattern
    """
    calculator = DuvalCibmtrScoreAmlSurvivalCalculator()
    return calculator.calculate(disease_group, cytogenetics, hla_match_group,
                               circulating_blasts, karnofsky_lansky_scale)