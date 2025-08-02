"""
Subtle Anterior STEMI Calculator (4-Variable)

Differentiates normal variant ST elevation (benign early repolarization) from 
anterior STEMI in patients with chest pain and non-diagnostic ECG changes.
Developed by Dr. Stephen Smith to identify subtle anterior wall MI that may 
benefit from urgent percutaneous coronary intervention.

References (Vancouver style):
1. Driver BE, Khalil A, Henry T, Kazmi F, Adil A, Smith SW. A new 4-variable 
   formula to differentiate normal variant ST segment elevation in V2-V4 (early 
   repolarization) from subtle left anterior descending coronary occlusion – 
   Adding QRS amplitude of V2 improves the model. J Electrocardiol. 2017 
   Nov-Dec;50(6):836-843. doi: 10.1016/j.jelectrocard.2017.08.005.
2. Smith SW, Khalil A, Henry TD, Rosas M, Chang RJ, Hocken C, et al. 
   Electrocardiographic differentiation of early repolarization from subtle 
   anterior ST-elevation myocardial infarction. Ann Emerg Med. 2012 
   Jul;60(1):45-56.e2. doi: 10.1016/j.annemergmed.2012.02.015.
"""

from typing import Dict, Any


class SubtleAnteriorStemi4VariableCalculator:
    """Calculator for Subtle Anterior STEMI 4-Variable Score"""
    
    def __init__(self):
        # Formula coefficients from original research
        self.QTC_COEFFICIENT = 0.052
        self.QRS_V2_COEFFICIENT = -0.151
        self.R_WAVE_V4_COEFFICIENT = -0.268
        self.ST_ELEVATION_V3_COEFFICIENT = 1.062
        
        # Diagnostic threshold
        self.STEMI_THRESHOLD = 18.2
        
        # Validation ranges
        self.QTC_MIN = 300
        self.QTC_MAX = 700
        self.QRS_MIN = 0
        self.QRS_MAX = 50
        self.R_WAVE_MIN = 0
        self.R_WAVE_MAX = 50
        self.ST_ELEVATION_MIN = 0
        self.ST_ELEVATION_MAX = 10
    
    def calculate(self, qtc_interval: float, qrs_amplitude_v2: float,
                  r_wave_amplitude_v4: float, st_elevation_v3: float) -> Dict[str, Any]:
        """
        Calculates the Subtle Anterior STEMI 4-Variable Score
        
        This calculator uses four ECG parameters to distinguish between normal 
        variant ST elevation (benign early repolarization) and subtle anterior 
        STEMI that may require urgent intervention. The formula incorporates 
        temporal (QTc interval), morphological (QRS and R wave amplitudes), 
        and ST segment characteristics to provide enhanced diagnostic accuracy.
        
        Args:
            qtc_interval (float): Bazett-corrected QT interval in milliseconds
            qrs_amplitude_v2 (float): QRS amplitude in lead V2 in millimeters
            r_wave_amplitude_v4 (float): R wave amplitude in lead V4 in millimeters
            st_elevation_v3 (float): ST elevation 60ms after J point in V3 in millimeters
            
        Returns:
            Dict with the calculated score and clinical interpretation
        """
        
        # Validate inputs
        self._validate_inputs(qtc_interval, qrs_amplitude_v2, r_wave_amplitude_v4, st_elevation_v3)
        
        # Calculate the score using the 4-variable formula
        score = self._calculate_formula(qtc_interval, qrs_amplitude_v2, r_wave_amplitude_v4, st_elevation_v3)
        
        # Get interpretation
        interpretation = self._get_interpretation(score)
        
        return {
            "result": round(score, 2),
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, qtc_interval: float, qrs_amplitude_v2: float,
                        r_wave_amplitude_v4: float, st_elevation_v3: float):
        """Validates input parameters for the calculation"""
        
        # QTc interval validation
        if not isinstance(qtc_interval, (int, float)):
            raise ValueError("QTc interval must be a number")
        
        if qtc_interval < self.QTC_MIN or qtc_interval > self.QTC_MAX:
            raise ValueError(f"QTc interval must be between {self.QTC_MIN} and {self.QTC_MAX} ms")
        
        # QRS amplitude V2 validation
        if not isinstance(qrs_amplitude_v2, (int, float)):
            raise ValueError("QRS amplitude in V2 must be a number")
        
        if qrs_amplitude_v2 < self.QRS_MIN or qrs_amplitude_v2 > self.QRS_MAX:
            raise ValueError(f"QRS amplitude in V2 must be between {self.QRS_MIN} and {self.QRS_MAX} mm")
        
        # R wave amplitude V4 validation
        if not isinstance(r_wave_amplitude_v4, (int, float)):
            raise ValueError("R wave amplitude in V4 must be a number")
        
        if r_wave_amplitude_v4 < self.R_WAVE_MIN or r_wave_amplitude_v4 > self.R_WAVE_MAX:
            raise ValueError(f"R wave amplitude in V4 must be between {self.R_WAVE_MIN} and {self.R_WAVE_MAX} mm")
        
        # ST elevation V3 validation
        if not isinstance(st_elevation_v3, (int, float)):
            raise ValueError("ST elevation in V3 must be a number")
        
        if st_elevation_v3 < self.ST_ELEVATION_MIN or st_elevation_v3 > self.ST_ELEVATION_MAX:
            raise ValueError(f"ST elevation in V3 must be between {self.ST_ELEVATION_MIN} and {self.ST_ELEVATION_MAX} mm")
    
    def _calculate_formula(self, qtc_interval: float, qrs_amplitude_v2: float,
                          r_wave_amplitude_v4: float, st_elevation_v3: float) -> float:
        """
        Implements the 4-variable formula for subtle anterior STEMI detection
        
        Formula: Score = 0.052 × QTc - 0.151 × QRS_V2 - 0.268 × R_V4 + 1.062 × ST_V3
        
        Args:
            qtc_interval (float): Bazett-corrected QT interval in ms
            qrs_amplitude_v2 (float): QRS amplitude in lead V2 in mm
            r_wave_amplitude_v4 (float): R wave amplitude in lead V4 in mm
            st_elevation_v3 (float): ST elevation 60ms after J point in V3 in mm
            
        Returns:
            float: Calculated score
        """
        
        score = (self.QTC_COEFFICIENT * qtc_interval +
                self.QRS_V2_COEFFICIENT * qrs_amplitude_v2 +
                self.R_WAVE_V4_COEFFICIENT * r_wave_amplitude_v4 +
                self.ST_ELEVATION_V3_COEFFICIENT * st_elevation_v3)
        
        return score
    
    def _get_interpretation(self, score: float) -> Dict[str, str]:
        """
        Determines the clinical interpretation based on the calculated score
        
        Args:
            score (float): Calculated 4-variable score
            
        Returns:
            Dict with stage, description, and detailed interpretation
        """
        
        if score < self.STEMI_THRESHOLD:
            return {
                "stage": "Benign Early Repolarization",
                "description": "Low probability of anterior STEMI",
                "interpretation": (
                    f"Score {score:.2f} is below the diagnostic threshold of {self.STEMI_THRESHOLD}, "
                    f"suggesting benign early repolarization rather than acute coronary occlusion. "
                    f"This indicates a low probability of anterior STEMI requiring urgent intervention. "
                    f"However, clinical correlation is essential - continue to monitor symptoms and "
                    f"consider serial ECGs if chest pain persists or clinical suspicion remains high. "
                    f"The 4-variable formula has 83.3% sensitivity and 87.7% specificity for detecting "
                    f"subtle anterior STEMI."
                )
            }
        else:
            return {
                "stage": "Likely Anterior STEMI",
                "description": "High probability of anterior STEMI",
                "interpretation": (
                    f"Score {score:.2f} meets or exceeds the diagnostic threshold of {self.STEMI_THRESHOLD}, "
                    f"indicating a high probability of anterior STEMI with likely LAD occlusion. "
                    f"This patient may have a subtle but significant anterior wall myocardial infarction "
                    f"that could benefit from urgent percutaneous coronary intervention. Immediate "
                    f"cardiology consultation and consideration for cardiac catheterization are "
                    f"recommended. The 4-variable formula demonstrates 83.3% sensitivity and 87.7% "
                    f"specificity with 85.9% diagnostic accuracy for identifying subtle anterior STEMI."
                )
            }


def calculate_subtle_anterior_stemi_4_variable(qtc_interval: float, qrs_amplitude_v2: float,
                                              r_wave_amplitude_v4: float, st_elevation_v3: float) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    Calculates the Subtle Anterior STEMI 4-Variable Score to differentiate 
    benign early repolarization from subtle anterior STEMI.
    
    Args:
        qtc_interval (float): Bazett-corrected QT interval in ms
        qrs_amplitude_v2 (float): QRS amplitude in lead V2 in mm
        r_wave_amplitude_v4 (float): R wave amplitude in lead V4 in mm
        st_elevation_v3 (float): ST elevation 60ms after J point in V3 in mm
        
    Returns:
        Dict with calculated score and clinical interpretation
    """
    calculator = SubtleAnteriorStemi4VariableCalculator()
    return calculator.calculate(qtc_interval, qrs_amplitude_v2, r_wave_amplitude_v4, st_elevation_v3)