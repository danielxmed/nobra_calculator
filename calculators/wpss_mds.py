"""
WPSS (WHO classification-based Prognostic Scoring System) for Myelodysplastic Syndrome Calculator

Time-dependent prognostic scoring system for predicting survival and leukemic evolution 
in myelodysplastic syndromes based on WHO morphological classification.

References:
1. Malcovati L, Germing U, Kuendgen A, et al. Time-dependent prognostic scoring system 
   for predicting survival and leukemic evolution in myelodysplastic syndromes. 
   J Clin Oncol. 2007;25(23):3503-3510. doi: 10.1200/JCO.2006.08.5696
2. Malcovati L, Della Porta MG, Strupp C, et al. Impact of the degree of anemia on the 
   outcome of patients with myelodysplastic syndrome and its integration into the WHO 
   classification-based Prognostic Scoring System (WPSS). Haematologica. 2011;96(10):1433-1440.
"""

from typing import Dict, Any


class WpssMdsCalculator:
    """Calculator for WPSS (WHO classification-based Prognostic Scoring System) for MDS"""
    
    def __init__(self):
        # WPSS scoring system
        self.WHO_CATEGORY_SCORES = {
            "ra_rars_del5q": 0,  # RA, RARS, or MDS with isolated del(5q)
            "rcmd_rcmd_rs": 1,   # RCMD or RCMD-RS
            "raeb_1": 2,         # RAEB-1 (2-4% blasts)
            "raeb_2": 3          # RAEB-2 (5-19% blasts)
        }
        
        self.KARYOTYPE_SCORES = {
            "good": 0,        # Normal, -Y, del(5q), del(20q)
            "intermediate": 1, # All other abnormalities
            "poor": 2         # Complex ≥3 abnormalities, chromosome 7 anomalies
        }
        
        self.TRANSFUSION_SCORES = {
            "none": 0,      # No regular transfusion requirement
            "regular": 1    # ≥1 RBC transfusion every 8 weeks over 4 months
        }
        
        # Risk categories with median survival (months)
        self.RISK_CATEGORIES = {
            0: {
                "risk": "Very Low Risk",
                "description": "Excellent prognosis",
                "median_survival_months": 141,
                "median_survival_years": 11.8
            },
            1: {
                "risk": "Low Risk", 
                "description": "Good prognosis",
                "median_survival_months": 66,
                "median_survival_years": 5.5
            },
            2: {
                "risk": "Intermediate Risk",
                "description": "Moderate prognosis", 
                "median_survival_months": 48,
                "median_survival_years": 4.0
            },
            3: {
                "risk": "High Risk",
                "description": "Poor prognosis",
                "median_survival_months": 26,
                "median_survival_years": 2.2
            },
            4: {
                "risk": "High Risk",
                "description": "Poor prognosis",
                "median_survival_months": 26,
                "median_survival_years": 2.2
            },
            5: {
                "risk": "Very High Risk",
                "description": "Very poor prognosis",
                "median_survival_months": 9,
                "median_survival_years": 0.8
            },
            6: {
                "risk": "Very High Risk",
                "description": "Very poor prognosis",
                "median_survival_months": 9,
                "median_survival_years": 0.8
            }
        }
    
    def calculate(self, who_category: str, karyotype: str, transfusion_requirement: str) -> Dict[str, Any]:
        """
        Calculates WPSS score for myelodysplastic syndrome prognosis
        
        Args:
            who_category (str): WHO morphological classification
            karyotype (str): Cytogenetic risk category
            transfusion_requirement (str): Regular transfusion requirement
            
        Returns:
            Dict with WPSS score, risk category, and prognostic information
        """
        
        # Validate inputs
        self._validate_inputs(who_category, karyotype, transfusion_requirement)
        
        # Calculate component scores
        who_score = self.WHO_CATEGORY_SCORES[who_category]
        karyotype_score = self.KARYOTYPE_SCORES[karyotype]
        transfusion_score = self.TRANSFUSION_SCORES[transfusion_requirement]
        
        # Calculate total WPSS score
        total_score = who_score + karyotype_score + transfusion_score
        
        # Get risk category information
        risk_info = self.RISK_CATEGORIES[total_score]
        
        # Generate interpretation
        interpretation = self._generate_interpretation(total_score, risk_info, who_category, karyotype, transfusion_requirement)
        
        return {
            "result": total_score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": risk_info["risk"],
            "stage_description": risk_info["description"],
            "median_survival_months": risk_info["median_survival_months"],
            "median_survival_years": risk_info["median_survival_years"],
            "component_scores": {
                "who_category_score": who_score,
                "karyotype_score": karyotype_score,
                "transfusion_score": transfusion_score
            },
            "risk_assessment": interpretation["risk_assessment"],
            "clinical_recommendations": interpretation["clinical_recommendations"]
        }
    
    def _validate_inputs(self, who_category: str, karyotype: str, transfusion_requirement: str):
        """Validates input parameters"""
        
        if who_category not in self.WHO_CATEGORY_SCORES:
            raise ValueError(f"WHO category must be one of: {list(self.WHO_CATEGORY_SCORES.keys())}")
        
        if karyotype not in self.KARYOTYPE_SCORES:
            raise ValueError(f"Karyotype must be one of: {list(self.KARYOTYPE_SCORES.keys())}")
        
        if transfusion_requirement not in self.TRANSFUSION_SCORES:
            raise ValueError(f"Transfusion requirement must be one of: {list(self.TRANSFUSION_SCORES.keys())}")
    
    def _generate_interpretation(self, total_score: int, risk_info: Dict[str, Any], 
                               who_category: str, karyotype: str, transfusion_requirement: str) -> Dict[str, Any]:
        """Generates clinical interpretation and recommendations"""
        
        # Base interpretation
        interpretation = (f"WPSS score {total_score} points indicates {risk_info['risk']} myelodysplastic syndrome "
                         f"with median overall survival of {risk_info['median_survival_months']} months "
                         f"({risk_info['median_survival_years']} years). {risk_info['description']}.")
        
        # Risk assessment details
        risk_assessment = self._generate_risk_assessment(total_score, risk_info)
        
        # Clinical recommendations
        clinical_recommendations = self._generate_clinical_recommendations(total_score, who_category, karyotype, transfusion_requirement)
        
        return {
            "interpretation": interpretation,
            "risk_assessment": risk_assessment,
            "clinical_recommendations": clinical_recommendations
        }
    
    def _generate_risk_assessment(self, total_score: int, risk_info: Dict[str, Any]) -> Dict[str, Any]:
        """Generates detailed risk assessment"""
        
        if total_score == 0:
            leukemic_transformation = "Very low probability of leukemic transformation"
            management_urgency = "Routine monitoring appropriate"
        elif total_score == 1:
            leukemic_transformation = "Low probability of leukemic transformation"
            management_urgency = "Regular monitoring with supportive care"
        elif total_score == 2:
            leukemic_transformation = "Moderate probability of leukemic transformation"
            management_urgency = "Close monitoring, consider therapeutic intervention"
        elif total_score in [3, 4]:
            leukemic_transformation = "High probability of leukemic transformation"
            management_urgency = "Consider intensive treatment strategies"
        else:  # score 5-6
            leukemic_transformation = "Very high probability of leukemic transformation"
            management_urgency = "Urgent consideration for intensive treatment"
        
        return {
            "risk_category": risk_info["risk"],
            "median_survival": f"{risk_info['median_survival_months']} months ({risk_info['median_survival_years']} years)",
            "leukemic_transformation_risk": leukemic_transformation,
            "management_urgency": management_urgency,
            "prognosis": risk_info["description"]
        }
    
    def _generate_clinical_recommendations(self, total_score: int, who_category: str, 
                                         karyotype: str, transfusion_requirement: str) -> Dict[str, Any]:
        """Generates clinical management recommendations"""
        
        recommendations = []
        monitoring = []
        treatment_considerations = []
        
        # Risk-based recommendations
        if total_score <= 1:  # Very Low/Low Risk
            recommendations.extend([
                "Watch and wait approach with regular monitoring",
                "Supportive care for symptomatic anemia",
                "Monitor for disease progression",
                "Quality of life optimization"
            ])
            monitoring.extend([
                "Complete blood count every 3-6 months",
                "Bone marrow assessment annually or if clinical change",
                "Iron overload monitoring if transfusion dependent"
            ])
            treatment_considerations.extend([
                "ESAs (erythropoiesis-stimulating agents) for anemia",
                "Iron chelation if transfusion dependent",
                "Clinical trial participation"
            ])
        
        elif total_score == 2:  # Intermediate Risk
            recommendations.extend([
                "Regular monitoring with consideration for early intervention",
                "Evaluate for hypomethylating agents",
                "Support care optimization",
                "Consider clinical trial participation"
            ])
            monitoring.extend([
                "Complete blood count every 2-3 months",
                "Bone marrow assessment every 6-12 months",
                "Cytogenetic monitoring for clonal evolution"
            ])
            treatment_considerations.extend([
                "Hypomethylating agents (azacitidine, decitabine)",
                "Lenalidomide for del(5q) cases",
                "ESAs if appropriate"
            ])
        
        else:  # High/Very High Risk (3-6 points)
            recommendations.extend([
                "Urgent hematology-oncology consultation",
                "Consider intensive treatment strategies",
                "Evaluate for allogeneic stem cell transplantation",
                "Aggressive supportive care"
            ])
            monitoring.extend([
                "Complete blood count monthly or more frequently",
                "Bone marrow assessment every 3-6 months",
                "Monitor for AML transformation"
            ])
            treatment_considerations.extend([
                "Hypomethylating agents as first-line therapy",
                "Allogeneic stem cell transplantation evaluation",
                "Clinical trials for novel agents",
                "Intensive supportive care including transfusions"
            ])
        
        # Specific recommendations based on parameters
        if transfusion_requirement == "regular":
            recommendations.append("Iron overload assessment and chelation therapy consideration")
        
        if karyotype == "poor":
            recommendations.append("Consider more aggressive treatment approach due to poor cytogenetics")
        
        if who_category == "raeb_2":
            recommendations.append("Close monitoring for AML transformation given high blast count")
        
        return {
            "general_recommendations": recommendations,
            "monitoring_schedule": monitoring,
            "treatment_considerations": treatment_considerations,
            "follow_up": "WPSS can be recalculated throughout disease course as clinical parameters change"
        }


def calculate_wpss_mds(who_category, karyotype, transfusion_requirement) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_wpss_mds pattern
    """
    calculator = WpssMdsCalculator()
    return calculator.calculate(who_category, karyotype, transfusion_requirement)