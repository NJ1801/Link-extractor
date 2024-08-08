# Link Extractor

## Overview

The THH Link Extractor is a Streamlit application designed to generate Boolean search queries based on user input, perform Google searches using these queries, and extract and store relevant links into a MySQL database and a CSV file. The application utilizes the Gemini Generative AI model for query generation and SerpAPI for search results.

## Features

- **Boolean Search Query Generation**: Generates Boolean search queries based on user input using the Gemini Generative AI model.
- **Google Search**: Performs searches on Google and extracts relevant results using the SerpAPI.
- **Link Extraction**: Filters and stores LinkedIn profile links from search results.
- **Database Storage**: Saves extracted links to a local and remote MySQL database.
- **CSV Export**: Exports search results to a downloadable CSV file.

## Setup Instructions

### Prerequisites

Ensure you have the following installed:

- Python 3.7+
- pip
- MySQL server

### Installation

1. **Clone the repository**:

    ```bash
    git clone https://github.com/your-username/thh-link-extractor.git
    cd thh-link-extractor
    ```

2. **Create a virtual environment** (optional but recommended):

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. **Install the required packages**:

    ```bash
    pip install -r requirements.txt
    ```

    Ensure `requirements.txt` contains the following dependencies:

    ```txt
    streamlit
    google-generativeai
    serpapi
    mysql-connector-python
    pandas
    ```
    
4. **Update the configuration**:

    - Replace `"Gemini-API-Key"` with your actual Gemini API key in the `generate_search_query` function.
    - Replace `"Serp-API-Key"` with your actual SerpAPI key in the `search_google` function.
    - Update MySQL connection details in the `save_to_database` and `connect_to_mysql` functions with your database credentials.

5. **Run the Streamlit app**:

    ```bash
    streamlit run app.py
    ```

## Usage

1. **Run the application** using the command provided in the setup instructions.

2. **Enter your prompt** in the text input field to generate a Boolean search query.

3. **Enter a file name** in the text input field to specify the name of the CSV file where results will be saved.

4. **Click "Search"** to generate the query, perform the search, and extract links.

5. **Download the CSV file** containing the extracted links by clicking the download link provided after the search results.

## File Structure

- `app.py`: Main application file containing the Streamlit code.
- `README.md`: This README file.
- `requirements.txt`: File listing the Python package dependencies.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Contributing

Feel free to open issues or submit pull requests for improvements or bug fixes.

## Contact

For any questions or inquiries, please contact [njnagaraj007@gmail.com].
