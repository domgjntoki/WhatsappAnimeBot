# Whatsapp MyAnimeList BOT
A MyAnimeList Bot that reacts to Whatsapp's chat commands, using selenium with javascript to send messages, without yowsup, at the moment with commands only in portuguese (Will add english later)

## Available commands

### Portuguese
- **[ !help ]** - Mostra todos os comandos disponíveis no bot

- **[ !anime** _título_ **]** - Busca por um anime no MyAnimeList 
    - _!anime Shingeki no Kyojin_
   
- **[ !manga** _título_ **]** - Busca por um manga no MyAnimeList 
  - _!manga Shingeki no Kyojin_
  
- **[ !personagem** _título_ **]** - Busca por um personagem no MyAnimeList 
   - _!personagem Rem_
   
- **[ !monogatari ]** Mostra ordem das temporadas de monogatari 

- **[ !user ]** - Mostra comandos relacionados ao perfil do usuário
    - **[ !user** _usuário_ **]** - Mostra o perfil do MAL do usuário
        - _!user AltrianZ_
    - **[ !user perfil** _usuário_ **]** - Mostra o perfil do MAL do usuário
        -  _!user perfil AltrianZ_
    - **[ !user historico** _usuário_ **]** - Mostra histórico de update do usuário
        - _!user historico Yamashine_

- **[ !favorite ]** - Mostra os comandos que mostram os favoritos de um usuário no MAL
    - **[ !favorite anime** _usuário_ **]** - Mostra os animes favoritos do usuário
        - _!favorite anime DomGintoki_
    - **[ !favorite manga** _usuário_ **]** - Mostra os mangas favoritos do usuário
    - **[ !favorite personagem** _usuário_ **]** - Mostra os personagens favoritos do usuário
    - **[ !list ]** - Mostra comandos relacionados às listas de usuários do MAL

- **[ !semanal ]** - Mostra comandos relacionados a lançamentos de animes na semana
    - **[ !semanal [ontem, hoje, amanhã...] ]** - Mostra todos os animes que lançam ontem, hoje ou amanhã
    	- **tipos=** [antes de ontem, anteontem, hoje, amanhã, depois de amanhã]
        - _!semanal hoje, !semanal ontem_

    - **[ !semanal** dia **]** - Mostra todos animes lançados nesse dia
        -  _!semanal segunda_
    - **[ !semanal** anime **]** - Mostra em que dia da semana e a data de lançamento do anime
    - _**OBS: Além da palavra-chave semanal, também é possível usar !lançamento ou !semana**_

- **[ !top ]** - Mostra os comandos que mostram os tops do MyAnimeList, inclusive os top animes da temporada
    - **Geral:** **[ !top** tipo **]**
	    -  **tipos =** _anime, manga, pessoa, personagem_
	    -  _!top anime, !top manga..._
	
    - **Tops anime especificado:**
        - **[ !top anime** tipo **]**
        - **tipos =** _temporada, tv, filme, ova, pop, favorite_
        -  _!top anime temporada, !top anime pop..._

    - **Top manga especificado:**
        - **[ !top manga** tipo **]**
        - **tipos =** _manga, novel, oneshot, manhwa, manhua, pop, favorite_
        -  _!top manga manga, !top manga novel, !top manga manhwa..._
- **[ !list ]** - Mostra todos os comandos relacionados às listas de usuários no MyAnimeList
	- **Anime:**
		- **[ !list anime tipo** usuário **]**
		- **tipos =** _watching, completed, onhold, dropped, ptw_
		- **EX:** _!list anime dropped DomGintoki, !list anime ptw DomGintoki_
		- **_OBS: se não informar o tipo, a lista "watching" é mostrada por padrão_** 
			- _(!list anime DomGintoki)_
	- **Manga:**
		- **[ !list manga tipo** usuário **]**
		- **tipos =** _reading, completed, onhold, dropped, ptr_
		- **EX:** _!list manga completed DomGintoki, !list manga ptr DomGintoki_
		- **_OBS: se não informar o tipo, a lista "reading" é mostrada por padrão_** 
			- _(!list manga DomGintoki)_

- **[ !help ]** - Mostra todos os comandos disponíveis no bot

- **[ !anime** _título_ **]** - Busca por um anime no MyAnimeList 
    - _!anime Shingeki no Kyojin_
   
- **[ !manga** _título_ **]** - Busca por um manga no MyAnimeList 
  - _!manga Shingeki no Kyojin_
  
- **[ !personagem** _título_ **]** - Busca por um personagem no MyAnimeList 
   - _!personagem Rem_
   
- **[ !monogatari ]** Mostra ordem das temporadas de monogatari 

- **[ !user ]** - Mostra comandos relacionados ao perfil do usuário

- **[ !favorite ]** - Mostra os comandos que mostram os favoritos de um usuário no MAL

- **[ !semanal, !semana, !lançamento ]** - Mostra comandos relacionados a lançamentos de animes na semana 
	- (Fazem a mesma coisa, apenas palavras-chaves diferentes)

- **[ !top ]** - Mostra os comandos que mostram os tops do MyAnimeList, inclusive os top animes da temporada

- **[ !list ]** - Mostra todos os comandos relacionados às listas de usuários no MyAnimeList



## App Demonstration
<img src="app_demo_images/searching_releases.jpg" width="250">  <img src="app_demo_images/releases_of_day.jpg" width="250">

<img src="app_demo_images/searching_releases_for_anime.jpg" width="250">  <img src="app_demo_images/command_fail_example.jpg" width="250">

<img src="app_demo_images/user_mal.PNG" width="500">
