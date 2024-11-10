use std::fs::File;
use std::io::{self, BufRead};
use std::path::Path;

// const FILENAME: &str = "../test01.txt";
const FILENAME: &str = "../input.txt";
const KEYPAD: [[char; 5]; 5] = [
    ['0', '0', '1', '0', '0'],
    ['0', '2', '3', '4', '0'],
    ['5', '6', '7', '8', '9'],
    ['0', 'A', 'B', 'C', '0'],
    ['0', '0', 'D', '0', '0'],
];

fn main() {
    let path = Path::new(FILENAME);
    let file = File::open(&path).unwrap();
    let lines = io::BufReader::new(file).lines();

    let mut code = String::new();
    let mut x: usize = 0;
    let mut y: usize = 2;

    for line in lines {
        let line = line.unwrap();
        for c in line.chars() {
            if c == 'U' {
                if y > 0 && KEYPAD[y - 1][x] != '0' {
                    y -= 1;
                }
            } else if c == 'D' {
                if y < 4 && KEYPAD[y + 1][x] != '0' {
                    y += 1;
                }
            } else if c == 'L' {
                if x > 0 && KEYPAD[y][x - 1] != '0' {
                    x -= 1;
                }
            } else if c == 'R' {
                if x < 4 && KEYPAD[y][x + 1] != '0' {
                    x += 1;
                }
            }
        }
        code.push(KEYPAD[y][x]);
    }

    println!("The code is: {}", code);
}
