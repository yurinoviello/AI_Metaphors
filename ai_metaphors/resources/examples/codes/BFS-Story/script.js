let currentStep = 0;

const graph = {
    A: ['B', 'C'],
    B: ['D', 'E'],
    C: ['F'],
    D: [],
    E: ['F'],
    F: []
};

// Steps with enqueue and dequeue actions
const steps = [
    // Step 0: Initial state
    { queue: ['A'], visited: [], codeLine: 2, currentNode: null, actionType: null, actionNode: null },
    // Step 1: Enqueue A
    { queue: ['A'], visited: [], codeLine: 2, currentNode: 'A', actionType: 'enqueue', actionNode: 'A' },
    // Step 2: Dequeue A
    { queue: [], visited: ['A'], codeLine: 5, currentNode: 'A', actionType: 'dequeue', actionNode: 'A' },
    // Step 3: Enqueue B
    { queue: ['B'], visited: ['A'], codeLine: 8, currentNode: 'A', actionType: 'enqueue', actionNode: 'B' },
    // Step 4: Enqueue C
    { queue: ['B', 'C'], visited: ['A'], codeLine: 8, currentNode: 'A', actionType: 'enqueue', actionNode: 'C' },
    // Step 5: Dequeue B
    { queue: ['C'], visited: ['A', 'B'], codeLine: 5, currentNode: 'B', actionType: 'dequeue', actionNode: 'B' },
    // Step 6: Enqueue D
    { queue: ['C', 'D'], visited: ['A', 'B'], codeLine: 8, currentNode: 'B', actionType: 'enqueue', actionNode: 'D' },
    // Step 7: Enqueue E
    { queue: ['C', 'D', 'E'], visited: ['A', 'B'], codeLine: 8, currentNode: 'B', actionType: 'enqueue', actionNode: 'E' },
    // Step 8: Dequeue C
    { queue: ['D', 'E'], visited: ['A', 'B', 'C'], codeLine: 5, currentNode: 'C', actionType: 'dequeue', actionNode: 'C' },
    // Step 9: Enqueue F
    { queue: ['D', 'E', 'F'], visited: ['A', 'B', 'C'], codeLine: 8, currentNode: 'C', actionType: 'enqueue', actionNode: 'F' },
    // Step10: Dequeue D
    { queue: ['E', 'F'], visited: ['A', 'B', 'C', 'D'], codeLine: 5, currentNode: 'D', actionType: 'dequeue', actionNode: 'D' },
    // Step11: Dequeue E
    { queue: ['F'], visited: ['A', 'B', 'C', 'D', 'E'], codeLine: 5, currentNode: 'E', actionType: 'dequeue', actionNode: 'E' },
    // Step12: Dequeue F
    { queue: [], visited: ['A', 'B', 'C', 'D', 'E', 'F'], codeLine: 5, currentNode: 'F', actionType: 'dequeue', actionNode: 'F' },
    // Step13: BFS complete
    { queue: [], visited: ['A', 'B', 'C', 'D', 'E', 'F'], codeLine: 10, currentNode: null, actionType: null, actionNode: null }
];

// Step explanations with narrative
const stepExplanations = [
    "Initialization: Start BFS with <span class='variable'>Superhero Headquarters</span> in the queue.",
    "Enqueue <span class='variable'>Superhero Headquarters</span> to plan your mission.",
    "Dequeue <span class='variable'>Superhero Headquarters</span> and begin your mission.",
    "From Headquarters, you discover <span class='variable'>Hero Alpha</span>. Enqueue <span class='variable'>Hero Alpha</span>.",
    "From Headquarters, you also find <span class='variable'>Hero Beta</span>. Enqueue <span class='variable'>Hero Beta</span>.",
    "Dequeue <span class='variable'>Hero Alpha</span> and start coordinating with them.",
    "From <span class='variable'>Hero Alpha</span>, you recruit <span class='variable'>Sidekick Delta</span>. Enqueue <span class='variable'>Sidekick Delta</span>.",
    "From <span class='variable'>Hero Alpha</span>, you also recruit <span class='variable'>Sidekick Epsilon</span>. Enqueue <span class='variable'>Sidekick Epsilon</span>.",
    "Dequeue <span class='variable'>Hero Beta</span> and start coordinating with them.",
    "From <span class='variable'>Hero Beta</span>, you confront <span class='variable'>Villain Omega</span>. Enqueue <span class='variable'>Villain Omega</span>.",
    "Dequeue <span class='variable'>Sidekick Delta</span> and assist them.",
    "Dequeue <span class='variable'>Sidekick Epsilon</span> and assist them.",
    "Dequeue <span class='variable'>Villain Omega</span> and neutralize them.",
    "BFS is complete. All nodes have been visited."
];

