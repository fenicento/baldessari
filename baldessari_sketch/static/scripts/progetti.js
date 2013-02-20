
/*
 * progetti.js
 * 2012
 * this script handles all the interface for the "opere" section of the site
 */



/*
 * ------------------------------------       GLOBAL SETTINGS -------------------------------------------------------------------
 */

settings = {
			mode : "elenco",
			type : "projects",
			sort : "alphab",
			itemsNumber : 10,
			filters : []
		   }

/*
 * ----------------------------------------------- GLOBAL VARIABLES AND INITIALIZATION --------------------------------------------------
 */

//loading documents on start
$(document).ready(function(){
	parseURL();
	// switchType();
	loadData();
	attributeButtons();
	ddpowerzoomer.init($);
	setFiltri();	
});

d3.selectAll('#modes label, .filter, #types label')
	//.style('background-color', 'grey')
	.style('background-image', function(){
	return 'url('+static_prefix + 'img_interface/button_normal.jpg)';
}).style('background-size', '100% 100%').style('background-repeat', 'no-repeat');


var globalIndex = 10; //item that handle loading of items

//two arrays for driving items displaying
//a reference one, that changes just when user switch between project mode and document mode
var referenceArray = {};
//a dynamic one, that change regarding to filtering parameters
var dynamicArray = {};

//docCount is used in order to handle the number of elements displayed
var docCount = [];
for(var i = 0 ; i < 100 ; i++){
	docCount.push(0);
}
//for first load
var dataLoaded = false;

//this function updates this url in order to match with the js's settings (at the begining of this code)	
function updateURL(){
			var address = ''
			for(var id in settings){
				if(id != 'itemsNumber' && id != 'filters'){
					address += '"' + id + '"' + '=' + '"' + settings[id]+ '"' + '&'
				}
			}
			address = address.substring(0, address.length - 1);
			window.history.pushState({path:window.location.href},'', address);
}

//this function parses the url on start in order to fix the settings
function parseURL(){
	var address = decodeURI(window.location.href);
	var paramsL = address.split('/')
	var params = paramsL[paramsL.length - 1];
				
	var exp = params.match(/"(.+?)"/g);
	if(exp){
		for(i in exp){
			if(i%2 == 0){
				var set = exp[i].substring(1, exp[i].length - 1);
				var j = parseInt(i)+1
				if(set != 'filters'){
					settings[set] = exp[j].substring(1, exp[j].length - 1);
				}
				
				if(settings['mode'] == 'galleria')settings.itemsNumber = 100;
			}
		}
	}
	
}


/*
 * ************************************************ INTERFACE ELEMENTS ********************************************************
 */


//function that handle filters
function setFiltri(){
	//var selectdates = d3.select('#filtri').append('p').append('select').attr('id', 'selectdate').attr('title', 'select date').attr('multiple', 'multiple').attr('name', 'select date').attr('size', 10);
	var selecttype = d3.select('#filtri').append('p').append('select').attr('id', 'selecttype').attr('title', 'select type').attr('multiple', 'multiple').attr('name', 'select filter').attr('size', 5);
	

	$.get('getInfo', {action : 'getTipi'}, function(data){
					var obj1 = {
						name : 'projecttype',
						value : []
					}
					for(i in data.tipi){
						var val = data.tipi[i];
						obj1.value.push(val)
						selecttype.append('option').attr('value', function(){return val;}).text(function(){return val;}).attr('selected', true);
						
					}
					settings.filters.push(obj1);
					
						$('#selecttype').multiselect({
							selectedText : "Tipo",
							noneSelectedText : 'Tipo di progetto',
							show: "blind",
							hide: "blind",
							click: updateType,
							checkAll: function(event, ui){
								for(i in settings.filters){
										if (settings.filters[i].name == 'projecttype'){
											$.get('getInfo', {action : 'getTipi'}, function(data){
												for(i in settings.filters){
													if (settings.filters[i].name == 'projecttype'){
															settings.filters[i].value = [];
															for(j in data.tipi){
																settings.filters[i].value.push(data.tipi[j]);
															}
													}
												}
											});
										}
									}
								dynamicArray = filterData();
								updateView();
								},
							uncheckAll: function(event, ui){
									for(i in settings.filters){
										if (settings.filters[i].name == 'projecttype'){
											settings.filters[i].value = [];
										}
									}
									dynamicArray = filterData();
									updateView();
								},
						})
					
		});
}

