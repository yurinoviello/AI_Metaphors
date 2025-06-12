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
const dbNew = firebase.firestore().collection('conditions');  // Using new collection

// Initialize step counter
let currentStep = 0;

// Define the steps corresponding to each line of the code for condition checking
const steps = [
    { line: "line1", changes: [{ variable: 'weather', value: "sunny" }] }, // Setting weather
    { line: "line2", changes: [{ variable: 'time_of_day', value: "morning" }] }, // Setting time_of_day
    { line: "line3", changes: [] }, // Start of first condition
    { line: "line4", changes: [] }, // Checking if time_of_day == 'morning'
    { line: "line6", changes: [] }, // Checking if time_of_day == 'afternoon'
    { line: "line7", changes: [] }, // Printing 'Go for a jog!'
];

const stepExplanations = [
    "Step 1: Assigning 'sunny' to <span class='variable'>weather</span>",
    "Step 2: Assigning 'afternoon' to <span class='variable'>time_of_day</span>",
    "Step 3: Checking if <span class='variable'>weather == 'sunny'</span>",
    "Step 4: Checking if <span class='variable'>time_of_day == 'morning'</span>",
    "Step 5: Checking if <span class='variable'>time_of_day == 'afternoon'</span>",
    "Step 6: Assigning <span class='variable'>activity</span> to <span class='variable'>\"picnic\"</span> because <span class='variable'>weather == 'sunny'</span> and <span class='variable'>time_of_day == 'afternoon'</span>",
    "All conditions are complete."
];

// Reuse logInteraction to log interactions to the "conditions" collection
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

const userId = 'user-' + Date.now() + '-' + Math.floor(Math.random() * 10000);

function incrementStep() {
    if (currentStep < steps.length - 1) {
        currentStep++;
        updateMemory();
        updateVisual();
        updateStepExplanation();
        logInteraction('incrementStep', { currentStep: currentStep });
    } else {
        alert("All steps have been executed.");
        logInteraction('alert', { message: "All steps have been executed." });
    }
}

function decrementStep() {
    if (currentStep > 0) {
        currentStep--;
        updateMemory();
        updateVisual();
        updateStepExplanation();
        logInteraction('decrementStep', { currentStep: currentStep });
    } else {
        alert("You are at the start.");
        logInteraction('alert', { message: "You are at the start." });
    }
}

function resetSteps() {
    currentStep = 0;
    updateMemory();
    updateVisual();
    updateStepExplanation();
    logInteraction('resetSteps', { currentStep: currentStep });
}

function runAllSteps() {
    currentStep = steps.length - 1;
    updateMemory();
    updateVisual();
    updateStepExplanation();
    logInteraction('runAllSteps', { currentStep: currentStep });
}


function updateStepExplanation() {
    const stepExplanation = document.getElementById('step-explanation');
    stepExplanation.innerHTML = stepExplanations[currentStep];
}

function updateMemory() {
    document.getElementById('step-info').textContent = `Step ${currentStep + 1}`;
    const svg = document.getElementById('memory');
    while (svg.firstChild) {
        svg.removeChild(svg.firstChild);
    }
    steps.forEach(step => document.getElementById(step.line).classList.remove('highlight'));
    document.getElementById(steps[currentStep].line).classList.add('highlight');

    if (currentStep >= 0) {
        highlighting = currentStep === 0 || currentStep == 2
        drawVariableBox(svg, "weather", 30, 10, "sunny", highlighting);
        drawValueBox(svg, "\"sunny\"", 280, 10, highlighting);
        drawMemoryArrow(svg, 130, 25, 280, 25, highlighting);
    }

    if (currentStep >= 1) {
        highlighting = currentStep === 1 || currentStep == 3
        drawVariableBox(svg, "time_of_day", 30, 80, "morning", highlighting);
        drawValueBox(svg, "\"afternoon\"", 280, 80, highlighting);
        drawMemoryArrow(svg, 130, 95, 280, 95, highlighting);
    }

    if (currentStep >= 5) {
        drawVariableBox(svg, "activity", 30, 150, "picnic", currentStep === 5);
        drawValueBox(svg, "\"picnic\"", 280, 150, currentStep === 5);
        drawMemoryArrow(svg, 130, 165, 280, 165, currentStep === 5);
    }

}


