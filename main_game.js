const card=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52];
round=1;
const card1=[];
const card2=[];
const card3=[];
const card4=[];

function setround(r){
    round=r;
}

function start(){
    if(round==0)
        return 0;
    round--;
    card.sort(function(){return 0.5 - Math.random()});
    card1=card.slice(0,13);
    card2=card.slice(13,26);
    card3=card.slice(26,39);
    card4=card.slice(39,52);
    print(card1);
    return 1;
}

function getcard(id){
    if(id==1)
    return card1;
    if(id==2)
    return card2;
    if(id==3)
    return card3;
    if(id==4)
    return card4;
}