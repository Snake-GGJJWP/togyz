const lang_data = JSON.parse(document.getElementById('lang-data').textContent);

function parse(obj) { 
	for (key in obj) {
		console.log(obj[key])
		let el = document.getElementById(key);
		el.innerHTML += obj[key];
	}
};

parse(lang_data);