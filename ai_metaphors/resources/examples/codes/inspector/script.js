let currentIteration = 0;
const maxIterations = 4; // Adjusted for your list length
let total = "";
const lst = ['""', '""', 'Bunny', '""'];
let wantedItemInitialized = false;
let searching = true;
let counter = 0;
let wanted_item = 'Bunny';

let currentStep = 0;

// Step explanations
const stepExplanations = [
    'Initialize <span class="variable">Searching</span> to <span class="variable">True</span>',
    'Initialize <span class="variable">Counter</span> to <span class="variable">0</span>',
    'Initialize <span class="variable">wanted_item</span> to <span class="variable">"Bunny"</span>',
    'Define the list <span class="variable">lst</span>',
    'Check while loop condition',
    'Iteration 1: Current found item does not equal <span class="variable">wanted_item</span>. Enter else statement.',
    'Increment <span class="variable">Counter</span>',
    'Iteration 2: Current found item does not equal <span class="variable">wanted_item</span>. Enter else statement.',
    'Increment <span class="variable">Counter</span>',
    'Iteration 3: Current found item DOES equal <span class="variable">wanted_item</span>. Enter if statement',
    '<span class="variable">Searching</span> is now set to <span class="variable">False</span>',
    '<span class="variable">Searching</span> makes while loop condition negative, exit while loop',
];

// Increment loop iteration
function incrementLoop() {
    if (currentIteration < stepExplanations.length) {
        currentIteration++;
        currentStep++;

        updateMemory();
        updateVisual();
        updateCodeHighlight();
        updateStepExplanation();
    } else {
        alert("Program has finished executing.");
    }
}

// Decrement loop iteration
function decrementLoop() {
    if (currentIteration > 0) {
        currentIteration--;
        currentStep--;
        
        updateMemory();
        updateVisual();
        updateCodeHighlight();
        updateStepExplanation();
    } else {
        alert("Already at the start of the loop.");
    }
}

function scaleApp() {
    const app = document.getElementById('app');
    // For example, base design is for 1920px width
    const scaleFactor = window.innerWidth / 1920;
    app.style.transform = 'scale(' + scaleFactor + ')';
    app.style.transformOrigin = 'center center';
}


// Reset loop
function resetLoop() {
    currentIteration = 0;
    currentStep = 0;
    counter = 0;
    total = "";
    wantedItemInitialized = false;

    document.getElementById('var0').style.backgroundColor = '#e8e8e8';
        document.getElementById('var0').style.border = '1px solid #000000';
        document.getElementById('val0').style.backgroundColor = '#e8e8e8';
        document.getElementById('val0').style.border = '1px solid #000000';

        document.getElementById('var1').style.backgroundColor = '#e8e8e8';
        document.getElementById('var1').style.border = '1px solid #000000';
        document.getElementById('val1').style.backgroundColor = '#e8e8e8';
        document.getElementById('val1').style.border = '1px solid #000000';

        document.getElementById('var2').style.backgroundColor = '#e8e8e8';
        document.getElementById('var2').style.border = '1px solid #000000';
        document.getElementById('val2').style.backgroundColor = '#e8e8e8';
        document.getElementById('val2').style.border = '1px solid #000000';

        document.getElementById('cont0').style.backgroundColor = '#e8e8e8';
        document.getElementById('cont0').style.border = '';

        document.getElementById('cont1').style.backgroundColor = '#e8e8e8';
        document.getElementById('cont1').style.border = '';
        document.getElementById('hat1-image').style.visibility = 'visible';
        document.getElementById('hat2-image').style.visibility = 'visible';

        document.getElementById('hat1-image').src = 'hat-bl.PNG';
        document.getElementById('hat2-image').src = 'hat-bl.PNG';
        document.getElementById('hat3-image').src = 'hat-bl.PNG';

        document.getElementById('hat-var1').classList.remove('highlight-item');
        document.getElementById('hat-var1').classList.remove('highlight-visited-index');

        document.getElementById('hat-var2').classList.remove('highlight-item');
        document.getElementById('hat-var2').classList.remove('highlight-visited-index');
        document.getElementById('hat-var3').classList.remove('highlight-item');
        document.getElementById('hat-var3').classList.remove('highlight-visited-index');

     
    
    
    updateMemory();
    updateVisual();
    updateCodeHighlight();
    updateStepExplanation();


}

// Run all iterations
function runAllIterations() {
    while (currentIteration < stepExplanations.length) {
        incrementLoop();
    }
}

