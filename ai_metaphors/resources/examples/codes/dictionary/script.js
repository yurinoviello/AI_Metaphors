let currentIteration = 0;
const maxIterations = 4; // Adjusted for your list length
let total = "";
const lst = ['item1', 'item2', 'Wanted Item Name', 'item4'];
let wantedItemInitialized = false;
let searching = true;
let counter = 0;
let wanted_item = 'Wanted Item Name';

let currentStep = 0;

// Step explanations
const stepExplanations = [
    'Define the dictionary <span class="variable">grades</span>', //0
    'Print output: 92', //1
    'Add to <span class="variable">grades</span> key <span class="variable">"David"</span> with value 88',//2
    'Print output: 88', //3
    'Update <span class="variable">grades</span> key <span class="variable">"Alice"</span> with value 90',//4
    'Print output: 90',//5
    'Searching <span class="variable">grades</span> for key <span class="variable">"Eve"</span>',//6
    'Print output: No Grade Found',//7
    
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

// Reset loop
function resetLoop() {
    currentIteration = 0;
    currentStep = 0;
    counter = 0;
    const student = document.getElementById('box-top-left');
    const reply = document.getElementById('box-bottom-right');
    const alice = document.getElementById('alice-val');
    const bob = document.getElementById('bob-val');
    
    const david = document.getElementById('david-val');

    document.getElementById('val1').style.backgroundColor = '#e8e8e8';
    document.getElementById('val1').style.border = '#e8e8e8';

    document.getElementById('cont3').style.visibility = 'hidden';
    document.getElementById('david-name').innerText = '';
    david.innerText = '';

        alice.style.backgroundColor = '';
        alice.style.border = '';
        alice.innerText = '85';

        student.innerText = '';
        reply.innerText = '';
        bob.style.backgroundColor = '';
        bob.style.border = '';

        david.style.backgroundColor = '';
        david.style.border = '';

        student.style.backgroundImage = "url('bubbleB.png')";
        reply.style.backgroundImage = "url('bubble.png')";

        document.getElementById('paper-line1').style.backgroundColor = '';
        document.getElementById('paper-line1').style.border = '';

        document.getElementById('paper-line2').style.backgroundColor = '';
        document.getElementById('paper-line2').style.border = '';

        document.getElementById('paper-line4').style.backgroundColor = '';
        document.getElementById('paper-line4').style.border = '';
    
       

     
    
    
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
    const lines = ["line1", "line2", "line3", "line4", "line5", "line6", "line7"];
    
    // Clear all highlights
    lines.forEach(line => {
        document.getElementById(line).classList.remove("highlight");
    });

    // Highlight the appropriate line based on currentIteration using if statements
    if (currentIteration === 0) {
        document.getElementById("line1").classList.add("highlight");
    } else if (currentIteration === 1) {
        document.getElementById("line2").classList.add("highlight");
    } else if (currentIteration === 2) {
        document.getElementById("line3").classList.add("highlight");
    } else if (currentIteration === 3) {
        document.getElementById("line4").classList.add("highlight");
    } else if (currentIteration === 4) {
        document.getElementById("line5").classList.add("highlight");
    } else if (currentIteration === 5 ) {
        document.getElementById("line6").classList.add("highlight"); 
    } 
    else if (currentIteration === 6) { 
        document.getElementById("line7").classList.add("highlight"); 


    }
}


function updateMemory() {
   
    const memoryLstValue = document.getElementById('memory-lst-value');



    // Display and highlight based on the current step
    if (currentStep === 0) { // Initializing searching
        memoryLstValue.style.display = 'block'; // Show lst

        document.getElementById('cont0').style.backgroundColor = '';
        document.getElementById('cont0').style.border = '';

        document.getElementById('cont1').style.backgroundColor = '';
        document.getElementById('cont1').style.border = '';

        document.getElementById('cont2').style.backgroundColor = '';
        document.getElementById('cont2').style.border = '';

        document.getElementById('cont3').style.visibility = 'hidden';
        // document.getElementById('cont3').style.visibility = 'visible';
       
        

        memoryLstValue.style.backgroundColor = 'yellow';
        memoryLstValue.style.border = '3px solid #ff6a00';
        document.getElementById('val1').style.backgroundColor = '#e8e8e8';
        document.getElementById('val1').style.border = '1px solid #000000';
        
      


    } else if (currentStep === 1) { 

        memoryLstValue.style.backgroundColor = '#e8e8e8';
        memoryLstValue.style.border = '#e8e8e8';


        document.getElementById('val1').style.backgroundColor = 'yellow';
        document.getElementById('val1').style.border = '3px solid #ff6a00';

        document.getElementById('cont3').style.visibility = 'hidden';
   
        


    } else if (currentStep === 2) { 
        document.getElementById('val1').style.backgroundColor = '#e8e8e8';
        document.getElementById('val1').style.border = '1px solid #000000';

        document.getElementById('cont3').style.visibility = 'visible';

        document.getElementById('cont3').style.backgroundColor = 'yellow';
        document.getElementById('cont3').style.border = '3px solid #ff6a00';
        document.getElementById('val3').style.backgroundColor = '#e8e8e8';
        document.getElementById('val3').style.border = '1px solid #000000';
       


    } else if (currentStep === 3) { 
        document.getElementById('cont3').style.backgroundColor = '#e8e8e8';
        document.getElementById('cont3').style.border = '#e8e8e8';

        document.getElementById('val1').style.backgroundColor = '#e8e8e8';
        document.getElementById('val1').style.border = '1px solid #000000';

        document.getElementById('val0').style.backgroundColor = '#e8e8e8';
        document.getElementById('val0').style.border = '1px solid #000000';

        document.getElementById('val3').style.backgroundColor = 'yellow';
        document.getElementById('val3').style.border = '3px solid #ff6a00';
        
        document.getElementById('cont0').style.backgroundColor = '#e8e8e8';
        document.getElementById('cont0').style.border = '#e8e8e8';

        




    } else if (currentStep === 4) { 

        document.getElementById('cont3').style.backgroundColor = '#e8e8e8';
        document.getElementById('cont3').style.border = '#e8e8e8';

        document.getElementById('val1').style.backgroundColor = '#e8e8e8';
        document.getElementById('val1').style.border = '1px solid #000000';

        document.getElementById('val3').style.backgroundColor = '#e8e8e8';
        document.getElementById('val3').style.border = '1px solid #000000';

        document.getElementById('cont0').style.backgroundColor = 'yellow';
        document.getElementById('cont0').style.border = '3px solid #ff6a00';
        document.getElementById('val0').innerText = 90;

        document.getElementById('val0').style.backgroundColor = '#e8e8e8';
        document.getElementById('val0').style.border = '1px solid #000000';

       
       

    } else if (currentStep === 5) { 
        document.getElementById('cont3').style.backgroundColor = '#e8e8e8';
        document.getElementById('cont3').style.border = '#e8e8e8';

        document.getElementById('cont0').style.backgroundColor = '#e8e8e8';
        document.getElementById('cont0').style.border = '#e8e8e8';

        document.getElementById('val1').style.backgroundColor = '#e8e8e8';
        document.getElementById('val1').style.border = '1px solid #000000';

        document.getElementById('val0').style.backgroundColor = 'yellow';
        document.getElementById('val0').style.border = '3px solid #ff6a00';

         memoryLstValue.style.backgroundColor = '#e8e8e8';
        memoryLstValue.style.border = '1px solid #000000';
        

        
      
        
        
        
    }
    else if (currentIteration === 6) { // nothing
        document.getElementById('val0').style.backgroundColor = '#e8e8e8';
        document.getElementById('val0').style.border = '1px solid #000000';
         memoryLstValue.style.backgroundColor = 'yellow';
        memoryLstValue.style.border = '3px solid #ff6a00';

        document.getElementById('cont0').style.backgroundColor = '';
        document.getElementById('cont0').style.border = '';

        document.getElementById('cont1').style.backgroundColor = '';
        document.getElementById('cont1').style.border = '';

        document.getElementById('cont2').style.backgroundColor = '';
        document.getElementById('cont2').style.border = '';
        
      
    
    }
    else if(currentIteration === 7){
        memoryLstValue.style.backgroundColor = '#e8e8e8';
        memoryLstValue.style.border = '1px solid #000000';

    }
    
    
    
     

}




// Update visual representation
function updateVisual() {
    const student = document.getElementById('box-top-left');
    const reply = document.getElementById('box-bottom-right');
    const alice = document.getElementById('alice-val');
    const bob = document.getElementById('bob-val');
    
    const david = document.getElementById('david-val');
    const gb = document.getElementById('grade-book');


   

    if (currentStep === 0){
        //Highlight around the grade book
        gb.style.backgroundColor = 'yellow';
        gb.style.border = '3px solid #ff6a00';

        student.innerText = '';
        reply.innerText = '';

        bob.style.backgroundColor = '';
        bob.style.border = '';

        alice.style.backgroundColor = '';
        alice.style.border = '';
        alice.innerText = '85';

        david.style.backgroundColor = '';
        david.style.border = '';

        student.style.backgroundImage = "url('bubbleB.png')";
        reply.style.backgroundImage = "url('bubble.png')";

        document.getElementById('paper-line1').style.backgroundColor = '';
        document.getElementById('paper-line1').style.border = '';

        document.getElementById('paper-line2').style.backgroundColor = '';
        document.getElementById('paper-line2').style.border = '';

        document.getElementById('paper-line4').style.backgroundColor = '';
        document.getElementById('paper-line4').style.border = '';
        

    }
    else if (currentStep === 1){
        gb.style.backgroundColor = '';
        gb.style.border = '';

        student.innerText =  '\nBob:\nWhat is my\ngrade?';
        reply.innerText = '\n92';

        bob.style.backgroundColor = 'yellow';
        bob.style.border = '3px solid #ff6a00';

        student.style.backgroundImage = "url('bubbleB.png')";
        reply.style.backgroundImage = "url('bubble-hl.png')";

        //Bob: What is my grade
        //Highlight line in grade book
        //Reply: 92


        document.getElementById('david-name').innerText = '';
        david.innerText = '';
        document.getElementById('paper-line4').style.backgroundColor = '';
        document.getElementById('paper-line4').style.border = '';
       
    }
    else if (currentStep === 2){

        student.innerText =  '\nDavid: I just \nhanded in my\ntest';
        reply.innerText = '\nOkay, adding\n David and their \ngrade.';

        bob.style.backgroundColor = '';
        bob.style.border = '';

        david.style.backgroundColor = '';
        david.style.border = '';

        document.getElementById('paper-line4').style.backgroundColor = 'yellow';
        document.getElementById('paper-line4').style.border = '3px solid #ff6a00';

        document.getElementById('david-name').innerText = 'David:\t';
        david.innerText = ' 88';

        
       
    }
    else if (currentStep === 3){
        document.getElementById('paper-line4').style.backgroundColor = '';
        document.getElementById('paper-line4').style.border = '';
        student.innerText =  '\nDavid:\nWhat is my\ngrade?';
        reply.innerText = '\n88';
        
       
        david.style.backgroundColor = 'yellow';
        david.style.border = '3px solid #ff6a00';

        alice.style.backgroundColor = '';
        alice.style.border = '';
        alice.innerText = '85';

        document.getElementById('paper-line1').style.backgroundColor = '';
        document.getElementById('paper-line1').style.border = '';
       
    }
    else if (currentStep === 4){
        david.style.backgroundColor = '';
        david.style.border = '';

        student.innerText =  '\nAlice: I \nneed a regrade.\n Should be 90';
        reply.innerText = '\nOkay, updating\n Alice grade';
        alice.style.backgroundColor = '';
        alice.style.border = '';

        document.getElementById('paper-line1').style.backgroundColor = 'yellow';
        document.getElementById('paper-line1').style.border = '3px solid #ff6a00';
        alice.innerText = ' 90';
      
       
    }
    
    else if (currentStep === 5 ){ 

        document.getElementById('paper-line1').style.backgroundColor = '';
        document.getElementById('paper-line1').style.border = '';

        student.innerText =  '\nAlice:\nWhat is my\ngrade?';
        reply.innerText = '\n90';
        alice.style.backgroundColor = 'yellow';
        alice.style.border = '3px solid #ff6a00';
        //Alice: What is my grade
        //Reply: 90
        reply.style.backgroundImage = "url('bubble-hl.png')";

        gb.style.backgroundColor = '';
        gb.style.border = '';
     
        
    }
    else if (currentStep === 6 ){
        alice.style.backgroundColor = '';
        alice.style.border = '';

        student.innerText =  '\nEve:\nWhat is my\ngrade?';
        reply.innerText = '\nSearching for\n Eve.';
        reply.style.backgroundImage = "url('bubble.png')";

        
        gb.style.backgroundColor = 'yellow';
        gb.style.border = '3px solid #ff6a00';
        david.style.backgroundColor = '';


        
    }
    else if (currentStep === 7){ 
        //Reply: No grade found. 
        gb.style.backgroundColor = '';
        gb.style.border = '';
        reply.innerText = '\nNo student \nfound. So no\n grade exists.';
        david.style.backgroundColor = '';
        alice.style.backgroundColor = '';

        reply.style.backgroundImage = "url('bubble-hl.png')";
       
        
    }
   
    
    
}

// Update step explanation
function updateStepExplanation() {
    const explanationDiv = document.getElementById('step-explanation');
    explanationDiv.innerHTML = stepExplanations[currentIteration] || "Program has finished executing.";
}

window.onload = () => {
    updateCodeHighlight();
    updateMemory();
    updateVisual();
    updateStepExplanation();
};
