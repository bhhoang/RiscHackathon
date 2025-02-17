AI-Powered Quiz Generator

Streamlit
Python
AI

The AI-Powered Quiz Generator is a web application designed to create interactive quizzes for young students. It leverages advanced AI models, including the DeepSeek-67B model, to dynamically generate quizzes with a variety of question types such as multiple-choice, fill-in-the-blank, and drag-and-drop. The project aims to provide an engaging and educational tool for students while showcasing the capabilities of AI in educational technology.

This project is intended to be deployed in the market as a fully functional website, allowing students to benefit from its interactive and adaptive learning features. By collaborating with established learning platforms, the application will integrate seamlessly into existing educational ecosystems, providing a scalable and accessible solution for students worldwide.
Features

    Dynamic Quiz Generation: Generates quizzes with randomized question types and difficulty levels.

    Multiple Question Formats: Supports multiple-choice, fill-in-the-blank, and drag-and-drop questions.

    Real-Time Feedback: Provides immediate feedback on user answers.

    Interactive Interface: Built using Streamlit for a user-friendly and responsive web interface.

    AI-Powered: Utilizes the DeepSeek-67B model for question generation and answer validation.

    Scalable: Designed to be deployed as a website for widespread use.

Getting Started
Prerequisites

Before running the project, ensure you have the following installed:

    Python 3.8 or higher

    Streamlit (pip install streamlit)

    CAMEL framework (install from the CAMEL GitHub repository)

    An API key for the DeepSeek model (replace the placeholder key in the code with your own)

Installation

    Clone the repository:
    bash
    Copy

    git clone https://github.com/1sarthakbhardwaj/CAMEL-Deepseek-AIMLAPI.git
    cd CAMEL-Deepseek-AIMLAPI/SOCIETY_WITH_DEEPSEEK_RAG

    Install the required Python packages:
    bash
    Copy

    pip install -r requirements.txt

    Replace the placeholder API key in app.py with your own DeepSeek API key:
    python
    Copy

    aiml_api_key = "your_api_key_here"  # Replace with your actual API key

    Run the Streamlit application:
    bash
    Copy

    streamlit run app.py

    Open your browser and navigate to http://localhost:8501 to access the application.

How It Works

    Quiz Generation:

        The Teacher Agent (an AI model) generates a quiz with 5 questions, each in a different format.

        Questions are dynamically created based on predefined rules and math concepts.

    User Interaction:

        Users interact with the quiz through the Streamlit interface.

        They can answer questions, submit their responses, and receive immediate feedback.

    Answer Validation:

        The application checks user answers against the correct answers provided by the AI model.

        Feedback is displayed in real-time, indicating whether the answer is correct or incorrect.

    Result Display:

        After completing the quiz, users can view their results, including the number of correct answers and feedback for each question.

Project Structure
Copy

SOCIETY_WITH_DEEPSEEK_RAG/
├── app.py                  # Main application file
├── requirements.txt        # List of dependencies
├── README.md               # Project documentation
└── assets/                 # Folder for images or other assets (optional)

Future Enhancements

    Integration with Learning Platforms: Collaborate with established learning platforms to integrate the quiz generator into their ecosystems.

    Additional Question Types: Expand the range of question formats (e.g., matching, true/false).

    User Authentication: Add user accounts to track progress and performance over time.

    Gamification: Introduce gamified elements like badges and leaderboards to increase engagement.

Contributing

We welcome contributions to this project! If you'd like to contribute, please follow these steps:

    Fork the repository.

    Create a new branch for your feature or bugfix.

    Commit your changes and push them to your fork.

    Submit a pull request with a detailed description of your changes.

DEMO
https://drive.google.com/file/d/1kqQzwdhtsn3zOeRFiiIrqQfLEeGSvhbz/view?usp=sharing

This project is licensed under the MIT License. See the LICENSE file for details.
Acknowledgments

    CAMEL Framework: For providing the AI agent infrastructure.

    DeepSeek: For the powerful language model used in this project.

    Streamlit: For the intuitive web interface framework.

Contact

For questions or feedback, please reach out to:

    ELshafey Nadin: nadeinfarid@gmail.com

    SIMEAO Guilhem: GuilhemSimeao@gmail.com

    JOSEPH Remy: remy.josephpf@gmail.com

    GOUNOU Rajath: rajathgounou030@gmail.com

    BUI HUY Huang: canhchimcuajin@gmail.com
