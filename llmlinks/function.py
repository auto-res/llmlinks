from .parser import xml


def output_parser_xml(text, output_variables):
    output = {var: [] for var in output_variables}
    # tree = xml.parse(text)
    for var in output_variables:
        for leaf in xml.findall(xml.parse(text), var):
            output[var].append(xml.deparse(leaf["content"]).strip())
    return output


class LLMFunction:
    def __init__(
        self,
        llm,
        prompt_template,
        input_variables,
        output_variables,
        output_parser=output_parser_xml,
    ):
        self.llm = llm
        self.prompt_template = prompt_template
        self.input_variables = input_variables
        self.output_variables = output_variables
        self.output_parser = output_parser

    def __call__(self, **kwargs):
        inputs = {var: "None" for var in self.input_variables}
        inputs.update(kwargs)
        prompt = self.prompt_template.format(**kwargs)
        ret = self.llm(prompt)
        outputs = self.output_parser(ret, self.output_variables)
        return outputs
