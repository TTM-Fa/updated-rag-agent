# UDST Policy Query System

This Streamlit application allows users to query various policies from the University of Doha for Science and Technology (UDST). The app fetches relevant policies, processes user queries, and provides answers based on the content of the policies.

## Features

- **Real-time Typing Effect**: Displays responses with a typing effect.
- **Policy Scraping**: Fetches and processes policy documents from provided URLs.
- **AI-Powered Query System**: Uses the Mistral AI model to determine relevant policies and generate answers.

## Requirements

To run this application, you need the following Python packages:

- `streamlit`
- `requests`
- `beautifulsoup4`
- `numpy`
- `faiss-cpu`
- `mistralai`

You can install these packages using the `requirements.txt` file:

```sh
pip install -r streamlit/requirements.txt
```

## Running the Application

To run the application, use the following command:

```sh
streamlit run streamlit/app.py
```

## File Structure

```
streamlit-policy-query/
├── streamlit/
│   ├── app.py
│   ├── requirements.txt
├── README.md
```

## Configuration

The application requires an API key for the Mistral AI model, which should be stored in the Streamlit secrets file (`.streamlit/secrets.toml`):

```toml
[MISTRAL_API_KEY]
MISTRAL_API_KEY = "your_api_key_here"
```

## Usage

1. **Enter a Query**: Type your question into the input box.
2. **Processing**: The app will process your query and fetch relevant policies.
3. **View Results**: The app will display the consolidated answer and provide links to the relevant policies.