function(properties, context) {
	
    const cheerio = require("cheerio");
    const axios = require('axios')

    const url = properties.url

    async function getParas () {
        var paragraphs = "";
        const $ = cheerio.load(await
            axios
            .get(url)
            .then(res => res.data)
            .catch(error => {
                console.error(error)
            })
        );
        paragraphs = $('p').text();
        return paragraphs
    }
    
    let data = context.async(async callback => {
		try{
			let data = await getParas()
			callback(null, data);
		}
		catch(err){
			callback(err);
		}
	});
	return {text: data}
}