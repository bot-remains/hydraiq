import bs4
from langchain_community.document_loaders import WebBaseLoader

loader = WebBaseLoader("https://dev.to/ranjancse/web-scraping-with-langchain-and-html2text-5edl")
docs = []
for doc in loader.lazy_load():
    docs.append(doc)
    return docs