
#k = 3;
#if(k<5)
 #   i = 1;
#else
 #   m = 3;

#print m;

###########

#a = [1,2;
#    3,4];


#b = zeros(2,2);
#c = a-b;
#c = a-b+a;
#c = [1,2;
 #   3,4] +  zeros(2,2);
c = [1,2;4,5] +  ones(2) * eye(2) + ones(2,2) * [3,4];
print c;
#############