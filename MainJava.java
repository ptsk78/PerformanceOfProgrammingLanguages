import java.sql.Timestamp;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.Random;
import java.util.Hashtable;

public class MainJava {
    public static void main(String[] args) {
        Random rand = new Random();
        String letter =  "qwertyuiopasdfghjklz";
        Hashtable<String, Boolean> dic = new Hashtable<String, Boolean>();
        for(int i=0;i<5000001;i++)
        {
            if(i%1000000==0)
            {
                Timestamp timestamp = new Timestamp(System.currentTimeMillis());
                System.out.println(timestamp);
            }

            String s = "";
            for(int j=0;j<50;j++)
            {
                s += letter.charAt(rand.nextInt(20));
            }
            dic.put(s, true);
        }
    }
}