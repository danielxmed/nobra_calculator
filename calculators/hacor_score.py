"""
HACOR Score Calculator

Predicts non-invasive ventilation (NIV) failure in hypoxemic patients. 
HACOR stands for Heart rate, Acidosis, Consciousness, Oxygenation, and Respiratory rate.

References:
1. Duan J, Han X, Bai L, Zhou L, Huang S. Assessment of heart rate, acidosis, 
   consciousness, oxygenation, and respiratory rate to predict noninvasive ventilation 
   failure in hypoxemic patients. Intensive Care Med. 2017;43(2):192-199. 
   doi: 10.1007/s00134-016-4601-3
2. Liu J, Duan J, Bai L, Zhou L. Noninvasive Ventilation Intolerance: Characteristics, 
   Predictors, and Outcomes. Respir Care. 2016;61(3):277-284. doi: 10.4187/respcare.04220
"""

from typing import Dict, Any


class HacorScoreCalculator:
    """Calculator for HACOR Score for predicting NIV failure in hypoxemic patients"""
    
    def __init__(self):
        # HACOR scoring thresholds and points
        pass
    
    def calculate(self, heart_rate: int, ph: float, gcs: int, 
                  pao2_fio2_ratio: int, respiratory_rate: int) -> Dict[str, Any]:
        """
        Calculates the HACOR Score using the provided parameters
        
        Args:
            heart_rate (int): Heart rate in beats per minute
            ph (float): Arterial blood gas pH value
            gcs (int): Glasgow Coma Scale score
            pao2_fio2_ratio (int): PaO₂/FiO₂ ratio in mmHg
            respiratory_rate (int): Respiratory rate in breaths per minute
            
        Returns:
            Dict with the score result and interpretation
        """
        
        # Validations
        self._validate_inputs(heart_rate, ph, gcs, pao2_fio2_ratio, respiratory_rate)
        
        # Calculate HACOR score components
        heart_rate_points = self._calculate_heart_rate_points(heart_rate)
        acidosis_points = self._calculate_acidosis_points(ph)
        consciousness_points = self._calculate_consciousness_points(gcs)
        oxygenation_points = self._calculate_oxygenation_points(pao2_fio2_ratio)
        respiratory_points = self._calculate_respiratory_points(respiratory_rate)
        
        # Calculate total score
        total_score = (heart_rate_points + acidosis_points + consciousness_points + 
                      oxygenation_points + respiratory_points)
        
        # Get interpretation
        interpretation = self._get_interpretation(total_score, heart_rate, ph, gcs, 
                                                pao2_fio2_ratio, respiratory_rate)
        
        return {
            "result": total_score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, heart_rate: int, ph: float, gcs: int, 
                        pao2_fio2_ratio: int, respiratory_rate: int):
        """Validates input parameters"""
        
        # Heart rate validation
        if not isinstance(heart_rate, int) or heart_rate < 30 or heart_rate > 250:
            raise ValueError("Heart rate must be an integer between 30 and 250 bpm")
        
        # pH validation
        if not isinstance(ph, (int, float)) or ph < 6.8 or ph > 7.8:
            raise ValueError("pH must be between 6.8 and 7.8")
        
        # GCS validation
        if not isinstance(gcs, int) or gcs < 3 or gcs > 15:
            raise ValueError("Glasgow Coma Scale must be an integer between 3 and 15")
        
        # PaO2/FiO2 ratio validation
        if not isinstance(pao2_fio2_ratio, int) or pao2_fio2_ratio < 50 or pao2_fio2_ratio > 600:
            raise ValueError("PaO₂/FiO₂ ratio must be an integer between 50 and 600 mmHg")
        
        # Respiratory rate validation
        if not isinstance(respiratory_rate, int) or respiratory_rate < 8 or respiratory_rate > 80:
            raise ValueError("Respiratory rate must be an integer between 8 and 80 breaths/min")
    
    def _calculate_heart_rate_points(self, heart_rate: int) -> int:
        """
        Calculate points for heart rate component
        
        Heart Rate (H):
        - ≤120 beats/min: 0 points
        - ≥121 beats/min: 1 point
        """
        if heart_rate <= 120:
            return 0
        else:  # ≥121
            return 1
    
    def _calculate_acidosis_points(self, ph: float) -> int:
        """
        Calculate points for acidosis component based on pH
        
        Acidosis (A) - pH:
        - ≥7.35: 0 points
        - 7.30–7.34: 2 points
        - 7.25–7.29: 3 points
        - <7.25: 4 points
        """
        if ph >= 7.35:
            return 0
        elif 7.30 <= ph <= 7.34:
            return 2
        elif 7.25 <= ph <= 7.29:
            return 3
        else:  # <7.25
            return 4
    
    def _calculate_consciousness_points(self, gcs: int) -> int:
        """
        Calculate points for consciousness component based on GCS
        
        Consciousness (C) - Glasgow Coma Scale (GCS):
        - 15: 0 points
        - 13-14: 2 points
        - 11-12: 5 points
        - ≤10: 10 points
        """
        if gcs == 15:
            return 0
        elif 13 <= gcs <= 14:
            return 2
        elif 11 <= gcs <= 12:
            return 5
        else:  # ≤10
            return 10
    
    def _calculate_oxygenation_points(self, pao2_fio2_ratio: int) -> int:
        """
        Calculate points for oxygenation component based on PaO₂/FiO₂ ratio
        
        Oxygenation (O) - PaO₂/FiO₂, mm Hg:
        - ≥201: 0 points
        - 176–200: 2 points
        - 151–175: 3 points
        - 126–150: 4 points
        - 101–125: 5 points
        - ≤100: 6 points
        """
        if pao2_fio2_ratio >= 201:
            return 0
        elif 176 <= pao2_fio2_ratio <= 200:
            return 2
        elif 151 <= pao2_fio2_ratio <= 175:
            return 3
        elif 126 <= pao2_fio2_ratio <= 150:
            return 4
        elif 101 <= pao2_fio2_ratio <= 125:
            return 5
        else:  # ≤100
            return 6
    
    def _calculate_respiratory_points(self, respiratory_rate: int) -> int:
        """
        Calculate points for respiratory rate component
        
        Respiratory Rate (R):
        - ≤30 breaths/min: 0 points
        - 31–35: 1 point
        - 36–40: 2 points
        - 41–45: 3 points
        - ≥46: 4 points
        """
        if respiratory_rate <= 30:
            return 0
        elif 31 <= respiratory_rate <= 35:
            return 1
        elif 36 <= respiratory_rate <= 40:
            return 2
        elif 41 <= respiratory_rate <= 45:
            return 3
        else:  # ≥46
            return 4
    
    def _get_interpretation(self, score: int, heart_rate: int, ph: float, gcs: int, 
                           pao2_fio2_ratio: int, respiratory_rate: int) -> Dict[str, str]:
        """
        Determines the interpretation based on the HACOR score
        
        Args:
            score (int): Calculated HACOR score
            heart_rate, ph, gcs, pao2_fio2_ratio, respiratory_rate: Input parameters
            
        Returns:
            Dict with interpretation details
        """
        
        # Format patient characteristics
        patient_summary = (f"Patient characteristics: Heart rate {heart_rate} bpm, "
                          f"pH {ph:.2f}, GCS {gcs}, PaO₂/FiO₂ ratio {pao2_fio2_ratio} mmHg, "
                          f"respiratory rate {respiratory_rate} breaths/min.")
        
        # Determine risk category and recommendations
        if score <= 5:
            stage = "Low Risk"
            description = "Low risk of NIV failure"
            clinical_recs = (
                f"Low risk of non-invasive ventilation failure (HACOR score: {score} points, "
                "≤5 = low risk). Less than 20% probability of NIV failure. "
                "Clinical recommendations: Continue NIV with standard monitoring protocols. "
                "Maintain current respiratory support settings with routine assessment. "
                "Monitor for clinical deterioration including worsening gas exchange, "
                "increased work of breathing, or hemodynamic instability. "
                "Reassess HACOR score periodically (at 12, 24, and 48 hours) to detect "
                "any changes in patient condition. Standard ICU monitoring and supportive "
                "care are appropriate. Consider optimization of NIV settings based on "
                "patient comfort and synchrony."
            )
        else:
            stage = "High Risk"
            description = "High risk of NIV failure"
            clinical_recs = (
                f"High risk of non-invasive ventilation failure (HACOR score: {score} points, "
                ">5 = high risk). Greater than 50% probability of NIV failure. "
                "Clinical recommendations: Consider early intubation within 12 hours to "
                "reduce hospital mortality risk. Intensive monitoring is essential with "
                "preparation for mechanical ventilation. Ensure immediate availability of "
                "intubation equipment and experienced personnel. Consider ICU or HDU-level "
                "care if not already provided. Optimize NIV settings (pressure support, PEEP, "
                "FiO₂) while preparing for potential intubation. Monitor closely for signs "
                "of respiratory fatigue, worsening hypoxemia, or hemodynamic compromise. "
                "Early intubation in high-risk patients has been associated with improved "
                "survival outcomes compared to delayed intubation."
            )
        
        # Important considerations
        considerations = (
            "Important considerations: The HACOR score should be assessed 60 minutes "
            "after initiating NIV for optimal predictive accuracy. This score has been "
            "validated in patients with various causes of hypoxemic respiratory failure "
            "including pneumonia, ARDS, and COPD exacerbations. The score demonstrates "
            "good discriminative ability with AUC 0.88-0.90 in validation studies. "
            "Clinical judgment should always be used in conjunction with the HACOR score "
            "for respiratory management decisions. Reassessment at regular intervals "
            "is recommended as patient condition may change during the course of treatment."
        )
        
        full_interpretation = f"{patient_summary} HACOR Score: {score} points. Risk Category: {stage} ({description}). Clinical recommendations: {clinical_recs} {considerations}"
        
        return {
            "stage": stage,
            "description": description,
            "interpretation": full_interpretation
        }


def calculate_hacor_score(heart_rate: int, ph: float, gcs: int, 
                         pao2_fio2_ratio: int, respiratory_rate: int) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_hacor_score pattern
    """
    calculator = HacorScoreCalculator()
    return calculator.calculate(heart_rate, ph, gcs, pao2_fio2_ratio, respiratory_rate)