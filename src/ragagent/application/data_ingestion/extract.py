from typing import Generator
import re
import ast

import pandas as pd

from langchain_core.documents import Document
from tqdm import tqdm


# function to remove '$' and ',' from the string
def _clean_value(val):
    if not isinstance(val, str):
        return val
    val = val.replace('$', '').replace(',', '')
    if re.match(r'^\(.*\)$', val):
        val = '-' + val.strip('()')
    return val

# clearn data by removing '$' and ',' from the string
def clean_currency_nested_list(row):
    """
    Takes a nested list (e.g., table) and cleans currency formatting.
    Returns a cleaned list of lists.
    """
    cleaned = []
    for sublist in row:
        if isinstance(sublist, list):
            cleaned_row = [_clean_value(item) for item in sublist]
            cleaned.append(cleaned_row)
        else:
            raise ValueError("Expected nested list structure (list of lists).")
    return cleaned

# convert table into markdown
def convert_table_to_markdown_and_chunks(table):
    # Extract header and rows
    header = table[0]
    data_rows = table[1:]

    # Convert to markdown table
    markdown = "| " + " | ".join(header) + " |\n"
    markdown += "| " + " | ".join(["---"] * len(header)) + " |\n"
    for row in data_rows:
        markdown += "| " + " | ".join(row) + " |\n"

    return markdown

def extract_data_from_dataframe(
    url: str
) -> list[Document]:
    """Extract documents from dataframe.

    Args:
        urls: List of URLs to extract content from.

    Returns:
        str: path of documents.
    """
    
    if len(url) == 0:
        return []
    
    clearn_data_column = "clean_data"
    metadata_columns = ['filename']
    column_to_ingest = "new_table"

    df = pd.read_csv(url)
    
    # clearn data
    df[column_to_ingest] = df[column_to_ingest].map(lambda x: ast.literal_eval(x))
    df[column_to_ingest] = df[column_to_ingest].apply(clean_currency_nested_list)
    df[clearn_data_column] = df[column_to_ingest].apply(convert_table_to_markdown_and_chunks)

    documents = []
    for _, row in df.iterrows():
        page_content = str(row[clearn_data_column])

        metadata = {col: row[col] for col in metadata_columns}

        document = Document(page_content=page_content, metadata=metadata)
        documents.append(document)
    return documents


if __name__ == "__main__":
    url = 'dataset\trainingdata.csv'
    docs = extract_data_from_dataframe(url)
    print(docs)