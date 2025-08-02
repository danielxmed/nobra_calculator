"""
Kawasaki Disease Diagnostic Criteria Calculator

Diagnoses Kawasaki Disease using fever duration and principal clinical features.
Kawasaki disease is a systemic vasculitis of childhood that can cause coronary artery 
aneurysms if untreated. Early diagnosis and treatment are crucial to prevent complications.

References:
1. McCrindle BW, Rowley AH, Newburger JW, Burns JC, Bolger AF, Gewitz M, et al. 
   Diagnosis, Treatment, and Long-Term Management of Kawasaki Disease: A Scientific 
   Statement for Health Professionals From the American Heart Association. 
   Circulation. 2017;135(17):e927-e999.
2. Newburger JW, Takahashi M, Gerber MA, Gewitz MH, Tani LY, Burns JC, et al. 
   Diagnosis, treatment, and long-term management of Kawasaki disease: a statement 
   for health professionals from the Committee on Rheumatic Fever, Endocarditis and 
   Kawasaki Disease, Council on Cardiovascular Disease in the Young, American Heart 
   Association. Circulation. 2004;110(17):2747-71.
3. Ayusawa M, Sonobe T, Uemura S, Ogawa S, Nakamura Y, Kiyosawa N, et al. 
   Revision of diagnostic guidelines for Kawasaki disease (the 5th revised edition). 
   Pediatr Int. 2005;47(2):232-4.
4. Yellen ES, Gauvreau K, Takahashi M, Burns JC, Shulman S, Baker AL, et al. 
   Performance of 2004 American Heart Association recommendations for treatment of 
   Kawasaki disease. Pediatrics. 2010;125(2):e234-41.
"""

from typing import Dict, Any


