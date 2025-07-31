"""
GIPSS - Genetically Inspired Prognostic Scoring System for Primary Myelofibrosis Calculator

The GIPSS is a genetically-based prognostic scoring system for primary myelofibrosis that 
relies exclusively on cytogenetic and molecular genetic markers. This system eliminates 
subjective clinical variables and provides more accurate risk stratification for treatment 
planning, particularly for allogeneic stem cell transplant decisions.

References (Vancouver style):
1. Tefferi A, Guglielmelli P, Nicolosi M, et al. GIPSS: genetically inspired prognostic scoring 
   system for primary myelofibrosis. Leukemia. 2018;32(7):1631-1642. doi: 10.1038/s41375-018-0107-z.
2. Passamonti F, Giorgino T, Mora B, et al. A clinical-molecular prognostic model to predict 
   survival in patients with post polycythemia vera and post essential thrombocythemia myelofibrosis. 
   Leukemia. 2017;31(12):2726-2731. doi: 10.1038/leu.2017.169.
3. Guglielmelli P, Lasho TL, Rotunno G, et al. MIPSS70: Mutation-Enhanced International Prognostic 
   Score System for transplantation-age patients with primary myelofibrosis. J Clin Oncol. 
   2018;36(4):310-318. doi: 10.1200/JCO.2017.76.4886.
"""

from typing import Dict, Any