//behavior when scrolling
$(window).scroll(function(){
	if(settings.mode != 'mappa' && $(window).scrollTop() + $(window).height() > $(document).height() - 50 && $(window).height() < $(document).height()) {
		
		if(globalIndex+settings.itemsNumber< dynamicArray.list.length){
			globalIndex+=settings.itemsNumber
			updateView();
		}
	}
})


//interface handling
d3.select("#opere_modes_ul").selectAll("input").on("click", function(){
		var value = d3.select(this).attr("value");
		if(value != settings.mode){
			changeMode(value);
			settings.mode = value;
			updateURL();
		}
		
	});

//handle the change of images for the buttons (dirty)
function attributeButtons(){
	
	d3.selectAll('#modes label').style('background-image', function(){
			var val = d3.select(this).select("input").attr("value");
			if(val == settings.mode){
				return 'url('+static_prefix + 'img_interface/button_selected.jpg)';
			}else{
				return 'url('+static_prefix + 'img_interface/button_normal.jpg)';
			}
	});
	
	d3.selectAll('#types label').style('background-image', function(){
			var val = d3.select(this).select("input").attr("value");
			if(val == settings.type){
				return 'url('+static_prefix + 'img_interface/button_selected.jpg)';
			}else{
				return 'url('+static_prefix + 'img_interface/button_normal.jpg)';
			}
	});	
}


/*                                                                                                                                  /*
 * *********************************************************** LOADING OF DATA ***************************************************
 *                                                                                                                                  */


//this function loads all items of a specific type (documents/projects) and stock them in referenceArray
function loadData(){
	var params = {
					action : function(){
								if(settings.type == 'documents'){
									return 'getAllDocsList'
								}else{
									return 'getAllProjectsList'
								}
							}
					}
			var pre = d3.select('#opere_display').append('div').attr('id', 'preloader').style('text-align', 'center').style('padding-bottom', '3%')
			pre.append('img').attr('src', function(){return static_prefix+ "img_interface/preloader.gif"})
		
	       $.get("getInfo", params, function(data){
	       		d3.selectAll('#preloader').remove();
	       		referenceArray = {}
				referenceArray = data;
				
				//this portion is just done in the begining
				if(!dataLoaded){
					dynamicArray = filterData();
					globalIndex+=settings.itemsNumber
					updateView();
					dataLoaded = true;
				}
		});
}


/*
 * ************************************** UPDATING DATA AND VIEW **********************************************************
 */

//this function handle displayed items, adding and deleting regarding to scroll and filtering
function updateView(){
		//console.log(dynamicArray.list.length)
		//console.log('updateview')
		if(dynamicArray.list.length >= 0){
				if(settings.mode == 'elenco'){
					if(settings.type == 'documents'){
						
						var data = dynamicArray.list.slice(0,globalIndex+settings.itemsNumber);
						
						//enter
						for(i in data){
							var obj = data[i]
							var id = '#' + obj.segnatura
							if(d3.select(id)[0][0] == null){
								var item = d3.select('#opere_display').append('div').datum(data[i]).call(itemDocElenco);
							}
						}
						
						d3.select('#opere_display').selectAll('.itemelenco').each(function(d){
							var div = d3.select(this)
							var id = d.segnatura
							var exists = false;
							for (i in data){
								var obj = data[i];
								if(obj.segnatura == id){
									exists = true;
								}
							}
							
							if(!exists){
								var w = document.getElementById(div.attr('id')).offsetHeight;
								div.style('opacity', 1).style('height', w).transition().duration(300).style('height', 0).remove();
							}
						})
						
						
					}else if(settings.type == 'projects'){
						/*for(var i = 0 ; i < dynamicArray.list.length ; i++){
							projElenco(dynamicArray.list[i]);
						}*/
						
						var data = dynamicArray.list.slice(0,globalIndex+settings.itemsNumber);
						
						//enter
						for(i in data){
							var obj = data[i]
							var id = '#' + obj.segnatura
							if(d3.select(id)[0][0] == null){
								var item = d3.select('#opere_display').append('div').datum(data[i]).call(projElenco);
							}
						}
						
						d3.select('#opere_display').selectAll('.itemelenco').each(function(d){
							var div = d3.select(this)
							var id = d.sigla
							var exists = false;
							for (i in data){
								var obj = data[i];
								if(obj.segnatura == id){
									exists = true;
								}
							}
							
							if(!exists){
								var w = document.getElementById(div.attr('id')).offsetHeight;
								div.style('opacity', 1).style('height', w).transition().duration(300).style('height', 0).remove();
							}
						})
						
					}
					}else if(settings.mode == 'galleria'){
						for(var i = 0 ; i < dynamicArray.list.length ; i++){
							docGalleria(dynamicArray.list[i]);
						}
					}else if(settings.mode == 'mappa'){
						displayMap();
					}
			}	
			
			attributeButtons();
			d3.select('#detailgalleria').remove()			
}

