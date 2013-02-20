settings = {
			mode : "elenco",
			type : "documents",
			sort : "alphab",
			itemsNumber : 10,
			filters : []
		}

d3.selectAll('#modes label, .filter, #types label')
	//.style('background-color', 'grey')
	.style('background-image', function(){
	return 'url('+static_prefix + 'img_interface/button_normal.jpg)';
}).style('background-size', '100% 100%').style('background-repeat', 'no-repeat');

/*Image Power Zoomer v1.1 (June 18th, 2010)
* This notice must stay intact for usage 
* Author: Dynamic Drive at http://www.dynamicdrive.com/
* Visit http://www.dynamicdrive.com/ for full source code
*/

//June 18th, 10: Adds ability to specify a different, higher resolution version of the original image as the image shown inside the magnifying glass.

//jQuery.noConflict()

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
	
	//changeMode(settings.mode);
}

var globalIndex = 0; //item that handle loading of items

//two arrays for driving items displaying
//a reference one, that changes just when user switch between project mode and document mode
var referenceArray = {};
//a dynamic one, that change regarding to filtering parameters
var dynamicArray = {};



var docCount = [];
for(var i = 0 ; i < 100 ; i++){
	docCount.push(0);
}


//for fist load
var dataLoaded = false;
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
		
	       $.get("getInfo", params, function(data){
	       		referenceArray = {}
				referenceArray = data;
				
				//this portion is just done in the begining
				if(!dataLoaded){
					dynamicArray = filterData();
					updateView();
					dataLoaded = true;
				}
		});
}



