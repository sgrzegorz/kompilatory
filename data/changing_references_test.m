a = 5;
b = a;
c = b;
a = 3;
print c, " EEEEEEENDDDDDDDDDDDD";


a = 5;
b = a + 2;
print b;
c = b * 3;
print c;
d = c + b + a;
print d;

a = [1,2,3];
b = a;
c = b;
b = 5;
d = [1,2,3] + c;
print d;

e = 4;
a = zeros(5);
b = a;
d = ones(5) * e;
c = b + d;
b = ones(5);
print a, " ", b, " ", c, " ", d;