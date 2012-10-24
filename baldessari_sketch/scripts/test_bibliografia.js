if(typeof liste_biblio != 'undefined'){
	
	var cont = d3.select("#content").append("div")
	
	for(var i = 0 ; i < liste_biblio.length ; i++){
		cont.append("p").text(liste_biblio[i]);
	}
}