from openai import OpenAI

client = OpenAI(
  api_key="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"
)

response = client.responses.create(
  model="gpt-5-nano",
  input="write a short summary of what you think the 2026 F1 season will pan out",
  store=True,
)

print(response.output_text);
