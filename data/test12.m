
A = [ 1, 2, 3;
       4, 5, 6;
       7, 8, 9 ] ;

A[1,3] = 0;

b = zeros(5);

B= eye(3);

C = A *B;
print C;

print A;
