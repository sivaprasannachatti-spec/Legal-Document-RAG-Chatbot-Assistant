import sys

from src.exception import CustomException
from src.logger import logging
from langchain_core.prompts import load_prompt
from langchain_groq import ChatGroq
from langchain_classic.output_parsers import StructuredOutputParser, ResponseSchema

class DataPreparation:
    def prepareData(self, docs):
        try:
            prompt = load_prompt(r'C:\Projects\artifacts\evaluation_prompt.json')
            model = ChatGroq(model='llama-3.1-8b-instant', temperature=0.3)
            schema = [
                ResponseSchema(name='qa_pairs', description="A list of exactly 2 question-answer objects. Each object must contain 'question' and 'answer'."),
            ]
            parser = StructuredOutputParser.from_response_schemas(schema) 
            format_instructions = parser.get_format_instructions()
            prompt = prompt.partial(format_instructions=format_instructions)
            evaluation_dataset = []
            for i, doc in enumerate(docs):
                chunk_text = doc.page_content
                chain = prompt | model | parser

                # Retry up to 3 times if LLM returns invalid JSON
                max_retries = 3
                for attempt in range(max_retries):
                    try:
                        result = chain.invoke({"chunk": chunk_text})
                        for qa in result["qa_pairs"]:
                            evaluation_dataset.append(qa)
                        logging.info(f"Chunk {i+1}/{len(docs)} processed successfully")
                        break
                    except Exception as parse_err:
                        if attempt < max_retries - 1:
                            logging.warning(f"Chunk {i+1} attempt {attempt+1} failed (bad JSON), retrying...")
                            continue
                        else:
                            logging.warning(f"Chunk {i+1} skipped after {max_retries} failed attempts: {parse_err}")

            logging.info(f"Evaluation dataset prepared with {len(evaluation_dataset)} QA pairs")
            return evaluation_dataset
        except Exception as e:
            raise CustomException(e, sys)