"""
Dutch Criteria for Familial Hypercholesterolemia (FH) Calculator

Diagnoses familial hypercholesterolemia (FH) based on clinical, genetic, and family 
history using the Dutch Lipid Clinic Network (DLCN) point-based scoring system. 
Provides stratification into possible, probable, or definite FH categories.

References:
1. The diagnosis and management of familial hypercholesterolaemia. Dutch Health Care 
   Insurance Board. 1999.
2. Nordestgaard BG, Chapman MJ, Humphries SE, Ginsberg HN, Masana L, Descamps OS, et al. 
   Familial hypercholesterolaemia is underdiagnosed and undertreated in the general 
   population: guidance for clinicians to prevent coronary heart disease. Eur Heart J. 2013.
"""

from typing import Dict, Any


class DutchCriteriaFamilialHypercholesterolemiaCalculator:
    """Calculator for Dutch Criteria for Familial Hypercholesterolemia"""
    
    def __init__(self):
        # LDL cholesterol scoring thresholds (mmol/L)
        self.LDL_SCORING = {
            8.5: 8,    # ≥8.5 mmol/L = 8 points
            6.5: 5,    # 6.5-8.4 mmol/L = 5 points  
            5.0: 3,    # 5.0-6.4 mmol/L = 3 points
            4.0: 1     # 4.0-4.9 mmol/L = 1 point
        }
        
        # Clinical and family history point values
        self.TENDON_XANTHOMAS_POINTS = 6
        self.CORNEAL_ARCUS_POINTS = 4
        self.FAMILY_HISTORY_LDL_POINTS = 1
        self.FAMILY_HISTORY_CHD_POINTS = 1
        self.PERSONAL_CHD_POINTS = 2
        self.PERSONAL_CVD_POINTS = 1
        self.DNA_POSITIVE_POINTS = 8
    
    def calculate(self, ldl_cholesterol_mmol: float, tendon_xanthomas: str, corneal_arcus: str,
                  family_history_ldl: str, family_history_chd: str, personal_chd: str,
                  personal_cvd: str, dna_analysis: str) -> Dict[str, Any]:
        """
        Calculates the Dutch Criteria for Familial Hypercholesterolemia score
        
        Args:
            ldl_cholesterol_mmol (float): LDL cholesterol level in mmol/L
            tendon_xanthomas (str): Presence of tendon xanthomas (yes/no)
            corneal_arcus (str): Corneal arcus in patient <45 years old (yes/no)
            family_history_ldl (str): Family history of elevated LDL cholesterol (yes/no)
            family_history_chd (str): Family history of premature CHD (yes/no)
            personal_chd (str): Personal history of premature CHD (yes/no)
            personal_cvd (str): Personal history of premature CVD (yes/no)
            dna_analysis (str): DNA analysis results (positive/negative/not_performed)
            
        Returns:
            Dict with the result and interpretation
        """
        
        # Map parameters for easier processing
        parameters = {
            'ldl_cholesterol_mmol': ldl_cholesterol_mmol,
            'tendon_xanthomas': tendon_xanthomas,
            'corneal_arcus': corneal_arcus,
            'family_history_ldl': family_history_ldl,
            'family_history_chd': family_history_chd,
            'personal_chd': personal_chd,
            'personal_cvd': personal_cvd,
            'dna_analysis': dna_analysis
        }
        
        # Validate inputs
        self._validate_inputs(parameters)
        
        # Calculate total score
        total_score = self._calculate_total_score(parameters)
        
        # Get interpretation
        interpretation = self._get_interpretation(total_score)
        
        return {
            "result": total_score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, parameters: Dict[str, Any]):
        """Validates input parameters"""
        
        # Validate LDL cholesterol
        ldl = parameters['ldl_cholesterol_mmol']
        if not isinstance(ldl, (int, float)):
            raise ValueError("LDL cholesterol must be a number")
        
        if ldl < 0 or ldl > 30:
            raise ValueError("LDL cholesterol must be between 0 and 30 mmol/L")
        
        # Validate yes/no parameters
        yes_no_params = ['tendon_xanthomas', 'corneal_arcus', 'family_history_ldl', 
                        'family_history_chd', 'personal_chd', 'personal_cvd']
        
        for param in yes_no_params:
            value = parameters[param]
            if not isinstance(value, str):
                raise ValueError(f"Parameter '{param}' must be a string")
            
            if value.lower() not in ['yes', 'no']:
                raise ValueError(f"Parameter '{param}' must be 'yes' or 'no', got '{value}'")
        
        # Validate DNA analysis
        dna = parameters['dna_analysis']
        if not isinstance(dna, str):
            raise ValueError("DNA analysis must be a string")
        
        if dna.lower() not in ['positive', 'negative', 'not_performed']:
            raise ValueError("DNA analysis must be 'positive', 'negative', or 'not_performed'")
    
    def _calculate_total_score(self, parameters: Dict[str, Any]) -> int:
        """Calculates the total Dutch FH score"""
        
        total_score = 0
        
        # LDL cholesterol points
        ldl = parameters['ldl_cholesterol_mmol']
        ldl_points = self._calculate_ldl_points(ldl)
        total_score += ldl_points
        
        # Clinical findings
        if parameters['tendon_xanthomas'].lower() == 'yes':
            total_score += self.TENDON_XANTHOMAS_POINTS
        
        if parameters['corneal_arcus'].lower() == 'yes':
            total_score += self.CORNEAL_ARCUS_POINTS
        
        # Family history
        if parameters['family_history_ldl'].lower() == 'yes':
            total_score += self.FAMILY_HISTORY_LDL_POINTS
        
        if parameters['family_history_chd'].lower() == 'yes':
            total_score += self.FAMILY_HISTORY_CHD_POINTS
        
        # Personal history
        if parameters['personal_chd'].lower() == 'yes':
            total_score += self.PERSONAL_CHD_POINTS
        
        if parameters['personal_cvd'].lower() == 'yes':
            total_score += self.PERSONAL_CVD_POINTS
        
        # DNA analysis
        if parameters['dna_analysis'].lower() == 'positive':
            total_score += self.DNA_POSITIVE_POINTS
        
        return total_score
    
    def _calculate_ldl_points(self, ldl: float) -> int:
        """Calculates points for LDL cholesterol level"""
        
        if ldl >= 8.5:
            return 8
        elif ldl >= 6.5:
            return 5
        elif ldl >= 5.0:
            return 3
        elif ldl >= 4.0:
            return 1
        else:
            return 0
    
    def _get_interpretation(self, total_score: int) -> Dict[str, str]:
        """
        Determines the interpretation based on the Dutch FH score
        
        Args:
            total_score (int): Calculated Dutch FH score
            
        Returns:
            Dict with interpretation
        """
        
        if total_score <= 2:
            return {
                "stage": "Unlikely FH",
                "description": "FH unlikely",
                "interpretation": f"Familial hypercholesterolemia is unlikely (Dutch score = {total_score}) based on Dutch criteria. Consider other causes of hypercholesterolemia including secondary causes (hypothyroidism, diabetes, nephrotic syndrome, medications). Routine lipid management and cardiovascular risk assessment appropriate."
            }
        elif total_score <= 5:
            return {
                "stage": "Possible FH",
                "description": "Possible familial hypercholesterolemia",
                "interpretation": f"Possible familial hypercholesterolemia (Dutch score = {total_score}). Consider genetic testing if available and appropriate. Initiate high-intensity statin therapy. Screen first-degree relatives for elevated cholesterol. Consider cascade screening and specialist referral."
            }
        elif total_score <= 7:
            return {
                "stage": "Probable FH",
                "description": "Probable familial hypercholesterolemia",
                "interpretation": f"Probable familial hypercholesterolemia (Dutch score = {total_score}). Strong indication for genetic testing and specialist referral. Initiate high-intensity statin therapy with goal LDL <1.8 mmol/L (70 mg/dL). Mandatory cascade screening of first-degree relatives. Consider additional lipid-lowering therapy if statin alone insufficient."
            }
        else:  # score >= 8
            return {
                "stage": "Definite FH",
                "description": "Definite familial hypercholesterolemia",
                "interpretation": f"Definite familial hypercholesterolemia (Dutch score = {total_score}). Immediate specialist referral required. Aggressive lipid-lowering therapy with combination treatment (statin + ezetimibe ± PCSK9 inhibitor) targeting LDL <1.8 mmol/L (70 mg/dL). Mandatory cascade screening of all first-degree relatives. Consider genetic counseling."
            }


def calculate_dutch_criteria_familial_hypercholesterolemia(ldl_cholesterol_mmol: float, tendon_xanthomas: str, 
                                                          corneal_arcus: str, family_history_ldl: str, 
                                                          family_history_chd: str, personal_chd: str,
                                                          personal_cvd: str, dna_analysis: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_dutch_criteria_familial_hypercholesterolemia pattern
    """
    calculator = DutchCriteriaFamilialHypercholesterolemiaCalculator()
    return calculator.calculate(
        ldl_cholesterol_mmol, tendon_xanthomas, corneal_arcus, family_history_ldl,
        family_history_chd, personal_chd, personal_cvd, dna_analysis
    )