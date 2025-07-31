"""
Geneva Risk Score for Venous Thromboembolism (VTE) Prophylaxis Calculator

The Geneva Risk Score for VTE Prophylaxis is a validated tool for predicting the need for 
venous thromboembolism prophylaxis in hospitalized medical patients. It helps clinicians 
identify patients at high risk for VTE who would benefit from thromboprophylaxis and those 
at low risk who may not require anticoagulation, thus optimizing prophylaxis decisions and 
reducing unnecessary interventions.

References (Vancouver style):
1. Chopard P, Spirk D, Bounameaux H. Identifying acutely ill medical patients requiring 
   thromboprophylaxis. J Thromb Haemost. 2006;4(4):915-916. doi: 10.1111/j.1538-7836.2006.01818.x.
2. Nendaz M, Spirk D, Kucher N, et al. Multicentre validation of the Geneva Risk Score for 
   hospitalised medical patients at risk of venous thromboembolism. Explicit ASsessment of 
   Thromboembolic RIsk and Prophylaxis for Medical PATients in SwitzErland (ESTIMATE). 
   Thromb Haemost. 2014;111(3):531-538. doi: 10.1160/TH13-05-0427.
3. Decousus H, Tapson VF, Bergmann JF, et al. Factors at admission associated with bleeding 
   risk in medical patients: findings from the IMPROVE investigators. Chest. 2011;139(1):69-79. 
   doi: 10.1378/chest.09-3081.
"""

from typing import Dict, Any


