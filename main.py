from lightup.State import State, StatePreProcessor
from lightup.Action import Action
from searching.BFS import BFS
from searching.DFS import DFS
from searching.BestFirstSearch import BestFirstSearch
import os

instances_folder = './instances/14-14/easy/'

instances = os.listdir(instances_folder)
archivo = open('./results/'+instances_folder.replace('.','').replace('/','')+'.txt','w')
tiempo_total = 0
resuelto = 0
for instance in instances:
    print('Oringinal')
    state = State(instances_folder+instance)
    print(state)
    pre_processor = StatePreProcessor(state).process_state()
    #print('Pre-Procesado')
    #print(pre_processor)
    bfs = BestFirstSearch(pre_processor,show_execution_time=True, notify_iterations=1000).solve()
    if bfs is not None:
        archivo.write('Instancia : {} Tiempo : {} segundos\n'.format(instance,bfs.taken_time))
        print('Solucion')
        print(bfs)
        tiempo_total += bfs.taken_time
        resuelto+=1
    else:
        archivo.write('Instancia : {} Tiempo : NO RESUELTO segundos\n'.format(instance))
archivo.write('Total Resueltos {}/{}\n'.format(resuelto, len(instances)))
archivo.write('Tiempo Promedio {} segundos'.format(tiempo_total/resuelto))
archivo.close()