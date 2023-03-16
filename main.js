var dict = {}
const letter = 'qwertyuiopasdfghjklz'
for (let i = 0; i < 5000001; i++) {
    if (i%1000000==0) {
        let tzoffset = (new Date()).getTimezoneOffset() * 60000
        console.log(new Date(Date.now() - tzoffset).toISOString().replace('T',' ').replace('Z',''))
    }
    var s = ""
    for (let j = 0; j < 50; j++) {
        s += letter[Math.floor(Math.random() * 20)]
    }
    dict[s] = true
}
