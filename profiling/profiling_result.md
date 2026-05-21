Algorithm            | Events  | Time (s)   | ms/Evt   | Peak (KB) 
----------------------------------------------------------------------
QuickSort (N=200)    | 20399   | 0.5969     | 0.029    | 24873.54  
MergeSort (N=200)    | 2475    | 0.0654     | 0.026    | 3070.13   
ShellSort (N=200)    | 3451    | 0.0903     | 0.026    | 4190.53   
Dijkstra             | 17      | 0.0006     | 0.033    | 16.77     
Bellman-Ford         | 18      | 0.0005     | 0.025    | 18.07     
A*                   | 18      | 0.0004     | 0.022    | 17.64     

============================================================
(TOP 20 CUMULATIVE TIME)
============================================================
         3484701 function calls (1219701 primitive calls) in 1.198 seconds

   Ordered by: cumulative time

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
   135000    0.024    0.000    1.198    0.000 C:\Users\User\Python-project\src\algorithms\sorting\quick.py:12(run)
2399900/134900    0.366    0.000    1.173    0.000 C:\Users\User\Python-project\src\algorithms\sorting\quick.py:22(_quick_sort)
   139700    0.114    0.000    0.807    0.000 C:\Users\User\Python-project\src\algorithms\sorting\quick.py:30(_partition)
   134900    0.108    0.000    0.694    0.000 C:\Users\User\Python-project\src\algorithms\base.py:21(_emit)
   134900    0.098    0.000    0.585    0.000 C:\Users\user\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.11_qbz5n2kfra8p0\LocalCache\local-packages\Python311\site-packages\pydantic\main.py:153(__init__)
   134900    0.345    0.000    0.488    0.000 {method 'validate_python' of 'pydantic_core._pydantic_core.SchemaValidator' objects}
   134900    0.051    0.000    0.143    0.000 C:\Users\user\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.11_qbz5n2kfra8p0\LocalCache\local-packages\Python311\site-packages\pydantic\_internal\_std_types_schema.py:91(to_enum)
   134900    0.074    0.000    0.093    0.000 C:\Program Files\WindowsApps\PythonSoftwareFoundation.Python.3.11_3.11.2544.0_x64__qbz5n2kfra8p0\Lib\enum.py:688(__call__)
   134900    0.019    0.000    0.019    0.000 C:\Program Files\WindowsApps\PythonSoftwareFoundation.Python.3.11_3.11.2544.0_x64__qbz5n2kfra8p0\Lib\enum.py:1095(__new__)
      100    0.000    0.000    0.000    0.000 C:\Users\User\Python-project\src\algorithms\sorting\quick.py:9(__init__)
      100    0.000    0.000    0.000    0.000 C:\Users\User\Python-project\src\algorithms\base.py:10(__init__)
      100    0.000    0.000    0.000    0.000 C:\Users\User\Python-project\src\algorithms\base.py:44(_validate_input)
      300    0.000    0.000    0.000    0.000 {built-in method builtins.len}
      100    0.000    0.000    0.000    0.000 {built-in method builtins.isinstance}
        1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}



============================================================
AlgorithmEvent ~80 bytes
============================================================
