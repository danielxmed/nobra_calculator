"""
Fong Clinical Risk Score for Colorectal Cancer Recurrence Calculator

Predicts recurrence and survival risk for colorectal cancer patients with liver metastases 
after hepatic resection. Uses five clinical criteria to stratify patients into risk groups.

References:
1. Fong Y, Fortner J, Sun RL, Brennan MF, Blumgart LH. Clinical score for predicting recurrence 
   after hepatic resection for metastatic colorectal cancer: analysis of 1001 consecutive cases. 
   Ann Surg. 1999;230(3):309-318.
2. Mala T, Bohler G, Mathisen O, Bergan A, Soreide O. Hepatic resection for colorectal metastases: 
   can preoperative scoring predict patient outcome? World J Surg. 2002;26(11):1348-1353.
3. Mann CD, Metcalfe MS, Leopardi LN, Maddern GJ. The clinical risk score: emerging as a reliable 
   preoperative prognostic index in hepatectomy for colorectal metastases. Arch Surg. 2004;139(11):1168-1172.
"""

from typing import Dict, Any


class FongClinicalRiskScoreCalculator:
    """Calculator for Fong Clinical Risk Score"""
    
    def __init__(self):
        # Survival rates by score (approximate values from original study)
        self.SURVIVAL_RATES = {
            0: 60,  # 5-year survival rate %
            1: 44,
            2: 30,
            3: 16,
            4: 11,
            5: 14
        }
        
        # Risk stratification thresholds
        self.LOW_RISK_THRESHOLD = 2  # Scores 0-2 considered favorable
        self.HIGH_RISK_THRESHOLD = 3  # Scores 3+ considered for adjuvant therapy
    
    def calculate(self, node_positive_primary: str, disease_free_interval: str, 
                  number_of_tumors: str, cea_level: str, largest_tumor_size: str) -> Dict[str, Any]:
        """
        Calculates the Fong Clinical Risk Score
        
        Args:
            node_positive_primary (str): "yes" or "no" for lymph node involvement
            disease_free_interval (str): "less_than_12_months" or "12_months_or_more"
            number_of_tumors (str): "single" or "multiple"
            cea_level (str): "200_or_less" or "greater_than_200"
            largest_tumor_size (str): "5_cm_or_less" or "greater_than_5_cm"
            
        Returns:
            Dict with the score, interpretation, and survival estimates
        """
        
        # Validations
        self._validate_inputs(node_positive_primary, disease_free_interval, number_of_tumors, 
                            cea_level, largest_tumor_size)
        
        # Calculate score
        score = self._calculate_score(node_positive_primary, disease_free_interval, number_of_tumors, 
                                    cea_level, largest_tumor_size)
        
        # Get interpretation
        interpretation_data = self._get_interpretation(score)
        
        return {
            "result": score,
            "unit": "points",
            "interpretation": interpretation_data["interpretation"],
            "stage": interpretation_data["stage"],
            "stage_description": interpretation_data["description"]
        }
    
    def _validate_inputs(self, node_positive_primary: str, disease_free_interval: str, 
                        number_of_tumors: str, cea_level: str, largest_tumor_size: str):
        """Validates input parameters"""
        
        # Validate node_positive_primary
        if node_positive_primary not in ["yes", "no"]:
            raise ValueError("Node positive primary must be 'yes' or 'no'")
        
        # Validate disease_free_interval
        if disease_free_interval not in ["less_than_12_months", "12_months_or_more"]:
            raise ValueError("Disease free interval must be 'less_than_12_months' or '12_months_or_more'")
        
        # Validate number_of_tumors
        if number_of_tumors not in ["single", "multiple"]:
            raise ValueError("Number of tumors must be 'single' or 'multiple'")
        
        # Validate cea_level
        if cea_level not in ["200_or_less", "greater_than_200"]:
            raise ValueError("CEA level must be '200_or_less' or 'greater_than_200'")
        
        # Validate largest_tumor_size
        if largest_tumor_size not in ["5_cm_or_less", "greater_than_5_cm"]:
            raise ValueError("Largest tumor size must be '5_cm_or_less' or 'greater_than_5_cm'")
    
    def _calculate_score(self, node_positive_primary: str, disease_free_interval: str, 
                        number_of_tumors: str, cea_level: str, largest_tumor_size: str) -> int:
        """Calculates the Fong Clinical Risk Score"""
        
        score = 0
        
        # 1 point for node-positive primary tumor
        if node_positive_primary == "yes":
            score += 1
        
        # 1 point for disease-free interval < 12 months
        if disease_free_interval == "less_than_12_months":
            score += 1
        
        # 1 point for multiple tumors
        if number_of_tumors == "multiple":
            score += 1
        
        # 1 point for CEA > 200 ng/mL
        if cea_level == "greater_than_200":
            score += 1
        
        # 1 point for largest tumor > 5 cm
        if largest_tumor_size == "greater_than_5_cm":
            score += 1
        
        return score
    
    def _get_interpretation(self, score: int) -> Dict[str, str]:
        """
        Determines the interpretation based on the score
        
        Args:
            score (int): Calculated Fong score (0-5)
            
        Returns:
            Dict with interpretation details
        """
        
        survival_rate = self.SURVIVAL_RATES.get(score, 0)
        
        if score == 0:
            return {
                "stage": "Score 0",
                "description": "Excellent prognosis",
                "interpretation": (f"5-year survival rate approximately {survival_rate}%. "
                                f"Lowest risk group with best prognosis after hepatic resection. "
                                f"Excellent candidate for liver resection with favorable long-term outcome.")
            }
        
        elif score == 1:
            return {
                "stage": "Score 1", 
                "description": "Good prognosis",
                "interpretation": (f"5-year survival rate approximately {survival_rate}%. "
                                f"Favorable outcome expected after hepatic resection. "
                                f"Good candidate for surgical intervention with acceptable long-term survival.")
            }
        
        elif score == 2:
            return {
                "stage": "Score 2",
                "description": "Moderate prognosis", 
                "interpretation": (f"5-year survival rate approximately {survival_rate}%. "
                                f"Acceptable outcome with potential benefit from hepatic resection. "
                                f"Still within favorable risk group (score ≤2) for surgical intervention.")
            }
        
        elif score == 3:
            return {
                "stage": "Score 3",
                "description": "Poor prognosis",
                "interpretation": (f"5-year survival rate approximately {survival_rate}%. "
                                f"Consider experimental adjuvant therapy or alternative treatment strategies. "
                                f"High-risk group requiring careful consideration of treatment options.")
            }
        
        elif score == 4:
            return {
                "stage": "Score 4",
                "description": "Very poor prognosis",
                "interpretation": (f"5-year survival rate approximately {survival_rate}%. "
                                f"Strong consideration for experimental adjuvant therapy or systemic treatment. "
                                f"Very high-risk group with limited benefit from resection alone.")
            }
        
        else:  # score == 5
            return {
                "stage": "Score 5",
                "description": "Extremely poor prognosis",
                "interpretation": (f"5-year survival rate approximately {survival_rate}%. "
                                f"Highest risk group requiring aggressive adjuvant therapy consideration. "
                                f"Multimodal treatment approach recommended over resection alone.")
            }


def calculate_fong_clinical_risk_score(node_positive_primary: str, disease_free_interval: str, 
                                     number_of_tumors: str, cea_level: str, 
                                     largest_tumor_size: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_fong_clinical_risk_score pattern
    """
    calculator = FongClinicalRiskScoreCalculator()
    return calculator.calculate(node_positive_primary, disease_free_interval, number_of_tumors, 
                              cea_level, largest_tumor_size)