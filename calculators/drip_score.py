"""
Drug Resistance in Pneumonia (DRIP) Score Calculator

Predicts risk for community-acquired pneumonia due to drug-resistant pathogens (CAP-DRP).
Helps determine when broad-spectrum antibiotics should be used.

References:
1. Webb BJ, Dascomb K, Stenehjem E, Dean N. Derivation and multicenter validation 
   of the drug resistance in pneumonia clinical prediction score. Antimicrob Agents 
   Chemother. 2016;60(5):2652-63.
2. Attridge RT, Frei CR, Restrepo MI, et al. Guideline-concordant therapy and outcomes 
   in healthcare-associated pneumonia. Eur Respir J. 2011;38(4):878-87.
"""

from typing import Dict, Any


class DripScoreCalculator:
    """Calculator for Drug Resistance in Pneumonia (DRIP) Score"""
    
    def __init__(self):
        # DRIP Score weights
        self.MAJOR_RISK_FACTOR_POINTS = 2
        self.MINOR_RISK_FACTOR_POINTS = 1
        
        # Major risk factors (2 points each)
        self.MAJOR_FACTORS = [
            'antibiotic_use_60_days',
            'long_term_care_facility', 
            'tube_feeding',
            'prior_drug_resistant_infection'
        ]
        
        # Minor risk factors (1 point each)
        self.MINOR_FACTORS = [
            'chronic_pulmonary_disease',
            'hospitalization_60_days',
            'poor_functional_status', 
            'mrsa_colonization',
            'wound_care',
            'gastric_acid_suppression'
        ]
    
    def calculate(self, antibiotic_use_60_days: str, long_term_care_facility: str,
                  tube_feeding: str, prior_drug_resistant_infection: str,
                  chronic_pulmonary_disease: str, hospitalization_60_days: str,
                  poor_functional_status: str, mrsa_colonization: str,
                  wound_care: str, gastric_acid_suppression: str) -> Dict[str, Any]:
        """
        Calculates the DRIP score using the provided risk factors
        
        Args:
            antibiotic_use_60_days (str): Antibiotic use within 60 days (major factor)
            long_term_care_facility (str): Residence in long-term care facility (major factor)
            tube_feeding (str): Tube feeding (major factor)
            prior_drug_resistant_infection (str): Prior drug-resistant infection (major factor)
            chronic_pulmonary_disease (str): Chronic pulmonary disease (minor factor)
            hospitalization_60_days (str): Prior hospitalization within 60 days (minor factor)
            poor_functional_status (str): Poor functional status (minor factor)
            mrsa_colonization (str): MRSA colonization (minor factor)
            wound_care (str): Wound care (minor factor)
            gastric_acid_suppression (str): Gastric acid suppression (minor factor)
            
        Returns:
            Dict with the result and interpretation
        """
        
        # Map parameters for easier processing
        parameters = {
            'antibiotic_use_60_days': antibiotic_use_60_days,
            'long_term_care_facility': long_term_care_facility,
            'tube_feeding': tube_feeding,
            'prior_drug_resistant_infection': prior_drug_resistant_infection,
            'chronic_pulmonary_disease': chronic_pulmonary_disease,
            'hospitalization_60_days': hospitalization_60_days,
            'poor_functional_status': poor_functional_status,
            'mrsa_colonization': mrsa_colonization,
            'wound_care': wound_care,
            'gastric_acid_suppression': gastric_acid_suppression
        }
        
        # Validate inputs
        self._validate_inputs(parameters)
        
        # Calculate score
        result = self._calculate_score(parameters)
        
        # Get interpretation
        interpretation = self._get_interpretation(result)
        
        return {
            "result": result,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, parameters: Dict[str, str]):
        """Validates input parameters"""
        
        valid_responses = ["yes", "no"]
        
        for param_name, response in parameters.items():
            if not isinstance(response, str):
                raise ValueError(f"Parameter '{param_name}' must be a string")
            
            if response.lower() not in valid_responses:
                raise ValueError(f"Parameter '{param_name}' must be 'yes' or 'no', got '{response}'")
    
    def _calculate_score(self, parameters: Dict[str, str]) -> int:
        """Implements the DRIP scoring formula"""
        
        score = 0
        
        # Count major risk factors (2 points each)
        for factor in self.MAJOR_FACTORS:
            if parameters[factor].lower() == "yes":
                score += self.MAJOR_RISK_FACTOR_POINTS
        
        # Count minor risk factors (1 point each)
        for factor in self.MINOR_FACTORS:
            if parameters[factor].lower() == "yes":
                score += self.MINOR_RISK_FACTOR_POINTS
                
        return score
    
    def _get_interpretation(self, result: int) -> Dict[str, str]:
        """
        Determines the interpretation based on the DRIP score
        
        Args:
            result (int): Calculated DRIP score
            
        Returns:
            Dict with interpretation details
        """
        
        if result < 4:
            return {
                "stage": "Low Risk",
                "description": "Low risk of drug-resistant pneumonia",
                "interpretation": "Scores <4 were associated with lower risk of drug-resistant pneumonia. Consider treating without extended-spectrum antibiotics. Standard empirical antibiotics appropriate."
            }
        else:  # >= 4
            return {
                "stage": "High Risk",
                "description": "High risk of drug-resistant pneumonia", 
                "interpretation": "Scores ≥4 were associated with higher risk of drug-resistant pneumonia. Extended-spectrum antibiotic coverage is recommended to ensure effective treatment."
            }


def calculate_drip_score(antibiotic_use_60_days: str, long_term_care_facility: str,
                        tube_feeding: str, prior_drug_resistant_infection: str,
                        chronic_pulmonary_disease: str, hospitalization_60_days: str,
                        poor_functional_status: str, mrsa_colonization: str,
                        wound_care: str, gastric_acid_suppression: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_drip_score pattern
    """
    calculator = DripScoreCalculator()
    return calculator.calculate(
        antibiotic_use_60_days, long_term_care_facility, tube_feeding,
        prior_drug_resistant_infection, chronic_pulmonary_disease, hospitalization_60_days,
        poor_functional_status, mrsa_colonization, wound_care, gastric_acid_suppression
    )