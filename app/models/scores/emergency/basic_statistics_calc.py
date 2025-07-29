"""
Basic Statistics Calculator Models

Request and response models for Basic Statistics Calculator.

References (Vancouver style):
1. Altman DG, Bland JM. Diagnostic tests. 1: Sensitivity and specificity. BMJ. 1994 Jun 11;308(6943):1552.
2. Van der Helm HJ, Hische EA. Application of Bayes's theorem to results of quantitative clinical chemical determinations. Clin Chem. 1979 Jun;25(6):985-8.
3. Akobeng AK. Understanding diagnostic tests 1: sensitivity, specificity and predictive values. Acta Paediatr. 2007 Mar;96(3):338-41.
4. Laupacis A, Sackett DL, Roberts RS. An assessment of clinically useful measures of the consequences of treatment. N Engl J Med. 1988 Jun 30;318(26):1728-33.

The Basic Statistics Calculator provides comprehensive statistical analysis for diagnostic tests
and treatment outcomes, essential for evidence-based medicine decision making.
"""

from pydantic import BaseModel, Field, field_validator, ValidationInfo
from typing import Literal, Optional, Dict, Any, Union


class BasicStatisticsCalcRequest(BaseModel):
    """
    Request model for Basic Statistics Calculator
    
    This calculator supports two main types of analyses:
    
    1. Diagnostic Test Analysis:
       - Input Method A: Rates (prevalence, sensitivity, specificity as percentages)
       - Input Method B: Counts (true positives, false positives, false negatives, true negatives)
    
    2. Treatment Analysis:
       - Requires 2x2 contingency table data (A, B, C, D)
       - A: Experimental group with outcome
       - B: Experimental group without outcome
       - C: Control group with outcome
       - D: Control group without outcome
    
    The calculator computes various statistical measures including:
    - Sensitivity, Specificity, PPV, NPV
    - Likelihood ratios (positive and negative)
    - Relative risk, Odds ratio
    - Absolute and relative risk reduction
    - Number needed to treat (NNT)
    """
    
    calculation_type: Literal["diagnostic_test", "treatment"] = Field(
        ...,
        description="Type of calculation to perform. Choose 'diagnostic_test' for test performance metrics or 'treatment' for treatment effectiveness measures",
        example="diagnostic_test"
    )
    
    input_method: Optional[Literal["rates", "counts"]] = Field(
        None,
        description="Method of input for diagnostic test calculations. Use 'rates' for prevalence/sensitivity/specificity or 'counts' for TP/FP/FN/TN. Only required for diagnostic_test",
        example="rates"
    )
    
    # Diagnostic test parameters - rates method
    prevalence: Optional[float] = Field(
        None,
        description="Disease prevalence in the population (0-100%). Required for diagnostic test with 'rates' method",
        ge=0,
        le=100,
        example=10.0
    )
    
    sensitivity: Optional[float] = Field(
        None,
        description="Test sensitivity - probability of positive test when disease is present (0-100%). Required for diagnostic test with 'rates' method",
        ge=0,
        le=100,
        example=90.0
    )
    
    specificity: Optional[float] = Field(
        None,
        description="Test specificity - probability of negative test when disease is absent (0-100%). Required for diagnostic test with 'rates' method",
        ge=0,
        le=100,
        example=95.0
    )
    
    # Diagnostic test parameters - counts method
    true_positive: Optional[int] = Field(
        None,
        description="Number of true positive results (disease present, test positive). Required for diagnostic test with 'counts' method",
        ge=0,
        example=45
    )
    
    false_positive: Optional[int] = Field(
        None,
        description="Number of false positive results (disease absent, test positive). Required for diagnostic test with 'counts' method",
        ge=0,
        example=5
    )
    
    false_negative: Optional[int] = Field(
        None,
        description="Number of false negative results (disease present, test negative). Required for diagnostic test with 'counts' method",
        ge=0,
        example=5
    )
    
    true_negative: Optional[int] = Field(
        None,
        description="Number of true negative results (disease absent, test negative). Required for diagnostic test with 'counts' method",
        ge=0,
        example=95
    )
    
    # Treatment parameters
    experimental_with_outcome: Optional[int] = Field(
        None,
        description="Number of patients in experimental/treatment group who experienced the outcome (A). Required for treatment calculations",
        ge=0,
        example=20
    )
    
    experimental_without_outcome: Optional[int] = Field(
        None,
        description="Number of patients in experimental/treatment group who did not experience the outcome (B). Required for treatment calculations",
        ge=0,
        example=80
    )
    
    control_with_outcome: Optional[int] = Field(
        None,
        description="Number of patients in control group who experienced the outcome (C). Required for treatment calculations",
        ge=0,
        example=40
    )
    
    control_without_outcome: Optional[int] = Field(
        None,
        description="Number of patients in control group who did not experience the outcome (D). Required for treatment calculations",
        ge=0,
        example=60
    )
    
    @field_validator('input_method')
    def validate_input_method(cls, v, info: ValidationInfo):
        if info.data.get('calculation_type') == 'diagnostic_test' and v is None:
            # Auto-detect based on provided fields
            return None
        return v
    
    @field_validator('prevalence', 'sensitivity', 'specificity')
    def validate_rates_parameters(cls, v, info: ValidationInfo):
        if info.data.get('calculation_type') == 'diagnostic_test' and info.data.get('input_method') == 'rates':
            if v is None:
                raise ValueError(f"{info.field_name} is required when using 'rates' input method")
        return v
    
    @field_validator('true_positive', 'false_positive', 'false_negative', 'true_negative')
    def validate_counts_parameters(cls, v, info: ValidationInfo):
        if info.data.get('calculation_type') == 'diagnostic_test' and info.data.get('input_method') == 'counts':
            if v is None:
                raise ValueError(f"{info.field_name} is required when using 'counts' input method")
        return v
    
    @field_validator('experimental_with_outcome', 'experimental_without_outcome', 
                     'control_with_outcome', 'control_without_outcome')
    def validate_treatment_parameters(cls, v, info: ValidationInfo):
        if info.data.get('calculation_type') == 'treatment' and v is None:
            raise ValueError(f"{info.field_name} is required for treatment calculations")
        return v
    
    class Config:
        json_schema_extra = {
            "examples": [
                {
                    "title": "Diagnostic Test - Rates Method",
                    "value": {
                        "calculation_type": "diagnostic_test",
                        "input_method": "rates",
                        "prevalence": 10.0,
                        "sensitivity": 90.0,
                        "specificity": 95.0
                    }
                },
                {
                    "title": "Diagnostic Test - Counts Method",
                    "value": {
                        "calculation_type": "diagnostic_test",
                        "input_method": "counts",
                        "true_positive": 45,
                        "false_positive": 5,
                        "false_negative": 5,
                        "true_negative": 95
                    }
                },
                {
                    "title": "Treatment Analysis",
                    "value": {
                        "calculation_type": "treatment",
                        "experimental_with_outcome": 20,
                        "experimental_without_outcome": 80,
                        "control_with_outcome": 40,
                        "control_without_outcome": 60
                    }
                }
            ]
        }


