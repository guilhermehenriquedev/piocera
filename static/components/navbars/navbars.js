class NavbarHome extends HTMLElement {
	connectedCallback() {
		this.innerHTML = `
			<nav class="navbar">
				<a href="/"><img src="/static/images/logos/cerapioBranca.png" class="w-32 shrink-0"/></a>
				<ul class="nav-links w-full justify-end xl:justify-center items-center flex pr-4 xl:pr-0">
					<input type="checkbox" id="checkbox_toggle_home" class="input-navbar"/>
					<label for="checkbox_toggle_home" class="cursor-pointer hamburger">&#9776;</label>
					<div class="menu font-bold gap-4">
						<li><a href="/">Home</a></li>
						<li><a href="/">O evento</a></li>
						<li><a href="/">Notícias</a></li>
						<li><a href="/">Agência de viagens</a></li>
						<li><a href="/">Contato</a></li>
						<li><a href="/">Área do competidor</a></li>
					</div>
				</ul>

                <a href="/static/pages/inscricao/modalidade.html">
                    <button type="button" class="bg-[#8FC74A] rounded-lg py-3 px-4 flex">
                        <img src="/static/images/home/inscricao.png"/>
                    </button>
                </a><!--Caso o usuário não esteja logado-->

				<!--<div class="cursor-pointer text-[#545454] bg-white rounded-lg px-3 py-2 flex items-center justify-center flex-row gap-2">
					<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6 shrik-0">
						<path 
							stroke-linecap="round" 
							stroke-linejoin="round" 
							d="M17.982 18.725A7.488 7.488 0 0012 15.75a7.488 7.488 0 00-5.982 2.975m11.963 0a9 9 0 10-11.963 0m11.963 0A8.966 8.966 0 0112 21a8.966 8.966 0 01-5.982-2.275M15 9.75a3 3 0 11-6 0 3 3 0 016 0z"
						/>
					</svg>
					<div class="text-sm font-medium">Username</div>
					<svg width="13" height="8" viewBox="0 0 13 8" fill="none" xmlns="http://www.w3.org/2000/svg">
						<path d="M1.5 1.5L6.5 6.5L11.5 1.5" stroke="#344054" stroke-width="1.66667" stroke-linecap="round" stroke-linejoin="round"/>
					</svg>
				</div>--><!--Caso o usuário esteja logado-->
			</nav>
		`;
	}
}
customElements.define('navbar-home', NavbarHome);

class NavbarReduzidaInscricao extends HTMLElement {
	connectedCallback() {
		this.innerHTML = `
			<nav class="navbar-inscricao">
				<a href="/">
					<img src="{{logo.SITE_LOGO_BRANCA}}" class="w-32 shrink-0"/>
				</a><!--Caso o usuário não esteja logado-->
				<!--<button type="button" class="bg-[#8FC74A] rounded-lg p-2 sm:py-3 sm:px-4 flex">
                    <img src="/static/images/inscricao/frases/inscricaoCerapio.png" class="max-w-[80px] sm:max-w-[150px]"/>
                </button>--><!--Caso o usuário esteja logado-->
				<ul class="nav-links-inscricao w-full justify-end xl:justify-center items-center flex pr-4 xl:pr-0">
					<input type="checkbox" id="checkbox_toggle_inscricao" class="input-navbar-inscricao"/>
					<label for="checkbox_toggle_inscricao" class="cursor-pointer hamburger-inscricao">&#9776;</label>
					<div class="menu-inscricao font-bold gap-4">
						<li><a href="/">Home</a></li>
						<li><a href="/">O evento</a></li>
						<li><a href="/">Notícias</a></li>
						<li><a href="/">Agência de viagens</a></li>
						<li><a href="/">Contato</a></li>
						<li><a href="/">Área do competidor</a></li>
					</div>
				</ul>

                <button type="button" class="bg-[#8FC74A] rounded-lg p-2 sm:py-3 sm:px-4 flex">
                    <img src="/static/images/inscricao/frases/inscricaoCerapio.png" class="max-w-[80px] sm:max-w-[150px]"/>
                </button><!--Caso o usuário não esteja logado-->

                <!--<div class="cursor-pointer text-[#545454] bg-white rounded-lg px-3 py-2 flex items-center justify-center flex-row gap-2">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6 shrik-0">
                        <path 
                            stroke-linecap="round" 
                            stroke-linejoin="round" 
                            d="M17.982 18.725A7.488 7.488 0 0012 15.75a7.488 7.488 0 00-5.982 2.975m11.963 0a9 9 0 10-11.963 0m11.963 0A8.966 8.966 0 0112 21a8.966 8.966 0 01-5.982-2.275M15 9.75a3 3 0 11-6 0 3 3 0 016 0z"
                        />
                    </svg>
                    <div class="text-sm font-medium">Username</div>
					<svg width="13" height="8" viewBox="0 0 13 8" fill="none" xmlns="http://www.w3.org/2000/svg">
						<path d="M1.5 1.5L6.5 6.5L11.5 1.5" stroke="#344054" stroke-width="1.66667" stroke-linecap="round" stroke-linejoin="round"/>
					</svg>
                </div>--><!--Caso o usuário esteja logado-->
			</nav>
		`;
	}
}
customElements.define('navbar-reduzida-inscricao', NavbarReduzidaInscricao);

