# 📚 Semantic Book Recommender

A semantic book recommendation system that helps users discover books based on a short text description, category, and emotional tone. This interactive Gradio app leverages Google’s Generative AI Embeddings and vector similarity search via LangChain & ChromaDB to return highly relevant book suggestions.

---

## 🔍 Features

- 🔎 **Semantic Search**: Matches user queries with book descriptions using AI-powered embeddings.
- 📂 **Category & Emotion Filters**: Narrow down results by genre and emotional tone (Joy, Fear, Anger, etc.).
- 🧠 **Google Generative AI Embeddings**: Captures deep semantic meaning of queries and descriptions.
- 💾 **Chroma Vector Database**: Efficient similarity search powered by LangChain.
- 🎨 **Interactive Gradio UI**: Simple and intuitive user interface to explore recommendations visually.

---

## 🛠️ Requirements

- Python 3.11.0
- Required Python packages (listed in `requirements.txt`)
- Google API Key for accessing the Gemini AI services

---

## 🚀 Installation

1. **Clone the repository**:

     ```bash
    git clone https://github.com/Vish501/Book-Recommender.git
    ```
     
     ```bash
     cd Book-Recommender
    ```

2. **Install dependencies**:

    It's recommended to use a virtual environment to manage dependencies. You can create and activate one using:
   
     ```bash
     conda create -p venv python=3.11.0 -y
    ```
     
     ```bash
    conda activate venv/
   ```
     Then, install the required packages: ```pip install -r requirements.txt```  

---

## 💻 Setting Up the Google API Key

To use the Gemini API, you need to set up your GOOGLE_API_KEY:

1. Obtain your **Google API Key** from the **Google Cloud Console**.
2. Add the API key to your environment:
     - Locally (Linux/macOS): ```export GOOGLE_API_KEY="your-api-key-here"```
     - Locally (Windows - Command Prompt): ```set GOOGLE_API_KEY="your-api-key-here"```
     - Locally (Windows - PowerShell): ```$env:GOOGLE_API_KEY="your-api-key-here"```

3. If you are using GitHub Codespaces, store the API key as a GitHub repository secret:
     
     - Go to your GitHub repository
     - Navigate to **Settings > Secrets and variables > Actions**
     - Click **New repository secret**
     - Set the name as ```GOOGLE_API_KEY``` and paste your API key as the value
     - Click **Add secret**

4. Using a `.venv` file:
   Add the following line to your `.venv` file in the root directory:
     ```env
     GOOGLE_API_KEY=your_google_api_key_here
     ```

This will allow the project to authenticate and communicate with the Gemini API securely.

---

## 📁 Setting Up the Working Directory

To ensure the app can locate and load the dataset correctly, you need to set the `WORKING_DIRECTORY` environment variable. This should point to the **root directory of the project** (where `app.py` and the `data/` folder are located).

1. Determine the **absolute path** of your project directory.

2. Set the `WORKING_DIRECTORY` environment variable:
     - Locally (Linux/macOS): ```export WORKING_DIRECTORY="/absolute/path/to/Book-Recommender"```
     - Locally (Windows - Command Prompt): ```set WORKING_DIRECTORY="C:\path\to\Book-Recommender"```
     - Locally (Windows - PowerShell): ```$env:WORKING_DIRECTORY="C:\path\to\Book-Recommender"```

3. Using GitHub Codespaces or GitHub Actions:
   
   - Store the working directory as a secret or variable:
     - Go to your GitHub repository
     - Navigate to **Settings > Secrets and variables > Actions**
     - Click **New repository secret**
     - Set the name as `WORKING_DIRECTORY` and the value as your project path
     - Click **Add secret**

4. Using a `.venv` file:
   Add the following line to your `.venv` file in the root directory:
   ```env
   WORKING_DIRECTORY=/absolute/path/to/Book-Recommender
   ```

---

## 💻 Usage

To run the application:​

```bash
python app.py
```

This will launch the application, which will provide you with a link in the terminal that needs to be pasted into your browser.

---

## 📁 Project Structure
- ```app.py```: Main application file for Gardio.
- ```data```: CSV datasets used in the project.
- ```requirements.txt```: List of required Python packages.
- ```setup.py```: Setup configuration for the project.
- ```template.py```: Contains template code to create the basic project structure.
- ```research/```: Directory for research-related and data-cleaning files.
- ```src/```: Source code directory containing modules and packages.
- ```.venv```: Environment variables (not tracked in Git)

---

## 📄 License

This project is licensed under the MIT License. See the LICENSE file for details.

---

## 🙋‍♂️ Author

Feel free to contribute to this project by submitting issues or pull requests. For any questions or suggestions, please contact ```Vish501```.