// Update code highlight based on current iteration
function updateCodeHighlight() {
    const lines = ["line1", "counter", "item", "line2", "line3", "line4", "line5", "line6", "line7", "line8"];
    
    // Clear all highlights
    lines.forEach(line => {
        document.getElementById(line).classList.remove("highlight");
    });

    // Highlight the appropriate line based on currentIteration using if statements
    if (currentIteration === 0) {
        document.getElementById("line1").classList.add("highlight");
    } else if (currentIteration === 1) {
        document.getElementById("counter").classList.add("highlight");
    } else if (currentIteration === 2) {
        document.getElementById("item").classList.add("highlight");
    } else if (currentIteration === 3) {
        scaleApp();
        document.getElementById("line2").classList.add("highlight");
    } else if (currentIteration === 4) {
        document.getElementById("line3").classList.add("highlight");
    } else if (currentIteration === 5 || currentIteration === 7) {
        document.getElementById("line4").classList.add("highlight"); // Highlight else statement
    } 
    else if (currentIteration === 6 || currentIteration === 8) {
        document.getElementById("line7").classList.add("highlight"); // Highlight counter statement
    }else if (currentIteration === 9) {
        document.getElementById("line4").classList.add("highlight"); // Highlight if statement
    } else if (currentIteration === 10) {
        document.getElementById("line5").classList.add("highlight"); // Highlight inside if statement
    } else if (currentIteration === 11) {
        document.getElementById("line8").classList.add("highlight"); // Highlight the exit print statement
    }
}