// this function is dedicated to switch between types of viz (documents/projects) in elenco mode
function switchType(){
	d3.select("#opere_switchtype_ul").selectAll("input").on("click", function(){
		var value = d3.select(this).attr("value");
		var params = {
			action : function(){
				if(value == 'documents'){
					return 'getAllDocsList'
				}else{
					return 'getAllProjectsList'
				}
			}
		}
		
			//ajax query
		if(value != settings.type){
				settings.type = d3.select(this).attr("value");
				referenceArray = {}
				dynamicArray = {}
				//globalIndex = 0; //index to handle dynamic loading of items
				//delete former files
				d3.select('#opere_display').selectAll("div")/*.style("opacity", 1).transition().duration(500).style("opacity", 0)*/
					.remove();
													
				dataLoaded = false;//reinitialize the state of data (to handle actions stack regarding to ajax)
				loadData();
				//change url
				updateURL();
				//change buttons
				attributeButtons();
			}
			
		});
}
	
//changing the visualization modes
function changeMode(value){
	d3.select('#opere_display').selectAll('div').style("opacity", 1).transition().duration(500).style('opacity', 0e-6).remove();
	d3.select('#types').style("opacity", 1).transition().duration(500).style('opacity', 0e-6).remove();
	//delete detailgaleria if it's present
	d3.selectAll('.detailgalleria').remove();
	
	globalIndex = 0;
	if(value == 'elenco' && $("#types").length == 0){
		var cont = d3.select("#params1").append("div").attr("id", "types");
		/*var cont2 = cont.append('ul').attr("id", "opere_switchtype_ul");
		var label1 = cont2.append('li').append("label")*/
		
		cont.html('<form method="post" id="opere_switchtype_form" action="/switchtype/"><ul id="opere_switchtype_ul"><li><label><input checked="checked" type="radio" name="typeviz" id="doctype" value="documents">Documenti</label></li><li><label><input type="radio" name="typeviz" id="projtype" value="projects">Progetti</label></li></ul></form>')
		cont.selectAll('label').style('background-image', function(){
						return 'url('+static_prefix + 'img_interface/button_normal.jpg)';
					}).style('background-size', '100% 100%').style('background-repeat', 'no-repeat')
		dataLoaded  = false;
		settings.type = 'documents'
		settings.itemsNumber = 10;
		switchType();
		loadData();
		cont.style("opacity", 0e-6).transition().duration(500).style("opacity", 1);
	}else if (value == 'galleria'){
		dataLoaded = false;
		settings.type = 'documents';
		settings.itemsNumber = 100;
		loadData();
	}else if (value == 'mappa'){
		dataLoaded = false;
		settings.type = 'projects';
		settings.itemsNumber = 2000;
		loadData();
	}
}

function updateType(event, ui){
	
	for(i in settings.filters){
		if (settings.filters[i].name == 'projecttype'){
			if(ui.checked == true){
				settings.filters[i].value.push(ui.value)
			}else{
				for(j in settings.filters[i].value){
					if(settings.filters[i].value[j] == ui.value){
						settings.filters[i].value.splice(j, 1);
					}
				}
			}
		}
	}
	dynamicArray = filterData();	
	updateView();
}

// TODO - function that update the date
/*function updateDate(event, ui){
	//first, add the filter if it doesn't exist	
	
	for(i in settings.filters){
		if (settings.filters[i].name == 'date'){
			if(ui.checked == true){
				settings.filters[i].value.push(ui.value)
			}else{
				for(j in settings.filters[i].value){
					if(settings.filters[i].value[j] == ui.value){
						settings.filters[i].value.splice(j, 1);
					}
				}
			}
		}
	}
	dynamicArray = filterData();	
	updateView();
}
*/


/*
 * ******************************************************** FILTERING AND SORTING FUNCTIONS *****************************************
 */



//this function updates dynamicArray regarding to filtering parameters
function filterData(){
	//first, copy the reference array
	array = {}
	array['list'] = []
	
	
	//filters
	if(settings.filters){
		for(key in settings.filters){
			var filter = settings.filters[key];
			switch(settings.filters[key].name){
				
				//filter by date - TODO
				case 'date':
				break;
				
				//filter by type of project
				case 'projecttype':
				for(j in settings.filters){
					if (settings.filters[j].name = 'projecttype'){
						projtypes = settings.filters[j].value;
						for(i in referenceArray.list){
							var item = referenceArray.list[i];
							var ok = false;
							for(k in projtypes){
								if(item['tipo'] == projtypes[k]){
									ok = true;
								}
							}
							if(ok){
								array.list.push(item);
							}
						}
					}
				}
				break;
				
				default:
				break;
			}
		}
	}

	return array;
}

