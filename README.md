# ChatGPT Codex 기반 대화형 + 자율 진행 Agent (CLI)

이 프로젝트는 **OpenAI API (ChatGPT Codex 모델)** 를 사용해 아래 요구사항을 만족하는 최소 동작 예시입니다.

- 기본적으로 대화형 인터페이스
- 에이전트가 스스로 다음 행동을 제안/진행할 수 있는 구조
- 매 턴마다 **3개 이상 선택지**를 보여주고 사용자가 선택
- **Windows / macOS / Linux**에서 실행 가능
- 기본 모델을 **Codex 계열 모델**로 설정
- 필요 시 OpenAI Responses API의 **MCP tool** 연결 가능

## 구성 파일

- `agent.py`: CLI 에이전트 실행 파일
- `requirements.txt`: 의존성

## 빠른 시작

> 기본값: `OPENAI_MODEL=gpt-5.3-codex`

### macOS / Linux

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
export OPENAI_API_KEY="your_key"
python agent.py
```

### Windows (PowerShell)

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
py -m pip install -r requirements.txt
$env:OPENAI_API_KEY="your_key"
py agent.py
```

### Windows (cmd)

```bat
py -m venv .venv
.venv\Scripts\activate.bat
py -m pip install -r requirements.txt
set OPENAI_API_KEY=your_key
py agent.py
```

> `OPENAI_API_KEY`를 미리 설정하지 않아도 실행 시 콘솔에서 직접 입력할 수 있습니다.
> `OPENAI_MCP_SERVER_URL` 또는 `OPENAI_MCP_CONNECTOR_ID`를 설정하면 MCP 도구를 함께 사용합니다.

## 환경 변수

- `OPENAI_API_KEY` (필수): OpenAI API 키
- `OPENAI_MODEL` (선택): 사용할 모델명 (기본값 `gpt-5.3-codex`)
- `OPENAI_BASE_URL` (선택): 기본값 `https://api.openai.com/v1`
- `OPENAI_MCP_SERVER_URL` (선택): 원격 MCP 서버 URL
- `OPENAI_MCP_CONNECTOR_ID` (선택): OpenAI connector 방식 MCP 식별자
- `OPENAI_MCP_SERVER_LABEL` (선택): MCP 도구 이름(기본값 `remote-mcp`)
- `OPENAI_MCP_REQUIRE_APPROVAL` (선택): MCP 승인 정책(기본값 `never`)

예시 (PowerShell):

```powershell
$env:OPENAI_API_KEY="your_key"
$env:OPENAI_MCP_SERVER_URL="https://your-mcp-server.example.com/mcp"
$env:OPENAI_MCP_SERVER_LABEL="my-mcp"
$env:OPENAI_MCP_REQUIRE_APPROVAL="never"
py agent.py
```

## 트러블슈팅

### API 호출 실패 / 인증 오류

1. `OPENAI_API_KEY`가 유효한지 확인
2. `OPENAI_MODEL`이 현재 사용 가능한 모델인지 확인
3. 조직/프로젝트 제한으로 모델 접근이 막혔는지 확인
4. 최신 코드에서 `/responses` 스펙(`max_output_tokens`)을 사용하므로, 예전 코드라면 `git pull` 후 재실행
5. ChatGPT Pro 구독과 OpenAI API 과금은 별개이므로, 이 스크립트 실행에는 유효한 `OPENAI_API_KEY`가 필요

### 모델 응답 파싱 오류(JSONDecodeError)

- 이 에이전트는 모델 응답이 JSON 형식(`assistant_reply`, `autonomous_next_steps`, `options`)을 따르기를 기대합니다.
- 모델을 바꿨을 때 파싱 오류가 나면, `OPENAI_MODEL`을 기본값(`gpt-5.3-codex`)으로 먼저 되돌려 확인하세요.

## 동작 방식

매 대화 턴에서 모델은 다음 JSON 형식으로 응답합니다.

- `assistant_reply`: 사용자에게 보여줄 답변
- `autonomous_next_steps`: 에이전트가 스스로 제안하는 다음 진행
- `options`: 이후 진행 선택지 목록 (항상 3개 이상)

사용자는 다음 중 하나를 선택할 수 있습니다.

1. 번호 입력 (`1`, `2`, `3` ...)
2. 직접 새 메시지 입력
3. 종료 (`exit`)