//this function updates dynamicArray regarding to filtering parameters
function filterData(){
	//first, copy the reference array
	array = {}
	array['list'] = []
	
	array['list'] = referenceArray['list'].slice()
	
	//console.log(referenceArray['list'])
	
	
	
	//filters
	if(settings.filters){
		for(key in settings.filters){
			var filter = settings.filters[key];
			switch(settings.filters[key].name){
				
				case 'date':
					for(var i = array.list.length-1 ; i >= 0 ; i--){
						
						var item = array.list[i];
						if(typeof(item['data']) == 'number'){
							if(item['data'] < filter.begining || item["data"]>filter.end){
								array.list.splice(i, 1);
							}
							
						}else{
							var min;
							var max;
							if(item['data'].length == 1){
								min = item['data'][0]['begining'];
								max = item['data'][0]['end'];
							}else{
								min = 2000;
								max = 0;
								for(j in item['data']){
									if (item['data'][j]['begining'] < min){
										min = item['data'][j]['begining'];
									}
									if (item['data'][j]['end'] > max){
										max = item['data'][j]['end'];
									}
								}
							}
							if(max < filter.begining | min > filter.begining){
									array.list.splice(i, 1);
							}
						}
					}				
				break;
				
				case 'projecttype':
				for(i in array.list){
						var item = array.list[i];
						var ok = true;
						for(j in settings.filters[key]['values']){
							if(item['tipo'] != settings.filters[key]['values'][j]){
									ok = false;
							}
						}
						if(!ok){
							array.list.splice(i, 1);
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

function sortData(){
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


//this function handle displayed items, adding and deleting regarding to scroll and filtering
function updateView(){
	
		if(dynamicArray.list.length > 0){
				if(settings.mode == 'elenco'){
					if(settings.type == 'documents'){
						for(var i = globalIndex ; i < globalIndex+settings.itemsNumber ; i++){
							//loadDivDoc(data.list[i]);
							docElenco(dynamicArray.list[i]);
						}
					}else if(settings.type == 'projects'){
						for(var i = globalIndex ; i < globalIndex+settings.itemsNumber ; i++){
							projElenco(dynamicArray.list[i]);
						}
					}
					globalIndex = globalIndex+settings.itemsNumber;
					}else{
						
						for(var i = globalIndex ; i < globalIndex+settings.itemsNumber ; i++){
							//loadDivDoc(data.list[i]);
							docGalleria(dynamicArray.list[i]);
						}
					globalIndex = globalIndex+settings.itemsNumber;
				}
			}	
			
			attributeButtons();
			d3.select('#detailgalleria').remove()
					
}

//this function format document div for elenco mode
function docElenco(data){
	var item = d3.select('#opere_display').append("div").datum(data);
	//var item = d3.select("#opere_display").selectAll('div');
	item.attr("class", "itemelenco")
	
	var left = item.append('div').attr('class', 'elenco_left')
						.append('a').attr("href", function(d){ return 'document/'+d.segnatura;})
	var img = left.append('img').attr('src', function(d){
							return static_prefix+ d.adressthumb;
						}).style("width", "100px").style("height", "70px")
		
		/*img.on('mouseover', function(){
			d3.select(this).transition().duration(300).style("height", "280px").style("width", "400px");
		}).on('mouseout', function(){
			d3.select(this).transition().duration(300).style("height", "70px").style("width", "100px");
		})*/
		
		
		
			var right = item.append('div').attr('class', 'elenco_right')
			right.append('a').attr("href", function(d){ return 'document/'+d.segnatura;}).append('h3').text(function(d){ return 'Documento '+d.segnatura;});
			right.append('p').text(function(d){
				return 'Progetto : '+d.project;
			})
			var links = right.append('p').attr('class', 'buttons_elenco');
			links.append('a').attr("href", function(d){
				return 'document/'+d.segnatura;
			}).text('Andare sulla scheda documento')
			links.append('a').attr("href", function(d){
				return 'project/' + d.projectid;
			}).text('Andare sulla scheda progetto')
	item.style('opacity', 0.1).transition().duration(1000).style('opacity', 1)
	
	img.style("height", "0px").transition().duration(800).style("height", "70px");
}

//this function format a document div for elenco mode
function projElenco(data){
	var item = d3.select('#opere_display').append("div").datum(data);
	//var item = d3.select("#opere_display").selectAll('div');
	item.attr("class", "itemelenco");
	
			var left = item.append('div').attr('class', 'elenco_left')
						.append("a").attr("href", function(d){return 'project/'+d.sigla;})
			var img = left.append('img').attr('src', function(d){
							return static_prefix+ d.adressthumb;
						}).style("width", "100px").style("height", "70px")

			
			
			var right = item.append('div').attr('class', 'elenco_right')
			right.append('a').attr("href", function(d){return 'project/'+d.sigla;}).append('h3').text(function(d){ return d.denominazione;});
			right.append('p').text(function(d){
				return 'Tipo : '+d.tipo;
			})
	item.style('opacity', 0.1).transition().duration(1000).style('opacity', 1);
	img.style("height", "0px").transition().duration(800).style("height", "70px");
}

//this function format document div for elenco mode
function docGalleria(data){
	d3.selectAll('#types').remove()
	var item = d3.select('#opere_display').append("div").datum(data);
	//var item = d3.select("#opere_display").selectAll('div');
	item.attr("class", "itemgalleria")
	
	var img = item.append('a').attr("href", function(d){
								return 'document/'+d.segnatura;
							})
					.append('img').attr('src', function(d){
							return static_prefix+ d.adressthumb;
						}).style("width", "100px").style("height", "70px")
						.attr('title', function(d){return d.segnatura;})
	img.on('mouseover', function(d){
			d3.selectAll('.detailgalleria').remove();
				//var div = d3.select(this);
				var div = $(this);
				var pos = div.position();
				var x = pos.left;//+parseInt(div.width()/2);
				var y = pos.top;
				//var y = div.height();
				var detail = d3.select('#opere_viz_space').append('div').attr("class", "detailgalleria");
				data = d;
				
				detail.style('left', function(d){return x - 10;}).style('top', function(d){return y-10;});
				
				var img1 = detail.append('a').attr("href", function(d){
								return 'document/'+data.segnatura;
							}).append('img').attr('src', function(d){
							return static_prefix
							+ data.adressimage;
						}).style("width", "300px").style('cursor', 'crosshair').attr('id', 'imagezoom')
				
				$('#imagezoom').addpowerzoom({
					defaultpower: 2,
					powerrange: [2,5],
					largeimage: null,
					magnifiersize: [150,150] //<--no comma following last option!
				})				
	/*var img2 = detail.append('a').attr("href", function(d){
								return 'document/'+data.segnatura;
							}).append('img').attr('src', function(d){
							return static_prefix
							+ data.adressimage;
						}).style("width", "300px").style('height', '300px')*/
						
						
				detail.append('h4').text(function(){ return "documento " + data.segnatura;})
				//detail.append("p").text(function(return data.))
				
				/*detail.on("mouseout", function(){
					d3.select(this).remove();
				})*/
	})
						
	item.style('opacity', 0.1).transition().duration(1000).style('opacity', 1);
	img.style("height", "0px").transition().duration(800).style("height", "70px");
}



//behavior when scrolling
$(window).scroll(function(){
	if($(window).scrollTop() + $(window).height() > $(document).height() - 50 && $(window).height() < $(document).height()) {
		
		if(globalIndex+settings.itemsNumber< dynamicArray.list.length){
			updateView();
		}
	}
})



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
				globalIndex = 0; //index to handle dynamic loading of items
				//delete former files
				d3.select('#opere_display').selectAll("div")/*.style("opacity", 1).transition().duration(500).style("opacity", 0)*/
					.remove();
													
				dataLoaded = false;//reinitialize the state of data (to handle actions stack regarding to ajax)
				loadData();
				
				//change url
				updateURL();
			}
			
		});
}
	
	
	
//changing the visualization modes
function changeMode(value){
	d3.select('#opere_display').selectAll('div').style("opacity", 1).transition().duration(500).style('opacity', 0e-6).remove();
	d3.select('#types').style("opacity", 1).transition().duration(500).style('opacity', 0e-6).remove();
	if(value == 'elenco' && $("#types").length == 0){
		var cont = d3.select("#params1").append("div").attr("id", "types");
		/*var cont2 = cont.append('ul').attr("id", "opere_switchtype_ul");
		var label1 = cont2.append('li').append("label")*/
		
		cont.html('<form method="post" id="opere_switchtype_form" action="/switchtype/"><ul id="opere_switchtype_ul"><li><label><input checked="checked" type="radio" name="typeviz" id="doctype" value="documents">Documenti</label></li><li><label><input type="radio" name="typeviz" id="projtype" value="projects">Progetti</label></li></ul></form>')
		cont.selectAll('label').style('background-image', function(){
						return 'url('+static_prefix + 'img_interface/button_normal.jpg)';
					}).style('background-size', '100% 100%').style('background-repeat', 'no-repeat')
		dataLoaded  = false;
		settings.itemsNumber = 10;
		switchType();
		loadData();
		cont.style("opacity", 0e-6).transition().duration(500).style("opacity", 1);
	}else if (value == 'galleria'){
		dataLoaded = false;
		settings.type = 'documents';
		settings.itemsNumber = 100;
		loadData();
	}
}
				

//interface handling
d3.select("#opere_modes_ul").selectAll("input").on("click", function(){
		var value = d3.select(this).attr("value");
		if(value != settings.mode){
			changeMode(value);
			settings.mode = value;
			updateURL();
		}
		
	});
	
/*d3.select("#testfilter").on('click', function(){
	
	//set new parameter
	settings['filters'] = [
				{
					name : "date",
					begining : '1920',
					end : '1950'
				}
			]	
	
	//update dynamicArray
	//var newArray = filterData();
	//enters and exits
	//enterExist(newArray['list'], dynamicArray['list']);
	
	//update the array
	dynamicArray = filterData();
	globalIndex = 0;
	d3.select('#opere_display').selectAll('div').style("opacity", 1).transition().duration(500).style('opacity', 0e-6).remove();
	updateView();
	updateURL();
})*/

d3.select('#typefilter').on('click', function(){
	
	if($('#typefiltermenu').length == 0){
		
			d3.select(this).style('background-image', function(){
				return 'url('+static_prefix + 'img_interface/button_selected.jpg)';
			})

			$.get('getInfo', {action : 'getTipi'}, function(data){
				//register all types of projects
				var tipi = data['tipi'];
				
				var div = $('#typefilter');
				var pos = div.position()
				var x = div.position().left//+parseInt(div.width()/2);
				var y = div.height();		
									
				var cont = d3.select('#opere_viz_space').append("div").attr('id', 'typefiltermenu')
						.style("left", function(){return x;})
						.style("top", function(){return parseInt(pos.top + y+10);})
				
				cont.selectAll('p').data(tipi).enter().append('p').text(function(d){return d;})
					.style('background-size', '100% 100%').style('background-repeat', 'no-repeat')
					.style('margin', 0)
					.style('padding', 10)
					.style('background', function(d){
						if(settings.filters){
							var projecttype = {}
							var exists = false;
							for(i in settings['filters']){
								if (settings['filters'][i]['name'] == 'projecttype'){
									exists = true;
									projecttype = settings['filters'][i];
								}
							}
							if(exists){
								var present = false;
							
								for(i in projecttype.values){
									if(projecttype.values[i] == d){
										present = true;
									}
								}
								if(present)return 'grey';
								else return 'white';
								
							}else return 'grey'
						}else return 'grey';
					})
					.style('color', function(d){
						if(settings.filters){
								var projecttype = {}
								var exists = false;
								for(i in settings['filters']){
									if (settings['filters'][i]['name'] == 'projecttype'){
										exists = true;
										projecttype = settings['filters'][i];
									}
								}
								if(exists){
									var present = false;
								
									for(i in projecttype.values){
										if(projecttype.values[i] == d){
											present = true;
										}
									}
									if(present)return "white";
									else return "black";
									
								}else return "white"
							}else return "white";
					})
					.on("click", function(d){

						
						var projecttype = {}
						var exists = false;
						for(i in settings['filters']){
							if (settings['filters'][i]['name'] == 'projecttype'){
								exists = true;
								projecttype = settings['filters'][i];
							}
						}
						
						if(!exists){
							projecttype = {
															name : 'projecttype',
															values : tipi
														}
							settings['filters'].push(projecttype);
						}
						
						
						var present = false;
						var index = 0;
						
						
						
						for(i in projecttype['values']){
							if(projecttype['values'][i] == d){
								present = true;
								index = i;
							}
						}
						
						if(present){
							projecttype['values'].splice(index, 1);
							d3.select(this).style('color', 'white').style('background', 'grey');
						}else{
							//add
							projecttype['values'].push(d);
							d3.select(this).style('color', 'black').style('background', 'white');
						}
						d3.select('#opere_display').selectAll('div').style("opacity", 1).transition().duration(500).style('opacity', 0e-6).remove();
						filterData();
						updateView();
						
					})
				
				});
		
	}else{
		d3.select('#typefiltermenu').remove();
		
		d3.select(this).style('background-image', function(){
				return 'url('+static_prefix + 'img_interface/button_normal.jpg)';
			})
	}
	
	
	
})

d3.select('#datefilter').on('click', function(){
	if($('#datefiltermenu').length == 0){
		
		d3.select(this).style('background-image', function(){
		return 'url('+static_prefix + 'img_interface/button_selected.jpg)';
			})
		
		$.get('getInfo', {action : 'getDatesOverview'}, function(data){
		
				var div = $('#testfilter');
				var pos = div.position();
				var y = div.height();
				
				
				//feedDateOverView();
				
				var cont = d3.select('#opere_viz_space').append("div").attr('id', 'datefiltermenu')
						.style("left", function(){return parseInt(pos.left);})
						.style("top", function(){return parseInt(pos.top + y+10);})
						
				
				var margin = {top: 10, right: 10, bottom: 20, left: 10},
				    width = 960 - margin.right - margin.left,
				    height = 100 - margin.top - margin.bottom;
				
				var x = d3.scale.linear().domain([0, 600])
				    .range([0, width]);
				
				var y = d3.random.normal(height / 2, height / 8);
				
				var svg = cont.append("svg")
				    .attr("width", width + margin.right + margin.left)
				    .attr("height", height + margin.top + margin.bottom)
				  .append("g")
				    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");
				
				svg.append("g")
				    .attr("class", "x axis")
				    .attr("transform", "translate(0," + height + ")")
				    .call(d3.svg.axis().scale(x).orient("bottom"));
				
				var rect = svg.append("g").selectAll("rect")
				    .data(data)
				  .enter().append("rect")
				    .attr("transform", function(d) { return "translate(" + x(d) + "," + y() + ")"; })
				    .attr("height", function(d){return y();})
				    .attr("width", 3.5);
				
				svg.append("g")
				    .attr("class", "brush")
				    .call(d3.svg.brush().x(x)
				    .on("brushstart", brushstart)
				    .on("brush", brushmove)
				    .on("brushend", brushend))
				  .selectAll("rect")
				    .attr("height", height);
				
				function brushstart() {
				  svg.classed("selecting", true);
				}
				
				function brushmove() {
				  var s = d3.event.target.extent();
				  rect.classed("selected", function(d) { return s[0] <= d && d <= s[1]; });
				}
				
				function brushend() {
				  svg.classed("selecting", !d3.event.target.empty());
				}
		
		});	
		
	}else{
		d3.select('#datefiltermenu').remove();
		
		d3.select(this).style('background-image', function(){
		return 'url('+static_prefix + 'img_interface/button_normal.jpg)';
	})
	}
})


function feedDateOverView(){
	var counter = 0 ;
	for(var i = 0 ; i < referenceArray.list.length ; i++){
		dates = referenceArray.list[i].data;
		
		if(typeof(dates) == 'number'){
			docCount[k-1900-1] = docCount[k-1900-1]+1;
		}else{
			if(dates.length == 1){
				var begining = dates[0]['begining']-1901;
				var interval = dates[0]['begining']-dates[0]['end'];
				if(interval < 0) interval = -interval;
				
				if(begining+interval > 99){
					docCount[begining] = docCount[begining] +1;
					counter++;
					
				}else{
					for(var k = begining ; k < begining+interval; k++){
						docCount[k] = docCount[k]+1;
						counter++;
						if(k>max) k = max;
					}
					
				}
				
			}else{
				for(j in dates){
					
						var begining = dates[j]['begining']-1901;
						var interval = dates[j]['begining']-dates[j]['end'];
						if(interval < 0) interval = -interval;
						
						if(begining+interval > 99){
							docCount[begining] = docCount[begining] +1;
							counter++;
							
						}else{
							for(var k = begining ; k < begining+interval; k++){
								docCount[k] = docCount[k]+1;
								counter++;
							}
							
						}
					
					/*for(var n = dates[j]['begining'] ; n < dates[j]['end']; n++){
						docCount[n-1900-1] = docCount[n-1900-1]+1;
					}*/
				}
			}
		}
	}
}


//loading documents on start
$(document).ready(function(){
	parseURL();
	switchType();
	loadData();
	attributeButtons();
	ddpowerzoomer.init($)
});




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
