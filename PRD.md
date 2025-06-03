**Product Requirements Document (PRD)**

### **Project Title:**

Build an AI App Using ONLY Local Inference

---

### **Objective:**

Develop a simple AI-powered application leveraging a locally hosted LLM (e.g., Llama3) to provide AI services without relying on external APIs such as OpenAI or Anthropic.

---

### **App Type Selected:**

**AI Writer**: Generate creative text outputs such as blog introductions, tweets, or stories based on user-provided topics.

---

### **Key Features:**

#### 1. **Prompt Input Box:**

* A text input field for users to specify the topic or idea they want the AI to write about.
* Features such as placeholder text (“Enter your topic here”) and character limits for concise input.

#### 2. **Model Output Display:**

* A dynamic area to display the generated text.
* Includes features like copy-to-clipboard and clear output.

#### 3. **Temperature Setting (Optional):**

* A slider or dropdown allowing users to adjust the temperature of the generation model (e.g., from deterministic to creative output).

#### 4. **Loading UI:**

* A visual loading indicator (e.g., spinner or progress bar) to inform users when the model is generating output.

#### 5. **Output Logging:**

* Save all generated outputs locally in a file (e.g., `output_log.txt`).
* Includes metadata such as timestamps and prompt inputs for traceability.

#### 6. **Locally Hosted Inference Engine:**

* Run the Llama3 model locally using frameworks such as PyTorch or TensorFlow.
* Pre-load and initialize the model during app startup.

---

### **Non-Functional Requirements:**

#### **Performance:**

* Model inference should generate outputs within a maximum of 5 seconds for typical prompts.

#### **Compatibility:**

* The app should support major operating systems (Windows, macOS, Linux).

#### **Usability:**

* Simple and intuitive interface to maximize accessibility.

#### **Security:**

* Ensure no data is sent to external servers.

#### **Maintainability:**

* Modular architecture for easy updates or replacement of the LLM.

---

### **Implementation Details:**

#### **Local LLM Setup:**

1. Use the Llama3 model.
2. Dependencies:

   * Python 3.9+
   * PyTorch
   * Transformers library (Hugging Face)
   * SentencePiece (for tokenization)
3. Optimization:

   * Use 4-bit quantization for faster inference on consumer hardware.
   * Preload weights during startup to reduce runtime latency.

#### **Frontend Development:**

* **Framework:** React or Electron.js
* **Key Components:**

  * InputBox Component
  * OutputDisplay Component
  * TemperatureSlider Component
  * Loader Component

#### **Backend Development:**

* **Framework:** Flask or FastAPI
* **Key Endpoints:**

  * `/generate`: Accepts prompt and temperature; returns generated text.

#### **Local Logging:**

* Log format: `timestamp | prompt | output`
* File location: `./logs/output_log.txt`

---

### **Submission Guidelines:**

#### **Public GitHub Repository:**

* Repository containing the complete source code.
* Structured folders for `frontend`, `backend`, and `logs`.

#### **README.md:**

Include:

1. **App Type:** AI Writer
2. **Setup Instructions:**

   * Clone the repository.
   * Install dependencies: `pip install -r requirements.txt`
   * Download model weights (link or script provided in README).
   * Run the app: `python app.py` for backend and `npm start` for frontend.
3. **How to Use:**

   * Open the app in a browser.
   * Enter a topic in the prompt box.
   * Adjust the temperature (if needed).
   * Click “Generate” to view output.
4. **Model Used:** Llama3

---

### **Potential Challenges:**

#### **Model Performance:**

* **Mitigation:** Optimize model size and use techniques like quantization to ensure reasonable performance on local hardware.

#### **User Hardware Limitations:**

* **Mitigation:** Include hardware requirements in README and provide lighter-weight options if feasible.

#### **Ease of Use:**

* **Mitigation:** Design a highly intuitive UI and offer clear error messages for users.

---

### **Development Timeline:**

#### **Week 1:**

