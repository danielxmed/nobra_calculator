"""
Medication Regimen Complexity-Intensive Care Unit (MRC-ICU) Score Calculator

Predicts patient outcomes (mortality, length of stay), ICU complications, and 
pharmacist workload in the ICU based on medication regimen complexity.

References:
1. Gwynn ME, et al. Development and validation of a medication regimen complexity 
   scoring tool for critically ill patients. Am J Health Syst Pharm. 2019.
2. Sikora A, et al. Impact of Pharmacists to Improve Patient Care in the Critically 
   Ill: A Large Multicenter Analysis Using Meaningful Metrics With the MRC-ICU Score. 
   Crit Care Med. 2022.
3. Olney K, et al. Development of Machine Learning Models to Validate a Medication 
   Regimen Complexity Scoring Tool for Critically Ill Patients. Ann Pharmacother. 2021.
"""

from typing import Dict, Any


class MrcIcuScoreCalculator:
    """Calculator for Medication Regimen Complexity-ICU (MRC-ICU) Score"""
    
    def __init__(self):
        # Point values for specific medications
        self.AMINOGLYCOSIDE_POINTS = 3
        self.AMPHOTERICIN_B_POINTS = 1
        self.ANTIARRHYTHMIC_POINTS = 1
        self.ANTICOAGULANT_POINTS = 1
        self.ANTICONVULSANT_POINTS = 3
        self.ARGATROBAN_POINTS = 2
        self.AZOLE_ANTIFUNGAL_POINTS = 2
        self.BLOOD_PRODUCT_POINTS = 2
        self.CHEMOTHERAPY_POINTS = 3
        self.CLOZAPINE_POINTS = 3
        self.DIGOXIN_POINTS = 3
        self.VANCOMYCIN_POINTS = 3
        self.CRYSTALLOID_INFUSION_POINTS = 1
        self.VASOPRESSOR_POINTS = 1
        self.CONTINUOUS_OPIOID_POINTS = 2
        self.CONTINUOUS_SEDATIVE_POINTS = 2
        self.PARENTERAL_NUTRITION_POINTS = 2
        self.INSULIN_INFUSION_POINTS = 1
        self.PRN_OPIOID_POINTS = 1
        
    def calculate(self, aminoglycosides: int, amphotericin_b: str, antiarrhythmics: int,
                  anticoagulants: int, anticonvulsants: int, argatroban: str,
                  azole_antifungals: int, blood_products: int, chemotherapy: int,
                  clozapine: str, digoxin: str, vancomycin: str,
                  continuous_infusion_crystalloids: str, vasopressors_inotropes: int,
                  continuous_opioid_infusions: int, continuous_sedative_infusions: int,
                  parenteral_nutrition: str, insulin_infusion: str, prn_opioids: str,
                  other_high_complexity_meds: int) -> Dict[str, Any]:
        """
        Calculates the MRC-ICU score based on medication regimen complexity
        
        Args:
            aminoglycosides: Number of aminoglycosides (multiply by 3 points each)
            amphotericin_b: Presence of amphotericin B ('yes' or 'no')
            antiarrhythmics: Number of antiarrhythmic medications (multiply by 1 point each)
            anticoagulants: Number of anticoagulant medications (multiply by 1 point each)
            anticonvulsants: Number of anticonvulsant medications (multiply by 3 points each)
            argatroban: Presence of argatroban ('yes' or 'no')
            azole_antifungals: Number of azole antifungals (multiply by 2 points each)
            blood_products: Number of blood products (multiply by 2 points each)
            chemotherapy: Number of chemotherapy agents (multiply by 3 points each)
            clozapine: Presence of clozapine ('yes' or 'no')
            digoxin: Presence of digoxin ('yes' or 'no')
            vancomycin: Presence of vancomycin ('yes' or 'no')
            continuous_infusion_crystalloids: Continuous crystalloid infusion ('yes' or 'no')
            vasopressors_inotropes: Number of vasopressor/inotrope infusions (multiply by 1 point each)
            continuous_opioid_infusions: Number of continuous opioid infusions (multiply by 2 points each)
            continuous_sedative_infusions: Number of continuous sedative infusions (multiply by 2 points each)
            parenteral_nutrition: Presence of parenteral nutrition ('yes' or 'no')
            insulin_infusion: Continuous insulin infusion ('yes' or 'no')
            prn_opioids: As-needed opioid medications ('yes' or 'no')
            other_high_complexity_meds: Number of other high-complexity medications
            
        Returns:
            Dict with MRC-ICU score and clinical interpretation
        """
        
        # Validate inputs
        self._validate_inputs(
            aminoglycosides, amphotericin_b, antiarrhythmics, anticoagulants,
            anticonvulsants, argatroban, azole_antifungals, blood_products,
            chemotherapy, clozapine, digoxin, vancomycin, continuous_infusion_crystalloids,
            vasopressors_inotropes, continuous_opioid_infusions, continuous_sedative_infusions,
            parenteral_nutrition, insulin_infusion, prn_opioids, other_high_complexity_meds
        )
        
        # Calculate total score
        total_score = 0
        
        # Multiply medications by their point values
        total_score += aminoglycosides * self.AMINOGLYCOSIDE_POINTS
        total_score += antiarrhythmics * self.ANTIARRHYTHMIC_POINTS
        total_score += anticoagulants * self.ANTICOAGULANT_POINTS
        total_score += anticonvulsants * self.ANTICONVULSANT_POINTS
        total_score += azole_antifungals * self.AZOLE_ANTIFUNGAL_POINTS
        total_score += blood_products * self.BLOOD_PRODUCT_POINTS
        total_score += chemotherapy * self.CHEMOTHERAPY_POINTS
        total_score += vasopressors_inotropes * self.VASOPRESSOR_POINTS
        total_score += continuous_opioid_infusions * self.CONTINUOUS_OPIOID_POINTS
        total_score += continuous_sedative_infusions * self.CONTINUOUS_SEDATIVE_POINTS
        
        # Add single medication points
        if amphotericin_b == "yes":
            total_score += self.AMPHOTERICIN_B_POINTS
        if argatroban == "yes":
            total_score += self.ARGATROBAN_POINTS
        if clozapine == "yes":
            total_score += self.CLOZAPINE_POINTS
        if digoxin == "yes":
            total_score += self.DIGOXIN_POINTS
        if vancomycin == "yes":
            total_score += self.VANCOMYCIN_POINTS
        if continuous_infusion_crystalloids == "yes":
            total_score += self.CRYSTALLOID_INFUSION_POINTS
        if parenteral_nutrition == "yes":
            total_score += self.PARENTERAL_NUTRITION_POINTS
        if insulin_infusion == "yes":
            total_score += self.INSULIN_INFUSION_POINTS
        if prn_opioids == "yes":
            total_score += self.PRN_OPIOID_POINTS
            
        # Add other high-complexity medications (estimated at 2 points each average)
        total_score += other_high_complexity_meds * 2
        
        # Get interpretation
        interpretation = self._get_interpretation(total_score)
        
        return {
            "result": total_score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, aminoglycosides, amphotericin_b, antiarrhythmics,
                        anticoagulants, anticonvulsants, argatroban, azole_antifungals,
                        blood_products, chemotherapy, clozapine, digoxin, vancomycin,
                        continuous_infusion_crystalloids, vasopressors_inotropes,
                        continuous_opioid_infusions, continuous_sedative_infusions,
                        parenteral_nutrition, insulin_infusion, prn_opioids,
                        other_high_complexity_meds):
        """Validates all input parameters"""
        
        # Validate integer counts
        integer_params = {
            "aminoglycosides": (aminoglycosides, 0, 5),
            "antiarrhythmics": (antiarrhythmics, 0, 5),
            "anticoagulants": (anticoagulants, 0, 5),
            "anticonvulsants": (anticonvulsants, 0, 5),
            "azole_antifungals": (azole_antifungals, 0, 5),
            "blood_products": (blood_products, 0, 10),
            "chemotherapy": (chemotherapy, 0, 5),
            "vasopressors_inotropes": (vasopressors_inotropes, 0, 5),
            "continuous_opioid_infusions": (continuous_opioid_infusions, 0, 3),
            "continuous_sedative_infusions": (continuous_sedative_infusions, 0, 3),
            "other_high_complexity_meds": (other_high_complexity_meds, 0, 20)
        }
        
        for param_name, (value, min_val, max_val) in integer_params.items():
            if not isinstance(value, int):
                raise ValueError(f"{param_name} must be an integer")
            if value < min_val or value > max_val:
                raise ValueError(f"{param_name} must be between {min_val} and {max_val}")
        
        # Validate yes/no parameters
        yes_no_params = {
            "amphotericin_b": amphotericin_b,
            "argatroban": argatroban,
            "clozapine": clozapine,
            "digoxin": digoxin,
            "vancomycin": vancomycin,
            "continuous_infusion_crystalloids": continuous_infusion_crystalloids,
            "parenteral_nutrition": parenteral_nutrition,
            "insulin_infusion": insulin_infusion,
            "prn_opioids": prn_opioids
        }
        
        for param_name, value in yes_no_params.items():
            if value not in ["yes", "no"]:
                raise ValueError(f"{param_name} must be 'yes' or 'no'")
    
    def _get_interpretation(self, score: int) -> Dict[str, str]:
        """
        Determines the interpretation based on MRC-ICU score
        
        Args:
            score: Calculated MRC-ICU score
            
        Returns:
            Dict with stage, description, and interpretation
        """
        
        if score < 10:
            return {
                "stage": "Low Complexity",
                "description": "Low medication regimen complexity",
                "interpretation": "Lower MRC-ICU score suggests relatively simple medication regimen "
                                "with lower anticipated pharmacist workload. Associated with lower "
                                "mortality risk and shorter ICU length of stay."
            }
        elif score < 20:
            return {
                "stage": "Moderate Complexity",
                "description": "Moderate medication regimen complexity",
                "interpretation": "Moderate MRC-ICU score indicates intermediate medication regimen "
                                "complexity. Mean score in validation studies was approximately 10.3. "
                                "Each 1-point increase is associated with 7% increased odds of "
                                "mortality and 0.25 day increase in ICU LOS."
            }
        else:
            return {
                "stage": "High Complexity",
                "description": "High medication regimen complexity",
                "interpretation": "High MRC-ICU score indicates complex medication regimen requiring "
                                "intensive pharmacist monitoring and intervention. Associated with "
                                "significantly increased mortality risk, longer ICU stay, and need "
                                "for extensive pharmacist workload."
            }


def calculate_mrc_icu_score(aminoglycosides: int, amphotericin_b: str, antiarrhythmics: int,
                           anticoagulants: int, anticonvulsants: int, argatroban: str,
                           azole_antifungals: int, blood_products: int, chemotherapy: int,
                           clozapine: str, digoxin: str, vancomycin: str,
                           continuous_infusion_crystalloids: str, vasopressors_inotropes: int,
                           continuous_opioid_infusions: int, continuous_sedative_infusions: int,
                           parenteral_nutrition: str, insulin_infusion: str, prn_opioids: str,
                           other_high_complexity_meds: int) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = MrcIcuScoreCalculator()
    return calculator.calculate(
        aminoglycosides, amphotericin_b, antiarrhythmics, anticoagulants,
        anticonvulsants, argatroban, azole_antifungals, blood_products,
        chemotherapy, clozapine, digoxin, vancomycin, continuous_infusion_crystalloids,
        vasopressors_inotropes, continuous_opioid_infusions, continuous_sedative_infusions,
        parenteral_nutrition, insulin_infusion, prn_opioids, other_high_complexity_meds
    )