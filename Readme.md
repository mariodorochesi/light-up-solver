# Light - Up Solver

Para ejecutar este solver es necesario clonar el repositorio, se sugiere aun cuando no es obligación utilizar un entorno virtual de python.

```bash
    git clone https://github.com/mariodorochesi/light-up-solver.git
    cd light-up-solver
    pip3 install requirements.txt
    python3 main.py
```

# Configuracion
## Instancias
Dentro del repositorio se incluye una carpeta ***instances*** en la cual se almacenan diferentes instancias del problema. En el archivo main.py se define en que sub-carpeta se va a ir a buscar las instancias para posteriormente resolverlas. Por defecto tenemos colocado **7-7/easy/** no obstante se puede cambiar en la siguiente linea de codigo.

```python
    instances_folder = './instances/7-7/easy/'
```

## Metodo de Busqueda
Este trabajo incorpora 5 diferentes métodos de búsqueda, los cuales se pueden utilizar tan solo cambiando una linea de código en el programa principal.
```python
    bfs = BestFirstSearch(pre_processor,show_execution_time=True, notify_iterations=1000).solve()
```

Los métodos implementados y su respectiva clase son los siguientes:
  
  - Depth First Search : **DFS**

  - Breadth First Search : **BFS**

  - Best First Search : **BestFirstSearch**

  - Greedy : **Greedy**

  - Grasp : **Grasp**