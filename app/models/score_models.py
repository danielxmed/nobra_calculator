"""
Modelos Pydantic para requests e responses da API
"""

from pydantic import BaseModel, Field, field_validator
from typing import List, Optional, Dict, Any, Union
from enum import Enum


class SexType(str, Enum):
    """Enum para os tipos de sexo aceitos"""
    MASCULINO = "masculino"
    FEMININO = "feminino"


# Request Models
class CKDEpi2021Request(BaseModel):
    """Modelo de request para CKD-EPI 2021"""
    sex: SexType = Field(..., description="Sexo do paciente")
    age: int = Field(..., ge=18, le=120, description="Idade do paciente em anos")
    serum_creatinine: float = Field(..., ge=0.1, le=20.0, description="Creatinina sérica em mg/dL")
    
    class Config:
        schema_extra = {
            "example": {
                "sex": "feminino",
                "age": 65,
                "serum_creatinine": 1.2
            }
        }


# Response Models
class CKDEpi2021Response(BaseModel):
    """Modelo de response para CKD-EPI 2021"""
    result: float = Field(..., description="Taxa de filtração glomerular estimada")
    unit: str = Field(..., description="Unidade do resultado")
    interpretation: str = Field(..., description="Interpretação clínica do resultado")
    stage: str = Field(..., description="Estágio da doença renal crônica")
    stage_description: str = Field(..., description="Descrição do estágio")
    
    class Config:
        schema_extra = {
            "example": {
                "result": 52.3,
                "unit": "mL/min/1.73 m²",
                "interpretation": "Estágio 3a de Doença Renal Crônica. Acompanhamento nefrológico recomendado.",
                "stage": "G3a",
                "stage_description": "Diminuição leve a moderada da TFG"
            }
        }


class ScoreInfo(BaseModel):
    """Informações básicas de um score"""
    id: str = Field(..., description="ID único do score")
    title: str = Field(..., description="Título do score")
    description: str = Field(..., description="Descrição do score")
    category: str = Field(..., description="Categoria médica do score")
    version: Optional[str] = Field(None, description="Versão do score")


class ScoreListResponse(BaseModel):
    """Response para listagem de scores disponíveis"""
    scores: List[ScoreInfo] = Field(..., description="Lista de scores disponíveis")
    total: int = Field(..., description="Total de scores disponíveis")
    
    class Config:
        schema_extra = {
            "example": {
                "scores": [
                    {
                        "id": "ckd_epi_2021",
                        "title": "CKD-EPI 2021 - Taxa de Filtração Glomerular Estimada",
                        "description": "Equação CKD-EPI 2021 para estimar a taxa de filtração glomerular",
                        "category": "nefrologia",
                        "version": "2021"
                    }
                ],
                "total": 1
            }
        }


class Parameter(BaseModel):
    """Modelo para parâmetros de um score"""
    name: str = Field(..., description="Nome do parâmetro")
    type: str = Field(..., description="Tipo do parâmetro")
    required: bool = Field(..., description="Se o parâmetro é obrigatório")
    description: str = Field(..., description="Descrição do parâmetro")
    options: Optional[List[str]] = Field(None, description="Opções válidas para o parâmetro")
    validation: Optional[Dict[str, Any]] = Field(None, description="Regras de validação")
    unit: Optional[str] = Field(None, description="Unidade do parâmetro")


class ResultInfo(BaseModel):
    """Informações sobre o resultado de um score"""
    name: str = Field(..., description="Nome do resultado")
    type: str = Field(..., description="Tipo do resultado")
    unit: str = Field(..., description="Unidade do resultado")
    description: str = Field(..., description="Descrição do resultado")


class InterpretationRange(BaseModel):
    """Range de interpretação de um score"""
    min: float = Field(..., description="Valor mínimo do range")
    max: Optional[float] = Field(None, description="Valor máximo do range")
    stage: str = Field(..., description="Estágio ou classificação")
    description: str = Field(..., description="Descrição do estágio")
    interpretation: str = Field(..., description="Interpretação clínica")


class Interpretation(BaseModel):
    """Modelo para interpretações de um score"""
    ranges: List[InterpretationRange] = Field(..., description="Ranges de interpretação")


class ScoreMetadataResponse(BaseModel):
    """Response detalhada dos metadados de um score"""
    id: str = Field(..., description="ID único do score")
    title: str = Field(..., description="Título do score")
    description: str = Field(..., description="Descrição detalhada do score")
    category: str = Field(..., description="Categoria médica do score")
    version: Optional[str] = Field(None, description="Versão do score")
    parameters: List[Parameter] = Field(..., description="Parâmetros necessários para o cálculo")
    result: ResultInfo = Field(..., description="Informações sobre o resultado")
    interpretation: Interpretation = Field(..., description="Interpretações do resultado")
    references: List[str] = Field(..., description="Referências bibliográficas")
    formula: str = Field(..., description="Fórmula matemática do cálculo")
    notes: List[str] = Field(..., description="Notas importantes sobre o score")


class ErrorResponse(BaseModel):
    """Modelo para respostas de erro"""
    error: str = Field(..., description="Tipo do erro")
    message: str = Field(..., description="Mensagem de erro")
    details: Optional[Dict[str, Any]] = Field(None, description="Detalhes adicionais do erro")
    
    class Config:
        schema_extra = {
            "example": {
                "error": "ValidationError",
                "message": "Parâmetros inválidos fornecidos",
                "details": {
                    "field": "age",
                    "value": 15,
                    "constraint": "must be >= 18"
                }
            }
        }


