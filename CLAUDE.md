# Guide for Programming Agents: Implementing New Calculators in nobra_calculator

This guide is intended for programming agents (AI assistants) to implement new medical calculators within the modular structure of the **nobra_calculator API**. 

## 🎯 Interactive Documentation Standards

The nobra_calculator now features a comprehensive interactive documentation system at `/docs-interactive` that provides:

- **Didactic Learning**: Each score includes detailed parameter explanations, validation rules, and clinical context
- **Interactive Calculators**: Real-time calculation with immediate result interpretation
- **Visual Interpretation Guides**: Color-coded severity levels and comprehensive range explanations
- **Complete Clinical Context**: References, formulas, notes, and clinical guidance

### Documentation Quality Requirements

When implementing new calculators, ensure they meet these enhanced standards:

1. **Complete Parameter Documentation**: Every parameter must have clear descriptions, units, validation rules, and clinical significance
2. **Comprehensive Interpretation Ranges**: All possible result ranges with detailed clinical interpretations and recommended actions
3. **Educational Content**: Include formulas, references, clinical notes, and context for medical education
4. **Robust Validation**: Implement thorough input validation with descriptive error messages
5. **Interactive Compatibility**: Ensure all metadata works seamlessly with the interactive documentation system

## 🤖 Automated Workflow

### Continuous Implementation Process

This document defines an automated flow where Claude Code works autonomously implementing medical calculators progressively:

1. **📋 Check Task List** - Consult `@CALC_LIST.md` to identify the next calculator to implement
2. **📖 Review Context** - Read `@README.md` to understand the current application and architecture
2.5. **Search on MDCALC via Tavily MCP** - Use Tavily search to find information on how to calculate the score in question, its interpretation, and citeable references. Preferably on MDCALC. CRITICAL STEP.
3. **🏗️ Implement Calculator** - Follow the steps described in this document
4. **✅ Mark Completion** - Update `@CALC_LIST.md` with a check for the implemented calculator
5. **🗜️ Compact Conversation** - Use the `/compact` command to optimize context
6. **🔄 Restart Cycle** - Return to step 1 for the next implementation

### Criteria for Selecting the Next Calculator

When consulting `@CALC_LIST.md`, prioritize calculators that:
- Do not have ✅ (not yet implemented)
- Are from fundamental medical categories (cardiology, nephrology, neurology)
- Have well-documented and standardized formulas
- Are widely used in clinical practice

### Process Automation

The agent must work autonomously following this flow:
- **Do not request confirmations** for each individual calculator
- **Completely implement** each calculator before proceeding
- **Test functionality** via reload and API checks
- **Adequately document** each implementation
- **Maintain quality** and consistency across all implementations

## 🏗️ API Architecture

### Directory Structure
```
nobra_calculator/
├── app/
│   ├── models/          # Pydantic Models (requests/responses)
│   ├── routers/         # API Endpoints
│   └── services/        # Business Logic (loading and execution)
├── calculators/         # ⭐ Python modules with calculation logic
├── scores/              # ⭐ Score Metadata (JSON)
├── main.py             # Main FastAPI application
└── requirements.txt    # Dependencies
```

### Workflow
1. **ScoreService** loads metadata from JSONs in `/scores/`
2. **CalculatorService** dynamically imports modules from `/calculators/`
3. **API Routes** expose endpoints for calculations and metadata
4. **Reload System** allows adding scores without restarting

## 📝 Implementing a New Calculator

### STEP 1: Create the JSON Metadata File

Create a file in `/scores/{score_id}.json` following this structure:

```json
{
  "id": "score_name",
  "title": "Full Score Title (include year if applicable)",
  "description": "Comprehensive description explaining what the score calculates, its clinical purpose, target population, and when it should be used. Include context about why this score was developed and its clinical significance.",
  "category": "medical_category",
  "version": "year_or_version",
  "parameters": [
    {
      "name": "parameter1",
      "type": "string|integer|float",
      "required": true,
      "description": "Detailed parameter description explaining clinical significance, how it's measured, and any important considerations for accurate input",
      "options": ["option1", "option2"],  // For strings with fixed values - include all possible options
      "validation": {
        "min": 0,           // For numbers - set realistic clinical ranges
        "max": 100,
        "enum": ["val1", "val2"]  // For strings - must match options array
      },
      "unit": "unit (be specific, e.g., 'mg/dL', 'years', 'mmHg')",
      "clinical_context": "Additional context about this parameter's clinical significance and measurement considerations"
    }
  ],
  "result": {
    "name": "result_name",
    "type": "float|integer|string",
    "unit": "result_unit (be specific)",
    "description": "Clear description of what the result represents and how it should be interpreted"
  },
  "interpretation": {
    "ranges": [
      {
        "min": 0,
        "max": 10,
        "stage": "Stage1/Normal/Mild/Moderate/Severe",
        "description": "Concise clinical description of this range",
        "interpretation": "Detailed clinical interpretation including recommended actions, follow-up, referrals, monitoring, and clinical significance. Be specific about next steps and clinical decision-making."
      }
    ]
  },
  "references": [
    "Complete bibliographic reference with authors, title, journal, year, volume, pages",
    "Include original validation studies and major clinical guidelines",
    "Add URLs for guidelines when available (e.g., professional society recommendations)"
  ],
  "formula": "Complete mathematical formula with all variables defined. Use clear notation and explain any constants or special functions.",
  "notes": [
    "Important clinical limitations and contraindications",
    "Population-specific considerations (age, gender, ethnicity)",
    "Measurement requirements and standardization notes",
    "Clinical pearls and common pitfalls to avoid",
    "Validation study populations and external validation data"
  ],
  "clinical_use": {
    "indications": ["Primary clinical indication 1", "Secondary use case 2"],
    "contraindications": ["When not to use this score"],
    "limitations": ["Known limitations and edge cases"],
    "population": "Target population description (age ranges, clinical settings, etc.)"
  }
}
```

### STEP 2: Implement the Python Calculator

Create a file in `/calculators/{score_id}.py` with this structure:

```python
"""
{Score Name} Calculator

Brief description of what it calculates and references.
"""

import math
from typing import Dict, Any


class {ScoreId}Calculator:
    """Calculator for {Score Name}"""
    
    def __init__(self):
        # Formula constants
        self.CONSTANT_1 = value
        self.CONSTANT_2 = value
    
    def calculate(self, param1: type, param2: type, param3: type) -> Dict[str, Any]:
        """
        Calculates the score using the provided parameters
        
        Args:
            param1 (type): Description of parameter 1
            param2 (type): Description of parameter 2
            param3 (type): Description of parameter 3
            
        Returns:
            Dict with the result and interpretation
        """
        
        # Validations
        self._validate_inputs(param1, param2, param3)
        
        # Calculation logic
        result = self._calculate_formula(param1, param2, param3)
        
        # Get interpretation
        interpretation = self._get_interpretation(result)
        
        return {
            "result": result,
            "unit": "unit",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation.get("stage", ""),
            "stage_description": interpretation.get("description", "")
        }
    
    def _validate_inputs(self, param1, param2, param3):
        """Validates input parameters"""
        
        # Specific validations for each parameter
        if not isinstance(param1, expected_type):
            raise ValueError("Param1 must be of type X")
        
        if param2 < min_value or param2 > max_value:
            raise ValueError(f"Param2 must be between {min_value} and {max_value}")
    
    def _calculate_formula(self, param1, param2, param3):
        """Implements the score's mathematical formula"""
        
        # Implement specific calculation logic
        result = param1 * param2 + param3  # Example
        
        # Round if necessary
        return round(result, 2)
    
    def _get_interpretation(self, result: float) -> Dict[str, str]:
        """
        Determines the interpretation based on the result
        
        Args:
            result (float): Calculated value
            
        Returns:
            Dict with interpretation
        """
        
        # Logic based on ranges defined in JSON
        if result >= 90:
            return {
                "stage": "Normal",
                "description": "Normal result",
                "interpretation": "Detailed clinical interpretation"
            }
        elif result >= 60:
            return {
                "stage": "Mild",
                "description": "Mild alteration",
                "interpretation": "Detailed clinical interpretation"
            }
        # ... more conditions
        
        else:
            return {
                "stage": "Severe",
                "description": "Severe alteration",
                "interpretation": "Detailed clinical interpretation"
            }


def calculate_{score_id}(param1, param2, param3) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = {ScoreId}Calculator()
    return calculator.calculate(param1, param2, param3)
```

