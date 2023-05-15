function fp2=fp2(p,z,p1,z1,t1)

bt=sqrt((p.^2)+(p1.^2)+2*p.*p1.*cos(t1)+(z-z1).^2);
fp2=p.*p1.*cos(t1).*log(abs((z-z1)+bt));

end