class HealthResponse(BaseModel):
    """Response para endpoint de health check"""
    status: str = Field(..., description="Status da API")
    message: str = Field(..., description="Mensagem de status")
    version: str = Field(..., description="Versão da API")
    
    class Config:
        schema_extra = {
            "example": {
                "status": "healthy",
                "message": "nobra_calculator API está funcionando corretamente",
                "version": "1.0.0"
            }
        }


class Cha2ds2VascRequest(BaseModel):
    """Modelo de request para CHA₂DS₂-VASc Score"""
    age: int = Field(..., ge=18, le=120, description="Idade do paciente em anos")
    sex: SexType = Field(..., description="Sexo biológico do paciente")
    congestive_heart_failure: bool = Field(..., description="História de insuficiência cardíaca congestiva ou disfunção VE (FEVE ≤40%)")
    hypertension: bool = Field(..., description="História de hipertensão arterial")
    stroke_tia_thromboembolism: bool = Field(..., description="História prévia de AVC, AIT ou tromboembolismo")
    vascular_disease: bool = Field(..., description="Doença vascular (IAM prévio, DAP ou placa aórtica)")
    diabetes: bool = Field(..., description="História de diabetes mellitus")
    
    class Config:
        schema_extra = {
            "example": {
                "age": 75,
                "sex": "feminino",
                "congestive_heart_failure": True,
                "hypertension": True,
                "stroke_tia_thromboembolism": False,
                "vascular_disease": False,
                "diabetes": True
            }
        }


class Cha2ds2VascResponse(BaseModel):
    """Modelo de response para CHA₂DS₂-VASc Score"""
    result: int = Field(..., description="Escore CHA₂DS₂-VASc total (0-9 pontos)")
    unit: str = Field(..., description="Unidade do resultado")
    interpretation: str = Field(..., description="Interpretação clínica e recomendação de anticoagulação")
    stage: str = Field(..., description="Classificação de risco")
    stage_description: str = Field(..., description="Descrição do nível de risco")
    annual_stroke_risk: str = Field(..., description="Risco anual de AVC em porcentagem")
    components: Dict[str, int] = Field(..., description="Pontuação de cada componente do score")
    
    class Config:
        schema_extra = {
            "example": {
                "result": 5,
                "unit": "pontos",
                "interpretation": "Anticoagulação oral mandatória. Considerar estratégias para melhorar aderência e minimizar risco de sangramento.",
                "stage": "Alto Risco",
                "stage_description": "Risco anual de AVC: 10.0%",
                "annual_stroke_risk": "10.0%",
                "components": {
                    "congestive_heart_failure": 1,
                    "hypertension": 1,
                    "age_points": 2,
                    "diabetes": 1,
                    "stroke_tia": 0,
                    "vascular_disease": 0,
                    "sex_category": 1
                }
            }
        }


class Curb65Request(BaseModel):
    """Modelo de request para CURB-65 Score"""
    confusion: bool = Field(..., description="Confusão mental de início recente (desorientação em tempo, espaço ou pessoa)")
    urea: float = Field(..., ge=0, le=200, description="Ureia sérica em mg/dL")
    respiratory_rate: int = Field(..., ge=0, le=60, description="Frequência respiratória (respirações/min)")
    systolic_bp: int = Field(..., ge=0, le=300, description="Pressão arterial sistólica (mmHg)")
    diastolic_bp: int = Field(..., ge=0, le=200, description="Pressão arterial diastólica (mmHg)")
    age: int = Field(..., ge=0, le=120, description="Idade do paciente em anos")
    
    @field_validator('diastolic_bp')
    def validate_blood_pressure(cls, v, info):
        if 'systolic_bp' in info.data and v > info.data['systolic_bp']:
            raise ValueError('Pressão diastólica não pode ser maior que a sistólica')
        return v
    
    class Config:
        schema_extra = {
            "example": {
                "confusion": False,
                "urea": 25.0,
                "respiratory_rate": 32,
                "systolic_bp": 85,
                "diastolic_bp": 55,
                "age": 78
            }
        }


class Curb65Response(BaseModel):
    """Modelo de response para CURB-65 Score"""
    result: int = Field(..., description="Score CURB-65 total (0-5 pontos)")
    unit: str = Field(..., description="Unidade do resultado")
    interpretation: str = Field(..., description="Interpretação clínica e recomendação de tratamento")
    stage: str = Field(..., description="Classificação de risco")
    stage_description: str = Field(..., description="Descrição do nível de risco")
    mortality_risk: str = Field(..., description="Risco de mortalidade em porcentagem")
    components: Dict[str, int] = Field(..., description="Pontuação de cada componente do score")
    
    class Config:
        schema_extra = {
            "example": {
                "result": 3,
                "unit": "pontos",
                "interpretation": "Internação hospitalar mandatória. Considerar admissão em UTI, especialmente se CURB-65 ≥ 4. Iniciar antibioticoterapia endovenosa imediatamente.",
                "stage": "Alto Risco",
                "stage_description": "Mortalidade: 22%",
                "mortality_risk": "22%",
                "components": {
                    "confusion": 0,
                    "urea": 1,
                    "respiratory_rate": 1,
                    "blood_pressure": 1,
                    "age": 1
                }
            }
        }
