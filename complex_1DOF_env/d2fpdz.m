function d2fpdz=d2fpdz(p,z,p1,z1,t1)

bt2=(p.^2)+(p1.^2)+2*p.*p1.*cos(t1)+(z-z1).^2;
d2fpdz=-p.*p1.*cos(t1).*(bt2.^(-3/2)).*(3*((z-z1).^2).*(bt2.^-1)-1);

end