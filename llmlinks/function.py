from .parser import xml
from .llm.openai_model import OpenAILLM
from .llm.google_model import GoogleLLM
from .llm.anthropic_model import AnthoropicLLM


def output_parser_xml(text, output_variables):
    output = {var: [] for var in output_variables}
    tree = xml.parse(text)
    for var in output_variables:
        for leaf in xml.findall(xml.parse(text), var):
            output[var].append(xml.deparse([leaf]).strip())
    return output


class LLMFunction:

    def __init__(
            self,
            llm_name,
            prompt_template,
            input_variables,
            output_variables,
            output_parser=output_parser_xml
            ):
        # OpenAI
        if llm_name == 'gpt-4o-2024-08-06':
            self.llm = OpenAILLM(model = llm_name)
        elif llm_name == 'gpt-4o-2024-05-13':
            self.llm = OpenAILLM(model = llm_name)
        elif llm_name == 'gpt-4o-mini-2024-07-18':
            self.llm = OpenAILLM(model = llm_name)
        elif llm_name == 'gpt-4-turbo-2024-04-09':
            self.llm = OpenAILLM(model = llm_name)
        elif llm_name == 'gpt-4-0125-preview':
            self.llm = OpenAILLM(model = llm_name)
        # Google
        elif llm_name == 'gemini-1.0-pro':
            self.llm = GoogleLLM(model = llm_name)
        elif llm_name == 'gemini-1.5-pro':
            self.llm = GoogleLLM(model = llm_name)
        elif llm_name == 'gemini-1.5-flash':
            self.llm = GoogleLLM(model = llm_name)
        # Anthropic
        elif llm_name == 'claude-3-5-sonnet-20240620':
            self.llm = AnthoropicLLM(model = llm_name)
        elif llm_name == 'claude-3-opus-20240229':
            self.llm = AnthoropicLLM(model = llm_name)
        
        else:
            raise ValueError(f'Unknown LLM: {llm_name}')
        self.prompt_template = prompt_template
        self.input_variables = input_variables
        self.output_variables = output_variables
        self.output_parser = output_parser

    def __call__(self, **kwargs):
        inputs = {var: 'None' for var in self.input_variables}
        inputs.update(kwargs)

        prompt = self.prompt_template.format(**kwargs)
        ret = self.llm(prompt)
        outputs = self.output_parser(ret, self.output_variables)
        return outputs
