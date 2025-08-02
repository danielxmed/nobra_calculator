"""
Mutation-Enhanced International Prognostic Score System (MIPSS70/MIPSS70+) Calculator

Stratifies risk for patients with overt primary myelofibrosis (PMF) using clinical,
laboratory, and molecular genetic parameters. This enhanced prognostic system 
incorporates high molecular risk mutations to improve risk stratification.

References:
1. Guglielmelli P, Lasho TL, Rotunno G, Mudireddy M, Mannarelli C, Nicolosi M, et al. 
   MIPSS70: Mutation-Enhanced International Prognostic Score System for transplantation-age 
   patients with primary myelofibrosis. J Clin Oncol. 2018;36(4):310-318. 
   doi: 10.1200/JCO.2017.76.4886.
2. Tefferi A, Guglielmelli P, Lasho TL, Rotunno G, Finke C, Mannarelli C, et al. 
   MIPSS70+ Version 2.0: Mutation and Karyotype-Enhanced International Prognostic 
   Scoring System for Primary Myelofibrosis. J Clin Oncol. 2018;36(17):1769-1770. 
   doi: 10.1200/JCO.2018.78.9867.
"""

from typing import Dict, Any, Optional


class Mipss70Calculator:
    """Calculator for MIPSS70/MIPSS70+ Score"""
    
    def __init__(self):
        # Scoring criteria based on published literature
        self.AGE_THRESHOLD = 65  # years
        self.HEMOGLOBIN_THRESHOLD = 10.0  # g/dL
        self.WBC_THRESHOLD = 25.0  # ×10⁹/L
        self.PLATELET_THRESHOLD = 100.0  # ×10⁹/L
        self.BLAST_THRESHOLD = 2.0  # %
    
    def calculate(self, age_years: int, hemoglobin: float, white_blood_count: float,
                 platelet_count: float, circulating_blasts: float, 
                 constitutional_symptoms: str, high_molecular_risk_mutations: str,
                 very_high_molecular_risk: Optional[str] = "unknown") -> Dict[str, Any]:
        """
        Calculates the MIPSS70/MIPSS70+ Score for primary myelofibrosis
        
        Args:
            age_years (int): Patient age in years
            hemoglobin (float): Hemoglobin level in g/dL
            white_blood_count (float): WBC count in ×10⁹/L
            platelet_count (float): Platelet count in ×10⁹/L
            circulating_blasts (float): Percentage of circulating blasts
            constitutional_symptoms (str): Presence of constitutional symptoms ("yes" or "no")
            high_molecular_risk_mutations (str): Presence of high-risk mutations ("yes" or "no")
            very_high_molecular_risk (str): Very high molecular risk for MIPSS70+ ("yes", "no", or "unknown")
            
        Returns:
            Dict with the MIPSS70 score and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(age_years, hemoglobin, white_blood_count, platelet_count,
                            circulating_blasts, constitutional_symptoms, 
                            high_molecular_risk_mutations, very_high_molecular_risk)
        
        # Calculate individual component scores
        score_components = self._calculate_component_scores(
            age_years, hemoglobin, white_blood_count, platelet_count,
            circulating_blasts, constitutional_symptoms, high_molecular_risk_mutations,
            very_high_molecular_risk
        )
        
        # Calculate total score
        total_score = sum(score_components.values())
        
        # Determine if MIPSS70+ version is used
        is_mipss70_plus = very_high_molecular_risk in ["yes", "no"]
        
        # Get interpretation
        interpretation = self._get_interpretation(total_score, is_mipss70_plus)
        
        return {
            "result": total_score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, age_years: int, hemoglobin: float, white_blood_count: float,
                        platelet_count: float, circulating_blasts: float,
                        constitutional_symptoms: str, high_molecular_risk_mutations: str,
                        very_high_molecular_risk: Optional[str]):
        """Validates input parameters"""
        
        if not isinstance(age_years, int) or age_years < 18 or age_years > 120:
            raise ValueError("Age must be an integer between 18 and 120 years")
        
        if not isinstance(hemoglobin, (int, float)) or hemoglobin < 3.0 or hemoglobin > 20.0:
            raise ValueError("Hemoglobin must be between 3.0 and 20.0 g/dL")
        
        if not isinstance(white_blood_count, (int, float)) or white_blood_count < 0.1 or white_blood_count > 500.0:
            raise ValueError("White blood count must be between 0.1 and 500.0 ×10⁹/L")
        
        if not isinstance(platelet_count, (int, float)) or platelet_count < 1.0 or platelet_count > 2000.0:
            raise ValueError("Platelet count must be between 1.0 and 2000.0 ×10⁹/L")
        
        if not isinstance(circulating_blasts, (int, float)) or circulating_blasts < 0.0 or circulating_blasts > 100.0:
            raise ValueError("Circulating blasts must be between 0.0 and 100.0%")
        
        if constitutional_symptoms not in ["yes", "no"]:
            raise ValueError("Constitutional symptoms must be 'yes' or 'no'")
        
        if high_molecular_risk_mutations not in ["yes", "no"]:
            raise ValueError("High molecular risk mutations must be 'yes' or 'no'")
        
        if very_high_molecular_risk is not None and very_high_molecular_risk not in ["yes", "no", "unknown"]:
            raise ValueError("Very high molecular risk must be 'yes', 'no', or 'unknown'")
    
    def _calculate_component_scores(self, age_years: int, hemoglobin: float, 
                                  white_blood_count: float, platelet_count: float,
                                  circulating_blasts: float, constitutional_symptoms: str,
                                  high_molecular_risk_mutations: str, very_high_molecular_risk: Optional[str]) -> Dict[str, int]:
        """Calculates individual component scores"""
        
        scores = {}
        
        # Age score
        scores["age"] = 2 if age_years > self.AGE_THRESHOLD else 0
        
        # Hemoglobin score  
        scores["hemoglobin"] = 1 if hemoglobin < self.HEMOGLOBIN_THRESHOLD else 0
        
        # White blood count score
        scores["wbc"] = 2 if white_blood_count > self.WBC_THRESHOLD else 0
        
        # Platelet count score
        scores["platelets"] = 2 if platelet_count < self.PLATELET_THRESHOLD else 0
        
        # Circulating blasts score
        scores["blasts"] = 1 if circulating_blasts > self.BLAST_THRESHOLD else 0
        
        # Constitutional symptoms score
        scores["symptoms"] = 1 if constitutional_symptoms == "yes" else 0
        
        # High molecular risk mutations score
        scores["high_risk_mutations"] = 1 if high_molecular_risk_mutations == "yes" else 0
        
        # Very high molecular risk score (MIPSS70+ only)
        if very_high_molecular_risk == "yes":
            scores["very_high_risk"] = 1
        else:
            scores["very_high_risk"] = 0
        
        return scores
    
    def _get_interpretation(self, score: int, is_mipss70_plus: bool) -> Dict[str, str]:
        """
        Determines the interpretation based on MIPSS70/MIPSS70+ score
        
        Args:
            score (int): Calculated MIPSS70 score
            is_mipss70_plus (bool): Whether MIPSS70+ version is used
            
        Returns:
            Dict with interpretation details
        """
        
        version = "MIPSS70+" if is_mipss70_plus else "MIPSS70"
        
        if score <= 2:
            return {
                "stage": "Low Risk",
                "description": "Low risk primary myelofibrosis",
                "interpretation": f"LOW RISK PRIMARY MYELOFIBROSIS ({version} Score: {score}): Excellent prognosis with "
                                "median survival exceeding 20 years. MANAGEMENT: Standard monitoring with regular clinical "
                                "assessments every 3-6 months. Supportive care for symptom management as needed. "
                                "TREATMENT: Consider observation or clinical trial participation. JAK inhibitors only if "
                                "symptomatic splenomegaly or constitutional symptoms develop. TRANSPLANT: Allogeneic stem "
                                "cell transplantation not indicated due to excellent prognosis. MONITORING: Regular "
                                "complete blood counts, assessment for disease progression, and quality of life evaluation."
            }
        elif score <= 4:
            return {
                "stage": "Intermediate-1 Risk",
                "description": "Intermediate-1 risk primary myelofibrosis",
                "interpretation": f"INTERMEDIATE-1 RISK PRIMARY MYELOFIBROSIS ({version} Score: {score}): Good prognosis "
                                "with median survival 8-20 years. MANAGEMENT: Regular monitoring every 2-4 months with "
                                "symptom assessment and laboratory evaluation. TREATMENT: Consider JAK inhibitor therapy "
                                "for symptomatic disease (splenomegaly, constitutional symptoms). Supportive care for "
                                "anemia and other complications. TRANSPLANT: Allogeneic transplantation generally not "
                                "recommended unless disease progression or development of high-risk features. "
                                "MONITORING: Watch for signs of progression to higher risk category and assess treatment response."
            }
        elif score <= 6:
            return {
                "stage": "Intermediate-2 Risk",
                "description": "Intermediate-2 risk primary myelofibrosis",
                "interpretation": f"INTERMEDIATE-2 RISK PRIMARY MYELOFIBROSIS ({version} Score: {score}): Intermediate "
                                "prognosis with median survival 4-8 years. MANAGEMENT: Close monitoring every 1-3 months "
                                "with comprehensive assessment. TREATMENT: JAK inhibitor therapy for symptom control and "
                                "potential survival benefit. Aggressive supportive care for cytopenias and complications. "
                                "TRANSPLANT: Consider allogeneic stem cell transplantation evaluation if appropriate "
                                "candidate (age, performance status, comorbidities). Timing of transplant referral critical. "
                                "MONITORING: Regular assessment for disease progression and transplant eligibility."
            }
        else:  # score >= 7
            return {
                "stage": "High Risk",
                "description": "High risk primary myelofibrosis",
                "interpretation": f"HIGH RISK PRIMARY MYELOFIBROSIS ({version} Score: {score}): Poor prognosis with "
                                "median survival less than 4 years. MANAGEMENT: Intensive monitoring and aggressive "
                                "treatment approach. TREATMENT: JAK inhibitor therapy for symptom palliation. "
                                "Aggressive supportive care including transfusion support, infection prophylaxis, "
                                "and management of complications. TRANSPLANT: Prioritize urgent allogeneic stem cell "
                                "transplantation evaluation and referral to transplant center. Consider experimental "
                                "therapies and clinical trial participation. PROGNOSIS: Poor survival outcomes requiring "
                                "intensive multidisciplinary care and early transplant consideration."
            }


def calculate_mipss70(age_years: int, hemoglobin: float, white_blood_count: float,
                     platelet_count: float, circulating_blasts: float,
                     constitutional_symptoms: str, high_molecular_risk_mutations: str,
                     very_high_molecular_risk: Optional[str] = "unknown") -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = Mipss70Calculator()
    return calculator.calculate(age_years, hemoglobin, white_blood_count, platelet_count,
                               circulating_blasts, constitutional_symptoms, 
                               high_molecular_risk_mutations, very_high_molecular_risk)