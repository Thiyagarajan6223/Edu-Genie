// ============================================
// GET ELEMENTS
// ============================================

const typeOptions =
    document.querySelectorAll(".type-option");

const typeInputs =
    document.querySelectorAll(
        'input[name="type"]'
    );

const questionInput =
    document.getElementById("question");

const askButton =
    document.getElementById("askButton");

const result =
    document.getElementById("result");


// ============================================
// TYPE SELECTION
// ============================================

typeInputs.forEach(function(input) {

    input.addEventListener("change", function() {

        // Remove selected class
        typeOptions.forEach(function(option) {

            option.classList.remove("selected");

        });


        // Add selected class
        this.parentElement.classList.add(
            "selected"
        );


        // Change button
        updateButtonText(this.value);

    });

});


// ============================================
// BUTTON TEXT
// ============================================

function updateButtonText(type) {

    const buttonText = {

        question_ask:
            "Ask Question",

        learning_path:
            "Create Learning Path",

        quiz:
            "Generate Quiz",

        topic_explain:
            "Explain Topic",

        summarize:
            "Summarize"

    };


    askButton.innerText =
        buttonText[type] || "Ask";

}


// ============================================
// ASK BUTTON
// ============================================

askButton.addEventListener(
    "click",
    askEduGenie
);


// ============================================
// MAIN FUNCTION
// ============================================

async function askEduGenie() {

    const question =
        questionInput.value.trim();


    // Get selected type

    const selectedType =
        document.querySelector(
            'input[name="type"]:checked'
        );


    // Validate question

    if (!question) {

        result.innerText =
            "Please enter a question.";

        questionInput.focus();

        return;
    }


    // Validate type

    if (!selectedType) {

        result.innerText =
            "Please select a type.";

        return;
    }


    const type =
        selectedType.value;


    // Loading

    askButton.disabled = true;

    askButton.innerText =
        "Generating...";


    result.innerText =
        "EduGenie is thinking...";


    try {

        // ========================================
        // SEND DATA TO PYTHON
        // ========================================

        const response =
            await fetch("/ask", {

                method: "POST",

                headers: {

                    "Content-Type":
                        "application/json"

                },

                body: JSON.stringify({

                    question: question,

                    type: type

                })

            });


        // ========================================
        // READ RESPONSE
        // ========================================

        const data =
            await response.json();


        // Backend error

        if (!response.ok) {

            throw new Error(
                data.detail ||
                data.error ||
                "Something went wrong."
            );

        }


        // ========================================
        // DISPLAY ANSWER
        // ========================================

        result.innerText =
            data.answer;


    }

    catch (error) {

        console.error(error);

        result.innerText =
            "Error: " +
            error.message;

    }


    finally {

        askButton.disabled = false;

        updateButtonText(type);

    }

}