class KawasakiDiseaseCalculator:
    """Calculator for Kawasaki Disease Diagnostic Criteria"""
    
    def __init__(self):
        # Principal clinical features
        self.principal_features = [
            "bilateral_conjunctival_injection",
            "oral_changes", 
            "cervical_lymphadenopathy",
            "extremity_changes",
            "polymorphous_rash"
        ]
    
    def calculate(self, fever_duration: int, bilateral_conjunctival_injection: str, 
                 oral_changes: str, cervical_lymphadenopathy: str, 
                 extremity_changes: str, polymorphous_rash: str) -> Dict[str, Any]:
        """
        Evaluates Kawasaki Disease diagnostic criteria
        
        Args:
            fever_duration (int): Duration of fever in days
            bilateral_conjunctival_injection (str): Bilateral conjunctival injection
            oral_changes (str): Oral changes (lips, tongue, mucosa)
            cervical_lymphadenopathy (str): Cervical lymphadenopathy ≥1.5cm
            extremity_changes (str): Extremity changes (erythema, induration, desquamation)
            polymorphous_rash (str): Polymorphous rash
            
        Returns:
            Dict with the diagnosis and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(fever_duration, bilateral_conjunctival_injection, 
                            oral_changes, cervical_lymphadenopathy, 
                            extremity_changes, polymorphous_rash)
        
        # Count positive principal features
        features_present = self._count_principal_features(
            bilateral_conjunctival_injection, oral_changes, 
            cervical_lymphadenopathy, extremity_changes, polymorphous_rash
        )
        
        # Determine diagnosis
        diagnosis_result = self._determine_diagnosis(fever_duration, features_present)
        
        return {
            "result": f"{features_present}/5 principal features",
            "unit": "features",
            "interpretation": diagnosis_result["interpretation"],
            "stage": diagnosis_result["stage"],
            "stage_description": diagnosis_result["stage_description"]
        }
    
    def _validate_inputs(self, fever_duration: int, bilateral_conjunctival_injection: str,
                        oral_changes: str, cervical_lymphadenopathy: str,
                        extremity_changes: str, polymorphous_rash: str):
        """Validates input parameters"""
        
        if not isinstance(fever_duration, int):
            raise ValueError("Fever duration must be an integer")
        
        if fever_duration < 1 or fever_duration > 30:
            raise ValueError("Fever duration must be between 1 and 30 days")
        
        # Validate yes/no parameters
        yes_no_params = {
            "bilateral_conjunctival_injection": bilateral_conjunctival_injection,
            "oral_changes": oral_changes,
            "cervical_lymphadenopathy": cervical_lymphadenopathy,
            "extremity_changes": extremity_changes,
            "polymorphous_rash": polymorphous_rash
        }
        
        for param_name, param_value in yes_no_params.items():
            if param_value not in ["yes", "no"]:
                raise ValueError(f"{param_name} must be 'yes' or 'no'")
    
    def _count_principal_features(self, bilateral_conjunctival_injection: str,
                                 oral_changes: str, cervical_lymphadenopathy: str,
                                 extremity_changes: str, polymorphous_rash: str) -> int:
        """Counts the number of principal features present"""
        
        features = [
            bilateral_conjunctival_injection,
            oral_changes,
            cervical_lymphadenopathy,
            extremity_changes,
            polymorphous_rash
        ]
        
        return sum(1 for feature in features if feature == "yes")
    
    def _determine_diagnosis(self, fever_duration: int, features_present: int) -> Dict[str, str]:
        """
        Determines the Kawasaki disease diagnosis based on fever duration and features
        
        Args:
            fever_duration (int): Duration of fever in days
            features_present (int): Number of principal features present
            
        Returns:
            Dict with diagnosis interpretation
        """
        
        # Classic Kawasaki Disease: fever ≥4 days + ≥4 principal features
        if fever_duration >= 4 and features_present >= 4:
            return {
                "stage": "Classic Kawasaki Disease",
                "stage_description": "Meets criteria for classic diagnosis",
                "interpretation": (
                    f"Classic Kawasaki Disease diagnosed. Patient meets criteria with fever "
                    f"for {fever_duration} days and {features_present}/5 principal clinical features. "
                    "Immediate treatment with IVIG and aspirin is indicated. Echocardiography "
                    "should be performed to assess coronary arteries. Early treatment (within 10 days "
                    "of fever onset) significantly reduces risk of coronary artery abnormalities. "
                    "Close monitoring and cardiology consultation are recommended."
                )
            }
        
        # Incomplete Kawasaki Disease: fever ≥5 days + 2-3 principal features
        elif fever_duration >= 5 and 2 <= features_present <= 3:
            return {
                "stage": "Possible Incomplete Kawasaki Disease", 
                "stage_description": "Meets criteria for incomplete diagnosis consideration",
                "interpretation": (
                    f"Possible Incomplete Kawasaki Disease. Patient has fever for {fever_duration} days "
                    f"and {features_present}/5 principal clinical features. Laboratory studies "
                    "(ESR, CRP, albumin, ALT, platelet count, urinalysis) and echocardiography "
                    "should be obtained. If laboratory findings support inflammation or coronary "
                    "abnormalities are present, treatment with IVIG and aspirin should be considered. "
                    "Incomplete presentation is more common in infants <6 months and patients >8 years."
                )
            }
        
        # Fever duration adequate but insufficient features
        elif fever_duration >= 4 and features_present < 2:
            return {
                "stage": "Kawasaki Disease Unlikely",
                "stage_description": "Insufficient features for diagnosis",
                "interpretation": (
                    f"Kawasaki Disease unlikely. Patient has fever for {fever_duration} days but "
                    f"only {features_present}/5 principal clinical features. Continue monitoring "
                    "as features may develop over time. Consider alternative diagnoses. "
                    "If clinical suspicion remains high (especially in infants), laboratory studies "
                    "and echocardiography may be helpful. Repeat assessment in 24-48 hours if fever persists."
                )
            }
        
        # Fever duration too short
        elif fever_duration < 4:
            return {
                "stage": "Insufficient Fever Duration",
                "stage_description": "Fever duration too short for diagnosis",
                "interpretation": (
                    f"Insufficient fever duration for Kawasaki Disease diagnosis. Patient has fever "
                    f"for only {fever_duration} days (minimum 4 days required) with {features_present}/5 "
                    "principal clinical features. Continue monitoring and reassess if fever persists. "
                    "In rare cases with coronary abnormalities on echocardiography, treatment may "
                    "be considered even with shorter fever duration. Consider alternative diagnoses "
                    "and supportive care while monitoring for evolution of symptoms."
                )
            }
        
        # Fever ≥5 days but only 1 feature (borderline incomplete)
        else:  # fever_duration >= 5 and features_present == 1
            return {
                "stage": "Kawasaki Disease Possible",
                "stage_description": "Borderline for incomplete diagnosis",
                "interpretation": (
                    f"Kawasaki Disease possible but unlikely. Patient has fever for {fever_duration} days "
                    f"but only {features_present}/5 principal clinical features. Laboratory studies "
                    "(ESR, CRP, albumin, ALT, platelet count, urinalysis) and echocardiography "
                    "are recommended, especially in high-risk patients (infants <6 months). "
                    "If significant inflammation or coronary abnormalities are present, treatment "
                    "may be considered. Continue close monitoring for development of additional features."
                )
            }


def calculate_kawasaki_disease_diagnostic_criteria(fever_duration: int, 
                                                  bilateral_conjunctival_injection: str,
                                                  oral_changes: str, 
                                                  cervical_lymphadenopathy: str,
                                                  extremity_changes: str, 
                                                  polymorphous_rash: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_kawasaki_disease_diagnostic_criteria pattern
    """
    calculator = KawasakiDiseaseCalculator()
    return calculator.calculate(fever_duration, bilateral_conjunctival_injection, 
                               oral_changes, cervical_lymphadenopathy, 
                               extremity_changes, polymorphous_rash)