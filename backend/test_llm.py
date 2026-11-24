from llm import generate_response

intent = "book_appointment"

entities = {
    "date": "2026-06-23"
}

response = generate_response(
    intent,
    entities
)

print(response)