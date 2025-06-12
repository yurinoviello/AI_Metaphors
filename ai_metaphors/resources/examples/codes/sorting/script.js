let currentIteration = 0;
const maxIterations = 4; // Adjusted for your list length
let total = "";
const lst = ['item1', 'item2', 'Wanted Item Name', 'item4'];
let wantedItemInitialized = false;
let searching = true;
let counter = 0;
let wanted_item = 'Wanted Item Name';

let i = 0;
let j = 0;


let currentStep = 0;

// Step explanations
const stepExplanations = [
    'Define the list <span class="variable">lst</span>', //0
    'Define the variable <span class="variable">n</span> to the length of lst', //1
    'Enter outer loop: <span class="variable">i</span> = 0',//2 HIGHLIGHT OUTER and I
    'Enter inner loop: <span class="variable">j</span> = = 0', //3 HIGHLIGHT INNER and J
    'Compare lst[j] > lst[j+1] ',//4 HIGHLIGHT THIS LINE
    'Since 4 > 2, swap them. Now <span class="variable">lst</span> is [2, 4, 3, 1]',//5 HIGHLIGHT THE LST VAR and inside if statment
    'Re-enter inner loop: <span class="variable">j</span> = = 1',//6
    'Compare lst[j]  > lst[j+1]  ',//7
    'Since 4 > 3, swap them. Now <span class="variable">lst</span> is [2, 3, 4, 1]',//8
    'Re-enter inner loop: <span class="variable">j</span> = 2',//9
    'Compare lst[j] > lst[j+1]  ',//10
    'Since 4 > 1, swap them. Now <span class="variable">lst</span> is [2, 3, 1, 4] ',//11
    'Re-enter outer loop: <span class="variable">i</span> = 1',//12
    'Enter inner loop: <span class="variable">j</span> = 0', //13
    'Compare lst[j]  > lst[j+1]  ',//14
    'Since 2 !> 3, do not swap them. <span class="variable">lst</span> is still  [2, 3, 1, 4]',//15
    'Re-enter inner loop: <span class="variable">j</span> = 1', //16
    'Compare lst[j] > lst[j+1] ',//17
    'Since 3 > 1, swap them. Now <span class="variable">lst</span> is [2, 1, 3, 4] ',//18
    'Re-enter outer loop: <span class="variable">i</span> = 2',//19
    'Enter inner loop: <span class="variable">j</span> = 0', //20
    'Compare lst[j] > lst[j+1] ',//21
    'Since 2 > 1, swap them. Now <span class="variable">lst</span> is [1, 2, 3, 4]',//22
    'From now on all lst[j] !> lst[j + 1] because list is sorted', //23
    'Re-enter outer loop: <span class="variable">i</span> = 3',//24
    'Now <span class="variable">n</span> - <span class="variable">i</span> - 1 = 0. Does not enter inner loop.', //25
    'Exit Outer Loop. Now lst is sorted: [1, 2, 3, 4]' //26
    
   
];

// Initialize Firebase
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
const dbSorting = firebase.firestore().collection('sorting'); // Using "sorting" collection

const userId = 'user-' + Date.now() + '-' + Math.floor(Math.random() * 10000);

