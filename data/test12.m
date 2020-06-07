a=4;
T = [ 1, a];
print T;

A = [ 1, 2, 3;
       4, 5, 6;
       7, 8, 9 ] ;

A[1,3] = 0;
print "A: ", A;
print A+A;

b = zeros(5);

B= eye(3);

C = A *B;
print C;

print A;