class BannerInscriaoCerapio extends HTMLElement {
	connectedCallback() {
		this.innerHTML = `
            <nav class="hidden text-white lg:flex bg-cover bg-center w-full bg-no-repeat flex-col justify-center items-center gap-20 lg:p-10 xl:px-20 bg-[#C38934]" style="background-image: url(/static/images/inscricao/bannerDecoracaoInscricao.png);">
                <div class="w-full flex flex-row items-center justify-start">
                    <a href="/"><img src="/static/images/logos/branca.png" class="w-20 sm:w-32 hidden lg:block"/></a>
                    <ul class="nav-links w-full justify-start items-center flex lg:pl-9">
                        <input type="checkbox" id="checkbox_toggle" class="input-navbar"/>
                        <div class="menu-inscricao font-bold gap-4">
                            <li><a href="/"><img src="/static/images/logos/branca.png" class="w-20 sm:w-32 block lg:hidden"/></a></li>
                            <li><a href="/">Home</a></li>
                            <li><a href="/">O evento</a></li>
                            <li><a href="/">Notícias</a></li>
                            <li><a href="/">Agência de viagens</a></li>
                            <li><a href="/">Contato</a></li>
                            <li><a href="/">Área do competidor</a></li>
                        </div>
                    </ul>
					<!--<div class="cursor-pointer text-[#545454] bg-white rounded-lg px-3 py-2 flex items-center justify-center flex-row gap-2">
						<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6 shrik-0">
							<path 
								stroke-linecap="round" 
								stroke-linejoin="round" 
								d="M17.982 18.725A7.488 7.488 0 0012 15.75a7.488 7.488 0 00-5.982 2.975m11.963 0a9 9 0 10-11.963 0m11.963 0A8.966 8.966 0 0112 21a8.966 8.966 0 01-5.982-2.275M15 9.75a3 3 0 11-6 0 3 3 0 016 0z"
							/>
						</svg>
						<div class="text-sm font-medium">Username</div>
						<svg width="13" height="8" viewBox="0 0 13 8" fill="none" xmlns="http://www.w3.org/2000/svg">
							<path d="M1.5 1.5L6.5 6.5L11.5 1.5" stroke="#344054" stroke-width="1.66667" stroke-linecap="round" stroke-linejoin="round"/>
						</svg>
					</div>--><!--Caso o usuário esteja logado-->
                </div>
                <img src="/static/images/inscricao/frases/inscricaoCerapio.png" class="sm:w-1/2 hidden lg:block"/>
			</nav>
            <navbar-reduzida-inscricao></navbar-reduzida-inscricao>
		`;
	}
}
customElements.define('banner-inscricao-cerapio', BannerInscriaoCerapio);