// TODO - this function should sort data regarding to alphabetic/chronologic or other sorting rules
/*function sortData(){
		switch(settings.sort){
		case 'alphab':
		array.list.sort(function(a,b){
			if(settings.type == 'documents'){
				if(a.project < b.project){
					return -1;
				}
				if(a.project > b.project){
					return 1;
				}
				return 0;
				
			}else{
				if(a.denominazione < b.denominazione){
					return -1;
				}
				if(a.denominazione > b.denominazione){
					return 1;
				}
				return 0;
			}
		})
		break;

		case 'chronol':
		
		array.list.sort(function(a,b){
			
			var datea;
			var dateb;
			if(typeof(a.data) == 'object'){
				datea = a.data[0]['begining']
			}else if(typeof(a.data) == 'number'){
				datea = a.data;
			}else datea = 0;
			
			if(typeof(b.data) == 'object'){
				dateb = b.data[0]['begining']
			}else if(typeof(b.data) == 'number'){
				dateb = b.data;
			}else dateb = 0;
			
			
			if(datea < dateb){
				return -1;
			}
			if(datea > dateb){
				return 1;
			}
			return 0;
		})
		break;
		
		default:
		array.list.sort(function(a,b){
			if(settings.type == 'documents'){
				if(a.project < b.project){
					return -1;
				}
				if(a.project > b.project){
					return 1;
				}
				return 0;
				
			}else{
				if(a.denominazione < b.denominazione){
					return -1;
				}
				if(a.denominazione > b.denominazione){
					return 1;
				}
				return 0;
			}
		});
		break;
	}
}
*/

/*
 * ************************************ DISPLAYING FUNCTIONS *****************************************************************
 */

//this function fills  an item in elenco mode once it's been created
function itemDocElenco(){
	
						var item = this
						item.attr('id', function(d){
							return d.segnatura;})
						item.attr("class", "itemelenco")
						
						
						var left = item.append('div').attr('class', 'column').style('float', 'left')
											.append('a').attr("href", function(d){ return 'document/'+d.segnatura;})
						var img = left.append('img').attr('src', function(d){
												return media_prefix + d.adressthumb;
												// return static_prefix + d.adressthumb;
											}).style("height", function(){return window.innerHeight/15;})
											.style("width", function(){return window.innerHeight/15;})
											.style('display', 'inline-block')
						var leftHeight = left[0][0].offsetHeight;
											
						var middle = item.append('div').attr('class', 'column').style('margin-left', '30px').style('float', 'left').style('width', '20%')
						middle.append('a').attr("href", function(d){ return 'document/'+d.segnatura;}).append('h3').text(function(d){ return 'Documento '+d.segnatura;});
						
						var right = item.append('div').attr('class', 'column').style('float', 'right')
						.style('padding-left', '5%')
						.style('width', '40%')
						.style('border-left', '1px black solid')
						right.append('p').text(function(d){
							return 'Progetto : '+d.project;
						})
						
						item.on('mouseover', function(){
							var divs = d3.select(this).selectAll("div").transition().each(function(d,i){
								var data = d;
								if(i==0){
									d3.select(this).select('img')
									.attr('src', function(){
												console.log(data);
												return media_prefix + d.adressimage;
												// return static_prefix + d.adressimage;
											})
									.transition().duration(200)
									.style('width', function(){return window.innerHeight/3;})
									.style('height', function(){return window.innerHeight/3;})
								}
								if(i == 1){
									d3.select(this).append('p').attr('class', 'temp').style('padding-left', "10px").style('border-left', '1px solid black')
									.html(function(){
										var texte = ''
										
										texte += 'Supporto :<br> ' + data['supporto'] + '<br><br>';
										if(data['contenuto'] != undefined)texte += 'Contenuto :<br> ' + data['contenuto'] + '<br><br>';
										texte += 'Tipologia :<br> ' + data['tipologia'] + '<br><br>';
										var largezza = parseInt(data['largezza']);
										var altezza = parseInt(data['altezza']);
										texte += 'Dimensioni :<br> ' + largezza + ' x ' + altezza + 'cm';

										return texte;
									})
								}

							});
						})
						.on('mouseout', function(){
							d3.select(this).selectAll('.temp').transition().duration(200).delay(500).style('opacity', 0e-6).remove();
							var divs = d3.select(this).selectAll("div").each(function(d,i){
								if(i==0){
									d3.select(this).select('img')
									/*.attr('src', function(d){
												return static_prefix+ d.adressthumb;
											})*/
									.transition().duration(200)
									.style('width', function(){return window.innerHeight/15;})
									.style('height', function(){return window.innerHeight/15;})
								}
								if(i == 1){
									d3.select(this).selectAll('p').style('opacity', 1).remove();
								}
								if(i == 2){
									d3.select(this).selectAll('a,p').remove();
									d3.select(this).append('p').text(function(d){
																					return 'Progetto : '+d.project;
																				})
								}
							});
						})
						
}

