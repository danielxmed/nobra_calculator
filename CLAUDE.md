# Guia para Agentes de Programação: Implementando Novas Calculadoras na nobra_calculator

Este guia é destinado a agentes de programação (IA assistants) para implementar novas calculadoras médicas na estrutura modular da **nobra_calculator API**.

## 🤖 Fluxo de Trabalho Automatizado

### Processo Contínuo de Implementação

Este documento define um fluxo automatizado onde o Claude Code trabalha de forma autônoma implementando calculadoras médicas progressivamente:

1. **📋 Verificar Lista de Tarefas** - Consultar `@CALC_LIST.md` para identificar próxima calculadora a implementar
2. **📖 Revisar Contexto** - Ler `@README.md` para entender aplicação e arquitetura atual
2.5. **Pesquisar no MDCALC via Tavily MCP** - Usar o tavily search para encontrar informacoes sobre como calcular o score em questao, sua interpretacao e referencias citaveis. Preferencialmente no MDCALC. ETAPA CRÍTICA.
3. **🏗️ Implementar Calculadora** - Seguir etapas descritas neste documento
4. **✅ Marcar Conclusão** - Atualizar `@CALC_LIST.md` com check da calculadora implementada
5. **🗜️ Compactar Conversa** - Usar comando `/compact` para otimizar contexto
6. **🔄 Reiniciar Ciclo** - Retornar ao passo 1 para próxima implementação

### Critérios para Seleção da Próxima Calculadora

Ao consultar `@CALC_LIST.md`, priorizar calculadoras que:
- Não possuem ✅ (ainda não implementadas)
- São de categorias médicas fundamentais (cardiologia, nefrologia, neurologia)
- Têm fórmulas bem documentadas e padronizadas
- São amplamente utilizadas na prática clínica

### Automação do Processo

O agente deve trabalhar de forma autônoma seguindo este fluxo:
- **Não solicitar confirmações** para cada calculadora individual
- **Implementar completamente** cada calculadora antes de prosseguir
- **Testar funcionamento** via reload e verificações de API
- **Documentar adequadamente** cada implementação
- **Manter qualidade** e consistência em todas as implementações

## 🏗️ Arquitetura da API

### Estrutura de Diretórios
```
nobra_calculator/
├── app/
│   ├── models/          # Modelos Pydantic (requests/responses)
│   ├── routers/         # Endpoints da API
│   └── services/        # Lógica de negócio (carregamento e execução)
├── calculators/         # ⭐ Módulos Python com lógica de cálculo
├── scores/              # ⭐ Metadados JSON dos scores
├── main.py             # Aplicação FastAPI principal
└── requirements.txt    # Dependências
```

### Fluxo de Funcionamento
1. **ScoreService** carrega metadados dos JSONs em `/scores/`
2. **CalculatorService** importa dinamicamente módulos de `/calculators/`
3. **API Routes** expõem endpoints para cálculos e metadados
4. **Sistema de Reload** permite adicionar scores sem reiniciar

## 📝 Implementando Uma Nova Calculadora

### PASSO 1: Criar o Arquivo de Metadados JSON

Crie um arquivo em `/scores/{score_id}.json` seguindo esta estrutura:

```json
{
  "id": "nome_do_score",
  "title": "Título Completo do Score",
  "description": "Descrição detalhada do que o score calcula",
  "category": "categoria_medica",
  "version": "ano_ou_versao",
  "parameters": [
    {
      "name": "parametro1",
      "type": "string|integer|float",
      "required": true,
      "description": "Descrição do parâmetro",
      "options": ["opcao1", "opcao2"],  // Para strings com valores fixos
      "validation": {
        "min": 0,           // Para números
        "max": 100,
        "enum": ["val1", "val2"]  // Para strings
      },
      "unit": "unidade"
    }
  ],
  "result": {
    "name": "nome_resultado",
    "type": "float|integer|string",
    "unit": "unidade_resultado",
    "description": "Descrição do resultado"
  },
  "interpretation": {
    "ranges": [
      {
        "min": 0,
        "max": 10,
        "stage": "Estágio1",
        "description": "Descrição curta",
        "interpretation": "Interpretação clínica detalhada"
      }
    ]
  },
  "references": [
    "Referência bibliográfica 1",
    "Referência bibliográfica 2"
  ],
  "formula": "Fórmula matemática em texto",
  "notes": [
    "Nota importante 1",
    "Nota importante 2"
  ]
}
```

