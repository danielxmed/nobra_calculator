"""
Atropine Dosing for Cholinesterase Inhibitor Toxicity Calculator

Doses atropine for cholinesterase inhibitor toxicity from prescription drugs, 
nerve gas, or insecticides based on patient type and severity.

References:
1. Howland MA. Antidotes in Depth: Atropine. In: Goldfrank's Toxicologic Emergencies. 10th ed. 2015.
2. Abedin MJ, et al. Open-label randomized clinical trial of atropine bolus injection. Clin Toxicol. 2012;50(5):433-40.
3. Eddleston M, et al. Early management after self-poisoning with organophosphorus. Crit Care. 2004;8(6):R391-7.
"""

from typing import Dict, Any, Optional


class AtropineDosingCalculator:
    """Calculator for Atropine Dosing in Cholinesterase Inhibitor Toxicity"""
    
    def __init__(self):
        # Initial dosing recommendations in mg
        self.PEDIATRIC_DOSE_PER_KG = 0.02  # mg/kg
        self.ADULT_MILD_MIN = 1.0  # mg
        self.ADULT_MILD_MAX = 2.0  # mg
        self.ADULT_SEVERE_MIN = 3.0  # mg
        self.ADULT_SEVERE_MAX = 5.0  # mg
        
        # Infusion calculation
        self.INFUSION_PERCENTAGE = 0.10  # 10% of total initial doses per hour
    
    def calculate(self, patient_type: str, severity: str, weight: Optional[float] = None) -> Dict[str, Any]:
        """
        Calculates atropine dosing recommendations for cholinesterase inhibitor toxicity
        
        Args:
            patient_type (str): "adult" or "pediatric"
            severity (str): "mild" or "severe"
            weight (float, optional): Patient weight in kg (required for pediatric)
            
        Returns:
            Dict with complete dosing recommendations
        """
        
        # Validations
        self._validate_inputs(patient_type, severity, weight)
        
        # Calculate initial dose
        initial_dose = self._calculate_initial_dose(patient_type, severity, weight)
        
        # Generate complete dosing protocol
        dosing_protocol = self._generate_dosing_protocol(initial_dose, patient_type, severity, weight)
        
        return dosing_protocol
    
    def _validate_inputs(self, patient_type: str, severity: str, weight: Optional[float]):
        """Validates input parameters"""
        
        if patient_type not in ["adult", "pediatric"]:
            raise ValueError("Patient type must be 'adult' or 'pediatric'")
        
        if severity not in ["mild", "severe"]:
            raise ValueError("Severity must be 'mild' or 'severe'")
        
        if patient_type == "pediatric" and weight is None:
            raise ValueError("Weight is required for pediatric patients")
        
        if weight is not None and (weight < 0.1 or weight > 300):
            raise ValueError("Weight must be between 0.1 and 300 kg")
    
    def _calculate_initial_dose(self, patient_type: str, severity: str, weight: Optional[float]) -> Dict[str, float]:
        """Calculates the initial atropine dose"""
        
        if patient_type == "pediatric":
            dose = self.PEDIATRIC_DOSE_PER_KG * weight
            # Cap at adult maximum dose
            if severity == "mild":
                dose = min(dose, self.ADULT_MILD_MAX)
            else:
                dose = min(dose, self.ADULT_SEVERE_MAX)
            
            return {
                "min": dose,
                "max": dose,
                "recommended": dose
            }
        
        else:  # adult
            if severity == "mild":
                return {
                    "min": self.ADULT_MILD_MIN,
                    "max": self.ADULT_MILD_MAX,
                    "recommended": (self.ADULT_MILD_MIN + self.ADULT_MILD_MAX) / 2
                }
            else:  # severe
                return {
                    "min": self.ADULT_SEVERE_MIN,
                    "max": self.ADULT_SEVERE_MAX,
                    "recommended": (self.ADULT_SEVERE_MIN + self.ADULT_SEVERE_MAX) / 2
                }
    
    def _generate_dosing_protocol(self, initial_dose: Dict[str, float], 
                                  patient_type: str, severity: str, 
                                  weight: Optional[float]) -> Dict[str, Any]:
        """Generates complete dosing protocol with interpretation"""
        
        # Format initial dose string
        if initial_dose["min"] == initial_dose["max"]:
            initial_dose_str = f"{initial_dose['recommended']:.2f} mg"
        else:
            initial_dose_str = f"{initial_dose['min']:.0f}-{initial_dose['max']:.0f} mg"
        
        # Calculate example infusion rates based on different total doses
        example_total_doses = [10, 20, 50, 100]  # mg
        infusion_examples = []
        for total in example_total_doses:
            rate = total * self.INFUSION_PERCENTAGE
            infusion_examples.append(f"{total} mg total → {rate:.1f} mg/hr")
        
        # Build patient info string
        patient_info = f"{patient_type.capitalize()} patient"
        if patient_type == "pediatric" and weight:
            patient_info += f" ({weight} kg)"
        patient_info += f" with {severity} toxicity"
        
        return {
            "result": {
                "initial_dose": initial_dose_str,
                "initial_dose_mg": initial_dose["recommended"],
                "dose_range": {
                    "min": initial_dose["min"],
                    "max": initial_dose["max"]
                },
                "escalation_protocol": "Double dose every 5 minutes until atropinization achieved",
                "infusion_rate": "10% of total initial doses per hour",
                "infusion_examples": infusion_examples
            },
            "unit": "mg",
            "interpretation": f"""Initial atropine dose: {initial_dose_str}

Reassess for atropinization every 5 minutes:
• Clear lung exam (no rales/rhonchi)
• Heart rate >80 bpm
• Systolic blood pressure >80 mmHg

If not atropinized, double the previous dose.

Once atropinized, start continuous infusion at 10% of total initial doses per hour.

Example infusion rates:
{chr(10).join('• ' + ex for ex in infusion_examples)}""",
            "stage": severity.capitalize(),
            "stage_description": patient_info,
            "warnings": [
                "Not indicated for isolated bradycardia",
                "Large cumulative doses may be necessary",
                "Immediate decontamination is critical",
                "Consider concurrent pralidoxime administration"
            ]
        }


def calculate_atropine_dosing(patient_type: str, severity: str, weight: Optional[float] = None) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = AtropineDosingCalculator()
    return calculator.calculate(patient_type, severity, weight)