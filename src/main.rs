use chrono::prelude::*;
use rand::Rng;
use std::collections::HashMap;

fn main() {
    let letter = "qwertyuiopasdfghjklz";
    let mut rng = rand::thread_rng();
    let mut hm = HashMap::new();

    for i in 0..5000001 {
        if i % 1000000 == 0 {
            let now = Local::now();
            let res = now.format("%Y-%m-%d %H:%M:%S.%f");
            println!("{}", res);
        }
        let mut s = String::new();
        for _ in 0..50 {
            let ch = letter.chars().nth(rng.gen_range(0..20)).unwrap();
            s.push(ch);
        }
        hm.insert(s, true);
    }
}