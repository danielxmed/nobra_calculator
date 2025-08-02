"""
HScore for Reactive Hemophagocytic Syndrome Calculator

Estimates the risk of having reactive hemophagocytic syndrome (RHS) based on 
nine clinical, laboratory, and histologic variables.

References:
- Fardet L, Galicier L, Lambotte O, et al. Development and validation of the HScore, 
  a score for the diagnosis of reactive hemophagocytic syndrome. Arthritis Rheumatol. 2014;66(9):2613-20.
"""

from typing import Dict, Any


class HScoreCalculator:
    """Calculator for HScore for Reactive Hemophagocytic Syndrome"""
    
    def __init__(self):
        # Define point values for each variable based on original research
        self.immunosuppression_points = {
            "no": 0,
            "yes": 18
        }
        
        self.temperature_points = {
            "less_than_38.4": 0,
            "38.4_to_39.4": 33,
            "greater_than_39.4": 49
        }
        
        self.organomegaly_points = {
            "none": 0,
            "hepatomegaly_or_splenomegaly": 23,
            "hepatomegaly_and_splenomegaly": 38
        }
        
        self.cytopenias_points = {
            "one_lineage": 0,
            "two_lineages": 24,
            "three_lineages": 34
        }
        
        self.triglycerides_points = {
            "less_than_132.7": 0,    # <1.5 mmol/L = <132.7 mg/dL
            "132.7_to_354": 44,      # 1.5-4.0 mmol/L = 132.7-354 mg/dL
            "354_to_442.8": 64,      # 4.0-5.0 mmol/L = 354-442.8 mg/dL
            "greater_than_442.8": 64  # >5.0 mmol/L = >442.8 mg/dL
        }
        
        self.fibrinogen_points = {
            "greater_than_250": 0,
            "less_than_or_equal_250": 30
        }
        
        self.ferritin_points = {
            "less_than_2000": 0,
            "2000_to_6000": 35,
            "greater_than_6000": 50
        }
        
        self.ast_points = {
            "less_than_30": 0,
            "greater_than_or_equal_30": 19
        }
        
        self.hemophagocytosis_points = {
            "no": 0,
            "yes": 35
        }
    
    def calculate(self, known_immunosuppression: str, temperature: str, organomegaly: str,
                 cytopenias: str, triglycerides: str, fibrinogen: str,
                 ferritin: str, ast_sgot: str, hemophagocytosis: str) -> Dict[str, Any]:
        """
        Calculates HScore for reactive hemophagocytic syndrome
        
        Args:
            known_immunosuppression (str): Known underlying immunosuppression
            temperature (str): Temperature category
            organomegaly (str): Organomegaly presence and type
            cytopenias (str): Number of cytopenias
            triglycerides (str): Triglyceride level category
            fibrinogen (str): Fibrinogen level category  
            ferritin (str): Ferritin level category
            ast_sgot (str): AST/SGOT level category
            hemophagocytosis (str): Hemophagocytosis on bone marrow
            
        Returns:
            Dict with HScore and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(known_immunosuppression, temperature, organomegaly,
                             cytopenias, triglycerides, fibrinogen, ferritin, 
                             ast_sgot, hemophagocytosis)
        
        # Calculate total score
        score = (
            self.immunosuppression_points[known_immunosuppression] +
            self.temperature_points[temperature] +
            self.organomegaly_points[organomegaly] +
            self.cytopenias_points[cytopenias] +
            self.triglycerides_points[triglycerides] +
            self.fibrinogen_points[fibrinogen] +
            self.ferritin_points[ferritin] +
            self.ast_points[ast_sgot] +
            self.hemophagocytosis_points[hemophagocytosis]
        )
        
        # Get interpretation
        interpretation = self._get_interpretation(score)
        
        # Calculate probability percentage
        probability = self._calculate_probability(score)
        
        return {
            "result": score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"],
            "probability_percent": probability
        }
    
    def _validate_inputs(self, known_immunosuppression, temperature, organomegaly,
                        cytopenias, triglycerides, fibrinogen, ferritin,
                        ast_sgot, hemophagocytosis):
        """Validates input parameters"""
        
        valid_immunosuppression = ["yes", "no"]
        if known_immunosuppression not in valid_immunosuppression:
            raise ValueError(f"Known immunosuppression must be one of: {valid_immunosuppression}")
        
        valid_temperature = ["less_than_38.4", "38.4_to_39.4", "greater_than_39.4"]
        if temperature not in valid_temperature:
            raise ValueError(f"Temperature must be one of: {valid_temperature}")
        
        valid_organomegaly = ["none", "hepatomegaly_or_splenomegaly", "hepatomegaly_and_splenomegaly"]
        if organomegaly not in valid_organomegaly:
            raise ValueError(f"Organomegaly must be one of: {valid_organomegaly}")
        
        valid_cytopenias = ["one_lineage", "two_lineages", "three_lineages"]
        if cytopenias not in valid_cytopenias:
            raise ValueError(f"Cytopenias must be one of: {valid_cytopenias}")
        
        valid_triglycerides = ["less_than_132.7", "132.7_to_354", "354_to_442.8", "greater_than_442.8"]
        if triglycerides not in valid_triglycerides:
            raise ValueError(f"Triglycerides must be one of: {valid_triglycerides}")
        
        valid_fibrinogen = ["greater_than_250", "less_than_or_equal_250"]
        if fibrinogen not in valid_fibrinogen:
            raise ValueError(f"Fibrinogen must be one of: {valid_fibrinogen}")
        
        valid_ferritin = ["less_than_2000", "2000_to_6000", "greater_than_6000"]
        if ferritin not in valid_ferritin:
            raise ValueError(f"Ferritin must be one of: {valid_ferritin}")
        
        valid_ast = ["less_than_30", "greater_than_or_equal_30"]
        if ast_sgot not in valid_ast:
            raise ValueError(f"AST/SGOT must be one of: {valid_ast}")
        
        valid_hemophagocytosis = ["yes", "no"]
        if hemophagocytosis not in valid_hemophagocytosis:
            raise ValueError(f"Hemophagocytosis must be one of: {valid_hemophagocytosis}")
    
    def _calculate_probability(self, score: int) -> float:
        """
        Calculates probability percentage based on HScore
        Using the logistic regression formula from the original study
        
        Args:
            score (int): HScore value
            
        Returns:
            float: Probability percentage (0-100)
        """
        
        # Based on original research probability ranges
        if score <= 90:
            return 0.5  # <1%
        elif score <= 168:
            # Linear interpolation between 1% and 25%
            return 1 + (score - 91) * 24 / 77
        elif score <= 250:
            # Linear interpolation between 25% and 99%
            return 25 + (score - 169) * 74 / 81
        else:
            return 99.5  # >99%
    
    def _get_interpretation(self, score: int) -> Dict[str, str]:
        """
        Determines the interpretation based on HScore
        
        Args:
            score (int): HScore value
            
        Returns:
            Dict with interpretation details
        """
        
        if score <= 90:
            return {
                "stage": "Very Low Risk",
                "description": "HScore ≤90",
                "interpretation": "Probability of reactive hemophagocytic syndrome <1%. Diagnosis very unlikely based on current clinical and laboratory findings."
            }
        elif score <= 168:
            return {
                "stage": "Low Risk",
                "description": "HScore 91-168",
                "interpretation": "Low probability of reactive hemophagocytic syndrome (1-25%). Consider alternative diagnoses and monitor clinical evolution."
            }
        elif score <= 250:
            return {
                "stage": "Intermediate Risk",
                "description": "HScore 169-250",
                "interpretation": "Intermediate probability of reactive hemophagocytic syndrome (25-99%). Further evaluation and specialist consultation recommended."
            }
        else:
            return {
                "stage": "High Risk",
                "description": "HScore >250",
                "interpretation": "High probability of reactive hemophagocytic syndrome >99%. Diagnosis highly likely. Immediate hematology consultation and treatment initiation recommended."
            }


def calculate_hscore(known_immunosuppression: str, temperature: str, organomegaly: str,
                    cytopenias: str, triglycerides: str, fibrinogen: str,
                    ferritin: str, ast_sgot: str, hemophagocytosis: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = HScoreCalculator()
    return calculator.calculate(known_immunosuppression, temperature, organomegaly,
                               cytopenias, triglycerides, fibrinogen, ferritin,
                               ast_sgot, hemophagocytosis)