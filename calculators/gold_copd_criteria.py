"""
Global Initiative for Obstructive Lung Disease (GOLD) Criteria for COPD Calculator

The GOLD criteria provide a standardized approach for the diagnosis, assessment, and 
management of chronic obstructive pulmonary disease (COPD). Updated regularly, the 
GOLD 2025 guidelines use post-bronchodilator spirometry, symptom assessment, and 
exacerbation history to classify COPD severity and guide treatment decisions. The 
system emphasizes individualized treatment based on the ABE (Assessment, Bronchodilator, 
Exacerbation) framework.

References (Vancouver style):
1. Global Initiative for Chronic Obstructive Lung Disease. Global Strategy for the 
   Diagnosis, Management, and Prevention of Chronic Obstructive Pulmonary Disease, 
   2025 Report. Available from: https://goldcopd.org/
2. Singh SJ, Augustin IML, Correia de Sousa R, et al. An official systematic review 
   of the European Respiratory Society/American Thoracic Society: measurement 
   properties of field walking tests in chronic respiratory disease. Eur Respir J. 
   2014;44(6):1447-1478. doi: 10.1183/09031936.00150414.
3. Jones PW, Harding G, Berry P, et al. Development and first validation of the 
   COPD Assessment Test. Eur Respir J. 2009;34(3):648-654. 
   doi: 10.1183/09031936.00102509.
4. Bestall JC, Paul EA, Garrod R, et al. Usefulness of the Medical Research Council 
   (MRC) dyspnoea scale as a measure of disability in patients with chronic obstructive 
   pulmonary disease. Thorax. 1999;54(7):581-586. doi: 10.1136/thx.54.7.581.
"""

from typing import Dict, Any, Optional


