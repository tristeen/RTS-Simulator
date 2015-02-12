#no unit.dying_, ps using order_choice
{('ThinkerWeightedChoice', 'ThinkerUCT'): [1, 1, 1, 1, 1, 1, 1, 1, 1, 1], ('ThinkerEG', 'ThinkerMCTS'): [1, 1, -1, 1, 1, -1, -1, -1, 1, -1], ('ThinkerNaiveMCTS', 'ThinkerMCTS'): [-1, 1, -1, -1, 1, -1, 1, -1, 1, 1], ('ThinkerWeightedChoice', 'ThinkerNaiveMCTS'): [1, 1, 1, 1, 1, 1, 1, -1, 1, 1], ('ThinkerWeightedChoice', 'ThinkerEG'): [1, -1, 1, 1, 1, -1, 1, 1, 1, 1], ('ThinkerWeightedChoice', 'ThinkerMCTS'): [1, 1, 1, 1, 1, 1, 1, 1, 1, 1], ('ThinkerEG', 'ThinkerNaiveMCTS'): [-1, 1, -1, 1, -1, 1, -1, 1, -1, 1], ('ThinkerUCT', 'ThinkerNaiveMCTS'): [1, 1, 1, 1, 1, -1, 1, 1, 1, 1], ('ThinkerEG', 'ThinkerUCT'): [1, 1, -1, 1, 1, 1, 1, -1, 1, -1], ('ThinkerUCT', 'ThinkerMCTS'): [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1]}


#add unit.dying_, ps using random.choice
{('ThinkerWeightedChoice', 'ThinkerUCT'): [1, 1, 1, 1, 1, 1, 1, 1, 1, 1], ('ThinkerEG', 'ThinkerMCTS'): [-1, -1, -1, -1, -1, -1, -1, 1, -1, -1], ('ThinkerNaiveMCTS', 'ThinkerMCTS'): [-1, 1, -1, -1, -1, -1, -1, -1, -1, -1], ('ThinkerWeightedChoice', 'ThinkerNaiveMCTS'): [1, 1, 1, 1, 1, 1, 1, 1, 1, 1], ('ThinkerWeightedChoice', 'ThinkerEG'): [1, 0, 1, 1, 1, 1, 1, 1, 1, 1], ('ThinkerWeightedChoice', 'ThinkerMCTS'): [1, 1, 1, -1, 1, 1, -1, 1, 1, 1], ('ThinkerEG', 'ThinkerNaiveMCTS'): [-1, 1, -1, 1, 1, -1, 1, -1, -1, -1], ('ThinkerUCT', 'ThinkerNaiveMCTS'): [1, -1, -1, -1, 1, 1, 1, -1, -1, -1], ('ThinkerEG', 'ThinkerUCT'): [1, 1, -1, 1, 1, -1, 1, 1, -1, -1], ('ThinkerUCT', 'ThinkerMCTS'): [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1]}
{('ThinkerMCTS', 'ThinkerWeightedChoice'): [1, -1, 1, -1, 1, 1, 1, 1, 1, 1]}


#ps using order_weight_choice
{('ThinkerMCTS', 'ThinkerWeightedChoice'): [1, 1, 1, 1, -1, -1, 1, 1, 1, 1]}



{('ThinkerMCTS_RC', 'ThinkerWeightedChoice'): [1, 0, -1, 0, 1, 1, 1, 1, 1, -1]}

{('ThinkerMCTS', 'ThinkerRandom'): [1], ('ThinkerNaiveMCTS', 'ThinkerRandom'): [1], ('ThinkerMCTS', 'ThinkerNaiveMCTS'): [1], ('ThinkerMCTS', 'ThinkerMCTS_RC'): [1], ('ThinkerNaiveMCTS', 'ThinkerUCT'): [1], ('ThinkerMCTS_RC', 'ThinkerUCT'): [1], ('ThinkerEG', 'ThinkerRandom'): [-1], ('ThinkerMCTS_RC', 'ThinkerEG'): [1], ('ThinkerUCT', 'ThinkerRandom'): [1], ('ThinkerMCTS', 'ThinkerEG'): [1], ('ThinkerNaiveMCTS', 'ThinkerEG'): [1], ('ThinkerMCTS_RC', 'ThinkerRandom'): [1], ('ThinkerEG', 'ThinkerUCT'): [1], ('ThinkerMCTS_RC', 'ThinkerNaiveMCTS'): [1], ('ThinkerMCTS', 'ThinkerUCT'): [1]}