* Finalize project setup and install dependencies.
* Integrate Llama3 model for local inference.

#### **Week 2:**

* Develop core features (prompt input, output display, temperature slider).
* Implement basic logging.

#### **Week 3:**

* Create and integrate the frontend with the backend.
* Add loading UI and polish the interface.

#### **Week 4:**

* Test the app on various hardware configurations.
* Finalize and publish the GitHub repository.

---

### **Implementation Plan (Step-by-Step for AI Coding Agent):**

Below is a precise, granular plan that an AI coding agent can follow to build the AI Writer app using only local inference.

#### **Phase 0: Environment Preparation**

1. **Verify System Requirements:**

   * Ensure Python 3.9+ is installed (`python --version`).
   * Ensure Node.js (v14+) and npm are installed (`node --version`, `npm --version`).
2. **Create Project Directory Structure:**

   * Root folder: `ai-local-writer`

     * `backend/`
     * `frontend/`
     * `models/`
     * `logs/`
     * `README.md`
   * Initialize Git repository: `git init`

#### **Phase 1: Setting Up the Backend**

1. **Virtual Environment:**

   * Navigate to `backend/`.
   * Create a virtual environment: `python -m venv venv`.
   * Activate virtual environment:

     * On macOS/Linux: `source venv/bin/activate`
     * On Windows: `venv\Scripts\activate`
2. **Install Python Dependencies:**

   * Create `requirements.txt` with:

     ```
     fastapi
     uvicorn
     torch
     transformers
     sentencepiece
     ```
   * Run `pip install -r requirements.txt`.
3. **Download and Prepare Llama3 Model Weights:**

   * In `models/`, include a script `download_model.py` that:

     * Downloads Llama3 quantized weights (4-bit) from a specified source or instructs the user to place them manually.
   * Run `python download_model.py` to place weights under `models/llama3-4bit/`.
4. **Build Inference Module:**

   * In `backend/`, create `inference.py`:

     * Load model and tokenizer from `transformers`:

       ```python
       from transformers import AutoTokenizer, AutoModelForCausalLM
       import torch

       MODEL_PATH = '../models/llama3-4bit/'

       tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
       model = AutoModelForCausalLM.from_pretrained(MODEL_PATH, torch_dtype=torch.float16, load_in_4bit=True)
       model.eval()

       def generate_text(prompt: str, temperature: float = 0.7, max_length: int = 200):
           inputs = tokenizer(prompt, return_tensors='pt')
           outputs = model.generate(**inputs, do_sample=True, temperature=temperature, max_length=max_length)
           return tokenizer.decode(outputs[0], skip_special_tokens=True)
       ```
   * Test inference in REPL: import `generate_text` and confirm it returns text.
5. **Develop FastAPI Application:**

   * Create `app.py` in `backend/`:

     ```python
     from fastapi import FastAPI
     from pydantic import BaseModel
     from inference import generate_text
     import time
     import os

     app = FastAPI()

     class GenerateRequest(BaseModel):
         prompt: str
         temperature: float = 0.7

     @app.post('/generate')
     async def generate(req: GenerateRequest):
         start_time = time.time()
         output = generate_text(req.prompt, req.temperature)
         duration = time.time() - start_time
         # Logging
         os.makedirs('../logs', exist_ok=True)
         with open('../logs/output_log.txt', 'a') as f:
             f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} | {req.prompt} | {req.temperature} | {output}\n")
         return { 'output': output, 'time_taken': duration }
     ```
   * Create a `.env` file if needed for configuration (e.g., port or model path), but defaults are acceptable for initial version.
6. **Run and Test Backend:**

   * Start server: `uvicorn app:app --reload --host 0.0.0.0 --port 8000`.
   * Use `curl` or Postman to POST `http://localhost:8000/generate` with JSON `{ "prompt": "Hello world", "temperature": 0.7 }`.
   * Verify response contains generated text and time taken.

#### **Phase 2: Setting Up the Frontend**

