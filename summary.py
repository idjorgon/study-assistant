# Summarize text using OpenAI
def summarize_text(text, client, deployment_name):
    """Summarize the input text."""
    
    messages = [
        {"role": "system", "content": "You are an assistant that summarizes input text."},
        {"role": "user", "content": f"Summarize the following text into concise bullet points:\n\n{text}"}
    ]
    
    response = client.chat.completions.create(
        model=deployment_name,
        messages=messages,
        max_tokens=150,
        temperature=0.5
    )
    return response.choices[0].message.content
