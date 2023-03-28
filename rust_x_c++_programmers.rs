// riceve il parametro per valore, quindi avviene la move di una variabile v passata nella call
// al parametro _ ; quindi nel punto dopo la call , v non e' piu' usabile (vedi (3))
fn foo(_: Box<i32>) {
    
}
fn foobyr(_: &Box<i32>) {
    
}
fn foomod(x: &mut Box<i32> ) {
    // **x = 19;  // ok
    **x = **x * 10;  // x : &mut Box<i32>, *x = mut Box<i32>, **x = i32;
}

struct S {
  f: i32,
}
impl S {
    fn new(v :i32) -> S {
        Self{f:v}
    }
    fn add(&mut self, i: i32) {
        self.f += i;
    }
    fn toS(&self) -> String {
       //self.to_string() no: S dovrebbe soddisfare gia' std::fmt::Display
       format!("S({})", self.f) 
    }
}

fn f_i32ref_i32(_:&i32, _:i32) {
    
}
fn refs() {
    let x = &3;
    let y = *x;
    println!("x={}, y={}",x,y); // gli interi lavorano x copia
    f_i32ref_i32(x,y);
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
    println!("x={}",x);   // 7
    foobyr(&x);
    println!("x={}",x);   // ok sempre accessibile
    
    let mut xm = Box::new(16);   // xm deve essere mut, altrimenti non puoi passarla come &mut Box<i32>
    foomod(&mut xm);
    println!("xm={}",xm);   // ok sempre accessibile: xm=160
    
    let mut s0 = S::new(4);  // nota: s0 deve essere mutabile
    println!("s0.f={}", s0.f);  // s0.f=4
    s0.add(17);
    println!("s0.f={}", s0.f);  // s0.f=21
    let mut bbb = Box::new(Box::new(Box::new(S::new(8))));
    println!("bbb.f={}", bbb.f); // bbb.f=8  non serve derenziare 3 volte il puntatore
    bbb.add(200);
    println!("bbb.f={}", bbb.f); // anche per le call di metodi funziona: bbb.f=208
    println!("bbb.toS={}", bbb.toS()); // bbb.toS=S(208)
    // borrowed pointers == borrowed referemnce == references
    refs();
    
}