import os
import json
import openai
from dotenv import load_dotenv

def load_config(path="config.json"):
    with open(path, "r") as f:
        return json.load(f)

def load_prompt(prompt_path):
    with open(prompt_path, "r") as f:
        return f.read()

def call_openai(prompt, config):
    openai.api_key = config["openai_api_key"]
    model = config.get("openai_model", "gpt-4")

    response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a senior software project planner."},
            {"role": "user", "content": prompt}
        ],
        temperature=config.get("temperature", 0.5),
        max_tokens=config.get("max_tokens", 2048)
    )
    return response.choices[0].message.content.strip()

def save_output(task_list_str, output_path):
    try:
        task_list = json.loads(task_list_str)
    except json.JSONDecodeError:
        print("❌ Error: Model output was not valid JSON. Check your prompt or model settings.")
        return False

    with open(output_path, "w") as f:
        json.dump(task_list, f, indent=2)
    return True

def main():
    load_dotenv()
    config = load_config("config_openai.json")
    prompt = load_prompt(config["prompt_file"])
    print("⏳ Generating tasks using OpenAI...")
    output = call_openai(prompt, config)
    success = save_output(output, config["task_output_file"])

    if success:
        print(f"✅ Tasks saved to {config['task_output_file']}")
    else:
        print("⚠️ Task generation failed.")

if __name__ == "__main__":
    main()