//this function format a project div for elenco mode
function projElenco(){
	
						var item = this
						item.attr('id', function(d){
							console.log(d);
							return d.sigla;})
						item.attr("class", "itemelenco")
						
						
						var left = item.append('div').attr('class', 'column').style('float', 'left')
											.append('a').attr("href", function(d){ return 'project/'+d.sigla;})
						var img = left.append('img').attr('src', function(d){
												return media_prefix+ d.adressthumb;
												// return static_prefix+ d.adressthumb;
											}).style("height", function(){return window.innerHeight/15;})
											.style("width", function(){return window.innerHeight/15;})
											.style('display', 'inline-block')
						var leftHeight = left[0][0].offsetHeight;
											
						var middle = item.append('div').attr('class', 'column').style('margin-left', '30px').style('float', 'left').style('width', '20%')
						middle.append('a').attr("href", function(d){ return 'project/'+d.sigla;}).append('h3').text(function(d){ return d.denominazione;});
						
						
						item.on('mouseover', function(){
							var divs = d3.select(this).selectAll("div").transition().each(function(d,i){
								var data = d;
								if(i==0){
									d3.select(this).select('img')
									.transition().duration(200)
									.style('width', function(){return window.innerHeight/3;})
									.style('height', function(){return window.innerHeight/3;})
								}
								if(i == 1){
									d3.select(this).append('p').attr('class', 'temp').style('padding-left', "10px").style('border-left', '1px solid black')
									.html(function(){
										var texte = ''
										
										texte += 'Tipo : '  + data['tipo'] + '<br><br>';
										texte += 'Indirizzo : ' + data['address'] + '<br><br>';
										
										texte += 'Date : '
										
										for(i in data['data']){
											
											var interval = ''
											if(i!= 0) interval += ', '
											
											var d1 = data['data'][i]['begining'];
											var d2 = data['data'][i]['end'];
											
											if(d1<d2){
											interval += d1 + '-' + d2;
											} else interval += d2 + '-' + d1;
											
											texte += interval;
										}

										return texte;
									})
								}

							});
						})
						.on('mouseout', function(){
							d3.select(this).selectAll('.temp').transition().duration(200).delay(500).style('opacity', 0e-6).remove();
							var divs = d3.select(this).selectAll("div").each(function(d,i){
								if(i==0){
									d3.select(this).select('img')
									.transition().duration(200)
									.style('width', function(){return window.innerHeight/15;})
									.style('height', function(){return window.innerHeight/15;})
								}
								if(i == 1){
									d3.select(this).selectAll('p').style('opacity', 1).remove();
								}
								if(i == 2){
									d3.select(this).selectAll('a,p').remove();
									d3.select(this).append('p').text(function(d){
																					return 'Progetto : '+d.project;
																				})
								}
							});
						})				
}