function updateMemory() {
    const memorySearchingValue = document.getElementById('memory-searching-value');
    const memoryCounterValue = document.getElementById('memory-counter-value');
    const memoryItemValue = document.getElementById('memory-item-value');
    const memoryLstValue = document.getElementById('memory-lst-value');



    // Display and highlight based on the current step
    if (currentStep === 0) { // Initializing searching
        document.getElementById('memory-item').classList.add('hidden')
        document.getElementById('memory-counter').classList.add('hidden')
        document.getElementById('memory-lst').classList.add('hidden')
        if (searching) memorySearchingValue.innerText = 'True';
        else memorySearchingValue.innerText = 'False';
        memorySearchingValue.style.display = 'block'; // Show searching
        

        memorySearchingValue.style.backgroundColor = 'yellow';
        memorySearchingValue.style.border = '3px solid #ff6a00';


    } else if (currentStep === 1) { // Initializing counter
        document.getElementById('memory-item').classList.add('hidden')
        document.getElementById('memory-lst').classList.add('hidden')
        memorySearchingValue.style.backgroundColor = '#e8e8e8';
        memorySearchingValue.style.border = '1px solid #000000';
        document.getElementById('memory-counter').classList.remove('hidden')
        
        memoryCounterValue.innerText = counter;
        memoryCounterValue.style.display = 'block'; // Show counter

        memoryCounterValue.style.backgroundColor = 'yellow';
        memoryCounterValue.style.border = '3px solid #ff6a00';
        memoryCounterValue.innerText = 0;
        


    } else if (currentStep === 2) { // Initializing wanted_item
        document.getElementById('memory-lst').classList.add('hidden')
        memorySearchingValue.style.backgroundColor = '#e8e8e8';
        memorySearchingValue.style.border = '1px solid #000000';
        memoryCounterValue.style.backgroundColor = '#e8e8e8';
        memoryCounterValue.style.border = '1px solid #000000';

        document.getElementById('memory-item').classList.remove('hidden')


       
        memoryItemValue.innerText = wanted_item;
        memoryItemValue.style.display = 'block'; // Show wanted_item

        memoryItemValue.style.backgroundColor = 'yellow';
        memoryItemValue.style.border = '3px solid #ff6a00';
        memoryCounterValue.innerText = 0;


    } else if (currentStep === 3) { // Defining lst
        memorySearchingValue.style.backgroundColor = '#e8e8e8';
        memorySearchingValue.style.border = '1px solid #000000';
        memoryCounterValue.style.backgroundColor = '#e8e8e8';
        memoryCounterValue.style.border = '1px solid #000000';
        memoryItemValue.style.backgroundColor = '#e8e8e8';
        memoryItemValue.style.border = '1px solid #000000';

        document.getElementById('memory-lst').classList.remove('hidden')
        
        memoryLstValue.style.display = 'block'; // Show lst

        document.getElementById('cont0').style.backgroundColor = '';
        document.getElementById('cont0').style.border = '';

        document.getElementById('cont1').style.backgroundColor = '';
        document.getElementById('cont1').style.border = '';
        

        memoryLstValue.style.backgroundColor = 'yellow';
        memoryLstValue.style.border = '3px solid #ff6a00';
        memoryCounterValue.innerText = 0;




    } else if (currentStep === 4) { // Check while loop condition
        memoryCounterValue.innerText = 0;
        memorySearchingValue.style.backgroundColor = '#e8e8e8';
        memorySearchingValue.style.border = '1px solid #000000';
        memoryCounterValue.style.backgroundColor = '#e8e8e8';
        memoryCounterValue.style.border = '1px solid #000000';
        memoryItemValue.style.backgroundColor = '#e8e8e8';
        memoryItemValue.style.border = '1px solid #000000';
        memoryLstValue.style.backgroundColor = '#e8e8e8';
        memoryLstValue.style.border = '1px solid #000000';

        memoryItemValue.style.backgroundColor = '#e8e8e8';
        memoryItemValue.style.border = '1px solid #000000';

        document.getElementById('cont0').style.backgroundColor = '';
        document.getElementById('cont0').style.border = '';
        document.getElementById('cont1').style.backgroundColor = '';
        document.getElementById('cont1').style.border = '';

    } else if (currentStep === 5) { // Iteration 1 
        
        memoryCounterValue.innerText = 0;
        document.getElementById('cont0').style.backgroundColor = 'yellow';
        document.getElementById('cont0').style.border = '3px solid #ff6a00';
        // document.getElementById('val0').style.backgroundColor = 'yellow';
        // document.getElementById('val0').style.border = '3px solid #ff6a00';

        document.getElementById('var1').style.backgroundColor = '#e8e8e8';
        document.getElementById('var1').style.border = '1px solid #000000';
        document.getElementById('val1').style.backgroundColor = '#e8e8e8';
        document.getElementById('val1').style.border = '1px solid #000000';

        document.getElementById('var2').style.backgroundColor = '#e8e8e8';
        document.getElementById('var2').style.border = '1px solid #000000';
        document.getElementById('val2').style.backgroundColor = '#e8e8e8';
        document.getElementById('val2').style.border = '1px solid #000000';

        memoryCounterValue.style.backgroundColor = '#e8e8e8';
        memoryCounterValue.style.border = '1px solid #000000';

        memoryItemValue.style.backgroundColor = 'yellow';
        memoryItemValue.style.border = '3px solid #ff6a00';
        
        
        
    }
    else if (currentIteration === 6) { // Counter
        memoryCounterValue.innerText = 1;
        document.getElementById('cont0').style.backgroundColor = '#e8e8e8';
        document.getElementById('cont0').style.border = '';
        document.getElementById('cont1').style.backgroundColor = '#e8e8e8';
        document.getElementById('cont1').style.border = '';
        document.getElementById('val0').style.backgroundColor = '#e8e8e8';
        document.getElementById('val0').style.border = '1px solid #000000';
        document.getElementById('var0').style.backgroundColor = '#e8e8e8';
        document.getElementById('var0').style.border = '1px solid #000000';

        document.getElementById('var1').style.backgroundColor = '#e8e8e8';
        document.getElementById('var1').style.border = '1px solid #000000';
        document.getElementById('val1').style.backgroundColor = '#e8e8e8';
        document.getElementById('val1').style.border = '1px solid #000000';

        document.getElementById('var2').style.backgroundColor = '#e8e8e8';
        document.getElementById('var2').style.border = '1px solid #000000';
        document.getElementById('val2').style.backgroundColor = '#e8e8e8';
        document.getElementById('val2').style.border = '1px solid #000000';

        memoryCounterValue.style.backgroundColor = 'yellow';
        memoryCounterValue.style.border = '3px solid #ff6a00';

        memoryItemValue.style.backgroundColor = '#e8e8e8';
        memoryItemValue.style.border = '1px solid #000000';
      
    
    }
    else if (currentStep === 7) { // Iteration  2
        memoryCounterValue.innerText = 1;
        document.getElementById('cont1').style.backgroundColor = 'yellow';
        document.getElementById('cont1').style.border = '3px solid #ff6a00';
        // document.getElementById('val1').style.backgroundColor = 'yellow';
        // document.getElementById('val1').style.border = '3px solid #ff6a00';

        document.getElementById('var0').style.backgroundColor = 'lightblue';
        document.getElementById('var0').style.border = '1px solid #000000';
        document.getElementById('val0').style.backgroundColor = '#c8e6c9';
        document.getElementById('val0').style.border = '1px solid #9ccd8b';

        document.getElementById('var2').style.backgroundColor = '#e8e8e8';
        document.getElementById('var2').style.border = '1px solid #000000';
        document.getElementById('val2').style.backgroundColor = '#e8e8e8';
        document.getElementById('val2').style.border = '1px solid #000000';

        memoryCounterValue.style.backgroundColor = '#e8e8e8';
        memoryCounterValue.style.border = '1px solid #000000';
      
        memoryItemValue.style.backgroundColor = 'yellow';
        memoryItemValue.style.border = '3px solid #ff6a00';
    
    } 
     
    else if (currentIteration === 8) { // Counter
        memoryCounterValue.innerText = 2;
        document.getElementById('var0').style.backgroundColor = '#e8e8e8';
        document.getElementById('var0').style.border = '1px solid #000000';
        document.getElementById('val0').style.backgroundColor = '#e8e8e8';
        document.getElementById('val0').style.border = '1px solid #000000';

        document.getElementById('cont0').style.backgroundColor = '#e8e8e8';
        document.getElementById('cont0').style.border = '';
        document.getElementById('cont1').style.backgroundColor = '#e8e8e8';
        document.getElementById('cont1').style.border = '';

        document.getElementById('val1').style.backgroundColor = '#e8e8e8';
        document.getElementById('val1').style.border = '1px solid #000000';
        document.getElementById('var1').style.backgroundColor = '#e8e8e8';
        document.getElementById('var1').style.border = '1px solid #000000';

        document.getElementById('var2').style.backgroundColor = '#e8e8e8';
        document.getElementById('var2').style.border = '1px solid #000000';
        document.getElementById('val2').style.backgroundColor = '#e8e8e8';
        document.getElementById('val2').style.border = '1px solid #000000';

        memoryCounterValue.style.backgroundColor = 'yellow';
        memoryCounterValue.style.border = '3px solid #ff6a00';

        memoryItemValue.style.backgroundColor = '#e8e8e8';
        memoryItemValue.style.border = '1px solid #000000';
      
    
    } 
    else if (currentStep === 9) { // Iteration 3, if statement
        memoryCounterValue.innerText = 2;
        document.getElementById('var2').style.backgroundColor = 'yellow';
        document.getElementById('var2').style.border = '3px solid #ff6a00';
        document.getElementById('val2').style.backgroundColor = 'yellow';
        document.getElementById('val2').style.border = '3px solid #ff6a00';


        document.getElementById('var0').style.backgroundColor = 'lightblue';
        document.getElementById('var0').style.border = '1px solid #000000';
        document.getElementById('val0').style.backgroundColor = '#c8e6c9';
        document.getElementById('val0').style.border = '1px solid #9ccd8b';

        document.getElementById('var1').style.backgroundColor = 'lightblue';
        document.getElementById('var1').style.border = '1px solid #000000';
        document.getElementById('val1').style.backgroundColor = '#c8e6c9';
        document.getElementById('val1').style.border = '1px solid #9ccd8b';

        memoryCounterValue.style.backgroundColor = '#e8e8e8';
        memoryCounterValue.style.border = '1px solid #000000';

        memorySearchingValue.style.backgroundColor = '#e8e8e8';
        memorySearchingValue.style.border = '1px solid #000000';

        memoryItemValue.style.backgroundColor = 'yellow';
        memoryItemValue.style.border = '3px solid #ff6a00';



        
    } else if (currentStep === 10) { //Searching turns false
        memorySearchingValue.style.backgroundColor = 'yellow';
        memorySearchingValue.style.border = '3px solid #ff6a00';
        memorySearchingValue.innerText = 'False';

        document.getElementById('var0').style.backgroundColor = '#e8e8e8';
        document.getElementById('var0').style.border = '1px solid #000000';
        document.getElementById('val0').style.backgroundColor = '#e8e8e8';
        document.getElementById('val0').style.border = '1px solid #000000';

        document.getElementById('var1').style.backgroundColor = '#e8e8e8';
        document.getElementById('var1').style.border = '1px solid #000000';
        document.getElementById('val1').style.backgroundColor = '#e8e8e8';
        document.getElementById('val1').style.border = '1px solid #000000';

        document.getElementById('var2').style.backgroundColor = '#e8e8e8';
        document.getElementById('var2').style.border = '1px solid #000000';
        document.getElementById('val2').style.backgroundColor = '#e8e8e8';
        document.getElementById('val2').style.border = '1px solid #000000';

        memoryItemValue.style.backgroundColor = '#e8e8e8';
        memoryItemValue.style.border = '1px solid #000000';
        // No specific action needed for this step
    }
    else if (currentStep === 11) {

        memorySearchingValue.style.backgroundColor = '#e8e8e8';
        memorySearchingValue.style.border = '1px solid #000000';

        memoryItemValue.style.backgroundColor = '#e8e8e8';
        memoryItemValue.style.border = '1px solid #000000';

     }

}




