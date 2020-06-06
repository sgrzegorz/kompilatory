# control flow instruction

N = 10;
M = 20;


for i = 1:N {
    if(i<=5)
        continue;
    else if(i<=8)
        print "break";
    else if(i<=9)
        print "continue";
    else if(i<=12)
        return 0;
}


{
  N = 100;
  M = 200;
}

print N;

