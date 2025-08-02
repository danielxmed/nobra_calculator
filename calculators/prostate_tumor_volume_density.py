"""
Prostate Tumor Volume & Density Calculator

Calculates prostate volume using ellipsoid formula and PSA density to help
distinguish between benign prostatic hyperplasia (BPH) and prostate cancer.
Assists in biopsy decision-making and risk stratification.

References:
1. Terris MK, Stamey TA. Determination of prostate volume by transrectal 
   ultrasound. J Urol. 1991;145(5):984-7. doi: 10.1016/s0022-5347(17)38491-9.
2. Benson MC, Whang IS, Olsson CA, McMahon DJ, Cooner WH. The use of prostate 
   specific antigen density to enhance the predictive value of intermediate 
   levels of serum prostate specific antigen. J Urol. 1992;147(3 Pt 2):817-21. 
   doi: 10.1016/s0022-5347(17)37394-9.
"""

import math
from typing import Dict, Any


class ProstateTumorVolumeDensityCalculator:
    """Calculator for Prostate Tumor Volume & Density"""
    
    def __init__(self):
        # Validation ranges
        self.MIN_DIMENSION = 1.0  # cm
        self.MAX_DIMENSION = 20.0  # cm
        self.MIN_PSA = 0.1  # ng/mL
        self.MAX_PSA = 1000.0  # ng/mL
        
        # Clinical thresholds
        self.PSA_DENSITY_LOW_RISK = 0.10
        self.PSA_DENSITY_INTERMEDIATE = 0.15
        self.PSA_DENSITY_HIGH_RISK = 0.20
        
        self.NORMAL_PROSTATE_MIN = 25.0  # mL
        self.NORMAL_PROSTATE_MAX = 30.0  # mL
        self.MILD_ENLARGEMENT = 50.0  # mL
        self.MODERATE_ENLARGEMENT = 80.0  # mL
    
    def calculate(self, prostate_length: float, prostate_width: float, 
                  prostate_height: float, psa_value: float) -> Dict[str, Any]:
        """
        Calculates prostate volume and PSA density
        
        Args:
            prostate_length (float): Anteroposterior diameter in cm
            prostate_width (float): Transverse diameter in cm
            prostate_height (float): Craniocaudal diameter in cm
            psa_value (float): PSA level in ng/mL
            
        Returns:
            Dict with prostate volume, PSA density, and interpretations
        """
        
        # Validate inputs
        self._validate_inputs(prostate_length, prostate_width, prostate_height, psa_value)
        
        # Calculate prostate volume using ellipsoid formula
        # Volume = Length × Width × Height × π/6
        prostate_volume = prostate_length * prostate_width * prostate_height * (math.pi / 6)
        
        # Round to 1 decimal place
        prostate_volume = round(prostate_volume, 1)
        
        # Calculate PSA density
        psa_density = psa_value / prostate_volume
        psa_density = round(psa_density, 3)
        
        # Get interpretations
        volume_interpretation = self._get_volume_interpretation(prostate_volume)
        density_interpretation = self._get_density_interpretation(psa_density)
        
        # Generate overall clinical interpretation
        overall_interpretation = self._get_overall_interpretation(
            prostate_volume, psa_density, volume_interpretation, density_interpretation
        )
        
        return {
            "result": {
                "prostate_volume": prostate_volume,
                "psa_density": psa_density,
                "volume_interpretation": volume_interpretation,
                "density_interpretation": density_interpretation
            },
            "unit": "volume: mL, density: ng/mL²",
            "interpretation": overall_interpretation,
            "stage": density_interpretation["stage"],
            "stage_description": f"Volume: {volume_interpretation['stage']}, PSA Density: {density_interpretation['stage']}"
        }
    
    def _validate_inputs(self, length: float, width: float, height: float, psa: float):
        """Validates input parameters"""
        
        if not all(isinstance(x, (int, float)) for x in [length, width, height, psa]):
            raise ValueError("All measurements must be numbers")
        
        if not (self.MIN_DIMENSION <= length <= self.MAX_DIMENSION):
            raise ValueError(f"Prostate length must be between {self.MIN_DIMENSION} and {self.MAX_DIMENSION} cm")
        
        if not (self.MIN_DIMENSION <= width <= self.MAX_DIMENSION):
            raise ValueError(f"Prostate width must be between {self.MIN_DIMENSION} and {self.MAX_DIMENSION} cm")
        
        if not (self.MIN_DIMENSION <= height <= self.MAX_DIMENSION):
            raise ValueError(f"Prostate height must be between {self.MIN_DIMENSION} and {self.MAX_DIMENSION} cm")
        
        if not (self.MIN_PSA <= psa <= self.MAX_PSA):
            raise ValueError(f"PSA value must be between {self.MIN_PSA} and {self.MAX_PSA} ng/mL")
    
    def _get_volume_interpretation(self, volume: float) -> Dict[str, str]:
        """
        Determines volume interpretation based on prostate size
        
        Args:
            volume (float): Calculated prostate volume in mL
            
        Returns:
            Dict with volume interpretation
        """
        
        if volume < self.NORMAL_PROSTATE_MIN:
            return {
                "stage": "Small",
                "description": "Small prostate volume",
                "interpretation": "Below normal size, may indicate underdevelopment or atrophy."
            }
        elif volume <= self.NORMAL_PROSTATE_MAX:
            return {
                "stage": "Normal",
                "description": "Normal prostate volume",
                "interpretation": "Normal prostate size for adult males."
            }
        elif volume <= self.MILD_ENLARGEMENT:
            return {
                "stage": "Mildly Enlarged",
                "description": "Mild benign prostatic hyperplasia",
                "interpretation": "Mild enlargement, may cause some urinary symptoms."
            }
        elif volume <= self.MODERATE_ENLARGEMENT:
            return {
                "stage": "Moderately Enlarged",
                "description": "Moderate benign prostatic hyperplasia",
                "interpretation": "Moderate enlargement, likely causing urinary symptoms."
            }
        else:
            return {
                "stage": "Severely Enlarged",
                "description": "Severe benign prostatic hyperplasia",
                "interpretation": "Severe enlargement, likely causing significant urinary obstruction."
            }
    
    def _get_density_interpretation(self, density: float) -> Dict[str, str]:
        """
        Determines PSA density interpretation for cancer risk
        
        Args:
            density (float): Calculated PSA density in ng/mL²
            
        Returns:
            Dict with density interpretation
        """
        
        if density < self.PSA_DENSITY_LOW_RISK:
            return {
                "stage": "Low Risk",
                "description": "Low cancer risk",
                "interpretation": "Very low probability of clinically significant prostate cancer."
            }
        elif density < self.PSA_DENSITY_INTERMEDIATE:
            return {
                "stage": "Intermediate Risk",
                "description": "Intermediate cancer risk",
                "interpretation": "Moderate probability of prostate cancer, consider additional evaluation."
            }
        elif density < self.PSA_DENSITY_HIGH_RISK:
            return {
                "stage": "High Risk",
                "description": "High cancer risk",
                "interpretation": "High probability of prostate cancer, biopsy strongly recommended."
            }
        else:
            return {
                "stage": "Very High Risk",
                "description": "Very high cancer risk",
                "interpretation": "Very high probability of clinically significant prostate cancer."
            }
    
    def _get_overall_interpretation(self, volume: float, density: float, 
                                   volume_interp: Dict, density_interp: Dict) -> str:
        """
        Generates comprehensive clinical interpretation
        
        Args:
            volume (float): Prostate volume
            density (float): PSA density
            volume_interp (Dict): Volume interpretation
            density_interp (Dict): Density interpretation
            
        Returns:
            str: Overall clinical interpretation
        """
        
        return (f"PROSTATE VOLUME: {volume} mL ({volume_interp['stage']}) - "
                f"{volume_interp['interpretation']} "
                f"PSA DENSITY: {density:.3f} ng/mL² ({density_interp['stage']}) - "
                f"{density_interp['interpretation']} "
                f"CLINICAL CORRELATION: "
                f"{'Large prostate volume may account for elevated PSA, reducing cancer suspicion. ' if volume > 50 else ''}"
                f"{'Small prostate with elevated PSA density increases cancer concern. ' if volume < 30 and density > 0.15 else ''}"
                f"RECOMMENDATIONS: "
                f"{'Consider prostate biopsy given high PSA density. ' if density >= 0.15 else ''}"
                f"{'Monitor with serial PSA and consider advanced imaging. ' if 0.10 <= density < 0.15 else ''}"
                f"{'Low cancer risk, continue routine screening. ' if density < 0.10 else ''}"
                f"Consider clinical context, DRE findings, and patient risk factors for final management decisions.")


def calculate_prostate_tumor_volume_density(prostate_length: float, prostate_width: float, 
                                          prostate_height: float, psa_value: float) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = ProstateTumorVolumeDensityCalculator()
    return calculator.calculate(prostate_length, prostate_width, prostate_height, psa_value)