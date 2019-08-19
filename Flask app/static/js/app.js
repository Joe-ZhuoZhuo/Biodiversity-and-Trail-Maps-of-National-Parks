function buildCharts(state) {
    // TO DO: Iterate through all states

    d3.json(`/metadata/state/${state}`, function(stateData) {
        console.log(state);

        // 

        console.log('state data', stateData);
        
        // Build line chart
	    var trace1 = {
            x: stateData.state,
            y: stateData.park_name,
            type: "line",
            text: 'Counts per 1,000'
        };
        var data = [trace1];
        var layout = {
            title: `${state} Fauna`,
            xaxis: { title: "States Names"},
            yaxis: { title: "Park Names"}
        };
        Plotly.newPlot("line", data, layout);        
    });

    // Build map with static data

    d3.json(`/metadata/state/park_name`, function(stateData) {
        console.log('state data', stateData)


        // Build bar chart
        var myPlot = document.getElementById('bar'),
            data = [{
                x: stateData.state,
                y: stateData.parks,
                type: "bar",
                marker: {
                    color: 'light blue'
                },
                text: 'Counts per 1,000',
            }];
            layout = {
                title: "Parks",
                xaxis: { 
                    tickangle: 40,
                    tickfont: {
                        size: 9.5
                    }
                },
                yaxis: {title: "State Parks"},
                hovermode: 'closest'
            };

        Plotly.newPlot("bar", data, layout);

    });
    
}

function init() {      

    // Set up the dropdown menu
    // Grab a reference to the dropdown select element
    var selector = d3.select("#selDataset");

    // Use the list of sample names to populate the select options
    d3.json("/states").then((state) => {
        state.forEach((instance) => {
        selector
            .append("option")
            .text(instance)
            .property("value", instance);
        });

        // Use Alabama to build the initial plot
        const defaultState = state[0];
        buildCharts(defaultState);
    });
}

function optionChanged(newState) {
    // Fetch new data each time a new state is selected
    buildCharts(newState);
}

init();