### STEP 3: Create Pydantic Models (Optional)

If you want specific endpoints, add them to `/app/models/score_models.py`:

```python
class {ScoreId}Request(BaseModel):
    """Request model for {Score Name}"""
    param1: type = Field(..., description="Description")
    param2: int = Field(..., ge=min_val, le=max_val, description="Description")
    param3: float = Field(..., description="Description")
    
    class Config:
        schema_extra = {
            "example": {
                "param1": "example_value",
                "param2": 50,
                "param3": 1.5
            }
        }


class {ScoreId}Response(BaseModel):
    """Response model for {Score Name}"""
    result: float = Field(..., description="Calculation result")
    unit: str = Field(..., description="Result unit")
    interpretation: str = Field(..., description="Clinical interpretation")
    stage: str = Field(..., description="Stage/classification")
    stage_description: str = Field(..., description="Stage description")
```

### STEP 4: Add Specific Endpoint

In `/app/routers/scores.py`, add:

```python
@router.post("/{score_id}", response_model={ScoreId}Response)
async def calculate_{score_id}(request: {ScoreId}Request):
    """
    Calculates {Score Name}
    
    Args:
        request: Parameters needed for calculation
        
    Returns:
        {ScoreId}Response: Result with clinical interpretation
    """
    try:
        # Convert request to dictionary
        parameters = {
            "param1": request.param1,
            "param2": request.param2,
            "param3": request.param3
        }
        
        # Execute calculation
        result = calculator_service.calculate_score("{score_id}", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating {Score Name}",
                    "details": {"parameters": parameters}
                }
            )
        
        return {ScoreId}Response(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for {Score Name}",
                "details": {"error": str(e)}
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "error": "InternalServerError",
                "message": "Internal error in calculation",
                "details": {"error": str(e)}
            }
        )
```

## 🧪 Testing the Implementation

### Comprehensive Testing Protocol

Every implementation must pass this complete testing protocol:

### 1. Reload Scores and Verify Loading
```bash
curl -X POST http://localhost:8000/api/reload
```

### 2. Verify Score Appears in List
```bash
curl http://localhost:8000/api/scores | grep "score_id"
```

### 3. Check Complete Metadata
```bash
curl http://localhost:8000/api/scores/{score_id} | jq '.'
```

### 4. Test Valid Calculations (Multiple Test Cases)
```bash
# Test case 1: Normal values
curl -X POST http://localhost:8000/api/{score_id} \
  -H "Content-Type: application/json" \
  -d '{"param1": "normal_value", "param2": 50, "param3": 1.5}'

# Test case 2: Edge case - minimum values
curl -X POST http://localhost:8000/api/{score_id} \
  -H "Content-Type: application/json" \
  -d '{"param1": "min_value", "param2": 18, "param3": 0.1}'

# Test case 3: Edge case - maximum values
curl -X POST http://localhost:8000/api/{score_id} \
  -H "Content-Type: application/json" \
  -d '{"param1": "max_value", "param2": 120, "param3": 20.0}'
```

### 5. Test Input Validation (Error Cases)
```bash
# Test missing required parameter
curl -X POST http://localhost:8000/api/{score_id} \
  -H "Content-Type: application/json" \
  -d '{"param1": "value"}'

# Test invalid parameter type
curl -X POST http://localhost:8000/api/{score_id} \
  -H "Content-Type: application/json" \
  -d '{"param1": "value", "param2": "invalid", "param3": 1.5}'

# Test out-of-range values
curl -X POST http://localhost:8000/api/{score_id} \
  -H "Content-Type: application/json" \
  -d '{"param1": "value", "param2": -10, "param3": 1.5}'
```

### 6. Verify Interactive Documentation
```bash
# Check that the score appears in interactive docs
curl http://localhost:8000/docs-interactive/ | grep "score_id"
```

### 7. Test All Interpretation Ranges
Create test cases that produce results in each interpretation range to verify:
- Correct stage assignment
- Appropriate clinical interpretation
- Proper severity classification for UI color coding

