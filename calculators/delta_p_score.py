"""
Dutch-English LEMS Tumor Association Prediction (DELTA-P) Score Calculator

Predicts small-cell lung cancer (SCLC) risk in patients with Lambert-Eaton myasthenic 
syndrome (LEMS) using a 6-parameter clinical scoring system. Developed using Dutch 
and British cohorts with prospective validation.

References:
1. Titulaer MJ, Maddison P, Sont JK, Wirtz PW, Hilton-Jones D, Klooster R, et al. 
   Clinical Dutch-English Lambert-Eaton Myasthenic syndrome (LEMS) tumor association 
   prediction score accurately predicts small-cell lung cancer in the LEMS. 
   J Clin Oncol. 2011;29(7):902-8. doi: 10.1200/JCO.2010.32.0440.
2. van Sonderen A, Wirtz PW, Verschuuren JJ, Titulaer MJ. Paraneoplastic syndromes 
   of the neuromuscular junction: therapeutic implications. Brain. 2016;139(Pt 10):2759-71.
"""

from typing import Dict, Any


class DeltaPScoreCalculator:
    """Calculator for Dutch-English LEMS Tumor Association Prediction (DELTA-P) Score"""
    
    def __init__(self):
        # Each parameter scores 1 point if positive
        self.PARAMETER_POINTS = 1
        
        # Risk thresholds based on validation studies
        self.RISK_THRESHOLDS = {
            0: 0.0,      # 0% risk
            1: 2.6,      # 2.6% risk  
            2: 45.0,     # 45% risk
            3: 83.9,     # 83.9% risk
            4: 93.5,     # 93.5% risk
            5: 96.6,     # 96.6% risk
            6: 100.0     # 100% risk
        }
    
    def calculate(self, age_at_onset: str, smoking_status: str, weight_loss: str,
                  bulbar_involvement: str, erectile_dysfunction: str, 
                  karnofsky_status: str) -> Dict[str, Any]:
        """
        Calculates the DELTA-P score for SCLC prediction in LEMS patients
        
        Args:
            age_at_onset (str): Age at LEMS onset (under_50/50_or_over)
            smoking_status (str): Smoking at diagnosis (current_smoker/former_or_never)
            weight_loss (str): Weight loss >5% within 3 months (yes/no)
            bulbar_involvement (str): Bulbar symptoms present (yes/no)
            erectile_dysfunction (str): Erectile dysfunction in males (yes/no)
            karnofsky_status (str): Performance status (less_than_70/70_or_greater)
            
        Returns:
            Dict with the result and interpretation
        """
        
        # Map parameters for easier processing
        parameters = {
            'age_at_onset': age_at_onset,
            'smoking_status': smoking_status,
            'weight_loss': weight_loss,
            'bulbar_involvement': bulbar_involvement,
            'erectile_dysfunction': erectile_dysfunction,
            'karnofsky_status': karnofsky_status
        }
        
        # Validate inputs
        self._validate_inputs(parameters)
        
        # Calculate total score
        total_score = self._calculate_total_score(parameters)
        
        # Get interpretation
        interpretation = self._get_interpretation(total_score)
        
        return {
            "result": total_score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, parameters: Dict[str, Any]):
        """Validates input parameters"""
        
        # Validate age at onset
        age = parameters['age_at_onset']
        if not isinstance(age, str):
            raise ValueError("Age at onset must be a string")
        
        if age.lower() not in ['under_50', '50_or_over']:
            raise ValueError("Age at onset must be 'under_50' or '50_or_over'")
        
        # Validate smoking status
        smoking = parameters['smoking_status']
        if not isinstance(smoking, str):
            raise ValueError("Smoking status must be a string")
        
        if smoking.lower() not in ['current_smoker', 'former_or_never']:
            raise ValueError("Smoking status must be 'current_smoker' or 'former_or_never'")
        
        # Validate yes/no parameters
        yes_no_params = ['weight_loss', 'bulbar_involvement', 'erectile_dysfunction']
        
        for param in yes_no_params:
            value = parameters[param]
            if not isinstance(value, str):
                raise ValueError(f"Parameter '{param}' must be a string")
            
            if value.lower() not in ['yes', 'no']:
                raise ValueError(f"Parameter '{param}' must be 'yes' or 'no', got '{value}'")
        
        # Validate Karnofsky status
        karnofsky = parameters['karnofsky_status']
        if not isinstance(karnofsky, str):
            raise ValueError("Karnofsky status must be a string")
        
        if karnofsky.lower() not in ['less_than_70', '70_or_greater']:
            raise ValueError("Karnofsky status must be 'less_than_70' or '70_or_greater'")
    
    def _calculate_total_score(self, parameters: Dict[str, Any]) -> int:
        """Calculates the total DELTA-P score"""
        
        total_score = 0
        
        # Age at onset ≥50 years = 1 point
        if parameters['age_at_onset'].lower() == '50_or_over':
            total_score += self.PARAMETER_POINTS
        
        # Current smoking = 1 point
        if parameters['smoking_status'].lower() == 'current_smoker':
            total_score += self.PARAMETER_POINTS
        
        # Weight loss >5% = 1 point
        if parameters['weight_loss'].lower() == 'yes':
            total_score += self.PARAMETER_POINTS
        
        # Bulbar involvement = 1 point
        if parameters['bulbar_involvement'].lower() == 'yes':
            total_score += self.PARAMETER_POINTS
        
        # Erectile dysfunction = 1 point
        if parameters['erectile_dysfunction'].lower() == 'yes':
            total_score += self.PARAMETER_POINTS
        
        # Karnofsky performance status <70 = 1 point
        if parameters['karnofsky_status'].lower() == 'less_than_70':
            total_score += self.PARAMETER_POINTS
        
        return total_score
    
    def _get_interpretation(self, total_score: int) -> Dict[str, str]:
        """
        Determines the interpretation based on the DELTA-P score
        
        Args:
            total_score (int): Calculated DELTA-P score
            
        Returns:
            Dict with interpretation
        """
        
        # Get approximate risk percentage
        risk_percentage = self.RISK_THRESHOLDS.get(total_score, 100.0)
        
        if total_score <= 1:
            return {
                "stage": "Very Low Risk",
                "description": "SCLC virtually excluded",
                "interpretation": f"Very low risk of small-cell lung cancer (DELTA-P score = {total_score}, ~{risk_percentage}% risk). SCLC is virtually excluded. Standard cancer screening protocols appropriate with annual chest imaging. Continue neurological management of LEMS with standard monitoring."
            }
        elif total_score == 2:
            return {
                "stage": "Low-Moderate Risk", 
                "description": "Low to moderate SCLC risk",
                "interpretation": f"Low to moderate risk of small-cell lung cancer (DELTA-P score = {total_score}, ~{risk_percentage}% risk). Consider enhanced screening with chest CT every 6 months. Monitor closely for development of additional risk factors or cancer symptoms."
            }
        else:  # score 3-6
            return {
                "stage": "High Risk",
                "description": "High SCLC risk - intensive screening required",
                "interpretation": f"High risk of small-cell lung cancer (DELTA-P score = {total_score}, ~{risk_percentage}% risk). Immediate and intensive cancer screening required with chest CT, bronchoscopy if indicated, and multidisciplinary oncology evaluation. Screen every 3 months as recommended for high-risk patients. Early detection and treatment of SCLC is critical for improved outcomes."
            }


def calculate_delta_p_score(age_at_onset: str, smoking_status: str, weight_loss: str,
                           bulbar_involvement: str, erectile_dysfunction: str, 
                           karnofsky_status: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_delta_p_score pattern
    """
    calculator = DeltaPScoreCalculator()
    return calculator.calculate(
        age_at_onset, smoking_status, weight_loss, bulbar_involvement,
        erectile_dysfunction, karnofsky_status
    )