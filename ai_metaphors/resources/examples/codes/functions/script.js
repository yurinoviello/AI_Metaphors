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
const dbNew = firebase.firestore().collection('functionsExample');  // Using new collection

firebase.auth().signInAnonymously()
  .then(() => {
    console.log("User signed in anonymously");
  })
  .catch((error) => {
    console.error("Error during anonymous authentication: ", error);
  });

function logInteraction(eventType, details) {
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

function scaleApp() {
    const app = document.getElementById('app');
    // For example, base design is for 1920px width
    const scaleFactor = window.innerWidth / 1920;
    app.style.transform = 'scale(' + scaleFactor + ')';
    app.style.transformOrigin = 'center center';
}

const userId = 'user-' + Date.now() + '-' + Math.floor(Math.random() * 10000);

let currentStep = 0;
let isSteppingIntoFunction = false;  // Default state: skipping the function details

const steps = [
    { line: "line1", changes: [{ variable: 'a', value: 5 }] },
    { line: "line2", changes: [{ variable: 'b', value: 2 }] },
    { line: "line3", changes: [] },  // Function declaration
    { line: "line6", changes: [] },  // calling the function
    { line: "line4", changes: [{ variable: 'a', value: 7 }] },    // a's current value
    { line: "line5", changes: [] },    // returning
    { line: "line6", changes: [{ variable: 'c', value: 7 }] }
];

const stepExplanations = [
    'Step 1: Assigning the value <span class="variable">5</span> to <span class="variable">a</span>',
    'Step 2: Assigning the value <span class="variable">2</span> to <span class="variable">b</span>',
    'Step 3: Defining the function <span class="variable">my_add(a, b)</span>',
    'Step 4: Calling the function <span class="variable">my_add(a, b)</span>',
    isSteppingIntoFunction ? 
    'Step 5: Assigning <span class="variable">a</span> to <span class="variable">a + b</span> which is <span class="variable">7</span>' : 
    'Step 5: Function execution hidden',
    'Step 6: Returning the function\'s value of <span class="variable">a</span>',
    'Step 7: Returned value (7) assigned to <span class="variable">c</span>'
];

const variables = { a: null, b: null, temp: null };

function incrementStep() {
    if (currentStep < steps.length - 1) {
        if (!isSteppingIntoFunction && currentStep == 3) {
            currentStep = 5;
        }
        else {
        currentStep++;
        }
        updateMemory();
        updateVisual();
        updateStepExplanation();
        logInteraction('incrementStep', { currentStep: currentStep });
    } else {
        alert("All lines have been executed.");
        logInteraction('alert', { message: "All lines have been executed." });
    }
}

function decrementStep() {
    if (currentStep > 0) {
        if (!isSteppingIntoFunction && currentStep == 5) {
            currentStep = 3;
        }
        else currentStep--;
        updateMemory();
        updateVisual();
        updateStepExplanation();
        logInteraction('decrementStep', { currentStep: currentStep });
    } else {
        alert("You are at the beginning.");
        logInteraction('alert', { message: "You are at the beginning." });
    }
}

function resetSteps() {
    currentStep = 0;
    variables.a = null;
    variables.b = null;
    variables.temp = null;
    updateMemory();
    updateVisual();
    updateStepExplanation();
    logInteraction('resetSteps', { currentStep: currentStep });
}

function toggleStepInto() {
    isSteppingIntoFunction = !isSteppingIntoFunction;
    const stepIntoButton = document.getElementById("step-into-btn");
    if (isSteppingIntoFunction) {
        stepIntoButton.innerHTML = "Hide Function";
    } else {
        stepIntoButton.innerHTML = "Reveal Function";
    }
    updateMemory();
    updateVisual();
    updateStepExplanation();
}

function updateStepExplanation() {
    const stepExplanation = document.getElementById('step-explanation');
    stepExplanations[4] = isSteppingIntoFunction ? 
        'Step 5: Assigning <span class="variable">a</span> to <span class="variable">a + b</span> which is <span class="variable">7</span>' :
        'Step 5: Function execution hidden';
    stepExplanation.innerHTML = stepExplanations[currentStep];
}

function runAllSteps() {
    currentStep = steps.length - 1;
    updateMemory();
    updateVisual();
    updateStepExplanation();
    logInteraction('runAllSteps', { currentStep: currentStep });
}

function updateMemory() {
    const svg = document.getElementById('memory');
    while (svg.firstChild) {
        svg.removeChild(svg.firstChild);
    }
    document.getElementById('step-info').textContent = `Step ${currentStep + 1}`;
    steps.forEach(step => document.getElementById(step.line).classList.remove('highlight'));
    document.getElementById(steps[currentStep].line).classList.add('highlight');
    if (currentStep >= 0){ // inside the function
        // Draw the memory frame (global frame)
        const memoryFrame1 = document.createElementNS("http://www.w3.org/2000/svg", "rect");
        memoryFrame1.setAttribute("x", 40);
        memoryFrame1.setAttribute("y", 170);
        memoryFrame1.setAttribute("width", 180);
        memoryFrame1.setAttribute("height", 140);
        memoryFrame1.setAttribute("fill", "#e4ecf0");
        memoryFrame1.setAttribute("stroke", "black");
        memoryFrame1.setAttribute("stroke-width", 2);
        if (currentStep < 3 || currentStep >= 5) {
            memoryFrame1.setAttribute("fill", "#fff3d4");
            memoryFrame1.setAttribute("stroke", "#ff6a00");
            memoryFrame1.setAttribute("stroke-width", 3);
        }
        svg.appendChild(memoryFrame1);
        const frameLabel = document.createElementNS("http://www.w3.org/2000/svg", "text");
        frameLabel.setAttribute("x", 170);
        frameLabel.setAttribute("y", 305);
        frameLabel.setAttribute("text-anchor", "middle");
        frameLabel.setAttribute("fill", "black");
        frameLabel.textContent = "Global Scope";
        svg.appendChild(frameLabel);
    }

    if (currentStep >= 3){ // inside the function
        // Draw the memory frame (function frame)
        const memoryFrame = document.createElementNS("http://www.w3.org/2000/svg", "rect");
        memoryFrame.setAttribute("x", 40);
        memoryFrame.setAttribute("y", 20);
        memoryFrame.setAttribute("width", 180);
        memoryFrame.setAttribute("height", 140);
        memoryFrame.setAttribute("fill", "#e4ecf0");
        memoryFrame.setAttribute("stroke", "black");
        memoryFrame.setAttribute("stroke-width", 2);
        if (currentStep >= 3 && currentStep < 5) {
            memoryFrame.setAttribute("fill", "#fff3d4");
            memoryFrame.setAttribute("stroke", "#ff6a00");
            memoryFrame.setAttribute("stroke-width", 3);
        }
        svg.appendChild(memoryFrame);
        // Label for the memory frame
        const frameLabel = document.createElementNS("http://www.w3.org/2000/svg", "text");
        frameLabel.setAttribute("x", 170);
        frameLabel.setAttribute("y", 150);
        frameLabel.setAttribute("text-anchor", "middle");
        frameLabel.setAttribute("fill", "black");
        frameLabel.textContent = "my_add(5, 2)";
        svg.appendChild(frameLabel);
    }

    if (currentStep >= 3 && isSteppingIntoFunction) {
        // Show the function's memory details
        drawVariableBox(svg, "x", 50, 30, variables.a, currentStep == 3);
        drawValueBox(svg, 5, 280, 30, currentStep == 3);
        drawMemoryArrow(svg, 110, 45, 280, 45, currentStep == 3);
        drawVariableBox(svg, "y", 50, 70, variables.b, currentStep == 3);
        drawValueBox(svg, 2, 280, 70, currentStep == 3);
        drawMemoryArrow(svg, 110, 85, 280, 85, currentStep == 3);
    } else if (currentStep >= 3 && !isSteppingIntoFunction) {
        // Show placeholder "hidden" if not stepping into the function
        const hiddenText = document.createElementNS("http://www.w3.org/2000/svg", "text");
        hiddenText.setAttribute("x", 120);
        hiddenText.setAttribute("y", 100);
        hiddenText.setAttribute("text-anchor", "middle");
        hiddenText.setAttribute("fill", "black");
        hiddenText.textContent = "Function hidden";
        svg.appendChild(hiddenText);
    }

    if (currentStep >= 4 && isSteppingIntoFunction) {
        drawVariableBox(svg, "a", 50, 110, variables.a, currentStep == 4);
        drawValueBox(svg, 7, 280, 110, currentStep == 4);
        drawMemoryArrow(svg, 110, 125, 280, 125, currentStep == 4);
    }

    // Global scope variables
    drawVariableBox(svg, "a", 50, 180, variables.a, currentStep == 0);
    drawValueBox(svg, 5, 280, 180, currentStep == 0);
    drawMemoryArrow(svg, 110, 195, 280, 195, currentStep == 0);
    if (currentStep >= 1) {
        drawVariableBox(svg, "b", 50, 220, variables.b, currentStep == 1);
        drawValueBox(svg, 2, 280, 220, currentStep == 1);
        drawMemoryArrow(svg, 110, 235, 280, 235, currentStep == 1);
    }
    if (currentStep >= 6) {
        drawVariableBox(svg, "c", 50, 260, variables.b, currentStep == 6);
        drawValueBox(svg, 7, 280, 260, currentStep == 6);
        drawMemoryArrow(svg, 110, 275, 280, 275, currentStep == 6);
    }
}

function drawVariableBox(svg, name, x, y, value, highlight) {
    const varBox = document.createElementNS("http://www.w3.org/2000/svg", "rect");
    varBox.setAttribute("x", x);
    varBox.setAttribute("y", y);
    varBox.setAttribute("width", 60);
    varBox.setAttribute("height", 30);
    varBox.setAttribute("fill", "#b3e5fc"); // Light blue for variables
    varBox.setAttribute("stroke", "black");
    varBox.setAttribute("stroke-width", 2);
    if (highlight) {
        varBox.setAttribute("stroke", "#ff6a00");
        varBox.setAttribute("fill", "#ffff00");
        varBox.setAttribute("stroke-width", 3);
    }
    svg.appendChild(varBox);

    const varText = document.createElementNS("http://www.w3.org/2000/svg", "text");
    varText.setAttribute("x", x + 30);
    varText.setAttribute("y", y + 20);
    varText.setAttribute("text-anchor", "middle");
    varText.setAttribute("fill", "black");
    varText.textContent = name;
    svg.appendChild(varText);
}

function drawValueBox(svg, value, x, y, highlight) {
    const valueBox = document.createElementNS("http://www.w3.org/2000/svg", "rect");
    valueBox.setAttribute("x", x);
    valueBox.setAttribute("y", y);
    valueBox.setAttribute("width", 30);
    valueBox.setAttribute("height", 30);
    valueBox.setAttribute("fill", "#cdf8bf"); // Light green for values
    valueBox.setAttribute("stroke", "black");
    valueBox.setAttribute("stroke-width", 2);
    if (highlight) {
        valueBox.setAttribute("fill", "#ffff00");
        valueBox.setAttribute("stroke", "#ff6a00");
        valueBox.setAttribute("stroke-width", 3);
    }
    svg.appendChild(valueBox);

    const valueText = document.createElementNS("http://www.w3.org/2000/svg", "text");
    valueText.setAttribute("x", x + 15);
    valueText.setAttribute("y", y + 20);
    valueText.setAttribute("text-anchor", "middle");
    valueText.setAttribute("fill", "black");
    valueText.textContent = value;
    svg.appendChild(valueText);
}

function drawMemoryArrow(svg, x1, y1, x2, y2, highlight) {
    const arrow = document.createElementNS("http://www.w3.org/2000/svg", "line");
    arrow.setAttribute("x1", x1);
    arrow.setAttribute("y1", y1);
    arrow.setAttribute("x2", x2);
    arrow.setAttribute("y2", y2);
    arrow.setAttribute("stroke", "black");
    arrow.setAttribute("stroke-width", 2);
    arrow.setAttribute("marker-end", "url(#arrow)"); // Use an arrowhead marker
    if (highlight) {
        arrow.setAttribute("stroke", "#ff6a00");
        arrow.setAttribute("stroke-width", 3);
    }
    svg.appendChild(arrow);
}

function updateVisual() {
    const svg = document.getElementById('visual');
    while (svg.firstChild) {
        svg.removeChild(svg.firstChild);
    }

    if (currentStep >= 0) {
        drawHouseWithRoof1(svg, "Global Scope", 5, 50, currentStep == 0);  // Left house for Global
        drawStickFigure(svg, 120, 170, "", currentStep < 3 || currentStep >= 5);  // Stick figure for Global
    }

    if (currentStep >= 3) {
        drawInteractionArrow(svg, 146, 150, 248, 150, "add 5 and 2", "up", currentStep == 3);  // Adding values arrow
        drawHouseWithRoof2(svg, "my_add(5, 2)", 295, 50);  // Function scope house
        drawStickFigure(svg, 275, 170, "", currentStep >= 3 && currentStep < 5);  // Function stick figure
        if (isSteppingIntoFunction) {
            if (currentStep >= 4) {
                drawWindow(svg, 'a', 295 + 50, 150, currentStep == 4 || currentStep == 5);  // Right window
                assignValueToWindow(svg, 295 + 50, 150, 7, currentStep == 4 || currentStep == 5);

            } 
            assignValueToWindow(svg, 315, 90, 5, currentStep == 3);  // Assign values to function house windows
            assignValueToWindow(svg, 375, 90, 2, currentStep == 3);  
        }
    } else if (currentStep >= 3 && !isSteppingIntoFunction) {
        // Hide function details and show "hidden" message
        const hiddenText = document.createElementNS("http://www.w3.org/2000/svg", "text");
        hiddenText.setAttribute("x", 345);
        hiddenText.setAttribute("y", 120);
        hiddenText.setAttribute("text-anchor", "middle");
        hiddenText.setAttribute("fill", "black");
        hiddenText.textContent = "Function hidden";
        svg.appendChild(hiddenText);
    }

    if (currentStep >= 5) {
        drawInteractionArrow(svg, 150, 175, 255, 180, "returning 7", "down", currentStep == 5);  // Returning result arrow
    }

    assignValueToWindow(svg, 25, 90, 5, currentStep == 0);  // Assign value to Global house window 1
    if (currentStep >= 1) {
        assignValueToWindow(svg, 85, 90, 2, currentStep == 1);  // Assign value to Global house window 2
    }

    if (currentStep >= 6) {
        drawWindow(svg, 'c', 55, 160, currentStep == 6);  // Left window
        assignValueToWindow(svg, 55, 160, 7, currentStep == 6);
    }
}

function drawHouseWithRoof1(svg, label, x, y, highlight) {
    const house = document.createElementNS("http://www.w3.org/2000/svg", "rect");
    house.setAttribute("x", x);
    house.setAttribute("y", y);
    house.setAttribute("width", 100);
    house.setAttribute("height", 150);
    house.setAttribute("fill", "#e4ecf0");
    house.setAttribute("stroke", "black");
    house.setAttribute("stroke-width", 2);
    if (currentStep < 3 || currentStep >= 5) {
        house.setAttribute("fill", "#fff3d4");
        house.setAttribute("stroke", "#ff6a00");
        house.setAttribute("stroke-width", 3);
    }
    svg.appendChild(house);


    const roofURL = (currentStep < 3 || currentStep >= 5) ? "./images/home-hl.png" : "./images/home.png";
    const roofImage = document.createElementNS("http://www.w3.org/2000/svg", "image");
    roofImage.setAttributeNS("http://www.w3.org/1999/xlink", "href", roofURL);
    roofImage.setAttribute("width", "130");
    roofImage.setAttribute("height", "110");
    roofImage.setAttribute("x", x - 15);
    roofImage.setAttribute("y", y - 65);
    svg.appendChild(roofImage);

    // const roof = document.createElementNS("http://www.w3.org/2000/svg", "polygon");
    // roof.setAttribute("points", `${x},${y} ${x + 50},${y - 40} ${x + 100},${y}`);
    // roof.setAttribute("fill", "#ffcc80");  // Light orange color for roof
    // roof.setAttribute("stroke", "black");
    // roof.setAttribute("stroke-width", 2);
    // svg.appendChild(roof);

    const houseLabel = document.createElementNS("http://www.w3.org/2000/svg", "text");
    houseLabel.setAttribute("x", x + 50);
    houseLabel.setAttribute("y", y + 170);
    houseLabel.setAttribute("text-anchor", "middle");
    houseLabel.setAttribute("fill", "black");
    houseLabel.textContent = label;
    svg.appendChild(houseLabel);

    drawWindow(svg, 'a', x + 20, y + 40, highlight);  // Left window
    if (currentStep >= 1) drawWindow(svg, 'b', x + 80, y + 40, currentStep == 1);  // Right window
}

function drawHouseWithRoof2(svg, label, x, y, highlight) {
    const house = document.createElementNS("http://www.w3.org/2000/svg", "rect");
    house.setAttribute("x", x);
    house.setAttribute("y", y);
    house.setAttribute("width", 100);
    house.setAttribute("height", 150);
    house.setAttribute("fill", "#e4ecf0");
    house.setAttribute("stroke", "black");
    house.setAttribute("stroke-width", 2);
    if (currentStep >= 3 && currentStep < 5) {
        house.setAttribute("fill", "#fff3d4");
        house.setAttribute("stroke", "#ff6a00");
        house.setAttribute("stroke-width", 3);
    }
    svg.appendChild(house);

    if (!isSteppingIntoFunction){
        const houseLabel2 = document.createElementNS("http://www.w3.org/2000/svg", "text");
        houseLabel2.setAttribute("x", x + 50);
        houseLabel2.setAttribute("y", y + 70);
        houseLabel2.setAttribute("text-anchor", "middle");
        houseLabel2.setAttribute("fill", "black");
        houseLabel2.textContent = "Hidden";
        svg.appendChild(houseLabel2);
    }

    const roofURL = (currentStep >= 3 && currentStep < 5) ? "./images/home-hl.png" : "./images/home.png";
    const roofImage = document.createElementNS("http://www.w3.org/2000/svg", "image");
    roofImage.setAttributeNS("http://www.w3.org/1999/xlink", "href", roofURL);
    roofImage.setAttribute("width", "130");
    roofImage.setAttribute("height", "110");
    roofImage.setAttribute("x", x - 15);
    roofImage.setAttribute("y", y - 65);
    svg.appendChild(roofImage);

    const houseLabel = document.createElementNS("http://www.w3.org/2000/svg", "text");
    houseLabel.setAttribute("x", x + 50);
    houseLabel.setAttribute("y", y + 170);
    houseLabel.setAttribute("text-anchor", "middle");
    houseLabel.setAttribute("fill", "black");
    houseLabel.textContent = label;
    svg.appendChild(houseLabel);
    if (isSteppingIntoFunction){
        drawWindow(svg, 'x', x + 20, y + 40, currentStep == 3 || currentStep == 4);  // Left window
        drawWindow(svg, 'y', x + 80, y + 40, currentStep == 3);  // Right window
    }
}

function drawWindow(svg, variable, x, y, highlight) {
    const boxWidth = 32;
    const boxHeight = 32;
    const lidHeight = 10;

    const varBox = document.createElementNS("http://www.w3.org/2000/svg", "rect");
    varBox.setAttribute("x", x - boxWidth / 2);
    varBox.setAttribute("y", y - boxHeight / 2);
    varBox.setAttribute("width", boxWidth);
    varBox.setAttribute("height", boxHeight);
    varBox.setAttribute("fill", "powderblue");
    varBox.setAttribute("stroke", "black");
    varBox.setAttribute("stroke-width", 2);
    if (highlight) {
        varBox.setAttribute("fill", "yellow");
        varBox.setAttribute("stroke", "#ff6a00");
        varBox.setAttribute("stroke-width", 3);
    }
    svg.appendChild(varBox);

    const lidLine = document.createElementNS("http://www.w3.org/2000/svg", "line");
    lidLine.setAttribute("x1", x - boxWidth / 2);
    lidLine.setAttribute("y1", y - boxHeight / 2);
    lidLine.setAttribute("x2", x + boxWidth / 2);
    lidLine.setAttribute("y2", y - boxHeight / 2 - lidHeight);
    lidLine.setAttribute("stroke", "black");
    lidLine.setAttribute("stroke-width", 2);
    if (highlight) {
        lidLine.setAttribute("stroke", "#ff6a00");
        lidLine.setAttribute("stroke-width", 3);
    }
    svg.appendChild(lidLine);

    const varText = document.createElementNS("http://www.w3.org/2000/svg", "text");
    varText.setAttribute("x", x);
    varText.setAttribute("y", y + boxHeight);
    varText.setAttribute("text-anchor", "middle");
    varText.setAttribute("fill", "black");
    varText.textContent = variable;
    svg.appendChild(varText);
}

function assignValueToWindow(svg, x, y, value, highlight) {
    const valueRect = document.createElementNS("http://www.w3.org/2000/svg", "rect");
    if (!highlight) {
        valueRect.setAttribute("x", x - 10);
        valueRect.setAttribute("y", y - 10);
        valueRect.setAttribute("width", 20);
        valueRect.setAttribute("height", 20);
        valueRect.setAttribute("fill", "#cdf8bf");
        valueRect.setAttribute("stroke", "black");
        svg.appendChild(valueRect);
    }

    const valueText = document.createElementNS("http://www.w3.org/2000/svg", "text");
    valueText.setAttribute("x", x);
    valueText.setAttribute("y", y + 5);
    valueText.setAttribute("text-anchor", "middle");
    valueText.setAttribute("fill", "black");
    valueText.textContent = value;
    svg.appendChild(valueText);
}

function drawStickFigure(svg, x, y, label, highlight) {
    const color = highlight ? "#ff6a00" : "black";

    const head = document.createElementNS("http://www.w3.org/2000/svg", "circle");
    head.setAttribute("cx", x);
    head.setAttribute("cy", y);
    head.setAttribute("r", 10);
    head.setAttribute("stroke", color);
    head.setAttribute("fill", "none");
    if (highlight) head.setAttribute("stroke-width", 3);
    svg.appendChild(head);

    const body = document.createElementNS("http://www.w3.org/2000/svg", "line");
    body.setAttribute("x1", x);
    body.setAttribute("y1", y + 10);
    body.setAttribute("x2", x);
    body.setAttribute("y2", y + 40);
    body.setAttribute("stroke", color);
    if (highlight) body.setAttribute("stroke-width", 3);
    svg.appendChild(body);

    const leftArm = document.createElementNS("http://www.w3.org/2000/svg", "line");
    leftArm.setAttribute("x1", x);
    leftArm.setAttribute("y1", y + 20);
    leftArm.setAttribute("x2", x - 15);
    leftArm.setAttribute("y2", y + 35);
    leftArm.setAttribute("stroke", color);
    if (highlight) leftArm.setAttribute("stroke-width", 3);
    svg.appendChild(leftArm);

    const rightArm = document.createElementNS("http://www.w3.org/2000/svg", "line");
    rightArm.setAttribute("x1", x);
    rightArm.setAttribute("y1", y + 20);
    rightArm.setAttribute("x2", x + 15);
    rightArm.setAttribute("y2", y + 35);
    rightArm.setAttribute("stroke", color);
    if (highlight) rightArm.setAttribute("stroke-width", 3);
    svg.appendChild(rightArm);

    const leftLeg = document.createElementNS("http://www.w3.org/2000/svg", "line");
    leftLeg.setAttribute("x1", x);
    leftLeg.setAttribute("y1", y + 40);
    leftLeg.setAttribute("x2", x - 10);
    leftLeg.setAttribute("y2", y + 60);
    leftLeg.setAttribute("stroke", color);
    if (highlight) leftLeg.setAttribute("stroke-width", 3);
    svg.appendChild(leftLeg);

    const rightLeg = document.createElementNS("http://www.w3.org/2000/svg", "line");
    rightLeg.setAttribute("x1", x);
    rightLeg.setAttribute("y1", y + 40);
    rightLeg.setAttribute("x2", x + 10);
    rightLeg.setAttribute("y2", y + 60);
    rightLeg.setAttribute("stroke", color);
    if (highlight) rightLeg.setAttribute("stroke-width", 3);
    svg.appendChild(rightLeg);

    const labelText = document.createElementNS("http://www.w3.org/2000/svg", "text");
    labelText.setAttribute("x", x);
    labelText.setAttribute("y", y + 70);
    labelText.setAttribute("text-anchor", "middle");
    labelText.setAttribute("fill", "black");
    labelText.textContent = label;
    if (highlight) labelText.setAttribute("fill", "#ff6a00");
    svg.appendChild(labelText);
}

function drawInteractionArrow(svg, x1, y1, x2, y2, label, curveDirection = 'up', highlight) {
    const arrowhead = document.createElementNS("http://www.w3.org/2000/svg", "marker");
    arrowhead.setAttribute("id", "arrowhead");
    arrowhead.setAttribute("markerWidth", 10);
    arrowhead.setAttribute("markerHeight", 7);
    arrowhead.setAttribute("refX", 0);
    arrowhead.setAttribute("refY", 3.5);
    arrowhead.setAttribute("orient", "auto");
    arrowhead.setAttribute("markerUnits", "strokeWidth");

    const arrowheadPath = document.createElementNS("http://www.w3.org/2000/svg", "path");
    arrowheadPath.setAttribute("d", "M0,0 L0,7 L10,3.5 Z");
    arrowheadPath.setAttribute("fill", "#757575");

    arrowhead.appendChild(arrowheadPath);
    svg.appendChild(arrowhead);

    const arrowhead_hl = document.createElementNS("http://www.w3.org/2000/svg", "marker");
    arrowhead_hl.setAttribute("id", "arrowhead_hl");
    arrowhead_hl.setAttribute("markerWidth", 10);
    arrowhead_hl.setAttribute("markerHeight", 7);
    arrowhead_hl.setAttribute("refX", 0);
    arrowhead_hl.setAttribute("refY", 3.5);
    arrowhead_hl.setAttribute("orient", "auto");
    arrowhead_hl.setAttribute("markerUnits", "strokeWidth");

    const arrowhead_hlPath = document.createElementNS("http://www.w3.org/2000/svg", "path");
    arrowhead_hlPath.setAttribute("d", "M0,0 L0,7 L10,3.5 Z");
    arrowhead_hlPath.setAttribute("fill", "#ff6a00");

    arrowhead_hl.appendChild(arrowhead_hlPath);
    svg.appendChild(arrowhead_hl);

    const curve = document.createElementNS("http://www.w3.org/2000/svg", "path");

    let controlPointY1, controlPointY2, arrowMarker;
    if (curveDirection === 'up') {
        controlPointY1 = y1 - 50;
        controlPointY2 = y2 - 50;
        arrowMarker = "url(#arrowhead)";
    } else {
        controlPointY1 = y1 + 50;
        controlPointY2 = y2 + 50;
        arrowMarker = "url(#arrowhead)";
        [x1, x2] = [x2, x1];
    }

    const curvePath = `
        M ${x1},${y1}
        C ${(x1 + x2) / 2},${controlPointY1} ${(x1 + x2) / 2},${controlPointY2} ${x2},${y2}
    `;
    curve.setAttribute("d", curvePath);
    curve.setAttribute("stroke", "black");
    curve.setAttribute("stroke-width", 2);
    curve.setAttribute("fill", "none");
    curve.setAttribute("stroke-dasharray", "5, 5");
    curve.setAttribute("marker-end", arrowMarker);
    if (highlight) {
        curve.setAttribute("stroke", "#ff6a00");
        curve.setAttribute("marker-end", "url(#arrowhead_hl)");
    }
    svg.appendChild(curve);

    // Add phone icon on top for "up" direction and below for "down"
    const phoneIconUrl = highlight ? "./images/highlighted-phone.png" : "./images/phone.png";
    const phoneImage = document.createElementNS("http://www.w3.org/2000/svg", "image");
    phoneImage.setAttributeNS("http://www.w3.org/1999/xlink", "href", phoneIconUrl);
    phoneImage.setAttribute("width", "35");
    phoneImage.setAttribute("height", "35");

    const responseURL = highlight ? "./images/call-response-hl.png" : "./images/call-response.png";
    const responseImage = document.createElementNS("http://www.w3.org/2000/svg", "image");
    responseImage.setAttributeNS("http://www.w3.org/1999/xlink", "href", responseURL);
    responseImage.setAttribute("width", "50");
    responseImage.setAttribute("height", "50");

    if (curveDirection === 'up') {
        phoneImage.setAttribute("x", (x1 + x2) / 2 - 15);
        phoneImage.setAttribute("y", controlPointY1 - 60);
        svg.appendChild(phoneImage);
    } else {
        responseImage.setAttribute("x", (x1 + x2) / 2 - 17);
        responseImage.setAttribute("y", controlPointY2 + 20);
        svg.appendChild(responseImage);
    }

    // Label the arrow
    const labelText = document.createElementNS("http://www.w3.org/2000/svg", "text");
    labelText.setAttribute("x", (x1 + x2) / 2);
    labelText.setAttribute("y", (curveDirection === 'up' ? controlPointY1 : controlPointY2 + 10));
    labelText.setAttribute("text-anchor", "middle");
    labelText.setAttribute("fill", "black");
    if (highlight){
        labelText.setAttribute("fill", "#ff6a00");
    }
    labelText.textContent = label;
    svg.appendChild(labelText);
}

window.onload = () => {
    window.addEventListener('resize', scaleApp);
    window.addEventListener('load', scaleApp);
    resetSteps();
    updateStepExplanation();
}