from lightup.State import State, StatePreProcessor
from lightup.Action import Action
from searching.BFS import BFS
from searching.DFS import DFS
import os

instances_folder = './instances/25-25/easy/'

instances = os.listdir(instances_folder)

for instance in instances:
    state = State(instances_folder+instance)
    pre_processor = StatePreProcessor(state).process_state()
    bfs = DFS(pre_processor,
            show_execution_time=True, notify_iterations=1000).solve()