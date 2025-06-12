const firebaseConfig = {
    apiKey: "AIzaSyAn_mT725rpxJdgdZ_HchR6FpAYs1sD6Zo",
    authDomain: "visual-interactions-csc108.firebaseapp.com",
    projectId: "visual-interactions-csc108",
    storageBucket: "visual-interactions-csc108.appspot.com",
    messagingSenderId: "703068795993",
    appId: "1:703068795993:web:2c734051b205606affad48",
    measurementId: "G-QWCWFNX1BR"
};


firebase.initializeApp(firebaseConfig);
const dbNew = firebase.firestore().collection('simple-sum');  // Using new collection


function logInteractionToSimpleSum(eventType, details) {
    dbNew.add({
        userId: userId,
        eventType: eventType,
        details: details,
        timestamp: firebase.firestore.FieldValue.serverTimestamp()
    }).then(() => {
        console.log("Interaction logged successfully!");
    }).catch((error) => {
        console.error("Error logging interaction: ", error);
    });
}

const userId = 'user-' + Date.now() + '-' + Math.floor(Math.random() * 10000);

let currentIteration = 0;
let maxIterations = 5;
let total = 0;
let lst = [2, 4, 6, 8];
let lst2 = [0, 2, 4, 6, 8];
let previousTotals = [];

// Step explanations
const stepExplanations = [
    'Initialize <span class="variable">total</span> to <span class="variable">0</span>',
    'Define the list <span class="variable">lst</span>',
    'Iteration 1: Start loop - add <span class="variable">lst[0]</span> to <span class="variable">total</span>',
    'Iteration 2: Add <span class="variable">lst[1]</span> to <span class="variable">total</span>',
    'Iteration 3: Add <span class="variable">lst[2]</span> to <span class="variable">total</span>',
    'Iteration 4: Add <span class="variable">lst[3]</span> to <span class="variable">total</span>',
    'Looping complete!'
];


// Update step explanation
function updateStepExplanation() {
    const stepExplanation = document.getElementById('step-explanation');
    stepExplanation.innerHTML = stepExplanations[currentIteration];
}

// Increment loop
function incrementLoop() {
    if (currentIteration < maxIterations) {
        if (currentIteration >= 0) {
            previousTotals.push(total);  // Save the current state
            if (currentIteration < 4) {
                total += lst2[currentIteration];  // Add the current value to total
            }
        }
        currentIteration++;
        updateMemory();
        updateVisual();
        updateCodeHighlight();
        updateStepExplanation();

        // Log the interaction
        logInteractionToSimpleSum('incrementLoop', { currentIteration: currentIteration, total: total });
    } else {
        alert("Loop has completed all iterations.");
        logInteractionToSimpleSum('alert', { message: "Loop has completed all iterations." });
    }
}

// Decrement loop
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

        // Log the interaction
        logInteractionToSimpleSum('decrementLoop', { currentIteration: currentIteration, total: total });
    } else {
        alert("You are at the beginning of the loop.");
        logInteractionToSimpleSum('alert', { message: "You are at the beginning of the loop." });
    }
}

// Reset loop
function resetLoop() {
    currentIteration = 0;
    total = 0;
    previousTotals = [];  // Reset the state history
    updateMemory();
    updateVisual();
    updateCodeHighlight();
    updateStepExplanation();

    // Log the interaction
    logInteractionToSimpleSum('resetLoop', { currentIteration: currentIteration, total: total });
}

// Run all iterations
function runAllIterations() {
    while (currentIteration < maxIterations) {
        incrementLoop();
    }

    // Log the interaction
    logInteractionToSimpleSum('runAllIterations', { finalIteration: currentIteration, finalTotal: total });
}


// Update code highlight
function updateCodeHighlight() {
    const lines = ["line1", "line2", "line3", "line4"];
    lines.forEach(line => {
        document.getElementById(line).classList.remove("highlight");
        document.getElementById(line).querySelector('.iteration-values')?.remove();  // Remove previous iteration values if any
    });

    if (currentIteration === 0) {
        document.getElementById("line1").classList.add("highlight");
    }
    else if (currentIteration === 1){
        document.getElementById("line2").classList.add("highlight");
    } 
    else if (currentIteration <= maxIterations) {        
        document.getElementById("line4").classList.add("highlight");
        document.getElementById("line3").classList.add("highlight");
    
    }
}