### 8. Validate Clinical Accuracy
- Cross-reference calculations with published examples
- Verify formulas against original references
- Test edge cases mentioned in clinical literature
- Ensure interpretations match clinical guidelines

## ⚠️ Important Points

### Naming Conventions
- **score_id**: snake_case (e.g., `ckd_epi_2021`)
- **Calculator Class**: PascalCase + "Calculator" (e.g., `CkdEpi2021Calculator`)  
- **Convenience Function**: `calculate_{score_id}` (e.g., `calculate_ckd_epi_2021`)

### Mandatory Validations
- ✅ Validate parameter types
- ✅ Validate value ranges/limits
- ✅ Handle special cases (division by zero, negative values)
- ✅ Return descriptive errors

### Return Structure
The return **MUST** always have this minimum structure:
```python
{
    "result": float|int,           # Calculated value
    "unit": str,                   # Unit of measurement
    "interpretation": str,         # Clinical interpretation
    "stage": str,                  # Classification/stage (optional)
    "stage_description": str       # Stage description (optional)
}
```

## 🐛 Common Troubleshooting

### Error: "Score not found"
- ✅ Check if the JSON file exists in `/scores/`
- ✅ Check if the `id` in the JSON matches the file name
- ✅ Execute reload: `POST /api/reload`

### Error: "Calculator not found"
- ✅ Check if the Python file exists in `/calculators/`
- ✅ Check if the `calculate_{score_id}` function exists
- ✅ Check imports and Python syntax

### Error: "Invalid parameters"
- ✅ Check data types in parameters
- ✅ Check validation ranges
- ✅ Compare with JSON definitions

### Error: "Invalid JSON"
- ✅ Validate JSON syntax
- ✅ Check mandatory fields: `id`, `title`, `description`, `category`, `parameters`, `result`
- ✅ Check if `parameters` is an array and `result` is an object

## 📚 Complete Example: APGAR Score

### `/scores/apgar.json`
```json
{
  "id": "apgar",
  "title": "APGAR Score",
  "description": "Assessment of newborn vitality",
  "category": "neonatology",
  "version": "1953",
  "parameters": [
    {
      "name": "heart_rate",
      "type": "integer",
      "required": true,
      "description": "Heart rate (bpm)",
      "validation": {"min": 0, "max": 200},
      "unit": "bpm"
    },
    {
      "name": "respiratory_effort",
      "type": "string",
      "required": true,
      "description": "Respiratory effort",
      "options": ["absent", "irregular", "regular"],
      "validation": {"enum": ["absent", "irregular", "regular"]}
    }
  ],
  "result": {
    "name": "apgar_score",
    "type": "integer",
    "unit": "points",
    "description": "Total APGAR score"
  },
  "interpretation": {
    "ranges": [
      {
        "min": 8,
        "max": 10,
        "stage": "Normal",
        "description": "Newborn in good condition",
        "interpretation": "Vigorous newborn, no intervention needed."
      },
      {
        "min": 4,
        "max": 7,
        "stage": "Moderate",
        "description": "Moderate depression",
        "interpretation": "Needs stimulation and possible ventilation."
      },
      {
        "min": 0,
        "max": 3,
        "stage": "Severe",
        "description": "Severe asphyxia",
        "interpretation": "Needs immediate resuscitation."
      }
    ]
  },
  "references": [
    "Apgar V. A proposal for a new method of evaluation of the newborn infant. Curr Res Anesth Analg. 1953;32(4):260-7."
  ],
  "formula": "Sum of the 5 components: HR + Resp + Tone + Reflexes + Color",
  "notes": [
    "Assessment at 1 and 5 minutes of life",
    "Each component is worth 0-2 points"
  ]
}
```

