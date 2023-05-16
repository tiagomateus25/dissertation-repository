function [ob,at,bp,bz]=bpz(p,z,p1,z1)

b2=(p+p1).^2+(z-z1).^2;
a2=(p-p1).^2+(z-z1).^2;
k2=(4*p.*p1)./b2;
[K,E] = ellipke(k2);
ob=sqrt(b2).*((1-(k2/2)).*K-E);
at=ob./p;
bz=(1./sqrt(b2)).*((((p1.^2)-(p.^2)-((z-z1).^2))./a2).*E+K);
bp=((z-z1)./(p.*sqrt(b2))).*((((p1.^2)+(p.^2)+((z-z1).^2))./a2).*E-K);

end