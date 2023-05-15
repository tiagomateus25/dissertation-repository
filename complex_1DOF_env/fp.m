function fp=fp(p,z,p1,z1)

b2=(p+p1).^2+(z-z1).^2;
k2=(4*p.*p1)./b2;
[K,E] = ellipke(k2);
fp=sqrt(b2).*((1-(k2/2)).*K-E);

end