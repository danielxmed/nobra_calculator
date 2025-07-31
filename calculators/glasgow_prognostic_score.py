"""
Glasgow Prognostic Score (GPS) Calculator

The Glasgow Prognostic Score is an inflammation and nutrition-based prognostic 
score for cancer patients using serum C-reactive protein and albumin levels. It 
reflects both the presence of systemic inflammatory response (CRP) and progressive 
nutritional decline (albumin) in cancer patients. The GPS has been extensively 
validated across multiple cancer types and is one of the most widely used 
systemic inflammation-based prognostic scores in oncology.

References (Vancouver style):
1. Forrest LM, McMillan DC, McArdle CS, Angerson WJ, Dunlop DJ. Evaluation of 
   cumulative prognostic scores based on the systemic inflammatory response in 
   patients with inoperable non-small-cell lung cancer. Br J Cancer. 2003;89(5):1028-1030.
2. McMillan DC. The systemic inflammation-based Glasgow Prognostic Score: a decade 
   of experience in patients with cancer. Cancer Treat Rev. 2013;39(5):534-540. 
   doi: 10.1016/j.ctrv.2012.08.003.
3. Roxburgh CS, McMillan DC. Role of systemic inflammatory response in predicting 
   survival in patients with primary operable cancer. Future Oncol. 2010;6(1):149-163. 
   doi: 10.2217/fon.09.136.
4. Proctor MJ, Morrison DS, Talwar D, et al. A comparison of inflammation-based 
   prognostic scores in patients with cancer. A Glasgow Inflammation Outcome Study. 
   Eur J Cancer. 2011;47(17):2633-2641. doi: 10.1016/j.ejca.2011.03.028.
"""

from typing import Dict, Any