class GipssPrimaryMyelofibrosisCalculator:
    """Calculator for GIPSS - Genetically Inspired Prognostic Scoring System for Primary Myelofibrosis"""
    
    def __init__(self):
        # Karyotype risk point mapping
        self.KARYOTYPE_POINTS = {
            'favorable': 0,
            'unfavorable': 1,
            'very_high_risk': 2
        }
        
        # Survival data by GIPSS score
        self.SURVIVAL_DATA = {
            0: {
                'risk_category': 'Low Risk',
                'median_survival_years': 26.4,
                'five_year_survival_percent': 94
            },
            1: {
                'risk_category': 'Intermediate-1 Risk', 
                'median_survival_years': 8.0,
                'five_year_survival_percent': 73
            },
            2: {
                'risk_category': 'Intermediate-2 Risk',
                'median_survival_years': 4.2,
                'five_year_survival_percent': 40
            },
            3: {
                'risk_category': 'High Risk',
                'median_survival_years': 2.0,
                'five_year_survival_percent': 14
            },
            4: {
                'risk_category': 'High Risk',
                'median_survival_years': 2.0,
                'five_year_survival_percent': 14
            },
            5: {
                'risk_category': 'High Risk',
                'median_survival_years': 2.0,
                'five_year_survival_percent': 14
            },
            6: {
                'risk_category': 'High Risk',
                'median_survival_years': 2.0,
                'five_year_survival_percent': 14
            }
        }
    
    def calculate(self, karyotype_risk: str, calr_type1_mutation: str, asxl1_mutation: str,
                 srsf2_mutation: str, u2af1q157_mutation: str) -> Dict[str, Any]:
        """
        Calculates GIPSS score using provided genetic parameters
        
        Args:
            karyotype_risk (str): Cytogenetic risk classification
            calr_type1_mutation (str): Presence of type 1/like CALR mutation
            asxl1_mutation (str): Presence of ASXL1 mutation
            srsf2_mutation (str): Presence of SRSF2 mutation
            u2af1q157_mutation (str): Presence of U2AF1Q157 mutation
            
        Returns:
            Dict with the result and clinical interpretation
        """
        
        # Validate inputs
        self._validate_inputs(karyotype_risk, calr_type1_mutation, asxl1_mutation,
                             srsf2_mutation, u2af1q157_mutation)
        
        # Calculate GIPSS score
        gipss_score = self._calculate_gipss_score(karyotype_risk, calr_type1_mutation, 
                                                 asxl1_mutation, srsf2_mutation, 
                                                 u2af1q157_mutation)
        
        # Get survival data
        survival_data = self.SURVIVAL_DATA[min(gipss_score, 6)]  # Cap at score 6 for lookup
        
        # Get clinical interpretation
        interpretation = self._get_interpretation(gipss_score, survival_data, karyotype_risk,
                                                calr_type1_mutation, asxl1_mutation, 
                                                srsf2_mutation, u2af1q157_mutation)
        
        return {
            "result": gipss_score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"],
            "median_survival_years": survival_data["median_survival_years"],
            "five_year_survival_percent": survival_data["five_year_survival_percent"],
            "karyotype_points": self.KARYOTYPE_POINTS[karyotype_risk],
            "calr_points": 0 if calr_type1_mutation == 'yes' else 1,
            "asxl1_points": 1 if asxl1_mutation == 'yes' else 0,
            "srsf2_points": 1 if srsf2_mutation == 'yes' else 0,
            "u2af1q157_points": 1 if u2af1q157_mutation == 'yes' else 0
        }
    
    def _validate_inputs(self, karyotype_risk, calr_type1_mutation, asxl1_mutation,
                        srsf2_mutation, u2af1q157_mutation):
        """Validates input parameters"""
        
        if karyotype_risk not in self.KARYOTYPE_POINTS:
            raise ValueError("Karyotype risk must be 'favorable', 'unfavorable', or 'very_high_risk'")
        
        yes_no_params = [
            ("calr_type1_mutation", calr_type1_mutation),
            ("asxl1_mutation", asxl1_mutation),
            ("srsf2_mutation", srsf2_mutation),
            ("u2af1q157_mutation", u2af1q157_mutation)
        ]
        
        for param_name, param_value in yes_no_params:
            if param_value not in ["yes", "no"]:
                raise ValueError(f"{param_name} must be 'yes' or 'no'")
    
    def _calculate_gipss_score(self, karyotype_risk, calr_type1_mutation, asxl1_mutation,
                              srsf2_mutation, u2af1q157_mutation):
        """Calculates the GIPSS total score"""
        
        score = 0
        
        # Karyotype risk points
        score += self.KARYOTYPE_POINTS[karyotype_risk]
        
        # CALR type 1 mutation (absence adds 1 point)
        if calr_type1_mutation == 'no':
            score += 1
        
        # High molecular risk mutations (presence adds 1 point each)
        if asxl1_mutation == 'yes':
            score += 1
        
        if srsf2_mutation == 'yes':
            score += 1
            
        if u2af1q157_mutation == 'yes':
            score += 1
        
        return score
    
    def _get_interpretation(self, gipss_score: int, survival_data: Dict, karyotype_risk: str,
                           calr_type1_mutation: str, asxl1_mutation: str, srsf2_mutation: str,
                           u2af1q157_mutation: str) -> Dict[str, str]:
        """
        Determines clinical interpretation based on GIPSS score
        
        Args:
            gipss_score (int): Calculated GIPSS score
            survival_data (Dict): Survival data for the score
            Other parameters for detailed interpretation
            
        Returns:
            Dict with interpretation
        """
        
        # Build genetic profile summary
        genetic_factors = []
        
        if karyotype_risk == 'very_high_risk':
            genetic_factors.append("very high-risk karyotype")
        elif karyotype_risk == 'unfavorable':
            genetic_factors.append("unfavorable karyotype")
        else:
            genetic_factors.append("favorable karyotype")
        
        if calr_type1_mutation == 'no':
            genetic_factors.append("absence of type 1/like CALR mutation")
        else:
            genetic_factors.append("presence of type 1/like CALR mutation")
        
        high_risk_mutations = []
        if asxl1_mutation == 'yes':
            high_risk_mutations.append("ASXL1")
        if srsf2_mutation == 'yes':
            high_risk_mutations.append("SRSF2")
        if u2af1q157_mutation == 'yes':
            high_risk_mutations.append("U2AF1Q157")
        
        if high_risk_mutations:
            genetic_factors.append(f"presence of {', '.join(high_risk_mutations)} mutation(s)")
        else:
            genetic_factors.append("absence of high molecular risk mutations")
        
        genetic_summary = "; ".join(genetic_factors)
        
        # Base interpretation with score and genetic factors
        base_interpretation = (
            f"GIPSS score of {gipss_score} points based on: {genetic_summary}. "
            f"Risk category: {survival_data['risk_category']}. "
            f"Median overall survival: {survival_data['median_survival_years']} years. "
            f"5-year survival: {survival_data['five_year_survival_percent']}%. "
        )
        
        # Score-specific management recommendations
        if gipss_score == 0:
            return {
                "stage": "Low Risk",
                "description": "Excellent prognosis",
                "interpretation": base_interpretation +
                    "Excellent long-term prognosis with minimal therapeutic intervention indicated. "
                    "Consider long-term observation with regular monitoring every 6-12 months. "
                    "Focus on symptom management and quality of life. Allogeneic stem cell transplant "
                    "not typically indicated. Monitor for disease progression or transformation."
            }
        elif gipss_score == 1:
            return {
                "stage": "Intermediate-1 Risk",
                "description": "Good prognosis", 
                "interpretation": base_interpretation +
                    "Good prognosis with symptom-directed therapy approach. Regular monitoring "
                    "every 3-6 months recommended. Consider JAK inhibitor therapy for symptomatic "
                    "disease or splenomegaly. Allogeneic transplant generally not indicated unless "
                    "disease progression occurs. Focus on maintaining quality of life and functional status."
            }
        elif gipss_score == 2:
            return {
                "stage": "Intermediate-2 Risk",
                "description": "Intermediate prognosis",
                "interpretation": base_interpretation +
                    "Intermediate prognosis requiring active treatment consideration. Evaluate for "
                    "allogeneic stem cell transplant candidacy in appropriate patients. Consider "
                    "JAK inhibitor therapy for symptom control. Regular monitoring every 2-3 months. "
                    "Discuss treatment goals and preferences with patient and family. Assess comorbidities "
                    "and transplant eligibility if age and performance status appropriate."
            }
        else:  # Score 3-6 (High Risk)
            return {
                "stage": "High Risk",
                "description": "Poor prognosis",
                "interpretation": base_interpretation +
                    "Poor prognosis with strong consideration for allogeneic stem cell transplant "
                    "if patient is eligible. Urgent hematology/oncology referral for transplant "
                    "evaluation. Aggressive supportive care and symptom management. Consider clinical "
                    "trial participation. Regular monitoring every 1-2 months. Discuss prognosis "
                    "and treatment options with patient and family. Focus on symptom control and "
                    "quality of life while pursuing curative options."
            }


def calculate_gipss_primary_myelofibrosis(karyotype_risk: str, calr_type1_mutation: str, 
                                         asxl1_mutation: str, srsf2_mutation: str, 
                                         u2af1q157_mutation: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_gipss_primary_myelofibrosis pattern
    """
    calculator = GipssPrimaryMyelofibrosisCalculator()
    return calculator.calculate(karyotype_risk, calr_type1_mutation, asxl1_mutation,
                               srsf2_mutation, u2af1q157_mutation)