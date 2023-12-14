class CoPatrocinadoresHome extends HTMLElement {
	connectedCallback() {
		this.innerHTML = `
			<div class="bg-white flex flex-row scrollbar p-4 md:py-8 md:px-9 gap-4 md:gap-6 justify-between items-center overflow-x-auto mx-auto">
				<img src="/images/home/logos/farmaciasGlobo.png" class="w-24 xl:w-36"/>
				<img src="/images/home/logos/farmaciasGlobo.png" class="w-24 xl:w-36"/>
				<img src="/images/home/logos/farmaciasGlobo.png" class="w-24 xl:w-36"/>
				<img src="/images/home/logos/farmaciasGlobo.png" class="w-24 xl:w-36"/>
				<img src="/images/home/logos/governoDoMaranhao.png" class="w-24 xl:w-36"/>
				<img src="/images/home/logos/goodYear.png" class="w-24 xl:w-36"/>
				<img src="/images/home/logos/goodYear.png" class="w-24 xl:w-36"/>
			</div>
		`;
	}
}
customElements.define('co-patrocinadores-home', CoPatrocinadoresHome);

class LotesHome extends HTMLElement {
	connectedCallback() {
		this.innerHTML = `
			<div class="w-full flex border-y-[23px] md:border-y-[47px] border-[#8FC74A]">
				<div class="w-full flex flex-col lg:flex-row p-6 sm:py-8 sm:px-10 justify-between gap-y-6 gap-x-9 items-center lg:container mx-auto">	
					<div class="flex flex-row gap-2 items-center  text-white font-semibold">
						<div class="flex rounded-lg bg-[#8FC74A] flex-col justify-center items-center p-2 w-[70px] sm:w-[80px]">
							<div class="text-xl">00</div>
							<div class="text-xs sm:text-sm">Dias</div>
						</div>
						<div class="flex rounded-lg bg-[#8FC74A] flex-col justify-center items-center p-2 w-[70px] sm:w-[80px]">
							<div class="text-xl">00</div>
							<div class="text-xs sm:text-sm">Horas</div>
						</div>
						<div class="flex rounded-lg bg-[#8FC74A] flex-col justify-center items-center p-2 w-[70px] sm:w-[80px]">
							<div class="text-xl">00</div>
							<div class="text-xs sm:text-sm">Minutos</div>
						</div>
						<div class="flex rounded-lg bg-[#8FC74A] flex-col justify-center items-center p-2 w-[70px] sm:w-[80px]">
							<div class="text-xl">00</div>
							<div class="text-xs sm:text-sm">Segundos</div>
						</div>
					</div>
					<div class="flex flex-col items-center gap-1 text-[#545454] uppercase">
						<div class="text-3xl font-black">1° lote disponível</div>
						<div class="text-sm font-light tracking-[10px]">Vagas limitadas</div>
					</div>
					<div class="flex justify-center items-center xl:w-[340px]">
						<button type="button" class="bg-[#8FC74A] rounded-lg py-3 px-4 flex gap-y-6 text-white font-semibold">
							Garanta sua inscrição
						</button>
					</div>
				</div>
			</div>
		`;
	}
}
customElements.define('lotes-home', LotesHome);
