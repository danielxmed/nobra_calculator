"""
Binet Staging System for Chronic Lymphocytic Leukemia (CLL) Calculator

Stages chronic lymphocytic leukemia based on lymphadenopathy areas and hematologic 
parameters to predict prognosis and guide treatment decisions according to the 
European staging system established by Binet et al. in 1981.

References (Vancouver style):
1. Binet JL, Auquier A, Dighiero G, Chastang C, Piguet H, Goasguen J, et al. 
   A new prognostic classification of chronic lymphocytic leukemia derived from 
   a multivariate survival analysis. Cancer. 1981 Jul 1;48(1):198-206.
2. Hallek M, Cheson BD, Catovsky D, Caligaris-Cappio F, Dighiero G, Döhner H, et al. 
   iwCLL guidelines for diagnosis, indications for treatment, response assessment, 
   and supportive management of CLL. Blood. 2018 Jun 21;131(25):2745-2760.
3. Rai KR, Sawitsky A, Cronkite EP, Chanana AD, Levy RN, Pasternack BS. 
   Clinical staging of chronic lymphocytic leukemia. Blood. 1975 Aug;46(2):219-34.
"""

from typing import Dict, Any


class BinetStagingCllCalculator:
    """Calculator for Binet Staging System for Chronic Lymphocytic Leukemia (CLL)"""
    
    def __init__(self):
        # Binet staging thresholds
        self.ANEMIA_THRESHOLD = 10.0  # Hemoglobin <10 g/dL
        self.THROMBOCYTOPENIA_THRESHOLD = 100  # Platelets <100×10³/mm³
        self.LYMPHOID_AREAS_THRESHOLD = 3  # ≥3 areas for Stage B
    
    def calculate(self, cervical_lymphadenopathy: str, axillary_lymphadenopathy: str,
                 inguinal_lymphadenopathy: str, splenomegaly: str, hepatomegaly: str,
                 hemoglobin: float, platelet_count: int) -> Dict[str, Any]:
        """
        Calculates Binet staging for chronic lymphocytic leukemia
        
        Args:
            cervical_lymphadenopathy (str): Enlarged cervical lymph nodes ("yes" or "no")
            axillary_lymphadenopathy (str): Enlarged axillary lymph nodes ("yes" or "no")
            inguinal_lymphadenopathy (str): Enlarged inguinal lymph nodes ("yes" or "no")
            splenomegaly (str): Enlarged spleen ("yes" or "no")
            hepatomegaly (str): Enlarged liver ("yes" or "no")
            hemoglobin (float): Hemoglobin level in g/dL
            platelet_count (int): Platelet count in ×10³/mm³
            
        Returns:
            Dict with Binet stage, prognosis, and clinical interpretation
        """
        
        # Validate inputs
        self._validate_inputs(cervical_lymphadenopathy, axillary_lymphadenopathy,
                            inguinal_lymphadenopathy, splenomegaly, hepatomegaly,
                            hemoglobin, platelet_count)
        
        # Count lymphoid areas involved
        lymphoid_areas_count = self._count_lymphoid_areas(
            cervical_lymphadenopathy, axillary_lymphadenopathy,
            inguinal_lymphadenopathy, splenomegaly, hepatomegaly
        )
        
        # Check for anemia and thrombocytopenia
        has_anemia = hemoglobin < self.ANEMIA_THRESHOLD
        has_thrombocytopenia = platelet_count < self.THROMBOCYTOPENIA_THRESHOLD
        
        # Determine Binet stage
        stage = self._determine_stage(lymphoid_areas_count, has_anemia, has_thrombocytopenia)
        
        # Get interpretation
        interpretation = self._get_interpretation(stage)
        
        return {
            "result": stage,
            "unit": "stage",
            "interpretation": interpretation["interpretation"],
            "stage": stage,
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, cervical_lymphadenopathy, axillary_lymphadenopathy,
                        inguinal_lymphadenopathy, splenomegaly, hepatomegaly,
                        hemoglobin, platelet_count):
        """Validates input parameters"""
        
        # Validate yes/no parameters
        yes_no_params = [
            ("cervical_lymphadenopathy", cervical_lymphadenopathy),
            ("axillary_lymphadenopathy", axillary_lymphadenopathy),
            ("inguinal_lymphadenopathy", inguinal_lymphadenopathy),
            ("splenomegaly", splenomegaly),
            ("hepatomegaly", hepatomegaly)
        ]
        
        for param_name, param_value in yes_no_params:
            if param_value not in ["yes", "no"]:
                raise ValueError(f"{param_name} must be 'yes' or 'no'")
        
        # Validate hemoglobin
        if not isinstance(hemoglobin, (int, float)):
            raise ValueError("hemoglobin must be a number")
        
        if hemoglobin < 3.0 or hemoglobin > 20.0:
            raise ValueError("hemoglobin must be between 3.0 and 20.0 g/dL")
        
        # Validate platelet count
        if not isinstance(platelet_count, int):
            raise ValueError("platelet_count must be an integer")
        
        if platelet_count < 10 or platelet_count > 1000:
            raise ValueError("platelet_count must be between 10 and 1000 ×10³/mm³")
    
    def _count_lymphoid_areas(self, cervical_lymphadenopathy, axillary_lymphadenopathy,
                             inguinal_lymphadenopathy, splenomegaly, hepatomegaly):
        """
        Counts the number of lymphoid areas involved
        
        Returns:
            int: Number of lymphoid areas involved (0-5)
        """
        
        areas = [
            cervical_lymphadenopathy,
            axillary_lymphadenopathy,
            inguinal_lymphadenopathy,
            splenomegaly,
            hepatomegaly
        ]
        
        return sum(1 for area in areas if area == "yes")
    
    def _determine_stage(self, lymphoid_areas_count: int, has_anemia: bool, 
                        has_thrombocytopenia: bool) -> str:
        """
        Determines Binet stage based on lymphoid involvement and hematologic parameters
        
        Args:
            lymphoid_areas_count (int): Number of lymphoid areas involved
            has_anemia (bool): Presence of anemia (Hgb <10 g/dL)
            has_thrombocytopenia (bool): Presence of thrombocytopenia (platelets <100×10³/mm³)
            
        Returns:
            str: Binet stage (Stage A, Stage B, or Stage C)
        """
        
        # Stage C has priority - any anemia or thrombocytopenia
        if has_anemia or has_thrombocytopenia:
            return "Stage C"
        
        # Stage A vs Stage B based on lymphoid areas
        if lymphoid_areas_count < self.LYMPHOID_AREAS_THRESHOLD:
            return "Stage A"
        else:
            return "Stage B"
    
    def _get_interpretation(self, stage: str) -> Dict[str, str]:
        """
        Provides clinical interpretation and management recommendations
        
        Args:
            stage (str): Binet stage
            
        Returns:
            Dict with interpretation and description
        """
        
        interpretations = {
            "Stage A": {
                "description": "Low risk - <3 lymphoid areas involved, normal Hgb and platelets",
                "interpretation": "Low risk CLL with favorable prognosis. Estimated median overall survival: ~12 years. Most patients can be monitored with watchful waiting. Consider treatment only if disease progression or symptoms develop."
            },
            "Stage B": {
                "description": "Intermediate risk - ≥3 lymphoid areas involved, normal Hgb and platelets",
                "interpretation": "Intermediate risk CLL with moderate prognosis. Estimated median overall survival: ~7 years. May require earlier treatment consideration. Monitor closely for disease progression and development of symptoms."
            },
            "Stage C": {
                "description": "High risk - Anemia (Hgb <10 g/dL) and/or thrombocytopenia (platelets <100×10³/mm³)",
                "interpretation": "High risk CLL with poor prognosis. Estimated median overall survival: 2-4 years. Typically requires immediate treatment consideration. Close monitoring and aggressive management indicated."
            }
        }
        
        return interpretations.get(stage, interpretations["Stage A"])


def calculate_binet_staging_cll(cervical_lymphadenopathy: str, axillary_lymphadenopathy: str,
                               inguinal_lymphadenopathy: str, splenomegaly: str, 
                               hepatomegaly: str, hemoglobin: float, 
                               platelet_count: int) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    Calculates Binet staging for chronic lymphocytic leukemia based on lymphoid 
    involvement and hematologic parameters. The Binet system is the European 
    standard for CLL staging, assessing five lymphoid areas (cervical, axillary, 
    inguinal lymph nodes, spleen, and liver) plus anemia and thrombocytopenia.
    """
    calculator = BinetStagingCllCalculator()
    return calculator.calculate(cervical_lymphadenopathy, axillary_lymphadenopathy,
                               inguinal_lymphadenopathy, splenomegaly, hepatomegaly,
                               hemoglobin, platelet_count)