function incrementStep() {
    if (currentStep < steps.length - 1) {
        currentStep++;
        updateVisualization();
    } else {
        alert("All steps have been executed.");
    }
}

function decrementStep() {
    if (currentStep > 0) {
        currentStep--;
        updateVisualization();
    } else {
        alert("You are at the start.");
    }
}

function resetSteps() {
    currentStep = 0;
    updateVisualization();
}

function runAllSteps() {
    currentStep = steps.length - 1;
    updateVisualization();
}

function updateVisualization() {
    // Update step explanation
    document.getElementById('step-explanation').innerHTML = stepExplanations[currentStep];

    // Highlight current pseudocode line
    for (let i = 1; i <= 10; i++) { // Adjusted for new pseudocode lines
        document.getElementById(`line${i}`).classList.remove('highlight');
    }
    const currentCodeLine = steps[currentStep].codeLine;
    if (currentCodeLine) {
        document.getElementById(`line${currentCodeLine}`).classList.add('highlight');
    }

    // Update queue visualization
    updateQueueVisual(steps[currentStep].queue, steps[currentStep].actionType, steps[currentStep].actionNode);

    // Update visited table
    const table = document.getElementById('bfs-table');
    table.innerHTML = "<tr><th>Visited Nodes</th></tr>"; // Reset table header
    steps[currentStep].visited.forEach(node => {
        const row = `<tr><td>${node}</td></tr>`;
        table.innerHTML += row;
    });

    // Update graph visualization
    drawGraph(steps[currentStep].queue, steps[currentStep].visited, steps[currentStep].currentNode, steps[currentStep].actionType, steps[currentStep].actionNode);

    // Update step info
    document.getElementById('step-info').innerHTML = `Step ${currentStep}`;
}

function updateQueueVisual(queue, actionType, actionNode) {
    const queueVisual = document.getElementById('queue-visual');
    queueVisual.innerHTML = ''; // Clear existing queue

    queue.forEach((node, index) => {
        const nodeDiv = document.createElement('div');
        nodeDiv.classList.add('queue-node');
        nodeDiv.textContent = node;

        // Highlight enqueue and dequeue actions
        if (actionType === 'enqueue' && actionNode === node) {
            nodeDiv.classList.add('enqueue-visual');
        } else if (actionType === 'dequeue' && actionNode === node) {
            nodeDiv.classList.add('dequeue-visual');
        }

        queueVisual.appendChild(nodeDiv);

        // Add arrow between nodes except after the last node
        if (index < queue.length - 1) {
            const arrow = document.createElement('div');
            arrow.classList.add('arrow');
            arrow.innerHTML = '&rarr;';
            queueVisual.appendChild(arrow);
        }
    });

    // If queue is empty
    if (queue.length === 0) {
        const emptyDiv = document.createElement('div');
        emptyDiv.classList.add('empty-queue');
        emptyDiv.textContent = 'Empty';
        queueVisual.appendChild(emptyDiv);
    }
}

function drawGraph(queue, visited, currentNode, actionType, actionNode) {
    const svg = document.getElementById('graph');
    while (svg.firstChild) {
        svg.removeChild(svg.firstChild);
    }

    const nodes = {
        A: { x: 300, y: 100 },
        B: { x: 150, y: 250 },
        C: { x: 450, y: 250 },
        D: { x: 100, y: 400 },
        E: { x: 200, y: 400 },
        F: { x: 450, y: 400 }
    };

    // Draw edges (connections)
    drawEdge(svg, nodes.A, nodes.B);
    drawEdge(svg, nodes.A, nodes.C);
    drawEdge(svg, nodes.B, nodes.D);
    drawEdge(svg, nodes.B, nodes.E);
    drawEdge(svg, nodes.C, nodes.F);
    drawEdge(svg, nodes.E, nodes.F);

    // Draw nodes with highlighting and image placeholders
    Object.keys(nodes).forEach(node => {
        const isInQueue = queue.includes(node);
        const isVisited = visited.includes(node);
        let isCurrentNodeFlag = node === currentNode;
        let isEnqueued = (actionType === 'enqueue' && actionNode === node);
        let isDequeued = (actionType === 'dequeue' && actionNode === node);
        drawNode(svg, nodes[node], node, isInQueue, isVisited, isCurrentNodeFlag, isEnqueued, isDequeued);
    });

    // Apply greying out to unvisited and not in queue nodes
    Object.keys(nodes).forEach(node => {
        const isInQueue = queue.includes(node);
        const isVisited = visited.includes(node);
        if (!isInQueue && !isVisited) {
            const nodeElement = document.getElementById(`node-${node}`);
            if (nodeElement) {
                nodeElement.style.opacity = 0.3;
            }
        }
    });
}

