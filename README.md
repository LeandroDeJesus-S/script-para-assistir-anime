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
  🚫  No momento o site animeseonline está fora do ar...  🚧
</h4>

### Features

- [x] Acessar pagina home do anime.
- [x] Acessar episódio e/ou temporada especifico.
- [x] Acessar episódio mais recente do anime.
- [x] Adicionar um anime.
- [x] Listar lançamentos de animes e episódios.
- [x] Mostrar sugestão caso anime passado esteja incorreto ou não seja encontrado.
- [x] Atualizar animes automaticamente
- [x] Salvar histórico de episódios e animes assistidos.
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

# para atualizar os animes e episódios manualmente
$ python3 manage.py --update

# Para ver os comandos utilize
$ python3 ani.py --help
```

### 🛠 Tecnologias

As seguintes ferramentas foram usadas na construção do projeto:

- [Python](https://www.python.org/)

### Autor
---

<a href="">
 <img style="border-radius: 50%;" src="https://instagram.fsbj1-1.fna.fbcdn.net/v/t51.2885-19/309266936_508450560617948_4798171976938283294_n.jpg?stp=dst-jpg_s150x150&_nc_ht=instagram.fsbj1-1.fna.fbcdn.net&_nc_cat=108&_nc_ohc=pdBAKWz-Az0AX8hRBLx&edm=AOQ1c0wBAAAA&ccb=7-5&oh=00_AfDhM6RWL6qWdZqCAOms5hHYvgxfEoi1pIkLh0DLt8qngA&oe=63AC8DE6&_nc_sid=8fd12b" width="100px;" alt=""/>
 <br />
 <sub><b>Leandro de Jesus Santos</b></sub></a> <a href="https://www.instagram.com/_leandro_zz/">🚀</a>


Feito por Leandro de Jesus Santos 
# Contato:

Email: [leandrojs@proton.me](mailto:leandrojs@proton.me) • 
instagram: [@_leandro_zz](https://www.instagram.com/_leandro_zz/)
