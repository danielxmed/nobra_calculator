"""
Blast Lung Injury Severity Score Calculator

Stratifies primary blast lung injuries into three severity categories to guide 
ventilatory treatment and predict clinical outcomes. Developed by Pizov et al. 
for assessment of blast-related respiratory injuries.

References (Vancouver style):
1. Pizov R, Oppenheim-Eden A, Matot I, Weiss YG, Eidelman LA, Rivkind AI, et al. 
   Blast lung injury from an explosion on a civilian bus. Chest. 1999 Jan;115(1):165-72.
2. Leibovici D, Gofrit ON, Stein M, Shapira SC, Noga Y, Heruti RJ, et al. 
   Blast injuries: bus versus open-air bombings--a comparative study of injuries 
   in survivors of open-air versus confined-space explosions. J Trauma. 1996 Dec;41(6):1030-5.
3. Wolf SJ, Bebarta VS, Bonnett CJ, Pons PT, Cantrill SV. Blast injuries. 
   Lancet. 2009 Jul 18;374(9687):405-15.
"""

from typing import Dict, Any


class BlastLungInjurySeverityCalculator:
    """Calculator for Blast Lung Injury Severity Score"""
    
    def __init__(self):
        # PaO2/FiO2 ratio scoring thresholds
        self.NORMAL_PAO2_FIO2_THRESHOLD = 200
        self.MODERATE_PAO2_FIO2_THRESHOLD = 60
        
        # Chest X-ray findings scores
        self.chest_xray_scores = {
            "localized": 0,
            "bilateral_or_unilateral": 1,
            "massive_bilateral": 2
        }
        
        # Bronchial pleural fistula scores
        self.fistula_scores = {
            "no": 0,
            "yes": 1
        }
        
        # Severity thresholds
        self.MILD_THRESHOLD = 0
        self.MODERATE_MIN = 1
        self.MODERATE_MAX = 4
        self.SEVERE_THRESHOLD = 5
    
    def calculate(self, pao2_fio2_ratio: float, chest_xray_findings: str, 
                 bronchial_pleural_fistula: str) -> Dict[str, Any]:
        """
        Calculates Blast Lung Injury Severity Score
        
        Args:
            pao2_fio2_ratio (float): PaO₂/FiO₂ ratio in mmHg
            chest_xray_findings (str): Chest X-ray infiltrate findings
            bronchial_pleural_fistula (str): Presence of bronchial pleural fistula
            
        Returns:
            Dict with severity score, category, and clinical recommendations
        """
        
        # Validate inputs
        self._validate_inputs(pao2_fio2_ratio, chest_xray_findings, bronchial_pleural_fistula)
        
        # Calculate component scores
        pao2_score = self._calculate_pao2_score(pao2_fio2_ratio)
        xray_score = self.chest_xray_scores[chest_xray_findings]
        fistula_score = self.fistula_scores[bronchial_pleural_fistula]
        
        # Calculate total score
        total_score = pao2_score + xray_score + fistula_score
        
        # Get interpretation
        interpretation = self._get_interpretation(total_score)
        
        return {
            "result": total_score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, pao2_fio2_ratio, chest_xray_findings, bronchial_pleural_fistula):
        """Validates input parameters"""
        
        # Validate PaO2/FiO2 ratio
        if not isinstance(pao2_fio2_ratio, (int, float)):
            raise ValueError("pao2_fio2_ratio must be a number")
        
        if pao2_fio2_ratio < 20 or pao2_fio2_ratio > 500:
            raise ValueError("pao2_fio2_ratio must be between 20 and 500 mmHg")
        
        # Validate chest X-ray findings
        if chest_xray_findings not in self.chest_xray_scores:
            raise ValueError(f"chest_xray_findings must be one of: {list(self.chest_xray_scores.keys())}")
        
        # Validate bronchial pleural fistula
        if bronchial_pleural_fistula not in self.fistula_scores:
            raise ValueError(f"bronchial_pleural_fistula must be one of: {list(self.fistula_scores.keys())}")
    
    def _calculate_pao2_score(self, pao2_fio2_ratio: float) -> int:
        """
        Calculates PaO₂/FiO₂ ratio component score
        
        Args:
            pao2_fio2_ratio (float): PaO₂/FiO₂ ratio in mmHg
            
        Returns:
            int: Score (0-2 points)
        """
        
        if pao2_fio2_ratio > self.NORMAL_PAO2_FIO2_THRESHOLD:
            return 0
        elif pao2_fio2_ratio >= self.MODERATE_PAO2_FIO2_THRESHOLD:
            return 1
        else:  # pao2_fio2_ratio < 60
            return 2
    
    def _get_interpretation(self, score: int) -> Dict[str, str]:
        """
        Provides clinical interpretation based on blast lung injury severity score
        
        Args:
            score (int): Total blast lung injury severity score (0-5)
            
        Returns:
            Dict with interpretation, stage, and description
        """
        
        if score == self.MILD_THRESHOLD:
            return {
                "stage": "Mild",
                "description": "0 points - Mild blast lung injury",
                "interpretation": "Mild blast lung injury with excellent prognosis. ARDS risk: ~0%, Mortality: ~0%. Recommended ventilation: Volume-controlled or pressure support ventilation. PEEP: ≤5 cm H₂O. Standard respiratory monitoring and supportive care."
            }
        elif self.MODERATE_MIN <= score <= self.MODERATE_MAX:
            return {
                "stage": "Moderate",
                "description": "1-4 points - Moderate blast lung injury",
                "interpretation": "Moderate blast lung injury with intermediate risk. ARDS risk: 33%, Mortality: ~0%. Recommended ventilation: Conventional modes, consider inverse-ratio ventilation if needed. PEEP: 5-10 cm H₂O. Close respiratory monitoring required."
            }
        else:  # score == 5
            return {
                "stage": "Severe",
                "description": "5 points - Severe blast lung injury",
                "interpretation": "Severe blast lung injury with poor prognosis. ARDS risk: 100%, Mortality: 75%. Recommended ventilation: Conventional modes with potential advanced therapies. PEEP: >10 cm H₂O. Consider nitric oxide, high-frequency jet ventilation, independent lung ventilation, or ECMO."
            }


def calculate_blast_lung_injury_severity(pao2_fio2_ratio: float, chest_xray_findings: str, 
                                       bronchial_pleural_fistula: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    Calculates Blast Lung Injury Severity Score to stratify primary blast lung 
    injuries and guide ventilatory treatment. Score evaluates three key factors: 
    PaO₂/FiO₂ ratio, chest X-ray infiltrate pattern, and presence of bronchial 
    pleural fistula. Developed by Pizov et al. for blast injury assessment.
    """
    calculator = BlastLungInjurySeverityCalculator()
    return calculator.calculate(pao2_fio2_ratio, chest_xray_findings, bronchial_pleural_fistula)