class GlasgowPrognosticScoreCalculator:
    """Calculator for Glasgow Prognostic Score (GPS)"""
    
    def __init__(self):
        # Cut-off thresholds
        self.CRP_THRESHOLD = 1.0  # mg/dL
        self.ALBUMIN_THRESHOLD = 3.5  # g/dL
        
        # Score descriptions
        self.SCORE_DESCRIPTIONS = {
            0: "Low risk - Normal inflammation and nutrition",
            1: "Intermediate risk - Mild inflammation or nutritional compromise", 
            2: "High risk - Severe inflammation and nutritional compromise"
        }
    
    def calculate(self, crp: float, albumin: float, score_type: str) -> Dict[str, Any]:
        """
        Calculates Glasgow Prognostic Score using CRP and albumin levels
        
        Args:
            crp (float): C-reactive protein level in mg/dL
            albumin (float): Serum albumin level in g/dL
            score_type (str): Type of GPS calculation ("original" or "modified")
            
        Returns:
            Dict with the GPS score and clinical interpretation
        """
        
        # Validate inputs
        self._validate_inputs(crp, albumin, score_type)
        
        # Calculate GPS score
        gps_score = self._calculate_gps(crp, albumin, score_type)
        
        # Get interpretation
        interpretation = self._get_interpretation(gps_score, crp, albumin, score_type)
        
        return {
            "result": gps_score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, crp: float, albumin: float, score_type: str):
        """Validates input parameters"""
        
        if not isinstance(crp, (int, float)) or crp < 0 or crp > 50:
            raise ValueError("CRP must be a number between 0 and 50 mg/dL")
        
        if not isinstance(albumin, (int, float)) or albumin < 1.0 or albumin > 6.0:
            raise ValueError("Albumin must be a number between 1.0 and 6.0 g/dL")
        
        if score_type not in ["original", "modified"]:
            raise ValueError("Score type must be 'original' or 'modified'")
    
    def _calculate_gps(self, crp: float, albumin: float, score_type: str) -> int:
        """
        Calculates the GPS score based on CRP and albumin levels
        
        Args:
            crp (float): C-reactive protein level in mg/dL
            albumin (float): Serum albumin level in g/dL
            score_type (str): Type of GPS calculation
            
        Returns:
            int: GPS score (0, 1, or 2)
        """
        
        # Determine if parameters are abnormal
        crp_elevated = crp > self.CRP_THRESHOLD
        albumin_low = albumin < self.ALBUMIN_THRESHOLD
        
        if score_type == "original":
            # Original GPS
            if crp_elevated and albumin_low:
                return 2  # Both abnormal
            elif crp_elevated or albumin_low:
                return 1  # One abnormal
            else:
                return 0  # Both normal
        
        else:  # modified GPS
            # Modified GPS - prioritizes CRP elevation
            if crp_elevated and albumin_low:
                return 2  # Both abnormal
            elif crp_elevated and not albumin_low:
                return 1  # Only CRP elevated
            else:
                return 0  # CRP normal (regardless of albumin)
    
    def _get_interpretation(self, gps_score: int, crp: float, albumin: float, 
                          score_type: str) -> Dict[str, str]:
        """
        Provides clinical interpretation based on the GPS score
        
        Args:
            gps_score (int): Calculated GPS score
            crp (float): C-reactive protein level
            albumin (float): Albumin level
            score_type (str): Type of GPS calculation
            
        Returns:
            Dict with interpretation details
        """
        
        # Build laboratory summary
        crp_status = "elevated" if crp > self.CRP_THRESHOLD else "normal"
        albumin_status = "low" if albumin < self.ALBUMIN_THRESHOLD else "normal"
        
        lab_summary = f"CRP: {crp:.1f} mg/dL ({crp_status}), Albumin: {albumin:.1f} g/dL ({albumin_status})"
        
        score_name = "GPS" if score_type == "original" else "mGPS"
        
        if gps_score == 0:
            return {
                "stage": "GPS 0",
                "description": "Low risk - Normal inflammation and nutrition",
                "interpretation": (
                    f"{score_name}: {gps_score}/2. [{lab_summary}]. "
                    f"Low risk category with normal inflammatory markers and nutritional status. "
                    f"CRP ≤1.0 mg/dL indicates minimal systemic inflammatory response. "
                    f"Albumin {'≥3.5 g/dL' if score_type == 'original' else 'level acceptable'} "
                    f"suggests adequate nutritional status and liver synthetic function. "
                    f"This profile is associated with the best prognosis and longest survival "
                    f"in cancer patients. Continue routine oncological management and monitoring. "
                    f"Consider this favorable prognostic indicator in treatment planning and "
                    f"patient counseling regarding expected outcomes."
                )
            }
        elif gps_score == 1:
            intermediate_explanation = ""
            if score_type == "original":
                if crp > self.CRP_THRESHOLD and albumin >= self.ALBUMIN_THRESHOLD:
                    intermediate_explanation = "elevated inflammatory response with preserved nutrition"
                elif crp <= self.CRP_THRESHOLD and albumin < self.ALBUMIN_THRESHOLD:
                    intermediate_explanation = "nutritional compromise without significant inflammation"
                else:
                    intermediate_explanation = "mild systemic dysfunction"
            else:  # modified GPS
                intermediate_explanation = "elevated inflammatory response with preserved albumin"
            
            return {
                "stage": "GPS 1", 
                "description": "Intermediate risk - Mild inflammation or nutritional compromise",
                "interpretation": (
                    f"{score_name}: {gps_score}/2. [{lab_summary}]. "
                    f"Intermediate risk category indicating {intermediate_explanation}. "
                    f"{'Either elevated CRP or low albumin present' if score_type == 'original' else 'Elevated CRP with normal albumin'}. "
                    f"This profile suggests either systemic inflammatory response or nutritional "
                    f"compromise affecting cancer prognosis. Associated with intermediate survival "
                    f"outcomes. Consider nutritional assessment and support if albumin is low. "
                    f"Monitor inflammatory markers and consider anti-inflammatory interventions "
                    f"if clinically appropriate. This score may influence treatment intensity "
                    f"and supportive care decisions."
                )
            }
        else:  # GPS score = 2
            return {
                "stage": "GPS 2",
                "description": "High risk - Severe inflammation and nutritional compromise", 
                "interpretation": (
                    f"{score_name}: {gps_score}/2. [{lab_summary}]. "
                    f"High risk category with both elevated inflammatory response and nutritional "
                    f"compromise. CRP >1.0 mg/dL indicates significant systemic inflammation. "
                    f"Albumin <3.5 g/dL suggests nutritional decline and possibly impaired liver "
                    f"synthetic function. This combination reflects advanced systemic effects of "
                    f"cancer and is associated with the worst prognosis and shortest survival. "
                    f"Consider aggressive nutritional support, anti-inflammatory measures if "
                    f"appropriate, and discussion of goals of care. This score may warrant "
                    f"modification of treatment intensity and enhanced supportive care measures. "
                    f"Close monitoring and multidisciplinary team involvement recommended."
                )
            }


def calculate_glasgow_prognostic_score(crp: float, albumin: float, score_type: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_glasgow_prognostic_score pattern
    """
    calculator = GlasgowPrognosticScoreCalculator()
    return calculator.calculate(crp, albumin, score_type)