class GoldCopdCriteriaCalculator:
    """Calculator for GOLD COPD Criteria Assessment"""
    
    def __init__(self):
        # GOLD spirometric stages
        self.GOLD_STAGES = {
            1: {"name": "GOLD 1", "description": "Mild", "fev1_min": 80, "fev1_max": 120},
            2: {"name": "GOLD 2", "description": "Moderate", "fev1_min": 50, "fev1_max": 79},
            3: {"name": "GOLD 3", "description": "Severe", "fev1_min": 30, "fev1_max": 49},
            4: {"name": "GOLD 4", "description": "Very Severe", "fev1_min": 10, "fev1_max": 29}
        }
        
        # mMRC Dyspnea Scale descriptions
        self.MMRC_DESCRIPTIONS = {
            0: "Breathless only with strenuous exercise",
            1: "Short of breath when hurrying on level ground or walking up slight hill",
            2: "Walks slower than people of same age due to breathlessness, or stops for breath when walking at own pace",
            3: "Stops for breath after walking about 100 meters or after few minutes on level ground",
            4: "Too breathless to leave house or breathless when dressing/undressing"
        }
        
        # Treatment recommendations by group
        self.TREATMENT_RECOMMENDATIONS = {
            "A": {
                "bronchodilator": "Short-acting bronchodilator (SABA or SAMA) as needed",
                "additional": "Smoking cessation, vaccination, pulmonary rehabilitation if breathless"
            },
            "B": {
                "bronchodilator": "Long-acting bronchodilator (LABA or LAMA)",
                "additional": "If still breathless: LABA + LAMA combination"
            },
            "E": {
                "bronchodilator": "LABA + LAMA combination",
                "additional": "If continued exacerbations: Consider ICS based on eosinophil count and phenotype"
            }
        }
    
    def calculate(self, fev1_percent_predicted: float, fvc_fev1_ratio: float, 
                 dyspnea_mmrc: int, exacerbations_last_year: int, 
                 hospitalizations_last_year: int, cat_score: Optional[int] = None) -> Dict[str, Any]:
        """
        Calculates GOLD COPD classification and treatment recommendations
        
        Args:
            fev1_percent_predicted (float): FEV1 as percentage of predicted (10-120%)
            fvc_fev1_ratio (float): Post-bronchodilator FEV1/FVC ratio (0.30-1.00)
            dyspnea_mmrc (int): mMRC dyspnea scale (0-4)
            exacerbations_last_year (int): Number of exacerbations in last 12 months
            hospitalizations_last_year (int): Number of hospitalizations in last 12 months
            cat_score (int, optional): CAT score (0-40), alternative to mMRC
            
        Returns:
            Dict with GOLD stage, group, and comprehensive treatment recommendations
        """
        
        # Validate inputs
        self._validate_inputs(fev1_percent_predicted, fvc_fev1_ratio, dyspnea_mmrc, 
                            exacerbations_last_year, hospitalizations_last_year, cat_score)
        
        # Check for COPD diagnosis
        copd_diagnosis = fvc_fev1_ratio < 0.70
        
        if not copd_diagnosis:
            return self._no_copd_result(fev1_percent_predicted, fvc_fev1_ratio)
        
        # Determine GOLD spirometric stage
        gold_stage = self._determine_gold_stage(fev1_percent_predicted)
        
        # Assess symptoms
        symptom_burden = self._assess_symptoms(dyspnea_mmrc, cat_score)
        
        # Assess exacerbation risk
        exacerbation_risk = self._assess_exacerbation_risk(exacerbations_last_year, hospitalizations_last_year)
        
        # Determine COPD group (A, B, or E)
        copd_group = self._determine_copd_group(symptom_burden, exacerbation_risk)
        
        # Get comprehensive interpretation
        interpretation = self._get_interpretation(
            gold_stage, copd_group, fev1_percent_predicted, fvc_fev1_ratio,
            dyspnea_mmrc, exacerbations_last_year, hospitalizations_last_year,
            symptom_burden, exacerbation_risk, cat_score
        )
        
        return {
            "result": f"{gold_stage['name']} - {gold_stage['description']} COPD, Group {copd_group}",
            "unit": "classification",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, fev1_percent: float, fvc_fev1_ratio: float, mmrc: int,
                        exacerbations: int, hospitalizations: int, cat_score: Optional[int]):
        """Validates input parameters"""
        
        if not isinstance(fev1_percent, (int, float)) or fev1_percent < 10 or fev1_percent > 120:
            raise ValueError("FEV1 percent predicted must be between 10 and 120%")
        
        if not isinstance(fvc_fev1_ratio, (int, float)) or fvc_fev1_ratio < 0.30 or fvc_fev1_ratio > 1.00:
            raise ValueError("FEV1/FVC ratio must be between 0.30 and 1.00")
        
        if not isinstance(mmrc, int) or mmrc < 0 or mmrc > 4:
            raise ValueError("mMRC dyspnea scale must be integer between 0 and 4")
        
        if not isinstance(exacerbations, int) or exacerbations < 0:
            raise ValueError("Number of exacerbations must be non-negative integer")
        
        if not isinstance(hospitalizations, int) or hospitalizations < 0:
            raise ValueError("Number of hospitalizations must be non-negative integer")
        
        if cat_score is not None and (not isinstance(cat_score, int) or cat_score < 0 or cat_score > 40):
            raise ValueError("CAT score must be integer between 0 and 40")
    
    def _no_copd_result(self, fev1_percent: float, fvc_fev1_ratio: float) -> Dict[str, Any]:
        """Returns result when FEV1/FVC ratio doesn't meet COPD criteria"""
        
        return {
            "result": "No COPD - Normal spirometry",
            "unit": "classification",
            "interpretation": (
                f"FEV1/FVC ratio: {fvc_fev1_ratio:.2f} (≥0.70). FEV1: {fev1_percent:.1f}% predicted. "
                f"Post-bronchodilator spirometry does not meet criteria for COPD diagnosis "
                f"(requires FEV1/FVC <0.70). Consider other causes of respiratory symptoms "
                f"if present. Continue smoking cessation counseling if applicable. "
                f"Recommend routine health maintenance and vaccination. If high clinical "
                f"suspicion for COPD remains, consider repeat spirometry or referral to "
                f"pulmonology for further evaluation."
            ),
            "stage": "No COPD",
            "stage_description": "Normal lung function"
        }
    
    def _determine_gold_stage(self, fev1_percent: float) -> Dict[str, Any]:
        """Determines GOLD spirometric stage based on FEV1 percentage"""
        
        for stage_num, stage_info in self.GOLD_STAGES.items():
            if stage_info["fev1_min"] <= fev1_percent <= stage_info["fev1_max"]:
                return {
                    "number": stage_num,
                    "name": stage_info["name"],
                    "description": stage_info["description"],
                    "fev1_range": f"{stage_info['fev1_min']}-{stage_info['fev1_max']}% predicted"
                }
        
        # Handle edge cases
        if fev1_percent < 10:
            return {
                "number": 4,
                "name": "GOLD 4",
                "description": "Very Severe",
                "fev1_range": "<30% predicted"
            }
        else:
            return {
                "number": 1,
                "name": "GOLD 1", 
                "description": "Mild",
                "fev1_range": "≥80% predicted"
            }
    
    def _assess_symptoms(self, mmrc: int, cat_score: Optional[int]) -> Dict[str, Any]:
        """Assesses symptom burden using mMRC and/or CAT"""
        
        # Primary assessment with mMRC
        mmrc_high = mmrc >= 2
        mmrc_description = self.MMRC_DESCRIPTIONS[mmrc]
        
        result = {
            "mmrc_score": mmrc,
            "mmrc_description": mmrc_description,
            "mmrc_high_symptoms": mmrc_high
        }
        
        # Add CAT assessment if provided
        if cat_score is not None:
            cat_high = cat_score >= 10
            result.update({
                "cat_score": cat_score,
                "cat_high_symptoms": cat_high,
                "high_symptoms": mmrc_high or cat_high  # Either can indicate high symptoms
            })
        else:
            result["high_symptoms"] = mmrc_high
        
        return result
    
    def _assess_exacerbation_risk(self, exacerbations: int, hospitalizations: int) -> Dict[str, Any]:
        """Assesses exacerbation risk based on history"""
        
        # High risk: ≥2 exacerbations OR ≥1 hospitalization in last year
        high_risk = exacerbations >= 2 or hospitalizations >= 1
        
        return {
            "exacerbations": exacerbations,
            "hospitalizations": hospitalizations,
            "high_risk": high_risk,
            "risk_level": "High" if high_risk else "Low"
        }
    
    def _determine_copd_group(self, symptoms: Dict[str, Any], exacerbations: Dict[str, Any]) -> str:
        """Determines COPD group (A, B, E) based on symptoms and exacerbation risk"""
        
        high_symptoms = symptoms["high_symptoms"]
        high_exacerbation_risk = exacerbations["high_risk"]
        
        if high_exacerbation_risk:
            return "E"  # High exacerbation risk (regardless of symptoms)
        elif high_symptoms:
            return "B"  # High symptoms, low exacerbation risk
        else:
            return "A"  # Low symptoms, low exacerbation risk
    
    def _get_interpretation(self, gold_stage: Dict[str, Any], copd_group: str,
                          fev1_percent: float, fvc_fev1_ratio: float, mmrc: int,
                          exacerbations: int, hospitalizations: int,
                          symptoms: Dict[str, Any], exacerbation_risk: Dict[str, Any],
                          cat_score: Optional[int]) -> Dict[str, str]:
        """Provides comprehensive clinical interpretation and treatment recommendations"""
        
        # Build clinical summary
        spirometry_summary = f"Post-bronchodilator spirometry: FEV1/FVC {fvc_fev1_ratio:.2f} (<0.70 confirms COPD), FEV1 {fev1_percent:.1f}% predicted"
        
        symptom_summary = f"Symptoms: mMRC {mmrc} ({symptoms['mmrc_description']})"
        if cat_score is not None:
            symptom_summary += f", CAT {cat_score}/40"
        
        exacerbation_summary = f"Exacerbation history: {exacerbations} exacerbations, {hospitalizations} hospitalizations in last year"
        
        # Get treatment recommendations
        treatment = self.TREATMENT_RECOMMENDATIONS.get(copd_group, self.TREATMENT_RECOMMENDATIONS["A"])
        
        # Build comprehensive interpretation
        stage_description = f"{gold_stage['name']} - {gold_stage['description']} COPD, Group {copd_group}"
        
        if copd_group == "A":
            group_explanation = "Low symptom burden, low exacerbation risk"
            management_focus = "Focus on smoking cessation, vaccination, and bronchodilator therapy as needed"
        elif copd_group == "B":
            group_explanation = "High symptom burden, low exacerbation risk"
            management_focus = "Regular long-acting bronchodilator therapy with pulmonary rehabilitation"
        else:  # Group E
            group_explanation = "High exacerbation risk (regardless of symptom level)"
            management_focus = "Intensive therapy to prevent exacerbations with combination bronchodilators"
        
        interpretation = (
            f"{stage_description}. {spirometry_summary}. {symptom_summary}. {exacerbation_summary}. "
            f"Classification: {group_explanation}. "
            f"Treatment recommendations: {treatment['bronchodilator']}. {treatment['additional']}. "
            f"{management_focus}. Essential interventions: smoking cessation (most important), "
            f"annual influenza vaccination, pneumococcal vaccination, COVID-19 vaccination. "
            f"Pulmonary rehabilitation recommended for all symptomatic patients (Groups B and E). "
            f"Monitor for comorbidities especially cardiovascular disease. Regular follow-up "
            f"with spirometry, symptom assessment, and exacerbation review. Consider oxygen "
            f"therapy evaluation if FEV1 <30% or clinical signs of respiratory failure."
        )
        
        return {
            "stage": stage_description,
            "description": f"{gold_stage['description']} airflow limitation, Group {copd_group}",
            "interpretation": interpretation
        }


def calculate_gold_copd_criteria(fev1_percent_predicted: float, fvc_fev1_ratio: float,
                               dyspnea_mmrc: int, exacerbations_last_year: int,
                               hospitalizations_last_year: int, 
                               cat_score: Optional[int] = None) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_gold_copd_criteria pattern
    """
    calculator = GoldCopdCriteriaCalculator()
    return calculator.calculate(fev1_percent_predicted, fvc_fev1_ratio, dyspnea_mmrc,
                              exacerbations_last_year, hospitalizations_last_year, cat_score)