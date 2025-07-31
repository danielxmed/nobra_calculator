"""
Expanded Disability Status Scale (EDSS) / Functional Systems Score (FSS) Calculator

Describes severity of disability in MS patients based on functional systems assessment 
and ambulatory ability. The most widely used disability scale for multiple sclerosis.

References:
- Kurtzke JF. Rating neurologic impairment in multiple sclerosis: an expanded 
  disability status scale (EDSS). Neurology. 1983 Nov;33(11):1444-52.
"""

import math
from typing import Dict, Any


class EdssCalculator:
    """Calculator for Expanded Disability Status Scale (EDSS)"""
    
    def __init__(self):
        # No constants needed for this calculator
        pass
    
    def calculate(self, pyramidal: int, cerebellar: int, brainstem: int, 
                 sensory: int, bowel_bladder: int, visual: int, 
                 cerebral: int, ambulation: int) -> Dict[str, Any]:
        """
        Calculates the EDSS score using functional systems scores
        
        Args:
            pyramidal (int): Pyramidal Functions score (0-6)
            cerebellar (int): Cerebellar Functions score (0-5)
            brainstem (int): Brainstem Functions score (0-5)
            sensory (int): Sensory Functions score (0-6)
            bowel_bladder (int): Bowel and Bladder Functions score (0-6)
            visual (int): Visual Functions score (0-6)
            cerebral (int): Cerebral Functions score (0-5)
            ambulation (int): Ambulation score (0-10)
            
        Returns:
            Dict with the EDSS score and interpretation
        """
        
        # Validations
        self._validate_inputs(pyramidal, cerebellar, brainstem, sensory, 
                           bowel_bladder, visual, cerebral, ambulation)
        
        # Convert visual and bowel/bladder scores if needed
        visual_converted = self._convert_visual_score(visual)
        bowel_bladder_converted = self._convert_bowel_bladder_score(bowel_bladder)
        
        # Create functional systems list with converted values
        fs_scores = [
            pyramidal,
            cerebellar,
            brainstem,
            sensory,
            bowel_bladder_converted,
            visual_converted,
            cerebral
        ]
        
        # Calculate EDSS based on ambulation and functional systems
        result = self._calculate_edss(fs_scores, ambulation)
        
        # Get interpretation
        interpretation = self._get_interpretation(result)
        
        return {
            "result": result,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation.get("stage", ""),
            "stage_description": interpretation.get("description", "")
        }
    
    def _validate_inputs(self, pyramidal, cerebellar, brainstem, sensory, 
                        bowel_bladder, visual, cerebral, ambulation):
        """Validates input parameters"""
        
        # Validate pyramidal (0-6)
        if not isinstance(pyramidal, int) or pyramidal < 0 or pyramidal > 6:
            raise ValueError("Pyramidal score must be between 0 and 6")
        
        # Validate cerebellar (0-5)
        if not isinstance(cerebellar, int) or cerebellar < 0 or cerebellar > 5:
            raise ValueError("Cerebellar score must be between 0 and 5")
        
        # Validate brainstem (0-5)
        if not isinstance(brainstem, int) or brainstem < 0 or brainstem > 5:
            raise ValueError("Brainstem score must be between 0 and 5")
        
        # Validate sensory (0-6)
        if not isinstance(sensory, int) or sensory < 0 or sensory > 6:
            raise ValueError("Sensory score must be between 0 and 6")
        
        # Validate bowel_bladder (0-6)
        if not isinstance(bowel_bladder, int) or bowel_bladder < 0 or bowel_bladder > 6:
            raise ValueError("Bowel/bladder score must be between 0 and 6")
        
        # Validate visual (0-6)
        if not isinstance(visual, int) or visual < 0 or visual > 6:
            raise ValueError("Visual score must be between 0 and 6")
        
        # Validate cerebral (0-5)
        if not isinstance(cerebral, int) or cerebral < 0 or cerebral > 5:
            raise ValueError("Cerebral score must be between 0 and 5")
        
        # Validate ambulation (0-10)
        if not isinstance(ambulation, int) or ambulation < 0 or ambulation > 10:
            raise ValueError("Ambulation score must be between 0 and 10")
    
    def _convert_visual_score(self, visual: int) -> int:
        """Converts visual score for EDSS calculation"""
        # Visual scores 5 and 6 are converted to 4 for EDSS calculation
        if visual >= 5:
            return 4
        return visual
    
    def _convert_bowel_bladder_score(self, bowel_bladder: int) -> int:
        """Converts bowel/bladder score for EDSS calculation"""
        # Bowel/bladder score 6 is converted to 5 for EDSS calculation
        if bowel_bladder == 6:
            return 5
        return bowel_bladder
    
    def _calculate_edss(self, fs_scores: list, ambulation: int) -> float:
        """
        Calculates EDSS based on functional systems and ambulation
        
        Args:
            fs_scores (list): List of functional system scores
            ambulation (int): Ambulation score
            
        Returns:
            float: EDSS score
        """
        
        # Count functional systems with each score
        fs_count = {}
        for score in fs_scores:
            if score > 0:
                fs_count[score] = fs_count.get(score, 0) + 1
        
        # Get maximum FS score
        max_fs = max(fs_scores) if fs_scores else 0
        
        # Special rule: If 5 FS are grade 2, EDSS is 5.0
        if fs_count.get(2, 0) >= 5:
            return 5.0
        
        # For ambulatory patients (ambulation < 5), use FS-based calculation
        if ambulation < 5:
            # EDSS 0: All FS are 0
            if max_fs == 0:
                return 0.0
            
            # EDSS 1.0-1.5: Based on number of FS with score 1
            elif max_fs == 1:
                count_1 = fs_count.get(1, 0)
                if count_1 == 1:
                    return 1.0
                else:
                    return 1.5
            
            # EDSS 2.0-2.5: Based on FS with score 2
            elif max_fs == 2:
                count_2 = fs_count.get(2, 0)
                count_1 = fs_count.get(1, 0)
                if count_2 == 1 and count_1 <= 1:
                    return 2.0
                else:
                    return 2.5
            
            # EDSS 3.0-3.5: Based on FS with score 3
            elif max_fs == 3:
                count_3 = fs_count.get(3, 0)
                count_2 = fs_count.get(2, 0)
                if count_3 == 1 and count_2 <= 1:
                    return 3.0
                else:
                    return 3.5
            
            # EDSS 4.0-4.5: Based on FS with score 4 or higher
            elif max_fs >= 4:
                if ambulation >= 4:
                    return 4.5
                else:
                    return 4.0
        
        # For non-ambulatory patients (ambulation >= 5), use ambulation-based calculation
        else:
            # Direct mapping from ambulation score to EDSS
            if ambulation == 5:
                return 5.0 if max_fs < 4 else 5.5
            elif ambulation == 6:
                return 6.0 if max_fs < 4 else 6.5
            elif ambulation == 7:
                return 7.0 if max_fs < 5 else 7.5
            elif ambulation == 8:
                return 8.0 if max_fs < 5 else 8.5
            elif ambulation == 9:
                return 9.0 if max_fs < 5 else 9.5
            elif ambulation >= 10:
                return 10.0
        
        # Default case (should not reach here)
        return float(ambulation)
    
    def _get_interpretation(self, result: float) -> Dict[str, str]:
        """
        Determines the interpretation based on the EDSS score
        
        Args:
            result (float): EDSS score
            
        Returns:
            Dict with interpretation
        """
        
        if result == 0.0:
            return {
                "stage": "Normal",
                "description": "Normal neurological exam",
                "interpretation": "Normal neurological examination. All grade 0 in all functional systems."
            }
        elif result >= 1.0 and result <= 1.5:
            return {
                "stage": "Minimal Disability",
                "description": "No disability, minimal signs",
                "interpretation": "No disability, minimal signs in one or more functional systems."
            }
        elif result >= 2.0 and result <= 2.5:
            return {
                "stage": "Mild Disability",
                "description": "Minimal disability in one FS",
                "interpretation": "Minimal disability in one functional system."
            }
        elif result >= 3.0 and result <= 3.5:
            return {
                "stage": "Moderate Disability",
                "description": "Moderate disability in one FS",
                "interpretation": "Moderate disability in one functional system or mild disability in three or four functional systems though fully ambulatory."
            }
        elif result >= 4.0 and result <= 4.5:
            return {
                "stage": "Relatively Severe Disability",
                "description": "Fully ambulatory without aid",
                "interpretation": "Fully ambulatory without aid, self-sufficient, up and about some 12 hours a day despite relatively severe disability. Able to walk without aid or rest for 500m."
            }
        elif result >= 5.0 and result <= 5.5:
            return {
                "stage": "Disability Severe Enough",
                "description": "Ambulatory without aid for 200m",
                "interpretation": "Ambulatory without aid or rest for about 200 meters; disability severe enough to impair full daily activities."
            }
        elif result >= 6.0 and result <= 6.5:
            return {
                "stage": "Assistance Required",
                "description": "Intermittent or constant assistance required",
                "interpretation": "Intermittent or unilateral constant assistance (cane, crutch, brace) required to walk about 100 meters with or without resting."
            }
        elif result >= 7.0 and result <= 7.5:
            return {
                "stage": "Restricted to Wheelchair",
                "description": "Unable to walk beyond 5m",
                "interpretation": "Unable to walk beyond approximately 5 meters even with aid, essentially restricted to wheelchair."
            }
        elif result >= 8.0 and result <= 8.5:
            return {
                "stage": "Restricted to Bed or Chair",
                "description": "Essentially restricted to bed/chair",
                "interpretation": "Essentially restricted to bed or chair or perambulated in wheelchair, but out of bed most of day; retains many self-care functions."
            }
        elif result >= 9.0 and result <= 9.5:
            return {
                "stage": "Helpless Bed Patient",
                "description": "Helpless bed patient",
                "interpretation": "Helpless bed patient; can communicate and eat."
            }
        else:  # result == 10.0
            return {
                "stage": "Death",
                "description": "Death due to MS",
                "interpretation": "Death due to MS."
            }


def calculate_edss(pyramidal, cerebellar, brainstem, sensory, 
                  bowel_bladder, visual, cerebral, ambulation) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = EdssCalculator()
    return calculator.calculate(pyramidal, cerebellar, brainstem, sensory,
                              bowel_bladder, visual, cerebral, ambulation)