# ViralIQ — Complete Project Requirements for Antigravity

## 1. Project Title

**AI-Based Viral Reel Performance Prediction and Intelligent Script Optimization System**

Product name: **ViralIQ**

---

## 2. Project Objective

Build a complete AI-powered web application for creators, marketers, and businesses that can:

1. Analyze an existing reel script.
2. Predict its viral performance potential using Machine Learning and ANN.
3. Accept a video upload and extract its spoken content into text.
4. Analyze the transcript as a script.
5. Analyze the video's thumbnail/visual frame separately using CNN.
6. Generate new reel scripts from natural-language user requirements.
7. Provide a Grammarly-style **Enhance Prompt** button that converts an informal user request into a structured professional LLM prompt.
8. Use an LLM to generate multiple candidate scripts.
9. Evaluate every generated candidate using ML + ANN.
10. Select the highest-scoring candidate.
11. If the target score is not reached, generate another batch and repeat within a safe maximum limit.
12. Use a SQLite database containing high-performing/viral script examples as contextual knowledge for generation.
13. Give the user an explanation of weaknesses and actionable improvements.
14. Store user scripts, predictions, generated candidates, and analysis history with CRUD operations.
15. Provide a clean, premium, React-style SaaS dashboard.

---

# 3. IMPORTANT PRODUCT LOGIC

The application must NOT claim that a reel is guaranteed to go viral.

Use terminology such as:

- Predicted Viral Potential
- Predicted Performance Score
- Content Performance Score
- Visual Quality Score

Do NOT present the model output as a guarantee.

The 80% value is an **optimization target**, not a universal definition of virality.

---

# 4. CORE USER FLOWS

## Flow A — Analyze Existing Script

User pastes or uploads a script.

Pipeline:

User Script
→ Text Preprocessing
→ Feature Extraction
→ ML Prediction
→ ANN Prediction
→ Combined Predicted Score
→ LLM Explanation
→ Improvement Recommendations

Example:

- ML Score: 72%
- ANN Score: 78%
- Combined Score: 75%
- Status: Needs Optimization

If score >= 80%, show High Potential.

If score < 80%, offer AI Optimization.

---

## Flow B — Analyze Existing Video

User uploads an MP4/video.

The video must have two separate pipelines.

### Pipeline 1 — Spoken Content

Video
→ Audio Extraction
→ Speech-to-Text
→ Transcript
→ Script Feature Extraction
→ ML + ANN
→ Script Performance Score

### Pipeline 2 — Thumbnail / Visual

Video
→ Frame Extraction
→ Candidate Frames
→ CNN
→ Visual/Thumbnail Quality Analysis
→ Best Thumbnail Recommendation

IMPORTANT:
CNN must NOT be used for script analysis.

CNN is specifically for the thumbnail/visual-analysis module.

The final LLM can explain both:

- Script/content weaknesses
- Thumbnail/visual weaknesses

---

## Flow C — Generate New Script

User enters natural requirements such as:

"real estate 50 lakh na ghar sale"

Optional structured fields:

- Topic
- Audience
- Platform
- Duration
- Goal
- Tone
- Language
- Content Type
- CTA Goal

User sees a small button:

**✨ Enhance Prompt**

The system transforms the informal request into a structured prompt containing:

- Role
- Context
- Task
- Audience
- Goal
- Platform
- Tone
- Duration
- Constraints
- Output format
- Relevant examples/context

Example:

Role:
Act as an expert real-estate Instagram Reel script writer.

Task:
Create a 30-second lead-generation reel script for a ₹50 lakh property.

Output:
Hook
Script
CTA
Caption
Hashtags

The enhanced prompt can be previewed, edited, copied, or used directly.

---

# 5. AI SCRIPT GENERATION + OPTIMIZATION ENGINE

The system should generate multiple candidate scripts instead of trusting one generation.

Example configuration:

- Candidate batch size: 10–20
- Target score: 80
- Maximum batches: configurable, default 5

Pipeline:

