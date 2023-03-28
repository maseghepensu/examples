// esempi rust da rust x c++ programmers

// riceve il parametro per valore, quindi avviene la move di una variabile v passata nella call
// al parametro _ ; quindi nel punto dopo la call , v non e' piu' usabile (vedi (3))
fn foo(_: Box<i32>) {
    
}

fn main() {
    println!("Hello, world!");
    let x: Box<i32> = Box::new(7);
    println!("x={}, x punta a *x={}", x, *x);
    let y = Box::new(8);
    // y = x;   no, y non mut
    // *y = 43;  no, *y non e' mut
    println!("{}",*y);
    let mut ym = Box::new(9);
    *ym = *ym + 1;
    println!("*ym={}", *ym);
    
    /*
    x=7, x punta a *x=7
    8
    *ym=10
    */
    let mut zm = ym;  // questo provoca la "move" ad ym a zm, e quindi (2)
                      // e' con questo meccanismo che si realizza che i puntatori "Box" sono
                      // "unici": in un dato scope, solo un puntatore punta alla Box
    *zm = 0;
    // println!("{}", *ym);  errore: ym non possiede piu' alcun valore (2)
    println!("*zm={}", *zm);  //*zm=0
    //(3)
    foo(zm);
    // println!("zm={}",zm);  no, come detto nell commento a foo, zm non e' piu' usabile
    // rustc suggerisce di fare foo(zm.clone()):
    foo(y.clone());
    println!("dopo foo(y.clone()), y={}", y);  // dopo foo(y.clone()), y=8
}