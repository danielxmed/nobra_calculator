"""
Murray Score for Acute Lung Injury Calculator

Stratifies severity of acute lung injury (ALI) and acute respiratory distress syndrome (ARDS),
and is used for patient selection for extracorporeal membrane oxygenation (ECMO). The Murray
Score provides objective assessment of lung injury severity using four physiological parameters.

References:
1. Murray JF, Matthay MA, Luce JM, Flick MR. An expanded definition of the adult respiratory 
   distress syndrome. Am Rev Respir Dis. 1988;138(3):720-3. doi: 10.1164/ajrccm/138.3.720.
2. Bernard GR, Artigas A, Brigham KL, Carlet J, Falke K, Hudson L, et al. The American-European 
   Consensus Conference on ARDS. Definitions, mechanisms, relevant outcomes, and clinical trial 
   coordination. Am J Respir Crit Care Med. 1994;149(3 Pt 1):818-24. doi: 10.1164/ajrccm.149.3.7509706.
"""

from typing import Dict, Any


class MurrayScoreCalculator:
    """Calculator for Murray Score for Acute Lung Injury"""
    
    def __init__(self):
        # Score component ranges and descriptions
        self.CHEST_XRAY_CRITERIA = {
            0: "No consolidation",
            1: "Consolidation in 1 quadrant", 
            2: "Consolidation in 2 quadrants",
            3: "Consolidation in 3 quadrants",
            4: "Consolidation in all 4 quadrants"
        }
        
        self.HYPOXEMIA_CRITERIA = {
            0: "PaO2/FiO2 ≥300",
            1: "PaO2/FiO2 225-299",
            2: "PaO2/FiO2 175-224", 
            3: "PaO2/FiO2 100-174",
            4: "PaO2/FiO2 <100"
        }
        
        self.PEEP_CRITERIA = {
            0: "PEEP ≤5 cmH2O",
            1: "PEEP 6-8 cmH2O",
            2: "PEEP 9-11 cmH2O",
            3: "PEEP 12-14 cmH2O", 
            4: "PEEP ≥15 cmH2O"
        }
        
        self.COMPLIANCE_CRITERIA = {
            0: "Compliance ≥80 mL/cmH2O",
            1: "Compliance 60-79 mL/cmH2O",
            2: "Compliance 40-59 mL/cmH2O",
            3: "Compliance 20-39 mL/cmH2O",
            4: "Compliance ≤19 mL/cmH2O"
        }
    
    def calculate(self, chest_xray_score: int, hypoxemia_score: int, 
                 peep_score: int, compliance_score: int) -> Dict[str, Any]:
        """
        Calculates the Murray Score for Acute Lung Injury
        
        Args:
            chest_xray_score (int): Chest X-ray score (0-4) based on quadrants with consolidation
            hypoxemia_score (int): Hypoxemia score (0-4) based on PaO2/FiO2 ratio
            peep_score (int): PEEP score (0-4) based on positive end-expiratory pressure
            compliance_score (int): Compliance score (0-4) based on static lung compliance
            
        Returns:
            Dict with the Murray Score and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(chest_xray_score, hypoxemia_score, peep_score, compliance_score)
        
        # Calculate Murray Score (average of the four components)
        murray_score = (chest_xray_score + hypoxemia_score + peep_score + compliance_score) / 4
        
        # Get interpretation
        interpretation = self._get_interpretation(murray_score)
        
        return {
            "result": round(murray_score, 2),
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, chest_xray_score: int, hypoxemia_score: int, 
                        peep_score: int, compliance_score: int):
        """Validates input parameters"""
        
        if not isinstance(chest_xray_score, int) or chest_xray_score not in [0, 1, 2, 3, 4]:
            raise ValueError("Chest X-ray score must be an integer between 0 and 4")
        
        if not isinstance(hypoxemia_score, int) or hypoxemia_score not in [0, 1, 2, 3, 4]:
            raise ValueError("Hypoxemia score must be an integer between 0 and 4")
        
        if not isinstance(peep_score, int) or peep_score not in [0, 1, 2, 3, 4]:
            raise ValueError("PEEP score must be an integer between 0 and 4")
        
        if not isinstance(compliance_score, int) or compliance_score not in [0, 1, 2, 3, 4]:
            raise ValueError("Compliance score must be an integer between 0 and 4")
    
    def _get_interpretation(self, murray_score: float) -> Dict[str, str]:
        """
        Determines the interpretation based on Murray Score
        
        Args:
            murray_score (float): Calculated Murray Score
            
        Returns:
            Dict with interpretation details
        """
        
        if murray_score < 1.0:
            return {
                "stage": "No Lung Injury",
                "description": "No acute lung injury",
                "interpretation": "NO ACUTE LUNG INJURY: The Murray Score indicates no evidence of acute lung injury. "
                                "MANAGEMENT: Continue standard respiratory care and monitoring. No specific interventions "
                                "for acute lung injury are indicated at this time. MONITORING: Routine vital signs and "
                                "oxygen saturation monitoring. Watch for signs of respiratory deterioration. "
                                "ECMO CONSIDERATION: ECMO is not indicated based on lung injury severity. "
                                "FOLLOW-UP: Standard care with reassessment if clinical status changes."
            }
        elif murray_score < 2.5:
            return {
                "stage": "Mild to Moderate Lung Injury", 
                "description": "Mild to moderate acute lung injury",
                "interpretation": "MILD TO MODERATE ACUTE LUNG INJURY: The Murray Score indicates mild to moderate "
                                "acute lung injury requiring supportive care. MANAGEMENT: Implement lung-protective "
                                "ventilation with low tidal volumes (6 mL/kg predicted body weight), plateau pressure "
                                "<30 cmH2O, and appropriate PEEP. Monitor arterial blood gases and adjust ventilator "
                                "settings accordingly. MONITORING: Close monitoring for progression to severe ARDS. "
                                "Serial Murray Score assessments may be helpful. ECMO CONSIDERATION: ECMO is generally "
                                "not indicated at this severity level unless other critical factors are present. "
                                "PROGNOSIS: Good potential for recovery with appropriate supportive care."
            }
        elif murray_score < 3.0:
            return {
                "stage": "Severe Lung Injury",
                "description": "Severe acute lung injury", 
                "interpretation": "SEVERE ACUTE LUNG INJURY (ARDS): The Murray Score indicates severe acute lung injury "
                                "consistent with ARDS requiring intensive management. MANAGEMENT: Implement strict "
                                "lung-protective ventilation, consider prone positioning for 12-16 hours daily, "
                                "neuromuscular blockade for 48 hours if severe hypoxemia persists, and conservative "
                                "fluid management. ADVANCED THERAPIES: Consider inhaled nitric oxide, recruitment "
                                "maneuvers, or high-frequency oscillatory ventilation in refractory cases. "
                                "ECMO CONSIDERATION: ECMO evaluation may be appropriate in select patients with "
                                "refractory hypoxemia despite optimal conventional therapy. PROGNOSIS: Guarded with "
                                "significant mortality risk requiring aggressive intervention."
            }
        else:  # murray_score >= 3.0
            return {
                "stage": "Very Severe Lung Injury",
                "description": "Very severe acute lung injury",
                "interpretation": "VERY SEVERE ACUTE LUNG INJURY: The Murray Score indicates very severe acute lung "
                                "injury with poor prognosis requiring maximal supportive care. MANAGEMENT: Maximize "
                                "lung-protective ventilation strategies, prone positioning, neuromuscular blockade, "
                                "and consider all available rescue therapies. Strict fluid restriction and hemodynamic "
                                "optimization are critical. ECMO CONSIDERATION: Strong consideration for ECMO in "
                                "appropriate candidates with refractory hypoxemia. Ensure ECMO center consultation "
                                "and transfer if not available locally. MULTIDISCIPLINARY CARE: Involve pulmonary/critical "
                                "care specialists, ECMO team if available, and provide family counseling regarding "
                                "prognosis. PROGNOSIS: Very poor with high mortality risk despite aggressive intervention."
            }


def calculate_murray_score(chest_xray_score: int, hypoxemia_score: int,
                          peep_score: int, compliance_score: int) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = MurrayScoreCalculator()
    return calculator.calculate(chest_xray_score, hypoxemia_score, peep_score, compliance_score)