function mFzi=mFzif(mM,mP1,mZ11,mL,i,J,d,AbsTol,RelTol,u0)

mZ11i=d+[-mL(i);mL(i)];
mFzi1=0;
for j=J  % magnet number\i 
        Intdt1_pf2_mZ1_mP1_mZ_mP=integral(@(t1) fp2_mZ1_mP1_mZ_mP(mP1(:,i),mZ11i,mP1(:,j),mZ11(:,j),t1),0,pi,"AbsTol",AbsTol,"RelTol",RelTol,'ArrayValued',true);
        mFzi1=mFzi1+mM(j)*Intdt1_pf2_mZ1_mP1_mZ_mP;       
end
mFzi=mM(i)*u0*mFzi1; % Lorentz force by magnets on magnet i 

end