### `/calculators/apgar.py`
```python
"""
APGAR Score Calculator

Assesses newborn vitality through 5 components.
"""

from typing import Dict, Any


class ApgarCalculator:
    """Calculator for APGAR Score"""
    
    def calculate(self, heart_rate: int, respiratory_effort: str, 
                 muscle_tone: str, reflexes: str, color: str) -> Dict[str, Any]:
        """
        Calculates the APGAR score
        
        Args:
            heart_rate: Heart rate in bpm
            respiratory_effort: "absent", "irregular", "regular"
            muscle_tone: "flaccid", "mild_flexion", "active_movement"
            reflexes: "absent", "grimace", "cry_cough"
            color: "cyanotic", "blue_extremities", "pink"
            
        Returns:
            Dict with result and interpretation
        """
        
        # Validations
        self._validate_inputs(heart_rate, respiratory_effort, muscle_tone, reflexes, color)
        
        # Calculate score for each component
        hr_score = self._score_heart_rate(heart_rate)
        resp_score = self._score_respiratory(respiratory_effort)
        tone_score = self._score_muscle_tone(muscle_tone)
        reflex_score = self._score_reflexes(reflexes)
        color_score = self._score_color(color)
        
        # Sum total
        total_score = hr_score + resp_score + tone_score + reflex_score + color_score
        
        # Get interpretation
        interpretation = self._get_interpretation(total_score)
        
        return {
            "result": total_score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, heart_rate, respiratory_effort, muscle_tone, reflexes, color):
        """Validates input parameters"""
        
        if not isinstance(heart_rate, int) or heart_rate < 0 or heart_rate > 200:
            raise ValueError("Heart rate must be an integer between 0 and 200")
        
        valid_resp = ["absent", "irregular", "regular"]
        if respiratory_effort not in valid_resp:
            raise ValueError(f"Respiratory effort must be: {', '.join(valid_resp)}")
        
        # More validations...
    
    def _score_heart_rate(self, hr: int) -> int:
        """Scores heart rate"""
        if hr == 0:
            return 0
        elif hr < 100:
            return 1
        else:
            return 2
    
    def _score_respiratory(self, effort: str) -> int:
        """Scores respiratory effort"""
        mapping = {"absent": 0, "irregular": 1, "regular": 2}
        return mapping[effort]
    
    def _get_interpretation(self, score: int) -> Dict[str, str]:
        """Interprets the APGAR score"""
        
        if score >= 8:
            return {
                "stage": "Normal",
                "description": "Newborn in good condition",
                "interpretation": "Vigorous newborn, no intervention needed."
            }
        elif score >= 4:
            return {
                "stage": "Moderate", 
                "description": "Moderate depression",
                "interpretation": "Needs stimulation and possible ventilation."
            }
        else:
            return {
                "stage": "Severe",
                "description": "Severe asphyxia", 
                "interpretation": "Needs immediate resuscitation."
            }


def calculate_apgar(heart_rate: int, respiratory_effort: str, muscle_tone: str, 
                   reflexes: str, color: str) -> Dict[str, Any]:
    """Convenience function for the dynamic loading system"""
    calculator = ApgarCalculator()
    return calculator.calculate(heart_rate, respiratory_effort, muscle_tone, reflexes, color)
```

## 🔄 Automated Implementation Protocol

### Detailed Flow per Iteration

For each implementation cycle, strictly follow:

#### 1. **📋 Consult CALC_LIST.md**
```
- Read file @CALC_LIST.md
- Identify first calculator without ✅
- Prioritize by clinical relevance and formula availability
- Select calculator for implementation
```

#### 2. **📖 Review README.md** 
```
- Read @README.md for application context
- Check current directory structure
- Confirm naming conventions
- Understand endpoint architecture
```

#### 3. **🏗️ Complete Implementation**
```
- Create JSON in /scores/{score_id}.json
- Implement calculator in /calculators/{score_id}.py
- Test with POST /api/reload
- Verify functionality via API
- Validate all input scenarios
```

#### 4. **✅ Update CALC_LIST.md**
```
- Add ✅ to the line of the implemented calculator
- Maintain original file formatting
- Confirm that the change was saved
```

#### 5. **🗜️ Compact Context**
```
- Execute /compact command
- Summarize implementations performed
- Prepare context for next cycle
```

#### 6. **🔄 Proceed Automatically**
```
- Return to step 1 without interruption
- Continue until list is exhausted or stop instruction is received
- Maintain quality and consistency across all implementations
```

### Quality Guidelines

