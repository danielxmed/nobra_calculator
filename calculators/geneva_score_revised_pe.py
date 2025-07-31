"""
Geneva Score (Revised) for Pulmonary Embolism Calculator

The Geneva Score (Revised) for Pulmonary Embolism is a validated clinical decision rule 
that helps determine the probability of pulmonary embolism in patients presenting with 
suspected PE. Unlike Wells' criteria, it does not require clinical gestalt, making it 
more objective and reproducible across different clinicians and settings.

References (Vancouver style):
1. Le Gal G, Righini M, Roy PM, et al. Prediction of pulmonary embolism in the emergency 
   department: the revised Geneva score. Ann Intern Med. 2006;144(3):165-171. 
   doi: 10.7326/0003-4819-144-3-200602070-00004.
2. Klok FA, Mos IC, Nijkeuter M, et al. Simplification of the revised Geneva score for 
   assessing clinical probability of pulmonary embolism. Arch Intern Med. 2008;168(19):2131-2136. 
   doi: 10.1001/archinte.168.19.2131.
3. Ceriani E, Combescure C, Le Gal G, et al. Clinical prediction rules for pulmonary embolism: 
   a systematic review and meta-analysis. J Thromb Haemost. 2010;8(5):957-970. 
   doi: 10.1111/j.1538-7836.2010.03801.x.
"""

from typing import Dict, Any


