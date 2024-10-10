// loops : conditon : true
let a=0 // initialization 
//declaration : value

// for(a=1;a<10;a++){
//     console.log(a); 
// }

// while(a<10){
//     console.log(a);
//     a++
// }

// do{
// console.log(a);
// a++
// }
// while(a<10)
// let inc = 4
// console.log(inc++);  // inc = inc+1
// //4+1 = 5
// console.log(++inc); //6

// break/continue : prime/composite
let prime = []
let composite = []

for(let i = 0 ; i<50;i++){
let n = i;
if(n === 0 || n === 1){
    console.log("neither prime nor composite");
    
}
else if(i%1=== 0 && i%i === 0){
        // prime.push(i)
        console.log(i);
        

}
else{
    // composite.push(i)
    console.log("comp",i);
    
}
}

// console.log(composite,prime);
