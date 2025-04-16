from huggingface_hub import InferenceClient
import json

class AIModel:
    def __init__(self, api_key, model_name):
        self.client = InferenceClient(api_key=api_key)
        self.model_name = model_name

    def recommend_solution(self, log_entry, issue_type):
        if not log_entry:
            return "No log entry provided."

        if issue_type == "false_positive":
            prompt = f"""
            Analyze the following defense log entry:
            {json.dumps(log_entry, indent=2)}

            Classification: {issue_type}

            Provide a concise recommendation to adjust my detection rules to avoid this issue.
            """
        elif issue_type == "missed_attack":  # small typo fix from your code
            prompt = f"""
            Analyze the following attack log entry:
            {json.dumps(log_entry, indent=2)}

            Classification: {issue_type}

            This attack passed through my detection rules undetected.
            Provide a concise recommendation to improve my detection and avoid missing such attacks.
            """
        else:
            return f"Unknown issue type: {issue_type}"

        try:
            response = self.client.text_generation(
                model=self.model_name,
                prompt=prompt,
                max_new_tokens=200
            )
            return response.strip()
        except Exception as e:
            return f"AI generation error: {e}"
