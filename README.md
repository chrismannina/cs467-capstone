# Medical Document Q&A Application

This application enables users to ask questions related to specific documents, particularly medical guidelines. It uses vector embeddings and similarity search to retrieve relevant sections of the documents and then utilizes a chat model to generate detailed answers.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)

## Features

- Upload and process documents to be used as a knowledge base.
- Ask questions related to the uploaded documents.
- Receive precise answers and relevant document references.
- Interactive Streamlit interface for ease of use.
- CLI support for direct command-line interaction.

## Installation

1. Clone the repository:

   ```
   git clone https://github.com/chrismannina/cs467-capstone.git
   ```

2. Navigate to the project directory and install the required packages:
   ```
   cd cs467-capstone
   pip install -r requirements.txt
   ```

## Usage

### Streamlit Interface

1. To launch the Streamlit app, run:

   ```
   streamlit run app.py
   ```

2. Use the Streamlit interface to upload documents and ask questions.
