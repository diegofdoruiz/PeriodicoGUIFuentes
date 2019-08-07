%Cargar datos:
int: n;
array[1..n] of int: PotentialReaders;
array[1..n] of int: MinTopicPages;
array[1..n] of int: MaxTopicPages;
int : NewspaperTotalPages;
% Variables:
array[1..n] of var bool: x;
array[1..n] of var int : pages_x;
% Restricciones:
constraint forall(i in 1..n)(pages_x[i]>= 0);
constraint forall(i in 1..n)(x[i] == false \/ pages_x[i]>=MinTopicPages[i] /\ pages_x[i] <= MaxTopicPages[i]);
constraint sum(i in 1..n)(x[i]*pages_x[i])<= NewspaperTotalPages;
% Función objetivo
solve maximize sum(i in 1..n)(PotentialReaders[i]*x[i]*pages_x[i]);