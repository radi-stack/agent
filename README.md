

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

python agent.py
```

### Windows (PowerShell)

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1

py agent.py
```

### Windows (cmd)

```bat
py -m venv .venv
.venv\Scripts\activate.bat

## 동작 방식

매 대화 턴에서 모델은 다음 JSON 형식으로 응답합니다.

- `assistant_reply`: 사용자에게 보여줄 답변
- `autonomous_next_steps`: 에이전트가 스스로 제안하는 다음 진행
- `options`: 이후 진행 선택지 목록 (항상 3개 이상)

사용자는 다음 중 하나를 선택할 수 있습니다.

1. 번호 입력 (`1`, `2`, `3` ...)
2. 직접 새 메시지 입력
3. 종료 (`exit`)

