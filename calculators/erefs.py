"""
Eosinophilic Esophagitis Endoscopic Reference Score (EREFS) Calculator

Assesses severity of endoscopic findings in patients with eosinophilic esophagitis
using standardized scoring of five major endoscopic features.

References:
1. Hirano I, Moy N, Heckman MG, Thomas CS, Gonsalves N, Achem SR. Endoscopic 
   assessment of the oesophageal features of eosinophilic oesophagitis: validation 
   of a novel classification and grading system. Gut. 2013 Apr;62(4):489-95.
2. Dellon ES, Cotton CC, Gebhart JH, Higgins LL, Beitia R, Woosley JT, et al. 
   Accuracy of the Eosinophilic Esophagitis Endoscopic Reference Score in Diagnosis 
   and Determining Response to Treatment. Clin Gastroenterol Hepatol. 2016 Jan;14(1):31-9.
"""

from typing import Dict, Any


class ErefsCalculator:
    """Calculator for Eosinophilic Esophagitis Endoscopic Reference Score (EREFS)"""
    
    def __init__(self):
        """Initialize calculator with scoring definitions"""
        
        # Scoring definitions for validation and interpretation
        self.EDEMA_GRADES = {
            0: "Absent",
            1: "Present (loss of vascular markings)"
        }
        
        self.RINGS_GRADES = {
            0: "None",
            1: "Mild (subtle)",
            2: "Moderate", 
            3: "Severe (fixed rings)"
        }
        
        self.EXUDATES_GRADES = {
            0: "None",
            1: "Mild (≤10% mucosal surface)",
            2: "Severe (>10%)"
        }
        
        self.FURROWS_GRADES = {
            0: "Absent",
            1: "Present"
        }
        
        self.STRICTURES_GRADES = {
            0: "None",
            1: "Present"
        }
    
    def calculate(self, edema: int, rings: int, exudates: int, 
                 furrows: int, strictures: int) -> Dict[str, Any]:
        """
        Calculates EREFS score based on endoscopic findings
        
        Args:
            edema (int): Edema grade (0-1)
            rings (int): Rings grade (0-3)
            exudates (int): Exudates grade (0-2)
            furrows (int): Furrows grade (0-1)
            strictures (int): Strictures grade (0-1)
            
        Returns:
            Dict with EREFS score and clinical interpretation
        """
        
        # Validate inputs
        self._validate_inputs(edema, rings, exudates, furrows, strictures)
        
        # Calculate total EREFS score
        total_score = self._calculate_total_score(edema, rings, exudates, furrows, strictures)
        
        # Get interpretation
        interpretation = self._get_interpretation(total_score, edema, rings, exudates, furrows, strictures)
        
        return {
            "result": total_score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, edema: int, rings: int, exudates: int, 
                        furrows: int, strictures: int):
        """Validates input parameters"""
        
        # Validate edema
        if not isinstance(edema, int) or edema not in [0, 1]:
            raise ValueError("edema must be an integer: 0 (absent) or 1 (present)")
        
        # Validate rings
        if not isinstance(rings, int) or rings not in [0, 1, 2, 3]:
            raise ValueError("rings must be an integer: 0 (none), 1 (mild), 2 (moderate), or 3 (severe)")
        
        # Validate exudates
        if not isinstance(exudates, int) or exudates not in [0, 1, 2]:
            raise ValueError("exudates must be an integer: 0 (none), 1 (mild ≤10%), or 2 (severe >10%)")
        
        # Validate furrows
        if not isinstance(furrows, int) or furrows not in [0, 1]:
            raise ValueError("furrows must be an integer: 0 (absent) or 1 (present)")
        
        # Validate strictures
        if not isinstance(strictures, int) or strictures not in [0, 1]:
            raise ValueError("strictures must be an integer: 0 (none) or 1 (present)")
    
    def _calculate_total_score(self, edema: int, rings: int, exudates: int,
                              furrows: int, strictures: int) -> int:
        """
        Calculates total EREFS score
        
        Args:
            All five endoscopic feature grades
            
        Returns:
            int: Total EREFS score (0-9)
        """
        
        return edema + rings + exudates + furrows + strictures
    
    def _get_interpretation(self, total_score: int, edema: int, rings: int, 
                           exudates: int, furrows: int, strictures: int) -> Dict[str, str]:
        """
        Determines clinical interpretation based on EREFS score
        
        Args:
            total_score (int): Total EREFS score
            Individual component scores for detailed interpretation
            
        Returns:
            Dict with interpretation details
        """
        
        # Create detailed findings summary
        findings = []
        if edema > 0:
            findings.append(f"Edema: {self.EDEMA_GRADES[edema]}")
        if rings > 0:
            findings.append(f"Rings: {self.RINGS_GRADES[rings]}")
        if exudates > 0:
            findings.append(f"Exudates: {self.EXUDATES_GRADES[exudates]}")
        if furrows > 0:
            findings.append(f"Furrows: {self.FURROWS_GRADES[furrows]}")
        if strictures > 0:
            findings.append(f"Strictures: {self.STRICTURES_GRADES[strictures]}")
        
        findings_text = "; ".join(findings) if findings else "No endoscopic features identified"
        
        # Determine severity category and interpretation
        if total_score == 0:
            return {
                "stage": "No Endoscopic Features",
                "description": "No visible EoE features",
                "interpretation": (
                    f"EREFS score: {total_score}/9. {findings_text}. "
                    f"No endoscopic evidence of eosinophilic esophagitis. Consider histologic "
                    f"assessment as endoscopic findings may be absent in early or treated disease. "
                    f"Normal endoscopy does not exclude EoE diagnosis."
                )
            }
        elif 1 <= total_score <= 2:
            return {
                "stage": "Mild Disease",
                "description": "Mild endoscopic features",
                "interpretation": (
                    f"EREFS score: {total_score}/9. {findings_text}. "
                    f"Mild endoscopic evidence of eosinophilic esophagitis. Consider correlation "
                    f"with histologic findings and clinical symptoms. Monitor response to treatment "
                    f"and reassess endoscopically."
                )
            }
        elif 3 <= total_score <= 5:
            return {
                "stage": "Moderate Disease",
                "description": "Moderate endoscopic features", 
                "interpretation": (
                    f"EREFS score: {total_score}/9. {findings_text}. "
                    f"Moderate endoscopic evidence of eosinophilic esophagitis. Multiple features "
                    f"present suggest established disease. Correlate with histology and consider "
                    f"appropriate anti-inflammatory treatment."
                )
            }
        else:  # 6-9
            return {
                "stage": "Severe Disease",
                "description": "Severe endoscopic features",
                "interpretation": (
                    f"EREFS score: {total_score}/9. {findings_text}. "
                    f"Severe endoscopic evidence of eosinophilic esophagitis. Multiple severe "
                    f"features indicate advanced disease with potential complications. Consider "
                    f"aggressive treatment and close monitoring for stricture formation."
                )
            }


def calculate_erefs(edema: int, rings: int, exudates: int, 
                   furrows: int, strictures: int) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_erefs pattern
    """
    calculator = ErefsCalculator()
    return calculator.calculate(edema, rings, exudates, furrows, strictures)