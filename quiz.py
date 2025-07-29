# Generate quizzes using OpenAI
def generate_quiz(text, client, deployment_name):
    """Generate multiple-choice questions from input text."""

    messages = [
        {
            "role": "system",
            "content": (
                "You are an assistant that generates multiple-choice "
                "questions from input text."
            ),
        },
        {
            "role": "user",
            "content": (
                "Generate multiple-choice questions from the input text:\n\n"
                f"{text}"
            ),
        }
    ]

    response = client.chat.completions.create(
        model=deployment_name,
        messages=messages,
        max_tokens=300,
        temperature=0.7
    )

    return response.choices[0].message.content
