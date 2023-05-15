function fp_mP1_mZ_mP=fp_mP1_mZ_mP(mP,mZ,mP1,z1)

fp_mP1_mZ_mP=0;
for i=1:2
    for j=1:2
        for k=1:2
            fp_mP1_mZ_mP=fp_mP1_mZ_mP+((-1)^(i+j+k))*fp(mP(i,:),mZ(j,:),mP1(k,:),z1);
        end
    end
end

end