class BannerFormularioCerapio extends HTMLElement {
	connectedCallback() {
		this.innerHTML = `
            <nav class="hidden text-white lg:flex bg-cover bg-center w-full bg-no-repeat flex-col justify-center items-center gap-20 lg:p-10 xl:px-20 bg-[#C38934]" style="background-image: url(/static/images/inscricao/bannerDecoracaoInscricao.png);">
                <div class="w-full flex flex-row items-center justify-start">
                    <a href="/"><img src="/static/images/logos/branca.png" class="w-20 sm:w-32 hidden lg:block"/></a>
                    <ul class="nav-links w-full justify-start items-center flex lg:pl-9">
                        <input type="checkbox" id="checkbox_toggle" class="input-navbar"/>
                        <div class="menu-inscricao font-bold gap-4">
                            <li><a href="/"><img src="/static/images/logos/branca.png" class="w-20 sm:w-32 block lg:hidden"/></a></li>
                            <li><a href="/">Home</a></li>
                            <li><a href="/">O evento</a></li>
                            <li><a href="/">Notícias</a></li>
                            <li><a href="/">Agência de viagens</a></li>
                            <li><a href="/">Contato</a></li>
                            <li><a href="/">Área do competidor</a></li>
                        </div>
                    </ul>
					<!--<div class="cursor-pointer text-[#545454] bg-white rounded-lg px-3 py-2 flex items-center justify-center flex-row gap-2">
						<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6 shrik-0">
							<path 
								stroke-linecap="round" 
								stroke-linejoin="round" 
								d="M17.982 18.725A7.488 7.488 0 0012 15.75a7.488 7.488 0 00-5.982 2.975m11.963 0a9 9 0 10-11.963 0m11.963 0A8.966 8.966 0 0112 21a8.966 8.966 0 01-5.982-2.275M15 9.75a3 3 0 11-6 0 3 3 0 016 0z"
							/>
						</svg>
						<div class="text-sm font-medium">Username</div>
						<svg width="13" height="8" viewBox="0 0 13 8" fill="none" xmlns="http://www.w3.org/2000/svg">
							<path d="M1.5 1.5L6.5 6.5L11.5 1.5" stroke="#344054" stroke-width="1.66667" stroke-linecap="round" stroke-linejoin="round"/>
						</svg>
					</div>--><!--Caso o usuário esteja logado-->
                </div>
                <img src="/static/images/inscricao/frases/formularioCerapio.png" class="sm:w-1/2 hidden lg:block"/>
			</nav>
            <navbar-reduzida-inscricao></navbar-reduzida-inscricao>
		`;
	}
}
customElements.define('banner-formulario-cerapio', BannerFormularioCerapio);

class BannerFormularioPiocera extends HTMLElement {
	connectedCallback() {
		this.innerHTML = `
            <nav class="hidden text-white lg:flex bg-cover bg-center w-full bg-no-repeat flex-col justify-center items-center gap-20 lg:p-10 xl:px-20 bg-[#C38934]" style="background-image: url(/static/images/inscricao/bannerDecoracaoInscricao.png);">
                <div class="w-full flex flex-row items-center justify-start">
                    <a href="/"><img src="/static/images/logos/branca.png" class="w-20 sm:w-32 hidden lg:block"/></a>
                    <ul class="nav-links w-full justify-start items-center flex lg:pl-9">
                        <input type="checkbox" id="checkbox_toggle" class="input-navbar"/>
                        <div class="menu-inscricao font-bold gap-4">
                            <li><a href="/"><img src="/static/images/logos/branca.png" class="w-20 sm:w-32 block lg:hidden"/></a></li>
                            <li><a href="/">Home</a></li>
                            <li><a href="/">O evento</a></li>
                            <li><a href="/">Notícias</a></li>
                            <li><a href="/">Agência de viagens</a></li>
                            <li><a href="/">Contato</a></li>
                            <li><a href="/">Área do competidor</a></li>
                        </div>
                    </ul>
					<!--<div class="cursor-pointer text-[#545454] bg-white rounded-lg px-3 py-2 flex items-center justify-center flex-row gap-2">
						<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6 shrik-0">
							<path 
								stroke-linecap="round" 
								stroke-linejoin="round" 
								d="M17.982 18.725A7.488 7.488 0 0012 15.75a7.488 7.488 0 00-5.982 2.975m11.963 0a9 9 0 10-11.963 0m11.963 0A8.966 8.966 0 0112 21a8.966 8.966 0 01-5.982-2.275M15 9.75a3 3 0 11-6 0 3 3 0 016 0z"
							/>
						</svg>
						<div class="text-sm font-medium">Username</div>
						<svg width="13" height="8" viewBox="0 0 13 8" fill="none" xmlns="http://www.w3.org/2000/svg">
							<path d="M1.5 1.5L6.5 6.5L11.5 1.5" stroke="#344054" stroke-width="1.66667" stroke-linecap="round" stroke-linejoin="round"/>
						</svg>
					</div>--><!--Caso o usuário esteja logado-->
                </div>
                <img src="/static/images/inscricao/frases/formularioPiocera.png" class="sm:w-1/2 hidden lg:block"/>
			</nav>
            <navbar-reduzida-inscricao></navbar-reduzida-inscricao>
		`;
	}
}
customElements.define('banner-formulario-piocera', BannerFormularioPiocera);

