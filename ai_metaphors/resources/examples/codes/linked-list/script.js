// Firebase Initialization
const firebaseConfig = {
    apiKey: "AIzaSyAn_mT725rpxJdgdZ_HchR6FpAYs1sD6Zo",
    authDomain: "visual-interactions-csc108.firebaseapp.com",
    projectId: "visual-interactions-csc108",
    storageBucket: "visual-interactions-csc108.appspot.com",
    messagingSenderId: "703068795993",
    appId: "1:703068795993:web:2c734051b205606affad48",
    measurementId: "G-QWCWFNX1BR",
  };
  
  firebase.initializeApp(firebaseConfig);
  const db = firebase.firestore().collection("linked-list");
  
  // Generate a unique user ID
  const userId =
    "user-" + Date.now() + "-" + Math.floor(Math.random() * 10000);
  
  // Log user interactions to Firebase
  function logInteraction(eventType, details) {
    db.add({
      userId: userId,
      eventType: eventType,
      details: details,
      timestamp: firebase.firestore.FieldValue.serverTimestamp(),
    })
      .then(() => {
        console.log(`Logged: ${eventType}`, details);
      })
      .catch((error) => {
        console.error("Error logging interaction: ", error);
      });
  }
  
  let currentStep = 0;
  const totalSteps = 6; // Total steps based on your description
  
  const stepInfo = document.getElementById("step-info");
  const stepExplanation = document.getElementById("step-explanation");
  const codeElement = document.getElementById("code");
  
  const stepDescriptions = [
    "Step 1: Create a LinkedList instance.",
    "Step 2: Execute LinkedList.__init__ constructor.",
    "Step 3: Append a node with data=10 to the LinkedList.",
    "Step 4: Execute Node.__init__ constructor for data 10.",
    "Step 5: Append a node with data=20 to the LinkedList.",
    "Step 6: Execute Node.__init__ constructor for data 20.",
  ];
  
  function scaleApp() {
    const app = document.getElementById('app');
    // For example, base design is for 1920px width
    const scaleFactor = window.height/ 750;
    app.style.transform = 'scale(' + scaleFactor + ')';
    app.style.transformOrigin = 'center center';
}

  function highlightCode(step) {
    // Remove existing highlights
    for (let i = 1; i <= 20; i++) {
      const line = document.getElementById(`line${i}`);
      if (line) {
        line.classList.remove("highlight");
      }
    }
    // Highlight relevant line based on the step
    switch (step) {
      case 1:
        document.getElementById("line18").classList.add("highlight");
        break;
      case 2:
        document.getElementById("line6").classList.add("highlight");
        break;
      case 3:
        document.getElementById("line19").classList.add("highlight");
        break;
      case 4:
        document.getElementById("line2").classList.add("highlight");
        break;
      case 5:
        document.getElementById("line20").classList.add("highlight");
        break;
      case 6:
        document.getElementById("line2").classList.add("highlight");
        break;
      default:
        break;
    }
  }
  
  function updateStepDescription(step) {
    if (step >= 1 && step <= stepDescriptions.length) {
      stepExplanation.innerHTML = stepDescriptions[step - 1];
    } else {
      stepExplanation.innerHTML = "Step 0: Initialize two empty Linked Lists.";
    }
  }
  
  function updateStepInfo(step) {
    stepInfo.textContent = `Step ${step}`;
  }
  
  // NEW: Simply update the memory window image based on the step number.
  function updateMemoryWindow(step) {
    const memoryImage = document.getElementById("memory-image");
    if (step === 0) {
        // Clear the image (or set to a blank placeholder if you prefer)
        memoryImage.src = "";
        memoryImage.alt = "No memory visualization for Step 0";
      } else {
        memoryImage.src = `memory/Step${step}.png`;
        memoryImage.alt = `Memory Visualization Step ${step}`;
    }

  }

  // NEW: Function to update the visual window image based on the step number.
function updateVisualWindow(step) {
    const visualImage = document.getElementById("visual-image");
    visualImage.src = `memory2/Step${step}.png`;
    visualImage.alt = `Visual Visualization Step ${step}`;
    
  }
  
  
  function resetSteps() {
    currentStep = 0;
    highlightCode(0);
    updateStepDescription(0);
    updateStepInfo(0);
    updateMemoryWindow(0);
    updateVisualWindow(0);
    logInteraction("resetSteps", { step: currentStep });
  }
  
  function incrementStep() {
    if (currentStep < totalSteps) {
      currentStep++;
      executeStep(currentStep);
      logInteraction("incrementStep", { step: currentStep });
    } else {
      alert("All steps completed.");
      logInteraction("alert", { message: "All steps completed." });
    }
  }
  
  function decrementStep() {
    if (currentStep > 0) {
      currentStep--;
      executeStep(currentStep);
      logInteraction("decrementStep", { step: currentStep });
    } else {
      alert("Already at the first step.");
      logInteraction("alert", { message: "Already at the first step." });
    }
  }
  
  function runAllSteps() {
    while (currentStep < totalSteps) {
      currentStep++;
      executeStep(currentStep);
      logInteraction("runAllSteps", { step: currentStep });
    }
  }
  
  function executeStep(step) {
    // Instead of dynamically creating memory objects,
    // we just update the memory window image.
    updateMemoryWindow(step);
    updateVisualWindow(step);
    highlightCode(step);
    updateStepDescription(step);
    updateStepInfo(step);
    // (You can still call other functions here if you wish to update the linked list visualization.)
  }
  
  window.onload = () => {
    window.addEventListener('resize', scaleApp);
    window.addEventListener('load', scaleApp);
    resetSteps();
  };
  