### PASSO 2: Implementar a Calculadora Python

Crie um arquivo em `/calculators/{score_id}.py` com esta estrutura:

```python
"""
{Score Name} Calculator

Breve descrição do que calcula e referências.
"""

import math
from typing import Dict, Any


class {ScoreId}Calculator:
    """Calculadora para {Score Name}"""
    
    def __init__(self):
        # Constantes da fórmula
        self.CONSTANTE_1 = valor
        self.CONSTANTE_2 = valor
    
    def calculate(self, param1: type, param2: type, param3: type) -> Dict[str, Any]:
        """
        Calcula o score usando os parâmetros fornecidos
        
        Args:
            param1 (type): Descrição do parâmetro 1
            param2 (type): Descrição do parâmetro 2
            param3 (type): Descrição do parâmetro 3
            
        Returns:
            Dict com o resultado e interpretação
        """
        
        # Validações
        self._validate_inputs(param1, param2, param3)
        
        # Lógica do cálculo
        resultado = self._calcular_formula(param1, param2, param3)
        
        # Obter interpretação
        interpretation = self._get_interpretation(resultado)
        
        return {
            "result": resultado,
            "unit": "unidade",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation.get("stage", ""),
            "stage_description": interpretation.get("description", "")
        }
    
    def _validate_inputs(self, param1, param2, param3):
        """Valida os parâmetros de entrada"""
        
        # Validações específicas para cada parâmetro
        if not isinstance(param1, expected_type):
            raise ValueError("Param1 deve ser do tipo X")
        
        if param2 < min_value or param2 > max_value:
            raise ValueError(f"Param2 deve estar entre {min_value} e {max_value}")
    
    def _calcular_formula(self, param1, param2, param3):
        """Implementa a fórmula matemática do score"""
        
        # Implementar a lógica específica do cálculo
        resultado = param1 * param2 + param3  # Exemplo
        
        # Arredondar se necessário
        return round(resultado, 2)
    
    def _get_interpretation(self, resultado: float) -> Dict[str, str]:
        """
        Determina a interpretação baseada no resultado
        
        Args:
            resultado (float): Valor calculado
            
        Returns:
            Dict com interpretação
        """
        
        # Lógica baseada nos ranges definidos no JSON
        if resultado >= 90:
            return {
                "stage": "Normal",
                "description": "Resultado normal",
                "interpretation": "Interpretação clínica detalhada"
            }
        elif resultado >= 60:
            return {
                "stage": "Leve",
                "description": "Alteração leve",
                "interpretation": "Interpretação clínica detalhada"
            }
        # ... mais condições
        
        else:
            return {
                "stage": "Grave",
                "description": "Alteração grave",
                "interpretation": "Interpretação clínica detalhada"
            }


def calculate_{score_id}(param1, param2, param3) -> Dict[str, Any]:
    """
    Função de conveniência para o sistema de carregamento dinâmico
    
    IMPORTANTE: Esta função deve seguir o padrão calculate_{score_id}
    """
    calculator = {ScoreId}Calculator()
    return calculator.calculate(param1, param2, param3)
```

### PASSO 3: Criar Modelos Pydantic (Opcional)

Se quiser endpoints específicos, adicione em `/app/models/score_models.py`:

```python
class {ScoreId}Request(BaseModel):
    """Modelo de request para {Score Name}"""
    param1: type = Field(..., description="Descrição")
    param2: int = Field(..., ge=min_val, le=max_val, description="Descrição")
    param3: float = Field(..., description="Descrição")
    
    class Config:
        schema_extra = {
            "example": {
                "param1": "valor_exemplo",
                "param2": 50,
                "param3": 1.5
            }
        }


class {ScoreId}Response(BaseModel):
    """Modelo de response para {Score Name}"""
    result: float = Field(..., description="Resultado do cálculo")
    unit: str = Field(..., description="Unidade do resultado")
    interpretation: str = Field(..., description="Interpretação clínica")
    stage: str = Field(..., description="Estágio/classificação")
    stage_description: str = Field(..., description="Descrição do estágio")
```

