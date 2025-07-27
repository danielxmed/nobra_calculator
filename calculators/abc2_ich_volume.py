"""
ABC/2 Formula for Intracerebral Hemorrhage Volume Calculator

Predicts volume of intracranial hemorrhage from CT measurements using the
Kothari ABC/2 method, a simplified ellipsoid formula widely used for bedside
ICH volume estimation.

Based on: Kothari RU, Brott T, Broderick JP, et al. The ABCs of measuring 
intracerebral hemorrhage volumes. Stroke. 1996;27:1304-1305.
"""

import math
from typing import Dict, Any


class Abc2IchVolumeCalculator:
    """Calculator for ABC/2 Formula for Intracerebral Hemorrhage Volume"""
    
    def __init__(self):
        # Constants for volume calculation
        self.DIVISOR = 2  # ABC/2 formula divisor
        self.MM_TO_CM = 0.1  # Convert mm to cm
    
    def calculate(self, hemorrhage_shape: str, length_a: float, width_b: float, 
                 weighted_slices: float, slice_thickness: float) -> Dict[str, Any]:
        """
        Calculates the intracerebral hemorrhage volume using ABC/2 formula
        
        Args:
            hemorrhage_shape (str): Shape of hemorrhage ('round_ellipsoid' or 'irregular_multinodular')
            length_a (float): Greatest hemorrhage diameter in cm
            width_b (float): Diameter perpendicular to A in cm  
            weighted_slices (float): Number of CT slices weighted by hemorrhage area
            slice_thickness (float): CT slice thickness in mm
            
        Returns:
            Dict with the volume result and clinical interpretation
        """
        
        # Validate inputs
        self._validate_inputs(hemorrhage_shape, length_a, width_b, weighted_slices, slice_thickness)
        
        # Calculate volume using ABC/2 formula
        volume = self._calculate_abc2_volume(length_a, width_b, weighted_slices, slice_thickness)
        
        # Get clinical interpretation
        interpretation = self._get_interpretation(volume, hemorrhage_shape)
        
        return {
            "result": volume,
            "unit": "cm³",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, hemorrhage_shape: str, length_a: float, width_b: float, 
                        weighted_slices: float, slice_thickness: float):
        """Validates input parameters"""
        
        # Validate hemorrhage shape
        valid_shapes = ["round_ellipsoid", "irregular_multinodular"]
        if hemorrhage_shape not in valid_shapes:
            raise ValueError(f"Invalid hemorrhage shape. Must be one of: {', '.join(valid_shapes)}")
        
        # Validate length A
        if not isinstance(length_a, (int, float)) or length_a <= 0:
            raise ValueError("Length A must be a positive number")
        if length_a < 0.1 or length_a > 20.0:
            raise ValueError("Length A must be between 0.1 and 20.0 cm")
        
        # Validate width B
        if not isinstance(width_b, (int, float)) or width_b <= 0:
            raise ValueError("Width B must be a positive number")
        if width_b < 0.1 or width_b > 20.0:
            raise ValueError("Width B must be between 0.1 and 20.0 cm")
        
        # Validate weighted slices
        if not isinstance(weighted_slices, (int, float)) or weighted_slices <= 0:
            raise ValueError("Weighted slices must be a positive number")
        if weighted_slices < 0.5 or weighted_slices > 50.0:
            raise ValueError("Weighted slices must be between 0.5 and 50.0")
        
        # Validate slice thickness
        if not isinstance(slice_thickness, (int, float)) or slice_thickness <= 0:
            raise ValueError("Slice thickness must be a positive number")
        if slice_thickness < 1.0 or slice_thickness > 15.0:
            raise ValueError("Slice thickness must be between 1.0 and 15.0 mm")
    
    def _calculate_abc2_volume(self, length_a: float, width_b: float, 
                              weighted_slices: float, slice_thickness: float) -> float:
        """Implements the ABC/2 mathematical formula"""
        
        # Convert slice thickness from mm to cm
        c_dimension = weighted_slices * (slice_thickness * self.MM_TO_CM)
        
        # Apply ABC/2 formula: Volume = (A × B × C) / 2
        # This is derived from the ellipsoid volume formula 4/3π(A/2)(B/2)(C/2)
        # where π is approximated as 3, yielding ABC/2
        volume = (length_a * width_b * c_dimension) / self.DIVISOR
        
        # Round to 2 decimal places for clinical reporting
        return round(volume, 2)
    
    def _get_interpretation(self, volume: float, hemorrhage_shape: str) -> Dict[str, str]:
        """
        Determines clinical interpretation based on hemorrhage volume
        
        Args:
            volume (float): Calculated hemorrhage volume in cm³
            hemorrhage_shape (str): Shape of the hemorrhage
            
        Returns:
            Dict with clinical interpretation
        """
        
        # Base interpretation on volume ranges established in literature
        if volume < 10:
            interpretation = {
                "stage": "Small",
                "description": "Small volume hemorrhage",
                "interpretation": "Small ICH volume associated with better prognosis. Consider conservative management unless neurological deterioration occurs."
            }
        elif volume < 30:
            interpretation = {
                "stage": "Moderate", 
                "description": "Moderate volume hemorrhage",
                "interpretation": "Moderate ICH volume. Monitor closely for expansion and neurological changes. Consider surgical evaluation based on clinical condition."
            }
        elif volume < 60:
            interpretation = {
                "stage": "Large",
                "description": "Large volume hemorrhage", 
                "interpretation": "Large ICH volume associated with increased mortality risk. Surgical intervention may be considered based on location and clinical condition."
            }
        else:
            interpretation = {
                "stage": "Very Large",
                "description": "Very large volume hemorrhage",
                "interpretation": "Very large ICH volume with high mortality risk. Aggressive management and surgical consultation recommended. Consider goals of care discussion."
            }
        
        # Add shape-specific considerations
        if hemorrhage_shape == "irregular_multinodular":
            interpretation["interpretation"] += " Note: Irregular hemorrhage shape may reduce ABC/2 accuracy compared to elliptical hemorrhages."
        
        return interpretation


def calculate_abc2_ich_volume(hemorrhage_shape: str, length_a: float, width_b: float,
                             weighted_slices: float, slice_thickness: float) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = Abc2IchVolumeCalculator()
    return calculator.calculate(hemorrhage_shape, length_a, width_b, weighted_slices, slice_thickness)