function drawVariableBox(svg, name, x, y, value, highlight) {
    const varBox = document.createElementNS("http://www.w3.org/2000/svg", "rect");
    varBox.setAttribute("x", x);
    varBox.setAttribute("y", y);
    varBox.setAttribute("width", 100);
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
    varText.setAttribute("x", x + 50);
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
    valueBox.setAttribute("width", 100);
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
    valueText.setAttribute("x", x + 50);
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

    // Draw all roads first
    drawRoad(svg, 200, 50, 200, 120, currentStep == 2, false,currentStep >= 3);  // Main road
    drawRoad(svg, 200, 120, 100, 180, (currentStep == 2) || (currentStep == 3), false, currentStep >= 4);  // Branch to sunny path
    drawRoad(svg, 100, 180, 60, 240, currentStep == 3, currentStep >= 4);  // Path to morning result
    drawRoad(svg, 100, 180, 140, 240, (currentStep == 4 || currentStep == 3), false, currentStep >= 5);  // Path to afternoon result
    drawRoad(svg, 140, 240, 80, 300, (currentStep == 5 || currentStep == 4), false, currentStep >= 5);  // Path to picnic
    drawRoad(svg, 140, 240, 200, 300, currentStep == 4, currentStep >= 5);  // Path to sunset

    //drawRoad(svg, 100, 180, 100, 240);  // Path to else/sunset result

    drawRoad(svg, 200, 120, 300, 180, (currentStep == 2) , currentStep >= 3);  // Branch to rainy path
    drawRoad(svg, 300, 180, 280, 240, false, currentStep >= 3);  // Path to rainy result
    drawRoad(svg, 300, 180, 350, 240, false, currentStep >= 3);  // Path to else/default result

    // Draw the signposts and decisions
    drawSignpost(svg, "sunny?", 150, 110, currentStep == 2, false,currentStep >= 3);  // First decision: weather == "sunny"
    drawYesNoLabels(svg, 110, 150, 290, 150, currentStep == 2, currentStep >= 3); // Yes and No signs for weather == sunny

    drawSignpost(svg, "morning?", 45, 170, currentStep == 3, false, currentStep >= 4);  // Nested decision: time_of_day == "morning"
    drawYesNoLabels(svg, 40, 220, 160, 220, currentStep == 3, currentStep >= 4); // Yes and No signs for time_of_day == morning

    drawSignpost(svg, "afternoon?", 100, 230, currentStep == 4, false, currentStep >= 5);  // First decision: weather == "sunny"
    drawYesNoLabels(svg, 60, 285, 220, 285, currentStep == 4, currentStep >= 5);

    drawSignpost(svg, "rainy?", 250, 170, false, currentStep >= 3);  // Second decision: weather == "rainy"
    drawYesNoLabels(svg, 250, 220, 370, 220, false, currentStep >= 3);  // Yes and No signs for weather == rainy

    // Draw the destination results last
    drawDestination(svg, "images/running.png", 50, 255);  // Morning result
    if (currentStep >= 4) {
        drawDestination(svg, "images/running-g.png", 50, 255);  // Morning result
    }
    drawDestination(svg, "images/picnic.png", 80, 320);  // Afternoon result
    if (currentStep >= 5) {
        drawDestination(svg, "images/picnic-hl.png", 80, 320);  // Afternoon result
        // drawWindow(svg, "activity", 80, 380, true);
        // assignValueToWindow(svg, 80, 380, "\"picnic\"", true);
    }
    drawDestination(svg, "images/sunrise.png", 200, 320);  // Else result for sunny
    if (currentStep >= 5) {
        drawDestination(svg, "images/sunrise-g.png", 200, 320);  // Else result for sunny
    }
    drawDestination(svg, "images/umbrella.png", 280, 265);  // Rainy result
    drawDestination(svg, "images/indoor.png", 350, 265);  // Else result
    if (currentStep >= 3) {
        drawDestination(svg, "images/umbrella-g.png", 280, 265);  // Rainy result
        drawDestination(svg, "images/indoor-g.png", 350, 265);  // Else result
    }
}

function drawRoad(svg, x1, y1, x2, y2, highlight, greyed, passed) {
    const road = document.createElementNS("http://www.w3.org/2000/svg", "line");
    road.setAttribute("x1", x1);
    road.setAttribute("y1", y1);
    road.setAttribute("x2", x2);
    road.setAttribute("y2", y2);
    road.setAttribute("stroke", "black");
    road.setAttribute("stroke-width", 15);
    if (highlight){
        road.setAttribute("stroke", "#ff6a00");
        road.setAttribute("stroke-width", 20);
    }
    if (greyed) {
        road.setAttribute("stroke", "#c2c2c2");
    }
    if (passed) {
        road.setAttribute("stroke", "#e8ada0");
    }
    svg.appendChild(road);
}