// Update memory
function updateMemory() {
    const memoryIValue = document.getElementById('memory-i-value');
    const memoryTotalValue = document.getElementById('memory-total-value');
    const memoryLstValue = document.getElementById('memory-lst-value');

    // Set iteration and total values
    memoryIValue.textContent = currentIteration < maxIterations ? currentIteration - 1 : maxIterations - 1;
    memoryTotalValue.textContent = total;


    if (currentIteration > 1) {
            // Update the list with index highlighting logic
        memoryLstValue.innerHTML = `
        <div class="nested-list">
            <div class="list-container">
                ${lst.map((value, index) => {
                    let indexClass = '';
                    let valueClass = '';

                    if (index === currentIteration - 2) {
                        // Current iteration index
                        indexClass = 'highlight-item-index';
                        valueClass = 'highlight-item';
                    } else if (index < currentIteration - 2) {
                        // Visited indices
                        indexClass = 'highlight-visited-index';
                        valueClass = 'highlight-visited';
                    }

                    return `
                        <div class="index-container">
                            <div class="list-index ${indexClass}">[${index}]</div>
                            <div class="arrow-down"></div>
                            <div class="list-value ${valueClass}">${value}</div>
                        </div>
                    `;
                }).join('')}
            </div>
        </div>
`;
    }

    else {
            // Update the list with index highlighting logic
            memoryLstValue.innerHTML = `
            <div class="nested-list">
                <div class="list-container">
                    ${lst.map((value, index) => {
                        indexClass = 'highlight-visited-index';
                        valueClass = 'highlight-visited';
    
                        return `
                            <div class="index-container">
                                <div class="list-index ${indexClass}">[${index}]</div>
                                <div class="arrow-down"></div>
                                <div class="list-value ${valueClass}">${value}</div>
                            </div>
                        `;
                    }).join('')}
                </div>
            </div>
    `;
    }

    console.log(currentIteration);
    if (currentIteration === 0){
        document.getElementById('memory-lst').classList.add('hidden')
        document.getElementById('variable-total').classList.add('variable-name-hl');
        document.getElementById('variable-total').classList.remove('variable-name');
        document.getElementById('memory-total-value').classList.add('variable-name-hl');
        document.getElementById('memory-total-value').classList.remove('memory-value');
    }
    else{
        document.getElementById('memory-total-value').classList.add('memory-value');
        document.getElementById('memory-total-value').classList.remove('variable-name-hl');
        document.getElementById('variable-total').classList.add('variable-name');
        document.getElementById('variable-total').classList.remove('variable-name-hl');
    }

    if (currentIteration > 1) {
        memoryIValue.textContent = currentIteration - 1;
        document.getElementById('memory-i').classList.remove('hidden');
        document.getElementById('variable-i').classList.add('variable-name-hl');
        document.getElementById('variable-i').classList.remove('variable-name');
        document.getElementById('memory-i-value').classList.add('variable-name-hl');
        document.getElementById('memory-i-value').classList.remove('memory-value');
        document.getElementById('variable-lst').classList.add('variable-name-hl');
        document.getElementById('variable-lst').classList.remove('variable-name');
    } 
    else if (currentIteration === 1){
        document.getElementById('memory-lst').classList.remove('hidden')
        document.getElementById('variable-lst').classList.remove('variable-name');
        document.getElementById('variable-lst').classList.add('variable-name-hl');
    }
    else {
        // Hide 'i' during step 0
        document.getElementById('memory-i').classList.add('hidden');
    }
}



// Update visual
function updateVisual() {
    const visualDiv = document.getElementById('visual');
    
    let vizcurrentIteration = currentIteration - 1;
    
    // List of images for the boxes, without the '-hl' part
    const images = ['./fruit1-bw.png', './fruit2-bw.png', './fruit3-bw.png', './fruit4-bw.png'];
    const highlightedImages = ['./fruit1-hl.png', './fruit2-hl.png', './fruit3-hl.png', './fruit4-hl.png'];

    // Use scanner-hl.png for all steps except step 0
    const scannerImage = vizcurrentIteration === 0 ? './scanner.png' : './scanner-hl.png';
    // Set text color based on the scanner image
    const textColor = vizcurrentIteration === 0 ? '#ffffff' : '#ff6a00';  // Default color or orange when scanner is highlighted

    // List of items on the conveyor belt
    const conveyorItems = lst.map((_, index) => {
        let boxClass = '';
        let indexClass = '';
        let imageSrc = images[index];  // Default to the non-highlighted image

        if (index === vizcurrentIteration - 1) {
            // Current index is highlighted
            indexClass = 'highlight-item-index';
            imageSrc = highlightedImages[index];  // Use the highlighted version of the image
        } else if (index < vizcurrentIteration - 1) {
            // Indices that have been visited disappear
            return '';  // Skip adding to the conveyor belt
        }

        return `
            <div class="box ${boxClass}">
                <img src="${imageSrc}" alt="Item ${index}" class="box-image">
                <div class="list-index ${indexClass}">${index}</div>
            </div>`;
    }).slice(0, 4).join(""); // Only show the first 4 items for the conveyor

    // Create the conveyor belt with the boxes and index numbers
    const conveyorBelt = `
    <div class="conveyor-belt-wrapper">
        <div class="total-box">
            <img src="${scannerImage}" alt="Price Screen" class="total-box-image">
            <div class="total-value" style="color: ${textColor};"> $ ${total}</div> <!-- Set the text color dynamically -->
        </div>
        <div class="conveyor-belt">
            ${conveyorItems}
        </div>
    </div>`;

    // Clear previous content and insert the new layout
    visualDiv.innerHTML = conveyorBelt;
}



// Function to update pencil position
function updatePencilPosition() {
    const pencilImage = document.getElementById('pencil-image');
    const listItems = document.querySelectorAll('.list-item');
    
    if (currentIteration > 0 && currentIteration <= listItems.length) {
        const targetItem = listItems[currentIteration - 1];
        const paperRect = document.querySelector('.lined-paper').getBoundingClientRect();
        const itemRect = targetItem.getBoundingClientRect();
        
        // Position the pencil to point to the current item
        pencilImage.style.top = (itemRect.top - paperRect.top + window.scrollY - pencilImage.clientHeight) + 'px';
        pencilImage.style.left = (itemRect.left - paperRect.left + window.scrollX - pencilImage.clientWidth / 2) + 'px';
    }
}

// Show question
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

// Show info
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

// Check answer
function checkAnswer(answer) {
    if (answer === 'B') {
        alert('Correct!');
    } else {
        alert('Try again.');
    }
}

// Hide interactive
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
