"""
NEDOCS Score for Emergency Department Overcrowding Calculator

Estimates severity of overcrowding in emergency departments using objective parameters.

References:
- Weiss SJ, et al. Acad Emerg Med. 2004 Jan;11(1):38-50.
- Hwang U, et. al. Acad Emerg Med. 2011; 18:527–538
"""

from typing import Dict, Any


class NedocsCalculator:
    """Calculator for NEDOCS Score for Emergency Department Overcrowding"""
    
    def calculate(self, ed_beds: int, hospital_beds: int, total_patients: int,
                  ventilated_patients: int, admitted_patients: int,
                  longest_admit_wait: float, longest_waiting_room_wait: float) -> Dict[str, Any]:
        """
        Calculates the NEDOCS score using the provided parameters
        
        Args:
            ed_beds (int): Number of ED beds (total licensed)
            hospital_beds (int): Number of hospital beds
            total_patients (int): Total patients in the ED
            ventilated_patients (int): Patients on ventilators in the ED
            admitted_patients (int): Number of admits in the ED
            longest_admit_wait (float): Waiting time of longest admitted patient (hours)
            longest_waiting_room_wait (float): Waiting time of longest waiting room patient (hours)
            
        Returns:
            Dict with the result and interpretation
        """
        
        # Validations
        self._validate_inputs(ed_beds, hospital_beds, total_patients,
                            ventilated_patients, admitted_patients,
                            longest_admit_wait, longest_waiting_room_wait)
        
        # Calculate NEDOCS score using the validated formula
        # NEDOCS = -20 + 85.8 × (Total ED patients / ED beds) + 
        #          600 × (ED admits / Hospital beds) + 
        #          13.3 × (Ventilated patients) + 
        #          0.93 × (Longest admit time in hours) + 
        #          5.64 × (Last patient wait time in hours)
        
        nedocs_score = (
            -20 +
            85.8 * (total_patients / ed_beds) +
            600 * (admitted_patients / hospital_beds) +
            13.3 * ventilated_patients +
            0.93 * longest_admit_wait +
            5.64 * longest_waiting_room_wait
        )
        
        # Ensure score is within valid range (1-200)
        nedocs_score = max(1, min(200, round(nedocs_score, 1)))
        
        # Get interpretation
        interpretation = self._get_interpretation(nedocs_score)
        
        return {
            "result": nedocs_score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, ed_beds: int, hospital_beds: int, total_patients: int,
                        ventilated_patients: int, admitted_patients: int,
                        longest_admit_wait: float, longest_waiting_room_wait: float):
        """Validates input parameters"""
        
        # Validate ED beds
        if not isinstance(ed_beds, int) or ed_beds < 1 or ed_beds > 500:
            raise ValueError("Number of ED beds must be between 1 and 500")
        
        # Validate hospital beds
        if not isinstance(hospital_beds, int) or hospital_beds < 1 or hospital_beds > 5000:
            raise ValueError("Number of hospital beds must be between 1 and 5000")
        
        # Validate total patients
        if not isinstance(total_patients, int) or total_patients < 0 or total_patients > 1000:
            raise ValueError("Total patients must be between 0 and 1000")
        
        # Validate ventilated patients
        if not isinstance(ventilated_patients, int) or ventilated_patients < 0 or ventilated_patients > 100:
            raise ValueError("Ventilated patients must be between 0 and 100")
        
        # Validate admitted patients
        if not isinstance(admitted_patients, int) or admitted_patients < 0 or admitted_patients > 500:
            raise ValueError("Admitted patients must be between 0 and 500")
        
        # Validate longest admit wait
        if not isinstance(longest_admit_wait, (int, float)) or longest_admit_wait < 0 or longest_admit_wait > 168:
            raise ValueError("Longest admit wait must be between 0 and 168 hours")
        
        # Validate longest waiting room wait
        if not isinstance(longest_waiting_room_wait, (int, float)) or longest_waiting_room_wait < 0 or longest_waiting_room_wait > 168:
            raise ValueError("Longest waiting room wait must be between 0 and 168 hours")
        
        # Logical validations
        if ventilated_patients > total_patients:
            raise ValueError("Ventilated patients cannot exceed total patients")
        
        if admitted_patients > total_patients:
            raise ValueError("Admitted patients cannot exceed total patients")
    
    def _get_interpretation(self, score: float) -> Dict[str, str]:
        """
        Determines the interpretation based on the NEDOCS score
        
        Args:
            score (float): Calculated NEDOCS score
            
        Returns:
            Dict with interpretation details
        """
        
        if score <= 20:
            return {
                "stage": "Level 1",
                "description": "Not busy",
                "interpretation": "The emergency department is operating smoothly with minimal patient load and adequate resources."
            }
        elif score <= 60:
            return {
                "stage": "Level 2",
                "description": "Busy",
                "interpretation": "The emergency department is experiencing moderate patient volume but remains functional with acceptable wait times."
            }
        elif score <= 100:
            return {
                "stage": "Level 3",
                "description": "Extremely busy but not overcrowded",
                "interpretation": "The emergency department is very busy with high patient volume, but resources are still adequate to manage patient flow effectively."
            }
        elif score <= 140:
            return {
                "stage": "Level 4",
                "description": "Overcrowded",
                "interpretation": "The emergency department is overcrowded with inadequate resources for patient volume. Patient care may be compromised and wait times are excessive."
            }
        elif score <= 180:
            return {
                "stage": "Level 5",
                "description": "Severely overcrowded",
                "interpretation": "The emergency department is severely overcrowded with critical resource limitations. Patient safety is at risk and immediate measures should be taken."
            }
        else:
            return {
                "stage": "Level 6",
                "description": "Dangerously overcrowded",
                "interpretation": "The emergency department is dangerously overcrowded. Patient safety is severely compromised and emergency measures must be implemented immediately."
            }


def calculate_nedocs(ed_beds: int, hospital_beds: int, total_patients: int,
                    ventilated_patients: int, admitted_patients: int,
                    longest_admit_wait: float, longest_waiting_room_wait: float) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_nedocs pattern
    """
    calculator = NedocsCalculator()
    return calculator.calculate(ed_beds, hospital_beds, total_patients,
                              ventilated_patients, admitted_patients,
                              longest_admit_wait, longest_waiting_room_wait)