function drawSignpost(svg, label, x, y, highlight, greyed, passed) {
    const signpost = document.createElementNS("http://www.w3.org/2000/svg", "rect");
    signpost.setAttribute("x", x);
    signpost.setAttribute("y", y);
    signpost.setAttribute("width", 100);
    signpost.setAttribute("height", 30);
    signpost.setAttribute("fill", "#e4ecf0");
    signpost.setAttribute("stroke", "black");
    if(highlight){
        signpost.setAttribute("stroke", "#ff6a00");
        signpost.setAttribute("fill", "#ffff00");
    }
    if (greyed) {
        signpost.setAttribute("fill", "#c2c2c2");
    }

    if (passed) {
        signpost.setAttribute("fill", "#e8ada0");
    }
    svg.appendChild(signpost);

    const signText = document.createElementNS("http://www.w3.org/2000/svg", "text");
    signText.setAttribute("x", x + 50);
    signText.setAttribute("y", y + 20);
    signText.setAttribute("text-anchor", "middle");
    signText.setAttribute("fill", "black");
    if (greyed) {
        signText.setAttribute("fill", "#6e6e6e");
    }
    signText.textContent = label;
    svg.appendChild(signText);

    if (greyed) {
        const strikeThrough = document.createElementNS("http://www.w3.org/2000/svg", "line");
        strikeThrough.setAttribute("x1", x + 10);  // Starting point of the line
        strikeThrough.setAttribute("y1", y + 15);  // Mid-point of the text vertically
        strikeThrough.setAttribute("x2", x + 90);  // End point of the line
        strikeThrough.setAttribute("y2", y + 15);
        strikeThrough.setAttribute("stroke", "black");
        strikeThrough.setAttribute("stroke-width", "0.5");
        svg.appendChild(strikeThrough);
    }
}


function drawDestination(svg, imageUrl, x, y) {
    const img = document.createElementNS("http://www.w3.org/2000/svg", "image");
    img.setAttributeNS("http://www.w3.org/1999/xlink", "href", imageUrl);
    img.setAttribute("x", x - 15);  // Adjust the x-coordinate
    img.setAttribute("y", y - 15);  // Adjust the y-coordinate
    img.setAttribute("width", 30);  // Set the width of the icon
    img.setAttribute("height", 30); // Set the height of the icon
    svg.appendChild(img);
}


function drawYesNoLabels(svg, yesX, yesY, noX, noY, highlight, greyed, passed) {
    const yesText = document.createElementNS("http://www.w3.org/2000/svg", "text");
    yesText.setAttribute("x", yesX);
    yesText.setAttribute("y", yesY);
    yesText.setAttribute("text-anchor", "middle");
    yesText.setAttribute("fill", "black");
    yesText.setAttribute("font-size", "18px");
    yesText.setAttribute("font-weight", "bold");
    yesText.textContent = "True";
    if (highlight) {
        yesText.setAttribute("fill", "#ff6a00");
    }
    if (greyed){
        yesText.setAttribute("fill", "#c2c2c2");
    }
    if (passed) {
        yesText.setAttribute("fill", "#e8ada0");
    }
    svg.appendChild(yesText);

    const noText = document.createElementNS("http://www.w3.org/2000/svg", "text");
    noText.setAttribute("x", noX);
    noText.setAttribute("y", noY);
    noText.setAttribute("text-anchor", "middle");
    noText.setAttribute("fill", "black");
    noText.setAttribute("font-size", "18px");
    noText.setAttribute("font-weight", "bold");
    noText.textContent = "False";
    if (highlight) {
        noText.setAttribute("fill", "#ff6a00");
    }
    if (greyed){
        noText.setAttribute("fill", "#c2c2c2");
    }
    if (passed) {
        noText.setAttribute("fill", "#e8ada0");
    }
    svg.appendChild(noText);

}

function drawWindow(svg, variable, x, y, highlight) {
    const boxWidth = 80;
    const boxHeight = 50;
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


window.onload = () => {
    resetSteps();
    updateStepExplanation();
}
