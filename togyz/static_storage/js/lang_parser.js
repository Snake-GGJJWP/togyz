const lang_data = JSON.parse(document.getElementById('lang-data').textContent);

function parse(obj) { 
	for (key in obj) {
		let els = document.querySelectorAll(`[name='${key}']`);
		console.log(els);
		for (let i = 0; i < els.length; i++) { 
			els[i].innerHTML += obj[key];
		}
	}
};

parse(lang_data);