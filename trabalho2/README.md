# Computação Gráfica - PROJETO 2

### Autores

👤 Beatriz Cardoso de Oliveira - 12566400

👤 Heitor Tanoue de Mello - 12547260

## Descrição

Este é um projeto para disciplina SCC0650 - Computação Gráfica que permite carregar e exibir objetos a partir de arquivos no formato wavefront (*.obj) junto com suas respectivas texturas. O projeto é estruturado em três arquivos Python, localizados na pasta "src" e um arquivo `main.py` que executa o código:

- `model.py`: Contém a classe `Model` que lida com o arquivo .obj, a inserção da textura, atributos do modelo e funções para aplicar a matriz de transformação.

- `functions.py`: Contém funções auxiliares utilizadas no código, incluindo cálculos de proporções, criação do caminho do arquivo a partir do nome do obj e carregamento do modelo a partir do caminho do arquivo .obj.

- `engine.py`: Contém a lógica principal do programa, incluindo a estrutura para a troca de modelos, tratamento de eventos de teclado, movimentação, translação e escala do objeto.

- `camera.py`: Contém a classe `Camera` que lida com a câmera virtual, incluindo a matriz de projeção e a matriz de visualização.

## Funcionalidades do Projeto

O projeto atende às seguintes restrições e funcionalidades:

1. Possibilita a leitura e processamento de 5 objetos a partir de arquivos .obj, cada um com sua textura.

2. É possível andar com a câmera virtual utilizando as teclas "W", "A", "S" e "D" e olhando para a direção desejada com o mouse.

3. A tecla "P" ativa ou desativa a textura do objeto em exibição, alternando entre a visualização da malha poligonal e a aplicação da textura.

4. A tecla "V" permite alternar entre técnicas de magnificação da aplicação da textura, escolhendo entre LINEAR e NEAREST.

5. A tecla "B" permite ativar/desativar a visualização do Bounding Box para o objeto selecionado.

6.  A tecla "ESC" permite encerrar a execução do programa.

7.  As teclas "J" e "K" permitem diminuir ou aumentar a intensidade da luz ambiente.

8.  As setas direcionais e as teclas "M" e "N" permitem alterar a posição da fonte de luz.

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