function drawEdge(svg, from, to) {
    const line = document.createElementNS("http://www.w3.org/2000/svg", "line");
    line.setAttribute("x1", from.x);
    line.setAttribute("y1", from.y);
    line.setAttribute("x2", to.x);
    line.setAttribute("y2", to.y);
    line.setAttribute("stroke", "black");
    line.setAttribute("stroke-width", 2);
    svg.appendChild(line);
}

function drawNode(svg, position, label, isInQueue, isVisited, isCurrentNode, isEnqueued, isDequeued) {
    const group = document.createElementNS("http://www.w3.org/2000/svg", "g");
    group.setAttribute("id", `node-${label}`);

    // Create circle
    const circle = document.createElementNS("http://www.w3.org/2000/svg", "circle");
    circle.setAttribute("cx", position.x);
    circle.setAttribute("cy", position.y);
    circle.setAttribute("r", 40); // Increased radius for larger images
    if (isCurrentNode) {
        circle.setAttribute("fill", "#ffff00"); // Yellow for current node
    } else if (isEnqueued) {
        circle.setAttribute("fill", "#f0ad4e"); // Orange for enqueue
    } else if (isDequeued) {
        circle.setAttribute("fill", "#ff6a00"); // Darker orange/red for dequeue
    } else if (isVisited) {
        circle.setAttribute("fill", "#d5ddde"); // Light blue for visited
    } else if (isInQueue) {
        circle.setAttribute("fill", "#f0ad4e"); // Orange for in queue
    } else {
        circle.setAttribute("fill", "#fff");
    }
    circle.setAttribute("stroke", isCurrentNode ? "#ff6a00" : "black");
    circle.setAttribute("stroke-width", isCurrentNode ? "4" : "2");
    group.appendChild(circle);

    // Determine image based on node label
    let imagePath = 'images/placeholder.png'; // Default placeholder

    switch(label) {
        case 'A':
            imagePath = 'images/headquarters.png';
            break;
        case 'B':
            imagePath = 'images/hero_alpha.png';
            break;
        case 'C':
            imagePath = 'images/hero_beta.png';
            break;
        case 'D':
            imagePath = 'images/sidekick_delta.png';
            break;
        case 'E':
            imagePath = 'images/sidekick_epsilon.png';
            break;
        case 'F':
            imagePath = 'images/villain_omega.png';
            break;
        default:
            imagePath = 'images/placeholder.png';
    }

    // Create image
    const image = document.createElementNS("http://www.w3.org/2000/svg", "image");
    image.setAttributeNS("http://www.w3.org/1999/xlink", "href", imagePath); // Updated image path
    image.setAttribute("x", position.x - 30); // Adjusted to center the larger image
    image.setAttribute("y", position.y - 30);
    image.setAttribute("width", 60); // Increased width
    image.setAttribute("height", 60); // Increased height
    image.setAttribute("opacity", "0.8"); // Semi-transparent for better text visibility
    group.appendChild(image);

    // Create text label
    const text = document.createElementNS("http://www.w3.org/2000/svg", "text");
    text.setAttribute("x", position.x);
    text.setAttribute("y", position.y + 70); // Shifted below the circle
    text.setAttribute("text-anchor", "middle");
    text.setAttribute("fill", "black");
    text.setAttribute("font-size", "20px");
    text.setAttribute("font-weight", "bold");
    text.textContent = label;
    group.appendChild(text);

    svg.appendChild(group);
}

window.onload = () => {
    resetSteps();
};