### PASSO 4: Adicionar Endpoint Específico (Opcional)

Em `/app/routers/scores.py`, adicione:

```python
@router.post("/{score_id}", response_model={ScoreId}Response)
async def calculate_{score_id}(request: {ScoreId}Request):
    """
    Calcula {Score Name}
    
    Args:
        request: Parâmetros necessários para o cálculo
        
    Returns:
        {ScoreId}Response: Resultado com interpretação clínica
    """
    try:
        # Converte request para dicionário
        parameters = {
            "param1": request.param1,
            "param2": request.param2,
            "param3": request.param3
        }
        
        # Executa o cálculo
        result = calculator_service.calculate_score("{score_id}", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Erro no cálculo do {Score Name}",
                    "details": {"parameters": parameters}
                }
            )
        
        return {ScoreId}Response(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Parâmetros inválidos para {Score Name}",
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
                "message": "Erro interno no cálculo",
                "details": {"error": str(e)}
            }
        )
```

## 🧪 Testando a Implementação

### 1. Recarregar Scores
```bash
curl -X POST http://localhost:8000/api/reload
```

### 2. Verificar se o Score Aparece na Lista
```bash
curl http://localhost:8000/api/scores
```

### 3. Testar o Cálculo
```bash
curl -X POST http://localhost:8000/api/{score_id} \
  -H "Content-Type: application/json" \
  -d '{"param1": "valor", "param2": 50, "param3": 1.5}'
```

### 4. Verificar Metadados
```bash
curl http://localhost:8000/api/scores/{score_id}
```

## ⚠️ Pontos Importantes

### Convenções de Nomenclatura
- **score_id**: snake_case (ex: `ckd_epi_2021`)
- **Classe Calculator**: PascalCase + "Calculator" (ex: `CkdEpi2021Calculator`)  
- **Função de conveniência**: `calculate_{score_id}` (ex: `calculate_ckd_epi_2021`)

### Validações Obrigatórias
- ✅ Validar tipos de parâmetros
- ✅ Validar ranges/limites dos valores
- ✅ Tratar casos especiais (divisão por zero, valores negativos)
- ✅ Retornar erros descritivos

### Estrutura do Retorno
O retorno **DEVE** sempre ter esta estrutura mínima:
```python
{
    "result": float|int,           # Valor calculado
    "unit": str,                   # Unidade de medida
    "interpretation": str,         # Interpretação clínica
    "stage": str,                  # Classificação/estágio (opcional)
    "stage_description": str       # Descrição da classificação (opcional)
}
```

## 🐛 Troubleshooting Comum

### Erro: "Score não encontrado"
- ✅ Verificar se o arquivo JSON existe em `/scores/`
- ✅ Verificar se o `id` no JSON corresponde ao nome do arquivo
- ✅ Executar reload: `POST /api/reload`

### Erro: "Calculadora não encontrada"
- ✅ Verificar se o arquivo Python existe em `/calculators/`
- ✅ Verificar se a função `calculate_{score_id}` existe
- ✅ Verificar imports e sintaxe do Python

### Erro: "Parâmetros inválidos"
- ✅ Verificar tipos de dados nos parâmetros
- ✅ Verificar ranges de validação
- ✅ Comparar com definições no JSON

### Erro: "JSON inválido"
- ✅ Validar sintaxe JSON
- ✅ Verificar campos obrigatórios: `id`, `title`, `description`, `category`, `parameters`, `result`
- ✅ Verificar se `parameters` é array e `result` é object

## 📚 Exemplo Completo: Score APGAR

