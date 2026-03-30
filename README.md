# OpenRouter 기반 대화형 + 자율 진행 Agent (CLI)

이 프로젝트는 **OpenRouter API**를 사용해 아래 요구사항을 만족하는 최소 동작 예시입니다.

- 기본적으로 대화형 인터페이스
- 에이전트가 스스로 다음 행동을 제안/진행할 수 있는 구조
- 매 턴마다 **3개 이상 선택지**를 보여주고 사용자가 선택
- **Windows / macOS / Linux**에서 실행 가능
- 기본 모델을 **무료(`:free`) 모델**로 설정

## 구성 파일

- `agent.py`: CLI 에이전트 실행 파일
- `requirements.txt`: 의존성

## 빠른 시작

> 기본값: `OPENROUTER_MODEL=nvidia/nemotron-3-super-120b-a12b:free`

### macOS / Linux

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
export OPENROUTER_API_KEY="your_key"
python agent.py
```

### Windows (PowerShell)

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
py -m pip install -r requirements.txt
$env:OPENROUTER_API_KEY="your_key"
py agent.py
```

### Windows (cmd)

```bat
py -m venv .venv
.venv\Scripts\activate.bat
py -m pip install -r requirements.txt
set OPENROUTER_API_KEY=your_key
py agent.py
```

> `OPENROUTER_API_KEY`를 미리 설정하지 않아도 실행 시 콘솔에서 직접 입력할 수 있습니다.

## 환경 변수

- `OPENROUTER_API_KEY` (필수): OpenRouter API 키
- `OPENROUTER_MODEL` (선택): 사용할 모델명 (`:free` 모델 권장)
- `OPENROUTER_BASE_URL` (선택): 기본값 `https://openrouter.ai/api/v1`

## 트러블슈팅

### API 호출 실패 / 인증 오류

1. `OPENROUTER_API_KEY`가 유효한지 확인
2. `OPENROUTER_MODEL`이 현재 사용 가능한 모델인지 확인
3. 무료 모델은 수시 변경될 수 있으니 `:free` 모델명으로 바꿔 재시도

## 동작 방식

매 대화 턴에서 모델은 다음 JSON 형식으로 응답합니다.

- `assistant_reply`: 사용자에게 보여줄 답변
- `autonomous_next_steps`: 에이전트가 스스로 제안하는 다음 진행
- `options`: 이후 진행 선택지 목록 (항상 3개 이상)

사용자는 다음 중 하나를 선택할 수 있습니다.

1. 번호 입력 (`1`, `2`, `3` ...)
2. 직접 새 메시지 입력
3. 종료 (`exit`)
