from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from langchain_huggingface.llms import HuggingFacePipeline
from langchain_core.prompts import PromptTemplate
from services.logger_service import logger

# Path to your local model directory in the root of your project
MODEL_PATH = "C:\Jony\Projects\Ongoing\doc-chat\model\jony-jas--DeepSeek-R1-Distill-Llama-8B-Electrical-engineering"  # change this to the actual path if different

# try:
#     logger.info("Loading tokenizer and model from local directory...")
#     tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
#     # model = AutoModelForCausalLM.from_pretrained(MODEL_PATH)
#     model = ''

#     # Create a Hugging Face pipeline for text generation
#     pipe = pipeline(
#         "text-generation",
#         model=model,
#         tokenizer=tokenizer,
#         max_length=256,
#         do_sample=True,
#         temperature=0.7,
#     )
#     llm = HuggingFacePipeline(pipeline=pipe)
#     logger.info("Local model loaded successfully.")
# except Exception as e:
#     logger.error(f"Error loading local model: {e}")
#     raise

# Define your prompt template based on the training prompt style
prompt_template = """Below is an instruction that describes a task, paired with an input that provides further context.
Write a response that appropriately completes the request. If you don't know the answer to a question, please don't share false information. Just say "Not Found".

### Instruction:
You are an electrical engineer and you will answer questions related to electrical engineering.

### Question:
{question}

### Response:"""

# Create a PromptTemplate object for LangChain
prompt = PromptTemplate(template=prompt_template, input_variables=["question"])

logger.info("Initialized the Local LLM model.")

def answer_question(question: str) -> str:
    """
    Uses the local model via LangChain to generate an answer for the given question.
    """
    try:
        # Use the `prompt | llm` syntax to generate the answer
        chain = prompt | "llm"
        result = chain.invoke({"question": question})
        return result.strip()
    except Exception as e:
        logger.error(f"Error generating answer: {e}")
        return "Error generating answer"