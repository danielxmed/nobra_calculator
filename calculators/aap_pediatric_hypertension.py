"""
AAP Pediatric Hypertension Guidelines Calculator

Diagnostica hipertensão em pacientes pediátricos baseado nas diretrizes AAP 2017.
Referência: Flynn JT et al. Pediatrics. 2017;140(3):e20171904.
"""

import math
from typing import Dict, Any


class AAPPediatricHypertensionCalculator:
    """Calculadora para AAP Pediatric Hypertension Guidelines"""
    
    def __init__(self):
        # Tabelas simplificadas de percentis de altura por idade e sexo (WHO/CDC)
        # Para fins de implementação, usando valores aproximados
        self.height_percentiles = {
            "masculino": {
                1: {"p50": 76.1}, 2: {"p50": 87.8}, 3: {"p50": 96.1}, 4: {"p50": 103.3},
                5: {"p50": 109.9}, 6: {"p50": 116.1}, 7: {"p50": 121.9}, 8: {"p50": 128.0},
                9: {"p50": 133.3}, 10: {"p50": 138.4}, 11: {"p50": 143.5}, 12: {"p50": 149.1},
                13: {"p50": 156.2}, 14: {"p50": 163.8}, 15: {"p50": 170.1}, 16: {"p50": 173.4},
                17: {"p50": 175.2}
            },
            "feminino": {
                1: {"p50": 74.3}, 2: {"p50": 86.4}, 3: {"p50": 95.1}, 4: {"p50": 102.7},
                5: {"p50": 109.4}, 6: {"p50": 115.5}, 7: {"p50": 121.1}, 8: {"p50": 126.4},
                9: {"p50": 132.2}, 10: {"p50": 138.4}, 11: {"p50": 144.8}, 12: {"p50": 151.0},
                13: {"p50": 156.7}, 14: {"p50": 160.4}, 15: {"p50": 162.5}, 16: {"p50": 163.0},
                17: {"p50": 163.0}
            }
        }
        
        # Valores de referência simplificados para percentis de PA (baseado em tabelas AAP 2017)
        # Para implementação completa, seriam necessárias tabelas extensas por idade, sexo e percentil de altura
        self.bp_references = {
            "percentil_90": {"sys": 110, "dia": 70},
            "percentil_95": {"sys": 115, "dia": 75},
            "percentil_99": {"sys": 125, "dia": 82}
        }
    
    def calculate(self, age: int, sex: str, height: float, 
                 systolic_bp: int, diastolic_bp: int) -> Dict[str, Any]:
        """
        Classifica pressão arterial pediátrica conforme diretrizes AAP 2017
        
        Args:
            age: Idade em anos (1-17)
            sex: "masculino" ou "feminino"
            height: Altura em centímetros
            systolic_bp: Pressão sistólica em mmHg
            diastolic_bp: Pressão diastólica em mmHg
            
        Returns:
            Dict com classificação e interpretação
        """
        
        # Validações
        self._validate_inputs(age, sex, height, systolic_bp, diastolic_bp)
        
        # Calcular percentil de altura
        height_percentile = self._calculate_height_percentile(age, sex, height)
        
        # Determinar classificação para adolescentes ≥13 anos (critérios adultos híbridos)
        if age >= 13:
            classification = self._classify_adolescent_bp(systolic_bp, diastolic_bp, age, sex, height)
        else:
            # Para menores de 13 anos, usar tabelas pediátricas
            classification = self._classify_pediatric_bp(systolic_bp, diastolic_bp, age, sex, height_percentile)
        
        # Obter interpretação detalhada
        interpretation = self._get_interpretation(classification, age, systolic_bp, diastolic_bp)
        
        return {
            "result": classification,
            "unit": "classificação",
            "height_percentile": round(height_percentile, 1),
            "systolic_bp": systolic_bp,
            "diastolic_bp": diastolic_bp,
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, age: int, sex: str, height: float, 
                        systolic_bp: int, diastolic_bp: int):
        """Valida os parâmetros de entrada"""
        
        if not isinstance(age, int) or age < 1 or age > 17:
            raise ValueError("Idade deve ser um inteiro entre 1 e 17 anos")
        
        if sex not in ["masculino", "feminino"]:
            raise ValueError("Sexo deve ser 'masculino' ou 'feminino'")
        
        if not isinstance(height, (int, float)) or height < 70.0 or height > 200.0:
            raise ValueError("Altura deve estar entre 70.0 e 200.0 cm")
        
        if not isinstance(systolic_bp, int) or systolic_bp < 60 or systolic_bp > 200:
            raise ValueError("Pressão sistólica deve estar entre 60 e 200 mmHg")
        
        if not isinstance(diastolic_bp, int) or diastolic_bp < 30 or diastolic_bp > 150:
            raise ValueError("Pressão diastólica deve estar entre 30 e 150 mmHg")
        
        if systolic_bp <= diastolic_bp:
            raise ValueError("Pressão sistólica deve ser maior que a diastólica")
    
    def _calculate_height_percentile(self, age: int, sex: str, height: float) -> float:
        """
        Calcula percentil de altura aproximado baseado em altura mediana
        
        NOTA: Implementação simplificada. Para uso clínico real, 
        usar tabelas completas WHO/CDC com Z-scores.
        """
        
        if age not in self.height_percentiles[sex]:
            # Aproximação para idades não tabeladas
            closest_age = min(self.height_percentiles[sex].keys(), 
                            key=lambda x: abs(x - age))
            median_height = self.height_percentiles[sex][closest_age]["p50"]
        else:
            median_height = self.height_percentiles[sex][age]["p50"]
        
        # Estimativa simplificada de percentil baseada na diferença da mediana
        # Assumindo distribuição aproximadamente normal
        z_score = (height - median_height) / (median_height * 0.1)  # Desvio estimado
        percentile = self._z_to_percentile(z_score)
        
        return max(1.0, min(99.0, percentile))
    
    def _z_to_percentile(self, z_score: float) -> float:
        """Converte Z-score para percentil aproximado"""
        
        # Função de distribuição cumulativa normal padrão simplificada
        return 50.0 * (1.0 + math.erf(z_score / math.sqrt(2.0)))
    
    def _classify_adolescent_bp(self, systolic: int, diastolic: int, 
                               age: int, sex: str, height: float) -> str:
        """
        Classifica PA em adolescentes ≥13 anos usando critérios híbridos
        (combina percentis pediátricos com valores absolutos adultos)
        """
        
        # Para adolescentes, usar valores adultos se maiores que percentis pediátricos
        if systolic >= 140 or diastolic >= 90:
            return "Hipertensão Estágio 2"
        elif systolic >= 130 or diastolic >= 80:
            return "Hipertensão Estágio 1"
        elif systolic >= 120:
            return "Elevada"
        else:
            # Verificar também percentis pediátricos
            return self._classify_pediatric_bp(systolic, diastolic, age, sex, 50.0)
    
    def _classify_pediatric_bp(self, systolic: int, diastolic: int, 
                              age: int, sex: str, height_percentile: float) -> str:
        """
        Classifica PA usando tabelas pediátricas
        
        NOTA: Implementação simplificada com valores de referência aproximados.
        Para uso clínico real, usar tabelas completas AAP 2017.
        """
        
        # Ajuste aproximado baseado na idade (PA aumenta com idade)
        age_factor = 1.0 + (age - 5) * 0.02  # Incremento aproximado por ano
        
        # Ajuste aproximado baseado no percentil de altura
        height_factor = 1.0 + (height_percentile - 50) * 0.001  # Ajuste por altura
        
        # Valores de referência ajustados
        p90_sys = self.bp_references["percentil_90"]["sys"] * age_factor * height_factor
        p90_dia = self.bp_references["percentil_90"]["dia"] * age_factor * height_factor
        
        p95_sys = self.bp_references["percentil_95"]["sys"] * age_factor * height_factor
        p95_dia = self.bp_references["percentil_95"]["dia"] * age_factor * height_factor
        
        p99_sys = self.bp_references["percentil_99"]["sys"] * age_factor * height_factor
        p99_dia = self.bp_references["percentil_99"]["dia"] * age_factor * height_factor
        
        # Classificação baseada no maior percentil (sistólica ou diastólica)
        if systolic >= p99_sys or diastolic >= p99_dia:
            return "Hipertensão Estágio 2"
        elif systolic >= p95_sys or diastolic >= p95_dia:
            return "Hipertensão Estágio 1"
        elif systolic >= p90_sys or diastolic >= p90_dia:
            return "Elevada"
        else:
            return "Normal"
    
    def _get_interpretation(self, classification: str, age: int, 
                          systolic: int, diastolic: int) -> Dict[str, str]:
        """
        Fornece interpretação clínica baseada na classificação
        """
        
        interpretations = {
            "Normal": {
                "stage": "Normal",
                "description": "Pressão arterial normal",
                "interpretation": f"PA {systolic}/{diastolic} mmHg está abaixo do percentil 90 para idade, sexo e altura. Não requer intervenção específica. Recomenda-se manutenção de estilo de vida saudável e reavaliação anual."
            },
            "Elevada": {
                "stage": "Elevada",
                "description": "Pressão arterial elevada",
                "interpretation": f"PA {systolic}/{diastolic} mmHg está entre percentis 90-94 para idade, sexo e altura. Requer modificações do estilo de vida (dieta, exercício, redução de peso se necessário) e reavaliação em 6 meses. Avaliar fatores de risco cardiovascular."
            },
            "Hipertensão Estágio 1": {
                "stage": "Hipertensão Estágio 1",
                "description": "Hipertensão arterial estágio 1",
                "interpretation": f"PA {systolic}/{diastolic} mmHg está entre percentis 95-98 para idade, sexo e altura. Deve ser confirmada em 3 visitas diferentes. Iniciar modificações do estilo de vida e considerar medicação se fatores de risco presentes."
            },
            "Hipertensão Estágio 2": {
                "stage": "Hipertensão Estágio 2",
                "description": "Hipertensão arterial estágio 2",
                "interpretation": f"PA {systolic}/{diastolic} mmHg está ≥percentil 99 para idade, sexo e altura. Deve ser confirmada em 1-2 semanas. Requer tratamento medicamentoso imediato junto com modificações intensivas do estilo de vida. Investigar causas secundárias."
            }
        }
        
        return interpretations.get(classification, interpretations["Normal"])


def calculate_aap_pediatric_hypertension(age: int, sex: str, height: float,
                                       systolic_bp: int, diastolic_bp: int) -> Dict[str, Any]:
    """
    Função de conveniência para o sistema de carregamento dinâmico
    
    IMPORTANTE: Esta função deve seguir o padrão calculate_{score_id}
    """
    calculator = AAPPediatricHypertensionCalculator()
    return calculator.calculate(age, sex, height, systolic_bp, diastolic_bp)