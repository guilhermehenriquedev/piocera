let allergies = [];

document
	.querySelector('button[name=adicionar]')
	.addEventListener('click', () => {
		let alergia = document.querySelector('input[name=allergy]');

		allergies.push(alergia.value);

		let listaAlergias = document.querySelector('.list-allergies');

		listaAlergias.innerHTML = '';
		allergies.map((item) => {
			listaAlergias.innerHTML += `<div class="rounded-lg bg-gray-200 p-2 text-xs text-gray-700 font-medium flex text-center">` + item + `</div>`;
		});

		alergia.value = '';

		console.log(allergies);
	});

document.querySelector('button[name=limpar]').addEventListener('click', () => {
	allergies = [];

	document.querySelector('.list-allergies').innerHTML = '';
});

function concluir() {
	let alergia = document.querySelector('input[name=allergy]');
	alergia.value = allergies;
}


