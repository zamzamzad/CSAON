// Create SVG elements for graph and bar chart
const graphWidth = document.getElementById('graph').clientWidth;
const graphHeight = document.getElementById('graph').clientHeight;
const barChartWidth = document.getElementById('bar-chart').clientWidth;
const barChartHeight = document.getElementById('bar-chart').clientHeight;

const svgGraph = d3.select('#graph').append('svg')
    .attr('width', graphWidth)
    .attr('height', graphHeight);

const svgBarChart = d3.select('#bar-chart').append('svg')
    .attr('width', barChartWidth)
    .attr('height', barChartHeight);

// Load data
d3.json('topic_relationships.json').then(data => {
    const nodes = {};
    const links = data.map(d => ({
        source: d.source,
        target: d.target,
        value: d.value
    }));

    // Create a unique set of nodes
    links.forEach(link => {
        nodes[link.source] = { id: link.source };
        nodes[link.target] = { id: link.target };
    });

    // Create node and link elements for the graph
    const nodeElements = svgGraph.append('g').selectAll('circle')
        .data(Object.values(nodes))
        .enter().append('circle')
        .attr('r', 20) // Adjust node size here
        .attr('fill', '#1f77b4')
        .attr('stroke', '#fff')
        .attr('stroke-width', 2);

    const linkElements = svgGraph.append('g').selectAll('line')
        .data(links)
        .enter().append('line')
        .attr('stroke', '#ccc')
        .attr('stroke-width', d => Math.sqrt(d.value) * 3); // Adjust link width here

    // Create a force simulation
    const simulation = d3.forceSimulation(Object.values(nodes))
        .force('link', d3.forceLink(links).id(d => d.id))
        .force('charge', d3.forceManyBody())
        .force('center', d3.forceCenter(graphWidth / 2, graphHeight / 2));

    // Update node and link positions
    simulation.on('tick', () => {
        linkElements
            .attr('x1', d => d.source.x)
            .attr('y1', d => d.source.y)
            .attr('x2', d => d.target.x)
            .attr('y2', d => d.target.y);

        nodeElements
            .attr('cx', d => d.x)
            .attr('cy', d => d.y);
    });

    // Add labels to nodes
    svgGraph.append('g').selectAll('text')
        .data(Object.values(nodes))
        .enter().append('text')
        .attr('x', d => d.x)
        .attr('y', d => d.y)
        .attr('dy', 4)
        .attr('text-anchor', 'middle')
        .attr('fill', '#333')
        .text(d => d.id);

    // Add grid background
    const grid = svgGraph.append('g').attr('class', 'grid');
    for (let i = 0; i < graphWidth; i += 50) {
        grid.append('line')
            .attr('x1', i)
            .attr('y1', 0)
            .attr('x2', i)
            .attr('y2', graphHeight)
            .attr('stroke', '#ddd')
            .attr('stroke-width', 1);
    }
    for (let i = 0; i < graphHeight; i += 50) {
        grid.append('line')
            .attr('x1', 0)
            .attr('y1', i)
            .attr('x2', graphWidth)
            .attr('y2', i)
            .attr('stroke', '#ddd')
            .attr('stroke-width', 1);
    }
});

// Generate random data for bar chart
const barData = Array.from({ length: 10 }, (_, i) => ({
    topic: `Topic ${i}`,
    count: Math.floor(Math.random() * 100) + 1
}));

const x = d3.scaleBand()
    .domain(barData.map(d => d.topic))
    .range([0, barChartWidth])
    .padding(0.1);

const y = d3.scaleLinear()
    .domain([0, d3.max(barData, d => d.count)])
    .nice()
    .range([barChartHeight, 0]);

// Add bars to the bar chart
svgBarChart.selectAll('.bar')
    .data(barData)
    .enter().append('rect')
    .attr('class', 'bar')
    .attr('x', d => x(d.topic))
    .attr('y', d => y(d.count))
    .attr('width', x.bandwidth())
    .attr('height', d => barChartHeight - y(d.count))
    .attr('fill', '#1f77b4');

// Add x-axis and y-axis
svgBarChart.append('g')
    .attr('class', 'x-axis')
    .attr('transform', `translate(0,${barChartHeight})`)
    .call(d3.axisBottom(x));

svgBarChart.append('g')
    .attr('class', 'y-axis')
    .call(d3.axisLeft(y));
