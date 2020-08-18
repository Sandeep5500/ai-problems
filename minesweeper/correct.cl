class Main inherits IO {
  x: Bool  
  main(): Object {{
    x <- true; 
    out_string.("Hello World\n");
    if x = true then out_string("True") fi  
  }};
};--Prints Hello World--