- **Rigorous Validation**: Each calculator must have complete input validations
- **Functional Tests**: Always test reload and endpoints after implementation  
- **Complete Documentation**: Include bibliographic references and clinical notes
- **Consistent Naming**: Follow snake_case for IDs and PascalCase for classes
- **Clinical Interpretation**: Provide appropriate medical interpretations for each result

### Error Handling

- **Implementation Error**: Correct and retest before marking as complete
- **Incomplete Formula**: Seek additional references or skip to the next calculator
- **Naming Conflict**: Adapt name following established conventions

## 🎯 Summary of Steps

1. **Create JSON** in `/scores/{score_id}.json` with complete metadata
2. **Implement calculator** in `/calculators/{score_id}.py` with `calculate_{score_id}` function  
3. **Test** via reload and API endpoints
4. **Add Pydantic models** (optional) for specific endpoints
5. **Document** references and formulas appropriately
6. **Mark as complete** in CALC_LIST.md
7. **Compact conversation** and restart cycle

## 🔄 Enhancing Existing Scores

### Upgrading Legacy Implementations

When enhancing existing scores to meet the new interactive documentation standards:

#### 1. **Audit Current Implementation**
```bash
# Check current metadata completeness
curl http://localhost:8000/api/scores/{score_id} | jq '.clinical_use // "missing"'
curl http://localhost:8000/api/scores/{score_id} | jq '.parameters[].clinical_context // "missing"'
```

#### 2. **Research Enhancement Requirements**
- Review original clinical literature for missing context
- Check for updated guidelines or validation studies
- Identify gaps in parameter descriptions or interpretation ranges
- Look for clinical pearls and common pitfalls

#### 3. **Update JSON Metadata**
- Add missing `clinical_use` section
- Enhance parameter descriptions with clinical context
- Expand interpretation ranges with specific clinical actions
- Add comprehensive references and clinical notes
- Include formula explanations and variable definitions

#### 4. **Enhance Calculator Logic**
- Improve error messages for better user guidance
- Add validation for clinical edge cases
- Ensure robust handling of boundary conditions
- Verify calculation accuracy against multiple test cases

#### 5. **Validate Enhanced Implementation**
- Test all new interpretation ranges
- Verify enhanced error messages
- Check interactive documentation display
- Validate clinical accuracy with published examples

### Priority Enhancement List

Focus on enhancing these commonly used scores first:
1. **CKD-EPI 2021** - Add clinical context for creatinine standardization
2. **CHA₂DS₂-VASc** - Enhance stroke risk interpretations with specific recommendations
3. **CURB-65** - Add detailed admission criteria and treatment guidance
4. **4C COVID-19** - Include updated mortality risk interpretations

### Quality Assurance Checklist

Before marking any score as "enhanced":
- [ ] All parameters have clinical context explanations
- [ ] Interpretation ranges include specific clinical actions
- [ ] References include original validation studies
- [ ] Clinical use section is complete
- [ ] Formula is fully explained with variable definitions
- [ ] Notes include limitations and clinical pearls
- [ ] Interactive documentation displays correctly
- [ ] All test cases pass validation
- [ ] Clinical accuracy verified against literature

## 🎓 Educational Implementation Guidelines

### Making Scores Didactic

Each implementation should serve as a learning tool:

#### Parameter Education
- Explain why each parameter is clinically relevant
- Describe how parameters are typically measured
- Include normal ranges and clinical significance
- Note measurement standardization requirements

#### Result Interpretation Education
- Explain the clinical reasoning behind score ranges
- Describe the evidence base for interpretations
- Include specific next steps for each result level
- Note limitations and when to use clinical judgment

#### Clinical Context Education
- Explain when and why the score was developed
- Describe the target population and clinical setting
- Include validation study details and external validation
- Note updates or modifications to original score

### Interactive Learning Features

The interactive documentation should enable:
- **Progressive Disclosure**: Basic info → detailed explanations → clinical pearls
- **Contextual Help**: Parameter tooltips with clinical significance
- **Visual Learning**: Color-coded severity levels and range visualization
- **Practical Application**: Real-time calculation with immediate interpretation

By following this enhanced guide, any programming agent can implement new medical calculators in nobra_calculator that are not only functionally correct but also educationally valuable and clinically robust! 🚀