1. **Initialize Frontend Project:**

   * Navigate to `frontend/`.
   * Run `npx create-react-app .` to bootstrap a React app.
   * Install necessary packages:

     ```bash
     npm install axios
     ```
2. **Project Structure:**

   * `src/components/`

     * `InputBox.jsx`
     * `TemperatureSlider.jsx`
     * `Loader.jsx`
     * `OutputDisplay.jsx`
   * `src/App.jsx`
   * `src/api.js`
3. **API Helper Module:**

   * Create `src/api.js`:

     ```js
     import axios from 'axios';

     const API_URL = 'http://localhost:8000';

     export const generateText = async (prompt, temperature) => {
       const response = await axios.post(`${API_URL}/generate`, { prompt, temperature });
       return response.data;
     };
     ```
4. **Build Components:**

   * **InputBox.jsx**:

     ```jsx
     import React from 'react';

     const InputBox = ({ prompt, setPrompt }) => (
       <textarea
         value={prompt}
         onChange={(e) => setPrompt(e.target.value)}
         placeholder="Enter your topic here"
         rows={3}
         maxLength={200}
         style={{ width: '100%', padding: '8px', fontSize: '16px' }}
       />
     );

     export default InputBox;
     ```
   * **TemperatureSlider.jsx**:

     ```jsx
     import React from 'react';

     const TemperatureSlider = ({ temperature, setTemperature }) => (
       <div>
         <label>Temperature: {temperature.toFixed(1)}</label>
         <input
           type="range"
           min="0"
           max="1"
           step="0.1"
           value={temperature}
           onChange={(e) => setTemperature(parseFloat(e.target.value))}
         />
       </div>
     );

     export default TemperatureSlider;
     ```
   * **Loader.jsx**:

     ```jsx
     import React from 'react';

     const Loader = () => (
       <div className="loader" style={{ margin: '20px auto', textAlign: 'center' }}>
         <div>Loading...</div>
       </div>
     );

     export default Loader;
     ```
   * **OutputDisplay.jsx**:

     ```jsx
     import React from 'react';

     const OutputDisplay = ({ output }) => (
       <div style={{ whiteSpace: 'pre-wrap', marginTop: '20px', padding: '10px', border: '1px solid #ccc' }}>
         {output}
       </div>
     );

     export default OutputDisplay;
     ```
5. **App.jsx Assembly:**

   * Modify `src/App.jsx`:

     ```jsx
     import React, { useState } from 'react';
     import InputBox from './components/InputBox';
     import TemperatureSlider from './components/TemperatureSlider';
     import Loader from './components/Loader';
     import OutputDisplay from './components/OutputDisplay';
     import { generateText } from './api';

     function App() {
       const [prompt, setPrompt] = useState('');
       const [temperature, setTemperature] = useState(0.7);
       const [loading, setLoading] = useState(false);
       const [output, setOutput] = useState('');

       const handleGenerate = async () => {
         if (!prompt.trim()) return;
         setLoading(true);
         setOutput('');
         try {
           const res = await generateText(prompt, temperature);
           setOutput(res.output);
         } catch (err) {
           setOutput('Error generating text.');
         } finally {
           setLoading(false);
         }
       };

       return (
         <div style={{ maxWidth: '600px', margin: '40px auto', fontFamily: 'Arial, sans-serif' }}>
           <h1>Local AI Writer</h1>
           <InputBox prompt={prompt} setPrompt={setPrompt} />
           <TemperatureSlider temperature={temperature} setTemperature={setTemperature} />
           <button
             onClick={handleGenerate}
             style={{ marginTop: '20px', padding: '10px 20px', fontSize: '16px' }}
             disabled={loading}
           >
             Generate
           </button>
           {loading && <Loader />}
           {output && <OutputDisplay output={output} />}
         </div>
       );
     }

     export default App;
     ```
