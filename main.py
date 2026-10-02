import json
import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from openai import OpenAI


# ============================================================
# CONFIGURATION AZURE OPENAI
# ============================================================

load_dotenv()

AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT")

if not AZURE_OPENAI_ENDPOINT:
    raise RuntimeError("AZURE_OPENAI_ENDPOINT is missing from .env")

if not AZURE_OPENAI_API_KEY:
    raise RuntimeError("AZURE_OPENAI_API_KEY is missing from .env")

if not AZURE_OPENAI_DEPLOYMENT:
    raise RuntimeError("AZURE_OPENAI_DEPLOYMENT is missing from .env")


client = OpenAI(
    api_key=AZURE_OPENAI_API_KEY,
    base_url=f"{AZURE_OPENAI_ENDPOINT.rstrip('/')}/openai/v1/"
)


# ============================================================
# FASTAPI
# ============================================================

app = FastAPI(
    title="IT Quiz Generator",
    description="Generate IT quizzes using Azure OpenAI GPT-5 mini",
    version="1.0.0"
)


# ============================================================
# PAGE WEB
# ============================================================

@app.get("/", response_class=HTMLResponse)
def home():

    return """
<!DOCTYPE html>

<html lang="en">

<head>

    <meta charset="UTF-8">

    <meta name="viewport"
          content="width=device-width, initial-scale=1.0">

    <title>IT Quiz Generator</title>


    <style>

        * {
            box-sizing: border-box;
        }


        body {

            margin: 0;

            font-family: Arial, sans-serif;

            background: #f4f7fb;

            color: #1f2937;
        }


        .container {

            max-width: 900px;

            margin: 50px auto;

            padding: 30px;

            background: white;

            border-radius: 12px;

            box-shadow:
                0 4px 20px
                rgba(0, 0, 0, 0.08);
        }


        h1 {

            text-align: center;

            margin-bottom: 30px;
        }


        label {

            display: block;

            margin-top: 20px;

            margin-bottom: 8px;

            font-weight: bold;
        }


        input[type="text"],
        input[type="number"] {

            width: 100%;

            padding: 12px;

            border: 1px solid #d1d5db;

            border-radius: 8px;

            font-size: 16px;
        }


        button {

            width: 100%;

            margin-top: 25px;

            padding: 13px;

            border: none;

            border-radius: 8px;

            background: #2563eb;

            color: white;

            font-size: 16px;

            cursor: pointer;
        }


        button:hover {

            background: #1d4ed8;
        }


        button:disabled {

            background: #9ca3af;

            cursor: not-allowed;
        }


        #loading {

            display: none;

            text-align: center;

            margin-top: 20px;

            font-weight: bold;
        }


        #error {

            display: none;

            margin-top: 20px;

            padding: 15px;

            border-radius: 8px;

            background: #fee2e2;

            color: #991b1b;
        }


        #quiz {

            margin-top: 30px;
        }


        .question {

            margin-bottom: 25px;

            padding: 20px;

            border: 1px solid #e5e7eb;

            border-radius: 10px;

            background: #f9fafb;
        }


        .question h3 {

            margin-top: 0;

            line-height: 1.5;
        }


        .option {

            display: block;

            margin: 10px 0;

            padding: 12px;

            border-radius: 8px;

            border: 1px solid transparent;

            cursor: pointer;

            background: white;
        }


        .option:hover {

            background: #eef2ff;

            border-color: #c7d2fe;
        }


        .option input {

            width: auto;

            margin-right: 8px;

            cursor: pointer;
        }


        .correction {

            display: none;

            margin-top: 18px;

            padding: 15px;

            border-radius: 8px;

            background: #f3f4f6;

            border-left: 5px solid #6b7280;
        }


        .correct {

            color: #166534;

            font-weight: bold;
        }


        .incorrect {

            color: #991b1b;

            font-weight: bold;
        }


        .result {

            margin-bottom: 25px;

            padding: 20px;

            text-align: center;

            border-radius: 10px;

            background: #eff6ff;

            border: 1px solid #bfdbfe;
        }


        .result h2 {

            margin-top: 0;

            color: #1d4ed8;
        }


        .score {

            font-size: 28px;

            font-weight: bold;

            margin: 10px 0;
        }


        .submit-container {

            margin-top: 30px;
        }


        .submit-button {

            background: #16a34a;
        }


        .submit-button:hover {

            background: #15803d;
        }

    </style>

</head>


<body>


<div class="container">


    <h1>
        IT Quiz Generator
    </h1>


    <!-- ==================================================
         FORMULAIRE
         ================================================== -->


    <label for="topic">
        Enter IT Topic
    </label>


    <input
        type="text"
        id="topic"
        placeholder="Example: Docker"
    >


    <label for="number">
        Number of Questions
    </label>


    <input
        type="number"
        id="number"
        min="1"
        max="10"
        value="5"
    >


    <button
        id="generateButton"
        onclick="generateQuiz()"
    >
        Generate Quiz
    </button>


    <div id="loading">

        Generating quiz with GPT-5 mini...

    </div>


    <div id="error"></div>


    <!-- ==================================================
         QUIZ
         ================================================== -->


    <div id="quiz"></div>


</div>


<script>


// ============================================================
// VARIABLES
// ============================================================

let currentQuiz = null;


// ============================================================
// GENERATE QUIZ
// ============================================================

async function generateQuiz() {


    const topic =
        document
            .getElementById("topic")
            .value
            .trim();


    const number =
        parseInt(
            document
                .getElementById("number")
                .value
        );


    const loading =
        document.getElementById("loading");


    const quiz =
        document.getElementById("quiz");


    const error =
        document.getElementById("error");


    const generateButton =
        document.getElementById(
            "generateButton"
        );


    // Reset
    error.style.display = "none";

    error.textContent = "";

    quiz.innerHTML = "";


    // Validate topic

    if (!topic) {

        alert(
            "Please enter an IT topic."
        );

        return;
    }


    // Validate number

    if (
        isNaN(number) ||
        number < 1 ||
        number > 10
    ) {

        alert(
            "Number of questions must be between 1 and 10."
        );

        return;
    }


    loading.style.display = "block";

    generateButton.disabled = true;


    try {


        const response =
            await fetch(
                "/generate-quiz",
                {

                    method: "POST",

                    headers: {

                        "Content-Type":
                            "application/json"

                    },

                    body: JSON.stringify({

                        topic: topic,

                        number: number

                    })

                }
            );


        const data =
            await response.json();


        if (!response.ok) {

            throw new Error(
                data.detail ||
                "An error occurred."
            );
        }


        currentQuiz = data;


        displayQuiz(data);


    }

    catch (err) {


        error.textContent =
            err.message;


        error.style.display =
            "block";

    }

    finally {


        loading.style.display =
            "none";


        generateButton.disabled =
            false;

    }

}


// ============================================================
// DISPLAY QUIZ
// ============================================================

function displayQuiz(data) {


    const quiz =
        document.getElementById(
            "quiz"
        );


    quiz.innerHTML = "";


    // Display every question

    data.questions.forEach(
        (item, index) => {


            const questionDiv =
                document.createElement(
                    "div"
                );


            questionDiv.className =
                "question";


            // Question title

            const title =
                document.createElement(
                    "h3"
                );


            title.textContent =
                `${index + 1}. ${item.question}`;


            questionDiv.appendChild(
                title
            );


            // Options

            item.options.forEach(
                (option, optionIndex) => {


                    const optionLabel =
                        document.createElement(
                            "label"
                        );


                    optionLabel.className =
                        "option";


                    const radio =
                        document.createElement(
                            "input"
                        );


                    radio.type =
                        "radio";


                    radio.name =
                        `question-${index}`;


                    radio.value =
                        option;


                    optionLabel.appendChild(
                        radio
                    );


                    const optionText =
                        document.createTextNode(
                            ` ${String.fromCharCode(65 + optionIndex)}. ${option}`
                        );


                    optionLabel.appendChild(
                        optionText
                    );


                    questionDiv.appendChild(
                        optionLabel
                    );

                }
            );


            // Correction hidden

            const correction =
                document.createElement(
                    "div"
                );


            correction.className =
                "correction";


            correction.id =
                `correction-${index}`;


            questionDiv.appendChild(
                correction
            );


            quiz.appendChild(
                questionDiv
            );

        }
    );


    // Submit button

    const submitContainer =
        document.createElement(
            "div"
        );


    submitContainer.className =
        "submit-container";


    const submitButton =
        document.createElement(
            "button"
        );


    submitButton.className =
        "submit-button";


    submitButton.textContent =
        "Valider le quiz";


    submitButton.onclick =
        validateQuiz;


    submitContainer.appendChild(
        submitButton
    );


    quiz.appendChild(
        submitContainer
    );

}


// ============================================================
// VALIDATE QUIZ
// ============================================================

function validateQuiz() {


    if (!currentQuiz) {

        return;
    }


    const questions =
        document.querySelectorAll(
            ".question"
        );


    let score = 0;

    let answered = 0;


    // Check every question

    questions.forEach(
        (question, index) => {


            const selected =
                question.querySelector(
                    `input[name="question-${index}"]:checked`
                );


            const correction =
                document.getElementById(
                    `correction-${index}`
                );


            const quizQuestion =
                currentQuiz.questions[index];


            const correctAnswer =
                quizQuestion.correct_answer;


            const explanation =
                quizQuestion.explanation;


            // No answer

            if (!selected) {


                correction.innerHTML = `

                    <p class="incorrect">
                        🔴 Aucune réponse sélectionnée.
                    </p>

                    <p>
                        <strong>
                            Bonne réponse :
                        </strong>

                        ${escapeHtml(correctAnswer)}
                    </p>

                    <p>
                        <strong>
                            Explication :
                        </strong>

                        ${escapeHtml(explanation)}
                    </p>

                `;

            }


            // Answer exists

            else {


                answered++;


                if (
                    selected.value ===
                    correctAnswer
                ) {


                    score++;


                    correction.innerHTML = `

                        <p class="correct">
                            🟢 Correct !
                        </p>

                        <p>
                            <strong>
                                Votre réponse :
                            </strong>

                            ${escapeHtml(selected.value)}
                        </p>

                        <p>
                            <strong>
                                Explication :
                            </strong>

                            ${escapeHtml(explanation)}
                        </p>

                    `;

                }


                else {


                    correction.innerHTML = `

                        <p class="incorrect">
                            🔴 Incorrect !
                        </p>

                        <p>
                            <strong>
                                Votre réponse :
                            </strong>

                            ${escapeHtml(selected.value)}
                        </p>

                        <p>
                            <strong>
                                Bonne réponse :
                            </strong>

                            ${escapeHtml(correctAnswer)}
                        </p>

                        <p>
                            <strong>
                                Explication :
                            </strong>

                            ${escapeHtml(explanation)}
                        </p>

                    `;

                }

            }


            correction.style.display =
                "block";


            // Disable answers

            const inputs =
                question.querySelectorAll(
                    "input"
                );


            inputs.forEach(
                input => {

                    input.disabled =
                        true;

                }
            );

        }
    );


    // ========================================================
    // SCORE
    // ========================================================

    const total =
        currentQuiz.questions.length;


    const percentage =
        Math.round(
            (score / total) * 100
        );


    const result =
        document.createElement(
            "div"
        );


    result.className =
        "result";


    result.innerHTML = `

        <h2>
            Résultat du quiz
        </h2>

        <div class="score">
            ${score} / ${total}
        </div>

        <p>
            Score : <strong>${percentage}%</strong>
        </p>

        <p>
            Questions répondues :
            <strong>
                ${answered} / ${total}
            </strong>
        </p>

    `;


    // Put result at beginning

    const quiz =
        document.getElementById(
            "quiz"
        );


    quiz.prepend(result);


    // Disable validation button

    const submitButton =
        document.querySelector(
            ".submit-button"
        );


    if (submitButton) {

        submitButton.disabled =
            true;

        submitButton.textContent =
            "Quiz corrigé";

    }

}


// ============================================================
// SECURITY
// ============================================================

function escapeHtml(text) {


    const div =
        document.createElement(
            "div"
        );


    div.textContent =
        text;


    return div.innerHTML;

}

</script>


</body>

</html>
"""


