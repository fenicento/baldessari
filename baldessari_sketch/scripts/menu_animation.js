


//add a floating div with a svg inside
d3.select('#content').style('margin-top', function(){
	var height = d3.select('header')[0][0].offsetHeight;
	return height;
})

var cursormenudiv = d3.select("header").append("div")
							     .style("position", "relative")
							     .attr("id", "menucursor")
							     .attr("display", "inline")
							     //.style("float", "left")
							     .attr("margin", "0px")
							     .attr("padding", "0px")
							     .style("left", "10px")
							     .style("bottom", '-1px')
							     .style('width', '20px')
							     .style('height', '15px')
							     ;

var cursormenusvg = d3.select("#menucursor").append("svg:svg")
											.attr("width", function(){
												return "20px";
											})
											.attr("height", function(){
												return "15px";
											})
												

											
//draw a triangle in the svg
cursormenusvg.append('svg:path')
      .attr('d', function(d) { 
        var x = 10, y = 10;
        return 'M ' + x +' '+ y + ' l 4 4 l -8 0 z';
      })
     .style("fill", "#f2f2f0")
     
     
d3.select('header').style('height', function(){
	var height = d3.select('#menu')[0][0].offsetHeight + d3.select('#menucursor')[0][0].offsetHeight;
	return height;
})

//set behavior for begining
var idname = '';
if(typeof section_name != "undefined"){
	idname = section_name + "menu";
	
	d3.select("#"+idname+" a").style("color", "#f2f2f0");
	
	var target = document.getElementById(idname);
		var pos = parseInt(target.offsetLeft + (target.offsetWidth/2))
					-target.parentNode.offsetLeft-5;
	d3.select("#menucursor").style("left", function(){return pos+"px";	});
}


//set behavior of elements regarding to mouseover
var itemsanim = d3.selectAll("#menu li a")
										.on("mouseover", function(){
											d3.select(this).transition().duration(300)
															.style("color", "#f2f2f0")
										
										var pos = parseInt(this.offsetLeft + (this.offsetWidth/2))-this.parentNode.parentNode.offsetLeft-5;
										
										
										//moving the little triangle
										d3.select("#menucursor")
											.transition()
											.duration(500)
											.style("left", function(){
												return pos+"px";
											});
										})
										.on("mouseout", function(){
											if(this.parentNode.id != idname){
												d3.select(this).transition().duration(300)
												.style("color", "#8b8b7f")
											}
										})


//set behavior of the title
var titleanim = d3.select("#bannertext").style("opacity", 1)
										.on("mouseover", function(){
											d3.select(this).transition().duration(300)
															.style("opacity", 0.8)
										})
										.on("mouseout", function(){
											d3.select(this).transition().duration(300)
															.style("opacity", 1)
										})
										
										
//animation on mouseover
d3.select('#bannertext').style('opacity', 0e-6).style('top', function(){
	var height = -10 -d3.select('#bannertext')[0][0].offsetHeight;
	return height;
})

d3.select('header').on('mouseover', function(){
	var height = d3.select('#bannertext')[0][0].offsetHeight + 10;
	d3.select(this).transition().duration(500).delay(500).style('height', function(){return height;})
	d3.select('#bannertext').transition().duration(500).delay(500).style('opacity', 1)
	.style('top', '-10px');
})
.on('mouseout', function(){
	var height = d3.select('#menu')[0][0].offsetHeight + d3.select('#menucursor')[0][0].offsetHeight;
	d3.select(this).transition().duration(200).delay(500).style('height', function(){return height;})
	
	d3.select('#bannertext').transition().duration(200).delay(500).style('opacity', 0e-6).style('top', function(){
		var height = -10 -d3.select('#bannertext')[0][0].offsetHeight;
	return height;
	})
})
