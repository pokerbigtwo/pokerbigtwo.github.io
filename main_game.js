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
    document.write(card+"<br>");
    var i;
    for (i=0;i<13;i++){
        card1[i]=card[i];
        card2[i]=card[i+13];
        card3[i]=card[i+26];
        card4[i]=card[i+39];
    }
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