// Funcție pentru a popula dropdown-ul cu pair-uri
function populatePairs() {
    fetch('http://127.0.0.1:5000/financial/available_pairs')
        .then(response => response.json())
        .then(data => {
            let select = document.getElementById('currency-pair');
            data.pairs.forEach(pair => {
                let option = document.createElement('option');
                option.value = pair;
                option.innerText = pair;
                select.appendChild(option);
            });
        });
}

// Funcție pentru a popula dropdown-ul cu timeframe-uri
function populateTimeframes(pair) {
    fetch(`http://127.0.0.1:5000/financial/available_timeframes/${pair}`)
        .then(response => response.json())
        .then(data => {
            let select = document.getElementById('time-frame');
            select.innerHTML = '';  // Golim conținutul existent
            data.forEach(timeframe => {
                let option = document.createElement('option');
                option.value = timeframe;
                option.innerText = timeframe;
                select.appendChild(option);
            });
        });
}

document.getElementById("analyze-btn").addEventListener("click", function() {
    const selected_pair = document.getElementById("currency-pair").value;
    const selected_timeframe = document.getElementById("time-frame").value;

    fetch(`/analyze?pair=${selected_pair}&timeframe=${selected_timeframe}`)
        .then(response => response.json())
        .then(data => {
            // Aici poți afișa rezultatele analizei în interfața grafică
        });
});

// Adaugă un event listener pentru schimbarea valorii dropdown-ului de pair-uri
document.getElementById('currency-pair').addEventListener('change', function() {
    populateTimeframes(this.value);
});

// Populează dropdown-ul cu pair-uri la încărcarea paginii
populatePairs();

function startAnalysis() {
    const selectedInstrument = document.getElementById("currency-pair").value;
    const selectedTimeframe = document.getElementById("time-frame").value;

    if (selectedInstrument && selectedTimeframe) {
        fetch("http://127.0.0.1:5000/get_analysis", {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                instrument: selectedInstrument,
                timeframe: selectedTimeframe
            })
        }).then(response => response.json()).then(data => {
            // Handle the response data here
            console.log(data);
        });
    }
}

function sendMessage() {
    const userInput = document.getElementById("user-input");
    const chatMessages = document.getElementById("chat-messages");

    // Display user's message
    const userMessage = document.createElement("div");
    userMessage.textContent = userInput.value;
    userMessage.style.textAlign = "right";
    userMessage.style.marginBottom = "10px";
    chatMessages.appendChild(userMessage);

    // Send message to backend
    fetch('http://127.0.0.1:5000/process_message', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ message: userInput.value })
    })
    .then(response => response.json())
    .then(data => {
        // Display response from the server
        const serverMessage = document.createElement("div");
        serverMessage.textContent = data.response;
        serverMessage.style.marginBottom = "10px";
        chatMessages.appendChild(serverMessage);
    });

    // Clear user input
    userInput.value = "";
}

function showAnalysis() {
    const currencyPair = document.getElementById("currency-pair").value;
    const timeFrame = document.getElementById("time-frame").value;

    fetch('http://127.0.0.1:5000/get_analysis', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            currency_pair: currencyPair,
            time_frame: timeFrame
        })
    })
    .then(response => response.json())
    .then(data => {
        const analysisMessage = document.createElement("div");
        analysisMessage.textContent = data.analysis;
        analysisMessage.style.marginBottom = "10px";
        chatMessages.appendChild(analysisMessage);
    });
}
