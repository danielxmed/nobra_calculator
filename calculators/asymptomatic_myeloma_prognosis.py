"""
Asymptomatic Myeloma Prognosis Calculator

Predicts risk of progression of asymptomatic (smoldering) multiple myeloma to active myeloma or amyloidosis.

References (Vancouver style):
1. Kyle RA, Remstein ED, Therneau TM, Dispenzieri A, Kurtin PJ, Hodnefield JM, et al. 
   Clinical course and prognosis of smoldering (asymptomatic) multiple myeloma. 
   N Engl J Med. 2007;356(25):2582-90.
2. Rajkumar SV, Landgren O, Mateos MV. Smoldering multiple myeloma. Blood. 2015;125(20):3069-75.
3. Mateos MV, Kumar S, Dimopoulos MA, González-Calle V, Kastritis E, Hajek R, et al. 
   International Myeloma Working Group risk stratification model for smoldering multiple myeloma (SMM). 
   Blood Cancer J. 2020;10(10):102.

The Asymptomatic Myeloma Prognosis score stratifies patients with smoldering multiple myeloma 
into risk groups based on bone marrow plasmacytosis percentage and serum monoclonal protein level. 
This helps identify patients who would benefit from closer monitoring or early intervention.
"""

from typing import Dict, Any


class AsymptomaticMyelomaPrognosisCalculator:
    """Calculator for Asymptomatic Myeloma Prognosis"""
    
    def __init__(self):
        # Risk groups and their characteristics
        self.RISK_GROUPS = {
            "Low Risk": {
                "description": "Both bone marrow plasmacytosis <10% and serum M-protein <3 g/dL",
                "interpretation": "Lowest risk of progression to symptomatic multiple myeloma. Median time to progression approximately 117 months. Annual risk of progression approximately 2-3%.",
                "median_ttp_months": 117,
                "annual_risk_percent": "2-3%"
            },
            "Intermediate Risk": {
                "description": "Either bone marrow plasmacytosis ≥10% OR serum M-protein ≥3 g/dL (but not both)",
                "interpretation": "Intermediate risk of progression to symptomatic multiple myeloma. Median time to progression approximately 60-75 months. Annual risk of progression approximately 5-7%.",
                "median_ttp_months": "60-75",
                "annual_risk_percent": "5-7%"
            },
            "High Risk": {
                "description": "Both bone marrow plasmacytosis ≥10% AND serum M-protein ≥3 g/dL",
                "interpretation": "Highest risk of progression to symptomatic multiple myeloma. Median time to progression approximately 26-27 months. Annual risk of progression approximately 15-20%.",
                "median_ttp_months": "26-27",
                "annual_risk_percent": "15-20%"
            }
        }
    
    def calculate(self, bone_marrow_plasmacytosis: str, serum_monoclonal_protein: str) -> Dict[str, Any]:
        """
        Calculates the Asymptomatic Myeloma Prognosis risk group
        
        Args:
            bone_marrow_plasmacytosis (str): Bone marrow plasmacytosis percentage ("≥10%" or "<10%")
            serum_monoclonal_protein (str): Serum monoclonal protein level ("≥3" or "<3")
            
        Returns:
            Dict with risk group and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(bone_marrow_plasmacytosis, serum_monoclonal_protein)
        
        # Determine risk factors
        high_plasmacytosis = bone_marrow_plasmacytosis == "≥10%"
        high_m_protein = serum_monoclonal_protein == "≥3"
        
        # Calculate risk group
        risk_group = self._determine_risk_group(high_plasmacytosis, high_m_protein)
        
        # Get interpretation
        risk_info = self.RISK_GROUPS[risk_group]
        
        return {
            "result": risk_group,
            "unit": "",
            "interpretation": risk_info["interpretation"],
            "stage": risk_group,
            "stage_description": risk_info["description"]
        }
    
    def _validate_inputs(self, bone_marrow_plasmacytosis: str, serum_monoclonal_protein: str):
        """Validates input parameters"""
        
        # Validate bone marrow plasmacytosis
        valid_plasmacytosis = ["≥10%", "<10%"]
        if bone_marrow_plasmacytosis not in valid_plasmacytosis:
            raise ValueError(f"Bone marrow plasmacytosis must be one of: {valid_plasmacytosis}")
        
        # Validate serum monoclonal protein
        valid_m_protein = ["≥3", "<3"]
        if serum_monoclonal_protein not in valid_m_protein:
            raise ValueError(f"Serum monoclonal protein must be one of: {valid_m_protein}")
    
    def _determine_risk_group(self, high_plasmacytosis: bool, high_m_protein: bool) -> str:
        """
        Determines the risk group based on risk factors
        
        Args:
            high_plasmacytosis (bool): True if bone marrow plasmacytosis ≥10%
            high_m_protein (bool): True if serum M-protein ≥3 g/dL
            
        Returns:
            str: Risk group classification
        """
        
        # Count number of risk factors present
        risk_factors = sum([high_plasmacytosis, high_m_protein])
        
        if risk_factors == 0:
            # Both factors are low risk
            return "Low Risk"
        elif risk_factors == 1:
            # Only one factor is present
            return "Intermediate Risk"
        else:
            # Both factors are present (risk_factors == 2)
            return "High Risk"


def calculate_asymptomatic_myeloma_prognosis(bone_marrow_plasmacytosis: str, serum_monoclonal_protein: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    Args:
        bone_marrow_plasmacytosis (str): Bone marrow plasmacytosis percentage ("≥10%" or "<10%")
        serum_monoclonal_protein (str): Serum monoclonal protein level ("≥3" or "<3")
        
    Returns:
        Dict with risk group and interpretation
    """
    calculator = AsymptomaticMyelomaPrognosisCalculator()
    return calculator.calculate(bone_marrow_plasmacytosis, serum_monoclonal_protein)
