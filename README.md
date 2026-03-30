# Claude 기반 대화형 + 자율 진행 Agent (CLI)

이 프로젝트는 **Claude API(Anthropic)** 를 사용해 아래 요구사항을 만족하는 최소 동작 예시입니다.

- 기본적으로 대화형 인터페이스
- 에이전트가 스스로 다음 행동을 제안/진행할 수 있는 구조
- 매 턴마다 **3개 이상 선택지**를 보여주고 사용자가 선택
- **Windows / macOS / Linux**에서 실행 가능

## 구성 파일

- `agent.py`: CLI 에이전트 실행 파일
- `requirements.txt`: 의존성

## 빠른 시작

### macOS / Linux

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export ANTHROPIC_API_KEY="your_key"
python agent.py
```

### Windows (PowerShell)

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1

$env:ANTHROPIC_API_KEY="your_key"
py agent.py
```

### Windows (cmd)

```bat
py -m venv .venv
.venv\Scripts\activate.bat

set ANTHROPIC_API_KEY=your_key
py agent.py
```

> `ANTHROPIC_API_KEY`를 미리 설정하지 않아도 실행 시 콘솔에서 직접 입력할 수 있습니다.

## 동작 방식

매 대화 턴에서 모델은 다음 JSON 형식으로 응답합니다.

- `assistant_reply`: 사용자에게 보여줄 답변
- `autonomous_next_steps`: 에이전트가 스스로 제안하는 다음 진행
- `options`: 이후 진행 선택지 목록 (항상 3개 이상)

사용자는 다음 중 하나를 선택할 수 있습니다.

1. 번호 입력 (`1`, `2`, `3` ...)
2. 직접 새 메시지 입력
3. 종료 (`exit`)

## 확장 아이디어

- 옵션 선택 결과를 상태 머신으로 저장
- 툴 호출(검색, 파일, DB 등) 연결
- 옵션마다 비용/위험도/예상시간 표시
- 웹 UI(Streamlit/FastAPI)로 확장
