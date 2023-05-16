function bz1_mZ1_mP1=bz1_mZ1_mP1(p,z,mP1,mZ1,t1)

bz1_mZ1_mP1=0;
for i=1:2
    for j=1:2
        bt=sqrt((p.^2)+(mP1(i,:).^2)+2*p.*mP1(i,:).*cos(t1)+(z-mZ1(j,:)).^2);
        bz1_mZ1_mP1=bz1_mZ1_mP1+((-1)^(i+j))*mP1(i,:).*cos(t1).*((1./p).*log(abs(z-mZ1(j,:)+bt))+((p+mP1(i,:).*cos(t1))./(bt.*(z-mZ1(j,:)+bt))));
    end
end

end