class GenevaVteProphylaxisCalculator:
    """Calculator for Geneva Risk Score for VTE Prophylaxis"""
    
    def __init__(self):
        # Major risk factors (2 points each)
        self.MAJOR_RISK_FACTORS = {
            'cardiac_failure': 2,
            'respiratory_failure': 2,
            'recent_stroke': 2,
            'recent_myocardial_infarction': 2,
            'acute_infectious_disease': 2,
            'acute_rheumatic_disease': 2,
            'active_malignancy': 2,
            'myeloproliferative_syndrome': 2,
            'nephrotic_syndrome': 2,
            'prior_vte_history': 2,
            'known_hypercoagulable_state': 2
        }
        
        # Minor risk factors (1 point each)
        self.MINOR_RISK_FACTORS = {
            'immobilization': 1,
            'recent_travel': 1,
            'age_over_60': 1,
            'obesity': 1,
            'chronic_venous_insufficiency': 1,
            'pregnancy': 1,
            'hormonal_therapy': 1,
            'dehydration': 1
        }
        
        # All risk factors combined
        self.ALL_RISK_FACTORS = {**self.MAJOR_RISK_FACTORS, **self.MINOR_RISK_FACTORS}
    
    def calculate(self, cardiac_failure: str, respiratory_failure: str, recent_stroke: str,
                 recent_myocardial_infarction: str, acute_infectious_disease: str,
                 acute_rheumatic_disease: str, active_malignancy: str, 
                 myeloproliferative_syndrome: str, nephrotic_syndrome: str,
                 prior_vte_history: str, known_hypercoagulable_state: str,
                 immobilization: str, recent_travel: str, age_over_60: str,
                 obesity: str, chronic_venous_insufficiency: str, pregnancy: str,
                 hormonal_therapy: str, dehydration: str) -> Dict[str, Any]:
        """
        Calculates Geneva Risk Score for VTE Prophylaxis using provided risk factors
        
        Args:
            cardiac_failure (str): Presence of cardiac failure
            respiratory_failure (str): Presence of respiratory failure
            recent_stroke (str): Recent stroke within 3 months
            recent_myocardial_infarction (str): Recent MI within 4 weeks
            acute_infectious_disease (str): Acute infectious disease including sepsis
            acute_rheumatic_disease (str): Acute rheumatic disease
            active_malignancy (str): Active malignancy
            myeloproliferative_syndrome (str): Myeloproliferative syndrome
            nephrotic_syndrome (str): Nephrotic syndrome
            prior_vte_history (str): Prior VTE history
            known_hypercoagulable_state (str): Known hypercoagulable state
            immobilization (str): Immobilization ≥3 days
            recent_travel (str): Recent travel >6 hours
            age_over_60 (str): Age >60 years
            obesity (str): BMI >30 kg/m²
            chronic_venous_insufficiency (str): Chronic venous insufficiency
            pregnancy (str): Pregnancy
            hormonal_therapy (str): Hormonal therapy
            dehydration (str): Dehydration
            
        Returns:
            Dict with the result and clinical interpretation
        """
        
        # Collect all parameters for validation
        parameters = {
            'cardiac_failure': cardiac_failure,
            'respiratory_failure': respiratory_failure,
            'recent_stroke': recent_stroke,
            'recent_myocardial_infarction': recent_myocardial_infarction,
            'acute_infectious_disease': acute_infectious_disease,
            'acute_rheumatic_disease': acute_rheumatic_disease,
            'active_malignancy': active_malignancy,
            'myeloproliferative_syndrome': myeloproliferative_syndrome,
            'nephrotic_syndrome': nephrotic_syndrome,
            'prior_vte_history': prior_vte_history,
            'known_hypercoagulable_state': known_hypercoagulable_state,
            'immobilization': immobilization,
            'recent_travel': recent_travel,
            'age_over_60': age_over_60,
            'obesity': obesity,
            'chronic_venous_insufficiency': chronic_venous_insufficiency,
            'pregnancy': pregnancy,
            'hormonal_therapy': hormonal_therapy,
            'dehydration': dehydration
        }
        
        # Validate inputs
        self._validate_inputs(parameters)
        
        # Calculate Geneva VTE score
        geneva_score = self._calculate_geneva_score(parameters)
        
        # Get clinical interpretation
        interpretation = self._get_interpretation(geneva_score, parameters)
        
        return {
            "result": geneva_score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, parameters: Dict[str, str]):
        """Validates input parameters"""
        
        for param_name, param_value in parameters.items():
            if param_value not in ["yes", "no"]:
                raise ValueError(f"{param_name} must be 'yes' or 'no'")
    
    def _calculate_geneva_score(self, parameters: Dict[str, str]) -> int:
        """Calculates the Geneva Risk Score total"""
        
        total_score = 0
        
        for risk_factor, value in parameters.items():
            if value == "yes" and risk_factor in self.ALL_RISK_FACTORS:
                total_score += self.ALL_RISK_FACTORS[risk_factor]
        
        return total_score
    
    def _get_interpretation(self, score: int, parameters: Dict[str, str]) -> Dict[str, str]:
        """
        Determines clinical interpretation based on Geneva VTE score
        
        Args:
            score (int): Calculated Geneva VTE score
            parameters (Dict): Risk factor parameters for detailed interpretation
            
        Returns:
            Dict with interpretation
        """
        
        # Build risk factor summary
        present_major_factors = []
        present_minor_factors = []
        
        for factor, value in parameters.items():
            if value == "yes":
                if factor in self.MAJOR_RISK_FACTORS:
                    present_major_factors.append(self._format_risk_factor_name(factor))
                elif factor in self.MINOR_RISK_FACTORS:
                    present_minor_factors.append(self._format_risk_factor_name(factor))
        
        # Build risk factor summary text
        risk_summary = ""
        if present_major_factors:
            risk_summary += f"Major risk factors (2 pts each): {', '.join(present_major_factors)}. "
        if present_minor_factors:
            risk_summary += f"Minor risk factors (1 pt each): {', '.join(present_minor_factors)}. "
        
        if not risk_summary:
            risk_summary = "No significant risk factors identified. "
        
        # Determine risk category and recommendations
        if score < 3:
            return {
                "stage": "Low Risk",
                "description": "Low risk for VTE",
                "interpretation": (
                    f"Geneva VTE Risk Score: {score} points. {risk_summary}"
                    f"Low risk for venous thromboembolism (approximately 0.6% risk). "
                    f"Pharmacological prophylaxis not routinely recommended. Consider mechanical "
                    f"prophylaxis (sequential compression devices, early mobilization) if feasible. "
                    f"Monitor for changes in clinical status that may increase VTE risk. "
                    f"Reassess daily during hospitalization."
                )
            }
        else:
            return {
                "stage": "High Risk",
                "description": "High risk for VTE",
                "interpretation": (
                    f"Geneva VTE Risk Score: {score} points. {risk_summary}"
                    f"High risk for venous thromboembolism (approximately 3.2% risk). "
                    f"Thromboprophylaxis recommended unless contraindicated. Consider low molecular "
                    f"weight heparin, unfractionated heparin, or fondaparinux based on renal function "
                    f"and bleeding risk. If pharmacological prophylaxis is contraindicated, use "
                    f"mechanical prophylaxis (sequential compression devices). Continue prophylaxis "
                    f"throughout hospitalization and consider extended prophylaxis based on risk factors."
                )
            }
    
    def _format_risk_factor_name(self, factor_name: str) -> str:
        """Formats risk factor names for display"""
        
        factor_display_names = {
            'cardiac_failure': 'cardiac failure',
            'respiratory_failure': 'respiratory failure',
            'recent_stroke': 'recent stroke (<3 months)',
            'recent_myocardial_infarction': 'recent MI (<4 weeks)',
            'acute_infectious_disease': 'acute infectious disease/sepsis',
            'acute_rheumatic_disease': 'acute rheumatic disease',
            'active_malignancy': 'active malignancy',
            'myeloproliferative_syndrome': 'myeloproliferative syndrome',
            'nephrotic_syndrome': 'nephrotic syndrome',
            'prior_vte_history': 'prior VTE history',
            'known_hypercoagulable_state': 'hypercoagulable state',
            'immobilization': 'immobilization (≥3 days)',
            'recent_travel': 'recent travel (>6 hours)',
            'age_over_60': 'age >60 years',
            'obesity': 'obesity (BMI >30)',
            'chronic_venous_insufficiency': 'chronic venous insufficiency',
            'pregnancy': 'pregnancy',
            'hormonal_therapy': 'hormonal therapy',
            'dehydration': 'dehydration'
        }
        
        return factor_display_names.get(factor_name, factor_name)


def calculate_geneva_vte_prophylaxis(cardiac_failure: str, respiratory_failure: str, 
                                   recent_stroke: str, recent_myocardial_infarction: str,
                                   acute_infectious_disease: str, acute_rheumatic_disease: str,
                                   active_malignancy: str, myeloproliferative_syndrome: str,
                                   nephrotic_syndrome: str, prior_vte_history: str,
                                   known_hypercoagulable_state: str, immobilization: str,
                                   recent_travel: str, age_over_60: str, obesity: str,
                                   chronic_venous_insufficiency: str, pregnancy: str,
                                   hormonal_therapy: str, dehydration: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_geneva_vte_prophylaxis pattern
    """
    calculator = GenevaVteProphylaxisCalculator()
    return calculator.calculate(
        cardiac_failure, respiratory_failure, recent_stroke, recent_myocardial_infarction,
        acute_infectious_disease, acute_rheumatic_disease, active_malignancy,
        myeloproliferative_syndrome, nephrotic_syndrome, prior_vte_history,
        known_hypercoagulable_state, immobilization, recent_travel, age_over_60,
        obesity, chronic_venous_insufficiency, pregnancy, hormonal_therapy, dehydration
    )