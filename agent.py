import getpass


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



    def _extract_json(text: str) -> dict:
        text = text.strip()
        if text.startswith("```"):
            text = text.removeprefix("```json").removeprefix("```").strip()
            if text.endswith("```"):
                text = text[:-3].strip()
        return json.loads(text)



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


            self._print_turn(data)
            pending_options = data.get("options", [])


if __name__ == "__main__":

