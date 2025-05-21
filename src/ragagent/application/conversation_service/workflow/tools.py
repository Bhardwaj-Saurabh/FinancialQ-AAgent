
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent

from ragagent.application.rag.helper.utils import GradeDocuments
from ragagent.application.rag.retrievers import get_retriever
from ragagent.application.rag.helper.utils import deduplicate_documents_by_content
from ragagent.domain.prompts import DOCUMENT_GRADER_PROMPT

from ragagent.config import settings

from ragagent.application.conversation_service.workflow.chat_model import get_chat_model
from langchain.retrievers.multi_query import MultiQueryRetriever
from langgraph.prebuilt import create_react_agent
from langchain_experimental.utilities import PythonREPL
from langchain_core.tools import tool
from langchain_core.prompts import ChatPromptTemplate
from ragagent.config import settings

from typing import TypedDict, Annotated, List

llm = get_chat_model()
repl = PythonREPL()

retriever = get_retriever(
    embedding_model_id=settings.RAG_TEXT_EMBEDDING_MODEL_ID,
    k=settings.RAG_TOP_K)

retriever = MultiQueryRetriever.from_llm(
    retriever=retriever, llm=llm
)

@tool
def python_repl_tool(
    code: Annotated[str, "The python code to execute code, provide output."],
    ):
    """Use this to execute python code and do math. If you want to see the output of a value,
    you should print it out with `print(...)`. This is visible to the user."""
    try:
        result = repl.run(code)
    except BaseException as e:
        return f"Failed to execute. Error: {repr(e)}"
    result_str = f"Successfully executed:\n```python\n{code}\n```\nCODE OUTPUT:\n {result}"
    return result_str

# Create Coder Sub-Agent
code_agent = create_react_agent(llm, tools=[python_repl_tool],
                                state_modifier="""You are an expert python coder who can write and run python code.
                                                Only extract the most relevant data related to the question before running code.
                                                Once your task is done report final output only.""")

# create tool function for coder sub-agent
@tool
def write_and_run_python_code(query: str) -> str:
    """A function which takes a query and perform following actions:
    - Write python code to solve the query
    - Run the python code and provide output
    """
    result = code_agent.invoke({'messages': query})
    return result['messages'][-1].content

# create tool function for retriever
@tool
def retrieve_documents(question: str) -> list:
    """
    Retrieve finance related documents from vector database.
    Search and return information about the financial queries request by user.

    Args:
        question (str): The query to retrieve data from vector database

    Returns:
        list : documents - that contains retrieved context documents
    """
    # Use retriever to get documents
    documents = retriever.invoke(question)
    
    # REMOVE Deduplicate
    unique_documents = deduplicate_documents_by_content(documents)
    
    docs = []

    for doc in unique_documents:
        docs.append(doc.page_content)
        
    docs = "\n\n\n".join(docs)
    
    # model = get_chat_model()
    # model = model.with_structured_output(GradeDocuments)
    # system_message = DOCUMENT_GRADER_PROMPT

    # grade_prompt = ChatPromptTemplate.from_messages(
    #     [
    #         ("system", system_message.prompt),
    #         ("human", """Retrieved document:
    #                  {document}

    #                  User question:
    #                  {question}
    #               """),
    #     ],
    #     template_format="jinja2",
    # )
    
    # # Build grader chain
    # doc_grader = (grade_prompt
    #                   |
    #                 model)

    # # Score each doc
    # filtered_docs = []
    # total_irrelevant = 0
    # if unique_documents:
    #     for d in unique_documents:
    #         score = doc_grader.invoke(
    #             {"question": question, "document": d.page_content}
    #         )
    #         grade = score.binary_score
    #         if grade == "yes":
    #             print("---GRADE: DOCUMENT RELEVANT---")
    #             filtered_docs.append(d.page_content)
    #         else:
    #             print("---GRADE: DOCUMENT NOT RELEVANT---")
    #             total_irrelevant += 1

    return docs

tools = [retrieve_documents, write_and_run_python_code]