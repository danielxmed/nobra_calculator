"""
International Ovarian Tumor Analysis (IOTA) Simple Rules Risk Assessment Calculator

Predicts risk of malignancy in adnexal masses using ultrasonographic features.
The IOTA Simple Rules use 10 ultrasound features to classify ovarian masses as 
benign, malignant, or inconclusive based on the presence of B-features (benign) 
and M-features (malignant).

References (Vancouver style):
1. Timmerman D, Testa AC, Bourne T, et al. Logistic regression model to distinguish 
   between the benign and malignant adnexal mass before surgery: a multicenter study 
   by the International Ovarian Tumor Analysis Group. J Clin Oncol. 2005 Dec 1;23(34):8794-801. 
   doi: 10.1200/JCO.2005.01.7632.
2. Timmerman D, Ameye L, Fischerova D, et al. Simple ultrasound rules to distinguish 
   between benign and malignant adnexal masses before surgery: prospective validation 
   study. BMJ. 2010 Dec 14;341:c6839. doi: 10.1136/bmj.c6839.
3. Nunes N, Ambler G, Foo X, et al. Use of IOTA simple rules for diagnosis of ovarian 
   cancer: meta-analysis. Ultrasound Obstet Gynecol. 2014 Nov;44(5):503-14. 
   doi: 10.1002/uog.13437.
"""

from typing import Dict, Any