class DiagnosticTestResult(BaseModel):
    """Result model for diagnostic test calculations"""
    
    # Input values (when counts method used)
    true_positive: Optional[int] = Field(None, description="Number of true positives")
    false_positive: Optional[int] = Field(None, description="Number of false positives")
    false_negative: Optional[int] = Field(None, description="Number of false negatives")
    true_negative: Optional[int] = Field(None, description="Number of true negatives")
    total: Optional[int] = Field(None, description="Total number of cases")
    
    # Core metrics
    prevalence: float = Field(..., description="Disease prevalence (%)")
    sensitivity: float = Field(..., description="Test sensitivity (%)")
    specificity: float = Field(..., description="Test specificity (%)")
    positive_predictive_value: float = Field(..., description="Positive predictive value (%)")
    negative_predictive_value: float = Field(..., description="Negative predictive value (%)")
    accuracy: Optional[float] = Field(None, description="Overall accuracy (%)")
    
    # Likelihood ratios
    positive_likelihood_ratio: float = Field(..., description="Positive likelihood ratio")
    negative_likelihood_ratio: float = Field(..., description="Negative likelihood ratio")
    
    # Pre/post-test probabilities (when rates method used)
    pre_test_probability: Optional[float] = Field(None, description="Pre-test probability (%)")
    post_test_probability_positive: Optional[float] = Field(None, description="Post-test probability if positive (%)")
    post_test_probability_negative: Optional[float] = Field(None, description="Post-test probability if negative (%)")


