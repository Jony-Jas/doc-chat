## Requirements

- Python 3.11
- Conda
- FastAPI
- Uvicorn

## Installation

1. Clone the repository:

   ```sh
   git clone <repository-url>
   cd doc-chat
   ```

2. Run the Application 🚀:

   ```sh
   run_app.bat
   ```

## Environment Variables

Create a `.env` file in the root directory and add the following environment variables:

```properties
HUGGINGFACE_TOKEN="your_huggingface_token" # Currently not used
NVIDIA_KEY="your_nvidia_key"
GROQ_API_KEY="your_groq_api_key"

# Models
NVIDIA_EMBEDDING_MODEL="nvidia/llama-3.2-nv-embedqa-1b-v2"
GROQ_CHAT_MODEL="deepseek-r1-distill-llama-70b"
```

## Usage

1. Start the FastAPI application 🚀:

   ```sh
   ./run_app.bat
   ```

## API Endpoints

### Upload a PDF

- **URL:** `/upload`
- **Method:** `POST`
- **Description:** Upload a PDF document.
- **Parameters:**

| Name | Type         | Description             |
| ---- | ------------ | ----------------------- |
| file | `UploadFile` | The PDF file to upload. |

- **Response:**

| Name    | Type   | Description               |
| ------- | ------ | ------------------------- |
| message | string | Success or error message. |
| error   | string | Error message, if any.    |

- **Axios Example:**

  ```javascript
  //<--skip-->
  const formData = new FormData();
  formData.append("file", fileInput.files[0]);

  axios.post("http://127.0.0.1:8000/upload", formData, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });
  //<--skip-->
  ```

### Ask a Question

- **URL:** `/ask`
- **Method:** `POST`
- **Description:** Ask a question related to the uploaded PDF document.
- **Parameters:**

| Name     | Type   | Description                        |
| -------- | ------ | ---------------------------------- |
| question | string | The question to ask.               |
| context  | string | The context (filename) of the PDF. |

- **Response:**

| Name     | Type   | Description                 |
| -------- | ------ | --------------------------- |
| question | string | The question asked.         |
| answer   | string | The answer to the question. |
| error    | string | Error message, if any.      |

- **Axios Example:**
  ```javascript
  //<--skip-->
  axios.post("http://127.0.0.1:8000/ask?context=fileName", {
    question: "What is the main topic of the document?",
  });
  //<--skip-->
  ```

### Clear Database

- **URL:** `/clear`
- **Method:** `GET`
- **Description:** Clear the cached data for a specific PDF document.
- **Parameters:**

| Name    | Type   | Description                        |
| ------- | ------ | ---------------------------------- |
| context | string | The context (filename) of the PDF. |

- **Response:**

| Name    | Type   | Description               |
| ------- | ------ | ------------------------- |
| message | string | Success or error message. |
| error   | string | Error message, if any.    |

- **Axios Example:**
  ```javascript
  //<--skip-->
  axios.get("http://127.0.0.1:8000/clear?context=fileName");
  //<--skip-->
  ```