class GenevaScoreRevisedPeCalculator:
    """Calculator for Geneva Score (Revised) for Pulmonary Embolism"""
    
    def __init__(self):
        # Risk factor point values
        self.RISK_FACTOR_POINTS = {
            'age_over_65': 1,
            'previous_dvt_pe': 3,
            'surgery_fracture_past_month': 2,
            'active_malignancy': 2,
            'unilateral_limb_pain': 3,
            'hemoptysis': 2,
            'limb_palpation_edema': 4
        }
        
        # Heart rate category points
        self.HEART_RATE_POINTS = {
            'under_75': 0,
            '75_to_94': 3,
            '95_or_higher': 5
        }
        
        # PE probability by score ranges
        self.PE_PROBABILITY = {
            'low': {'min': 0, 'max': 3, 'probability': '<10%'},
            'intermediate': {'min': 4, 'max': 10, 'probability': '20-30%'},
            'high': {'min': 11, 'max': 25, 'probability': '>60%'}
        }
    
    def calculate(self, age_over_65: str, previous_dvt_pe: str, surgery_fracture_past_month: str,
                 active_malignancy: str, unilateral_limb_pain: str, hemoptysis: str,
                 heart_rate_category: str, limb_palpation_edema: str) -> Dict[str, Any]:
        """
        Calculates Geneva Score (Revised) for Pulmonary Embolism using provided clinical parameters
        
        Args:
            age_over_65 (str): Age greater than 65 years
            previous_dvt_pe (str): Previous DVT or PE history
            surgery_fracture_past_month (str): Surgery or lower limb fracture within past month
            active_malignancy (str): Active malignant condition
            unilateral_limb_pain (str): Unilateral lower limb pain
            hemoptysis (str): Hemoptysis (coughing up blood)
            heart_rate_category (str): Heart rate category
            limb_palpation_edema (str): Pain on limb palpation and unilateral edema
            
        Returns:
            Dict with the result and clinical interpretation
        """
        
        # Collect all parameters for validation
        parameters = {
            'age_over_65': age_over_65,
            'previous_dvt_pe': previous_dvt_pe,
            'surgery_fracture_past_month': surgery_fracture_past_month,
            'active_malignancy': active_malignancy,
            'unilateral_limb_pain': unilateral_limb_pain,
            'hemoptysis': hemoptysis,
            'heart_rate_category': heart_rate_category,
            'limb_palpation_edema': limb_palpation_edema
        }
        
        # Validate inputs
        self._validate_inputs(parameters)
        
        # Calculate Geneva PE score
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
        
        # Validate yes/no parameters
        yes_no_params = [
            'age_over_65', 'previous_dvt_pe', 'surgery_fracture_past_month',
            'active_malignancy', 'unilateral_limb_pain', 'hemoptysis', 'limb_palpation_edema'
        ]
        
        for param in yes_no_params:
            if parameters[param] not in ["yes", "no"]:
                raise ValueError(f"{param} must be 'yes' or 'no'")
        
        # Validate heart rate category
        if parameters['heart_rate_category'] not in self.HEART_RATE_POINTS:
            raise ValueError("heart_rate_category must be 'under_75', '75_to_94', or '95_or_higher'")
    
    def _calculate_geneva_score(self, parameters: Dict[str, str]) -> int:
        """Calculates the Geneva PE score total"""
        
        total_score = 0
        
        # Add points for yes/no risk factors
        for risk_factor in self.RISK_FACTOR_POINTS:
            if parameters[risk_factor] == "yes":
                total_score += self.RISK_FACTOR_POINTS[risk_factor]
        
        # Add points for heart rate category
        total_score += self.HEART_RATE_POINTS[parameters['heart_rate_category']]
        
        return total_score
    
    def _get_interpretation(self, score: int, parameters: Dict[str, str]) -> Dict[str, str]:
        """
        Determines clinical interpretation based on Geneva PE score
        
        Args:
            score (int): Calculated Geneva PE score
            parameters (Dict): Clinical parameters for detailed interpretation
            
        Returns:
            Dict with interpretation
        """
        
        # Build present risk factors summary
        present_factors = []
        
        risk_factor_names = {
            'age_over_65': 'age >65 years (1 pt)',
            'previous_dvt_pe': 'previous DVT/PE (3 pts)',
            'surgery_fracture_past_month': 'surgery/fracture past month (2 pts)',
            'active_malignancy': 'active malignancy (2 pts)',
            'unilateral_limb_pain': 'unilateral limb pain (3 pts)',
            'hemoptysis': 'hemoptysis (2 pts)',
            'limb_palpation_edema': 'limb palpation pain and edema (4 pts)'
        }
        
        for factor, value in parameters.items():
            if factor in risk_factor_names and value == "yes":
                present_factors.append(risk_factor_names[factor])
        
        # Add heart rate category if not under 75
        heart_rate_descriptions = {
            'under_75': '',
            '75_to_94': 'heart rate 75-94 bpm (3 pts)',
            '95_or_higher': 'heart rate ≥95 bpm (5 pts)'
        }
        
        hr_description = heart_rate_descriptions[parameters['heart_rate_category']]
        if hr_description:
            present_factors.append(hr_description)
        
        # Build risk factor summary
        if present_factors:
            risk_summary = f"Present risk factors: {', '.join(present_factors)}. "
        else:
            risk_summary = "No significant risk factors present. "
        
        # Determine risk category and recommendations
        if score <= 3:
            return {
                "stage": "Low Risk",
                "description": "Low clinical probability of PE",
                "interpretation": (
                    f"Geneva Score (Revised): {score} points. {risk_summary}"
                    f"Low clinical probability of pulmonary embolism (less than 10% incidence). "
                    f"Recommend D-dimer testing. If D-dimer is negative, pulmonary embolism is "
                    f"effectively ruled out and no further testing is needed. If D-dimer is positive, "
                    f"consider CT pulmonary angiogram for definitive diagnosis. Age-adjusted D-dimer "
                    f"cutoffs may be appropriate in elderly patients."
                )
            }
        elif score <= 10:
            return {
                "stage": "Intermediate Risk",
                "description": "Intermediate clinical probability of PE",
                "interpretation": (
                    f"Geneva Score (Revised): {score} points. {risk_summary}"
                    f"Intermediate clinical probability of pulmonary embolism (20-30% incidence). "
                    f"Recommend D-dimer testing. If D-dimer is negative, pulmonary embolism is "
                    f"unlikely and further testing may not be necessary. If D-dimer is positive, "
                    f"CT pulmonary angiogram is recommended for definitive diagnosis. Consider "
                    f"clinical context and patient factors when interpreting results."
                )
            }
        else:
            return {
                "stage": "High Risk",
                "description": "High clinical probability of PE",
                "interpretation": (
                    f"Geneva Score (Revised): {score} points. {risk_summary}"
                    f"High clinical probability of pulmonary embolism (greater than 60% incidence). "
                    f"Urgent CT pulmonary angiogram is recommended. D-dimer testing is not necessary "
                    f"as the high clinical probability warrants proceeding directly to definitive "
                    f"imaging. If CT-PA is contraindicated, consider ventilation-perfusion scan or "
                    f"alternative imaging modalities. Anticoagulation may be considered while awaiting "
                    f"imaging if bleeding risk is low."
                )
            }


def calculate_geneva_score_revised_pe(age_over_65: str, previous_dvt_pe: str, 
                                    surgery_fracture_past_month: str, active_malignancy: str,
                                    unilateral_limb_pain: str, hemoptysis: str,
                                    heart_rate_category: str, limb_palpation_edema: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_geneva_score_revised_pe pattern
    """
    calculator = GenevaScoreRevisedPeCalculator()
    return calculator.calculate(
        age_over_65, previous_dvt_pe, surgery_fracture_past_month, active_malignancy,
        unilateral_limb_pain, hemoptysis, heart_rate_category, limb_palpation_edema
    )