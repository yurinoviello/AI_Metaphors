let currentIteration = 0;
let maxIterations = 5;
let total = 0;
let lst = [2, 4, 6, 8];
let previousTotals = [];

const stepExplanations = [
    "Step 1: Initialize total to 0 and define the list lst",
    "Step 2: Start loop - add lst[0] to total.",
    "Step 3: Add lst[1] to total.",
    "Step 4: Add lst[2] to total",
    "Step 5: Add lst[3] to total",
    "Looping complete!"
];

function updateStepExplanation() {
    const stepExplanation = document.getElementById('step-explanation');
    stepExplanation.textContent = stepExplanations[currentIteration];
}

function incrementLoop() {
    if (currentIteration < maxIterations) {
        if (currentIteration > 0) {
            previousTotals.push(total);  // Save the current state
            total += lst[currentIteration - 1];  // Add the current value to total
        }
        currentIteration++;
        updateMemory();
        updateVisual();
        updateCodeHighlight();
        updateStepExplanation();
    } else {
        alert("Loop has completed all iterations.");
    }
}

function decrementLoop() {
    if (currentIteration > 0) {
        currentIteration--;
        if (currentIteration > 0) {
            total = previousTotals.pop();  // Restore the previous state
        } else {
            total = 0;
        }
        updateMemory();
        updateVisual();
        updateCodeHighlight();
        updateStepExplanation();
    } else {
        alert("You are at the beginning of the loop.");
    }
}

function resetLoop() {
    currentIteration = 0;
    total = 0;
    previousTotals = [];  // Reset the state history
    updateMemory();
    updateVisual();
    updateCodeHighlight();
    updateStepExplanation();
}

function runAllIterations() {
    while (currentIteration < maxIterations) {
        incrementLoop();
    }
}

function updateCodeHighlight() {
    const lines = ["line1", "line2", "line3", "line4"];
    lines.forEach(line => {
        document.getElementById(line).classList.remove("highlight");
        document.getElementById(line).querySelector('.iteration-values')?.remove();  // Remove previous iteration values if any
    });

    if (currentIteration === 0) {
        document.getElementById("line1").classList.add("highlight");
        document.getElementById("line2").classList.add("highlight");
    } 
    else if (currentIteration <= maxIterations) {        
        document.getElementById("line4").classList.add("highlight");
        document.getElementById("line4").insertAdjacentHTML('beforeend', `<span class="iteration-values" style="color: blue; font-size: small;"> i = ${currentIteration - 1}</span>`);
    
        document.getElementById("line3").classList.add("highlight");
        document.getElementById("line3").insertAdjacentHTML('beforeend', `<span class="iteration-values" style="color: blue; font-size: small;"> i = ${currentIteration - 1}</span>`);
    
    }
}

function updateMemory() {
    const memoryIValue = document.getElementById('memory-i-value');
    const memoryTotalValue = document.getElementById('memory-total-value');
    const memoryLstValue = document.getElementById('memory-lst-value');

    memoryIValue.textContent = currentIteration < maxIterations ? currentIteration - 1 : maxIterations - 1;
    memoryTotalValue.textContent = total;

    memoryLstValue.innerHTML = `
        <div class="nested-list">
            <div class="list-container">
                ${lst.map((value, index) => `
                    <div class="index-container">
                        <div class="list-index">[${index}]</div>
                        <div class="arrow-down"></div>
                        <div class="list-value">${value}</div>
                    </div>
                `).join('')}
            </div>
        </div>
    `;
}

function updateVisual() {
    const visualDiv = document.getElementById('visual');
    visualDiv.innerHTML = lst.map((value, index) => 
        `<div class="visual-box ${index === currentIteration - 1 ? 'highlight-box' : ''}">
            ${value}
            <span class="index-value">[${index}]</span>
            ${index === currentIteration - 1 ? '<div class="arrow"></div>' : ''}
        </div>`
    ).join("");

    // Add the total basket
    visualDiv.innerHTML += `
        <div class="basket-box">
            <div class="basket">
                <div class="basket-top"></div>
                <div class="basket-body">
                    Total: <span class="basket-value">${total}</span>
                </div>
            </div>
        </div>
    `;

    document.getElementById('iteration-info').textContent = `Iteration i = ${currentIteration < maxIterations ? currentIteration - 1 : maxIterations - 1}`;
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
                <li><button onclick="checkAnswer('C')">C) To increase the value of total</button></li>
            </ul>
        `;
    } else if (topic === 'increment') {
        questionDiv.innerHTML = `
            <p>What does the statement <code>total += lst[i]</code> do?</p>
            <ul>
                <li><button onclick="checkAnswer('A')">A) It sets the value of total to the value at lst[i]</button></li>
                <li><button onclick="checkAnswer('B')">B) It increases the value of total by the value at lst[i]</button></li>
                <li><button onclick="checkAnswer('C')">C) It decreases the value of total by the value at lst[i]</button></li>
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
    } else if (variable === 'total') {
        questionDiv.innerHTML = `<p>The variable <code>total</code> is used to keep track of the running total of the list elements.</p>`;
    } else if (variable === 'lst') {
        questionDiv.innerHTML = `<p>The variable <code>lst</code> is the 1D list of values being iterated over.</p>`;
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
    updateStepExplanation();
};