class IotaSimpleRulesCalculator:
    """Calculator for IOTA Simple Rules Risk Assessment"""
    
    def __init__(self):
        # Define benign features (B-rules)
        self.benign_features = [
            "unilocular_cyst",              # B1
            "solid_components_small",        # B2
            "acoustic_shadows",              # B3
            "smooth_multilocular_small",     # B4
            "no_blood_flow"                  # B5
        ]
        
        # Define malignant features (M-rules)
        self.malignant_features = [
            "irregular_solid_tumor",         # M1
            "ascites",                       # M2
            "papillary_structures",          # M3
            "irregular_multilocular_large",  # M4
            "strong_blood_flow"              # M5
        ]
    
    def calculate(self, unilocular_cyst: str, solid_components_small: str, acoustic_shadows: str,
                 smooth_multilocular_small: str, no_blood_flow: str, irregular_solid_tumor: str,
                 ascites: str, papillary_structures: str, irregular_multilocular_large: str,
                 strong_blood_flow: str) -> Dict[str, Any]:
        """
        Calculates the IOTA Simple Rules risk classification
        
        Args:
            unilocular_cyst (str): B1 - Unilocular cyst
            solid_components_small (str): B2 - Solid components <7mm
            acoustic_shadows (str): B3 - Acoustic shadows
            smooth_multilocular_small (str): B4 - Smooth multilocular tumor <100mm
            no_blood_flow (str): B5 - No blood flow (color score 1)
            irregular_solid_tumor (str): M1 - Irregular solid tumor
            ascites (str): M2 - Ascites
            papillary_structures (str): M3 - At least 4 papillary structures
            irregular_multilocular_large (str): M4 - Irregular multilocular solid tumor ≥100mm
            strong_blood_flow (str): M5 - Very strong blood flow (color score 4)
            
        Returns:
            Dict with the IOTA classification and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(
            unilocular_cyst, solid_components_small, acoustic_shadows,
            smooth_multilocular_small, no_blood_flow, irregular_solid_tumor,
            ascites, papillary_structures, irregular_multilocular_large, strong_blood_flow
        )
        
        # Create parameters dictionary
        parameters = {
            "unilocular_cyst": unilocular_cyst,
            "solid_components_small": solid_components_small,
            "acoustic_shadows": acoustic_shadows,
            "smooth_multilocular_small": smooth_multilocular_small,
            "no_blood_flow": no_blood_flow,
            "irregular_solid_tumor": irregular_solid_tumor,
            "ascites": ascites,
            "papillary_structures": papillary_structures,
            "irregular_multilocular_large": irregular_multilocular_large,
            "strong_blood_flow": strong_blood_flow
        }
        
        # Classify based on IOTA Simple Rules
        classification = self._classify_mass(parameters)
        
        # Get interpretation
        interpretation = self._get_interpretation(classification)
        
        return {
            "result": classification,
            "unit": "classification",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, unilocular_cyst: str, solid_components_small: str, acoustic_shadows: str,
                        smooth_multilocular_small: str, no_blood_flow: str, irregular_solid_tumor: str,
                        ascites: str, papillary_structures: str, irregular_multilocular_large: str,
                        strong_blood_flow: str):
        """Validates input parameters"""
        
        # Define valid options
        valid_options = ["absent", "present"]
        
        # Parameters to validate
        parameters = {
            "unilocular_cyst": unilocular_cyst,
            "solid_components_small": solid_components_small,
            "acoustic_shadows": acoustic_shadows,
            "smooth_multilocular_small": smooth_multilocular_small,
            "no_blood_flow": no_blood_flow,
            "irregular_solid_tumor": irregular_solid_tumor,
            "ascites": ascites,
            "papillary_structures": papillary_structures,
            "irregular_multilocular_large": irregular_multilocular_large,
            "strong_blood_flow": strong_blood_flow
        }
        
        for param_name, param_value in parameters.items():
            if param_value not in valid_options:
                raise ValueError(f"{param_name} must be 'absent' or 'present'")
    
    def _classify_mass(self, parameters: Dict[str, str]) -> str:
        """
        Classifies the mass according to IOTA Simple Rules
        
        IOTA Simple Rules Logic:
        - If B-features present AND no M-features → Benign
        - If M-features present AND no B-features → Malignant  
        - If both B-features and M-features present → Inconclusive
        - If neither B-features nor M-features present → Inconclusive
        
        Args:
            parameters (Dict): Dictionary of ultrasound features
            
        Returns:
            str: Classification (Benign, Malignant, or Inconclusive)
        """
        
        # Check for presence of benign features
        has_b_features = any(parameters[feature] == "present" for feature in self.benign_features)
        
        # Check for presence of malignant features
        has_m_features = any(parameters[feature] == "present" for feature in self.malignant_features)
        
        # Apply IOTA Simple Rules classification logic
        if has_b_features and not has_m_features:
            return "Benign"
        elif has_m_features and not has_b_features:
            return "Malignant"
        else:
            # Both present or neither present = Inconclusive
            return "Inconclusive"
    
    def _get_interpretation(self, classification: str) -> Dict[str, str]:
        """
        Provides clinical interpretation based on IOTA classification
        
        Args:
            classification (str): IOTA classification (Benign, Malignant, Inconclusive)
            
        Returns:
            Dict with interpretation details
        """
        
        if classification == "Benign":
            return {
                "stage": "Benign",
                "description": "One or more B-features present, no M-features",
                "interpretation": "Low risk of malignancy. Mass classified as benign based on IOTA Simple Rules. Consider routine gynecologic follow-up. Surgery may be considered for symptomatic masses or patient preference."
            }
        elif classification == "Malignant":
            return {
                "stage": "Malignant",
                "description": "One or more M-features present, no B-features",
                "interpretation": "High risk of malignancy. Mass classified as malignant based on IOTA Simple Rules. Immediate referral to gynecologic oncology for comprehensive staging and management. Consider tumor markers (CA-125, HE4) and CT/MRI for surgical planning."
            }
        else:  # Inconclusive
            return {
                "stage": "Inconclusive",
                "description": "Both B-features and M-features present, or no features present",
                "interpretation": "Cannot be classified using Simple Rules (10-20% of cases). Consider additional diagnostic methods: subjective assessment by expert sonographer, IOTA ADNEX model, magnetic resonance imaging, or tumor markers. Multidisciplinary team discussion recommended."
            }


def calculate_iota_simple_rules(unilocular_cyst: str, solid_components_small: str, acoustic_shadows: str,
                               smooth_multilocular_small: str, no_blood_flow: str, irregular_solid_tumor: str,
                               ascites: str, papillary_structures: str, irregular_multilocular_large: str,
                               strong_blood_flow: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = IotaSimpleRulesCalculator()
    return calculator.calculate(
        unilocular_cyst, solid_components_small, acoustic_shadows,
        smooth_multilocular_small, no_blood_flow, irregular_solid_tumor,
        ascites, papillary_structures, irregular_multilocular_large, strong_blood_flow
    )