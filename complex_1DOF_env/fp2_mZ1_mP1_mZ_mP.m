function fp2_mZ1_mP1_mZ_mP=fp2_mZ1_mP1_mZ_mP(mP,mZ,mP1,mZ1,t1)

fp2_mZ1_mP1_mZ_mP=0;
for i=1:2
    for j=1:2
        fp2_mZ1_mP1_mZ_mP=fp2_mZ1_mP1_mZ_mP+((-1)^(i+j))*fp2_mZ1_mP1(mP(i,:),mZ(j,:),mP1,mZ1,t1);
    end
end

end