class BannerAreaCompetidor extends HTMLElement {
	connectedCallback() {
		this.innerHTML = `
            <nav class="text-white flex bg-cover bg-center w-full bg-no-repeat flex-col justify-center items-center p-10 xl:px-20 bg-[#C38934]" style="background-image: url(/static/images/inscricao/bannerDecoracaoInscricao.png);">
                <div class="w-full flex flex-row items-center justify-between">
                    <a href="/"><img src="/static/images/logos/branca.png" class="w-20 sm:w-32"/></a>
					<div class="cursor-pointer text-[#545454] bg-white rounded-lg px-3 py-2 flex items-center justify-center flex-row gap-2">
						<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6 shrik-0">
							<path 
								stroke-linecap="round" 
								stroke-linejoin="round" 
								d="M17.982 18.725A7.488 7.488 0 0012 15.75a7.488 7.488 0 00-5.982 2.975m11.963 0a9 9 0 10-11.963 0m11.963 0A8.966 8.966 0 0112 21a8.966 8.966 0 01-5.982-2.275M15 9.75a3 3 0 11-6 0 3 3 0 016 0z"
							/>
						</svg>
						<div class="text-sm font-medium">Username</div>
						<svg width="13" height="8" viewBox="0 0 13 8" fill="none" xmlns="http://www.w3.org/2000/svg">
							<path d="M1.5 1.5L6.5 6.5L11.5 1.5" stroke="#344054" stroke-width="1.66667" stroke-linecap="round" stroke-linejoin="round"/>
						</svg>
					</div>
                </div>
			</nav>
		`;
	}
}
customElements.define('banner-area-competidor', BannerAreaCompetidor);

class BannerGaleriaCampeoes extends HTMLElement {
	connectedCallback() {
		this.innerHTML = `
            <nav class="hidden text-white lg:flex bg-cover bg-center w-full bg-no-repeat flex-col justify-center items-center gap-20 lg:p-10 xl:px-20 bg-[#C38934]" style="background-image: url(/static/images/inscricao/bannerDecoracaoInscricao.png);">
                <div class="w-full flex flex-row items-center justify-start">
                    <a href="/"><img src="/static/images/logos/branca.png" class="w-20 sm:w-32 hidden lg:block"/></a>
                    <ul class="nav-links w-full justify-start items-center flex lg:pl-9">
                        <input type="checkbox" id="checkbox_toggle" class="input-navbar"/>
                        <div class="menu-inscricao font-bold gap-4">
                            <li><a href="/"><img src="/static/images/logos/branca.png" class="w-20 sm:w-32 block lg:hidden"/></a></li>
                            <li><a href="/">Home</a></li>
                            <li><a href="/">O evento</a></li>
                            <li><a href="/">Notícias</a></li>
                            <li><a href="/">Agência de viagens</a></li>
                            <li><a href="/">Contato</a></li>
                            <li><a href="/">Área do competidor</a></li>
                        </div>
                    </ul>
					<!--<div class="cursor-pointer text-[#545454] bg-white rounded-lg px-3 py-2 flex items-center justify-center flex-row gap-2">
						<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6 shrik-0">
							<path 
								stroke-linecap="round" 
								stroke-linejoin="round" 
								d="M17.982 18.725A7.488 7.488 0 0012 15.75a7.488 7.488 0 00-5.982 2.975m11.963 0a9 9 0 10-11.963 0m11.963 0A8.966 8.966 0 0112 21a8.966 8.966 0 01-5.982-2.275M15 9.75a3 3 0 11-6 0 3 3 0 016 0z"
							/>
						</svg>
						<div class="text-sm font-medium">Username</div>
						<svg width="13" height="8" viewBox="0 0 13 8" fill="none" xmlns="http://www.w3.org/2000/svg">
							<path d="M1.5 1.5L6.5 6.5L11.5 1.5" stroke="#344054" stroke-width="1.66667" stroke-linecap="round" stroke-linejoin="round"/>
						</svg>
					</div>--><!--Caso o usuário esteja logado-->
                </div>
                <img src="/static/images/inscricao/frases/galeriaCampeoes.png" class="sm:w-1/2 hidden lg:block"/>
			</nav>
            <navbar-reduzida-inscricao></navbar-reduzida-inscricao>
		`;
	}
}
customElements.define('banner-galeria-campeoes', BannerGaleriaCampeoes);

