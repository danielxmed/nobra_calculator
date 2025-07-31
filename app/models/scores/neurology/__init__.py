"""
Neurology score models
"""

from .abcd2 import Abcd2Request, Abcd2Response
from .four_at import FourAtRequest, FourAtResponse
from .abc2_ich_volume import Abc2IchVolumeRequest, Abc2IchVolumeResponse
from .aspects import AspectsRequest, AspectsResponse
from .ascod_algorithm import AscodAlgorithmRequest, AscodAlgorithmResponse
from .astral_score import AstralScoreRequest, AstralScoreResponse
from .awol_score import AwolScoreRequest, AwolScoreResponse
from .barnes_jewish_dysphagia import BarnesJewishDysphagiaRequest, BarnesJewishDysphagiaResponse
from .canadian_tia_score import CanadianTiaScoreRequest, CanadianTiaScoreResponse
from .cerebral_perfusion_pressure import CerebralPerfusionPressureRequest, CerebralPerfusionPressureResponse
from .clinical_dementia_rating import ClinicalDementiaRatingRequest, ClinicalDementiaRatingResponse
from .ndi import NdiRequest, NdiResponse
from .disease_steps_ms import DiseaseStepsMsRequest, DiseaseStepsMsResponse
from .dragon_score import DragonScoreRequest, DragonScoreResponse
from .embolic_stroke_undetermined_source_esus_criteria import EmbolicStrokeUndeterminedSourceEsusCriteriaRequest, EmbolicStrokeUndeterminedSourceEsusCriteriaResponse
from .neuropathic_pain_scale import NeuropathicPainScaleRequest, NeuropathicPainScaleResponse
from .new_orleans_charity_head_trauma import NewOrleansCharityHeadTraumaRequest, NewOrleansCharityHeadTraumaResponse
from .edss import EdssRequest, EdssResponse
from .fisher_grading_scale import FisherGradingScaleRequest, FisherGradingScaleResponse
from .four_score import FourScoreRequest, FourScoreResponse
from .gcs_pupils_score import GcsPupilsScoreRequest, GcsPupilsScoreResponse
from .glasgow_coma_scale import GlasgowComaScaleRequest, GlasgowComaScaleResponse
from .func_score import FuncScoreRequest, FuncScoreResponse
from .hat_score import HatScoreRequest, HatScoreResponse

__all__ = [
    "Abcd2Request",
    "Abcd2Response",
    "FourAtRequest",
    "FourAtResponse",
    "Abc2IchVolumeRequest",
    "Abc2IchVolumeResponse",
    "AspectsRequest",
    "AspectsResponse",
    "AscodAlgorithmRequest",
    "AscodAlgorithmResponse",
    "AstralScoreRequest",
    "AstralScoreResponse",
    "AwolScoreRequest",
    "AwolScoreResponse",
    "BarnesJewishDysphagiaRequest",
    "BarnesJewishDysphagiaResponse",
    "CanadianTiaScoreRequest",
    "CanadianTiaScoreResponse",
    "CerebralPerfusionPressureRequest",
    "CerebralPerfusionPressureResponse",
    "ClinicalDementiaRatingRequest",
    "ClinicalDementiaRatingResponse",
    "NdiRequest",
    "NdiResponse",
    "DiseaseStepsMsRequest",
    "DiseaseStepsMsResponse",
    "DragonScoreRequest",
    "DragonScoreResponse",
    "EmbolicStrokeUndeterminedSourceEsusCriteriaRequest",
    "EmbolicStrokeUndeterminedSourceEsusCriteriaResponse",
    "NeuropathicPainScaleRequest",
    "NeuropathicPainScaleResponse",
    "NewOrleansCharityHeadTraumaRequest",
    "NewOrleansCharityHeadTraumaResponse",
    "EdssRequest",
    "EdssResponse",
    "FisherGradingScaleRequest",
    "FisherGradingScaleResponse",
    "FourScoreRequest",
    "FourScoreResponse",
    "GcsPupilsScoreRequest",
    "GcsPupilsScoreResponse",
    "GlasgowComaScaleRequest",
    "GlasgowComaScaleResponse",
    "FuncScoreRequest",
    "FuncScoreResponse",
    "HatScoreRequest",
    "HatScoreResponse",
]