User Requirements
+
Enhanced Prompt
+
Relevant Viral Script Database Examples
+
LLM
→ Candidate 1...N
→ ML + ANN scoring for every candidate
→ Rank candidates
→ Save global best candidate

If best score >= 80:
STOP and return best candidate.

If best score < 80:
Generate another batch.

After maximum batches:
Return the highest-scoring candidate found across ALL batches.

Never create an infinite generation loop.

Example:

Batch 1 best = 76
Batch 2 best = 74
Batch 3 best = 89

Return the 89 score candidate.

If all batches are below 80:

76, 74, 79, 77, 78

Return the 79 candidate.

---

# 6. GLOBAL BEST TRACKING

Maintain:

- best_script
- best_score
- best_batch
- best_candidate_id

Every candidate must be evaluated.

Pseudo logic:

if candidate_score > best_score:
    best_score = candidate_score
    best_script = candidate

if best_score >= TARGET_SCORE:
    stop_generation

else if batch_count >= MAX_BATCHES:
    return best_script

else:
    generate_next_batch

---

# 7. MACHINE LEARNING — AI-503

Use Scikit-learn.

Suggested initial model:

**Random Forest Classifier**

Possible alternatives for comparison:

- Logistic Regression
- Gradient Boosting

Do not overcomplicate the model selection.

ML responsibilities:

- Data preprocessing
- Feature engineering
- Training
- Evaluation
- Prediction
- Save model
- Load model
- Real-time inference

Possible script features:

- Word count
- Script duration
- Hook strength
- CTA presence
- Question presence
- Curiosity indicators
- Emotional-word count
- Topic/category
- Posting metadata when available
- Engagement features when historical performance data is available

Evaluation:

- Accuracy
- Precision
- Recall
- F1-score
- Confusion matrix

Model file:

`models/ml_viral_model.pkl`

---

# 8. ARTIFICIAL NEURAL NETWORK — AI-505

Use TensorFlow/Keras.

Suggested ANN:

Input
→ Dense 64 + ReLU
→ Dense 32 + ReLU
→ Dense 16 + ReLU
→ Output

Responsibilities:

- Train
- Validate
- Predict
- Save
- Load
- Evaluate

Use EarlyStopping during ANN training.

Track:

- Training accuracy
- Validation accuracy
- Training loss
- Validation loss
- Precision
- Recall
- F1-score
- Confusion matrix where applicable

Model file:

`models/viral_ann.keras`

IMPORTANT:
EarlyStopping controls ANN training. It does NOT replace the script-generation batch stopping logic.

---

# 9. CNN — AI-505 — SEPARATE OPTIONAL/LATER MODULE

IMPORTANT:
**Do NOT implement CNN/thumbnail analysis during the initial build.**

The CNN module must remain completely separate from the core script-analysis and script-generation pipeline.

### Core project must work WITHOUT CNN first.

Later, after the main application is stable, CNN can be added as a separate module:

Video
→ Frame Extraction
→ Candidate Thumbnail Frames
→ CNN
→ Visual/Thumbnail Quality Analysis
→ Best Thumbnail Recommendation

CNN responsibility:
- Thumbnail quality classification
- Visual clarity
- Composition
- Subject prominence
- Text visibility
- Presentation quality

CNN must NOT:
- Analyze the script
- Predict script virality
- Replace ML/ANN
- Be part of the initial script-generation loop

Recommended future model file:
`models/thumbnail_cnn.keras`

### Development priority

Build and test the following first:

1. SQLite CRUD
2. Streamlit UI
3. Dataset and preprocessing
4. ML model
5. ANN model
6. Script analysis
7. Prompt Engineering
8. Gemini API integration
9. Script candidate generation
10. ML + ANN candidate scoring
11. Best-candidate selection
12. Viral Script Library
13. AI Agent
14. Analytics
15. Reports

Only after the above is working and stable, create a separate:
**Thumbnail Intelligence / Visual Analysis** section for CNN.

The CNN module should be independently switchable and must not break the core application if it is unavailable.

# 10. LLM — AI-504 — GEMINI API

Use **Google Gemini API as the primary LLM for this project**.

