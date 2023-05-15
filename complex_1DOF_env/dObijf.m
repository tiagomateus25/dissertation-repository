function dObij=dObijf(iP,iZ,mM,mP1,mZ11,mL,i,d,Ncoil,u0)

mZ11i=d+[-mL(i);mL(i)];
dObij=zeros(length(d),Ncoil);
for j=1:Ncoil
    fp_mZ1_mP1ij=fp_mZ1_mP1(iP{j},iZ{j},mP1(:,i),mZ11i);
    dObij(:,j)=((u0*mM(i))*sum(fp_mZ1_mP1ij,1)).'; % Magnetic flux change by magnet i on coil j
end

end