6. **Connect Frontend and Backend:**

   * Ensure CORS is enabled in FastAPI or use a proxy in `package.json`:

     * Option A (FastAPI CORS):

       ```python
       from fastapi.middleware.cors import CORSMiddleware

       app.add_middleware(
         CORSMiddleware,
         allow_origins=["http://localhost:3000"],
         allow_credentials=True,
         allow_methods=["*"],
         allow_headers=["*"],
       )
       ```
     * Option B (React Proxy): In `frontend/package.json`, add:

       ```json
       "proxy": "http://localhost:8000"
       ```
7. **Run Frontend:**

   * In `frontend/`, run `npm start`.
   * Navigate to `http://localhost:3000` and verify UI appears.

#### **Phase 3: Logging & File Management**

1. **Implement Logging in Backend (Already in place):**

   * Confirm logs are written to `logs/output_log.txt`.
   * Log entries format: `2025-06-03 14:23:45 | prompt | temperature | generated text`.
2. **Verify Log Creation and Rotation:**

   * Manually run several generations and check `logs/output_log.txt`.
   * Optionally implement simple rotation: if file > 5MB, rename to `output_log_1.txt` and start new file.

#### **Phase 4: Configuration & Testing**

1. **Configuration File (Optional):**

   * Create `config.json` at project root:

     ```json
     {
       "backend_port": 8000,
       "frontend_port": 3000,
       "model_path": "./models/llama3-4bit/"
     }
     ```
   * Modify code to read from `config.json` for portability.
2. **Unit Tests for Backend:**

   * Install `pytest`.
   * In `backend/tests/`, create `test_inference.py`:

     ```python
     import pytest
     from inference import generate_text

     def test_generate_text_non_empty():
         result = generate_text("Test prompt", temperature=0.5)
         assert isinstance(result, str)
         assert len(result) > 0
     ```
   * Run `pytest` to confirm tests pass.
3. **UI Testing (Manual/Automated):**

   * Manual: Test generating text, changing temperature, ensure loader appears.
   * Automated (Optional): Use Cypress or React Testing Library to simulate user interactions.

#### **Phase 5: Optimization and Finalization**

1. **Quantization and Performance Tuning:**

   * If inference is slow, experiment with:

     * Lowering bit-precision further (e.g., 3-bit if supported).
     * Enabling GPU inference if available: ensure PyTorch finds CUDA and model loads onto GPU.
   * Measure average generation time; aim for <5 seconds on test hardware.
2. **UI Polishing:**

   * Add responsive styling: ensure components resize on mobile.
   * Improve loader design (CSS spinner).
   * Add copy-to-clipboard button to OutputDisplay.
3. **Documentation:**

   * Finalize `README.md` with:

     * Overview of app and features.
     * Detailed setup steps (as in Phase 0–Phase 2).
     * Usage guide with screenshots or GIFs.
     * Troubleshooting common issues (e.g., model download failures).
   * Add a `LICENSE` file (e.g., MIT License).
4. **GitHub Actions (CI) Setup (Optional):**

   * Add `.github/workflows/ci.yml` to run:

     * Linting checks (ESLint for frontend, Flake8 for backend).
     * Unit tests for backend.
     * Build validation for frontend (`npm run build`).

#### **Phase 6: Deployment (Local-Only Distribution)**

1. **Packaging for Users:**

   * Provide a shell script `setup.sh` or `setup.bat`:

     * Installs Python dependencies.
     * Installs npm dependencies.
     * Downloads model weights.
     * Prints instructions to run backend and frontend.
2. **Distribution via GitHub:**

   * Tag a release (e.g., `v1.0.0`).
   * Create Release notes summarizing features and setup.
3. **Future Work (Optional):**

   * Add user authentication to store personal writing history.
   * Provide alternative models for lower-end hardware (e.g., smaller local LLM).
   * Extend to other app types (Rephraser, Explainer).

---

### **Success Metrics:**

* Functional app with a user-friendly interface.
* Outputs generated consistently within 5 seconds.
* Logged outputs stored locally with no external dependencies.
* Positive user feedback on ease of use and performance.
