"""
Benzodiazepine Conversion Calculator

Provides equivalents between different benzodiazepines for safe medication interchanging.

References (Vancouver style):
1. Ashton H. Benzodiazepines: how they work and how to withdraw. The Ashton Manual. 2002. 
   Available at: https://www.benzo.org.uk/manual/
2. Lader M, Tylee A, Donoghue J. Withdrawing benzodiazepines in primary care. 
   CNS Drugs. 2009;23(1):19-34.
3. Parr JM, Kavanagh DJ, Cahill L, et al. Effectiveness of current treatment approaches 
   for benzodiazepine discontinuation: a meta-analysis. Addiction. 2009 Jan;104(1):13-24.
"""

from typing import Dict, Any


class BenzodiazepineConversionCalculator:
    """Calculator for Benzodiazepine Conversion"""
    
    def __init__(self):
        # Benzodiazepine potency factors (relative to diazepam = 1.0)
        # Based on standard equivalency tables
        self.potency_factors = {
            "alprazolam": 2.0,      # 0.5 mg = 1 mg diazepam
            "chlordiazepoxide": 0.2, # 25 mg = 5 mg diazepam  
            "clonazepam": 4.0,      # 0.25 mg = 1 mg diazepam
            "diazepam": 1.0,        # 5 mg = 5 mg diazepam (reference)
            "lorazepam": 2.0,       # 0.5 mg = 1 mg diazepam
            "midazolam": 3.0,       # ~0.33 mg = 1 mg diazepam
            "oxazepam": 0.33,       # 15 mg = 5 mg diazepam
            "temazepam": 0.5        # 10 mg = 5 mg diazepam
        }
        
        # Drug information for clinical context
        self.drug_info = {
            "alprazolam": {"brand": "Xanax", "duration": "short acting (6-12 hours)", "half_life": "11-13 hours"},
            "chlordiazepoxide": {"brand": "Librium", "duration": "long acting (>24 hours)", "half_life": "36-200 hours"},
            "clonazepam": {"brand": "Klonopin", "duration": "long acting (>24 hours)", "half_life": "18-50 hours"},
            "diazepam": {"brand": "Valium", "duration": "long acting (>24 hours)", "half_life": "20-100 hours"},
            "lorazepam": {"brand": "Ativan", "duration": "intermediate acting (12-24 hours)", "half_life": "10-20 hours"},
            "midazolam": {"brand": "Versed", "duration": "very short acting (<6 hours)", "half_life": "1-4 hours"},
            "oxazepam": {"brand": "Serax", "duration": "short acting (6-12 hours)", "half_life": "4-15 hours"},
            "temazepam": {"brand": "Restoril", "duration": "short acting (6-12 hours)", "half_life": "3-18 hours"}
        }
    
    def calculate(self, converting_from: str, total_daily_dose: float, converting_to: str) -> Dict[str, Any]:
        """
        Calculates benzodiazepine conversion between medications
        
        Args:
            converting_from (str): Current benzodiazepine medication
            total_daily_dose (float): Total daily dose in mg of current medication
            converting_to (str): Target benzodiazepine medication
            
        Returns:
            Dict with equivalent dose and clinical guidance
        """
        
        # Validations
        self._validate_inputs(converting_from, total_daily_dose, converting_to)
        
        # Calculate equivalent dose
        equivalent_dose = self._calculate_conversion(converting_from, total_daily_dose, converting_to)
        
        # Get interpretation
        interpretation = self._get_interpretation(
            converting_from, total_daily_dose, converting_to, equivalent_dose
        )
        
        return {
            "result": equivalent_dose,
            "unit": "mg",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, converting_from: str, total_daily_dose: float, converting_to: str):
        """Validates input parameters"""
        
        if not isinstance(converting_from, str):
            raise ValueError("Converting from must be a string")
        if not isinstance(converting_to, str):
            raise ValueError("Converting to must be a string")
        if not isinstance(total_daily_dose, (int, float)):
            raise ValueError("Total daily dose must be a number")
        
        if converting_from not in self.potency_factors:
            raise ValueError(f"Converting from '{converting_from}' is not a supported benzodiazepine")
        if converting_to not in self.potency_factors:
            raise ValueError(f"Converting to '{converting_to}' is not a supported benzodiazepine")
        
        if total_daily_dose <= 0:
            raise ValueError("Total daily dose must be greater than 0")
        if total_daily_dose > 100:
            raise ValueError("Total daily dose exceeds safe maximum (100 mg)")
        
        if converting_from == converting_to:
            raise ValueError("Cannot convert to the same medication")
    
    def _calculate_conversion(self, converting_from: str, dose: float, converting_to: str) -> float:
        """Calculates the equivalent dose conversion"""
        
        # Convert current dose to diazepam equivalents first
        diazepam_equivalent = dose * self.potency_factors[converting_from]
        
        # Convert from diazepam equivalent to target medication
        target_dose = diazepam_equivalent / self.potency_factors[converting_to]
        
        # Round to appropriate precision (2 decimal places)
        return round(target_dose, 2)
    
    def _get_interpretation(self, from_drug: str, from_dose: float, 
                          to_drug: str, to_dose: float) -> Dict[str, str]:
        """
        Generates clinical interpretation of the conversion
        
        Args:
            from_drug (str): Original medication
            from_dose (float): Original daily dose
            to_drug (str): Target medication
            to_dose (float): Equivalent target dose
            
        Returns:
            Dict with clinical interpretation
        """
        
        from_info = self.drug_info[from_drug]
        to_info = self.drug_info[to_drug]
        
        # Generate conversion ratio for context
        conversion_ratio = to_dose / from_dose
        
        interpretation = (
            f"Benzodiazepine conversion: {from_dose} mg {from_drug} ({from_info['brand']}) "
            f"daily is approximately equivalent to {to_dose} mg {to_drug} ({to_info['brand']}) "
            f"daily (conversion ratio: 1:{conversion_ratio:.2f}). "
            f"Original medication: {from_info['duration']} with half-life {from_info['half_life']}. "
            f"Target medication: {to_info['duration']} with half-life {to_info['half_life']}. "
            
            "IMPORTANT CLINICAL CONSIDERATIONS: "
            "This conversion is intended for interchanging benzodiazepines in patients already "
            "on benzodiazepine therapy, NOT for calculating initial doses in benzodiazepine-naive patients. "
            "Use the lower end of the dose range initially to minimize oversedation risk. "
            "Monitor closely for signs of oversedation (sedation, confusion, ataxia) or withdrawal "
            "symptoms (anxiety, insomnia, tremor, seizures). "
            "Consider half-life differences when timing the conversion - longer-acting medications "
            "may require less frequent dosing but take longer to reach steady state. "
            "Individual patient factors such as age, hepatic function, and concurrent medications "
            "may require dose adjustments. Abrupt discontinuation should be avoided due to risk "
            "of withdrawal symptoms including potentially life-threatening seizures."
        )
        
        return {
            "stage": "Conversion Complete",
            "description": "Benzodiazepine conversion calculated",
            "interpretation": interpretation
        }


def calculate_benzodiazepine_conversion(converting_from: str, total_daily_dose: float, 
                                      converting_to: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = BenzodiazepineConversionCalculator()
    return calculator.calculate(converting_from, total_daily_dose, converting_to)