### `/scores/apgar.json`
```json
{
  "id": "apgar",
  "title": "Escore de APGAR",
  "description": "Avaliação da vitalidade do recém-nascido",
  "category": "neonatologia",
  "version": "1953",
  "parameters": [
    {
      "name": "heart_rate",
      "type": "integer",
      "required": true,
      "description": "Frequência cardíaca (bpm)",
      "validation": {"min": 0, "max": 200},
      "unit": "bpm"
    },
    {
      "name": "respiratory_effort",
      "type": "string",
      "required": true,
      "description": "Esforço respiratório",
      "options": ["ausente", "irregular", "regular"],
      "validation": {"enum": ["ausente", "irregular", "regular"]}
    }
  ],
  "result": {
    "name": "apgar_score",
    "type": "integer",
    "unit": "pontos",
    "description": "Escore APGAR total"
  },
  "interpretation": {
    "ranges": [
      {
        "min": 8,
        "max": 10,
        "stage": "Normal",
        "description": "Recém-nascido em boas condições",
        "interpretation": "RN vigoroso, sem necessidade de intervenção."
      },
      {
        "min": 4,
        "max": 7,
        "stage": "Moderado",
        "description": "Depressão moderada",
        "interpretation": "Necessita estimulação e possível ventilação."
      },
      {
        "min": 0,
        "max": 3,
        "stage": "Grave",
        "description": "Asfixia grave",
        "interpretation": "Necessita reanimação imediata."
      }
    ]
  },
  "references": [
    "Apgar V. A proposal for a new method of evaluation of the newborn infant. Curr Res Anesth Analg. 1953;32(4):260-7."
  ],
  "formula": "Soma dos 5 componentes: FC + Resp + Tônus + Reflexos + Cor",
  "notes": [
    "Avaliação aos 1 e 5 minutos de vida",
    "Cada componente vale 0-2 pontos"
  ]
}
```

### `/calculators/apgar.py`
```python
"""
Escore de APGAR Calculator

Avalia a vitalidade do recém-nascido através de 5 componentes.
"""

from typing import Dict, Any


class ApgarCalculator:
    """Calculadora para Escore de APGAR"""
    
    def calculate(self, heart_rate: int, respiratory_effort: str, 
                 muscle_tone: str, reflexes: str, color: str) -> Dict[str, Any]:
        """
        Calcula o escore APGAR
        
        Args:
            heart_rate: Frequência cardíaca em bpm
            respiratory_effort: "ausente", "irregular", "regular"
            muscle_tone: "flácido", "flexão_leve", "movimento_ativo"
            reflexes: "ausente", "careta", "choro_tosse"
            color: "cianótico", "extremidades_azuis", "rosado"
            
        Returns:
            Dict com resultado e interpretação
        """
        
        # Validações
        self._validate_inputs(heart_rate, respiratory_effort, muscle_tone, reflexes, color)
        
        # Calcular pontuação de cada componente
        hr_score = self._score_heart_rate(heart_rate)
        resp_score = self._score_respiratory(respiratory_effort)
        tone_score = self._score_muscle_tone(muscle_tone)
        reflex_score = self._score_reflexes(reflexes)
        color_score = self._score_color(color)
        
        # Somar total
        total_score = hr_score + resp_score + tone_score + reflex_score + color_score
        
        # Obter interpretação
        interpretation = self._get_interpretation(total_score)
        
        return {
            "result": total_score,
            "unit": "pontos",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, heart_rate, respiratory_effort, muscle_tone, reflexes, color):
        """Valida parâmetros de entrada"""
        
        if not isinstance(heart_rate, int) or heart_rate < 0 or heart_rate > 200:
            raise ValueError("Frequência cardíaca deve ser um inteiro entre 0 e 200")
        
        valid_resp = ["ausente", "irregular", "regular"]
        if respiratory_effort not in valid_resp:
            raise ValueError(f"Esforço respiratório deve ser: {', '.join(valid_resp)}")
        
        # Mais validações...
    
    def _score_heart_rate(self, hr: int) -> int:
        """Pontua frequência cardíaca"""
        if hr == 0:
            return 0
        elif hr < 100:
            return 1
        else:
            return 2
    
    def _score_respiratory(self, effort: str) -> int:
        """Pontua esforço respiratório"""
        mapping = {"ausente": 0, "irregular": 1, "regular": 2}
        return mapping[effort]
    
    def _get_interpretation(self, score: int) -> Dict[str, str]:
        """Interpreta o escore APGAR"""
        
        if score >= 8:
            return {
                "stage": "Normal",
                "description": "Recém-nascido em boas condições",
                "interpretation": "RN vigoroso, sem necessidade de intervenção."
            }
        elif score >= 4:
            return {
                "stage": "Moderado", 
                "description": "Depressão moderada",
                "interpretation": "Necessita estimulação e possível ventilação."
            }
        else:
            return {
                "stage": "Grave",
                "description": "Asfixia grave", 
                "interpretation": "Necessita reanimação imediata."
            }


def calculate_apgar(heart_rate: int, respiratory_effort: str, muscle_tone: str, 
                   reflexes: str, color: str) -> Dict[str, Any]:
    """Função de conveniência para o sistema de carregamento dinâmico"""
    calculator = ApgarCalculator()
    return calculator.calculate(heart_rate, respiratory_effort, muscle_tone, reflexes, color)
```