//this function is dedicated to the display of the map mode
function displayMap(data){
	
	//delete the documents/projects button
	d3.select('#types').style("opacity", 1).transition().duration(500).style('opacity', 0e-6).remove();
	
	
	    var divmap = d3.select("#opere_display").append('div').style('width', function(){
	    	return d3.select('#params').style('width');
	    }).style('height', function(){
	    	return '100%';//window.innerHeight-d3.select('#opere_display')[0][0].offsetTop-10;
	    })
	    
        var map = new google.maps.Map(divmap.node(), {
          zoom: 5,
          center: new google.maps.LatLng(48.856626, 2.351139),
          //paris
          mapTypeId: google.maps.MapTypeId.ROADMAP,

          //gérer tous les controles : 
          panControl: false,
          mapTypeControl: false,
          overviewMapControl: false,
          streetViewControl: false,
          zoomControl: false,
          keyboardShortcuts: true,
          scrollwheel: true,

          //gérer le style :
          styles: [{
            featureType: "all",
            elementType: "geometry",
            stylers: [{
              saturation: -100
            }, {
              lightness: 50
            }, {
              visibility: "simplified"
            }]
          }, {
            featureType: "all",
            elementType: "labels",
            stylers: [{
              saturation: -100
            }]
          }, {
            featureType: "road",
            elementType: "labels",
            stylers: [{
              visibility: "on"
            }]
          }, {
            featureType: "water",
            elementType: "geometry",
            stylers: [{
              hue: "#FFFFFF"
            }, {
              saturation: 100
            }, {
              lightness: 100
            }]
          }, {
            featureType: "administrative.country",
            elementType: "all",
            stylers: [{
              saturation: 0
            }, {
              lightness: 0
            }, {
              visibility: "on"
            }]
          }]
        }); //fin de la map 	
	
	
	var overlay = new google.maps.OverlayView();
	
	var data = dynamicArray.list;
	
  // Add the container when the overlay is added to the map.
  overlay.onAdd = function() {
    var layer = d3.select(this.getPanes().overlayLayer).append("div")
        .attr("class", "stations");

    // Draw each marker as a separate SVG element.
    // We could use a single SVG, but what size would it have?
    overlay.draw = function() {
      var projection = this.getProjection(),
          padding = 10;

      var marker = layer.selectAll("svg")
          .data(data)
          .each(transform) // update existing markers
        .enter().append("svg:svg")
          .each(transform)
          .attr("class", "marker");

      // Add a circle.
      marker.append("svg:circle")
          .attr("r", 4.5)
          .attr("cx", padding)
          .attr("cy", padding)
          .style('cursor', 'pointer')
          .on('mouseover',function(){
          	d3.select(this).transition().duration(200).attr("r", 9);

          	})
          .on('mouseout',function(){d3.select(this).transition().duration(200).attr("r", 4.5)})
          .on('click', function(d){window.location.href = 'project/'+d.sigla})
          ;
      
      marker.on('mouseover', function(d){
      	
      				//d3.select(this).append('text').text('coucou').attr("x", 0).attr('y', 0)
      				//console.log(d3.select(this))
			      	var top = window.event.clientY ;//d3.select(this)[0][0].offsetTop;
			      	var left = window.event.clientX;//d3.select(this)[0][0].offsetLeft;
			      	var data = d;
			      	var tooltip = d3.select('#opere_display').append('div').attr('id', 'maptooltip')
			      	
			      	tooltip.style('left', function(){
			      		return left;
			      	})
			      	tooltip.style('top', function(){
			      		//console.log(d3.select(this));
			      		return top +20;//+ d3.select('#opere_display')[0][0].offsetTop;
			      	})			      		
			      		
			      	var text = tooltip.append("h3").text(function(d){return data.denominazione;})
			      	
			      	tooltip.append('p').attr('class', 'temp').style('padding-left', "10px").style('border-left', '1px solid black')
									.html(function(){
										var texte = ''
										
										texte += 'Tipo : '  + data['tipo'] + '<br><br>';
										texte += 'Indirizzo : ' + data['address'] + '<br><br>';
										
										texte += 'Date : '
										
										for(i in data['data']){
											
											var interval = ''
											if(i!= 0) interval += ', '
											
											var d1 = data['data'][i]['begining'];
											var d2 = data['data'][i]['end'];
											
											if(d1<d2){
											interval += d1 + '-' + d2;
											} else interval += d2 + '-' + d1;
											
											texte += interval;
											return texte;
										}
										})
			      			
			      	
			      	})

      .on('mouseout', function(d){
      	d3.selectAll('#maptooltip').remove();
      });
        
        /*
       var mask = marker.append ('svg:defs').append('svg:clipPath').attr('class', 'decoupe')
       
       mask.append('circle').attr('cx', 30).attr('cy', 30).attr('r', 10);
       
       var img = marker.append('image').attr('xlink:href', function(d){
							return static_prefix+ d.adressthumb;
						})
						.attr("x", -25)
						.attr('y', -25)
						.attr('width', 50)
						.attr('height', 50)
						.attr("clip-path", "url(.decoupe)")*/
      
      /*var img = marker.append('image').attr('xlink:href', function(d){
							return static_prefix+ d.adressthumb;
						})
						.attr("x", -25)
						.attr('y', -25)
						.attr('width', 50)
						.attr('height', 50)*/

      // Add a label.
      /*marker.append("svg:text")
          .attr("x", padding + 7)
          .attr("y", padding)
          .attr("dy", ".31em")
          .text(function(d) { return d.address; });*/

      function transform(d) {
        d = new google.maps.LatLng(d['x'], d['y']);
        d = projection.fromLatLngToDivPixel(d);
        return d3.select(this)
            .style("left", (d.x - padding) + "px")
            .style("top", (d.y - padding) + "px");
      }
    };
  };

  // Bind our overlay to the map…
  overlay.setMap(map);
  
	
}

