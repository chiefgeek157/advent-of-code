// Open the file text01.txt

use std::fs::File;
use std::io::{self, BufRead};
use std::path::Path;

// Set a global variable with the name of the file

// const FILENAME: &str = "../test01.txt";
const FILENAME: &str = "../input.txt";
const KEYPAD: [[char; 3]; 3] = [['1', '2', '3'], ['4', '5', '6'], ['7', '8', '9']];

fn main() {
    let path = Path::new(FILENAME);
    let file = File::open(&path).unwrap();
    let lines = io::BufReader::new(file).lines();

    let mut code = String::new();
    let mut x = 1;
    let mut y = 1;

    for line in lines {
        let line = line.unwrap();
        for c in line.chars() {
            match c {
                'U' => y = y - 1,
                'D' => y = y + 1,
                'L' => x = x - 1,
                'R' => x = x + 1,
                _ => panic!("Invalid character"),
            }

            if x < 0 {
                x = 0;
            } else if x > 2 {
                x = 2;
            }

            if y < 0 {
                y = 0;
            } else if y > 2 {
                y = 2;
            }
        }
        code.push(KEYPAD[y as usize][x as usize]);
    }

    println!("The code is: {}", code);
}
