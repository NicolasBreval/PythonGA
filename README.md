# PythonGA

## ES
### Descripción del proyecto
Este proyecto presenta la implementación sencilla y altamente configurable de un algoritmo genético, utilizando la librería Numpy para representar los cromosomas y operar con ellos.

### Organización del código
El código se organiza en un único módulo, llamado GA, el cual contiene los siguientes submódulos:

* **ga**: Contiene la clase que representa el algoritmo, permite definir el problema y ejecutar el algoritmo para obtener resultados.
* **exceptions**: Contiene las posibles excepciones que puede devolver cualquier clase o método dentro del módulo GA.
* **default_funcs**: Contiene las funciones por defecto para selección, cruce y mutación de individuos.
* **historical**: Contiene lo necesario para poder almacenar todos los cambios obtenidos en una ejecución del algoritmo.

### Cómo utilizar la librería
La librería ofrece una clase, llamada GeneticAlgorithm, la cual permite definir nuestro problema y parametrizar algunos aspectos del algoritmo. A continuación, la lista de parámetros disponibles y su significado:

* **Parámetros obligatorios**
    * **chromosome_limits**: Es un array de Numpy. Cada elemento de este array es otro array con dos posiciones, la primera posición es el mínimo valor posible para el gen, mientras que la segunda posición es el máximo valor posible para el gen. Por ejemplo, para un cromosoma de 3 posiciones en el que cada gen únicamente puede tomar valores entre 0 y 2, su *chromosome_limits* sería: [[0, 2], [0, 2], [0, 2]].
    * **chromosome_type**: Es el tipo de array de numpy para el cromosoma. Los valores de Numpy típicos son numpy.int32, numpy.float42, numpy.bool, etcétera. Esto sirve para que, cuando se generen valores aleatorios o se creen nuevos individuos, se mantenga el tipo de datos original.
    * **fitness_func**: Es la función que determina lo buena que es una solución alcanzada por el algotimo. Debe ser una función cuyo único argumento de entrada sea un array de Numpy y cuyo único argumento de salida sea un número. Se determina cuanto menor el valor de fitness, mejor es la solución, por lo que el usuario debe tener esto en cuenta a la hora de diseñar la función de fitness.

* **Parámetros opcionales**
    * **selection_func**: Si no se pone el parámetro, se utiliza la función de selección por defecto. En caso de que se utilice, el parámetro de entrada debe ser una función cuyo argumento es un diccionario con todas las variables internas de la clase del algoritmo y debe devolver una lista de arrays de Numpy con la selección de individuos.
    * **cross_func**: Si no se pone el parámetro, se utiliza la función de cruce por defecto. En caso de que se utilice, el parámetro de entrada debe ser una función cuyo argumento es un diccionario con todas las variables internas de la clase del algoritmo y debe devolver una lista de arrays de Numpy con los nuevos individuos obtenidos a partir del cruce de la población actual.
    * **mutation_func**: Si no se pone el parámetro, se utiliza la función de mutación por defecto. En caso de que se utilice, el parámetro de entrada debe ser una función cuyo argumento es un diccionario con todas las variables internas de la clase del algoritmo y debe devolver la lista de hijos mutados.
    * **stop_fitness**: Si se pone un valor numérico, el algoritmo parará automáticamente cuando su fitness sea igual o menor a dicho valor, independientemente del número de iteraciones que se hayan configurado. Si no se indica ningún valor, al algoritmo parará cuando se hayan cumplido todas las iteraciones
    * **default_cross_prop**: Indica el porcentaje del primer padre que se utiliza para el cruce de individuos. Si no se indica, es 0.5. Debe ser un valor entre 0 y 1, ambos incluidos.
    * **default_mutation_prob**: Indica la probabilidad que hay de que un gen mute en un nuevo individuo. Si no se indica, es 0.5. Debe ser un valor entre 0 y 1. Ambos incluidos.
    * **popsize**: Número de individuos en la población por cada iteración. Si no se indica, por defecto son 10. Debe ser un número par.
    * **max_iters**: Máximo número de iteraciones que debe ejecutar el algoritmo. Si no se indica, por defecto son 10. Debe ser un número mayor o igual a cero, aunque si se pone cero, no se ejecutará ninguna iteración.
    * **verbose**: Por defecto es False, si se pone a True, se imprimirá por pantalla cierta información sobre cada iteración del algoritmo.

### Funciones por defecto
Esta librería está diseñada para que, manteniendo el flujo de datos de la ejecución del algoritmo, el usuario pueda personalizar las piezas esenciales y obtener así un resultado completamente diferente y único. Aun así, para poder comprobar fácilmente el funcionamiento, o para obtener resultados con una ejecución más sencilla, la librería ofrece una funciones por defecto que permiten que el algoritmo sea 100% funcional desde el principio:

#### Algoritmo de selección
Este algoritmo selecciona la mitad de la población únicamente por su fitness, por tanto únicamente se mantienen en la población aquellas soluciones más cercanas al fitness ideal.

El pseudocódigo sería el siguiente:

```
1.- Se ordenan los individuos según su fitness en una lista.
2.- Se obtiene la mitad de la lista ordenada.
3.- Se devuelve la lista como la selección de individuos.
```


#### Algoritmo de cruce
El algoritmo de cruce permite que los individuos de una población produzcan nuevos individuos con propiedades mixtas de sus padres. 

El peudocódigo sería el siguiente:

```
1.- Se desordenan los individuos de la selección (Esto ofrece resultados más variados y suele evitar una convergencia forzada hacia un fitness concreto).
2.- Por cada par de padres:
    2.1- Se obtienen dos hijos, realizando el cruce (Si los padres son [A | B] y [C | D], siendo cada letra una parte del padre tras hacer la división, los hijos serían [A | D] y [C | B])
    2.2 - Se almacenan los hijos en la lista.
3.- Se devuelven los hijos para añadirlos a la población.
```

El algoritmo de cruce se puede parametrizar con el argumento *default_cross_prop*, el cual indica qué porcentaje se corta de los individuos a la hora de realizar el cruce. Por ejemplo, si es 0.5, se parte por la mitad cada individuo. Si fuera 0.3, se dividiría de la siguiente forma:

padre 1: [A: 30% | B: 70%]     |  hijo 1: [A: 30% | D: 70%]
padre 2: [C: 30% | D: 70%]     |  hijo 2: [C: 30% | B: 70%]

#### Algoritmo de mutación
La mutación ofrece pequeños cambios dentro de los individuos para obtener variaciones que el cruce sería incapaz de obtener. El algoritmo se parametriza con el argumento *default_mutation_prob*, que representa la probabilidad de que un gen mute dentro de un cromosoma hijo.

El pseudocódigo sería el siguiente:

```
1.- Por cada hijo en la lista:
    1.1- Por cada gen dentro del cromosoma hijo:
        1.1.1- Se calcula si ese gen debe mutar utilizando la probabilidad mutliplicada por el porcentaje de iteraciones que lleva el algoritmo.
        1.1.2- Si el gen debe mutar, se obtiene un valor aleatorio entre los límites y se modifica el gen por ese valor
2.- Se devuelve la lista de hijos modificados
```

Se ha decidido hacer el algoritmo de mutación progresivo, es decir, la probabilidad de que mute un gen varía desde 0 hasta el límite impuesto según avanzan las iteraciones del algoritmo genético, porque la selección y el cruce permiten convergen rápidamente al algoritmo en valores de fitness muy cercanos al esperado y, las mutaciones obtenidas al avanzar en el algoritmo ayudan a acercarse aún más, mientras que realizar mutaciones desde el principio puede demorar la convergencia.

---


## EN
TODO

