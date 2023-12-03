# Computação Gráfica - PROJETO 1

### Autores

👤 Beatriz Cardoso de Oliveira - 12566400

👤 Heitor Tanoue de Mello - 12547260

## Descrição

Este é um projeto para disciplina SCC0650 - Computação Gráfica que permite carregar e exibir objetos a partir de arquivos no formato wavefront (*.obj) junto com suas respectivas texturas. O projeto é estruturado em três arquivos Python, localizados na pasta "src" e um arquivo `main.py` que executa o código:

- `model.py`: Contém a classe `Model` que lida com o arquivo .obj, a inserção da textura, atributos do modelo e funções para aplicar a matriz de transformação.

- `functions.py`: Contém funções auxiliares utilizadas no código, incluindo cálculos de proporções, criação do caminho do arquivo a partir do nome do obj e carregamento do modelo a partir do caminho do arquivo .obj.

- `engine.py`: Contém a lógica principal do programa, incluindo a estrutura para a troca de modelos, tratamento de eventos de teclado, movimentação, translação e escala do objeto.

## Funcionalidades do Projeto

O projeto atende às seguintes restrições e funcionalidades:

1. Possibilita a leitura e processamento de 5 objetos a partir de arquivos .obj, cada um com sua textura.

2. Permite a exibição individual de cada objeto por meio de eventos de teclado. Pressione a tecla "1" para exibir o objeto 1, a tecla "2" para o objeto 2 e assim por diante.

3. Cada objeto é centralizado no ponto (0, 0, 0) na primeira exibição e se movimenta de acordo com as teclas "A", "W", "S" e "D", usando transformações de translação para realizar essa movimentação. O código também garante que nenhum vértice do objeto fique fora do intervalo [-1, 1] em seus eixos, quando aplicadas as transformações de movimentação e escala.

4. É possível utilizar as teclas "Z" e "X" para aumentar e reduzir a escala do objeto em exibição.

5.  As teclas direcionais são utilizadas para rotacionar o objeto em exibição nos eixos X e Y. É possível realizar rotações no eixo Z com as teclas "M" e "N".

6. A tecla "P" ativa ou desativa a textura do objeto em exibição, alternando entre a visualização da malha poligonal e a aplicação da textura.

7. A tecla "V" permite alternar entre técnicas de magnificação da aplicação da textura, escolhendo entre LINEAR e NEAREST.

8. A tecla "B" permite ativar/desativar a visualização do Bounding Box para o objeto selecionado.

9. A tecla "F" permite alterar entre o modo janela e o modo tela cheia.

10. A tecla "ESC" permite encerrar a execução do programa.

## Dependências

Antes de executar o projeto, é necessário instalar todas as bibliotecas e módulos Python necessários. Você pode fazer isso utilizando o arquivo requirements.txt fornecido.

Para instalar as dependências, no terminal, navegue até o diretório onde se encontra o arquivo requirements.txt e execute o seguinte comando:

```bash
pip install -r requirements.txt
```

## Execução

Para executar o projeto, você pode rodar o arquivo `main.py` a partir do diretório "src".

Certifique-se de que todos os requisitos para a execução do projeto estão satisfeitos e que os objetos .obj e suas texturas estejam localizados no diretório adequado.

**Nota**: Certifique-se de que todos os módulos e bibliotecas necessários estejam instalados para a execução adequada do projeto.
