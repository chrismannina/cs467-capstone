"""Utility functions"""
from collections import defaultdict
from urllib.parse import urlparse
import os


def format_context(docs):
    formatted_context = ""
    for doc in docs:
        source = doc.metadata.get("source", "Unknown source")
        page = doc.metadata.get("page", "Unknown page")
        content = doc.page_content
        formatted_context += f"Source: {source}\nPage: {page}\nContent: {content}\n\n"
    return formatted_context


def format_metadata(docs):
    # Using defaultdict to automatically handle new sources
    source_pages = defaultdict(list)

    for doc in docs:
        # Get the filename only, not the full path
        full_path = doc.metadata.get("source", "Unknown source")
        if full_path.startswith(("http://", "https://")):
            filename = urlparse(full_path).path.rsplit("/", 1)[-1]
        else:
            filename = os.path.basename(full_path)

        # Attempt to parse and increment page number
        page_str = doc.metadata.get("page", "Unknown page")
        if page_str.isdigit():
            page = int(page_str) + 1
            # Appending page to respective source
            source_pages[filename].append(page)

        # page = doc.metadata.get('page', 'Unknown page')
        # page = int(page) + 1

        # Appending page to respective source
        # source_pages[filename].append(page)

    formatted_metadata = ""
    for source, pages in source_pages.items():
        # Sorting pages for display
        pages = sorted(pages)

        # Grouping continuous pages
        page_groups = []
        group_start = group_end = pages[0]

        for page in pages[1:]:
            if page - group_end > 1:
                page_groups.append((group_start, group_end))
                group_start = page
            group_end = page
        page_groups.append((group_start, group_end))

        page_strs = []
        for start, end in page_groups:
            if start == end:
                page_strs.append(str(start))
            else:
                page_strs.append(f"{start}-{end}")

        formatted_metadata += f"- {source} (pages: {', '.join(page_strs)})"

    return formatted_metadata


def format_retrieved_docs(docs):
    formatted_output = ""

    for idx, doc in enumerate(docs):
        formatted_output += f"Retrieved chunk {idx + 1}:\n"
        formatted_output += "-------------------\n"
        formatted_output += f"Source: {doc.metadata['source']}\n\n"
        formatted_output += "Content:\n"
        formatted_output += "-------------------\n"
        formatted_output += f"{doc.page_content}\n\n"

    return formatted_output
