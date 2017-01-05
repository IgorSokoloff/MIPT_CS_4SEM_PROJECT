#Eng
## MIPT_CS_4SEM_PROJECT

Here is the source code of the project in Informatics of 4 semester in MIPT.

The project contains a 2D physics engine and a program used mathematical apparatus of the engine renders the scene.
Programming language: python + pygame.
Pygame used for rendering the scene and key events.


##Opportunities of the engine:
Generate an unlimited set of scenes with an unlimited number of objects there.
Smooth solid balls were used as physical objects.
Implemented an algorithm for determining and processing of elastic collision between the balls.

##Opportunities of the program:
Generate an unlimited number of balls on the same stage. Features check menu.

#Control:
_The methods are performed for whole scene:_
+ ***Space*** - pause
+ ***B*** - On / Off border
+ ***Crt*** - on / off display velocity vectors
+ ***Shift*** - on / off display of acceleration vectors
+ ***RMB*** - add a new ball (its parameters are generated randomly (default acceleration is zero))

_The methods are performed for the concrete sphere of when you hover the cursor on it_
+ ***Delete*** - remove the ball from the scene
+ ***LMB*** - information output to the console of it
+ ***LMB + MouseMotion*** - moving the ball
+ ***R + MOusewheel*** - radius change 
+ ***A + MOusewheel*** - acceleration change
+ ***V + MOusewheel*** - speed change
+ ***F + LMB + MouseMotion*** - the application of force to a concrete ball
+ ***M + MOusewheel*** - mass change


#Rus
## MIPT_CS_4SEM_PROJECT

В данном репозитории находится исходный код проекта по информатике за 4 семестр МФТИ.

Проект состоит из 2D физического движка и программы, которая задействует математический аппарат движка и отрисовывает сцену.
Язык программирования: python + pygame.
Pygame использовался в качеcтве средства рендеринга сцены и обработки нажатия клавиш.


##Возможности движка:
Генерировать неограниченное множество сцен с неограниченным количеством объектов на ней.
В качестве физических объектов участвуют твердые гладкими  шарики.
Реализован алгоритм определения и обработки упругих столкновений между шариками.

##Возможности программы:
Генерировать неограниченное количество шариков на одной сцене. Возможности программы отображатся меню управления.

#Управление:
_Методы выполняются для всей сцены:_
+ ***space*** - пауза
+ ***b*** - вкл/выкл границы
+ ***crt*** - вкл/выкл отображения векторов скорости
+ ***shift*** - вкл/выкл отображения векторов ускорения
+ ***RMB*** - добавить новую сферу (ее параметры генерируются случайно(по умолчанию ускорение нулевое))

_Методы выполняются для конкретной сферы при наведении на нее курсора:_
+ ***delete*** - удаление сферы со сцены
+ ***LMB*** - вывод в консоль информации о ней
+ ***LMB + MouseMotion*** - перемещение сферы
+ ***r + MOusewheel*** - изменение радиуса
+ ***a + MOusewheel*** - изменение ускорения
+ ***v + MOusewheel*** - изменение скорости
+ ***f + LMB + MouseMotion***- приложение силы к конкретной сфере
+ ***m + MOusewheel*** - изменение массы