# ============================================================
# GENERATE QUIZ API
# ============================================================

@app.post("/generate-quiz")
def generate_quiz(data: dict):


    topic = str(
            data.get(
                "topic",
                ""
            )
        ).strip()


    number = data.get(
            "number"
        )


    # --------------------------------------------------------
    # Validation topic
    # --------------------------------------------------------

    if not topic:

        return JSONResponse(
            status_code=400,
            content={
                "detail":
                    "Topic is required."
            }
        )


    # --------------------------------------------------------
    # Validation number
    # --------------------------------------------------------

    try:

        number = int(number)

    except (
        TypeError,
        ValueError
    ):

        return JSONResponse(
            status_code=400,
            content={
                "detail":
                    "Number must be an integer."
            }
        )


    if number < 1 or number > 10:

        return JSONResponse(
            status_code=400,
            content={
                "detail":
                    "Number of questions must be between 1 and 10."
            }
        )


    # --------------------------------------------------------
    # PROMPT GPT-5 MINI
    # --------------------------------------------------------

    prompt = f"""

You are an expert IT teacher.

Generate exactly {number} multiple-choice questions
about the following IT topic:

{topic}

The quiz is for IT students.

Requirements:

1. Generate exactly {number} questions.

2. Each question must have exactly 4 options.

3. Only ONE option must be correct.

4. Questions must be clear and unambiguous.

5. Questions must test real IT knowledge.

6. Avoid duplicate questions.

7. Each question must have a short explanation.

8. The correct answer must be exactly one
of the four options.

9. Return ONLY valid JSON.

10. Do NOT return Markdown.

11. Do NOT add text before or after the JSON.

Use exactly this JSON structure:

{{
    "topic": "{topic}",
    "questions": [
        {{
            "question": "Question text",
            "options": [
                "Option A",
                "Option B",
                "Option C",
                "Option D"
            ],
            "correct_answer": "Correct option",
            "explanation": "Short explanation"
        }}
    ]
}}

"""


    # --------------------------------------------------------
    # CALL AZURE OPENAI
    # --------------------------------------------------------

    try:


        response = client.responses.create(

                model=
                    AZURE_OPENAI_DEPLOYMENT,

                input=prompt,

                max_output_tokens=3000

            )


        result_text = response.output_text.strip()


        # Remove possible Markdown fences

        if result_text.startswith(
            "```"
        ):

            result_text = result_text.replace(
                    "```json",
                    ""
                ).replace(
                    "```",
                    ""
                ).strip()


        quiz = json.loads(
                result_text
            )


        # ----------------------------------------------------
        # Basic validation
        # ----------------------------------------------------

        if "questions" not in quiz:

            raise ValueError(
                "The AI response does not contain questions."
            )


        if len(
            quiz["questions"]
        ) != number:

            raise ValueError(
                "The AI did not generate the requested number of questions."
            )


        for question in quiz["questions"]:


            if len(
                question["options"]
            ) != 4:

                raise ValueError(
                    "Every question must contain exactly 4 options."
                )


            if (
                question["correct_answer"]
                not in question["options"]
            ):

                raise ValueError(
                    "The correct answer must be one of the options."
                )


        return quiz


    # --------------------------------------------------------
    # JSON ERROR
    # --------------------------------------------------------

    except json.JSONDecodeError:

        return JSONResponse(

            status_code=500,

            content={
                "detail":
                    "GPT-5 mini returned invalid JSON."
            }

        )


    # --------------------------------------------------------
    # OTHER ERROR
    # --------------------------------------------------------

    except Exception as e:

        return JSONResponse(

            status_code=500,

            content={
                "detail":
                    f"Azure OpenAI error: {str(e)}"
            }

        )