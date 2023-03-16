Dictionary<string, bool> dic = new Dictionary<string, bool>();
Random r = new Random();
string letter = "qwertyuiopasdfghjklz";
for (int i = 0; i < 5000001; i++)
{
    if (i % 1000000 == 0)
    {
        Console.WriteLine(DateTime.Now.ToString("yyyy-MM-dd HH:mm:ss.fff"));
    }
    string s = "";
    for (int j = 0; j < 50; j++)
    {
        s += letter[r.Next(20)];
    }
    dic[s] = true;
}