The user/developer will provide the Gemini API key separately. Never hard-code the API key.

Use environment variables / secrets, for example:
`GEMINI_API_KEY`

The LLM layer is responsible for:

- Script generation
- Hook generation
- CTA generation
- Caption generation
- Script improvement
- Script analysis explanation
- Prompt enhancement
- AI recommendations
- AI report generation
- Candidate script generation

### Gemini integration requirements

Create a dedicated service such as:

`services/gemini_service.py`

Keep all Gemini-specific code inside this service.

Expose clean functions such as:

- `generate_script()`
- `generate_candidates()`
- `improve_script()`
- `enhance_prompt()`
- `analyze_script()`
- `generate_report()`

Do NOT scatter Gemini API calls throughout the UI code.

Use configuration/environment variables for:
- API key
- model name
- temperature where applicable
- candidate batch size
- maximum batches

The application must show a clear error state if:
- API key is missing
- API request fails
- quota/rate limit occurs
- Gemini returns invalid/empty output

Do not expose raw API errors or secrets to the user.

### Provider architecture

Gemini is the required primary implementation for this project.

However, keep the LLM service modular so an approved alternative can be added later without rewriting the rest of the application.

# 11. PROMPT ENGINEERING — AI-504

Implement real prompt-engineering techniques:

1. Role prompting
2. Context injection
3. Clear task definition
4. User requirements
5. Constraints
6. Output format
7. Audience specification
8. Tone specification
9. Few-shot examples where appropriate
10. Prompt enhancement from unstructured user text

The Viral Script Database can provide relevant examples as context.

Never instruct the LLM to copy stored scripts verbatim.

Use examples to learn structure, hook patterns, CTA patterns, and style.

---

# 12. AI AGENT — AI-504

Implement an AI Agent/workflow that coordinates:

User Requirement
→ Database Retrieval
→ Prompt Construction
→ LLM Candidate Generation
→ ML Evaluation
→ ANN Evaluation
→ Ranking
→ Target Check
→ Regeneration if needed
→ Final Best Script

The agent should not invent model scores.

All ML/ANN scores must come from the actual trained models.

---

# 13. SQLITE DATABASE — AI-503

Use SQLite.

Minimum tables:

## users

- id
- name
- email
- created_at

## scripts

- id
- user_id
- title
- script_text
- category
- audience
- platform
- duration
- created_at
- updated_at

## predictions

- id
- script_id
- ml_score
- ann_score
- final_score
- status
- created_at

## viral_scripts

- id
- category
- topic
- audience
- hook
- script_text
- duration
- views
- likes
- comments
- shares
- engagement_rate
- performance_label

## generated_candidates

- id
- original_script_id
- batch_number
- candidate_number
- script_text
- ml_score
- ann_score
- final_score
- is_best
- created_at

## reports

- id
- script_id
- analysis
- recommendations
- created_at

CRUD MUST be visible in the application.

---

# 14. STREAMLIT / FRONTEND REQUIREMENT

The UI must be a premium, clean, modern SaaS interface.

The visual experience should feel similar to a polished React application.

IMPORTANT:
If Streamlit is required by the university, keep Streamlit as the application framework.

Use custom CSS/components to create the React-style visual experience.

Do not create an unnecessary React frontend if it creates syllabus/deployment complexity.

If the project architecture is approved for a React frontend + Python API, it can be separated later, but the initial implementation should prioritize syllabus compliance and working AI features.

---

# 15. UI DESIGN DIRECTION

Design language:

- Minimal
- Premium
- Clean
- Spacious
- Neutral base
- Strong typography
- Subtle borders
- Soft shadows
- Rounded cards
- Small controlled gradients only where useful
- No excessive glassmorphism
- No excessive animations
- No clutter
- No giant unnecessary hero sections inside the dashboard
- Strong information hierarchy

Reference the calm, focused product UI philosophy of Linear, the clean dashboard patterns available through Vercel templates, and Pinterest's visual discovery/card organization.

Useful references:

- Linear: https://linear.app/
- Linear UI redesign principles: https://linear.app/now/how-we-redesigned-the-linear-ui
- Vercel UI guidelines: https://vercel.com/design/guidelines
- Vercel clean React/Next.js dashboard templates: https://vercel.com/templates/next.js/next-js-and-shadcn-ui-admin-dashboard
- Vercel modern dashboard template: https://vercel.com/templates/react/modernize-admin-dashboard
- Pinterest: https://www.pinterest.com/

Do NOT copy any website. Use them only as design inspiration.

---

# 16. MAIN NAVIGATION

Sidebar:

- Dashboard
- Analyze Script
- Analyze Reel
- Generate Script
- Viral Library
- My Scripts
- AI Advisor
- Analytics
- Reports
- Settings

Top bar:

- Search
- Notifications
- User profile
- Theme toggle if implemented

---

# 17. DASHBOARD

Show:

- Total Scripts
- Reels Analyzed
- Average Predicted Score
- Best Predicted Score
- Scripts Optimized
- Recent Analyses

Main cards:

- Recent Scripts
- Best Performing Predictions
- Optimization Activity
- Score Trend

Use clean charts.

---

# 18. ANALYZE SCRIPT PAGE

Components:

- Large script editor/text area
- Upload script option
- Analyze button
- Score card
- ML score
- ANN score
- Combined score
- Hook score
- CTA score
- Audience match
- AI feedback
- Improvement button

Use visual score indicators but do not overuse circular gauges.

---

# 19. ANALYZE REEL PAGE

Upload:

- MP4
- Supported video format clearly displayed

Show:

- Video preview
- Transcript extraction progress
- Transcript result
- Script prediction
- ML score
- ANN score
- Thumbnail analysis
- CNN visual score
- Recommended thumbnail/frame
- AI recommendations

Separate sections clearly:

### Script Intelligence
ML + ANN

### Visual Intelligence
CNN

### AI Recommendations
LLM

---

# 20. GENERATE SCRIPT PAGE

Input:

- Topic
- Target audience
- Platform
- Duration
- Goal
- Tone
- Language
- Content type
- Additional requirements

Chat-style free-text input:

"real estate 50 lakh na ghar sale"

Button:

**✨ Enhance Prompt**

Then show:

### Enhanced Prompt Preview

Buttons:

- Edit
- Copy
- Use Prompt

Then:

**Generate Best Script**

Show optimization progress:

Batch 1
- 20 candidates
- Best: 76%

Batch 2
- 20 candidates
- Best: 81%

Target achieved.

Show:

### Recommended Script

- Score
- Hook
- Full script
- CTA
- Caption
- Hashtags
- Why this version was selected

Also show optional:

### Candidate Comparison

Top 3 candidates with scores.

---

# 21. VIRAL SCRIPT LIBRARY

Show high-performing script records.

Filters:

- Category
- Platform
- Duration
- Audience
- Performance label

Cards/table should show:

- Hook
- Category
- Performance
- Engagement
- Use as reference

Do not expose copyrighted/private data without permission.

---

# 22. MY SCRIPTS

CRUD interface:

- Create
- View
- Edit
- Delete

Show:

- Script title
- Score
- Status
- Date
- Optimization count

---

# 23. AI ADVISOR

Chat-style assistant.

User can ask:

- Why is my script weak?
- How can I improve the hook?
- Give me a stronger CTA.
- Why did candidate 3 score higher?
- What should I change in this reel?

The assistant must use project data where relevant.

---

# 24. ANALYTICS

Charts:

- ML vs ANN scores
- Score distribution
- Category performance
- Optimization improvement
- Candidate score distribution
- Batch performance
- Model metrics

Do not fake metrics.

Use actual model outputs.

---

# 25. REPORTS

Generate a clean report containing:

- Input
- Transcript
- ML score
- ANN score
- CNN visual score if video
- LLM analysis
- Weaknesses
- Recommendations
- Best generated script
- Optimization history

Allow download if supported.

---

# 26. PROJECT STRUCTURE

Prefer a clean modular structure:

