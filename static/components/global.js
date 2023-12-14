class FooterHome extends HTMLElement {
	connectedCallback() {
		this.innerHTML = `
			<div
				class="text-white bg-[#709B74] flex flex-col items-center justify-center py-12 md:py-24 px-10 md:px-20 gap-20 md:gap-28"
			>
				<div
					class="grid grid-cols-1 lg:grid-cols-3 gap-y-12 gap-x-4 text-base text-start w-full"
				>
                    <a href="/pages/home.html">
					    <img src="/static/images/logos/cerapioBranca.png" class="max-w-[150px]" />
                    </a>
					<div
						class="lg:col-span-2 w-full grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-y-9 gap-x-6 text-base text-start"
					>
						<div class="flex flex-col gap-6 font-semibold">
							<div>Competidor</div>
							<div class="flex flex-col gap-2">
								<a href="#" class="hover:text-gray-200">Home</a>
								<a href="#" class="hover:text-gray-200">O Evento</a>
								<a href="#" class="hover:text-gray-200">Notícias</a>
								<a href="#" class="hover:text-gray-200">Agência de Viagens</a>
							</div>
						</div>
						<div class="flex flex-col gap-6 font-semibold">
							<div>Parceiro</div>
							<div class="flex flex-col gap-2">
								<a href="#" class="hover:text-gray-200">Números do Evento</a>
								<a href="#" class="hover:text-gray-200">O Evento nas mídias</a>
								<a href="#" class="hover:text-gray-200">Lista de Parceiros</a>
							</div>
						</div>
						<div class="flex flex-col gap-6 font-semibold">
							<div>Redes Sociais</div>
							<div class="flex flex-col gap-2">
								<a href="#" class="hover:text-gray-200 flex flex-row items-center gap-1">
									<img
										src="/static/images/home/redesSociais/facebook.png"
									/>Facebook
								</a>
								<a href="#" class="hover:text-gray-200 flex flex-row items-center gap-1">
									<img
										src="/static/images/home/redesSociais/instagram.png"
									/>Instagram
								</a>
								<a href="#" class="hover:text-gray-200 flex flex-row items-center gap-1">
									<img
										src="/static/images/home/redesSociais/youtube.png"
									/>Youtube
								</a>
							</div>
						</div>
					</div>
				</div>
				<div class="font-light text-sm text-center">
					© 2022 RADICAL, Produzido por Fábrica de Gênios
				</div>
			</div>
		`;
	}
}
customElements.define('footer-home', FooterHome);


class FooterEditions extends HTMLElement {
	connectedCallback() {
		this.innerHTML = `
			<nav class="flex flex-row gap-6 justify-start items-center p-5 w-full bg-[#386380]">
				<a href="/"><img src="/static/images/logos/pioceraBranca.png" class="w-32 shrink-0"/></a>
				<a href="/"><img src="/static/images/logos/cerapioBranca.png" class="w-32 shrink-0"/></a>
			</nav>
		`;
	}
}
customElements.define('footer-editions', FooterEditions);
