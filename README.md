Sarathi - Voice Bot & AI Backend
This repository contains the backend server for the Sarathi web accessibility project. This server will act as the "AI brain" of the application, handling complex tasks like natural language processing, content generation, and third-party integrations.

🎯 Project Goal
The primary goal of this backend is to provide a robust and scalable API that the main Sarathi frontend can communicate with. It will process user input (like voice commands), perform intelligent actions using AI models, and return structured data for the frontend to act upon.

✨ Features (Planned)
We plan to build a series of micro-features, each exposed via its own API endpoint. The initial planned features include:

AI Voice Command Interpreter: An endpoint that will accept transcribed voice commands from the frontend, interpret the user's intent (e.g., scroll, navigate, read), and return a structured JSON command.

Emergency SOS Handler: An endpoint that will manage the logic for sending an emergency alert when triggered by a specific voice command from the user.

Generative Content Engine: Endpoints that will leverage generative AI to create on-demand, accessible content, such as educational games or social stories tailored to user needs.

🛠️ Proposed Technology Stack
To achieve our goals, we will be using a modern Python-based stack.

Language: Python

Framework: A lightweight web framework (such as Flask or FastAPI) to build the REST API.

Core Logic: We will explore various AI and Natural Language Processing (NLP) libraries to power our intelligent features.


## Features 

Automated Emergency mail