```text
viraliq/
├── app.py
├── pages/
│   ├── dashboard.py
│   ├── analyze_script.py
│   ├── analyze_reel.py
│   ├── generate_script.py
│   ├── viral_library.py
│   ├── my_scripts.py
│   ├── ai_advisor.py
│   ├── analytics.py
│   └── reports.py
│
├── models/
│   ├── ml_viral_model.pkl
│   ├── viral_ann.keras
│   └── thumbnail_cnn.keras
│
├── services/
│   ├── ml_service.py
│   ├── ann_service.py
│   ├── cnn_service.py
│   ├── llm_service.py
│   ├── prompt_service.py
│   ├── agent_service.py
│   ├── transcription_service.py
│   └── optimization_service.py
│
├── database/
│   ├── db.py
│   ├── models.py
│   └── crud.py
│
├── data/
│   ├── datasets/
│   └── viral_scripts.db
│
├── prompts/
│   ├── script_generation.txt
│   ├── prompt_enhancement.txt
│   ├── script_analysis.txt
│   └── report_generation.txt
│
├── utils/
│   ├── feature_extraction.py
│   ├── scoring.py
│   └── validation.py
│
├── assets/
├── requirements.txt
└── README.md
```

---

# 27. SCORING DESIGN

Do not blindly average ML and ANN without documenting the methodology.

Start with a configurable score aggregation layer:

`final_score = aggregation(ml_score, ann_score)`

Keep the aggregation method configurable.

Document and validate the chosen method using test/validation results.

The system must always store:

- ML score
- ANN score
- final score

Never overwrite raw model predictions.

---

# 28. DATASET REQUIREMENTS

The dataset is one of the most important parts of the project.

Need historical reel/script performance data.

Possible fields:

- category
- topic
- duration
- word count
- hook type
- CTA
- views
- likes
- comments
- shares
- saves
- engagement rate
- audience size where available
- performance label

Define the performance/viral label using a documented methodology.

Do NOT simply label random scripts as viral.

Keep:

- training set
- validation set
- test set

Separate preprocessing for training and inference to avoid data leakage.

---

# 29. ERROR HANDLING

The application must handle:

- Invalid video
- Unsupported file
- Empty script
- LLM API failure
- Missing API key
- Model not found
- Database failure
- Speech-to-text failure
- CNN frame extraction failure
- Timeout
- Large upload

Never expose raw stack traces to users.

Show clear actionable messages.

---

# 30. SECURITY

- Never hard-code API keys.
- Use environment variables / secrets.
- Validate uploads.
- Limit file size.
- Validate file type.
- Sanitize user inputs.
- Never execute uploaded files.
- Do not store sensitive data unnecessarily.

---

# 31. PERFORMANCE

- Cache loaded ML/ANN/CNN models.
- Avoid reloading models for every prediction.
- Process video frames efficiently.
- Limit candidate generation batch size.
- Use configurable maximum batches.
- Show progress during long operations.
- Do not run unlimited LLM calls.

---

# 32. ACADEMIC SUBJECT MAPPING

## AI-503

- Scikit-learn ML
- Feature engineering
- Model training
- Evaluation
- Model save/load
- Real-time prediction
- Streamlit
- SQLite
- CRUD
- Deployment

## AI-504

- Prompt Engineering
- LLM
- Open-source AI compatibility
- Prompt Enhancement
- Script Generation
- Context Injection
- Few-shot prompting
- AI Agent
- LangChain/Ollama/Hugging Face where approved
- AI recommendations

## AI-505

- Artificial Neural Network
- TensorFlow/Keras
- ANN prediction
- Deep Learning
- CNN
- Thumbnail/visual analysis
- Model evaluation
- EarlyStopping
- Model save/load

---

# 33. DEVELOPMENT PRIORITY

Build in this exact order:

### Phase 1 — Foundation
- Project structure
- SQLite
- CRUD
- Streamlit UI
- Dashboard

### Phase 2 — ML
- Dataset
- preprocessing
- feature extraction
- ML training
- evaluation
- prediction

