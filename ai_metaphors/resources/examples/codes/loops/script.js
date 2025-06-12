let currentIteration = 0;
let maxIterations = 10;
let star = 0;

function incrementLoop() {
    if (currentIteration < maxIterations - 1) {
        currentIteration++;
        updateCodeHighlight();
        updateMemory();
        updateVisual();
    } else {
        alert("Loop has completed all iterations.");
    }
}

function decrementLoop() {
    if (currentIteration > 0) {
        currentIteration--;
        updateCodeHighlight();
        updateMemory();
        updateVisual();
    } else {
        alert("You are at the beginning of the loop.");
    }
}

function resetLoop() {
    currentIteration = 0;
    star = 0;
    updateCodeHighlight();
    updateMemory();
    updateVisual();
}

function runAllIterations() {
    currentIteration = maxIterations - 1;
    star = currentIteration;
    updateCodeHighlight();
    updateMemory();
    updateVisual();
}

function updateRange() {
    const rangeInput = document.getElementById('range-input').value;
    document.getElementById('range-value').textContent = rangeInput;
    maxIterations = parseInt(rangeInput);
    resetLoop();
}

function updateCodeHighlight() {
    const lines = ["line1", "line2", "line3"];
    lines.forEach(line => {
        document.getElementById(line).classList.remove("highlight");
        document.getElementById(line).querySelector('.iteration-values')?.remove();  // Remove previous iteration values if any
    });

    if (currentIteration === 0) {
        document.getElementById("line1").classList.add("highlight");
    } else if (currentIteration <= maxIterations) {
        document.getElementById("line2").classList.add("highlight");
        document.getElementById("line2").insertAdjacentHTML('beforeend', `<span class="iteration-values" style="color: lightblue; font-size: small; margin-left: 10px;">i = ${currentIteration}</span>`);
        setTimeout(() => {
            document.getElementById("line3").classList.add("highlight");
            document.getElementById("line3").insertAdjacentHTML('beforeend', `<span class="iteration-values" style="color: lightblue; font-size: small; margin-left: 10px;">i = ${currentIteration}</span>`);
        }, 500);
    }
}


function updateMemory() {
    const memoryIValue = document.getElementById('memory-i-value');
    const memoryStarValue = document.getElementById('memory-star-value');

    memoryIValue.textContent = currentIteration;
    if (currentIteration === 0) {
        star = 0;
    } else if (currentIteration <= maxIterations) {
        star = currentIteration;
    }
    memoryStarValue.textContent = star;
}

function updateVisual() {
    const starsDiv = document.getElementById('stars');
    starsDiv.innerHTML = '★'.repeat(star - 1) + '<span style="color: red;">★</span>';
    document.getElementById('iteration-info').textContent = `Iteration i = ${currentIteration}`;
}

function showQuestion(topic) {
    const interactiveElement = document.getElementById('interactive-element');
    const questionDiv = document.getElementById('question');
    interactiveElement.classList.remove('hidden');

    if (topic === 'range') {
        questionDiv.innerHTML = `
            <p>What is the purpose of the range function in the loop?</p>
            <ul>
                <li><button onclick="checkAnswer('A')">A) To set the starting value of i</button></li>
                <li><button onclick="checkAnswer('B')">B) To determine the number of iterations</button></li>
                <li><button onclick="checkAnswer('C')">C) To increase the value of star</button></li>
            </ul>
        `;
    } else if (topic === 'increment') {
        questionDiv.innerHTML = `
            <p>What does the statement <code>star += 1</code> do?</p>
            <ul>
                <li><button onclick="checkAnswer('A')">A) It sets the value of star to 1</button></li>
                <li><button onclick="checkAnswer('B')">B) It increases the value of star by 1</button></li>
                <li><button onclick="checkAnswer('C')">C) It decreases the value of star by 1</button></li>
            </ul>
        `;
    }
}

function showInfo(variable) {
    const interactiveElement = document.getElementById('interactive-element');
    const questionDiv = document.getElementById('question');
    interactiveElement.classList.remove('hidden');

    if (variable === 'i') {
        questionDiv.innerHTML = `<p>The variable <code>i</code> is used as the loop counter.</p>`;
    } else if (variable === 'star') {
        questionDiv.innerHTML = `<p>The variable <code>star</code> is used to count the number of iterations completed.</p>`;
    }
}

function checkAnswer(answer) {
    if (answer === 'B') {
        alert('Correct!');
    } else {
        alert('Try again.');
    }
}

function hideInteractive() {
    const interactiveElement = document.getElementById('interactive-element');
    interactiveElement.classList.add('hidden');
}

window.onload = () => {
    updateCodeHighlight();
    updateMemory();
    updateVisual();
};