// Update visual representation
function updateVisual() {
    
    const hat1 = document.getElementById('hat1-image');
    const hat2 = document.getElementById('hat2-image');
    const hat3 = document.getElementById('hat3-image');
    const hat4 = document.getElementById('hat4-image');

    const hatv1 = document.getElementById('hat-var1');
    const hatv2 = document.getElementById('hat-var2');
    const hatv3 = document.getElementById('hat-var3');


   

    if (currentStep === 0 || currentStep === 1 || currentStep === 2 ){
        //Make grey 
        hat1.src = 'hat-bl.PNG';
        hat2.src = 'hat-bl.PNG';
        hat3.src = 'hat-bl.PNG';
        hat4.src = 'hat-bl.PNG';


    }
    else if (currentStep === 3 || currentStep === 4){ //lst initalized
        hat1.src = 'hat.PNG';
        hat2.src = 'hat.PNG';
        hat3.src = 'hat.PNG';
        hat4.src = 'hat.PNG';
        hatv1.classList.remove('highlight-item');
    }
    
    else if (currentStep === 5 ){ //First hat Looked at 
        hat1.style.visibility = 'visible';
        hat1.src = 'hat-hl.PNG';
        hat2.src = 'hat.PNG';
        hat3.src = 'hat.PNG';
        hatv1.classList.remove('highlight-visited-index');
        hatv2.classList.remove('highlight-visited-index');
        hatv1.classList.add('highlight-item');
        hatv2.classList.remove('highlight-item');
        hatv3.classList.remove('highlight-item');
        
    }
    else if (currentStep === 6){ //First hat Looked at 
        hat1.style.visibility = 'hidden';
        hat2.src = 'hat.PNG';
        hat3.src = 'hat.PNG';
        hatv1.classList.remove('highlight-item');
        hatv2.classList.remove('highlight-visited-index');
        hatv1.classList.add('highlight-visited-index');
        hatv2.classList.remove('highlight-item');
        hatv3.classList.remove('highlight-item');
    }
    else if (currentStep === 7){ // Second Hat looked at
        hat2.style.visibility = 'visible';
       
        hat2.src = 'hat-hl.PNG';
        hat3.src = 'hat.PNG';
        hatv1.classList.remove('highlight-item');
        hatv2.classList.remove('highlight-visited-index');
        hatv1.classList.add('highlight-visited-index');
        hatv2.classList.add('highlight-item');
        hatv3.classList.remove('highlight-item');
        
    }
    else if (currentStep ===  8){ // Second Hat looked at
        hat2.style.visibility = 'hidden';
       
        hat2.src = 'hat-hl.PNG';
        hat3.src = 'hat.PNG';
        hatv1.classList.remove('highlight-item');
        
        hatv1.classList.add('highlight-visited-index');
        hatv2.classList.add('highlight-visited-index');
        hatv2.classList.remove('highlight-item');
        hatv3.classList.remove('highlight-item');
        
    }
    else if (currentStep === 9){ // Third Hat looked at
        hat1.src = 'hat.PNG';
        hat2.src = 'hat.PNG';
        hat3.src = 'hat-hl.PNG';
        hatv2.classList.remove('highlight-item');
        hatv3.classList.remove('highlight-visited-index');
        hatv2.classList.add('highlight-visited-index');
        hatv3.classList.add('highlight-item');
        
    }
    else if (currentStep === 10){ // Third Hat looked at
        hat1.src = 'hat.PNG';
        hat2.src = 'hat.PNG';
        hat3.src = 'rabbit.PNG';
        hatv3.classList.remove('highlight-item');
        hatv3.classList.add('highlight-visited-index');

    }
    
    
}

// Update step explanation
function updateStepExplanation() {
    const explanationDiv = document.getElementById('step-explanation');
    explanationDiv.innerHTML = stepExplanations[currentIteration] || "Program has finished executing.";
}

window.onload = () => {
    window.addEventListener('resize', scaleApp);
    window.addEventListener('load', scaleApp);
    updateCodeHighlight();
    updateMemory();
    updateVisual();
    updateStepExplanation();
};