### Phase 3 — ANN
- TensorFlow/Keras
- ANN training
- evaluation
- EarlyStopping
- save/load

### Phase 4 — Script Analysis
- Analyze script
- ML + ANN scores
- LLM explanation

### Phase 5 — LLM
- Gemini/open-source provider adapter
- Prompt Enhancer
- Script Generator
- Candidate generation

### Phase 6 — Optimization Engine
- Generate N candidates
- Score all
- Rank
- Global best
- Target score
- Maximum batch limit

### Phase 7 — Viral Library
- SQLite viral scripts
- Retrieval/filtering
- Context injection

### Phase 8 — Video
- Upload
- Speech-to-text
- Transcript
- Script analysis

### Phase 9 — CNN
- Frame extraction
- Thumbnail model
- Best-frame recommendation

### Phase 10 — Agent
- Connect retrieval
- prompt generation
- LLM
- ML
- ANN
- ranking
- regeneration

### Phase 11 — Reports + Analytics
- Reports
- charts
- history
- model metrics

### Phase 12 — Testing + Deployment
- unit tests
- integration tests
- UI tests
- model tests
- deployment
- documentation

---

# 34. NON-NEGOTIABLE RULES FOR ANTIGRAVITY

1. Do not build fake AI functionality.
2. Do not hard-code fake prediction scores.
3. Do not show random percentages as model outputs.
4. Do not claim guaranteed virality.
5. Do not use CNN for script analysis.
6. Do not use ANN EarlyStopping as the script-generation stopping mechanism.
7. Do not create an infinite candidate-generation loop.
8. Always keep the global highest-scoring candidate.
9. Always preserve raw ML and ANN scores.
10. Keep LLM provider replaceable.
11. Keep SQLite CRUD fully functional.
12. Keep UI clean and production-like.
13. Do not sacrifice syllabus requirements for visual effects.
14. Build real working modules before adding decorative animations.
15. Use real model evaluation metrics in the report.

---

# 35. UI QUALITY BAR

The UI should feel like a modern AI SaaS product, not a college-project dashboard.

Priorities:

1. Typography
2. Spacing
3. Alignment
4. Information hierarchy
5. Clean navigation
6. Clear states
7. Fast interactions
8. Responsive layout
9. Accessible controls
10. Subtle motion

Avoid:

- Excessive gradients
- Neon colors everywhere
- Excessive glassmorphism
- Huge cards
- Too many charts
- Unnecessary animations
- Tiny text
- Cluttered sidebar
- Fake 3D effects

Use a restrained neutral palette with one primary accent.

---

# 36. FINAL PRODUCT EXPERIENCE

The final user experience should feel like:

**Upload → Analyze → Understand → Improve → Generate → Evaluate → Select**

The application should make the user feel that the system is not merely generating random scripts, but is using:

- historical high-performing content
- user requirements
- prompt engineering
- LLM generation
- ML prediction
- ANN prediction
- CNN visual analysis
- iterative candidate ranking

to recommend the strongest available content.

---

# 37. SUCCESS CRITERIA

## Core MVP — must be completed first

The core application is considered successful when a user can:

1. Add a script.
2. Analyze a script.
3. Receive real ML + ANN predictions.
4. Enter natural-language requirements.
5. Use the Enhance Prompt feature.
6. Generate multiple scripts through Gemini API.
7. Score every candidate with ML + ANN.
8. Select the highest-scoring candidate.
9. Regenerate another batch when the target is not achieved.
10. Stop safely at the maximum batch limit.
11. Always preserve the global best candidate.
12. Store history in SQLite.
13. Edit/delete records.
14. View analytics.
15. Generate a report.
16. Demonstrate the complete core workflow during viva.

## Later CNN Module — separate milestone

Only after the core MVP is stable:

17. Upload a video.
18. Extract candidate frames.
19. Run CNN thumbnail/visual analysis.
20. Recommend the strongest thumbnail/frame.
21. Show visual improvement recommendations.

The CNN module must remain separate and must not be required for the core script-generation pipeline.
