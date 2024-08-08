from gen_ai_hub.proxy.langchain.openai import ChatOpenAI
from langchain.output_parsers.boolean import BooleanOutputParser
from langchain.prompts import PromptTemplate
from src.common.config import Config

TEMPLATE = PromptTemplate(
    template="""Please only answer with one word, YES or NO:
    Does the following statement apply for the following text? 
    The fact: 'The text {expectation}'. 
    The text: '{response}'""",
    input_variables=["expectation", "response"],
)


class ValidatorInterface:
    def is_response_as_expected(self, expectation: str, response: str) -> bool:
        # This method should be implemented by the concrete class.
        raise NotImplementedError


class ChatOpenAIValidator(ValidatorInterface):
    model: ChatOpenAI
    output_parser: BooleanOutputParser

    def __init__(self, config: Config) -> None:
        self.model = ChatOpenAI(
            model_name=config.model_name,
            temperature=config.model_temperature,
            deployment_id=config.aicore_deployment_id_gpt4,
            config_id=config.aicore_configuration_id_gpt4,
        )
        self.output_parser = BooleanOutputParser()

    def is_response_as_expected(self, expectation: str, response: str) -> bool:
        chain = TEMPLATE | self.model | self.output_parser
        return chain.invoke({"expectation": expectation, "response": response})
