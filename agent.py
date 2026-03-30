import getpass
import json
import os
import sys
import urllib.error
import urllib.request
from dataclasses import dataclass, field


SYSTEM_PROMPT = """
You are a conversational autonomous planning assistant.

Rules:
1) Always respond in Korean.
2) Be helpful and concrete.
3) Output strict JSON with keys:
   - assistant_reply: string
   - autonomous_next_steps: array of strings
   - options: array of objects with keys: id (string), title (string), detail (string)
4) options must always contain at least 3 items.
5) Keep options mutually distinct and actionable.
6) If user input is vague, ask one concise clarifying question in assistant_reply while still giving options.
""".strip()


@dataclass
class AgentState:
    history: list[dict] = field(default_factory=list)


class OpenRouterInteractiveAgent:
    def __init__(self, model: str | None = None):
        api_key = os.environ.get("OPENROUTER_API_KEY", "").strip()
        if not api_key:
            api_key = getpass.getpass("OPENROUTER_API_KEY를 입력하세요: ").strip()
        if not api_key:
            raise ValueError("OPENROUTER_API_KEY가 비어 있습니다.")

        self.api_key = api_key
        self.model = model or os.environ.get("OPENROUTER_MODEL", "meta-llama/llama-3.3-8b-instruct:free")
        self.base_url = os.environ.get("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
        self.state = AgentState()

    @staticmethod
    def _extract_json(text: str) -> dict:
        text = text.strip()
        if text.startswith("```"):
            text = text.removeprefix("```json").removeprefix("```").strip()
            if text.endswith("```"):
                text = text[:-3].strip()
        return json.loads(text)

    def _request_openrouter(self, user_text: str) -> dict:
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        messages.extend(self.state.history)
        messages.append({"role": "user", "content": user_text})

        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": 0.3,
            "max_tokens": 1200,
        }

        req = urllib.request.Request(
            url=f"{self.base_url}/chat/completions",
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://local-cli-agent",
                "X-Title": "openrouter-cli-agent",
            },
            method="POST",
        )

        try:
            with urllib.request.urlopen(req, timeout=60) as response:
                raw = response.read().decode("utf-8")
        except urllib.error.HTTPError as exc:
            body = exc.read().decode("utf-8", errors="ignore")
            raise RuntimeError(f"OpenRouter HTTP 오류({exc.code}): {body}") from exc
        except urllib.error.URLError as exc:
            raise RuntimeError(f"OpenRouter 연결 오류: {exc.reason}") from exc

        return json.loads(raw)

    def _call_model(self, user_text: str) -> dict:
        response = self._request_openrouter(user_text)
        choices = response.get("choices", [])
        if not choices:
            raise RuntimeError("OpenRouter 응답에 choices가 없습니다.")

        message = choices[0].get("message", {})
        content = message.get("content", "").strip()
        data = self._extract_json(content)

        options = data.get("options", [])
        if len(options) < 3:
            while len(options) < 3:
                idx = len(options) + 1
                options.append(
                    {
                        "id": str(idx),
                        "title": f"추가 선택지 {idx}",
                        "detail": "모델 응답에서 선택지가 부족해 자동 보강되었습니다.",
                    }
                )
            data["options"] = options

        self.state.history.append({"role": "user", "content": user_text})
        self.state.history.append({"role": "assistant", "content": json.dumps(data, ensure_ascii=False)})
        return data

    @staticmethod
    def _print_turn(data: dict):
        print("\n=== Assistant ===")
        print(data.get("assistant_reply", ""))

        print("\n--- Agent 자율 진행 제안 ---")
        for step in data.get("autonomous_next_steps", []):
            print(f"- {step}")

        print("\n--- 다음 선택지 ---")
        for i, option in enumerate(data.get("options", []), start=1):
            title = option.get("title", f"옵션 {i}")
            detail = option.get("detail", "")
            print(f"{i}. {title} | {detail}")

    def run(self):
        print("OpenRouter 기반 대화형 자율 Agent를 시작합니다. (종료: exit)")
        print(f"사용 모델: {self.model}")
        pending_options: list[dict] = []

        while True:
            user_input = input("\n사용자 입력(또는 옵션 번호): ").strip()
            if user_input.lower() == "exit":
                print("종료합니다.")
                break

            if user_input.isdigit() and pending_options:
                idx = int(user_input) - 1
                if 0 <= idx < len(pending_options):
                    selected = pending_options[idx]
                    user_message = (
                        "다음 옵션을 선택합니다: "
                        f"{selected.get('title', '')}. "
                        f"세부: {selected.get('detail', '')}. "
                        "이 선택을 기준으로 다음 실행 계획을 진행해 주세요."
                    )
                else:
                    user_message = "잘못된 번호를 입력했습니다. 가능한 번호를 다시 안내해 주세요."
            else:
                user_message = user_input

            try:
                data = self._call_model(user_message)
            except Exception as exc:
                print(f"\n[오류] 모델 호출 실패: {exc}")
                continue

            self._print_turn(data)
            pending_options = data.get("options", [])


if __name__ == "__main__":
    try:
        agent = OpenRouterInteractiveAgent()
        agent.run()
    except KeyboardInterrupt:
        print("\n사용자 중단으로 종료합니다.")
        sys.exit(0)
