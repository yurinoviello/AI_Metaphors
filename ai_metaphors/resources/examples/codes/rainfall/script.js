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
const dbNew = firebase.firestore().collection('rainfall');  // Using new collection

// Reuse logInteraction to log interactions to the "conditions" collection
function logInteractionToRainfall(eventType, details) {
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
let maxIterations = 9;
let total = 0;
let lst = [
    [20, 12, 1, 5],
    [25, 10, 7],
    [9, 30]
];
let previousTotals = [];

let lst1 = [20, 12, 1, 5];
let lst2 = [25, 10, 7];
let lst3 = [9, 30];

let lsta1 = ["Lego &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; $20", "Trucks &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; $12", "Video Game &nbsp;&nbsp; $1", "Puzzle &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; $5"];
let lsta2 = ["Hot Wheels &nbsp;&nbsp;&nbsp;$25", "Sketch Book &nbsp;  $10", "Trade Cards&nbsp;&nbsp;&nbsp; $7"];
let lsta3 = ["Basket Ball &nbsp;&nbsp;&nbsp;&nbsp; $9", "Markers &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;$30"];

let visitedIndices = {
    0: new Set(), // For lst1
    1: new Set(), // For lst2
    2: new Set()  // For lst3
};



function incrementLoop() {
    if (currentIteration < maxIterations) {
        previousTotals.push(total);  // Save the current state
        let row = 0;
        let col = 0;
        if (0 <= currentIteration && currentIteration <= 3) {
            // First list
            row = 0;
            col = currentIteration % 4;
            total += lst[row][col];
        } else if (4 <= currentIteration && currentIteration <= 6) {
            // Second list
            row = 1;
            col = currentIteration - 4;
            total += lst[row][col];
        } else if (7 <= currentIteration && currentIteration <= 8) {
            // Third list
            row = 2;
            col = currentIteration - 7;
            total += lst[row][col];
        }

        currentIteration++;

        // Log interaction
        logInteractionToRainfall('incrementLoop', { currentIteration: currentIteration, total: total, row: row, col: col });

        // Call your update functions
        updateCodeHighlight();
        updateMemory();
        updateVisual();
    } else {
        alert("Loop has completed all iterations.");
        logInteractionToRainfall('alert', { message: "Loop has completed all iterations." });
    }
}

// Decrement loop
function decrementLoop() {
    if (currentIteration > 0) {
        let row = 0;
        let col = 0;
        if (0 <= currentIteration - 1 && currentIteration - 1 <= 3) {
            // First list
            row = 0;
            col = currentIteration - 1;
            visitedIndices[row].delete(col);
        } else if (4 <= currentIteration - 1 && currentIteration - 1 <= 6) {
            // Second list
            row = 1;
            col = currentIteration - 5;
            visitedIndices[row].delete(col);
        } else if (7 <= currentIteration - 1 && currentIteration - 1 <= 8) {
            // Third list
            row = 2;
            col = currentIteration - 8;
            visitedIndices[row].delete(col);
        }

        currentIteration--;
        total = previousTotals.pop();  // Restore the previous state

        // Log interaction
        logInteractionToRainfall('decrementLoop', { currentIteration: currentIteration, total: total, row: row, col: col });

        updateCodeHighlight();
        updateMemory();
        updateVisual();
    } else {
        alert("You are at the beginning of the loop.");
        logInteractionToRainfall('alert', { message: "You are at the beginning of the loop." });
    }
}

// Reset loop
function resetLoop() {
    currentIteration = 0;
    total = 0;
    previousTotals = [];  // Reset the state history
    visitedIndices = {
        0: new Set(),
        1: new Set(),
        2: new Set()
    };

    document.getElementById('paper1').style.backgroundImage = "url('cb.png')";
    document.getElementById('paper2').style.backgroundImage = "url('cb.png')";
    document.getElementById('paper3').style.backgroundImage = "url('cb.png')";

    // Log interaction
    logInteractionToRainfall('resetLoop', { currentIteration: currentIteration, total: total });

    updateCodeHighlight();
    updateMemory();
    document.getElementById('memory-total-value').style.backgroundColor = '#e8e8e8';
    document.getElementById('memory-total-value').style.border = '1px solid #000000';
    updateVisual();
}

// Run all iterations
function runAllIterations() {
    while (currentIteration < maxIterations) {
        incrementLoop();
    }

    // Log interaction
    logInteractionToRainfall('runAllIterations', { finalIteration: currentIteration, finalTotal: total });

    updateCodeHighlight();
    updateMemory();
    updateVisual();
}

function updateCodeHighlight() {
    const lines = ["line1", "line2", "line3", "line4", "line5"];
    lines.forEach(line => {
        document.getElementById(line).classList.remove("highlight");
        document.getElementById(line).querySelector('.iteration-values')?.remove();  // Remove previous iteration values if any
    });

    if (currentIteration === 0) {
        document.getElementById("line1").classList.add("highlight");
    } else if (currentIteration <= maxIterations) {
        const step = currentIteration % 2;
        if (step === 0) {
            document.getElementById("line5").classList.add("highlight");
        } else {
            document.getElementById("line5").classList.add("highlight");
        }
    }
}



function updateMemory() {
    const memoryIValue = document.getElementById('memory-i-value');
    const memoryTotalValue = document.getElementById('memory-total-value');
    const memoryJValue = document.getElementById('memory-j-value');
    const memoryLstValue = document.getElementById('memory-lst-value');

    // const var1 = document.getElementById('var1');
    // const var2 = document.getElementById('var2');
    // const var3 = document.getElementById('var3');
    // const var4 = document.getElementById('var4');

    

    if (currentIteration !== 0) {
        memoryTotalValue.style.backgroundColor = 'yellow';
        memoryTotalValue.style.border = '3px solid #ff6a00';
        // memoryIValue.style.backgroundColor = 'yellow';
        // memoryIValue.style.border = '3px solid #ff6a00';
        // memoryLstValue.style.backgroundColor = 'yellow';
        // memoryLstValue.style.border = '3px solid #ff6a00';
        // memoryJValue.style.backgroundColor = 'yellow';
        // memoryJValue.style.border = '3px solid #ff6a00';
        // var1.style.backgroundColor = 'yellow';
        // var2.style.backgroundColor = 'yellow';
        // var3.style.backgroundColor = 'yellow';
        // var4.style.backgroundColor = 'yellow';
        // var1.style.border = '3px solid #ff6a00';
        // var2.style.border = '3px solid #ff6a00';
        // var3.style.border = '3px solid #ff6a00';
        // var4.style.border = '3px solid #ff6a00';
        
         
    } 

   

    let row = Math.floor((currentIteration - 1) / 4);
    let col = (currentIteration - 1) % 4;

    
    memoryTotalValue.textContent = total;
    
    const flatIndex = currentIteration - 1;
    if (0 <= flatIndex && flatIndex <= 3) {
        // First list
        row = 0;
        col = currentIteration - 1;
    } else if (4 <= flatIndex && flatIndex <= 6) {
        row = 1;
        col = currentIteration - 5;
    } else if (7 <= flatIndex && flatIndex <= 8) {
        row = 2;
        col = currentIteration - 8;
    }

    memoryIValue.textContent = row;
    memoryJValue.textContent = col;

    // Update visited indices
    if (row === 0) {
        visitedIndices[0].add(col);
    } else if (row === 1) {
        visitedIndices[1].add(col);
    } else if (row === 2) {
        visitedIndices[2].add(col);
    }

    memoryLstValue.innerHTML = `
    <div class="nested-lists-container">
        <div class="nested-list">
            <div class="variable-name ${row === 0 ? 'variable-name-highlight' : ''}">lst0</div>
            <div class="arrow-pointer"></div>
            <div class="list-container">
                ${lst1.map((value, index) => {
                    let indexClass = '';
                    let valueClass = '';

                    if (row === 0 && index === col) {
                        indexClass = 'highlight-item-index';
                        valueClass = 'highlight-item';
                    } else if (visitedIndices[0].has(index)) {
                        indexClass = 'highlight-visited-index';
                        valueClass = 'highlight-visited';
                    }

                    return `
                        <div class="index-container">
                            <div class="list-index ${indexClass}">${index}</div>
                            <div class="list-value ${valueClass}">${value}</div>
                        </div>`;
                }).join('')}
            </div>
        </div>
        <div class="nested-list">
            <div class="variable-name ${row === 1 ? 'variable-name-highlight' : ''}">lst1</div>
            <div class="arrow-pointer"></div>
            <div class="list-container">
                ${lst2.map((value, index) => {
                    let indexClass = '';
                    let valueClass = '';

                    if (row === 1 && index === col) {
                        indexClass = 'highlight-index';
                        valueClass = 'highlight-item';
                    } else if (visitedIndices[1].has(index)) {
                        indexClass = 'highlight-visited-index';
                        valueClass = 'highlight-visited';
                    }

                    return `
                        <div class="index-container">
                            <div class="list-index ${indexClass}">${index}</div>
                            <div class="list-value ${valueClass}">${value}</div>
                        </div>`;
                }).join('')}
            </div>
        </div>
        <div class="nested-list">
            <div class="variable-name ${row === 2 ? 'variable-name-highlight' : ''}">lst2</div>
            <div class="arrow-pointer"></div>
            <div class="list-container">
                ${lst3.map((value, index) => {
                    let indexClass = '';
                    let valueClass = '';

                    if (row === 2 && index === col) {
                        indexClass = 'highlight-index';
                        valueClass = 'highlight-item';
                    } else if (visitedIndices[2].has(index)) {
                        indexClass = 'highlight-visited-index';
                        valueClass = 'highlight-visited';
                    }

                    return `
                        <div class="index-container">
                            <div class="list-index ${indexClass}">${index}</div>
                            <div class="list-value ${valueClass}">${value}</div>
                        </div>`;
                }).join('')}
            </div>
        </div>
    </div>
    `;
}




function updateVisual() {
    const visualDiv = document.getElementById('visual');
    const paperDivs = [
        document.getElementById('paper1'),
        document.getElementById('paper2'),
        document.getElementById('paper3')
    ];

    
    const lists = [lsta1, lsta2, lsta3];
    const titles = ["[0]'s Wishlist", "[1]'s Wishlist", "[2]'s Wishlist"]
    const maxListLength = Math.max(lst1.length, lst2.length, lst3.length);
    const totalImage = currentIteration === 0 ? "total-box1" : "total-box2";
    const totalValue = currentIteration === 0 ? "total-value" : "total-value2";

    
    
    
   
    let flatIndex = currentIteration - 1; // The global index across all papers
    let currentListIndex = Math.floor(flatIndex / maxListLength); // Determine which list the current iteration is in
    let currentIndexInList = flatIndex  % maxListLength; // Determine the index in that list
    if (0 <= flatIndex && flatIndex <= 3){
        //First list
        currentListIndex  = 0;
        currentIndexInList = currentIteration -1;
        document.getElementById('paper-image1').src = "Man0.PNG";
        document.getElementById('paper-image2').src = "Man1b.jpg";
        document.getElementById('paper-image3').src = "Man2b.jpg";
        document.getElementById('paper1').style.backgroundImage = "url('c.png')";
      
        document.getElementById('paper2').style.backgroundImage = "url('cb.png')";
        document.getElementById('paper3').style.backgroundImage = "url('cb.png')";
    }
    else if (4 <= flatIndex && flatIndex <= 6){
        currentListIndex  = 1;
        currentIndexInList = currentIteration - 5;
        document.getElementById('paper-image1').src = "Man0b.jpg";
        document.getElementById('paper-image2').src = "Man1.PNG";
        document.getElementById('paper-image3').src = "Man2b.jpg";
        document.getElementById('paper1').style.backgroundImage = "url('cb.png')";
        document.getElementById('paper2').style.backgroundImage = "url('c.png')";
        document.getElementById('paper3').style.backgroundImage = "url('cb.png')";
        
    }
    else if (7 <= flatIndex && flatIndex <= 8){
        currentListIndex  = 2;
        currentIndexInList = currentIteration - 8;
        document.getElementById('paper-image1').src = "Man0b.jpg";
        document.getElementById('paper-image2').src = "Man1b.jpg";
        document.getElementById('paper-image3').src = "Man2.PNG";
        document.getElementById('paper1').style.backgroundImage = "url('cb.png')";
        document.getElementById('paper2').style.backgroundImage = "url('cb.png')";
        document.getElementById('paper3').style.backgroundImage = "url('c.png')";
        
        
    }

    

    // For each paper, display the items
    lists.forEach((list, paperIndex) => {
        const listItems = list.map((value, index) =>{
            
            let indexClass = '';
            let valueClass = '';
            if (paperIndex === currentListIndex && index === currentIndexInList) {
                        // Current index is highlighted
                        
                indexClass = 'highlight-item-index';
                valueClass = 'highlight-item';
            }else if (paperIndex === currentListIndex && index < currentIndexInList) {
                // Previous indices in the current list are highlighted
                indexClass = 'highlight-visited-index';
                valueClass = 'highlight-visited';
            } else if (paperIndex < currentListIndex) {
                // Indices in previous lists are highlighted
                indexClass = 'highlight-visited-index';
                valueClass = 'highlight-visited';
            }


            return `
            <div class="list-item ">
                <div class="index ${indexClass}">${index}.</div>
                <div class="value ${valueClass}">${value}</div>
            </div>`
    }).join("");

        paperDivs[paperIndex].innerHTML = `<h3>${titles[paperIndex]}</h3>${listItems}`;
    });

    // Clear previous pencil position
    visualDiv.innerHTML = '';

   
    const totalBox = `
    <div class="total-container">
       
        <div class="${totalImage}">
            
            <div class="${totalValue}">$ ${total}</div>
        </div>
         
    </div>`;
    
    visualDiv.insertAdjacentHTML('beforeend', totalBox);

    const topRightImage = `<img src="store.png" alt="Top Right Image" class="banner" />`;
    visualDiv.insertAdjacentHTML('beforeend', topRightImage); // Add the image to the visual window


    document.getElementById('iteration-info').textContent = `Iteration i = ${currentListIndex}, j = ${currentIndexInList}`;

    

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
                <li><button onclick="checkAnswer('A')">A) It sets the value of total to the value at lst[i][j]</button></li>
                <li><button onclick="checkAnswer('B')">B) It increases the value of total by the value at lst[i][j]</button></li>
                <li><button onclick="checkAnswer('C')">C) It decreases the value of total by the value at lst[i][j]</button></li>
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
    } else if (variable === 'j') {
        questionDiv.innerHTML = `<p>The variable <code>j</code> is used to track the current index in the loop.</p>`;
    } else if (variable === 'lst') {
        questionDiv.innerHTML = `<p>The variable <code>lst</code> is the 2D list (or matrix) of values being iterated over.</p>`;
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