// Logging function
function logInteraction(eventType, details) {
    dbSorting.add({
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


// Increment loop iteration
function incrementLoop() {
    if (currentIteration < stepExplanations.length) {
        
        
        currentIteration++;
        currentStep++;

        updateMemory();
        updateVisual();
        updateCodeHighlight();
        updateStepExplanation();
        // Log the interaction
        logInteraction('incrementLoop', { currentIteration: currentIteration, currentStep: currentStep });
    } else {
        alert("Program has finished executing.");
        logInteraction('alert', { message: "Program has finished executing." });
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
        logInteraction('decrementLoop', { currentIteration: currentIteration, currentStep: currentStep });
    } else {
        alert("Already at the start of the loop.");
        logInteraction('alert', { message: "Already at the start of the loop." });
    }
}

// Reset loop
function resetLoop() {
    currentIteration = 0;
    currentStep = 0;
    counter = 0;

    const blocks = ["block1","block2", "block3", "block4" ];
    document.getElementById("block1").src = "block4.png";
    document.getElementById("block2").src = "block2.png";
    document.getElementById("block3").src = "block3.png";
    document.getElementById("block4").src = "block1.png";

    blocks.forEach(con => {
        document.getElementById(con).style.backgroundColor = '#e8e8e8';
        document.getElementById(con).style.border = '';
       
    });
    
   
    const vars = ["block-var1","block-var2", "block-var3", "block-var4" ];
    
    // Clear all highlights
    vars.forEach(con => {
        document.getElementById(con).style.backgroundColor = '#e8e8e8';
        document.getElementById(con).style.border = '1px solid #000000';
    });

    const pointers = ["pointer1","pointer2", "pointer3", "pointer4" ];
    
    // Clear all highlights
    pointers.forEach(con => {
        document.getElementById(con).style.visibility = 'hidden';
       
    });

    document.getElementById('val0').innerText = "4";
    document.getElementById('val1').innerText = "2";
    document.getElementById('val2').innerText = "3";
    document.getElementById('val3').innerText = "1";


     
    
    
    updateMemory();
    updateVisual();
    updateCodeHighlight();
    updateStepExplanation();

    logInteraction('resetLoop', { currentIteration: currentIteration, currentStep: currentStep });
}

// Run all iterations
function runAllIterations() {
    while (currentIteration < stepExplanations.length) {
        incrementLoop();
    }
    logInteraction('runAllIterations', { finalIteration: currentIteration, finalStep: currentStep });
}

// Update code highlight based on current iteration
function updateCodeHighlight() {
    const lines = ["line1", "line2", "line3", "line4", "line5", "line6", "line7"];
    
    // Clear all highlights
    lines.forEach(line => {
        document.getElementById(line).classList.remove("highlight");
    });

    // Highlight the appropriate line based on currentIteration using if statements
    if (currentIteration === 0) { // highlight define lst


        document.getElementById("line1").classList.add("highlight");
    } else if (currentIteration === 1) { // highlight define n 

        document.getElementById("line2").classList.add("highlight");

    } else if (currentIteration === 2 || currentIteration === 12 || currentIteration === 19 || currentIteration === 24 || currentIteration === 25) { // highlight outer loop

        document.getElementById("line3").classList.add("highlight");

    } else if (currentIteration === 3 || currentIteration === 6 || currentIteration === 9 || currentIteration === 13 || currentIteration === 16 || currentIteration === 20) { // highlight inner loop


        document.getElementById("line4").classList.add("highlight");

    } else if (currentIteration === 4 || currentIteration === 7 || currentIteration === 10 || currentIteration === 14 || currentIteration === 17 || currentIteration === 21) { //highlight if statment (compare)

        document.getElementById("line5").classList.add("highlight");

    } else if (currentIteration === 5 || currentIteration === 8 || currentIteration === 11 || currentIteration === 15 || currentIteration === 18 || currentIteration === 22) { // highlight inside if statment
        document.getElementById("line6").classList.add("highlight"); 

    } 
    else if (currentIteration === 26) { //highlight end of program
        document.getElementById("line7").classList.add("highlight"); 


    }
}


function updateMemory() {

    const lines = ["memory-lst-value", "memory-lst-var", "memory-i-value", "memory-j-value", "memory-n-value", "n-var", "i-var", "j-var", "val0", "val1", "val2", "val3"];
    
    // Clear all highlights
    lines.forEach(line => {
        document.getElementById(line).style.backgroundColor = '#e8e8e8';
        document.getElementById(line).style.border = '1px solid #000000';
    });

    const conts = ["cont0","cont1", "cont2", "cont3" ];
    
    // Clear all highlights
    conts.forEach(con => {
        document.getElementById(con).style.backgroundColor = '';
        document.getElementById(con).style.border = '';
    });


  
    const memoryLstValue = document.getElementById('memory-lst-value');
    const memoryLstVar = document.getElementById('memory-lst-var');
    
    const memoryi = document.getElementById('memory-i');
    const memoryj = document.getElementById('memory-j');
    const memoryn = document.getElementById('memory-n');

    const nval = document.getElementById('memory-n-value');
    const nvar = document.getElementById('n-var');


    if (currentStep === 0) { // Initializing searching
        memoryi.style.visibility = 'hidden';
        memoryj.style.visibility = 'hidden';
        memoryn.style.visibility = 'hidden';
       
        

        memoryLstValue.style.backgroundColor = 'yellow';
        memoryLstValue.style.border = '3px solid #ff6a00';

        memoryLstVar.style.backgroundColor = 'yellow';
        memoryLstVar.style.border = '3px solid #ff6a00';
      

    } else if (currentStep === 1) { 

        

        
        memoryn.style.visibility = 'visible';
        nval.style.backgroundColor = 'yellow';
        nval.style.border = '3px solid #ff6a00'; 

        nvar.style.backgroundColor = 'yellow';
        nvar.style.border = '3px solid #ff6a00'; 

        memoryi.style.visibility = 'hidden'; 


       

    } else if (currentStep === 2) { 
       

        memoryi.style.visibility = 'visible';
        document.getElementById('i-var').style.backgroundColor = 'yellow';
        document.getElementById('i-var').style.border = '3px solid #ff6a00';
        document.getElementById('memory-i-value').style.backgroundColor = 'yellow';
        document.getElementById('memory-i-value').style.border = '3px solid #ff6a00';

        memoryj.style.visibility = 'hidden';
        
       


    } else if (currentStep === 3) { 
       

        memoryj.style.visibility = 'visible';
        document.getElementById('j-var').style.backgroundColor = 'yellow';
        document.getElementById('j-var').style.border = '3px solid #ff6a00';
        document.getElementById('memory-j-value').style.backgroundColor = 'yellow';
        document.getElementById('memory-j-value').style.border = '3px solid #ff6a00';

    } else if (currentStep === 4) { 

        document.getElementById('cont0').style.backgroundColor = 'yellow';
        document.getElementById('cont0').style.border = '3px solid #ff6a00';

        document.getElementById('cont1').style.backgroundColor = 'yellow';
        document.getElementById('cont1').style.border = '3px solid #ff6a00';

        document.getElementById('val0').innerText = "4";
        document.getElementById('val1').innerText = "2";
       

    } else if (currentStep === 5) { 
        document.getElementById('val0').style.backgroundColor = 'yellow';
        document.getElementById('val0').style.border = '3px solid #ff6a00';

        document.getElementById('val1').style.backgroundColor = 'yellow';
        document.getElementById('val1').style.border = '3px solid #ff6a00';

        document.getElementById('val0').innerText = "2";
        document.getElementById('val1').innerText = "4";

        document.getElementById('memory-j-value').innerText = "0";
       
    
    }
    else if (currentIteration === 6) { 
        document.getElementById('memory-j-value').style.backgroundColor = 'yellow';
        document.getElementById('memory-j-value').style.border = '3px solid #ff6a00';

        document.getElementById('memory-j-value').innerText = "1";
       
      
    
    }
    else if (currentIteration === 7) { 
        document.getElementById('cont2').style.backgroundColor = 'yellow';
        document.getElementById('cont2').style.border = '3px solid #ff6a00';

        document.getElementById('cont1').style.backgroundColor = 'yellow';
        document.getElementById('cont1').style.border = '3px solid #ff6a00';

        document.getElementById('val2').innerText = "3";
        document.getElementById('val1').innerText = "4";

    }
    else if (currentStep === 8) { 
        document.getElementById('val2').style.backgroundColor = 'yellow';
        document.getElementById('val2').style.border = '3px solid #ff6a00';

        document.getElementById('val1').style.backgroundColor = 'yellow';
        document.getElementById('val1').style.border = '3px solid #ff6a00';

        document.getElementById('val2').innerText = "4";
        document.getElementById('val1').innerText = "3";

        document.getElementById('memory-j-value').innerText = "1";
       
    
    }
    else if (currentIteration === 9) { 
        document.getElementById('memory-j-value').style.backgroundColor = 'yellow';
        document.getElementById('memory-j-value').style.border = '3px solid #ff6a00';

        document.getElementById('memory-j-value').innerText = "2";
       
      
    
    }
    else if (currentIteration === 10) { 
        document.getElementById('cont2').style.backgroundColor = 'yellow';
        document.getElementById('cont2').style.border = '3px solid #ff6a00';

        document.getElementById('cont3').style.backgroundColor = 'yellow';
        document.getElementById('cont3').style.border = '3px solid #ff6a00';

        document.getElementById('val2').innerText = "4";
        document.getElementById('val3').innerText = "1";

    }
    else if (currentStep === 11) { 
        document.getElementById('val2').style.backgroundColor = 'yellow';
        document.getElementById('val2').style.border = '3px solid #ff6a00';

        document.getElementById('val3').style.backgroundColor = 'yellow';
        document.getElementById('val3').style.border = '3px solid #ff6a00';

        document.getElementById('val2').innerText = "1";
        document.getElementById('val3').innerText = "4";

        document.getElementById('memory-i-value').innerText = "0";
       
    
    }
    else if (currentIteration === 12) { 
        document.getElementById('memory-i-value').style.backgroundColor = 'yellow';
        document.getElementById('memory-i-value').style.border = '3px solid #ff6a00';

        document.getElementById('memory-i-value').innerText = "1";
        document.getElementById('memory-j-value').innerText = "2";
       
      
    
    }
    else if (currentIteration === 13) { 
        document.getElementById('memory-j-value').style.backgroundColor = 'yellow';
        document.getElementById('memory-j-value').style.border = '3px solid #ff6a00';

        document.getElementById('memory-j-value').innerText = "0";
       
    }
    else if (currentIteration === 14) { 
        document.getElementById('cont1').style.backgroundColor = 'yellow';
        document.getElementById('cont1').style.border = '3px solid #ff6a00';

        document.getElementById('cont0').style.backgroundColor = 'yellow';
        document.getElementById('cont0').style.border = '3px solid #ff6a00';

    }
    else if (currentStep === 15) { 
        document.getElementById('val1').style.backgroundColor = 'yellow';
        document.getElementById('val1').style.border = '3px solid #ff6a00';

        document.getElementById('val0').style.backgroundColor = 'yellow';
        document.getElementById('val0').style.border = '3px solid #ff6a00';

        document.getElementById('memory-j-value').innerText = "0";

     
       
    
    }
    else if (currentIteration === 16) { 
        document.getElementById('memory-j-value').style.backgroundColor = 'yellow';
        document.getElementById('memory-j-value').style.border = '3px solid #ff6a00';

        document.getElementById('memory-j-value').innerText = "1";
       
    }
    else if (currentIteration === 17) { 
        document.getElementById('cont2').style.backgroundColor = 'yellow';
        document.getElementById('cont2').style.border = '3px solid #ff6a00';

        document.getElementById('cont1').style.backgroundColor = 'yellow';
        document.getElementById('cont1').style.border = '3px solid #ff6a00';

        document.getElementById('val2').innerText = "1";
        document.getElementById('val1').innerText = "3";

    }
    else if (currentStep === 18) { 
        document.getElementById('val2').style.backgroundColor = 'yellow';
        document.getElementById('val2').style.border = '3px solid #ff6a00';

        document.getElementById('val1').style.backgroundColor = 'yellow';
        document.getElementById('val1').style.border = '3px solid #ff6a00';

        document.getElementById('val2').innerText = "3";
        document.getElementById('val1').innerText = "1";

        document.getElementById('memory-i-value').innerText = "1";
       
    
    }
    else if (currentIteration === 19) { 
        document.getElementById('memory-i-value').style.backgroundColor = 'yellow';
        document.getElementById('memory-i-value').style.border = '3px solid #ff6a00';

        document.getElementById('memory-i-value').innerText = "2";
        document.getElementById('memory-j-value').innerText = "1";
       
      
    
    }
    else if (currentIteration === 20) { 
        document.getElementById('memory-j-value').style.backgroundColor = 'yellow';
        document.getElementById('memory-j-value').style.border = '3px solid #ff6a00';

        document.getElementById('memory-j-value').innerText = "0";
       
    }
    else if (currentIteration === 21) { 
        document.getElementById('cont0').style.backgroundColor = 'yellow';
        document.getElementById('cont0').style.border = '3px solid #ff6a00';

        document.getElementById('cont1').style.backgroundColor = 'yellow';
        document.getElementById('cont1').style.border = '3px solid #ff6a00';

        document.getElementById('val0').innerText = "2";
        document.getElementById('val1').innerText = "1";

    }
    else if (currentStep === 22) { 
        document.getElementById('val0').style.backgroundColor = 'yellow';
        document.getElementById('val0').style.border = '3px solid #ff6a00';

        document.getElementById('val1').style.backgroundColor = 'yellow';
        document.getElementById('val1').style.border = '3px solid #ff6a00';

        document.getElementById('val0').innerText = "1";
        document.getElementById('val1').innerText = "2";
       
    
    }
    
    
     

}




// Update visual representation
function updateVisual() {
    
    const blocks = ["block1","block2", "block3", "block4" ];

    blocks.forEach(con => {
        document.getElementById(con).style.backgroundColor = '';
        document.getElementById(con).style.border = '';
       
    });
    
   
    const vars = ["block-var1","block-var2", "block-var3", "block-var4" ];
    
    // Clear all highlights
    vars.forEach(con => {
        document.getElementById(con).style.backgroundColor = '#e8e8e8';
        document.getElementById(con).style.border = '1px solid #000000';
    });

    const pointers = ["pointer1","pointer2", "pointer3", "pointer4" ];
    
   
    pointers.forEach(con => {
        document.getElementById(con).style.visibility = 'hidden';
       
    });
    if (currentStep === 0){
        document.getElementById("block1").src = "block4.png";
        document.getElementById("block2").src = "block2.png";
        document.getElementById("block3").src = "block3.png";
        document.getElementById("block4").src = "block1.png";

        
    }

    else if (currentStep === 4){
      
        
        
        document.getElementById("block1").style.backgroundColor = 'yellow';
        document.getElementById("block1").style.border = '3px solid #ff6a00';

        document.getElementById("block2").style.backgroundColor = 'yellow';
        document.getElementById("block2").style.border = '3px solid #ff6a00';

        document.getElementById("block-var1").style.backgroundColor = 'yellow';
        document.getElementById("block-var1").style.border = '3px solid #ff6a00';

        document.getElementById("block-var2").style.backgroundColor = 'yellow';
        document.getElementById("block-var2").style.border = '3px solid #ff6a00';

        // document.getElementById("pointer1").style.visibility = 'visible';
        // document.getElementById("pointer2").style.visibility = 'visible';

        document.getElementById("block1").src = "block4.png";
        document.getElementById("block2").src = "block2.png";

    }
    else if (currentStep === 5){
        document.getElementById("block1").style.backgroundColor = 'yellow';
        document.getElementById("block1").style.border = '3px solid #ff6a00';

        document.getElementById("block2").style.backgroundColor = 'yellow';
        document.getElementById("block2").style.border = '3px solid #ff6a00';

        document.getElementById("block1").src = "block2.png";
        document.getElementById("block2").src = "block4.png";



        // document.getElementById("pointer1").style.visibility = 'visible';
        // document.getElementById("pointer2").style.visibility = 'visible';
       
       
        
    }
    else if (currentStep === 7){
        document.getElementById("block3").style.backgroundColor = 'yellow';
        document.getElementById("block3").style.border = '3px solid #ff6a00';

        document.getElementById("block2").style.backgroundColor = 'yellow';
        document.getElementById("block2").style.border = '3px solid #ff6a00';

        document.getElementById("block-var3").style.backgroundColor = 'yellow';
        document.getElementById("block-var3").style.border = '3px solid #ff6a00';

        document.getElementById("block-var2").style.backgroundColor = 'yellow';
        document.getElementById("block-var2").style.border = '3px solid #ff6a00';

        // document.getElementById("pointer3").style.visibility = 'visible';
        // document.getElementById("pointer2").style.visibility = 'visible';

        document.getElementById("block3").src = "block3.png";
        document.getElementById("block2").src = "block4.png";
      

        
    }
    else if (currentStep === 8){
        document.getElementById("block3").style.backgroundColor = 'yellow';
        document.getElementById("block3").style.border = '3px solid #ff6a00';

        document.getElementById("block2").style.backgroundColor = 'yellow';
        document.getElementById("block2").style.border = '3px solid #ff6a00';

        document.getElementById("block3").src = "block4.png";
        document.getElementById("block2").src = "block3.png";



        // document.getElementById("pointer3").style.visibility = 'visible';
        // document.getElementById("pointer2").style.visibility = 'visible';
        
    }
    else if (currentStep === 10){
        document.getElementById("block3").style.backgroundColor = 'yellow';
        document.getElementById("block3").style.border = '3px solid #ff6a00';

        document.getElementById("block4").style.backgroundColor = 'yellow';
        document.getElementById("block4").style.border = '3px solid #ff6a00';

        document.getElementById("block-var3").style.backgroundColor = 'yellow';
        document.getElementById("block-var3").style.border = '3px solid #ff6a00';

        document.getElementById("block-var4").style.backgroundColor = 'yellow';
        document.getElementById("block-var4").style.border = '3px solid #ff6a00';

        // document.getElementById("pointer3").style.visibility = 'visible';
        // document.getElementById("pointer4").style.visibility = 'visible';

        document.getElementById("block3").src = "block4.png";
        document.getElementById("block4").src = "block1.png";
       
       
    }
    
    else if (currentStep === 11 ){ 
        document.getElementById("block3").style.backgroundColor = 'yellow';
        document.getElementById("block3").style.border = '3px solid #ff6a00';

        document.getElementById("block4").style.backgroundColor = 'yellow';
        document.getElementById("block4").style.border = '3px solid #ff6a00';

        document.getElementById("block3").src = "block1.png";
        document.getElementById("block4").src = "block4.png";

        // document.getElementById("pointer3").style.visibility = 'visible';
        // document.getElementById("pointer4").style.visibility = 'visible';

        
     
        
    }
    else if (currentStep === 14 ){

        document.getElementById("block1").style.backgroundColor = 'yellow';
        document.getElementById("block1").style.border = '3px solid #ff6a00';

        document.getElementById("block2").style.backgroundColor = 'yellow';
        document.getElementById("block2").style.border = '3px solid #ff6a00';

        document.getElementById("block-var1").style.backgroundColor = 'yellow';
        document.getElementById("block-var1").style.border = '3px solid #ff6a00';

        document.getElementById("block-var2").style.backgroundColor = 'yellow';
        document.getElementById("block-var2").style.border = '3px solid #ff6a00';

        // document.getElementById("pointer1").style.visibility = 'visible';
        // document.getElementById("pointer2").style.visibility = 'visible';

      

        
    }
    else if (currentStep === 15){ 
        document.getElementById("block1").style.backgroundColor = 'yellow';
        document.getElementById("block1").style.border = '3px solid #ff6a00';

        document.getElementById("block2").style.backgroundColor = 'yellow';
        document.getElementById("block2").style.border = '3px solid #ff6a00';

        // document.getElementById("pointer1").style.visibility = 'visible';
        // document.getElementById("pointer2").style.visibility = 'visible';

        
    }
    else if (currentStep === 17 ){

        document.getElementById("block3").style.backgroundColor = 'yellow';
        document.getElementById("block3").style.border = '3px solid #ff6a00';

        document.getElementById("block2").style.backgroundColor = 'yellow';
        document.getElementById("block2").style.border = '3px solid #ff6a00';

        document.getElementById("block-var3").style.backgroundColor = 'yellow';
        document.getElementById("block-var3").style.border = '3px solid #ff6a00';

        document.getElementById("block-var2").style.backgroundColor = 'yellow';
        document.getElementById("block-var2").style.border = '3px solid #ff6a00';

        // document.getElementById("pointer2").style.visibility = 'visible';
        // document.getElementById("pointer3").style.visibility = 'visible';

        document.getElementById("block2").src = "block3.png";
        document.getElementById("block3").src = "block1.png";

      

        
    }
    else if (currentStep === 18){ 
        document.getElementById("block3").style.backgroundColor = 'yellow';
        document.getElementById("block3").style.border = '3px solid #ff6a00';

        document.getElementById("block2").style.backgroundColor = 'yellow';
        document.getElementById("block2").style.border = '3px solid #ff6a00';

        // document.getElementById("pointer3").style.visibility = 'visible';
        // document.getElementById("pointer2").style.visibility = 'visible';

        document.getElementById("block2").src = "block1.png";
        document.getElementById("block3").src = "block3.png";
       
        
    }
    else if (currentStep === 21 ){

        document.getElementById("block1").style.backgroundColor = 'yellow';
        document.getElementById("block1").style.border = '3px solid #ff6a00';

        document.getElementById("block2").style.backgroundColor = 'yellow';
        document.getElementById("block2").style.border = '3px solid #ff6a00';

        document.getElementById("block-var1").style.backgroundColor = 'yellow';
        document.getElementById("block-var1").style.border = '3px solid #ff6a00';

        document.getElementById("block-var2").style.backgroundColor = 'yellow';
        document.getElementById("block-var2").style.border = '3px solid #ff6a00';

        // document.getElementById("pointer1").style.visibility = 'visible';
        // document.getElementById("pointer2").style.visibility = 'visible';

        document.getElementById("block2").src = "block1.png";
        document.getElementById("block1").src = "block2.png";

      

        
    }
    else if (currentStep === 22){ 
        document.getElementById("block1").style.backgroundColor = 'yellow';
        document.getElementById("block1").style.border = '3px solid #ff6a00';

        document.getElementById("block2").style.backgroundColor = 'yellow';
        document.getElementById("block2").style.border = '3px solid #ff6a00';

        // document.getElementById("pointer1").style.visibility = 'visible';
        // document.getElementById("pointer2").style.visibility = 'visible';

        document.getElementById("block2").src = "block2.png";
        document.getElementById("block1").src = "block1.png";
       
        
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
