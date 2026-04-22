# AutoStream AI Agent

## How to run

1. Install dependencies
pip install -r requirements.txt

2. Run project
python app.py


## Architecture Explanation

We used a conversational AI agent that integrates
Intent Detection, Retrieval Augmented Generation (RAG),
and Tool Execution.

Intent detection identifies whether the user is greeting,
asking about pricing, or showing high purchase intent.

RAG retrieves information from a local JSON knowledge base
containing AutoStream pricing and company policies.

State is managed using a Python dictionary that stores
conversation memory such as name, email, and creator platform.

Once the user shows high intent, the system collects
lead information and calls a mock API function to simulate
lead capture.


## WhatsApp Integration (Concept)

The agent can be deployed on WhatsApp using:

WhatsApp Business API → Webhook → FastAPI server → Agent logic

Steps:

1. User sends message on WhatsApp
2. WhatsApp webhook sends message to backend server
3. Backend sends message to AI agent
4. Agent response is returned to WhatsApp user