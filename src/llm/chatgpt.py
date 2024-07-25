import openai


class ChatGPT:

    def __init__(self, **kwargs):
        self.kwargs = kwargs
        if 'model' not in kwargs:
            self.kwargs['model'] = 'gpt-4-turbo'
        self.client = openai.OpenAI()

    def __call__(self, input_text, as_system=True):
        messages = [
            {
                'role': 'system' if as_system else 'user',
                'content': input_text
            }
        ]
        response = self.client.chat.completions.create(
            messages=messages,
            **self.kwargs)
        output_text = response.choices[0].message.content
        return output_text     