//this function format document div for gallery mode
function docGalleria(data){
	d3.selectAll('#types').remove()
	var item = d3.select('#opere_display').append("div").datum(data);
	//var item = d3.select("#opere_display").selectAll('div');
	item.attr("class", "itemgalleria")
	
	var img = item.append('a').attr("href", function(d){
								return 'document/'+d.segnatura;
							})
					.append('img').attr('src', function(d){
							return media_prefix + d.adressthumb;
							// return static_prefix+ d.adressthumb;
						}).style("width", "100px").style("height", "70px")
						.attr('title', function(d){return d.segnatura;})
	img.on('mouseover', function(d){
			d3.selectAll('.detailgalleria').remove();
				//var div = d3.select(this);
				
				if(settings.mode == "galleria"){
					var div = $(this);
					var pos = div.position();
					var x = pos.left;//+parseInt(div.width()/2);
					var y = pos.top;
					//var y = div.height();
					var detail = d3.select('#opere_viz_space').append('div').attr("class", "detailgalleria");
					data = d;
					
					detail.style('left', function(d){return x - 10;}).style('top', function(d){return y-10;});
					
					var img1 = detail.append('a').attr('href', function(){
						return 'document/'+ data.segnatura
					})
					
					img1.append('a').attr("href", function(d){
									return 'document/'+data.segnatura;
								}).append('img').attr('src', function(d){
									return media_prefix + data.adressimage;
									// return static_prefix + data.adressimage;
							}).style("width", "300px").style('cursor', 'crosshair').attr('id', 'imagezoom')
					
					$('#imagezoom').addpowerzoom({
						defaultpower: 2,
						powerrange: [2,5],
						largeimage: null,
						magnifiersize: [150,150] //<--no comma following last option!
					})								
							
					detail.append('a').attr('href', function(){return "document/"+data.segnatura;}).append('h4').text(function(){ return "documento " + data.segnatura;});
					
					detail.append('p').html(function(){
						var texte = ''
											
											texte += 'Supporto : ' + data['supporto'] + '<br>';
											if(data['contenuto'] != undefined)texte += 'Contenuto : ' + data['contenuto'] + '<br>';
											texte += 'Tipologia : ' + data['tipologia'] + '<br>';
											var largezza = parseInt(data['largezza']);
											var altezza = parseInt(data['altezza']);
											texte += 'Dimensioni : ' + largezza + ' x ' + altezza + 'cm';
						return texte;
					})
					.style("width", "300px")
					.style('font-size', '0.7em')
					
				}
				
	})
						
	item.style('opacity', 0.1).transition().duration(1000).style('opacity', 1);
	img.style("height", "0px").transition().duration(800).style("height", "70px");
}


/*
 * ------------------------------- ZOOM SYSTEM FOR THE GALLERY MODE ---------------------------------------------------------
 */


