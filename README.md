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

2. Ensure conda is installed. https://www.anaconda.com/download and set set to environment variables

3. Run the Application 🚀:

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

Links to Get:

NVIDIA_KEY -> https://build.nvidia.com/nvidia/llama-3_2-nv-embedqa-1b-v2

GROQ_API_KEY -> https://console.groq.com/keys

## API Endpoints

### Upload a PDF

- **URL:** `/upload`
- **Method:** `POST`
- **Description:** Upload a PDF document.
- **Body:**

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
- **Params:**

  | Name    | Type   | Description                        |
  | ------- | ------ | ---------------------------------- |
  | context | string | The context (filename) of the PDF. |

- **body:**
  | Name | Type | Description |
  | -------- | ------ | ---------------------------------- |
  | question | string | The question to ask. |

- **Response:**

  | Name     | Type   | Description                 |
  | -------- | ------ | --------------------------- |
  | question | string | The question asked.         |
  | answer   | string | The answer to the question. |
  | error    | string | Error message, if any.      |

- **Axios Example:**
  ```javascript
  //<--skip-->
  axios.post("http://127.0.0.1:8000/ask", {
    question: "What is AC/DC?",
  });
  //<--skip-->
  ```
  ```javascript
  //<--skip-->
  axios.post("http://127.0.0.1:8000/ask?context=fileName", {
    question: "What is the pdf about?",
  });
  //<--skip-->
  ```

### Clear Database

- **URL:** `/clear`
- **Method:** `GET`
- **Description:** Clear the cached data for a specific PDF document.
- **Params:**

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
