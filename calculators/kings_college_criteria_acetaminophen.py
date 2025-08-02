"""
King's College Criteria for Acetaminophen Toxicity Calculator

Determines need for liver transplant referral in patients with acute liver failure 
secondary to acetaminophen overdose.

References:
1. O'Grady JG, Alexander GJ, Hayllar KM, Williams R. Early indicators of prognosis 
   in fulminant hepatic failure. Gastroenterology. 1989 Aug;97(2):439-45.
2. Bailey B, Amre DK, Gaudreault P. Fulminant hepatic failure secondary to 
   acetaminophen poisoning: a systematic review and meta-analysis of prognostic 
   criteria determining the need for liver transplantation. Crit Care Med. 2003 
   Jan;31(1):299-305.
3. Bernal W, Auzinger G, Dhawan A, Wendon J. Acute liver failure. Lancet. 2010 
   Jul 17;376(9736):190-201.
"""

from typing import Dict, Any, Optional


class KingsCollegeCriteriaAcetaminophenCalculator:
    """Calculator for King's College Criteria for Acetaminophen Toxicity"""
    
    def __init__(self):
        # Criteria thresholds
        self.PH_THRESHOLD = 7.30
        self.INR_THRESHOLD = 6.5
        self.CREATININE_THRESHOLD = 3.4  # mg/dL
        
        # Additional prognostic markers
        self.LACTATE_EARLY_THRESHOLD = 3.5  # mmol/L after early resuscitation
        self.LACTATE_FULL_THRESHOLD = 3.0   # mmol/L after full resuscitation
        self.PHOSPHATE_THRESHOLD = 3.75     # mg/dL at 48-96 hours
        
        # Performance characteristics
        self.SENSITIVITY = 58  # %
        self.SPECIFICITY = 95  # %
    
    def calculate(self, arterial_ph: float, inr: float, creatinine: float,
                 hepatic_encephalopathy_grade: str, lactate: Optional[float] = None,
                 phosphate: Optional[float] = None) -> Dict[str, Any]:
        """
        Calculates King's College Criteria for acetaminophen toxicity
        
        Args:
            arterial_ph (float): Arterial pH
            inr (float): International Normalized Ratio
            creatinine (float): Serum creatinine in mg/dL
            hepatic_encephalopathy_grade (str): Encephalopathy grade
            lactate (Optional[float]): Serum lactate in mmol/L
            phosphate (Optional[float]): Serum phosphate in mg/dL
            
        Returns:
            Dict with criteria assessment and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(arterial_ph, inr, creatinine, hepatic_encephalopathy_grade,
                            lactate, phosphate)
        
        # Evaluate criteria
        criteria_results = self._evaluate_criteria(arterial_ph, inr, creatinine, 
                                                 hepatic_encephalopathy_grade,
                                                 lactate, phosphate)
        
        # Get interpretation
        interpretation = self._get_interpretation(criteria_results)
        
        return {
            "result": criteria_results,
            "unit": "criteria",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["stage_description"]
        }
    
    def _validate_inputs(self, arterial_ph: float, inr: float, creatinine: float,
                        hepatic_encephalopathy_grade: str, lactate: Optional[float],
                        phosphate: Optional[float]):
        """Validates input parameters"""
        
        if not isinstance(arterial_ph, (int, float)):
            raise ValueError("Arterial pH must be a number")
        
        if arterial_ph < 6.0 or arterial_ph > 8.0:
            raise ValueError("Arterial pH must be between 6.0 and 8.0")
        
        if not isinstance(inr, (int, float)):
            raise ValueError("INR must be a number")
        
        if inr < 0.5 or inr > 20.0:
            raise ValueError("INR must be between 0.5 and 20.0")
        
        if not isinstance(creatinine, (int, float)):
            raise ValueError("Creatinine must be a number")
        
        if creatinine < 0.1 or creatinine > 25.0:
            raise ValueError("Creatinine must be between 0.1 and 25.0 mg/dL")
        
        valid_grades = ["none", "grade_i", "grade_ii", "grade_iii", "grade_iv"]
        if hepatic_encephalopathy_grade not in valid_grades:
            raise ValueError(f"Hepatic encephalopathy grade must be one of: {', '.join(valid_grades)}")
        
        if lactate is not None:
            if not isinstance(lactate, (int, float)):
                raise ValueError("Lactate must be a number")
            if lactate < 0.1 or lactate > 30.0:
                raise ValueError("Lactate must be between 0.1 and 30.0 mmol/L")
        
        if phosphate is not None:
            if not isinstance(phosphate, (int, float)):
                raise ValueError("Phosphate must be a number")
            if phosphate < 0.5 or phosphate > 15.0:
                raise ValueError("Phosphate must be between 0.5 and 15.0 mg/dL")
    
    def _evaluate_criteria(self, arterial_ph: float, inr: float, creatinine: float,
                          hepatic_encephalopathy_grade: str, lactate: Optional[float],
                          phosphate: Optional[float]) -> Dict[str, Any]:
        """
        Evaluates King's College Criteria
        
        Args:
            arterial_ph (float): Arterial pH
            inr (float): INR
            creatinine (float): Creatinine
            hepatic_encephalopathy_grade (str): Encephalopathy grade
            lactate (Optional[float]): Lactate level
            phosphate (Optional[float]): Phosphate level
            
        Returns:
            Dict with criteria evaluation results
        """
        
        # Primary criteria evaluation
        ph_criterion = arterial_ph < self.PH_THRESHOLD
        inr_criterion = inr > self.INR_THRESHOLD
        creatinine_criterion = creatinine > self.CREATININE_THRESHOLD
        encephalopathy_criterion = hepatic_encephalopathy_grade in ["grade_iii", "grade_iv"]
        
        # Combined criteria (all three must be present)
        combined_criterion = inr_criterion and creatinine_criterion and encephalopathy_criterion
        
        # Overall criteria met
        criteria_met = ph_criterion or combined_criterion
        
        # Additional prognostic markers
        additional_markers = {}
        if lactate is not None:
            additional_markers["high_lactate"] = lactate > self.LACTATE_EARLY_THRESHOLD
            additional_markers["lactate_value"] = lactate
        
        if phosphate is not None:
            additional_markers["high_phosphate"] = phosphate > self.PHOSPHATE_THRESHOLD
            additional_markers["phosphate_value"] = phosphate
        
        return {
            "criteria_met": criteria_met,
            "ph_criterion": ph_criterion,
            "ph_value": arterial_ph,
            "combined_criterion": combined_criterion,
            "inr_criterion": inr_criterion,
            "inr_value": inr,
            "creatinine_criterion": creatinine_criterion,
            "creatinine_value": creatinine,
            "encephalopathy_criterion": encephalopathy_criterion,
            "encephalopathy_grade": hepatic_encephalopathy_grade,
            "additional_markers": additional_markers
        }
    
    def _get_interpretation(self, criteria_results: Dict[str, Any]) -> Dict[str, str]:
        """
        Provides clinical interpretation based on criteria results
        
        Args:
            criteria_results (Dict): Results from criteria evaluation
            
        Returns:
            Dict with interpretation details
        """
        
        criteria_met = criteria_results["criteria_met"]
        ph_criterion = criteria_results["ph_criterion"]
        combined_criterion = criteria_results["combined_criterion"]
        additional_markers = criteria_results["additional_markers"]
        
        if criteria_met:
            stage = "Meets Criteria"
            stage_description = "Poor prognosis - liver transplant evaluation needed"
            
            interpretation = (
                "Meets King's College Criteria for acetaminophen toxicity. "
                f"This indicates poor prognosis with {self.SPECIFICITY}% specificity for mortality. "
                "URGENT liver transplant evaluation and referral to transplant center required. "
            )
            
            # Specify which criteria met
            if ph_criterion:
                interpretation += f"Arterial pH {criteria_results['ph_value']:.2f} is <{self.PH_THRESHOLD}. "
            
            if combined_criterion:
                interpretation += (
                    f"All three secondary criteria met: INR {criteria_results['inr_value']:.1f} "
                    f"(>{self.INR_THRESHOLD}), creatinine {criteria_results['creatinine_value']:.1f} mg/dL "
                    f"(>{self.CREATININE_THRESHOLD}), and Grade III/IV hepatic encephalopathy. "
                )
            
            interpretation += (
                "Immediate intensive care management required including: "
                "N-acetylcysteine continuation, hemodynamic support, management of "
                "intracranial hypertension, renal replacement therapy if indicated, "
                "and preparation for potential liver transplantation."
            )
        
        else:
            stage = "Does Not Meet Criteria"
            stage_description = "Does not meet transplant criteria but requires close monitoring"
            
            interpretation = (
                "Does not meet King's College Criteria for liver transplantation. "
                "However, criteria are specific but not sensitive (58% sensitivity), "
                "so close monitoring and continued aggressive medical management are essential. "
            )
            
            # Note individual values
            interpretation += (
                f"Current values: pH {criteria_results['ph_value']:.2f}, "
                f"INR {criteria_results['inr_value']:.1f}, "
                f"creatinine {criteria_results['creatinine_value']:.1f} mg/dL, "
                f"encephalopathy {criteria_results['encephalopathy_grade'].replace('_', ' ')}. "
            )
            
            interpretation += (
                "Continue N-acetylcysteine, monitor for deterioration, "
                "and reassess criteria frequently. Consider early transplant center "
                "consultation if clinical deterioration occurs."
            )
        
        # Add information about additional prognostic markers
        if additional_markers:
            interpretation += " Additional prognostic markers: "
            
            if "high_lactate" in additional_markers:
                if additional_markers["high_lactate"]:
                    interpretation += (
                        f"Elevated lactate {additional_markers['lactate_value']:.1f} mmol/L "
                        f"(>{self.LACTATE_EARLY_THRESHOLD}) suggests poor prognosis. "
                    )
                else:
                    interpretation += (
                        f"Lactate {additional_markers['lactate_value']:.1f} mmol/L "
                        f"(<{self.LACTATE_EARLY_THRESHOLD}) is reassuring. "
                    )
            
            if "high_phosphate" in additional_markers:
                if additional_markers["high_phosphate"]:
                    interpretation += (
                        f"Elevated phosphate {additional_markers['phosphate_value']:.1f} mg/dL "
                        f"(>{self.PHOSPHATE_THRESHOLD}) at 48-96h suggests poor prognosis."
                    )
                else:
                    interpretation += (
                        f"Phosphate {additional_markers['phosphate_value']:.1f} mg/dL "
                        f"(<{self.PHOSPHATE_THRESHOLD}) is within normal range."
                    )
        
        return {
            "stage": stage,
            "stage_description": stage_description,
            "interpretation": interpretation
        }


def calculate_kings_college_criteria_acetaminophen(arterial_ph: float, inr: float, 
                                                   creatinine: float, hepatic_encephalopathy_grade: str,
                                                   lactate: Optional[float] = None,
                                                   phosphate: Optional[float] = None) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_kings_college_criteria_acetaminophen pattern
    """
    calculator = KingsCollegeCriteriaAcetaminophenCalculator()
    return calculator.calculate(arterial_ph, inr, creatinine, hepatic_encephalopathy_grade,
                              lactate, phosphate)