var ddpowerzoomer={
	dsetting: {defaultpower:2, powerrange:[2,7], magnifiersize:[75, 75]},
	mousewheelevt: (/Firefox/i.test(navigator.userAgent))? "DOMMouseScroll" : "mousewheel", //FF doesn't recognize mousewheel as of FF3.x
	$magnifier: {outer:null, inner:null, image:null},
	activeimage: null,

	movemagnifier:function(e, moveBol, zoomdir){
		var activeimage=ddpowerzoomer.activeimage //get image mouse is currently over
		var activeimginfo=activeimage.info
		var coords=activeimginfo.coords //get offset coordinates of image relative to upper left corner of page
		var $magnifier=ddpowerzoomer.$magnifier
		var magdimensions=activeimginfo.magdimensions //get dimensions of magnifier
		var power=activeimginfo.power.current
		var powerrange=activeimginfo.power.range
		var x=e.pageX-coords.left //get x coords of mouse within image (where top corner of image is 0)
		var y=e.pageY-coords.top
		if (moveBol==true){
			if (e.pageX>=coords.left && e.pageX<=coords.right && e.pageY>=coords.top && e.pageY<=coords.bottom)  //if mouse is within currently within boundaries of active base image
				$magnifier.outer.css({left:e.pageX-magdimensions[0]/2, top:e.pageY-magdimensions[1]/2})	//move magnifier so it follows the cursor
			else{ //if mouse is outside base image
				ddpowerzoomer.activeimage=null
				$magnifier.outer.hide() //hide magnifier
			}
		}
		else if (zoomdir){ //if zoom in
			var od=activeimginfo.dimensions //get dimensions of image
			var newpower=(zoomdir=="in")? Math.min(power+1, powerrange[1]) : Math.max(power-1, powerrange[0]) //get new power from zooming in or out
			var nd=[od[0]*newpower, od[1]*newpower] //calculate dimensions of new enlarged image within magnifier
			$magnifier.image.css({width:nd[0], height:nd[1]})
			activeimginfo.power.current=newpower //set current power to new power after magnification
		}
		power=activeimginfo.power.current //get current power
		var newx=-x*power+magdimensions[0]/2 //calculate x coord to move enlarged image
		var newy=-y*power+magdimensions[1]/2
		$magnifier.inner.css({left:newx, top:newy}) //move image wrapper within magnifier so the correct image area is shown
	},

	setupimage:function($, imgref, options){
		var s=jQuery.extend({}, ddpowerzoomer.dsetting, options)
		var $imgref=$(imgref)
		imgref.info={ //create object to remember various info regarding image 
			power: {current:s.defaultpower, range:s.powerrange},
			magdimensions: s.magnifiersize,
			dimensions: [$imgref.width(), $imgref.height()],
			coords: null
		}
		$imgref.unbind('mouseenter').mouseenter(function(e){ //mouseenter event over base image
			var $magnifier=ddpowerzoomer.$magnifier
			$magnifier.outer.css({width:s.magnifiersize[0], height:s.magnifiersize[1]}) //set magnifier's size
			var offset=$imgref.offset() //get image offset from document
			var power=imgref.info.power.current
			$magnifier.inner.html('<img src="'+options.largeimagesrc+'"/>') //get base image's src and create new image inside magnifier based on it
			$magnifier.image=$magnifier.outer.find('img:first')
				.css({width:imgref.info.dimensions[0]*power, height:imgref.info.dimensions[1]*power}) //set size of enlarged image
			var coords={left:offset.left, top:offset.top, right:offset.left+imgref.info.dimensions[0], bottom:offset.top+imgref.info.dimensions[1]}
			imgref.info.coords=coords //remember left, right, and bottom right coordinates of image relative to doc
			$magnifier.outer.show()
			ddpowerzoomer.activeimage=imgref
		})
	},

	
	init:function($){
		var $magnifier=$('<div style="position:absolute;width:100px;height:100px;display:none;overflow:hidden;border:1px solid black;" />')
			.append('<div style="position:relative;left:0;top:0;" />')
			.appendTo(document.body) //create magnifier container and add to doc
		ddpowerzoomer.$magnifier={outer:$magnifier, inner:$magnifier.find('div:eq(0)'), image:null} //reference and remember various parts of magnifier
		$magnifier=ddpowerzoomer.$magnifier
		$(document).unbind('mousemove.trackmagnifier').bind('mousemove.trackmagnifier', function(e){ //bind mousemove event to doc
			if (ddpowerzoomer.activeimage){ //if mouse is currently over a magnifying image
				ddpowerzoomer.movemagnifier(e, true) //move magnifier
			}
		}) //end document.mousemove

		$magnifier.outer.bind(ddpowerzoomer.mousewheelevt, function(e){ //bind mousewheel event to magnifier
			if (ddpowerzoomer.activeimage){
				var delta=e.detail? e.detail*(-120) : e.wheelDelta //delta returns +120 when wheel is scrolled up, -120 when scrolled down
				if (delta<=-120){ //zoom out
					ddpowerzoomer.movemagnifier(e, false, "out")
				}
				else{ //zoom in
					ddpowerzoomer.movemagnifier(e, false, "in")
				}
				e.preventDefault()
			}
		})
	}
} //ddpowerzoomer

jQuery.fn.addpowerzoom=function(options){
	var $=jQuery
	return this.each(function(){ //return jQuery obj
		if (this.tagName!="IMG")
			return true //skip to next matched element
		if (typeof options=="undefined")
			options={}
		if (options.largeimage && options.largeimage.length>0){ //preload large image?
			options.preloadimg=new Image()
			options.preloadimg.src=options.largeimage
		}
		var $imgref=$(this)
		options.largeimagesrc=(options.preloadimg)? options.preloadimg.src : $imgref.attr('src')
		if (parseInt(this.style.width)>0 && parseInt(this.style.height)>0) //if image has explicit CSS width/height defined
			ddpowerzoomer.setupimage($, this, options)
		else if (this.complete){ //account for IE not firing image.onload
			ddpowerzoomer.setupimage($, this, options)
		}
		else{
			$imgref.bind('load', function(){
				ddpowerzoomer.setupimage($, this, options)
			})
		}
	})
}