{('ThinkerMCTS', 'ThinkerRandom'): [1, 1], ('ThinkerNaiveMCTS', 'ThinkerRandom'): [1, -1], ('Thinker
MCTS', 'ThinkerNaiveMCTS'): [1, 1], ('ThinkerMCTS', 'ThinkerMCTS_RC'): [1, -1], ('ThinkerNaiveMCTS',
 'ThinkerUCT'): [1, -1], ('ThinkerMCTS_RC', 'ThinkerUCT'): [1, 1], ('ThinkerEG', 'ThinkerRandom'): [
-1, 1], ('ThinkerMCTS_RC', 'ThinkerEG'): [1, 1], ('ThinkerUCT', 'ThinkerRandom'): [-1, -1], ('Thinke
rMCTS', 'ThinkerEG'): [1, 1], ('ThinkerNaiveMCTS', 'ThinkerEG'): [-1, -1], ('ThinkerMCTS_RC', 'Think
erRandom'): [1, 1], ('ThinkerEG', 'ThinkerUCT'): [1, -1], ('ThinkerMCTS_RC', 'ThinkerNaiveMCTS'): [1
, 1], ('ThinkerMCTS', 'ThinkerUCT'): [1, 1]}

{('ThinkerMCTS', 'ThinkerRandom'): [1, 1, 1, 1, 1, 1, 1, 1, 1, -1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], ('
ThinkerMCTS', 'ThinkerNaiveMCTS'): [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], ('T
hinkerMCTS', 'ThinkerMCTS_RC'): [-1, 1, 1, 1, 1, 1, -1, -1, -1, 1, -1, 1, -1, -1, 1, 1, 1, 1, 1, 1],
 ('ThinkerMCTS', 'ThinkerEG'): [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], ('Think
erMCTS_RC', 'ThinkerNaiveMCTS'): [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], ('ThinkerMCTS', 'ThinkerUCT'): [
1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]}



#after modify update camp
{('ThinkerUCT', 'ThinkerWeightedChoice'): [-1], ('ThinkerNaiveMCTS', 'ThinkerWeightedChoice'): [-1], ('ThinkerMCTS', 'ThinkerNaiveMCTS'): [1], ('ThinkerMCTS', 'ThinkerMCTS_RC'): [-1], ('ThinkerNaiveMCTS', 'ThinkerUCT'): [-1], ('ThinkerMCTS', 'ThinkerWeightedChoice'): [1], ('ThinkerMCTS_RC', 'ThinkerUCT'): [1], ('ThinkerMCTS_RC', 'ThinkerEG'): [1], ('ThinkerEG', 'ThinkerWeightedChoice'): [-1], ('ThinkerMCTS', 'ThinkerEG'): [1], ('ThinkerNaiveMCTS', 'ThinkerEG'): [1], ('ThinkerMCTS_RC', 'ThinkerWeightedChoice'): [1], ('ThinkerEG', 'ThinkerUCT'): [-1], ('ThinkerMCTS_RC', 'ThinkerNaiveMCTS'): [1], ('ThinkerMCTS', 'ThinkerUCT'): [1]}


{('ThinkerMCTS', 'ThinkerNaiveMCTS'): [1, 1, 1, 1, 1, 1, 1, 1, 1, 1], ('ThinkerMCTS', 'ThinkerMCTS_R
C'): [1, 1, 1, -1, 1, -1, -1, -1, -1, 1], ('ThinkerMCTS', 'ThinkerWeightedChoice'): [1, 1, 1, -1, 1,
 1, 1, -1, 1, 1], ('ThinkerMCTS_RC', 'ThinkerUCT'): [1, 1, 1, 1, 1, 1, 1, 1, 1, 1], ('ThinkerMCTS_RC
', 'ThinkerEG'): [1, 1, 1, 1, 1, 1, 1, 1, 1, 1], ('ThinkerMCTS', 'ThinkerEG'): [1, 1, 1, 1, 1, 1, 1,
 1, 1, 1], ('ThinkerNaiveMCTS', 'ThinkerEG'): [1, 1, 1, -1, 1, -1], ('ThinkerMCTS_RC', 'ThinkerWeigh
tedChoice'): [-1, 1, 1, 1, 1, 1, -1, 1, -1, 1], ('ThinkerMCTS_RC', 'ThinkerNaiveMCTS'): [1, 1, 1, 1,
 1, 1, 1, 1, 1, 1], ('ThinkerMCTS', 'ThinkerUCT'): [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]}
 
 {('ThinkerUCT', 'ThinkerWeightedChoice'): [-1, -1, -1, 1, 1, -1, 1, -1, -1, -1], ('ThinkerNaiveMCTS'
, 'ThinkerWeightedChoice'): [1, -1, -1, -1, -1, -1, 1, -1, -1, -1], ('ThinkerMCTS', 'ThinkerNaiveMCT
S'): [1, 1, 1, 1, 1, 1, 1, 1, 1, 1], ('ThinkerMCTS', 'ThinkerMCTS_RC'): [1, 1, 1, -1, 1, -1, -1, 1,
1, 1], ('ThinkerNaiveMCTS', 'ThinkerUCT'): [1, 1, -1, 1, 1, -1, -1, 1, 1, 1], ('ThinkerMCTS', 'Think
erWeightedChoice'): [1, 1, 1, 1, 1, 1, 1, 1, 1, -1], ('ThinkerMCTS_RC', 'ThinkerUCT'): [1, 1, 1, 1,
1, 1, 1, 1, 1, 1], ('ThinkerMCTS_RC', 'ThinkerEG'): [1, 1, 1, 1, 1, 1, 1, 1, 1, 1], ('ThinkerEG', 'T
hinkerWeightedChoice'): [-1, 1, -1, -1, -1, -1, -1, -1, -1, -1], ('ThinkerMCTS', 'ThinkerEG'): [1, 1
, 1, 1, 1, 1, 1, 1, 1, 1], ('ThinkerNaiveMCTS', 'ThinkerEG'): [1, 1, -1, -1, 1, -1, 1, 1, 1, -1], ('
ThinkerMCTS_RC', 'ThinkerWeightedChoice'): [1, 1, -1, 1, 1, 1, 1, 1, -1, 1], ('ThinkerEG', 'ThinkerU
CT'): [1, -1, 1, 1, 1, 1, 1, -1, -1, 1], ('ThinkerMCTS_RC', 'ThinkerNaiveMCTS'): [1, 1, 1, 1, 1, 1,
1, 1, 1, 1], ('ThinkerMCTS', 'ThinkerUCT'): [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]}

#map2
{('ThinkerMCTS', 'ThinkerNaiveMCTS'): [1, 1], ('ThinkerMCTS', 'ThinkerMCTS_RC'): [-1, -1], ('Thinker
MCTS', 'ThinkerWeightedChoice'): [-1, -1], ('ThinkerMCTS_RC', 'ThinkerUCT'): [1, 1], ('ThinkerMCTS_R
C', 'ThinkerEG'): [1, 1], ('ThinkerMCTS', 'ThinkerEG'): [-1, 1], ('ThinkerNaiveMCTS', 'ThinkerEG'):
[-1], ('ThinkerMCTS_RC', 'ThinkerWeightedChoice'): [1, 1], ('ThinkerMCTS_RC', 'ThinkerNaiveMCTS'): [
1, 1], ('ThinkerMCTS', 'ThinkerUCT'): [1, 1]}
 
 
{('ThinkerMCTS', 'ThinkerWeightedChoice'): [-1, 1, 1, 1, 1, 1, -1, -1, -1, -1], ('ThinkerNewMCTS', 'ThinkerWeightedChoice'): [1, 1, -1, 1, 1, 1, 1, -1, 1, -1], ('ThinkerMCTS', 'ThinkerNewMCTS'): [-1, -1, -1, 1, -1, 1, -1, 1, 1, 1]}

{('ThinkerMCTS', 'ThinkerWeightedChoice'): [1, -1, 1, 1, -1, -1, 1, 1, 1, -1], ('ThinkerNewMCTS', 'ThinkerWeightedChoice'): [1, 1, 1, 1, -1, -1, 1, -1, 1, 1], ('ThinkerMCTS', 'ThinkerNewMCTS'): [1, -1, 1, -1, -1, 1, -1, -1, 1, 1]}

{('ThinkerMCTS', 'ThinkerWeightedChoice'): [1, -1, 1, 1, 1, 1, 1, 1, 1, 1], ('ThinkerNewMCTS', 'ThinkerWeightedChoice'): [1, 1, 1, 1, -1, 1, 1, 1, -1, 1], ('ThinkerMCTS', 'ThinkerNewMCTS'): [1, 1, 1, -1, 1, -1, -1, 1, -1, -1]}

{('ThinkerNewMCTS', 'ThinkerNaiveMCTS'): [1, 1, 1, 1, 1, 1, 1, 1, 1, 1], ('ThinkerNewMCTS', 'Thinker
UCT'): [1, 1, 1, 1, 1, 1, 1, 1, 1, 1], ('ThinkerNewMCTS', 'ThinkerMCTS_RC'): [1, 1, -1, 1, 1, 1, 1,
1, -1, 1], ('ThinkerNewMCTS', 'ThinkerEG'): [1, 1, 1, 1, 1, 1, 1, 1, 1, 1], ('ThinkerMCTS_RC', 'Thin
kerNaiveMCTS'): [1, 1, 1, 1, 1], ('ThinkerNewMCTS', 'ThinkerWeightedChoice'): [1, 1, 1, 1, -1, 1, 1,
 1, 1, 1]}
 
 {('ThinkerNewMCTS', 'ThinkerMCTS'): [1, 1, 1, 1, -1, -1, 1, 1, 1, -1], ('ThinkerNewMCTS', 'ThinkerMC
TS_RC'): [1, 1, -1, -1, -1, 1]}

{('ThinkerMCTS', 'ThinkerMCTS_RC'): [1, 1, -1, 1, 1, 1, 1, 1, 1, 1], ('ThinkerMCTS', 'ThinkerNaiveMC
TS'): [1]}

{('ThinkerNaiveMCTS', 'ThinkerWeightedChoice'): [-1, -1, 1, -1, -1, -1, -1, -1, -1, -1], ('ThinkerNe
wMCTS', 'ThinkerNaiveMCTS'): [1, 1, 1, 1, 1, 1, 1, 1, 1, 1], ('ThinkerNaiveMCTS', 'ThinkerUCT'): [-1
, 1, -1, 1, 1, 1, 1, 1, 1, 1], ('ThinkerNaiveMCTS', 'ThinkerEG'): [1, -1, 1, -1, 1, -1, 1, 1, 1, 1],
 ('ThinkerMCTS_RC', 'ThinkerWeightedChoice'): [1, 1, 1, 1, 1, 1, -1, 1, -1, 1], ('ThinkerNewMCTS', '
ThinkerUCT'): [1, 1, 1, 1, 1, 1, 1, 1, 1, 1], ('ThinkerNewMCTS', 'ThinkerMCTS_RC'): [1, 1, 1, 1, -1,
 1, -1, -1, 1, 1], ('ThinkerMCTS_RC', 'ThinkerEG'): [1, 1, 1, 1, 1, 1, 1, 1, 1, 1], ('ThinkerEG', 'T
hinkerWeightedChoice'): [-1, -1, 0, -1, 1, -1, -1, -1, -1, -1], ('ThinkerMCTS_RC', 'ThinkerUCT'): [1
, 1, 1, 1, 1, 1, 1, 1, 1, 1], ('ThinkerUCT', 'ThinkerWeightedChoice'): [-1, -1, -1, -1, -1, 1, -1, -
1, -1, 0], ('ThinkerNewMCTS', 'ThinkerEG'): [1, 1, 1, 1, 1, 1, 1, 1, 1, 1], ('ThinkerEG', 'ThinkerUC
T'): [1, 1, -1, -1, -1, 1, -1, 1, 1, 1], ('ThinkerMCTS_RC', 'ThinkerNaiveMCTS'): [1, 1, 1, 1, 1, 1,
1, 1, 1, 1], ('ThinkerNewMCTS', 'ThinkerWeightedChoice'): [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]}


#map4
{('ThinkerMCTS', 'ThinkerWeightedChoice'): [1, 1, 1, 1, 1, 1, 1, 1, 1, -1], ('ThinkerNewMCTS', 'Thin
kerWeightedChoice'): [-1, 1, 1, 1, 1, 1, 1, 1, 1, 1], ('ThinkerMCTS', 'ThinkerNewMCTS'): [1, 1, 1, 1
, 1, 1, 1, 1, 1, 1]}

#map3 512 shuffle
{('ThinkerNewMCTS', 'ThinkerNaiveMCTS'): [1, 1, 1, 1, 1, 1, 1, 1, 1, 1], ('ThinkerNewMCTS', 'Thinker
UCT'): [1, 1, 1, 1, 1, 1, 1, 1, 1, 1], ('ThinkerNewMCTS', 'ThinkerMCTS_RC'): [-1, 1, -1, -1, 1, 0, 1
, 1, -1, 1], ('ThinkerNewMCTS', 'ThinkerEG'): [1, 1, 1, 1, 1, 1, 1, 1, 1, 1], ('ThinkerNewMCTS', 'Th
inkerMCTS'): [-1, 1, -1, 1, -1, -1, 1, 1, 1, 1], ('ThinkerNewMCTS', 'ThinkerWeightedChoice'): [1, 1,
 1, 1, 1, 1, 1, 1, -1, 1], ('ThinkerMCTS', 'ThinkerNewMCTS'): [-1, 1, 1, -1, 0, 1]}


 {('ThinkerNaiveMCTS', 'ThinkerNewMCTS'): [1, -1, -1, -1, 1, -1, -1, -1, -1, 1], ('ThinkerNaiveMCTS',
 'ThinkerEG'): [1, 1, 1, 0, 1, 1, 1, 0], ('ThinkerNewMCTS', 'ThinkerNaiveMCTS'): [1, 1, 1, 1, 1, 1,
1, 1, 1, 1], ('ThinkerNewMCTS', 'ThinkerUCT'): [1, 1, 1, 1, 1, 1, 1, 1, 1, 1], ('ThinkerNewMCTS', 'T
hinkerEG'): [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]}

{('ThinkerNaiveMCTS', 'ThinkerNewMCTS'): [-1, -1], ('ThinkerNaiveMCTS', 'ThinkerUCT'): [1, -1], ('ThinkerWeightedChoice', 'ThinkerNewMCTS'): [1, 1], ('ThinkerWeightedChoice', 'ThinkerNaiveMCTS'): [0, 1], ('ThinkerNewMCTS', 'ThinkerEG'): [1, 1], ('ThinkerNewMCTS', 'ThinkerUCT'): [1, 1], ('ThinkerUCT', 'ThinkerNewMCTS'): [-1, 0], ('ThinkerWeightedChoice', 'ThinkerEG'): [1, 1], ('ThinkerMCTS_RC', 'ThinkerUCT'): [1, 1], ('ThinkerMCTS_RC', 'ThinkerNewMCTS'): [1, 1], ('ThinkerMCTS', 'ThinkerMCTS_RC'): [1, -1], ('ThinkerMCTS', 'ThinkerNewMCTS'): [1, 1], ('ThinkerNewMCTS', 'ThinkerNaiveMCTS'): [1, 1], ('ThinkerMCTS', 'ThinkerEG'): [1, 1], ('ThinkerMCTS_RC', 'ThinkerNaiveMCTS'): [1, 1], ('ThinkerWeightedChoice', 'ThinkerMCTS'): [1, 1], ('ThinkerMCTS', 'ThinkerUCT'): [1, 1], ('ThinkerNaiveMCTS', 'ThinkerMCTS_RC'): [-1, 1], ('ThinkerMCTS_RC', 'ThinkerWeightedChoice'): [1, 1], ('ThinkerNaiveMCTS', 'ThinkerEG'): [1, 1], ('ThinkerNewMCTS', 'ThinkerWeightedChoice'): [1, 1], ('ThinkerEG', 'ThinkerNewMCTS'): [-1, -1], ('ThinkerEG', 'ThinkerMCTS_RC'): [-1, 1], ('ThinkerMCTS_RC', 'ThinkerMCTS'): [1, -1], ('ThinkerUCT', 'ThinkerMCTS_RC'): [-1, -1], ('ThinkerUCT', 'ThinkerEG'): [1, -1], ('ThinkerEG', 'ThinkerWeightedChoice'): [1, 1], ('ThinkerWeightedChoice', 'ThinkerUCT'): [1, 1], ('ThinkerNaiveMCTS', 'ThinkerMCTS'): [1, -1], ('ThinkerMCTS_RC', 'ThinkerEG'): [1, 1], ('ThinkerNaiveMCTS', 'ThinkerWeightedChoice'): [1, 1], ('ThinkerMCTS', 'ThinkerNaiveMCTS'): [1, 1], ('ThinkerEG', 'ThinkerMCTS'): [-1, -1], ('ThinkerNewMCTS', 'ThinkerMCTS'): [1, 1], ('ThinkerMCTS', 'ThinkerWeightedChoice'): [1, 1], ('ThinkerNewMCTS', 'ThinkerMCTS_RC'): [1, 1], ('ThinkerUCT', 'ThinkerNaiveMCTS'): [1, -1], ('ThinkerWeightedChoice', 'ThinkerMCTS_RC'): [-1, -1], ('ThinkerEG', 'ThinkerNaiveMCTS'): [1, 1], ('ThinkerEG', 'ThinkerUCT'): [1, 1], ('ThinkerUCT', 'ThinkerWeightedChoice'): [1, -1], ('ThinkerUCT', 'ThinkerMCTS'): [-1, -1]}

#256 20
{('ThinkerMCTS_RC', 'ThinkerMCTS'): [1, 0], ('ThinkerNewMCTS', 'ThinkerMCTS'): [1, 1], ('ThinkerWeightedChoice', 'ThinkerMCTS_RC'): [1, 0], ('ThinkerMCTS', 'ThinkerWeightedChoice'): [1, 1], ('ThinkerNewMCTS', 'ThinkerMCTS_RC'): [1, 1], ('ThinkerWeightedChoice', 'ThinkerMCTS'): [1, -1], ('ThinkerMCTS_RC', 'ThinkerWeightedChoice'): [1, 1], ('ThinkerWeightedChoice', 'ThinkerNewMCTS'): [-1, -1], ('ThinkerMCTS_RC', 'ThinkerNewMCTS'): [0, -1], ('ThinkerMCTS', 'ThinkerMCTS_RC'): [1, 1], ('ThinkerNewMCTS', 'ThinkerWeightedChoice'): [1, 1], ('ThinkerMCTS', 'ThinkerNewMCTS'): [1, 1]}