class TreatmentResult(BaseModel):
    """Result model for treatment calculations"""
    
    experimental_event_rate: float = Field(..., description="Event rate in experimental group (%)")
    control_event_rate: float = Field(..., description="Event rate in control group (%)")
    relative_risk: float = Field(..., description="Relative risk (RR)")
    relative_risk_ci: str = Field(..., description="95% confidence interval for RR")
    odds_ratio: float = Field(..., description="Odds ratio (OR)")
    odds_ratio_ci: str = Field(..., description="95% confidence interval for OR")
    absolute_risk_reduction: float = Field(..., description="Absolute risk reduction (%)")
    relative_risk_reduction: float = Field(..., description="Relative risk reduction (%)")
    number_needed_to_treat: Union[float, str] = Field(..., description="Number needed to treat (NNT)")


class BasicStatisticsCalcResponse(BaseModel):
    """
    Response model for Basic Statistics Calculator
    
    Returns comprehensive statistical analysis results based on the calculation type.
    
    For diagnostic tests:
    - Sensitivity, specificity, predictive values
    - Likelihood ratios
    - Pre/post-test probabilities
    
    For treatment analysis:
    - Event rates
    - Risk ratios (relative and absolute)
    - Odds ratio
    - Number needed to treat
    
    All results include appropriate confidence intervals where applicable.
    """
    
    result: Union[DiagnosticTestResult, TreatmentResult, Dict[str, Any]] = Field(
        ...,
        description="Comprehensive statistical analysis results",
        example={
            "prevalence": 10.0,
            "sensitivity": 90.0,
            "specificity": 95.0,
            "positive_predictive_value": 66.7,
            "negative_predictive_value": 98.8,
            "positive_likelihood_ratio": 18.0,
            "negative_likelihood_ratio": 0.11
        }
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the results",
        example="percent/ratio"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation of the statistical results with guidance for decision making",
        example="Very high sensitivity (≥95%): Excellent for ruling out disease when negative. High specificity (90-94%): Good for ruling in disease when positive. LR+ >10: Large and often conclusive increase in disease likelihood."
    )
    
    class Config:
        json_schema_extra = {
            "examples": [
                {
                    "title": "Diagnostic Test Result",
                    "value": {
                        "result": {
                            "prevalence": 10.0,
                            "sensitivity": 90.0,
                            "specificity": 95.0,
                            "positive_predictive_value": 66.7,
                            "negative_predictive_value": 98.8,
                            "positive_likelihood_ratio": 18.0,
                            "negative_likelihood_ratio": 0.11,
                            "pre_test_probability": 10.0,
                            "post_test_probability_positive": 66.7,
                            "post_test_probability_negative": 1.2
                        },
                        "unit": "percent/ratio",
                        "interpretation": "High sensitivity (90-94%): Good for ruling out disease when negative. Very high specificity (≥95%): Excellent for ruling in disease when positive. LR+ >10: Large and often conclusive increase in disease likelihood. LR- 0.1-0.2: Moderate decrease in disease likelihood."
                    }
                },
                {
                    "title": "Treatment Result",
                    "value": {
                        "result": {
                            "experimental_event_rate": 20.0,
                            "control_event_rate": 40.0,
                            "relative_risk": 0.5,
                            "relative_risk_ci": "(0.32 - 0.78)",
                            "odds_ratio": 0.375,
                            "odds_ratio_ci": "(0.20 - 0.71)",
                            "absolute_risk_reduction": -20.0,
                            "relative_risk_reduction": -50.0,
                            "number_needed_to_treat": 5
                        },
                        "unit": "percent/ratio",
                        "interpretation": "RR = 0.50: Treatment reduces risk of outcome by 50.0%. ARR = 20.0%: Treatment reduces absolute risk. NNT = 5: Need to treat 5 patients to prevent one adverse outcome."
                    }
                }
            ]
        }