class NavbarEditions extends HTMLElement {
	connectedCallback() {
		this.innerHTML = `
			<nav class="navbar flex flex-col gap-10 justify-center items-center pb-0">
				<div class="flex flex-row justify-center items-center gap-6">
					<a href="/"><img src="/static/images/logos/pioceraBranca.png" class="w-32 shrink-0"/></a>
					<a href="/"><img src="/static/images/logos/cerapioBranca.png" class="w-32 shrink-0"/></a>
				</div>
				
				<ul class="pb-5 md:pb-0 flex-wrap nav-links w-full justify-center items-center flex font-bold flex-row gap-4 text-center">
					<li class="md:border-b-2 md:border-white md:pb-5"><a href="/">Home</a></li>
					<li class="md:pb-5"><a href="/">O evento</a></li>
					<li class="md:pb-5"><a href="/">Notícias</a></li>
					<li class="md:pb-5"><a href="/">Agência de viagens</a></li>
					<li class="md:pb-5"><a href="/">Contato</a></li>
				</ul>
			</nav>
		`;
	}
}
customElements.define('navbar-editions', NavbarEditions);

class BannerGaleriaFotos extends HTMLElement {
	connectedCallback() {
		this.innerHTML = `
            <nav class="hidden text-white lg:flex bg-cover bg-center w-full bg-no-repeat flex-col justify-center items-center gap-20 lg:p-10 xl:px-20 bg-[#C38934]" style="background-image: url(/static/images/inscricao/bannerDecoracaoInscricao.png);">
                <div class="w-full flex flex-row items-center justify-start">
                    <a href="/"><img src="/static/images/logos/cerapioBranca.png" class="w-20 sm:w-32 hidden lg:block"/></a>
                    <ul class="nav-links w-full justify-start items-center flex lg:pl-9">
                        <input type="checkbox" id="checkbox_toggle" class="input-navbar"/>
                        <div class="menu-inscricao font-bold gap-4">
                            <li><a href="/"><img src="/static/images/logos/cerapioBranca.png" class="w-20 sm:w-32 block lg:hidden"/></a></li>
                            <li><a href="/">Home</a></li>
                            <li><a href="/">O evento</a></li>
                            <li><a href="/">Notícias</a></li>
                            <li><a href="/">Agência de viagens</a></li>
                            <li><a href="/">Contato</a></li>
                            <li><a href="/">Área do competidor</a></li>
                        </div>
                    </ul>
					<!--<div class="cursor-pointer text-[#545454] bg-white rounded-lg px-3 py-2 flex items-center justify-center flex-row gap-2">
						<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6 shrik-0">
							<path 
								stroke-linecap="round" 
								stroke-linejoin="round" 
								d="M17.982 18.725A7.488 7.488 0 0012 15.75a7.488 7.488 0 00-5.982 2.975m11.963 0a9 9 0 10-11.963 0m11.963 0A8.966 8.966 0 0112 21a8.966 8.966 0 01-5.982-2.275M15 9.75a3 3 0 11-6 0 3 3 0 016 0z"
							/>
						</svg>
						<div class="text-sm font-medium">Username</div>
						<svg width="13" height="8" viewBox="0 0 13 8" fill="none" xmlns="http://www.w3.org/2000/svg">
							<path d="M1.5 1.5L6.5 6.5L11.5 1.5" stroke="#344054" stroke-width="1.66667" stroke-linecap="round" stroke-linejoin="round"/>
						</svg>
					</div>--><!--Caso o usuário esteja logado-->
                </div>
                <img src="/static/images/inscricao/frases/galeriaFotos.png" class="sm:w-1/2 hidden lg:block"/>
			</nav>
            <navbar-reduzida-inscricao></navbar-reduzida-inscricao>
		`;
	}
}
customElements.define('banner-galeria-fotos', BannerGaleriaFotos);
