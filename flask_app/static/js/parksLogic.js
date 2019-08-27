var map = L.map('map').setView([37.8, -96], 4);

L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw', {
	maxZoom: 18,
	attribution: 'We made this',
	id: 'mapbox.light'
}).addTo(map);


	// control that shows state info on hover
	var info = L.control();

	info.onAdd = function (map) {
		this._div = L.DomUtil.create('div', 'info');
		this.update();
		return this._div;
	};

	info.update = function (props) {
		this._div.innerHTML = '<h4>US State Parks</h4>' +  
		(props ? '<b>' + props.name : '');
	};

	info.addTo(map);


	// get color depending on population density value
	function getColor(d) {
		return d>0 ?'#FFEDA0':'blue';
	}

	function style(feature) {
		return {
			weight: 2,
			opacity: 1,
			color: 'white',
			dashArray: '3',
			fillOpacity: 0.7,
			fillColor: getColor(feature.properties.density)
		};
	}

	function highlightFeature(e) {
		var layer = e.target;

		layer.setStyle({
			weight: 5,
			color: '#666',
			dashArray: '',
			fillOpacity: 0.7
		});

		if (!L.Browser.ie && !L.Browser.opera && !L.Browser.edge) {
			layer.bringToFront();
		}

		info.update(layer.feature.properties);
	}

	var geojson;

	function resetHighlight(e) {
		geojson.resetStyle(e.target);
		info.update();
	}

	function zoomToFeature(e) {
		map.fitBounds(e.target.getBounds());
	}

	function onEachFeature(feature, layer) {
		layer.on({
			mouseover: highlightFeature,
			mouseout: resetHighlight,
			click: zoomToFeature
		});
	}

	geojson = L.geoJson(statesData, {
		style: style,
		onEachFeature: onEachFeature
	}).addTo(map);

//GOOGLE CHARTS STUFF
//I'm putting this up here to preload the charts
      google.charts.load('current', {'packages':['bar']});
      google.charts.setOnLoadCallback(drawChart);

//Ming: Declaring the function up here so that it's hoisted. I don't think this is necessary but my javascript is rusty. 
function drawChart(cat) {
	//Google chart uses this format to make their charts.
	// var data = google.visualization.arrayToDataTable([
  //   ['Park Name', 'Mammals', 'Bugs', 'Peppers', 'Rogers'],
  //   ['<b>Arcadia</b>', 1000, 400, 200, 222]
  // ]);

	//Cat looks like: [ {park_name:"zzz", category:"Amphibian", category.1: "13"}, {...}]
	//It's an array with 1 object for every category in the park.

	let header_row = [];
	let data_row = [];
	let park_name = cat[0]["park_name"];
	header_row[0] = park_name;
	data_row[0] = "Different categories of species at " + park_name;
	//Looping through park categories
	for (let i = 0; i < cat.length; i++){
		//The first column is just Park name and theRealParkName
		//The rest are the categories so thats why we use this here.
		header_row[i+1] = cat[i]["category"];
		data_row[i+1] = cat[i]["category.1"];
	}

	var data = google.visualization.arrayToDataTable([
    header_row, data_row ]);


  var options = {
    chart: {
      title: 'Animal Categories',
      subtitle: 'The number of species per category in ' + park_name,
    },
    bars: 'vertical', // Required for Material Bar Charts.
    hAxis: {format: 'decimal'},
    height: 400, //MAKE THIS THE MAXIMUM NUMBER OF SPECIES FOR THE CHARTS 
    colors: ['#1b9e77', 'yellow', '#d95f02', 'teal', '#7570b3', '#eb5f9f','#0f4f17', '#99c7d2', '#1b9e77', 'yellow', '#d95f02', 'teal', '#7570b3', '#eb5f9f','#0f4f17', '#99c7d2']
  };

  var chart = new google.charts.Bar(document.getElementById('chart_div'));

  chart.draw(data, google.charts.Bar.convertOptions(options));

}

//Cats is an array of multiple objects with park names. We need to sort them into single array objects with the same park names. This is used below but placed up here for hoisting reasons 
//check for source here 
//https://gist.github.com/JamieMason/0566f8412af9fe6a1d470aa1e089a752
const groupBy = key => array =>
  array.reduce((objectsByKeyValue, obj) => {
    const value = obj[key];
    objectsByKeyValue[value] = (objectsByKeyValue[value] || []).concat(obj);
    return objectsByKeyValue;
  }, {});



  

var parks = {};
console.log("About to run D3.json")

// This code below does not work even though it did before August 24, 2016 13:00(1:00PM).

// d3.json('/parks', function(data) {
// 	parks = data;
	// for (var i = 0; i < parks.length; i++) {
 //    var location = [parks[i].latitude, parks[i].longitude]
 //    console.log(location)
 //    L.marker(location).addTo(myMap);
 //  }
// });

//To make it work, we had to split the d3.json and the .then into two parts.
//Just as Abraham split the goat into two to sacrifice for God.
//Now it works. It's ugly. But it works.

// And yes, we tried this too:

  // var request = new XMLHttpRequest()
  // // Open a new connection, using the GET request on the URL endpoint
  // request.open('GET', '/parks', true)
  // request.onload = function (parks) {
  //   console.log(parks)
  // };

//Call d3.json on the parks to get the API
park_api_call = d3.json('/all');



//See giant comment blog above for explanation on why we do setTimeout.
setTimeout(function(){
    park_api_call.then(function(data){
    	//We do this because the API json within data is a string. It needs to be converted into an array.
    	let parks = eval(data["parks"]);
    	let cats = eval(data["cat"]);


    	//See above for documentation on this
    	groupByParkName = groupBy("park_name");
    	cats = groupByParkName(cats)
    	// groupBy function returns an object. Convert it into array
    	cats = Object.values(cats)

    	//DIGRESSION:
    	//Just going to draw cats here real quick because otherwise the chart is blank when you load the page.
    	drawChart(cats[0]);

    	//Loop through all the parks and get their geo-coordinates
  		for (let i = 0; i < parks.length; i++) {
  			let park = parks[i];
  			let cat = cats[i];
		    let location = [park.latitude, park.longitude]
				var greenIcon = L.icon({
					iconUrl: 'static/leaf-green.png',
					shadowUrl: 'static/leaf-shadow.png',

					iconSize:     [19, 47], // size of the icon
					shadowSize:   [25, 32], // size of the shadow
					iconAnchor:   [11, 47], // point of the icon which will correspond to marker's location
					shadowAnchor: [4, 62],  // the same for the shadow
					popupAnchor:  [0, 0] // point from which the popup should open relative to the iconAnchor
				});
		    //Create markers on map based on the coordinates
		    marker = L.marker(location, {icon:greenIcon})
		    marker.addTo(map);
		    //The popup box when you mouseover
		    marker.on('mouseover', function(e) {
			  var popup = L.popup({ offset:[0,-20]})
			   .setLatLng(e.latlng) 
			   .setContent("<b>" + park.park_name + '</b><br/> Acres: ' + park.acres +
			   	'</b><br/> Latitude: ' + park.latitude + '</b><br/> Longitude: ' + park.longitude)
			   .openOn(map);
					});
		    //The thing that updates the chart
		    marker.on('click', function(e) {
		    	drawChart(cat)
		    });
  }
    })
}, 1500);





