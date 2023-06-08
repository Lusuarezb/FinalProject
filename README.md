# **Hand Tetris**

Proyecto final para la asignatura Creación multimedia.

## **Integrantes.**

* David Pérez Zapata.
* Luis Antonio Suárez Bula.

---

## **Idea.**

Nuestro punto de partida consistía en que queríamos hacer un juego, y que estuviera controlado por medio de la cámara, ya fuera con gestos, objetos o algo relacionado. Con estas ideas en mente llegamos a lo que es nuestro proyecto: *Hand Tetris*, el clásico juego de bloques cayendo, pero esta vez controlado principalmente por la posición de la mano de jugador, así como por algunos gestos.

---

## **Inspiraciones.**

**Tetris Effect:** este juego que se encuentra en la biblioteca de Steam nos sirvió de base para visualizar lo que queríamos lograr, a una menor escala. Este juego entrega una versión moderna de Tetris, con efectos visuales y de sonido y personalización, los cuales fueron los factores que quisimos replicar en nuestra versión.

---

## **Funcionamiento.**

https://github.com/Lusuarezb/FinalProject/assets/83037028/0782efdc-7c7b-4639-bd3c-4f5206371fa3

Al abrir el juego se verá el menu principal, que cuenta con dos botones: "Start Game" y "Theme Selected" 

Al hacer click en "Theme Selected" se cambiará entre los dos temas principales que se tienen para personalizar la experiencia de juego (esto incluye la fuente, las imágenes y los sonidos), los cuales son *Normal* y *Metal*, siendo este último una versión más rockera y extrema. 

Hacer clic en el botón "Start Game" se iniciará el juego, el cual, en jugabilidad se comporta exactamente igual a un tetris normal. La principal diferencia son los controles, los cuales ahora estan asignados a la mano del jugador. El objetivo es entonces alcanzar la máxima puntuación eliminando la mayor cantidad de filas posible. 

---

## **Instrucciones.**

Para iniciar el juego hay que ejecutar el archivo *main.exe* que se encuentra en la carpeta main. Se abrirán dos ventanas, la del juego y la de la cámara. La de la cámara es una simple guía para observar cómo es que funcionará el control del juego usando una mano.

Al iniciar el juego comenzarán a caer las piezas como en cualquier versión normal de Tetris, el cambio ocurre cuando el jugador muestra la una mano con la palma extendida frente a la cámara, pues así podrá controlar el movimiento horizontal de las piezas de acuerdo a la posición horizontal de su mano. Luego, teniendo de igual forma la mano extendida pero doblando el pulgar hacia adentro de la palma, se podrá rotar la pieza. Finalmente, al cerrar la mano en un puño (siempre mirando hacia la cámara), se desencadenará el efecto de caída rápida de la pieza o *drop*.

![How to Play](https://github.com/Lusuarezb/FinalProject/assets/83037028/25111fba-0eaf-46bf-9a85-ee8f9330d90d)

El juego continuará indefinidamente hasta que el jugador decida detenerse o hasta que pierda.
