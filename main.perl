use Time::HiRes qw(time);
use POSIX qw(strftime);

my $letter = "qwertyuiopasdfghjklz";
my %dic = ();
for(0..5000001){
    if($_ % 1000000 == 0){
        # https://stackoverflow.com/questions/18100208/how-to-get-milliseconds-as-a-part-of-time-in-perl
        my $t = time;
        my $date = strftime "%Y-%m-%d %H:%M:%S", localtime $t;
        $date .= sprintf ".%03d", ($t-int($t))*1000; # without rounding
        print $date, "\n";
    }
    my $s = "";
    for(0..50){
        $s .= substr $letter,  int(rand(20)), 1;
    }
    $dic{$s} = True;
}
