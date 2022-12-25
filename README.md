# script-para-assistir-anime
## script python de argumentos de sistema para assistir animes no site animesonline

<p align="center">
 <a href="#Features">Features</a> •
 <a href="#Pré-requisitos">Pré requisitos</a> • 
 <a href="#inicio rapido">Como usar</a> • 
 <a href="#Pré-requisitos">Pré requisitos</a> • 
 <a href="#Comandos">Comandos</a> • 
 <a href="https://animesonline.cc/tv/">site ultilizado</a>
</p>

<h4 align="center"> 
  🚀 Em construção...  🚧
</h4>

### Features

- [x] Acessar pagina home do anime.
- [x] Acessar episódio e/ou temporada especifico.
- [x] Acessar episódio mais recente do anime.
- [x] Adicionar um anime.
- [x] Listar lançamentos de animes e episódios.
- [x] Mostrar sugestão caso anime passado esteja incorreto ou não seja encontrado.
- [x] Atualizar animes automaticamente
- [ ] Salvar histórico de episódios e animes assistidos.
- [ ] Mostrar resumo de animes lançados

### Pré-requisitos

Ter o [Python](https://www.python.org/downloads/) e o [Git](https://git-scm.com) instalados.

### Inicio rapido

```bash
# Clone este repositório
$ git clone https://github.com/LeandroDeJesus-S/animes-online.git

# Acesse a pasta do projeto no terminal/cmd
$ cd script-para-assistir-anime

# Instale as dependências
$ pip3 install request
$ pip3 install beautifulsoup4
$ pip3 install colorama

# Execute a aplicação com o argumento --help para ver os comandos
$ python3 ani.py --help
```
### Comandos
```bash
# acessar home page de um anime
$ python3 ani.py -w "nome do anime"

# Para acessar um ep ou temporada especificos, por exemplo, episódio 3 da temporada 2:
$ python3 ani.py -w "nome do anime" -e 3 -s 2

# Para adicionar um novo anime
$ python3 ani.py -add "nome do anime" "url da home page do anime"

# acessar episódio mais recente do anime
$ python3 ani.py -new "nome do anime"

# listar animes recentes
$ python3 ani.py -la

# listar episódios recentes
$ python3 ani.py -le

# acessar a home page do site
$ python3 ani.py -sh

# Para ver os comandos utilize
$ python3 ani.py --help
```

### 🛠 Tecnologias

As seguintes ferramentas foram usadas na construção do projeto:

- [Python](https://www.python.org/)

### Autor
---

<a href="">
 <img style="border-radius: 50%;" src="https://instagram.fsbj1-1.fna.fbcdn.net/v/t51.2885-19/309266936_508450560617948_4798171976938283294_n.jpg?stp=dst-jpg_s150x150&_nc_ht=instagram.fsbj1-1.fna.fbcdn.net&_nc_cat=108&_nc_ohc=6lYSylM18kAAX-JqbCu&edm=AOQ1c0wBAAAA&ccb=7-5&oh=00_AfD79rRggK9QWSo4ByIzzFVtUTFFLLQOp7Gaakx8GzTYTw&oe=6396CD26&_nc_sid=8fd12b" width="100px;" alt=""/>
 <br />
 <sub><b>Leandro de Jesus Santos</b></sub></a> <a href="https://www.instagram.com/_leandro_zz/">🚀</a>


Feito por Leandro de Jesus Santos 
# Contato:

Email: [leandrojs@proton.me](mailto:leandrojs@proton.me) • 
instagram: [@_leandro_zz](https://www.instagram.com/_leandro_zz/)
