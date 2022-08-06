extern const putc = function(ch: char) -> int

pub const print = function(str: string){
    for ch in string{
        putc(ch)
    }
}

pub const println = function(str: string){
    print(str)
    print('\n')
}
