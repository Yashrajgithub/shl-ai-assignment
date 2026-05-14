from app.agent import generate_response


messages = [
    {
        "role": "user",
        "content": (
            "Hiring a Java backend developer "
            "with stakeholder communication skills"
        )
    }
]


response = generate_response(messages)

print(response)