package main

import  (
    "fmt"
    "time"
    "math/rand"
)

func main() {
    s1 := rand.NewSource(time.Now().UnixNano())
    r1 := rand.New(s1)

    m := make(map[string]bool)
    letter := "qwertyuiopasdfghjklz"
    for i := 0; i < 5000001; i++ {
        if i % 1000000 == 0 {
            dt := time.Now()
            fmt.Println(dt.Format("2006-01-02 15:04:05.999"))
        }

        s := "";
        for j := 0; j < 50; j++ {
            s += string(letter[r1.Intn(20)])
        }
        m[s] = true
    }

}
