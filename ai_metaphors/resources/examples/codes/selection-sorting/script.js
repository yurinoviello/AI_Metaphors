let currentIteration = 0;
let currentStep = 0;
let lst = [4, 2, 3, 1];
let i = 1;
let j = 0;
let key = null;
let lstSnapshots = [];
let iSnapshots = [];
let jSnapshots = [];
let keySnapshots = [];

// Step explanations for insertion sort
const stepExplanations = [
    'Define the list <span class="variable">lst</span>', // Step 0
    'Enter outer loop: <span class="variable">i</span> = 1', // Step 1
    'Set <span class="variable">key</span> = lst[i]', // Step 2
    'Set <span class="variable">j</span> = i - 1', // Step 3
    'Compare lst[j] > key', // Step 4
    'Since lst[j] > key, move lst[j] to lst[j + 1]', // Step 5
    'Decrement <span class="variable">j</span>', // Step 6
    'Insert <span class="variable">key</span> at lst[j + 1]', // Step 7
    'Now lst is [2, 4, 3, 1]', // Step 8
    'Increment <span class="variable">i</span> to 2', // Step 9
    // Continue for the rest of the steps
];

// Simulate insertion sort and record snapshots
function simulateInsertionSort() {
    let arr = [4, 2, 3, 1];
    lstSnapshots.push([...arr]);
    iSnapshots.push(null);
    jSnapshots.push(null);
    keySnapshots.push(null);

    for (let ii = 1; ii < arr.length; ii++) {
        let k = arr[ii];
        let jj = ii - 1;

        lstSnapshots.push([...arr]);
        iSnapshots.push(ii);
        jSnapshots.push(null);
        keySnapshots.push(k);

        lstSnapshots.push([...arr]);
        iSnapshots.push(ii);
        jSnapshots.push(jj);
        keySnapshots.push(k);

        while (jj >= 0 && arr[jj] > k) {
            arr[jj + 1] = arr[jj];

            lstSnapshots.push([...arr]);
            iSnapshots.push(ii);
            jSnapshots.push(jj);
            keySnapshots.push(k);

            jj--;

            lstSnapshots.push([...arr]);
            iSnapshots.push(ii);
            jSnapshots.push(jj);
            keySnapshots.push(k);
        }

        arr[jj + 1] = k;

        lstSnapshots.push([...arr]);
        iSnapshots.push(ii);
        jSnapshots.push(jj);
        keySnapshots.push(k);
    }

    lstSnapshots.push([...arr]);
    iSnapshots.push(null);
    jSnapshots.push(null);
    keySnapshots.push(null);
}

simulateInsertionSort();

// Control functions
function incrementLoop() {
    if (currentIteration < lstSnapshots.length - 1) {
        currentIteration++;
        updateAll();
    } else {
        alert("Program has finished executing.");
    }
}

function decrementLoop() {
    if (currentIteration > 0) {
        currentIteration--;
        updateAll();
    } else {
        alert("Already at the start of the loop.");
    }
}

function resetLoop() {
    currentIteration = 0;
    updateAll();
}

function runAllIterations() {
    while (currentIteration < lstSnapshots.length - 1) {
        incrementLoop();
    }
}

function updateAll() {
    updateCodeHighlight();
    updateMemory();
    updateVisual();
    updateStepExplanation();
}

// Update code highlight
function updateCodeHighlight() {
    const lines = ["line1", "line2", "line3", "line4", "line5", "line6", "line7", "line8", "line9"];

    lines.forEach(line => {
        document.getElementById(line).classList.remove("highlight");
    });

    if (currentIteration === 0) {
        document.getElementById("line1").classList.add("highlight");
    } else if (iSnapshots[currentIteration] !== null && jSnapshots[currentIteration] === null) {
        document.getElementById("line2").classList.add("highlight");
    } else if (keySnapshots[currentIteration] !== null && jSnapshots[currentIteration] === null) {
        document.getElementById("line3").classList.add("highlight");
    } else if (jSnapshots[currentIteration] !== null) {
        document.getElementById("line4").classList.add("highlight");
    } else if (currentIteration > 0) {
        document.getElementById("line9").classList.add("highlight");
    }
}

// Update memory window
function updateMemory() {
    const lstValues = lstSnapshots[currentIteration];
    for (let idx = 0; idx < lstValues.length; idx++) {
        document.getElementById('val' + idx).innerText = lstValues[idx];
    }

    let iVal = iSnapshots[currentIteration];
    let jVal = jSnapshots[currentIteration];
    let keyVal = keySnapshots[currentIteration];

    document.getElementById('memory-i-value').innerText = iVal !== null ? iVal : '';
    document.getElementById('memory-j-value').innerText = jVal !== null ? jVal : '';
    document.getElementById('memory-key-value').innerText = keyVal !== null ? keyVal : '';
}

// Update visual representation
function updateVisual() {
    const lstValues = lstSnapshots[currentIteration];
    const blocks = ["block1", "block2", "block3", "block4"];

    for (let idx = 0; idx < lstValues.length; idx++) {
        const block = document.getElementById(blocks[idx]);
        block.src = `block${lstValues[idx]}.png`;
    }

    // Reset highlights
    blocks.forEach(blockId => {
        document.getElementById(blockId).style.backgroundColor = '';
        document.getElementById(blockId).style.border = '';
    });

    const pointers = ["pointer1", "pointer2", "pointer3", "pointer4"];
    pointers.forEach(pointerId => {
        document.getElementById(pointerId).style.visibility = 'hidden';
    });

    // Highlight current i and j positions
    let iVal = iSnapshots[currentIteration];
    let jVal = jSnapshots[currentIteration];

    if (iVal !== null) {
        document.getElementById(`block${iVal + 1}`).style.backgroundColor = 'yellow';
        document.getElementById(`block${iVal + 1}`).style.border = '3px solid #ff6a00';
        document.getElementById(`pointer${iVal + 1}`).style.visibility = 'visible';
    }

    if (jVal !== null && jVal >= 0) {
        document.getElementById(`block${jVal + 1}`).style.backgroundColor = 'lightgreen';
        document.getElementById(`block${jVal + 1}`).style.border = '3px solid green';
        document.getElementById(`pointer${jVal + 1}`).style.visibility = 'visible';
    }
}

// Update step explanation
function updateStepExplanation() {
    const explanationDiv = document.getElementById('step-explanation');
    explanationDiv.innerHTML = stepExplanations[currentIteration] || "Program has finished executing.";
}

window.onload = () => {
    updateAll();
};
