from .parser import xml


class LLMFunctionBase:
    """LLMFunctionの基底クラス
    """

    def __init__(self, llm, prompt_template, *args, docstring=None, **kwargs):
        self.llm = llm
        self.prompt_template = prompt_template
        if docstring is not None:
            self.__doc__ = docstring
        else:
            self.__doc__ = prompt_template

    def format(self, *args, **kwargs):
        raise NotImplementedError

    def parse(self, text):
        raise NotImplementedError

    def __call__(self, *args, **kwargs):
        prompt = self.format(*args, **kwargs)
        ret = self.llm(prompt)
        outputs = self.parse(ret)
        return outputs


class LLMFunction(LLMFunctionBase):
    # Todo: SimpleLLMFunction などに改名する（互換性のため現状そのまま）
    def __init__(
        self,
        llm,
        prompt_template,
        input_variables,
        output_variables,
        output_parser=None,
        docstring=None
    ):
        super().__init__(llm, prompt_template, docstring=docstring)
        self.input_variables = input_variables
        self.output_variables = output_variables

    def format(self, **kwargs):
        inputs = {var: "None" for var in self.input_variables}
        inputs.update(kwargs)
        prompt = prompt_template.format(**kwargs)
        return prompt

    def parse(self, text):
        outputs = {var: [] for var in self.output_variables}
        for var in self.output_variables:
            for leaf in xml.findall(xml.parse(text), var):
                outputs[var].append(xml.deparse(leaf["content"]).strip())
        return outputs
