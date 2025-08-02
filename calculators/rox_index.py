"""
ROX Index for Intubation after HFNC Calculator

Predicts high-flow nasal cannula (HFNC) failure and need for intubation in patients 
with acute hypoxemic respiratory failure. The ROX Index combines oxygen saturation, 
fraction of inspired oxygen, and respiratory rate to provide early prediction of 
treatment success or failure.

References (Vancouver style):
1. Roca O, Messika J, Caralt B, García-de-Acilu M, Sztrymf B, Ricard JD, Masclans JR. 
   Predicting success of high-flow nasal cannula in pneumonia patients with hypoxemic 
   respiratory failure: The utility of the ROX index. J Crit Care. 2016 Oct;35:200-5. 
   doi: 10.1016/j.jcrc.2016.05.022.
2. Roca O, Caralt B, Messika J, Samper M, Sztrymf B, Hernández G, García-de-Acilu M, 
   Frat JP, Masclans JR, Ricard JD. An Index Combining Respiratory Rate and Oxygenation 
   to Predict Outcome of Nasal High-Flow Therapy. Am J Respir Crit Care Med. 
   2019 Jun 1;199(11):1368-1376. doi: 10.1164/rccm.201803-0589OC.
3. Suliman LA, Abdelgawad TT, Farrag NS, Abdelwahab HW. Validity of ROX index in 
   prediction of risk of intubation in patients with COVID-19 pneumonia. Adv Respir Med. 
   2021;89(1):1-6. doi: 10.5603/ARM.a2020.0176.
"""

from typing import Dict, Any


