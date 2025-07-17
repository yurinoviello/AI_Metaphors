function appendNode(data) {
    // Simulate: ll1.append(data)
    const linkedListId = memoryData.main['ll1']; // e.g., id60
    if (!linkedListId || !memoryData.objects[linkedListId]) {
        console.error("LinkedList instance not found.");
        return;
    }
    // Create a new node (constructor execution)
    const nodeInitId = `id${idCounter++}`; // e.g., id64, id66
    const nodeId = `id${idCounter++}`; // e.g., id65, id67
    const intId = `id${idCounter++}`; // e.g., id65, id67 for int values
    
    // Create Node.__init__ scope
    createObjectBox(nodeInitId, "Node.__init__", [
        {name: "self", value: nodeId},
        {name: "data", value: intId }
    ], 20, (data === 10 ? 300 : 120), true);

    memoryData.objects[nodeId] = {
        class: 'Node',
        variables: {
            'data': data,    // Directly assign the data value
            'next': 'None'
        }
    };
    console.log('memory data');
    console.log(memoryDada.objects);
    if (memoryData.objects[linkedListId].variables['_first'] === 'None') {
        memoryData.objects[linkedListId].variables['_first'] = nodeId;
    } else {
        // Traverse to the last node and update its 'next'
        let current = memoryData.objects[linkedListId].variables['_first'];
        while (memoryData.objects[current].variables['next'] !== 'None') {
            current = memoryData.objects[current].variables['next'];
        }
        memoryData.objects[current].variables['next'] = nodeId;
    }

    // Create int object for data
    createObjectBox(intId, "int", [
        {name: "", value: data}
    ], 450, (data === 10 ? 300 : 500), false);

    // Create Node object with data
    createObjectBox(nodeId, "Node", [
        {name: "data", value: intId}, // id65 for 10, id67 for 20
        {name: "next", value: "id63"} // None
    ], 260, (data === 10 ? 300 : 500), false);

    // Show LinkedList object updated
    updateObjectBox(linkedListId, "_first", memoryData.objects[linkedListId].variables['_first']);
    if(currentStep === 4){
        createObjectBox("id60", "LinkedList", [
            {name: "_first", value: "id65"}
        ], 260, 120, false);
    }
    if(currentStep === 6){
        createObjectBox("id65", "Node", [
            {name: "data", value: "id66"},
            {name: "next", value: "id68"}
        ], 260, 300, false);
    }
} // Close the function here
