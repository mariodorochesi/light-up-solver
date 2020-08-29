from lightup.State import State, StatePreProcessor
from lightup.Action import Action
from searching.BFS import BFS
from searching.DFS import DFS
import os

instances_folder = './instances/7-7/hard/'

instances = os.listdir(instances_folder)

for instance in instances:
    print('Oringinal')
    state = State(instances_folder+instance)
    print(state)
    pre_processor = StatePreProcessor(state).process_state()
    print('Pre-Procesado')
    print(pre_processor)
    bfs = DFS(pre_processor,show_execution_time=True, notify_iterations=1000).solve()
    print('Solucion')
    print(bfs)