import * from "crawler";

var spi = new Crawler({
	maxConnections : 10,
	// This will be called for each crawled page
	callback : function (error, res, done) {
		if(error){
			console.log(error);
		}else{
			var $ = res.$;
			// $ is Cheerio by default
			//a lean implementation of core jQuery designed specifically for the server
			console.log($("title").text());
		}
		done();
	}
});

console.log(spi.queue("https://en.wikipedia.org/wiki/Paprika_(2006_film)"))

console.log(spi)
