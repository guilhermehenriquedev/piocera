let pixButton = document.querySelector('button[name=pix-button]');
let creditButton = document.querySelector('button[name=credit-button]');

let cardInfoPix = document.querySelector('.pix-card');
let cardInfoCredit = document.querySelector('.credit-card');

pixButton.addEventListener('click', () => {
	pixButton.classList.toggle('border-4');
	pixButton.classList.toggle('border-[#83B746]');

	creditButton.classList.remove('border-4');
	creditButton.classList.remove('border-[#83B746]');

	cardInfoCredit.classList.add('hidden');
	cardInfoCredit.classList.remove('flex');

	cardInfoPix.classList.toggle('hidden');
	cardInfoPix.classList.toggle('flex');
});

creditButton.addEventListener('click', () => {
	creditButton.classList.toggle('border-4');
	creditButton.classList.toggle('border-[#83B746]');

	pixButton.classList.remove('border-4');
	pixButton.classList.remove('border-[#83B746]');

	cardInfoPix.classList.add('hidden');
	cardInfoPix.classList.remove('flex');

	cardInfoCredit.classList.toggle('hidden');
	cardInfoCredit.classList.toggle('flex');
});