class RoxIndexCalculator:
    """Calculator for ROX Index for HFNC failure prediction"""
    
    def __init__(self):
        # ROX Index thresholds based on validation studies
        self.HIGH_RISK_THRESHOLD = 3.85      # <3.85 = high risk for HFNC failure
        self.LOWER_RISK_THRESHOLD = 4.88     # ≥4.88 = lower risk for intubation
        
        # Time-specific thresholds for enhanced prediction
        self.THRESHOLD_2_HOURS = 2.85        # 98-99% specificity at 2 hours
        self.THRESHOLD_6_HOURS = 3.47        # 98-99% specificity at 6 hours
        self.THRESHOLD_12_HOURS = 3.85       # 98-99% specificity at 12 hours
        
        # Performance characteristics
        self.SENSITIVITY = 0.67              # Pooled sensitivity from meta-analysis
        self.SPECIFICITY = 0.72              # Pooled specificity from meta-analysis
        self.PPV_SUCCESS = 0.80              # >80% PPV for HFNC success when ROX ≥4.88
        
        # Optimal confidence interval range
        self.OPTIMAL_RANGE_MIN = 4.2
        self.OPTIMAL_RANGE_MAX = 5.4
    
    def calculate(self, spo2: int, fio2: float, respiratory_rate: int) -> Dict[str, Any]:
        """
        Calculates the ROX Index for HFNC failure prediction
        
        The ROX Index is defined as the ratio of SpO2/FiO2 to respiratory rate,
        providing a simple bedside tool for predicting high-flow nasal cannula
        success or failure in patients with acute hypoxemic respiratory failure.
        
        Args:
            spo2 (int): Pulse oximetry oxygen saturation (70-100%)
            fio2 (float): Fraction of inspired oxygen (0.21-1.0)
            respiratory_rate (int): Current respiratory rate (10-50 breaths/min)
            
        Returns:
            Dict with the ROX index value and clinical interpretation
        """
        
        # Validate inputs
        self._validate_inputs(spo2, fio2, respiratory_rate)
        
        # Calculate ROX Index
        rox_value = self._calculate_rox_index(spo2, fio2, respiratory_rate)
        
        # Determine risk category and interpretation
        interpretation = self._get_interpretation(rox_value)
        
        return {
            "result": round(rox_value, 2),
            "unit": "index",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, spo2: int, fio2: float, respiratory_rate: int):
        """Validates input parameters for ROX Index calculation"""
        
        # SpO2 validation
        if not isinstance(spo2, int):
            raise ValueError("SpO2 must be an integer")
        
        if spo2 < 70 or spo2 > 100:
            raise ValueError("SpO2 must be between 70% and 100%")
        
        # FiO2 validation
        if not isinstance(fio2, (int, float)):
            raise ValueError("FiO2 must be a number")
        
        if fio2 < 0.21 or fio2 > 1.0:
            raise ValueError("FiO2 must be between 0.21 (21%) and 1.0 (100%)")
        
        # Respiratory rate validation
        if not isinstance(respiratory_rate, int):
            raise ValueError("Respiratory rate must be an integer")
        
        if respiratory_rate < 10 or respiratory_rate > 50:
            raise ValueError("Respiratory rate must be between 10 and 50 breaths/min")
        
        # Clinical validity checks
        if spo2 < 85 and fio2 < 0.4:
            raise ValueError("Clinical concern: Low SpO2 with low FiO2 - verify accuracy of measurements")
        
        if respiratory_rate > 35 and spo2 > 95:
            raise ValueError("Clinical concern: High respiratory rate with good oxygenation - consider non-respiratory causes")
    
    def _calculate_rox_index(self, spo2: int, fio2: float, respiratory_rate: int) -> float:
        """
        Calculates the ROX Index using the standard formula
        
        ROX Index = (SpO2/FiO2) / Respiratory Rate
        
        Args:
            spo2 (int): Oxygen saturation percentage
            fio2 (float): Fraction of inspired oxygen
            respiratory_rate (int): Respiratory rate in breaths per minute
            
        Returns:
            float: Calculated ROX Index value
        """
        
        # Convert FiO2 to percentage if given as fraction
        if fio2 <= 1.0:
            fio2_percent = fio2 * 100
        else:
            fio2_percent = fio2
        
        # Calculate SpO2/FiO2 ratio
        spo2_fio2_ratio = spo2 / fio2_percent * 100
        
        # Calculate ROX Index
        rox_index = spo2_fio2_ratio / respiratory_rate
        
        return rox_index
    
    def _get_interpretation(self, rox_value: float) -> Dict[str, str]:
        """
        Provides detailed clinical interpretation based on ROX Index value
        
        Args:
            rox_value (float): Calculated ROX Index
            
        Returns:
            Dict with stage, description, and detailed interpretation
        """
        
        if rox_value < self.HIGH_RISK_THRESHOLD:
            return {
                "stage": "High Risk for HFNC Failure",
                "description": "Early intubation consideration",
                "interpretation": (
                    f"High risk of HFNC failure requiring early intubation consideration. "
                    f"This ROX index value ({rox_value:.2f}) indicates poor response to high-flow "
                    f"nasal cannula therapy with significant risk for treatment failure. Prepare for "
                    f"early intubation and invasive mechanical ventilation. Optimize underlying "
                    f"conditions and consider alternative respiratory support strategies. Never delay "
                    f"intubation when clinical signs indicate impending respiratory decompensation. "
                    f"Monitor closely for signs of respiratory distress, work of breathing, and "
                    f"clinical deterioration."
                )
            }
        
        elif rox_value < self.LOWER_RISK_THRESHOLD:
            return {
                "stage": "Indeterminate Risk",
                "description": "Reassess in 1-2 hours",
                "interpretation": (
                    f"Indeterminate range requiring close monitoring and reassessment in 1-2 hours. "
                    f"This ROX index value ({rox_value:.2f}) suggests uncertain prognosis with HFNC "
                    f"therapy. Optimize HFNC settings, treat underlying respiratory condition "
                    f"aggressively, and reassess ROX index within 1-2 hours. Consider factors "
                    f"contributing to respiratory failure and address reversible causes. Maintain "
                    f"high level of vigilance for clinical deterioration and be prepared for "
                    f"escalation to invasive ventilation if ROX index trends downward or clinical "
                    f"condition worsens."
                )
            }
        
        else:  # rox_value >= self.LOWER_RISK_THRESHOLD
            optimal_range_note = ""
            if self.OPTIMAL_RANGE_MIN <= rox_value <= self.OPTIMAL_RANGE_MAX:
                optimal_range_note = " This value falls within the optimal confidence interval (4.2-5.4) for HFNC success prediction."
            
            return {
                "stage": "Lower Risk for Intubation",
                "description": "Continue HFNC and wean FiO2",
                "interpretation": (
                    f"Lower risk for intubation with good response to HFNC therapy. This ROX index "
                    f"value ({rox_value:.2f}) suggests successful treatment with high-flow nasal "
                    f"cannula and low likelihood of requiring intubation.{optimal_range_note} "
                    f"Continue current HFNC therapy and consider weaning FiO2 as tolerated while "
                    f"maintaining adequate oxygenation. Monitor for continued improvement and plan "
                    f"for further de-escalation of respiratory support. Maintain standard monitoring "
                    f"protocols and continue treatment of underlying respiratory pathology. This "
                    f"favorable ROX index indicates effective HFNC therapy with good prognosis for "
                    f"avoiding invasive mechanical ventilation."
                )
            }


def calculate_rox_index(spo2: int, fio2: float, respiratory_rate: int) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    Calculates ROX Index for predicting HFNC failure and need for intubation.
    
    Args:
        spo2 (int): Pulse oximetry oxygen saturation (70-100%)
        fio2 (float): Fraction of inspired oxygen (0.21-1.0)
        respiratory_rate (int): Current respiratory rate (10-50 breaths/min)
        
    Returns:
        Dict with ROX index value and clinical interpretation
    """
    calculator = RoxIndexCalculator()
    return calculator.calculate(spo2, fio2, respiratory_rate)