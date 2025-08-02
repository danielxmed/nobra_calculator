"""
Urine Output and Fluid Balance Calculator

Calculates 24-hour urine output rate and fluid balance for assessment of 
renal function and fluid status. Helps identify oliguria, polyuria, and 
fluid imbalances in hospitalized patients.

References:
- Kellum JA, Lameire N, Aspelin P, et al. Kidney disease: improving global 
  outcomes (KDIGO) acute kidney injury work group. KDIGO clinical practice 
  guideline for acute kidney injury. Kidney Int Suppl. 2012;2(1):1-138.
- Macedo E, Malhotra R, Bouchard J, Wynn SK, Mehta RL. Oliguria is an early 
  predictor of higher mortality in critically ill patients. Kidney Int. 2011;80(7):760-767.
"""

from typing import Dict, Any


class UrineOutputFluidBalanceCalculator:
    """Calculator for Urine Output and Fluid Balance"""
    
    def __init__(self):
        # Clinical thresholds for urine output classification (mL/kg/hr)
        self.ANURIA_THRESHOLD = 0.3
        self.OLIGURIA_THRESHOLD = 0.5
        self.NORMAL_LOW_THRESHOLD = 1.0
        self.NORMAL_HIGH_THRESHOLD = 2.0
    
    def calculate(self, weight_kg: float, urine_output_ml: float, 
                  collection_hours: float, fluid_intake_ml: float) -> Dict[str, Any]:
        """
        Calculates urine output rate and fluid balance
        
        Args:
            weight_kg (float): Patient body weight in kg (1-300)
            urine_output_ml (float): Total urine output in mL (0-10000)
            collection_hours (float): Number of hours for collection (1-48)
            fluid_intake_ml (float): Total fluid intake in mL (0-20000)
            
        Returns:
            Dict with the result and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(weight_kg, urine_output_ml, collection_hours, fluid_intake_ml)
        
        # Calculate urine output rate
        urine_output_rate = self._calculate_urine_output_rate(weight_kg, urine_output_ml, collection_hours)
        
        # Calculate fluid balance
        fluid_balance = self._calculate_fluid_balance(fluid_intake_ml, urine_output_ml)
        
        # Calculate 24-hour extrapolated values
        extrapolated_24h_output = self._extrapolate_24h_output(urine_output_ml, collection_hours)
        
        # Get interpretation
        interpretation = self._get_interpretation(urine_output_rate, fluid_balance, extrapolated_24h_output)
        
        return {
            "result": urine_output_rate,
            "unit": "mL/kg/hr",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"],
            "fluid_balance_ml": fluid_balance,
            "extrapolated_24h_output_ml": extrapolated_24h_output
        }
    
    def _validate_inputs(self, weight_kg: float, urine_output_ml: float, 
                        collection_hours: float, fluid_intake_ml: float):
        """Validates input parameters"""
        
        # Validate weight
        if not isinstance(weight_kg, (int, float)) or weight_kg <= 0:
            raise ValueError("Weight must be a positive number")
        if weight_kg < 1 or weight_kg > 300:
            raise ValueError("Weight must be between 1 and 300 kg")
        
        # Validate urine output
        if not isinstance(urine_output_ml, (int, float)) or urine_output_ml < 0:
            raise ValueError("Urine output must be a non-negative number")
        if urine_output_ml > 10000:
            raise ValueError("Urine output must be ≤10000 mL")
        
        # Validate collection hours
        if not isinstance(collection_hours, (int, float)) or collection_hours <= 0:
            raise ValueError("Collection hours must be a positive number")
        if collection_hours < 1 or collection_hours > 48:
            raise ValueError("Collection hours must be between 1 and 48 hours")
        
        # Validate fluid intake
        if not isinstance(fluid_intake_ml, (int, float)) or fluid_intake_ml < 0:
            raise ValueError("Fluid intake must be a non-negative number")
        if fluid_intake_ml > 20000:
            raise ValueError("Fluid intake must be ≤20000 mL")
    
    def _calculate_urine_output_rate(self, weight_kg: float, urine_output_ml: float, 
                                   collection_hours: float) -> float:
        """
        Calculates the urine output rate per kg body weight per hour
        
        Formula: Urine Output Rate (mL/kg/hr) = Total Urine Output (mL) / (Weight (kg) × Hours)
        """
        
        urine_output_rate = urine_output_ml / (weight_kg * collection_hours)
        
        # Round to 2 decimal places for clinical precision
        return round(urine_output_rate, 2)
    
    def _calculate_fluid_balance(self, fluid_intake_ml: float, urine_output_ml: float) -> float:
        """
        Calculates the fluid balance (intake minus output)
        
        Formula: Fluid Balance = Fluid Intake - Urine Output
        Positive value = fluid retention, Negative value = fluid loss
        """
        
        fluid_balance = fluid_intake_ml - urine_output_ml
        
        # Round to nearest mL
        return round(fluid_balance, 0)
    
    def _extrapolate_24h_output(self, urine_output_ml: float, collection_hours: float) -> float:
        """
        Extrapolates urine output to 24-hour equivalent for comparison with normal ranges
        """
        
        if collection_hours == 24:
            return urine_output_ml
        
        # Calculate hourly rate and multiply by 24
        hourly_output = urine_output_ml / collection_hours
        extrapolated_24h = hourly_output * 24
        
        # Round to nearest mL
        return round(extrapolated_24h, 0)
    
    def _get_interpretation(self, urine_output_rate: float, fluid_balance: float, 
                          extrapolated_24h_output: float) -> Dict[str, str]:
        """
        Determines the interpretation based on urine output rate and fluid balance
        
        Args:
            urine_output_rate (float): Calculated urine output rate in mL/kg/hr
            fluid_balance (float): Calculated fluid balance in mL
            extrapolated_24h_output (float): 24-hour extrapolated urine output in mL
            
        Returns:
            Dict with interpretation details
        """
        
        # Determine fluid balance status
        if fluid_balance > 500:
            fluid_status = "positive fluid balance (retention)"
        elif fluid_balance < -500:
            fluid_status = "negative fluid balance (loss)"
        else:
            fluid_status = "neutral fluid balance"
        
        # Format 24-hour output for interpretation
        extrapolated_24h_str = f"{extrapolated_24h_output:.0f}"
        
        if urine_output_rate < self.ANURIA_THRESHOLD:
            return {
                "stage": "Anuria/Severe Oliguria",
                "description": "Critically low urine output",
                "interpretation": f"Critically low urine output ({urine_output_rate} mL/kg/hr) indicating severe acute renal failure or anuria. Extrapolated 24-hour output: {extrapolated_24h_str} mL (normal: 800-2000 mL). Current {fluid_status} of {abs(fluid_balance):.0f} mL. This level sustained for >24 hours or complete anuria for >12 hours suggests acute kidney injury requiring immediate nephrology consultation and intervention."
            }
        elif urine_output_rate < self.OLIGURIA_THRESHOLD:
            return {
                "stage": "Oliguria",
                "description": "Low urine output",
                "interpretation": f"Low urine output ({urine_output_rate} mL/kg/hr) indicating oliguria. Extrapolated 24-hour output: {extrapolated_24h_str} mL (normal: 800-2000 mL). Current {fluid_status} of {abs(fluid_balance):.0f} mL. This level sustained for >12 hours may indicate acute kidney injury. Monitor closely and evaluate for underlying causes such as volume depletion, nephrotoxic medications, or intrinsic renal disease."
            }
        elif urine_output_rate < self.NORMAL_LOW_THRESHOLD:
            return {
                "stage": "Normal Low",
                "description": "Lower normal range",
                "interpretation": f"Lower normal urine output ({urine_output_rate} mL/kg/hr). Extrapolated 24-hour output: {extrapolated_24h_str} mL (normal: 800-2000 mL). Current {fluid_status} of {abs(fluid_balance):.0f} mL. This is within acceptable range but monitor for trends. Ensure adequate hydration and evaluate if sustained at lower end of range with clinical signs of volume depletion."
            }
        elif urine_output_rate <= self.NORMAL_HIGH_THRESHOLD:
            return {
                "stage": "Normal",
                "description": "Normal urine output",
                "interpretation": f"Normal urine output ({urine_output_rate} mL/kg/hr) indicating adequate renal function and fluid balance. Extrapolated 24-hour output: {extrapolated_24h_str} mL (normal: 800-2000 mL). Current {fluid_status} of {abs(fluid_balance):.0f} mL. This range suggests normal kidney function and appropriate fluid status in most clinical contexts."
            }
        else:
            return {
                "stage": "Polyuria",
                "description": "High urine output",
                "interpretation": f"High urine output ({urine_output_rate} mL/kg/hr) indicating polyuria. Extrapolated 24-hour output: {extrapolated_24h_str} mL (normal: 800-2000 mL). Current {fluid_status} of {abs(fluid_balance):.0f} mL. Evaluate for diabetes insipidus, diabetes mellitus, diuretic use, excessive fluid intake, or resolving acute tubular necrosis. May require further investigation and management."
            }


def calculate_urine_output_fluid_balance(weight_kg: float, urine_output_ml: float, 
                                       collection_hours: float, fluid_intake_ml: float) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = UrineOutputFluidBalanceCalculator()
    return calculator.calculate(weight_kg, urine_output_ml, collection_hours, fluid_intake_ml)