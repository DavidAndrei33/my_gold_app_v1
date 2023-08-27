document.getElementById("yourButtonID").addEventListener("click", function() {
    const selectedInstrument = document.getElementById("pairs_select").value;
    const selectedGranularity = document.getElementById("timeframes_select").value;
    // Adaugă și datele de început și de sfârșit dacă este necesar
const pairsDropdown = document.getElementById('pairs-dropdown');
const timeframesDropdown = document.getElementById('timeframes-dropdown');

// Fetch available pairs
fetch('http://127.0.0.1:5000/financial/available_pairs')
    .then(response => response.json())
    .then(data => {
        let pairDropdown = document.getElementById("pair");
        data.pairs.forEach(pair => {
            let option = document.createElement("option");
            option.text = pair;
            option.value = pair;
            pairDropdown.add(option);
        });
    })
    .catch(error => {
        console.error('Error fetching pairs:', error);
    });


// Adăugați un ascultător de evenimente pentru a actualiza timeframe-urile atunci când se schimbă perechea
pairsDropdown.addEventListener('change', function() {
    const selectedPair = this.value;
    fetch(`http://127.0.0.1:5000/financial/available_timeframes/${selectedPair}`)
        .then(response => response.json())
        .then(data => {
            // Golim dropdown-ul existent
            timeframesDropdown.innerHTML = '';
            data.forEach(timeframe => {
                const option = document.createElement('option');
                option.value = timeframe;
                option.textContent = timeframe;
                timeframesDropdown.appendChild(option);
            });
        });
});

// Restul codului dvs. chat.js aici...
function analyzeData() {
    let selectedInstrument = document.getElementById("instrumentSelect").value;
    let selectedTimeframe = document.getElementById("timeframeSelect").value;

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

    // TODO: Here you should send a request to the server with the selected values 
    // and get the analysis results to display in the chat or another suitable area.

    // Example:
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
        // Display analysis data (this is just an example, modify as needed)
        const analysisMessage = document.createElement("div");
        analysisMessage.textContent = data.analysis;
        analysisMessage.style.marginBottom = "10px";
        chatMessages.appendChild(analysisMessage);
    });
}
function loadAvailablePairs() {
    fetch('http://127.0.0.1:5000/financial/available_pairs')
    .then(response => response.json())
    .then(data => {
        const selectElement = document.getElementById("currency-pair");
        data.pairs.forEach(pair => {
            const option = document.createElement("option");
            option.value = pair;
            option.textContent = pair;
            selectElement.appendChild(option);
        });
    });
}
// Funcție pentru a popula dropdown-ul cu pair-uri
function populatePairs() {
    fetch('http://127.0.0.1:5000/financial/available_pairs')
        .then(response => response.json())
        .then(data => {
            let select = document.getElementById('pairSelect');
            data.forEach(pair => {
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
            let select = document.getElementById('timeframeSelect');
            select.innerHTML = '';  // Golim conținutul existent
            data.forEach(timeframe => {
                let option = document.createElement('option');
                option.value = timeframe;
                option.innerText = timeframe;
                select.appendChild(option);
            });
        });
}

// Adaugă un event listener pentru schimbarea valorii dropdown-ului de pair-uri
document.getElementById('pairs_select').addEventListener('change', function()
    {
    populateTimeframes(this.value);
});

// Populează dropdown-ul cu pair-uri la încărcarea paginii
populatePairs();

// Apelați funcția la încărcarea paginii
window.onload = loadAvailablePairs;