## 🔄 Protocolo de Implementação Automatizada

### Fluxo Detalhado por Iteração

Para cada ciclo de implementação, seguir rigorosamente:

#### 1. **📋 Consultar CALC_LIST.md**
```
- Ler arquivo @CALC_LIST.md
- Identificar primeira calculadora sem ✅
- Priorizar por relevância clínica e disponibilidade de fórmulas
- Selecionar calculadora para implementação
```

#### 2. **📖 Revisar README.md** 
```
- Ler @README.md para contexto da aplicação
- Verificar estrutura atual de diretórios
- Confirmar padrões de nomenclatura
- Entender arquitetura de endpoints
```

#### 3. **🏗️ Implementação Completa**
```
- Criar JSON em /scores/{score_id}.json
- Implementar calculadora em /calculators/{score_id}.py
- Testar com POST /api/reload
- Verificar funcionamento via API
- Validar todos os cenários de entrada
```

#### 4. **✅ Atualizar CALC_LIST.md**
```
- Adicionar ✅ na linha da calculadora implementada
- Manter formatação original do arquivo
- Confirmar que alteração foi salva
```

#### 5. **🗜️ Compactar Contexto**
```
- Executar comando /compact
- Resumir implementações realizadas
- Preparar contexto para próximo ciclo
```

#### 6. **🔄 Prosseguir Automaticamente**
```
- Retornar ao passo 1 sem interrupção
- Continuar até esgotar lista ou receber instrução de parada
- Manter qualidade e consistência em todas implementações
```

### Diretrizes de Qualidade

- **Validação Rigorosa**: Cada calculadora deve ter validações completas de entrada
- **Testes Funcionais**: Sempre testar reload e endpoints após implementação  
- **Documentação Completa**: Incluir referências bibliográficas e notas clínicas
- **Nomenclatura Consistente**: Seguir padrões snake_case para IDs e PascalCase para classes
- **Interpretação Clínica**: Fornecer interpretações médicas adequadas para cada resultado

### Tratamento de Erros

- **Erro de Implementação**: Corrigir e testar novamente antes de marcar como completo
- **Fórmula Incompleta**: Buscar referências adicionais ou pular para próxima calculadora
- **Conflito de Nomenclatura**: Adaptar nome seguindo convenções estabelecidas

## 🎯 Resumo dos Passos

1. **Criar JSON** em `/scores/{score_id}.json` com metadados completos
2. **Implementar calculadora** em `/calculators/{score_id}.py` com função `calculate_{score_id}`  
3. **Testar** via reload e endpoints da API
4. **Adicionar modelos Pydantic** (opcional) para endpoints específicos
5. **Documentar** referências e fórmulas adequadamente
6. **Marcar como concluído** em CALC_LIST.md
7. **Compactar conversa** e reiniciar ciclo

Seguindo este guia, qualquer agente de programação pode implementar novas calculadoras médicas na nobra_calculator de forma consistente, funcional e totalmente automatizada! 🚀
